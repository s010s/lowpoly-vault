import { CARD_RENDER_PRESET, cameraDirection } from './render-preset.js';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// Encoded bytes and decoded CPU/GPU resources have independent, bounded LRUs.
// Decoded sizes are estimates: unique geometry/animation buffers and texture
// storage (including mipmaps), not a claim to measure driver or JS heap memory.
export const MODEL_STAGE_LIMITS = Object.freeze({
  encodedEntries: 3, encodedBytes: 24 * 1024 * 1024,
  decodedEntries: 3, decodedBytes: 48 * 1024 * 1024, uncachedActiveEntries: 1,
});
const now = () => performance.now();

/** GLTFLoader parsing cannot be cancelled; tokens dispose its eventual stale result. */
function waitForPresentation(promise, signal) {
  if (signal.aborted) return Promise.reject(abortError());
  return new Promise((resolve, reject) => {
    const abort = () => { cleanup(); reject(abortError()); };
    const cleanup = () => signal.removeEventListener('abort', abort);
    signal.addEventListener('abort', abort, { once: true });
    Promise.resolve(promise).then(value => { cleanup(); resolve(value); }, error => { cleanup(); reject(error); });
  });
}

function collectResources(gltf) {
  const geometries = new Set(), materials = new Set(), textures = new Set(), skeletons = new Set();
  const buffers = new Set();
  const buffer = value => { if (value?.buffer) buffers.add(value.buffer); };
  for (const root of gltf.scenes || [gltf.scene]) root.traverse(object => {
    if (object.geometry) geometries.add(object.geometry);
    if (object.skeleton) skeletons.add(object.skeleton);
    for (const material of Array.isArray(object.material) ? object.material : [object.material]) {
      if (!material) continue;
      materials.add(material);
      for (const value of Object.values(material)) if (value?.isTexture) textures.add(value);
      for (const uniform of Object.values(material.uniforms || {})) {
        for (const value of Array.isArray(uniform.value) ? uniform.value : [uniform.value]) {
          if (value?.isTexture) textures.add(value);
        }
      }
    }
  });
  for (const geometry of geometries) {
    const attributes = [...Object.values(geometry.attributes), geometry.index,
      ...Object.values(geometry.morphAttributes).flat()];
    for (const attribute of attributes) buffer(attribute?.array || attribute?.data?.array);
  }
  for (const animation of gltf.animations || []) for (const track of animation.tracks) {
    buffer(track.times); buffer(track.values);
  }
  for (const skeleton of skeletons) {
    buffer(skeleton.boneMatrices);
    if (skeleton.boneTexture) textures.add(skeleton.boneTexture);
  }
  let textureBytes = 0;
  for (const texture of textures) {
    const images = texture.source?.data;
    for (const image of Array.isArray(images) ? images : [images]) {
      // Data/compressed textures expose their real storage. Ordinary image
      // textures are estimated as RGBA8 plus a full mip chain when requested.
      if (texture.isCompressedTexture && texture.mipmaps?.length) continue;
      const bytes = image?.data?.byteLength || (image?.width || 0) * (image?.height || 0) * (image?.depth || 1) * 4;
      textureBytes += Math.ceil(bytes * (texture.generateMipmaps ? 4 / 3 : 1));
    }
    if (texture.isCompressedTexture) for (const mip of texture.mipmaps || []) textureBytes += mip.data?.byteLength || 0;
  }
  const bufferBytes = [...buffers].reduce((total, item) => total + item.byteLength, 0);
  return { geometries, materials, textures, skeletons, bufferBytes, textureBytes, estimatedBytes: bufferBytes + textureBytes };
}
const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
const abortError = () => new DOMException('Model request cancelled', 'AbortError');
let sharedStage;

/** Validate authored meters before making a metric claim; never infer a conversion. */
export function metricReferenceSpec(size, metadata) {
  const dimensions = size.toArray();
  const longest = Math.max(...dimensions);
  if (metadata?.units !== 'meters' || !Array.isArray(metadata.dimensions) || metadata.dimensions.length !== 3) {
    return { available: false, reason: 'missing-metric-metadata' };
  }
  if ((metadata.axes?.glb_up && metadata.axes.glb_up !== '+Y') ||
    (metadata.blender_unit_scale !== undefined && metadata.blender_unit_scale !== 1)) {
    return { available: false, reason: 'unit-mismatch' };
  }
  if (!dimensions.every((value, axis) => Number.isFinite(value) && value >= 0 &&
    Number.isFinite(metadata.dimensions[axis]) && metadata.dimensions[axis] >= 0 &&
    Math.abs(value - metadata.dimensions[axis]) <= longest * 0.00001) || longest <= 0) {
    return { available: false, reason: 'bounds-mismatch' };
  }
  // A compact floor reference also works for a tall, narrow asset. Cell spacing
  // follows the decoded footprint, using readable 1 / 2 / 5 metric increments.
  const halfX = Math.max(size.x / 2, longest * 0.12) + longest * 0.025;
  const halfZ = Math.max(size.z / 2, longest * 0.12) + longest * 0.025;
  const desired = Math.max(halfX, halfZ) / 3;
  const magnitude = 10 ** Math.floor(Math.log10(desired));
  const spacingMeters = [1, 2, 5, 10].find(step => step * magnitude >= desired) * magnitude;
  if (!Number.isFinite(spacingMeters) || spacingMeters <= 0) return { available: false, reason: 'unsupported-scale' };
  return {
    available: true, reason: null, dimensionsMeters: dimensions,
    spacingMeters, halfX, halfZ, floorY: -size.y / 2 - longest * 0.002,
  };
}

/** One movable canvas, one attached model lease, and bounded decoded/byte LRUs. */
export class ModelStage {
  constructor({ onStatus } = {}) {
    // Repeated consumers still share the same context rather than creating one per card.
    if (sharedStage && !sharedStage._disposed) return sharedStage;
    sharedStage = this;
    this.onStatus = onStatus;
    this._disposed = false;
    this._token = 0;
    this._cache = new Map();
    this._resources = new Map();
    this._tail = Promise.resolve();
    this._raf = 0;
    this._inView = true;
    this._reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    this._diagnostics = {
      renderers: 0, rendererCount: 0, rendererCreations: 0,
      liveScenes: 0, cacheEntries: 0, cacheBytes: 0,
      cachedScenes: 0, cachedDecodedBytes: 0, decodedEntries: 0, decodedBytes: 0,
      decodedBufferBytes: 0, decodedTextureBytes: 0, decodedBytesEstimated: true,
      decodedEntryLimit: MODEL_STAGE_LIMITS.decodedEntries, decodedByteLimit: MODEL_STAGE_LIMITS.decodedBytes,
      activeLeases: 0, pendingLeases: 0, activeEstimatedBytes: 0, pendingEstimatedBytes: 0,
      uncachedActiveScenes: 0, resourceReferences: 0,
      geometries: 0, materials: 0, textures: 0, skeletons: 0,
      activeRequests: 0, peakRequests: 0, networkRequests: 0, networkBytes: 0,
      networkMilliseconds: 0, lastNetworkMilliseconds: 0, byteCacheHits: 0,
      parseCount: 0, activeParses: 0, peakParses: 0, parseMilliseconds: 0,
      decodedCacheHits: 0, resourceReuses: 0, evictedScenes: 0, staleScenes: 0,
      disposedScenes: 0, disposedGeometries: 0, disposedMaterials: 0, disposedTextures: 0,
      lastShowMilliseconds: 0, lastShowCacheHit: false,
      renderedFrames: 0, rafPending: 0, activeMode: null, activeURL: null,
      referenceObjects: 0, referenceGeometries: 0, referenceMaterials: 0, disposedReferences: 0,
      returnOverlayMeshes: 0, returnOverlayMaterials: 0,
    };
    window.__vaultGPU = this._diagnostics;
    this._onVisibility = () => {
      if (document.hidden) this._stopFrame();
      else this._invalidate();
    };
    // Motion preference changes must never snap an inspected model back to its
    // poster pose. Rendering is demand-only in both preference modes.
    this._onMotion = () => this._invalidate();
    this._onKey = (event) => this._key(event);
    document.addEventListener('visibilitychange', this._onVisibility);
    this._reducedMotion.addEventListener('change', this._onMotion);
  }

  get stats() { return { ...this._diagnostics }; }

  get canonicalView() {
    if (!this._pivot) return null;
    return { azimuth_deg: CARD_RENDER_PRESET.camera.azimuth_deg,
      elevation_deg: CARD_RENDER_PRESET.camera.elevation_deg, distance: this._distance };
  }

  /** Reparent the current lease for a finite return flight, without reload/reset. */
  moveTo(host, { mode = 'return', onStatus } = {}) {
    if (!host || !this._pivot || !this._renderer || this._contextLost || this._disposed) return false;
    ++this._token;
    this._externalSignal?.removeEventListener('abort', this._externalAbort);
    this._externalSignal = this._externalAbort = null;
    this._controller?.abort(); this._controller = null;
    this._stopFrame();
    this._resizeObserver?.disconnect(); this._intersectionObserver?.disconnect();
    const previous = this._host;
    if (previous) {
      previous.removeEventListener('keydown', this._onKey);
      for (const key of ['renderTriangles', 'renderLines', 'renderCalls', 'presentedUrl', 'viewAzimuth', 'viewElevation', 'viewDistance']) delete previous.dataset[key];
      if (this._addedTabIndex) previous.removeAttribute('tabindex');
      previous.dataset.modelState = 'idle';
    }
    this._host = host; this._mode = mode; this._statusCallback = onStatus; this._addedTabIndex = false;
    this._viewTouched = true; this._inView = true; this._controls.enabled = false;
    this._diagnostics.activeMode = mode;
    this._attach(host); this._resize(); this._draw();
    return true;
  }

  /** Inspection-only line/grid layers blend back to the solid poster preset. */
  beginCanonicalReturnStyles() {
    this.endCanonicalReturnStyles(this._returnStyles);
    const state = { overlays: [], materials: new Map(), clones: new Map(), reference: this._reference,
      referenceOpacity: this._reference?.material.opacity };
    this._returnStyles = state;
    if (this._wireframe) {
      const objects = [];
      this._gltf?.scene.traverse(object => { if (object.isMesh) objects.push(object); });
      const clone = material => {
        if (!material || !('wireframe' in material)) return material;
        if (!state.clones.has(material)) {
          state.materials.set(material, { opacity: material.opacity, transparent: material.transparent, depthWrite: material.depthWrite });
          const copy = material.clone(); copy.wireframe = true; copy.transparent = true;
          state.clones.set(material, copy);
          material.wireframe = false; material.transparent = true; material.depthWrite = false; material.opacity = 0; material.needsUpdate = true;
        }
        return state.clones.get(material);
      };
      for (const object of objects) {
        const materials = Array.isArray(object.material) ? object.material.map(clone) : clone(object.material);
        const overlay = object.isSkinnedMesh ? new THREE.SkinnedMesh(object.geometry, materials) : new THREE.Mesh(object.geometry, materials);
        if (object.isSkinnedMesh) { overlay.skeleton = object.skeleton; overlay.bindMatrix.copy(object.bindMatrix); overlay.bindMatrixInverse.copy(object.bindMatrixInverse); }
        overlay.name = 'canonical-return-wire-overlay'; overlay.raycast = () => {};
        object.add(overlay); state.overlays.push(overlay);
      }
    }
    this._diagnostics.returnOverlayMeshes = state.overlays.length;
    this._diagnostics.returnOverlayMaterials = state.clones.size;
    return state;
  }

  canonicalReturnStyleProgress(progress, state) {
    if (!state || state !== this._returnStyles) return;
    const t = clamp(progress, 0, 1);
    for (const [material, saved] of state.materials) {
      material.opacity = saved.opacity * t;
      state.clones.get(material).opacity = saved.opacity * (1 - t);
    }
    if (state.reference && this._reference === state.reference) state.reference.material.opacity = state.referenceOpacity * (1 - t);
    if (t === 1) this.endCanonicalReturnStyles(state);
  }

  endCanonicalReturnStyles(state) {
    if (!state || state !== this._returnStyles) return;
    this._returnStyles = null;
    for (const overlay of state.overlays) overlay.removeFromParent();
    for (const material of state.clones.values()) material.dispose();
    for (const [material, saved] of state.materials) {
      Object.assign(material, saved, { wireframe: false }); material.needsUpdate = true;
    }
    if (state.reference && this._reference === state.reference) this._disposeReference();
    this._wireframe = false;
    this._diagnostics.returnOverlayMeshes = this._diagnostics.returnOverlayMaterials = 0;
  }

  /** Measurements are from the decoded GLB before display-only normalization. */
  get scaleReferenceInfo() {
    return {
      available: this._mode === 'detail' && Boolean(this._metricReference?.available),
      enabled: Boolean(this._reference),
      spacingMeters: this._metricReference?.spacingMeters ?? null,
      dimensionsMeters: this._metricReference?.dimensionsMeters?.slice() ?? null,
      reason: this._metricReference?.reason ?? (this._metricReference ? null : 'not-loaded'),
    };
  }

  /** Resolves false for superseded/aborted work; actual loading errors reject. */
  show(host, url, { mode = 'hover', signal, onStatus, metadata, initialView, presentationReady } = {}) {
    if (this._disposed) return Promise.reject(new Error('ModelStage has been disposed'));
    if (!host || !url) return Promise.reject(new Error('A model host and URL are required'));
    const absoluteURL = new URL(url, document.baseURI).href;
    const held = this._activeResource || this._pendingResource;
    // Oversized assets are never cached. A direct same-URL handoff can still
    // transfer their single lease instead of decoding them a second time.
    const transferred = held?.url === absoluteURL && !held.cached ? held : null;
    if (transferred) transferred.leases++;
    this.hide();
    this._pendingResource = transferred;
    this._syncResources();
    const token = ++this._token;
    const controller = new AbortController();
    this._controller = controller;
    this._host = host;
    this._mode = mode === 'detail' ? 'detail' : 'hover';
    this._initialView = {
      azimuth_deg: Number.isFinite(initialView?.azimuth_deg) ? initialView.azimuth_deg : CARD_RENDER_PRESET.camera.azimuth_deg,
      elevation_deg: Number.isFinite(initialView?.elevation_deg) ? clamp(initialView.elevation_deg, -89.999, 89.999) : CARD_RENDER_PRESET.camera.elevation_deg,
      distance: Number.isFinite(initialView?.distance) && initialView.distance > 0 ? initialView.distance : undefined,
    };
    this._statusCallback = onStatus;
    this._url = absoluteURL;
    this._inView = true;
    this._viewTouched = false;
    this._wireframe = false;
    this._addedTabIndex = false;
    this._diagnostics.activeMode = this._mode;
    this._diagnostics.activeURL = this._url;
    const current = () => !this._disposed && token === this._token && !controller.signal.aborted;
    if (signal) {
      this._externalSignal = signal;
      this._externalAbort = () => { if (token === this._token) this.hide(); };
      signal.addEventListener('abort', this._externalAbort, { once: true });
      if (signal.aborted) { this.hide(); return Promise.resolve(false); }
    }
    this._emit('loading');
    const started = now();
    this._showStarted = started;
    // Serializing fetch and parse bounds in-flight decoding to one resource.
    // A stale parse is disposed before the next operation enters the queue.
    const operation = this._tail.catch(() => {}).then(async () => {
      if (!current()) return false;
      let entry;
      try {
        entry = this._pendingResource || this._resources.get(absoluteURL);
        const cacheHit = Boolean(entry);
        // New cache leases wait for the presentation gate. An oversized transfer
        // owns one cancellable pending lease, released by hide like an active one.
        const bytes = entry ? null : await this._bytes(absoluteURL, controller.signal);
        if (presentationReady) await waitForPresentation(presentationReady, controller.signal);
        if (!current()) return false;
        if (entry) {
          this._diagnostics.decodedCacheHits++;
          this._diagnostics.resourceReuses++;
          if (entry.cached) {
            this._resources.delete(absoluteURL);
            this._resources.set(absoluteURL, entry);
          }
        } else {
          const parseStarted = now();
          this._diagnostics.parseCount++;
          this._diagnostics.activeParses++;
          this._diagnostics.peakParses = Math.max(this._diagnostics.peakParses, this._diagnostics.activeParses);
          let gltf;
          try { gltf = await new GLTFLoader().parseAsync(bytes, new URL('.', absoluteURL).href); }
          catch (error) {
            // A successful HTTP response can still contain a transient error
            // page or corrupt bytes. An explicit retry must get fresh bytes.
            this._forgetBytes(absoluteURL);
            throw error;
          }
          finally {
            this._diagnostics.activeParses--;
            this._diagnostics.parseMilliseconds += now() - parseStarted;
          }
          if (!current()) {
            this._diagnostics.staleScenes++;
            this._disposeGLTF(gltf);
            return false;
          }
          try { entry = this._resource(absoluteURL, gltf); }
          catch (error) { this._forgetBytes(absoluteURL); throw error; }
        }
        // The stage owns one lease; the LRU independently owns a cache reference.
        // Eviction can drop only unleased entries, never attached detail geometry.
        if (this._pendingResource === entry) this._pendingResource = null;
        else entry.leases++;
        this._activeResource = entry;
        this._gltf = entry.gltf;
        this._retainResource(entry);
        this._syncResources();
        this._ensureRenderer();
        this._attach(host);
        this._pivot = new THREE.Group();
        // Center with a display-only parent. Never mutate the retained GLTF root,
        // so repeated acquire/release cannot accumulate centering transforms.
        this._centered = new THREE.Group();
        this._centered.position.copy(entry.center).negate();
        this._centered.add(entry.gltf.scene);
        this._pivot.add(this._centered);
        this._scene.add(this._pivot);
        this._diagnostics.liveScenes = 1;
        const size = entry.size;
        this._metricReference = metricReferenceSpec(size, metadata);
        entry.gltf.scene.traverse((object) => {
          if (object.userData.units && object.userData.units !== 'meters') {
            this._metricReference = { available: false, reason: 'unit-mismatch' };
          }
        });
        const scale = 2 / Math.max(size.x, size.y, size.z, 0.00001);
        this._pivot.scale.setScalar(scale);
        this._radius = Math.max(size.length() * scale / 2, 0.1);
        this._controls.enabled = this._mode === 'detail';
        this._controls.minDistance = this._radius * 1.1;
        this._controls.maxDistance = this._radius * 20;
        this._resize();
        this.reset();
        this._diagnostics.lastShowCacheHit = cacheHit;
        // Publish ready only after a successful draw; hidden tabs keep fallback.
        this._draw();
        return true;
      } catch (error) {
        if (!current() || error?.name === 'AbortError') return false;
        this._disposeModel();
        this._stopFrame();
        if (this._renderer) this._renderer.domElement.style.visibility = 'hidden';
        this._emit('error', error);
        throw error;
      }
    });
    this._tail = operation.catch(() => {});
    return operation;
  }

  _resource(url, gltf) {
    const resources = collectResources(gltf);
    try {
      const bounds = new THREE.Box3().setFromObject(gltf.scene);
      const size = bounds.getSize(new THREE.Vector3());
      if (bounds.isEmpty() || !Number.isFinite(size.length())) throw new Error('Model has no visible geometry');
      // No animations or post-load dependency resolution are used by this viewer.
      // Release the loader dependency cache, which otherwise retains GLB buffers.
      gltf.parser?.cache?.removeAll();
      gltf.parser = null;
      return { url, gltf, resources, size, center: bounds.getCenter(new THREE.Vector3()),
        leases: 0, cached: false, disposed: false,
        wireframes: new Map([...resources.materials].filter(material => 'wireframe' in material).map(material => [material, material.wireframe])) };
    } catch (error) { this._disposeGLTF(gltf, resources); throw error; }
  }

  _retainResource(entry) {
    if (entry.cached || entry.resources.estimatedBytes > MODEL_STAGE_LIMITS.decodedBytes) return;
    const bytes = () => [...this._resources.values()].reduce((sum, item) => sum + item.resources.estimatedBytes, 0);
    while (this._resources.size >= MODEL_STAGE_LIMITS.decodedEntries || bytes() + entry.resources.estimatedBytes > MODEL_STAGE_LIMITS.decodedBytes) {
      const oldest = [...this._resources.values()].find(item => item.leases === 0);
      if (!oldest) return; // An active lease is never a candidate for eviction.
      this._resources.delete(oldest.url);
      oldest.cached = false;
      this._diagnostics.evictedScenes++;
      this._disposeResource(oldest);
    }
    entry.cached = true;
    this._resources.set(entry.url, entry);
  }

  _disposeResource(entry) {
    if (entry.disposed || entry.leases || entry.cached) return;
    entry.disposed = true;
    this._disposeGLTF(entry.gltf, entry.resources);
  }

  _syncResources() {
    const cached = [...this._resources.values()];
    const all = new Set(cached);
    if (this._activeResource) all.add(this._activeResource);
    if (this._pendingResource) all.add(this._pendingResource);
    const stats = this._diagnostics;
    stats.cachedScenes = cached.length;
    stats.cachedDecodedBytes = cached.reduce((sum, entry) => sum + entry.resources.estimatedBytes, 0);
    stats.decodedEntries = all.size;
    stats.decodedBytes = stats.decodedBufferBytes = stats.decodedTextureBytes = 0;
    stats.geometries = stats.materials = stats.textures = stats.skeletons = stats.resourceReferences = 0;
    for (const entry of all) {
      const resources = entry.resources;
      stats.decodedBytes += resources.estimatedBytes;
      stats.decodedBufferBytes += resources.bufferBytes;
      stats.decodedTextureBytes += resources.textureBytes;
      stats.resourceReferences += entry.leases + Number(entry.cached);
      for (const key of ['geometries', 'materials', 'textures', 'skeletons']) stats[key] += resources[key].size;
    }
    stats.activeLeases = this._activeResource?.leases || 0;
    stats.pendingLeases = this._pendingResource?.leases || 0;
    stats.activeEstimatedBytes = this._activeResource?.resources.estimatedBytes || 0;
    stats.pendingEstimatedBytes = this._pendingResource?.resources.estimatedBytes || 0;
    stats.uncachedActiveScenes = [...all].filter(entry => !entry.cached).length;
  }

  async _bytes(url, signal) {
    if (signal.aborted) throw abortError();
    const cached = this._cache.get(url);
    if (cached) {
      this._cache.delete(url);
      this._cache.set(url, cached);
      this._diagnostics.byteCacheHits++;
      return cached;
    }
    const started = now();
    this._diagnostics.networkRequests++;
    this._diagnostics.activeRequests++;
    this._diagnostics.peakRequests = Math.max(this._diagnostics.peakRequests, this._diagnostics.activeRequests);
    try {
      const response = await fetch(url, { signal });
      if (!response.ok) throw new Error(`Unable to load model (${response.status})`);
      const bytes = await response.arrayBuffer();
      if (signal.aborted) throw abortError();
      this._diagnostics.networkBytes += bytes.byteLength;
      if (bytes.byteLength <= MODEL_STAGE_LIMITS.encodedBytes) {
        while (this._cache.size >= MODEL_STAGE_LIMITS.encodedEntries || this._diagnostics.cacheBytes + bytes.byteLength > MODEL_STAGE_LIMITS.encodedBytes) {
          const oldest = this._cache.keys().next().value;
          const entry = this._cache.get(oldest);
          this._cache.delete(oldest);
          this._diagnostics.cacheBytes -= entry.byteLength;
        }
        this._cache.set(url, bytes);
        this._diagnostics.cacheBytes += bytes.byteLength;
        this._diagnostics.cacheEntries = this._cache.size;
      }
      return bytes;
    } finally {
      this._diagnostics.activeRequests--;
      this._diagnostics.lastNetworkMilliseconds = now() - started;
      this._diagnostics.networkMilliseconds += this._diagnostics.lastNetworkMilliseconds;
    }
  }

  _forgetBytes(url) {
    const bytes = this._cache.get(url);
    if (!bytes) return;
    this._cache.delete(url);
    this._diagnostics.cacheBytes -= bytes.byteLength;
    this._diagnostics.cacheEntries = this._cache.size;
  }

  _ensureRenderer() {
    if (this._renderer) return;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' });
    this._renderer = renderer;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setClearColor(CARD_RENDER_PRESET.background, 0);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = CARD_RENDER_PRESET.exposure;
    renderer.domElement.className = 'model-canvas';
    renderer.domElement.setAttribute('aria-hidden', 'true');
    Object.assign(renderer.domElement.style, {
      position: 'absolute', inset: '0', display: 'block', width: '100%', height: '100%', visibility: 'hidden',
    });
    this._scene = new THREE.Scene();
    this._camera = new THREE.PerspectiveCamera(CARD_RENDER_PRESET.camera.fov, 1, 0.01, 1000);
    const hemi = CARD_RENDER_PRESET.hemisphere;
    this._scene.add(new THREE.HemisphereLight(hemi.sky, hemi.ground, hemi.intensity));
    for (const spec of CARD_RENDER_PRESET.lights) {
      const light = new THREE.DirectionalLight(spec.color, spec.intensity);
      light.position.set(...spec.position); this._scene.add(light);
    }
    this._controls = new OrbitControls(this._camera, renderer.domElement);
    this._controls.enableDamping = false;
    this._controls.enablePan = false;
    this._controls.autoRotate = false;
    this._controls.addEventListener('change', () => this._invalidate());
    this._controls.addEventListener('start', () => { this._viewTouched = true; });
    this._onContextLost = (event) => {
      event.preventDefault();
      this._contextLost = true;
      this._stopFrame();
      renderer.domElement.style.visibility = 'hidden';
      if (this._host) this._emit('error', new Error('3D view interrupted. The image preview is still available.'));
    };
    this._onContextRestored = () => { this._contextLost = false; this._invalidate(); };
    renderer.domElement.addEventListener('webglcontextlost', this._onContextLost);
    renderer.domElement.addEventListener('webglcontextrestored', this._onContextRestored);
    this._diagnostics.renderers = this._diagnostics.rendererCount = 1;
    this._diagnostics.rendererCreations++;
  }

  _attach(host) {
    const canvas = this._renderer.domElement;
    canvas.style.visibility = 'hidden';
    canvas.style.pointerEvents = this._mode === 'detail' ? 'auto' : 'none';
    host.append(canvas);
    if (this._mode === 'detail') {
      this._addedTabIndex = !host.hasAttribute('tabindex');
      if (this._addedTabIndex) host.tabIndex = 0;
      host.addEventListener('keydown', this._onKey);
    }
    this._resizeObserver = new ResizeObserver(() => this._resize());
    this._resizeObserver.observe(host);
    if ('IntersectionObserver' in window) {
      this._intersectionObserver = new IntersectionObserver(([entry]) => {
        if (this._host !== host) return;
        this._inView = entry.isIntersecting;
        if (this._inView) this._invalidate();
        else this._stopFrame();
      });
      this._intersectionObserver.observe(host);
    }
  }

  _resize() {
    if (!this._host || !this._renderer) return;
    const width = Math.round(this._host.clientWidth);
    const height = Math.round(this._host.clientHeight);
    if (!width || !height) { this._stopFrame(); return; }
    this._renderer.setSize(width, height, false);
    this._camera.aspect = width / height;
    const halfFov = THREE.MathUtils.degToRad(CARD_RENDER_PRESET.camera.fov / 2);
    this._camera.fov = THREE.MathUtils.radToDeg(2 * Math.atan(Math.tan(halfFov) / Math.min(1, this._camera.aspect)));
    this._camera.updateProjectionMatrix();
    if (this._radius) {
      // Preserve the same perspective and object scale inside a centered square
      // at every modal aspect ratio; only the surrounding neutral margin changes.
      this._distance = this._radius / Math.sin(halfFov) * CARD_RENDER_PRESET.camera.fit_padding;
      this._camera.near = Math.max(this._radius / 100, 0.001);
      this._camera.far = Math.max(this._radius * 100, this._distance * 10);
      this._camera.updateProjectionMatrix();
      if (!this._viewTouched) this.reset();
    }
    this._invalidate();
  }

  _canDraw() {
    return !this._disposed && !this._contextLost && !!this._pivot && !!this._host?.isConnected &&
      !document.hidden && this._inView && this._host.clientWidth > 0 && this._host.clientHeight > 0;
  }

  _draw() {
    if (!this._canDraw()) return;
    if (this._reference) {
      // Detail mode orbits the camera, not the model. From below the floor, omit
      // the grid so it cannot draw in front of and obscure the asset silhouette.
      this._reference.visible = this._camera.position.y >= this._metricReference.floorY * this._pivot.scale.y;
    }
    this._renderer.render(this._scene, this._camera);
    if (this._showStarted !== null && this._showStarted !== undefined) {
      this._diagnostics.lastShowMilliseconds = now() - this._showStarted;
      this._showStarted = null;
    }
    globalThis.__vaultFrameProbe?.({canvas:this._renderer.domElement,host:this._host,view:this.presentationInfo});
    this._diagnostics.renderedFrames++;
    this._host.dataset.renderTriangles = String(this._renderer.info.render.triangles);
    this._host.dataset.renderLines = String(this._renderer.info.render.lines);
    this._host.dataset.renderCalls = String(this._renderer.info.render.calls);
    const view = this.presentationInfo;
    this._host.dataset.viewAzimuth = String(view.azimuth_deg);
    this._host.dataset.viewElevation = String(view.elevation_deg);
    this._host.dataset.viewDistance = String(view.distance);
    this._host.dataset.presentedUrl = this._url;
    this._renderer.domElement.style.visibility = 'visible';
    if (this._host.dataset.modelState !== 'ready') this._emit('ready');
  }

  _invalidate() {
    if (this._raf || !this._canDraw()) return;
    this._raf = requestAnimationFrame(() => {
      this._raf = 0;
      this._diagnostics.rafPending = 0;
      if (!this._canDraw()) return;
      this._draw();
    });
    this._diagnostics.rafPending = 1;
  }

  _stopFrame() {
    if (this._raf) cancelAnimationFrame(this._raf);
    this._raf = 0;
    this._diagnostics.rafPending = 0;
  }

  /** Legacy pointer convenience; all inspection rotates the camera, never the model. */
  pointer(x, y) {
    if (this._mode !== 'hover' || !Number.isFinite(x) || !Number.isFinite(y)) return;
    const view = this._initialView || CARD_RENDER_PRESET.camera;
    this.setView((view.azimuth_deg ?? CARD_RENDER_PRESET.camera.azimuth_deg) + clamp(x, -1, 1) * 16,
      (view.elevation_deg ?? CARD_RENDER_PRESET.camera.elevation_deg) - clamp(y, -1, 1) * 7.5);
  }

  reset() {
    if (!this._camera || !this._pivot) return;
    this._viewTouched = false;
    this._pivot.rotation.set(0, 0, 0);
    const distance = Number.isFinite(this._initialView?.distance)
      ? clamp(this._initialView.distance, this._controls.minDistance, this._controls.maxDistance) : this._distance || 5;
    this._camera.position.set(...cameraDirection(this._initialView?.azimuth_deg, this._initialView?.elevation_deg)).multiplyScalar(distance);
    this._controls.target.set(0, 0, 0);
    this._controls.update();
    this._invalidate();
  }

  get presentationInfo() {
    if (!this._camera || !this._pivot) return null;
    const p = this._camera.position.clone().sub(this._controls.target), radius = p.length();
    return { azimuth_deg:(THREE.MathUtils.radToDeg(Math.atan2(p.x,p.z))+360)%360,
      elevation_deg:THREE.MathUtils.radToDeg(Math.asin(p.y/radius)), distance:radius,
      fov:this._camera.fov, aspect:this._camera.aspect, preset:CARD_RENDER_PRESET.version };
  }

  /** Use the actual orbit and distance for list/detail handoffs, with no autoplay. */
  setView(azimuth_deg, elevation_deg = CARD_RENDER_PRESET.camera.elevation_deg, distance) {
    if (!this._camera || !this._pivot || !Number.isFinite(azimuth_deg) || !Number.isFinite(elevation_deg)) return;
    this._viewTouched = true;
    const currentDistance = this._camera.position.distanceTo(this._controls.target);
    const requested = Number.isFinite(distance) && distance > 0 ? distance : currentDistance || this._distance || 5;
    this._camera.position.set(...cameraDirection(azimuth_deg, clamp(elevation_deg, -89.999, 89.999)))
      .multiplyScalar(clamp(requested, this._controls.minDistance, this._controls.maxDistance));
    this._controls.target.set(0, 0, 0);
    this._controls.update();
    // Offline capture also uses setView followed by toDataURL in the same task.
    // Paint synchronously and consume the controls' queued invalidation once.
    this._stopFrame();
    this._draw();
  }

  /** Copy the actual draw before releasing its lease; never create a second scene. */
  snapshot({ square = false } = {}) {
    if (!this._renderer || !this._canDraw() || this._host?.dataset.modelState !== 'ready') return null;
    this._draw();
    const source = this._renderer.domElement, canvas = document.createElement('canvas');
    const side = Math.min(source.width, source.height);
    const width = square ? side : source.width, height = square ? side : source.height;
    const scale = Math.min(1, 1024 / Math.max(width, height));
    canvas.width = Math.round(width * scale); canvas.height = Math.round(height * scale);
    const context = canvas.getContext('2d');
    if (!context) return null;
    context.drawImage(source, square ? (source.width - side) / 2 : 0,
      square ? (source.height - side) / 2 : 0, width, height, 0, 0, canvas.width, canvas.height);
    canvas.__presentation = this.presentationInfo;
    canvas.dataset.assetId = new URL(this._url).pathname.split('/').at(-1).replace(/\.glb$/, '');
    canvas.className = 'model-handoff'; canvas.setAttribute('aria-hidden', 'true');
    return canvas;
  }

  zoom(factor) {
    if (!this._pivot || !Number.isFinite(factor) || factor <= 0) return;
    this._viewTouched = true;
    const offset = this._camera.position.clone().sub(this._controls.target);
    const distance = clamp(offset.length() * factor, this._controls.minDistance, this._controls.maxDistance);
    this._camera.position.copy(offset.setLength(distance).add(this._controls.target));
    this._controls.update();
    this._invalidate();
  }

  wireframe(enabled) {
    this._wireframe = Boolean(enabled);
    this._gltf?.scene.traverse((object) => {
      for (const material of Array.isArray(object.material) ? object.material : [object.material]) {
        if (material && 'wireframe' in material) material.wireframe = this._wireframe;
      }
    });
    this._invalidate();
    return this._wireframe;
  }

  /** One optional draw call, no textures, picking targets, camera changes or loop. */
  scaleReference(enabled) {
    const show = Boolean(enabled) && this.scaleReferenceInfo.available && !!this._pivot;
    if (show === Boolean(this._reference)) return show;
    if (!show) this._disposeReference();
    else {
      const { halfX, halfZ, floorY, spacingMeters } = this._metricReference;
      const positions = [], colors = [];
      const centerColor = new THREE.Color(0x607c70), gridColor = new THREE.Color(0x82988b);
      const line = (x1, z1, x2, z2, center) => {
        positions.push(x1, floorY, z1, x2, floorY, z2);
        const color = center ? centerColor : gridColor;
        colors.push(color.r, color.g, color.b, color.r, color.g, color.b);
      };
      const columns = Math.floor(halfX / spacingMeters), rows = Math.floor(halfZ / spacingMeters);
      for (let i = -columns; i <= columns; i++) line(i * spacingMeters, -halfZ, i * spacingMeters, halfZ, i === 0);
      for (let i = -rows; i <= rows; i++) line(-halfX, i * spacingMeters, halfX, i * spacingMeters, i === 0);
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
      geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
      const material = new THREE.LineBasicMaterial({
        vertexColors: true, transparent: true, opacity: 0.55, depthTest: true, depthWrite: false, toneMapped: false,
      });
      const reference = this._reference = new THREE.LineSegments(geometry, material);
      reference.name = 'metric-floor-reference';
      reference.raycast = () => {};
      // The model has already been centered. Sharing its display-only parent scale
      // makes a one-meter cell exactly one authored meter at every fitted size.
      this._pivot.add(reference);
      this._diagnostics.referenceObjects = this._diagnostics.referenceGeometries = this._diagnostics.referenceMaterials = 1;
    }
    this._invalidate();
    return show;
  }

  _key(event) {
    if (this._mode !== 'detail' || !this._pivot || event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.target instanceof Element && event.target.closest('button,input,select,textarea,a')) return;
    const key = event.key;
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', '+', '=', '-', '_', 'Home'].includes(key)) return;
    event.preventDefault();
    if (key === 'Home') { this.reset(); return; }
    if (['+', '=', '-', '_'].includes(key)) { this.zoom(key === '-' || key === '_' ? 1.15 : 1 / 1.15); return; }
    this._viewTouched = true;
    const spherical = new THREE.Spherical().setFromVector3(this._camera.position.clone().sub(this._controls.target));
    if (key === 'ArrowLeft') spherical.theta -= 0.12;
    if (key === 'ArrowRight') spherical.theta += 0.12;
    if (key === 'ArrowUp') spherical.phi -= 0.12;
    if (key === 'ArrowDown') spherical.phi += 0.12;
    spherical.makeSafe();
    this._camera.position.copy(new THREE.Vector3().setFromSpherical(spherical).add(this._controls.target));
    this._controls.update();
    this._invalidate();
  }

  _emit(status, error) {
    const detail = { host: this._host, url: this._url, mode: this._mode, error, stats: this.stats, scaleReference: this.scaleReferenceInfo };
    if (this._host) this._host.dataset.modelState = status;
    // UI callbacks must not prevent resource cleanup or poison the serialized queue.
    for (const callback of new Set([this.onStatus, this._statusCallback])) {
      if (typeof callback === 'function') {
        try { callback(status, detail); } catch (callbackError) { console.error(callbackError); }
      }
    }
  }

  _disposeGLTF(gltf, resources = collectResources(gltf)) {
    const { geometries, materials, textures, skeletons } = resources, images = new Set();
    for (const root of gltf.scenes || [gltf.scene]) root.removeFromParent();
    for (const geometry of geometries) geometry.dispose();
    for (const material of materials) material.dispose();
    for (const texture of textures) {
      const data = texture.source?.data;
      for (const image of Array.isArray(data) ? data : [data]) if (image?.close) images.add(image);
      texture.dispose();
    }
    for (const skeleton of skeletons) {
      // A bone texture already belongs to the deduplicated texture set.
      if (textures.has(skeleton.boneTexture)) skeleton.boneTexture = null;
      skeleton.dispose();
    }
    for (const image of images) image.close();
    gltf.parser?.cache?.removeAll();
    gltf.parser = null;
    this._diagnostics.disposedScenes++;
    this._diagnostics.disposedGeometries += geometries.size;
    this._diagnostics.disposedMaterials += materials.size;
    this._diagnostics.disposedTextures += textures.size;
  }

  _disposeModel() {
    this.endCanonicalReturnStyles(this._returnStyles);
    this._disposeReference();
    this._metricReference = null;
    this._pivot?.removeFromParent();
    this._gltf?.scene.removeFromParent();
    const held = new Set([this._activeResource, this._pendingResource].filter(Boolean));
    this._activeResource = this._pendingResource = null;
    for (const entry of held) {
      for (const [material, wireframe] of entry.wireframes) material.wireframe = wireframe;
      entry.leases--;
      this._disposeResource(entry);
    }
    this._gltf = this._pivot = this._centered = null;
    this._radius = this._distance = null;
    this._diagnostics.liveScenes = 0;
    this._syncResources();
    this._renderer?.renderLists.dispose();
  }

  _disposeReference() {
    if (!this._reference) return;
    this._reference.removeFromParent();
    this._reference.geometry.dispose();
    this._reference.material.dispose();
    this._reference = null;
    this._diagnostics.referenceObjects = this._diagnostics.referenceGeometries = this._diagnostics.referenceMaterials = 0;
    this._diagnostics.disposedReferences++;
  }

  hide() {
    ++this._token;
    this._showStarted = null;
    this._controller?.abort();
    this._controller = null;
    this._externalSignal?.removeEventListener('abort', this._externalAbort);
    this._externalSignal = this._externalAbort = null;
    this._stopFrame();
    this._resizeObserver?.disconnect();
    this._intersectionObserver?.disconnect();
    this._resizeObserver = this._intersectionObserver = null;
    this._disposeModel();
    if (this._controls) this._controls.enabled = false;
    if (this._renderer) {
      this._renderer.domElement.style.visibility = 'hidden';
      if (!this._contextLost) this._renderer.clear?.();
      this._renderer.domElement.remove();
    }
    if (this._host) {
      this._host.removeEventListener('keydown', this._onKey);
      delete this._host.dataset.renderTriangles;
      delete this._host.dataset.renderLines;
      delete this._host.dataset.renderCalls;
      delete this._host.dataset.presentedUrl;
      delete this._host.dataset.viewAzimuth;
      delete this._host.dataset.viewElevation;
      delete this._host.dataset.viewDistance;
      if (this._addedTabIndex) this._host.removeAttribute('tabindex');
      this._emit('idle');
    }
    this._host = null;
    this._statusCallback = null;
    this._url = null;
    this._diagnostics.activeMode = this._diagnostics.activeURL = null;
  }

  dispose() {
    if (this._disposed) return;
    this.hide();
    this._disposed = true;
    document.removeEventListener('visibilitychange', this._onVisibility);
    this._reducedMotion.removeEventListener('change', this._onMotion);
    this._controls?.dispose();
    if (this._renderer) {
      const canvas = this._renderer.domElement;
      canvas.removeEventListener('webglcontextlost', this._onContextLost);
      canvas.removeEventListener('webglcontextrestored', this._onContextRestored);
      this._renderer.dispose();
      this._renderer.forceContextLoss();
      this._renderer = null;
    }
    for (const entry of this._resources.values()) {
      entry.cached = false;
      this._disposeResource(entry);
    }
    this._resources.clear();
    this._scene = this._camera = this._controls = null;
    this._onContextLost = this._onContextRestored = null;
    this._syncResources();
    this._cache.clear();
    this._diagnostics.cacheEntries = this._diagnostics.cacheBytes = 0;
    this._diagnostics.renderers = this._diagnostics.rendererCount = 0;
    if (sharedStage === this) sharedStage = null;
  }
}

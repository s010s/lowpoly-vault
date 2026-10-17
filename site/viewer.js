import { CARD_RENDER_PRESET, cameraDirection } from './render-preset.js';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const CACHE_LIMIT = 3;
const CACHE_BYTES = 24 * 1024 * 1024;
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

/** One movable canvas, one live model and a small LRU of original GLB bytes. */
export class ModelStage {
  constructor({ onStatus } = {}) {
    // Repeated consumers still share the same context rather than creating one per card.
    if (sharedStage && !sharedStage._disposed) return sharedStage;
    sharedStage = this;
    this.onStatus = onStatus;
    this._disposed = false;
    this._token = 0;
    this._cache = new Map();
    this._tail = Promise.resolve();
    this._raf = 0;
    this._inView = true;
    this._target = new THREE.Vector2();
    this._reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    this._diagnostics = {
      renderers: 0, rendererCount: 0, rendererCreations: 0,
      liveScenes: 0, cacheEntries: 0, cacheBytes: 0,
      activeRequests: 0, peakRequests: 0, disposedScenes: 0,
      renderedFrames: 0, rafPending: 0, activeMode: null, activeURL: null,
      referenceObjects: 0, referenceGeometries: 0, referenceMaterials: 0, disposedReferences: 0,
    };
    window.__vaultGPU = this._diagnostics;
    this._onVisibility = () => {
      if (document.hidden) this._stopFrame();
      else this._invalidate();
    };
    this._onMotion = () => {
      if (this._reducedMotion.matches) {
        this._target.set(0, 0);
        this._pivot?.rotation.set(0, 0, 0);
      }
      this._invalidate();
    };
    this._onKey = (event) => this._key(event);
    document.addEventListener('visibilitychange', this._onVisibility);
    this._reducedMotion.addEventListener('change', this._onMotion);
  }

  get stats() { return { ...this._diagnostics }; }

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
  show(host, url, { mode = 'hover', signal, onStatus, metadata, initialView } = {}) {
    if (this._disposed) return Promise.reject(new Error('ModelStage has been disposed'));
    if (!host || !url) return Promise.reject(new Error('A model host and URL are required'));
    this.hide();
    const token = ++this._token;
    const controller = new AbortController();
    this._controller = controller;
    this._host = host;
    this._mode = mode === 'detail' ? 'detail' : 'hover';
    this._initialView = initialView || CARD_RENDER_PRESET.camera;
    this._statusCallback = onStatus;
    this._url = new URL(url, document.baseURI).href;
    this._inView = true;
    this._viewTouched = false;
    this._wireframe = false;
    this._addedTabIndex = false;
    this._target.set(0, 0);
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
    const absoluteURL = this._url;
    // Serializing parsing as well as fetch means stale decoded scenes never overlap
    // a newer model. Aborted fetches settle before the next request can start.
    const operation = this._tail.catch(() => {}).then(async () => {
      if (!current()) return false;
      try {
        const bytes = await this._bytes(absoluteURL, controller.signal);
        if (!current()) return false;
        const gltf = await new GLTFLoader().parseAsync(bytes, new URL('.', absoluteURL).href);
        this._diagnostics.liveScenes++;
        if (!current()) { this._disposeGLTF(gltf); return false; }
        this._gltf = gltf;
        this._ensureRenderer();
        this._attach(host);
        this._pivot = new THREE.Group();
        this._pivot.add(gltf.scene);
        this._scene.add(this._pivot);
        const bounds = new THREE.Box3().setFromObject(gltf.scene);
        const size = bounds.getSize(new THREE.Vector3());
        const center = bounds.getCenter(new THREE.Vector3());
        if (bounds.isEmpty() || !Number.isFinite(size.length())) throw new Error('Model has no visible geometry');
        this._metricReference = metricReferenceSpec(size, metadata);
        // Exported unit extras provide an additional consistency check when present.
        gltf.scene.traverse((object) => {
          if (object.userData.units && object.userData.units !== 'meters') {
            this._metricReference = { available: false, reason: 'unit-mismatch' };
          }
        });
        gltf.scene.position.sub(center);
        const scale = 2 / Math.max(size.x, size.y, size.z, 0.00001);
        this._pivot.scale.setScalar(scale);
        this._radius = Math.max(size.length() * scale / 2, 0.1);
        this._controls.enabled = this._mode === 'detail';
        this._controls.minDistance = this._radius * 1.1;
        this._controls.maxDistance = this._radius * 20;
        this._resize();
        this.reset();
        // Publish ready only after a successful draw; a hidden tab keeps its fallback.
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

  async _bytes(url, signal) {
    if (signal.aborted) throw abortError();
    const cached = this._cache.get(url);
    if (cached) {
      this._cache.delete(url);
      this._cache.set(url, cached);
      return cached;
    }
    this._diagnostics.activeRequests++;
    this._diagnostics.peakRequests = Math.max(this._diagnostics.peakRequests, this._diagnostics.activeRequests);
    try {
      const response = await fetch(url, { signal });
      if (!response.ok) throw new Error(`Unable to load model (${response.status})`);
      const bytes = await response.arrayBuffer();
      if (signal.aborted) throw abortError();
      if (bytes.byteLength <= CACHE_BYTES) {
        while (this._cache.size >= CACHE_LIMIT || this._diagnostics.cacheBytes + bytes.byteLength > CACHE_BYTES) {
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
    }
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
      let moving = false;
      if (this._mode === 'hover' && !this._reducedMotion.matches) {
        const dx = this._target.x - this._pivot.rotation.x;
        const dy = this._target.y - this._pivot.rotation.y;
        moving = Math.abs(dx) + Math.abs(dy) > 0.0005;
        this._pivot.rotation.x += moving ? dx * 0.2 : dx;
        this._pivot.rotation.y += moving ? dy * 0.2 : dy;
      }
      this._draw();
      if (moving) this._invalidate();
    });
    this._diagnostics.rafPending = 1;
  }

  _stopFrame() {
    if (this._raf) cancelAnimationFrame(this._raf);
    this._raf = 0;
    this._diagnostics.rafPending = 0;
  }

  /** Pointer coordinates relative to the host, normalized to [-1, 1]. */
  pointer(x, y) {
    if (this._mode !== 'hover' || this._reducedMotion.matches) return;
    if (!Number.isFinite(x) || !Number.isFinite(y)) return;
    this._target.set(clamp(y, -1, 1) * 0.13, clamp(x, -1, 1) * 0.28);
    this._invalidate();
  }

  reset() {
    if (!this._camera || !this._pivot) return;
    this._viewTouched = false;
    this._target.set(0, 0);
    this._pivot.rotation.set(0, 0, 0);
    this._camera.position.set(...cameraDirection(this._initialView?.azimuth_deg, this._initialView?.elevation_deg)).multiplyScalar(Number.isFinite(this._initialView?.distance)?clamp(this._initialView.distance,this._controls.minDistance,this._controls.maxDistance):(this._distance || 5));
    this._controls.target.set(0, 0, 0);
    this._controls.update();
    this._invalidate();
  }

  get presentationInfo() {
    if (!this._camera) return null;
    const p = this._camera.position.clone().sub(this._controls.target), radius = p.length();
    return { azimuth_deg:(THREE.MathUtils.radToDeg(Math.atan2(p.x,p.z))+360)%360,
      elevation_deg:THREE.MathUtils.radToDeg(Math.asin(p.y/radius)), distance:radius,
      fov:this._camera.fov, aspect:this._camera.aspect, preset:CARD_RENDER_PRESET.version };
  }

  /** The offline card renderer and card-to-detail handoff use the same camera angles. */
  setView(azimuth_deg, elevation_deg = CARD_RENDER_PRESET.camera.elevation_deg) {
    if (!this._camera || !this._pivot) return;
    this._viewTouched = true;
    this._camera.position.set(...cameraDirection(azimuth_deg, elevation_deg)).multiplyScalar(this._distance || 5);
    this._controls.target.set(0, 0, 0); this._controls.update(); this._draw();
  }

  /** Copy the last actual draw before releasing GPU geometry; no second live scene. */
  snapshot() {
    if (!this._renderer || !this._pivot || this._host?.dataset.modelState !== 'ready') return null;
    this._draw();
    const source = this._renderer.domElement, canvas = document.createElement('canvas');
    const scale = Math.min(1, 1024 / Math.max(source.width, source.height));
    canvas.width = Math.round(source.width * scale); canvas.height = Math.round(source.height * scale);
    canvas.getContext('2d').drawImage(source, 0, 0, canvas.width, canvas.height);
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

  _disposeGLTF(gltf) {
    const geometries = new Set(), materials = new Set(), textures = new Set(), skeletons = new Set(), images = new Set();
    for (const root of gltf.scenes || [gltf.scene]) root.traverse((object) => {
      if (object.geometry) geometries.add(object.geometry);
      if (object.skeleton) skeletons.add(object.skeleton);
      for (const material of Array.isArray(object.material) ? object.material : [object.material]) {
        if (!material) continue;
        materials.add(material);
        for (const value of Object.values(material)) if (value?.isTexture) textures.add(value);
        for (const uniform of Object.values(material.uniforms || {})) {
          const values = Array.isArray(uniform.value) ? uniform.value : [uniform.value];
          for (const value of values) if (value?.isTexture) textures.add(value);
        }
      }
    });
    for (const geometry of geometries) geometry.dispose();
    for (const material of materials) material.dispose();
    for (const texture of textures) {
      const data = texture.source?.data;
      for (const image of Array.isArray(data) ? data : [data]) if (image?.close) images.add(image);
      texture.dispose();
    }
    for (const skeleton of skeletons) skeleton.dispose();
    for (const image of images) image.close();
    gltf.parser?.cache?.removeAll();
    this._diagnostics.liveScenes = Math.max(0, this._diagnostics.liveScenes - 1);
    this._diagnostics.disposedScenes++;
  }

  _disposeModel() {
    this._disposeReference();
    this._metricReference = null;
    this._pivot?.removeFromParent();
    if (this._gltf) this._disposeGLTF(this._gltf);
    this._gltf = null;
    this._pivot = null;
    this._radius = null;
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
      this._renderer.domElement.remove();
    }
    if (this._host) {
      this._host.removeEventListener('keydown', this._onKey);
      delete this._host.dataset.renderTriangles;
      delete this._host.dataset.renderLines;
      delete this._host.dataset.renderCalls;
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
    this._cache.clear();
    this._diagnostics.cacheEntries = this._diagnostics.cacheBytes = 0;
    this._diagnostics.renderers = this._diagnostics.rendererCount = 0;
    if (sharedStage === this) sharedStage = null;
  }
}

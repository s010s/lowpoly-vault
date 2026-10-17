// Real Three.js resource objects with deterministic renderer/network stand-ins.
// Browser tests separately exercise actual WebGL pixels and context restoration.
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { ModelStage, MODEL_STAGE_LIMITS } from './viewer.js';

const frames = new Map(), parsed = [], disposed = [], closed = [], snapshotDraws = [];
let frameID = 0, fetchCount = 0, clears = 0, failFetch = false;
let parseGate = null, fetchGate = null, failParse = false;
const motion = { matches: false, addEventListener() {}, removeEventListener() {} };
globalThis.window = { matchMedia: () => motion };
globalThis.document = { baseURI: 'https://example.test/', hidden: false, addEventListener() {}, removeEventListener() {},
  createElement: () => ({ dataset: {}, setAttribute() {}, getContext: () => ({ drawImage(...args) { snapshotDraws.push(args); } }) }) };
globalThis.requestAnimationFrame = callback => { frames.set(++frameID, callback); return frameID; };
globalThis.cancelAnimationFrame = id => frames.delete(id);
const flush = () => { const pending = [...frames.values()]; frames.clear(); for (const callback of pending) callback(); };
const tick = () => new Promise(resolve => setTimeout(resolve, 0));
const deferred = () => { let resolve; const promise = new Promise(done => { resolve = done; }); return { promise, resolve }; };
const metadata = { units: 'meters', dimensions: [1, 1, 0] };
const makeHost = (width = 500, height = 500) => ({ clientWidth: width, clientHeight: height, isConnected: true, dataset: {}, removeEventListener() {} });
const host = makeHost(), detail = makeHost(900, 650);
const originalParse = GLTFLoader.prototype.parseAsync;
function makeGLTF(id) {
  const scene = new THREE.Group();
  scene.position.set(7, 3, -2);
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0, 1, 0, 0, 0, 1, 0], 3));
  geometry.setIndex([0, 1, 2]);
  const imageSize = id === 'oversized' ? 8192 : id.startsWith('budget-') ? 2500 : 8;
  const texture = new THREE.Texture({ width: imageSize, height: imageSize,
    close() { closed.push(id); } });
  const material = new THREE.MeshStandardMaterial({ map: texture });
  for (const [kind, resource] of [['geometry', geometry], ['material', material], ['texture', texture]]) {
    resource.addEventListener('dispose', () => disposed.push(`${id}:${kind}`));
  }
  scene.add(new THREE.Mesh(geometry, material));
  // A second scene sharing resources checks that disposal and size accounting dedupe.
  const alternate = new THREE.Group(); alternate.add(new THREE.Mesh(geometry, material));
  const gltf = { scene, scenes: [scene, alternate], animations: [], parser: { cache: { removeAll() {} } } };
  parsed.push({ id, gltf });
  return gltf;
}
GLTFLoader.prototype.parseAsync = async function (bytes) {
  if (failParse) throw new Error('Intentional parse failure');
  const id = new TextDecoder().decode(bytes).replace(/\0+$/, '');
  const gate = parseGate; parseGate = null;
  const gltf = makeGLTF(id);
  if (gate) await gate.promise;
  return gltf;
};
globalThis.fetch = async (url, { signal }) => {
  fetchCount++;
  if (failFetch) throw new Error('Intentional network failure');
  if (fetchGate) {
    const gate = fetchGate; fetchGate = null;
    await new Promise((resolve, reject) => {
      signal.addEventListener('abort', () => reject(new DOMException('cancelled', 'AbortError')), { once: true });
      gate.promise.then(resolve);
    });
  }
  const id = new URL(url).pathname.slice(1).replace(/\.glb$/, '');
  return { ok: true, arrayBuffer: async () => id.startsWith('encoded-') ? new ArrayBuffer(id === 'encoded-oversized' ? 25 * 1024 * 1024 : 16 * 1024 * 1024) : new TextEncoder().encode(id).buffer };
};
function createStage() {
  const stage = new ModelStage();
  stage._ensureRenderer = function () {
    if (this._renderer) return;
    this._renderer = {
      domElement: { width: 500, height: 500, style: {}, remove() {}, removeEventListener() {} },
      render() {}, clear() { clears++; }, info: { render: { triangles: 1, lines: 0, calls: 1 } },
      setSize() {}, renderLists: { dispose() {} }, dispose() {}, forceContextLoss() {},
    };
    this._scene = new THREE.Scene();
    this._camera = new THREE.PerspectiveCamera(38, 1, 0.01, 1000);
    this._controls = { target: new THREE.Vector3(), update() {}, dispose() {} };
    this._diagnostics.rendererCreations++;
    this._diagnostics.renderers = this._diagnostics.rendererCount = 1;
  };
  stage._attach = () => {};
  return stage;
}
const show = (stage, id, options = {}) => stage.show(options.host || host, `${id}.glb`, { mode: 'hover', metadata, ...options });
const near = (a, b, message) => assert(Math.abs(a - b) < 1e-9, message || `${a} != ${b}`);
function bounded(stage) {
  const s = stage.stats;
  assert(s.liveScenes <= 1 && s.activeLeases <= 1 && s.activeParses <= 1);
  assert(s.cachedScenes <= MODEL_STAGE_LIMITS.decodedEntries);
  assert(s.cachedDecodedBytes <= MODEL_STAGE_LIMITS.decodedBytes);
  assert(s.decodedEntries <= MODEL_STAGE_LIMITS.decodedEntries + MODEL_STAGE_LIMITS.uncachedActiveEntries);
  assert(s.uncachedActiveScenes <= 1);
  assert(s.cacheEntries <= MODEL_STAGE_LIMITS.encodedEntries && s.cacheBytes <= MODEL_STAGE_LIMITS.encodedBytes);
}
function empty(stage) {
  for (const key of ['liveScenes', 'cachedScenes', 'cachedDecodedBytes', 'decodedEntries', 'decodedBytes', 'decodedBufferBytes',
    'decodedTextureBytes', 'activeLeases', 'pendingLeases', 'activeEstimatedBytes', 'pendingEstimatedBytes', 'uncachedActiveScenes', 'resourceReferences', 'geometries',
    'materials', 'textures', 'skeletons', 'cacheEntries', 'cacheBytes', 'referenceObjects', 'referenceGeometries',
    'referenceMaterials', 'returnOverlayMeshes', 'returnOverlayMaterials', 'renderers', 'rendererCount', 'rafPending']) assert.equal(stage.stats[key], 0, key);
}

try {
  const stage = createStage();
  assert.equal(new ModelStage(), stage);
  await show(stage, 'a'); flush();
  const resource = stage._activeResource, root = stage._gltf.scene;
  const authoredPosition = root.position.clone();
  assert.equal(stage.stats.liveScenes, 1); assert.equal(stage.stats.activeLeases, 1);
  assert.equal(stage.stats.resourceReferences, 2, 'Cache ownership and active lease are explicit independent references.');
  assert.equal(stage.stats.decodedBufferBytes, 42, 'Shared geometry buffers count once across all scenes.');
  assert.equal(stage.stats.decodedTextureBytes, Math.ceil(8 * 8 * 4 * 4 / 3));
  stage.setView(128, 31, 6.4);
  near(Number(host.dataset.viewAzimuth), 128, 'setView paints synchronously for offline capture.');
  assert.equal(frames.size, 0); flush();
  const hover = stage.presentationInfo;
  near(hover.azimuth_deg, 128); near(hover.elevation_deg, 31); near(hover.distance, 6.4);
  assert.equal(stage._pivot.rotation.y, 0, 'Camera orbit must never rotate the asset relative to lights.');
  assert.equal(frames.size, 0, 'Inspection starts no animation loop.');
  motion.matches = true; stage._onMotion(); flush();
  assert.deepEqual(stage.presentationInfo, hover, 'Reduced motion changes preserve the actual inspected view.');
  stage.zoom(0.9); flush();
  const zoomed = stage.presentationInfo.distance;
  stage.setView(146, 27); flush(); near(stage.presentationInfo.distance, zoomed, 'Orbit preserves zoom without an explicit distance.');
  const snapshot = stage.snapshot();
  assert(snapshot); assert.equal(snapshot.dataset.assetId, 'a');
  const captured = snapshot.__presentation;
  const sourceCanvas = stage._renderer.domElement;
  for (const [width, height, x, y] of [[600, 400, 100, 0], [400, 600, 0, 100]]) {
    sourceCanvas.width = width; sourceCanvas.height = height;
    const square = stage.snapshot({ square: true });
    assert.equal(square.width, 400); assert.equal(square.height, 400);
    assert.deepEqual(snapshotDraws.at(-1), [sourceCanvas, x, y, 400, 400, 0, 0, 400, 400], 'Wide/tall card capture crops the exact centered render square in one copy.');
    const full = stage.snapshot();
    assert.equal(full.width, width); assert.equal(full.height, height, 'Default detail snapshots retain their full stage aspect.');
    assert.deepEqual(square.__presentation, captured);
  }
  sourceCanvas.width = sourceCanvas.height = 500;
  const requestsBefore = fetchCount, parsesBefore = stage.stats.parseCount;
  await show(stage, 'a', { host: detail, mode: 'detail', initialView: captured }); flush();
  assert.equal(stage._activeResource, resource, 'Card to detail reuses the exact decoded objects and GPU resources.');
  assert.equal(stage._gltf.scene, root); assert(root.position.equals(authoredPosition));
  for (const key of ['azimuth_deg', 'elevation_deg', 'distance']) near(stage.presentationInfo[key], captured[key]);
  assert.equal(stage.stats.parseCount, parsesBefore); assert.equal(fetchCount, requestsBefore);
  assert.equal(stage.stats.resourceReuses, 1); assert.equal(stage.stats.lastShowCacheHit, true);
  assert.equal(stage.stats.rendererCreations, 1);
  stage.scaleReference(true); stage.wireframe(true); flush();
  assert.equal(stage.stats.referenceObjects, 1);
  const returning = makeHost(600, 600), currentView = stage.presentationInfo, originalMaterial = [...resource.resources.materials][0];
  const originalMaterialState = { opacity: originalMaterial.opacity, transparent: originalMaterial.transparent, depthWrite: originalMaterial.depthWrite };
  assert(stage.moveTo(returning)); flush();
  assert.equal(stage._activeResource, resource); assert.equal(stage._gltf.scene, root);
  assert.equal(stage.stats.activeLeases, 1); assert.equal(stage.stats.rendererCreations, 1);
  for (const key of ['azimuth_deg', 'elevation_deg', 'distance']) near(stage.presentationInfo[key], currentView[key]);
  assert.equal(stage.stats.activeMode, 'return');
  const styles = stage.beginCanonicalReturnStyles(); let returnMaterialDisposals = 0;
  for (const material of styles.clones.values()) material.addEventListener('dispose', () => returnMaterialDisposals++);
  assert.equal(originalMaterial.opacity, 0); assert.equal(originalMaterial.wireframe, false);
  assert(styles.overlays.every(overlay => resource.resources.geometries.has(overlay.geometry)), 'Return styling reuses original geometry.');
  stage.canonicalReturnStyleProgress(.5, styles);
  near(originalMaterial.opacity, originalMaterialState.opacity * .5);
  near(styles.clones.get(originalMaterial).opacity, originalMaterialState.opacity * .5);
  near(stage._reference.material.opacity, .55 * .5);
  stage.canonicalReturnStyleProgress(1, styles);
  assert.equal(returnMaterialDisposals, styles.clones.size); assert.equal(stage.stats.referenceObjects, 0);
  assert.equal(stage.stats.returnOverlayMeshes, 0); assert.equal(stage.stats.returnOverlayMaterials, 0);
  assert.deepEqual({ opacity: originalMaterial.opacity, transparent: originalMaterial.transparent, depthWrite: originalMaterial.depthWrite }, originalMaterialState);
  assert.equal(originalMaterial.wireframe, false); assert(styles.overlays.every(overlay => overlay.parent === null));
  // Cancelling by hide restores every modified material property and retires
  // transient clones without disposing the cached original resources.
  stage.wireframe(true); const cancelledStyles = stage.beginCanonicalReturnStyles();
  stage.canonicalReturnStyleProgress(.3, cancelledStyles);
  stage.hide();
  assert.deepEqual({ opacity: originalMaterial.opacity, transparent: originalMaterial.transparent, depthWrite: originalMaterial.depthWrite }, originalMaterialState);
  assert.equal(originalMaterial.wireframe, false);
  assert.equal(stage.stats.liveScenes, 0); assert.equal(stage.stats.activeLeases, 0);
  assert.equal(stage.stats.referenceObjects, 0); assert.equal(stage.stats.cachedScenes, 1);
  assert.equal(root.parent, null); assert(root.position.equals(authoredPosition));
  assert.equal([...resource.resources.materials][0].wireframe, false, 'Release restores shared material state.');
  assert.equal(disposed.filter(value => value.startsWith('a:')).length, 0, 'Hide retains cached GPU resources.');
  assert.equal(frames.size, 0); assert(clears > 0); assert.equal(stage._renderer.domElement.style.visibility, 'hidden');
  assert.equal(detail.dataset.presentedUrl, undefined, 'Released hosts must not advertise a stale draw.');
  for (let i = 0; i < 5; i++) { await show(stage, 'a'); flush(); stage.hide(); }
  assert(root.position.equals(authoredPosition), 'Repeated reuse never accumulates a centering transform.');
  assert.equal(stage.stats.parseCount, parsesBefore);

  await show(stage, 'b'); await show(stage, 'c'); await show(stage, 'a'); await show(stage, 'd'); flush(); bounded(stage);
  assert(!stage._resources.has('https://example.test/b.glb'), 'LRU evicts the least recently acquired decoded model.');
  assert.deepEqual(disposed.filter(value => value.startsWith('b:')).sort(), ['b:geometry', 'b:material', 'b:texture']);
  assert.equal(closed.filter(id => id === 'b').length, 1);
  // Simulate pressure while the active model is the oldest cached entry.
  const active = stage._activeResource;
  stage._resources.delete(active.url); stage._resources = new Map([[active.url, active], ...stage._resources]);
  const extra = stage._resource('https://example.test/extra.glb', makeGLTF('extra'));
  stage._retainResource(extra); stage._syncResources(); bounded(stage);
  assert.equal(active.leases, 1); assert.equal(active.disposed, false);
  assert(!disposed.some(value => value.startsWith('d:')), 'Cache pressure cannot dispose the active/detail lease.');
  stage._disposeResource(active); assert.equal(active.disposed, false);

  await show(stage, 'oversized'); flush(); bounded(stage);
  assert.equal(stage.stats.uncachedActiveScenes, 1);
  assert(stage.stats.activeEstimatedBytes > MODEL_STAGE_LIMITS.decodedBytes);
  assert(!stage._resources.has('https://example.test/oversized.glb'));
  const oversized = stage._activeResource, oversizedParses = stage.stats.parseCount;
  const oversizedGate = deferred();
  const transferred = show(stage, 'oversized', { host: detail, mode: 'detail', presentationReady: oversizedGate.promise });
  await tick(); bounded(stage);
  assert.equal(stage.stats.pendingLeases, 1); assert.equal(stage.stats.liveScenes, 0);
  oversizedGate.resolve(); assert.equal(await transferred, true); flush();
  assert.equal(stage._activeResource, oversized);
  assert.equal(stage.stats.parseCount, oversizedParses, 'Even an oversized active same-URL transfer reuses its decoded resources.');
  assert.equal(stage.stats.pendingLeases, 0);
  stage.hide(); bounded(stage);
  assert.equal(stage.stats.uncachedActiveScenes, 0);
  assert.deepEqual(disposed.filter(value => value.startsWith('oversized:')).sort(), ['oversized:geometry', 'oversized:material', 'oversized:texture']);
  await show(stage, 'oversized'); flush();
  const transferAbort = new AbortController();
  const cancelledTransfer = show(stage, 'oversized', { signal: transferAbort.signal, presentationReady: new Promise(() => {}) });
  await tick(); assert.equal(stage.stats.pendingLeases, 1);
  transferAbort.abort(); assert.equal(await cancelledTransfer, false);
  assert.equal(stage.stats.pendingLeases, 0); assert.equal(stage.stats.uncachedActiveScenes, 0);
  assert.equal(disposed.filter(value => value.startsWith('oversized:')).length, 6,
    'An aborted oversized pending transfer releases its final lease.');

  // A rejected gate has the same cleanup contract as cancellation, including
  // the sole lease of an oversized model transferred out of its active host.
  await show(stage, 'oversized'); flush();
  let rejectPresentation;
  const rejectedPresentation = new Promise((resolve, reject) => { rejectPresentation = reject; });
  const rejectedTransfer = show(stage, 'oversized', { presentationReady: rejectedPresentation });
  await tick(); assert.equal(stage.stats.pendingLeases, 1);
  rejectPresentation(new Error('Intentional presentation failure'));
  await assert.rejects(rejectedTransfer, /Intentional presentation failure/);
  assert.equal(stage.stats.pendingLeases, 0); assert.equal(stage.stats.activeLeases, 0);
  assert.equal(stage.stats.uncachedActiveScenes, 0);
  bounded(stage);

  await show(stage, 'budget-a'); flush();
  await show(stage, 'budget-b'); flush(); bounded(stage);
  assert.equal(stage.stats.cachedScenes, 1, 'Decoded byte pressure evicts even before the entry limit.');
  assert.equal(stage.stats.disposedScenes > 0, true);
  assert(!stage._resources.has('https://example.test/budget-a.glb'));
  const bytesSignal = new AbortController().signal;
  await stage._bytes('https://example.test/encoded-a.glb', bytesSignal);
  await stage._bytes('https://example.test/encoded-b.glb', bytesSignal);
  assert.equal(stage.stats.cacheEntries, 1); assert.equal(stage.stats.cacheBytes, 16 * 1024 * 1024);
  assert(!stage._cache.has('https://example.test/encoded-a.glb'));
  await stage._bytes('https://example.test/encoded-oversized.glb', bytesSignal);
  assert(!stage._cache.has('https://example.test/encoded-oversized.glb'));
  bounded(stage);

  // Cancelling a gate which never resolves must not block a newer request.
  const gate = deferred(), abort = new AbortController();
  const gated = show(stage, 'gated', { presentationReady: gate.promise, signal: abort.signal });
  await tick(); abort.abort();
  assert.equal(await gated, false);
  assert.equal(await show(stage, 'after-gate'), true); flush();
  assert(!parsed.some(item => item.id === 'gated'));

  // GLTFLoader has no abort API. Its stale result is explicitly disposed before
  // the serialized next parse, and can neither attach nor enter the decoded LRU.
  parseGate = deferred(); const held = parseGate;
  const stale = show(stage, 'stale'); await tick();
  assert.equal(stage.stats.activeParses, 1);
  const fresh = show(stage, 'fresh'); held.resolve();
  assert.equal(await stale, false); assert.equal(await fresh, true); flush(); bounded(stage);
  assert.equal(stage.stats.staleScenes, 1); assert.equal(stage.stats.peakParses, 1);
  assert.equal(host.dataset.presentedUrl, 'https://example.test/fresh.glb');
  assert(!stage._resources.has('https://example.test/stale.glb'));
  assert.deepEqual(disposed.filter(value => value.startsWith('stale:')).sort(), ['stale:geometry', 'stale:material', 'stale:texture']);

  fetchGate = deferred();
  const cancelledFetch = show(stage, 'cancelled-fetch'); await tick();
  const next = show(stage, 'next');
  assert.equal(await cancelledFetch, false); assert.equal(await next, true); flush();
  assert.equal(stage.stats.peakRequests, 1); assert.equal(stage.stats.activeRequests, 0);
  failFetch = true;
  await assert.rejects(show(stage, 'failure'), /Intentional network failure/);
  assert.equal(stage.stats.liveScenes, 0); assert.equal(stage.stats.activeLeases, 0);
  assert.equal(host.dataset.modelState, 'error'); failFetch = false;
  failParse = true;
  await assert.rejects(show(stage, 'parse-failure'), /Intentional parse failure/);
  assert.equal(stage.stats.liveScenes, 0); assert.equal(stage.stats.activeParses, 0);
  assert.equal(stage.stats.activeLeases, 0); failParse = false;
  assert(!stage._cache.has('https://example.test/parse-failure.glb'), 'A failed parse cannot poison same-URL retries with corrupt bytes.');
  const recoveryRequests = stage.stats.networkRequests;
  await show(stage, 'parse-failure'); flush();
  assert.equal(stage.stats.networkRequests, recoveryRequests + 1, 'An explicit same-URL retry refetches after parse failure.');
  assert.equal(host.dataset.presentedUrl, 'https://example.test/parse-failure.glb');
  await show(stage, 'recovered'); flush();
  assert(stage.stats.networkMilliseconds >= 0 && stage.stats.lastShowMilliseconds >= 0);
  stage.dispose(); empty(stage);
  assert.equal(stage.stats.activeRequests, 0); assert.equal(stage.stats.activeParses, 0);
  assert.equal(frames.size, 0);
  assert.equal(disposed.length, parsed.length * 3, 'Every retained or stale resource is disposed exactly once.');
  assert.equal(closed.length, parsed.length);

  // Disposal during parsing still cleans up the uncancellable late result.
  const second = createStage();
  parseGate = deferred(); const late = parseGate;
  const pending = show(second, 'dispose-during-parse'); await tick();
  second.dispose(); empty(second); late.resolve();
  assert.equal(await pending, false); empty(second);
  assert.equal(second.stats.activeParses, 0);
  assert.equal(second.stats.disposedScenes, 1);
  assert.equal(disposed.length, parsed.length * 3);
  console.log(JSON.stringify({ status: 'pass', limits: MODEL_STAGE_LIMITS, checks: [
    'Exact decoded and GPU object reuse across card/detail', 'Orbit angle/elevation/distance and zoom continuity',
    'Reduced-motion view preservation and demand-only frames', 'Original transforms and wireframes restored',
    'Bounded LRU estimated geometry/texture bytes', 'Active lease protected from cache eviction',
    'Single oversized uncached active scene', 'Rejected oversized transfer gate cleanup',
    'Abortable presentation gate and fetch', 'Parse failure and queue recovery',
    'Stale parse disposal and one serialized parse', 'Complete teardown including pending parse',
  ] }, null, 2));
} finally { GLTFLoader.prototype.parseAsync = originalParse; }

// Real GLB bounds plus isolated lifecycle tests; no claim of WebGL visual coverage.
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { ModelStage, metricReferenceSpec } from './viewer.js';

async function discover(dir) {
  const paths = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) paths.push(...await discover(path));
    else if (entry.name === 'metadata.json') paths.push(path);
  }
  return paths;
}
const arrayBuffer = bytes => bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
const assets = [];
for (const path of await discover('assets')) {
  const metadata = JSON.parse(await readFile(path, 'utf8'));
  const bytes = arrayBuffer(await readFile(metadata.glb));
  const gltf = await new GLTFLoader().parseAsync(bytes, '');
  const size = new THREE.Box3().setFromObject(gltf.scene).getSize(new THREE.Vector3());
  const spec = metricReferenceSpec(size, metadata);
  assert(spec.available, `${metadata.id} must have verified meter bounds: ${spec.reason}`);
  assert.deepEqual(spec.dimensionsMeters, size.toArray(), 'Measurements must come from the loaded GLB.');
  assert(spec.floorY < -size.y / 2, 'Grid must remain below the model.');
  assets.push({ metadata, bytes });
  gltf.scene.traverse(object => {
    object.geometry?.dispose();
    for (const material of Array.isArray(object.material) ? object.material : [object.material]) material?.dispose();
  });
}
assert(assets.length > 0);

for (const longest of [0.000001, 0.001, 0.03, 1, 50, 10000]) {
  const size = new THREE.Vector3(longest, longest * 0.5, longest * 0.02);
  const metadata = { units: 'meters', dimensions: size.toArray() };
  const spec = metricReferenceSpec(size, metadata);
  assert(spec.available && spec.spacingMeters > 0 && Number.isFinite(spec.spacingMeters));
  assert(spec.halfX / spec.spacingMeters <= 3.01 && spec.halfZ / spec.spacingMeters <= 3.01,
    'Tiny and large references must have bounded line counts.');
  assert.equal(metricReferenceSpec(size, { ...metadata, dimensions: metadata.dimensions.map(value => value * 2) }).available, false);
}
const size = new THREE.Vector3(1, 2, 3);
const valid = { units: 'meters', dimensions: [1, 2, 3], axes: { glb_up: '+Y' }, blender_unit_scale: 1 };
for (const metadata of [undefined, {}, { ...valid, units: 'centimeters' }, { ...valid, dimensions: [1, 2, 4] },
  { ...valid, blender_unit_scale: 0.01 }, { ...valid, axes: { glb_up: '+Z' } }, { ...valid, dimensions: [1, NaN, 3] }]) {
  assert.equal(metricReferenceSpec(size, metadata).available, false, 'Unknown or contradictory units must not receive a metric reference.');
}

// Minimal renderer/DOM stand-ins let the real stage exercise lifecycle and RAF
// scheduling without pretending to test rasterization or browser interactions.
const frames = new Map();
let nextFrame = 0, renders = 0, fetches = 0;
globalThis.requestAnimationFrame = callback => { frames.set(++nextFrame, callback); return nextFrame; };
globalThis.cancelAnimationFrame = id => frames.delete(id);
globalThis.window = { matchMedia: () => ({ matches: false, addEventListener() {}, removeEventListener() {} }) };
globalThis.document = { baseURI: 'https://example.test/', hidden: false, addEventListener() {}, removeEventListener() {} };
globalThis.fetch = async url => {
  fetches++;
  const asset = assets.find(item => new URL(item.metadata.glb, document.baseURI).href === url);
  assert(asset, `Unexpected URL ${url}`);
  return { ok: true, arrayBuffer: async () => asset.bytes.slice(0) };
};
const flush = () => {
  const pending = [...frames];
  frames.clear();
  for (const [, callback] of pending) callback();
};
const stage = new ModelStage();
assert.equal(new ModelStage(), stage, 'The stage must remain a singleton.');
stage._ensureRenderer = function () {
  if (this._renderer) return;
  this._renderer = {
    domElement: { style: {}, remove() {}, removeEventListener() {} },
    render: () => renders++, info: { render: { triangles: 0, lines: 0, calls: 0 } },
    setSize() {}, renderLists: { dispose() {} }, dispose() {}, forceContextLoss() {},
  };
  this._scene = new THREE.Scene();
  this._camera = new THREE.PerspectiveCamera(38, 1, 0.01, 1000);
  this._controls = { target: new THREE.Vector3(), update() {}, dispose() {} };
};
stage._attach = () => {};
const host = { clientWidth: 700, clientHeight: 600, isConnected: true, dataset: {}, removeEventListener() {} };
const show = (asset = assets[0], metadata = asset.metadata) => stage.show(host, asset.metadata.glb, { mode: 'detail', metadata });
await show(); flush();
assert(stage.scaleReferenceInfo.available);
assert.equal(stage.scaleReferenceInfo.enabled, false);
const transform = stage._gltf.scene.matrix.clone();
const geometry = [];
stage._gltf.scene.traverse(object => { if (object.geometry) geometry.push([object.geometry, Array.from(object.geometry.attributes.position.array)]); });
const camera = stage._camera.position.clone();
let before = renders;
assert.equal(stage.scaleReference(true), true);
assert.equal(frames.size, 1, 'A toggle must request exactly one frame.');
flush();
assert.equal(renders, before + 1);
assert.equal(frames.size, 0, 'The reference must never start an animation loop.');
assert.equal(stage.stats.referenceObjects, 1);
assert.equal(stage.stats.referenceGeometries, 1);
assert.equal(stage.stats.referenceMaterials, 1);
assert.equal(stage._reference.parent, stage._pivot, 'Grid and asset must share exactly the same display normalization.');
assert.equal(stage._reference.material.depthTest, true);
assert.equal(stage._reference.material.depthWrite, false);
assert.equal(stage._reference.material.map, null, 'The reference must allocate no textures.');
assert(stage._camera.position.equals(camera), 'The scale toggle must not navigate.');
assert(stage._gltf.scene.matrix.equals(transform), 'The toggle must not change authored transforms.');
for (const [object, positions] of geometry) assert.deepEqual(Array.from(object.attributes.position.array), positions);
const measured = stage.scaleReferenceInfo.dimensionsMeters;
measured[0] = 999;
assert.notEqual(stage.scaleReferenceInfo.dimensionsMeters[0], 999, 'Returned measurements must not expose mutable state.');
stage.scaleReference(true);
assert.equal(frames.size, 0, 'An unchanged toggle is a no-op.');
stage._camera.position.y = -100;
stage._invalidate(); flush();
assert.equal(stage._reference.visible, false, 'An underside camera must not place the grid over the silhouette.');
stage._camera.position.copy(camera);
stage._invalidate(); flush();
assert.equal(stage._reference.visible, true);

let disposedGeometry = 0, disposedMaterial = 0;
const watchDisposal = () => {
  stage._reference.geometry.addEventListener('dispose', () => disposedGeometry++);
  stage._reference.material.addEventListener('dispose', () => disposedMaterial++);
};
watchDisposal();
stage.wireframe(true); flush();
assert.equal(stage._reference.material.wireframe, undefined, 'Wireframe must affect only the asset.');
stage.scaleReference(false);
assert.equal(disposedGeometry, 1); assert.equal(disposedMaterial, 1);
assert.equal(stage.stats.referenceObjects, 0);
flush();

stage._inView = false;
before = renders;
stage.scaleReference(true);
assert.equal(frames.size, 0, 'An offscreen reference must not schedule GPU work.');
assert.equal(renders, before);
watchDisposal();
await show(assets[1] || assets[0]); flush();
assert.equal(disposedGeometry, 2); assert.equal(disposedMaterial, 2);
assert.equal(stage.stats.liveScenes, 1);
assert.equal(stage.stats.referenceObjects, 0, 'A scene switch must remove the previous reference.');
assert.equal(stage.scaleReferenceInfo.enabled, false, 'Every new asset starts with its reference off.');
stage.scaleReference(true); watchDisposal();
stage.hide();
assert.equal(disposedGeometry, 3); assert.equal(disposedMaterial, 3);
assert.equal(stage.stats.referenceObjects, 0);
assert.equal(stage.stats.referenceGeometries, 0);
assert.equal(stage.stats.referenceMaterials, 0);
assert.equal(stage.stats.liveScenes, 0);
assert.equal(frames.size, 0, 'Hiding must cancel pending reference draws.');
assert.equal(stage.scaleReference(true), false);

const fetched = fetches;
await show(); flush();
assert.equal(fetches, fetched, 'The existing byte cache must survive reference use.');
await show(assets[0], { ...assets[0].metadata, units: 'unknown' }); flush();
assert.equal(stage.scaleReferenceInfo.available, false);
assert.equal(stage.scaleReference(true), false);
assert.equal(stage.stats.referenceObjects, 0);
const controller = new AbortController();
await stage.show(host, assets[0].metadata.glb, { mode: 'detail', metadata: assets[0].metadata, signal: controller.signal });
flush(); stage.scaleReference(true); watchDisposal();
controller.abort();
assert.equal(stage.stats.referenceObjects, 0, 'External cancellation must dispose the reference.');
assert.equal(disposedGeometry, 4); assert.equal(disposedMaterial, 4);
assert.equal(frames.size, 0);
const early = new AbortController();
const cancelled = stage.show(host, assets[0].metadata.glb, { mode: 'detail', metadata: assets[0].metadata, signal: early.signal });
early.abort();
assert.equal(await cancelled, false);
assert.equal(stage.stats.liveScenes, 0);
let releasePresentation;
const presentationReady = new Promise(resolve => { releasePresentation = resolve; });
const duringFlight = stage.show(host, assets[2].metadata.glb, { mode: 'detail', metadata: assets[2].metadata, presentationReady });
await new Promise(resolve => setTimeout(resolve, 0));
assert.equal(stage.stats.activeRequests, 0, 'Bytes finish fetching while the bitmap flies.');
assert.equal(stage.stats.liveScenes, 0, 'Parsing and renderer work wait for the presentation gate.');
releasePresentation(); assert.equal(await duringFlight, true); stage.hide();
const abortDuringFlight = new AbortController();
const gated = stage.show(host, assets[0].metadata.glb, { mode: 'detail', metadata: assets[0].metadata,
  signal: abortDuringFlight.signal, presentationReady: new Promise(resolve => { releasePresentation = resolve; }) });
await new Promise(resolve => setTimeout(resolve, 0));
abortDuringFlight.abort(); releasePresentation();
assert.equal(await gated, false, 'An aborted flight must never attach a stale GLB after the gate releases.');
assert.equal(stage.stats.liveScenes, 0);
stage.dispose();
assert.equal(stage.stats.cacheEntries, 0);
console.log(`PASS metric reference: ${assets.length} real GLBs, scale validation, immutable geometry, bounded resources, one-frame toggles, offscreen pause and disposal.`);

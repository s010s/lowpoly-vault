/** A wheel-only presentation record is not scientific, GPU, visual, or publication approval. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
export const wheelHash = bytes => createHash('sha256').update(bytes).digest('hex');
const HASH = /^[a-f0-9]{64}$/, ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
export function assertWheelSpec(spec) {
  assert(spec && typeof spec === 'object', 'Wheel framing required');
  for (const key of ['azimuth', 'elevation', 'zoom', 'aspect']) assert(Number.isFinite(spec[key]), `Invalid wheel ${key}`);
  assert(spec.zoom > 0 && Math.abs(spec.aspect - 16 / 9) < 1e-9, 'Invalid wheel projection');
  assert(spec.elevation > -90 && spec.elevation < 90, 'Invalid wheel elevation');
  for (const key of ['offset', 'floorCenter']) assert(Array.isArray(spec[key]) && spec[key].length === 2 && spec[key].every(Number.isFinite), `Invalid wheel ${key}`);
  assert(Array.isArray(spec.floorPoints) && spec.floorPoints.length >= 3 && spec.floorPoints.every(p => Array.isArray(p) && p.length === 2 && p.every(Number.isFinite)), 'Invalid wheel floor contour');
  assert(spec.projectedBounds && ['left','right','top','bottom'].every(k => Number.isFinite(spec.projectedBounds[k])), 'Invalid wheel projected bounds');
  assert(spec.projectedBounds.right > spec.projectedBounds.left && spec.projectedBounds.top > spec.projectedBounds.bottom, 'Empty wheel projected bounds');
  return spec;
}
export function assertWheelPNG(bytes, seal) {
  assert(Buffer.isBuffer(bytes) && bytes.length >= 33 && bytes.length <= 8 * 1024 * 1024, 'Wheel PNG bytes required');
  assert.equal(bytes.subarray(0,8).toString('hex'), '89504e470d0a1a0a', 'Wheel PNG signature');
  assert.equal(bytes.subarray(12,16).toString(), 'IHDR', 'Wheel PNG header');
  assert.deepEqual([bytes.readUInt32BE(16),bytes.readUInt32BE(20)], [768,432], 'Wheel PNG dimensions');
  assert.equal(bytes[24],8,'8-bit wheel PNG required'); assert.equal(bytes[25],6,'RGBA wheel PNG required');
  assert.equal(bytes.length,seal.bytes,'Wheel PNG byte count'); assert.equal(wheelHash(bytes),seal.sha256,'Wheel PNG hash');
}
export function createWheelPresentation({frame, png, asset, sourceGLB, previousWheel, unchangedDetail, rendererSha256, browserVersion}) {
  assert(ID.test(asset?.id || ''), 'Exact asset ID required');
  assert.equal(frame?.id, asset.id, 'Capture belongs to another asset');
  assert.equal(frame.source_glb_sha256, asset.sha256?.glb, 'Capture source differs');
  assert.equal(wheelHash(sourceGLB),asset.sha256.glb,'Source GLB bytes differ');
  assert(HASH.test(rendererSha256 || ''),'Renderer recipe hash required');
  assert(/^\d+\.\d+\.\d+\.\d+$/.test(browserVersion || ''),'Actual browser version required');
  assert(Buffer.isBuffer(previousWheel) && previousWheel.length && Buffer.isBuffer(unchangedDetail) && unchangedDetail.length,'Original wheel and unchanged detail bytes required');
  assert.equal(frame.dataURL,`data:image/png;base64,${png.toString('base64')}`,'PNG does not match the returned capture');
  const record = {version:1, kind:'unreviewed-wheel-presentation', publication_authority:false,
    id:asset.id, source_glb_sha256:asset.sha256.glb, previous_wheel_sha256:wheelHash(previousWheel),
    unchanged_detail_sha256:wheelHash(unchangedDetail), renderer_sha256:rendererSha256,
    browser_version:browserVersion, wheelSpec:structuredClone(assertWheelSpec(frame.wheelSpec)),
    png:{bytes:png.length,sha256:wheelHash(png)}, visual_review:'pending', physical_gpu:'unknown'};
  assertWheelPNG(png,record.png); return record;
}
/** The caller supplies reviewed source bytes, not a mutable generated resources.json. */
export function assertWheelPresentation(record,{asset,sourceGLB,png,previousWheel,unchangedDetail,rendererSha256,browserVersion}) {
  assert.equal(record?.version,1); assert.equal(record.kind,'unreviewed-wheel-presentation');
  assert.equal(record.publication_authority,false); assert.equal(record.visual_review,'pending'); assert.equal(record.physical_gpu,'unknown');
  const expected=createWheelPresentation({frame:{id:record.id,source_glb_sha256:record.source_glb_sha256,dataURL:`data:image/png;base64,${png.toString('base64')}`,wheelSpec:record.wheelSpec},png,asset,sourceGLB,previousWheel,unchangedDetail,rendererSha256,browserVersion});
  assert.deepEqual(record,expected,'Wheel presentation source/renderer/original bindings changed'); return record;
}

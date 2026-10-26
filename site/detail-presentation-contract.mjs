/** Publication-time seals, not a substitute for browser/visual review. */
import {authenticateDetailProofs,assertDetailAuthority,assertCapturedGeometry} from './detail-capture-authority.mjs';
import assert from 'node:assert/strict';
import {DETAIL_HIRES_METHOD,detailPresentationPolicy,detailCapturePolicy} from './gallery/detail-presentation-policy.js';
import {DETAIL_V2_SCOPE_KIND,DETAIL_V2_SCOPE_SHA256} from './detail-capture-scope.mjs';
import {readCaptureArchives,assertCaptureEntry} from './detail-capture-provenance.mjs';
import inputProofs from './gallery/detail-input-proofs.js';
import {decodeDetailPNG} from './detail-pixels.mjs';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {CAPTURE_POLICY,posterRendererFiles,posterInputKey} from './gallery-poster-inputs.mjs';
import {resolveGalleryPoster,resolveWheelPoster} from './gallery/wheel-presentations.js';
// Global baseline digests are historical provenance, not invalidation of unchanged per-asset captures.
const root=process.cwd(),sha=b=>createHash('sha256').update(b).digest('hex');
const index=(await import(pathToFileURL(resolve('site/gallery/detail-presentations-index.js')))).default;
const manifest=JSON.parse(await readFile('assets/manifest.json')),resources=JSON.parse(await readFile('site/public/gallery/resources.json'));
const presentation=index.renderer_policy?.detail_revision||null;
if(presentation)assert.deepEqual(presentation,detailPresentationPolicy(1536),'Unapproved delivery raster policy');
const files=[...await posterRendererFiles(root),'package-lock.json','site/capture-detail-presentations.mjs','site/detail-pixels.mjs',...(presentation?['site/gallery/detail-renderer.js','site/gallery/detail-presentation-policy.js','site/detail-capture-scope.mjs']:[])].sort();
const inputs=await Promise.all(files.map(async path=>({path,sha256:sha(await readFile(path))})));
const browsers=JSON.parse(await readFile('node_modules/playwright-core/browsers.json')),browser=browsers.browsers.find(b=>b.name==='chromium').browserVersion;
assert.equal(sha(JSON.stringify({files:inputs,policy:detailCapturePolicy(CAPTURE_POLICY,presentation),browser})),index.renderer_input_sha256,'Runtime detail renderer changed');
const affected=manifest.assets.filter(a=>['blender-cycles-cpu-v1','blender-detail-preview-wheel-v1'].includes(resources.posters[a.id]?.render_route));
const scopeBytes=await readFile('qa/detail-presentation-scope-20261025.json');
assert.equal(sha(scopeBytes),'a9903a78cbb5750e07c44a1ab2c1b5d0c4304f52935ab738ff78825d5cfe1778','Original two authorized cohorts changed');
const scope=JSON.parse(scopeBytes);assert.deepEqual(scope.cohorts.map(c=>[c.id,c.count]),[['original-right250',250],['pr72-replacement14',14]]);
const originalIds=scope.cohorts.flatMap(c=>c.assets.map(a=>a.id));assert.equal(new Set(originalIds).size,264);if(presentation)assert.deepEqual(index.migration_scope,{kind:DETAIL_V2_SCOPE_KIND,sha256:DETAIL_V2_SCOPE_SHA256,ids:[...originalIds].sort()},'Initial migration cohort provenance changed');for(const id of originalIds)assert(affected.some(a=>a.id===id),'Original right repair model disappeared '+id);
assert.equal(inputProofs.version,1);assert.equal(inputProofs.kind,'runtime-detail-input-proofs');assert(inputProofs.receipts.length>0,'Authenticated capture input receipts required');
assert.deepEqual(Object.keys(index.presentations).sort(),affected.map(a=>a.id).sort());
const authority=await authenticateDetailProofs({root,index,inputProofs,manifest,baseSha:process.env.BASE_SHA});
assertDetailAuthority(authority.capability,{root,index,inputProofs,manifest});
console.log('Right-detail proof authority:',JSON.stringify(authority.records));
const archives=await readCaptureArchives(inputProofs.receipts);
const decodedProofs=new Map();for(const receipt of inputProofs.receipts){assert.equal(receipt.decoded_proof.path,`qa/detail-presentation-evidence/captures/${receipt.run_id}/independent-decoded-checks.json`);const raw=await readFile(receipt.decoded_proof.path);assert.equal(sha(raw),receipt.decoded_proof.sha256);const proof=JSON.parse(raw);assert.equal(proof.status,'PASS');assert.equal(proof.count,proof.cases.length);decodedProofs.set(receipt,new Map(proof.cases.map(c=>[c.id,c])));}

for(const a of manifest.assets){const poster=resolveGalleryPoster(a,resources);if(!index.presentations[a.id]){assert.equal(poster.detail,resources.posters[a.id].detail,'Ordinary detail altered '+a.id);continue;}
 const wheel=resolveWheelPoster(a,resources);assert(wheel?.wheelSpec,'Production runtime wheel framing is required '+a.id);if(resources.posters[a.id].render_route==='blender-cycles-cpu-v1')assert.notEqual(wheel.wheel,resources.posters[a.id].wheel,'New Blender production must not bypass runtime left capture '+a.id);
 const e=index.presentations[a.id];const inputReceipt=inputProofs.receipts.find(r=>r.source_commit===e.capture.source_commit&&r.renderer_input_sha256===e.capture.renderer_input_sha256&&r.assets?.[a.id]?.detail_png_sha256===e.png.sha256);assert(inputReceipt,'Missing authenticated per-asset capture input proof '+a.id);assertCaptureEntry(archives,inputReceipt,a.id,e);assert(/^[a-f0-9]{64}$/.test(inputReceipt.capture_index_sha256)&&/^[a-f0-9]{64}$/.test(inputReceipt.artifact_sha256)&&Number.isSafeInteger(inputReceipt.run_id),'Incomplete capture provenance');assert.equal(inputReceipt.assets[a.id].source_glb_sha256,a.sha256.glb);assert.equal(inputReceipt.assets[a.id].asset_input_sha256,posterInputKey(a,{sha256:'detail-scope-source-only-v1'}),'Per-asset capture metadata changed '+a.id);assert.equal(poster.detail,e.detail,'Override rejected '+a.id);assert.equal(sha(await readFile(a.glb)),e.source_glb_sha256);
 const bytes=await readFile(resolve('site/public',e.detail));assert.equal(bytes.length,e.png.bytes);assert.equal(sha(bytes),e.png.sha256);assert.equal(bytes.subarray(1,4).toString(),'PNG');assert.equal(bytes.readUInt32BE(16),presentation?.raster_size||512);assert.equal(bytes.readUInt32BE(20),presentation?.raster_size||512);assert.equal(e.png.width,presentation?.raster_size||512);assert.equal(e.png.height,presentation?.raster_size||512);
 assert.equal(e.capture.first_frame.path,`qa/detail-presentation-evidence/first-frames/${a.id}.png`);decodeDetailPNG(bytes);const decoded=decodedProofs.get(inputReceipt).get(a.id);assert(decoded,'Independent decoded acceptance missing '+a.id);for(const key of ['different_pixels','max_channel_error','mask_iou'])assert.equal(decoded[key],e.capture.checks[key],'Archived independent metric differs '+a.id);
 // first_frame is the normalized fresh-selection repeat, not the native canvas.
 assert.equal(e.capture.method,presentation?DETAIL_HIRES_METHOD:'PreviewRenderer.select(detail)/canonical-square-native-clipping-v1');if(presentation){assert.deepEqual(e.capture.presentation,presentation);assertCapturedGeometry(e.capture.geometry_validation);}else assert.equal(e.capture.presentation,undefined);
 assert.equal(e.capture.native_frames?.length,2,'Both untouched native acknowledgments required');
 const tokens=new Set();for(const [n,frame] of e.capture.native_frames.entries()){
  assert.equal(frame.path,`qa/detail-presentation-evidence/native-frames/${a.id}-${n?'repeat':'first'}.png`);
  assert.equal(frame.method,'Unmodified canvas before acknowledgeDetailFrame');assert.equal(frame.id,a.id);assert.equal(frame.gl_error,0);assert(Number.isSafeInteger(frame.token)&&frame.token>0);tokens.add(frame.token);
  assert(Number.isSafeInteger(frame.bytes)&&frame.bytes>0&&/^[a-f0-9]{64}$/.test(frame.sha256),'Sealed native proof reference required');
  const c=frame.camera;assert(Number.isFinite(c.near)&&c.near>0&&Number.isFinite(c.far)&&c.far>c.near);assert(Number.isFinite(c.aspect)&&c.aspect>0);for(const [key,length] of [['position',3],['quaternion',4],['projection',16]])assert(c[key]?.length===length&&c[key].every(Number.isFinite));
 }assert.equal(tokens.size,2,'Fresh selection must have a distinct owner token');
 assert.equal(e.capture.checks.first_frame_id,a.id);assert.equal(e.capture.checks.gl_error,0);assert(e.capture.checks.mask_iou>.999);assert(e.capture.checks.different_pixels<100);
 assert.equal(sha(await readFile(resolve('site/public',e.previous_detail.path))),e.previous_detail.sha256,'Historical detail altered');
}
console.log(`PASS integrity: ${affected.length} exact source/runtime-bound right deliveries; ${manifest.assets.length-affected.length} ordinary detail selections preserved; runtime wheel framing required.`);

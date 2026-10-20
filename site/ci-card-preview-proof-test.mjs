/** Synthetic byte/input/report fixtures only. No browser or production capture
 * runs here; these tests cannot attest that any production WebP was reproduced.
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {assertCardPreviewRecord,freshCardPreviewRecords,CARD_PREVIEW_CHROMIUM} from './ci-card-preview-proof.mjs';

const hash=value=>createHash('sha256').update(value).digest('hex');
const canonical=value=>value&&typeof value==='object'?(Array.isArray(value)?value.map(canonical):Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])]))):value;
const hashObject=value=>hash(JSON.stringify(canonical(value)));
const clone=value=>structuredClone(value);
const preset={version:2,camera:{azimuth_deg:42},image:{width:768,height:768,format:'image/webp',quality:0.9,frames:24}};
const renderer={render_preset_sha256:hash(JSON.stringify(preset)),viewer_source_sha256:hash('synthetic viewer source, not production evidence')};
const model=index=>{
  const id=`model-${String(index+1).padStart(3,'0')}`,bytes=`Synthetic card WebP bytes for ${id}`;
  return {id,input_key:hash(`input key ${id}`),input_sha256:hash(`input bytes ${id}`),glb_sha256:hash(`synthetic GLB ${id}`),card_preview:{path:`assets/card-previews/${id}-v2-768-q90.webp`,sha256:hash(bytes),bytes:Buffer.byteLength(bytes)}};
};
const inputsFor=count=>({version:2,render_inputs:'verified-built-render-v1',built_payload_sha256:hash(`synthetic build ${count}`),
  gpu_policy:{browser:{chromium:CARD_PREVIEW_CHROMIUM}},card_preview_renderer:clone(renderer),models:Array.from({length:count},(_,index)=>model(index))});
const identityFor=(commit='a',run_id=101)=>({source_commit:commit.repeat(40),source_tree:'b'.repeat(40),run_id:String(run_id),run_attempt:'1'});
function syntheticReport(inputs,ids){
  return {status:'pass',target_renderer:'threejs-modelstage',render_preset:clone(preset),...renderer,
    chromium_version:CARD_PREVIEW_CHROMIUM,pinned_chromium_version:CARD_PREVIEW_CHROMIUM,
    assets:ids.map(id=>{const input=inputs.models.find(row=>row.id===id);return {id,source_glb_sha256:input.glb_sha256,frames:1,wall_ms:1,frame_bytes_total:0,poster_bytes:input.card_preview.bytes};}),
    gpu:{activeRequests:0,peakRequests:1,networkRequests:ids.length},reproducibility:{checked:ids.length,mismatches:[]}};
}
function argumentsFor(count=4){
  const inputs=inputsFor(count),selectedIDs=inputs.models.map(row=>row.id);
  return {inputs,selectedIDs,report:syntheticReport(inputs,selectedIDs),identity:identityFor(),payload_sha256:inputs.built_payload_sha256};
}
const args=argumentsFor(),records=freshCardPreviewRecords(args);
assert.equal(records.length,4);
for(const row of records){
  const input=args.inputs.models.find(model=>model.id===row.id);
  assert.equal(assertCardPreviewRecord(row,{input,identity:args.identity,payload_sha256:args.payload_sha256,renderer}),row);
  assert.equal(row.report_sha256,hashObject(args.report),'The receipt seals the entire original report, including diagnostics');
  assert.deepEqual(row.result.report_model_ids,args.selectedIDs);
  assert.deepEqual(row.card_preview,input.card_preview);
  assert.equal(row.result.source_glb_sha256,input.glb_sha256);
  assert.equal(row.result.render_preset_sha256,args.report.render_preset_sha256);
  assert.equal(row.result.viewer_source_sha256,args.report.viewer_source_sha256);
  assert.deepEqual(row.result.gpu,args.report.gpu);
  assert.equal(row.origin.run_id,101);
}
// Report order is immaterial; exact membership, including duplicates, is not.
const reverse=clone(args);reverse.report.assets.reverse();
assert.deepEqual(freshCardPreviewRecords(reverse).map(row=>row.id),[...args.selectedIDs].reverse());
// Receipt objects must not change when the original report/input is mutated.
const mutable=clone(args),detached=freshCardPreviewRecords(mutable);
mutable.report.gpu.peakRequests=99;mutable.report.render_preset.image.quality=0.1;mutable.report.reproducibility.mismatches.push({path:'bad'});mutable.inputs.models[0].card_preview.sha256='0'.repeat(64);
assert.deepEqual(detached,records);

let rejectedReports=0;
function rejectReport(label,change){const modified=clone(args);change(modified);assert.throws(()=>freshCardPreviewRecords(modified),undefined,label);rejectedReports++;}
const invalidReports=[
  ['failed report',a=>a.report.status='fail'],
  ['running report',a=>a.report.status='running'],
  ['missing report',a=>delete a.report],
  ['GPU first-paint report',a=>a.report={status:'pass',models:a.report.assets,gpu:{status:'pass'}}],
  ['gallery PNG report',a=>a.report={status:'pass',assets:a.report.assets,target_renderer:'PreviewRenderer.poster'}],
  ['missing actual IDs',a=>delete a.report.assets],
  ['missing executed model',a=>a.report.assets.pop()],
  ['extra executed model',a=>a.report.assets.push({...a.report.assets[0],id:'unselected'})],
  ['duplicated execution',a=>a.report.assets[1]=clone(a.report.assets[0])],
  ['wrong executed ID',a=>a.report.assets[0].id='model-other'],
  ['empty selection',a=>{a.selectedIDs=[];a.report.assets=[];a.report.reproducibility.checked=0;}],
  ['duplicate selection',a=>a.selectedIDs.push(a.selectedIDs[0])],
  ['unsafe selection',a=>a.selectedIDs[0]='../escape'],
  ['unknown input model',a=>a.inputs.models.shift()],
  ['duplicate input model',a=>a.inputs.models.push(clone(a.inputs.models[0]))],
  ['missing source GLB',a=>delete a.report.assets[0].source_glb_sha256],
  ['wrong source GLB',a=>a.report.assets[0].source_glb_sha256='f'.repeat(64)],
  ['unpinned actual browser',a=>a.report.chromium_version='142.0.0.0'],
  ['wrong pinned browser',a=>a.report.pinned_chromium_version='142.0.0.0'],
  ['missing pinned browser',a=>delete a.report.pinned_chromium_version],
  ['wrong policy browser',a=>a.inputs.gpu_policy.browser.chromium='142.0.0.0'],
  ['wrong renderer',a=>a.report.target_renderer='gallery-preview'],
  ['missing render preset',a=>delete a.report.render_preset],
  ['missing preset hash',a=>delete a.report.render_preset_sha256],
  ['wrong preset hash',a=>a.report.render_preset_sha256='e'.repeat(64)],
  ['self-consistent but wrong preset',a=>{a.report.render_preset.image.width=512;a.report.render_preset_sha256=hash(JSON.stringify(a.report.render_preset));}],
  ['not WebP',a=>{a.report.render_preset.image.format='image/png';a.report.render_preset_sha256=hash(JSON.stringify(a.report.render_preset));a.inputs.card_preview_renderer.render_preset_sha256=a.report.render_preset_sha256;}],
  ['missing viewer hash',a=>delete a.report.viewer_source_sha256],
  ['wrong viewer hash',a=>a.report.viewer_source_sha256='e'.repeat(64)],
  ['missing expected renderer',a=>delete a.inputs.card_preview_renderer],
  ['invalid expected renderer',a=>delete a.inputs.card_preview_renderer.viewer_source_sha256],
  ['turntable frames',a=>a.report.assets[0].frames=24],
  ['unrendered poster',a=>a.report.assets[0].frames=0],
  ['string frame count',a=>a.report.assets[0].frames='1'],
  ['turntable frame bytes',a=>a.report.assets[0].frame_bytes_total=8],
  ['missing frame byte total',a=>delete a.report.assets[0].frame_bytes_total],
  ['zero poster bytes',a=>a.report.assets[0].poster_bytes=0],
  ['wrong poster byte count',a=>a.report.assets[0].poster_bytes++],
  ['missing original GPU',a=>delete a.report.gpu],
  ['no GPU request',a=>a.report.gpu.peakRequests=0],
  ['too many GPU requests',a=>a.report.gpu.peakRequests=2],
  ['string GPU request count',a=>a.report.gpu.peakRequests='1'],
  ['missing reproduction check',a=>delete a.report.reproducibility],
  ['missing checked count',a=>delete a.report.reproducibility.checked],
  ['too few checked files',a=>a.report.reproducibility.checked--],
  ['too many checked files',a=>a.report.reproducibility.checked++],
  ['string checked count',a=>a.report.reproducibility.checked='4'],
  ['missing mismatch list',a=>delete a.report.reproducibility.mismatches],
  ['nonempty mismatches',a=>a.report.reproducibility.mismatches=[{path:a.inputs.models[0].card_preview.path,matches:false}]],
  ['another checked build',a=>a.payload_sha256='e'.repeat(64)],
  ['missing payload hash',a=>delete a.payload_sha256],
  ['missing identity',a=>delete a.identity],
  ['invalid source commit',a=>a.identity.source_commit='main'],
  ['invalid source tree',a=>a.identity.source_tree='main-tree'],
  ['missing origin run',a=>delete a.identity.run_id],
  ['zero origin attempt',a=>a.identity.run_attempt=0],
  ['missing input key',a=>delete a.inputs.models[0].input_key],
  ['missing shipped WebP seal',a=>delete a.inputs.models[0].card_preview],
  ['unsafe shipped WebP',a=>a.inputs.models[0].card_preview.path='assets/card-previews/../other.webp'],
  ['gallery PNG seal',a=>a.inputs.models[0].card_preview.path='gallery/posters/model-001.png'],
  ['missing actual WebP hash',a=>delete a.inputs.models[0].card_preview.sha256],
  ['invalid shipped byte count',a=>a.inputs.models[0].card_preview.bytes=-1],
  ['missing shipped byte count',a=>delete a.inputs.models[0].card_preview.bytes],
];
for(const [label,change]of invalidReports)rejectReport(label,change);

let rejectedReceipts=0;
function rejectReceipt(label,change){const row=clone(records[0]);change(row);assert.throws(()=>assertCardPreviewRecord(row,{input:args.inputs.models[0],identity:args.identity,payload_sha256:args.payload_sha256,renderer}),undefined,label);rejectedReceipts++;}
for(const [label,change]of [
  ['legacy GPU-only kind',r=>r.kind='strict-gpu-model-proof'],
  ['missing separate proof schema',r=>delete r.version],
  ['failed receipt',r=>r.status='fail'],
  ['wrong input key',r=>r.input_key='f'.repeat(64)],
  ['wrong input digest',r=>r.input_sha256='f'.repeat(64)],
  ['wrong GLB',r=>r.glb_sha256='f'.repeat(64)],
  ['missing original report hash',r=>delete r.report_sha256],
  ['missing original report IDs',r=>delete r.result.report_model_ids],
  ['duplicate original report IDs',r=>r.result.report_model_ids.push(r.id)],
  ['own ID missing from original report',r=>r.result.report_model_ids=r.result.report_model_ids.slice(1)],
  ['wrong original per-asset ID',r=>r.result.report_asset_id='model-002'],
  ['altered original source',r=>r.result.source_glb_sha256='f'.repeat(64)],
  ['wrong origin source',r=>r.origin.source_commit='c'.repeat(40)],
  ['wrong origin tree',r=>r.origin.source_tree='c'.repeat(40)],
  ['wrong origin run',r=>r.origin.run_id++],
  ['wrong origin attempt',r=>r.origin.run_attempt++],
  ['wrong origin build',r=>r.origin.payload_sha256='e'.repeat(64)],
  ['missing shipped seal',r=>delete r.card_preview],
  ['wrong shipped WebP bytes',r=>r.card_preview.sha256='e'.repeat(64)],
  ['wrong shipped WebP path',r=>r.card_preview.path='assets/card-previews/other.webp'],
])rejectReceipt(label,change);
// Selection fixture: 190 original receipts plus exactly four NEW report IDs.
// Independent GitHub run/artifact authentication and actual process invocation
// are intentionally tested by the integration/aggregate tests, not simulated here.
const baseline=inputsFor(190),originalIDs=baseline.models.map(row=>row.id),oldIdentity=identityFor('a',101);
const old=freshCardPreviewRecords({inputs:baseline,selectedIDs:originalIDs,report:syntheticReport(baseline,originalIDs),identity:oldIdentity,payload_sha256:baseline.built_payload_sha256});
const next=inputsFor(194),newIDs=next.models.slice(190).map(row=>row.id),newIdentity=identityFor('c',102),newReport=syntheticReport(next,newIDs);
const fresh=freshCardPreviewRecords({inputs:next,selectedIDs:newIDs,report:newReport,identity:newIdentity,payload_sha256:next.built_payload_sha256});
assert.equal(old.length,190);assert.equal(fresh.length,4);assert.deepEqual(newReport.assets.map(row=>row.id),newIDs);
for(const row of old)assertCardPreviewRecord(row,{input:next.models.find(model=>model.id===row.id),identity:oldIdentity,payload_sha256:baseline.built_payload_sha256,renderer});
for(const row of fresh)assertCardPreviewRecord(row,{input:next.models.find(model=>model.id===row.id),identity:newIdentity,payload_sha256:next.built_payload_sha256,renderer});
assert.equal(new Set([...old,...fresh].map(row=>row.id)).size,194);
assert(old.every(row=>row.origin.run_id===101));assert(fresh.every(row=>row.origin.run_id===102));
const changedCard=clone(next.models[0]);changedCard.card_preview.sha256=hash('changed actual shipped bytes');
assert.throws(()=>assertCardPreviewRecord(old[0],{input:changedCard}),/different shipped WebP/);
const changedRenderer={...renderer,viewer_source_sha256:hash('changed viewer source')};
assert.throws(()=>assertCardPreviewRecord(old[0],{input:next.models[0],renderer:changedRenderer}),/checked renderer inputs/);
assert.throws(()=>freshCardPreviewRecords({inputs:next,selectedIDs:newIDs,report:syntheticReport(next,next.models.map(row=>row.id)),identity:newIdentity,payload_sha256:next.built_payload_sha256}),/exact selected IDs/);
console.log(`Card-preview synthetic fixtures passed: ${rejectedReports} report and ${rejectedReceipts} receipt failures rejected; separate old190 + exact new4 provenance retained. No browser ran and no production rendering is claimed.`);

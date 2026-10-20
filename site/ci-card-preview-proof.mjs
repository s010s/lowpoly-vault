/** Separate receipts for the actual shipped-WebP reproduction task.
 * A GPU first paint or a gallery PNG capture cannot establish this evidence.
 * Authenticating a baseline run/artifact remains the aggregate verifier's job.
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

export const CARD_PREVIEW_PROOF_VERSION=1;
export const CARD_PREVIEW_PROOF_KIND='card-preview-reproducibility';
export const CARD_PREVIEW_CHROMIUM='141.0.7390.37';
const HASH=/^[a-f0-9]{64}$/,SHA=/^[a-f0-9]{40}$/,ID=/^[a-z0-9-]+$/;
const hash=value=>createHash('sha256').update(value).digest('hex');
const canonical=value=>value&&typeof value==='object'?(Array.isArray(value)?value.map(canonical):Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])]))):value;
const hashObject=value=>hash(JSON.stringify(canonical(value)));
const copy=value=>structuredClone(value);
const safePath=path=>typeof path==='string'&&!/[\\\u0000-\u001f?#%:]/.test(path)&&!path.startsWith('/')&&path.split('/').every(part=>part&&part!=='.'&&part!=='..');

function exactIDs(ids,label){
  assert(Array.isArray(ids)&&ids.length>0,`${label} must be a nonempty ID array`);
  assert(ids.every(id=>typeof id==='string'&&ID.test(id)),`${label} contains an invalid model ID`);
  assert.equal(new Set(ids).size,ids.length,`${label} contains duplicate model IDs`);
  return [...ids].sort();
}
function assertOrigin(origin){
  assert(SHA.test(origin?.source_commit||''),'Missing card-preview tested source');
  if(origin.source_tree!==undefined)assert(SHA.test(origin.source_tree),'Invalid card-preview source tree');
  assert(Number.isSafeInteger(origin.run_id)&&origin.run_id>0,'Missing card-preview origin run');
  assert(Number.isSafeInteger(origin.run_attempt)&&origin.run_attempt>0,'Missing card-preview origin attempt');
  assert(HASH.test(origin.payload_sha256||''),'Missing card-preview original tested build');
}
function assertCardFile(file){
  assert(file&&safePath(file.path)&&file.path.startsWith('assets/card-previews/')&&file.path.endsWith('.webp'),'Missing safe shipped card-preview WebP path');
  assert(HASH.test(file.sha256||''),'Missing actual shipped card-preview byte hash');
  if(file.bytes!==undefined)assert(Number.isSafeInteger(file.bytes)&&file.bytes>0,'Invalid shipped card-preview byte count');
}
function assertRenderer(result,expected){
  assert.equal(result.target_renderer,'threejs-modelstage','Card previews require the original ModelStage renderer');
  assert.equal(result.chromium_version,CARD_PREVIEW_CHROMIUM,'Card-preview browser is not lockfile-pinned Chromium');
  assert.equal(result.pinned_chromium_version,CARD_PREVIEW_CHROMIUM,'Card-preview report has a different pinned Chromium');
  assert(result.render_preset&&typeof result.render_preset==='object'&&!Array.isArray(result.render_preset),'Missing original card render preset');
  assert.equal(result.render_preset.image?.format,'image/webp','Card-preview report did not use WebP');
  assert(HASH.test(result.render_preset_sha256||''),'Missing original card render-preset hash');
  // The renderer uses ordinary JSON.stringify, not canonical key ordering.
  assert.equal(result.render_preset_sha256,hash(JSON.stringify(result.render_preset)),'Original card render-preset hash does not match its reported preset');
  assert(HASH.test(result.viewer_source_sha256||''),'Missing original card viewer-source hash');
  if(expected){
    for(const key of ['render_preset_sha256','viewer_source_sha256']){
      assert(HASH.test(expected[key]||''),`Missing expected card renderer ${key}`);
      assert.equal(result[key],expected[key],`Card-preview ${key} differs from checked renderer inputs`);
    }
  }
}

/** Check one durable receipt. Supplying its enclosing input/origin prevents a
 * valid receipt for another model, run, or build from being spliced into proof.
 */
export function assertCardPreviewRecord(row,{input,identity,payload_sha256,renderer}={}){
  assert.equal(row?.version,CARD_PREVIEW_PROOF_VERSION,'Missing separate card-preview proof');
  assert.equal(row.kind,CARD_PREVIEW_PROOF_KIND,'GPU/gallery evidence is not card-preview proof');
  assert.equal(row.status,'card-preview-pass');
  assert(typeof row.id==='string'&&ID.test(row.id),'Invalid card-preview model ID');
  for(const key of ['input_key','input_sha256','glb_sha256','report_sha256'])assert(HASH.test(row[key]||''),`Missing card-preview ${key}`);
  const result=row.result;
  assert.equal(result?.report_status,'pass','Original card-preview report did not pass');
  assertRenderer(result,renderer||input?.card_preview_renderer);
  const ids=exactIDs(result.report_model_ids,'Original card-preview report');
  assert(ids.includes(row.id),'Card-preview model was absent from the original report');
  assert.equal(result.report_asset_id,row.id,'Card-preview original report model differs');
  assert.equal(result.source_glb_sha256,row.glb_sha256,'Card-preview original GLB differs');
  assert.equal(result.frames,1,'Card-preview receipt requires posters-only execution');
  assert.equal(result.frame_bytes_total,0,'Posters-only execution cannot contain turntable frames');
  assert(Number.isSafeInteger(result.poster_bytes)&&result.poster_bytes>0,'Missing original rendered poster byte count');
  assert.equal(result.gpu?.peakRequests,1,'Original card renderer must assert one peak GPU request');
  assert.equal(result.reproducibility?.checked,ids.length,'Card-preview reproduction count must equal exact executed IDs');
  assert.deepEqual(result.reproducibility?.mismatches,[],'Shipped card-preview bytes were not reproduced exactly');
  assertOrigin(row.origin);
  assertCardFile(row.card_preview);
  if(row.card_preview.bytes!==undefined)assert.equal(row.card_preview.bytes,result.poster_bytes,'Reproduced poster byte count differs from shipped card');
  if(input){
    for(const key of ['id','input_key','input_sha256','glb_sha256'])assert.equal(row[key],input[key],`Card-preview ${key} differs from model input`);
    if(input.card_preview!==undefined){assertCardFile(input.card_preview);assert.deepEqual(row.card_preview,input.card_preview,'Card-preview receipt is for different shipped WebP bytes');}
  }
  if(identity){
    assert.equal(row.origin.source_commit,identity.source_commit,'Card-preview source differs from the original tested model source');
    assert.equal(row.origin.run_id,Number(identity.run_id),'Card-preview origin run differs');
    assert.equal(row.origin.run_attempt,Number(identity.run_attempt),'Card-preview origin attempt differs');
    if(identity.source_tree!==undefined)assert.equal(row.origin.source_tree,identity.source_tree,'Card-preview origin source tree differs');
    if(identity.payload_sha256!==undefined)assert.equal(row.origin.payload_sha256,identity.payload_sha256,'Card-preview origin build differs');
  }
  if(payload_sha256!==undefined)assert.equal(row.origin.payload_sha256,payload_sha256,'Card-preview tested another built payload');
  return row;
}

/** Consume render-web-previews.mjs's unmodified report after a successful
 * VERIFY_SHIPPED_PREVIEWS=1 PREVIEW_POSTERS_ONLY=1 subprocess. This function does
 * not execute Chromium and does not authenticate caller-supplied JSON itself.
 */
export function freshCardPreviewRecords({inputs,selectedIDs,report,identity,payload_sha256}){
  assert.equal(inputs?.version,2,'Card-preview proof requires content-addressed v2 model inputs');
  const selected=exactIDs(selectedIDs,'Selected card previews');
  assert(Array.isArray(inputs.models),'Missing checked card-preview model inputs');
  exactIDs(inputs.models.map(row=>row.id),'Checked model inputs');
  if(inputs.render_inputs==='verified-built-render-v1')assert.equal(inputs.built_payload_sha256,payload_sha256,'Card-preview inputs verified a different built payload');
  if(inputs.gpu_policy?.browser?.chromium!==undefined)assert.equal(inputs.gpu_policy.browser.chromium,CARD_PREVIEW_CHROMIUM,'Card-preview policy has a different pinned Chromium');
  assert.equal(report?.status,'pass','Card-preview report did not pass');
  assert(Array.isArray(report.assets),'Missing original card-preview asset report');
  const actualIDs=exactIDs(report.assets.map(row=>row.id),'Executed card previews');
  assert.deepEqual(actualIDs,selected,'Card-preview report did not execute exact selected IDs');
  assert(inputs.card_preview_renderer&&typeof inputs.card_preview_renderer==='object','Missing expected card-preview renderer input hashes');
  assertRenderer(report,inputs.card_preview_renderer);
  assert.equal(report.gpu?.peakRequests,1,'Original card renderer must assert one peak GPU request');
  assert.equal(report.reproducibility?.checked,selected.length,'Card-preview reproduction count must equal selected IDs');
  assert.deepEqual(report.reproducibility?.mismatches,[],'Shipped card-preview bytes were not reproduced exactly');
  const origin={source_commit:identity?.source_commit,...(identity?.source_tree!==undefined?{source_tree:identity.source_tree}:{}),run_id:Number(identity?.run_id),run_attempt:Number(identity?.run_attempt),payload_sha256};
  assertOrigin(origin);
  const report_sha256=hashObject(report);
  return report.assets.map(asset=>{
    const input=inputs.models.find(model=>model.id===asset.id);
    assert(input,'Unpublished card-preview execution');
    assertCardFile(input.card_preview);
    assert(Number.isSafeInteger(input.card_preview.bytes)&&input.card_preview.bytes>0,'Missing measured shipped card-preview bytes');
    assert.equal(asset.source_glb_sha256,input.glb_sha256,'Card-preview executed another source GLB');
    const result={report_status:report.status,target_renderer:report.target_renderer,
      chromium_version:report.chromium_version,pinned_chromium_version:report.pinned_chromium_version,
      render_preset:copy(report.render_preset),render_preset_sha256:report.render_preset_sha256,viewer_source_sha256:report.viewer_source_sha256,
      report_model_ids:[...actualIDs],report_asset_id:asset.id,source_glb_sha256:asset.source_glb_sha256,
      frames:asset.frames,frame_bytes_total:asset.frame_bytes_total,poster_bytes:asset.poster_bytes,
      gpu:copy(report.gpu),reproducibility:copy(report.reproducibility)};
    return assertCardPreviewRecord({version:CARD_PREVIEW_PROOF_VERSION,kind:CARD_PREVIEW_PROOF_KIND,status:'card-preview-pass',
      id:input.id,input_key:input.input_key,input_sha256:input.input_sha256,glb_sha256:input.glb_sha256,
      card_preview:copy(input.card_preview),report_sha256,result,origin:copy(origin)},
    {input,identity,payload_sha256,renderer:inputs.card_preview_renderer});
  });
}

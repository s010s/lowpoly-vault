/** Exact eleven newly selected inputs. Historical283 remains historical, never
 * a grant for five replacement meshes or six added representations. */
import assert from 'node:assert/strict';
import {hashBytes} from './model-registry.mjs';
import {CORRECTIVE_IDS,CORRECTIVE_REPRESENTATION_IDS,correctiveContext} from './old-corrective-ten-selection.mjs';
export const CORRECTIVE_DETAIL_PROFILE='corrective11-v2';
export const CORRECTIVE_DETAIL_BASE=Object.freeze({
 index:{path:'qa/old-corrective-ten-20261027/baseline/detail-presentations-index.js',sha256:'f7f88f686abc2a9ede118a2a53d2ccd47476735cf878a67020fc7417f9aef7cd',bytes:1150267},
 proofs:{path:'qa/old-corrective-ten-20261027/baseline/detail-input-proofs.js',sha256:'000b9fbc165bd722b285ab1c4c72b1a2a748e7a4f8ecb01419dd23acdc1fb65c',bytes:169458}
});
function exactData(read,pin){const raw=read(pin.path);assert.equal(raw.length,pin.bytes);assert.equal(hashBytes(raw),pin.sha256);const s=raw.toString();assert(s.startsWith('export default '));assert(s.trimEnd().endsWith(';'));return JSON.parse(s.slice(15).trim().slice(0,-1));}
export function assertCorrectiveDetailDelta({context,index,proofs,read}){
 const baseline=exactData(read,CORRECTIVE_DETAIL_BASE.index),oldProofs=exactData(read,CORRECTIVE_DETAIL_BASE.proofs);
 assert.equal(Object.keys(baseline.presentations).length,283);assert.deepEqual(CORRECTIVE_IDS.filter(id=>Object.hasOwn(baseline.presentations,id)),['oncoid-bed'],'Only Oncoid previously had a marked right presentation');const added=CORRECTIVE_IDS.filter(id=>id!=='oncoid-bed'),expected=[...Object.keys(baseline.presentations),...added].sort();
 assert.deepEqual(Object.keys(index.presentations).sort(),expected,'Only ten newly marked current inputs may extend original283; Oncoid is replaced');
 assert.deepEqual(Object.keys(proofs).sort(),Object.keys(oldProofs).sort());assert.equal(proofs.version,oldProofs.version);assert.equal(proofs.kind,oldProofs.kind);assert.equal(proofs.receipts.length,oldProofs.receipts.length+1);assert.deepEqual(proofs.receipts.slice(0,-1),oldProofs.receipts,'All original capture receipts remain exact');
 const fresh=proofs.receipts.at(-1);assert.equal(fresh.scope_kind,'bounded-fresh-subset-v1');assert.equal(fresh.capture_revision,2);assert.deepEqual([...fresh.requested_ids].sort(),[...CORRECTIVE_IDS].sort());assert.deepEqual(Object.keys(fresh.assets).sort(),[...CORRECTIVE_IDS].sort());assert(!oldProofs.receipts.some(r=>r.source_commit===fresh.source_commit||r.run_id===fresh.run_id),'New11 requires a distinct actual capture');
 for(const key of ['version','kind','renderer_policy','renderer_input_sha256','browser_version','renderer_files','migration_scope'])assert.deepEqual(index[key],baseline[key],'Unchanged right renderer/policy required: '+key);
 assert.equal(index.source_commit,fresh.source_commit);assert.equal(index.source_manifest_sha256,fresh.source_manifest_sha256);assert.equal(index.renderer_input_sha256,fresh.renderer_input_sha256);
 for(const [id,entry]of Object.entries(baseline.presentations))if(!CORRECTIVE_IDS.includes(id))assert.deepEqual(index.presentations[id],entry,'Unchanged historical right entry changed: '+id);
 const subjects=[];assert.deepEqual(context.entries.map(e=>e.next.id),CORRECTIVE_IDS);
 for(const {next}of context.entries){const asset=next.asset,id=asset.id,e=index.presentations[id],pin=fresh.assets[id];assert(e&&pin);assert.equal(e.detail,`detail-presentations/${id}.png`);assert.equal(e.source_glb_sha256,asset.sha256.glb);assert.equal(e.capture.source_commit,fresh.source_commit);assert.equal(e.capture.renderer_input_sha256,fresh.renderer_input_sha256);assert.equal(e.png.sha256,pin.detail_png_sha256);assert.equal(pin.source_glb_sha256,asset.sha256.glb);assert.equal(e.capture.method,'PreviewRenderer.select(detail)/canonical-square-native-clipping-hires-v2');assert.deepEqual(e.capture.presentation,{revision:2,minimum_margin:.025,screen_shift:.06,raster_size:1536});assert.equal(e.png.width,1536);assert.equal(e.png.height,1536);assert.equal(hashBytes(read(asset.glb)),asset.sha256.glb);const png=read('site/public/'+e.detail);assert.equal(hashBytes(png),e.png.sha256);assert.equal(png.length,e.png.bytes);subjects.push({id,source_glb_sha256:asset.sha256.glb,detail:e.detail,png_sha256:e.png.sha256,png_bytes:e.png.bytes});}
 return {pin:context.selectionPin,ids:[...CORRECTIVE_IDS],added_ids:added,subjects,baseline_count:283,current_count:293,unchanged_count:282,old_acceptance:'HISTORICAL_UNCHANGED_INPUTS_ONLY_NOT_CURRENT_REPLACEMENT_ACCEPTANCE',new_acceptance:'ALL_ELEVEN_REQUIRE_CURRENT_EXECUTION',publication_authorized:false};
}
export function selectedCorrectiveDetail({manifest,index,proofs,read}){const context=correctiveContext({manifest,read});if(!context)return null;return assertCorrectiveDetailDelta({context,index,proofs,read});}

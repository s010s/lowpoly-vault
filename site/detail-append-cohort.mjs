/** Exact extra samples, not a new authorization or a relabelled full264 review. */
import assert from 'node:assert/strict';
import {hashBytes} from './model-registry.mjs';
import {successorContext} from './same-id-successors.mjs';
export function exactDetailCohorts({legacyIds,appendIds,indexIds,affectedIds}){
 assert.equal(legacyIds.length,264);assert.equal(new Set(legacyIds).size,264,'Immutable original264 contains duplicates');
 assert.equal(new Set(appendIds).size,appendIds.length,'Duplicate explicit append sample');
 assert(appendIds.every(id=>!legacyIds.includes(id)),'Append cannot replace original264');
 const expected=[...legacyIds,...appendIds].sort();
 assert.deepEqual([...indexIds].sort(),expected,'Detail index must be exact original264 union authenticated append IDs');
 assert.deepEqual([...affectedIds].sort(),expected,'Affected cohort must be exact original264 union authenticated append IDs');
 return expected;
}
export function selectedDetailAppend({manifest,index,read}){
 if(!manifest.publication?.same_id_successor_append)return null;
 const context=successorContext({manifest,read});assert(context?.append,'Explicit validated append context required');
 const ids=context.append.records.map(record=>record.id),subjects=[];
 for(const record of context.append.records){
  const entry=index.presentations[record.id];assert(entry,'Explicit appended detail presentation missing');assert.equal(entry.detail,`detail-presentations/${record.id}.png`,'Appended right PNG needs exact ID ownership');
  assert.equal(entry.source_glb_sha256,record.asset.sha256.glb,'Appended detail capture source changed');
  const raw=read(record.asset.glb);assert.equal(hashBytes(raw),record.asset.sha256.glb,'Actual appended GLB differs');
  const png=read('site/public/'+entry.detail);assert.equal(hashBytes(png),entry.png.sha256,'Actual appended detail PNG differs');assert.equal(png.length,entry.png.bytes);
  subjects.push({id:record.id,source_glb_sha256:record.asset.sha256.glb,detail:entry.detail,png_sha256:entry.png.sha256,png_bytes:entry.png.bytes});
 }
 return {pin:context.appendPin,ids,subjects,legacy_appearance:'ORIGINAL264_REVIEW_NOT_RELABELED',new_appearance:'EXPLICIT_NEW_SAMPLES_REQUIRE_CURRENT_EXECUTION',publication_authorized:false};
}

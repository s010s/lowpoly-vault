/** Owner-authorized independent-QA release, with explicit static-profile diagnostics. */
import assert from 'node:assert/strict';
import {readFile,realpath} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {ACCEPTED_ROUND02_ASSETS} from './accepted-round02-release.mjs';
import {collectSmallLifeBatchRelease} from './small-life-batch-release.mjs';
import {assetFileAllowlist} from './asset-delivery.mjs';
export const ROUND02_IDS=Object.keys(ACCEPTED_ROUND02_ASSETS).sort();
export const ROUND02_PACK='prehistoric-small-life-round02-20261018';
const hash=b=>createHash('sha256').update(b).digest('hex');
function zeroErrors(value){if(Array.isArray(value)){value.forEach(zeroErrors);return;}if(!value||typeof value!=='object')return;for(const[k,v]of Object.entries(value)){if(['errors','failed','page_errors','pageErrors','consoleErrors','resource_errors'].includes(k))assert(Array.isArray(v)&&v.length===0);if(k==='gl_error')assert.equal(v,0);zeroErrors(v);}}
export async function collectRound02Release(root,p){
 const cache=new Map();
 async function checked(pin){assert(pin&&Object.keys(pin).sort().join(',')==='path,sha256');assert(typeof pin.path==='string'&&/^(assets|production|qa)\//.test(pin.path)&&!/[\\\u0000-\u001f?#%:]/.test(pin.path)&&pin.path.split('/').every(s=>s&&s!=='.'&&s!=='..'));assert(/^[a-f0-9]{64}$/.test(pin.sha256));const full=resolve(root,pin.path);assert.equal(await realpath(full),full,'Release symlinks forbidden');let b=cache.get(full);if(!b){b=await readFile(full);cache.set(full,b);}assert.equal(hash(b),pin.sha256,`${pin.path}: release hash mismatch`);return b;}
 const json=async pin=>JSON.parse(await checked(pin)),plain=pin=>({path:pin.path,sha256:pin.sha256});
 assert.equal(p?.path,'assets/releases/small-life-round02-twelve-20261018.json');const release=await json(p);
 assert.equal(release.version,1);assert.equal(release.scope,'small-life-round02-twelve-20261018');assert.equal(release.authorization,'owner_authorized_publish_independent_qa_passed_batches');assert.equal(release.validation_profile,'static-stylized-v1');assert.equal(release.rule_version,'2026-10-18.1');
 assert.equal(release.publication_policy.path,'production/policies/qa-passed-batch-publication-20261018.json');const policy=await json(release.publication_policy);assert.equal(policy.authority,'owner_authorized_qa_passed_batch_release');assert.equal(policy.candidate_gate_grants_publication,false);
 assert.equal(release.base_descriptor.path,'assets/releases/small-life-twelve-20261018.json');const base=await collectSmallLifeBatchRelease(root,release.base_descriptor);assert.equal(base.assets.length,31);assert.deepEqual(release.additions.map(a=>a.id).sort(),ROUND02_IDS);assert.equal(release.batches.length,3);
 const additions=[];
 for(const entry of release.additions){
  const id=entry.id,accepted=ACCEPTED_ROUND02_ASSETS[id],folder=`assets/additions/${id}/small-life-round02-20261018`,batch=release.batches.find(b=>b.batch===accepted.batch);assert(batch);assert.equal(batch.source_commit,accepted.source_commit);assert.equal(batch.review_commit,accepted.review_commit);assert.deepEqual(batch.review,accepted.review);assert(batch.ids.includes(id));
  assert.equal(entry.metadata.path,`${folder}/release-metadata.json`);const a=await json(entry.metadata),source=await json(accepted.source_metadata);assert.equal(a.id,id);assert.equal(a.source_category,source.category);assert.equal(a.category,'animals');assert.equal(a.collection,'prehistoric');assert.deepEqual(a.worlds,['prehistoric']);assert.deepEqual(a.packs,[ROUND02_PACK]);assert.equal(a.license,'CC-BY-4.0');assert.equal(a.author,'Leon Made This / s010s');assert.equal(a.units,'meters');
  for(const key of ['name','description','triangles','dimensions','axes','origin','bounds_glb_m','sources','nominal_scale','reconstruction_notes','mounting_point','warnings_disposition','source_warnings_review'])assert.deepEqual(a[key],source[key],`Preserve reviewed ${key}`);
  for(const key of ['name','description','scientific_scope'])for(const lang of ['en','zh'])assert(a[key]?.[lang]?.trim());
  assert.equal(a.source_url,`https://github.com/s010s/lowpoly-vault/tree/${accepted.source_commit}/${dirname(source.glb)}`);
  for(const key of ['qa','review_only','release_status','quality_status','publication','downloads','turntable','card_preview','revision','revision_provenance','independent_qa','independent_acceptance','status','review_state','independent_review','candidate_record','approval_provenance'])assert(!Object.hasOwn(a,key));
  assert.deepEqual(a.sha256,entry.sha256);assetFileAllowlist({assets:[a]});
  for(const key of ['glb','blend','preview']){assert.equal(dirname(a[key]),folder);const b=await checked({path:a[key],sha256:entry.sha256[key]});if(key!=='preview'){assert.equal(entry.sha256[key],accepted[key].sha256);assert.equal(b.length,accepted[key].bytes);assert.equal(hash(await checked(plain(accepted[key]))),entry.sha256[key]);assert.equal(source.sha256[key],entry.sha256[key]);}if(key==='glb')assert(b.toString('ascii',0,4)==='glTF'&&b.readUInt32LE(4)===2&&b.readUInt32LE(8)===b.length);}
  for(const evidence of accepted.evidence)await checked(evidence);for(const dep of accepted.dependencies)await checked(dep.snapshot);
  // Candidate-format errors must not prevent an independent fresh budget audit.
  const candidate=await json(accepted.candidate),brief=await json(plain(candidate.artifacts.brief)),limits=brief.geometry_policy;
  const auditRun=spawnSync('python3',['scripts/qa_glb.py',source.glb,'--max-triangles',String(limits.max_triangles),'--max-materials',String(limits.max_materials),'--max-primitives',String(limits.max_primitives)],{cwd:root,encoding:'utf8',timeout:30000,maxBuffer:2*1024*1024});assert(!auditRun.error,auditRun.error?.message);assert.equal(auditRun.status,0,auditRun.stderr);const measured=JSON.parse(auditRun.stdout);assert.deepEqual(measured.errors,[]);assert.equal(measured.sha256,a.sha256.glb);assert.equal(measured.scene_triangles,a.triangles);assert(measured.scene_triangles<=limits.max_triangles&&measured.materials<=limits.max_materials&&measured.scene_primitives_estimated_base_draw_calls<=limits.max_primitives&&accepted.glb.bytes<=limits.max_glb_bytes,'Original frozen geometry budgets remain mandatory');
  const validator=await json(accepted.validator);assert.equal(validator.issues.numErrors,0);assert.equal(validator.issues.numWarnings,0);assert.equal(validator.issues.truncated,false);
  const sourceExport=await json(accepted.source_export);assert(['pass','pass_with_warnings'].includes(sourceExport.status));assert.equal(sourceExport.glb_sha256,a.sha256.glb);assert.equal(sourceExport.source_sha256,a.sha256.blend);assert.equal(sourceExport.triangles_match,true);assert.equal(sourceExport.bounds_match,true);assert.deepEqual(sourceExport.errors,[]);
  const runtime=await json(accepted.runtime);assert.equal(runtime.status,'pass');assert.equal(runtime.glb_sha256,a.sha256.glb);assert.equal(runtime.webgl2,true);zeroErrors(runtime);assert(runtime.views.length>0&&runtime.views.every(v=>v.triangles>0));
  const scene=await json(accepted.scene);assert.equal(scene.status,'pass');zeroErrors(scene);assert(scene.instances>=2&&scene.views.length>0&&scene.views.every(v=>v.triangles>0));assert(scene.loaded.some(a=>a.id===id));
  const views=await json(accepted.views);if(accepted.batch==='06')assert.equal(views.glb.sha256,a.sha256.glb);else{assert.equal(views.glb_sha256,a.sha256.glb);assert.equal(views.turntable_frames,0);}
  const review=(await checked(accepted.review)).toString();assert(review.includes(accepted.source_commit)&&review.includes(a.sha256.glb)&&review.includes(a.sha256.blend));assert(new RegExp(id+'[^\\n]*PASS','i').test(review),'Per-asset independent model PASS required');
  // Profile compatibility does not turn malformed/pending historical candidate records into approvals.
  await checked(accepted.profile_contract);const frozen=await json(accepted.profile_result);const run=spawnSync('python3',['scripts/validate_candidate.py',accepted.candidate.path,'--root',resolve(root),'--profile','static-stylized-v1','--profile-contract',accepted.profile_contract.path,'--json'],{cwd:root,encoding:'utf8',timeout:30000,maxBuffer:2*1024*1024});assert(!run.error,run.error?.message);assert([0,1].includes(run.status),run.stderr);const current=JSON.parse(run.stdout);
  for(const result of [frozen,current]){assert.equal(result.validation_profile,'static-stylized-v1');assert.equal(result.rule_version,release.rule_version);assert.equal(result.profile_contract_status,'pass',JSON.stringify(result.errors));for(const key of ['valid','approved_for_brief','errors','approval_blockers','profile_contract_status'])assert.deepEqual(result[key],accepted.profile_outcome[key]);assert.equal(result.approved_for_brief,false);assert.equal(result.legacy_result.valid,false);}
  assert.deepEqual(current.errors,frozen.errors);assert.deepEqual(current.legacy_result.errors,frozen.legacy_result.errors);
  additions.push({...a,quality_status:'independent_qa_accepted_stylized_prop',approval_provenance:{source_commit:accepted.source_commit,review_commit:accepted.review_commit,review_sha256:accepted.review.sha256,validation_profile:'static-stylized-v1',rule_version:release.rule_version,candidate_record_approved_for_brief:false}});
 }
 assert(!additions.some(a=>base.assets.some(b=>a.id===b.id)));
 return {...base,assets:[...base.assets,...additions],publication:{...base.publication,round02_descriptor:p,approved_round02_ids:ROUND02_IDS}};
}

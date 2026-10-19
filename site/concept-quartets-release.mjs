/** Bounded website publication, separate from unchanged formal candidate gates. */
import assert from 'node:assert/strict';
import {readFile,realpath} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {CONCEPT_QUARTETS_RELEASE as fixed} from './accepted-concept-quartets-release.mjs';
import {collectConceptSevenRelease} from './concept-seven-release.mjs';
import {assetFileAllowlist} from './asset-delivery.mjs';
export const CONCEPT_QUARTETS_IDS=fixed.additions.map(a=>a.id).sort();
export const CONCEPT_QUARTETS_PACK='prehistoric-concept-quartets-20261019';
export async function collectConceptQuartetsRelease(root,descriptor){
 const cache=new Map(),sha=b=>createHash('sha256').update(b).digest('hex');
 async function checked(pin){assert(pin&&/^(assets|production|qa|scripts)\/[a-zA-Z0-9_./-]+$/.test(pin.path)&&!pin.path.split('/').some(p=>!p||p==='.'||p==='..'));assert(/^[a-f0-9]{64}$/.test(pin.sha256));const p=resolve(root,pin.path);assert.equal(await realpath(p),p,'Release symlinks forbidden');let b=cache.get(p);if(!b){b=await readFile(p);cache.set(p,b);}assert.equal(sha(b),pin.sha256,`${pin.path}: release hash mismatch`);return b;}
 const json=async pin=>JSON.parse(await checked(pin));
 const run=(script,args)=>{const r=spawnSync('python3',[script,...args],{cwd:root,encoding:'utf8',timeout:30000,maxBuffer:2*1024*1024});assert(!r.error,r.error?.message);assert([0,1].includes(r.status),r.stderr);return JSON.parse(r.stdout);};
 assert.equal(descriptor.path,'assets/releases/concept-quartets-20261019.json');const release=await json(descriptor);assert.deepEqual(release,fixed,'Only exact reviewed assets and bounded claims are authorized');
 const policy=await json(release.publication_policy);assert.equal(policy.authority,'owner_authorized_qa_passed_batch_release');assert.equal(policy.candidate_gate_grants_publication,false);
 const bundle=await json(release.source_bundle);assert.equal(new Set(bundle.files.map(f=>f.path)).size,bundle.files.length);for(const p of bundle.files)await checked(p);
 const audit=await json(release.integration_audit);assert.equal(audit.status,'pass');assert.equal(audit.source_matches_exact_commit,true);assert.equal(audit.qa_matches_exact_commit,true);assert.equal(audit.original_files_unchanged_except_allowed_delivery_metadata,true);
 const additions=[];
 for(const entry of release.additions){
  const a=await json(entry.metadata),source=await json(entry.source_metadata),folder=`assets/additions/${entry.id}/concept-quartets-20261019`;
  assert.equal(entry.metadata.path,`${folder}/release-metadata.json`);assert.equal(a.id,entry.id);assert.equal(a.category,'animals');assert.equal(a.collection,'prehistoric');assert.deepEqual(a.worlds,['prehistoric']);assert.deepEqual(a.packs,[CONCEPT_QUARTETS_PACK]);assert.equal(a.license,'CC-BY-4.0');assert.equal(a.author,'Leon Made This / s010s');assert.equal(a.units,'meters');assert.deepEqual(a.sha256,entry.sha256);assetFileAllowlist({assets:[a]});
  for(const key of ['name','description','scientific_scope'])for(const lang of ['en','zh'])assert(a[key]?.[lang]?.trim());
  for(const key of ['quality_status','approval_provenance','candidate_record','qa','publication_status','downloads','turntable','card_preview'])assert(!Object.hasOwn(a,key),`Reserved metadata ${key}`);
  for(const key of ['triangles','dimensions','axes','bounds_glb_m','blender_dimensions_m','export_options','materials','generator'])assert.deepEqual(a[key],source[key],`Preserve measured ${key}`);
  for(const key of ['glb','blend','preview']){assert.equal(dirname(a[key]),folder);await checked({path:a[key],sha256:a.sha256[key]});}
  for(const key of ['glb','blend']){assert.equal(entry.artifacts[key].sha256,a.sha256[key]);await checked(entry.artifacts[key]);}
  assert.deepEqual(a.sources,(await json(entry.artifacts.references)).sources);assert.deepEqual(entry.limits,(await json(entry.artifacts.brief)).budgets);
  const limits=entry.limits,measured=run('scripts/qa_glb.py',[a.glb,'--max-triangles',String(limits.max_triangles),'--max-materials',String(limits.max_materials),'--max-primitives',String(limits.max_primitives)]);assert.deepEqual(measured.errors,[]);assert.equal(measured.sha256,a.sha256.glb);assert.equal(measured.scene_triangles,a.triangles);assert.deepEqual(measured.bounds_m.size,a.dimensions);assert((await checked(entry.artifacts.glb)).length<=limits.soft_glb_bytes);
  for(const key of ['source_export','rebuild_1','rebuild_2','runtime_parse']){const t=await json(entry.technical[key]);assert(['pass','pass_with_warnings'].includes(t.status));assert(!t.errors?.length);assert.equal(t.glb_sha256??t.subject?.glb_sha256,a.sha256.glb);if(key==='source_export'){assert.equal(t.source_sha256,a.sha256.blend);assert.equal(t.triangles_match,true);assert.equal(t.bounds_match,true);}if(key.startsWith('rebuild')){assert.equal(t.semantic_match,true);assert.equal(t.provenance_status,'bound_successful_build_run');}}
  const capture=await json(entry.capture.report),captureIndex=await json(entry.capture.index);assert.equal(capture.status,'pass');assert.equal(capture.chromium_version,capture.pinned_chromium_version);assert.equal(capture.assets.find(r=>r.id===a.id).source_glb_sha256,a.sha256.glb);assert.equal(captureIndex.posters.find(r=>r.id===a.id).source_glb_sha256,a.sha256.glb);assert.equal(entry.capture.reference.sha256,a.sha256.preview);await checked(entry.capture.reference);
  const format=await json(entry.technical.khronos);assert.equal(format.issues.numErrors,0);assert.equal(format.issues.numWarnings,0);
  const proof=await json(entry.proof);assert.equal(proof.source_glb_sha256,a.sha256.glb);assert.equal(proof.frames.length,12);for(const frame of proof.frames){const b=await checked({path:`${dirname(entry.proof.path)}/${frame.path}`,sha256:frame.sha256});assert.equal(b.length,frame.bytes);assert.equal(b.readUInt32BE(16),frame.width);assert.equal(b.readUInt32BE(20),frame.height);}
  const review=await json(entry.review);assert.equal(review.frozen_source_commit,entry.original_review_freeze);assert.equal(review.scoped_review,'pass');assert.equal(review.models_modified,false);assert.equal(review.formal_candidate_acceptance,'blocked');assert.equal(review.release_acceptance,'not_granted');const r=review.assets.find(r=>r.asset_id===a.id);assert.equal(r.independent_scoped_review,'pass');assert.equal(r.concept_visual_status,'pass');assert.equal(r.glb_sha256,a.sha256.glb);assert.equal(r.blend_sha256,a.sha256.blend);assert.deepEqual(r.dimensions_glb_xyz_m,a.dimensions);
  const runtime=await json(entry.runtime);assert.equal(runtime.status,'pass');assert.deepEqual(runtime.errors,[]);assert.deepEqual(runtime.resource_errors,[]);assert.equal(runtime.scene_assets.find(r=>r.id===a.id).glb_sha256,a.sha256.glb);
  const candidate=await json(entry.candidate);assert.equal(candidate.approval.status,'pending');const current=run('scripts/validate_candidate.py',[entry.candidate.path,'--root',resolve(root),'--json']);assert.deepEqual(current,await json(entry.candidate_validation));assert.equal(current.valid,true);assert.equal(current.approved_for_brief,false);assert.equal(current.validation_profile,'legacy-v1');
  additions.push({...a,quality_status:'independent_qa_accepted_stylized_prop',approval_provenance:{source_commit:entry.source_commit,review_commit:entry.review_commit,review_sha256:entry.review.sha256,source_contract:'bounded-concept-study:12-views; retrospective pending legacy candidate record',candidate_record_approved_for_brief:false,formal_profile_acceptance:'BLOCKED',hardware_gpu_verified:false,target_scene_verified:false,concept_chronology:'producer records preserved; not an independent timing attestation'}});
 }
 const base=await collectConceptSevenRelease(root,release.base_descriptor);assert.equal(base.assets.length,182);assert(!additions.some(a=>base.assets.some(b=>b.id===a.id)));assert(!additions.some(a=>release.excluded_ids.includes(a.id)));return {...base,assets:[...base.assets,...additions],publication:{...base.publication,concept_quartets_descriptor:descriptor,approved_concept_quartets_ids:CONCEPT_QUARTETS_IDS}};
}

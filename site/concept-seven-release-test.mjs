/** Exact-seven scope, immutable source/QA, and explicitly unapproved formal gates. */
import assert from 'node:assert/strict';
import { mkdtemp,readFile,writeFile,rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join,resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { collectConceptSevenRelease,CONCEPT_SEVEN_IDS } from './concept-seven-release.mjs';
import { CONCEPT_SEVEN_RELEASE as fixed } from './accepted-concept-seven-release.mjs';
const root=await mkdtemp(join(tmpdir(),'vault-concept-seven-')),file='assets/releases/concept-seven-20261019.json'; let checks=0;
const pin=async path=>({path,sha256:createHash('sha256').update(await readFile(resolve(root,path))).digest('hex')});
async function mutate(path,change,action){const bytes=await readFile(resolve(root,path));try{const d=JSON.parse(bytes);change(d);await writeFile(resolve(root,path),JSON.stringify(d));await action();checks++;}finally{await writeFile(resolve(root,path),bytes);}}
try {
 for(const dir of ['assets','production','qa','scripts','experiments','package-lock.json'])execFileSync('cp',['-a','--reflink=auto',dir,resolve(root,dir)]);
 const collect=async()=>collectConceptSevenRelease(root,await pin(file));
 const manifest=await collect(),before=JSON.parse(await readFile('assets/manifest.json'));
 assert.equal(manifest.assets.length,182);assert.deepEqual(manifest.assets.slice(0,175),before.assets.slice(0,175));assert.deepEqual(manifest.assets.slice(175).map(a=>a.id).sort(),CONCEPT_SEVEN_IDS);checks++;
 assert(!manifest.assets.some(a=>a.id==='ctenoimbricata'));checks++;
 for(const a of manifest.assets.slice(175)){
  assert.equal(a.quality_status,'independent_qa_accepted_stylized_prop');assert.equal(a.approval_provenance.candidate_record_approved_for_brief,false);assert.equal(a.approval_provenance.formal_profile_acceptance,'BLOCKED');assert.equal(a.approval_provenance.hardware_gpu_verified,false);assert.equal(a.approval_provenance.target_scene_verified,false);assert(!a.approval_provenance.validation_profile);checks++;
 }
 assert.equal(manifest.assets.find(a=>a.id==='dorypterus').display_length_m,0.0996);assert(manifest.assets.find(a=>a.id==='pteraspis').description.en.includes('unverified'));checks++;
 for(const change of [d=>d.additions.pop(),d=>d.additions.push(d.additions[0]),d=>d.additions[0].id='ctenoimbricata',d=>d.authorization='pending',d=>d.formal_profile_acceptance='PASS',d=>d.hardware_gpu_verified=true,d=>d.target_scene_verified=true,d=>d.additions[0].source_commit='0'.repeat(40),d=>d.additions[0].review_commit='0'.repeat(40),d=>d.excluded_ids=[],d=>d.source_bundle.sha256='0'.repeat(64),d=>d.base_descriptor.path='../escape'])await mutate(file,change,()=>assert.rejects(collect));
 const entry=fixed.additions[0];
 for(const change of [m=>m.description.en='Exact scientific reconstruction',m=>m.sources=[],m=>m.sha256.glb='0'.repeat(64),m=>m.approval_provenance={approved_for_brief:true},m=>m.packs=['other']])await mutate(entry.metadata.path,change,async()=>{const metadata=await pin(entry.metadata.path);await mutate(file,d=>d.additions[0].metadata=metadata,()=>assert.rejects(collect));});
 for(const path of [manifest.assets[175].glb,manifest.assets[175].blend,entry.review.path,entry.artifacts.brief.path,entry.proof.path,entry.technical.rebuild_1.path,fixed.additions[4].review.path,fixed.source_bundle.path]){
  const bytes=await readFile(resolve(root,path));try{await writeFile(resolve(root,path),Buffer.concat([bytes,Buffer.from('tamper')]));await assert.rejects(collect,/hash mismatch/);checks++;}finally{await writeFile(resolve(root,path),bytes);}
 }
 console.log(`Concept-seven release: ${checks} checks passed; exact seven, unchanged 175, source/QA bindings and open formal/hardware gates preserved.`);
} finally {await rm(root,{recursive:true,force:true});}

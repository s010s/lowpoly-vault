/** Exact independent-QA scope; original candidate failures cannot be rewritten as approvals. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,cp,readFile,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
import {createHash} from 'node:crypto';
import {collectRound03Release,ROUND03_IDS} from './small-life-round03-release.mjs';
import {ACCEPTED_ROUND03_ASSETS} from './accepted-round03-release.mjs';
const root=await mkdtemp(join(tmpdir(),'vault-round03-')),file='assets/releases/small-life-round03-twelve-20261018.json';
const pin=async path=>({path,sha256:createHash('sha256').update(await readFile(resolve(root,path))).digest('hex')});let checks=0;
async function mutate(path,change,action){const bytes=await readFile(resolve(root,path));try{const data=JSON.parse(bytes);change(data);await writeFile(resolve(root,path),JSON.stringify(data));await action();checks++;}finally{await writeFile(resolve(root,path),bytes);}}
try{
 for(const path of ['scripts','package-lock.json','assets/initial-publication.json','assets/prehistoric','assets/revisions','assets/releases','assets/additions','assets/candidates/small-fauna-trio-v2','assets/candidates/continuous-small-life-20261018','assets/candidates/continuous-small-life-round02-20261018','assets/candidates/continuous-small-life-round03-20261018','experiments/structural-refinement-2026-10-17/accepted','qa/small-life-release-20261018/upstream','production/small-fauna-trio-v2','qa/small-fauna-trio-v2','production/continuous-release-20261018','production/continuous-small-life-20261018','qa/continuous-small-life-20261018','production/continuous-release-round02-20261018','production/continuous-small-life-round02-20261018','qa/continuous-release-round02-20261018/profile-checks','production/continuous-release-round03-20261018','production/continuous-small-life-round03-20261018','production/policies','qa/continuous-release-round03-20261018/profile-checks','qa/continuous-release-round03-20261018/texture-checks']){await mkdir(resolve(root,path,'..'),{recursive:true});await cp(path,resolve(root,path),{recursive:true});}
 const collect=async()=>collectRound03Release(root,await pin(file)),published=await collect(),release=JSON.parse(await readFile(resolve(root,file))),before=JSON.parse(await readFile('assets/manifest.json'));
 assert.equal(published.assets.length,55);assert.deepEqual(published.assets.slice(0,43),before.assets.slice(0,43));assert.deepEqual(published.assets.slice(43).map(a=>a.id).sort(),ROUND03_IDS);assert(published.assets.slice(43).every(a=>a.approval_provenance.candidate_record_approved_for_brief===false));checks++;
 for(const change of [d=>d.additions.pop(),d=>d.additions.push(d.additions[0]),d=>d.authorization='pending',d=>d.validation_profile='legacy-v1',d=>d.rule_version='future',d=>d.batches[0].sources[d.batches[0].ids[0]]='0'.repeat(40),d=>d.batches[1].review_commit='0'.repeat(40),d=>d.base_descriptor.path='../escape'])await mutate(file,change,()=>assert.rejects(collect));
 const entry=release.additions[0],id=entry.id;
 for(const change of [m=>m.name.en='unreviewed',m=>m.sources=[],m=>m.category='plants',m=>m.status='approved',m=>m.approval_provenance={approved_for_brief:true},m=>m.packs=['other']])await mutate(entry.metadata.path,change,async()=>{const metadata=await pin(entry.metadata.path);await mutate(file,d=>d.additions[0].metadata=metadata,()=>assert.rejects(collect));});
 const accepted=ACCEPTED_ROUND03_ASSETS[id];
 for(const path of [published.assets[43].glb,published.assets[43].blend,accepted.runtime.path,accepted.review.path,accepted.profile_result.path,accepted.profile_candidate.path,accepted.original_legacy_result.path]){const bytes=await readFile(resolve(root,path));try{await writeFile(resolve(root,path),Buffer.concat([bytes,Buffer.from('tamper')]));await assert.rejects(collect,/hash mismatch/);checks++;}finally{await writeFile(resolve(root,path),bytes);}}
 const isoxys=release.additions.find(a=>a.id==='isoxys');await mutate(isoxys.metadata.path,m=>m.placement_offset_y_m=0,async()=>{const metadata=await pin(isoxys.metadata.path);await mutate(file,d=>d.additions.find(a=>a.id==='isoxys').metadata=metadata,()=>assert.rejects(collect));});
 const olderPath=published.assets[0].glb,olderBytes=await readFile(resolve(root,olderPath));
 try{await writeFile(resolve(root,olderPath),Buffer.concat([olderBytes,Buffer.from('tamper')]));await assert.rejects(collect,error=>error.message.includes(olderPath)&&/hash|SHA|bytes|checksum/i.test(error.message));checks++;}finally{await writeFile(resolve(root,olderPath),olderBytes);}
 try{await rm(resolve(root,olderPath));await assert.rejects(collect,error=>error.code==='ENOENT'&&error.message.includes(olderPath));checks++;}finally{await writeFile(resolve(root,olderPath),olderBytes);}
 console.log(`Round03 release: ${checks} checks passed; exact twelve, unchanged forty-three, independent QA, explicit profile and preserved candidate failures.`);
}finally{await rm(root,{recursive:true,force:true});}

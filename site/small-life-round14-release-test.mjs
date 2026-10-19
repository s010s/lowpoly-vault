/** New release scope, immutable evidence, and preserved pending/hardware gates. */
import assert from 'node:assert/strict';
import {mkdtemp,readFile,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {collectRound14Release,ROUND14_IDS} from './small-life-round14-release.mjs';
import {ACCEPTED_ROUND14_ASSETS as accepted,SOURCE_BUNDLE} from './accepted-round14-release.mjs';
const root=await mkdtemp(join(tmpdir(),'vault-round14-')),file='assets/releases/small-life-round14-twelve-20261018.json';let checks=0;
const pin=async path=>({path,sha256:createHash('sha256').update(await readFile(resolve(root,path))).digest('hex')});
async function mutate(path,change,action){const bytes=await readFile(resolve(root,path));try{const data=JSON.parse(bytes);change(data);await writeFile(resolve(root,path),JSON.stringify(data));await action();checks++;}finally{await writeFile(resolve(root,path),bytes);}}
try{
 for(const dir of ['assets','production','qa','scripts','experiments','package-lock.json'])execFileSync('cp',['-a','--reflink=auto',dir,resolve(root,dir)]);
 const collect=async()=>collectRound14Release(root,await pin(file));
 const published=await collect(),before=JSON.parse(await readFile('assets/manifest.json'));
 assert.equal(published.assets.length,187);assert.deepEqual(published.assets.slice(0,175),before.assets.slice(0,175));assert.deepEqual(published.assets.slice(175).map(a=>a.id).sort(),ROUND14_IDS);assert(published.assets.slice(175).every(a=>a.approval_provenance.candidate_record_approved_for_brief===false));checks++;
 for(const id of ['sollasina','ottoia','eocladus','limestone-pavement','gryphaea','folded-strata-outcrop','volcanic-bomb','teredolites-wood-boring-cast',...ROUND14_IDS]){const p=published.assets.find(a=>a.id===id).approval_provenance;assert.equal(p.formal_profile_acceptance,'BLOCKED');assert.equal(p.hardware_gpu_verified,false);checks++;}
 for(const change of [d=>d.additions.pop(),d=>d.additions.push(d.additions[0]),d=>d.authorization='pending',d=>d.validation_profile='legacy-v1',d=>d.rule_version='future',d=>d.batches[0].handoff_commit='0'.repeat(40),d=>d.batches[1].review_commit='0'.repeat(40),d=>d.base_descriptor.path='../escape',d=>d.source_bundle.sha256='0'.repeat(64)])await mutate(file,change,()=>assert.rejects(collect));
 const entry=JSON.parse(await readFile(resolve(root,file))).additions[0];
 for(const change of [m=>m.name.en='unreviewed',m=>m.sources=[],m=>m.category='plants',m=>m.status='approved',m=>m.approval_provenance={approved_for_brief:true},m=>m.packs=['other'],m=>m.claim_scope='strict specimen',m=>m.reference_status='verified',m=>m.scientific_scope.en='Strict specimen'])await mutate(entry.metadata.path,change,async()=>{const metadata=await pin(entry.metadata.path);await mutate(file,d=>d.additions[0].metadata=metadata,()=>assert.rejects(collect));});
 const a=accepted[entry.id];
 for(const path of [published.assets[175].glb,published.assets[175].blend,a.review.path,a.candidate.path,a.profile_result.path,a.texture_audit.path,a.handoff.path,SOURCE_BUNDLE.path,accepted.conularia.review.path]){const bytes=await readFile(resolve(root,path));try{await writeFile(resolve(root,path),Buffer.concat([bytes,Buffer.from('tamper')]));await assert.rejects(collect,/hash mismatch/);checks++;}finally{await writeFile(resolve(root,path),bytes);}}
 console.log(`Round14 release: ${checks} checks passed; exact twelve, unchanged 175, immutable QA and pending formal/hardware gates.`);
}finally{await rm(root,{recursive:true,force:true});}

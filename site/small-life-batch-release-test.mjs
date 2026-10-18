/** Exercise release boundaries using disposable copies, preserving raw source/QA evidence. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,cp,readFile,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
import {createHash} from 'node:crypto';
import {collectSmallLifeBatchRelease,BATCH_IDS} from './small-life-batch-release.mjs';
import {ACCEPTED_BATCH_ASSETS} from './accepted-small-life-batch-data.mjs';
const root=await mkdtemp(join(tmpdir(),'vault-batch-')),file='assets/releases/small-life-twelve-20261018.json';
const pin=async path=>({path,sha256:createHash('sha256').update(await readFile(resolve(root,path))).digest('hex')});
let checks=0;
async function mutate(path,change,action){const bytes=await readFile(resolve(root,path));try{const data=JSON.parse(bytes);change(data);await writeFile(resolve(root,path),JSON.stringify(data));await action();checks++;}finally{await writeFile(resolve(root,path),bytes);}}
try{
 for(const path of ['assets/initial-publication.json','assets/prehistoric','assets/revisions','assets/releases','assets/additions','assets/candidates/small-fauna-trio-v2','assets/candidates/continuous-small-life-20261018','experiments/structural-refinement-2026-10-17/accepted','qa/small-life-release-20261018/upstream','production/small-fauna-trio-v2','qa/small-fauna-trio-v2','production/continuous-release-20261018','production/continuous-small-life-20261018','qa/continuous-small-life-20261018']){await mkdir(resolve(root,path,'..'),{recursive:true});await cp(path,resolve(root,path),{recursive:true});}
 const collect=async()=>collectSmallLifeBatchRelease(root,await pin(file)),published=await collect(),release=JSON.parse(await readFile(resolve(root,file)));
 assert.equal(published.assets.length,31);assert.deepEqual(published.assets.slice(19).map(a=>a.id).sort(),BATCH_IDS);checks++;
 for(const change of [d=>d.additions.pop(),d=>d.additions.push(d.additions[0]),d=>d.authorization='pending',d=>d.batches[0].source_commit='0'.repeat(40),d=>d.batches[1].review_commit='0'.repeat(40),d=>d.base_descriptor.path='../escape'])await mutate(file,change,()=>assert.rejects(collect));
 const entry=release.additions.find(a=>a.id==='hydropteris');
 for(const change of [m=>m.name.en='Hydropteris pinnata',m=>m.description.zh='unqualified',m=>m.category='animals',m=>m.revision='forged',m=>m.packs=['other']])await mutate(entry.metadata.path,change,async()=>{const metadata=await pin(entry.metadata.path);await mutate(file,d=>d.additions.find(a=>a.id==='hydropteris').metadata=metadata,()=>assert.rejects(collect));});
 const a=published.assets.find(a=>a.id==='hydropteris');
 for(const path of [a.glb,a.blend,ACCEPTED_BATCH_ASSETS.hydropteris.runtime.path,ACCEPTED_BATCH_ASSETS.hydropteris.review.path]){const bytes=await readFile(resolve(root,path));try{await writeFile(resolve(root,path),Buffer.concat([bytes,Buffer.from('tamper')]));await assert.rejects(collect,/hash mismatch/);checks++;}finally{await writeFile(resolve(root,path),bytes);}}
 console.log(`Twelve-asset release: ${checks} checks passed; exact source/QA bindings, corrected taxonomy, scope and immutable payloads.`);
}finally{await rm(root,{recursive:true,force:true});}

/** Disposable mutations prove scope and payload/evidence failures remain release blockers. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,cp,readFile,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
import {createHash} from 'node:crypto';
import {collectSmallFaunaRelease,FAUNA_IDS} from './small-fauna-release.mjs';
import {checkPublishedManifest} from './initial-release.mjs';
const root=await mkdtemp(join(tmpdir(),'vault-fauna-')),file='assets/releases/small-fauna-trio-v002-20261018.json';
const pin=async path=>({path,sha256:createHash('sha256').update(await readFile(resolve(root,path))).digest('hex')});
let checks=0;
async function mutate(path,change,action){const bytes=await readFile(resolve(root,path)),data=JSON.parse(bytes);change(data);try{await writeFile(resolve(root,path),JSON.stringify(data));await action();checks++;}finally{await writeFile(resolve(root,path),bytes);}}
try {
 for(const path of ['assets/initial-publication.json','assets/prehistoric','assets/revisions','assets/releases','assets/additions','assets/candidates/small-fauna-trio-v2','experiments/structural-refinement-2026-10-17/accepted','qa/small-life-release-20261018/upstream','production/small-fauna-trio-v2','qa/small-fauna-trio-v2']){await mkdir(resolve(root,path,'..'),{recursive:true});await cp(path,resolve(root,path),{recursive:true});}
 const collect=async()=>collectSmallFaunaRelease(root,await pin(file)),manifest=await collect(),release=JSON.parse(await readFile(resolve(root,file)));
 const before=JSON.parse(await readFile('assets/manifest.json'));assert.equal(manifest.assets.length,19);assert.deepEqual(manifest.assets.slice(0,16),before.assets.slice(0,16));assert.deepEqual(manifest.assets.slice(16).map(a=>a.id).sort(),FAUNA_IDS);checks++;
 for(const change of [d=>d.additions.pop(),d=>d.additions.push(d.additions[0]),d=>d.additions[0].id='wrong',d=>d.authorization='pending',d=>d.source_commit='0'.repeat(40),d=>d.base_descriptor.path='../escape'])await mutate(file,change,()=>assert.rejects(collect));
 const entry=release.additions[0];
 for(const change of [m=>m.name.en='unpinned',m=>m.glb='../outside.glb'])await mutate(entry.metadata.path,change,()=>assert.rejects(collect,/hash mismatch/));
 for(const change of [m=>m.category='plants',m=>m.revision='forged',m=>m.source_url='https://example.com',m=>m.packs=['another-pack']])await mutate(entry.metadata.path,change,async()=>{const metadata=await pin(entry.metadata.path);await mutate(file,d=>d.additions[0].metadata=metadata,()=>assert.rejects(collect));});
 for(const key of ['glb','blend','preview']){const meta=JSON.parse(await readFile(resolve(root,entry.metadata.path))),path=resolve(root,meta[key]),bytes=await readFile(path);try{await writeFile(path,Buffer.concat([bytes,Buffer.from('tamper')]));await assert.rejects(collect,/hash mismatch/);checks++;}finally{await writeFile(path,bytes);}}
 await writeFile(resolve(root,'assets/manifest.json'),JSON.stringify(manifest));assert.deepEqual(await checkPublishedManifest(root),manifest);checks++;
 await mutate('assets/manifest.json',m=>m.assets.push({...m.assets[18],id:'unapproved'}),()=>assert.rejects(()=>checkPublishedManifest(root),/exactly match/));
 console.log(`Small fauna release: ${checks} checks passed; exact accepted v002 payloads, original sixteen unchanged, authorization and metadata/evidence boundaries.`);
}finally{await rm(root,{recursive:true,force:true});}

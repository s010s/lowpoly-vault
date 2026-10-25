/** Snapshot tests do not claim new capture or visual approval for the old library. */
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,mkdtemp,rm} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {tmpdir} from 'node:os';
import {fileURLToPath} from 'node:url';
import index from './gallery/wheel-presentations-index.js';
import {wheelHash} from './wheel-presentation-contract.mjs';
import {assertWheelHistoricalExtension,wheelHistoricalBaseline} from './wheel-historical-baseline.mjs';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..'),base='qa/wheel-parity-20261024/presentation-evidence/';
const mb=await readFile(resolve(root,base+'baseline-manifest.json')),rb=await readFile(resolve(root,base+'baseline-resources.json'));
const manifest=JSON.parse(mb),resources=JSON.parse(rb);
assert.equal(wheelHash(mb),index.source_manifest_sha256);assert.equal(wheelHash(rb),index.source_resources_sha256);
function expanded(){const m=structuredClone(manifest),r=structuredClone(resources);m.assets.push({id:'new-test',sha256:{glb:'a'.repeat(64)}});r.posters['new-test']={detail:'gallery/posters/new-test.png',wheel:'gallery/posters/new-test-wheel.png'};r.files.push(...Object.values(r.posters['new-test']).map(path=>({path,bytes:40,sha256:'b'.repeat(64)})));return [m,r];}
test('original snapshot globals exactly match the authentic historical index',()=>{assert.equal(manifest.assets.length,594);assert.equal(Object.keys(index.presentations).length,242);assertWheelHistoricalExtension(manifest,resources,manifest,resources);});
test('strict additive new assets preserve every old594 metadata/poster/seal',()=>{const [m,r]=expanded();assertWheelHistoricalExtension(m,r,manifest,resources);assert.equal(m.assets.length,595);});
for(const [name,change] of [
 ['old metadata',(m)=>m.assets[0].name.en='changed'],['old source',(m)=>m.assets[400].sha256.glb='f'.repeat(64)],['old order',(m)=>m.assets.reverse()],['removed old asset',(m)=>m.assets.splice(5,1)],['duplicate ID',(m)=>m.assets.push(m.assets[0])],['old poster',(_,r)=>r.posters[manifest.assets[400].id].wheel='changed'],['old framing',(_,r)=>r.posters[manifest.assets[0].id].wheelSpec.zoom=7],['old file seal',(_,r)=>r.files[0].sha256='f'.repeat(64)],['removed old file',(_,r)=>r.files.shift()],['duplicate file',(_,r)=>r.files.push(r.files[0])],['unbound extra poster',(_,r)=>r.posters.unknown={wheel:'fake'}],['unbound extra file',(_,r)=>r.files.push({path:'gallery/unbound.png'})],['global resource provenance',(_,r)=>r.runtime_revision='changed'],
])test(name+' rejected on extended catalog',()=>{const [m,r]=expanded();change(m,r);assert.throws(()=>assertWheelHistoricalExtension(m,r,manifest,resources));});
await test('fallback authenticates exact historical globals, not mutable re-signed snapshot',async()=>{
 const temp=await mkdtemp(resolve(tmpdir(),'wheel-history-'));async function put(path,data){await mkdir(dirname(resolve(temp,path)),{recursive:true});await writeFile(resolve(temp,path),data);}
 try{
  const [m,r]=expanded();await put('assets/manifest.json',JSON.stringify(m));await put('site/public/gallery/resources.json',JSON.stringify(r));await put(base+'baseline-manifest.json',mb);await put(base+'baseline-resources.json',rb);
  const historical=await wheelHistoricalBaseline(temp,m,r,index);assert.deepEqual(historical,{manifest,resources});
  await assert.rejects(()=>wheelHistoricalBaseline(temp,manifest,r,index));
  await put(base+'baseline-manifest.json',Buffer.concat([mb,Buffer.from(' ')]));await assert.rejects(()=>wheelHistoricalBaseline(temp,m,r,index),/Historical manifest snapshot changed/);
  await put(base+'baseline-manifest.json',mb);await put(base+'baseline-resources.json',Buffer.concat([rb,Buffer.from(' ')]));await assert.rejects(()=>wheelHistoricalBaseline(temp,m,r,index),/Historical resources snapshot changed/);
 }finally{await rm(temp,{recursive:true,force:true});}
});

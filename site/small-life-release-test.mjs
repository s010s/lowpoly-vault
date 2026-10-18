/** Regression tests mutate disposable release copies; source models and approvals remain untouched. */
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, cp, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { createHash } from 'node:crypto';
import { collectSmallLifeRelease, SMALL_LIFE_IDS } from './small-life-release.mjs';
import { collectRefinedRelease } from './refined-release.mjs';
import { checkPublishedManifest } from './initial-release.mjs';
const root=await mkdtemp(join(tmpdir(),'vault-small-life-')),file='assets/releases/small-life-six-20261018.json';
const sha=data=>createHash('sha256').update(data).digest('hex');
const save=(path,data)=>writeFile(resolve(root,path),JSON.stringify(data,null,2)+'\n');
const pin=async path=>({path,sha256:sha(await readFile(resolve(root,path)))});
let checks=0;
async function check(action){await action();checks++;}
async function mutate(path,change,action){const bytes=await readFile(resolve(root,path)),data=JSON.parse(bytes);change(data);try{await save(path,data);await action();}finally{await writeFile(resolve(root,path),bytes);}}
try {
  for(const path of ['assets/initial-publication.json','assets/prehistoric','assets/revisions','assets/releases','assets/additions','experiments/structural-refinement-2026-10-17/accepted','qa/small-life-release-20261018/upstream']) {
    await mkdir(resolve(root,path,'..'),{recursive:true}); await cp(path,resolve(root,path),{recursive:true});
  }
  const collect=async()=>collectSmallLifeRelease(root,await pin(file));
  const manifest=await collect(),descriptor=JSON.parse(await readFile(resolve(root,file)));
  await check(async()=>{assert.equal(manifest.assets.length,16);assert.deepEqual(manifest.assets.slice(0,10),(await collectRefinedRelease(root,descriptor.base_descriptor)).assets);assert.deepEqual(manifest.assets.slice(10).map(a=>a.id).sort(),SMALL_LIFE_IDS);});
  for(const change of [d=>d.additions.pop(),d=>d.additions.push({...d.additions[0],id:'dapedium'}),d=>d.additions[1].id=d.additions[0].id,d=>d.authorization='unreviewed',d=>d.authorization_reference='unknown'])await check(()=>mutate(file,change,()=>assert.rejects(collect)));
  await check(()=>mutate(descriptor.additions[0].metadata.path,d=>d.name.en='Stale change',()=>assert.rejects(collect,/hash mismatch/)));
  for(const key of ['glb','blend','preview'])await check(async()=>{const m=JSON.parse(await readFile(resolve(root,descriptor.additions[0].metadata.path))),path=resolve(root,m[key]),bytes=await readFile(path);try{await writeFile(path,Buffer.concat([bytes,Buffer.from('tamper')]));await assert.rejects(collect,/hash mismatch/);}finally{await writeFile(path,bytes);}});
  const entry=descriptor.additions[0];
  // Explicitly re-pin deliberately changed metadata to prove semantic validation is not just hashing.
  for(const change of [m=>m.category='geology',m=>m.turntable={},m=>m.revision='forged',m=>m.preview='../escape.png'])await check(()=>mutate(entry.metadata.path,change,async()=>{const updated=await pin(entry.metadata.path);await mutate(file,d=>d.additions[0].metadata=updated,()=>assert.rejects(collect));}));
  await check(()=>mutate(entry.runtime.path,r=>r.status='fail',async()=>{const updated=await pin(entry.runtime.path);await mutate(file,d=>{for(const a of d.additions)if(a.runtime.path===updated.path)a.runtime=updated;},()=>assert.rejects(collect));}));
  await check(async()=>{await save('assets/manifest.json',manifest);assert.deepEqual(await checkPublishedManifest(root),manifest);await mutate('assets/manifest.json',m=>m.assets.push({...m.assets[10],id:'callichimaera'}),()=>assert.rejects(()=>checkPublishedManifest(root),/exactly match/));});
  console.log(`Small-life release: ${checks} checks passed; exact six additions, untouched ten originals, payload/evidence pins, scope and metadata mutation refusals.`);
} finally { await rm(root,{recursive:true,force:true}); }

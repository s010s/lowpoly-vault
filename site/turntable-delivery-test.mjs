import assert from 'node:assert/strict';
import { readFile, writeFile, mkdtemp, mkdir, cp, rm, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { collectTurntables, webpDimensions, publishedImagePaths } from './turntable-delivery.mjs';
import { collectInitialRelease } from './initial-release.mjs';
const root=process.cwd(),manifest=JSON.parse(await readFile('assets/manifest.json'));const hash=b=>createHash('sha256').update(b).digest('hex');
const initial=await collectTurntables(manifest);assert.equal(initial.descriptors.size,10);assert.equal(initial.files.length,260);let checks=1;
const temp=await mkdtemp(resolve(tmpdir(),'vault-turntables-'));
try{
 await mkdir(resolve(temp,'assets'),{recursive:true});await cp(resolve(root,'assets/turntables'),resolve(temp,'assets/turntables'),{recursive:true});await cp(resolve(root,'assets/card-previews'),resolve(temp,'assets/card-previews'),{recursive:true});
 const indexPath=resolve(temp,'assets/turntables/index.json'),indexBytes=await readFile(indexPath),index=JSON.parse(indexBytes),first=index.assets[0],dataPath=resolve(temp,first.manifest),dataBytes=await readFile(dataPath),data=JSON.parse(dataBytes),framePath=resolve(temp,data.frames[0].path),frameBytes=await readFile(framePath);
 assert.deepEqual(webpDimensions(frameBytes),[data.width,data.height]);assert.throws(()=>webpDimensions(Buffer.from('not webp')));checks+=2;
 async function invalidIndex(mutate){const changed=structuredClone(index);mutate(changed);await writeFile(indexPath,JSON.stringify(changed));await assert.rejects(collectTurntables(manifest,temp));await writeFile(indexPath,indexBytes);checks++;}
 await invalidIndex(i=>i.assets[0].id='unpublished-candidate');await invalidIndex(i=>i.assets.push(i.assets[0]));await invalidIndex(i=>i.assets[0].manifest='../escape.json');await invalidIndex(i=>i.assets[0].source_glb_sha256='b'.repeat(64));await invalidIndex(i=>i.assets[0].manifest_sha256='b'.repeat(64));
 async function invalidManifest(mutate){const changed=structuredClone(data);mutate(changed);const bytes=Buffer.from(JSON.stringify(changed));await writeFile(dataPath,bytes);const next=structuredClone(index);next.assets[0].manifest_sha256=hash(bytes);await writeFile(indexPath,JSON.stringify(next));await assert.rejects(collectTurntables(manifest,temp));await writeFile(dataPath,dataBytes);await writeFile(indexPath,indexBytes);checks++;}
 await invalidManifest(d=>d.total_bytes++);await invalidManifest(d=>d.frames[0].path='assets/turntables/natural-arch/../outside.webp');await invalidManifest(d=>d.width=511);await invalidManifest(d=>d.frames[0].sha256='b'.repeat(64));
 await writeFile(framePath,Buffer.from('corrupt'));await assert.rejects(collectTurntables(manifest,temp));await writeFile(framePath,frameBytes);checks++;
 const outside=resolve(temp,'outside.webp');await writeFile(outside,frameBytes);await rm(framePath);await symlink(outside,framePath);await assert.rejects(collectTurntables(manifest,temp));checks++;
 assert.equal((await collectTurntables(await collectInitialRelease(root),await mkdtemp(resolve(temp,'empty-')))).descriptors.size,0);checks++;
}finally{await rm(temp,{recursive:true,force:true});}
console.log(JSON.stringify({status:'pass',checks,assets:initial.descriptors.size,frames:initial.files.length-initial.descriptors.size-initial.posters.size,source:'immutable original GLB hashes',coverage:'sealed metadata/bytes/dimensions/path allowlist/symlink rejection/static-only fallback'}));

// Synthetic mixed-manifest routing fixture only. This does not approve any real refinement.
const mixedRoot=await mkdtemp(resolve(tmpdir(),'vault-revision-turntables-'));
let revisionChecks=0;
try {
 await mkdir(resolve(mixedRoot,'assets'),{recursive:true});
 await cp(resolve(root,'assets/turntables'),resolve(mixedRoot,'assets/turntables'),{recursive:true});
 await cp(resolve(root,'assets/card-previews'),resolve(mixedRoot,'assets/card-previews'),{recursive:true});
 // Construct the synthetic seed from immutable originals, even after the real
 // source catalog has selected accepted revisions. Current publication state
 // must never leak accepted markers or double revision segments into fixtures.
 const seedManifest=await collectInitialRelease(root);
 const seedIndex={version:1,render_preset_sha256:initial.descriptors.size?JSON.parse(await readFile(resolve(root,'assets/turntables/index.json'))).render_preset_sha256:undefined,assets:[],posters:[]};
 for(const asset of seedManifest.assets){
  const paths=publishedImagePaths(asset,seedManifest),bytes=await readFile(resolve(root,paths.manifest)),sequence=JSON.parse(bytes),posterBytes=await readFile(resolve(root,paths.poster));
  seedIndex.assets.push({id:asset.id,manifest:paths.manifest,source_glb_sha256:asset.sha256.glb,manifest_sha256:hash(bytes)});
  seedIndex.posters.push({id:asset.id,path:paths.poster,sha256:hash(posterBytes),bytes:posterBytes.length,width:sequence.width,height:sequence.height,source_glb_sha256:asset.sha256.glb,render_preset_sha256:sequence.render_preset_sha256});
 }
 await writeFile(resolve(mixedRoot,'assets/turntables/index.json'),JSON.stringify(seedIndex));
 const initialFixture=await collectTurntables(seedManifest,mixedRoot);
 const mixed=structuredClone(seedManifest);mixed.release_status='mixed';mixed.quality_status='mixed';mixed.publication={approved_asset_ids:['natural-arch']};
 const revised=mixed.assets.find(a=>a.id==='natural-arch'),revision='r002-test';
 revised.revision=revision;revised.quality_status='accepted_for_brief';
 for(const key of ['glb','blend','preview'])revised[key]=`assets/revisions/${revised.id}/${revision}/${key==='preview'?'preview.webp':`${revised.id}.${key}`}`;
 revised.sha256.glb='a'.repeat(64);
 const indexPath=resolve(mixedRoot,'assets/turntables/index.json'),index=JSON.parse(await readFile(indexPath));
 const item=index.assets.find(a=>a.id===revised.id),poster=index.posters.find(a=>a.id===revised.id);
 const originalPath=item.manifest,originalBytes=await readFile(resolve(mixedRoot,originalPath)),originalData=JSON.parse(originalBytes);
 const originalFrameBytes=await Promise.all(originalData.frames.map(f=>readFile(resolve(mixedRoot,f.path))));
 const originalPosterPath=poster.path,originalPoster=await readFile(resolve(mixedRoot,poster.path));
 const nextPath=item.manifest.replace(`/${revised.id}/`,`/${revised.id}/${revision}/`),nextFolder=nextPath.slice(0,nextPath.lastIndexOf('/'));
 await cp(resolve(mixedRoot,originalPath.slice(0,originalPath.lastIndexOf('/'))),resolve(mixedRoot,nextFolder),{recursive:true});
 const data=structuredClone(originalData);data.source_glb_sha256=revised.sha256.glb;
 data.frames=data.frames.map((f,i)=>({...f,path:`${nextFolder}/frame-${String(i).padStart(3,'0')}.webp`}));
 const dataPath=resolve(mixedRoot,nextPath),dataBytes=Buffer.from(JSON.stringify(data));await writeFile(dataPath,dataBytes);
 Object.assign(item,{manifest:nextPath,manifest_sha256:hash(dataBytes),source_glb_sha256:revised.sha256.glb});
 poster.path=poster.path.replace(`${revised.id}-`,`${revised.id}-${revision}-`);poster.source_glb_sha256=revised.sha256.glb;
 await writeFile(resolve(mixedRoot,poster.path),originalPoster);revised.sha256.preview=poster.sha256;
 const indexBytes=Buffer.from(JSON.stringify(index));await writeFile(indexPath,indexBytes);
 async function checkRevision(name,action){try{await action();revisionChecks++;}catch(error){error.message=`${name}: ${error.message}`;throw error;}}
 async function invalidMixed(name,mutate,pattern){await checkRevision(name,async()=>{const changed=structuredClone(mixed);mutate(changed);await assert.rejects(()=>collectTurntables(changed,mixedRoot),pattern);});}
 async function invalidRevisionIndex(name,mutate,pattern){await checkRevision(name,async()=>{const changed=structuredClone(index);mutate(changed);try{await writeFile(indexPath,JSON.stringify(changed));await assert.rejects(()=>collectTurntables(mixed,mixedRoot),pattern);}finally{await writeFile(indexPath,indexBytes);}});}
 async function invalidRevisionData(name,mutate,pattern){await checkRevision(name,async()=>{const changed=structuredClone(data);mutate(changed);const bytes=Buffer.from(JSON.stringify(changed)),next=structuredClone(index);next.assets.find(a=>a.id===revised.id).manifest_sha256=hash(bytes);try{await writeFile(dataPath,bytes);await writeFile(indexPath,JSON.stringify(next));await assert.rejects(()=>collectTurntables(mixed,mixedRoot),pattern);}finally{await writeFile(dataPath,dataBytes);await writeFile(indexPath,indexBytes);}});}
 await checkRevision('missing index cannot omit accepted revision sequences and posters',async()=>{const empty=await mkdtemp(resolve(tmpdir(),'vault-mixed-missing-index-'));try{await assert.rejects(()=>collectTurntables(mixed,empty),/require a sealed turntable index/);}finally{await rm(empty,{recursive:true,force:true});}});
 await checkRevision('accepted revision routes are deterministic and original routes are retained',async()=>{
  const collected=await collectTurntables(mixed,mixedRoot);
  assert.equal(collected.descriptors.size,10);assert.equal(collected.posters.size,10);assert.equal(collected.files.length,260);
  assert.equal(collected.descriptors.get(revised.id).manifest,nextPath);assert.equal(collected.posters.get(revised.id),poster.path);
  assert(!collected.files.includes(originalPath));assert(!collected.files.includes(originalPosterPath));
  for(const frame of data.frames)assert(collected.files.includes(frame.path));
  for(const asset of seedManifest.assets.filter(a=>a.id!==revised.id)){
   assert.equal(collected.descriptors.get(asset.id).manifest,initialFixture.descriptors.get(asset.id).manifest);
   assert.equal(collected.posters.get(asset.id),initialFixture.posters.get(asset.id));
  }
 });
 await invalidMixed('reject revision routes on an initial release',m=>{m.release_status='initial';},/explicitly authorized mixed-release/);
 await invalidMixed('reject blanket mixed approval',m=>{m.quality_status='approved';},/explicitly authorized mixed-release/);
 await invalidMixed('reject review-only revision',m=>{m.review_only=true;},/explicitly authorized mixed-release/);
 await invalidMixed('reject revision outside approved IDs',m=>{m.publication.approved_asset_ids=[];},/explicitly authorized mixed-release/);
 await invalidMixed('reject unaccepted revision',m=>{m.assets.find(a=>a.id===revised.id).quality_status='work_in_progress';},/individually accepted/);
 await invalidMixed('reject absent accepted revision',m=>{delete m.assets.find(a=>a.id===revised.id).revision;},/revision identifier/);
 for(const value of ['../outside','/absolute','r002/child','r002%2foutside','r002\\outside','r002?query','r002#fragment','.', '..']){
  await invalidMixed(`reject unsafe revision ${value}`,m=>{m.assets.find(a=>a.id===revised.id).revision=value;},/revision identifier/);
 }
 await invalidMixed('reject revision different from released storage',m=>{m.assets.find(a=>a.id===revised.id).revision='r003';},/storage revision/);
 await invalidMixed('reject arbitrary accepted asset ID',m=>{m.assets.find(a=>a.id===revised.id).id='unapproved';m.publication.approved_asset_ids=['unapproved'];},/explicitly authorized mixed-release/);
 await invalidMixed('reject duplicate published IDs',m=>{m.assets.push(m.assets[0]);},/Duplicate published/);
 await invalidMixed('reject poster absent from approved preview',m=>{m.assets.find(a=>a.id===revised.id).sha256.preview='0'.repeat(64);},/approved published preview/);
 await invalidRevisionIndex('reject legacy manifest path for revised model',i=>{i.assets[0].manifest=originalPath;});
 await invalidRevisionIndex('reject arbitrary manifest route',i=>{i.assets[0].manifest='assets/turntables/natural-arch/r002-test/arbitrary.json';});
 await invalidRevisionIndex('reject cross-revision manifest route',i=>{i.assets[0].manifest=nextPath.replace(revision,'r999');});
 await invalidRevisionIndex('reject revised route for WIP original',i=>{i.assets[1].manifest=i.assets[1].manifest.replace('/v2-','/unapproved/v2-');});
 await invalidRevisionIndex('reject old poster path for revised asset',i=>{i.posters[0].path=originalPosterPath;});
 await invalidRevisionIndex('reject arbitrary poster route',i=>{i.posters[0].path='assets/card-previews/unapproved.webp';});
 await invalidRevisionIndex('reject source hash drift',i=>{i.assets[0].source_glb_sha256='b'.repeat(64);});
 await invalidRevisionIndex('reject poster source hash drift',i=>{i.posters[0].source_glb_sha256='b'.repeat(64);});
 await invalidRevisionIndex('reject poster preset drift',i=>{i.posters[0].render_preset_sha256='b'.repeat(64);});
 await invalidRevisionIndex('reject missing revised sequence',i=>{i.assets=i.assets.filter(a=>a.id!==revised.id);},/require the accepted revision sequence/);
 await invalidRevisionIndex('reject different poster frame',i=>{i.posters[0].sha256=data.frames[1].sha256;i.posters[0].bytes=data.frames[1].bytes;},/match frame 0/);
 await invalidRevisionIndex('reject poster byte count mismatch',i=>{i.posters[0].bytes++;},/bytes must match frame 0/);
 await invalidRevisionData('reject repinned wrong frame azimuth',d=>{d.frames[0].azimuth_deg=999;},/azimuth/);
 await invalidRevisionData('reject repinned wrong frame elevation',d=>{d.frames[0].elevation_deg=-999;},/elevation/);
 await invalidRevisionData('reject repinned nonfinite frame angle',d=>{d.frames[0].azimuth_deg=Infinity;},/azimuth/);
 await invalidRevisionData('reject repinned missing frame angle',d=>{delete d.frames[0].azimuth_deg;},/azimuth/);
 await invalidRevisionData('reject repinned incorrect frame view',d=>{d.frames[0].view='incorrect';},/view must be turntable/);
 await invalidRevisionData('reject alternate frame filename',d=>{d.frames[0].path=`${nextFolder}/unapproved.webp`;},/deterministic ordered frame/);
 await invalidRevisionData('reject nested arbitrary frame path',d=>{d.frames[0].path=`${nextFolder}/nested/frame-000.webp`;},/deterministic ordered frame/);
 await invalidRevisionData('reject original frame alias',d=>{d.frames[0].path=originalData.frames[0].path;},/unsafe turntable frame/);
 await invalidRevisionData('reject revision path traversal',d=>{d.frames[0].path=`${nextFolder}/../outside.webp`;},/unsafe turntable frame/);
 await invalidRevisionData('reject frame permutation',d=>{[d.frames[0],d.frames[1]]=[d.frames[1],d.frames[0]];},/deterministic ordered frame/);
 await invalidRevisionData('reject changed frame checksum',d=>{d.frames[0].sha256='0'.repeat(64);},/frame changed/);
 await invalidRevisionData('reject missing declared alpha',d=>{d.alpha=false;});
 await invalidRevisionData('reject opaque background',d=>{d.background='white';});
 await invalidRevisionData('reject nonzero poster frame',d=>{d.poster_index=1;},/poster must be frame 0/);
 await invalidRevisionData('reject wrong revision dimensions',d=>{d.width=512;});
 await invalidRevisionData('reject revision quality drift',d=>{d.quality=0.7;});
 await invalidRevisionData('reject revision renderer preset drift',d=>{d.render_preset_sha256='0'.repeat(64);});
 const firstFramePath=resolve(mixedRoot,data.frames[0].path),frameBytes=await readFile(firstFramePath);
 assert.equal(frameBytes.toString('ascii',12,16),'VP8X');
 const noAlpha=Buffer.from(frameBytes);noAlpha[20]&=~0x10;
 try{await writeFile(firstFramePath,noAlpha);await invalidRevisionData('reject absent encoded alpha even when declared and repinned',d=>{d.frames[0].sha256=hash(noAlpha);},/encoded alpha/);}
 finally{await writeFile(firstFramePath,frameBytes);}
 for(const [name,path,bytes] of [['frame',firstFramePath,frameBytes],['poster',resolve(mixedRoot,poster.path),originalPoster],['metadata',dataPath,dataBytes]]){
  await checkRevision(`reject ${name} symlink outside its publication path`,async()=>{
   const outside=resolve(mixedRoot,`outside-${name}`);await writeFile(outside,bytes);await rm(path);await symlink(outside,path);
   try{await assert.rejects(()=>collectTurntables(mixed,mixedRoot),/symlink/);}finally{await rm(path);await writeFile(path,bytes);await rm(outside);}
  });
 }
 await checkRevision('all original image and sequence bytes remain untouched',async()=>{
  assert.deepEqual(await readFile(resolve(mixedRoot,originalPath)),originalBytes);
  assert.deepEqual(await readFile(resolve(mixedRoot,originalPosterPath)),originalPoster);
  for(const [i,frame] of originalData.frames.entries())assert.deepEqual(await readFile(resolve(mixedRoot,frame.path)),originalFrameBytes[i]);
  assert.equal((await collectTurntables(mixed,mixedRoot)).files.length,260);
 });
 console.log(`Revision turntable delivery tests passed: ${revisionChecks} checks; deterministic accepted-revision routes, original paths/bytes preserved, exact preset/alpha, frame-0/approved-preview equality, no arbitrary routes.`);
} finally {await rm(mixedRoot,{recursive:true,force:true});}

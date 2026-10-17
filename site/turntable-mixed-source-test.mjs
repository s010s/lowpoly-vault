/** Synthetic source-state regression. This never creates real asset approval. */
import assert from 'node:assert/strict';
import {cp,mkdir,mkdtemp,readFile,writeFile,rm} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {tmpdir} from 'node:os';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {collectInitialRelease} from './initial-release.mjs';
import {publishedImagePaths,collectTurntables} from './turntable-delivery.mjs';
import {REFINABLE_ASSET_IDS} from './refined-release.mjs';
const source=process.cwd(),root=await mkdtemp(resolve(tmpdir(),'vault-already-mixed-'));
const hash=b=>createHash('sha256').update(b).digest('hex');
async function copy(path){await mkdir(dirname(resolve(root,path)),{recursive:true});await cp(resolve(source,path),resolve(root,path));}
try {
 const original=await collectInitialRelease(source),mixed=structuredClone(original);
 Object.assign(mixed,{release_status:'mixed',quality_status:'mixed',publication:{approved_asset_ids:[...REFINABLE_ASSET_IDS]}});
 await copy('assets/initial-publication.json');
 await cp(resolve(source,'assets/turntables'),resolve(root,'assets/turntables'),{recursive:true});
 await cp(resolve(source,'assets/card-previews'),resolve(root,'assets/card-previews'),{recursive:true});
 const index={version:1,assets:[],posters:[]};
 for(const asset of original.assets){
  for(const path of [asset.glb,asset.blend,asset.preview,`${dirname(asset.glb)}/metadata.json`,`${dirname(asset.glb)}/qa.json`])await copy(path);
  const before=publishedImagePaths(asset,original),data=JSON.parse(await readFile(resolve(source,before.manifest)));
  const posterBytes=await readFile(resolve(source,before.poster));
  const selected=mixed.assets.find(item=>item.id===asset.id);
  if(REFINABLE_ASSET_IDS.includes(asset.id)){
   selected.revision='synthetic-source';selected.quality_status='accepted_for_brief';
   const folder=`assets/revisions/${asset.id}/${selected.revision}`;
   Object.assign(selected,{glb:`${folder}/${asset.id}.glb`,blend:`${folder}/${asset.id}.blend`,preview:`${folder}/preview.webp`});
   selected.sha256.preview=hash(posterBytes);
   await mkdir(resolve(root,folder),{recursive:true});
   await cp(resolve(source,asset.glb),resolve(root,selected.glb));
   await cp(resolve(source,asset.blend),resolve(root,selected.blend));
   await writeFile(resolve(root,selected.preview),posterBytes);
  }
  const after=publishedImagePaths(selected,mixed);
  if(before.manifest!==after.manifest){
   await cp(resolve(source,dirname(before.manifest)),resolve(root,dirname(after.manifest)),{recursive:true});
   data.frames=data.frames.map((frame,i)=>({...frame,path:`${dirname(after.manifest)}/frame-${String(i).padStart(3,'0')}.webp`}));
  }
  const bytes=Buffer.from(JSON.stringify(data));await writeFile(resolve(root,after.manifest),bytes);
  await writeFile(resolve(root,after.poster),posterBytes);
  index.render_preset_sha256=data.render_preset_sha256;
  index.assets.push({id:asset.id,manifest:after.manifest,manifest_sha256:hash(bytes),source_glb_sha256:asset.sha256.glb});
  index.posters.push({id:asset.id,path:after.poster,sha256:hash(posterBytes),bytes:posterBytes.length,width:data.width,height:data.height,source_glb_sha256:asset.sha256.glb,render_preset_sha256:data.render_preset_sha256});
 }
 await writeFile(resolve(root,'assets/manifest.json'),JSON.stringify(mixed));
 await writeFile(resolve(root,'assets/turntables/index.json'),JSON.stringify(index));
 assert.equal((await collectTurntables(mixed,root)).descriptors.size,10);
 const {stdout}=await promisify(execFile)(process.execPath,[fileURLToPath(new URL('./turntable-delivery-test.mjs',import.meta.url))],{cwd:root,maxBuffer:2*1024*1024});
 assert(stdout.includes('Revision turntable delivery tests passed:'));
 console.log('Mixed-source regression passed: full original and synthetic revision test suites run after source selection of all three revision routes. No real assets approved.');
} finally {await rm(root,{recursive:true,force:true});}

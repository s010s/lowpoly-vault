/** Integration of already-reviewed models: existence, one build, packaging. Not model QA. */
import assert from 'node:assert/strict';
import {checkGlbSizes} from './glb-size-gate.mjs';
import {checkReleaseGlbSizes} from './glb-release-size-gate.mjs';
import {checkReleaseGlbMaterials,DEFAULT_MATERIAL_BASELINE_COMMIT} from './glb-material-gate.mjs';
import {readFile,writeFile,mkdir,cp,stat,realpath,readdir,rm} from 'node:fs/promises';
import {resolve,dirname,sep} from 'node:path';
import {pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';
import {clearDeliveredAssets,deliverManifestAssets} from './asset-delivery.mjs';
import {writeCatalog} from './catalog-build.mjs';
import {releaseCatalogPath} from './release-catalog-path.js';
import {writeGalleryCatalog} from './gallery/catalog-build.mjs';
import {writeStaticRoutes} from './static-routes.mjs';
export async function copyPublicMember(root,out,path){
 assert(typeof path==='string'&&!/[\\\u0000-\u001f?#%]/.test(path)&&!path.startsWith('/')&&path.split('/').every(x=>x&&x!=='.'&&x!=='..'),'Unsafe delivery path');
 const source=resolve(root,path);assert((await realpath(source)).startsWith(resolve(root)+sep),'Delivery escapes source');
 const info=await stat(source);assert(info.isFile()&&info.size,'Empty delivery member '+path);
 await mkdir(dirname(resolve(out,path)),{recursive:true});await cp(source,resolve(out,path));
}
export async function deliverLegacyMedia(manifest,{root=process.cwd(),out='dist'}={}){
 // Compatibility data only; no batch collector or historical QA replay.
 const index=JSON.parse(await readFile(resolve(root,'assets/turntables/index.json')));
 const byId=new Map(manifest.assets.map(a=>[a.id,a]));
 for(const row of index.posters||[]){const asset=byId.get(row.id);if(!asset||asset.production_posters||row.source_glb_sha256!==asset.sha256?.glb)continue;await copyPublicMember(root,out,row.path);asset.card_preview=row.path;}
 for(const row of index.assets||[]){const asset=byId.get(row.id);if(!asset||asset.production_posters||row.source_glb_sha256!==asset.sha256?.glb)continue;
  const data=JSON.parse(await readFile(resolve(root,row.manifest)));await copyPublicMember(root,out,row.manifest);
  for(const frame of data.frames)await copyPublicMember(root,out,frame.path);
  asset.turntable={manifest:row.manifest,source_glb_sha256:row.source_glb_sha256,frame_count:data.frame_count,width:data.width,height:data.height,poster_index:data.poster_index,total_bytes:data.total_bytes};
 }
 return manifest;
}
export async function pruneUnusedPublicPosters(manifest,delivery,{root=process.cwd(),out='dist'}={}){
 const resources=JSON.parse(await readFile(resolve(root,'site/public/gallery/resources.json'),'utf8'));
 const keep=new Set();
 for(const model of delivery?.models||[])for(const file of Object.values(model.files||{}))if(file?.path?.startsWith('site/public/'))keep.add(file.path.slice('site/public/'.length));
 for(const a of manifest?.assets||[])for(const role of ['wheel','detail']){const p=resources.posters?.[a.id]?.[role];if(typeof p==='string'&&p)keep.add(p);}
 let removedFiles=0,removedBytes=0;
 async function walk(dir,relPrefix,isTop){
  let entries;
  try{entries=await readdir(dir,{withFileTypes:true});}catch(error){if(error.code==='ENOENT')return;throw error;}
  for(const entry of entries){
   const rel=relPrefix?`${relPrefix}/${entry.name}`:entry.name,full=resolve(dir,entry.name);
   if(rel==='gallery/scale-reference')continue;
   if(entry.isDirectory()){
    await walk(full,rel,false);
   }else if(entry.isFile()&&/\.(?:png|webp|jpe?g)$/i.test(entry.name)&&!keep.has(rel)){
    removedBytes+=(await stat(full)).size;removedFiles++;await rm(full,{force:true});
   }
  }
  if(!isTop&&(await readdir(dir)).length===0)await rm(dir,{recursive:true,force:true});
 }
 for(const folder of ['gallery','wheel-presentations','detail-presentations'])await walk(resolve(out,folder),folder,folder==='gallery');
 return {removedFiles,removedBytes};
}
export async function buildSimple(){
 const started=performance.now(),source=JSON.parse(await readFile('assets/manifest.json'));
 assert(!source.review_only,'Review-only manifests cannot be deployed');
 const byteBudget=await checkReleaseGlbSizes({manifest:source,baselineCommit:process.env.GLB_SIZE_BASELINE_COMMIT||'dfa8877b3a74959ce514c4c1dea93351d1a4f952'});
 console.log(`GLB byte gate: ${byteBudget.changed_count} new/replaced files pass; ${byteBudget.legacy_oversize.length} unchanged legacy files exceed 5 MB and are not certified by this release.`);
 const materialGate=await checkReleaseGlbMaterials({manifest:source,baselineCommit:process.env.GLB_MATERIAL_BASELINE_COMMIT||DEFAULT_MATERIAL_BASELINE_COMMIT});
 console.log(`GLB material gate: ${materialGate.changed_count} new/replaced files pass (${materialGate.unchanged_count} unchanged baseline files skipped).`);
 const {checkDelivery}=await import('./unified-delivery-contract.mjs');
 const delivery=await checkDelivery({root:process.cwd()});
 if(/^[a-f0-9]{40}$/.test(process.env.GITHUB_SHA||'')) process.env.VITE_RELEASE_CATALOG_TOKEN=process.env.GITHUB_SHA;
 const build=spawnSync(process.execPath,['node_modules/vite/bin/vite.js','build'],{stdio:'inherit'});assert.equal(build.status,0,build.error?.message||'Vite failed');
 await clearDeliveredAssets('dist');
 const pruned=await pruneUnusedPublicPosters(source,delivery,{out:'dist'});
 if(pruned.removedFiles)console.log(`Pruned ${pruned.removedFiles} unreferenced poster files (${(pruned.removedBytes/1e6).toFixed(1)} MB) from dist.`);
 let manifest=await deliverManifestAssets(source,'dist',{verifyHashes:false});
 manifest=await deliverLegacyMedia(manifest);
 const changedAssets=manifest.assets.filter(a=>byteBudget.changed_ids.includes(a.id));
 if(changedAssets.length)await checkGlbSizes({assets:changedAssets},{root:'dist'});
 await writeFile('dist/glb-byte-budget.json',JSON.stringify(byteBudget,null,2)+'\n');
 await writeFile('dist/glb-material-gate.json',JSON.stringify(materialGate,null,2)+'\n');
 await writeFile('dist/assets/manifest.json',JSON.stringify(manifest,null,2)+'\n');
 await writeCatalog(manifest,'dist',{approvedOnly:true});
 await writeGalleryCatalog(manifest,'dist');
 for(const path of ['LICENSE','THIRD_PARTY_NOTICES.md'])await cp(path,resolve('dist',path));
 await cp('LICENSES','dist/LICENSES',{recursive:true});
 await writeStaticRoutes(manifest,'dist');
 // Small output check: required model files and generated download/HTML paths exist.
 for(const a of manifest.assets)for(const path of [a.glb,a.blend,a.preview,a.downloads.bundle,a.downloads.credits,`models/${a.id}/index.html`,`zh-CN/models/${a.id}/index.html`])assert((await stat(resolve('dist',path))).size>0,'Missing built member '+path);
 for(const model of delivery.models)for(const file of Object.values(model.files)){const path=file.path.replace(/^site\/public\//,'');assert((await stat(resolve('dist',path))).size>0,'Missing built delivery '+path);}
 const sample=[delivery.models[0],delivery.models.at(-1)].filter((m,i,rows)=>rows.findIndex(x=>x.id===m.id)===i).map(m=>({id:m.id,files:Object.fromEntries(Object.entries(m.files).map(([role,f])=>[role,f.path.replace(/^site\/public\//,'')]))}));
 const stamp=process.env.VITE_RELEASE_CATALOG_TOKEN||'';
 const catalogPaths={gallery_path:releaseCatalogPath('gallery',stamp),catalog_path:releaseCatalogPath('catalog',stamp)};
 await writeFile('dist/release-build.json',JSON.stringify({source_commit:process.env.GITHUB_SHA||null,models:manifest.assets.length,...catalogPaths,sample})+'\n');
 const result={status:'PASS',models:manifest.assets.length,seconds:(performance.now()-started)/1000,model_qa:'NOT_REPEATED',hashes:'NOT_REPEATED'};
 await mkdir('qa/ci-timings',{recursive:true});await writeFile('qa/ci-timings/simple-build.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));return result;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)await buildSimple();

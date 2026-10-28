/** Integration of already-reviewed models: existence, one build, packaging. Not model QA. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,cp,stat,realpath} from 'node:fs/promises';
import {resolve,dirname,sep} from 'node:path';
import {pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';
import {clearDeliveredAssets,deliverManifestAssets} from './asset-delivery.mjs';
import {writeCatalog} from './catalog-build.mjs';
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
export async function buildSimple(){
 const started=performance.now(),source=JSON.parse(await readFile('assets/manifest.json'));
 assert(!source.review_only,'Review-only manifests cannot be deployed');
 const {checkDelivery}=await import('./unified-delivery-contract.mjs');
 const delivery=await checkDelivery({root:process.cwd()});
 const build=spawnSync(process.execPath,['node_modules/vite/bin/vite.js','build'],{stdio:'inherit'});assert.equal(build.status,0,build.error?.message||'Vite failed');
 await clearDeliveredAssets('dist');
 let manifest=await deliverManifestAssets(source,'dist',{verifyHashes:false});
 manifest=await deliverLegacyMedia(manifest);
 await writeFile('dist/assets/manifest.json',JSON.stringify(manifest,null,2)+'\n');
 await writeCatalog(manifest,'dist',{approvedOnly:true});
 for(const path of ['LICENSE','THIRD_PARTY_NOTICES.md'])await cp(path,resolve('dist',path));
 await cp('LICENSES','dist/LICENSES',{recursive:true});
 await writeStaticRoutes(manifest,'dist');
 // Small output check: required model files and generated download/HTML paths exist.
 for(const a of manifest.assets)for(const path of [a.glb,a.blend,a.preview,a.downloads.bundle,a.downloads.credits,`models/${a.id}/index.html`,`zh-CN/models/${a.id}/index.html`])assert((await stat(resolve('dist',path))).size>0,'Missing built member '+path);
 for(const model of delivery.models)for(const file of Object.values(model.files)){const path=file.path.replace(/^site\/public\//,'');assert((await stat(resolve('dist',path))).size>0,'Missing built delivery '+path);}
 const sample=[delivery.models[0],delivery.models.at(-1)].filter((m,i,rows)=>rows.findIndex(x=>x.id===m.id)===i).map(m=>({id:m.id,files:Object.fromEntries(Object.entries(m.files).map(([role,f])=>[role,f.path.replace(/^site\/public\//,'')]))}));
 await writeFile('dist/release-build.json',JSON.stringify({source_commit:process.env.GITHUB_SHA||null,models:manifest.assets.length,sample})+'\n');
 const result={status:'PASS',models:manifest.assets.length,seconds:(performance.now()-started)/1000,model_qa:'NOT_REPEATED',hashes:'NOT_REPEATED'};
 await mkdir('qa/ci-timings',{recursive:true});await writeFile('qa/ci-timings/simple-build.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));return result;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)await buildSimple();

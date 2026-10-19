/** Versioned WebGL poster recipe. UI styles/fonts are not rasterized into these transparent canvases. */
import {createHash} from 'node:crypto';
import {readFile,readdir,realpath} from 'node:fs/promises';
import {resolve} from 'node:path';
import assert from 'node:assert/strict';
const canonical=value=>value&&typeof value==='object'?(Array.isArray(value)?value.map(canonical):Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])]))):value;
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
export const CAPTURE_POLICY={version:1,node_major:'22',viewport:{width:1440,height:900},deviceScaleFactor:1,reducedMotion:'reduce',detail:[512,512],wheel:[768,432],engine:'playwright-pinned-chromium',args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'],fonts:'Not applicable: poster() draws transparent WebGL geometry directly to PNG, with no text or DOM rasterization.'};
async function sourceFiles(root,directory='site'){
 const files=[];
 for(const item of await readdir(resolve(root,directory),{withFileTypes:true})){
  const path=`${directory}/${item.name}`;
  if(path==='site/public/gallery'||path==='site/gallery/tests'||path==='site/gallery/approved-poster-inputs.json')continue;
  assert(!item.isSymbolicLink(),`Poster input symlink rejected: ${path}`);
  if(item.isDirectory())files.push(...await sourceFiles(root,path));
  else if(path.endsWith('.js')||(/^site\/gallery\/.*\.json$/.test(path))||['site/capture-gallery-posters.mjs','site/gallery-poster-inputs.mjs','site/catalog-build.mjs','site/asset-delivery.mjs','site/turntable-delivery.mjs'].includes(path))files.push(path);
 }
 return files;
}
export async function posterSharedInputs(root=process.cwd()){
 const paths=[...await sourceFiles(root),'package.json','package-lock.json','vite.config.js'].sort(),files=[];
 for(const path of paths){assert.equal(await realpath(resolve(root,path)),resolve(root,path));files.push([path,hash(await readFile(resolve(root,path)))]);}
 const browsers=JSON.parse(await readFile(resolve(root,'node_modules/playwright-core/browsers.json'))),browser=browsers.browsers.find(item=>item.name==='chromium').browserVersion;
 return {version:1,sha256:hash(JSON.stringify({policy:CAPTURE_POLICY,files,browser})),files,policy:CAPTURE_POLICY,browser};
}
export function posterInputKey(asset,shared){
 // Delivery-only fields are derived at build time and never consumed by poster().
 const {qa,material_count,file_sizes,glb_bytes,blend_bytes,downloads,card_preview,turntable,galleryPosters,wheelSpec,worlds,packs,...source}=asset;
 return hash(JSON.stringify(canonical({version:1,shared_sha256:shared.sha256,asset:source})));
}
export async function posterInputState(manifest,resources,{root=process.cwd()}={}){
 const shared=await posterSharedInputs(root);
 let baseline;try{baseline=JSON.parse(await readFile(resolve(root,'site/gallery/approved-poster-inputs.json')));}catch{baseline=null;}
 const valid=[],stale=[];
 for(const asset of manifest.assets){
  const poster=resources.posters[asset.id];if(!poster)continue;
  const key=posterInputKey(asset,shared),approved=baseline?.posters?.[asset.id];
  const seals=resources.files.filter(file=>[poster.detail,poster.wheel].includes(file.path)).sort((a,b)=>a.path.localeCompare(b.path));
  // Golden approved pixels are preserved, never silently re-signed for a changed recipe.
  if(approved){
   assert.equal(approved.poster_sha256,hash(JSON.stringify({poster,seals})),`Approved poster pixels or metadata changed: ${asset.id}; explicitly review a new baseline`);
   assert.equal(approved.input_sha256,key,`Approved poster inputs changed: ${asset.id}; recapture and explicitly review a new baseline`);
   valid.push(asset.id);
  }else if(poster.input_sha256===key&&poster.browser_version===shared.browser)valid.push(asset.id);
  else stale.push(asset.id);
 }
 return {shared,valid,stale};
}

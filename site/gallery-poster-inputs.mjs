/** Versioned WebGL poster recipe. UI styles/fonts are not rasterized into these transparent canvases. */
import {createHash} from 'node:crypto';
import {readFile,realpath} from 'node:fs/promises';
import {resolve,dirname,relative,sep} from 'node:path';
import {parseAst} from 'rollup/parseAst';
import assert from 'node:assert/strict';
const canonical=value=>value&&typeof value==='object'?(Array.isArray(value)?value.map(canonical):Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])]))):value;
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
export const CAPTURE_POLICY={version:2,site_base:'/',node_major:'22',viewport:{width:1440,height:900},deviceScaleFactor:1,reducedMotion:'reduce',detail:[512,512],wheel:[768,432],engine:'playwright-pinned-chromium',args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'],fonts:'Not applicable: poster() draws transparent WebGL geometry directly to PNG, with no text or DOM rasterization.'};
// Parse the actual isolated renderer import closure, never guess from file extensions.
// Rollup is supplied by the lockfile-pinned Vite toolchain used for the site build.
export async function posterRendererFiles(root=process.cwd()){
 const files=new Set();
 async function visit(path){
  if(files.has(path))return;
  const absolute=resolve(root,path);assert(absolute.startsWith(resolve(root)+sep),'Poster dependency escapes repository');
  assert.equal(await realpath(absolute),absolute,`Poster dependency symlink rejected: ${path}`);
  files.add(path);
  if(!/\.(?:js|mjs)$/.test(path))return;
  const tree=parseAst(await readFile(absolute,'utf8'));
  async function dependency(specifier){
   assert.equal(typeof specifier,'string','Computed poster dependencies require an explicit versioned recipe');
   if(specifier.startsWith('.'))await visit(relative(root,resolve(dirname(absolute),specifier)).split(sep).join('/'));
   else assert(specifier==='three'||specifier.startsWith('three/'),'Only lockfile-pinned Three.js package imports are allowed in the isolated renderer');
  }
  async function walk(node){
   if(!node||typeof node!=='object')return;
   if(['ImportDeclaration','ExportNamedDeclaration','ExportAllDeclaration'].includes(node.type)&&node.source)await dependency(node.source.value);
   if(node.type==='ImportExpression')await dependency(node.source.type==='Literal'?node.source.value:undefined);
   // Asset imports using Vite's URL idiom are also part of the recipe (including fonts).
   if(node.type==='NewExpression'&&node.callee?.name==='URL'&&node.arguments[1]?.object?.type==='MetaProperty')await dependency(node.arguments[0]?.value);
   for(const [key,value]of Object.entries(node))if(key!=='source'){
    if(Array.isArray(value)){for(const child of value)await walk(child);}
    else if(value&&typeof value==='object')await walk(value);
   }
  }
  await walk(tree);
 }
 await visit('site/gallery/renderer.js');return [...files].sort();
}
export async function posterSharedInputs(root=process.cwd()){
 const paths=[...await posterRendererFiles(root),'site/capture-gallery-posters.mjs','site/gallery-poster-inputs.mjs','package.json','package-lock.json','vite.config.js'].sort(),files=[];
 for(const path of paths){assert.equal(await realpath(resolve(root,path)),resolve(root,path));files.push([path,hash(await readFile(resolve(root,path)))]);}
 const browsers=JSON.parse(await readFile(resolve(root,'node_modules/playwright-core/browsers.json'))),browser=browsers.browsers.find(item=>item.name==='chromium').browserVersion;
 return {version:2,sha256:hash(JSON.stringify({policy:CAPTURE_POLICY,files,browser})),files,policy:CAPTURE_POLICY,browser};
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

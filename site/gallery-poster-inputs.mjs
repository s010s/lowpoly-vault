// BEGIN GALLERY POSTER V3 ORCHESTRATION
import {successorReader,successorContext,historicalGalleryView,verifySuccessorPresentation} from './same-id-successors.mjs';
import {assertHistoricalPosterRecipe,assertHistoricalPosterApprovals} from './gallery-poster-compat.mjs';
import {appendProductionPosterInputState} from './production-release.mjs';
import {assertMain842PosterRecipe} from './gallery-main842-compat.mjs';
const historicalRecipes=new WeakMap();
// END GALLERY POSTER V3 ORCHESTRATION
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
// BEGIN GALLERY POSTER V3 ORCHESTRATION
 return {version:3,sha256:hash(JSON.stringify({domain:'gallery-poster-capture-v3',policy:CAPTURE_POLICY,files,browser})),files,policy:CAPTURE_POLICY,browser};
// END GALLERY POSTER V3 ORCHESTRATION
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
// BEGIN GALLERY POSTER V3 ORCHESTRATION
 if(manifest.publication?.same_id_successors){
  const read=successorReader(root),context=successorContext({manifest,read});
  await verifySuccessorPresentation(root,context);
  const historicalResources=historicalGalleryView({manifest,resources,read});
  const legacy=await posterInputState(context.base,historicalResources,{root});
  const ids=context.entries.map(row=>row.entry.id);
  // Unchanged historical metadata/pixels are checked above, fresh mesh presentation
  // is checked separately. Do not relabel successor receipts as old golden approval.
  return {...legacy,valid:[...new Set([...legacy.valid,...ids])],stale:legacy.stale.filter(id=>!ids.includes(id)),approved:legacy.approved.filter(id=>!ids.includes(id)),capture:legacy.capture.filter(id=>!ids.includes(id)),successors:ids};
 }
 await assertHistoricalPosterApprovals({root,baseline});
 const production=manifest.assets.filter(asset=>asset.production_release);
 if(production.length){
  for(const asset of production)assert(!baseline?.posters?.[asset.id],'Production route cannot replace a historical golden approval');
  const legacy=await posterInputState({...manifest,assets:manifest.assets.filter(asset=>!asset.production_release)},resources,{root});
  return appendProductionPosterInputState(root,production,resources,legacy);
 }
// END GALLERY POSTER V3 ORCHESTRATION
 const valid=[],stale=[],approvedIds=[];
 for(const asset of manifest.assets){
  const poster=resources.posters[asset.id];if(!poster)continue;
  const key=posterInputKey(asset,shared),approved=baseline?.posters?.[asset.id];
  const seals=resources.files.filter(file=>[poster.detail,poster.wheel].includes(file.path)).sort((a,b)=>a.path.localeCompare(b.path));
// BEGIN GALLERY POSTER V3 ORCHESTRATION
  if(approved&&baseline.shared){
   if(!historicalRecipes.has(baseline))historicalRecipes.set(baseline,assertHistoricalPosterRecipe({root,baseline,shared}));
   const historical=await historicalRecipes.get(baseline);
   assert.equal(approved.poster_sha256,hash(JSON.stringify({poster,seals})),`Approved poster pixels or metadata changed: ${asset.id}; explicitly review a new baseline`);
   assert.equal(approved.input_sha256,posterInputKey(asset,historical),`Approved poster inputs changed: ${asset.id}; explicitly review a new baseline`);
   valid.push(asset.id);approvedIds.push(asset.id);continue;
  }
  // Existing non-golden consistency is retained only for the exact main842 v3
  // recipe. These captures remain unapproved and stay in the fresh-capture list.
  if(!approved&&baseline?.shared){
   const main842=await assertMain842PosterRecipe({root,shared});
   if(poster.input_sha256===posterInputKey(asset,main842)&&poster.browser_version===main842.browser){valid.push(asset.id);continue;}
  }
// END GALLERY POSTER V3 ORCHESTRATION
  // Golden approved pixels are preserved, never silently re-signed for a changed recipe.
  if(approved){
   assert.equal(approved.poster_sha256,hash(JSON.stringify({poster,seals})),`Approved poster pixels or metadata changed: ${asset.id}; explicitly review a new baseline`);
   assert.equal(approved.input_sha256,key,`Approved poster inputs changed: ${asset.id}; recapture and explicitly review a new baseline`);
   valid.push(asset.id);approvedIds.push(asset.id);
  }else if(poster.input_sha256===key&&poster.browser_version===shared.browser)valid.push(asset.id);
  else stale.push(asset.id);
 }
 // Repository-authored matching hashes are consistency claims, not generation proof.
 // A fresh build captures every non-golden ID; only trusted artifact reuse may skip that.
 return {shared,valid,stale,approved:approvedIds,capture:manifest.assets.filter(asset=>!approvedIds.includes(asset.id)).map(asset=>asset.id)};
}

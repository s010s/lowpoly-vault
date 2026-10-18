// Geometry parsing only. Textured published GLBs use real browser image decoding; no rendering claim.
import { readFile,readdir,writeFile,mkdir,stat } from 'node:fs/promises';
import { join,resolve,extname,sep } from 'node:path';
import { createServer } from 'node:http';
import assert from 'node:assert/strict';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { Box3,Vector3 } from 'three';
import { chromium } from 'playwright';
async function discover(dir){const found=[];for(const e of await readdir(dir,{withFileTypes:true})){const p=join(dir,e.name);if(e.isDirectory())found.push(...await discover(p));else if(e.name==='metadata.json')found.push(p);}return found.sort();}
const results=[], inputs=new Map(),root=resolve('.');
// Historical originals and every exact publication. Rejected/unpublished candidate revisions are not release inputs.
for(const path of await discover('assets/prehistoric')) {
 const asset=JSON.parse(await readFile(path,'utf8'));inputs.set(asset.glb,{...asset,parse_scope:'original'});
}
const published=JSON.parse(await readFile('assets/manifest.json','utf8'));
for(const asset of published.assets)if(!inputs.has(asset.glb))inputs.set(asset.glb,{...asset,parse_scope:'published_revision'});
let browser,context,page,server;
const browserErrors=[];
async function textured(asset) {
 if(!browser) {
  server=createServer(async(req,res)=>{try {
   const path=new URL(req.url,'http://localhost').pathname;
   if(path==='/'){res.setHeader('Content-Type','text/html');res.end('<!doctype html><link rel="icon" href="data:,"><script type="importmap">{"imports":{"three":"/node_modules/three/build/three.module.js"}}</script>');return;}
   const file=resolve(root,'.'+decodeURIComponent(path));assert(file.startsWith(root+sep));assert((await stat(file)).isFile());
   res.setHeader('Content-Type',{'.js':'text/javascript','.glb':'model/gltf-binary','.png':'image/png','.webp':'image/webp'}[extname(file)]||'application/octet-stream');res.end(await readFile(file));
  }catch{res.writeHead(404).end();}});
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox']});context=await browser.newContext();page=await context.newPage();
  page.on('pageerror',e=>browserErrors.push(e.message));page.on('response',r=>{if(r.status()>=400)browserErrors.push(`${r.status()} ${r.url()}`);});
  await page.goto(`http://127.0.0.1:${server.address().port}/`);
 }
 return page.evaluate(async path=>{
  const {GLTFLoader}=await import('/node_modules/three/examples/jsm/loaders/GLTFLoader.js'),{Box3,Vector3}=await import('three');
  const gltf=await new GLTFLoader().loadAsync('/'+path);gltf.scene.updateMatrixWorld(true);
  let triangles=0,meshes=0;const images=new Set(),textures=new Set();
  gltf.scene.traverse(o=>{if(!o.isMesh)return;meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;
   for(const m of Array.isArray(o.material)?o.material:[o.material])for(const value of Object.values(m))if(value?.isTexture){textures.add(value);const image=value.source.data;if(!(image?.width>0&&image?.height>0))throw Error('Embedded texture must actually decode');images.add(image);}
  });
  const dimensions=new Box3().setFromObject(gltf.scene).getSize(new Vector3()).toArray(),declared=gltf.parser.json.images?.length||0;
  if(images.size!==declared)throw Error(`Decoded ${images.size}/${declared} embedded images`);
  gltf.scene.traverse(o=>{o.geometry?.dispose();for(const m of Array.isArray(o.material)?o.material:[o.material])m?.dispose();});for(const t of textures)t.dispose();for(const i of images)i.close?.();
  return {triangles,meshes,dimensions,decoded_images:images.size,parser:'browser GLTFLoader + real image decoding'};
 },asset.glb);
}
try {
 for(const a of inputs.values()){
  try{
   const bytes=await readFile(a.glb),doc=JSON.parse(bytes.subarray(20,20+bytes.readUInt32LE(12)).toString());let measured;
   if(doc.images?.length) measured=await textured(a);
   else {
    const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');const scene=gltf.scene;scene.updateMatrixWorld(true);let triangles=0,meshes=0;scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});
    measured={triangles,meshes,dimensions:new Box3().setFromObject(scene).getSize(new Vector3()).toArray(),decoded_images:0,parser:'Node GLTFLoader'};
    scene.traverse(o=>{o.geometry?.dispose();for(const m of Array.isArray(o.material)?o.material:[o.material])m?.dispose();});
   }
   const delta=Math.max(...measured.dimensions.map((n,i)=>Math.abs(n-a.dimensions[i])));
   assert.equal(measured.triangles,a.triangles,'Triangle count must match');assert(delta<=.0001,`Bounds mismatch: ${delta} m`);
   results.push({id:a.id,revision:a.revision,glb:a.glb,scope:a.parse_scope,status:'pass',...measured,bounds_max_delta_m:delta});console.log(`PASS ${a.id}: ${measured.meshes} meshes, ${measured.triangles} triangles, dimensions match, ${measured.decoded_images} decoded images`);
  }catch(e){results.push({id:a.id,glb:a.glb,scope:a.parse_scope,status:'fail',error:e.message});console.error(`FAIL ${a.id}: ${e.message}`);}
 }
}finally{await context?.close();await browser?.close();if(server?.listening)await new Promise(r=>server.close(r));}
await mkdir('qa',{recursive:true});await writeFile('qa/threejs-parser.json',JSON.stringify({test:'Three.js GLTFLoader geometry and embedded-image decoding',browser_rendering:'not_tested',visual_review:'not_tested',errors:browserErrors,results},null,2)+'\n');
if(!results.length||results.some(r=>r.status==='fail')||browserErrors.length)process.exitCode=1;

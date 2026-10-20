#!/usr/bin/env node
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const { chromium } = require('playwright');

const repoRoot = path.resolve(process.argv[2] || process.cwd());
const outDir = path.resolve(process.argv[3] || '/tmp/batch55-independent-qa/webgl');
const ids = ['vermicularia','weichselia','ventifact','pentichnus-deep-dwelling-trace'];
const revisions = {vermicularia:'r001', weichselia:'r001', ventifact:'r001', 'pentichnus-deep-dwelling-trace':'r002'};
const pinnedCandidateCommit = 'b2341debdb31f73e0719d4aadbe832321db6008a';
const pinnedSourceCommit = '1e43f9e2c79b6d2465d8eadf2169355cba3690c7';
const scope = JSON.parse(fs.readFileSync(path.join(repoRoot,'production/continuous-small-life-round20-20261020/batch-55-QA-SCOPE.json'),'utf8'));
const assets = {};
for (const id of ids) {
  const file = path.join(repoRoot,'assets/candidates/continuous-small-life-round20-20261020/batch-55',id,revisions[id],id+'.glb');
  const bytes = fs.readFileSync(file);
  const sha = crypto.createHash('sha256').update(bytes).digest('hex');
  if (sha !== scope.expected_glb_sha256_by_asset[id]) throw new Error(`Pinned hash mismatch: ${id}`);
  assets[id] = {file, bytes, sha};
}
const html = `<!doctype html><meta charset="utf-8"><title>Batch 55 GLB software WebGL QA</title>
<script type="importmap">{"imports":{"three":"/three/build/three.module.js","three/addons/":"/three/examples/jsm/"}}</script>
<body style="margin:0;background:#e8e4dc"><script type="module">
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
const ids = ${JSON.stringify(ids)};
const revisions = ${JSON.stringify(revisions)};
const renderer = new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:'low-power'});
renderer.setPixelRatio(1); renderer.setSize(960,640,false);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1;
document.body.appendChild(renderer.domElement);
const gl = renderer.getContext();
const dbg=gl.getExtension('WEBGL_debug_renderer_info'); const context = {webgl_version:gl.getParameter(gl.VERSION), glsl_version:gl.getParameter(gl.SHADING_LANGUAGE_VERSION), vendor:gl.getParameter(gl.VENDOR), renderer:gl.getParameter(gl.RENDERER), unmasked_vendor:dbg?gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL):null, unmasked_renderer:dbg?gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL):null, webgl2:renderer.capabilities.isWebGL2};
function addLights(scene) {
  scene.add(new THREE.HemisphereLight(0xffffff,0x716957,1.5));
  const key = new THREE.DirectionalLight(0xffffff,2.2); key.position.set(2.5,3.5,4); scene.add(key);
  const fill = new THREE.DirectionalLight(0xffffff,0.8); fill.position.set(-3,1.5,-2); scene.add(fill);
}
function addGround(scene,box,pad) {
  const width = Math.max(box.max.x-box.min.x+pad*2,0.1);
  const depth = Math.max(box.max.z-box.min.z+pad*2,0.1);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(width,depth),new THREE.MeshStandardMaterial({color:0xd2cec5,roughness:1,metalness:0}));
  ground.rotation.x = -Math.PI/2; ground.position.set((box.min.x+box.max.x)/2,box.min.y-0.001,(box.min.z+box.max.z)/2); scene.add(ground);
}
function bounds(object) {
  object.updateMatrixWorld(true);
  const box = new THREE.Box3().setFromObject(object);
  const size = new THREE.Vector3(); box.getSize(size);
  const center = new THREE.Vector3(); box.getCenter(center);
  return {box,size,center};
}
function cameraFor(box,aspect,spanMultiplier=1.65) {
  const size = new THREE.Vector3(); box.getSize(size);
  const center = new THREE.Vector3(); box.getCenter(center);
  const maxDim = Math.max(size.x,size.y,size.z,0.01);
  const height = Math.max(size.y*1.45, maxDim*spanMultiplier, size.x/aspect*1.35, size.z*1.4);
  const camera = new THREE.OrthographicCamera(-height*aspect/2,height*aspect/2,height/2,-height/2,0.0001,100);
  camera.up.set(0,1,0); camera.position.set(center.x+maxDim*1.55,center.y+maxDim*1.25,center.z+maxDim*2.25); camera.lookAt(center); camera.updateProjectionMatrix();
  return camera;
}
function pngData(canvas) { return canvas.toDataURL('image/png').split(',')[1]; }
const loader = new GLTFLoader();
window.runSuite = async () => {
  const loaded=[];
  const result={three_revision:THREE.REVISION,context,standalone:[],composition:null,errors:[]};
  for (const id of ids) {
    const gltf=await loader.loadAsync('/asset/'+encodeURIComponent(id)+'.glb');
    const object=gltf.scene;
    const b=bounds(object);
    let tri=0,materials=new Set(),meshes=0;
    object.traverse(o=>{if(o.isMesh){meshes++;const a=o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count;tri+=Math.floor(a/3);const mats=Array.isArray(o.material)?o.material:[o.material];for(const m of mats)materials.add(m.name||'(unnamed)');}});
    loaded.push({id,object,box:b.box,size:b.size,center:b.center,triangles:tri,material_names:[...materials],meshes});
  }
  for (const item of loaded) {
    const scene=new THREE.Scene(); scene.background=new THREE.Color(0xe8e4dc); addLights(scene);
    const object=item.object.clone(true); scene.add(object);
    const box=new THREE.Box3().setFromObject(object); addGround(scene,box,Math.max(item.size.x,item.size.z)*0.35);
    const camera=cameraFor(box,renderer.domElement.width/renderer.domElement.height);
    renderer.info.reset(); renderer.render(scene,camera);
    const draws={calls:renderer.info.render.calls,triangles:renderer.info.render.triangles,points:renderer.info.render.points,lines:renderer.info.render.lines};
    result.standalone.push({asset_id:item.id,revision:revisions[item.id],bounds_m:{min:box.min.toArray(),max:box.max.toArray(),size:item.size.toArray()},mesh_count:item.meshes,material_names:item.material_names,asset_triangles_from_GLTF:item.triangles,render_info_including_ground:draws,png_base64:pngData(renderer.domElement)});
  }
  const scene=new THREE.Scene(); scene.background=new THREE.Color(0xe8e4dc); addLights(scene);
  const gap=0.12; const totalWidth=loaded.reduce((sum,x)=>sum+x.size.x,0)+gap*(loaded.length-1); let cursor=-totalWidth/2;
  for (const item of loaded) {
    const clone=item.object.clone(true); clone.position.x += cursor-item.box.min.x; clone.position.z += -item.center.z; scene.add(clone); cursor += item.size.x+gap;
  }
  const box=new THREE.Box3().setFromObject(scene); addGround(scene,box,0.2);
  const aspect=renderer.domElement.width/renderer.domElement.height; const maxDim=Math.max(box.max.x-box.min.x,box.max.y-box.min.y,box.max.z-box.min.z);
  const viewH=Math.max((box.max.y-box.min.y)*1.5,((box.max.x-box.min.x)/aspect)*1.4,(box.max.z-box.min.z)*1.7);
  const center=new THREE.Vector3(); box.getCenter(center);
  const camera=new THREE.OrthographicCamera(-viewH*aspect/2,viewH*aspect/2,viewH/2,-viewH/2,0.0001,100);
  camera.up.set(0,1,0); camera.position.set(center.x+maxDim*0.45,center.y+maxDim*1.1,center.z+maxDim*2.4); camera.lookAt(center); camera.updateProjectionMatrix();
  renderer.info.reset(); renderer.render(scene,camera);
  result.composition={kind:'synthetic-four-asset-software-WebGL-smoke-scene',assets:loaded.map(x=>({asset_id:x.id,revision:revisions[x.id],triangles:x.triangles,meshes:x.meshes})),bounds_m:{min:box.min.toArray(),max:box.max.toArray()},render_info_including_ground:{calls:renderer.info.render.calls,triangles:renderer.info.render.triangles,points:renderer.info.render.points,lines:renderer.info.render.lines},png_base64:pngData(renderer.domElement)};
  return result;
};
</script></body>`;

const threeRoot=path.resolve(repoRoot,'node_modules/three');
const server=http.createServer((req,res)=>{
  const pathname=new URL(req.url,'http://127.0.0.1').pathname;
  res.setHeader('Access-Control-Allow-Origin','*');
  if(pathname==='/') {res.writeHead(200,{'content-type':'text/html; charset=utf-8'});res.end(html);return;}
  if(pathname==='/favicon.ico') {res.writeHead(204);res.end();return;}
  if(pathname.startsWith('/asset/')) {
    const id=decodeURIComponent(path.basename(pathname,'.glb'));
    if(!assets[id]) {res.writeHead(404);res.end('unknown asset');return;}
    res.writeHead(200,{'content-type':'model/gltf-binary','content-length':assets[id].bytes.length,'cache-control':'no-store'});res.end(assets[id].bytes);return;
  }
  if(pathname.startsWith('/three/')) {
    const relative=pathname.slice('/three/'.length); const file=path.resolve(threeRoot,relative);
    if(!file.startsWith(threeRoot+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()) {res.writeHead(404);res.end('missing vendor file');return;}
    const type=file.endsWith('.js')?'text/javascript; charset=utf-8':'application/octet-stream';
    res.writeHead(200,{'content-type':type,'cache-control':'no-store'});fs.createReadStream(file).pipe(res);return;
  }
  res.writeHead(404);res.end('not found');
});

(async()=>{
  fs.mkdirSync(outDir,{recursive:true});
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const port=server.address().port;
  let browser;
  try {
    browser=await chromium.launch({headless:true,executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--enable-webgl','--ignore-gpu-blocklist','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-gpu-sandbox']});
    const page=await browser.newPage({viewport:{width:960,height:640},deviceScaleFactor:1});
    const pageErrors=[]; const consoleErrors=[];
    page.on('pageerror',e=>pageErrors.push(String(e)));
    page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text());});
    await page.goto(`http://127.0.0.1:${port}/`,{waitUntil:'load'});
    await page.waitForFunction('typeof window.runSuite === "function"',{timeout:30000});
    const report=await page.evaluate(()=>window.runSuite());
    for(const frame of report.standalone){const raw=Buffer.from(frame.png_base64,'base64');fs.writeFileSync(path.join(outDir,frame.asset_id+'.png'),raw);frame.png_sha256=crypto.createHash('sha256').update(raw).digest('hex');delete frame.png_base64;}
    const composite=Buffer.from(report.composition.png_base64,'base64');fs.writeFileSync(path.join(outDir,'four-asset-smoke-scene.png'),composite);report.composition.png_sha256=crypto.createHash('sha256').update(composite).digest('hex');delete report.composition.png_base64;
    report.run={browser:browser.version(),execution:'Chromium headless; ANGLE/SwiftShader software WebGL',candidate_commit:pinnedCandidateCommit,model_source_commit:pinnedSourceCommit,scope_id:scope.batch_id,expected_glb_sha256_by_asset:scope.expected_glb_sha256_by_asset,page_errors:pageErrors,console_errors:consoleErrors,software_renderer_confirmed:/swiftshader|software/i.test([report.context.renderer,report.context.unmasked_renderer].join(' ')),target_hardware_tested:false,target_production_scene_tested:false};
    const reportPath=path.join(outDir,'software-webgl-report.json');fs.writeFileSync(reportPath,JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify({report:reportPath,browser:report.run.browser,context:report.context,assets:report.standalone.map(x=>({id:x.asset_id,bounds:x.bounds_m,triangles:x.asset_triangles_from_GLTF,render:x.render_info_including_ground,png_sha256:x.png_sha256})),composition:{...report.composition,png_base64:undefined},page_errors:pageErrors,console_errors:consoleErrors,software_renderer_confirmed:report.run.software_renderer_confirmed},null,2));
  } finally {if(browser) await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});

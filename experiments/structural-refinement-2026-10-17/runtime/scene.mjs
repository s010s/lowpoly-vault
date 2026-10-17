/** Bounded populated-scene probe. Exact bytes, authored meters, no approval claim. */
import {chromium} from 'playwright';
import {createServer} from 'node:http';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {resolve,sep,extname} from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {CARD_RENDER_PRESET} from '../../../site/render-preset.js';
const root=process.cwd(),out=resolve(process.env.PREVIEW_OUTPUT||'qa/structural-refinement-runtime');
const hash=b=>createHash('sha256').update(b).digest('hex');
const plan=JSON.parse(await readFile('dist/review-plan.json'));
const originals=JSON.parse(await readFile('assets/manifest.json'));
const inputs=originals.assets.map(a=>{const revised=plan.assets.find(p=>p.id===a.id);return revised?{...a,glb:revised.glb,sha256:{glb:revised.glb_sha256}}:a;});
for(const a of inputs)assert.equal(hash(await readFile(a.glb)),a.sha256.glb);
const report={status:'running',scope:'Ten distinct assets at authored scale in an open gallery grid. CI software-WebGL integration/work measurement, not a gameplay or physical-device FPS benchmark.',source_commit:process.env.GITHUB_SHA||null,assets:inputs.map(a=>({id:a.id,glb_sha256:a.sha256.glb,instances:1})),preset:CARD_RENDER_PRESET};
const mime={'.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.glb':'model/gltf-binary'};
const server=createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');if(url.pathname==='/')return res.writeHead(200,{'Content-Type':'text/html'}).end('<!doctype html><html><head><script type="importmap">{"imports":{"three":"/node_modules/three/build/three.module.js","three/addons/":"/node_modules/three/examples/jsm/"}}</script></head><body style="margin:0;background:#e8e4dc"><canvas id="scene"></canvas></body></html>');const p=resolve(root,decodeURIComponent(url.pathname.slice(1)));assert(p.startsWith(root+sep));assert(url.pathname.startsWith('/node_modules/three/')||inputs.some(a=>'/'+a.glb===url.pathname));res.writeHead(200,{'Content-Type':mime[extname(p)]||'application/octet-stream'}).end(await readFile(p));}catch{res.writeHead(404).end();}});
let browser;
try{
 await mkdir(out,{recursive:true});await new Promise(r=>server.listen(0,'127.0.0.1',r));
 browser=await chromium.launch({args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const context=await browser.newContext({viewport:{width:1600,height:1000},deviceScaleFactor:1,reducedMotion:'reduce'});
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(`http://127.0.0.1:${server.address().port}/`);
 const result=await page.evaluate(async({inputs,preset})=>{
  const T=await import('three'),{GLTFLoader}=await import('three/addons/loaders/GLTFLoader.js');
  const renderer=new T.WebGLRenderer({canvas:document.querySelector('#scene'),antialias:true,alpha:false});
  renderer.setSize(1600,1000,false);renderer.setPixelRatio(1);renderer.setClearColor(preset.background,1);renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=preset.exposure;
  const scene=new T.Scene(),h=preset.hemisphere;scene.add(new T.HemisphereLight(h.sky,h.ground,h.intensity));
  for(const spec of preset.lights){const l=new T.DirectionalLight(spec.color,spec.intensity);l.position.set(...spec.position);scene.add(l);}
  const loader=new GLTFLoader(),loaded=[];
  for(const asset of inputs){const start=performance.now(),g=await loader.loadAsync('/'+asset.glb),box=new T.Box3().setFromObject(g.scene),size=box.getSize(new T.Vector3()),center=box.getCenter(new T.Vector3());loaded.push({asset,model:g.scene,box,size,center,load_ms:performance.now()-start});}
  const spacing=Math.max(...loaded.map(x=>Math.max(x.size.x,x.size.z)))+1;
  const measurements=[];
  for(let i=0;i<loaded.length;i++){const a=loaded[i];a.model.position.x+=(i%5-2)*spacing-a.center.x;a.model.position.z+=(Math.floor(i/5)-.5)*spacing-a.center.z;a.model.position.y-=a.box.min.y;scene.add(a.model);measurements.push({id:a.asset.id,glb_sha256:a.asset.sha256.glb,dimensions:a.size.toArray(),position:a.model.position.toArray(),load_ms:a.load_ms});}
  const bounds=new T.Box3();for(const x of loaded)bounds.union(new T.Box3().setFromObject(x.model));
  const center=bounds.getCenter(new T.Vector3()),size=bounds.getSize(new T.Vector3()),radius=size.length()/2,camera=new T.PerspectiveCamera(38,1.6,.01,1000);camera.position.copy(center).add(new T.Vector3(1,.72,1.3).normalize().multiplyScalar(radius/Math.sin(38*Math.PI/360)*1.12));camera.lookAt(center);
  const gl=renderer.getContext(),ext=gl.getExtension('WEBGL_debug_renderer_info'),times=[];
  for(let i=0;i<20;i++){const start=performance.now();renderer.render(scene,camera);gl.finish();times.push(performance.now()-start);}
  const png=renderer.domElement.toDataURL('image/png');
  return {png,measurements,runtime:{engine:'Three.js',version:T.REVISION,loader:'GLTFLoader',renderer:'WebGLRenderer',device:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER),browser:navigator.userAgent,context:gl.constructor.name,context_created:true,rendered:true,rendered_frames:20,draw_calls:renderer.info.render.calls,triangles:renderer.info.render.triangles,output_color_space:renderer.outputColorSpace,tone_mapping:'ACESFilmic',exposure:renderer.toneMappingExposure},renderer_memory:renderer.info.memory,synchronous_render_finish_ms:times,viewport:[1600,1000],camera:{position:camera.position.toArray(),target:center.toArray(),fov:38}};
 },{inputs,preset:CARD_RENDER_PRESET});
 const bytes=Buffer.from(result.png.split(',')[1],'base64');delete result.png;await writeFile(resolve(out,'populated-scene.png'),bytes);
 Object.assign(report,result,{errors,screenshot:{path:'populated-scene.png',sha256:hash(bytes),bytes:bytes.length},status:errors.length?'fail':'pass'});assert.equal(errors.length,0);assert(report.runtime.triangles>0&&report.runtime.draw_calls>0);await context.close();
}catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;}
finally{await mkdir(out,{recursive:true});await writeFile(resolve(out,'scene-report.json'),JSON.stringify(report,null,2)+'\n');await browser?.close();if(server.listening)await new Promise(r=>server.close(r));console.log(JSON.stringify(report,null,2));}

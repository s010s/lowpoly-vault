#!/usr/bin/env node
// Functional exact-GLB scene in pinned Three.js using Chromium ANGLE SwiftShader.
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {createHash} from 'node:crypto';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {resolve, sep} from 'node:path';
import {chromium} from 'playwright';

const repo = resolve('.');
const qa = resolve('qa/independent/small-marine-quartet-20261019-gpt6-luna-xhigh/evidence/webgl');
const specs = [
  ['emeraldella','r002','7c64de69f55bca9a4bb6701dce818b5fbdf4656cef18b87785d0adfb8a1d8b7c',2996],
  ['burgessia','r002','e75fdf29738520f3d8a3ad3b5d50c582fabd558c086e0a817bbc7a592a315669',1862],
  ['tuzoia','r003','9f5f09b624b2d99da6c989b0e332903904452ffa9a7f68b2e731a31fb90dfe7c',2176],
  ['sanctacaris','r002','d51b77469b954e9adc97c48db4dcae78adc622297ab4c4ffbb124de521805a96',3604],
];
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const files = new Map(), assets = [];
for (const [id,revision,expectedHash,expectedTriangles] of specs) {
  const path = resolve(repo,`production/concept-small-marine-quartet-20261019/${id}/${revision}/${id}.glb`);
  assert(path.startsWith(repo+sep));
  const bytes = await readFile(path);
  assert.equal(digest(bytes),expectedHash,`${id}: GLB changed from the frozen SHA`);
  files.set(`/models/${id}.glb`,bytes);
  assets.push({id,revision,path:path.slice(repo.length+1),glb_sha256:expectedHash,bytes:bytes.length,expected_triangles:expectedTriangles});
}

const modules = resolve(repo,'node_modules/three');
const html = '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;width:100%;height:100%;background:#e8e4dc}canvas{display:block;width:100%;height:100%}</style><script type="importmap">{"imports":{"three":"/modules/build/three.module.js"}}</script></head><body></body></html>';
const server = createServer(async (req,res) => {
  try {
    const pathname = new URL(req.url,'http://127.0.0.1').pathname;
    if (pathname === '/') { res.setHeader('Content-Type','text/html'); res.end(html); return; }
    if (pathname === '/favicon.ico') { res.writeHead(204).end(); return; }
    if (files.has(pathname)) { res.setHeader('Content-Type','model/gltf-binary'); res.end(files.get(pathname)); return; }
    assert(pathname.startsWith('/modules/'));
    const path = resolve(modules,'.'+decodeURIComponent(pathname.slice('/modules'.length)));
    assert(path.startsWith(modules+sep) && path.endsWith('.js'));
    res.setHeader('Content-Type','text/javascript'); res.end(await readFile(path));
  } catch { res.writeHead(404).end(); }
});

const report = {
  schema_version:1,
  kind:'software_webgl_scene',
  status:'running',
  created_at_utc:new Date().toISOString(),
  engine:'Three.js GLTFLoader',
  three_version:'0.180.0',
  browser_engine:'Chromium ANGLE SwiftShader software WebGL2',
  device:'software renderer (SwiftShader)',
  limitations:['Functional WebGL parsing/rendering only; no physical GPU, target device or performance claim.','Assets remain at authored meter scales; scene translations only arrange them for visibility.'],
  scene_description:'Four frozen child-friendly marine candidate GLBs placed in a 2×2 scene at authored scales.',
  scene_assets:assets,
  errors:[],
  resource_errors:[],
};
let browser;
try {
  await mkdir(qa,{recursive:true});
  await new Promise(ok=>server.listen(0,'127.0.0.1',ok));
  browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  report.browser_version=browser.version();
  const page=await browser.newPage({viewport:{width:1280,height:900},deviceScaleFactor:1});
  page.on('pageerror',e=>report.errors.push(String(e)));
  page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());});
  page.on('response',r=>{if(r.status()>=400)report.resource_errors.push(`${r.status()} ${r.url()}`);});
  await page.goto(`http://127.0.0.1:${server.address().port}/`,{waitUntil:'networkidle'});
  const summary=await page.evaluate(async items=>{
    const T=await import('three');
    const {GLTFLoader}=await import('/modules/examples/jsm/loaders/GLTFLoader.js');
    const scene=new T.Scene();scene.background=new T.Color('#e8e4dc');
    const renderer=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});
    renderer.setSize(1280,900);renderer.setPixelRatio(1);renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;
    document.body.append(renderer.domElement);
    scene.add(new T.HemisphereLight(0xffffff,0x716755,2));
    const key=new T.DirectionalLight(0xffffff,2.4);key.position.set(-1,2,2);scene.add(key);
    const loaded=[];
    for(const item of items){
      const gltf=await new GLTFLoader().loadAsync('/models/'+item.id+'.glb');
      const group=new T.Group();group.add(gltf.scene);group.updateMatrixWorld(true);
      const b=new T.Box3().setFromObject(group),size=b.getSize(new T.Vector3());
      let triangles=0,meshes=0,materials=new Set();
      gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;for(const m of (Array.isArray(o.material)?o.material:[o.material]))if(m)materials.add(m.name);}});
      if(triangles!==item.expected_triangles||meshes<1||![size.x,size.y,size.z].every(v=>Number.isFinite(v)&&v>0))throw Error(item.id+': loader geometry mismatch');
      loaded.push({...item,group,size:size.toArray(),bounds:{min:b.min.toArray(),max:b.max.toArray()},triangles,meshes,material_names:[...materials].sort()});
    }
    const gap=.035,colWidths=[0,0],rowDepths=[0,0];
    loaded.forEach((a,i)=>{colWidths[i%2]=Math.max(colWidths[i%2],a.size[0]);rowDepths[Math.floor(i/2)]=Math.max(rowDepths[Math.floor(i/2)],a.size[2]);});
    const totalW=colWidths[0]+colWidths[1]+gap,totalD=rowDepths[0]+rowDepths[1]+gap;
    const colCenters=[-totalW/2+colWidths[0]/2,totalW/2-colWidths[1]/2];
    const rowCenters=[-totalD/2+rowDepths[0]/2,totalD/2-rowDepths[1]/2];
    loaded.forEach((a,i)=>{const col=i%2,row=Math.floor(i/2),b=new T.Box3().setFromObject(a.group);a.group.position.set(colCenters[col]-b.getCenter(new T.Vector3()).x,-b.min.y,rowCenters[row]-b.getCenter(new T.Vector3()).z);scene.add(a.group);a.presentation_translation=a.group.position.toArray();a.scale=a.group.scale.toArray();});
    const bounds=new T.Box3().setFromObject(scene),size=bounds.getSize(new T.Vector3()),center=bounds.getCenter(new T.Vector3());
    const aspect=1280/900,vertical=Math.max(size.y+size.z,size.x/aspect)*1.35,horizontal=vertical*aspect,distance=size.length()*3;
    const camera=new T.OrthographicCamera(-horizontal/2,horizontal/2,vertical/2,-vertical/2,.00001,distance*10);camera.position.copy(center).add(new T.Vector3(0,distance,distance*1.5));camera.lookAt(center);camera.updateProjectionMatrix();
    function capture(name,azimuth,elevation){
      const az=azimuth*Math.PI/180,el=elevation*Math.PI/180;
      const dir=new T.Vector3(Math.sin(az)*Math.cos(el),Math.sin(el),Math.cos(az)*Math.cos(el));
      camera.position.copy(center).addScaledVector(dir,distance);camera.lookAt(center);camera.updateProjectionMatrix();
      renderer.info.reset();renderer.render(scene,camera);
      const gl=renderer.getContext(),debug=gl.getExtension('WEBGL_debug_renderer_info'),pixels=new Uint8Array(1280*900*4);
      gl.readPixels(0,0,1280,900,gl.RGBA,gl.UNSIGNED_BYTE,pixels);
      let foreground=0;for(let i=0;i<pixels.length;i+=4)if(Math.abs(pixels[i]-232)+Math.abs(pixels[i+1]-228)+Math.abs(pixels[i+2]-220)>22)foreground++;
      return{name,azimuth_degrees:azimuth,elevation_degrees:elevation,render_calls:renderer.info.render.calls,render_triangles:renderer.info.render.triangles,foreground_pixels:foreground,gl_error:gl.getError(),webgl2:gl instanceof WebGL2RenderingContext,unmasked_renderer:debug?gl.getParameter(debug.UNMASKED_RENDERER_WEBGL):null};
    }
    window.__qa={capture};
    return{three_revision:T.REVISION,webgl2:renderer.getContext() instanceof WebGL2RenderingContext,scene_bounds_m:{min:bounds.min.toArray(),max:bounds.max.toArray(),size:size.toArray()},instances:loaded.length,expected_triangles:loaded.reduce((n,a)=>n+a.triangles,0),assets:loaded.map(({group,...a})=>a),capture_names:['hero','reversehero','front','side','top','low-oblique']};
  },assets);
  report.three_revision=summary.three_revision;report.webgl2=summary.webgl2;report.scene_bounds_m=summary.scene_bounds_m;report.instances=summary.instances;report.expected_triangles=summary.expected_triangles;report.assets=summary.assets;
  assert.equal(summary.three_revision,'180');assert.equal(summary.webgl2,true);assert.equal(summary.instances,4);
  const views=[['hero',35,20],['reversehero',215,20],['front',0,0],['side',90,0],['top',0,89],['low-oblique',35,5]];
  report.views=[];
  for(const [name,az,el] of views){
    const measured=await page.evaluate(v=>window.__qa.capture(...v),[name,az,el]);
    const path=resolve(qa,`scene-${name}.png`);
    await page.screenshot({path,fullPage:false});
    const bytes=await readFile(path);
    report.views.push({...measured,screenshot:path.slice(repo.length+1),screenshot_bytes:bytes.length,screenshot_sha256:digest(bytes)});
  }
  assert(report.views.every(v=>v.webgl2&&v.gl_error===0&&v.render_triangles===summary.expected_triangles&&v.foreground_pixels>500));
  assert(report.views.every(v=>v.render_calls>=summary.instances));
  assert.deepEqual(report.errors,[]);assert.deepEqual(report.resource_errors,[]);
  report.status='pass';
} catch(error) {
  report.status='fail';report.error=error.stack||String(error);process.exitCode=1;
} finally {
  report.finished_at_utc=new Date().toISOString();
  const out=resolve(qa,'runtime-report.json');
  await mkdir(qa,{recursive:true});await writeFile(out,JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));
  await browser?.close();if(server.listening)await new Promise(ok=>server.close(ok));
}

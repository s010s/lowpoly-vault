/** Capture-only wheel evidence in the existing Chromium toolchain. Never publishes. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,realpath} from 'node:fs/promises';
import {resolve,dirname,extname,sep} from 'node:path';
import {createServer} from 'node:http';
import {chromium} from 'playwright';
import {posterRendererFiles,CAPTURE_POLICY} from './gallery-poster-inputs.mjs';
import {createWheelPresentation,wheelHash} from './wheel-presentation-contract.mjs';
const root=process.cwd(),out=resolve('qa/wheel-parity-output');
const scope=JSON.parse(await readFile('qa/wheel-parity-20261024/capture-inputs.json'));
const manifest=JSON.parse(await readFile('assets/manifest.json'));
const resources=JSON.parse(await readFile('site/public/gallery/resources.json'));
const samples=['nucleocrinus','spyroceras','phragmoceras','lituites','natural-levee','teleoceras','aegirocassis'];
assert.equal(scope.version,1);assert.equal(scope.publication_authority,false);assert.equal(scope.mode,'samples');
assert.deepEqual(scope.assets.map(a=>a.id),samples);assert.equal(manifest.assets.length,scope.expected_catalog_count);
const affected=manifest.assets.filter(a=>resources.posters[a.id]?.render_route==='blender-cycles-cpu-v1'&&!resources.posters[a.id]?.wheelSpec);
assert.equal(affected.length,scope.expected_affected_count);assert.equal(affected[0].id,'spyroceras');
const selected=scope.assets.map(pin=>{const asset=manifest.assets.find(a=>a.id===pin.id);assert(asset);assert.equal(asset.sha256.glb,pin.source_glb_sha256);return {...asset,wheelSpec:resources.posters[asset.id].wheelSpec};});
const closure=await posterRendererFiles(root);closure.push('site/capture-wheel-frame.js','package-lock.json');
const rendererFiles=await Promise.all([...new Set(closure)].sort().map(async path=>({path,sha256:wheelHash(await readFile(path))})));
const rendererSha256=wheelHash(JSON.stringify(rendererFiles));
const allow=new Set(rendererFiles.map(f=>f.path));
for(const asset of selected){allow.add(asset.glb);allow.add('site/public/'+resources.posters[asset.id].wheel);}
const inputBytes=new Map();
for(const asset of selected){const pin=scope.assets.find(p=>p.id===asset.id),poster=resources.posters[asset.id];const glb=await readFile(asset.glb),wheel=await readFile('site/public/'+poster.wheel),detail=await readFile('site/public/'+poster.detail);assert.equal(wheelHash(glb),pin.source_glb_sha256);assert.equal(wheelHash(wheel),pin.previous_wheel_sha256);assert.equal(wheelHash(detail),pin.unchanged_detail_sha256);inputBytes.set(asset.id,{sourceGLB:glb,previousWheel:wheel,unchangedDetail:detail});}
const html=`<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#e8e4dc;font:16px sans-serif}.row{display:flex;gap:16px}.panel{width:768px}img{width:768px;height:432px}#host{width:768px;height:432px;position:relative}#host img,#host canvas{position:absolute;inset:0;width:100%;height:100%}#stage{position:absolute;left:800px;top:520px;width:512px;height:400px}.preview-renderer{position:fixed;pointer-events:none;top:0;left:0}.hover-table{display:none}</style><body data-site-base="/"><h1 id="title">Wheel capture-only sample</h1><div class="row"><div class="panel"><h2>Published wheel</h2><img id="old"></div><div class="panel"><h2>New wheel from actual PreviewRenderer</h2><img id="new"></div></div><div class="row" id="wheel"><div class="panel"><h2>Actual live hover first frame</h2><div id="host"><img></div></div><div id="stage"></div></div><script type="importmap">{"imports":{"three":"/node_modules/three/build/three.module.js","three/":"/node_modules/three/","three/addons/":"/node_modules/three/examples/jsm/"}}</script><script type="module">import {PreviewRenderer} from '/site/gallery/renderer.js';import {captureWheelFrame} from '/site/capture-wheel-frame.js';window.capture={renderer:new PreviewRenderer(document.querySelector('#stage'),()=>{}),captureWheelFrame};</script>`;
const mime={'.js':'text/javascript','.mjs':'text/javascript','.glb':'model/gltf-binary','.png':'image/png','.json':'application/json'};
let browser,server;const report={version:1,kind:'wheel-parity-sample-evidence',status:'running',publication_authority:false,visual_review:'pending',physical_gpu:'unknown',source_commit:process.env.GITHUB_SHA||null,baseline_commit:scope.baseline_commit,renderer_sha256:rendererSha256,renderer_files:rendererFiles,cases:[],errors:[]};
try{
 await mkdir(out,{recursive:true});
 server=createServer(async(req,res)=>{try{const path=decodeURIComponent(new URL(req.url,'http://localhost').pathname).slice(1);if(path==='capture.html'){res.setHeader('Content-Type','text/html');res.end(html);return;}assert(allow.has(path)||/^node_modules\/three\/[A-Za-z0-9_.\/-]+\.js$/.test(path));const file=resolve(root,path);assert(file.startsWith(root+sep));assert.equal(await realpath(file),file);res.setHeader('Content-Type',mime[extname(file)]||'application/octet-stream');res.end(await readFile(file));}catch{res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}`;
 browser=await chromium.launch({headless:true,args:CAPTURE_POLICY.args});
 const pin=JSON.parse(await readFile('node_modules/playwright-core/browsers.json')).browsers.find(x=>x.name==='chromium');assert.equal(browser.version(),pin.browserVersion,'Pinned Chromium required');report.browser_version=browser.version();
 const page=await browser.newPage({viewport:{width:1580,height:1200},deviceScaleFactor:1,reducedMotion:'no-preference',serviceWorkers:'block'});
 await page.route('**/*',route=>new URL(route.request().url()).origin===base?route.continue():route.abort());
 page.on('pageerror',e=>report.errors.push(e.message));page.on('requestfailed',r=>report.errors.push(r.url()+' '+r.failure()?.errorText));
 await page.goto(base+'/capture.html');await page.waitForFunction(()=>window.capture?.renderer);
 for(const asset of selected){
  const captured=await page.evaluate(async asset=>{const {renderer,captureWheelFrame}=window.capture;renderer.stopHover();document.querySelector('#title').textContent=asset.id;const frame=await captureWheelFrame(renderer,asset);document.querySelector('#old').src='/site/public/gallery/posters/'+asset.id+'-wheel.png';document.querySelector('#new').src=frame.dataURL;await Promise.all([...document.querySelectorAll('#old,#new')].map(x=>x.decode()));return frame;},asset);
  const png=Buffer.from(captured.dataURL.split(',')[1],'base64'),data=inputBytes.get(asset.id);
  const record=createWheelPresentation({frame:captured,png,asset,...data,rendererSha256,browserVersion:browser.version()});
  const directory=resolve(out,asset.id);await mkdir(directory,{recursive:true});await writeFile(resolve(directory,'wheel.png'),png);await writeFile(resolve(directory,'capture.json'),JSON.stringify(record,null,2));
  const live=await page.evaluate(async({asset,frame})=>{const r=window.capture.renderer,host=document.querySelector('#host');host.querySelector('img').src=frame.dataURL;await host.querySelector('img').decode();await r.select(asset);const ready=await r.preview({...asset,wheelSpec:frame.wheelSpec},host);if(!ready)throw Error('Real live hover unavailable');await new Promise(requestAnimationFrame);r.draw();const live=r.hover.presentation.frame;const c=document.createElement('canvas');c.width=768;c.height=432;const ctx=c.getContext('2d');ctx.drawImage(host.querySelector('img'),0,0,768,432);const a=ctx.getImageData(0,0,768,432).data;ctx.clearRect(0,0,768,432);ctx.drawImage(live,0,0,768,432);const b=ctx.getImageData(0,0,768,432).data;let union=0,intersection=0,diff=0;for(let i=0;i<a.length;i+=4){const aa=a[i+3]>200,bb=b[i+3]>200;union+=aa||bb;intersection+=aa&&bb;diff+=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]);}r.hover.presentation.mix=1;r.hover.presentation.draw();r.hover.presentation.canvas.style.opacity='1';return {png:live.toDataURL('image/png'),mask_iou:intersection/Math.max(union,1),mean_rgb_absolute_error:diff/(768*432*3),gl_error:r.renderer.getContext().getError(),first_frame_id:r.stats.hoverFirstFrameId,spec:r.hover.wheelSpec};},{asset,frame:captured});
  await writeFile(resolve(directory,'live-first-frame.png'),Buffer.from(live.png.split(',')[1],'base64'));delete live.png;
  await page.screenshot({path:resolve(directory,'comparison.png'),fullPage:true});
  assert.equal(live.first_frame_id,asset.id);assert.equal(live.gl_error,0);assert.deepEqual(live.spec,captured.wheelSpec);assert(live.mask_iou>.98,`Silhouette mismatch ${asset.id}: ${live.mask_iou}`);
  report.cases.push({id:asset.id,source_glb_sha256:asset.sha256.glb,wheel_sha256:wheelHash(png),...live,status:'geometry-check-pass',visual_review:'pending'});
  console.log(`WHEEL_SAMPLE ${asset.id} IoU=${live.mask_iou}`);
 }
 assert.deepEqual(report.errors,[]);report.status='capture-and-geometry-check-pass';
}catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;}
finally{await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2));await browser?.close();if(server)await new Promise(r=>server.close(r));console.log(JSON.stringify(report,null,2));}

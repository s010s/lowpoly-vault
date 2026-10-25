/** Capture-only wheel evidence in the existing Chromium toolchain. Never publishes. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile,writeFile,mkdir,realpath} from 'node:fs/promises';
import {resolve,dirname,extname,sep} from 'node:path';
import {createServer} from 'node:http';
import {chromium} from 'playwright';
import {CAPTURE_POLICY} from './gallery-poster-inputs.mjs';
import {wheelHash} from './wheel-presentation-contract.mjs';
import {productionWheelAsset,productionWheelRenderer,productionWheelBytes,productionWheelPin,createProductionWheel,assertProductionWheelCase} from './production-wheel-contract.mjs';
const root=process.cwd(),out=resolve(process.env.PRODUCTION_WHEEL_OUTPUT||'qa/production-wheel-output');
const scope=JSON.parse(await readFile(process.env.PRODUCTION_WHEEL_INPUTS||'qa/production-wheel-inputs.json'));
assert.equal(scope.version,1);assert.equal(scope.kind,'production-wheel-capture-inputs');assert.equal(scope.publication_authority,false);
assert(scope.producer?.id?.trim()&&scope.producer?.task_id?.trim(),'Capture producer identity required');
assert(Array.isArray(scope.assets)&&scope.assets.length>0&&scope.assets.length<=30,'Explicit bounded batch required');
const selected=scope.assets.map(row=>productionWheelAsset(row.asset));assert.equal(new Set(selected.map(a=>a.id)).size,selected.length,'Duplicate capture IDs');
const renderer=await productionWheelRenderer(root),rendererFiles=renderer.files,rendererSha256=renderer.sha256;
const allow=new Set(rendererFiles.map(f=>f.path)),inputBytes=new Map();
for(const [i,asset] of selected.entries()){
 const detail=scope.assets[i].detail;allow.add(asset.glb);allow.add(detail.path);
 const sourceGLB=await productionWheelBytes(root,asset.glb),unchangedDetail=await productionWheelPin(root,detail);assert.equal(wheelHash(sourceGLB),asset.sha256.glb);
 assert.equal(unchangedDetail.subarray(0,8).toString('hex'),'89504e470d0a1a0a');assert.deepEqual([unchangedDetail.readUInt32BE(16),unchangedDetail.readUInt32BE(20)],[512,512]);assert.equal(unchangedDetail[24],8);assert.equal(unchangedDetail[25],6);
 inputBytes.set(asset.id,{sourceGLB,unchangedDetail});
}
const html=`<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#e8e4dc;font:16px sans-serif}.row{display:flex;gap:16px}.panel{width:768px}img{width:768px;height:432px;object-fit:contain}#host{width:768px;height:432px;position:relative}#host img,#host canvas{position:absolute;inset:0;width:100%;height:100%}#stage{position:absolute;left:800px;top:650px;width:512px;height:400px}.preview-renderer{position:fixed;pointer-events:none;top:0;left:0}.hover-table{display:none}</style><body data-site-base="/"><h1 id="title">New production wheel capture</h1><div class="row"><div class="panel"><h2>Unchanged-source detail</h2><img id="old"></div><div class="panel"><h2>New wheel from actual PreviewRenderer</h2><img id="new"></div></div><div class="row" id="wheel"><div class="panel"><h2>Actual live hover first frame</h2><div id="host"><img></div></div><div id="stage"></div></div><script type="importmap">{"imports":{"three":"/node_modules/three/build/three.module.js","three/":"/node_modules/three/","three/addons/":"/node_modules/three/examples/jsm/"}}</script><script type="module">import {PreviewRenderer} from '/site/gallery/renderer.js';import {captureWheelFrame} from '/site/capture-wheel-frame.js';window.capture={renderer:new PreviewRenderer(document.querySelector('#stage'),()=>{}),captureWheelFrame};</script>`;
const mime={'.js':'text/javascript','.mjs':'text/javascript','.glb':'model/gltf-binary','.png':'image/png','.json':'application/json'};
let browser,server;const report={version:1,kind:'new-production-wheel-capture-evidence',producer:scope.producer,status:'running',publication_authority:false,visual_review:'pending',physical_gpu:'unknown',source_commit:process.env.GITHUB_SHA||null,renderer_sha256:rendererSha256,renderer_files:rendererFiles,cases:[],errors:[]};
try{
 await mkdir(out,{recursive:true});
 server=createServer(async(req,res)=>{try{const path=decodeURIComponent(new URL(req.url,'http://localhost').pathname).slice(1);if(path==='capture.html'){res.setHeader('Content-Type','text/html');res.end(html);return;}assert(allow.has(path)||/^node_modules\/three\/[A-Za-z0-9_.\/-]+\.js$/.test(path));const file=resolve(root,path);assert(file.startsWith(root+sep));assert.equal(await realpath(file),file);res.setHeader('Content-Type',mime[extname(file)]||'application/octet-stream');res.end(await readFile(file));}catch{res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}`;
 browser=await chromium.launch({headless:true,args:CAPTURE_POLICY.args});
 const pin=JSON.parse(await readFile('node_modules/playwright-core/browsers.json')).browsers.find(x=>x.name==='chromium');assert.equal(browser.version(),pin.browserVersion,'Pinned Chromium required');report.browser_version=browser.version();
 const page=await browser.newPage({viewport:{width:1580,height:1200},deviceScaleFactor:1,reducedMotion:'no-preference',serviceWorkers:'block'});
 await page.route('**/*',route=>new URL(route.request().url()).origin===base?route.continue():route.abort());
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error'&&/THREE\.|WebGL|shader|GL_INVALID|CONTEXT_LOST/i.test(m.text()))report.errors.push(m.text());});page.on('requestfailed',r=>report.errors.push(r.url()+' '+r.failure()?.errorText));
 await page.goto(base+'/capture.html');await page.waitForFunction(()=>window.capture?.renderer);
 for(const asset of selected){
  const captured=await page.evaluate(async ({asset,detailPath})=>{const {renderer,captureWheelFrame}=window.capture;renderer.stopHover();document.querySelector('#title').textContent=asset.id;const gl=renderer.renderer.getContext();if(gl.isContextLost())throw Error('WebGL context lost before capture');const frame=await captureWheelFrame(renderer,asset);if(gl.isContextLost()||gl.getError()!==gl.NO_ERROR)throw Error('WebGL capture error');document.querySelector('#old').src='/'+detailPath;document.querySelector('#new').src=frame.dataURL;await Promise.all([...document.querySelectorAll('#old,#new')].map(x=>x.decode()));return frame;},{asset,detailPath:scope.assets[selected.indexOf(asset)].detail.path});
  const png=Buffer.from(captured.dataURL.split(',')[1],'base64'),data=inputBytes.get(asset.id);
  const record=createProductionWheel({frame:captured,png,asset,...data,rendererSha256,browserVersion:browser.version()});
  const directory=resolve(out,asset.id);await mkdir(directory,{recursive:true});await writeFile(resolve(directory,'wheel.png'),png);await writeFile(resolve(directory,'capture.json'),JSON.stringify(record,null,2));
  const live=await page.evaluate(async({asset,frame})=>{const r=window.capture.renderer,host=document.querySelector('#host');host.querySelector('img').src=frame.dataURL;await host.querySelector('img').decode();await r.select(asset);const ready=await r.preview({...asset,wheelSpec:frame.wheelSpec},host);if(!ready)throw Error('Real live hover unavailable');await new Promise(requestAnimationFrame);r.draw();const live=r.hover.presentation.frame;const c=document.createElement('canvas');c.width=768;c.height=432;const ctx=c.getContext('2d');ctx.drawImage(host.querySelector('img'),0,0,768,432);const a=ctx.getImageData(0,0,768,432).data;ctx.clearRect(0,0,768,432);ctx.drawImage(live,0,0,768,432);const b=ctx.getImageData(0,0,768,432).data;let union=0,intersection=0,diff=0;for(let i=0;i<a.length;i+=4){const aa=a[i+3]>200,bb=b[i+3]>200;union+=aa||bb;intersection+=aa&&bb;diff+=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]);}await r.revealHover();return {png:live.toDataURL('image/png'),mask_iou:intersection/Math.max(union,1),mean_rgb_absolute_error:diff/(768*432*3),context_lost:r.renderer.getContext().isContextLost(),gl_error:r.renderer.getContext().getError(),first_frame_id:r.stats.hoverFirstFrameId,spec:r.hover.wheelSpec};},{asset,frame:captured});
  await writeFile(resolve(directory,'live-first-frame.png'),Buffer.from(live.png.split(',')[1],'base64'));delete live.png;
  await page.screenshot({path:resolve(directory,'comparison.png'),fullPage:true});
  assert.equal(live.first_frame_id,asset.id);assert.equal(live.gl_error,0);assert.equal(live.context_lost,false);assert(live.mean_rgb_absolute_error<2,`Pixel color mismatch ${asset.id}: ${live.mean_rgb_absolute_error}`);assert.deepEqual(live.spec,captured.wheelSpec);assert(live.mask_iou>.98,`Silhouette mismatch ${asset.id}: ${live.mask_iou}`);
  let lifecycle=null;
  {
   lifecycle=await page.evaluate(async({asset,frame})=>{const r=window.capture.renderer,host=document.querySelector('#host');r.stopHover();await new Promise(resolve=>setTimeout(resolve,220));if(host.querySelector('canvas'))throw Error('Hover exit did not remove surface');if(host.querySelector('img').style.opacity!=='')throw Error('Hover exit did not restore poster');if(!await r.preview({...asset,wheelSpec:frame.wheelSpec},host))throw Error('Re-entry unavailable');r.draw();const first=r.hover.presentation.frame.toDataURL('image/png');await r.revealHover();const frames=[];for(let i=0;i<8;i++){const angle=i*Math.PI/4;r.hover.model.rotation.y=angle;r.hover.effect?.rotate(angle);r.draw(true);const c=r.hover.presentation.frame,ctx=c.getContext('2d'),pixels=ctx.getImageData(0,0,c.width,c.height).data;let border=0;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if((x===0||y===0||x===c.width-1||y===c.height-1)&&pixels[(y*c.width+x)*4+3]>200)border++;frames.push({yaw:i*45,border_opaque_pixels:border,png:c.toDataURL('image/png')});}return {reentry_png:first,frames,context_lost:r.renderer.getContext().isContextLost(),gl_error:r.renderer.getContext().getError()};},{asset,frame:captured});
   assert.deepEqual(Buffer.from(lifecycle.reentry_png.split(',')[1],'base64'),await readFile(resolve(directory,'live-first-frame.png')),'Re-entry frame changed');delete lifecycle.reentry_png;lifecycle.reentry_exact=true;assert.equal(lifecycle.context_lost,false);assert.equal(lifecycle.gl_error,0);
   for(const f of lifecycle.frames){await writeFile(resolve(directory,`turn-${f.yaw}.png`),Buffer.from(f.png.split(',')[1],'base64'));delete f.png;assert.equal(f.border_opaque_pixels,0,`Turntable clipping ${asset.id} yaw ${f.yaw}`);}
   await writeFile(resolve(directory,'lifecycle.json'),JSON.stringify(lifecycle,null,2));
  }
  const result={id:asset.id,source_glb_sha256:asset.sha256.glb,wheel_sha256:wheelHash(png),...live,lifecycle,status:'geometry-check-pass',visual_review:'pending'};assertProductionWheelCase(result,{asset,pngPin:record.png,wheelSpec:captured.wheelSpec});report.cases.push(result);
  console.log(`WHEEL_SAMPLE ${asset.id} IoU=${live.mask_iou}`);
 }
 assert.deepEqual(report.errors,[]);report.status='capture-and-geometry-check-pass';
}catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;}
finally{await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2));await browser?.close();if(server)await new Promise(r=>server.close(r));console.log(JSON.stringify({status:report.status,cases:report.cases.length,errors:report.errors,error:report.error}));}

/** Independent actual Chromium/WebGL regression for one shared real-model stage. */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, readdir, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import assert from 'node:assert/strict';

const root=resolve(process.env.GALLERY_DIR||'dist');
const output=resolve(process.env.QA_OUTPUT_DIR||'qa/shared-model-preview/browser');
const prefix='/lowpoly-vault/';
const cpuDOMRaster=!/^(0|false)$/i.test(process.env.QA_CPU_DOM_RASTER||'1');
const browserArgs=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader',...(cpuDOMRaster?['--disable-gpu-rasterization']:[])];
const catalog=JSON.parse(await readFile(resolve(root,'assets/catalog.json'),'utf8'));
const assets=catalog.initial;
const viewerFile=(await readdir(resolve(root,'assets'))).find(n=>/^viewer-.*\.js$/.test(n));
assert(viewerFile,'Built viewer module required');
const report={status:'running',commit:process.env.GITHUB_SHA||null,execution_environment:process.env.GITHUB_ACTIONS?'GitHub Actions Linux':'cloud computer Linux',started:new Date().toISOString(),checks:[],cases:[],page_errors:[],screenshots:[],videos:[],limitations:['Actual Linux Chromium, ANGLE SwiftShader software WebGL; timings are local loopback and emulated input/viewport, not user-device or production-network benchmarks.','Decoded bytes are the application’s geometry/texture estimates, not driver GPU memory or JS heap measurements.'],server_requests:[]};
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp','.png':'image/png','.glb':'model/gltf-binary'};
let fixture;
const server=createServer(async(req,res)=>{
 const started=performance.now(); let bytes,contentType;
 try{
  const url=new URL(req.url,'http://localhost');
  if(!url.pathname.startsWith(prefix))throw new Error('Outside root');
  if(url.pathname===prefix+'__qa__/textured-stale.glb')bytes=fixture;
  else{let path=resolve(root,decodeURIComponent(url.pathname.slice(prefix.length))||'index.html');if(path!==root&&!path.startsWith(root+sep))throw new Error('Outside root');if((await stat(path)).isDirectory())path=resolve(path,'index.html');bytes=await readFile(path);contentType=mime[extname(path)];}
  res.writeHead(200,{'Content-Type':contentType||mime[extname(url.pathname)]||'application/octet-stream','Content-Length':bytes.length,'Cache-Control':'no-store'}).end(bytes);
  report.server_requests.push({path:url.pathname,status:200,bytes:bytes.length,ms:performance.now()-started});
 }catch{res.writeHead(404).end();report.server_requests.push({path:req.url,status:404,bytes:0,ms:performance.now()-started});}
});
let browser,base,current;
const requestLog=[];
const glbRequests=label=>requestLog.filter(r=>r.label===label&&/\.glb(?:\?|$)/.test(r.url));
const turntableRequests=label=>requestLog.filter(r=>r.label===label&&/turntable|frame\d{3}/.test(r.url));
function check(c,name,condition,detail){c.checks.push({name,pass:Boolean(condition),...(detail!==undefined?{detail}:{})});assert(condition,name);}
async function test(name,fn,options={}){
 const {recordVideo={dir:output,size:{width:1440,height:1000}},...contextOptions}=options;
 const c={name,checks:[],status:'running',video_recording:Boolean(recordVideo)};report.cases.push(c);
 // Timing/event probes run without video readback. Dedicated interaction cases
 // retain videos, while these cases still capture their settled screenshots.
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'no-preference',...(recordVideo?{recordVideo}:{}),...contextOptions});
 const page=await context.newPage();current=page;
 page.on('pageerror',error=>report.page_errors.push({case:name,error:error.message}));
 page.on('request',r=>requestLog.push({label:name,url:r.url(),type:r.resourceType(),time:Date.now()}));
 try{await fn(page,c,context);c.status='passed';}catch(error){c.status='failed';c.error=error.stack;try{await shot(page,name+'-failure');}catch{}}
 finally{const video=page.video();await context.close();if(video)report.videos.push({case:name,file:(await video.path()).split('/').at(-1)});await save();}
 console.log(c.status.toUpperCase()+': '+name+(c.error?'\n'+c.error:''));
}
async function save(){await writeFile(resolve(output,'report.json'),JSON.stringify(report,null,2));}
async function shot(page,name){await page.screenshot({path:resolve(output,name+'.png'),fullPage:false});report.screenshots.push(name+'.png');}
const card=(page,id)=>page.locator('#grid .asset-card[data-id="'+id+'"]');
async function listing(page){await page.goto(base+prefix+'models/');await page.waitForFunction(()=>document.querySelector('#grid')?.ariaBusy==='false');await page.mouse.move(1,1);}
async function hover(page,id='natural-arch'){const el=card(page,id);await el.scrollIntoViewIfNeeded();const r=await el.locator('.asset-image').boundingBox();await page.mouse.move(r.x+r.width*.5,r.y+r.height*.5);await page.waitForFunction(id=>document.querySelector('#grid [data-id="'+id+'"]')?.dataset.previewState==='ready'&&window.__vaultGPU?.renderedFrames>0,id,{timeout:30000});return el;}
async function detailReady(page,id){await page.waitForFunction(id=>document.querySelector('#viewer-dialog')?.open&&document.querySelector('#canvas-host')?.dataset.modelState==='ready'&&document.querySelector('#canvas-host')?.dataset.presentedUrl?.endsWith('/'+id+'.glb'),id,{timeout:30000});await page.waitForTimeout(200);}
async function close(page,{moveAway=false}={}){await page.locator('#close').click();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open&&!document.querySelector('.stage-flight')&&(!window.__vaultGPU||window.__vaultGPU.liveScenes===0));if(moveAway)await page.mouse.move(1,1);await page.waitForTimeout(80);}
async function stage(page){await page.evaluate(async path=>{const {ModelStage}=await import(path);window.__qaStage=new ModelStage();},base+prefix+'assets/'+viewerFile);}
async function stats(page){return page.evaluate(()=>({...window.__vaultGPU}));}
async function view(page){return page.evaluate(()=>window.__qaStage.presentationInfo);}
function angle(a,b){return Math.abs(((a-b+540)%360)-180);}
function sameView(c,a,b,label){check(c,label+' azimuth',angle(a.azimuth_deg,b.azimuth_deg)<.001,{a,b});check(c,label+' elevation',Math.abs(a.elevation_deg-b.elevation_deg)<.001);check(c,label+' distance',Math.abs(a.distance-b.distance)<.00001);}
async function canonicalView(page){return page.evaluate(()=>window.__qaStage.canonicalView);}
async function canonicalPoster(page,c,id,label){
 await page.waitForFunction(()=>!document.querySelector('.stage-flight')&&window.__vaultPreview?.activeId===null&&(!window.__vaultGPU||window.__vaultGPU.liveScenes===0));
 check(c,label+' has no retained snapshot or live canvas',await page.locator('.model-preview-snapshot,.model-canvas,.return-poster').count()===0);
 check(c,label+' source card displays only its canonical poster',await card(page,id).locator('.asset-image').evaluate(host=>{
  const img=host.querySelector('img');
  if(!img?.complete||!img.naturalWidth||host.querySelectorAll('img').length!==1)return false;
  for(let node=img;node;node=node.parentElement){const css=getComputedStyle(node);if(css.visibility==='hidden'||css.display==='none'||Number(css.opacity)<.99)return false;}
  return !host.closest('[data-detail-origin]');
 }));
}
async function trafficBoundary(page){
 return {browser_start_ms:await page.evaluate(()=>performance.now()),server_start_index:report.server_requests.length,request_start_index:requestLog.length};
}
async function trafficSince(page,boundary){
 const end=await page.evaluate(()=>performance.now());
 const resources=await page.evaluate(start=>performance.getEntriesByType('resource').filter(r=>r.startTime>=start&&/\.(?:js|glb)(?:$|\?)/.test(new URL(r.name).pathname)).map(r=>({url:r.name,start_ms:r.startTime,duration_ms:r.duration,transfer_bytes:r.transferSize,encoded_body_bytes:r.encodedBodySize,decoded_body_bytes:r.decodedBodySize})),boundary.browser_start_ms);
 const serverRows=report.server_requests.slice(boundary.server_start_index).filter(r=>/\.(?:js|glb)(?:$|\?)/.test(r.path));
 const summarize=extension=>{
  const matching=resources.filter(r=>new URL(r.url).pathname.endsWith(extension));
  return {requests:matching.length,transfer_bytes:matching.reduce((n,r)=>n+r.transfer_bytes,0),encoded_body_bytes:matching.reduce((n,r)=>n+r.encoded_body_bytes,0),decoded_body_bytes:matching.reduce((n,r)=>n+r.decoded_body_bytes,0),server_body_bytes:serverRows.filter(r=>r.path.endsWith(extension)).reduce((n,r)=>n+r.bytes,0)};
 };
 const viewer_js_and_dependencies=summarize('.js'),glb=summarize('.glb');
 const total=Object.fromEntries(Object.keys(glb).map(key=>[key,glb[key]+viewer_js_and_dependencies[key]]));
 return {window:{...boundary,browser_end_ms:end,server_end_index:report.server_requests.length,request_end_index:requestLog.length},viewer_js_and_dependencies,glb,total,resources,measurement:'Actual local uncompressed loopback HTTP. ResourceTiming transfer_bytes includes HTTP overhead; server_body_bytes is bytes served without gzip. Only JS initiated in this hover window and GLB are included; initial posters/catalog/UI traffic is excluded. This is not production compressed transfer size.'};
}
async function pixels(page,selector='.model-canvas'){
 return page.locator(selector).evaluate(canvas=>{
  if(canvas.classList.contains('model-canvas'))window.__qaStage._draw();
  const copy=document.createElement('canvas');copy.width=256;copy.height=256;
  const ctx=copy.getContext('2d',{willReadFrequently:true});const side=Math.min(canvas.width,canvas.height);ctx.drawImage(canvas,(canvas.width-side)/2,(canvas.height-side)/2,side,side,0,0,256,256);const p=ctx.getImageData(0,0,256,256).data;
  let transparent=0,foreground=0,hash=2166136261,sx=0,sy=0,left=256,right=-1,top=256,bottom=-1,weight=0;const rgb=[0,0,0];
  for(let i=0;i<p.length;i++){hash=Math.imul(hash^p[i],16777619)>>>0;if(i%4===3){if(p[i]<=3)transparent++;if(p[i]>16){const n=i>>>2,x=n%256,y=Math.floor(n/256);foreground++;weight+=p[i];for(let k=0;k<3;k++)rgb[k]+=p[i-3+k]*p[i];sx+=x;sy+=y;left=Math.min(left,x);right=Math.max(right,x);top=Math.min(top,y);bottom=Math.max(bottom,y);}}}
  return {hash:hash.toString(16),foreground_rgb_mean:rgb.map(v=>v/weight),transparent_fraction:transparent/65536,foreground,corner_alpha_max:Math.max(p[3],p[1023],p[(255*256)*4+3],p.at(-1)),bbox:{left,right,top,bottom},centroid:{x:sx/foreground,y:sy/foreground}};
 });
}
function alpha(c,p,label){check(c,label+' real visible silhouette',p.foreground>300,p);check(c,label+' transparent background',p.transparent_fraction>.2&&p.corner_alpha_max<=3,p);}

// A separate in-memory fixture adds a PNG texture to the real geometry. The
// source GLB stays byte-for-byte untouched; it makes native image decode awaitable.
const modelBytes=await readFile(resolve(root,assets.find(a=>a.id==='natural-arch').glb));
const jsonLength=modelBytes.readUInt32LE(12),json=JSON.parse(modelBytes.subarray(20,20+jsonLength).toString());
const originalBin=modelBytes.subarray(28+jsonLength),parts=[originalBin];let binOffset=originalBin.length;
for(const mesh of json.meshes)for(const primitive of mesh.primitives)if(primitive.material===0){
 const count=json.accessors[primitive.attributes.POSITION].count,uv=Buffer.alloc(count*8);
 const bufferView=json.bufferViews.push({buffer:0,byteOffset:binOffset,byteLength:uv.length,target:34962})-1;
 primitive.attributes.TEXCOORD_0=json.accessors.push({bufferView,componentType:5126,count,type:'VEC2',min:[0,0],max:[0,0]})-1;
 parts.push(uv);binOffset+=uv.length;
}
const png=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAFUlEQVR4nGP8////fwYGBgYmBigAAD34BADaOyqcAAAAAElFTkSuQmCC','base64');
const imageView=json.bufferViews.push({buffer:0,byteOffset:binOffset,byteLength:png.length})-1;
parts.push(png,Buffer.alloc((4-png.length%4)%4));const binBytes=Buffer.concat(parts);json.buffers[0].byteLength=binBytes.length;
json.images=[{bufferView:imageView,mimeType:'image/png'}];json.textures=[{source:0}];
json.materials[0].pbrMetallicRoughness.baseColorTexture={index:0};
let jsonBytes=Buffer.from(JSON.stringify(json));jsonBytes=Buffer.concat([jsonBytes,Buffer.alloc((4-jsonBytes.length%4)%4,32)]);
fixture=Buffer.alloc(28+jsonBytes.length+binBytes.length);modelBytes.copy(fixture,0,0,12);fixture.writeUInt32LE(fixture.length,8);fixture.writeUInt32LE(jsonBytes.length,12);fixture.writeUInt32LE(0x4e4f534a,16);jsonBytes.copy(fixture,20);fixture.writeUInt32LE(binBytes.length,20+jsonBytes.length);fixture.writeUInt32LE(0x004e4942,24+jsonBytes.length);binBytes.copy(fixture,28+jsonBytes.length);

try{
 await mkdir(output,{recursive:true});await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port;
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:browserArgs});
 report.timing_method='Cold/warm wall time includes the intentional 180ms hover dwell; firstPreviewMilliseconds and lastShowMilliseconds are app load/render timings. ResourceTiming and server byte counts are actual loopback HTTP transfers.';
 report.browser={version:browser.version(),executable:process.env.CHROMIUM_PATH||chromium.executablePath(),args:browserArgs};
 report.dom_raster_mode=cpuDOMRaster?'cpu':'browser-default';
 await test('poster-dwell-and-cold-warm',async(page,c)=>{
  await listing(page);await page.waitForTimeout(500);
  check(c,'initial static posters fetch zero GLBs',glbRequests(c.name).length===0,glbRequests(c.name));check(c,'initial creates no WebGL stage',await page.evaluate(()=>!window.__vaultGPU));
  check(c,'no image-frame/turntable fetches',turntableRequests(c.name).length===0,turntableRequests(c.name));
  const el=card(page,'natural-arch');await el.scrollIntoViewIfNeeded();const r=await el.locator('.asset-image').boundingBox();
  await page.mouse.move(r.x+r.width/2,r.y+r.height/2);await page.waitForTimeout(95);await page.mouse.move(1,1);await page.waitForTimeout(220);
  check(c,'short hover under 180ms loads no GLB',glbRequests(c.name).length===0);await shot(page,'01-static-poster');
  const coldBoundary=await trafficBoundary(page);const start=performance.now();await hover(page);c.cold_wall_ms=performance.now()-start;await stage(page);const cold=await stats(page);c.cold=cold;c.cold_traffic=await trafficSince(page,coldBoundary);check(c,'cold transfer includes lazy viewer JS and GLB',c.cold_traffic.viewer_js_and_dependencies.requests>=1&&c.cold_traffic.glb.requests===1&&c.cold_traffic.total.transfer_bytes>c.cold_traffic.glb.transfer_bytes,c.cold_traffic);
  check(c,'actual WebGL renders triangles',await page.locator('.model-canvas').evaluate(x=>Number(x.parentElement.dataset.renderTriangles)>0));alpha(c,await pixels(page),'hover');
  c.gpu=await page.evaluate(()=>{const s=window.__qaStage,g=s._renderer.getContext(),ext=g.getExtension('WEBGL_debug_renderer_info');return {renderer:ext?g.getParameter(ext.UNMASKED_RENDERER_WEBGL):g.getParameter(g.RENDERER),vendor:ext?g.getParameter(ext.UNMASKED_VENDOR_WEBGL):g.getParameter(g.VENDOR),webgl:g.getParameter(g.VERSION),maxTextureSize:g.getParameter(g.MAX_TEXTURE_SIZE),maxRenderbufferSize:g.getParameter(g.MAX_RENDERBUFFER_SIZE),drawingBuffer:[g.drawingBufferWidth,g.drawingBufferHeight]};});
  check(c,'one GLB request and parse for cold preview',cold.networkRequests===1&&cold.parseCount===1,cold);await shot(page,'02-live-hover');
  await page.evaluate(()=>{window.__qaIdentity={canvas:window.__qaStage._renderer.domElement,scene:window.__qaStage._gltf.scene,resource:window.__qaStage._activeResource};});
  await page.mouse.move(1,1);await page.waitForTimeout(120);const idle1=await stats(page);await page.waitForTimeout(260);const idle2=await stats(page);check(c,'inactive preview RAF stopped',idle2.renderedFrames===idle1.renderedFrames&&idle2.rafPending===0&&idle2.liveScenes===0,{idle1,idle2});
  const warmBoundary=await trafficBoundary(page);const warmStart=performance.now();await hover(page);c.warm_wall_ms=performance.now()-warmStart;const warm=await stats(page);c.warm=warm;c.warm_traffic=await trafficSince(page,warmBoundary);check(c,'warm hover transfers zero viewer JS and GLB bytes',c.warm_traffic.total.requests===0&&c.warm_traffic.total.transfer_bytes===0&&c.warm_traffic.total.server_body_bytes===0,c.warm_traffic);
  check(c,'warm hover no extra network or parse',warm.networkRequests===cold.networkRequests&&warm.parseCount===cold.parseCount,{cold,warm});
  check(c,'warm hover reuses exact decoded object and canvas',await page.evaluate(()=>window.__qaStage._gltf.scene===window.__qaIdentity.scene&&window.__qaStage._activeResource===window.__qaIdentity.resource&&window.__qaStage._renderer.domElement===window.__qaIdentity.canvas));
  c.actual_glb_requests=glbRequests(c.name);c.actual_traffic=await page.evaluate(()=>performance.getEntriesByType('resource').filter(r=>/\.glb$/.test(r.name)).map(r=>({url:r.name,duration:r.duration,transferSize:r.transferSize,encodedBodySize:r.encodedBodySize,decodedBodySize:r.decodedBodySize})));
 });
 await test('continuity-reuse-theme-resize-history',async(page,c)=>{
  await listing(page);const el=await hover(page);await stage(page);await page.evaluate(()=>{window.__qaStage.setView(137,31,window.__qaStage.presentationInfo.distance*.87);window.__qaIdentity={canvas:window.__qaStage._renderer.domElement,scene:window.__qaStage._gltf.scene,resource:window.__qaStage._activeResource};});
  const before=await stats(page),hoverView=await view(page),hoverPixels=await pixels(page);c.hover={view:hoverView,pixels:hoverPixels};
  await el.focus();await page.keyboard.press('Enter');await detailReady(page,'natural-arch');sameView(c,hoverView,await view(page),'list to detail');const detailPixels=await pixels(page);alpha(c,detailPixels,'detail');
  check(c,'same GLTF scene resource and canvas in detail',await page.evaluate(()=>window.__qaStage._gltf.scene===window.__qaIdentity.scene&&window.__qaStage._activeResource===window.__qaIdentity.resource&&window.__qaStage._renderer.domElement===window.__qaIdentity.canvas));
  const after=await stats(page);check(c,'list/detail handoff has no fetch parse or renderer creation',before.networkRequests===after.networkRequests&&before.parseCount===after.parseCount&&after.rendererCreations===1,{before,after});
  check(c,'only one real WebGL canvas in DOM',await page.locator('.model-canvas').count()===1);check(c,'lighting silhouette continuity',Math.abs(hoverPixels.foreground-detailPixels.foreground)/hoverPixels.foreground<.025,{hoverPixels,detailPixels});check(c,'lighting color continuity',hoverPixels.foreground_rgb_mean.every((v,k)=>Math.abs(v-detailPixels.foreground_rgb_mean[k])<3),{hover: hoverPixels.foreground_rgb_mean,detail: detailPixels.foreground_rgb_mean});await shot(page,'03-detail-shared-real-model');
  const saved=await view(page);await page.locator('#viewer-dialog [data-theme-toggle]').click();await page.waitForTimeout(100);sameView(c,saved,await view(page),'theme preserves view');check(c,'theme preserves model pixels',JSON.stringify(await pixels(page))===JSON.stringify(detailPixels));await shot(page,'04-dark-detail');
  await page.setViewportSize({width:1000,height:740});await page.waitForTimeout(160);sameView(c,saved,await view(page),'resize preserves view');alpha(c,await pixels(page),'resized');await shot(page,'05-resized-detail');
  await page.locator('#canvas-host').focus();await page.keyboard.press('ArrowRight');await page.keyboard.press('ArrowUp');await page.keyboard.press('+');await page.waitForTimeout(80);const inspected=await view(page);c.inspected=inspected;
  check(c,'detail keyboard orbit and zoom change view',angle(saved.azimuth_deg,inspected.azimuth_deg)>1&&Math.abs(saved.elevation_deg-inspected.elevation_deg)>1&&Math.abs(saved.distance-inspected.distance)>.01);
  const canonical=await canonicalView(page);await close(page);await canonicalPoster(page,c,'natural-arch','completed detail return');await shot(page,'06-returned-canonical-poster');
  await card(page,'natural-arch').focus();await page.keyboard.press('Enter');await detailReady(page,'natural-arch');sameView(c,canonical,await view(page),'canonical poster to reopened detail');await close(page);
  await page.goForward();await detailReady(page,'natural-arch');check(c,'browser Forward restores modal route',await page.locator('#viewer-dialog').evaluate(d=>d.open)&&/\/models\/natural-arch\/$/.test(new URL(page.url()).pathname));
  await page.goBack();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);check(c,'Back restores listing and scroll unlocked',await page.evaluate(()=>document.body.style.overflow===''&&!document.querySelector('#catalog-page').hidden));
  for(let i=0;i<3;i++){await card(page,'natural-arch').click();await detailReady(page,'natural-arch');await close(page);}
  const end=await stats(page);check(c,'repeated reopen retains single renderer and one original parse',end.rendererCreations===1&&end.parseCount===1&&end.networkRequests===1,end);
 });
 await test('actual-model-canonical-return-progression',async(page,c)=>{
  await listing(page);const el=await hover(page);await stage(page);
  await el.focus();await page.keyboard.press('Enter');await detailReady(page,'natural-arch');
  const canonical=await canonicalView(page);check(c,'canonical camera is the sole poster preset',angle(canonical.azimuth_deg,42)<.001&&Math.abs(canonical.elevation_deg-23.3)<.001&&canonical.distance>0,canonical);
  await page.evaluate(()=>{const s=window.__qaStage;s.setView(329,52,s.canonicalView.distance*.71);});
  const inspected=await view(page),before=await stats(page);
  await page.evaluate(()=>{
   const s=window.__qaStage,canvas=s._renderer.domElement,scene=s._gltf.scene,resource=s._activeResource;
   const image=document.querySelector('#grid [data-id="natural-arch"] .asset-image'),r=image.getBoundingClientRect(),side=Math.min(r.width,r.height);
   window.__qaReturn={draws:[],frames:[],errors:[],target:{x:r.x+(r.width-side)/2,y:r.y+(r.height-side)/2,width:side,height:side}};
   window.__vaultFrameProbe=({canvas:drawCanvas,host,view})=>{
    if(!host.classList.contains('live-model-return'))return;
    try{const r=host.getBoundingClientRect();window.__qaReturn.draws.push({time:performance.now(),progress:Number(host.dataset.returnProgress),phase:host.dataset.returnPhase,view:{...view},rect:{x:r.x,y:r.y,width:r.width,height:r.height},same_canvas:drawCanvas===canvas,same_scene:s._gltf.scene===scene,same_resource:s._activeResource===resource,canvases:document.querySelectorAll('.model-canvas').length,live_scenes:window.__vaultGPU.liveScenes});}catch(error){window.__qaReturn.errors.push(error.message);}
   };
   const sample=()=>{const flight=document.querySelector('.live-model-return');if(flight){const live=flight.querySelector('.model-canvas'),poster=flight.querySelector('.return-poster'),hostCSS=getComputedStyle(flight),liveCSS=getComputedStyle(live),posterCSS=getComputedStyle(poster);window.__qaReturn.frames.push({time:performance.now(),progress:Number(flight.dataset.returnProgress),phase:flight.dataset.returnPhase,opacity:Number(liveCSS.opacity),poster_opacity:Number(posterCSS.opacity),host_opacity:Number(hostCSS.opacity),isolation:hostCSS.isolation,live_blend:liveCSS.mixBlendMode,poster_blend:posterCSS.mixBlendMode,poster_visible:posterCSS.visibility!=='hidden',origin_hidden:Boolean(image.closest('[data-detail-origin]'))});}window.__qaReturnRAF=requestAnimationFrame(sample);};sample();
  });
  await close(page);await canonicalPoster(page,c,'natural-arch','animated canonical return');
  c.return_motion=await page.evaluate(()=>{cancelAnimationFrame(window.__qaReturnRAF);delete window.__vaultFrameProbe;return window.__qaReturn;});
  const {draws,frames,errors,target}=c.return_motion;
  check(c,'return actual-draw probe succeeds',errors.length===0,errors);
  check(c,'return animates actual WebGL model through intermediate poses',draws.length>=3&&draws.some(d=>d.progress>0&&d.progress<1),draws);
  sameView(c,inspected,draws[0].view,'first live return frame starts at inspected pose');
  const startRect=draws[0].rect,delta=((canonical.azimuth_deg-inspected.azimuth_deg+540)%360)-180;
  for(let i=0;i<draws.length;i++){
   const d=draws[i],p=d.progress,k=1-(1-p)**3;
   check(c,'return draw '+i+' borrows sole original renderer resource',d.same_canvas&&d.same_scene&&d.same_resource&&d.canvases===1&&d.live_scenes===1,d);
   check(c,'return draw '+i+' has valid monotonic progress',Number.isFinite(p)&&p>=0&&p<=1&&(!i||p>=draws[i-1].progress),d);
   const expected={azimuth_deg:inspected.azimuth_deg+delta*k,elevation_deg:inspected.elevation_deg+(canonical.elevation_deg-inspected.elevation_deg)*k,distance:inspected.distance+(canonical.distance-inspected.distance)*k};
   sameView(c,expected,d.view,'analytic shortest-angle return draw '+i);
   check(c,'return draw '+i+' center and square follow intended shrink',['x','y','width','height'].every(key=>Math.abs(d.rect[key]-(startRect[key]+(target[key]-startRect[key])*k))<=1),{actual:d.rect,start:startRect,target,k});
  }
  const aligned=draws.filter(d=>d.progress===1);check(c,'canonical angle and fit reached before retiring actual model',aligned.length>0,draws);sameView(c,canonical,aligned.at(-1).view,'final canonical live draw');
  const fade=frames.filter(f=>f.phase==='fading');check(c,'crossfade exposes matching canonical poster while live model fades',fade.length>0&&fade.every(f=>f.progress===1&&f.poster_visible)&&fade.some(f=>f.opacity>0&&f.opacity<.99&&f.poster_opacity>0&&f.poster_opacity<1),fade);
  check(c,'return uses an isolated complementary plus-lighter dissolve',frames.length>0&&frames.every(f=>f.isolation==='isolate'&&f.live_blend==='plus-lighter'&&f.poster_blend==='plus-lighter'&&f.host_opacity===1&&Math.abs(f.opacity+f.poster_opacity-1)<=.00001),frames);
  check(c,'origin poster stays hidden until the final canonical swap',frames.every(f=>f.origin_hidden),frames);
  check(c,'transient poster appears only at canonical alignment',frames.every(f=>f.phase==='fading'||!f.poster_visible),frames);
  const after=await stats(page);check(c,'return creates no renderer parse fetch or extra lease',after.rendererCreations===1&&after.networkRequests===before.networkRequests&&after.parseCount===before.parseCount&&after.liveScenes===0&&after.activeLeases===0&&after.rafPending===0,{before,after});
  await shot(page,'06b-actual-model-returned-canonical-poster');
 },{recordVideo:false});
 await test('moving-close-forward-back-before-queued-reopen',async(page,c)=>{
  await listing(page);const el=await hover(page);await stage(page);await el.focus();await page.keyboard.press('Enter');await detailReady(page,'natural-arch');
  await page.evaluate(()=>{const s=window.__qaStage;s.setView(315,49,s.canonicalView.distance*.76);});
  const canonical=await canonicalView(page),before=await stats(page);
  await page.evaluate(()=>{
   const stage=window.__qaStage,canvas=stage._renderer.domElement,scene=stage._gltf.scene,resource=stage._activeResource;
   const state=window.__qaTriple={draws:[],events:[],frames:[],forwardRequested:false,backRequested:false,finalBackSeen:false,holdChrome:true,cancellationSettlementsHeld:0,fixture:'Delay only cancelled closing-chrome finished promises until final native Back popstate, so the queued reopen cannot win the event/microtask race.'};
   let releaseChrome;const chromeGate=new Promise(resolve=>{releaseChrome=resolve;});
   const ids=new WeakMap();let nextId=0;const id=host=>{if(!ids.has(host))ids.set(host,++nextId);return ids.get(host);};
   // Keep the real animations and native history traversals. Only defer the
   // cancelled chrome promise's settlement to deterministically exercise the
   // queued-route branch before it can reopen the detail in a microtask.
   const animate=Element.prototype.animate;window.__qaTripleOriginalAnimate=animate;
   Element.prototype.animate=function(...args){
    const animation=animate.apply(this,args),keyframes=args[0];
    const closing=Array.isArray(keyframes)&&Number(keyframes.at(-1)?.opacity)===0&&Boolean(this.closest('#viewer-dialog'));
    if(closing){const finished=animation.finished;const delayed=finished.then(value=>value,error=>{if(!state.holdChrome)throw error;state.cancellationSettlementsHeld++;return chromeGate.then(()=>{throw error;});});Object.defineProperty(animation,'finished',{configurable:true,get:()=>delayed});}
    return animation;
   };
   const popstate=event=>{
    const detail=location.pathname.endsWith('/natural-arch/');
    state.events.push({time:performance.now(),path:location.pathname,detail,trusted:event.isTrusted,forwardRequested:state.forwardRequested,backRequested:state.backRequested});
    if(detail&&state.forwardRequested&&!state.backRequested){state.backRequested=true;state.forwardEventTime=performance.now();history.back();}
    else if(!detail&&state.backRequested){state.finalBackSeen=true;state.finalBackEventTime=performance.now();state.holdChrome=false;releaseChrome();}
   };
   window.__qaTriplePopstate=popstate;addEventListener('popstate',popstate,{capture:true});
   window.__vaultFrameProbe=({canvas:actual,host,view})=>{
    const flight=host.classList.contains('live-model-return'),r=host.getBoundingClientRect(),progress=flight?Number(host.dataset.returnProgress):null;
    state.draws.push({time:performance.now(),flight,id:flight?id(host):null,host:host.id||host.className,progress,phase:host.dataset.returnPhase||null,view:{...view},rect:{x:r.x,y:r.y,width:r.width,height:r.height},same_canvas:actual===canvas,same_scene:stage._gltf.scene===scene,same_resource:stage._activeResource===resource,live_scenes:window.__vaultGPU.liveScenes,canvases:document.querySelectorAll('.model-canvas').length});
    if(flight&&!state.forwardRequested&&progress>.1&&progress<1){state.forwardRequested=true;setTimeout(()=>history.forward(),0);}
   };
   const sample=()=>{const flight=document.querySelector('.live-model-return'),image=document.querySelector('#grid [data-id="natural-arch"] .asset-image img'),css=getComputedStyle(image);state.frames.push({time:performance.now(),open:document.querySelector('#viewer-dialog').open,flight:flight?id(flight):null,poster_visible:css.visibility!=='hidden'&&Number(css.opacity)>.99&&!image.closest('[data-detail-origin]')});window.__qaTripleRAF=requestAnimationFrame(sample);};sample();
  });
  await page.locator('#close').click();await page.waitForFunction(()=>window.__qaTriple.finalBackSeen&&!document.querySelector('#viewer-dialog').open&&!document.querySelector('.stage-flight'),null,{timeout:10000});
  await canonicalPoster(page,c,'natural-arch','triple-history resumed close');
  c.triple_history_return=await page.evaluate(()=>{cancelAnimationFrame(window.__qaTripleRAF);delete window.__vaultFrameProbe;removeEventListener('popstate',window.__qaTriplePopstate,{capture:true});Element.prototype.animate=window.__qaTripleOriginalAnimate;return window.__qaTriple;});
  const evidence=c.triple_history_return,flights=evidence.draws.filter(d=>d.flight),flightIds=[...new Set(flights.map(d=>d.id))];
  check(c,'triple history uses real Back Forward Back events in order',evidence.events.length===3&&evidence.events.every(e=>e.trusted)&&!evidence.events[0].detail&&evidence.events[1].detail&&!evidence.events[2].detail,evidence.events);
  check(c,'fixture exercises Back before cancelled-close queued reopen settlement',evidence.cancellationSettlementsHeld>0&&evidence.finalBackSeen,evidence);
  check(c,'queued detail reopen never starts between Forward and resumed close',evidence.draws.filter(d=>d.time>=evidence.forwardEventTime).every(d=>d.flight),evidence.draws);
  check(c,'latest Back resumes a second actual live return flight',flightIds.length===2,flights);
  const original=flights.filter(d=>d.id===flightIds[0]),resumed=flights.filter(d=>d.id===flightIds[1]),lastOriginal=original.at(-1),firstResumed=resumed[0];
  check(c,'first return was interrupted during actual camera movement',lastOriginal.progress>0&&lastOriginal.progress<1,original);
  check(c,'resumed return starts from held intermediate live pose at zero new progress',firstResumed.progress===0&&firstResumed.phase==='moving',firstResumed);sameView(c,lastOriginal.view,firstResumed.view,'triple-history held pose to resumed close');
  check(c,'resumed return keeps the exact saved flight rect',['x','y','width','height'].every(key=>Math.abs(lastOriginal.rect[key]-firstResumed.rect[key])<=1),{before:lastOriginal.rect,resumed:firstResumed.rect});
  check(c,'resumed first frame does not instantly snap to canonical',angle(firstResumed.view.azimuth_deg,canonical.azimuth_deg)>.001||Math.abs(firstResumed.view.elevation_deg-canonical.elevation_deg)>.001||Math.abs(firstResumed.view.distance-canonical.distance)>.00001,{first:firstResumed.view,canonical});
  check(c,'resumed flight visibly interpolates before canonical alignment',resumed.some(d=>d.progress>0&&d.progress<1)&&resumed.some(d=>d.progress===1),resumed);sameView(c,canonical,resumed.at(-1).view,'triple-history final canonical live draw');
  check(c,'triple history retains the same single actual canvas scene and decoded resource',flights.every(d=>d.same_canvas&&d.same_scene&&d.same_resource&&d.live_scenes===1&&d.canvases===1),flights);
  check(c,'resumed close keeps a live visual until the canonical poster is shown',evidence.frames.every(f=>f.flight||f.poster_visible||f.time<evidence.forwardEventTime),evidence.frames);
  const after=await stats(page);check(c,'triple history finishes canonical with no RAF leases fetches parses or renderer leaks',after.liveScenes===0&&after.activeLeases===0&&after.pendingLeases===0&&after.rafPending===0&&after.rendererCreations===before.rendererCreations&&after.networkRequests===before.networkRequests&&after.parseCount===before.parseCount,{before,after});
  await shot(page,'06d-triple-history-resumed-canonical-poster');
 },{recordVideo:false});
 await test('context-loss-during-live-canonical-return',async(page,c)=>{
  await listing(page);const el=await hover(page);await stage(page);await el.focus();await page.keyboard.press('Enter');await detailReady(page,'natural-arch');
  const before=await stats(page),canonical=await canonicalView(page);
  const supported=await page.evaluate(()=>{
   const s=window.__qaStage,canvas=s._renderer.domElement,gl=s._renderer.getContext(),extension=gl.getExtension('WEBGL_lose_context');
   if(!extension)return false;
   s.setView(318,47,s.canonicalView.distance*.8);
   window.__qaReturnLoss={extension,canvas,scene:s._gltf.scene,resource:s._activeResource,draws:[],frames:[],requested:false,lost:null};
   canvas.addEventListener('webglcontextlost',()=>{const flight=document.querySelector('.live-model-return');window.__qaReturnLoss.lost={time:performance.now(),progress:Number(flight?.dataset.returnProgress),phase:flight?.dataset.returnPhase,dialog_open:document.querySelector('#viewer-dialog').open};},{capture:true,once:true});
   window.__vaultFrameProbe=({host,view})=>{
    if(!host.classList.contains('live-model-return'))return;
    const state=window.__qaReturnLoss,p=Number(host.dataset.returnProgress);
    state.draws.push({time:performance.now(),progress:p,phase:host.dataset.returnPhase,view:{...view},toolbar_disabled:document.querySelector('.viewer-controls').inert||[...document.querySelectorAll('.viewer-controls button')].every(button=>button.disabled)});
    // Trigger on the first measured nonzero moving pose. Waiting for a
    // second arbitrary progress band can miss the only such frame on SwiftShader.
    if(!state.requested&&p>0&&p<1){state.requested=true;state.requestedAt={time:performance.now(),progress:p,phase:host.dataset.returnPhase};extension.loseContext();}
   };
   const sample=()=>{const state=window.__qaReturnLoss;if(state.lost){const image=document.querySelector('#grid [data-id="natural-arch"] .asset-image img'),flight=document.querySelector('.live-model-return'),poster=flight?.querySelector('.return-poster')||image,css=getComputedStyle(poster);state.frames.push({time:performance.now(),dialog_open:document.querySelector('#viewer-dialog').open,flight_phase:flight?.dataset.returnPhase||null,flight_opacity:flight?Number(getComputedStyle(flight.querySelector('.model-canvas')).opacity):null,poster_visible:css.visibility!=='hidden'&&Number(css.opacity)>.99&&(flight?true:!image.closest('[data-detail-origin]'))});}window.__qaReturnLossRAF=requestAnimationFrame(sample);};sample();
   return true;
  });
  check(c,'real WebGL context-loss extension available for strict return coverage',supported);
  await close(page);await canonicalPoster(page,c,'natural-arch','mid-return context-loss fallback');
  c.context_loss_return=await page.evaluate(()=>{cancelAnimationFrame(window.__qaReturnLossRAF);delete window.__vaultFrameProbe;const {draws,frames,requested,requestedAt,lost}=window.__qaReturnLoss;return {draws,frames,requested,requestedAt,lost,context_lost:window.__qaStage._contextLost};});
  const evidence=c.context_loss_return;
  check(c,'native context loss interrupts an actual moving return frame',evidence.requested&&evidence.lost?.dialog_open&&evidence.lost.phase==='moving'&&evidence.lost.progress>0&&evidence.lost.progress<1,evidence);
  check(c,'return toolbar input is blocked before and throughout actual return draws',evidence.draws.length>1&&evidence.draws.every(d=>d.toolbar_disabled),evidence.draws);
  check(c,'lost context reveals canonical poster before the next painted frame',evidence.frames.length>0&&evidence.frames.every(f=>f.poster_visible&&(!f.dialog_open||f.flight_phase==='fading'&&f.flight_opacity===0)),evidence.frames);
  const after=await stats(page);check(c,'lost-context close stops all scene leases and RAF without new fetch parse renderer',after.liveScenes===0&&after.activeLeases===0&&after.pendingLeases===0&&after.rafPending===0&&after.rendererCreations===before.rendererCreations&&after.networkRequests===before.networkRequests&&after.parseCount===before.parseCount,{before,after});
  await shot(page,'06c-mid-return-context-loss-canonical-poster');
  await page.waitForTimeout(120);await page.evaluate(()=>window.__qaReturnLoss.extension.restoreContext());await page.waitForFunction(()=>!window.__qaStage._contextLost);
  await el.focus();await page.keyboard.press('Enter');await detailReady(page,'natural-arch');sameView(c,canonical,await view(page),'context-restored reopen starts canonical');
  check(c,'restored context reuses original canvas and decoded GLTF after interrupted close',await page.evaluate(()=>window.__qaStage._renderer.domElement===window.__qaReturnLoss.canvas&&window.__qaStage._gltf.scene===window.__qaReturnLoss.scene&&window.__qaStage._activeResource===window.__qaReturnLoss.resource));
  const restored=await stats(page);check(c,'context restoration creates no extra renderer parse or request',restored.rendererCreations===before.rendererCreations&&restored.networkRequests===before.networkRequests&&restored.parseCount===before.parseCount,{before,restored});await close(page);
 },{recordVideo:false});
 await test('context-loss-during-ready-opening-dissolve',async(page,c)=>{
  await listing(page);const el=await hover(page);await stage(page);
  const before=await stats(page),openingView=await view(page);
  const supported=await page.evaluate(()=>{
   const s=window.__qaStage,canvas=s._renderer.domElement,extension=s._renderer.getContext().getExtension('WEBGL_lose_context');if(!extension)return false;
   const state=window.__qaOpeningLoss={canvas,scene:s._gltf.scene,resource:s._activeResource,frames:[],partial:null,lost:null,extension};
   canvas.addEventListener('webglcontextlost',event=>{const host=document.querySelector('#canvas-host'),bitmap=host.querySelector('.model-handoff');state.lost={time:performance.now(),trusted:event.isTrusted,dialog_open:document.querySelector('#viewer-dialog').open,state:host.dataset.modelState,bitmap_opacity:bitmap?Number(getComputedStyle(bitmap).opacity):null,live_opacity:Number(getComputedStyle(canvas).opacity)};},{once:true,capture:true});
   const visible=node=>{if(!node)return false;for(let n=node;n;n=n.parentElement){const css=getComputedStyle(n);if(css.visibility==='hidden'||css.display==='none'||Number(css.opacity)<.99)return false;}return true;};
   const sample=()=>{
    const host=document.querySelector('#canvas-host'),bitmap=host.querySelector('.model-handoff'),live=host.querySelector('.model-canvas'),poster=host.querySelector('.model-poster');
    if(!state.partial&&host.dataset.modelState==='ready'&&bitmap&&live){
     const b=Number(getComputedStyle(bitmap).opacity),l=Number(getComputedStyle(live).opacity);
     if(b>0&&b<1&&l>0&&l<1){state.partial={time:performance.now(),bitmap_opacity:b,live_opacity:l,isolation:getComputedStyle(host).isolation,bitmap_blend:getComputedStyle(bitmap).mixBlendMode,live_blend:getComputedStyle(live).mixBlendMode,same_canvas:live===canvas,same_scene:s._gltf.scene===state.scene,same_resource:s._activeResource===state.resource,view:{...s.presentationInfo},live_scenes:window.__vaultGPU.liveScenes,canvases:document.querySelectorAll('.model-canvas').length};extension.loseContext();}
    }
    if(state.lost&&!state.closing){const image=document.querySelector('#grid [data-id="natural-arch"] .asset-image img'),open=document.querySelector('#viewer-dialog').open;state.frames.push({time:performance.now(),open,state:host.dataset.modelState,poster_visible:open?Boolean(poster?.complete&&poster.naturalWidth&&visible(poster)):visible(image)&&!image.closest('[data-detail-origin]'),bitmap_count:host.querySelectorAll('.model-handoff').length,poster_animations:poster?.getAnimations().filter(a=>a.playState==='running'||a.playState==='finished').length||0,live_hidden:!live||getComputedStyle(live).visibility==='hidden'});}
    window.__qaOpeningLossRAF=requestAnimationFrame(sample);
   };sample();return true;
  });
  check(c,'native context-loss extension available during ready opening dissolve',supported);
  await el.focus();await page.keyboard.press('Enter');
  await page.waitForFunction(()=>window.__qaOpeningLoss.lost&&document.querySelector('#canvas-host').dataset.modelState==='error',null,{timeout:10000});
  await page.waitForTimeout(200);const idle1=await stats(page);await page.waitForTimeout(200);const idle2=await stats(page);
  check(c,'opening context loss stops rendering without an idle hang',idle2.rafPending===0&&idle2.renderedFrames===idle1.renderedFrames,{idle1,idle2});
  check(c,'opening error cancels original live target opacity animations',await page.evaluate(()=>window.__qaOpeningLoss.canvas.getAnimations().length===0));
  await page.evaluate(()=>{window.__qaOpeningLoss.closing=true;});await close(page);await canonicalPoster(page,c,'natural-arch','ready-opening context-loss return');
  c.opening_context_loss=await page.evaluate(()=>{cancelAnimationFrame(window.__qaOpeningLossRAF);const {frames,partial,lost}=window.__qaOpeningLoss;return {frames,partial,lost};});
  const evidence=c.opening_context_loss,p=evidence.partial;
  check(c,'native loss interrupts an observed ready partial bitmap-to-live dissolve',Boolean(p)&&evidence.lost?.trusted&&evidence.lost.dialog_open&&evidence.lost.state==='ready'&&evidence.lost.bitmap_opacity>0&&evidence.lost.bitmap_opacity<1&&evidence.lost.live_opacity>0&&evidence.lost.live_opacity<1&&p.bitmap_opacity>0&&p.bitmap_opacity<1&&p.live_opacity>0&&p.live_opacity<1,evidence);
  check(c,'interrupted opening borrows sole original canvas scene and decoded resource',p.same_canvas&&p.same_scene&&p.same_resource&&p.live_scenes===1&&p.canvases===1,p);sameView(c,openingView,p.view,'opening loss retains actual camera');
  check(c,'interrupted opening weights are isolated complementary plus-lighter',p.isolation==='isolate'&&p.bitmap_blend==='plus-lighter'&&p.live_blend==='plus-lighter'&&Math.abs(p.bitmap_opacity+p.live_opacity-1)<=.00001,p);
  check(c,'loss exposes decoded fallback before every subsequent painted frame',evidence.frames.length>1&&evidence.frames.every(f=>f.poster_visible&&(!f.open||f.state==='error'&&f.bitmap_count===0&&f.poster_animations===0&&f.live_hidden)),evidence.frames);
  const after=await stats(page);check(c,'opening-loss close leaves canonical poster with no RAF leases fetch parse or renderer leak',after.liveScenes===0&&after.activeLeases===0&&after.pendingLeases===0&&after.rafPending===0&&after.rendererCreations===before.rendererCreations&&after.networkRequests===before.networkRequests&&after.parseCount===before.parseCount,{before,after});
  check(c,'opening-loss close leaves no original target opacity animations',await page.evaluate(()=>window.__qaOpeningLoss.canvas.getAnimations().length===0));
  await shot(page,'06e-opening-dissolve-context-loss-canonical-poster');
  await page.waitForTimeout(120);await page.evaluate(()=>window.__qaOpeningLoss.extension.restoreContext());await page.waitForFunction(()=>!window.__qaStage._contextLost);
  await el.focus();await page.keyboard.press('Enter');await detailReady(page,'natural-arch');
  check(c,'loss reacquisition reuses original canvas scene resource with no retained opacity animation',await page.evaluate(()=>{const s=window.__qaStage,o=window.__qaOpeningLoss;return s._renderer.domElement===o.canvas&&s._gltf.scene===o.scene&&s._activeResource===o.resource&&o.canvas.getAnimations().length===0;}));
  await close(page);await canonicalPoster(page,c,'natural-arch','opening-loss restored reacquisition close');
  const settled=await stats(page);check(c,'loss reacquisition settles without RAF lease or fresh resource work',settled.liveScenes===0&&settled.activeLeases===0&&settled.pendingLeases===0&&settled.rafPending===0&&settled.rendererCreations===before.rendererCreations&&settled.networkRequests===before.networkRequests&&settled.parseCount===before.parseCount,{before,settled});
 },{recordVideo:false});
 await test('same-asset-close-during-ready-opening-dissolve',async(page,c)=>{
  await listing(page);const el=await hover(page);await stage(page);
  await page.evaluate(()=>{const s=window.__qaStage;s.setView(319,48,s.canonicalView.distance*.77);});
  const inspected=await view(page),canonical=await canonicalView(page),before=await stats(page);
  await page.evaluate(()=>{
   const s=window.__qaStage,canvas=s._renderer.domElement,scene=s._gltf.scene,resource=s._activeResource;
   const state=window.__qaOpeningClose={partial:null,draws:[],frames:[]};window.__qaOpeningCloseIdentity={canvas,scene,resource};
   window.__vaultFrameProbe=({canvas:actual,host,view})=>{if(host.classList.contains('live-model-return'))state.draws.push({time:performance.now(),progress:Number(host.dataset.returnProgress),phase:host.dataset.returnPhase,view:{...view},same_canvas:actual===canvas,same_scene:s._gltf.scene===scene,same_resource:s._activeResource===resource,live_scenes:window.__vaultGPU.liveScenes,canvases:document.querySelectorAll('.model-canvas').length});};
   const sample=()=>{
    const host=document.querySelector('#canvas-host'),bitmap=host.querySelector('.model-handoff'),live=host.querySelector('.model-canvas');
    if(!state.partial&&host.dataset.modelState==='ready'&&bitmap&&live){
     const b=Number(getComputedStyle(bitmap).opacity),l=Number(getComputedStyle(live).opacity);
     if(b>0&&b<1&&l>0&&l<1){state.partial={time:performance.now(),bitmap_opacity:b,live_opacity:l,asset_id:bitmap.dataset.assetId,same_canvas:live===canvas,same_scene:s._gltf.scene===scene,same_resource:s._activeResource===resource,isolation:getComputedStyle(host).isolation,bitmap_blend:getComputedStyle(bitmap).mixBlendMode,live_blend:getComputedStyle(live).mixBlendMode,view:{...s.presentationInfo}};document.querySelector('#close').click();}
    }
    if(state.partial){
     const flight=document.querySelector('.live-model-return'),image=document.querySelector('#grid [data-id="natural-arch"] .asset-image img'),open=document.querySelector('#viewer-dialog').open;
     if(flight){const actual=flight.querySelector('.model-canvas'),poster=flight.querySelector('.return-poster'),a=getComputedStyle(actual),p=getComputedStyle(poster),f=getComputedStyle(flight);state.frames.push({time:performance.now(),open,flight:true,phase:flight.dataset.returnPhase,progress:Number(flight.dataset.returnProgress),live_opacity:Number(a.opacity),poster_opacity:Number(p.opacity),poster_visible:p.visibility!=='hidden',live_visible:a.visibility!=='hidden',host_opacity:Number(f.opacity),isolation:f.isolation,live_blend:a.mixBlendMode,poster_blend:p.mixBlendMode,poster_decoded:poster instanceof HTMLCanvasElement&&poster.width>0&&poster.height>0,origin_hidden:Boolean(image.closest('[data-detail-origin]'))});}
     else{const css=getComputedStyle(image);state.frames.push({time:performance.now(),open,flight:false,poster_visible:image.complete&&image.naturalWidth>0&&css.visibility!=='hidden'&&Number(css.opacity)>.99&&!image.closest('[data-detail-origin]')});}
    }
    window.__qaOpeningCloseRAF=requestAnimationFrame(sample);
   };sample();
  });
  await el.focus();await page.keyboard.press('Enter');
  await page.waitForFunction(()=>window.__qaOpeningClose.partial&&!document.querySelector('#viewer-dialog').open&&!document.querySelector('.stage-flight'),null,{timeout:10000});
  await canonicalPoster(page,c,'natural-arch','same-asset partial-opening close');
  c.opening_close=await page.evaluate(()=>{cancelAnimationFrame(window.__qaOpeningCloseRAF);delete window.__vaultFrameProbe;return window.__qaOpeningClose;});
  const evidence=c.opening_close,p=evidence.partial,draws=evidence.draws,flights=evidence.frames.filter(f=>f.flight);
  check(c,'same-asset close starts inside an observed partial ready opening dissolve',p?.asset_id==='natural-arch'&&p.bitmap_opacity>0&&p.bitmap_opacity<1&&p.live_opacity>0&&p.live_opacity<1,p);
  check(c,'partial opening preserves original canvas scene resource and complementary blend',p.same_canvas&&p.same_scene&&p.same_resource&&p.isolation==='isolate'&&p.bitmap_blend==='plus-lighter'&&p.live_blend==='plus-lighter'&&Math.abs(p.bitmap_opacity+p.live_opacity-1)<=.00001,p);sameView(c,inspected,p.view,'partial opening retains inspected camera');
  check(c,'close during opening uses actual moving canonical-return draws',draws.length>=3&&draws.some(d=>d.progress>0&&d.progress<1)&&draws.some(d=>d.progress===1),draws);
  sameView(c,inspected,draws[0].view,'partial-opening close begins at actual inspected camera');sameView(c,canonical,draws.at(-1).view,'partial-opening close reaches final canonical camera');
  check(c,'opening interruption keeps sole original live canvas scene and resource',draws.every(d=>d.same_canvas&&d.same_scene&&d.same_resource&&d.live_scenes===1&&d.canvases===1),draws);
  check(c,'return has decoded transient poster and isolated complementary child weights',flights.length>1&&flights.every(f=>f.poster_decoded&&f.isolation==='isolate'&&f.live_blend==='plus-lighter'&&f.poster_blend==='plus-lighter'&&f.host_opacity===1&&Math.abs(f.live_opacity+f.poster_opacity-1)<=.00001),flights);
  check(c,'return keeps origin hidden until final swap and poster until canonical alignment',flights.every(f=>f.origin_hidden&&(f.phase==='fading'?f.progress===1&&f.poster_visible:!f.poster_visible))&&flights.some(f=>f.phase==='fading'&&f.live_opacity>0&&f.live_opacity<1&&f.poster_opacity>0&&f.poster_opacity<1),flights);
  check(c,'partial-opening close leaves no blank painted frame',evidence.frames.length>1&&evidence.frames.every(f=>f.flight?(f.live_visible&&f.live_opacity>0||f.poster_visible&&f.poster_opacity>0):!f.open&&f.poster_visible),evidence.frames);
  const after=await stats(page);check(c,'partial-opening close ends canonical without RAF lease network parse or renderer leaks',after.liveScenes===0&&after.activeLeases===0&&after.pendingLeases===0&&after.rafPending===0&&after.rendererCreations===before.rendererCreations&&after.networkRequests===before.networkRequests&&after.parseCount===before.parseCount,{before,after});
  check(c,'partial-opening close cancels original target opacity animations',await page.evaluate(()=>window.__qaOpeningCloseIdentity.canvas.getAnimations().length===0));
  await shot(page,'06f-same-asset-opening-close-canonical-poster');
  await el.focus();await page.keyboard.press('Enter');await detailReady(page,'natural-arch');sameView(c,canonical,await view(page),'partial-opening close reacquires canonical camera');
  check(c,'close reacquisition reuses original canvas scene resource with no retained opacity animation',await page.evaluate(()=>{const s=window.__qaStage,o=window.__qaOpeningCloseIdentity;return s._renderer.domElement===o.canvas&&s._gltf.scene===o.scene&&s._activeResource===o.resource&&o.canvas.getAnimations().length===0;}));
  await close(page);await canonicalPoster(page,c,'natural-arch','partial-opening restored reacquisition close');
  const settled=await stats(page);check(c,'close reacquisition settles without RAF lease or fresh resource work',settled.liveScenes===0&&settled.activeLeases===0&&settled.pendingLeases===0&&settled.rafPending===0&&settled.rendererCreations===before.rendererCreations&&settled.networkRequests===before.networkRequests&&settled.parseCount===before.parseCount,{before,settled});
 },{recordVideo:false});
 await test('rapid-hover-abort-latest-wins',async(page,c)=>{
  await page.route('**/*.glb',async route=>{await new Promise(r=>setTimeout(r,220));await route.continue().catch(()=>{});});await listing(page);
  const ids=['natural-arch','conifer-tree','cycad','dinosaur-nest'];
  for(const id of ids){const el=card(page,id);await el.scrollIntoViewIfNeeded();const r=await el.locator('.asset-image').boundingBox();await page.mouse.move(r.x+r.width*.5,r.y+r.height*.5);await page.waitForTimeout(195);}
  await page.waitForFunction(id=>window.__vaultPreview?.activeId===id&&document.querySelector('[data-id="'+id+'"]')?.dataset.previewState==='ready',ids.at(-1),{timeout:30000});await stage(page);await page.waitForTimeout(400);const s=await stats(page);c.stats=s;
  check(c,'latest hover remains attached',await page.evaluate(id=>window.__qaStage._host?.closest('[data-id]')?.dataset.id===id,ids.at(-1)));check(c,'serialized GLB requests and parses',s.peakRequests<=1&&s.peakParses<=1,s);check(c,'no old canvas attaches later',await page.locator('.model-canvas').count()===1&&s.liveScenes===1);await shot(page,'07-rapid-hover-latest-wins');
 });
 await test('interrupted-open-close-and-latest-detail',async(page,c)=>{
  await page.route('**/*.glb',async route=>{await new Promise(r=>setTimeout(r,300));await route.continue().catch(()=>{});});await listing(page);
  await card(page,'natural-arch').focus();await page.keyboard.press('Enter');await page.waitForFunction(()=>document.querySelector('#viewer-dialog').open&&window.__vaultGPU?.activeRequests===1);await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);await page.waitForTimeout(500);
  check(c,'closed loading detail never reattaches late canvas',await page.locator('.model-canvas').count()===0&&await page.locator('#viewer-dialog').evaluate(d=>!d.open)&&await page.evaluate(()=>document.body.style.overflow===''));const afterCancel=await stats(page);check(c,'cancelled load releases requests and scene',afterCancel.activeRequests===0&&afterCancel.liveScenes===0&&afterCancel.activeLeases===0&&afterCancel.pendingLeases===0&&afterCancel.rafPending===0,afterCancel);
  await card(page,'natural-arch').focus();await page.keyboard.press('Enter');await page.waitForFunction(()=>document.querySelector('#viewer-dialog').open&&document.querySelector('#next-model')?.dataset.modelId);const nextId=await page.locator('#next-model').getAttribute('data-model-id');await page.waitForFunction(()=>window.__vaultGPU?.activeRequests===1);await page.locator('#next-model').focus();await page.keyboard.press('Enter');await detailReady(page,nextId);await stage(page);await page.waitForTimeout(350);
  check(c,'newer detail stays authoritative after old fetch completion',await page.evaluate(id=>document.querySelector('#canvas-host').dataset.presentedUrl.endsWith('/'+id+'.glb')&&location.pathname.endsWith('/'+id+'/'),nextId));check(c,'detail switching shares sole renderer and active scene',(await stats(page)).rendererCreations===1&&(await stats(page)).liveScenes===1&&await page.locator('.model-canvas').count()===1);
  await page.goBack();await page.goForward();await detailReady(page,nextId);check(c,'interrupted Back/Forward preserves modal presentation',await page.locator('#viewer-dialog').evaluate(d=>d.open)&&await page.evaluate(()=>document.body.style.overflow==='hidden'));await shot(page,'07b-interrupted-history-modal');await close(page);
 });
 await test('offscreen-preview-stops-rendering',async(page,c)=>{
  await listing(page);const el=card(page,'conifer-tree');await el.scrollIntoViewIfNeeded();await el.focus();await page.keyboard.press('ArrowRight');await page.waitForFunction(()=>document.querySelector('[data-id="conifer-tree"]')?.dataset.previewState==='ready');await stage(page);await page.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));await page.waitForFunction(()=>window.__vaultPreview.activeId===null);await page.waitForTimeout(100);const a=await stats(page);await page.waitForTimeout(300);const b=await stats(page);check(c,'offscreen card releases sole scene and pending RAF',b.liveScenes===0&&b.activeLeases===0&&b.rafPending===0&&a.renderedFrames===b.renderedFrames,{a,b});check(c,'offscreen cleanup keeps renderer reusable',b.rendererCount===1&&b.rendererCreations===1);await hover(page,'conifer-tree');check(c,'visible card resumes cached exact model without extra parse',(await stats(page)).parseCount===1&&(await stats(page)).networkRequests===1);await shot(page,'07c-offscreen-reacquired');
 },{viewport:{width:800,height:560},recordVideo:{dir:output,size:{width:800,height:560}}});
 await test('native-stale-texture-decode-disposal',async(page,c)=>{
  await page.addInitScript(()=>{const original=window.createImageBitmap;window.__qaDecode={started:0,finished:0};window.createImageBitmap=async(...args)=>{window.__qaDecode.started++;const bitmap=await original.apply(window,args);await new Promise(r=>setTimeout(r,400));window.__qaDecode.finished++;return bitmap;};});
  await listing(page);await stage(page);
  await page.evaluate(url=>{const host=document.querySelector('[data-id="natural-arch"] .asset-image');window.__qaOld=window.__qaStage.show(host,url,{mode:'hover'});},base+prefix+'__qa__/textured-stale.glb');
  await page.waitForFunction(()=>window.__qaDecode.started>0&&window.__vaultGPU.activeParses===1);
  await page.evaluate(url=>{window.__qaStage.hide();window.__qaNew=window.__qaStage.show(document.querySelector('[data-id="conifer-tree"] .asset-image'),url,{mode:'hover'});},base+prefix+assets.find(a=>a.id==='conifer-tree').glb);
  c.results=await page.evaluate(async()=>({old:await window.__qaOld,new:await window.__qaNew,decode:{...window.__qaDecode}}));const s=await stats(page);c.stats=s;
  check(c,'actual native textured decode completed stale',c.results.decode.finished>0&&c.results.old===false&&c.results.new===true,c.results);check(c,'stale parse disposed before next parse',s.staleScenes===1&&s.disposedScenes>=1&&s.peakParses===1&&s.activeParses===0&&s.activeRequests===0,s);check(c,'new model owns sole active lease',s.activeLeases===1&&s.pendingLeases===0&&s.liveScenes===1&&await page.locator('.model-canvas').count()===1,s);await shot(page,'08-stale-decode-disposed');
 });
 await test('ten-models-bounded-LRU-and-idle',async(page,c)=>{
  await listing(page);c.samples=[];
  for(const asset of assets){await hover(page,asset.id);await stage(page);const s=await stats(page);c.samples.push({id:asset.id,...s});check(c,asset.id+' bounded encoded decoded resources',s.cacheEntries<=3&&s.cacheBytes<=24*1024*1024&&s.cachedScenes<=3&&s.cachedDecodedBytes<=48*1024*1024&&s.decodedEntries<=4&&s.uncachedActiveScenes<=1&&s.activeLeases===1&&s.liveScenes===1,s);await page.mouse.move(1,1);await page.waitForTimeout(50);}
  const a=await stats(page);await page.waitForTimeout(350);const b=await stats(page);check(c,'ten assets evict and dispose actual resources',b.evictedScenes>=7&&b.disposedScenes>=7&&b.disposedGeometries>0&&b.disposedMaterials>0,b);check(c,'one renderer after ten assets',b.rendererCreations===1&&b.rendererCount===1,b);check(c,'inactive frames stay stopped with bounded caches',a.renderedFrames===b.renderedFrames&&b.rafPending===0&&b.activeLeases===0&&b.pendingLeases===0&&b.liveScenes===0,b);check(c,'zero turntable frame/manifest requests',turntableRequests(c.name).length===0);await shot(page,'09-ten-assets-idle');
 });
 await test('keyboard-reduced-motion',async(page,c)=>{
  await listing(page);const el=card(page,'natural-arch');await el.scrollIntoViewIfNeeded();await el.focus();await page.keyboard.press('ArrowRight');await page.waitForFunction(()=>document.querySelector('[data-id="natural-arch"]')?.dataset.previewState==='ready');await stage(page);await page.waitForTimeout(80);const a=await view(page);await page.keyboard.press('ArrowRight');await page.waitForTimeout(60);const b=await view(page);check(c,'focused card keyboard intentionally activates and orbits',angle(a.azimuth_deg,b.azimuth_deg)>1,{a,b});
  const s1=await stats(page);await page.waitForTimeout(220);const s2=await stats(page);check(c,'reduced motion no autoplay/continuous RAF',s1.renderedFrames===s2.renderedFrames&&s2.rafPending===0,{s1,s2});await page.keyboard.press('Enter');await detailReady(page,'natural-arch');check(c,'keyboard Enter opens accessible dialog',await page.locator('#viewer-dialog').evaluate(d=>d.open)&&await page.locator('#close').evaluate(d=>document.activeElement===d));const inspected=await view(page);await page.emulateMedia({reducedMotion:'no-preference'});await page.waitForTimeout(60);sameView(c,inspected,await view(page),'motion preference change preserves inspected view');await page.emulateMedia({reducedMotion:'reduce'});await page.waitForTimeout(60);sameView(c,inspected,await view(page),'motion reduction preserves inspected view');await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);await canonicalPoster(page,c,'natural-arch','reduced-motion return');check(c,'Escape restores focus to card',await el.evaluate(d=>document.activeElement===d));await shot(page,'10-reduced-motion-keyboard');
 },{reducedMotion:'reduce'});
 await test('trusted-touch-swipe-and-tap',async(page,c,context)=>{
  await listing(page);await page.waitForTimeout(200);check(c,'touch initial poster no GLBs',glbRequests(c.name).length===0);
  const el=card(page,'natural-arch');await el.scrollIntoViewIfNeeded();
  const session=await context.newCDPSession(page);c.touch_swipes=[];
  await page.evaluate(()=>{
   window.__qaTouchEvents=[];
   for(const type of ['pointerdown','pointermove'])document.addEventListener(type,event=>{
    if(event.pointerType==='touch')window.__qaTouchEvents.push({type,x:event.clientX,y:event.clientY,pointerId:event.pointerId,trusted:event.isTrusted,imageWidth:event.target.closest('.asset-card')?.querySelector('.asset-image').getBoundingClientRect().width});
   },true);
  });
  const swipeCard=async({id,fraction,before,label})=>{
   const r=await el.locator('.asset-image').boundingBox(),x=r.x+r.width*.3,y=r.y+r.height*.5;
   await page.evaluate(()=>{window.__qaTouchEvents=[];});
   await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y,id}]});
   for(let i=1;i<=5;i++){
    await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:x+r.width*fraction*i/5,y,id}]});
    await page.waitForTimeout(25);
   }
   await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
   await page.waitForFunction(()=>document.querySelector('[data-id="natural-arch"]')?.dataset.previewState==='ready');
   await stage(page);await page.waitForTimeout(80);
   const after=await view(page),events=await page.evaluate(()=>window.__qaTouchEvents);
   const start=events.find(e=>e.type==='pointerdown'),end=events.filter(e=>e.type==='pointermove').at(-1);
   // Gallery entrance motion can still be scaling the card during the gesture.
   // Use the width observed with the actual last native move, as the handler does.
   const expectedAzimuth=(before?.azimuth_deg??42)+(end.x-start.x)/end.imageWidth*360;
   c.touch_swipes.push({label,before,after,expectedAzimuth,image_width:r.width,final_move_image_width:end.imageWidth,events});
   check(c,label+' uses trusted native touch',Boolean(start&&end)&&events.every(e=>e.trusted),events);
   check(c,label+' rotates from its actual starting azimuth',angle(after.azimuth_deg,expectedAzimuth)<.01,{before,after,expectedAzimuth});
   if(before){
    check(c,label+' preserves inspected elevation',Math.abs(after.elevation_deg-before.elevation_deg)<.001,{before,after});
    check(c,label+' preserves inspected zoom',Math.abs(after.distance-before.distance)<.00001,{before,after});
   }
   check(c,label+' does not accidentally open modal',await page.locator('#viewer-dialog').evaluate(d=>!d.open));
   return after;
  };
  const first=await swipeCard({id:1,fraction:.35,label:'first card swipe'});
  check(c,'horizontal trusted touch activates actual GLB',await page.locator('.model-canvas').count()===1);alpha(c,await pixels(page),'touch swipe');await shot(page,'11-touch-swipe');
  const second=await swipeCard({id:2,fraction:.22,before:first,label:'second card swipe'});
  check(c,'second drag continues beyond the first rotated pose',angle(first.azimuth_deg,second.azimuth_deg)>20,{first,second});await shot(page,'11b-second-touch-swipe-continuity');
  await el.tap();await detailReady(page,'natural-arch');check(c,'subsequent touch tap opens detail',await page.locator('#viewer-dialog').evaluate(d=>d.open));sameView(c,second,await view(page),'touch card to detail');
  const canvas=page.locator('#canvas-host .model-canvas');await canvas.scrollIntoViewIfNeeded();const r=await canvas.boundingBox(),x=r.x+r.width*.35,y=r.y+r.height*.5;
  const beforeOrbit=await view(page);
  await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y,id:3}]});
  for(let i=1;i<=5;i++){await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:x+r.width*.04*i,y:y-r.height*.01*i,id:3}]});await page.waitForTimeout(25);}
  await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await page.waitForTimeout(80);
  const orbited=await view(page);check(c,'trusted touch orbits detail away from card angle',angle(beforeOrbit.azimuth_deg,orbited.azimuth_deg)>5,{beforeOrbit,orbited});
  await page.locator('#zoom-in').tap();await page.waitForTimeout(80);const inspected=await view(page);c.inspected_touch_detail=inspected;
  check(c,'detail touch zoom changes actual camera distance',Math.abs(orbited.distance-inspected.distance)>.01,{orbited,inspected});await shot(page,'11c-inspected-touch-detail');
  const canonical=await canonicalView(page);await page.locator('#close').tap();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open&&!document.querySelector('.stage-flight'));await canonicalPoster(page,c,'natural-arch','completed touch detail return');
  const resumed=await swipeCard({id:4,fraction:.18,before:canonical,label:'canonical poster touch resume'});
  check(c,'touch resume keeps single renderer and original decoded GLTF',(await stats(page)).rendererCreations===1&&(await stats(page)).parseCount===1&&(await stats(page)).networkRequests===1,await stats(page));await shot(page,'11d-returned-detail-touch-resume');
  const r2=await el.locator('.asset-image').boundingBox();const before=await page.evaluate(()=>({gpu:{...window.__vaultGPU},activations:window.__vaultPreview.activations}));await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:r2.x+r2.width*.5,y:r2.y+r2.height*.5,id:5}]});await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:r2.x+r2.width*.5+1,y:r2.y+r2.height*.5-70,id:5}]});await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await page.waitForTimeout(200);const after=await page.evaluate(()=>({gpu:{...window.__vaultGPU},activations:window.__vaultPreview.activations,open:document.querySelector('#viewer-dialog').open}));check(c,'vertical touch scroll does not activate preview or detail',after.activations===before.activations&&after.gpu.parseCount===before.gpu.parseCount&&after.gpu.networkRequests===before.gpu.networkRequests&&!after.open,{before,after,resumed});await shot(page,'12-touch-return');
 },{viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1,recordVideo:{dir:output,size:{width:390,height:844}}});
 for(const failure of ['network','corrupt'])await test(failure+'-fallback-and-recovery',async(page,c)=>{
  const target=assets.find(a=>a.id==='natural-arch');await page.route('**/'+target.glb,route=>failure==='network'?route.fulfill({status:503,body:'Unavailable'}):route.fulfill({status:200,contentType:'model/gltf-binary',body:Buffer.from('this is not a GLB')}));await listing(page);const el=card(page,'natural-arch');await el.scrollIntoViewIfNeeded();await el.hover();await page.waitForFunction(()=>document.querySelector('[data-id="natural-arch"]')?.dataset.previewState==='fallback');check(c,'failed hover retains static poster',await el.locator('img').evaluate(img=>img.complete&&img.naturalWidth>0&&getComputedStyle(img).visibility!=='hidden'));check(c,'failed hover no running scene or RAF',(await stats(page)).liveScenes===0&&(await stats(page)).rafPending===0);await shot(page,'13-'+failure+'-hover-fallback');
  await el.click();await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='error');check(c,'failed detail keeps readable poster and status',await page.locator('#canvas-host img').evaluate(img=>img.complete&&img.naturalWidth>0&&getComputedStyle(img).visibility==='visible')&&Boolean(await page.locator('#viewer-status').textContent()));await shot(page,'14-'+failure+'-detail-fallback');
  await page.unroute('**/'+target.glb);await close(page);const retryBefore=await stats(page);
  await hover(page,'natural-arch');await stage(page);const retryAfter=await stats(page);c.same_url_recovery={before:retryBefore,after:retryAfter};
  check(c,'same failed URL explicitly retries fresh HTTP and parse',retryAfter.networkRequests===retryBefore.networkRequests+1&&retryAfter.parseCount===retryBefore.parseCount+1,{retryBefore,retryAfter});
  check(c,'same natural-arch URL recovers actual ready WebGL',await page.locator('.model-canvas').count()===1&&retryAfter.liveScenes===1&&await page.locator('[data-id="natural-arch"] .asset-image').evaluate(host=>host.dataset.modelState==='ready'&&host.dataset.presentedUrl.endsWith('/natural-arch.glb')));alpha(c,await pixels(page),'same-URL recovery');await shot(page,'14b-'+failure+'-same-url-recovered');
  await hover(page,'conifer-tree');check(c,'next healthy model also recovers',await page.locator('.model-canvas').count()===1&&(await stats(page)).liveScenes===1);
 });
 await test('actual-WebGL-context-loss-restore',async(page,c)=>{
  await listing(page);await hover(page);await stage(page);const original=await stats(page);await page.evaluate(()=>{const g=window.__qaStage._renderer.getContext();window.__qaLose=g.getExtension('WEBGL_lose_context');if(!window.__qaLose)throw new Error('WEBGL_lose_context unavailable');window.__qaLose.loseContext();});await page.waitForFunction(()=>document.querySelector('[data-id="natural-arch"]')?.dataset.previewState==='fallback');const lost=await stats(page);check(c,'actual lost context stops frames and keeps poster',lost.rafPending===0&&await card(page,'natural-arch').locator('img').evaluate(i=>i.complete&&i.naturalWidth>0),lost);await shot(page,'15-context-loss-fallback');
  await page.waitForTimeout(150);await page.evaluate(()=>window.__qaLose.restoreContext());await page.waitForFunction(()=>document.querySelector('[data-id="natural-arch"]')?.dataset.previewState==='ready',null,{timeout:30000});const restored=await stats(page);alpha(c,await pixels(page),'restored context');check(c,'restore reuses renderer GLTF no network/reparse',restored.rendererCreations===original.rendererCreations&&restored.parseCount===original.parseCount&&restored.networkRequests===original.networkRequests,{original,restored});await shot(page,'16-context-restored-real-WebGL');
 });
 report.status=report.cases.every(c=>c.status==='passed')&&report.page_errors.length===0?'passed':'failed';
} catch(error){report.status='failed';report.error=error.stack;console.error(error);}
finally{report.finished=new Date().toISOString();report.requests=requestLog;await save();await browser?.close();await new Promise(r=>server.close(r));}
console.log(JSON.stringify({status:report.status,cases:report.cases.map(c=>({name:c.name,status:c.status,error:c.error})),page_errors:report.page_errors,screenshots:report.screenshots.length,videos:report.videos.length},null,2));
if(report.status!=='passed')process.exitCode=1;

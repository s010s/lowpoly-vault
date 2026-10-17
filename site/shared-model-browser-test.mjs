/** Independent actual Chromium/WebGL regression for one shared real-model stage. */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, readdir, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import assert from 'node:assert/strict';

const root=resolve(process.env.GALLERY_DIR||'dist');
const output=resolve(process.env.QA_OUTPUT_DIR||'qa/shared-model-preview/browser');
const prefix='/lowpoly-vault/';
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
 const c={name,checks:[],status:'running'};report.cases.push(c);
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'no-preference',recordVideo:{dir:output,size:{width:1440,height:1000}},...options});
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
async function close(page,{moveAway=false}={}){await page.locator('#close').click();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);if(moveAway)await page.mouse.move(1,1);await page.waitForTimeout(80);}
async function stage(page){await page.evaluate(async path=>{const {ModelStage}=await import(path);window.__qaStage=new ModelStage();},base+prefix+'assets/'+viewerFile);}
async function stats(page){return page.evaluate(()=>({...window.__vaultGPU}));}
async function view(page){return page.evaluate(()=>window.__qaStage.presentationInfo);}
function angle(a,b){return Math.abs(((a-b+540)%360)-180);}
function sameView(c,a,b,label){check(c,label+' azimuth',angle(a.azimuth_deg,b.azimuth_deg)<.001,{a,b});check(c,label+' elevation',Math.abs(a.elevation_deg-b.elevation_deg)<.001);check(c,label+' distance',Math.abs(a.distance-b.distance)<.00001);}
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
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 report.timing_method='Cold/warm wall time includes the intentional 180ms hover dwell; firstPreviewMilliseconds and lastShowMilliseconds are app load/render timings. ResourceTiming and server byte counts are actual loopback HTTP transfers.';
 report.browser={version:browser.version(),executable:process.env.CHROMIUM_PATH||chromium.executablePath(),args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']};
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
  await close(page);check(c,'detail returns exact 2D snapshot',await card(page,'natural-arch').locator('.model-preview-snapshot').count()===1);const snapshot=await pixels(page,'[data-id="natural-arch"] .model-preview-snapshot');alpha(c,snapshot,'returned snapshot');await shot(page,'06-returned-card-snapshot');
  await card(page,'natural-arch').focus();await page.keyboard.press('Enter');await detailReady(page,'natural-arch');sameView(c,inspected,await view(page),'snapshot to reopened detail');await close(page);
  await page.goForward();await detailReady(page,'natural-arch');check(c,'browser Forward restores modal route',await page.locator('#viewer-dialog').evaluate(d=>d.open)&&/\/models\/natural-arch\/$/.test(new URL(page.url()).pathname));
  await page.goBack();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);check(c,'Back restores listing and scroll unlocked',await page.evaluate(()=>document.body.style.overflow===''&&!document.querySelector('#catalog-page').hidden));
  for(let i=0;i<3;i++){await card(page,'natural-arch').click();await detailReady(page,'natural-arch');await close(page);}
  const end=await stats(page);check(c,'repeated reopen retains single renderer and one original parse',end.rendererCreations===1&&end.parseCount===1&&end.networkRequests===1,end);
 });
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
  const s1=await stats(page);await page.waitForTimeout(220);const s2=await stats(page);check(c,'reduced motion no autoplay/continuous RAF',s1.renderedFrames===s2.renderedFrames&&s2.rafPending===0,{s1,s2});await page.keyboard.press('Enter');await detailReady(page,'natural-arch');check(c,'keyboard Enter opens accessible dialog',await page.locator('#viewer-dialog').evaluate(d=>d.open)&&await page.locator('#close').evaluate(d=>document.activeElement===d));const inspected=await view(page);await page.emulateMedia({reducedMotion:'no-preference'});await page.waitForTimeout(60);sameView(c,inspected,await view(page),'motion preference change preserves inspected view');await page.emulateMedia({reducedMotion:'reduce'});await page.waitForTimeout(60);sameView(c,inspected,await view(page),'motion reduction preserves inspected view');await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);check(c,'Escape restores focus to card',await el.evaluate(d=>document.activeElement===d));await shot(page,'10-reduced-motion-keyboard');
 },{reducedMotion:'reduce'});
 await test('trusted-touch-swipe-and-tap',async(page,c,context)=>{
  await listing(page);await page.waitForTimeout(200);check(c,'touch initial poster no GLBs',glbRequests(c.name).length===0);
  const el=card(page,'natural-arch');await el.scrollIntoViewIfNeeded();
  const session=await context.newCDPSession(page);c.touch_swipes=[];
  await page.evaluate(()=>{
   window.__qaTouchEvents=[];
   for(const type of ['pointerdown','pointermove'])document.addEventListener(type,event=>{
    if(event.pointerType==='touch')window.__qaTouchEvents.push({type,x:event.clientX,y:event.clientY,pointerId:event.pointerId,trusted:event.isTrusted});
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
   const expectedAzimuth=(before?.azimuth_deg??42)+(end.x-start.x)/r.width*360;
   c.touch_swipes.push({label,before,after,expectedAzimuth,image_width:r.width,events});
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
  await page.locator('#close').tap();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);await page.waitForTimeout(80);
  const snapshotView=await el.locator('.model-preview-snapshot').evaluate(canvas=>canvas.__presentation);sameView(c,inspected,snapshotView,'touch detail to card snapshot');
  const resumed=await swipeCard({id:4,fraction:.18,before:inspected,label:'returned detail touch resume'});
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

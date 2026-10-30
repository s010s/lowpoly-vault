/** Synthetic cold-load measurements of the built website. No external requests,
 * asset changes, publishing, or claims about real CDN/device performance. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,stat,realpath} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {createServer} from 'node:http';
import {createHash} from 'node:crypto';
import {chromium} from 'playwright';
import {EXPECTED} from './capture-five.mjs';

assert.equal(process.argv.length,4,'Usage: node measure-five.mjs REPOSITORY NEW_OUTPUT_DIRECTORY');
const repo=await realpath(resolve(process.argv[2])),out=resolve(process.argv[3]),root=resolve(repo,'dist');
assert(out!==repo&&!out.startsWith(repo+sep),'Output must be outside the checkout');
await mkdir(out,{recursive:false});
const hash=b=>createHash('sha256').update(b).digest('hex');
const manifest=JSON.parse(await readFile(resolve(root,'assets/manifest.json'))),models=Object.keys(EXPECTED).map(id=>manifest.assets.find(a=>a.id===id));
assert.equal(manifest.assets.length,752);
for(const a of models){assert(a);assert.equal(a.sha256.glb,EXPECTED[a.id]);assert.equal(hash(await readFile(resolve(root,a.glb))),EXPECTED[a.id]);}
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.svg':'image/svg+xml','.ico':'image/x-icon'};
const prefix='/lowpoly-vault/';
const report={status:'RUNNING',source_manifest_sha256:hash(await readFile(resolve(repo,'assets/manifest.json'))),scope:'Synthetic Cloud loopback, Chromium CDP bandwidth/latency emulation, uncompressed HTTP. Fresh context per model/profile, HTTP cache disabled, service workers blocked. Not real-world CDN timing or physical-device performance.',profiles:[{name:'5Mbps-80ms',download_mbps:5,latency_ms:80},{name:'20Mbps-40ms',download_mbps:20,latency_ms:40}],runs:[],errors:[]};
const server=createServer(async(req,res)=>{try{
 assert.equal(req.method,'GET');const u=new URL(req.url,'http://localhost');assert(u.pathname.startsWith(prefix));
 let file=resolve(root,decodeURIComponent(u.pathname.slice(prefix.length))||'index.html');assert(file.startsWith(root+sep));
 if((await stat(file)).isDirectory())file=resolve(file,'index.html');assert.equal(await realpath(file),file);
 const b=await readFile(file);res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream','Content-Length':b.length,'Cache-Control':'no-store'}).end(b);
 }catch{res.writeHead(404).end();}});
let browser;
try{
 await new Promise((ok,no)=>{server.once('error',no);server.listen(0,'127.0.0.1',ok);});const origin=`http://127.0.0.1:${server.address().port}`;
 browser=await chromium.launch({headless:true,executablePath:process.env.CAPTURE_CHROMIUM_EXECUTABLE||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});report.browser=browser.version();
 for(const profile of report.profiles)for(const asset of models){
  const context=await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1,reducedMotion:'reduce',serviceWorkers:'block'});
  const page=await context.newPage(),cdp=await context.newCDPSession(page),requests=new Map(),errors=[];
  const row={id:asset.id,profile:profile.name,status:'RUNNING',model_sha256:EXPECTED[asset.id],model_body_bytes:asset.file_sizes.glb,external_texture_bytes:0,optional_blend_download_bytes:asset.file_sizes.blend,blend_requested:false};report.runs.push(row);
  try{
   await page.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
   page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>errors.push(new URL(r.url()).pathname+': '+r.failure()?.errorText));
   await cdp.send('Network.enable');await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});await cdp.send('Network.setBypassServiceWorker',{bypass:true});
   await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:profile.latency_ms,downloadThroughput:profile.download_mbps*1_000_000/8,uploadThroughput:profile.download_mbps*1_000_000/8,connectionType:'cellular4g'});
   cdp.on('Network.requestWillBeSent',e=>{const u=new URL(e.request.url);if(u.origin===origin)requests.set(e.requestId,{path:u.pathname.slice(prefix.length),started:e.timestamp,type:e.type});});
   cdp.on('Network.responseReceived',e=>{const r=requests.get(e.requestId);if(r)Object.assign(r,{status:e.response.status,from_disk_cache:!!e.response.fromDiskCache,from_service_worker:!!e.response.fromServiceWorker,response_at:e.timestamp});});
   cdp.on('Network.loadingFinished',e=>{const r=requests.get(e.requestId);if(r)Object.assign(r,{finished:e.timestamp,encoded_transfer_bytes:e.encodedDataLength});});
   const started=performance.now();await page.goto(origin+prefix+'models/?model='+asset.id,{waitUntil:'domcontentloaded',timeout:120000});
   await page.waitForFunction(id=>window.__gallery?.state.selected===id&&document.querySelector('#detail')?.dataset.state==='ready',asset.id,{timeout:120000});row.navigation_to_ready_ms=performance.now()-started;
   const state=await page.evaluate(id=>{const g=window.__gallery,r=g.renderer,a=g.models.find(x=>x.id===id),gl=r.renderer.getContext();return {selected:g.state.selected,model_path:a.glb,poster_source:a.galleryPosters.source_glb_sha256,model_sha256:a.sha256.glb,loaded_bytes:r.detail.entry.bytes,renderers:document.querySelectorAll('canvas.preview-renderer').length,webgl_error:gl.getError(),context_lost:gl.isContextLost()};},asset.id);
   assert.equal(state.selected,asset.id);assert.equal(state.model_path,asset.glb);assert.equal(state.model_sha256,EXPECTED[asset.id]);assert.equal(state.loaded_bytes,row.model_body_bytes);assert.equal(state.renderers,1);assert.equal(state.webgl_error,0);assert.equal(state.context_lost,false);row.identity=state;
   if(profile.download_mbps===20){
    const p=`website-${asset.id}.png`;await page.screenshot({path:resolve(out,p),fullPage:false});const b=await readFile(resolve(out,p));row.screenshot={path:p,sha256:hash(b),bytes:b.length};
    const host=page.locator('#detail'),before=await page.evaluate(()=>window.__gallery.renderer.viewState());
    const box=await host.boundingBox();await page.mouse.move(box.x+box.width*.5,box.y+box.height*.5);await page.mouse.down();await page.mouse.move(box.x+box.width*.6,box.y+box.height*.55,{steps:5});await page.mouse.up();
    const afterRotate=await page.evaluate(()=>window.__gallery.renderer.viewState());assert.notDeepEqual(afterRotate,before);
    await page.mouse.wheel(0,-100);const afterZoom=await page.evaluate(()=>window.__gallery.renderer.viewState());assert.notDeepEqual(afterZoom,afterRotate);
    await page.locator('#reset').click();row.scoped_interactions='PASS: mouse orbit, wheel zoom, reset click, one renderer; not universal interaction acceptance';
   }
   row.requests=[...requests.values()];const selected=row.requests.filter(r=>r.path===asset.glb);assert.equal(selected.length,1);const transfer=selected[0];assert(transfer.finished&&transfer.status===200&&!transfer.from_disk_cache&&!transfer.from_service_worker);
   assert(!row.requests.some(r=>r.path.endsWith('.blend')));assert(!row.requests.some(r=>r.path.endsWith('.glb')&&r.path!==asset.glb));
   row.model_transfer_ms=(transfer.finished-transfer.started)*1000;row.model_encoded_transfer_bytes=transfer.encoded_transfer_bytes;
   row.page_js_encoded_transfer_bytes=row.requests.filter(r=>r.type==='Script').reduce((n,r)=>n+(r.encoded_transfer_bytes||0),0);
   row.poster_and_image_encoded_transfer_bytes=row.requests.filter(r=>r.type==='Image').reduce((n,r)=>n+(r.encoded_transfer_bytes||0),0);
   row.model_transfer_note='body bytes are pinned GLB bytes; encoded transfer additionally includes HTTP headers; application JS and posters are accounted separately';
   assert.deepEqual(errors,[]);row.status='PASS';console.log(profile.name,asset.id,Math.round(row.model_transfer_ms)+'ms transfer',Math.round(row.navigation_to_ready_ms)+'ms ready');
  }catch(error){row.status='FAIL';row.error=error.message;report.errors.push({id:asset.id,profile:profile.name,message:error.message});throw error;}
  finally{await context.close();await writeFile(resolve(out,'network-report.json'),JSON.stringify(report,null,2)+'\n');}
 }
 report.status='PASS';
}catch(error){report.status='FAIL';if(!report.errors.length)report.errors.push({message:error.message});throw error;}
finally{await browser?.close();await new Promise(ok=>server.close(ok));await writeFile(resolve(out,'network-report.json'),JSON.stringify(report,null,2)+'\n');}

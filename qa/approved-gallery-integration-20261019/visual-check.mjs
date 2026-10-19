// Additional actual raster sequences. Does not change application code.
import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile,writeFile,mkdir,stat} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
const out=resolve(process.env.QA_VISUAL_ROOT||'qa/approved-gallery-integration-20261019/visual'),root=resolve('dist'),prefix='/lowpoly-vault/';
await mkdir(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.webp':'image/webp','.glb':'model/gltf-binary'};
const server=createServer(async(req,res)=>{try{const path=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(!path.startsWith(prefix))throw Error('prefix');let file=resolve(root,path.slice(prefix.length)||'index.html');if(!file.startsWith(root+sep))throw Error('path');if((await stat(file)).isDirectory())file=resolve(file,'index.html');res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream'}).end(await readFile(file));}catch{res.writeHead(404).end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}${prefix}`;
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-gpu-rasterization']});
const report={source_sha:process.env.GITHUB_SHA,browser:browser.version(),base,frames:[],errors:[],notes:['Raster sequences use observed browser times; screenshot overhead is included. Software-rendered Chromium and emulated touch, not physical-device timing.']};
report.screencasts=[];
const ready=(page,id)=>page.waitForFunction(id=>document.querySelector('#detail')?.dataset.state==='ready'&&(!id||window.__gallery.state.selected===id),id,{timeout:45000});
async function shot(page,name){const state=await page.evaluate(()=>({time:performance.now(),selected:window.__gallery?.state.selected,detail:document.querySelector('#detail')?.dataset.state,poster:document.querySelector('#detail-poster')?.dataset.modelId,reference:window.__gallery?.renderer?.stats.referenceState,comparison:window.__gallery?.renderer?.comparison,transition:window.__gallery?.renderer?.stats.cameraTransition,viewport:[innerWidth,innerHeight],overflow:document.documentElement.scrollWidth>innerWidth}));await page.screenshot({path:resolve(out,name+'.png')});report.frames.push({name,...state});console.log('Frame '+name);}
async function sequence(page,name,action,delays=[0,150,450,900,1800,3000,4000]){await page.evaluate(()=>window.__visualStart=performance.now());await action();for(const target of delays){const elapsed=await page.evaluate(()=>performance.now()-window.__visualStart);if(elapsed<target)await page.waitForTimeout(target-elapsed);await shot(page,`${name}-${String(target).padStart(4,'0')}`);}}
async function screencast(page,name,action,duration=4200){
 const session=await page.context().newCDPSession(page),frames=[];
 const listener=event=>{frames.push({data:event.data,timestamp:event.metadata.timestamp});void session.send('Page.screencastFrameAck',{sessionId:event.sessionId}).catch(()=>{});};
 session.on('Page.screencastFrame',listener);await session.send('Page.startScreencast',{format:'jpeg',quality:85,maxWidth:960,maxHeight:667,everyNthFrame:1});
 await action();await page.waitForTimeout(duration);await session.send('Page.stopScreencast');session.off('Page.screencastFrame',listener);
 const indices=[...new Set(Array.from({length:8},(_,i)=>Math.round(i*Math.max(0,frames.length-1)/7)))];
 const selected=[];for(const [n,index] of indices.entries()){if(!frames[index])continue;const file=`${name}-cast-${String(n).padStart(2,'0')}.jpg`;await writeFile(resolve(out,file),Buffer.from(frames[index].data,'base64'));selected.push({file,frame_index:index,timestamp:frames[index].timestamp});}
 report.screencasts.push({name,captured_frames:frames.length,timestamps:frames.map(f=>f.timestamp),selected});await session.detach();
 await page.waitForFunction(()=>!window.__gallery.renderer.referenceFrame&&!window.__gallery.renderer.stats.cameraTransition,null,{timeout:20000});await shot(page,name+'-settled');
 console.log(`Screencast ${name}: ${frames.length} actual compositor frames`);
}
const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
try{
 if(process.env.QA_WARM_MOTION_ONLY==='1'){
  for(const [id,kind] of [['waptia','hand'],['conifer-tree','human']]){
   await page.goto(base+'models/?model='+id);await ready(page,id);await page.mouse.move(1400,20);
   await page.locator('#compare').click();await page.waitForFunction(()=>window.__gallery.renderer.companion&&!window.__gallery.renderer.referenceFrame&&!window.__gallery.renderer.stats.cameraTransition,null,{timeout:20000});
   await page.locator('#reset').click();await page.waitForFunction(()=>!window.__gallery.renderer.referenceFrame&&!window.__gallery.renderer.stats.cameraTransition);
   await screencast(page,kind+'-warm-entry',()=>page.locator('#compare').click());
   await screencast(page,kind+'-warm-reset',()=>page.locator('#reset').click(),2600);
  }
  report.status='captured-for-visual-review';
 }else{
 await page.goto(base+'models/?model=waptia');await ready(page,'waptia');await page.mouse.move(1400,20);await shot(page,'desktop-list');
 await page.locator('#filters').click();await page.waitForTimeout(350);await shot(page,'desktop-filters');await page.keyboard.press('Escape');
 await page.locator('#info').click();await page.waitForTimeout(300);await shot(page,'desktop-info-downloads');await page.keyboard.press('Escape');
 await sequence(page,'hand-entry',()=>page.locator('#compare').evaluate(e=>e.click()));
 await page.waitForFunction(()=>window.__gallery.renderer.stats.referenceState==='ready');
 await page.locator('#detail').focus();await page.keyboard.press('ArrowRight');await page.keyboard.press('+');await shot(page,'hand-orbit-zoom');
 await sequence(page,'hand-reset',()=>page.locator('#reset').evaluate(e=>e.click()));
 await page.waitForFunction(()=>!window.__gallery.renderer.comparison&&!window.__gallery.renderer.stats.cameraTransition);
 await screencast(page,'hand-warm-entry',()=>page.locator('#compare').click());
 await screencast(page,'hand-warm-reset',()=>page.locator('#reset').click(),2600);
 await page.evaluate(()=>window.__gallery.choose('conifer-tree'));await ready(page,'conifer-tree');
 await sequence(page,'human-entry',()=>page.locator('#compare').evaluate(e=>e.click()));
 await sequence(page,'human-reset',()=>page.locator('#reset').evaluate(e=>e.click()));
 await screencast(page,'human-warm-entry',()=>page.locator('#compare').click());
 await screencast(page,'human-warm-reset',()=>page.locator('#reset').click(),2600);
 // Keep one actual GLB request pending so the selected poster is visible.
 const manifest=JSON.parse(await readFile('assets/manifest.json','utf8')),asset=manifest.assets.find(a=>a.id==='nereites-lobed-meander');
 let release,arrived;const held=new Promise(r=>release=r),requested=new Promise(r=>arrived=r);
 const modelURL=new URL(asset.glb,base).href;
 await page.route(modelURL,async route=>{arrived();await held;await route.continue().catch(()=>{});});
 await page.evaluate(id=>void window.__gallery.choose(id),asset.id);await requested;await shot(page,'delayed-selected-poster');
 assert.equal(await page.locator('#detail-poster').getAttribute('data-model-id'),asset.id);
 await sequence(page,'selected-first-frame',async()=>release(),[0,150,450,900,1800]);await ready(page,asset.id);await page.unroute(modelURL);
 await page.goto(base+'models/cooperoceras/');await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready',null,{timeout:45000});await shot(page,'independent-detail');
 await page.goto(base);await page.locator('#home-page').waitFor({state:'visible'});await shot(page,'preserved-home');
 await page.locator('#hero-inspect').click();await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready');await shot(page,'preserved-home-modal');await page.keyboard.press('Escape');
 await context.close();
 const mobile=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true});const touch=await mobile.newPage();touch.on('pageerror',e=>report.errors.push(e.message));
 await touch.goto(base+'zh-CN/models/');await touch.waitForFunction(()=>window.__gallery?.models.length===175);await shot(touch,'mobile-list');
 await touch.locator('#search').fill('waptia');await touch.locator('#search').press('Enter');await touch.locator('#slots [data-id="waptia"]').tap();await shot(touch,'mobile-poster-detail');
 await touch.locator('#mobile-interact').tap();await ready(touch,'waptia');await shot(touch,'mobile-live-detail');
 await sequence(touch,'mobile-hand-entry',()=>touch.locator('#compare').evaluate(e=>e.click()),[0,450,1800,4000]);
 await sequence(touch,'mobile-reset',()=>touch.locator('#reset').evaluate(e=>e.click()),[0,450,1800,4000]);
 await touch.locator('#mobile-back').tap();await shot(touch,'mobile-back-to-results');await touch.locator('#filters').tap();await touch.waitForTimeout(350);await shot(touch,'mobile-filters');
 await mobile.close();assert.deepEqual(report.errors,[]);assert(report.frames.every(f=>!f.overflow));report.status='captured-for-visual-review';
 }
}catch(e){report.status='failed';report.error=e.stack;throw e;}
finally{await browser.close();await new Promise(r=>server.close(r));await writeFile(resolve(out,'sequence.json'),JSON.stringify(report,null,2)+'\n');}

// Independent real-browser checks for final sorting delta and native history.
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
import {createServer} from 'node:http';
import {readFile,writeFile,mkdir,stat} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
const root=resolve('dist'),prefix='/lowpoly-vault/',out=resolve(process.env.QA_OUTPUT_DIR);await mkdir(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.webp':'image/webp','.glb':'model/gltf-binary'};
const server=createServer(async(req,res)=>{try{const path=decodeURIComponent(new URL(req.url,'http://localhost').pathname);assert(path.startsWith(prefix));let file=resolve(root,path.slice(prefix.length)||'index.html');assert(file.startsWith(root+sep));if((await stat(file)).isDirectory())file=resolve(file,'index.html');res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream'}).end(await readFile(file));}catch{res.writeHead(404).end();}});await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}${prefix}`,browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-gpu-rasterization']});
const report={source_sha:process.env.GITHUB_SHA,browser:browser.version(),cases:[],errors:[]};
const ready=page=>page.waitForFunction(()=>document.querySelector('#detail')?.dataset.state==='ready');
try{
 for(const sort of ['name','name-desc','triangles-asc']){
  const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'}),page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));let requests=0;page.on('request',r=>{if(r.url().endsWith('.glb'))requests++;});
  await page.goto(base+`models/?model=waptia&sort=${sort}`);await ready(page);
  const original=await page.evaluate(()=>({ids:window.__gallery.state.results.map(a=>a.id),selected:window.__gallery.state.selected,token:window.__gallery.renderer.token}));const oldRequests=requests;
  if(sort==='triangles-asc'){
   await page.locator('#filters').click();assert.equal(await page.locator('#filter-form select').inputValue(),'triangles');await page.locator('#filter-apply').click();
   assert.deepEqual(await page.evaluate(()=>window.__gallery.state.results.map(a=>a.id)),original.ids);assert.equal(new URL(page.url()).searchParams.get('sort'),'triangles-asc');
   await page.screenshot({path:resolve(out,'triangles-alias-applied.png')});
  }else{
   await page.locator('#wheel').evaluate(w=>{w.scrollTop=50*128+11;});
   await page.waitForFunction(()=>window.__gallery.state.center===window.__gallery.state.results[50].id&&document.querySelector('#wheel').scrollTop===50*128+11);
   const before=await page.evaluate(()=>{const p=window.__gallery;return {ids:p.state.results.map(a=>a.id),center:p.state.center,keyboard:p.state.keyboard,scroll:document.querySelector('#wheel').scrollTop};});
   await page.locator('#language').click();
   const after=await page.evaluate(()=>{const p=window.__gallery;return {lang:p.state.lang,ids:p.state.results.map(a=>a.id),center:p.state.center,keyboard:p.state.keyboard,scroll:document.querySelector('#wheel').scrollTop,history:history.state};});
   assert.equal(after.lang,'zh');assert.notDeepEqual(after.ids,before.ids);assert.equal(after.center,before.center);assert.equal(after.keyboard,before.keyboard);
   assert.equal(after.scroll,after.ids.indexOf(before.center)*128+(before.scroll-before.ids.indexOf(before.center)*128));assert.equal(after.history.scroll,after.scroll);
   await page.locator('#language').click();assert.deepEqual(await page.evaluate(()=>window.__gallery.state.results.map(a=>a.id)),before.ids);
   await page.screenshot({path:resolve(out,sort+'-locale-roundtrip.png')});
  }
  assert.equal(requests,oldRequests,'Sort/locale changes do not fetch a new GLB');assert.equal(await page.evaluate(()=>window.__gallery.renderer.token),original.token);assert.equal(await page.evaluate(()=>window.__gallery.state.selected),original.selected);
  report.cases.push({name:sort,status:'pass',glb_requests_unchanged:true});await context.close();
 }
 const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));await page.goto(base+'models/?model=cooperoceras');await ready(page);
 const snap=()=>page.evaluate(()=>{const rect=s=>{const r=document.querySelector(s).getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height};};return {scroll:document.querySelector('#wheel').scrollTop,selected:window.__gallery.state.selected,center:window.__gallery.state.center,pageScroll:scrollY,header:rect('header'),catalog:rect('.catalog'),workspace:rect('.workspace')};});
 const before=await snap(),box=await page.locator('#wheel').boundingBox();await page.mouse.move(box.x+box.width*.3,box.y+box.height*.5);await page.mouse.wheel(0,900);
 // Require the observed position change before accepting a settled frame.
 await page.waitForFunction(s=>document.querySelector('#wheel').scrollTop>s&&window.__gallery.settler.state==='idle',before.scroll);const after=await snap();
 assert.equal(after.selected,before.selected);assert.equal(after.pageScroll,before.pageScroll);for(const k of ['header','catalog','workspace'])for(const f of ['x','y','width','height'])assert(Math.abs(before[k][f]-after[k][f])<.6);
 await page.locator(`#slots [data-id="${after.center}"]`).click();await page.waitForFunction(id=>document.querySelector('#detail').dataset.state==='ready'&&window.__gallery.state.selected===id,after.center);
 await page.goBack();await page.waitForFunction(id=>document.querySelector('#detail').dataset.state==='ready'&&window.__gallery.state.selected===id,before.selected);const back=await snap();assert(Math.abs(back.scroll-after.scroll)<1);
 await page.setViewportSize({width:1100,height:760});await page.waitForTimeout(150);assert.equal(await page.evaluate(()=>window.__gallery.state.selected),before.selected);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.screenshot({path:resolve(out,'native-scroll-back-resize.png')});report.cases.push({name:'native-scroll-history-resize-with-observed-position-wait',status:'pass',before,after,back});await context.close();
 const filtersContext=await browser.newContext({viewport:{width:1440,height:1000}}),filterPage=await filtersContext.newPage();await filterPage.goto(base+'models/?model=waptia');await ready(filterPage);await filterPage.locator('#filters').click();await filterPage.waitForTimeout(350);
 const filterHeader=await filterPage.evaluate(()=>({scrollY,headerY:document.querySelector('header').getBoundingClientRect().y,visualOffset:visualViewport.offsetTop,visualScale:visualViewport.scale}));await filterPage.screenshot({path:resolve(out,'desktop-filters-settled.png')});report.cases.push({name:'desktop-filter-header-observation',status:'observed',snapshot:filterHeader});await filtersContext.close();
 const mobile=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true}),touch=await mobile.newPage();
 await touch.goto(base+'zh-CN/models/');await touch.waitForFunction(()=>window.__gallery?.models.length===175);await touch.locator('#search').fill('waptia');await touch.locator('#search').press('Enter');await touch.locator('#slots [data-id="waptia"]').tap();
 const header=()=>touch.evaluate(()=>({time:performance.now(),scrollY,headerY:document.querySelector('header').getBoundingClientRect().y,visualOffset:visualViewport.offsetTop,visualScale:visualViewport.scale}));
 const headerSamples=[await header()];await touch.waitForTimeout(250);headerSamples.push(await header());await touch.waitForTimeout(750);headerSamples.push(await header());
 await touch.screenshot({path:resolve(out,'mobile-poster-header-settled.png')});report.cases.push({name:'mobile-poster-header-observation',status:'observed',samples:headerSamples});await mobile.close();
 assert.deepEqual(report.errors,[]);report.status='pass';
}catch(e){report.status='fail';report.error=e.stack;throw e;}
finally{await browser.close();await new Promise(r=>server.close(r));await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}

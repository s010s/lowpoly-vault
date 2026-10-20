/** First-paint acceptance against built HTML, with real delayed/failed resources. */
import assert from 'node:assert/strict';
import {readFile,readdir} from 'node:fs/promises';
import {resolve} from 'node:path';

export async function checkGalleryStartup({browser,root,baseURL,output,report}){
 const html=await readFile(resolve(root,'models/index.html'),'utf8');
 const entry=html.match(/<script\b[^>]*\bsrc="([^"]+)"[^>]*>/)?.[1];
 assert(entry,'Built page has an entry module');
 const names=await readdir(resolve(root,'assets')),sources=await Promise.all(names.filter(name=>/\.(?:js|css)$/.test(name)).map(async name=>[name,await readFile(resolve(root,'assets',name),'utf8')]));
 const locate=(marker,extension)=>{const found=sources.filter(([name,text])=>name.endsWith(extension)&&text.includes(marker));assert.equal(found.length,1,`Unique built resource for ${marker}`);return 'assets/'+found[0][0];};
 const targets={entry:new URL(entry,baseURL).pathname,bootstrap:locate('Gallery enhancement unavailable','.js'),main:locate('window.__gallery','.js'),css:locate('.slot-image','.css'),manifest:'assets/manifest.json',resources:'gallery/resources.json'};
 const variants=Object.entries(targets);
 async function captureFirstPaint(page,path){
  // A deliberately held module/stylesheet can keep document.fonts.ready pending.
  // Capture the actual interim pixels, not a later font-ready state that cannot
  // exist until this test releases the request. DOM/layout assertions stay intact.
  const previous=process.env.PW_TEST_SCREENSHOT_NO_FONTS_READY;
  process.env.PW_TEST_SCREENSHOT_NO_FONTS_READY='1';
  try{return await page.screenshot({path});}
  finally{if(previous===undefined)delete process.env.PW_TEST_SCREENSHOT_NO_FONTS_READY;else process.env.PW_TEST_SCREENSHOT_NO_FONTS_READY=previous;}
 }
 async function inspectFallback(page){
  await page.locator('#static-route-content .vault-header').waitFor({state:'visible'});
  const state=await page.evaluate(()=>({
   gallery:!!window.__gallery,mobileDetail:document.body.classList.contains('mobile-detail'),legacy:[...document.querySelectorAll('body>.skip,body>.topbar')].map(el=>getComputedStyle(el).display),
   links:document.querySelectorAll('#static-route-content .slot[href]').length,
   cards:document.querySelectorAll('#static-route-content .static-grid').length,
   mainDisplay:getComputedStyle(document.querySelector('#static-route-content main')).display,
   columns:getComputedStyle(document.querySelector('#static-route-content main')).gridTemplateColumns.split(' ').length,
   wheelHeight:document.querySelector('#wheel').clientHeight,
   selected:document.querySelector('.gallery-static .slot[data-selected=true]')?.dataset.id,
   header:document.querySelector('.vault-header').getBoundingClientRect().toJSON(),
   catalog:document.querySelector('.catalog').getBoundingClientRect().toJSON(),
   workspace:document.querySelector('.workspace').getBoundingClientRect().toJSON(),
   poster:document.querySelector('#detail-poster')?.getAttribute('src'),
   disabledControls:[...document.querySelectorAll('.gallery-static button,.gallery-static input')].every(el=>el.disabled),
   background:getComputedStyle(document.body).backgroundColor,color:getComputedStyle(document.querySelector('#static-route-content')).color,
   giantSVG:[...document.querySelectorAll('svg')].some(el=>{const b=el.getBoundingClientRect();return b.width>100||b.height>100;}),
   width:document.documentElement.scrollWidth,viewport:innerWidth,
  }));
  assert(!state.gallery);assert(state.links>30);assert.equal(state.cards,0,'The superseded card grid is never visible at startup');
  assert.equal(state.mainDisplay,'grid');assert.equal(state.columns,state.viewport<=760?1:2,'First paint already has approved responsive gallery geometry');assert(state.mobileDetail?state.workspace.height>100:state.wheelHeight>100);assert(state.poster);assert(state.disabledControls,'Native controls do not pretend unavailable interaction is ready');assert(state.legacy.every(value=>value==='none'),'Inactive legacy shell is hidden before JavaScript');
  assert(!state.giantSVG,'No unbounded black SVG first paint');assert(state.width<=state.viewport+1,'Fallback fits the viewport');
  assert.equal(state.background,'rgb(246, 243, 236)','The gallery does not flash a different site theme before enhancement');
  assert.equal(state.color,'rgb(38, 42, 37)');
  const detail=await page.locator('#static-route-content .slot').first().getAttribute('href');
  const response=await page.request.get(new URL(detail,baseURL).href);assert(response.ok());assert((await response.text()).includes('class="static-downloads"'));
  return state;
 }
 for(const width of [320,390,1440])for(const mode of ['delay','fail'])for(const [index,[kind,target]] of variants.entries()){
  const mobile=width<=760,dark=index%3!==0,name=`startup-${mode}-${kind}-${width}`,row={name,status:'running'};report.cases.push(row);
  const context=await browser.newContext({viewport:{width,height:mobile?844:1000},hasTouch:mobile,isMobile:mobile,colorScheme:dark?'dark':'light'});
  const page=await context.newPage();page.setDefaultTimeout(20000);
  await page.addInitScript(theme=>localStorage.setItem('vault-theme',theme),dark?'dark':'light');
  const posterRequests=[];page.on('request',request=>{if(/gallery\/posters\//.test(request.url()))posterRequests.push(request.url());});
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  let release,observed;const gate=new Promise(done=>release=done),requested=new Promise(done=>observed=done);
  const targetURL=new URL(target,baseURL).href;
  await page.route(targetURL,async route=>{observed();if(mode==='delay'){await gate;await route.continue();}else await route.abort('failed');});
  try{
   await page.goto(new URL(mobile?'zh-CN/models/page/2/':'models/',baseURL).href,{waitUntil:'commit'});
   let timer;await Promise.race([requested,new Promise((_,reject)=>timer=setTimeout(()=>reject(Error('Target prerequisite was never requested: '+kind)),15000))]).finally(()=>clearTimeout(timer));
   if(mode==='fail')await page.waitForLoadState('load');
   row.fallback=await inspectFallback(page);
   assert(new Set(posterRequests).size<row.fallback.links/2,'Native lazy poster loading does not eagerly fetch the entire collection');row.fallbackPosterRequests=new Set(posterRequests).size;
   await captureFirstPaint(page,resolve(output,`${name}-fallback.png`));
   if(mode==='delay'){
    release();await page.waitForFunction(()=>window.__gallery?.models.length>0,null,{timeout:45000});
    const mounted=await page.evaluate(()=>({legacy:document.querySelectorAll('body>.topbar,#static-route-content').length,headers:document.querySelectorAll('body>header').length,canvas:document.querySelectorAll('canvas.preview-renderer').length,wheelHeight:document.querySelector('#wheel').clientHeight,mainDisplay:getComputedStyle(document.querySelector('body>main')).display,selected:window.__gallery.state.selected,header:document.querySelector('.vault-header').getBoundingClientRect().toJSON(),catalog:document.querySelector('.catalog').getBoundingClientRect().toJSON(),workspace:document.querySelector('.workspace').getBoundingClientRect().toJSON()}));
    assert.equal(mounted.legacy,0);assert.equal(mounted.headers,1);assert(mounted.canvas<=1);assert(mounted.wheelHeight>100);assert(Math.abs(mounted.wheelHeight-row.fallback.wheelHeight)<=1,'The wheel keeps its first-paint height');assert.equal(mounted.mainDisplay,'grid');assert(mounted.selected);assert.equal(mounted.selected,row.fallback.selected,'The native selected model matches enhancement');
    for(const region of ['header','catalog','workspace'])for(const dimension of ['x','y','width','height'])assert(Math.abs(mounted[region][dimension]-row.fallback[region][dimension])<=1,`No ${region} ${dimension} layout jump at hydration`);row.mounted=mounted;
    if(kind==='entry'){await page.unroute(targetURL);await page.reload();await page.waitForFunction(()=>window.__gallery?.models.length>0,null,{timeout:45000});assert.equal(await page.locator('body>header').count(),1);}
    await page.screenshot({path:resolve(output,`${name}-mounted.png`)});
    assert.deepEqual(errors,[]);
   }else{
    // The browser may surface a rejected entry/bootstrap import. Those exact
    // injected network failures are expected; unrelated runtime errors are not.
    assert(errors.every(message=>/Failed to fetch dynamically imported module|Importing a module script failed|Unable to preload CSS|error loading dynamically imported module/i.test(message)),JSON.stringify(errors));
    row.expected_resource_errors=errors;
   }
   row.status='pass';
  }catch(error){row.status='fail';row.error=error.stack;await captureFirstPaint(page,resolve(output,`${name}-failure.png`)).catch(()=>{});}
  finally{release();await context.close();}
 }
 for(const width of [320,390,1440]){
  const name=`startup-delayed-entry-selected-${width}`,row={name,status:'running'};report.cases.push(row);
  const context=await browser.newContext({viewport:{width,height:width<=760?844:1000},hasTouch:width<=760,isMobile:width<=760}),page=await context.newPage();
  let release,observed;const gate=new Promise(done=>release=done),requested=new Promise(done=>observed=done);
  await page.route(new URL(targets.entry,baseURL).href,async route=>{observed();await gate;await route.continue();});
  try{
   await page.goto(new URL('models/?model=cooperoceras&q=cooperoceras',baseURL).href,{waitUntil:'commit'});await requested;
   row.fallback=await inspectFallback(page);assert.equal(row.fallback.selected,'cooperoceras');assert.equal(row.fallback.mobileDetail,width<=760);
   if(width<=760){assert(await page.locator('#mobile-back').isVisible());assert.equal(await page.locator('#mobile-back').getAttribute('href'),new URL('models/?q=cooperoceras',baseURL).pathname+'?q=cooperoceras');}
   await captureFirstPaint(page,resolve(output,`${name}-fallback.png`));release();await page.waitForFunction(()=>window.__gallery?.models.length>0,null,{timeout:45000});
   assert.equal(await page.evaluate(()=>document.body.classList.contains('mobile-detail')),width<=760);await page.screenshot({path:resolve(output,`${name}-mounted.png`)});row.status='pass';
  }catch(error){row.status='fail';row.error=error.stack;}finally{release();await context.close();}
 }
 for(const width of [320,390,1440])for(const dark of [false,true]){
  const name=`startup-no-javascript-no-external-css-${width}-${dark?'dark':'light'}`,row={name,status:'running'};report.cases.push(row);
  const context=await browser.newContext({javaScriptEnabled:false,viewport:{width,height:width<=760?844:1000},colorScheme:dark?'dark':'light'}),page=await context.newPage();
  try{await page.route('**/*.css',route=>route.abort());await page.goto(new URL('zh-CN/models/page/2/',baseURL).href);row.fallback=await inspectFallback(page);await captureFirstPaint(page,resolve(output,`${name}.png`));row.status='pass';}
  catch(error){row.status='fail';row.error=error.stack;}finally{await context.close();}
 }
}

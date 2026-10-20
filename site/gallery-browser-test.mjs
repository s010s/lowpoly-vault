/** Real Chromium acceptance for the approved wheel and the preserved document routes.
 * GALLERY_DIR, SITE_BASE, QA_OUTPUT_DIR, CHROMIUM_PATH and QA_BASE_URL are portable.
 * QA_BASE_URL uses that exact origin; otherwise this script serves the built files.
 */
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { modelHeight } from './gallery/model-dimensions.js';
import {checkGalleryStartup} from './gallery-startup-browser.mjs';
import {checkMobileGallery} from './gallery-mobile-browser.mjs';

const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.webp':'image/webp','.txt':'text/plain','.zip':'application/zip'};
const defaultGroups=process.env.QA_FORCE_WEBGL_FALLBACK==='1'?['fallback']:['startup','routes','interaction','handoff','detail','scroll','resources','scale','modal','fallback'];
export async function runGalleryBrowserTests({groups=defaultGroups,root=resolve(process.env.GALLERY_DIR||'dist'),output=resolve(process.env.QA_OUTPUT_DIR||'qa/approved-gallery-browser'),baseURL=process.env.QA_BASE_URL,modelId=process.env.QA_GALLERY_MODEL_ID}={}) {
  root=resolve(root);output=resolve(output);
  const prefix=process.env.SITE_BASE||'/lowpoly-vault/';
  const report={status:'running',source_commit:process.env.GITHUB_SHA||null,groups,cases:[],errors:[],requests:[],limitations:['Chromium software rendering; mobile and touch are emulated, not physical-device performance.']};
  let server,browser;
  await mkdir(output,{recursive:true});
  try {
    if(!baseURL){
      server=createServer(async(req,res)=>{try{
        const url=new URL(req.url,'http://localhost');if(!url.pathname.startsWith(prefix))throw Error('Outside prefix');
        let file=resolve(root,decodeURIComponent(url.pathname.slice(prefix.length))||'index.html');
        if(file!==root&&!file.startsWith(root+sep))throw Error('Outside root');
        if((await stat(file)).isDirectory())file=resolve(file,'index.html');
        const bytes=await readFile(file);res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream','Content-Length':bytes.length}).end(bytes);
      }catch{res.writeHead(404).end();}});
      await new Promise((done,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',done);});
      baseURL=`http://127.0.0.1:${server.address().port}${prefix}`;
    }
    baseURL=new URL(baseURL).href;if(!baseURL.endsWith('/'))baseURL+='/';
    report.base=baseURL;
    const response=await fetch(new URL('assets/manifest.json',baseURL));assert(response.ok,'Published manifest is accessible');
    const manifest=await response.json(),assets=manifest.assets;
    assert((!manifest.review_only||process.env.QA_REVIEW_ONLY==='1')&&Array.isArray(assets)&&assets.length>30,'Exercise the full catalog; review-only data requires the explicit isolated-review profile');
    const initial=assets.find(a=>a.id===(modelId||'cooperoceras'))||assets[0],last=assets.at(-1);
    report.published_count=assets.length;
    browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-gpu-rasterization']});
    report.browser=browser.version();
    const has=group=>groups.includes(group);
    if(has('startup')||has('routes'))await checkGalleryStartup({browser,root,baseURL,output,report});
    if(has('interaction'))await checkMobileGallery({browser,baseURL,output,report,assets});
    async function ready(page,id){await page.waitForFunction(id=>window.__gallery&&document.querySelector('#detail')?.dataset.state==='ready'&&(!id||document.querySelector('#detail').dataset.modelId===id),id,{timeout:45000});}
    async function boot(page,path=`models/?model=${initial.id}`,mobile=false){await page.goto(new URL(path,baseURL).href);await page.waitForFunction(()=>window.__gallery?.models.length>0,{},{timeout:45000});if(!mobile)await ready(page);if(manifest.review_only)assert(await page.locator('.gallery-review-notice').isVisible(),'The isolated review must remain visibly labeled');}
    async function search(page,value){await page.locator('#search').fill(value);await page.locator('#search').press('Enter');await page.waitForFunction(q=>window.__gallery.state.query===q,value);}
    async function choose(page,id,{mobile=false}={}){await search(page,id);await page.locator(`#slots [data-id="${id}"]`).click();if(mobile)await page.waitForFunction(id=>document.querySelector('#detail').dataset.modelId===id&&document.body.classList.contains('mobile-detail'),id);else await ready(page,id);}
    async function test(name,fn,{path,mobile=false,prepare,skipBoot=false,...options}={}){
      const row={name,status:'running'};report.cases.push(row);
      const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},hasTouch:mobile,isMobile:mobile,acceptDownloads:true,...options});
      await context.grantPermissions(['clipboard-read','clipboard-write'],{origin:new URL(baseURL).origin});
      const page=await context.newPage();page.setDefaultTimeout(20000);
      page.on('pageerror',error=>report.errors.push({case:name,message:error.message}));
      const glbs=[];page.on('request',request=>{if(new URL(request.url()).pathname.endsWith('.glb')){glbs.push(request.url());report.requests.push({case:name,url:request.url()});}});
      try{if(prepare)await prepare({page,context});if(!skipBoot)await boot(page,path,mobile);await fn({page,context,row,glbs});await page.screenshot({path:resolve(output,`${name}.png`)});row.status='pass';}
      catch(error){row.status='fail';row.error=error.stack;await page.screenshot({path:resolve(output,`${name}-failure.png`)}).catch(()=>{});}
      finally{await context.close();}
    }
    if(has('routes')){
      await test('full-catalog-virtualized-routes',async({page,row})=>{
        const snapshot=await page.evaluate(()=>({ids:window.__gallery.models.map(a=>a.id),count:window.__gallery.state.results.length,slots:document.querySelectorAll('#slots .slot').length,renderers:document.querySelectorAll('canvas.preview-renderer').length,legacy:!!document.querySelector('#grid'),label:document.querySelector('#results').textContent}));
        assert.deepEqual(snapshot.ids,assets.map(a=>a.id));assert.equal(snapshot.count,assets.length);assert(snapshot.slots<40&&snapshot.slots<assets.length);assert.equal(snapshot.renderers,1);assert.equal(snapshot.legacy,false);assert(snapshot.label.includes(String(assets.length)));row.snapshot=snapshot;
        await boot(page,'zh-CN/models/page/2/');assert.equal(await page.locator('html').getAttribute('lang'),'zh-CN');
        assert.equal(await page.evaluate(()=>window.__gallery.state.selected),assets[24].id);
        assert.equal(await page.locator('#download').getAttribute('href'),new URL(assets[24].glb,baseURL).href);
        await page.locator('#language').click();assert.equal(await page.locator('html').getAttribute('lang'),'en');assert(new URL(page.url()).pathname.endsWith('/models/page/2/'));
        for(const locale of ['','zh-CN/'])for(const path of ['','about/','models/','models/page/2/',`models/${last.id}/`]){
          const response=await page.request.get(new URL(locale+path,baseURL).href);assert(response.ok());const html=await response.text();assert(html.includes('id="static-route-content"'));assert(html.includes('rel="canonical"'));assert(html.includes('hreflang="zh-CN"'));if(path.includes(last.id))assert(html.includes('application/ld+json'));
        }
      });
      await test('deep-search-normalization-and-reload',async({page,row,glbs})=>{
        const before=glbs.length;
        const fullwidth=last.id.replace(/[!-~]/g,c=>String.fromCharCode(c.charCodeAt(0)+0xfee0));
        await search(page,fullwidth+' '+last.category);
        const ids=await page.evaluate(()=>window.__gallery.state.results.map(a=>a.id));assert(ids.includes(last.id));
        assert.equal(glbs.length,before,'Search must not download a new GLB or change selection');
        await page.locator(`#slots [data-id="${last.id}"]`).click();await ready(page,last.id);
        await page.reload();await ready(page,last.id);assert.equal(await page.locator('#search').inputValue(),fullwidth+' '+last.category);
        row.deep_id=last.id;row.result_ids=ids;
      });
      // No JavaScript must expose an actual linked catalog and functional file URLs.
      const context=await browser.newContext({javaScriptEnabled:false});const page=await context.newPage();
      try{await page.goto(new URL('zh-CN/models/page/2/',baseURL).href);assert(await page.locator('#static-route-content .vault-header').isVisible());assert(await page.locator('.gallery-static .slot[href]').count()>0);assert.equal(await page.locator('#home-page').isVisible(),false);await page.locator('.gallery-static .slot').first().click();assert(await page.locator('.static-downloads a[download]').count()>=2);report.cases.push({name:'no-javascript-linked-documents',status:'pass'});}finally{await context.close();}
    }
    if(has('interaction')){
      await test('filter-draft-cancel-apply-no-glb',async({page,row,glbs})=>{
        const before=glbs.length,selected=await page.evaluate(()=>window.__gallery.state.selected),original=await page.evaluate(()=>window.__gallery.state.results.map(a=>a.id));
        await page.locator('#filters').click();await page.locator('#filter-form input[data-group="category"][value="plants"]').check();
        assert.deepEqual(await page.evaluate(()=>window.__gallery.state.results.map(a=>a.id)),original,'Draft does not mutate results');
        await page.locator('#filter-cancel').click();assert.deepEqual(await page.evaluate(()=>window.__gallery.state.facets.category),[]);
        await page.locator('#filters').click();await page.locator('#filter-form input[data-group="category"][value="plants"]').check();await page.locator('#filter-form select').selectOption('triangles-desc');await page.locator('#filter-apply').click();
        const actual=await page.evaluate(()=>window.__gallery.state.results.map(a=>({id:a.id,category:a.category,triangles:a.triangles})));assert(actual.length>0&&actual.every(a=>a.category==='plants'));assert(actual.every((a,i)=>!i||actual[i-1].triangles>=a.triangles));
        assert.equal(await page.evaluate(()=>window.__gallery.state.selected),selected);assert.equal(glbs.length,before,'Applying filters/sort must not fetch a model');
        assert.equal(new URL(page.url()).searchParams.get('category'),'plants');assert.equal(new URL(page.url()).searchParams.get('sort'),'triangles-desc');
        await page.reload();await ready(page,selected);assert.deepEqual(await page.evaluate(()=>window.__gallery.state.results.map(a=>a.id)),actual.map(a=>a.id));row.filtered=actual.length;
      });
      await test('popover-interruption-keyboard-empty-recovery',async({page})=>{
        for(let i=0;i<3;i++){await page.locator('#filters').click();await page.locator('#filter-close').click();}
        await page.locator('#filters').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('#filter-panel').getAttribute('data-open'),'true');assert.equal(await page.locator('#filter-panel').evaluate(el=>el.inert),false);
        await page.keyboard.press('Escape');assert.equal(await page.locator('#filter-panel').evaluate(el=>el.inert),true);assert(await page.locator('#filters').evaluate(el=>el===document.activeElement));
        for(const q of ['fern','arch','zzzz-no-model-987654'])await page.locator('#search').fill(q);await page.locator('#search').press('Enter');
        await page.locator('#empty-state').waitFor({state:'visible'});assert.equal(await page.locator('#wheel').getAttribute('tabindex'),'-1');
        await page.locator('#empty-clear').click();assert.equal(await page.evaluate(()=>window.__gallery.state.results.length),assets.length);assert.equal(await page.locator('#wheel').getAttribute('tabindex'),'0');
        await page.locator('#info').focus();await page.keyboard.press('Enter');assert(await page.locator('#info-panel').isVisible());await page.keyboard.press('Escape');assert(await page.locator('#info').evaluate(el=>el===document.activeElement));
      });
      await test('downloads-information-clipboard',async({page,row})=>{
        await choose(page,last.id);assert.equal(await page.locator('#download').getAttribute('href'),new URL(last.glb,baseURL).href);assert.equal(await page.locator('#blend').getAttribute('href'),new URL(last.blend,baseURL).href);
        assert.equal(await page.locator('#dimensions').textContent(),modelHeight(last));
        await page.locator('#info').click();const links=await page.locator('#info-content a').evaluateAll(nodes=>nodes.map(a=>({href:a.href,download:a.hasAttribute('download')})));
        for(const key of ['bundle','credits']){assert(last.downloads?.[key],`Delivered ${key} exists`);assert(links.some(a=>a.href===new URL(last.downloads[key],baseURL).href&&a.download));}
        assert(links.some(a=>a.href===new URL(`models/${last.id}/`,baseURL).href));assert((await page.locator('#info-content').textContent()).includes('not verified specimen measurements'));
        await page.keyboard.press('Escape');
        const download=page.waitForEvent('download');await page.locator('#download').click();assert.equal((await download).url(),new URL(last.glb,baseURL).href);
        for(let i=0;i<2;i++){await page.locator('#credits').click();await page.waitForFunction(()=>document.querySelector('#credits').dataset.copyState==='success');}
        const copied=await page.evaluate(()=>navigator.clipboard.readText());assert(copied.includes(last.name.en)&&copied.includes('Leon Made This')&&/CC.?BY.?4\.0/.test(copied));
        await page.evaluate(()=>Object.defineProperty(navigator.clipboard,'writeText',{configurable:true,value:()=>Promise.reject(new Error('Test denial'))}));await page.locator('#credits').click();await page.waitForFunction(()=>document.querySelector('#credits').dataset.copyState==='error');assert.match(await page.locator('#copy-status').textContent(),/Could not copy/);row.links=links;
      });
      await test('keyboard-center-selection-history',async({page,row})=>{
        await page.locator('#wheel').focus();const old=await page.evaluate(()=>window.__gallery.state.selected);await page.keyboard.press('End');
        assert.equal(await page.evaluate(()=>window.__gallery.state.selected),old,'Moving keyboard focus alone does not select');
        const next=await page.evaluate(()=>window.__gallery.state.keyboard);await page.keyboard.press('Enter');await ready(page,next);
        await page.waitForFunction(()=>window.__gallery.settler.state==='idle');
        assert(Math.abs(await page.evaluate(()=>document.querySelector('#wheel').scrollTop-window.__gallery.state.results.findIndex(a=>a.id===window.__gallery.state.selected)*128))<1,'Activation centers the selected row');
        await page.goBack();await ready(page,old);await page.goForward();await ready(page,next);row.ids=[old,next];
        const frame=await page.evaluate(()=>({id:document.querySelector('#detail-poster').dataset.modelId,selected:window.__gallery.state.selected,detail:window.__gallery.renderer.stats.detailId,renderers:document.querySelectorAll('canvas.preview-renderer').length}));assert.equal(frame.id,next);assert.equal(frame.detail,next);assert.equal(frame.renderers,1);
      },{reducedMotion:'reduce'});
      await test('mobile-lazy-open-back-and-interact',async({page,glbs})=>{
        assert.equal(glbs.length,0,'Mobile listing starts with posters only');assert.equal(await page.locator('.workspace').isVisible(),false);
        await choose(page,last.id,{mobile:true});assert.equal(glbs.length,0,'Opening a mobile detail remains poster-first');assert(await page.locator('#mobile-interact').isVisible());
        await page.locator('#mobile-back').tap();await page.waitForFunction(()=>!document.body.classList.contains('mobile-detail'));assert.equal(await page.locator('.catalog').isVisible(),true);
        await page.locator(`#slots [data-id="${last.id}"]`).tap();await page.locator('#mobile-interact').tap();await ready(page,last.id);assert(glbs.some(url=>url===new URL(last.glb,baseURL).href));
        await page.locator('#mobile-interact').tap();assert.equal(await page.locator('#detail').getAttribute('data-state'),'static');
        await page.locator('#mobile-back').tap();await page.waitForFunction(()=>!document.body.classList.contains('mobile-detail'));assert(await page.locator('.catalog').isVisible());assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);assert.equal(await page.locator('canvas.preview-renderer').count(),1);
      },{mobile:true,path:'models/'});
      await test('reduced-motion-chinese-panels',async({page})=>{
        assert.equal(await page.locator('html').getAttribute('lang'),'zh-CN');await page.locator('#filters').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('#filter-panel').getAttribute('data-motion'),'false');
        await page.keyboard.press('Escape');await page.locator('#credits').focus();await page.keyboard.press('Enter');await page.waitForFunction(()=>document.querySelector('#credits').dataset.copyState==='success');assert.match(await page.locator('#copy-status').textContent(),/署名已复制/);
        await page.locator('#info').click();const rect=await page.locator('#info-panel').boundingBox();assert(rect.x>=0&&rect.y>=0&&rect.x+rect.width<=1441&&rect.y+rect.height<=1001);
      },{path:`zh-CN/models/?model=${initial.id}`,reducedMotion:'reduce',colorScheme:'dark'});
    }
    if(has('handoff')){
      await test('wheel-hover-single-renderer-current-selection',async({page,row})=>{
        await search(page,'');const selected=await page.evaluate(()=>window.__gallery.state.selected);
        await page.locator('#wheel').focus();await page.keyboard.press('Home');
        const id=await page.evaluate(()=>window.__gallery.state.results[0].id),slot=page.locator(`#slots [data-id="${id}"]`);
        await page.mouse.move(1400,20);await slot.locator('.slot-image').hover();
        await page.waitForFunction(id=>window.__gallery.renderer.stats.hoverFirstFrameId===id,id,{timeout:30000});
        assert.equal(await page.evaluate(()=>window.__gallery.state.selected),selected,'Hover inspection must not select a new model');assert.equal(await page.locator('canvas.preview-renderer').count(),1);
        await page.mouse.move(1400,20);await page.waitForFunction(()=>window.__gallery.renderer.stats.hoverId===null);
        assert.equal(await page.locator('#detail-poster').getAttribute('data-model-id'),selected);row.hovered=id;
      });
      await test('selected-poster-live-and-repeat-supersession',async({page,row})=>{
        const late=assets.find(a=>a.id!==initial.id&&a.id!==last.id),latest=last.id;let release,requested;
        const held=new Promise(done=>release=done),arrived=new Promise(done=>requested=done),url=new URL(late.glb,baseURL).href;
        await page.route(url,async route=>{requested();await held;await route.continue().catch(()=>{});});
        await page.evaluate(id=>{void window.__gallery.choose(id);},late.id);await Promise.race([arrived,new Promise((_,reject)=>setTimeout(()=>reject(new Error('Intercepted model request did not arrive')),20000))]);
        const pending=await page.locator('#detail-poster').getAttribute('data-model-id');assert.equal(pending,late.id,'The old bitmap node is replaced at selection time');
        await page.evaluate(id=>window.__gallery.choose(id),latest);await ready(page,latest);release();await page.unroute(url);
        for(let i=0;i<3;i++)await page.evaluate(id=>window.__gallery.choose(id),latest);
        await ready(page,latest);await page.waitForTimeout(200);
        const state=await page.evaluate(()=>({selected:window.__gallery.state.selected,poster:document.querySelector('#detail-poster').dataset.modelId,live:window.__gallery.renderer.stats.detailId,canvas:document.querySelectorAll('canvas.preview-renderer').length,cache:window.__gallery.renderer.stats.cacheEntries,bytes:window.__gallery.renderer.stats.estimatedCacheBytes,limit:window.__gallery.renderer.stats.cacheByteLimit}));
        assert.equal(state.selected,latest);assert.equal(state.poster,latest);assert.equal(state.live,latest);assert.equal(state.canvas,1);assert(state.cache<=3);assert(state.bytes<=state.limit);row.state=state;
        // Repeated native Back/Forward must settle on the latest requested identity.
        await page.goBack();await page.goForward();await ready(page,latest);
      });
      await test('failed-load-poster-and-retry',async({page})=>{
        const asset=assets.find(a=>a.id!==initial.id),url=new URL(asset.glb,baseURL).href;
        await page.route(url,route=>route.fulfill({status:503,body:'Intentional unavailable model'}));
        await search(page,asset.id);await page.locator(`#slots [data-id="${asset.id}"]`).click();await page.waitForFunction(()=>document.querySelector('#detail').dataset.state==='fallback');
        assert.equal(await page.locator('#detail').getAttribute('data-state'),'fallback');assert.equal(await page.locator('#detail-poster').getAttribute('data-model-id'),asset.id);await page.locator('#detail-poster').evaluate(img=>img.decode());assert(await page.locator('#detail-poster').evaluate(img=>img.complete&&img.naturalWidth>0));assert(await page.locator('#retry').isVisible());
        await page.unroute(url);await page.locator('#retry').click();await ready(page,asset.id);assert.equal(await page.locator('canvas.preview-renderer').count(),1);
      });
      await test('webgl-context-loss-restores-selected-poster',async({page})=>{
        const id=await page.evaluate(()=>window.__gallery.state.selected);
        const supported=await page.evaluate(()=>{const context=window.__gallery.renderer.renderer.getContext(),extension=context.getExtension('WEBGL_lose_context');if(!extension)return false;window.__testContextLoss=extension;extension.loseContext();return true;});
        assert(supported,'Chromium must expose the context-loss test extension');
        await page.waitForFunction(()=>document.querySelector('#detail').dataset.state==='fallback');
        assert.equal(await page.locator('#detail-poster').getAttribute('data-model-id'),id);assert(await page.locator('#detail-poster').isVisible());
        await page.waitForTimeout(150);await page.evaluate(()=>window.__testContextLoss.restoreContext());await ready(page,id);
        assert.equal(await page.locator('canvas.preview-renderer').count(),1);
      });
      await test('held-pointer-cannot-orbit-new-selection',async({page})=>{
        const bounds=await page.locator('#detail').boundingBox(),x=bounds.x+bounds.width*.5,y=bounds.y+bounds.height*.45;
        await page.mouse.move(x,y);await page.mouse.down();await page.mouse.move(x+70,y+25,{steps:4});
        await page.evaluate(id=>window.__gallery.choose(id),last.id);await ready(page,last.id);
        const before=await page.evaluate(()=>window.__gallery.renderer.viewState().modelQuaternion);
        await page.mouse.move(x+150,y+65,{steps:4});await page.mouse.up();
        const after=await page.evaluate(()=>window.__gallery.renderer.viewState().modelQuaternion);
        assert.deepEqual(after,before,'A pointer held through replacement cannot continue the previous model orbit');
        assert.equal(await page.locator('#detail-poster').getAttribute('data-model-id'),last.id);
      },{reducedMotion:'reduce'});
      await test('scale-reference-reset-authored-dimensions',async({page,row})=>{
        const asset=assets.find(a=>a.id==='waptia')||initial;await choose(page,asset.id);const label=await page.locator('#dimensions').textContent();assert.equal(label,modelHeight(asset));assert.equal(await page.locator('#compare').isDisabled(),false);
        await page.locator('#detail').focus();await page.keyboard.press('ArrowRight');await page.keyboard.press('+');await page.locator('#compare').click();
        await page.waitForFunction(()=>window.__gallery.renderer.stats.referenceState==='ready',{},{timeout:20000});assert.equal(await page.locator('#compare').getAttribute('aria-pressed'),'true');assert.equal(await page.locator('#dimensions').textContent(),label);
        const meters=await page.evaluate(()=>window.__gallery.renderer.stats.referenceMeters);assert([.18,1.8].includes(meters));row.reference_meters=meters;
        await page.locator('#reset').click();await page.waitForFunction(()=>!window.__gallery.renderer.comparison&&!window.__gallery.renderer.stats.cameraTransition);assert.equal(await page.locator('#compare').getAttribute('aria-pressed'),'false');assert.equal(await page.locator('#comparison-label').isVisible(),false);assert.equal(await page.locator('#dimensions').textContent(),label);
        assert.equal(await page.locator('canvas.preview-renderer').count(),1);
      },{reducedMotion:'reduce'});
    }
    if(has('fallback')){
      await test('forced-webgl-fallback-keeps-gallery-functional',async({page,row})=>{
        await page.goto(new URL(`models/?model=${initial.id}`,baseURL).href);await page.waitForFunction(()=>window.__gallery&&document.querySelector('#detail').dataset.state==='fallback');
        assert.equal(await page.locator('canvas.preview-renderer').count(),0,'Forced fallback cannot count as GPU acceptance');
        await page.locator('#detail-poster').evaluate(img=>img.decode());assert(await page.locator('#detail-poster').isVisible());assert(await page.locator('#retry').isVisible());
        await search(page,last.id);await page.locator(`#slots [data-id="${last.id}"]`).click();await page.waitForFunction(()=>document.querySelector('#detail').dataset.state==='fallback');
        assert.equal(await page.locator('#download').getAttribute('href'),new URL(last.glb,baseURL).href);assert.equal(await page.locator('#detail-poster').getAttribute('data-model-id'),last.id);
        await page.locator('#info').click();assert((await page.locator('#info-content').textContent()).includes(last.name.en));row.gpu='not-accepted-forced-fallback';
      },{skipBoot:true,prepare:async({page})=>page.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){if(/webgl/i.test(type))return null;return original.call(this,type,...args);};})});
      await test('failed-catalog-retains-real-html',async({page})=>{
        await page.goto(new URL('zh-CN/models/',baseURL).href);await page.locator('.gallery-load-error').waitFor();assert(await page.locator('#static-route-content .vault-header').isVisible());assert(await page.locator('#static-route-content .slot[href]').count()>0);
        const detail=await page.locator('#static-route-content .slot[href]').first().getAttribute('href');const response=await page.request.get(new URL(detail,baseURL).href);assert(response.ok());assert((await response.text()).includes('class="static-downloads"'));
      },{skipBoot:true,prepare:async({page})=>page.route('**/assets/manifest.json',route=>route.fulfill({status:503,body:'Intentional unavailable catalog'}))});
    }
    if(has('scale')){
      await test('ten-thousand-models-virtualized-deep-search',async({page,row,glbs})=>{
        const fixture=Array.from({length:10000},(_,i)=>({...initial,id:`scale-${String(i).padStart(5,'0')}`,name:{en:`Scale specimen ${i}`,zh:i===9999?'深页测试模型':`测试模型 ${i}`},category:i%2?'plants':'geology',packs:[`pack-${i%19}`],worlds:[i%3?'prehistoric':'fiction'],triangles:100+i}));
        await page.route('**/assets/manifest.json',route=>route.fulfill({contentType:'application/json',body:JSON.stringify({...manifest,review_only:false,assets:fixture})}));
        await page.goto(new URL('models/',baseURL).href);await page.waitForFunction(()=>window.__gallery?.models.length===10000);await ready(page);
        assert((await page.locator('#slots .slot').count())<40);await page.locator('#wheel').focus();await page.keyboard.press('End');assert.equal(await page.locator('#wheel').getAttribute('aria-activedescendant'),'option-scale-09999');
        const before=glbs.length;await search(page,'深页 测试');assert.deepEqual(await page.evaluate(()=>window.__gallery.state.results.map(a=>a.id)),['scale-09999']);assert.equal(glbs.length,before);
        await page.locator('#slots [data-id="scale-09999"]').click();await ready(page,'scale-09999');assert.equal(await page.locator('#detail-poster').getAttribute('data-model-id'),'scale-09999');row.total=10000;row.virtual_slots=await page.locator('#slots .slot').count();
      },{skipBoot:true,reducedMotion:'reduce'});
    }
    if(has('scroll')){
      await test('native-wheel-stationary-layout-resize-history',async({page,row})=>{
        const snapshot=()=>page.evaluate(()=>{const rect=selector=>{const r=document.querySelector(selector).getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height};};return{header:rect('header'),catalog:rect('.catalog'),workspace:rect('.workspace'),scroll:document.querySelector('#wheel').scrollTop,selected:window.__gallery.state.selected,pageScroll:scrollY};});
        const before=await snapshot(),box=await page.locator('#wheel').boundingBox();row.native={before};
        await page.mouse.move(box.x+box.width*.3,box.y+box.height*.5);await page.mouse.wheel(0,900);
        // wheel() dispatches input without waiting for scrolling. The initial
        // selected row may already have a nonzero, idle scroll position.
        try{
          await page.waitForFunction(previous=>document.querySelector('#wheel').scrollTop>previous,before.scroll);
          await page.waitForFunction(()=>window.__gallery.settler.state==='idle');
        }finally{row.native.after=await snapshot();}
        const after=row.native.after;
        assert(after.scroll>before.scroll);assert.equal(after.selected,before.selected,'Browsing alone cannot change the inspected model');assert.equal(after.pageScroll,before.pageScroll);
        for(const key of ['header','catalog','workspace'])for(const field of ['x','y','width','height'])assert(Math.abs(before[key][field]-after[key][field])<.6,'Native wheel scrolling does not move the surrounding layout');
        const center=await page.evaluate(()=>window.__gallery.state.center);await page.locator(`#slots [data-id="${center}"]`).click();await ready(page,center);await page.goBack();await ready(page,before.selected);assert(Math.abs((await snapshot()).scroll-after.scroll)<1);
        await page.setViewportSize({width:1100,height:760});await page.waitForTimeout(150);assert.equal(await page.evaluate(()=>window.__gallery.state.selected),before.selected);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
      });
      await test('touch-wheel-scroll-and-orientation',async({page,context})=>{
        const box=await page.locator('#wheel').boundingBox(),session=await context.newCDPSession(page);const x=box.x+box.width*.5,y=box.y+box.height*.7;
        await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y}]});for(let i=1;i<=8;i++){await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x,y:y-i*28}]});await page.waitForTimeout(15);}await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
        await page.waitForFunction(()=>document.querySelector('#wheel').scrollTop>40);assert.equal(await page.locator('.workspace').isVisible(),false);await page.setViewportSize({width:844,height:390});await page.waitForTimeout(150);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
      },{mobile:true,path:'models/'});
    }
    if(has('resources')){
      await test('bounded-real-model-cache-warm-reuse-and-idle',async({page,row,glbs})=>{
        const selected=assets.slice(0,10);for(const asset of selected)await page.evaluate(id=>window.__gallery.choose(id),asset.id);await ready(page,selected.at(-1).id);
        const before=glbs.length;await page.evaluate(id=>window.__gallery.choose(id),selected.at(-1).id);await ready(page,selected.at(-1).id);assert.equal(glbs.length,before,'Warm selection reuses already loaded GLB bytes');
        await page.mouse.move(1400,20);await page.waitForTimeout(200);const frames=await page.evaluate(()=>window.__gallery.renderer.stats.frames);await page.waitForTimeout(250);assert.equal(await page.evaluate(()=>window.__gallery.renderer.stats.frames),frames,'Idle inspection has no perpetual animation loop');
        const stats=await page.evaluate(()=>({...window.__gallery.renderer.stats}));assert(stats.cacheEntries<=3&&stats.estimatedCacheBytes<=stats.cacheByteLimit);assert.equal(stats.rendererCount,1);row.stats=stats;
      });
      await test('hover-premultiplied-alpha-and-exit-cleanup',async({page,row})=>{
        await search(page,initial.id);const slot=page.locator(`#slots [data-id="${initial.id}"]`);await page.mouse.move(1400,20);
        await page.evaluate(()=>{window.__alphaSamples=[];window.__alphaRunning=true;const sample=()=>{const h=document.querySelector('.slot-image'),p=h?.__hoverPresentation;if(p?.hasFrame&&p.mix>0&&p.mix<1){const {width,height}=p.canvas,base=document.createElement('canvas');base.width=width;base.height=height;const c=base.getContext('2d');c.drawImage(p.poster,0,0,width,height);const a=c.getImageData(0,0,width,height).data,b=p.frame.getContext('2d').getImageData(0,0,width,height).data,actual=p.canvas.getContext('2d').getImageData(0,0,width,height).data;let error=0,count=0;for(let i=3;i<a.length;i+=68){error+=Math.abs(actual[i]-Math.min(255,a[i]*(1-p.mix)+b[i]*p.mix));count++;}window.__alphaSamples.push({mix:p.mix,error:error/count});}if(window.__alphaRunning)requestAnimationFrame(sample);};requestAnimationFrame(sample);});
        await slot.locator('.slot-image').hover();await page.waitForFunction(()=>window.__alphaSamples.length>0);await page.waitForFunction(()=>document.querySelector('.slot-image').__hoverPresentation?.mix===1);row.samples=await page.evaluate(()=>{window.__alphaRunning=false;return window.__alphaSamples;});assert(row.samples.every(s=>s.error<=2),'The hover handoff preserves premultiplied silhouette alpha');
        await page.mouse.move(1400,20);await page.waitForFunction(()=>!document.querySelector('.hover-surface'));assert.equal(await slot.locator('img').evaluate(img=>Number(getComputedStyle(img).opacity)),1);assert.equal(await page.evaluate(()=>window.__gallery.renderer.stats.hoverId),null);
      });
    }
    if(has('modal')){
      await test('home-modal-keyboard-history-and-cleanup',async({page})=>{
        await page.goto(baseURL);await page.locator('#hero-inspect').waitFor();await page.locator('#hero-inspect').click();await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready');
        for(let i=0;i<3;i++){await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);assert.equal(await page.evaluate(()=>document.body.style.overflow),'');assert.equal(await page.locator('.stage-flight,.return-composite').count(),0);await page.goForward();await page.waitForFunction(()=>document.querySelector('#viewer-dialog').open&&document.querySelector('#canvas-host').dataset.modelState==='ready');}
        await page.locator('#close').focus();await page.keyboard.press('Shift+Tab');assert(await page.evaluate(()=>document.querySelector('#viewer-dialog').contains(document.activeElement)),'Tab focus stays within the open modal');await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);assert(await page.locator('#home-page').isVisible());
      });
    }
    if(has('detail')){
      await test('preserved-direct-detail-reload-and-close',async({page,row})=>{
        const url=new URL(`models/${initial.id}/`,baseURL).href;
        for(let i=0;i<2;i++){if(!i)await page.goto(url);else await page.reload();await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready',{},{timeout:45000});assert.equal(page.url(),url);assert(Number(await page.locator('#canvas-host').getAttribute('data-render-triangles'))>0);assert.equal(await page.locator('#asset-title').textContent(),initial.name.en);}
        await page.locator('#copy-attribution').click();await page.waitForFunction(()=>document.querySelector('#copy-attribution').dataset.copyState==='copied');assert((await page.evaluate(()=>navigator.clipboard.readText())).includes('CC BY 4.0'));
        await page.locator('#share').focus();await page.keyboard.press('Enter');await page.waitForFunction(()=>document.querySelector('#share').dataset.copyState==='copied');assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),url);
        await page.evaluate(()=>Object.defineProperty(navigator.clipboard,'writeText',{configurable:true,value:()=>Promise.reject(new Error('Test denial'))}));await page.locator('#copy-attribution').click();assert.match(await page.locator('#copy-attribution').textContent(),/Copy unavailable/);
        await page.locator('#close').click();await page.waitForFunction(()=>window.__gallery?.models.length>0,{},{timeout:45000});assert(new URL(page.url()).pathname.endsWith('/models/'));assert(await page.locator('#wheel').isVisible());row.detail=url;
      });
      await test('preserved-home-about-and-modal-return',async({page})=>{
        await page.goto(baseURL);await page.locator('#home-page').waitFor({state:'visible'});await page.locator('[data-route="about"]').first().click();await page.locator('#about-page').waitFor({state:'visible'});assert(new URL(page.url()).pathname.endsWith('/about/'));
        await page.locator('[data-route="home"]').first().click();await page.locator('#hero-inspect').click();await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready',{},{timeout:45000});
        await page.locator('#close').click();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);assert(await page.locator('#home-page').isVisible());
        await page.locator('#home-query').fill(last.id);await page.locator('#home-search').evaluate(form=>form.requestSubmit());await page.waitForFunction(()=>window.__gallery?.models.length>0,{},{timeout:45000});assert.equal(await page.locator('#search').inputValue(),last.id);assert((await page.evaluate(()=>window.__gallery.state.results.map(a=>a.id))).includes(last.id));
      });
    }
    assert(report.cases.length>0,'At least one real-browser case must run');
    assert.deepEqual(report.errors,[],'No unexpected runtime errors');
    assert(report.cases.every(row=>row.status==='pass'),JSON.stringify(report.cases.filter(row=>row.status!=='pass'),null,2));report.status='pass';
  }catch(error){report.status='fail';report.error=error.stack;throw error;}
  finally{await browser?.close();if(server?.listening)await new Promise(done=>server.close(done));await writeFile(resolve(output,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({status:report.status,cases:report.cases.map(({name,status})=>({name,status})),output},null,2));}
  return report;
}
if(process.argv[1]&&fileURLToPath(import.meta.url)===resolve(process.argv[1]))await runGalleryBrowserTests();

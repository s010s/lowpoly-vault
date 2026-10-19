import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { resolve, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { createCatalog } from './catalog-build.mjs';
const prefix='/lowpoly-vault/',root=resolve(process.env.GALLERY_DIR||'dist');
const manifest=JSON.parse(await readFile(resolve(root,'assets/manifest.json'),'utf8'));
const report={status:'running',commit:process.env.GITHUB_SHA||null,review_only:!!manifest.review_only,build_directory:root,visual_approval:'pending_human_inspection',models:[],checks:[],page_errors:[],resource_errors:[]};
if(process.env.QA_REVIEW_ONLY==='1')assert(manifest.review_only,'CI review must be visibly marked review_only');
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.webp':'image/webp','.glb':'model/gltf-binary'};
const server=createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');if(!url.pathname.startsWith(prefix)){res.writeHead(404);res.end();return;}const p=resolve(root,decodeURIComponent(url.pathname.slice(prefix.length))||'index.html');if(!p.startsWith(root+'/'))throw new Error('Invalid path');const data=await readFile(p);res.writeHead(200,{'Content-Type':mime[extname(p)]||'application/octet-stream'});res.end(data);}catch{res.writeHead(404);res.end();}});
await mkdir('qa/screenshots',{recursive:true});
let browser,page,intentionalFailure=false;

// Homepage navigation has isolated storage and history. The catalog and GPU
// checks below always enter #catalog, where their controls are visible.
async function checkHomepage(browser,url){
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 const homePage=await context.newPage();
 homePage.on('pageerror',e=>report.page_errors.push(`Homepage: ${e.message}`));
 homePage.on('response',r=>{if(r.status()>=400)report.resource_errors.push(`Homepage: ${r.status()} ${r.url()}`);});
 const waitForPage=async route=>{
  await homePage.waitForURL(current=>current.hash===(route==='home'?'':`#${route}`));
  const selectors={home:'#home-page',catalog:'#collection',about:'#about-page'};
  await homePage.locator(selectors[route]).waitFor({state:'visible'});
  for(const [name,selector] of Object.entries(selectors))if(name!==route)assert.equal(await homePage.locator(selector).isVisible(),false,`${name} must be hidden on ${route}`);
 };
 const waitForCatalog=async()=>{
  await waitForPage('catalog');
  await homePage.waitForFunction(()=>document.querySelector('#grid').getAttribute('aria-busy')==='false');
  await homePage.locator('#collection .asset-card').first().waitFor({timeout:30000});
 };
 try{
  await homePage.goto(url);await waitForPage('home');
  await homePage.waitForFunction(()=>document.querySelector('#grid').getAttribute('aria-busy')==='false'&&document.querySelectorAll('#collection .asset-card').length>0,null,{timeout:30000});
  assert.equal(await homePage.locator('canvas').count(),0,'The homepage must not create a live model renderer');
  const hero=homePage.locator('#home-page img[src$="home/editorial-hero.webp"]');
  await hero.waitFor({state:'visible'});
  await hero.evaluate(img=>img.decode());
  assert(await hero.evaluate(img=>img.naturalWidth>0),'The editorial homepage hero must load');
  await homePage.screenshot({path:'qa/screenshots/home-desktop.png',fullPage:true});
  await homePage.setViewportSize({width:390,height:844});
  assert(await homePage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'The homepage must fit a mobile viewport');
  await homePage.screenshot({path:'qa/screenshots/home-mobile.png',fullPage:true});
  await homePage.setViewportSize({width:1440,height:1000});
  const heroAssetID=await homePage.locator('#hero-inspect').getAttribute('data-home-asset');
  assert(heroAssetID&&manifest.assets.some(asset=>asset.id===heroAssetID),'The homepage inspection link must reference an actual asset');
  await homePage.locator('#hero-inspect').click();
  await homePage.waitForURL(current=>current.hash===`#asset=${encodeURIComponent(heroAssetID)}`);
  await homePage.waitForFunction(()=>document.querySelector('#canvas-host').dataset.modelState==='ready',null,{timeout:30000});
  await homePage.goBack();await homePage.locator('#viewer-dialog').waitFor({state:'hidden'});await waitForPage('home');
  assert.equal(await homePage.locator('canvas').count(),0,'Back from a homepage asset must release the live renderer');
  await homePage.locator('#home-page [data-browse]').first().click();await waitForCatalog();
  assert.equal(await homePage.locator('#collection .asset-card').count(),Math.min(24,manifest.assets.length));
  await homePage.locator('.primary-nav [data-route="home"]').click();await waitForPage('home');
  await homePage.goBack();await waitForCatalog();
  report.checks.push('default route is independent homepage','homepage editorial hero loads','homepage mobile layout without horizontal overflow','browse opens catalog and browser Back restores catalog','detail Back preserves homepage source');

  await homePage.locator('.primary-nav [data-route="about"]').click();await waitForPage('about');
  await homePage.reload();await waitForPage('about');
  await homePage.locator('.primary-nav [data-route="home"]').click();await waitForPage('home');
  const query=typeof manifest.assets[0].name==='object'?manifest.assets[0].name.en:manifest.assets[0].name;
  await homePage.locator('#home-query').fill(query);
  await homePage.locator('#home-query').press('Enter');await waitForCatalog();
  assert.equal(await homePage.locator('#search').inputValue(),query,'Homepage search must carry the query into the catalog');
  const matchingIDs=await homePage.locator('#collection .asset-card').evaluateAll(cards=>cards.map(card=>card.dataset.id));
  assert(matchingIDs.includes(manifest.assets[0].id),'Homepage search must find its matching asset');
  await homePage.locator('.primary-nav [data-route="home"]').click();await waitForPage('home');
  await homePage.locator('[data-home-category="geology"]').click();await waitForCatalog();
  assert.equal(await homePage.locator('[data-category="geology"]').getAttribute('aria-pressed'),'true');
  assert.equal(await homePage.locator('#search').inputValue(),'','A homepage category must clear the previous search');
  const geologyIDs=new Set(manifest.assets.filter(asset=>asset.category==='geology').map(asset=>asset.id));
  const filteredIDs=await homePage.locator('#collection .asset-card').evaluateAll(cards=>cards.map(card=>card.dataset.id));
  assert(filteredIDs.length>0&&filteredIDs.every(id=>geologyIDs.has(id)),'Homepage geology link must show only geology assets');
  const selectedID=filteredIDs[0];
  await homePage.locator('#collection .asset-card').first().click();
  await homePage.waitForURL(current=>current.hash===`#asset=${encodeURIComponent(selectedID)}`);
  await homePage.waitForFunction(()=>document.querySelector('#canvas-host').dataset.modelState==='ready',null,{timeout:30000});
  await homePage.goBack();await homePage.locator('#viewer-dialog').waitFor({state:'hidden'});await waitForCatalog();
  assert.equal(await homePage.locator('[data-category="geology"]').getAttribute('aria-pressed'),'true','Back from details must preserve the catalog filter');
  assert.deepEqual(await homePage.locator('#collection .asset-card').evaluateAll(cards=>cards.map(card=>card.dataset.id)),filteredIDs,'Back from details must preserve the source catalog results');
  report.checks.push('about route survives reload','homepage search opens populated catalog','homepage category opens filtered catalog','detail Back preserves catalog source and filters');

  // A fresh document with a share URL has no in-session source page to return to.
  const deepLinkPage=await context.newPage();
  deepLinkPage.on('pageerror',e=>report.page_errors.push(`Deep link: ${e.message}`));
  deepLinkPage.on('response',r=>{if(r.status()>=400)report.resource_errors.push(`Deep link: ${r.status()} ${r.url()}`);});
  await deepLinkPage.goto(`${url}#asset=${encodeURIComponent(manifest.assets[0].id)}`);
  await deepLinkPage.waitForFunction(()=>document.querySelector('#canvas-host').dataset.modelState==='ready',null,{timeout:30000});
  assert(await deepLinkPage.locator('#viewer-dialog').isVisible());
  await deepLinkPage.locator('#close').click();
  await deepLinkPage.locator('#viewer-dialog').waitFor({state:'hidden'});
  await deepLinkPage.waitForURL(current=>current.hash==='#catalog');
  assert(await deepLinkPage.locator('#collection').isVisible(),'Closing a direct asset link must fall back to the catalog');
  assert.equal(await deepLinkPage.locator('#home-page').isVisible(),false);
  assert.equal(await deepLinkPage.locator('canvas').count(),0);
  report.homepage={status:'pass',defaultRoute:'home',catalogRoute:'#catalog',aboutRoute:'#about',searchTransferred:true,categoryFilter:'geology',detailBackSources:['home','catalog'],detailFallback:'#catalog',mobileOverflow:false};
  report.checks.push('direct asset link opens model and closes to catalog fallback');
 }catch(error){
  try{await homePage.screenshot({path:'qa/screenshots/home-failure.png',fullPage:true});}catch{}
  throw error;
 }finally{await context.close();}
}

// Theme QA uses its own storage and media settings so it cannot change the
// language, reduced-motion, or asset-routing assumptions of the gallery checks.
async function checkThemes(browser,url){
 const context=await browser.newContext({viewport:{width:1440,height:1000},colorScheme:'dark',reducedMotion:'reduce'});
 const themePage=await context.newPage();
 themePage.on('pageerror',e=>report.page_errors.push(`Theme: ${e.message}`));
 themePage.on('response',r=>{if(r.status()>=400)report.resource_errors.push(`Theme: ${r.status()} ${r.url()}`);});
 await themePage.addInitScript(()=>{
  // Observe the browser's real animations; do not stub out the transition API.
  const audit=window.__themeQA={animations:[],activeTransitions:0,startedTransitions:0,finishedTransitions:0};
  const animate=Element.prototype.animate;
  Element.prototype.animate=function(frames,options){
   const animation=animate.call(this,frames,options);
   if(this===document.documentElement){
    const entry={frames:animation.effect.getKeyframes(),duration:animation.effect.getTiming().duration,pseudoElement:animation.effect.pseudoElement||null,settled:false};
    audit.animations.push(entry);
    animation.finished.then(()=>{entry.settled=true;},()=>{entry.settled=true;});
   }
   return animation;
  };
  if(typeof document.startViewTransition==='function'){
   const start=document.startViewTransition.bind(document);
   document.startViewTransition=(...args)=>{
    const transition=start(...args);
    audit.startedTransitions++;audit.activeTransitions++;
    const settled=()=>{audit.activeTransitions--;audit.finishedTransitions++;};
    transition.finished.then(settled,settled);
    return transition;
   };
  }
 });
 const waitForTheme=async expected=>{
  await themePage.waitForFunction(value=>{
   const audit=window.__themeQA;
   return document.documentElement.dataset.theme===value&&audit.activeTransitions===0&&audit.animations.every(a=>a.settled)&&
    !document.getAnimations().some(a=>a.effect?.pseudoElement?.startsWith('::view-transition')&&(a.playState==='running'||a.pending));
  },expected,{timeout:10000});
  const state=await themePage.evaluate(()=>({theme:document.documentElement.dataset.theme,colorScheme:document.documentElement.style.colorScheme,buttons:[...document.querySelectorAll('[data-theme-toggle]')].map(b=>({pressed:b.getAttribute('aria-pressed'),label:b.getAttribute('aria-label')}))}));
  assert.equal(state.theme,expected);assert.equal(state.colorScheme,expected);
  assert.equal(state.buttons.length,2,'Both gallery and modal must expose a theme button');
  for(const button of state.buttons){assert.equal(button.pressed,String(expected==='dark'));assert.equal(button.label,`Switch to ${expected==='dark'?'light':'dark'} theme`);}
 };
 const readGPU=()=>themePage.evaluate(()=>({...window.__vaultGPU}));
 const assertSameScene=(before,after)=>{
  for(const key of ['rendererCreations','renderers','rendererCount','liveScenes','disposedScenes','activeMode','activeURL'])assert.equal(after[key],before[key],`Theme switching changed GPU ${key}`);
  assert.equal(after.liveScenes,1);assert.equal(after.activeMode,'detail');assert.equal(after.activeRequests,0);
 };
 try{
  await themePage.goto(`${url}#catalog`);await themePage.locator('.asset-card').first().waitFor({timeout:30000});
  await waitForTheme('dark');
  assert.equal(await themePage.evaluate(()=>localStorage.length),0,'A fresh context must start with clean localStorage');
  await themePage.emulateMedia({colorScheme:'light'});await waitForTheme('light');
  assert.equal(await themePage.evaluate(()=>localStorage.getItem('vault-theme')),null,'Following the OS must not save an explicit preference');
  await themePage.reload();await themePage.locator('.asset-card').first().waitFor({timeout:30000});
  await waitForTheme('light');assert.equal(await themePage.evaluate(()=>localStorage.length),0);
  report.checks.push('clean-storage initial dark and light OS themes','OS changes followed before explicit selection');

  const headerToggle=themePage.locator('.topbar [data-theme-toggle]');
  const lightBackground=await themePage.locator('html').evaluate(el=>getComputedStyle(el).backgroundColor);
  await themePage.emulateMedia({reducedMotion:'no-preference'});
  await headerToggle.click();await waitForTheme('dark');
  const darkBackground=await themePage.locator('html').evaluate(el=>getComputedStyle(el).backgroundColor);
  assert.notEqual(darkBackground,lightBackground,'The theme button must change rendered UI colors');
  const normalAnimations=await themePage.evaluate(()=>window.__themeQA.animations);
  assert(normalAnimations.length>0,'Normal theme switching must animate');
  const nativeTransition=await themePage.evaluate(()=>typeof document.startViewTransition==='function');
  if(nativeTransition)assert(normalAnimations.some(a=>a.frames.some(f=>f.clipPath?.startsWith('circle('))),'Normal motion must exercise the circular reveal');
  await themePage.screenshot({path:'qa/screenshots/theme-dark.png',fullPage:true});
  await headerToggle.click();await waitForTheme('light');
  await themePage.screenshot({path:'qa/screenshots/theme-light.png',fullPage:true});
  assert.equal(await themePage.evaluate(()=>localStorage.getItem('vault-theme')),'light');
  // An explicit choice must win over the opposite OS scheme after navigation.
  await themePage.emulateMedia({colorScheme:'dark'});await themePage.reload();
  await themePage.locator('.asset-card').first().waitFor({timeout:30000});await waitForTheme('light');
  assert.equal(await themePage.evaluate(()=>matchMedia('(prefers-color-scheme: dark)').matches),true);
  assert.equal(await themePage.evaluate(()=>localStorage.getItem('vault-theme')),'light');
  report.checks.push('dark/light buttons and accessible state','theme preference survives reload and overrides OS');

  await themePage.emulateMedia({reducedMotion:'reduce'});
  await themePage.locator('.asset-card').first().click();
  await themePage.waitForFunction(()=>document.querySelector('#canvas-host').dataset.modelState==='ready',null,{timeout:30000});
  await themePage.locator('#wireframe').click();
  await themePage.locator('#canvas-host').focus();await themePage.keyboard.press('ArrowRight');await themePage.keyboard.press('+');
  await themePage.waitForFunction(()=>window.__vaultGPU.rafPending===0&&Number(document.querySelector('#canvas-host').dataset.renderLines)>0);
  const canvas=await themePage.locator('#canvas-host canvas').elementHandle();
  const diagnostics=await themePage.evaluateHandle(()=>window.__vaultGPU);
  const modalToggle=themePage.locator('#viewer-dialog [data-theme-toggle]');
  for(const [motion,nextTheme] of [['reduce','dark'],['no-preference','light']]){
   await themePage.emulateMedia({reducedMotion:motion});await themePage.waitForFunction(()=>window.__vaultGPU.rafPending===0);
   const before=await readGPU(),pixels=await canvas.screenshot();
   const animationStart=await themePage.evaluate(()=>window.__themeQA.animations.length);
   await modalToggle.click();await waitForTheme(nextTheme);
   assert.equal(await canvas.evaluate(node=>node===document.querySelector('#canvas-host canvas')),true,'Theme switch replaced the live canvas');
   assert.equal(await diagnostics.evaluate(stats=>stats===window.__vaultGPU),true,'Theme switch replaced the renderer diagnostics');
   assertSameScene(before,await readGPU());
   assert.equal(await themePage.locator('#canvas-host canvas').count(),1);
   assert.equal(await themePage.locator('#wireframe').getAttribute('aria-pressed'),'true');
   assert.deepEqual(await canvas.screenshot(),pixels,'Theme switch changed the rotated, zoomed, wireframe model');
   if(motion==='reduce'){
    const animations=await themePage.evaluate(start=>window.__themeQA.animations.slice(start),animationStart);
    assert(animations.length>0,'Reduced-motion switch must exercise its short fade');
    assert(animations.every(a=>a.duration<=150),'Reduced-motion transition must stay brief');
    assert(animations.every(a=>a.frames.every(f=>(!f.clipPath||f.clipPath==='none')&&(!f.transform||f.transform==='none'))),'Reduced motion must not use a large clip or transform animation');
   }
  }
  report.checks.push('modal theme keeps identical canvas and GPU scene','theme preserves model orbit zoom and wireframe pixels','reduced-motion short fade without circular clip');

  const beforeRapid=await readGPU(),rapidPixels=await canvas.screenshot();
  const rapidStart=await themePage.evaluate(()=>window.__themeQA.animations.length);
  await modalToggle.click();
  await themePage.waitForFunction(start=>window.__themeQA.animations.slice(start).some(a=>!a.settled),rapidStart);
  // Dispatch a burst within one task while the first real transition is active.
  // Waiting for Playwright actionability between clicks would serialize it.
  await modalToggle.evaluate(button=>{for(let i=0;i<6;i++)button.click();});
  await waitForTheme('dark');
  assert.equal(await themePage.evaluate(()=>localStorage.getItem('vault-theme')),'dark','Seven toggles must settle on the latest requested theme');
  const audit=await themePage.evaluate(()=>window.__themeQA);
  assert.equal(audit.activeTransitions,0);assert.equal(audit.startedTransitions,audit.finishedTransitions,'No view-transition overlay may be left active');
  assert.equal(await canvas.evaluate(node=>node===document.querySelector('#canvas-host canvas')),true);
  assertSameScene(beforeRapid,await readGPU());assert.deepEqual(await canvas.screenshot(),rapidPixels);
  // Real pointer clicks still reach the modal after the interrupted transitions.
  await modalToggle.click();await waitForTheme('light');
  await themePage.locator('#close').click();await themePage.locator('#viewer-dialog').waitFor({state:'hidden'});
  assert.equal(await themePage.locator('.stage-flight').count(),0);
  assert.equal(await themePage.locator('canvas').count(),0);
  assert.equal((await readGPU()).liveScenes,0);
  report.theme={status:'pass',nativeViewTransition:nativeTransition,initialSchemes:['dark','light'],persistedPreference:'light',rapidClicks:7,modalCanvasPreserved:true,modelPixelsPreserved:true,activeTransitionsAfterRapid:audit.activeTransitions};
  report.checks.push('rapid theme clicks settle latest choice with no overlay','modal remains clickable after interrupted theme transitions');
 }catch(error){
  try{await themePage.screenshot({path:'qa/screenshots/theme-failure.png',fullPage:true});}catch{}
  throw error;
 }finally{await context.close();}
}

try{
 if(existsSync(resolve(root,'gallery/resources.json'))){
  // The public command remains full acceptance, even when CI scope variables
  // are present. Real documents and every asset run in strict GPU mode first;
  // the remaining wheel groups exercise the replacement interaction contract.
  const output=resolve(process.env.QA_OUTPUT_DIR||'qa/browser-approved-gallery');
  const documentOutput=resolve(output,'documents-and-models');
  const result=spawnSync(process.execPath,[fileURLToPath(new URL('./redesign-browser-test.mjs',import.meta.url))],{
   stdio:'inherit',env:{...process.env,GALLERY_DIR:root,QA_OUTPUT_DIR:documentOutput,QA_BASE_URL:'',QA_REVIEW_SCOPE:'full',QA_MODEL_IDS:'',QA_STATIC_ONLY:'0',QA_ALLOW_WEBGL_FALLBACK:'0',QA_FORCE_WEBGL_FALLBACK:'0'}
  });
  if(result.error)throw result.error;
  assert.equal(result.status,0,'Full document, all-model GPU and wheel matrix acceptance must pass');
  const documents=JSON.parse(await readFile(resolve(documentOutput,'report.json'),'utf8'));
  assert.equal(documents.status,'pass');assert.equal(documents.browser_status,'pass');assert.equal(documents.gpu.status,'pass');
  assert.deepEqual(documents.models.map(model=>model.id),manifest.assets.map(asset=>asset.id),'Every delivered model must receive real browser acceptance');
  assert(documents.models.every(model=>model.status==='gpu-pass'),'Fallback cannot count as a model rendering pass');
  const {runGalleryBrowserTests}=await import('./gallery-browser-test.mjs');
  const wheel=await runGalleryBrowserTests({groups:['handoff','resources','detail'],root,output:resolve(output,'wheel-handoff-resources-detail'),baseURL:null});
  assert.equal(wheel.status,'pass');
  report.models=documents.models;report.chromium_version=documents.chromium_version;
  report.checks=[...documents.checks,...wheel.cases.map(test=>test.name)];
  report.evidence={documents_and_models:resolve(documentOutput,'report.json'),wheel_handoff_resources_detail:resolve(output,'wheel-handoff-resources-detail/report.json')};
  report.design_contract='Approved wheel: full bilingual static/no-JS documents, every real model and download, preserved detail theme/wireframe/metric controls, home/modal/history, virtualized search/filter/mobile, native scroll, supersession, hover, bounded renderer resources and explicit fallback. Retired hash/grid/card geometry and list-theme assumptions are not reported as measured.';
  report.status='pass';console.log(`Browser QA passed: ${report.models.length} real GLBs, preserved documents and approved wheel acceptance. Screenshots require human review; no asset QA state was changed.`);
 }else{
 await new Promise((r,j)=>{server.once('error',j);server.listen(0,'127.0.0.1',r);});
 const url=`http://127.0.0.1:${server.address().port}${prefix}?browse=grid`;
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 report.chromium_version=browser.version();
 await checkHomepage(browser,url);
 await checkThemes(browser,url);
 page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 page.on('pageerror',e=>report.page_errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!intentionalFailure)report.resource_errors.push(`${r.status()} ${r.url()}`);});
 await page.goto(`${url}#catalog`);await page.locator('.asset-card').first().waitFor({timeout:30000});
 const count=await page.locator('.asset-card').count();assert.equal(count,Math.min(24,manifest.assets.length));if(process.env.QA_REQUIRE_COUNT)assert.equal(count,Number(process.env.QA_REQUIRE_COUNT));
 if(manifest.review_only)assert(await page.locator('.review-notice').isVisible());
 await page.locator('#collection img').evaluateAll(imgs=>Promise.all(imgs.map(img=>img.decode())));await page.screenshot({path:'qa/screenshots/gallery-desktop.png',fullPage:true});
 assert(await page.locator('html').getAttribute('lang')==='en');await page.locator('[data-category="plants"]').click();await page.waitForFunction(()=>document.querySelector('#grid').getAttribute('aria-busy')==='false');assert(await page.locator('.asset-card').count()>0);assert(await page.locator('.asset-card').count()<count);await page.locator('[data-category="all"]').click();await page.waitForFunction(()=>document.querySelector('#grid').getAttribute('aria-busy')==='false');if(!await page.locator('#search').isVisible())await page.locator('#search-trigger').click();await page.locator('#search').fill('THIS_DOES_NOT_EXIST');await page.waitForFunction(()=>document.querySelectorAll('.asset-card').length===0);assert(await page.locator('.asset-card').count()===0);if(!await page.locator('#search').isVisible())await page.locator('#search-trigger').click();await page.locator('#search').fill('');await page.waitForFunction(()=>document.querySelectorAll('.asset-card').length>0);assert(await page.locator('.asset-card').count()===count);report.checks.push('category filters','search and empty result','desktop previews','project subpath');
 for(let i=0;i<count;i++){
  const a=manifest.assets[i];await page.locator(`.asset-card[data-id="${a.id}"]`).click();await page.waitForFunction(()=>document.querySelector('#viewer-status').textContent==='',null,{timeout:30000});assert(await page.locator('#canvas-host canvas').count()===1);assert(Number(await page.locator('#canvas-host').getAttribute('data-render-triangles'))>0,'WebGL must draw real triangles');assert(await page.locator('#downloads a').count()===2);
  for(const link of await page.locator('#downloads a').all()){const href=await link.getAttribute('href'),response=await page.request.get(href);assert(response.ok(),`Download failed: ${href}`);assert((await response.body()).length>0);}
  await page.screenshot({path:`qa/screenshots/model-${a.id}.png`});
  await page.locator('#wireframe').click();assert(await page.locator('#wireframe').getAttribute('aria-pressed')==='true');assert(Number(await page.locator('#canvas-host').getAttribute('data-render-lines'))>0,'Wireframe must draw real lines');await page.screenshot({path:`qa/screenshots/wireframe-${a.id}.png`});
  await page.locator('#canvas-host').focus();await page.keyboard.press('ArrowRight');await page.keyboard.press('+');await page.locator('#zoom-out').click();await page.locator('#reset').click();await page.locator('#wireframe').click();
  report.models.push({id:a.id,glb_sha256:a.sha256?.glb||null,status:'pass',checks:['GLTFLoader loaded in browser','WebGL canvas rendered','wireframe toggle','keyboard rotation and zoom','reset and zoom buttons','GLB and Blend downloads'],screenshots:[`model-${a.id}.png`,`wireframe-${a.id}.png`]});await page.keyboard.press('Escape');await page.locator('#viewer-dialog').waitFor({state:'hidden'});assert.equal(await page.evaluate(()=>window.__vaultGPU.liveScenes),0);assert.equal(await page.locator('canvas').count(),0);
 }
 await page.locator('#language').click();assert(await page.locator('html').getAttribute('lang')==='zh-CN');assert((await page.locator('#collection-title').textContent()).includes('脑洞'));await page.screenshot({path:'qa/screenshots/gallery-chinese.png',fullPage:true});await page.setViewportSize({width:390,height:844});await page.screenshot({path:'qa/screenshots/gallery-mobile.png',fullPage:true});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.locator('.asset-card').first().click();await page.waitForFunction(()=>document.querySelector('#viewer-status').textContent==='',null,{timeout:30000});await page.screenshot({path:'qa/screenshots/viewer-mobile.png',fullPage:true});assert(await page.locator('#viewer-dialog').evaluate(el=>el.scrollWidth<=el.clientWidth));await page.keyboard.press('Escape');await page.locator('#viewer-dialog').waitFor({state:'hidden'});report.checks.push('bilingual UI','mobile layout without horizontal overflow','mobile viewer','Escape closes dialog');

 // A shareable detail route restores on reload; in-session filter preservation is covered above.
 await page.setViewportSize({width:1440,height:1000});await page.locator('#language').click();
 await page.locator('[data-category="plants"]').click();await page.locator('.asset-card').first().click();
 await page.waitForFunction(()=>document.querySelector('#canvas-host').dataset.modelState==='ready');
 assert(page.url().includes('#asset='));await page.reload();await page.waitForFunction(()=>document.querySelector('#canvas-host').dataset.modelState==='ready');
 await page.locator('#close').click();await page.locator('#viewer-dialog').waitFor({state:'hidden'});
 // Hover changes actual model rotation; no card transform masquerades as 3D.
 await page.emulateMedia({reducedMotion:'no-preference'});
 await page.locator('.asset-card').first().hover();await page.waitForFunction(()=>document.querySelector('.asset-image[data-model-state="ready"]'));
 const hoverHost=page.locator('.asset-image[data-model-state="ready"]');assert(Number(await hoverHost.getAttribute('data-render-triangles'))>0);
 const before=await page.evaluate(()=>window.__vaultGPU.renderedFrames);
 const bounds=await hoverHost.boundingBox();await page.mouse.move(bounds.x+bounds.width*.85,bounds.y+bounds.height*.3);
 await page.waitForFunction(n=>window.__vaultGPU.renderedFrames>n,before);
 assert.equal(await page.locator('canvas').count(),1);await page.mouse.move(5,5);
 await page.waitForFunction(()=>window.__vaultGPU.liveScenes===0&&window.__vaultGPU.rafPending===0);
 report.checks.push('shared-element detail and hash refresh','one live hover renderer','real hover triangles','hover pointer redraw','scene release after close');
 // Test-only 10,000-entry metadata fixture. It never becomes a public asset manifest.
 const fixtureAssets=Array.from({length:10000},(_,i)=>({...manifest.assets[i%manifest.assets.length],id:`fixture-${String(i).padStart(5,'0')}`,name:{en:`Fixture ${String(i).padStart(5,'0')}`,zh:`测试资产 ${i}`}}));
 const fixture=createCatalog({...manifest,assets:fixtureAssets});
 await page.route('**/assets/catalog.json',r=>r.fulfill({contentType:'application/json',body:JSON.stringify(fixture.index)}));
 await page.route('**/assets/catalog/shards/*.json',r=>{const key='assets/'+new URL(r.request().url()).pathname.split('/assets/')[1];return r.fulfill({contentType:'application/json',body:JSON.stringify(fixture.shards.get(key))});});
 await page.route('**/assets/catalog/details/*.json',r=>{const id=new URL(r.request().url()).pathname.split('/').pop().replace('.json','');return r.fulfill({contentType:'application/json',body:JSON.stringify(fixtureAssets.find(a=>a.id===id))});});
 await page.goto(`${url}&qa=scale#catalog`);await page.waitForFunction(()=>document.querySelector('#count').textContent.includes('10,000'));
 const domCount=await page.locator('*').count();assert.equal(await page.locator('.asset-card').count(),24);assert(domCount<600,`DOM not bounded: ${domCount}`);
 await page.locator('#next-page').click();await page.waitForFunction(()=>document.querySelector('#page-number').textContent==='2 / 417');assert.equal(await page.locator('.asset-card').count(),24);
 if(!await page.locator('#search').isVisible())await page.locator('#search-trigger').click();await page.locator('#search').fill('Fixture 09999');await page.waitForFunction(()=>document.querySelectorAll('.asset-card').length===1);assert((await page.locator('.asset-card').textContent()).includes('09999'));
 if(!await page.locator('#search').isVisible())await page.locator('#search-trigger').click();await page.locator('#search').fill('');await page.waitForFunction(()=>document.querySelectorAll('.asset-card').length===24);
 for(let i=0;i<8;i++){await page.locator('.asset-card').nth(i).hover();await page.waitForTimeout(155);}
 await page.locator('.asset-card').nth(8).click();await page.waitForFunction(()=>document.querySelector('#canvas-host').dataset.modelState==='ready');
 const gpu=await page.evaluate(()=>({...window.__vaultGPU}));assert.equal(gpu.peakRequests,1);assert.equal(gpu.rendererCreations,1);assert.equal(gpu.liveScenes,1);assert(gpu.cacheEntries<=3);assert(gpu.cacheBytes<=24*1024*1024);assert.equal(await page.locator('canvas').count(),1);
 await page.locator('#close').click();await page.locator('#viewer-dialog').waitFor({state:'hidden'});assert.equal(await page.evaluate(()=>window.__vaultGPU.liveScenes),0);assert.equal(await page.locator('canvas').count(),0);
 report.scale={metadata:10000,cardNodes:24,totalDOMNodes:domCount,peakGLBRequests:gpu.peakRequests,rendererCreations:gpu.rendererCreations,cacheEntries:gpu.cacheEntries,cacheBytes:gpu.cacheBytes,closeLiveScenes:0};
 report.checks.push('10000 metadata fixture bounded DOM','distant shard search','417-page pagination','rapid hover abort and max-one GLB request','bounded byte cache','detail close frees all model scenes');
 await page.unroute('**/assets/catalog.json');await page.unroute('**/assets/catalog/shards/*.json');await page.unroute('**/assets/catalog/details/*.json');
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto(`${url}#catalog`);await page.locator('#language').click();
 intentionalFailure=true;await page.route('**/assets/catalog.json',r=>r.fulfill({status:503,body:'Unavailable'}));await page.reload();await page.waitForFunction(()=>document.querySelector('#grid').textContent.includes('暂时不可用'));assert(await page.locator('#collection').isVisible(),'Catalog load failure must remain visible on the catalog route');assert(await page.locator('#retry').isVisible(),'Catalog load failure must expose its retry control');assert(await page.locator('.asset-card').count()===0);report.checks.push('explicit manifest failure state');assert.deepEqual(report.page_errors,[]);assert.deepEqual(report.resource_errors,[]);report.status='pass';console.log(`Browser QA passed: ${count} real GLBs and gallery interactions. Screenshots require human review; no asset QA state was changed.`);
 }
}catch(error){report.status='fail';report.error=error.stack||error.message;try{await page?.screenshot({path:'qa/screenshots/failure.png',fullPage:true});}catch{}console.error(error);process.exitCode=1;}
finally{await writeFile('qa/browser-report.json',JSON.stringify(report,null,2)+'\n');await browser?.close();server.close();}

/** Detached actual-deployment checks. Writes only runtime evidence, never production records. */
import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {loadVerifiedRelease} from './ci-layered-release-scope.mjs';
import {waitForDeployedBuild} from './ci-deployment-contract.mjs';
import {createHash} from 'node:crypto';
import {waitForDeployedRelease} from './live-release-contract.mjs';
const out=resolve(process.env.QA_OUTPUT_DIR||'qa/post-release-runtime');
const report={status:'running',phase:'initialize',expected:{source_commit:process.env.DEPLOYED_SHA||null,run_id:process.env.UPSTREAM_RUN_ID||null,run_attempt:process.env.UPSTREAM_RUN_ATTEMPT||null},checks:{scope:'NOT_RUN',deployed_build:'NOT_RUN',browser:'NOT_RUN'},cases:[],static_routes:[],errors:[],resource_errors:[],entry_errors:[],loaded_entries:[],production_acceptance:false,reusable_browser_proof:false,limitations:['Actual public deployment origin in Chromium SwiftShader; emulated touch, no physical-device performance claim.']};
const hash=b=>createHash('sha256').update(b).digest('hex');
let browser;
try {
 await mkdir(out,{recursive:true});report.phase='receipt-scope-build-verification';
 const {context:deployment,scope,marker}=loadVerifiedRelease();report.checks.scope='PASS';
 const base=deployment.pageURL,expected=JSON.parse(await readFile('assets/manifest.json'));
 const ids=scope.affected_ids.length?scope.affected_ids:[expected.assets[0].id];
 Object.assign(report,{source_commit:scope.source_commit,base_commit:scope.base_commit,run_id:deployment.runId,run_attempt:deployment.runAttempt,origin:base,build_digest:marker.build_digest,affected_ids:scope.affected_ids,selected_ids:ids});
 report.phase='actual-deployed-build';report.deployed_build=await waitForDeployedBuild({baseURL:base,marker,markerSHA256:deployment.markerSHA256});report.checks.deployed_build='PASS';
 const deliveredEntries=new Map(marker.files.filter(f=>/\.(?:js|css|json)$/.test(f.path)).map(f=>[f.path,f])),entryChecks=[];
 // Pages/CDN caches may still return the previous release briefly. Only proceed on the exact expected payload set.
 const deployed=await waitForDeployedRelease(base+'assets/manifest.json?release='+report.source_commit,expected);
 report.deployed_payload_scope='exact-match';
 const limited=expected.assets.filter(a=>Object.hasOwn(a.approval_provenance||{},'hardware_gpu_verified'));
 for(const asset of limited){const actual=deployed.assets.find(a=>a.id===asset.id);assert.deepEqual(actual.approval_provenance,asset.approval_provenance,asset.id+': public approval/hardware limitations must remain intact');}
 report.preserved_hardware_limitations=limited.map(a=>({id:a.id,formal_profile_acceptance:a.approval_provenance.formal_profile_acceptance,hardware_gpu_verified:a.approval_provenance.hardware_gpu_verified}));
 report.phase='browser-launch';const {chromium}=await import('playwright');browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});report.browser=browser.version();
 report.phase='actual-browser-checks';
 for(const mobile of [false,true]) {
  const lang=mobile?'zh-CN/':'',context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},hasTouch:mobile,isMobile:mobile,reducedMotion:'reduce'});
  await context.grantPermissions(['clipboard-read','clipboard-write'],{origin:new URL(base).origin});
  const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));page.on('response',r=>{if(r.status()>=400)report.resource_errors.push(`${r.status()} ${r.url()}`);});
  page.on('response',response=>{const url=new URL(response.url()),origin=new URL(base);if(url.origin!==origin.origin||!url.pathname.startsWith(origin.pathname)||!/\.(?:js|css|json)$/.test(url.pathname))return;const path=decodeURIComponent(url.pathname.slice(origin.pathname.length));entryChecks.push((async()=>{const pin=deliveredEntries.get(path);assert(pin,'Unexpected runtime entry: '+path);const bytes=await response.body();assert.equal(bytes.length,pin.bytes,'Loaded entry size differs: '+path);assert.equal(hash(bytes),pin.sha256,'Loaded entry hash differs: '+path);report.loaded_entries.push(path);})().catch(error=>{report.entry_errors.push(error.message);}));});
  try {
   const catalog=base+lang+'models/';
   await page.goto(catalog);await page.waitForFunction(()=>window.__gallery?.models.length>0);
   assert.deepEqual((await page.evaluate(()=>window.__gallery.state.results.map(asset=>asset.id))).sort(),expected.assets.map(a=>a.id).sort());
   assert.equal(await page.evaluate(()=>window.__gallery.models.length),expected.assets.length,'Every published model is present, not only the prototype subset');
   assert(await page.locator('#wheel').evaluate(el=>['auto','scroll'].includes(getComputedStyle(el).overflowY)),'The approved wheel retains native scrolling');
   assert.equal(await page.locator('#grid').count(),0,'The retired grid is not mounted behind the approved gallery');
   for(const id of ids) {
    const asset=expected.assets.find(a=>a.id===id),card=page.locator(`#slots [data-id="${id}"]`);
    await page.locator('#wheel').evaluate((wheel,id)=>{wheel.scrollTop=window.__gallery.state.results.findIndex(asset=>asset.id===id)*128;},id);
    await card.waitFor({state:'visible'});
    await page.waitForFunction(id=>{const image=document.querySelector(`#slots [data-id="${id}"] img`);return image?.dataset.thumbnailState==='ready'&&image.complete&&image.naturalWidth>0;},id);
    await card.locator('img').evaluate(img=>img.decode());assert(await card.locator('img').evaluate(img=>img.naturalWidth>0));
    assert.equal(await card.getAttribute('aria-label'),asset.name[mobile?'zh':'en']);
    const before=await page.locator('html').evaluate(el=>({x:el.getBoundingClientRect().x,width:el.getBoundingClientRect().width}));
    await card.click();
    if(mobile){assert.equal(await page.locator('#detail').getAttribute('data-state'),'static','Touch detail remains poster-first until explicit interaction');await page.locator('#mobile-interact').tap();}
    await page.waitForFunction(id=>document.querySelector('#detail')?.dataset.state==='ready'&&window.__gallery.renderer.stats.detailFirstFrameId===id,id);
    assert(await page.evaluate(()=>!!window.__gallery.renderer.detail.model&&window.__gallery.renderer.detail.entry.bytes>0),'Selected detail must draw an actual loaded GLB');
    const after=await page.locator('html').evaluate(el=>({x:el.getBoundingClientRect().x,width:el.getBoundingClientRect().width}));
    assert(Math.abs(after.x-before.x)<=.5&&Math.abs(after.width-before.width)<=.5,'Deployed gallery must not shift horizontally');
    assert.equal(await page.locator('canvas.preview-renderer').count(),1,'Inline detail and hover share one renderer');
    assert.equal(await page.locator('#info-content h2').textContent(),asset.name[mobile?'zh':'en']);
    assert.equal(await page.locator('#download').getAttribute('href'),base+asset.glb);
    assert.equal(await page.locator('#blend').getAttribute('href'),base+asset.blend);
    const detailURL=base+lang+`models/${id}/`,staticResponse=await page.request.get(detailURL);assert(staticResponse.ok());const html=await staticResponse.text();assert(html.includes('application/ld+json')&&html.includes('static-route-content'));
    const downloaded={};
    for(const key of ['glb','blend']){const response=await page.request.get(base+asset[key]);assert(response.ok());const bytes=await response.body();assert.equal(hash(bytes),asset.sha256[key]);downloaded[key]=bytes.length;}
    assert.equal(downloaded.glb,(await readFile(asset.glb)).length);
    for(const [kind,path] of [['credits',`assets/downloads/${id}-CREDITS.txt`],['bundle',`assets/downloads/${id}.zip`]]) {
     const response=await page.request.get(base+path);assert(response.ok());const bytes=await response.body();assert(bytes.length>0);
     if(kind==='credits'){assert.match(bytes.toString(),/Leon Made This/);assert.match(bytes.toString(),/https:\/\/creativecommons\.org\/licenses\/by\/4\.0\//);}else assert.equal(bytes.subarray(0,2).toString(),'PK');
    }
    await page.locator('#credits').click();await page.waitForFunction(()=>document.querySelector('#credits')?.dataset.copyState==='success');assert((await page.evaluate(()=>navigator.clipboard.readText())).includes('Leon Made This'));
    await page.screenshot({path:resolve(out,`${mobile?'touch':'desktop'}-${id}.png`)});
    await page.goto(detailURL);await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready');await page.reload();await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready');
    assert(Number(await page.locator('#canvas-host').getAttribute('data-render-triangles'))>0,'Independent detail reload must draw actual GLB');
    report.static_routes.push(detailURL);report.cases.push({id,viewport:mobile?'390x844-touch':'1440x1000',status:'pass',glb_bytes:downloaded.glb,glb_sha256:asset.sha256.glb});
    await page.goto(catalog);await page.waitForFunction(()=>window.__gallery?.models.length>0);
   }
  }finally{await context.close();}
 }
 await Promise.all(entryChecks);assert.deepEqual(report.entry_errors,[]);assert(report.loaded_entries.some(p=>p.endsWith('.js')),'No exact runtime JS was observed');assert.deepEqual(report.errors,[]);assert.deepEqual(report.resource_errors,[]);report.checks.browser='PASS';report.status='pass';report.phase='complete';
}catch(error){report.status='fail';report.failed_phase=report.phase;report.error=error.stack;process.exitCode=1;console.error(error);}
finally{try{await browser?.close();}catch(error){report.status='fail';report.failed_phase||='browser-cleanup';report.cleanup_error=error.stack;process.exitCode=1;}await mkdir(out,{recursive:true});await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}

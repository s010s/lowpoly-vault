import {ACCEPTED_ROUND13_ASSETS} from './accepted-round13-release.mjs';
import {ROUND13_IDS,ROUND13_PACK} from './small-life-round13-release.mjs';
import {ACCEPTED_ROUND12_ASSETS} from './accepted-round12-release.mjs';
import {ROUND12_IDS,ROUND12_PACK} from './small-life-round12-release.mjs';
import {ACCEPTED_ROUND11_ASSETS} from './accepted-round11-release.mjs';
import {ROUND11_IDS,ROUND11_PACK} from './small-life-round11-release.mjs';
import {ACCEPTED_ROUND10_ASSETS} from './accepted-round10-release.mjs';
import {ROUND10_IDS,ROUND10_PACK} from './small-life-round10-release.mjs';
import {ACCEPTED_ROUND09_ASSETS} from './accepted-round09-release.mjs';
import {ROUND09_IDS,ROUND09_PACK} from './small-life-round09-release.mjs';
import {ACCEPTED_ROUND08_ASSETS} from './accepted-round08-release.mjs';
import {ROUND08_IDS,ROUND08_PACK} from './small-life-round08-release.mjs';
import {ACCEPTED_ROUND07_ASSETS} from './accepted-round07-release.mjs';
import {ROUND07_IDS,ROUND07_PACK} from './small-life-round07-release.mjs';
import {ACCEPTED_ROUND06_ASSETS} from './accepted-round06-release.mjs';
import {ROUND06_IDS,ROUND06_PACK} from './small-life-round06-release.mjs';
import {ACCEPTED_ROUND05_ASSETS} from './accepted-round05-release.mjs';
import {ROUND05_IDS,ROUND05_PACK} from './small-life-round05-release.mjs';
import {ACCEPTED_ROUND04_ASSETS} from './accepted-round04-release.mjs';
import {ROUND04_IDS,ROUND04_PACK} from './small-life-round04-release.mjs';
/** Actual Pages acceptance. Never substitutes a local server for the deployed origin. */
import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {chromium} from 'playwright';
import {ROUND03_IDS,ROUND03_PACK} from './small-life-round03-release.mjs';
import {ACCEPTED_ROUND03_ASSETS} from './accepted-round03-release.mjs';
import {ROUND02_IDS,ROUND02_PACK} from './small-life-round02-release.mjs';
import {ACCEPTED_ROUND02_ASSETS} from './accepted-round02-release.mjs';
import {BATCH_IDS,BATCH_PACK} from './small-life-batch-release.mjs';
import {ACCEPTED_BATCH_ASSETS} from './accepted-small-life-batch-data.mjs';
import {FAUNA_IDS} from './small-fauna-release.mjs';
import {waitForDeployedRelease} from './live-release-contract.mjs';
const base='https://s010s.github.io/lowpoly-vault/',out=resolve(process.env.QA_OUTPUT_DIR||'qa/live-fauna-release');
const expected=JSON.parse(await readFile('assets/manifest.json'));
const ids=expected.publication.round13_descriptor?ROUND13_IDS:expected.publication.round12_descriptor?ROUND12_IDS:expected.publication.round11_descriptor?ROUND11_IDS:expected.publication.round10_descriptor?ROUND10_IDS:expected.publication.round09_descriptor?ROUND09_IDS:expected.publication.round08_descriptor?ROUND08_IDS:expected.publication.round07_descriptor?ROUND07_IDS:expected.publication.round06_descriptor?ROUND06_IDS:expected.publication.round05_descriptor?ROUND05_IDS:expected.publication.round04_descriptor?ROUND04_IDS:expected.publication.round03_descriptor?ROUND03_IDS:expected.publication.round02_descriptor?ROUND02_IDS:expected.publication.batch_descriptor?BATCH_IDS:FAUNA_IDS,pack=expected.publication.round13_descriptor?ROUND13_PACK:expected.publication.round12_descriptor?ROUND12_PACK:expected.publication.round11_descriptor?ROUND11_PACK:expected.publication.round10_descriptor?ROUND10_PACK:expected.publication.round09_descriptor?ROUND09_PACK:expected.publication.round08_descriptor?ROUND08_PACK:expected.publication.round07_descriptor?ROUND07_PACK:expected.publication.round06_descriptor?ROUND06_PACK:expected.publication.round05_descriptor?ROUND05_PACK:expected.publication.round04_descriptor?ROUND04_PACK:expected.publication.round03_descriptor?ROUND03_PACK:expected.publication.round02_descriptor?ROUND02_PACK:expected.publication.batch_descriptor?BATCH_PACK:'prehistoric-small-fauna';
const report={status:'running',source_commit:process.env.GITHUB_SHA||null,origin:base,cases:[],static_routes:[],errors:[],resource_errors:[],limitations:['Actual public Pages origin in Chromium SwiftShader; emulated touch, no physical-device performance claim.']};
const hash=b=>createHash('sha256').update(b).digest('hex');
let browser;
try {
 await mkdir(out,{recursive:true});
 // Pages/CDN caches may still return the previous release briefly. Only proceed on the exact expected payload set.
 const deployed=await waitForDeployedRelease(base+'assets/manifest.json?release='+report.source_commit,expected);
 report.deployed_payload_scope='exact-match';
 const limited=expected.assets.filter(a=>Object.hasOwn(a.approval_provenance||{},'hardware_gpu_verified'));
 for(const asset of limited){const actual=deployed.assets.find(a=>a.id===asset.id);assert.deepEqual(actual.approval_provenance,asset.approval_provenance,asset.id+': public approval/hardware limitations must remain intact');}
 report.preserved_hardware_limitations=limited.map(a=>({id:a.id,formal_profile_acceptance:a.approval_provenance.formal_profile_acceptance,hardware_gpu_verified:a.approval_provenance.hardware_gpu_verified}));
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});report.browser=browser.version();
 for(const mobile of [false,true]) {
  const lang=mobile?'zh-CN/':'',context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},hasTouch:mobile,isMobile:mobile,reducedMotion:'reduce'});
  await context.grantPermissions(['clipboard-read','clipboard-write'],{origin:new URL(base).origin});
  const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));page.on('response',r=>{if(r.status()>=400)report.resource_errors.push(`${r.status()} ${r.url()}`);});
  try {
   const catalog=base+lang+'models/?pack='+pack;
   await page.goto(catalog);await page.waitForFunction(()=>window.__gallery?.models.length>0);
   assert.deepEqual((await page.evaluate(()=>window.__gallery.state.results.map(asset=>asset.id))).sort(),[...ids].sort());
   assert.equal(await page.evaluate(()=>window.__gallery.models.length),expected.assets.length,'Every published model is present, not only the prototype subset');
   assert(await page.locator('#wheel').evaluate(el=>['auto','scroll'].includes(getComputedStyle(el).overflowY)),'The approved wheel retains native scrolling');
   assert.equal(await page.locator('#grid').count(),0,'The retired grid is not mounted behind the approved gallery');
   for(const id of ids) {
    const asset=expected.assets.find(a=>a.id===id),card=page.locator(`#slots [data-id="${id}"]`);
    await page.locator('#wheel').evaluate((wheel,id)=>{wheel.scrollTop=window.__gallery.state.results.findIndex(asset=>asset.id===id)*128;},id);
    await card.waitFor({state:'visible'});await card.locator('img').evaluate(img=>img.decode());assert(await card.locator('img').evaluate(img=>img.naturalWidth>0));
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
    assert.equal(downloaded.glb,ACCEPTED_ROUND13_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND12_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND11_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND10_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND09_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND08_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND07_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND06_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND05_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND04_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND03_ASSETS[id]?.glb.bytes??ACCEPTED_ROUND02_ASSETS[id]?.glb.bytes??ACCEPTED_BATCH_ASSETS[id]?.glb.bytes??{burgessomedusa:122504,diplomystus:93752,kalligramma:150456}[id]);
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
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.resource_errors,[]);report.status='pass';
}catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;console.error(error);}
finally{await browser?.close();await mkdir(out,{recursive:true});await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}

/** Actual Pages acceptance. Never substitutes a local server for the deployed origin. */
import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {chromium} from 'playwright';
import {FAUNA_IDS} from './small-fauna-release.mjs';
const base='https://s010s.github.io/lowpoly-vault/',out=resolve(process.env.QA_OUTPUT_DIR||'qa/live-fauna-release');
const expected=JSON.parse(await readFile('assets/manifest.json'));
const scope=m=>m.assets.map(a=>({id:a.id,glb:a.sha256.glb,blend:a.sha256.blend,preview:a.sha256.preview}));
const report={status:'running',source_commit:process.env.GITHUB_SHA||null,origin:base,cases:[],static_routes:[],errors:[],resource_errors:[],limitations:['Actual public Pages origin in Chromium SwiftShader; emulated touch, no physical-device performance claim.']};
const hash=b=>createHash('sha256').update(b).digest('hex');
let browser;
try {
 await mkdir(out,{recursive:true});
 // Pages/CDN caches may still return the previous release briefly. Only proceed on the exact expected payload set.
 const deadline=Date.now()+180000;
 while(true){
  try{const response=await fetch(base+'assets/manifest.json?release='+report.source_commit,{cache:'no-store'});assert(response.ok());const current=await response.json();assert.deepEqual(scope(current),scope(expected));break;}
  catch(error){if(Date.now()>=deadline)throw error;await new Promise(r=>setTimeout(r,5000));}
 }
 report.deployed_payload_scope='exact-match';
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});report.browser=browser.version();
 for(const mobile of [false,true]) {
  const lang=mobile?'zh-CN/':'',context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},hasTouch:mobile,isMobile:mobile,reducedMotion:'reduce'});
  await context.grantPermissions(['clipboard-read','clipboard-write'],{origin:new URL(base).origin});
  const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));page.on('response',r=>{if(r.status()>=400)report.resource_errors.push(`${r.status()} ${r.url()}`);});
  try {
   const catalog=base+lang+'models/?pack=prehistoric-small-fauna';
   await page.goto(catalog);await page.waitForFunction(()=>document.querySelector('#grid')?.ariaBusy==='false');
   assert.deepEqual((await page.locator('#grid .asset-card').evaluateAll(nodes=>nodes.map(n=>n.dataset.id))).sort(),FAUNA_IDS);
   for(const id of FAUNA_IDS) {
    const asset=expected.assets.find(a=>a.id===id),card=page.locator(`#grid [data-id="${id}"]`);await card.scrollIntoViewIfNeeded();await card.locator('img').evaluate(img=>img.decode());assert(await card.locator('img').evaluate(img=>img.naturalWidth>0));
    if(!mobile){await card.hover();await page.waitForFunction(id=>document.querySelector(`[data-id="${id}"]`)?.dataset.previewState==='ready',id);}
    await card.click();await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready');
    assert(Number(await page.locator('#canvas-host').getAttribute('data-render-triangles'))>0);
    assert.equal(await page.locator('#asset-title').textContent(),asset.name[mobile?'zh':'en']);
    const detailURL=base+lang+`models/${id}/`,staticResponse=await page.request.get(detailURL);assert(staticResponse.ok());const html=await staticResponse.text();assert(html.includes('application/ld+json')&&html.includes('static-route-content'));
    for(const key of ['glb','blend']){const response=await page.request.get(base+asset[key]);assert(response.ok());assert.equal(hash(await response.body()),asset.sha256[key]);}
    for(const [kind,path] of [['credits',`assets/downloads/${id}-CREDITS.txt`],['bundle',`assets/downloads/${id}.zip`]]) {
     const response=await page.request.get(base+path);assert(response.ok());const bytes=await response.body();assert(bytes.length>0);
     if(kind==='credits'){assert.match(bytes.toString(),/Leon Made This/);assert.match(bytes.toString(),/https:\/\/creativecommons\.org\/licenses\/by\/4\.0\//);}else assert.equal(bytes.subarray(0,2).toString(),'PK');
    }
    await page.locator('#copy-attribution').click();await page.waitForFunction(()=>document.querySelector('#copy-attribution')?.dataset.copyState==='copied');assert((await page.evaluate(()=>navigator.clipboard.readText())).includes('Leon Made This'));
    await page.screenshot({path:resolve(out,`${mobile?'touch':'desktop'}-${id}.png`)});
    await page.goto(detailURL);await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready');await page.reload();await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready');
    assert(Number(await page.locator('#canvas-host').getAttribute('data-render-triangles'))>0,'Independent detail reload must draw actual GLB');
    report.static_routes.push(detailURL);report.cases.push({id,viewport:mobile?'390x844-touch':'1440x1000',status:'pass',glb_bytes:(await(page.request.get(base+asset.glb))).headers()['content-length'],glb_sha256:asset.sha256.glb});
    await page.goto(catalog);await page.waitForFunction(()=>document.querySelector('#grid')?.ariaBusy==='false');
   }
  }finally{await context.close();}
 }
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.resource_errors,[]);report.status='pass';
}catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;console.error(error);}
finally{await browser?.close();await mkdir(out,{recursive:true});await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}

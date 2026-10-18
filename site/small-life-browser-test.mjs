import {ROUND07_IDS,ROUND07_PACK} from './small-life-round07-release.mjs';
import {ROUND06_IDS,ROUND06_PACK} from './small-life-round06-release.mjs';
import {ROUND05_IDS,ROUND05_PACK} from './small-life-round05-release.mjs';
import {ROUND04_IDS,ROUND04_PACK} from './small-life-round04-release.mjs';
/** Real-site smoke coverage for every new prop on desktop and emulated touch. */
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { createHash } from 'node:crypto';
import { SMALL_LIFE_IDS } from './small-life-release.mjs';
import { ROUND03_IDS, ROUND03_PACK } from './small-life-round03-release.mjs';
import { ROUND02_IDS, ROUND02_PACK } from './small-life-round02-release.mjs';
import { BATCH_IDS, BATCH_PACK } from './small-life-batch-release.mjs';
import { FAUNA_IDS } from './small-fauna-release.mjs';
const pack=process.env.QA_ADDITION_PACK||'prehistoric-small-life';
assert(['prehistoric-small-life','prehistoric-small-fauna',BATCH_PACK,ROUND02_PACK,ROUND03_PACK,ROUND04_PACK,ROUND05_PACK,ROUND06_PACK,ROUND07_PACK].includes(pack));
const assetIDs=pack===ROUND07_PACK?ROUND07_IDS:pack===ROUND06_PACK?ROUND06_IDS:pack===ROUND05_PACK?ROUND05_IDS:pack===ROUND04_PACK?ROUND04_IDS:pack===ROUND03_PACK?ROUND03_IDS:pack===ROUND02_PACK?ROUND02_IDS:pack===BATCH_PACK?BATCH_IDS:pack==='prehistoric-small-fauna'?FAUNA_IDS:SMALL_LIFE_IDS;
const root=resolve(process.env.GALLERY_DIR||'dist'),out=resolve(process.env.QA_OUTPUT_DIR||'qa/small-life-release-20261018/new-props'),prefix='/lowpoly-vault/';
const manifest=JSON.parse(await readFile(resolve(root,'assets/manifest.json'))),report={status:'running',cases:[],page_errors:[],resource_errors:[],limitations:['Chromium SwiftShader and emulated touch; not physical-device performance.']},requests=[];
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp','.glb':'model/gltf-binary'};
const server=createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');assert(url.pathname.startsWith(prefix));let file=resolve(root,decodeURIComponent(url.pathname.slice(prefix.length))||'index.html');assert(file.startsWith(root+sep));if((await stat(file)).isDirectory())file=resolve(file,'index.html');res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream'}).end(await readFile(file));}catch{res.writeHead(404).end();}});
let browser;
try {
 await mkdir(out,{recursive:true});await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}${prefix}`;
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});report.browser=browser.version();
 for(const mobile of [false,true]) {
  const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},hasTouch:mobile,isMobile:mobile,reducedMotion:'reduce'}),page=await context.newPage();
  page.on('pageerror',e=>report.page_errors.push(e.message));page.on('request',r=>requests.push(r.url()));page.on('response',r=>{if(r.status()>=400)report.resource_errors.push(`${r.status()} ${r.url()}`);});
  const catalog=base+(mobile?'zh-CN/':'')+`models/?pack=${pack}`;
  await page.goto(catalog);await page.waitForFunction(()=>document.querySelector('#grid')?.ariaBusy==='false');
  assert.deepEqual((await page.locator('#grid .asset-card').evaluateAll(nodes=>nodes.map(n=>n.dataset.id))).sort(),assetIDs);
  for(const id of assetIDs) {
   const asset=manifest.assets.find(a=>a.id===id),card=page.locator(`#grid .asset-card[data-id="${id}"]`);await card.scrollIntoViewIfNeeded();await card.locator('img').evaluate(img=>img.decode());
   if(!mobile){await card.hover();await page.waitForFunction(id=>document.querySelector(`[data-id="${id}"]`)?.dataset.previewState==='ready',id);}
   await card.click();await page.waitForFunction(()=>document.querySelector('#canvas-host')?.dataset.modelState==='ready');
   assert.equal(await page.locator('#asset-title').textContent(),asset.name[mobile?'zh':'en']);
   assert(Number(await page.locator('#canvas-host').getAttribute('data-render-triangles'))>0);
   assert(await page.locator('#viewer-dialog').evaluate(dialog=>dialog.scrollWidth<=dialog.clientWidth+1),'No modal horizontal overflow');
   for(const key of ['glb','blend']){const response=await page.request.get(base+asset[key]);assert(response.ok());assert.equal(createHash('sha256').update(await response.body()).digest('hex'),asset.sha256[key]);}
   await page.screenshot({path:resolve(out,`${mobile?'mobile':'desktop'}-${id}.png`)});
   await page.locator('#close').click();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open&&!document.querySelector('.stage-flight'));
   assert.equal(new URL(page.url()).searchParams.get('pack'),pack);
   report.cases.push({id,viewport:mobile?'390x844-touch':'1440x1000',status:'pass',glb_sha256:asset.sha256.glb,blend_sha256:asset.sha256.blend});
  }
  await context.close();
 }
 assert.deepEqual(report.page_errors,[]);assert.deepEqual(report.resource_errors,[]);assert(!requests.some(url=>url.includes('/turntables/')),'New props must not request sequence frames or metadata');report.sequence_requests=0;report.status='pass';
} catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;}
finally {await browser?.close();if(server.listening)await new Promise(r=>server.close(r));await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}

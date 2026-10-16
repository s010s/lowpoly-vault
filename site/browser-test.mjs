import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve, extname } from 'node:path';
import assert from 'node:assert/strict';
const prefix='/lowpoly-vault/',root=resolve(process.env.GALLERY_DIR||'dist');
const manifest=JSON.parse(await readFile(resolve(root,'assets/manifest.json'),'utf8'));
const report={status:'running',commit:process.env.GITHUB_SHA||null,review_only:!!manifest.review_only,build_directory:root,visual_approval:'pending_human_inspection',models:[],checks:[],page_errors:[],resource_errors:[]};
if(process.env.QA_REVIEW_ONLY==='1')assert(manifest.review_only,'CI review must be visibly marked review_only');
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.glb':'model/gltf-binary'};
const server=createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');if(!url.pathname.startsWith(prefix)){res.writeHead(404);res.end();return;}const p=resolve(root,decodeURIComponent(url.pathname.slice(prefix.length))||'index.html');if(!p.startsWith(root+'/'))throw new Error('Invalid path');const data=await readFile(p);res.writeHead(200,{'Content-Type':mime[extname(p)]||'application/octet-stream'});res.end(data);}catch{res.writeHead(404);res.end();}});
await mkdir('qa/screenshots',{recursive:true});
let browser,page,intentionalFailure=false;
try{
 await new Promise((r,j)=>{server.once('error',j);server.listen(0,'127.0.0.1',r);});
 const url=`http://127.0.0.1:${server.address().port}${prefix}`;
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 report.chromium_version=browser.version();
 page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 page.on('pageerror',e=>report.page_errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!intentionalFailure)report.resource_errors.push(`${r.status()} ${r.url()}`);});
 await page.goto(url);await page.locator('.asset-card').first().waitFor({timeout:30000});
 const count=await page.locator('.asset-card').count();assert.equal(count,manifest.assets.length);if(process.env.QA_REQUIRE_COUNT)assert.equal(count,Number(process.env.QA_REQUIRE_COUNT));
 if(manifest.review_only)assert(await page.locator('.review-notice').isVisible());
 await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(img=>img.decode())));await page.screenshot({path:'qa/screenshots/gallery-desktop.png',fullPage:true});
 assert(await page.locator('html').getAttribute('lang')==='en');await page.locator('[data-category="plants"]').click();assert(await page.locator('.asset-card').count()>0);assert(await page.locator('.asset-card').count()<count);await page.locator('[data-category="all"]').click();await page.locator('#search').fill('THIS_DOES_NOT_EXIST');assert(await page.locator('.asset-card').count()===0);await page.locator('#search').fill('');assert(await page.locator('.asset-card').count()===count);report.checks.push('category filters','search and empty result','desktop previews','project subpath');
 for(let i=0;i<count;i++){
  const a=manifest.assets[i];await page.locator(`.asset-card[data-id="${a.id}"]`).click();await page.waitForFunction(()=>document.querySelector('#viewer-status').textContent==='',null,{timeout:30000});assert(await page.locator('#canvas-host canvas').count()===1);assert(Number(await page.locator('#canvas-host').getAttribute('data-render-triangles'))>0,'WebGL must draw real triangles');assert(await page.locator('#downloads a').count()===2);
  for(const link of await page.locator('#downloads a').all()){const href=await link.getAttribute('href'),response=await page.request.get(href);assert(response.ok(),`Download failed: ${href}`);assert((await response.body()).length>0);}
  await page.screenshot({path:`qa/screenshots/model-${a.id}.png`});
  await page.locator('#wireframe').click();assert(await page.locator('#wireframe').getAttribute('aria-pressed')==='true');assert(Number(await page.locator('#canvas-host').getAttribute('data-render-lines'))>0,'Wireframe must draw real lines');await page.screenshot({path:`qa/screenshots/wireframe-${a.id}.png`});
  await page.locator('#canvas-host').focus();await page.keyboard.press('ArrowRight');await page.keyboard.press('+');await page.locator('#zoom-out').click();await page.locator('#reset').click();await page.locator('#wireframe').click();
  report.models.push({id:a.id,glb_sha256:a.sha256?.glb||null,status:'pass',checks:['GLTFLoader loaded in browser','WebGL canvas rendered','wireframe toggle','keyboard rotation and zoom','reset and zoom buttons','GLB and Blend downloads'],screenshots:[`model-${a.id}.png`,`wireframe-${a.id}.png`]});await page.keyboard.press('Escape');assert(!(await page.locator('#viewer-dialog').isVisible()));
 }
 await page.locator('#language').click();assert(await page.locator('html').getAttribute('lang')==='zh-CN');assert((await page.locator('#collection-title').textContent()).includes('世界'));await page.screenshot({path:'qa/screenshots/gallery-chinese.png',fullPage:true});await page.setViewportSize({width:390,height:844});await page.screenshot({path:'qa/screenshots/gallery-mobile.png',fullPage:true});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.locator('.asset-card').first().click();await page.waitForFunction(()=>document.querySelector('#viewer-status').textContent==='',null,{timeout:30000});await page.screenshot({path:'qa/screenshots/viewer-mobile.png',fullPage:true});assert(await page.locator('#viewer-dialog').evaluate(el=>el.scrollWidth<=el.clientWidth));await page.keyboard.press('Escape');report.checks.push('bilingual UI','mobile layout without horizontal overflow','mobile viewer','Escape closes dialog');
 intentionalFailure=true;await page.route('**/assets/manifest.json',r=>r.fulfill({status:503,body:'Unavailable'}));await page.reload();await page.waitForFunction(()=>document.querySelector('#grid').textContent.includes('暂时不可用'));assert(await page.locator('.asset-card').count()===0);report.checks.push('explicit manifest failure state');assert.deepEqual(report.page_errors,[]);assert.deepEqual(report.resource_errors,[]);report.status='pass';console.log(`Browser QA passed: ${count} real GLBs and gallery interactions. Screenshots require human review; no asset QA state was changed.`);
}catch(error){report.status='fail';report.error=error.stack||error.message;try{await page?.screenshot({path:'qa/screenshots/failure.png',fullPage:true});}catch{}console.error(error);process.exitCode=1;}
finally{await writeFile('qa/browser-report.json',JSON.stringify(report,null,2)+'\n');await browser?.close();server.close();}

/** Screenshot-free demonstration recorded against the deployed public site. */
import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
const output=resolve(process.env.DEMO_OUTPUT||'qa/live-continuity-demo'),base='https://s010s.github.io/lowpoly-vault/';
const report={status:'running',url:base,cases:[],note:'Pinned Chromium software renderer; desktop and touch-emulated mobile. No screenshot-induced viewport resizing during the recording.'};
let browser;
async function ready(page,id){await page.waitForFunction(id=>{const h=document.querySelector('#canvas-host');return h?.dataset.modelState==='ready'&&h.dataset.presentedUrl?.endsWith('/'+id+'.glb');},id,{timeout:30000});}
async function run(label,mobile=false){
 const viewport=mobile?{width:390,height:844}:{width:1440,height:1000},context=await browser.newContext({viewport,reducedMotion:'no-preference',recordVideo:{dir:output,size:viewport},...(mobile?{isMobile:true,hasTouch:true,deviceScaleFactor:2}:{})});
 const page=await context.newPage(),started=Date.now(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 const entry={label};report.cases.push(entry);
 try{
  await page.goto(base+'models/');await page.waitForFunction(()=>document.querySelector('#grid')?.getAttribute('aria-busy')==='false');
  const card=page.locator('#grid [data-id="natural-arch"]');await card.scrollIntoViewIfNeeded();await page.waitForTimeout(500);entry.content_start_ms=Date.now()-started;
  const box=await card.locator('.asset-image').boundingBox();
  if(mobile){const session=await context.newCDPSession(page),x=box.x+box.width*.3,y=box.y+box.height*.5;await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y,id:1}]});for(let i=1;i<=10;i++){await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:x+i*7,y:y+1,id:1}]});await page.waitForTimeout(65);}await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});}
  else{await card.hover();await page.waitForFunction(()=>document.querySelector('#grid [data-id="natural-arch"]')?.dataset.scrubState==='ready');for(let i=1;i<=10;i++){await page.mouse.move(box.x+box.width*(.5+i*.035),box.y+box.height/2);await page.waitForTimeout(65);}}
  await page.waitForTimeout(400);entry.frame=await card.getAttribute('data-scrub-frame');assert(entry.frame!==null);if(mobile)await card.tap();else{await card.focus();await page.keyboard.press('Enter');}await ready(page,'natural-arch');await page.waitForTimeout(800);
  entry.detail_azimuth=Number(await page.locator('#canvas-host').getAttribute('data-view-azimuth'));const expected=(42+Number(entry.frame)*15)%360;assert(Math.abs(entry.detail_azimuth-expected)<.001);
  await page.locator('#canvas-host').focus();await page.keyboard.press('ArrowRight');await page.keyboard.press('ArrowUp');await page.waitForTimeout(450);
  await page.locator('#next-model').click();await ready(page,'stratified-cliff');await page.waitForTimeout(650);await page.locator('#previous-model').click();await ready(page,'natural-arch');await page.waitForTimeout(650);
  await page.locator('#close').click();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open);await page.waitForTimeout(650);entry.content_end_ms=Date.now()-started;assert.deepEqual(errors,[]);entry.status='pass';
 }finally{const video=page.video();await context.close();entry.video=(await video.path()).split(/[\\/]/).at(-1);entry.page_errors=errors;}
}
try{await mkdir(output,{recursive:true});browser=await chromium.launch({args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});report.chromium_version=browser.version();await run('desktop');await run('mobile',true);report.status='pass';}
catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;console.error(error);}
finally{await browser?.close();await writeFile(resolve(output,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}

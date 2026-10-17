import {chromium} from 'playwright';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='qa/release-conifer-doc1-live/cycle',base='https://s010s.github.io/lowpoly-vault/';
const expected=JSON.parse(await readFile('dist/assets/manifest.json'));
const report={status:'running',url:base,models:[],page_errors:[],note:'Actual public site; isolated Chromium SwiftShader. Functional correctness only; no physical-device performance claim.'};
let browser;
try{
 await mkdir(out,{recursive:true});
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH,proxy:{server:'http://127.0.0.1:10808'},args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'no-preference'}),page=await context.newPage();
 page.on('pageerror',e=>report.page_errors.push(e.message));
 const live=await (await context.request.get(base+'assets/manifest.json')).json();
 assert.deepEqual(live,expected);
 await page.goto(base+'models/conifer-tree/');
 const ready=()=>page.waitForFunction(()=>{const h=document.querySelector('#canvas-host'),id=location.pathname.split('/').filter(Boolean).at(-1);return h?.dataset.modelState==='ready'&&h.dataset.presentedUrl?.endsWith('/'+id+'.glb');},null,{timeout:45000});
 await ready();await page.screenshot({path:out+'/conifer-ready.png'});
 for(let j=0;j<10 && await page.locator('#previous-model').isVisible();j++){await page.locator('#previous-model').click();await ready();}
 const seen=new Set();
 for(let i=0;i<10;i++){
  await ready();
  const state=await page.locator('#canvas-host').evaluate(h=>({url:h.dataset.presentedUrl,liveScenes:window.__vaultGPU.liveScenes,canvases:h.querySelectorAll('.model-canvas').length}));
  const id=new URL(page.url()).pathname.split('/').filter(Boolean).at(-1),asset=expected.assets.find(x=>x.id===id);
  assert(asset);assert(new URL(state.url,base).pathname.endsWith('/'+asset.glb));assert.equal(state.liveScenes,1);assert.equal(state.canvases,1);
  seen.add(id);report.models.push({id,...state,expected_glb_sha256:asset.sha256.glb});
  if(i<9)await page.locator('#next-model').click();
 }
 assert.equal(seen.size,10);
 for(let i=0;i<2;i++){
  await page.locator('#previous-model').click();
  await ready();
  assert.equal(await page.evaluate(()=>window.__vaultGPU.liveScenes),1);
 }
 await page.locator('#close').click();await page.waitForFunction(()=>!document.querySelector('#viewer-dialog').open&&window.__vaultGPU.liveScenes===0);
 assert.deepEqual(report.page_errors,[]);report.status='pass';report.distinct_models=seen.size;report.chromium_version=browser.version();
}catch(e){report.status='fail';report.error=e.stack;process.exitCode=1;}
finally{await browser?.close();await mkdir(out,{recursive:true});await writeFile(out+'/report.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}

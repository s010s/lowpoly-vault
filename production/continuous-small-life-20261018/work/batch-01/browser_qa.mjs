// SPDX-License-Identifier: MIT
// Exact shipped GLB functional renderer. SwiftShader is software evidence only.
import {chromium} from 'playwright';
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
const ids=process.argv.slice(2);if(!ids.length)throw Error('Pass one or more batch-01 IDs');
const base='assets/candidates/continuous-small-life-20261018/batch-01';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{for(const id of ids){const bundle=path.join(base,id,'r001'),out=path.join(bundle,'evidence/runtime');fs.mkdirSync(out,{recursive:true});const hash=crypto.createHash('sha256').update(fs.readFileSync(path.join(bundle,id+'.glb'))).digest('hex');
 const records=[];
 for(const scene of [false,true]){
  const page=await browser.newPage({viewport:{width:640,height:640}});const errors=[],failed=[];page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('requestfailed',r=>failed.push({url:r.url(),failure:r.failure()}));
  await page.goto('http://127.0.0.1:8765/production/continuous-small-life-20261018/work/batch-01/viewer.html?asset='+id+(scene?'&scene=1':''));await page.waitForFunction(()=>window.ready,{timeout:60000});
  const metrics=await page.evaluate(()=>window.inspect),views=[];
  for(const [view,extent] of scene?[['hero',480],['top',480]]:[['hero',360],['reversehero',360],['front',360],['side',360],['rear',360],['top',360],['bottom',360],['hero',80],['hero',160],['hero',240]]){
   const measured=await page.evaluate(([v,n])=>window.setView(v,n),[view,extent]);const file=(scene?'scene-':'')+view+'-'+extent+'px.png';await page.locator('canvas').screenshot({path:path.join(out,file)});views.push({...measured,path:file,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(out,file))).digest('hex')});
  }
  records.push({scene,...metrics,views,errors,failed,glb_sha256:hash,status:errors.length||failed.length?'fail':'pass',scope:'Functional software WebGL rendering; not physical GPU/device performance. Three copies are a neutral prop benchmark, no museum integration/coexistence claim.'});await page.close();
 }
 const report={asset:id,glb_sha256:hash,status:records.some(r=>r.status==='fail')?'fail':'pass',records};fs.writeFileSync(path.join(out,'runtime.report.json'),JSON.stringify(report,null,2)+'\n');console.log(id,report.status,records[0].renderer);if(report.status==='fail')throw Error(JSON.stringify(report));
}}finally{await browser.close();}

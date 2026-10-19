// SPDX-License-Identifier: MIT
import {chromium} from 'playwright';import fs from'node:fs';import path from'node:path';import crypto from'node:crypto';
const asset=process.argv[2];if(!['sidneyia', 'botrychium', 'barrier-island', 'diplocraterion-spreite-burrow'].includes(asset))throw Error('asset required');
const attempt=JSON.parse(fs.readFileSync(`production/continuous-small-life-round14-20261018/work/batch-40/${asset}/r001/config.json`)).selected_attempt||'attempt-01';
const base=`assets/candidates/continuous-small-life-round14-20261018/batch-40/${asset}/r001/${attempt}/${asset}`,out=base+'/runtime';fs.mkdirSync(out,{recursive:true});
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),glbHash=hash(base+'/'+asset+'.glb');
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
for(const mode of ['single','scene']){
 const page=await browser.newPage({viewport:{width:640,height:640}});let errors=[],failed=[];page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('requestfailed',r=>failed.push({url:r.url(),failure:r.failure()}));
 await page.goto(`http://127.0.0.1:8800/production/continuous-small-life-round14-20261018/work/batch-40/viewer.html?asset=${asset}&mode=${mode}&attempt=${attempt}`);await page.waitForFunction(()=>window.ready,{timeout:60000});const metrics=await page.evaluate(()=>window.inspect);const views=[];
 for(const view of mode==='scene'?['hero','top']:['hero','reversehero','front','side','rear','top','bottom']){const result=await page.evaluate(v=>window.setView(v),view);const name=mode+'-'+view+'.png';await page.locator('canvas').screenshot({path:path.join(out,name)});views.push({...result,path:name,sha256:hash(path.join(out,name))})}
 if(mode==='single')for(const extent of[80,160,240]){const result=await page.evaluate(n=>window.setView('hero',n),extent);const name=mode+'-'+extent+'px.png';await page.locator('canvas').screenshot({path:path.join(out,name)});views.push({...result,path:name,sha256:hash(path.join(out,name))})}
 const result={asset,mode,...metrics,views,errors,failed,status:errors.length||failed.length?'fail':'pass',scope:'Actual GLTFLoader and Chromium ANGLE SwiftShader software WebGL2; no physical GPU/device performance claim',glb_sha256:glbHash};fs.writeFileSync(path.join(out,mode+'.json'),JSON.stringify(result,null,2)+'\n');if(errors.length||failed.length)throw Error(JSON.stringify(result));await page.close();console.log(asset,mode,result.status,metrics.renderer)
}await browser.close();

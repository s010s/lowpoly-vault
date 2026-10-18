import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const root=process.cwd();
const batch='production/continuous-small-life-round03-20261018/work/batch-09';
const outRoot=path.join(root,batch,'independent-review/qa-s010s-20261018/runtime');
const handoff=JSON.parse(fs.readFileSync(path.join(root,batch,'HANDOFF.json'),'utf8'));
const assets=handoff.assets;
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const viewNames=['hero','reversehero','front','side','rear','top','bottom'];
for(const item of assets){
 const aid=item.asset_id, glb=path.join(root,item.glb.path), glbHash=sha(glb), expected=item.glb.sha256;
 if(glbHash!==expected) throw Error(`${aid}: GLB hash mismatch ${glbHash} != ${expected}`);
 const out=path.join(outRoot,aid);fs.mkdirSync(out,{recursive:true});
 for(const mode of ['single','scene']){
  const page=await browser.newPage({viewport:{width:640,height:640}}),errors=[],failed=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
  page.on('requestfailed',r=>failed.push({url:r.url(),failure:r.failure()}));
  await page.goto(`http://127.0.0.1:8769/${batch}/viewer-final.html?asset=${aid}&mode=${mode}`);
  await page.waitForFunction(()=>window.ready,{timeout:60000});
  const metrics=await page.evaluate(()=>window.inspect),views=[];
  const selected=mode==='scene'?['hero','top']:viewNames;
  for(const view of selected){
   const info=await page.evaluate(v=>window.setView(v),view),name=`${mode}-${view}.png`,file=path.join(out,name);
   await page.locator('canvas').screenshot({path:file});views.push({...info,path:name,sha256:sha(file)});
  }
  if(mode==='single') for(const extent of [80,160,240]){
   const info=await page.evaluate(n=>window.setView('hero',n),extent),name=`${mode}-${extent}px.png`,file=path.join(out,name);
   await page.locator('canvas').screenshot({path:file});views.push({...info,path:name,sha256:sha(file)});
  }
  const result={asset:aid,mode,source_sha256:item.blend.sha256,glb_sha256:glbHash,...metrics,views,errors,failed,status:errors.length||failed.length?'fail':'pass',scope:'Independent fresh Chromium load of the exact frozen GLB through the supplied Three.js viewer; ANGLE SwiftShader software WebGL2; no physical GPU claim.'};
  fs.writeFileSync(path.join(out,`${mode}.json`),JSON.stringify(result,null,2)+'\n');
  console.log(aid,mode,result.status,metrics.renderer,'loaded',metrics.loaded?.[0]?.bounds,'calls',views.map(x=>x.calls).join(','));
  if(errors.length||failed.length) throw Error(JSON.stringify(result));
  await page.close();
 }
}
await browser.close();

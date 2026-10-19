/** Exact seven integration checks on the actual shared gallery renderer. */
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { mkdir,readFile,writeFile,stat } from 'node:fs/promises';
import { resolve,extname,sep } from 'node:path';
import { createHash } from 'node:crypto';
import { CONCEPT_SEVEN_IDS } from './concept-seven-release.mjs';
const root=resolve(process.env.GALLERY_DIR||'dist'),out=resolve(process.env.QA_OUTPUT_DIR||'qa/concept-seven-release-20261019/browser'),prefix=process.env.SITE_BASE||'/lowpoly-vault/';
const manifest=JSON.parse(await readFile(resolve(root,'assets/manifest.json'))),report={status:'running',cases:[],errors:[],limitations:['Chromium SwiftShader with emulated mobile; no physical-device or intended museum-scene performance claim.']};
assert.deepEqual(manifest.publication.approved_concept_seven_ids,CONCEPT_SEVEN_IDS);assert.equal(manifest.assets.length,182);assert(!manifest.assets.some(a=>a.id==='ctenoimbricata'));
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.webp':'image/webp','.glb':'model/gltf-binary'};
const server=createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');assert(url.pathname.startsWith(prefix));let file=resolve(root,decodeURIComponent(url.pathname.slice(prefix.length))||'index.html');assert(file.startsWith(root+sep));if((await stat(file)).isDirectory())file=resolve(file,'index.html');res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream'}).end(await readFile(file));}catch{res.writeHead(404).end();}});
let browser;
try {
 await mkdir(out,{recursive:true});await new Promise((done,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',done);});const base=`http://127.0.0.1:${server.address().port}${prefix}`;
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});report.browser=browser.version();
 for(const mobile of [false,true]){
  const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},isMobile:mobile,hasTouch:mobile,reducedMotion:'reduce'}),page=await context.newPage();
  page.on('pageerror',e=>report.errors.push(e.message));page.on('response',r=>{if(r.status()>=400)report.errors.push(`${r.status()} ${r.url()}`);});
  page.on('console',message=>{if(message.type()==='error'&&/THREE\.|WebGL|shader|GL_INVALID|CONTEXT_LOST/i.test(message.text()))report.errors.push(message.text());});
  page.setDefaultTimeout(45000);
  await page.goto(base+(mobile?'zh-CN/':'')+'models/?model='+CONCEPT_SEVEN_IDS[0]);await page.waitForFunction(()=>window.__gallery?.models.length===182);
  for(const id of CONCEPT_SEVEN_IDS){
   await page.evaluate(id=>{void window.__gallery.choose(id,{push:false,activateMobile:true});},id);
   await page.waitForFunction(id=>document.querySelector('#detail')?.dataset.state==='ready'&&document.querySelector('#detail').dataset.modelId===id,id,{timeout:45000});
   const snapshot=await page.evaluate(()=>{const p=window.__gallery,r=p.renderer,gl=r.renderer.getContext(),img=document.querySelector('#detail-poster');r.draw();return {selected:p.state.selected,rendered_asset:r.detail.asset.id,first_frame:r.stats.detailFirstFrameId,triangles:r.renderer.info.render.triangles,gl_error:gl.getError(),context_lost:gl.isContextLost(),poster:img.currentSrc,poster_width:img.naturalWidth,body_overflow:document.body.scrollWidth>window.innerWidth+1};});
   assert.equal(snapshot.selected,id);assert.equal(snapshot.rendered_asset,id);assert.equal(snapshot.first_frame,id);assert(snapshot.triangles>0);assert.equal(snapshot.gl_error,0);assert.equal(snapshot.context_lost,false);assert(snapshot.poster.includes(`/gallery/posters/${id}.png`));assert(snapshot.poster_width>0);assert.equal(snapshot.body_overflow,false);
   const asset=manifest.assets.find(a=>a.id===id);
   await page.locator('#info').click();
   assert(await page.locator('#info-panel').isVisible(),'Source labels must be presented in the visible information panel');
   const sourceLinks=await page.locator('#info-content a').evaluateAll(nodes=>nodes.map(a=>({href:a.href,label:a.textContent.trim()})));
   for(const source of asset.sources)assert(sourceLinks.some(a=>a.href===source.url&&a.label.includes(source.title||source.id||source.url)),'Every frozen source has a visible accessible label');
   await page.keyboard.press('Escape');
   for(const [key,selector] of [['glb','#download'],['blend','#blend']]){const control=page.locator(selector);assert(await control.isVisible());const href=await control.evaluate(a=>a.href);assert.equal(href,new URL(asset[key],base).href);const response=await page.request.get(href);assert(response.ok());assert.equal(createHash('sha256').update(await response.body()).digest('hex'),asset.sha256[key]);}
   await page.screenshot({path:resolve(out,`${mobile?'mobile':'desktop'}-${id}.png`)});report.cases.push({id,viewport:mobile?'390x844':'1440x1000',status:'pass',...snapshot,glb_sha256:asset.sha256.glb,blend_sha256:asset.sha256.blend});
  }
  await context.close();
 }
 assert.deepEqual(report.errors,[]);assert.equal(report.cases.length,14);report.status='pass';
}catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;}
finally{await browser?.close();if(server.listening)await new Promise(done=>server.close(done));await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}

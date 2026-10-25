/** Built-page integration: real pointer entry/exit; no renderer/camera substitutions. */
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile,mkdir,writeFile,stat} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {chromium} from 'playwright';
import {CAPTURE_POLICY} from './gallery-poster-inputs.mjs';
import {CATALOG_PAGE_SIZE} from './routes.js';
const out=resolve('qa/wheel-integration-evidence'),root=resolve('dist'),prefix='/lowpoly-vault/';
const ids=['nucleocrinus','spyroceras','phragmoceras','lituites','natural-levee','teleoceras','aegirocassis','thylacoleo'];
const report={version:1,status:'running',source_commit:process.env.GITHUB_SHA||null,physical_gpu:'unknown',cases:[],errors:[]};
let browser,server;
try{
 await mkdir(out,{recursive:true});
 server=createServer(async(req,res)=>{try{let path=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(path.startsWith(prefix))path=path.slice(prefix.length);else path=path.slice(1);let file=resolve(root,path);assert(file.startsWith(root+sep)||file===root);if((await stat(file)).isDirectory())file=resolve(file,'index.html');const mime={'.js':'text/javascript','.css':'text/css','.html':'text/html','.json':'application/json','.png':'image/png','.glb':'model/gltf-binary','.svg':'image/svg+xml'};res.setHeader('Content-Type',mime[extname(file)]||'application/octet-stream');res.end(await readFile(file));}catch{res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}`;
 browser=await chromium.launch({headless:true,args:CAPTURE_POLICY.args});report.browser_version=browser.version();
 const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1,serviceWorkers:'block'});
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error'&&/WebGL|THREE\.|shader|CONTEXT_LOST/i.test(m.text()))report.errors.push(m.text());});
 await page.route('**/*',r=>new URL(r.request().url()).origin===base?r.continue():r.abort());
 const manifest=JSON.parse(await readFile('assets/manifest.json'));const boundaryPage=Math.floor(manifest.assets.findIndex(a=>a.id==='spyroceras')/CATALOG_PAGE_SIZE)+1;assert(boundaryPage>1);
 const ssr=await (await page.request.get(base+prefix+`models/page/${boundaryPage}/`)).text();assert(ssr.includes('wheel-presentations/spyroceras.png'),'SSR boundary wheel not updated');
 await page.goto(base+prefix+'models/');await page.waitForFunction(()=>window.__gallery?.renderer,{timeout:90000});
 await page.evaluate(()=>{window.__wheelFrames=[];const r=window.__gallery.renderer,preview=r.preview.bind(r);r.preview=async function(asset,host){const ok=await preview(asset,host);if(ok){const live=this.hover.presentation.frame,img=host.querySelector('img'),canvas=document.createElement('canvas');canvas.width=live.width;canvas.height=live.height;const ctx=canvas.getContext('2d');ctx.drawImage(img,0,0,canvas.width,canvas.height);const a=ctx.getImageData(0,0,canvas.width,canvas.height).data,poster=canvas.toDataURL();ctx.clearRect(0,0,canvas.width,canvas.height);ctx.drawImage(live,0,0);const b=ctx.getImageData(0,0,canvas.width,canvas.height).data;let intersection=0,union=0,diff=0;for(let i=0;i<a.length;i+=4){const aa=a[i+3]>200,bb=b[i+3]>200;intersection+=aa&&bb;union+=aa||bb;diff+=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]);}const metrics=mask=>{let left=canvas.width,top=canvas.height,right=-1,bottom=-1,xsum=0,ysum=0,count=0;for(let y=0;y<canvas.height;y++)for(let x=0;x<canvas.width;x++)if(mask[(y*canvas.width+x)*4+3]>200){left=Math.min(left,x);top=Math.min(top,y);right=Math.max(right,x);bottom=Math.max(bottom,y);xsum+=x;ysum+=y;count++;}return {bounds:[left,top,right,bottom],centroid:[xsum/Math.max(count,1),ysum/Math.max(count,1)],count};};const ma=metrics(a),mb=metrics(b);let outside=0;const covered=(mask,x,y)=>{for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++){const xx=x+dx,yy=y+dy;if(xx>=0&&yy>=0&&xx<canvas.width&&yy<canvas.height&&mask[(yy*canvas.width+xx)*4+3]>200)return true;}return false;};for(let y=0;y<canvas.height;y++)for(let x=0;x<canvas.width;x++){const i=(y*canvas.width+x)*4;if(a[i+3]>200&&!covered(b,x,y))outside++;if(b[i+3]>200&&!covered(a,x,y))outside++;}const geometry={poster:ma,live:mb,outside_two_pixels:outside,opaque_union:union,maximum_bounds_delta:Math.max(...ma.bounds.map((v,i)=>Math.abs(v-mb.bounds[i]))),centroid_distance:Math.hypot(ma.centroid[0]-mb.centroid[0],ma.centroid[1]-mb.centroid[1])};window.__wheelFrames.push({geometry,id:asset.id,poster_url:img.src,wheelSpec:asset.wheelSpec,renderedSpec:this.hover.wheelSpec,mask_iou:intersection/Math.max(1,union),mean_rgb_absolute_error:diff/(canvas.width*canvas.height*3),width:canvas.width,height:canvas.height,poster,live:live.toDataURL(),context_lost:this.renderer.getContext().isContextLost(),gl_error:this.renderer.getContext().getError()});}return ok;};});
 for(const id of ids){
  await page.mouse.move(1300,50);await page.locator('#search').fill(id.replaceAll('-',' '));await page.locator('#search').press('Enter');
  const slot=page.locator(`.slot[data-id="${id}"]`);await slot.waitFor({state:'visible',timeout:30000});await slot.click();
  await page.waitForFunction(id=>window.__gallery?.renderer?.stats.detailId===id&&window.__gallery.renderer.stats.detailStatus==='ready',id,{timeout:60000});await page.waitForTimeout(500);await page.mouse.move(1300,50);await page.waitForTimeout(350);
  const host=slot.locator('.slot-image');
  for(let entry=0;entry<2;entry++){
   const count=await page.evaluate(()=>window.__wheelFrames.length);await host.hover();await page.waitForFunction(n=>window.__wheelFrames.length>n,count,{timeout:30000});
   const frame=await page.evaluate(()=>window.__wheelFrames.at(-1));assert.equal(frame.id,id);assert.equal(frame.gl_error,0);assert.equal(frame.context_lost,false);assert.deepEqual(frame.renderedSpec,frame.wheelSpec);
   if(id!=='nucleocrinus')assert(frame.poster_url.endsWith(`/wheel-presentations/${id}.png`));else assert(frame.poster_url.endsWith(`/gallery/posters/${id}-wheel.png`));
   await writeFile(resolve(out,`${id}-${entry}-poster.png`),Buffer.from(frame.poster.split(',')[1],'base64'));await writeFile(resolve(out,`${id}-${entry}-live.png`),Buffer.from(frame.live.split(',')[1],'base64'));delete frame.poster;delete frame.live;report.cases.push({...frame,entry});
   // The unchanged control demonstrates raster/downsample edge differences at 203x114.
   // Require bounded <=2px silhouette displacement, unchanged framing, and color parity;
   // do not confuse a hard-alpha IoU threshold with a camera/pose/scale mismatch.
   const g=frame.geometry;const parity=g.poster.count>0&&g.live.count>0&&g.maximum_bounds_delta<=2&&g.centroid_distance<=1.5&&g.outside_two_pixels/Math.max(1,g.opaque_union)<=.002&&frame.mask_iou>.85&&frame.mean_rgb_absolute_error<5;
   if(!parity)report.errors.push(`${id} entry ${entry} geometry/color: ${JSON.stringify({geometry:g,iou:frame.mask_iou,rgb:frame.mean_rgb_absolute_error})}`);
   await page.waitForTimeout(400);await page.screenshot({path:resolve(out,`${id}-${entry}-page.png`)});await page.mouse.move(1300,50);await page.waitForTimeout(350);assert.equal(await host.locator('canvas').count(),0,'Exit did not restore poster');
  }
 }
 assert.deepEqual(report.errors,[]);report.status='pass';
}catch(error){report.status='fail';report.error=error.stack;process.exitCode=1;}
finally{await mkdir(out,{recursive:true});await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2));await browser?.close();if(server)await new Promise(r=>server.close(r));console.log(JSON.stringify({status:report.status,cases:report.cases.length,error:report.error}));}

// Independent output QA. Run from repository root after approved capture.
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
import {createServer} from 'node:http';
import {readFile,writeFile,stat} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {auditGalleryAssets} from '../../site/gallery-assets.mjs';

const out=resolve('dist'),base='/lowpoly-vault/',qa=resolve('qa/gallery-matching-posters-20261019');
const manifest=JSON.parse(await readFile('assets/manifest.json','utf8'));
const audit=await auditGalleryAssets(manifest,{requireComplete:true});
await auditGalleryAssets(manifest,{outputRoot:out,requireComplete:true});
const baseline=JSON.parse(await readFile('site/public/gallery/approved-resources.json','utf8'));
const generated=manifest.assets.filter(a=>!baseline.posters[a.id]).map(a=>a.id);
assert.equal(generated.length,145);
const hash=b=>createHash('sha256').update(b).digest('hex');
const mime={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.png':'image/png','.glb':'model/gltf-binary'};
const server=createServer(async(req,res)=>{try{
 const path=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
 if(!path.startsWith(base))throw Error('base');
 let file=resolve(out,path.slice(base.length));
 if(!file.startsWith(out+sep))throw Error('path');
 if((await stat(file)).isDirectory())file=resolve(file,'index.html');
 res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream'});res.end(await readFile(file));
}catch{res.writeHead(404).end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const page=await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1,reducedMotion:'reduce'}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 await page.goto(`http://127.0.0.1:${server.address().port}${base}models/`,{waitUntil:'networkidle',timeout:120000});
 await page.waitForFunction(()=>window.__preview?.renderer?.detail?.model,null,{timeout:120000});
 const gpu=await page.evaluate(()=>{const r=window.__preview.renderer;r.stopHover();window.__preview.settler?.stop();const gl=r.renderer.getContext(),e=gl.getExtension('WEBGL_debug_renderer_info');return {version:gl.getParameter(gl.VERSION),renderer:e?gl.getParameter(e.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER)};});
 const rows=[];
 for(const asset of manifest.assets){
  const row=await page.evaluate(async id=>{
   const p=window.__preview,r=p.renderer,a=p.models.find(a=>a.id===id),entry=await r.resource(a,new AbortController().signal);
   const bounds=(view,turns)=>{
    const point=view.target.clone(),b={left:Infinity,right:-Infinity,bottom:Infinity,top:-Infinity,near:Infinity,far:-Infinity,vertices:0};
    view.camera.updateMatrixWorld(true);
    for(let turn=0;turn<turns;turn++){
     view.model.rotation.y=turn*Math.PI/4;view.model.updateMatrixWorld(true);
     view.model.traverse(o=>{if(!o.isMesh)return;const ps=o.geometry.attributes.position;for(let i=0;i<ps.count;i++){
      point.fromBufferAttribute(ps,i).applyMatrix4(o.matrixWorld).project(view.camera);
      b.left=Math.min(b.left,point.x);b.right=Math.max(b.right,point.x);b.bottom=Math.min(b.bottom,point.y);b.top=Math.max(b.top,point.y);b.near=Math.min(b.near,point.z);b.far=Math.max(b.far,point.z);b.vertices++;
     }});
    }
    return b;
   };
   const result={id};
   for(const kind of ['detail','wheel']){
    const view=r.makeView(false);
    try{r.attach(view,a,entry);if(kind==='wheel')r.wheelFrame(view,a);r.resizeCamera(view,kind==='wheel'?768:512,kind==='wheel'?432:512);result[kind]=bounds(view,kind==='wheel'?8:1);}finally{r.disposeView(view);}
   }
   return result;
  },asset.id);
  for(const kind of ['detail','wheel']){
   const b=row[kind];assert(b.vertices>0&&Object.values(b).every(Number.isFinite),`${asset.id} ${kind} invalid geometry`);
   assert(b.left>=-1.000001&&b.right<=1.000001&&b.bottom>=-1.000001&&b.top<=1.000001&&b.near>=-1&&b.far<=1,`${asset.id} ${kind} cropped: ${JSON.stringify(b)}`);
  }
  rows.push(row);console.log(`Projected geometry ${rows.length}/175: ${asset.id}`);
 }
 const samples=['cruziana-crawling-furrow',generated[0],generated[Math.floor(generated.length/4)],generated[Math.floor(generated.length/2)],generated[Math.floor(generated.length*3/4)],generated.at(-1)].filter((v,i,a)=>a.indexOf(v)===i);
 const recaptures=[];
 for(const id of samples){
  const data=await page.evaluate(async id=>{const r=window.__preview.renderer,a=window.__preview.models.find(a=>a.id===id);return {detail:await r.poster(a),wheel:await r.poster(a,{wheel:true})};},id);
  for(const kind of ['detail','wheel']){
   const path=audit.resources.posters[id][kind],actual=hash(Buffer.from(data[kind].split(',')[1],'base64')),expected=hash(await readFile(resolve('site/public',path)));
   assert.equal(actual,expected,`Sample recapture differs: ${id} ${kind}`);recaptures.push({id,kind,sha256:actual,exact_match:true});
  }
 }
 assert.deepEqual(errors,[]);
 const report={source_sha:execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),browser:browser.version(),chromium_path:process.env.CHROMIUM_PATH||'/usr/bin/chromium',gpu,renderer:'approved PreviewRenderer.poster',renderer_sha256:hash(await readFile('site/gallery/renderer.js')),capture_script_sha256:hash(await readFile('site/capture-gallery-posters.mjs')),generated_models:generated.length,generated_images:generated.length*2,published_models:manifest.assets.length,reviewed_models_preserved:Object.keys(baseline.posters).length,baseline_files_verified:baseline.files.length,coverage:audit.coverage,source_and_dist_seals:'pass',geometry_scope:'All 175 detail views and all 175 wheel views at eight 45-degree turns; actual mesh vertices in camera clip space',geometry:rows,sample_recaptures:recaptures,browser_errors:errors};
 await writeFile(resolve(qa,'browser-verification.json'),JSON.stringify(report,null,2)+'\n');
 console.log('Independent browser verification passed.');
}finally{await browser?.close();await new Promise(r=>server.close(r));}

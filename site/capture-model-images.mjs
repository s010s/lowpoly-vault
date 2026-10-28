/** Manual selected-model image generation. Outputs unreviewed pixels only;
 * never edits the catalog, site/public, acceptance records, or publication. */
import assert from 'node:assert/strict';
import {readFile,open,mkdir,realpath,stat} from 'node:fs/promises';
import {constants} from 'node:fs';
import {resolve,dirname,sep,extname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createServer} from 'node:http';
const codeRoot=resolve(dirname(fileURLToPath(import.meta.url)),'..');
export function parseCaptureArgs(args){
 assert(args.length===2&&args[0]==='--ids','Usage: node site/capture-model-images.mjs --ids model-id,other-id');
 const ids=args[1].split(',');assert(ids.length&&ids.every(id=>/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id))&&new Set(ids).size===ids.length,'Explicit unique comma-separated model IDs required');return ids;
}
export function selectCaptureAssets(manifest,ids){
 assert(Array.isArray(ids)&&ids.length&&new Set(ids).size===ids.length&&ids.every(id=>/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id)),'Explicit unique IDs required');
 assert(Array.isArray(manifest.assets),'Manifest assets required');
 return ids.map(id=>{const matches=manifest.assets.filter(a=>a.id===id);assert.equal(matches.length,1,'Unknown or ambiguous model ID: '+id);const asset=matches[0];assert(typeof asset.glb==='string'&&asset.glb.startsWith('assets/')&&asset.glb.endsWith('.glb')&&safePath(asset.glb),'Safe selected GLB required');assert(/^[a-f0-9]{64}$/.test(asset.sha256?.glb||''),'Existing source identity required by captureWheelFrame');return asset;});
}
const safePath=path=>typeof path==='string'&&path&&!/[\\\u0000-\u001f?#%:]/.test(path)&&!path.startsWith('/')&&path.split('/').every(p=>p&&p!=='.'&&p!=='..');
export async function captureRequestFile(path,{root,scriptRoot=codeRoot,threeRoot,selected}){
 assert(safePath(path),'Unsafe request path');let base,relative;
 if(selected.has(path)){base=root;relative=path;}
 else if(path.startsWith('site/')&&['.js','.mjs'].includes(extname(path))){base=scriptRoot;relative=path;}
 else if(path.startsWith('node_modules/three/')&&path.endsWith('.js')){base=threeRoot;relative=path.slice('node_modules/three/'.length);}
 else throw Error('Unselected input');
 base=await realpath(base);const full=resolve(base,relative);assert(full.startsWith(base+sep),'Request escapes workspace');assert.equal(await realpath(full),full,'Capture input symlink rejected');assert((await stat(full)).isFile());return full;
}
async function writeOutput(path,bytes){const file=await open(path,constants.O_WRONLY|constants.O_CREAT|constants.O_TRUNC|constants.O_NOFOLLOW,0o644);try{await file.writeFile(bytes);}finally{await file.close();}}
const html=`<!doctype html><meta charset="utf-8"><link rel="icon" href="data:,"><style>body{margin:0}#stage{width:512px;height:512px}.preview-renderer{position:fixed;top:0;left:0;pointer-events:none}</style><body data-site-base="/"><div id="stage"></div><script type="importmap">{"imports":{"three":"/node_modules/three/build/three.module.js","three/":"/node_modules/three/","three/addons/":"/node_modules/three/examples/jsm/"}}</script><script type="module">import {PreviewRenderer} from '/site/gallery/renderer.js';import {DetailRenderer} from '/site/gallery/detail-renderer.js';import {detailPresentationPolicy} from '/site/gallery/detail-presentation-policy.js';import {captureWheelFrame} from '/site/capture-wheel-frame.js';window.capture={PreviewRenderer,DetailRenderer,detailPresentationPolicy,captureWheelFrame};</script>`;
export async function captureModelImages({root=process.cwd(),ids,executablePath=process.env.CAPTURE_CHROMIUM_EXECUTABLE}={}){
 root=await realpath(root);const assets=selectCaptureAssets(JSON.parse(await readFile(resolve(root,'assets/manifest.json'))),ids),selected=new Set(assets.map(a=>a.glb));
 const qa=resolve(root,'qa');await mkdir(qa,{recursive:true});assert.equal(await realpath(qa),qa,'Capture output parent must remain inside workspace');
 const out=resolve(qa,'model-image-capture');await mkdir(out,{recursive:true});assert.equal(await realpath(out),out,'Capture output must remain inside workspace');
 const report={status:'running',visual_review:'NOT_REVIEWED',published:false,models:[],errors:[]};let server,browser;
 try{
  for(const asset of assets){const full=await captureRequestFile(asset.glb,{root,selected});assert((await stat(full)).size>0,'Empty selected GLB: '+asset.id);}
  const threeRoot=await realpath(resolve(codeRoot,'node_modules/three'));
  server=createServer(async(req,res)=>{try{assert(req.method==='GET');const url=new URL(req.url,'http://127.0.0.1');assert(!url.search);const path=decodeURIComponent(url.pathname).slice(1);if(!path){res.setHeader('Content-Type','text/html');res.end(html);return;}const full=await captureRequestFile(path,{root,threeRoot,selected});res.setHeader('Content-Type',extname(full)==='.glb'?'model/gltf-binary':'text/javascript');res.end(await readFile(full));}catch{res.writeHead(404);res.end('Unlisted capture input');}});
  await new Promise((ok,no)=>{server.once('error',no);server.listen(0,'127.0.0.1',ok);});const origin=`http://127.0.0.1:${server.address().port}`;
  const {chromium}=await import('playwright');browser=await chromium.launch({headless:true,...(executablePath?{executablePath}:{}),args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});report.browser=browser.version();
  for(const asset of assets){
   // One short-lived page per model keeps only selected model resources alive.
   const page=await browser.newPage({viewport:{width:512,height:512},deviceScaleFactor:1,reducedMotion:'reduce',serviceWorkers:'block'}),errors=[];
   try{
    await page.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
    page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>errors.push(r.url()+': '+r.failure()?.errorText));page.on('response',r=>{if(r.status()>=400)errors.push(r.url()+': '+r.status());});
    await page.goto(origin);await page.waitForFunction(()=>window.capture);
    const pixels=await page.evaluate(async asset=>{
     const {PreviewRenderer,DetailRenderer,detailPresentationPolicy,captureWheelFrame}=window.capture,host=document.querySelector('#stage');
     const wheelRenderer=new PreviewRenderer(host,()=>{}),wheel=await captureWheelFrame(wheelRenderer,asset);const wheelGL=wheelRenderer.renderer.getContext();if(wheelGL.isContextLost()||wheelGL.getError()!==0)throw Error('Left capture WebGL error');
     wheelRenderer.observer.disconnect();wheelRenderer.intersection.disconnect();wheelRenderer.stopHover();wheelRenderer.renderer.domElement.remove();wheelRenderer.renderer.dispose();
     const r=new DetailRenderer(host,()=>{}),model={...asset,detailPresentation:detailPresentationPolicy(1536)};
     if(!await r.select(model))throw Error('Right model selection failed');const v=r.detail,c=v.camera,near=c.near,far=c.far;
     c.clearViewOffset();c.aspect=1;c.updateProjectionMatrix();r.renderer.setPixelRatio(1);r.renderer.setSize(1536,1536,false);r.renderer.setScissorTest(false);r.renderer.setViewport(0,0,1536,1536);r.renderer.setClearColor(0,0);r.renderer.clear(true,true,true);v.shadowViewport.value.set(0,0,1536,1536);r.renderer.render(v.scene,c);
     const gl=r.renderer.getContext();if(gl.isContextLost()||gl.getError()!==0||c.near!==near||c.far!==far)throw Error('Right capture failed');
     return {wheel:wheel.dataURL,detail:r.renderer.domElement.toDataURL('image/png')};
    },asset);
    assert.deepEqual(errors,[],'Capture resource/page errors');const directory=resolve(out,asset.id);await mkdir(directory,{recursive:true});assert.equal(await realpath(directory),directory,'Capture output symlink rejected');
    for(const role of ['wheel','detail']){assert(pixels[role].startsWith('data:image/png;base64,'));const bytes=Buffer.from(pixels[role].split(',')[1],'base64');assert(bytes.length>0);await writeOutput(resolve(directory,role+'.png'),bytes);}
    report.models.push({id:asset.id,glb:asset.glb,wheel:asset.id+'/wheel.png',detail:asset.id+'/detail.png'});console.log('Captured unreviewed images:',asset.id);
   }finally{await page.close();}
  }report.status='CAPTURED_NOT_REVIEWED';return report;
 }catch(error){report.status='FAILED';report.errors.push(error.message);throw error;}
 finally{await browser?.close();if(server)await new Promise(ok=>server.close(ok));await writeOutput(resolve(out,'report.json'),JSON.stringify(report,null,2)+'\n');}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)await captureModelImages({ids:parseCaptureArgs(process.argv.slice(2))});

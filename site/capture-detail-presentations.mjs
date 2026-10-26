/** Capture only right-hand delivery overrides. Production evidence and left pixels are immutable. */
import assert from 'node:assert/strict';
import {assertDetailV2Migration} from './detail-capture-scope.mjs';
import {compareDetailPNGs} from './detail-pixels.mjs';
import {DETAIL_HIRES_METHOD,detailPresentationPolicy,detailCapturePolicy} from './gallery/detail-presentation-policy.js';
import {createHash} from 'node:crypto';
import {createServer} from 'node:http';
import {readFile,writeFile,mkdir,realpath} from 'node:fs/promises';
import {resolve,dirname,extname,sep} from 'node:path';
import {chromium} from 'playwright';
import previousIndex from './gallery/detail-presentations-index.js';
import {CAPTURE_POLICY,posterRendererFiles} from './gallery-poster-inputs.mjs';
const root=process.cwd(),out=resolve(process.env.DETAIL_CAPTURE_OUTPUT||'qa/detail-capture'),sha=b=>createHash('sha256').update(b).digest('hex');
const revision=Number(process.env.DETAIL_CAPTURE_REVISION||1);assert([1,2].includes(revision),'Unknown detail capture revision');
const rasterSize=revision===2?Number(process.env.DETAIL_CAPTURE_SIZE):512,presentation=revision===2?detailPresentationPolicy(rasterSize):null;
const manifest=JSON.parse(await readFile('assets/manifest.json')),resources=JSON.parse(await readFile('site/public/gallery/resources.json'));
const routes=new Set(['blender-cycles-cpu-v1','blender-detail-preview-wheel-v1']);
const assets=manifest.assets.filter(a=>routes.has(resources.posters[a.id]?.render_route));
const expectedCount=Number(process.env.DETAIL_EXPECTED_COUNT||250);assert(Number.isSafeInteger(expectedCount)&&expectedCount>0);assert.equal(assets.length,expectedCount,'Runtime delivery scope differs from explicitly expected catalog count');
const smokeIds=process.env.DETAIL_CAPTURE_IDS?.split(',').filter(Boolean);
const migration=process.env.DETAIL_CAPTURE_MIGRATION_V2==='1';
assert(!migration||revision===2,'Migration requires explicit revision2');
const migrationScope=migration?assertDetailV2Migration({scopeBytes:await readFile('qa/detail-presentation-scope-20261025.json'),assets,ids:smokeIds,presentation,smoke:process.env.DETAIL_CAPTURE_CANDIDATE_SMOKE==='1'}):null;
const incremental=process.env.DETAIL_CAPTURE_INCREMENTAL_V2==='1';assert(!incremental||(revision===2&&!migration&&process.env.DETAIL_CAPTURE_CANDIDATE_SMOKE!=='1'&&smokeIds?.length>0&&new Set(smokeIds).size===smokeIds.length&&rasterSize===1536),'Invalid explicit incremental v2 selection');
if(revision===2&&!migration&&!incremental){assert.equal(process.env.DETAIL_CAPTURE_CANDIDATE_SMOKE,'1','Revision-2 core is candidate-smoke only');assert(smokeIds,'Explicit candidate IDs required');assert.deepEqual([...smokeIds].sort(),['onoclea','pertica','azolla','sidneyia','arroyo-wash'].sort(),'Revision-2 core permits only the reviewed five-model probe');}
const files=[...await posterRendererFiles(root),'package-lock.json','site/capture-detail-presentations.mjs','site/detail-pixels.mjs',...(revision===2?['site/gallery/detail-renderer.js','site/gallery/detail-presentation-policy.js','site/detail-capture-scope.mjs']:[])].sort();
const inputs=await Promise.all(files.map(async path=>({path,sha256:sha(await readFile(path))})));
const toolchain=JSON.parse(await readFile('node_modules/playwright-core/browsers.json')),expectedBrowser=toolchain.browsers.find(b=>b.name==='chromium').browserVersion;
const rendererPolicy=detailCapturePolicy(CAPTURE_POLICY,presentation),rendererKey=sha(JSON.stringify({files:inputs,policy:rendererPolicy,browser:expectedBrowser}));
const reuseCandidate=a=>{const e=previousIndex.presentations?.[a.id],p=resources.posters[a.id];return e?.detail===`detail-presentations/${a.id}.png`&&e.capture?.first_frame?.path===`qa/detail-presentation-evidence/first-frames/${a.id}.png`&&e.source_glb_sha256===a.sha256.glb&&e.capture?.renderer_input_sha256===rendererKey&&e.production_descriptor===a.production_release&&e.previous_detail?.path===p.detail&&resources.files.some(f=>f.path===p.detail&&f.sha256===e.previous_detail.sha256);};
const reuseIds=new Set();for(const a of assets){if(!reuseCandidate(a))continue;const e=previousIndex.presentations[a.id];try{const png=await readFile(resolve('site/public',e.detail)),first=await readFile(e.capture.first_frame.path);if(png.length===e.png.bytes&&sha(png)===e.png.sha256&&first.length===e.capture.first_frame.bytes&&sha(first)===e.capture.first_frame.sha256)reuseIds.add(a.id);}catch{/* Missing proof requires a fresh runtime capture. */}}const reusable=a=>reuseIds.has(a.id);
const selected=smokeIds?assets.filter(a=>smokeIds.includes(a.id)):assets.filter(a=>!reusable(a));if(smokeIds)assert.equal(selected.length,new Set(smokeIds).size,'Unknown smoke IDs');
const allowed=new Set(files),glbs=new Map(assets.map(a=>[a.glb,a.sha256.glb]));
for(const a of assets){assert.equal(sha(await readFile(a.glb)),a.sha256.glb,a.id);assert.equal(resources.posters[a.id].source_glb_sha256,a.sha256.glb,a.id);}
const html=`<!doctype html><link rel="icon" href="data:,"><body data-site-base="/" style="margin:0"><div id="stage" style="width:512px;height:512px"></div><script type="importmap">${JSON.stringify({imports:{three:'/node_modules/three/build/three.module.js','three/':'/node_modules/three/','three/addons/':'/node_modules/three/examples/jsm/'}})}</script><script type="module">import {${revision===2?'DetailRenderer as ':''}PreviewRenderer} from '/site/gallery/${revision===2?'detail-renderer':'renderer'}.js';window.capture={renderer:new PreviewRenderer(document.querySelector('#stage'),()=>{}),models:await (await fetch('/capture-models.json')).json()};</script>`;
const mime={'.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png'};
let browser;const server=createServer(async(req,res)=>{try{const path=decodeURIComponent(new URL(req.url,'http://localhost').pathname).slice(1);if(path===''){res.setHeader('Content-Type','text/html');res.end(html);return;}if(path==='capture-models.json'){res.setHeader('Content-Type','application/json');res.end(JSON.stringify(assets.map(a=>presentation?{...a,detailPresentation:presentation}:a)));return;}
assert(allowed.has(path)||glbs.has(path)||/^node_modules\/three\/[a-zA-Z0-9_./-]+\.js$/.test(path));const file=await realpath(resolve(root,path));assert.equal(file,resolve(root,path));assert(file.startsWith(root+sep));const bytes=await readFile(file);if(glbs.has(path))assert.equal(sha(bytes),glbs.get(path));res.setHeader('Content-Type',mime[extname(path)]||'application/octet-stream');res.end(bytes);}catch(e){res.statusCode=404;res.end('Unlisted or invalid capture input');}});
const index={version:1,kind:'detail-only-presentations',...(presentation?{renderer_policy:rendererPolicy}:{}),...(migrationScope?{migration_scope:migrationScope}:{}),renderer_input_sha256:rendererKey,source_commit:process.env.GITHUB_SHA||null,browser_version:expectedBrowser,renderer_files:inputs,source_manifest_sha256:sha(await readFile('assets/manifest.json')),source_resources_sha256:sha(await readFile('site/public/gallery/resources.json')),source_wheel_index_sha256:sha(await readFile('site/gallery/wheel-presentations-index.js')),presentations:smokeIds?{}:Object.fromEntries(assets.filter(reusable).map(a=>[a.id,previousIndex.presentations[a.id]]))};
try{assert.equal(process.versions.node.split('.')[0],CAPTURE_POLICY.node_major);await mkdir(out,{recursive:true});await new Promise(ok=>server.listen(0,'127.0.0.1',ok));const origin=`http://127.0.0.1:${server.address().port}`;
browser=await chromium.launch({headless:true,args:CAPTURE_POLICY.args});assert.equal(browser.version(),expectedBrowser);
const page=await browser.newPage({viewport:{width:512,height:512},deviceScaleFactor:1,reducedMotion:'reduce',serviceWorkers:'block'}),errors=[];
await page.route('**/*',r=>new URL(r.request().url()).origin===origin?r.continue():r.abort());page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push('Missing capture input '+r.url());});page.on('requestfailed',r=>errors.push('Failed capture input '+r.url()));page.on('console',m=>{if(m.type()==='error'&&/THREE\.|WebGL|shader|GL_INVALID|CONTEXT_LOST/i.test(m.text()))errors.push(m.text());});await page.goto(origin);await page.waitForFunction(n=>window.capture?.models.length===n,assets.length);
for(const asset of selected){const data=await page.evaluate(async ({id,rasterSize})=>{
 const {renderer:r,models}=window.capture,a=models.find(a=>a.id===id),gl=r.renderer.getContext();
 const legacy=await r.poster(a),natives=[],acknowledge=r.acknowledgeDetailFrame,geometry=[];
 const geometryBounds=label=>{const c=r.detail.camera,v=r.detail.model,point=c.position.clone();c.updateMatrixWorld(true);v.updateMatrixWorld(true);let vertices=0,minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity,minZ=Infinity,maxZ=-Infinity;
  v.traverse(mesh=>{if(!mesh.isMesh)return;const p=mesh.geometry.attributes.position;for(let i=0;i<p.count;i++){point.fromBufferAttribute(p,i).applyMatrix4(mesh.matrixWorld).project(c);if(![point.x,point.y,point.z].every(Number.isFinite))throw Error('Nonfinite geometry projection');vertices++;minX=Math.min(minX,point.x);maxX=Math.max(maxX,point.x);minY=Math.min(minY,point.y);maxY=Math.max(maxY,point.y);minZ=Math.min(minZ,point.z);maxZ=Math.max(maxZ,point.z);}});
  const margin=Math.min(1+minX,1-maxX,1+minY,1-maxY)/2;if(!vertices||margin<=0||minZ < -1||maxZ>1)throw Error('Geometry clipped '+label);
  if(a.detailPresentation&&label==='native'&&margin<a.detailPresentation.minimum_margin-1e-7)throw Error('Native detail safe margin violated');geometry.push({label,vertices,min_x:minX,max_x:maxX,min_y:minY,max_y:maxY,min_z:minZ,max_z:maxZ,minimum_square_margin:margin});
 };
 r.acknowledgeDetailFrame=function(){
  const pending=this.firstDetailFrame;
  if(pending&&!pending.frame&&pending.token===this.token&&pending.id===this.detail.asset?.id&&this.detailPresentable()&&!natives.some(n=>n.token===pending.token)){
   const c=this.detail.camera;
   if(a.detailPresentation)geometryBounds('native');
   natives.push({id:pending.id,token:pending.token,png:this.renderer.domElement.toDataURL('image/png'),camera:{near:c.near,far:c.far,aspect:c.aspect,fov:c.fov,zoom:c.zoom,position:c.position.toArray(),quaternion:c.quaternion.toArray(),projection:c.projectionMatrix.toArray(),view:c.view?structuredClone(c.view):null},gl_error:gl.getError()});
  }
  return acknowledge.call(this);
 };
 const square=()=>{
  const v=r.detail,c=v.camera,near=c.near,far=c.far;
  // Delivery adapter removes only UI positioning/aspect. Native singleState
  // clip planes, model transforms, materials, lights and shadows stay intact.
  c.clearViewOffset();c.aspect=1;c.updateProjectionMatrix();if(a.detailPresentation)geometryBounds('delivery-square');
  r.renderer.setPixelRatio(1);r.renderer.setSize(rasterSize,rasterSize,false);r.renderer.setScissorTest(false);r.renderer.setViewport(0,0,rasterSize,rasterSize);r.renderer.setClearColor(0,0);r.renderer.clear(true,true,true);v.shadowViewport.value.set(0,0,rasterSize,rasterSize);r.renderer.render(v.scene,c);
  if(c.near!==near||c.far!==far)throw Error('Native clipping changed');
  return r.renderer.domElement.toDataURL('image/png');
 };
 let detail,first;
 try{
  if(!await r.select(a))throw Error('First select did not present');detail=square();
  // Restore normal buffer/view presentation before a genuinely fresh selection.
  r.draw();if(!await r.select(a))throw Error('Second select did not present');first=square();
 }finally{r.acknowledgeDetailFrame=acknowledge;r.draw();}
 if(gl.isContextLost())throw Error('WebGL lost');
 if(natives.length!==2||natives[0].token===natives[1].token||natives.some(n=>n.id!==id||n.gl_error!==0))throw Error('Native first-frame capture ownership failed');
const decode=async src=>{const img=new Image();img.src=src;await img.decode();const c=document.createElement('canvas');c.width=c.height=rasterSize;const ctx=c.getContext('2d');ctx.drawImage(img,0,0);return ctx.getImageData(0,0,rasterSize,rasterSize).data;};const left=await decode(detail),right=await decode(first);let different=0,max=0,maskUnion=0,maskIntersection=0;for(let i=0;i<left.length;i+=4){let d=0;for(let k=0;k<4;k++){const e=Math.abs(left[i+k]-right[i+k]);d=Math.max(d,e);max=Math.max(max,e);}if(d)different++;const a=left[i+3]>32,b=right[i+3]>32;if(a||b)maskUnion++;if(a&&b)maskIntersection++;}return {detail,first,legacy,natives,geometry,checks:{different_pixels:different,max_channel_error:max,mask_iou:maskIntersection/Math.max(1,maskUnion),gl_error:gl.getError(),first_frame_id:r.stats.detailFirstFrameId}};},{id:asset.id,rasterSize});
const nativePins=[];for(const [n,native] of data.natives.entries()){const bytes=Buffer.from(native.png.split(',')[1],'base64'),name=asset.id+(n?'-repeat':'-first')+'.png';await mkdir(resolve(out,'native-frames'),{recursive:true});await writeFile(resolve(out,'native-frames',name),bytes);nativePins.push({path:'qa/detail-presentation-evidence/native-frames/'+name,bytes:bytes.length,sha256:sha(bytes),id:native.id,token:native.token,camera:native.camera,gl_error:native.gl_error,method:'Unmodified canvas before acknowledgeDetailFrame'});}
// Preserve raw smoke pixels before any acceptance assertion; these are diagnostics, not approved output.
if((smokeIds&&!migration&&!incremental)||errors.length||data.checks.gl_error!==0||data.checks.mask_iou<=.999||data.checks.different_pixels>=100){const diagnostic=resolve(out,'diagnostics',asset.id);await mkdir(diagnostic,{recursive:true});await writeFile(resolve(diagnostic,'detail.png'),Buffer.from(data.detail.split(',')[1],'base64'));await writeFile(resolve(diagnostic,'normalized-selected.png'),Buffer.from(data.first.split(',')[1],'base64'));await writeFile(resolve(diagnostic,'legacy-canonical-poster.png'),Buffer.from(data.legacy.split(',')[1],'base64'));await writeFile(resolve(diagnostic,'checks.json'),JSON.stringify({status:'unreviewed-diagnostic',source_commit:process.env.GITHUB_SHA||null,id:asset.id,errors,checks:data.checks},null,2));}
assert.equal(errors.length,0,errors.join('; '));assert.equal(data.checks.gl_error,0);assert.equal(data.checks.first_frame_id,asset.id);assert(data.checks.mask_iou>.999,'Detail silhouette mismatch '+asset.id);assert(data.checks.different_pixels<100,'Detail raster mismatch '+asset.id+': '+JSON.stringify(data.checks));
const png=Buffer.from(data.detail.split(',')[1],'base64'),first=Buffer.from(data.first.split(',')[1],'base64'),poster=resources.posters[asset.id],old=await readFile(resolve('site/public',poster.detail));assert(resources.files.some(f=>f.path===poster.detail&&f.sha256===sha(old)),'Old detail seal mismatch '+asset.id);
const browserCanvasChecks=data.checks;data.checks={...data.checks,...compareDetailPNGs(png,first)};if(data.checks.mask_iou<=.999||data.checks.different_pixels>=100){const diagnostic=resolve(out,'diagnostics',asset.id);await mkdir(diagnostic,{recursive:true});await writeFile(resolve(diagnostic,'detail.png'),png);await writeFile(resolve(diagnostic,'normalized-selected.png'),first);await writeFile(resolve(diagnostic,'decoded-checks.json'),JSON.stringify({status:'unreviewed-diagnostic',id:asset.id,checks:data.checks},null,2));}assert(data.checks.mask_iou>.999&&data.checks.different_pixels<100,'Decoded PNG raster mismatch '+asset.id);
const path=`detail-presentations/${asset.id}.png`;await mkdir(dirname(resolve(out,path)),{recursive:true});await writeFile(resolve(out,path),png);await mkdir(resolve(out,'first-frames'),{recursive:true});await writeFile(resolve(out,'first-frames',asset.id+'.png'),first);
index.presentations[asset.id]={id:asset.id,source_glb_sha256:asset.sha256.glb,production_descriptor:asset.production_release,previous_detail:{path:poster.detail,sha256:sha(old)},detail:path,png:{bytes:png.length,sha256:sha(png),width:rasterSize,height:rasterSize},capture:{source_commit:process.env.GITHUB_SHA||null,detail_sha256:sha(png),source_glb_sha256:asset.sha256.glb,first_frame_id:asset.id,renderer_input_sha256:rendererKey,method:revision===2?DETAIL_HIRES_METHOD:'PreviewRenderer.select(detail)/canonical-square-native-clipping-v1',...(presentation?{presentation,geometry_validation:data.geometry}:{}),native_frames:nativePins,first_frame:{path:`qa/detail-presentation-evidence/first-frames/${asset.id}.png`,bytes:first.length,sha256:sha(first)},checks:data.checks,browser_canvas_checks:browserCanvasChecks}};await writeFile(resolve(out,'capture-progress.json'),JSON.stringify({captured:Object.keys(index.presentations).length,total:assets.length,id:asset.id}));console.log('PASS detail',asset.id,JSON.stringify(data.checks));}
await writeFile(resolve(out,'detail-presentations-index.js'),'export default '+JSON.stringify(index)+';\n');await writeFile(resolve(out,'capture-report.json'),JSON.stringify({status:'pass',smoke_only:!!smokeIds&&!migration,...(migrationScope?{scope_kind:migrationScope.kind,scope_sha256:migrationScope.sha256}:{}),captured:selected.length,reused:smokeIds?0:assets.length-selected.length,count:Object.keys(index.presentations).length,source_commit:index.source_commit,renderer_input_sha256:rendererKey,scope:'Native-clipping selected-scene square delivery and fresh-select reproducibility; untouched native first canvases retained; actual built-page CSS/native-frame parity remains a separate mandatory gate',left_modified:false,ordinary_detail_modified:false},null,2));
}finally{await browser?.close();server.close();}

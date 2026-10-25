/** Synthetic fixtures test rejection paths only, never claim a real browser/visual approval. */
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,mkdtemp,rm,copyFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {tmpdir} from 'node:os';
import {fileURLToPath} from 'node:url';
import {wheelHash} from './wheel-presentation-contract.mjs';
import {PRODUCTION_WHEEL_ROUTE,PRODUCTION_WHEEL_CHECKS,productionWheelAsset,productionWheelRenderer,createProductionWheel,assertProductionWheel,verifyProductionWheel} from './production-wheel-contract.mjs';
import {verifyProductionPosters,productionGalleryResources,appendProductionPosterInputState} from './production-release.mjs';
import {resolveGalleryPoster} from './gallery/wheel-presentations.js';
const codeRoot=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const png=(w,h)=>{const b=Buffer.alloc(40);Buffer.from('89504e470d0a1a0a','hex').copy(b);b.write('IHDR',12);b.writeUInt32BE(w,16);b.writeUInt32BE(h,20);b[24]=8;b[25]=6;return b;};
const sourceGLB=Buffer.from('TEST ONLY source, not a GLB'),wheel=png(768,432),detail=png(512,512);
const wheelSpec={azimuth:42,elevation:40,zoom:1.3,aspect:16/9,offset:[2,-3],floorCenter:[.5,.8],floorPoints:[[.3,.7],[.5,.9],[.7,.7]],projectedBounds:{left:-.7,right:.7,top:.6,bottom:-.6}};
const renderer=await productionWheelRenderer(codeRoot);
function captureInputs(asset){return {asset,sourceGLB,png:wheel,unchangedDetail:detail,rendererSha256:renderer.sha256,browserVersion:renderer.browser,frame:{id:asset.id,source_glb_sha256:asset.sha256.glb,dataURL:`data:image/png;base64,${wheel.toString('base64')}`,wheelSpec}};}
async function fixture(){
 const root=await mkdtemp(resolve(tmpdir(),'new-production-wheel-'));
 async function put(path,data){data=Buffer.isBuffer(data)?data:Buffer.from(typeof data==='string'?data:JSON.stringify(data));await mkdir(dirname(resolve(root,path)),{recursive:true});await writeFile(resolve(root,path),data);return {path,bytes:data.length,sha256:wheelHash(data)};}
 for(const {path} of renderer.files){await mkdir(dirname(resolve(root,path)),{recursive:true});await copyFile(resolve(codeRoot,path),resolve(root,path));}
 await put('node_modules/playwright-core/browsers.json',await readFile(resolve(codeRoot,'node_modules/playwright-core/browsers.json')));
 const glb=await put('assets/test-only/model.glb',sourceGLB),detailPin=await put('site/public/gallery/posters/test-only.png',detail),wheelPin=await put('site/public/gallery/posters/test-only-wheel.png',wheel);
 const asset={id:'test-only',glb:glb.path,sha256:{glb:glb.sha256},dimensions:[1,.2,1],units:'meters',production_release:'production/test/release.json'};
 const capture=createProductionWheel(captureInputs(asset));const capturePin=await put('qa/capture.json',capture);
 const report={version:1,kind:'new-production-wheel-capture-evidence',producer:{id:'capture-maker',task_id:'capture-task'},status:'capture-and-geometry-check-pass',publication_authority:false,visual_review:'pending',physical_gpu:'unknown',renderer_sha256:renderer.sha256,renderer_files:renderer.files,browser_version:renderer.browser,errors:[],cases:[{id:asset.id,source_glb_sha256:glb.sha256,wheel_sha256:wheelPin.sha256,first_frame_id:asset.id,spec:wheelSpec,status:'geometry-check-pass',context_lost:false,gl_error:0,mask_iou:1,mean_rgb_absolute_error:0,lifecycle:{context_lost:false,gl_error:0,reentry_exact:true,frames:[0,45,90,135,180,225,270,315].map(yaw=>({yaw,border_opaque_pixels:0}))}}]};const reportPin=await put('qa/report.json',report);
 const review={version:1,kind:'independent-production-wheel-review',status:'PASS',reviewer:{id:'reviewer',task_id:'review-task'},reviewed_capture_sha256:capturePin.sha256,reviewed_report_sha256:reportPin.sha256,source_glb_sha256:glb.sha256,wheel_sha256:wheelPin.sha256,checks:Object.fromEntries(PRODUCTION_WHEEL_CHECKS.map(k=>[k,'PASS'])),blocking_findings:[],publication_authority:false,physical_gpu:'unknown'};const reviewPin=await put('qa/review.json',review);
 const recipeFile=await put('qa/detail-renderer.py','TEST ONLY renderer');const recipe=await put('qa/detail-recipe.json',{source_glb_sha256:glb.sha256,blender_version:'TEST ONLY',rendered_unchanged_source:true,files:[recipeFile]});const config=await put('qa/detail-config.json',{source_geometry_and_materials_unchanged:true,film_transparent:true,version:'TEST ONLY',renderer_sha256:recipeFile.sha256,resolution:[512,512]});
 const record={asset_id:asset.id,maker:{id:'source-maker',task_id:'source-task'},final_posters:{route:PRODUCTION_WHEEL_ROUTE,source_glb_sha256:glb.sha256,browser_capture:true,blender_version:'TEST ONLY',recipe,recipe_sha256:recipe.sha256,detail:{...detailPin,source_glb_sha256:glb.sha256,render_config:config,camera_degrees:[42,23.3],pixel_sha256:'a'.repeat(64)},wheel:{...wheelPin,source_glb_sha256:glb.sha256,render_config:capturePin,capture_report:reportPin,visual_review:reviewPin,renderer_sha256:renderer.sha256,browser_version:renderer.browser,wheelSpec}}};
 asset.production_posters={route:PRODUCTION_WHEEL_ROUTE,detail:detailPin.path,wheel:wheelPin.path};return {root,put,asset,record,capture,report,review};
}
await test('new wheel separate route and negative boundaries',async t=>{
 const f=await fixture();const run=()=>verifyProductionPosters(f.root,f.asset,f.record);
 try{
  await t.test('unchanged-source detail plus browser wheel accepted without a previous wheel',async()=>{await run();assert.equal(f.capture.kind,'unreviewed-new-production-wheel');assert(!('previous_wheel_sha256'in f.capture));assert.equal(f.capture.visual_review,'pending');assert.equal(f.capture.physical_gpu,'unknown');});
  await t.test('minimal capture input never inherits an old wheelSpec',()=>{const asset={...f.asset,wheelSpec:{stale:true},name:{en:'label'}};assert.deepEqual(productionWheelAsset(asset),productionWheelAsset(f.asset));assert(!('wheelSpec'in productionWheelAsset(asset)));});
  for(const [name,change]of [['source bytes',i=>i.sourceGLB=Buffer.from('changed')],['detail bytes',i=>i.unchangedDetail=Buffer.from('changed')],['dimensions',i=>i.asset.dimensions[1]=.9],['renderer',i=>i.rendererSha256='f'.repeat(64)],['browser',i=>i.browserVersion='142.0.0.0']])await t.test(name+' cannot inherit capture',()=>{const inputs=captureInputs(structuredClone(f.asset));change(inputs);assert.throws(()=>assertProductionWheel(f.capture,inputs));});
  async function mutateJSON(field,value,change){const old=f.record.final_posters.wheel[field],data=structuredClone(value);change(data);try{f.record.final_posters.wheel[field]=await f.put('qa/mutated-'+field+'.json',data);await assert.rejects(run);}finally{f.record.final_posters.wheel[field]=old;}}
  for(const [name,change]of [['maker as reviewer',r=>r.reviewer=f.record.maker],['capture producer as reviewer',r=>r.reviewer=f.report.producer],['pending review',r=>r.status='PENDING'],['changed report review binding',r=>r.reviewed_report_sha256='f'.repeat(64)],['changed capture review binding',r=>r.reviewed_capture_sha256='f'.repeat(64)],['failed visual review',r=>r.checks.visual_presentation='FAIL'],['missing visual review',r=>delete r.checks.visual_presentation],['blocked finding',r=>r.blocking_findings=['bad']],['GPU claim',r=>r.physical_gpu='pass']])await t.test(name+' rejected',()=>mutateJSON('visual_review',f.review,change));
  for(const [name,change]of [['missing case',r=>r.cases=[]],['duplicate case',r=>r.cases.push(r.cases[0])],['wrong live asset',r=>r.cases[0].first_frame_id='other'],['poor parity',r=>r.cases[0].mask_iou=.1],['clipping',r=>r.cases[0].lifecycle.frames[2].border_opaque_pixels=1],['missing yaw',r=>r.cases[0].lifecycle.frames.pop()],['changed renderer files',r=>r.renderer_files[0].sha256='f'.repeat(64)],['no reentry',r=>r.cases[0].lifecycle.reentry_exact=false]])await t.test(name+' rejected before review binding',()=>mutateJSON('capture_report',f.report,change));
  for(const [name,change]of [['wrong route',p=>p.route='webgl'],['browser capture denied',p=>p.browser_capture=false],['stale spec',p=>p.wheel.wheelSpec={...wheelSpec,zoom:2}],['wrong recipe',p=>p.recipe_sha256='f'.repeat(64)]])await t.test(name+' rejected',async()=>{const saved=f.record.final_posters;try{f.record.final_posters=structuredClone(saved);change(f.record.final_posters);await assert.rejects(run);}finally{f.record.final_posters=saved;}});
  await t.test('resource selection propagates exact wheelSpec and retains legacy pixels',async()=>{
   const old={version:1,posters:{old:{wheel:'unchanged'}},files:[]},results=new Map([[f.asset.production_release,{assets:[f.asset],records:[f.record]}]]),manifest={assets:[f.asset]};
   const resources=await productionGalleryResources(f.root,manifest,old,results);assert.deepEqual(resources.posters.old,old.posters.old);assert.deepEqual(resources.posters[f.asset.id].wheelSpec,wheelSpec);assert.deepEqual(resolveGalleryPoster(f.asset,resources),resources.posters[f.asset.id]);
   const legacy={valid:['old'],capture:['old-pending']};const state=await appendProductionPosterInputState(f.root,[f.asset],resources,legacy,results);assert.deepEqual(state.capture,legacy.capture);assert.deepEqual(state.valid,['old',f.asset.id]);
   const tampered=structuredClone(resources);tampered.posters[f.asset.id].wheelSpec.zoom=2;await assert.rejects(()=>appendProductionPosterInputState(f.root,[f.asset],tampered,legacy,results));
  });
  await t.test('original Blender pair route still works, not silently upgraded',async()=>{
   const old=structuredClone(f.record),p=old.final_posters;p.route='blender-cycles-cpu-v1';p.browser_capture=false;const config=JSON.parse(await readFile(resolve(f.root,p.detail.render_config.path)));config.resolution=[768,432];p.wheel={...p.wheel,render_config:await f.put('qa/legacy-wheel-config.json',config),camera_degrees:[42,23.3],pixel_sha256:'a'.repeat(64)};const asset={...f.asset,production_posters:{...f.asset.production_posters,route:p.route}};await verifyProductionPosters(f.root,asset,old);
  });
 }finally{await rm(f.root,{recursive:true,force:true});}
});

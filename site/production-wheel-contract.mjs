/** New-only browser wheel evidence; never rewrites the 242 historical captures. */
import assert from 'node:assert/strict';
import {readFile,realpath} from 'node:fs/promises';
import {resolve,sep} from 'node:path';
import {assertWheelSpec,assertWheelPNG,wheelHash} from './wheel-presentation-contract.mjs';
import {posterRendererFiles} from './gallery-poster-inputs.mjs';
export const PRODUCTION_WHEEL_ROUTE='blender-detail-preview-wheel-v1';
export const PRODUCTION_WHEEL_CHECKS=['same_source_detail','first_frame_parity','hover_reentry','turntable_no_clipping','visual_presentation'];
const hash=value=>typeof value==='string'&&/^[a-f0-9]{64}$/.test(value);
export async function productionWheelBytes(root,path){
 assert(typeof path==='string'&&!/[\\\u0000-\u001f?#%]/.test(path)&&!path.startsWith('/')&&path.split('/').every(p=>p&&p!=='.'&&p!=='..'),'Unsafe wheel evidence path');
 const file=resolve(root,path);assert(file.startsWith(resolve(root)+sep));assert.equal(await realpath(file),file,'Wheel evidence symlink');return readFile(file);
}
export async function productionWheelPin(root,pin){
 assert(hash(pin?.sha256)&&Number.isSafeInteger(pin.bytes)&&pin.bytes>0,'Exact wheel evidence pin required');const data=await productionWheelBytes(root,pin.path);assert.equal(data.length,pin.bytes,'Wheel evidence bytes changed');assert.equal(wheelHash(data),pin.sha256,'Wheel evidence hash changed');return data;
}
/** Capture exactly this minimal input, including dimensions which affect the initial pose. */
export function productionWheelAsset(asset){
 assert(/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(asset?.id||''));assert(hash(asset.sha256?.glb));
 assert(typeof asset.glb==='string'&&asset.glb.startsWith('assets/'));
 assert(Array.isArray(asset.dimensions)&&asset.dimensions.length===3&&asset.dimensions.every(n=>Number.isFinite(n)&&n>=0));
 return {id:asset.id,glb:asset.glb,sha256:{glb:asset.sha256.glb},dimensions:[...asset.dimensions],...(asset.units===undefined?{}:{units:asset.units})};
}
export async function productionWheelRenderer(root){
 const paths=[...new Set([...await posterRendererFiles(root),'site/capture-wheel-frame.js','package-lock.json'])].sort();
 const files=await Promise.all(paths.map(async path=>({path,sha256:wheelHash(await productionWheelBytes(root,path))})));
 const browser=JSON.parse(await readFile(resolve(root,'node_modules/playwright-core/browsers.json'))).browsers.find(b=>b.name==='chromium').browserVersion;
 return {files,sha256:wheelHash(JSON.stringify(files)),browser};
}
export function createProductionWheel({frame,png,asset,sourceGLB,unchangedDetail,rendererSha256,browserVersion}){
 const input=productionWheelAsset(asset);assert.equal(frame?.id,asset.id);assert.equal(frame.source_glb_sha256,input.sha256.glb);assert.equal(wheelHash(sourceGLB),input.sha256.glb);
 assert(Buffer.isBuffer(unchangedDetail)&&unchangedDetail.length>0);assert(hash(rendererSha256));assert(/^\d+\.\d+\.\d+\.\d+$/.test(browserVersion||''));
 assert.equal(frame.dataURL,`data:image/png;base64,${png.toString('base64')}`);
 const record={version:1,kind:'unreviewed-new-production-wheel',publication_authority:false,id:asset.id,source_glb_sha256:input.sha256.glb,render_asset:input,unchanged_detail_sha256:wheelHash(unchangedDetail),renderer_sha256:rendererSha256,browser_version:browserVersion,wheelSpec:structuredClone(assertWheelSpec(frame.wheelSpec)),png:{bytes:png.length,sha256:wheelHash(png)},visual_review:'pending',physical_gpu:'unknown'};
 assertWheelPNG(png,record.png);return record;
}
export function assertProductionWheel(record,inputs){
 assert.deepEqual(record,createProductionWheel({...inputs,frame:{id:record?.id,source_glb_sha256:record?.source_glb_sha256,dataURL:`data:image/png;base64,${inputs.png.toString('base64')}`,wheelSpec:record?.wheelSpec}}),'New production wheel binding changed');return record;
}
function identity(x){assert(x&&typeof x.id==='string'&&x.id.trim()&&typeof x.task_id==='string'&&x.task_id.trim(),'Wheel reviewer/producer identity missing');}
function independent(a,b){identity(a);identity(b);assert.notEqual(a.id.trim().toLowerCase(),b.id.trim().toLowerCase(),'Wheel reviewer must be independent');assert.notEqual(a.task_id.trim().toLowerCase(),b.task_id.trim().toLowerCase(),'Wheel reviewer task must be independent');}
export function assertProductionWheelReview(review,{capturePin,reportPin,asset,pngPin,maker,producer}){
 assert.equal(review?.version,1);assert.equal(review.kind,'independent-production-wheel-review');assert.equal(review.status,'PASS');
 assert.equal(review.reviewed_capture_sha256,capturePin.sha256);assert.equal(review.reviewed_report_sha256,reportPin.sha256);assert.equal(review.source_glb_sha256,asset.sha256.glb);assert.equal(review.wheel_sha256,pngPin.sha256);
 independent(review.reviewer,maker);independent(review.reviewer,producer);
 assert.deepEqual(Object.keys(review.checks||{}).sort(),PRODUCTION_WHEEL_CHECKS.slice().sort());for(const key of PRODUCTION_WHEEL_CHECKS)assert.equal(review.checks[key],'PASS');
 assert.deepEqual(review.blocking_findings,[]);assert.equal(review.publication_authority,false);assert.equal(review.physical_gpu,'unknown');return review;
}
export function assertProductionWheelCase(result,{asset,pngPin,wheelSpec}){
 assert.equal(result?.id,asset.id);assert.equal(result.source_glb_sha256,asset.sha256.glb);assert.equal(result.wheel_sha256,pngPin.sha256);assert.equal(result.first_frame_id,asset.id);assert.deepEqual(result.spec,wheelSpec);
 assert.equal(result.status,'geometry-check-pass');assert.equal(result.context_lost,false);assert.equal(result.gl_error,0);assert(result.mask_iou>.98&&result.mask_iou<=1);assert(result.mean_rgb_absolute_error>=0&&result.mean_rgb_absolute_error<2);
 assert.equal(result.lifecycle?.context_lost,false);assert.equal(result.lifecycle.gl_error,0);assert.equal(result.lifecycle.reentry_exact,true);assert.deepEqual(result.lifecycle.frames.map(f=>f.yaw),[0,45,90,135,180,225,270,315]);for(const frame of result.lifecycle.frames)assert.equal(frame.border_opaque_pixels,0);
}
export async function verifyProductionWheel(root,asset,record){
 const p=record.final_posters,w=p.wheel;assert.equal(p.route,PRODUCTION_WHEEL_ROUTE);assert.equal(p.browser_capture,true);assert.equal(w.source_glb_sha256,asset.sha256.glb);
 const renderer=await productionWheelRenderer(root);assert.equal(w.renderer_sha256,renderer.sha256);assert.equal(w.browser_version,renderer.browser);
 const png=await productionWheelPin(root,w),capture=JSON.parse(await productionWheelPin(root,w.render_config));
 assertProductionWheel(capture,{asset,sourceGLB:await productionWheelBytes(root,asset.glb),unchangedDetail:await productionWheelPin(root,p.detail),png,rendererSha256:renderer.sha256,browserVersion:renderer.browser});assert.deepEqual(capture.wheelSpec,w.wheelSpec);
 const report=JSON.parse(await productionWheelPin(root,w.capture_report));assert.equal(report.version,1);assert.equal(report.kind,'new-production-wheel-capture-evidence');assert.equal(report.status,'capture-and-geometry-check-pass');assert.equal(report.publication_authority,false);assert.equal(report.visual_review,'pending');assert.equal(report.physical_gpu,'unknown');assert.deepEqual(report.errors,[]);assert.equal(report.renderer_sha256,renderer.sha256);assert.deepEqual(report.renderer_files,renderer.files);assert.equal(report.browser_version,renderer.browser);
 assert(Array.isArray(report.cases)&&report.cases.length>0&&new Set(report.cases.map(c=>c.id)).size===report.cases.length);assertProductionWheelCase(report.cases.find(c=>c.id===asset.id),{asset,pngPin:w,wheelSpec:w.wheelSpec});
 const review=JSON.parse(await productionWheelPin(root,w.visual_review));assertProductionWheelReview(review,{capturePin:w.render_config,reportPin:w.capture_report,asset,pngPin:w,maker:record.maker,producer:report.producer});return capture;
}

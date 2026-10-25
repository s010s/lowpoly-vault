/** Explicit selection orchestration. Revision probes never reuse or rewrite older capture evidence. */
import {detailPresentationPolicy,detailCapturePolicy,validDetailPresentation} from './gallery/detail-presentation-policy.js';
import {authenticateDetailProofs,assertDetailAuthority} from './detail-capture-authority.mjs';
import {readCaptureArchives,assertCaptureEntry} from './detail-capture-provenance.mjs';
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,mkdtemp,symlink,rm} from 'node:fs/promises';
import {spawn} from 'node:child_process';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {CAPTURE_POLICY,posterRendererFiles,posterInputKey} from './gallery-poster-inputs.mjs';
const sha=b=>createHash('sha256').update(b).digest('hex');
export function planDetailDelta(assets,index,receipts,ids,rendererKey){
 assert(ids.length&&new Set(ids).size===ids.length,'Explicit unique changed IDs required');
 const requested=new Set(ids),known=new Set(assets.map(a=>a.id));for(const id of ids)assert(known.has(id),'Unknown changed detail ID '+id);
 assert.equal(index.renderer_input_sha256,rendererKey,'Renderer changed: requires a separately reviewed full capture, not delta reuse');
 const reuse={};for(const a of assets){if(requested.has(a.id))continue;const e=index.presentations[a.id];assert(e,'New detail model must be named explicitly '+a.id);
  const proof=receipts.find(r=>r.source_commit===e.capture.source_commit&&r.renderer_input_sha256===rendererKey&&r.assets?.[a.id]?.detail_png_sha256===e.png.sha256)?.assets[a.id];
  assert(proof&&proof.source_glb_sha256===a.sha256.glb&&proof.asset_input_sha256===posterInputKey(a,{sha256:'detail-scope-source-only-v1'}),'Changed metadata/model must be named explicitly '+a.id);
  assert.equal(e.source_glb_sha256,a.sha256.glb);assert.equal(e.production_descriptor,a.production_release);reuse[a.id]=e;
 }return {requested:[...requested],reuse};
}
export function planDetailRevisionSmoke(assets,ids,presentation,smoke){
 assert(smoke&&validDetailPresentation(presentation),'Revision 2 is candidate-smoke only until actual-page review selects its raster policy');
 assert.deepEqual([...ids].sort(),['onoclea','pertica','azolla','sidneyia','arroyo-wash'].sort(),'Only the reviewed five-model raster/margin probe is enabled');
 assert(ids.every(id=>assets.some(a=>a.id===id)),'Probe ID outside current authorized routes');
 return {requested:ids,reuse:{}};
}
export async function captureDetailDelta(ids){
 assert(/^[a-f0-9]{40}$/.test(process.env.GITHUB_SHA||''),'Exact capture source commit required');
 const root=process.cwd(),indexPath=resolve('site/gallery/detail-presentations-index.js'),proofPath=resolve('site/gallery/detail-input-proofs.js');
 const immutable=new Map(await Promise.all([indexPath,proofPath].map(async p=>[p,await readFile(p)])));
 const index=(await import(pathToFileURL(indexPath))).default,proofs=(await import(pathToFileURL(proofPath))).default;
 const manifest=JSON.parse(await readFile('assets/manifest.json')),resources=JSON.parse(await readFile('site/public/gallery/resources.json'));
 const assets=manifest.assets.filter(a=>['blender-cycles-cpu-v1','blender-detail-preview-wheel-v1'].includes(resources.posters[a.id]?.render_route));
 const revision=Number(process.env.DETAIL_CAPTURE_REVISION||1),smoke=process.env.DETAIL_CAPTURE_CANDIDATE_SMOKE==='1';assert([1,2].includes(revision));
 const presentation=revision===2?detailPresentationPolicy(Number(process.env.DETAIL_CAPTURE_SIZE)):null;
 const files=[...await posterRendererFiles(root),'package-lock.json','site/capture-detail-presentations.mjs','site/detail-pixels.mjs',...(presentation?['site/gallery/detail-renderer.js','site/gallery/detail-presentation-policy.js']:[])].sort();
 const inputs=await Promise.all(files.map(async path=>({path,sha256:sha(await readFile(path))})));
 const browser=JSON.parse(await readFile('node_modules/playwright-core/browsers.json')).browsers.find(b=>b.name==='chromium').browserVersion;
 const rendererKey=sha(JSON.stringify({files:inputs,policy:detailCapturePolicy(CAPTURE_POLICY,presentation),browser}));
 let plan;
 if(presentation){
  plan=planDetailRevisionSmoke(assets,ids,presentation,smoke);
 }else {assert(!smoke,'Smoke profile requires its explicit renderer revision');plan=planDetailDelta(assets,index,proofs.receipts,ids,rendererKey);}
 const archives=Object.keys(plan.reuse).length?await readCaptureArchives(proofs.receipts):new Map();
 const authority=Object.keys(plan.reuse).length?await authenticateDetailProofs({root,index,inputProofs:proofs,manifest,baseSha:process.env.BASE_SHA,requiredIds:Object.keys(plan.reuse)}):{records:[]};
 if(Object.keys(plan.reuse).length)assertDetailAuthority(authority.capability,{root,index,inputProofs:proofs,manifest});
 for(const [id,e] of Object.entries(plan.reuse)){
  const receipt=proofs.receipts.find(r=>r.source_commit===e.capture.source_commit&&r.renderer_input_sha256===rendererKey&&r.assets?.[id]?.detail_png_sha256===e.png.sha256);assertCaptureEntry(archives,receipt,id,e);
  const p=resources.posters[id];assert.equal(e.previous_detail.path,p.detail);assert(resources.files.some(f=>f.path===p.detail&&f.sha256===e.previous_detail.sha256),'Changed old poster must be named explicitly '+id);
  for(const [path,pin] of [[resolve('site/public',e.detail),e.png]]){const bytes=await readFile(path);assert.equal(bytes.length,pin.bytes);assert.equal(sha(bytes),pin.sha256,'Missing unchanged proof: repair before delta '+id);}
 }
 // The copied core resolves this filtered index, but all actual asset/source reads
 // use the unchanged repository cwd. No edits, even temporary, to source index.
 const temp=await mkdtemp(resolve('.detail-delta-'));let report;
 try{
  await mkdir(resolve(temp,'gallery'));
  await writeFile(resolve(temp,'capture-detail-presentations.mjs'),await readFile('site/capture-detail-presentations.mjs'));
  await writeFile(resolve(temp,'gallery/detail-presentations-index.js'),'export default '+JSON.stringify({...index,presentations:{}})+';\n');
  for(const file of ['detail-pixels.mjs','gallery-poster-inputs.mjs','gallery/detail-presentation-policy.js'])await symlink(resolve('site',file),resolve(temp,file));
  const output=resolve(process.env.DETAIL_CAPTURE_OUTPUT||'qa/detail-capture-delta'),fresh=resolve(output,'fresh');
  assert(!process.env.DETAIL_CAPTURE_IDS,'Smoke selection cannot be mixed with delta publication capture');
  await new Promise((ok,no)=>{const child=spawn(process.execPath,[resolve(temp,'capture-detail-presentations.mjs')],{cwd:root,stdio:'inherit',env:{...process.env,DETAIL_EXPECTED_COUNT:String(assets.length),DETAIL_CAPTURE_OUTPUT:fresh,DETAIL_CAPTURE_IDS:ids.join(',')}});child.on('error',no);child.on('exit',code=>code===0?ok():no(Error('Detail delta capture failed '+code)));});
  const captured=(await import(pathToFileURL(resolve(fresh,'detail-presentations-index.js')))).default;
  assert.deepEqual(Object.keys(captured.presentations).sort(),[...ids].sort(),'Fresh subset differs from explicitly requested IDs');
  const result={...captured,presentations:{...plan.reuse,...captured.presentations}};
  report=JSON.parse(await readFile(resolve(fresh,'capture-report.json')));assert.equal(report.captured,ids.length);assert.equal(report.reused,0);assert.equal(report.count,ids.length);assert.equal(report.smoke_only,true);
  assert.equal(Object.keys(result.presentations).length,smoke?ids.length:assets.length);
  await writeFile(resolve(output,'detail-presentations-index.js'),'export default '+JSON.stringify(result)+';\n');
  for(const [id,e] of Object.entries(plan.reuse))assert.deepEqual(result.presentations[id],e,'Unrequested entry rewritten '+id);
  for(const id of ids){const e=result.presentations[id];assert(e&&e.capture.source_commit===process.env.GITHUB_SHA,'Requested ID lacks fresh exact-source capture '+id);assert.equal(e.source_glb_sha256,assets.find(a=>a.id===id).sha256.glb);}
  await writeFile(resolve(output,'delta-selection-report.json'),JSON.stringify({status:smoke?'UNACCEPTED_CANDIDATE_SMOKE':'pass',kind:smoke?'bounded-renderer-revision-smoke-v2':'bounded-detail-delta',...(presentation?{presentation}:{}),fresh_report_preserved:'fresh/capture-report.json',fresh_scope:'explicit-requested-subset',requested:ids,reused:Object.keys(plan.reuse),reuse_authority:authority.records,renderer_input_sha256:rendererKey,source_index_sha256:sha(immutable.get(indexPath)),source_receipts_sha256:sha(immutable.get(proofPath)),render_core_sha256:sha(await readFile('site/capture-detail-presentations.mjs'))},null,2));
 }finally{await rm(temp,{recursive:true,force:true});for(const [path,bytes] of immutable)assert.deepEqual(await readFile(path),bytes,'Immutable source evidence was modified');}
 return report;
}

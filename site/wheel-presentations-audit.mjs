/** Fail-closed delivery audit for the additive wheel correction, not historic production evidence. */
import assert from 'node:assert/strict';
import {readFile,readdir,realpath} from 'node:fs/promises';
import {resolve,sep} from 'node:path';
import index from './gallery/wheel-presentations-index.js';
import {resolveWheelPoster} from './gallery/wheel-presentations.js';
import {assertWheelPresentation,wheelHash} from './wheel-presentation-contract.mjs';
import {wheelHistoricalBaseline} from './wheel-historical-baseline.mjs';
import {posterRendererFiles} from './gallery-poster-inputs.mjs';
async function bytes(root,path){assert(typeof path==='string'&&!/[\\\u0000-\u001f?#%]/.test(path)&&!path.split('/').some(p=>!p||p==='.'||p==='..'));const file=resolve(root,path);assert(file.startsWith(resolve(root)+sep));assert.equal(await realpath(file),file,'Symlink wheel input');return readFile(file);}
export async function auditWheelPresentations(manifest,{root=process.cwd(),outputRoot}={}){
 const manifestBytes=await bytes(root,'assets/manifest.json'),resourceBytes=await bytes(root,'site/public/gallery/resources.json'),resources=JSON.parse(resourceBytes);
 const historical=await wheelHistoricalBaseline(root,manifest,resources,index);
 const affected=historical.manifest.assets.filter(a=>resources.posters[a.id]?.render_route==='blender-cycles-cpu-v1'&&!resources.posters[a.id]?.wheelSpec);
 assert.deepEqual(Object.keys(index.presentations).sort(),affected.map(a=>a.id).sort());assert.equal(index.count,affected.length);
 for(const pin of Object.values(index.evidence)){const data=await bytes(root,pin.path);assert.equal(data.length,pin.bytes);assert.equal(wheelHash(data),pin.sha256);}
 const report=JSON.parse(await bytes(root,index.evidence.batch_report.path));assert.equal(report.status,'capture-and-geometry-check-pass');assert.deepEqual(report.errors,[]);assert.equal(report.cases.length,affected.length);
 const review=JSON.parse(await bytes(root,index.evidence.review_summary.path));assert.equal(review.status,'pass');assert.equal(review.visual_review.count,affected.length);assert.equal(review.physical_gpu,'unknown');
 const saved=JSON.parse(await bytes(root,index.evidence.capture_records.path));
 const closure=[...new Set([...await posterRendererFiles(root),'site/capture-wheel-frame.js','package-lock.json'])].sort();const rendererFiles=await Promise.all(closure.map(async path=>({path,sha256:wheelHash(await bytes(root,path))})));
 assert.deepEqual(rendererFiles,report.renderer_files,'Renderer inputs changed since real capture');const rendererSha256=wheelHash(JSON.stringify(rendererFiles));assert.equal(rendererSha256,index.renderer_sha256);
 const browser=JSON.parse(await readFile(resolve(root,'node_modules/playwright-core/browsers.json'))).browsers.find(b=>b.name==='chromium').browserVersion;assert.equal(browser,index.browser_version);
 const files=[];
 for(const asset of affected){const entry=index.presentations[asset.id],poster=resources.posters[asset.id],record=saved.records.find(row=>row.id===asset.id);assert(record);assert.equal(wheelHash(JSON.stringify(record.record,null,2)),entry.capture_sha256);
  const selected=resolveWheelPoster(asset,resources);assert.equal(selected.wheel,entry.wheel);assert.equal(selected.detail,poster.detail);assert.deepEqual(selected.wheelSpec,entry.wheelSpec);
  const png=await bytes(root,'site/public/'+entry.wheel);assertWheelPresentation(record.record,{asset,sourceGLB:await bytes(root,asset.glb),previousWheel:await bytes(root,'site/public/'+poster.wheel),unchangedDetail:await bytes(root,'site/public/'+poster.detail),png,rendererSha256,browserVersion:browser});
  assert.equal(record.record.png.sha256,entry.png.sha256);assert.deepEqual(record.record.wheelSpec,entry.wheelSpec);
  const result=report.cases.find(c=>c.id===asset.id);assert(result);assert.equal(result.source_glb_sha256,asset.sha256.glb);assert.equal(result.wheel_sha256,entry.png.sha256);assert.deepEqual(result.spec,entry.wheelSpec);assert(result.mask_iou>.98&&result.mean_rgb_absolute_error<2);assert.equal(result.gl_error,0);assert.equal(result.context_lost,false);
  if(outputRoot)assert((await bytes(outputRoot,entry.wheel)).equals(png),'Delivered wheel bytes differ');files.push(entry.wheel);
 }
 const names=await readdir(resolve(root,'site/public/wheel-presentations'),{withFileTypes:true});assert(names.every(n=>n.isFile()&&!n.isSymbolicLink()));assert.deepEqual(names.map(n=>'wheel-presentations/'+n.name).sort(),files.slice().sort());return {files,count:files.length};
}

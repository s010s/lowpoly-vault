/** Hash-checked candidate staging is separate from the publication manifest. */
import assert from 'node:assert/strict';
import {readFile,writeFile,realpath,mkdir,cp,appendFile} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {resolve,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {prepareRenderCapture} from './prepare-render-capture.mjs';
import {LANDAIR_CAPTURE as fixed} from './accepted-landair-capture.mjs';
export async function prepareLandairCapture({root=process.cwd(),outDir=resolve(process.env.GALLERY_DIR||'qa/capture-inputs-site')}={}){
 const descriptor=JSON.parse(await readFile(resolve(root,'qa/landair-release-20261019/capture-inputs.json')));
 assert.deepEqual(descriptor,fixed);assert.equal(descriptor.publication_authority,false);
 async function checked(pin){assert(/^(production|qa)\/[a-zA-Z0-9_./-]+$/.test(pin.path)&&!pin.path.split('/').includes('..'));const p=resolve(root,pin.path);assert.equal(await realpath(p),p);const b=await readFile(p);assert.equal(createHash('sha256').update(b).digest('hex'),pin.sha256);return b;}
 const review=JSON.parse(await checked(descriptor.review));assert.equal(review.overall_status,'limited_qa_pass_with_formal_and_release_blockers');assert.equal(review.frozen_git_sha,'68483aa3b8eed2d86f9e59a930128d99579b0838');const delivery=JSON.parse(await checked(descriptor.delivery_review));assert.equal(delivery.status,'pass');assert.equal(delivery.repair_commit,'e874e99d20b3b98c73cddb8496bcd7e89be4e28c');assert.equal(delivery.original_qa_evidence_unchanged_and_accessible,true);
 const manifest=await prepareRenderCapture({root,outDir});const ids=[];
 for(const entry of descriptor.assets){const a=JSON.parse(await checked(entry.metadata)),glb=await checked(entry.glb),r=review.assets.find(r=>r.id===entry.id);assert.equal(a.id,entry.id);assert.equal(a.glb,entry.glb.path);assert.equal(a.sha256.glb,entry.glb.sha256);const repaired=delivery.assets.find(r=>r.asset_id===entry.id);assert.equal(repaired.status,'pass');assert.equal(repaired.approved_for_brief,false);assert.equal(repaired.glb_sha256,entry.glb.sha256);assert.equal(r.glb_sha256,entry.glb.sha256);const published=manifest.assets.find(p=>p.id===a.id);if(published)assert.equal(published.sha256.glb,a.sha256.glb);assert(!ids.includes(a.id));ids.push(a.id);await mkdir(dirname(resolve(outDir,a.glb)),{recursive:true});await writeFile(resolve(outDir,a.glb),glb);if(!published)manifest.assets.push(a);}
 manifest.capture_only=true;manifest.capture_only_ids=ids;
 await writeFile(resolve(outDir,'assets/manifest.json'),JSON.stringify(manifest)+'\n');
 if(process.env.GITHUB_ENV)await appendFile(process.env.GITHUB_ENV,`PREVIEW_ASSET_IDS=${ids.join(',')}\n`);
 console.log(`Staged ${ids.length} exact candidate GLBs for capture only. Published manifest and approval gates are unchanged.`);return manifest;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)await prepareLandairCapture();

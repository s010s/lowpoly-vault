/** Candidate-authored matching hashes cannot create or rewrite a historical approval. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,readFile,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,dirname,resolve} from 'node:path';
import {posterInputState,posterInputKey,posterSharedInputs} from './gallery-poster-inputs.mjs';
import {HISTORICAL_APPROVALS_SHA256} from './gallery-poster-compat.mjs';
import {createHash} from 'node:crypto';
import {collectProductionRelease} from './production-release.mjs';
const root=await mkdtemp(join(tmpdir(),'frozen-poster-approvals-'));
const approvalPath='site/gallery/approved-poster-inputs.json';
const original=await readFile(approvalPath),baseline=JSON.parse(original),manifest=JSON.parse(await readFile('assets/manifest.json')),resources=JSON.parse(await readFile('site/public/gallery/resources.json'));
assert.equal(createHash('sha256').update(original).digest('hex'),HISTORICAL_APPROVALS_SHA256);
try{
 // Keep the actual355 positive path: copy its exact verified production closure,
 // not just historical renderer files. Never rewrite or invent projection proof.
 const productionPaths=new Set(),descriptor=manifest.publication?.production_descriptor;
 if(descriptor){
  await collectProductionRelease(process.cwd(),descriptor);
  const source=JSON.parse(await readFile(descriptor));productionPaths.add(descriptor);productionPaths.add(source.review_path);
  const add=pin=>{assert(pin&&typeof pin.path==='string'&&/^[0-9a-f]{64}$/.test(pin.sha256||'')&&Number.isSafeInteger(pin.bytes));productionPaths.add(pin.path);};
  source.implementation.forEach(add);add(source.scope_document);
  for(const entry of source.assets){
   add(entry.metadata);add(entry.evidence);const record=JSON.parse(await readFile(entry.evidence.path));
   Object.values(record.roles).forEach(add);record.build_closure.forEach(add);add(record.preview);
   const posters=record.final_posters;add(posters.recipe);
   for(const kind of ['detail','wheel']){add(posters[kind]);add(posters[kind].render_config);}
   const recipe=JSON.parse(await readFile(posters.recipe.path));recipe.files.forEach(add);
  }
  for(const path of productionPaths)assert(!path.startsWith('/')&&!path.includes('\\')&&path.split('/').every(p=>p&&p!=='.'&&p!=='..'),'Safe pinned production fixture input');
 }
 for(const path of new Set([...baseline.shared.files.map(row=>row[0]),approvalPath,'node_modules/playwright-core/browsers.json',...productionPaths])){await mkdir(join(root,dirname(path)),{recursive:true});await writeFile(join(root,path),await readFile(resolve(path)));}
 const good=await posterInputState(manifest,resources,{root});assert.equal(good.approved.length,182);assert.deepEqual(good.approved.sort(),Object.keys(baseline.posters).sort());
 const reject=async mutate=>{const value=structuredClone(baseline);mutate(value);await writeFile(join(root,approvalPath),JSON.stringify(value));await assert.rejects(()=>posterInputState(manifest,resources,{root}),/Historical approval catalog bytes changed/);};
 await reject(value=>{value.posters['forged-new-model']={input_sha256:'a'.repeat(64),poster_sha256:'b'.repeat(64)};});
 await reject(value=>value.posters[Object.keys(value.posters)[0]].poster_sha256='c'.repeat(64));
 await reject(value=>value.posters[Object.keys(value.posters)[0]].input_sha256='d'.repeat(64));
 await reject(value=>delete value.shared);
 await writeFile(join(root,approvalPath),'{broken');await assert.rejects(()=>posterInputState(manifest,resources,{root}),/Historical approval catalog bytes changed/,'Parse catch cannot swallow tampering');
 await writeFile(join(root,approvalPath),original);
 const changed=structuredClone(manifest);changed.assets.find(a=>baseline.posters[a.id]).sha256.glb='e'.repeat(64);await assert.rejects(()=>posterInputState(changed,resources,{root}),/Approved poster inputs changed/);
 const changedResources=structuredClone(resources);changedResources.posters[Object.keys(baseline.posters)[0]].source_glb_sha256='f'.repeat(64);await assert.rejects(()=>posterInputState(manifest,changedResources,{root}),/Approved poster pixels or metadata changed/);
 console.log('Historical182 approval bytes frozen; added/re-signed/malformed/missing-shared catalogs refuse, unchanged inputs preserved.');
}finally{await rm(root,{recursive:true,force:true});}

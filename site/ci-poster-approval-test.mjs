import './gallery-poster-order-test.mjs';
import {successorReader,historicalManifestView,historicalGalleryView} from './same-id-successors.mjs';
/** Candidate-authored matching hashes cannot create or rewrite a historical approval. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,readFile,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,dirname,resolve} from 'node:path';
import {posterInputState,posterInputKey,posterSharedInputs} from './gallery-poster-inputs.mjs';
import {HISTORICAL_APPROVALS_SHA256,restoreHistoricalPosterSerialization} from './gallery-poster-compat.mjs';
import {createHash} from 'node:crypto';
import {productionSourceClosure} from './production-release.mjs';
import {productionWheelRenderer} from './production-wheel-contract.mjs';
import {collectManifestProduction} from './production-publication.mjs';
const root=await mkdtemp(join(tmpdir(),'frozen-poster-approvals-'));
const approvalPath='site/gallery/approved-poster-inputs.json';
const original=await readFile(approvalPath),baseline=JSON.parse(original),selected=JSON.parse(await readFile('assets/manifest.json')),selectedResources=JSON.parse(await readFile('site/public/gallery/resources.json'));
const successorRead=successorReader(process.cwd()),manifest=historicalManifestView({manifest:selected,read:successorRead}),resources=restoreHistoricalPosterSerialization(historicalGalleryView({manifest:selected,resources:selectedResources,read:successorRead}),baseline);
assert.equal(createHash('sha256').update(original).digest('hex'),HISTORICAL_APPROVALS_SHA256);
try{
 // Verify the current disjoint production set first, then copy its complete
 // pinned original/typed/bridge closure into an independent temporary fixture.
 // No review result, historical byte or source file is manufactured here.
 await collectManifestProduction(process.cwd(),manifest);
 const productionPaths=await productionSourceClosure(process.cwd(),manifest);
 // The authenticated production wheel route also reads its live renderer closure,
 // including capture-wheel-frame.js; copy those real inputs, not a fabricated seal.
 const wheelRenderer=await productionWheelRenderer(process.cwd());
 const wheelRendererPaths=wheelRenderer.files.map(file=>file.path);
 for(const path of productionPaths)assert(!path.startsWith('/')&&!path.includes('\\')&&path.split('/').every(p=>p&&p!=='.'&&p!=='..'),'Safe pinned production fixture input');
 for(const path of new Set([...baseline.shared.files.map(row=>row[0]),approvalPath,'node_modules/playwright-core/browsers.json',...productionPaths,...wheelRendererPaths])){await mkdir(join(root,dirname(path)),{recursive:true});await writeFile(join(root,path),await readFile(resolve(path)));}
 assert.deepEqual(await productionWheelRenderer(root),wheelRenderer,'Private fixture must preserve the complete real wheel renderer');
 const framePath=join(root,'site/capture-wheel-frame.js'),frame=await readFile(framePath);
 try{await rm(framePath);await assert.rejects(()=>productionWheelRenderer(root),/ENOENT/,'Missing renderer inputs must fail closed');}
 finally{await writeFile(framePath,frame);}
 try{await writeFile(framePath,Buffer.concat([frame,Buffer.from('\n// tamper\n')]));assert.notDeepEqual(await productionWheelRenderer(root),wheelRenderer,'Renderer-byte tampering must change the authenticated closure');}
 finally{await writeFile(framePath,frame);}
 assert.deepEqual(await productionWheelRenderer(root),wheelRenderer);
 // The isolated legacy fixture must not load the effective successor manifest from its copied file.
 await writeFile(join(root,'assets/manifest.json'),JSON.stringify(manifest));
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

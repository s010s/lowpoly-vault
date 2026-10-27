/** One immutable capture-only batch. No production approval or catalog mutation. */
import assert from 'node:assert/strict';
import {readFile, appendFile, realpath} from 'node:fs/promises';
import {resolve, sep} from 'node:path';
import {createHash} from 'node:crypto';
import {productionWheelAsset,productionWheelBytes,productionWheelRenderer,assertProductionWheel,assertProductionWheelCase} from './production-wheel-contract.mjs';
export const CORRECTIVE_CAPTURE=Object.freeze({path:'qa/old-corrective-ten-20261027/capture-inputs.json',sha256:'df63eaae6b117569c87f64c3837d781e7ae45bc91165120cb566d47be00bc109',bytes:17172,output:'qa/ci-publication-capture/old-corrective-ten-20261027',renderer_sha256:'f25626b74087690fc9d807fd473f719b2a22082038a47c5922e6f1bb977681b5',browser:'141.0.7390.37'});
export const CORRECTIVE_IDS=Object.freeze(['banded-iron-formation-far-lod','calamites-crown-lod0','calamites-crown-lod1','cave-popcorn-far-lod','coal-seam-outcrop','flute-cast-slab','mudpot','oncoid-bed','parabolic-dune-terrain-only','serac','stromatolite-mound-full-exterior']);
const sha=b=>createHash('sha256').update(b).digest('hex');
const json=b=>JSON.parse(b.toString());
function checkPin(b,p){assert.equal(b.length,p.bytes,'Corrective capture byte count changed');assert.equal(sha(b),p.sha256,'Corrective capture hash changed');return b;}
export async function validateCorrectiveCapture({bytes,read,renderer}){
 checkPin(bytes,CORRECTIVE_CAPTURE);const scope=json(bytes);
 assert.equal(scope.version,1);assert.equal(scope.kind,'production-wheel-capture-inputs');assert.equal(scope.publication_authority,false);assert.equal(scope.review_only,true);
 assert.equal(scope.base_main,'38ecb2c632dd4d6c23473a51f1d12bff5ea9f7af');assert.equal(scope.batch,'old-corrective-ten-20261027-r001');
 assert.deepEqual(scope.assets.map(x=>x.asset.id),CORRECTIVE_IDS);assert.equal(scope.stable_model_count,10);assert.equal(scope.configuration_count,11);
 assert.equal(renderer.sha256,CORRECTIVE_CAPTURE.renderer_sha256);assert.equal(renderer.browser,CORRECTIVE_CAPTURE.browser);assert.deepEqual(renderer,scope.renderer);
 for(const row of scope.assets){const a=productionWheelAsset(row.asset);assert.deepEqual(a,row.asset);assert.equal(a.units,'meters');assert.equal(row.source_identity.is_new_scientific_subject,false);assert.equal(sha(await read(a.glb)),a.sha256.glb);const png=checkPin(await read(row.detail.path),row.detail);checkPin(await read(row.native.path),row.native);assert.equal(png.subarray(0,8).toString('hex'),'89504e470d0a1a0a');assert.deepEqual([png.readUInt32BE(16),png.readUInt32BE(20),png[24],png[25]],[512,512,8,6]);}
 return scope;
}
export async function loadCorrectiveCapture({root=process.cwd()}={}){
 const file=resolve(root,CORRECTIVE_CAPTURE.path);let bytes;
 try {bytes=await readFile(file);}catch(e){if(e.code==='ENOENT'){assert.notEqual(process.env.OLD_CORRECTIVE_CAPTURE,'old-corrective-ten-20261027','Prepared corrective capture inputs disappeared');return null;}throw e;}
 assert.equal(await realpath(file),file,'Corrective capture input symlink');
 return validateCorrectiveCapture({bytes,read:p=>productionWheelBytes(root,p),renderer:await productionWheelRenderer(root)});
}
export async function prepareCorrectiveCapture({root=process.cwd(),envPath=process.env.GITHUB_ENV}={}){
 const scope=await loadCorrectiveCapture({root});if(!scope)return false;
 assert(envPath,'Capture-only preparation requires the existing Actions environment file');
 // Fixed values only: neither arbitrary caller paths nor input strings become environment assignments.
 await appendFile(envPath,`OLD_CORRECTIVE_CAPTURE=old-corrective-ten-20261027\nPRODUCTION_WHEEL_INPUTS=${CORRECTIVE_CAPTURE.path}\nPRODUCTION_WHEEL_OUTPUT=${CORRECTIVE_CAPTURE.output}\nPREVIEW_ASSET_IDS=${CORRECTIVE_IDS.join(',')}\n`);
 console.log(JSON.stringify({status:'PREPARED_EXACT_ELEVEN_CAPTURE_ONLY',publication_authority:false,ids:CORRECTIVE_IDS}));return true;
}
export async function runCorrectiveWheelCapture({root=process.cwd()}={}){
 if(!await loadCorrectiveCapture({root}))return false;
 assert.equal(resolve(root),process.cwd(),'Wheel capture runs in the checked repository');assert.equal(process.env.OLD_CORRECTIVE_CAPTURE,'old-corrective-ten-20261027');
 assert.equal(process.env.PRODUCTION_WHEEL_INPUTS,CORRECTIVE_CAPTURE.path);assert.equal(process.env.PRODUCTION_WHEEL_OUTPUT,CORRECTIVE_CAPTURE.output);assert.equal(process.env.PREVIEW_ASSET_IDS,CORRECTIVE_IDS.join(','));
 await import('./capture-production-wheels.mjs');return true;
}
export async function verifyCorrectiveWheelOutput({root=process.cwd(),readOutput}={}){
 const scope=await loadCorrectiveCapture({root});if(!scope)return false;
 const output=resolve(root,CORRECTIVE_CAPTURE.output);const read=readOutput|| (async p=>{assert(!p.includes('..')&&!p.includes('\\')&&!p.startsWith('/'));const f=resolve(output,p);assert(f.startsWith(output+sep));assert.equal(await realpath(f),f);return readFile(f);});
 const report=json(await read('report.json'));const renderer=await productionWheelRenderer(root);
 assert.equal(report.kind,'new-production-wheel-capture-evidence');assert.equal(report.status,'capture-and-geometry-check-pass');assert.equal(report.publication_authority,false);assert.equal(report.visual_review,'pending');assert.equal(report.physical_gpu,'unknown');assert.deepEqual(report.errors,[]);assert.deepEqual(report.producer,scope.producer);assert.equal(report.source_commit,process.env.GITHUB_SHA);assert.match(report.source_commit||'',/^[a-f0-9]{40}$/);assert.deepEqual(report.renderer_files,renderer.files);assert.equal(report.renderer_sha256,renderer.sha256);assert.equal(report.browser_version,renderer.browser);assert.deepEqual(report.cases.map(x=>x.id),CORRECTIVE_IDS);
 for(const row of scope.assets){const a=row.asset,png=await read(`${a.id}/wheel.png`),capture=json(await read(`${a.id}/capture.json`));assertProductionWheel(capture,{asset:a,png,sourceGLB:await productionWheelBytes(root,a.glb),unchangedDetail:await productionWheelBytes(root,row.detail.path),rendererSha256:renderer.sha256,browserVersion:renderer.browser});assertProductionWheelCase(report.cases.find(x=>x.id===a.id),{asset:a,pngPin:capture.png,wheelSpec:capture.wheelSpec});const lifecycle=json(await read(`${a.id}/lifecycle.json`));assert.deepEqual(lifecycle,report.cases.find(x=>x.id===a.id).lifecycle);for(const name of ['live-first-frame.png','comparison.png',...lifecycle.frames.map(x=>`turn-${x.yaw}.png`)])assert.equal((await read(`${a.id}/${name}`)).subarray(0,8).toString('hex'),'89504e470d0a1a0a');}
 console.log(JSON.stringify({status:'VERIFIED_EXACT_ELEVEN_CAPTURE_OUTPUT_NOT_VISUAL_APPROVAL',publication_authority:false,visual_review:'pending',source_commit:report.source_commit,ids:CORRECTIVE_IDS,output:CORRECTIVE_CAPTURE.output}));return true;
}

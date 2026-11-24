/** Exact poster-only branch integration; not a general release or visual approval. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {readFile,mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {assertOnlyTargetChanged,assertOnlyTargetResourcesChanged,assertModelIntegrationIsolation} from './model-commit-isolation.mjs';
import {checkDelivery} from '../../site/unified-delivery-contract.mjs';
import {resolveGalleryPoster} from '../../site/gallery/wheel-presentations.js';
import {createGalleryCatalog} from '../../site/gallery/catalog-build.mjs';
import {deliverManifestAssets} from '../../site/asset-delivery.mjs';
const id='pluricarpellatia',subject='fix(pluricarpellatia): match gallery posters to original 3D';
const manifestPath='assets/manifest.json', resourcesPath='site/public/gallery/resources.json';
const json=p=>readFile(p,'utf8').then(JSON.parse);
const gitJson=(rev,path)=>JSON.parse(execFileSync('git',['show',rev+':'+path],{encoding:'utf8',maxBuffer:16*1024*1024}));
const manifest=await json(manifestPath), resources=await json(resourcesPath);
const draft=process.argv.includes('--uncommitted');
const integration=draft?'HEAD':assertModelIntegrationIsolation({id,subject,currentManifest:manifest,currentResources:resources})+'^';
const baseline=gitJson(integration,manifestPath), baselineResources=gitJson(integration,resourcesPath);
if(draft){assertOnlyTargetChanged(baseline,manifest,id);assertOnlyTargetResourcesChanged(baselineResources,resources,id);}
const old=baseline.assets.find(a=>a.id===id), asset=manifest.assets.find(a=>a.id===id);
assert.notEqual(old.preview,asset.preview);assert.notDeepEqual(old.galleryPosters,asset.galleryPosters);
const withoutPosters=({preview,galleryPosters,sha256,file_sizes,...rest})=>({...rest,sha256:{glb:sha256.glb,blend:sha256.blend},file_sizes:{glb:file_sizes.glb,blend:file_sizes.blend}});
assert.deepEqual(withoutPosters(asset),withoutPosters(old),'The model, source, pose and non-preview metadata must all stay unchanged.');
assert.equal(asset.sha256.glb,'d5934e7086f70e54054230f76ab79b6969a9570afb82efad833347cb4017ac90');
assert.equal(asset.sha256.blend,'233cc2db2dd4a37da5bd157dccf14502e4782066d083368fc479d01e1a3a4dcb');
const bound=resolveGalleryPoster(asset,resources);
assert.equal(bound.source_glb_sha256,asset.sha256.glb);
assert.equal(bound.render_route,'webgl-poster-only-repair-v1');
assert.deepEqual({detail:bound.detail,wheel:bound.wheel},asset.galleryPosters);
for(const role of ['wheel','detail']){
 const oldPin=baselineResources.files.find(f=>f.path===old.galleryPosters[role]);
 assert.deepEqual(resources.files.find(f=>f.path===oldPin.path),oldPin,'Historic PNG pin changed.');
 const path=asset.galleryPosters[role], pin=resources.files.find(f=>f.path===path), bytes=await readFile('site/public/'+path);
 assert.equal(pin.bytes,bytes.length);assert.equal(createHash('sha256').update(bytes).digest('hex'),pin.sha256);
 assert.deepEqual([bytes.readUInt32BE(16),bytes.readUInt32BE(20)],role==='wheel'?[768,432]:[1536,1536]);
 assert.equal(bytes.readUInt8(25),6,'Manual capture must preserve an alpha channel.');
}
assert.deepEqual(await readFile(asset.preview),await readFile('site/public/'+asset.galleryPosters.detail));
assert.equal(asset.file_sizes.preview,(await readFile(asset.preview)).length);
const one={...manifest,assets:[asset]};
assert.deepEqual(createGalleryCatalog(one,resources).assets[0].galleryPosters,asset.galleryPosters);
assert.equal((await checkDelivery({manifest:one,resources,hash:true})).count,1);
const out=await mkdtemp(join(tmpdir(),'pluricarpellatia-poster-delivery-'));
try{
 const built=(await deliverManifestAssets(one,out,{verifyHashes:true})).assets[0];
 for(const k of ['glb','blend'])assert.deepEqual(await readFile(join(out,built.downloads[k])),await readFile(old[k]));
 const credits=await readFile(join(out,built.downloads.credits),'utf8');assert(credits.includes('CC-BY-4.0'));assert(credits.includes('Leon Made This'));
 execFileSync('python3',['-c',`import zipfile,sys,hashlib
with zipfile.ZipFile(sys.argv[1]) as z:
 assert z.testzip() is None
 assert hashlib.sha256(z.read('model.glb')).hexdigest()==sys.argv[2]
 assert hashlib.sha256(z.read('source.blend')).hexdigest()==sys.argv[3]`,join(out,built.downloads.bundle),asset.sha256.glb,asset.sha256.blend]);
}finally{await rm(out,{recursive:true,force:true});}
console.log('PASS: two new source-bound posters, preview parity, historic pins, unchanged original model and source, real download bundle/credits, single-model isolation.');

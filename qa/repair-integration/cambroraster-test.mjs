import {assertModelIntegrationIsolation} from './model-commit-isolation.mjs';
/** Focused branch integration; not a full build or visual release approval. */
import assert from 'node:assert/strict';
import {readFile,mkdtemp,rm} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {checkDelivery} from '../../site/unified-delivery-contract.mjs';
import {resolveGalleryPoster} from '../../site/gallery/wheel-presentations.js';
import {prepareModels} from '../../site/gallery/catalog-build.mjs';
import {deliverManifestAssets} from '../../site/asset-delivery.mjs';
const id='cambroraster';
const subject='fix(cambroraster): pair exact head-left pose and material repair';
const json=p=>readFile(p,'utf8').then(JSON.parse);
const manifest=await json('assets/manifest.json'),resources=await json('site/public/gallery/resources.json');
const introduced=assertModelIntegrationIsolation({id,subject,currentManifest:manifest,currentResources:resources});
const asset=manifest.assets.find(a=>a.id===id),one={...manifest,assets:[asset]};
const renderPath='site/gallery/renderer.js';
const at=(ref)=>execFileSync('git',['show',ref+':'+renderPath],{encoding:'utf8'});
const developed=at(introduced),current=await readFile(renderPath,'utf8');
let withoutModel=developed;
for(const [key,value] of [['DISPLAY_ORIENTATION_YAW',Math.PI],['DISPLAY_ORIENTATION_CANDIDATES',asset.sha256.glb]]){
 const prefix='const '+key+'={',tag=prefix+'"'+id+'": '+JSON.stringify(value)+', ';
 assert.equal(withoutModel.split(tag).length,2);
 withoutModel=withoutModel.replace(tag,prefix);
 const actual=JSON.parse(current.match(new RegExp('const '+key+'=(\\{[^\\n]+\\});'))[1]);
 assert.equal(actual[id],value);
}
assert.equal(withoutModel,at(introduced+'^'),'Only one exact-hash pose map pair changes; do not touch other runtime lines or IDs');

assert.equal(asset.quality_status,'independent_scoped_review_passed');
const poster=resolveGalleryPoster(asset,resources);assert(poster);assert.equal(poster.source_glb_sha256,asset.sha256.glb);
assert.deepEqual(prepareModels(one,resources)[0].galleryPosters,asset.galleryPosters);
const delivery=await checkDelivery({manifest:one,resources,hash:true});assert.equal(delivery.count,1);
for(const role of ['glb','blend','preview'])assert.equal(createHash('sha256').update(await readFile(asset[role])).digest('hex'),asset.sha256[role]);
assert.equal(asset.file_sizes.blend,(await readFile(asset.blend)).length);
assert.equal(asset.blend_bytes,asset.file_sizes.blend);
assert.equal(asset.file_sizes.glb,(await readFile(asset.glb)).length);
const oldGlb=await readFile('assets/additions/cambroraster/reviewed-release-20261114-07/model.glb');
const newGlb=await readFile(asset.glb);
const parse=b=>{
 assert.equal(b.readUInt32LE(0),0x46546c67);
 assert.equal(b.readUInt32LE(8),b.length);
 assert.equal(b.readUInt32LE(16),0x4e4f534a);
 const end=20+b.readUInt32LE(12);
 return [JSON.parse(b.subarray(20,end)),b.subarray(end)];
};
const [oldJson,oldBin]=parse(oldGlb),[newJson,newBin]=parse(newGlb);
assert.equal(newJson.materials[0].pbrMetallicRoughness.metallicFactor,.65);
delete newJson.materials[0].pbrMetallicRoughness.metallicFactor;
assert.deepEqual(newJson,oldJson);
assert.deepEqual(newBin,oldBin);
for(const [role,path] of Object.entries(asset.galleryPosters)){
 const bytes=await readFile('site/public/'+path);
 assert.deepEqual(bytes,await readFile('assets/candidates/cambroraster/material-20261119/'+role+'.png'));
 const file=resources.files.find(r=>r.path===path);
 assert.equal(file.bytes,bytes.length);
 assert.equal(file.sha256,createHash('sha256').update(bytes).digest('hex'));
}
const out=await mkdtemp(join(tmpdir(),'cambroraster-delivery-'));
try{
 const built=await deliverManifestAssets(one,out,{verifyHashes:true});const a=built.assets[0];
 assert.equal(a.downloads.glb,a.glb);assert.equal(a.downloads.blend,a.blend);
 for(const role of ['glb','blend'])assert.deepEqual(await readFile(join(out,a[role])),await readFile(a[role]));
 const credits=await readFile(join(out,a.downloads.credits),'utf8');assert(credits.includes('Material-only repair'));assert(credits.includes('0.65'));
 execFileSync('python3',['-c',`import zipfile,sys,hashlib,json\nz=zipfile.ZipFile(sys.argv[1]);assert z.testzip() is None\nassert hashlib.sha256(z.read('model.glb')).hexdigest()==sys.argv[2]\nassert hashlib.sha256(z.read('source.blend')).hexdigest()==sys.argv[3]`,join(out,a.downloads.bundle),a.sha256.glb,a.sha256.blend]);
}finally{await rm(out,{recursive:true,force:true});}
console.log('PASS: one-model source-bound posters, asset hashes, generated download ZIP/credits, and isolated manifest/resources at the model commit; full build/visual acceptance NOT run.');

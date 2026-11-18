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
const base='4bc5dcc7', id='archaeopteryx';
const json=p=>readFile(p,'utf8').then(JSON.parse);
const manifest=await json('assets/manifest.json'),resources=await json('site/public/gallery/resources.json');
// Verify isolation at this model's integration commit, not against other models' later work.
const integration=execFileSync('git',['log','-1','--format=%H','--fixed-strings','--grep=fix(archaeopteryx): pair material repair with reviewed gallery assets','--','assets/manifest.json'],{encoding:'utf8'}).trim();
assert.match(integration,/^[a-f0-9]{40}$/,'Missing integration commit');
const at=ref=>JSON.parse(execFileSync('git',['show',`${ref}:assets/manifest.json`],{encoding:'utf8',maxBuffer:16*1024*1024}));
const before=at(integration+'^'),introduced=at(integration);
assert.equal(manifest.assets.length,939);
assert.deepEqual(introduced.assets.filter(a=>a.id!==id),before.assets.filter(a=>a.id!==id),'Integration changed unrelated assets');
assert.deepEqual(manifest.assets.find(a=>a.id===id),introduced.assets.find(a=>a.id===id),'Current target differs from tested integration');
const asset=manifest.assets.find(a=>a.id===id),one={...manifest,assets:[asset]};
assert.equal(asset.quality_status,'work_in_progress');
const poster=resolveGalleryPoster(asset,resources);assert(poster);assert.equal(poster.source_glb_sha256,asset.sha256.glb);
assert.deepEqual(prepareModels(one,resources)[0].galleryPosters,asset.galleryPosters);
const delivery=await checkDelivery({manifest:one,resources,hash:true});assert.equal(delivery.count,1);
for(const role of ['glb','blend','preview'])assert.equal(createHash('sha256').update(await readFile(asset[role])).digest('hex'),asset.sha256[role]);
const out=await mkdtemp(join(tmpdir(),'archaeopteryx-delivery-'));
try{
 const built=await deliverManifestAssets(one,out,{verifyHashes:true});const a=built.assets[0];
 assert.equal(a.downloads.glb,a.glb);assert.equal(a.downloads.blend,a.blend);
 for(const role of ['glb','blend'])assert.deepEqual(await readFile(join(out,a[role])),await readFile(a[role]));
 const credits=await readFile(join(out,a.downloads.credits),'utf8');assert(credits.includes('Material-only repair'));assert(credits.includes('Integration and final acceptance pending'));
 execFileSync('python3',['-c',`import zipfile,sys,hashlib,json\nz=zipfile.ZipFile(sys.argv[1]);assert z.testzip() is None\nassert hashlib.sha256(z.read('model.glb')).hexdigest()==sys.argv[2]\nassert hashlib.sha256(z.read('source.blend')).hexdigest()==sys.argv[3]`,join(out,a.downloads.bundle),a.sha256.glb,a.sha256.blend]);
}finally{await rm(out,{recursive:true,force:true});}
console.log('PASS: one-model source-bound posters, asset hashes, generated download ZIP/credits, and 938 unchanged entries; full build/visual acceptance NOT run.');

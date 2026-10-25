import {historicalManifestView,successorReader} from './same-id-successors.mjs';
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,writeFile,cp,mkdir} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {inspectProductionRelease,collectProductionRelease,appendProductionRelease,productionGalleryResources,assertProductionMetadata,PRODUCTION_CHECKS} from './production-release.mjs';
import {publishedImagePaths,collectTurntables} from './turntable-delivery.mjs';
const root=resolve(process.env.PRODUCTION_SOURCE_ROOT||'.'),fixture=resolve(process.env.PRODUCTION_TEST_ROOT||'.production-release-test-fixture');
assert.notEqual(root,fixture,'Tests never approve real staging');
const descriptor='production/recovery-20261022/release.json',read=async p=>JSON.parse(await readFile(resolve(fixture,p))),save=async(p,j)=>writeFile(resolve(fixture,p),JSON.stringify(j,null,2)+'\n'),hash=b=>createHash('sha256').update(b).digest('hex');
await mkdir(fixture,{recursive:true});await cp(resolve(root,'assets'),resolve(fixture,'assets'),{recursive:true});await cp(resolve(root,'production'),resolve(fixture,'production'),{recursive:true});await cp(resolve(root,'site/public'),resolve(fixture,'site/public'),{recursive:true});
// Detached legacy adapter fixture uses only the authenticated historical source view.
await save('assets/manifest.json',historicalManifestView({manifest:JSON.parse(await readFile(resolve(root,'assets/manifest.json'))),read:successorReader(root)}));
const original=await read(descriptor),recordPath=original.assets[0].evidence.path,originalRecord=await read(recordPath),reviewPath=original.review_path;
for(const pin of original.implementation){await mkdir(resolve(fixture,pin.path,'..'),{recursive:true});await cp(resolve(root,pin.path),resolve(fixture,pin.path));}
async function repin(){const d=await read(descriptor);for(const row of d.assets)for(const key of ['metadata','evidence']){const b=await readFile(resolve(fixture,row[key].path));row[key].sha256=hash(b);row[key].bytes=b.length;}await save(descriptor,d);}
async function fixtureReview(){const d=await read(descriptor),records=await Promise.all(d.assets.map(a=>read(a.evidence.path)));await save(reviewPath,{schema_version:1,kind:'independent-production-projection-review-v1',status:'PASS',reviewer:{id:'TEST_FIXTURE_ONLY_NOT_AN_APPROVAL',task_id:'test-only-projection'},reviewed_descriptor_sha256:hash(await readFile(resolve(fixture,descriptor))),checks:Object.fromEntries(PRODUCTION_CHECKS.map(k=>[k,'PASS'])),original_acceptance_sha256:[...new Set(records.map(r=>r.original_acceptance?.sha256).filter(Boolean))].sort(),blocking_findings:[],publication_authorized:false,fixture_only:true});}
async function reset(){await save(recordPath,originalRecord);await save(descriptor,original);await repin();await fixtureReview();}
async function recordFailure(change){await reset();const r=await read(recordPath);change(r);await save(recordPath,r);await repin();await fixtureReview();await assert.rejects(()=>collectProductionRelease(fixture,descriptor));}
await test('layered production adapter negative and compatibility cases',async t=>{
 await t.test('actual staging review remains pending',async()=>{await assert.rejects(()=>collectProductionRelease(root,descriptor),/pending/);});
 await t.test('valid detached TEST fixture accepts exact three, browser stays NOT_PUBLISHED',async()=>{await reset();const a=await collectProductionRelease(fixture,descriptor);assert.equal(a.length,3);const r=await inspectProductionRelease(fixture,descriptor);assert(r.records.every(x=>x.postReleaseVerified.status==='NOT_PUBLISHED'));});
 await t.test('adapter code mutation invalidates bound projection',async()=>{await reset();const p=resolve(fixture,'site/production-release.mjs'),b=await readFile(p);try{await writeFile(p,Buffer.concat([b,Buffer.from('\n// altered fixture only\n')]));await assert.rejects(()=>collectProductionRelease(fixture,descriptor),/size changed|hash changed/);}finally{await writeFile(p,b);}});
 await t.test('scope text mutation invalidates bound projection',async()=>{await reset();const p=resolve(fixture,original.scope_document.path),b=await readFile(p);try{await writeFile(p,Buffer.concat([b,Buffer.from('altered fixture only')]));await assert.rejects(()=>collectProductionRelease(fixture,descriptor),/size changed|hash changed/);}finally{await writeFile(p,b);}});
 await t.test('wrong independent GLB subject rejected',()=>recordFailure(r=>r.original_acceptance.subject.glb_sha256='0'.repeat(64)));
 await t.test('missing independent production proof rejected',()=>recordFailure(r=>delete r.original_acceptance));
 await t.test('missing independent gate rejected',()=>recordFailure(r=>delete r.production_gates.visual));
 await t.test('real quality FAIL rejected',()=>recordFailure(r=>r.production_gates.visual.status='FAIL'));
 await t.test('explicit quality blocker rejected',()=>recordFailure(r=>r.blocking_findings.push('Geometry collision')));
 await t.test('wrong source role hash rejected',()=>recordFailure(r=>r.subject.finalBlend='0'.repeat(64)));
 await t.test('missing source dependency closure rejected',()=>recordFailure(r=>r.build_closure=[]));
 await t.test('wrong scientific brief binding rejected',()=>recordFailure(r=>r.legacy_record.scientific_brief_sha256='0'.repeat(64)));
 await t.test('known post-release failure cannot become PASS',()=>recordFailure(r=>r.postReleaseVerified.status='FAIL'));
 await t.test('poster from another GLB rejected',()=>recordFailure(r=>r.final_posters.source_glb_sha256='0'.repeat(64)));
 await t.test('poster output hash changed rejected',()=>recordFailure(r=>r.final_posters.detail.sha256='0'.repeat(64)));
 await t.test('browser mislabel on Blender capture rejected',()=>recordFailure(r=>r.final_posters.browser_capture=true));
 await t.test('self-review rejected',async()=>{await reset();const r=await read(reviewPath);r.reviewer=original.producer;await save(reviewPath,r);await assert.rejects(()=>collectProductionRelease(fixture,descriptor));});
 await t.test('stale detached review rejected',async()=>{await reset();const r=await read(reviewPath);r.reviewed_descriptor_sha256='0'.repeat(64);await save(reviewPath,r);await assert.rejects(()=>collectProductionRelease(fixture,descriptor));});
 await t.test('duplicate inventory ID cannot be silently incremented or replaced',async()=>{await reset();await assert.rejects(()=>appendProductionRelease(fixture,{assets:[{id:'spyroceras'}]},descriptor),/duplicate/);});
 await t.test('legacy no-production resource object unchanged',async()=>{const resources={posters:{old:{detail:'old.png'}}};assert.equal(await productionGalleryResources(root,{assets:[{id:'old'}]},resources),resources);});
 await t.test('legacy provisional image path and missing optional turntable unchanged',async()=>{const m={assets:[{id:'legacy-provisional'}]};assert.deepEqual(publishedImagePaths(m.assets[0],m),{manifest:'assets/turntables/legacy-provisional/v2-768-q90/turntable.json',poster:'assets/card-previews/legacy-provisional-v2-768-q90.webp',revised:false});const r=await collectTurntables(m,fixture);assert.equal(r.files.length,0);assert.throws(()=>publishedImagePaths({id:'legacy-provisional',revision:'x'},m),/explicitly authorized/);});
 await t.test('catalog cannot substitute reviewed source or public uncertainty',async()=>{await reset();const [a]=await collectProductionRelease(fixture,descriptor);assert.throws(()=>assertProductionMetadata(a,{...a,description:{en:'Intact animal',zh:'完整动物'}}));});
 await t.test('explicit new poster route extends resources, legacy entries unmodified',async()=>{await reset();const assets=await collectProductionRelease(fixture,descriptor),baseline={version:1,posters:{old:{detail:'gallery/posters/old.png'}},files:[]};const r=await productionGalleryResources(fixture,{assets},baseline);assert.deepEqual(r.posters.old,baseline.posters.old);assert.equal(r.files.length,6);assert.equal(r.posters.lituites.render_route,'blender-cycles-cpu-v1');assert(!r.posters.lituites.browser_version);assert.deepEqual(await productionGalleryResources(fixture,{assets},r),r);});
});

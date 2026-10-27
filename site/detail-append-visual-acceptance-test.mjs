import assert from 'node:assert/strict';
import test from 'node:test';
import {createHash} from 'node:crypto';
import {projectLegacyBuiltInputs,assertLegacyBuiltInputSeals,LEGACY_BUILT_INPUT_SEALS,assertLegacyDataProjection,assertVisualLedger,assertAppendRegistrationProjection,assertAppendChangeMode,freshAppendProofClosure,moduleData,APPEND_BATCH_PATH,APPEND_PRODUCTION_REGISTRY_PATH,APPEND_VISUAL_BASE,APPEND_VISUAL_PATH,APPEND_VISUAL_REVIEW_PATH} from './detail-append-visual-acceptance.mjs';
import {composeRegistry,encode,importLegacySnapshot,LEGACY_OUTPUTS,recordReference} from './model-registry.mjs';
const sha=b=>createHash('sha256').update(b).digest('hex'),enc=x=>Buffer.from(JSON.stringify(x,null,2)+'\n');
const IDS='acanthodes alalcomenaeus birkenia camptosaurus dapedium diictodon dimetrodon diplocaulus eusthenopteron habelia mammuthus nipponites paradoxides proganochelys pterichthyodes rhamphorhynchus thrinaxodon xiphactinus yochelcionella'.split(' ');
function projection(){
 const records=IDS.map(id=>({id,asset:{id,value:1},gallery:{wheel_framing:null,poster:{detail:id+'.png'},files:[{path:id+'.png',sha256:'a'.repeat(64),bytes:1}]},turntable:{asset:null,poster:{id,path:id+'.webp'}}}));
 const before={manifest:{assets:Array.from({length:602},(_,i)=>({id:'old'+i,value:i})),publication:{same_id_successors:{original:true}}},catalog:{version:1,worlds:[],packs:[]},turntables:{version:1,assets:[],posters:[{id:'old0'}]},gallery:{version:1,posters:{old0:{detail:'old.png'}},files:[{path:'old.png'}]},framing:{old0:{}},detail:{version:1,kind:'detail',source_commit:'a'.repeat(40),renderer_input_sha256:'b'.repeat(64),renderer_policy:{},migration_scope:{original:true},presentations:Object.fromEntries(Array.from({length:264},(_,i)=>['old'+i,{id:'old'+i}]))},proofs:{version:1,receipts:[{id:'old'}]}};
 const after=structuredClone(before);after.manifest.publication.same_id_successor_append={path:'append'};after.manifest.assets.push(...structuredClone(records.map(r=>r.asset)));after.catalog.packs.push({id:'reviewed-static4-20261026',asset_ids:IDS});after.turntables.posters.push(...records.map(r=>r.turntable.poster));for(const r of records){after.gallery.posters[r.id]=r.gallery.poster;after.gallery.files.push(...r.gallery.files);after.detail.presentations[r.id]={id:r.id};}after.proofs.receipts.push({renderer_input_sha256:before.detail.renderer_input_sha256,assets:Object.fromEntries(IDS.map(id=>[id,{}]))});return {before,after,records};
}
test('exact602/264 inverse retains old evidence while selecting every19',()=>assert.equal(assertLegacyDataProjection(projection()).legacy_details,264));
for(const [name,mutate]of [
 ['old metadata',f=>f.after.manifest.assets[0].value++],['old order',f=>f.after.manifest.assets.reverse()],['unknown new model',f=>f.after.manifest.assets.push({id:'carnotaurus'})],['header',f=>f.after.manifest.publication.extra=true],['new metadata',f=>f.after.manifest.assets.at(-1).value=2],['old resource',f=>f.after.gallery.posters.old0.detail='wrong'],['extra resource',f=>f.after.gallery.files.push({path:'extra.png'})],['old facet',f=>f.after.catalog.worlds.push({id:'x'})],['wrong pack',f=>f.after.catalog.packs[0].asset_ids=[]],['old card',f=>f.after.turntables.posters[0].path='wrong'],['old framing',f=>f.after.framing.old0={changed:1}],['old detail',f=>f.after.detail.presentations.old0={changed:1}],['new detail missing',f=>delete f.after.detail.presentations.acanthodes],['renderer policy',f=>f.after.detail.renderer_policy.changed=true],['old receipt',f=>f.after.proofs.receipts[0].id='changed'],['missing fresh',f=>f.after.proofs.receipts.pop()],['unknown fresh',f=>f.after.proofs.receipts[1].assets.carnotaurus={}],['partial fresh',f=>delete f.after.proofs.receipts[1].assets.acanthodes],['new index execution field',f=>f.after.detail.execute='evil']
])test('inverse rejects '+name,()=>{const f=projection();mutate(f);assert.throws(()=>assertLegacyDataProjection(f));});
function ledger(){const path='site/detail-append-visual-acceptance.mjs',bytes=Buffer.from('fixture'),descriptor={version:1,kind:'exact602-264-plus-explicit19-visual-continuation-v1',baseline:APPEND_VISUAL_BASE,append:{path:'append'},new_ids:IDS,producer:{id:'producer',task_id:'/root/producer'},files:[{path,sha256:sha(bytes),bytes:bytes.length,role:'independently-reviewed-offline-contract'}],review_path:APPEND_VISUAL_REVIEW_PATH,publication_authorized:false,reviewer_authority:false};const review={kind:'independent-exact602-264-plus19-visual-continuation-review-v1',status:'PASS',descriptor:{path:APPEND_VISUAL_PATH,sha256:sha(enc(descriptor))},baseline:APPEND_VISUAL_BASE,new_ids:IDS,reviewer:{id:'reviewer',task_id:'/root/reviewer'},blocking_findings:[],checks:Object.fromEntries(['exact_changed_file_inventory','unchanged_runtime_dependency_closure','original602_inverse_projection','original264_and_receipts_unchanged','baseline_snapshot_complete_and_exact','historical_failed_artifact_authentication','fresh19_profile_and_all_negative_controls','mandatory_dist_and_public_execution'].map(k=>[k,'PASS'])),publication_authorized:false,reviewer_authority:false};return {descriptor,review,changes:[path,APPEND_VISUAL_PATH,APPEND_VISUAL_REVIEW_PATH],read:()=>bytes,baseExists:()=>true,closure:[]};}
const rebind=f=>{f.review.descriptor.sha256=sha(enc(f.descriptor));};
test('exact independent ledger accepts its explicitly reviewed offline contract',()=>assert.equal(assertVisualLedger(ledger()).changed_files,1));
for(const p of ['site/ci-lean-release-test.mjs','site/concept-landair-successor-test.mjs'])test('ledger accepts exact reviewed fixture '+p+', never CI runtime or workflow code',()=>{const f=ledger();f.descriptor.files[0].path=p;f.changes[0]=p;rebind(f);assert.equal(assertVisualLedger(f).changed_files,1);for(const forbidden of ['site/ci-lean-regressions.mjs','site/ci-lean-scope.mjs','site/ci-build-release.mjs','.github/workflows/pages.yml','site/ci-other-test.mjs']){const bad=structuredClone(f.descriptor);bad.files[0].path=forbidden;const g={...f,descriptor:bad,review:structuredClone(f.review),changes:[forbidden,APPEND_VISUAL_PATH,APPEND_VISUAL_REVIEW_PATH]};rebind(g);assert.throws(()=>assertVisualLedger(g));}});
test('ledger accepts only the exact independently reviewed historical authority fixture test',()=>{const f=ledger(),p='site/detail-capture-authority-test.mjs';f.descriptor.files[0].path=p;f.changes[0]=p;rebind(f);assert.equal(assertVisualLedger(f).changed_files,1);for(const forbidden of ['site/detail-capture-authority.mjs','site/detail-other-test.mjs']){const bad=structuredClone(f.descriptor);bad.files[0].path=forbidden;const g={...f,descriptor:bad,review:structuredClone(f.review),changes:[forbidden,APPEND_VISUAL_PATH,APPEND_VISUAL_REVIEW_PATH]};rebind(g);assert.throws(()=>assertVisualLedger(g));}});
for(const [name,mutate]of [
 ['unlisted path',f=>f.changes.push('site/gallery/renderer.js')],['runtime file even with recalculated digest',f=>{f.descriptor.files[0].path='site/gallery/renderer.js';f.changes[0]='site/gallery/renderer.js';rebind(f);}],['arbitrary code',f=>{f.descriptor.files[0].path='site/evil.mjs';f.changes[0]='site/evil.mjs';rebind(f);}],['changed bytes',f=>f.read=()=>Buffer.from('changed')],['self review',f=>f.review.reviewer.id='producer'],['cross alias self review',f=>f.review.reviewer.id=' /root/Producer '],['missing independent check',f=>delete f.review.checks.fresh19_profile_and_all_negative_controls],['false check',f=>f.review.checks.original264_and_receipts_unchanged='PENDING'],['old delivery overwritten',f=>{f.descriptor.files[0].path='assets/old.glb';f.descriptor.files[0].role='exact-reviewed-new-delivery';f.changes[0]='assets/old.glb';f.closure=['assets/old.glb'];rebind(f);}],['authority escalation',f=>{f.descriptor.publication_authorized=true;rebind(f);}],['wrong baseline',f=>{f.descriptor.baseline='0'.repeat(40);rebind(f);}]
])test('review ledger rejects '+name,()=>{const f=ledger();mutate(f);assert.throws(()=>assertVisualLedger(f));});

test('data-only modules reject trailing executable statements and dynamic expressions before import',()=>{assert.deepEqual(moduleData(Buffer.from('export default {"value":1};\n')),{value:1});for(const text of ['export default {}; process.exit(0);','export default (()=>({}))();','import x from "private"; export default {};','export default {"value":1}; /* trailing executable container */'])assert.throws(()=>moduleData(Buffer.from(text)));});


test('new wheel framing uses exact authenticated wheel_framing value',()=>{const f=projection();f.records[0].gallery.wheel_framing={zoom:1.25,center:[0,1,0]};f.after.framing.acanthodes=structuredClone(f.records[0].gallery.wheel_framing);assertLegacyDataProjection(f);});
for(const [name,mutate]of [
 ['missing declaration',f=>delete f.records[0].gallery.wheel_framing],
 ['null changed to present',f=>f.after.framing.acanthodes={}],
 ['non-null omitted',f=>f.records[0].gallery.wheel_framing={zoom:1.25}],
 ['value changed',f=>{f.records[0].gallery.wheel_framing={zoom:1.25};f.after.framing.acanthodes={zoom:2};}],
 ['wrong historical framing field',f=>{f.records[0].gallery.framing={zoom:2};f.after.framing.acanthodes={zoom:2};}]
])test('new wheel framing rejects '+name,()=>{const f=projection();mutate(f);assert.throws(()=>assertLegacyDataProjection(f));});
for(const [name,mutate]of [
 ['root alias self review',f=>{f.review.reviewer={id:' /root/PRODUCER ',task_id:'producer'};}],
 ['swapped aliases',f=>{f.descriptor.producer={id:'producer',task_id:'reviewer'};f.review.reviewer={id:'reviewer',task_id:'producer'};rebind(f);}],
 ['conflicting preparer aliases',f=>{f.descriptor.producer.task_id='/root/other';rebind(f);}],
 ['conflicting reviewer aliases',f=>f.review.reviewer.task_id='/root/other'],
 ['unknown actor',f=>f.review.reviewer={id:'unknown',task_id:'/root/unknown'}],
 ['pending actor',f=>f.review.reviewer={id:'pending-review',task_id:'/root/pending-review'}],
 ['extra identity field',f=>f.review.reviewer.alias='producer']
])test('canonical actor rejects '+name,()=>{const f=ledger();mutate(f);assert.throws(()=>assertVisualLedger(f));});
test('canonical actor accepts case and root task aliases consistently',()=>{const f=ledger();f.review.reviewer={id:' /root/ReVieWer ',task_id:' reviewer '};assertVisualLedger(f);});
for(const status of ['A','M'])test('mode accepts exact regular '+status,()=>assertAppendChangeMode({status,before:status==='M'?'100644':null,after:'100644'}));
for(const [name,value]of [
 ['historical executable mode change',{status:'M',before:'100755',after:'100644'}],
 ['new executable',{status:'A',before:null,after:'100755'}],
 ['symlink',{status:'M',before:'120000',after:'100644'}],
 ['overwrite disguised as addition',{status:'A',before:'100644',after:'100644'}],
 ['missing original modification',{status:'M',before:null,after:'100644'}],
 ['deleted file',{status:'D',before:'100644',after:null}]
])test('mode rejects '+name,()=>assert.throws(()=>assertAppendChangeMode(value)));

const RELEASE='reviewed-static4-20261026',HASH='a'.repeat(64);
function registryRecord(id,pack='old-pack'){
 const root=`assets/additions/${id}/r001`,files=['','-wheel'].map(suffix=>({path:`gallery/posters/${id}${suffix}.png`,sha256:HASH,bytes:1}));
 return {version:1,id,asset:{id,revision:'r001',name:{en:id,zh:id},worlds:['old-world'],packs:[pack],glb:root+'/model.glb',blend:root+'/source.blend',preview:root+'/preview.png',sha256:{glb:HASH,blend:HASH,preview:HASH}},catalog:{pack_ids:[pack],legacy_pack_ids:[]},gallery:{poster:{detail:files[0].path,wheel:files[1].path,source_glb_sha256:HASH},files,wheel_framing:null},turntable:{asset:null,poster:null}};
}
const definition=id=>({id,name:{en:id,zh:id},description:{en:'bounded static4',zh:'有限静态4视图'}});
let registrationFixture;
function registration(){
 if(!registrationFixture){
  const old=Array.from({length:601},(_,i)=>registryRecord('old-'+i));
  const snapshot={manifest:{version:1,assets:old.map(r=>r.asset)},catalog:{version:1,worlds:[{id:'old-world',name:{en:'Old world',zh:'原世界'}}],packs:[{...definition('old-pack'),asset_ids:old.map(r=>r.id)}],legacy_memberships:[]},gallery:{version:1,posters:Object.fromEntries(old.map(r=>[r.id,r.gallery.poster])),files:old.flatMap(r=>r.gallery.files)},framing:{},turntables:{version:1,assets:[],posters:[]}};
  const beforeRegistry=importLegacySnapshot(snapshot,{sourceCommit:APPEND_VISUAL_BASE,sourcePins:Object.fromEntries(Object.entries(LEGACY_OUTPUTS).map(([key,path])=>[key,{path,sha256:sha(encode(snapshot[key]))}]))});
  const historic=registryRecord('old-601','old-batch');beforeRegistry.records.push(historic);beforeRegistry.batches.push({version:1,id:'old-batch',records:[recordReference(historic)],definitions:{worlds:[],packs:[definition('old-batch')]},evidence:[{path:'production/old/release.json',sha256:HASH}]});
  const records=IDS.map(id=>registryRecord(id,RELEASE)),releasePin={path:`production/${RELEASE}/release.json`,sha256:'b'.repeat(64),bytes:1};
  const append={release_id:RELEASE,entries:records.map(r=>{const pin=recordReference(r);return {id:r.id,record:{path:pin.path,sha256:pin.sha256,bytes:Buffer.byteLength(encode(r))}};}),content_releases:[{descriptor:releasePin}]};
  const batch={version:1,id:RELEASE,records:records.map(recordReference),definitions:{worlds:[],packs:[definition(RELEASE)]},evidence:[{path:releasePin.path,sha256:releasePin.sha256}]};
  const afterRegistry={baseline:structuredClone(beforeRegistry.baseline),records:[...structuredClone(beforeRegistry.records),...records],batches:[...structuredClone(beforeRegistry.batches),batch]};
  const beforeProduction={schema_version:1,kind:'production-release-set-v1',descriptors:[{path:'production/old/release.json',sha256:HASH,bytes:1,compatibility:{original:true}}],asset_ids:['old-601']};
  const afterProduction={...structuredClone(beforeProduction),descriptors:[...structuredClone(beforeProduction.descriptors),releasePin],asset_ids:[...beforeProduction.asset_ids,...IDS]};
  registrationFixture={beforeRegistry,afterRegistry,beforeProduction,afterProduction,append,records,catalog:composeRegistry(afterRegistry).catalog};
 }
 return Object.fromEntries(Object.entries(registrationFixture).map(([key,value])=>[key,structuredClone(value)]));
}
test('exact registration inverse binds 602 old records, one batch, one pack and ordered production append',()=>assert.deepEqual(assertAppendRegistrationProjection(registration()),[APPEND_BATCH_PATH,APPEND_PRODUCTION_REGISTRY_PATH]));
for(const [name,mutate]of [
 ['baseline header rewrite',f=>f.afterRegistry.baseline.headers.manifest.changed=true],
 ['rehashed old record',f=>{const r=f.afterRegistry.records.at(-20);r.asset.name.en='changed';f.afterRegistry.batches[0].records=[recordReference(r)];}],
 ['old batch evidence',f=>f.afterRegistry.batches[0].evidence[0].sha256='f'.repeat(64)],
 ['old record removed',f=>f.afterRegistry.records.splice(0,1)],
 ['extra registry model',f=>f.afterRegistry.records.push(registryRecord('unexpected',RELEASE))],
 ['duplicate batch',f=>f.afterRegistry.batches.push(structuredClone(f.afterRegistry.batches.at(-1)))],
 ['wrong new batch owner',f=>f.afterRegistry.batches.at(-1).id='other-batch'],
 ['wrong batch pin',f=>f.afterRegistry.batches.at(-1).records[0].sha256='f'.repeat(64)],
 ['wrong append pin',f=>f.append.entries[0].record.sha256='f'.repeat(64)],
 ['wrong append byte count',f=>f.append.entries[0].record.bytes++],
 ['wrong appended record',f=>f.records[0].asset.name.en='changed'],
 ['extra world',f=>f.afterRegistry.batches.at(-1).definitions.worlds.push({id:'new-world',name:{en:'New',zh:'新'}})],
 ['extra pack',f=>f.afterRegistry.batches.at(-1).definitions.packs.push(definition('new-pack'))],
 ['pack definition mismatch',f=>f.catalog.packs.find(p=>p.id===RELEASE).description.en='changed'],
 ['pack membership order',f=>f.catalog.packs.find(p=>p.id===RELEASE).asset_ids.reverse()],
 ['unexpected evidence',f=>f.afterRegistry.batches.at(-1).evidence.push({path:'production/extra.json',sha256:HASH})],
 ['wrong release path',f=>f.append.content_releases[0].descriptor.path='production/other/release.json'],
 ['extra release',f=>f.append.content_releases.push(structuredClone(f.append.content_releases[0]))],
 ['release compatibility override',f=>f.append.content_releases[0].descriptor.compatibility={}],
 ['historic production pin changed',f=>f.afterProduction.descriptors[0].sha256='f'.repeat(64)],
 ['historic production compatibility changed',f=>f.afterProduction.descriptors[0].compatibility.original=false],
 ['production added descriptor wrong',f=>f.afterProduction.descriptors.at(-1).bytes++],
 ['production order changed',f=>f.afterProduction.descriptors.reverse()],
 ['production membership order changed',f=>f.afterProduction.asset_ids.reverse()],
 ['production headers changed',f=>f.afterProduction.extra=true],
 ['Carno added',f=>f.afterProduction.asset_ids.push('carnotaurus')]
])test('registration inverse rejects '+name,()=>{const f=registration();mutate(f);assert.throws(()=>assertAppendRegistrationProjection(f));});
function registrationLedger(){
 const f=ledger();f.registration=registration();const files=new Map([[APPEND_BATCH_PATH,enc(f.registration.afterRegistry.batches.at(-1))],[APPEND_PRODUCTION_REGISTRY_PATH,enc(f.registration.afterProduction)]]);
 f.descriptor.files=[...files].map(([path,bytes])=>({path,sha256:sha(bytes),bytes:bytes.length,role:'validated-registration-append'})).sort((a,b)=>a.path.localeCompare(b.path));f.changes=f.descriptor.files.map(p=>p.path);f.read=path=>files.get(path);f.baseExists=path=>path===APPEND_PRODUCTION_REGISTRY_PATH;rebind(f);return f;
}
test('ledger admits only the two inverse-validated registration paths',()=>assert.equal(assertVisualLedger(registrationLedger()).changed_files,2));
for(const [name,mutate]of [
 ['absent validation',f=>{delete f.registration;f.closure=[APPEND_BATCH_PATH,APPEND_PRODUCTION_REGISTRY_PATH];}],
 ['old batch overwritten',f=>f.baseExists=()=>true],
 ['production registry treated as new',f=>f.baseExists=()=>false],
 ['registry wrong role',f=>{f.descriptor.files[0].role='exact-reviewed-new-delivery';rebind(f);}],
 ['other batch path',f=>{const old=f.read;f.descriptor.files[1].path='registry/batches/arbitrary.json';f.changes[1]='registry/batches/arbitrary.json';f.read=p=>p==='registry/batches/arbitrary.json'?old(APPEND_BATCH_PATH):old(p);rebind(f);}],
 ['registration object differs from bytes',f=>{f.registration.afterRegistry.batches.at(-1).definitions.packs[0].description.en='other';f.registration.catalog.packs.find(p=>p.id===RELEASE).description.en='other';}]
])test('registration ledger rejects '+name,()=>{const f=registrationLedger();mutate(f);assert.throws(()=>assertVisualLedger(f));});

for(const path of ['.github/workflows/reviewed-static4-presentation.yml','qa/static4-presentation-inputs.json','assets/additions/coquina-outcrop/capture-only.glb'])test('final ledger rejects temporary capture-only path '+path,()=>{const f=ledger();f.descriptor.files[0].path=path;f.changes[0]=path;f.baseExists=()=>false;rebind(f);assert.throws(()=>assertVisualLedger(f));});

function proofClosure(){
 const prefix='qa/detail-presentation-evidence/captures/123/',index=Buffer.from('export default {"kind":"fixture"};\n'),decoded=enc({kind:'fixture'}),files=new Map([[prefix+'original-capture-index.js',index],[prefix+'independent-decoded-checks.json',decoded]]);
 const before={receipts:[{original:'immutable'}]},fresh={run_id:123,capture_revision:2,scope_kind:'bounded-fresh-subset-v1',artifact_prefix:'fresh',capture_index_path:prefix+'original-capture-index.js',capture_index_sha256:sha(index),decoded_proof:{path:prefix+'independent-decoded-checks.json',sha256:sha(decoded)},assets:Object.fromEntries(IDS.map(id=>[id,{}]))};
 return {before,after:{receipts:[...structuredClone(before.receipts),fresh]},read:p=>{assert(files.has(p),'Missing exact proof file');return files.get(p);},files};
}
test('fresh proof closure includes only exact pinned index and decoded proof, not old receipts',()=>{const f=proofClosure();assert.deepEqual(freshAppendProofClosure(f),[...f.files.keys()]);});
for(const [name,mutate]of [
 ['old receipt changed',f=>f.after.receipts[0].original='changed'],
 ['missing fresh receipt',f=>f.after.receipts.pop()],
 ['bad run',f=>f.after.receipts[1].run_id=-1],
 ['duplicate run',f=>f.after.receipts.push(structuredClone(f.after.receipts[1]))],
 ['wrong revision',f=>f.after.receipts[1].capture_revision=1],
 ['wrong scope',f=>f.after.receipts[1].scope_kind='migration'],
 ['wrong prefix',f=>f.after.receipts[1].artifact_prefix='detail-capture'],
 ['index outside run',f=>f.after.receipts[1].capture_index_path='site/evil.js'],
 ['decoded outside run',f=>f.after.receipts[1].decoded_proof.path='site/evil.mjs'],
 ['decoded traversal',f=>f.after.receipts[1].decoded_proof.path='qa/detail-presentation-evidence/captures/123/../evil.json'],
 ['missing decoded proof',f=>delete f.after.receipts[1].decoded_proof],
 ['missing selected ID',f=>delete f.after.receipts[1].assets.acanthodes],
 ['unknown ID',f=>f.after.receipts[1].assets.carnotaurus={}],
 ['wrong index pin',f=>f.after.receipts[1].capture_index_sha256='f'.repeat(64)],
 ['wrong decoded pin',f=>f.after.receipts[1].decoded_proof.sha256='f'.repeat(64)],
 ['invalid decoded pin',f=>f.after.receipts[1].decoded_proof.sha256='not-a-hash'],
 ['missing bytes',f=>f.files.delete(f.after.receipts[1].decoded_proof.path)],
 ['decoded invalid JSON even repinned',f=>{const r=f.after.receipts[1],b=Buffer.from('malformed');f.files.set(r.decoded_proof.path,b);r.decoded_proof.sha256=sha(b);}],
 ['index executable tail even repinned',f=>{const r=f.after.receipts[1],b=Buffer.from('export default {}; process.exit(0);');f.files.set(r.capture_index_path,b);r.capture_index_sha256=sha(b);}]
])test('fresh proof closure rejects '+name,()=>{const f=proofClosure();mutate(f);assert.throws(()=>freshAppendProofClosure(f));});
test('ledger accepts exact decoded proof path only via validated fresh closure',()=>{const p=proofClosure(),f=ledger(),path=p.after.receipts[1].decoded_proof.path,bytes=p.read(path);f.descriptor.files=[{path,sha256:sha(bytes),bytes:bytes.length,role:'exact-reviewed-new-delivery'}];f.changes=[path,APPEND_VISUAL_PATH,APPEND_VISUAL_REVIEW_PATH];f.read=p.read;f.baseExists=()=>false;f.closure=freshAppendProofClosure(p);rebind(f);assertVisualLedger(f);f.closure=[];assert.throws(()=>assertVisualLedger(f),/Unclassified/);});

function builtProjection(){
 const f=projection();for(const id of IDS){f.after.gallery.posters[id]={detail:'gallery/posters/'+id+'.png',wheel:'gallery/posters/'+id+'-wheel.png'};}f.after.gallery.files=[...f.before.gallery.files,...IDS.flatMap(id=>[id,id+'-wheel'].map(n=>({path:'gallery/posters/'+n+'.png',sha256:'a'.repeat(64),bytes:1})))];
 const builtManifest=structuredClone(f.after.manifest);for(const a of builtManifest.assets)a.file_sizes={glb:100,blend:200,bundle:250};
 return {baselineManifest:f.before.manifest,sourceManifest:f.after.manifest,baselineResources:f.before.gallery,sourceResources:f.after.gallery,builtManifest,builtResources:{...structuredClone(f.after.gallery),production_projection:true}};
}
test('built input projection retains delivered old602 bytes rather than substituting raw source',()=>{const f=builtProjection(),out=projectLegacyBuiltInputs(f),expected=structuredClone(f.builtManifest);expected.assets=expected.assets.slice(0,602);delete expected.publication.same_id_successor_append;assert.deepEqual(out.manifestBytes,enc(expected));assert.deepEqual(out.resourcesBytes,enc({...f.baselineResources,production_projection:true}));assert.notDeepEqual(out.manifestBytes,enc(f.baselineManifest));});
for(const [name,mutate]of [
 ['raw602 in place of actual built621',f=>f.builtManifest=structuredClone(f.baselineManifest)],['missing delivered ID',f=>f.builtManifest.assets.pop()],['extra delivered ID',f=>f.builtManifest.assets.push({id:'carnotaurus'})],['duplicate delivered ID',f=>f.builtManifest.assets[2].id=f.builtManifest.assets[1].id],['delivered order',f=>f.builtManifest.assets.reverse()],['old source metadata',f=>f.sourceManifest.assets[0].value++],['old source order',f=>f.sourceManifest.assets.reverse()],['publication pointer missing',f=>delete f.sourceManifest.publication.same_id_successor_append],['delivered publication change',f=>f.builtManifest.publication.extra=true],['delivered GLB binding',f=>f.builtManifest.assets[0].glb='wrong.glb'],['old resource mutation',f=>f.builtResources.posters.old0.detail='changed.png'],['resource extra field',f=>f.builtResources.extra=true],['raw resources not delivery',f=>delete f.builtResources.production_projection],['new source poster missing',f=>delete f.sourceResources.posters.acanthodes],['new source file missing',f=>f.sourceResources.files.pop()],['new source poster aliases old',f=>f.sourceResources.posters.acanthodes.detail='old.png'],['old source resource mutated with build',f=>{f.sourceResources.posters.old0.detail='changed';f.builtResources.posters.old0.detail='changed';}]
])test('built input projection rejects '+name,()=>{const f=builtProjection();mutate(f);assert.throws(()=>projectLegacyBuiltInputs(f));});
test('one immutable historical built/report seal set, not caller-selected expected hashes',()=>{assert.deepEqual(LEGACY_BUILT_INPUT_SEALS,{report_sha256:'9fdd81660e6c95108eb62747bdb5dc6497346614364c3eea7d018bc0fa8f6d9a',manifest_sha256:'443a4b788511cec6b642691faaa6da78244d4f73948984e1f08e14a90ea1d589',resources_sha256:'c01b9e47d478992bdb35497567ae00e046b994b0a1f9e715aa177e087326b8b6'});assert(Object.isFrozen(LEGACY_BUILT_INPUT_SEALS));for(const reportSha256 of [LEGACY_BUILT_INPUT_SEALS.report_sha256,'0'.repeat(64),undefined])assert.throws(()=>assertLegacyBuiltInputSeals({manifestBytes:Buffer.from('{}'),resourcesBytes:Buffer.from('{}'),reportSha256}));});

// Browser source binding is shared by dist collection, retained verification,
// public reviewed-state, and the offline scope check; no Chromium is launched.
import {detailAppendScopeSource} from './detail-append-cohort.mjs';
function scopeInputs(){
 const asset=id=>({id,units:'meters',dimensions:{x:1,y:2,z:3},glb:`assets/${id}/model.glb`,blend:`assets/${id}/source.blend`,preview:`assets/${id}/preview.png`,sha256:{glb:'a'.repeat(64),blend:'b'.repeat(64),preview:'c'.repeat(64)},description:{en:'bounded original representation'},qa:`assets/${id}/qa.json`,material_count:2});
 const source={version:1,publication:{same_id_successors:{path:'selection.json'},same_id_successor_append:{path:'append.json',sha256:'d'.repeat(64)}},assets:[asset('old'),asset('new')]};
 const built=structuredClone(source);for(const a of built.assets){delete a.qa;a.material_count=3;a.file_sizes={glb:100,blend:200,bundle:150};a.glb_bytes=100;a.blend_bytes=200;a.downloads={glb:a.glb,blend:a.blend,bundle:`assets/downloads/${a.id}.zip`,credits:`assets/downloads/${a.id}-CREDITS.txt`};a.worlds=['derived'];a.packs=['derived'];a.card_preview=`assets/card-previews/${a.id}.webp`;a.turntable={frame_count:36};}
 return {source,built,read:path=>{assert.equal(path,'assets/manifest.json');return enc(source);}};
}
test('append browser uses exact source for selection while retaining actual built subject binding',()=>{const f=scopeInputs(),before=JSON.stringify(f);assert.deepEqual(detailAppendScopeSource({manifest:f.built,read:f.read}),f.source);assert.deepEqual(detailAppendScopeSource({manifest:f.source,read:f.read}),f.source);assert.equal(JSON.stringify(f),before);});
for(const [label,mutate]of [
 ['publication',f=>{f.built.publication.same_id_successor_append.sha256='e'.repeat(64);}],
 ['missing append',f=>{delete f.built.publication.same_id_successor_append;}],
 ['missing source append',f=>{delete f.source.publication.same_id_successor_append;}],
 ['top-level extra',f=>{f.built.release_override=true;}],
 ['order',f=>{f.built.assets.reverse();}],
 ['duplicate',f=>{f.built.assets[1]=structuredClone(f.built.assets[0]);}],
 ['extra ID',f=>{f.built.assets.push({...f.built.assets[1],id:'third'});}],
 ['missing ID',f=>{f.built.assets.pop();}],
 ['units',f=>{delete f.built.assets[1].units;}],
 ['dimensions',f=>{f.built.assets[1].dimensions.y=9;}],
 ['GLB path',f=>{f.built.assets[1].glb='assets/other/model.glb';}],
 ['GLB hash',f=>{f.built.assets[1].sha256.glb='f'.repeat(64);}],
 ['native hash',f=>{f.built.assets[1].sha256.blend='f'.repeat(64);}],
 ['preview hash',f=>{f.built.assets[1].sha256.preview='f'.repeat(64);}],
 ['scientific text',f=>{f.built.assets[1].description.en='unreviewed entire animal';}],
 ['old subject',f=>{f.built.assets[0].units='millimeters';}],
 ['unrecognized field',f=>{f.built.assets[1].unknown_render_override=1;}],
 ['duplicate source',f=>{f.source.assets[1]=structuredClone(f.source.assets[0]);f.built=structuredClone(f.source);}]
])test('append browser rejects changed source binding: '+label,()=>{const f=scopeInputs();mutate(f);assert.throws(()=>detailAppendScopeSource({manifest:f.built,read:f.read}));});
test('non-append historical browser path keeps its original manifest input',()=>{const source={assets:[{id:'old'}]},manifest={assets:[{id:'old',file_sizes:{glb:100}}]};assert.equal(detailAppendScopeSource({manifest,read:()=>enc(source)}),manifest);});

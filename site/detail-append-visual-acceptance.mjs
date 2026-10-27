/** One exact 19-ID append continuation. Never extends the historical visual verdict. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,mkdtemp,rm,symlink} from 'node:fs/promises';
import {resolve,join,dirname} from 'node:path';
import {tmpdir} from 'node:os';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {immutableGitEnv} from './ci-git.mjs';
import {successorContext,successorReader} from './same-id-successors.mjs';
import {selectedDetailAppend} from './detail-append-cohort.mjs';
import {assertRegistryAppend,composeRegistry,encode,recordReference} from './model-registry.mjs';
import {readRegistry,readRegistryAtCommit} from './model-registry-cli.mjs';
export const APPEND_VISUAL_BASE='05cf27f6ccee363043f4adf19ed3acbad71439d9';
export const APPEND_VISUAL_PATH='production/reviewed-static4-20261026/visual-continuation.json';
export const APPEND_VISUAL_REVIEW_PATH='production/reviewed-static4-20261026/visual-continuation-review.json';
export const APPEND_THREE_CASE_REVIEW_PATH='qa/detail-presentation-evidence/reviews/40479699435-append19-three-case-visual-disposition.json';
export const APPEND_THREE_CASE_REVIEW_SHA='db7ba824edeccf11bc72e25176583344b10eb5698c9a959225897cd4b5303137';
const IDS='acanthodes alalcomenaeus birkenia camptosaurus dapedium diictodon dimetrodon diplocaulus eusthenopteron habelia mammuthus nipponites paradoxides proganochelys pterichthyodes rhamphorhynchus thrinaxodon xiphactinus yochelcionella'.split(' ');
export const APPEND_BATCH_PATH='registry/batches/reviewed-static4-20261026.json';
export const APPEND_PRODUCTION_REGISTRY_PATH='production/production-releases-r002.json';
const DATA_PATHS=['assets/manifest.json','site/catalog-data.json','assets/turntables/index.json','site/public/gallery/resources.json','site/gallery/wheel-framing.json','site/gallery/detail-presentations-index.js','site/gallery/detail-input-proofs.js'];
// Not a configurable allowlist: these offline contracts/tests cannot replace any
// gallery executable, CSS, HTML, renderer, delivery policy or Vite build code.
// The two named quality contracts only extend the exact compute cohort, not thresholds.
export const APPEND_CONTRACT_PATHS=Object.freeze([
 'site/model-task-static4-acceptance.mjs','site/model-task-static4-acceptance-test.mjs','site/static4-source-profiles.mjs','site/static4-test-observed-checklists.mjs',
 'site/production-release.mjs','site/typed-production-release.mjs','site/asset-delivery.mjs','site/initial-release.mjs','site/initial-release-test.mjs',
 'site/same-id-append-continuation.mjs','site/same-id-append-continuation-test.mjs','site/same-id-successors.mjs','site/model-registry-sync.mjs',
 'site/detail-append-cohort.mjs','site/detail-browser-scope-test.mjs','site/detail-presentation-browser-test.mjs','site/detail-visual-disposition-test.mjs',
 'site/detail-visual-acceptance.mjs','site/detail-append-visual-acceptance.mjs','site/detail-append-visual-acceptance-test.mjs',
 'site/detail-capture-authority-test.mjs','site/ci-lean-release-test.mjs','site/concept-landair-successor-test.mjs',
 'site/detail-presentation-quality.mjs','site/detail-presentation-quality-test.mjs'
]);
const sha=b=>createHash('sha256').update(b).digest('hex'),copy=x=>structuredClone(x);
const git=(root,...args)=>execFileSync('git',args,{cwd:root,env:immutableGitEnv(),maxBuffer:64*1024**2,timeout:60000});
const raw=(root,path)=>git(root,'show',APPEND_VISUAL_BASE+':'+path);
const json=b=>JSON.parse(b.toString());
export const moduleData=b=>{const s=b.toString();assert(s.startsWith('export default '));return JSON.parse(s.slice(15).trim().replace(/;$/,''));};
const exact=(x,fields,label)=>assert.deepEqual(Object.keys(x||{}).sort(),[...fields].sort(),label);
const pinned=(bytes,pin)=>{assert.equal(bytes.length,pin.bytes);assert.equal(sha(bytes),pin.sha256);};
const removeKeys=(x,ids)=>Object.fromEntries(Object.entries(x).filter(([id])=>!ids.has(id)));
export function assertLegacyDataProjection({before,after,records}){
 const ids=records.map(r=>r.id);assert.deepEqual([...ids].sort(),IDS);const selected=new Set(ids),old=before.manifest.assets;
 assert.equal(old.length,602);assert.equal(after.manifest.assets.length,621);assert.deepEqual(after.manifest.assets.filter(a=>!selected.has(a.id)),old,'Original 602 values/order changed');
 const projected=copy(after.manifest);projected.assets=old;delete projected.publication.same_id_successor_append;assert.deepEqual(projected,before.manifest,'Original manifest headers changed');
 for(const r of records)assert.deepEqual(after.manifest.assets.find(a=>a.id===r.id),r.asset,'New asset differs from authenticated record');
 const resources=copy(after.gallery),newPaths=new Set(records.flatMap(r=>r.gallery.files.map(f=>f.path)));resources.posters=removeKeys(resources.posters,selected);resources.files=resources.files.filter(f=>!newPaths.has(f.path));assert.deepEqual(resources,before.gallery,'Original gallery resources changed');
 assert.deepEqual(Object.keys(after.gallery.posters).filter(id=>!Object.hasOwn(before.gallery.posters,id)).sort(),IDS);
 for(const r of records){assert.deepEqual(after.gallery.posters[r.id],r.gallery.poster);for(const f of r.gallery.files)assert.deepEqual(after.gallery.files.filter(x=>x.path===f.path),[f]);}
 const catalog=copy(after.catalog);catalog.packs=catalog.packs.filter(p=>p.id!=='reviewed-static4-20261026');assert.deepEqual(catalog,before.catalog,'Original catalog facets changed');
 const packs=after.catalog.packs.filter(p=>p.id==='reviewed-static4-20261026');assert.equal(packs.length,1);assert.deepEqual([...packs[0].asset_ids].sort(),IDS);
 const turntables=copy(after.turntables);turntables.posters=turntables.posters.filter(p=>!selected.has(p.id));assert.deepEqual(turntables,before.turntables,'Old animated/static cards changed');
 for(const r of records){assert.equal(r.turntable.asset,null);assert.deepEqual(after.turntables.posters.filter(p=>p.id===r.id),r.turntable.poster?[r.turntable.poster]:[]);}
 assert.deepEqual(removeKeys(after.framing,selected),before.framing,'Original wheel framing changed');
 for(const r of records){assert(Object.hasOwn(r.gallery,'wheel_framing'),'Explicit record wheel framing required');if(r.gallery.wheel_framing===null)assert(!Object.hasOwn(after.framing,r.id),'Null framing must remain absent');else {assert(Object.hasOwn(after.framing,r.id),'Missing new wheel framing');assert.deepEqual(after.framing[r.id],r.gallery.wheel_framing,'New wheel framing differs from authenticated record');}}
 assert.deepEqual(removeKeys(after.detail.presentations,selected),before.detail.presentations,'Original264 detail entries changed');assert.equal(Object.keys(before.detail.presentations).length,264);assert.deepEqual(Object.keys(after.detail.presentations).filter(id=>!Object.hasOwn(before.detail.presentations,id)).sort(),IDS);
 for(const key of ['version','kind','renderer_input_sha256','renderer_policy','migration_scope','browser_version','renderer_files','source_wheel_index_sha256'])assert.deepEqual(after.detail[key],before.detail[key],'Historical detail policy '+key);
 exact(after.detail,Object.keys(before.detail),'No unreviewed detail-index fields');
 assert.deepEqual(after.proofs.receipts.slice(0,before.proofs.receipts.length),before.proofs.receipts,'Historical capture receipts changed');assert(after.proofs.receipts.length>before.proofs.receipts.length,'Fresh capture receipt required');
 const seen=new Set();for(const receipt of after.proofs.receipts.slice(before.proofs.receipts.length)){for(const id of Object.keys(receipt.assets)){assert(selected.has(id)&&!seen.has(id),'Unexpected/repeated fresh capture ID');seen.add(id);}assert.equal(receipt.renderer_input_sha256,before.detail.renderer_input_sha256);}assert.deepEqual([...seen].sort(),IDS);
 assert.deepEqual({...after.proofs,receipts:before.proofs.receipts},before.proofs,'Capture proof headers changed');
 return {legacy_models:602,legacy_details:264,new_ids:IDS,legacy_result:'REUSED_EXACT_BASELINE_NOT_FRESH_MATH'};
}
// Only these two registration files are added to the ledger, after exact inverse
// projection. The 19 content-addressed records remain authenticated append closure.
export function assertAppendRegistrationProjection({beforeRegistry,afterRegistry,beforeProduction,afterProduction,append,records,catalog}){
 const release='reviewed-static4-20261026';
 assert.equal(append.release_id,release);assert.deepEqual(records.map(r=>r.id),IDS);
 assert.equal(beforeRegistry.records.length,602);assert.equal(afterRegistry.records.length,621);
 assert.deepEqual(assertRegistryAppend(beforeRegistry,afterRegistry),IDS,'Registry additions differ from authenticated19');
 assert.equal(afterRegistry.batches.length,beforeRegistry.batches.length+1,'Exactly one new batch');
 const batch=afterRegistry.batches.find(b=>b.id===release);assert(batch&&!beforeRegistry.batches.some(b=>b.id===release),'New batch owner already exists');
 const expected=records.map(recordReference);assert.deepEqual(batch.records,expected,'Batch record pins differ');
 assert.deepEqual(append.entries,expected.map((ref,i)=>({id:ref.id,record:{path:ref.path,sha256:ref.sha256,bytes:Buffer.byteLength(encode(records[i]))}})),'Append record pins differ');
 for(const record of records){assert.deepEqual(afterRegistry.records.find(r=>r.id===record.id),record,'Registry record differs from authenticated append');assert.deepEqual(record.catalog,{pack_ids:[release],legacy_pack_ids:[]},'New catalog membership differs');}
 assert.equal(append.content_releases.length,1);const releasePin=append.content_releases[0].descriptor;
 exact(releasePin,['path','sha256','bytes']);assert.equal(releasePin.path,`production/${release}/release.json`);assert.match(releasePin.sha256,/^[a-f0-9]{64}$/);assert(Number.isSafeInteger(releasePin.bytes)&&releasePin.bytes>0);
 assert.deepEqual(batch.evidence,[{path:releasePin.path,sha256:releasePin.sha256}],'Batch evidence must pin exact append production descriptor');
 assert.deepEqual(batch.definitions.worlds,[],'No new world definitions');assert.equal(batch.definitions.packs.length,1);assert.equal(batch.definitions.packs[0].id,release);
 assert.deepEqual(composeRegistry(afterRegistry).catalog,catalog,'Catalog differs from exact registry pack definitions');
 const pack=catalog.packs.filter(p=>p.id===release);assert.deepEqual(pack,[{...batch.definitions.packs[0],asset_ids:IDS}],'Pack definition/membership changed');
 exact(beforeProduction,['schema_version','kind','descriptors','asset_ids']);assert.equal(beforeProduction.schema_version,1);assert.equal(beforeProduction.kind,'production-release-set-v1');assert(Array.isArray(beforeProduction.descriptors)&&Array.isArray(beforeProduction.asset_ids));
 assert(!beforeProduction.descriptors.some(p=>p.path===releasePin.path));assert(!beforeProduction.asset_ids.some(id=>IDS.includes(id)));
 assert.deepEqual(afterProduction,{...beforeProduction,descriptors:[...beforeProduction.descriptors,releasePin],asset_ids:[...beforeProduction.asset_ids,...IDS]},'Original production registry headers, pins, order or IDs changed');
 return [APPEND_BATCH_PATH,APPEND_PRODUCTION_REGISTRY_PATH];
}
function canonicalActor(value){
 exact(value,['id','task_id'],'Exact actor identity required');
 const identities=['id','task_id'].map(key=>{assert(typeof value[key]==='string');const id=value[key].trim().toLowerCase().replace(/^\/root\//,'');assert(/^[a-z0-9][a-z0-9_-]*(?:\/[a-z0-9][a-z0-9_-]*)*$/.test(id),'Invalid actor identity');assert(!/^(?:unknown|pending|none|null|unassigned)(?:$|[-_/])/.test(id),'Unestablished actor identity');return id;});
 assert.equal(identities[0],identities[1],'Conflicting actor identity aliases');return identities[0];
}
export function assertAppendChangeMode({status,before,after}){
 assert(['A','M'].includes(status),'Only added/modified files permitted');assert.equal(after,'100644','Only regular nonexecutable files permitted');
 if(status==='M')assert.equal(before,after,'Historical file mode changed');else assert.equal(before,null,'Added file already exists in baseline');
}
// The two actual byte-pinned receipt files are necessary delivery, not a path
// wildcard and not an Actions-authentication grant. Runtime authority still
// authenticates the original run/artifact and decodes the exact current PNGs.
export function freshAppendProofClosure({before,after,read}){
 assert.deepEqual(after.receipts.slice(0,before.receipts.length),before.receipts,'Historical proof receipts changed');
 const fresh=after.receipts.slice(before.receipts.length),paths=[],seen=new Set(),runs=new Set();assert(fresh.length>0,'Fresh receipt required');
 for(const r of fresh){
  assert(Number.isSafeInteger(r.run_id)&&r.run_id>0&&!runs.has(r.run_id),'Unique positive fresh run required');runs.add(r.run_id);
  assert.equal(r.capture_revision,2);assert.equal(r.scope_kind,'bounded-fresh-subset-v1');assert.equal(r.artifact_prefix,'fresh');
  const prefix=`qa/detail-presentation-evidence/captures/${r.run_id}/`;
  assert.equal(r.capture_index_path,prefix+'original-capture-index.js');assert.equal(r.decoded_proof?.path,prefix+'independent-decoded-checks.json');
  const ids=Object.keys(r.assets||{});assert(ids.length>0);for(const id of ids){assert(IDS.includes(id)&&!seen.has(id),'Unexpected/repeated fresh proof ID');seen.add(id);}
  for(const [path,hash]of [[r.capture_index_path,r.capture_index_sha256],[r.decoded_proof.path,r.decoded_proof.sha256]]){assert.match(hash||'',/^[a-f0-9]{64}$/);const bytes=read(path);assert.equal(sha(bytes),hash,'Fresh proof bytes changed');if(path.endsWith('.js'))moduleData(bytes);else json(bytes);paths.push(path);}
 }
 assert.deepEqual([...seen].sort(),IDS);return paths;
}
// Exactly one independently signed three-case record; no path or review configuration.
export function appendThreeReviewClosure(read){
 const bytes=read(APPEND_THREE_CASE_REVIEW_PATH);assert.equal(sha(bytes),APPEND_THREE_CASE_REVIEW_SHA,'Pinned three-case visual review bytes required');const r=json(bytes);
 assert.equal(r.kind,'independent-explicit19-three-case-visual-disposition-v1');assert.equal(r.reviewer_kind,'INDEPENDENT_AI_REVIEW');assert.equal(r.disposition,'ACCEPTABLE_CURRENT_DISPLAY_CONSISTENCY_NOT_PIXEL_IDENTITY');assert.notEqual(canonicalActor(r.reviewer),'integrate_ready_model_release');
 assert.deepEqual(r.cases.map(c=>c.name),['scientific-quality-alalcomenaeus-1440x900-dpr1','scientific-quality-alalcomenaeus-900x1200-dpr1','scientific-quality-proganochelys-1440x900-dpr1']);for(const k of ['publication_authorized','reviewer_authority','productionAccepted'])assert.equal(r[k],false);
 return [APPEND_THREE_CASE_REVIEW_PATH];
}
export function assertVisualLedger({descriptor,review,changes,read,baseExists,closure,registration}){
 exact(descriptor,['version','kind','baseline','append','new_ids','producer','files','review_path','publication_authorized','reviewer_authority'],'Visual descriptor');assert.equal(descriptor.version,1);assert.equal(descriptor.kind,'exact602-264-plus-explicit19-visual-continuation-v1');assert.equal(descriptor.baseline,APPEND_VISUAL_BASE);assert.deepEqual(descriptor.new_ids,IDS);assert.equal(descriptor.review_path,APPEND_VISUAL_REVIEW_PATH);
 assert.equal(descriptor.publication_authorized,false);assert.equal(descriptor.reviewer_authority,false);
 assert.equal(review.kind,'independent-exact602-264-plus19-visual-continuation-review-v1');assert.equal(review.status,'PASS');assert.equal(review.descriptor.sha256,sha(Buffer.from(JSON.stringify(descriptor,null,2)+'\n')));assert.equal(review.descriptor.path,APPEND_VISUAL_PATH);assert.equal(review.baseline,APPEND_VISUAL_BASE);assert.deepEqual(review.new_ids,IDS);assert.deepEqual(review.blocking_findings,[]);
 assert.notEqual(canonicalActor(review.reviewer),canonicalActor(descriptor.producer),'Preparer/reviewer cross-alias');assert.equal(review.publication_authorized,false);assert.equal(review.reviewer_authority,false);
 const checks=['exact_changed_file_inventory','unchanged_runtime_dependency_closure','original602_inverse_projection','original264_and_receipts_unchanged','baseline_snapshot_complete_and_exact','historical_failed_artifact_authentication','fresh19_profile_and_all_negative_controls','mandatory_dist_and_public_execution'];exact(review.checks,checks);for(const k of checks)assert.equal(review.checks[k],'PASS');
 const files=descriptor.files;assert.deepEqual(files.map(f=>f.path),[...new Set(files.map(f=>f.path))].sort());
 assert.deepEqual(changes.filter(p=>![APPEND_VISUAL_PATH,APPEND_VISUAL_REVIEW_PATH].includes(p)).sort(),files.map(f=>f.path),'Unreviewed Git delta');
 const registrationPaths=registration?assertAppendRegistrationProjection(registration):[];
 if(registration){assert.deepEqual(json(read(APPEND_BATCH_PATH)),registration.afterRegistry.batches.find(b=>b.id==='reviewed-static4-20261026'),'Batch bytes differ from validated registry');assert.deepEqual(json(read(APPEND_PRODUCTION_REGISTRY_PATH)),registration.afterProduction,'Production registry bytes differ from validated registry');}
 const allowed=new Set([...APPEND_CONTRACT_PATHS,...DATA_PATHS,...closure,...registrationPaths]);
 for(const f of files){exact(f,['path','sha256','bytes','role']);pinned(read(f.path),f);if([APPEND_BATCH_PATH,APPEND_PRODUCTION_REGISTRY_PATH].includes(f.path))assert(registrationPaths.includes(f.path),'Unvalidated registration path');assert(allowed.has(f.path),'Unclassified changed file '+f.path);if(registrationPaths.includes(f.path)){assert.equal(baseExists(f.path),f.path===APPEND_PRODUCTION_REGISTRY_PATH,'Registration file baseline presence differs');assert.equal(f.role,'validated-registration-append');}else if(DATA_PATHS.includes(f.path))assert.equal(f.role,'validated-data-append');else if(APPEND_CONTRACT_PATHS.includes(f.path))assert.equal(f.role,'independently-reviewed-offline-contract');else {assert(!baseExists(f.path),'Original immutable delivery overwritten');assert.equal(f.role,'exact-reviewed-new-delivery');}}
 return {descriptor_sha256:sha(Buffer.from(JSON.stringify(descriptor,null,2)+'\n')),review_sha256:sha(Buffer.from(JSON.stringify(review,null,2)+'\n')),changed_files:files.length};
}
export async function assertAppendVisualRuntime({root,api,currentSha,legacy}){
 assert(!['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_ALTERNATE_OBJECT_DIRECTORIES'].some(k=>process.env[k]),'Custom Git context forbidden');assert.equal(git(root,'rev-parse','--show-toplevel').toString().trim(),resolve(root));assert(git(root,'ls-files','-v','-z').toString().split('\0').filter(Boolean).every(row=>row.startsWith('H ')),'Sparse/assume-unchanged index forbidden');
 assert.match(currentSha||'',/^[a-f0-9]{40}$/);assert.equal(git(root,'rev-parse','HEAD').toString().trim(),currentSha);assert.equal(git(root,'status','--porcelain','--untracked-files=no').toString().trim(),'');
 const read=successorReader(root),manifest=json(read('assets/manifest.json')),context=successorContext({manifest,read});assert(context?.append,'Authenticated append context required');assert.deepEqual(context.append.records.map(r=>r.id).sort(),IDS);
 const before={},after={};for(const [key,path]of Object.entries({manifest:DATA_PATHS[0],catalog:DATA_PATHS[1],turntables:DATA_PATHS[2],gallery:DATA_PATHS[3],framing:DATA_PATHS[4],detail:DATA_PATHS[5],proofs:DATA_PATHS[6]})){const parse=path.endsWith('.js')?moduleData:json;before[key]=parse(raw(root,path));after[key]=parse(read(path));}
 const projection=assertLegacyDataProjection({before,after,records:context.append.records});selectedDetailAppend({manifest,index:after.detail,read});
 const descriptor=json(read(APPEND_VISUAL_PATH)),review=json(read(APPEND_VISUAL_REVIEW_PATH));assert.deepEqual(descriptor.append,context.appendPin);
 const changed=git(root,'diff','--name-status','--no-renames',APPEND_VISUAL_BASE,currentSha).toString().trim().split('\n').filter(Boolean).map(row=>{const [status,path,...extra]=row.split('\t');assert(!extra.length&&['A','M'].includes(status),'Only regular added/modified files permitted');const item=git(root,'ls-tree',currentSha,'--',path).toString(),previous=git(root,'ls-tree',APPEND_VISUAL_BASE,'--',path).toString();assert(item.startsWith('100644 blob '),'No mode/link/gitlink changes');assertAppendChangeMode({status,before:previous?previous.split(' ')[0]:null,after:item.split(' ')[0]});return path;});
 const closure=[...context.append.closure,...context.append.records.flatMap(r=>[r.asset.glb,r.asset.blend,r.asset.preview,r.asset.credits,...r.gallery.files.map(f=>'site/public/'+f.path)]),...Object.values(after.detail.presentations).filter(e=>IDS.includes(e.id)).map(e=>'site/public/'+e.detail),...freshAppendProofClosure({before:before.proofs,after:after.proofs,read}),...appendThreeReviewClosure(read)];
 const registration={beforeRegistry:readRegistryAtCommit(root,APPEND_VISUAL_BASE),afterRegistry:readRegistry(root),beforeProduction:json(raw(root,APPEND_PRODUCTION_REGISTRY_PATH)),afterProduction:json(read(APPEND_PRODUCTION_REGISTRY_PATH)),append:context.append.descriptor,records:context.append.records,catalog:after.catalog};
 const ledger=assertVisualLedger({descriptor,review,changes:changed,read,registration,baseExists:path=>{try{raw(root,path);return true;}catch{return false;}},closure});
 for(const [path,hash]of Object.entries(legacy.ACCEPTANCE_CONTROL_HASHES))assert.equal(sha(raw(root,path)),hash,'Baseline controls must equal reviewed PR75');
 const p=legacy.VISUAL_REVIEW,source=await api.json('git/commits/'+p.source);assert.equal(source.sha,p.source);assert.deepEqual(source.parents.map(x=>x.sha),[p.base,p.head]);
 const localTree=async id=>({sha:id,truncated:false,tree:git(root,'ls-tree','-z',id).toString().split('\0').filter(Boolean).map(row=>{const at=row.indexOf('\t'),[mode,type,sha]=row.slice(0,at).split(' ');return {mode,type,sha,path:row.slice(at+1)};})});
 await legacy.compareRuntimeTrees({oldRoot:source.tree.sha,newRoot:git(root,'rev-parse',APPEND_VISUAL_BASE+'^{tree}').toString().trim(),oldTree:id=>api.json('git/trees/'+id),newTree:localTree});
 assert.equal(sha(await api.source('.github/workflows/pages.yml',p.source)),p.workflow_sha256);assert.equal(sha(await api.source('site/detail-presentation-browser-test.mjs',p.source)),p.browser_sha256);assert.equal(sha(raw(root,p.review_path)),p.review_sha256);
 return {current_source:currentSha,baseline_source:APPEND_VISUAL_BASE,...projection,...ledger,runtime_identity:'UNCHANGED_OLD_RUNTIME_AND_EXACT_REVIEWED_19_DATA_APPEND'};
}
// The historical report sealed delivered metadata, not raw source JSON. These
// immutable seals belong to the same already-authenticated failed PR73 report.
export const LEGACY_BUILT_INPUT_SEALS=Object.freeze({
 report_sha256:'9fdd81660e6c95108eb62747bdb5dc6497346614364c3eea7d018bc0fa8f6d9a',
 manifest_sha256:'443a4b788511cec6b642691faaa6da78244d4f73948984e1f08e14a90ea1d589',
 resources_sha256:'c01b9e47d478992bdb35497567ae00e046b994b0a1f9e715aa177e087326b8b6'
});
export function assertLegacyBuiltInputSeals({manifestBytes,resourcesBytes,reportSha256}){
 assert.equal(reportSha256,LEGACY_BUILT_INPUT_SEALS.report_sha256,'Historical report cannot be replaced');
 assert.equal(sha(manifestBytes),LEGACY_BUILT_INPUT_SEALS.manifest_sha256,'Historical delivered manifest bytes differ');
 assert.equal(sha(resourcesBytes),LEGACY_BUILT_INPUT_SEALS.resources_sha256,'Historical delivered resources bytes differ');
}
export function projectLegacyBuiltInputs({baselineManifest,sourceManifest,baselineResources,sourceResources,builtManifest,builtResources}){
 const selected=new Set(IDS),oldIds=baselineManifest.assets.map(a=>a.id);
 assert.equal(oldIds.length,602);assert.equal(new Set(oldIds).size,602);assert(oldIds.every(id=>!selected.has(id)));
 assert.deepEqual(sourceManifest.assets.map(a=>a.id),[...oldIds,...IDS],'Exact source621 order required');
 const sourceInverse=copy(sourceManifest);sourceInverse.assets=sourceInverse.assets.slice(0,602);
 assert(sourceInverse.publication?.same_id_successor_append,'Authenticated append pointer required');delete sourceInverse.publication.same_id_successor_append;
 assert.deepEqual(sourceInverse,baselineManifest,'Original source602 changed');
 assert.deepEqual(builtManifest.assets.map(a=>a.id),[...oldIds,...IDS],'Delivered metadata must contain exact621, not raw602');
 assert.deepEqual({...builtManifest,assets:sourceManifest.assets},sourceManifest,'Delivered headers changed');
 for(let i=0;i<sourceManifest.assets.length;i++)for(const key of ['id','glb','blend','preview','sha256'])assert.deepEqual(builtManifest.assets[i][key],sourceManifest.assets[i][key],'Delivered source binding changed: '+key);
 const newPaths=new Set(IDS.flatMap(id=>['gallery/posters/'+id+'.png','gallery/posters/'+id+'-wheel.png']));
 assert.deepEqual(Object.keys(sourceResources.posters).filter(id=>!Object.hasOwn(baselineResources.posters,id)).sort(),IDS);
 for(const id of IDS){assert.equal(sourceResources.posters[id].detail,'gallery/posters/'+id+'.png');assert.equal(sourceResources.posters[id].wheel,'gallery/posters/'+id+'-wheel.png');}
 for(const path of newPaths)assert.equal(sourceResources.files.filter(f=>f.path===path).length,1,'Exact added poster file required');
 const resourceInverse=copy(sourceResources);resourceInverse.posters=removeKeys(resourceInverse.posters,selected);resourceInverse.files=resourceInverse.files.filter(f=>!newPaths.has(f.path));assert.deepEqual(resourceInverse,baselineResources,'Original source resources changed');
 assert.deepEqual(builtResources,{...sourceResources,production_projection:true},'Delivered resources differ from authenticated source projection');
 const manifest=copy(builtManifest);manifest.assets=manifest.assets.slice(0,602);delete manifest.publication.same_id_successor_append;
 const resources=copy(builtResources);resources.posters=removeKeys(resources.posters,selected);resources.files=resources.files.filter(f=>!newPaths.has(f.path));
 return {manifestBytes:Buffer.from(JSON.stringify(manifest,null,2)+'\n'),resourcesBytes:Buffer.from(JSON.stringify(resources,null,2)+'\n')};
}
// Executable snapshot sources are exact Git blobs, never current code. Only the
// two delivered metadata inputs use the exact inverse above plus immutable byte
// seals. The snapshot executes the old offline verifier, never Chromium.
export async function createBaselineVerifierSnapshot(root,target,reportSha256){
 const projected=projectLegacyBuiltInputs({baselineManifest:json(raw(root,'assets/manifest.json')),sourceManifest:json(await readFile(join(root,'assets/manifest.json'))),baselineResources:json(raw(root,'site/public/gallery/resources.json')),sourceResources:json(await readFile(join(root,'site/public/gallery/resources.json'))),builtManifest:json(await readFile(join(root,'dist/assets/manifest.json'))),builtResources:json(await readFile(join(root,'dist/gallery/resources.json')))});
 assertLegacyBuiltInputSeals({...projected,reportSha256});
 const paths=git(root,'ls-tree','-rz','--name-only',APPEND_VISUAL_BASE).toString().split('\0').filter(p=>p&&((p.startsWith('site/')&&!p.startsWith('site/public/')&&/\.(mjs|js|json)$/.test(p))||(p.startsWith('qa/detail-presentation-')&&/\.(js|json)$/.test(p))||p==='package.json'));
 for(const path of paths){await mkdir(dirname(join(target,path)),{recursive:true});await writeFile(join(target,path),raw(root,path),{flag:'wx'});}
 for(const [bytes,path]of [[projected.manifestBytes,'baseline-gallery/assets/manifest.json'],[projected.resourcesBytes,'baseline-gallery/gallery/resources.json']]){await mkdir(dirname(join(target,path)),{recursive:true});await writeFile(join(target,path),bytes,{flag:'wx'});}
 await symlink(resolve(root,'node_modules'),join(target,'node_modules'));return paths;
}
export async function authenticateAppendVisualEvidence({root,api,currentSha,out,legacy}){
 const binding=await assertAppendVisualRuntime({root,api,currentSha,legacy}),p=legacy.VISUAL_REVIEW;legacy.assertRun(await api.json(`actions/runs/${p.run}`));legacy.assertRun(await api.json(`actions/runs/${p.run}/attempts/1`));const suite=await api.json(`check-suites/${p.suite}`);assert.equal(suite.id,p.suite);assert.equal(suite.head_sha,p.head);assert.equal(suite.app?.id,15368);assert.equal(suite.app?.slug,'github-actions');assert.equal(suite.status,'completed');assert.equal(suite.conclusion,'failure');const job=await api.json(`actions/jobs/${p.job}`);legacy.assertJob(job);legacy.assertArtifact(await api.json(`actions/artifacts/${p.artifact}`),job);
 const dir=await mkdtemp(join(tmpdir(),'append-visual-'));try{const oldOut=join(out,'legacy264'),freshOut=join(out,'fresh19');await mkdir(oldOut,{recursive:true});const zip=await api.archive(p.artifact,{revision:2});assert.equal(zip.length,p.zip_bytes);assert.equal(sha(zip),p.zip_sha256);const archive=join(dir,'original.zip');await writeFile(archive,zip);execFileSync('python3',['-c',legacy.extractPython,archive,oldOut],{maxBuffer:1024**2});assert.equal(sha(await readFile(join(oldOut,'report.json'))),p.report_sha256);
  const snapshot=join(dir,'baseline');await mkdir(snapshot);await createBaselineVerifierSnapshot(root,snapshot,p.report_sha256);
  execFileSync(process.execPath,['site/detail-presentation-browser-test.mjs','--verify-visual-disposition-seals'],{cwd:snapshot,env:{...immutableGitEnv(),GALLERY_DIR:join(snapshot,'baseline-gallery'),DETAIL_BROWSER_PROFILE:'full264-v2',DETAIL_BROWSER_TARGET:'dist',DETAIL_EXPECTED_SOURCE_COMMIT:p.source,QA_OUTPUT_DIR:oldOut},stdio:'inherit'});
  legacy.assertRun(await api.json(`actions/runs/${p.run}`));
  for(const args of [[],['--verify-evidence']])execFileSync(process.execPath,['site/detail-presentation-browser-test.mjs',...args],{cwd:root,env:{...immutableGitEnv(),GALLERY_DIR:resolve(root,'dist'),DETAIL_BROWSER_PROFILE:'append19-v2',DETAIL_BROWSER_TARGET:'dist',GITHUB_SHA:currentSha,QA_OUTPUT_DIR:freshOut},stdio:'inherit'});
  const bytes=await readFile(join(freshOut,'report.json')),fresh=json(bytes);assert.equal(fresh.status,'pass');assert.equal(fresh.profile,'append19-v2');assert.equal(fresh.source_commit,currentSha);
  const result={status:'PASS_BOUNDED_APPEND_WITH_AUTHENTICATED_LEGACY_REUSE',...binding,legacy264:{original_run_status:'FAIL',original_report_status:'fail',artifact_sha256:p.zip_sha256,report_sha256:p.report_sha256,review_sha256:p.review_sha256,math:'CURRENT_MATH_NOT_REEXECUTED'},new19:{status:'PASS',report_sha256:sha(bytes),profile:'append19-v2',scope:'ALL_19_FRESH_PLUS_UNCHANGED_CONTROL'},public_acceptance:'NOT_RUN'};await writeFile(join(out,'acceptance.json'),JSON.stringify(result,null,2)+'\n');return result;
 }finally{await rm(dir,{recursive:true,force:true});}
}

export async function executeFreshAppendPublic({root,currentSha,out}){
 const freshOut=join(out,'fresh19');for(const args of [[],['--verify-evidence']])execFileSync(process.execPath,['site/detail-presentation-browser-test.mjs',...args],{cwd:root,env:{...immutableGitEnv(),GALLERY_DIR:resolve(root,'dist'),DETAIL_BROWSER_PROFILE:'append19-v2',DETAIL_BROWSER_TARGET:'public',GITHUB_SHA:currentSha,DEPLOYED_SHA:currentSha,QA_OUTPUT_DIR:freshOut},stdio:'inherit'});
 const bytes=await readFile(join(freshOut,'report.json')),fresh=json(bytes);assert.equal(fresh.status,'pass');assert.equal(fresh.profile,'append19-v2');assert.equal(fresh.source_commit,currentSha);assert.equal(fresh.target,'public');return {status:'PASS',report_sha256:sha(bytes),profile:'append19-v2',scope:'ALL_19_FRESH_PLUS_UNCHANGED_CONTROL'};
}

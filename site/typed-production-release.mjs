/** Opt-in typed route. Legacy production-release-v1 remains on its existing implementation. */
import assert from 'node:assert/strict';
import {readFile,realpath} from 'node:fs/promises';
import {resolve,sep,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {sha256,SOURCE_ROLES,assertProductionMaterial,validateInventoryCompatibilityReceipt,verifyInventoryCompatibilityReceipt,validateNativeInventoryMeasurements,bindNativeInventoryGlb,verifyExactLocalSourceAvailability,preserveUnverifiedRuntimeStatus,validateSupplementaryReviewBinding} from './inventory-type-acceptance.mjs';
import {validateModelTaskV2Receipt,verifyModelTaskV2Review,validateV2Measurements,preserveV2Runtime} from './model-task-v2-acceptance.mjs';
import {isPreservedImplementationBridge} from './preserved-implementation-bridges.mjs';
const digest=x=>typeof x==='string'&&/^[a-f0-9]{64}$/.test(x);
const text=x=>typeof x==='string'&&Boolean(x.trim());
async function read(root,path){assert(text(path)&&!/[\\\u0000-\u001f?#%]/.test(path)&&!path.startsWith('/')&&path.split('/').every(p=>p&&p!=='.'&&p!=='..'),'Unsafe typed production path');const full=resolve(root,path);assert(full.startsWith(resolve(root)+sep));assert.equal(await realpath(full),full,'Typed source symlink rejected');return readFile(full);}
async function pinned(root,pin){assert(pin&&digest(pin.sha256)&&Number.isSafeInteger(pin.bytes)&&pin.bytes>0,'Exact typed pin required');const b=await read(root,pin.path);assert.equal(b.length,pin.bytes,'Typed source bytes changed');assert.equal(sha256(b),pin.sha256,'Typed source hash changed');return b;}
const bilingual=x=>{for(const l of ['en','zh'])assert(text(x?.[l]),'Typed bilingual text required');};
function identity(x){for(const key of ['id','task_id'])assert(text(x?.[key]),'Typed maker/preparer identity missing');}

export async function inspectTypedProductionRelease(root,descriptorPath,raw,registryPath){
 return inspectTypedContent(root,descriptorPath,raw,registryPath,false);
}
// This route changes only the descriptor binding, not the asset acceptance rules.
export async function inspectProductionContent(root,descriptorPath,raw){
 return inspectTypedContent(root,descriptorPath,raw,undefined,true);
}
async function inspectTypedContent(root,descriptorPath,raw,registryPath,contentOnly){
 raw=raw||await read(root,descriptorPath);const descriptor=JSON.parse(raw);
 const compatibilityPins=contentOnly?null:await resolveImplementationCompatibility(root,descriptorPath,descriptor,raw,registryPath);
 assertProductionMaterial(descriptor);
 assert.equal(descriptor.kind,contentOnly?'content-production-release-v1':'typed-production-release-v1');assert.equal(descriptor.schema_version,1);assert.equal(descriptor.publication_authorized,false);assert(/^[a-f0-9]{40}$/.test(descriptor.baseline_commit));identity(descriptor.producer);
 if(!contentOnly){assert(Array.isArray(descriptor.implementation)&&new Set(descriptor.implementation.map(p=>p.path)).size===descriptor.implementation.length);for(const path of ['site/production-release.mjs','site/typed-production-release.mjs','site/inventory-type-acceptance.mjs','site/asset-delivery.mjs','scripts/qa_glb.py','scripts/asset_common.py'])assert(descriptor.implementation.some(p=>p.path===path),'Missing typed implementation dependency '+path);for(const pin of compatibilityPins||descriptor.implementation)await pinned(root,pin);}
 else assert(!Object.hasOwn(descriptor,'implementation'),'Content acceptance must not bind implementation');
 await pinned(root,descriptor.scope_document);
 assert(Array.isArray(descriptor.assets)&&descriptor.assets.length);const ids=new Set(),assets=[],records=[],audits=[];
 for(const item of descriptor.assets){
  assert(/^[a-z0-9][a-z0-9-]*$/.test(item.id)&&!ids.has(item.id));ids.add(item.id);
  const asset=JSON.parse(await pinned(root,item.metadata)),record=JSON.parse(await pinned(root,item.evidence));
  assertProductionMaterial(asset);assertProductionMaterial(record);
  assert.equal(asset.id,item.id);assert.equal(record.asset_id,item.id);assert.equal(record.kind,'compact-typed-production-release-v1');assert.equal(record.schema_version,1);assert.equal(record.productionAccepted,true);identity(record.maker);
  assert.equal(asset.production_release,descriptorPath);assert.equal(asset.revision,record.revision);assert.deepEqual(record.blocking_findings,[]);
  const v2=asset.production_acceptance_adapter==='model-task-v2';
  assert(v2||asset.production_acceptance_adapter==='inventory-types-v1','Explicit typed metadata route required');
  if(v2&&!contentOnly)assert(descriptor.implementation.some(p=>p.path==='site/model-task-v2-acceptance.mjs'),'Missing v2 implementation dependency');
  assert.deepEqual(Object.keys(record.roles).sort(),[...SOURCE_ROLES].sort());
  const roleBytes={};for(const role of SOURCE_ROLES){roleBytes[role]=await pinned(root,record.roles[role]);if(!record.source_role_derivations?.[role])assert.equal(record.subject[role],record.roles[role].sha256);}
  assert(Array.isArray(record.build_closure)&&record.build_closure.length>=2);for(const pin of record.build_closure)await pinned(root,pin);
  const brief=JSON.parse(await pinned(root,record.roles.brief)),references=JSON.parse(await pinned(root,record.roles.references)),receipt=JSON.parse(await pinned(root,record.typed_compatibility));
  assert.equal(receipt.kind,v2?'compact-model-task-v2-compatibility-v1':'compact-inventory-compatibility-v1','Production requires compact public proof, not raw private QA');
  if(v2)assert.equal((record.independence_evidence||[]).length,0,'V2 must use its exact independent projection review');
  for(const pin of record.independence_evidence||[])validateSupplementaryReviewBinding(JSON.parse(await pinned(root,pin)),record,receipt);
  const budget=(v2?validateModelTaskV2Receipt:validateInventoryCompatibilityReceipt)(receipt,record,asset,brief,references);
  if(!v2)assert.equal(asset.reconstruction_type,typeof brief.subject==='object'?brief.subject.reconstruction_type:'whole-organism','Original reconstruction scope relabeled');
  assert.deepEqual(record.frozen_budget,budget,'Frozen budget changed');
  for(const [name,role]of [['glb','finalGLB'],['blend','finalBlend']]){assert.equal(asset[name],record.roles[role].path);assert.equal(asset.sha256[name],record.roles[role].sha256);}
  assert.equal(record.legacy_record?.mutated,false);assert.equal(record.legacy_record.approval_rewritten,false);
  const sourceAvailability=verifyExactLocalSourceAvailability(record,receipt,roleBytes);
  bilingual(asset.name);bilingual(asset.description);bilingual(record.scientific_limits);assert.deepEqual(asset.description,record.scientific_limits);assert.equal(asset.license,'CC-BY-4.0');assert.equal(asset.units,'meters');assert(Array.isArray(asset.reference_credits)&&asset.reference_credits.length);
  const originalCredits=v2?(references.sources??references.references).map(s=>({title:s.title??s.id??s.url,url:s.url})):references.sources.map(s=>({title:s.title,url:s.url}));
  assert(originalCredits.every(s=>text(s.title)&&text(s.url)),'Missing original reference credit label/URL');
  assert.deepEqual(asset.reference_credits.map(s=>({title:s.title,url:s.url})),originalCredits,'Original reference credits changed');
  await pinned(root,record.preview);assert.equal(asset.preview,record.preview.path);assert.equal(asset.sha256.preview,record.preview.sha256);assert.equal(record.preview_provenance.source_glb_sha256,asset.sha256.glb);
  // A newly rendered preview must not be labeled as an old independently accepted image.
  assert.equal(record.preview_provenance.route,'fresh_final_glb_poster');assert.equal(record.preview_provenance.independently_reviewed_original_preview,false);assert.equal(record.preview.sha256,record.final_posters.detail.sha256);
  const native=bindNativeInventoryGlb(await pinned(root,record.roles.finalGLB),JSON.parse(execFileSync('python3',[resolve(dirname(fileURLToPath(import.meta.url)),'../scripts/qa_glb.py'),resolve(root,asset.glb),'--max-triangles',String(budget.max_triangles),'--max-materials',String(budget.max_materials),'--max-primitives',String(budget.max_primitives)],{encoding:'utf8',maxBuffer:2*1024*1024,env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}})));
  (v2?validateV2Measurements:validateNativeInventoryMeasurements)(native,asset,record,receipt);
  record.postReleaseVerified=v2?preserveV2Runtime(record,receipt):preserveUnverifiedRuntimeStatus(record.postReleaseVerified);
  if(asset.postReleaseVerified!==undefined)asset.postReleaseVerified=preserveUnverifiedRuntimeStatus(typeof asset.postReleaseVerified==='string'?{status:asset.postReleaseVerified}:asset.postReleaseVerified);
  // Preserve a reported post-release FAIL rather than rewriting it; remediation is a separate layer.
  assets.push(asset);records.push(record);audits.push({id:asset.id,status:'PASS',native,compatibility:receipt,sourceAvailability});
 }
 const runtimeStates=[...new Set(records.map(r=>r.postReleaseVerified.status))];
 return {descriptor,descriptor_sha256:sha256(raw),assets,records,audits,productionAccepted:true,releaseChecks:'PENDING_INDEPENDENT_PROJECTION_REVIEW',postReleaseVerified:runtimeStates.includes('FAIL')?'FAIL':runtimeStates.length===1?runtimeStates[0]:'MIXED',publication_authorized:false};
}

export async function verifyTypedProjectionReviews(root,result,projectionReview){
 assertProductionMaterial(projectionReview);
 assert.equal(result.descriptor.kind,'typed-production-release-v1');
 assert(Array.isArray(projectionReview.inventory_compatibility)&&projectionReview.inventory_compatibility.length===result.assets.length,'Missing independent typed reviews');
 for(let i=0;i<result.assets.length;i++){
  const asset=result.assets[i],record=result.records[i],review=projectionReview.inventory_compatibility.find(r=>r.asset_id===asset.id);
  assert(review,'Missing exact typed review');assert.deepEqual(review.reviewer,projectionReview.reviewer,'Typed/overall independent reviewer mismatch');
  const receipt=JSON.parse(await pinned(root,record.typed_compatibility)),brief=JSON.parse(await pinned(root,record.roles.brief)),refs=JSON.parse(await pinned(root,record.roles.references));
  (asset.production_acceptance_adapter==='model-task-v2'?verifyModelTaskV2Review:verifyInventoryCompatibilityReceipt)(receipt,record,asset,brief,refs,review);
 }
}

const jsonHash=value=>sha256(Buffer.from(JSON.stringify(value)));
const exactKeys=(value,keys,label)=>assert.deepEqual(Object.keys(value||{}).sort(),keys.slice().sort(),'Unknown/missing '+label+' fields');
const exactPin=pin=>exactKeys(pin,['path','bytes','sha256'],'pin');
export const COMPATIBILITY_CURRENT_PATHS=Object.freeze(['site/ci-release-fast-scope.mjs','site/production-release.mjs','site/typed-production-release.mjs','site/inventory-type-acceptance.mjs','site/model-task-v2-acceptance.mjs','site/asset-delivery.mjs','scripts/qa_glb.py','scripts/asset_common.py','site/production-publication.mjs','site/ci-production-release-check.mjs','site/ci-historical-publication.mjs','site/ci-poster-approval-test.mjs','site/turntable-delivery-test.mjs','site/model-registry.mjs','site/model-registry-sync.mjs','site/model-registry-cli.mjs','site/ci-production-baseline.mjs','site/ci-proof-fetch.mjs','site/ci-proof-budget.mjs','site/ci-git.mjs']);
export async function loadProductionRegistry(root,path){
 const registry=JSON.parse(await read(root,path));exactKeys(registry,['schema_version','kind','descriptors','asset_ids'],'production registry');assert.equal(registry.schema_version,1);assert.equal(registry.kind,'production-release-set-v1');
 assert(Array.isArray(registry.descriptors)&&registry.descriptors.length>0);assert(Array.isArray(registry.asset_ids)&&registry.asset_ids.length>0&&new Set(registry.asset_ids).size===registry.asset_ids.length);assert(registry.asset_ids.every(id=>/^[a-z0-9][a-z0-9-]*$/.test(id)));
 const paths=new Set();for(const entry of registry.descriptors){exactKeys(entry,entry.compatibility?['path','bytes','sha256','compatibility']:['path','bytes','sha256'],'registered descriptor');assert(!paths.has(entry.path),'Duplicate registered descriptor');paths.add(entry.path);await pinned(root,{path:entry.path,bytes:entry.bytes,sha256:entry.sha256});if(entry.compatibility){exactPin(entry.compatibility);await pinned(root,entry.compatibility);}}
 return registry;
}
/** No override object: only exact, registered, independently reviewed version bridges. */
export async function resolveImplementationCompatibility(root,descriptorPath,descriptor,raw,registryPath){
 let current;try{current=JSON.parse(await read(root,'assets/manifest.json'));}catch(error){if(error.code!=='ENOENT')throw error;}
 assert(!(current?.publication?.production_registry&&current?.publication?.production_descriptor),'Ambiguous production routes');
 registryPath=registryPath??current?.publication?.production_registry;
 if(!registryPath)return null;
 if(current?.publication?.production_registry)assert.equal(registryPath,current.publication.production_registry,'Different production registry contexts');
 const registry=await loadProductionRegistry(root,registryPath),entry=registry.descriptors.find(p=>p.path===descriptorPath);assert(entry,'Descriptor is not in the explicit production registry');assert.equal(entry.sha256,sha256(raw));assert.equal(entry.bytes,raw.length);
 if(!entry.compatibility)return null;
 assert(['production-release-v1','typed-production-release-v1'].includes(descriptor.kind),'Implementation bridge requires an existing supported production schema');
 const bridgeRaw=await pinned(root,entry.compatibility),bridge=JSON.parse(bridgeRaw);assertProductionMaterial(bridge);
 exactKeys(bridge,['schema_version','kind','producer','original_descriptor','original_review','original_implementation','current_implementation','subjects','previous_manifest','preserved_records','review_path','publication_authorized'],'implementation bridge');
 assert.equal(bridge.schema_version,1);assert.equal(bridge.kind,'exact-implementation-compatibility-v1');assert.equal(bridge.publication_authorized,false);identity(bridge.producer);
 exactPin(bridge.original_descriptor);assert.deepEqual(bridge.original_descriptor,{path:descriptorPath,bytes:raw.length,sha256:sha256(raw)});await pinned(root,bridge.original_descriptor);
 exactPin(bridge.original_review);assert.equal(bridge.original_review.path,descriptor.review_path);await pinned(root,bridge.original_review);
 assert(Array.isArray(bridge.original_implementation));assert.deepEqual(bridge.original_implementation.map(x=>x.original),descriptor.implementation,'Original implementation mapping changed');
 for(const row of bridge.original_implementation){exactKeys(row,['original','preserved'],'implementation mapping');exactPin(row.original);exactPin(row.preserved);assert.deepEqual(row.preserved,{path:`production/implementation-history/${row.original.sha256}/${row.original.path}`,bytes:row.original.bytes,sha256:row.original.sha256},'Arbitrary implementation remapping refused');await pinned(root,row.preserved);}
 const bridgeReviewRaw=await read(root,bridge.review_path);
 const historical=isPreservedImplementationBridge(entry.compatibility.path,bridgeRaw,bridge.review_path,bridgeReviewRaw);
 assert(historical,'Unknown or modified implementation bridge: use content-bound acceptance, not a new bridge');
 for(const pin of bridge.current_implementation)exactPin(pin);
 const subjects=[];for(const item of descriptor.assets){const record=JSON.parse(await pinned(root,item.evidence));await pinned(root,item.metadata);subjects.push({...item,subject:record.subject});}
 assert.deepEqual(bridge.subjects,subjects,'Compatibility bridge subject/metadata/evidence changed');
 exactPin(bridge.previous_manifest);const previous=JSON.parse(await pinned(root,bridge.previous_manifest));assert(Array.isArray(previous.assets));
 assert(Array.isArray(bridge.preserved_records));assert.deepEqual(bridge.preserved_records.map(p=>p.id).sort(),previous.assets.map(a=>a.id).sort(),'Historical registry coverage incomplete/duplicate');
 for(const pin of bridge.preserved_records){exactKeys(pin,['id','path','bytes','sha256'],'preserved registry record');assert.equal(pin.path,`registry/models/${pin.id}/revisions/${pin.sha256}/record.json`,'Historical record path changed');const record=JSON.parse(await pinned(root,pin));assert.equal(record.id,pin.id);assert.deepEqual(record.asset,previous.assets.find(a=>a.id===pin.id),'Historical registry metadata changed');if(current)assert.deepEqual(current.assets.find(a=>a.id===pin.id),record.asset,'Published historical metadata/backlink changed or missing');}
 const review=JSON.parse(bridgeReviewRaw);assertProductionMaterial(review);
 exactKeys(review,['schema_version','kind','status','reviewer','bridge_sha256','original_descriptor_sha256','original_implementation_sha256','current_implementation_sha256','subjects_sha256','previous_manifest_sha256','preserved_records_sha256','checks','blocking_findings','publication_authorized'],'compatibility review');
 exactKeys(review.reviewer,['id','task_id'],'compatibility reviewer');
 exactKeys(review.checks,['original_descriptor_and_review_exact','original_implementation_preserved','current_implementation_pinned','original_subjects_and_metadata_unchanged','immutable_registry_records_unchanged','legacy_semantics_and_consumers','no_science_or_media_reacceptance'],'compatibility review checks');assert.equal(review.schema_version,1);assert.equal(review.kind,'independent-implementation-compatibility-review-v1');assert.equal(review.status,'PASS','Fresh implementation compatibility review required');identity(review.reviewer);
 for(const key of ['id','task_id'])assert.notEqual(review.reviewer[key].trim().toLowerCase(),bridge.producer[key].trim().toLowerCase(),'Compatibility producer cannot self-review');
 assert.equal(review.bridge_sha256,sha256(bridgeRaw),'Stale compatibility review');assert.equal(review.original_descriptor_sha256,sha256(raw));assert.equal(review.original_implementation_sha256,jsonHash(bridge.original_implementation));assert.equal(review.current_implementation_sha256,jsonHash(bridge.current_implementation));assert.equal(review.subjects_sha256,jsonHash(subjects));assert.equal(review.previous_manifest_sha256,bridge.previous_manifest.sha256);assert.equal(review.preserved_records_sha256,jsonHash(bridge.preserved_records));
 for(const check of ['original_descriptor_and_review_exact','original_implementation_preserved','current_implementation_pinned','original_subjects_and_metadata_unchanged','immutable_registry_records_unchanged','legacy_semantics_and_consumers','no_science_or_media_reacceptance'])assert.equal(review.checks?.[check],'PASS','Missing compatibility check '+check);
 assert.deepEqual(review.blocking_findings,[]);assert.equal(review.publication_authorized,false);
 return bridge.original_implementation.map(row=>row.preserved);
}
/** Exact closure for isolated CI fixtures; callers must run normal collection first. */
export async function productionSourceClosure(root,manifest,descriptorPaths){
 const paths=new Set(['assets/manifest.json']),registryPath=manifest.publication?.production_registry;
 assert(!(registryPath&&manifest.publication?.production_descriptor),'Ambiguous production routes');
 const entries=registryPath?(await loadProductionRegistry(root,registryPath)).descriptors:manifest.publication?.production_descriptor?[{path:manifest.publication.production_descriptor}]:[];
 if(registryPath)paths.add(registryPath);
 const add=pin=>{assert(pin&&typeof pin.path==='string');paths.add(pin.path);};
 for(const entry of entries){if(descriptorPaths&&!descriptorPaths.includes(entry.path))continue;paths.add(entry.path);const descriptor=JSON.parse(await read(root,entry.path));paths.add(descriptor.review_path);(descriptor.implementation||[]).forEach(add);(descriptor.licenses||[]).forEach(add);add(descriptor.scope_document);
  if(entry.compatibility){add(entry.compatibility);const bridge=JSON.parse(await pinned(root,entry.compatibility));paths.add(bridge.review_path);add(bridge.original_descriptor);add(bridge.original_review);add(bridge.previous_manifest);bridge.preserved_records.forEach(add);bridge.original_implementation.forEach(p=>add(p.preserved));bridge.current_implementation.forEach(add);}
  for(const item of descriptor.assets){add(item.metadata);add(item.evidence);const record=JSON.parse(await pinned(root,item.evidence));Object.values(record.roles).forEach(add);record.build_closure.forEach(add);add(record.preview);if(record.typed_compatibility)add(record.typed_compatibility);for(const p of record.independence_evidence||[])add(p);const posters=record.final_posters;add(posters.recipe);for(const kind of ['detail','wheel']){add(posters[kind]);add(posters[kind].render_config);}const recipe=JSON.parse(await pinned(root,posters.recipe));recipe.files.forEach(add);}
 }
 return [...paths];
}

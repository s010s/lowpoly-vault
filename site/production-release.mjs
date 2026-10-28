import {correctiveContext,correctiveManifestView,composeCorrectiveRegistry} from './old-corrective-ten-selection.mjs';
import {successorReader,successorContext,composeSuccessorRegistry,historicalManifestView} from './same-id-successors.mjs';
/** Additive compact production acceptance. Does not change legacy QA or grant publication.
 * Independent review is an auditable attestation, not cryptographic reviewer authentication.
 * Process evidence stays in the private archive; one detached review binds its projection.
 */
import assert from 'node:assert/strict';
import {PRODUCTION_WHEEL_ROUTE,verifyProductionWheel} from './production-wheel-contract.mjs';
import {inspectContentProductionRelease,verifyContentProjectionReviews,CONTENT_PRODUCTION_CHECKS} from './content-production-acceptance.mjs';
import {inspectTypedProductionRelease,verifyTypedProjectionReviews,loadProductionRegistry,resolveImplementationCompatibility,productionSourceClosure as sourceClosure} from './typed-production-release.mjs';
import {readFile,realpath,stat} from 'node:fs/promises';
import {readFileSync} from 'node:fs';
import {resolve,sep,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {isDeepStrictEqual} from 'node:util';
import {immutableGitEnv} from './ci-git.mjs';
import {fetchVerifiedProductionBase,authenticatedProductionBase} from './ci-production-baseline.mjs';
const hash=b=>createHash('sha256').update(b).digest('hex');
const digest=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
const roles=['brief','config','references','generator','dependency-list','finalGLB','finalBlend'];
const canonical=v=>JSON.stringify(v,(_,x)=>x&&typeof x==='object'&&!Array.isArray(x)?Object.fromEntries(Object.keys(x).sort().map(k=>[k,x[k]])):x);
export const PRODUCTION_CHECKS=['adapter_code_and_legacy_compatibility','independent_source_acceptance','exact_subject_and_source','scientific_scope_and_limits','geometry_and_topology','source_reproducibility','standard_glb_and_decode','final_preview_and_posters','compact_provenance_and_credits'];
async function read(root,path){
 assert(typeof path==='string'&&path&&!/[\\\u0000-\u001f?#%]/.test(path)&&!path.startsWith('/')&&path.split('/').every(p=>p&&p!=='.'&&p!=='..'),'Unsafe production path');
 const full=resolve(root,path);assert(full.startsWith(resolve(root)+sep));assert.equal(await realpath(full),full,'Production symlink rejected');return readFile(full);
}
async function pinned(root,pin){assert(pin&&digest(pin.sha256)&&Number.isSafeInteger(pin.bytes)&&pin.bytes>0,'Exact production pin required');const raw=await read(root,pin.path);assert.equal(raw.length,pin.bytes,'Production size changed');assert.equal(hash(raw),pin.sha256,'Production hash changed');return raw;}
function identity(x,label){assert(x&&typeof x.id==='string'&&x.id.trim()&&typeof x.task_id==='string'&&x.task_id.trim(),label+' identity missing');}
function bilingual(x,label){for(const k of ['en','zh'])assert(typeof x?.[k]==='string'&&x[k].trim(),label+' bilingual text required');}
function independent(a,b){identity(a,'Reviewer');identity(b,'Maker');assert(a.id.trim().toLowerCase()!==b.id.trim().toLowerCase()&&a.task_id.trim().toLowerCase()!==b.task_id.trim().toLowerCase(),'Reviewer must differ from maker and preparer');}
function productionStages(record){
 assert(['layered-production-acceptance-v001','independent-production-review-receipt'].includes(record.original_acceptance.kind),'Unsupported production proof schema');
 const gates=record.production_gates;
 const required=record.original_acceptance.kind==='layered-production-acceptance-v001'
  ?['factual','visual','technical','standard_glb','source_reproducibility','runtime_parse','specification']
  :['scientific_factual_scope','visual','technical_geometry','frozen_specification','source_reproducibility','standard_glb_and_decode','package_integrity'];
 assert(gates&&required.every(k=>gates[k]?.status==='PASS'),'Missing or nonpassing production gate');
 assert(Object.values(gates).every(v=>v.status==='PASS'),'Real quality failure remains blocking');
 assert(Object.values(gates).every(v=>Array.isArray(v.source_evidence_sha256)&&v.source_evidence_sha256.length>0&&v.source_evidence_sha256.every(digest)),'Each production gate needs original evidence hash anchors');
}

// An optimization of the original checks, never a caller-supplied ID allowlist.
// Scope is established from the PR event and actual Git objects. Unknown inputs stay full.
const productionPlans=new Map();
const sha40=x=>typeof x==='string'&&/^[a-f0-9]{40}$/.test(x)&&!/^0+$/.test(x);
async function resolveProductionValidationPlan(root='.'){
 const key=resolve(root);if(productionPlans.has(key))return productionPlans.get(key);
 const pending=(async()=>{
  const full=reason=>({mode:'full',reason,reusedIds:[],descriptors:new Map()});let checkingGlobal=false;
  const git=(...args)=>execFileSync('git',args,{cwd:key,env:immutableGitEnv(),stdio:['ignore','pipe','pipe'],encoding:'utf8',maxBuffer:32*1024*1024}).trim();
  try{
   if(!['pull_request','push'].includes(process.env.GITHUB_EVENT_NAME)||!process.env.GITHUB_EVENT_PATH)return full('No authenticated PR/push event context');
   if(['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_ALTERNATE_OBJECT_DIRECTORIES'].some(k=>process.env[k]))return full('Custom Git storage/index context');
   if(git('rev-parse','--show-toplevel')!==key)return full('Source root differs from Git checkout');
   const contextKeys=['GITHUB_EVENT_NAME','GITHUB_EVENT_PATH','GITHUB_REPOSITORY','GITHUB_SHA'],context=contextKeys.map(k=>process.env[k]);
   const eventBytes=await readFile(process.env.GITHUB_EVENT_PATH),event=JSON.parse(eventBytes),pr=event.pull_request;
   const push=process.env.GITHUB_EVENT_NAME==='push';
   if(push){if(event.ref!=='refs/heads/main'||process.env.GITHUB_REF!==event.ref||event.repository?.full_name!==process.env.GITHUB_REPOSITORY)return full('Unsupported push repository/ref');}
   else if(!pr||pr.base?.ref!=='main'||pr.base?.repo?.full_name!==process.env.GITHUB_REPOSITORY||pr.head?.repo?.full_name!==process.env.GITHUB_REPOSITORY)return full('Unsupported PR repository/base');
   const base=push?event.before:pr.base.sha,head=push?event.after:pr.head.sha,checkout=git('rev-parse','HEAD');
   if(!sha40(base)||!sha40(head)||!sha40(checkout)||process.env.GITHUB_SHA!==checkout)return full('Invalid exact Git provenance');
   const parents=git('show','-s','--format=%P',checkout).split(' ');
   if((push&&checkout!==head)||(!push&&checkout!==head&&!(parents.length===2&&parents[0]===base&&parents[1]===head)))return full('PR merge checkout does not bind exact base/head');
   git('merge-base','--is-ancestor',base,checkout);
   const clean=()=>contextKeys.every((k,i)=>process.env[k]===context[i])&&readFileSync(context[1]).equals(eventBytes)&&git('rev-parse','HEAD')===checkout&&git('status','--porcelain','--untracked-files=no')===''&&execFileSync('git',['ls-files','-v','-z'],{cwd:key,env:immutableGitEnv(),encoding:'utf8',stdio:['ignore','pipe','pipe'],maxBuffer:32*1024*1024}).split('\0').filter(Boolean).every(line=>line.startsWith('H '));
   if(!clean())return full('Tracked worktree/index changed');
   // Model content scope is independent of code regression scope. Changing a validator
   // does not invalidate unchanged accepted bytes; changed code is tested separately.
   const paths=execFileSync('git',['diff','--no-renames','--name-only','-z',base,checkout],{cwd:key,env:immutableGitEnv(),stdio:['ignore','pipe','pipe'],encoding:'utf8',maxBuffer:32*1024*1024}).split('\0').filter(Boolean);
   const implementationPath=p=>/^(?:site\/(?!public\/).*\.(?:js|mjs|css|html)$|scripts\/.*\.(?:py|js|mjs)$|\.github\/|schemas\/)|(?:^|\/)package(?:-lock)?\.json$/.test(p);
   const authenticated=await fetchVerifiedProductionBase({root:key,repository:process.env.GITHUB_REPOSITORY,baseSha:base,currentSha:checkout});
   if(!authenticated.capability)return full(authenticated.reasons.join('; '));
   const baseline=authenticatedProductionBase(authenticated.capability,{root:key,repository:process.env.GITHUB_REPOSITORY,baseSha:base,currentSha:checkout});
   let prior=JSON.parse(git('show',`${base}:assets/manifest.json`));const selected=JSON.parse(await readFile(resolve(key,'assets/manifest.json')));
   const successorRead=successorReader(key),successors=successorContext({manifest:selected,read:successorRead}),current=successors?successors.base:selected;
   const corrective=correctiveContext({manifest:selected,read:successorRead});
   if(corrective){assert.equal(corrective.selection.baseline_commit,base,'Corrective baseline moved');assert(isDeepStrictEqual(prior,corrective.baseline.manifest),'Corrective before-image differs from authenticated production base');prior=historicalManifestView({manifest:prior,read:successorRead});}
   else if(successors)assert.equal(successors.selection.baseline_commit,base,'Successor baseline commit moved; rebind and independently review the exact current base');
   checkingGlobal=true;
   const unique=m=>Array.isArray(m.assets)&&new Set(m.assets.map(a=>a.id)).size===m.assets.length;
   assert(unique(prior)&&unique(current),'Duplicate/missing catalog IDs');
   for(const a of prior.assets)assert(isDeepStrictEqual(a,current.assets.find(b=>b.id===a.id)),'Append-only historical metadata changed');
   const registry=current.publication?.production_registry;
   if(!registry||registry!==prior.publication?.production_registry||current.publication.production_descriptor)return full('Production route transition');
   const {assets:priorAssets,...priorShared}=prior,{assets:currentAssets,...currentShared}=current;
   if(!isDeepStrictEqual(priorShared,currentShared))return full('Shared publication metadata changed');
   const previousRegistry=JSON.parse(git('show',`${base}:${registry}`)),nextRegistry=await loadProductionRegistry(key,registry);
   assert(isDeepStrictEqual(nextRegistry.descriptors.slice(0,previousRegistry.descriptors.length),previousRegistry.descriptors),'Old registered descriptor changed');
   assert(isDeepStrictEqual(nextRegistry.asset_ids.slice(0,previousRegistry.asset_ids.length),previousRegistry.asset_ids),'Old registered IDs changed');
   const allPaths=new Set(await sourceClosure(key,selected));
   // Reuse the existing global registry composition and append-only validators.
   const {readRegistry,readRegistryAtCommit}=await import('./model-registry-cli.mjs');
   const {assertRegistryAppend,composeRegistry,LEGACY_OUTPUTS,recordReference}=await import('./model-registry.mjs');
   const previousModels=readRegistryAtCommit(key,base),currentModels=readRegistry(key);
   const addedIds=assertRegistryAppend(previousModels,currentModels),added=new Set(addedIds),composed=successors?composeSuccessorRegistry({registry:currentModels,baseManifest:current,selection:successors.selection,selectionPin:successors.selectionPin,appendPin:successors.appendPin,read:successorRead}):composeRegistry(currentModels);
   assert.deepEqual(current.assets.map(a=>a.id).sort(),currentModels.records.map(r=>r.id).sort(),'Registry/manifest ID coverage differs');
   for(const record of currentModels.records)assert.deepEqual(record.asset,current.assets.find(a=>a.id===record.id),'Registry/manifest metadata differs');
   const finalComposition=corrective?composeCorrectiveRegistry({baseOutput:composed,context:corrective}):composed;
   for(const [kind,path]of Object.entries(LEGACY_OUTPUTS)){
    if(kind!=='manifest')assert.deepEqual(JSON.parse(await read(key,path)),finalComposition[kind],'Derived registry output differs: '+path);
    allPaths.add(path);
   }
   allPaths.add('registry/baseline.json');
   for(const record of currentModels.records){allPaths.add(recordReference(record).path);if(record.asset.credits){assert(record.asset.credits.startsWith(`assets/additions/${record.id}/`)&&record.asset.credits.endsWith('/CREDITS.txt'),'Invalid owned credits path');allPaths.add(record.asset.credits);}}
   const oldBatches=new Set(previousModels.batches.map(b=>b.id));
   for(const batch of currentModels.batches){allPaths.add(`registry/batches/${batch.id}.json`);if(!oldBatches.has(batch.id)){assert(batch.records.every(r=>added.has(r.id)),'New batch must own only added IDs');for(const pin of batch.evidence){assert(allPaths.has(pin.path),'New evidence is not in production source closure');assert.equal(hash(await read(key,pin.path)),pin.sha256,'Registry evidence hash changed');}}}

   // No directory exemptions: new catalog-side inputs must enter a validated graph.
   if(paths.some(p=>!allPaths.has(p)&&!implementationPath(p)))return full('Changed path outside validated source closure');
   const objects=ref=>new Map(execFileSync('git',['ls-tree','-r','-z',ref],{cwd:key,env:immutableGitEnv(),stdio:['ignore','pipe','pipe'],encoding:'utf8',maxBuffer:32*1024*1024}).split('\0').filter(Boolean).map(row=>{const tab=row.indexOf('\t');assert(tab>0,'Malformed Git tree entry');return [row.slice(tab+1),row.slice(0,tab)];}));
   const baseObjects=objects(base),headObjects=objects(checkout);
   const descriptors=new Map(),reusedIds=[];
   for(const entry of previousRegistry.descriptors){
    const descriptorJSON=JSON.parse(await read(key,entry.path));
    const creditPaths=descriptorJSON.assets.map(a=>current.assets.find(b=>b.id===a.id)?.credits).filter(Boolean);
    const implementation=new Set((descriptorJSON.implementation||[]).map(p=>p.path));
    if(entry.compatibility){const bridge=JSON.parse(await pinned(key,entry.compatibility));for(const pin of bridge.current_implementation)implementation.add(pin.path);}
    // A file used as actual model source is content even if it is also a tool.
    for(const item of descriptorJSON.assets){const record=JSON.parse(await pinned(key,item.evidence));for(const pin of [...Object.values(record.roles||{}),...(record.build_closure||[])])implementation.delete(pin.path);}
    const closure=[...await sourceClosure(key,current,[entry.path]),...creditPaths].filter(p=>p!=='assets/manifest.json'&&p!==registry&&!implementation.has(p));
    if(!closure.every(p=>{const b=baseObjects.get(p),h=headObjects.get(p);return /^100644 blob [a-f0-9]{40}$/.test(b||'')&&b===h;}))continue;
    const raw=await read(key,entry.path),descriptor=JSON.parse(raw),assets=[],records=[];
    for(const item of descriptor.assets){const asset=JSON.parse(await pinned(key,item.metadata)),record=JSON.parse(await pinned(key,item.evidence));assert.equal(asset.id,item.id);assert.equal(record.asset_id,item.id);assert(isDeepStrictEqual(asset,prior.assets.find(a=>a.id===item.id)),'Baseline metadata projection differs');assets.push(asset);records.push(record);}
    descriptors.set(entry.path,{descriptor,descriptor_sha256:hash(raw),assets,records,audits:assets.map(a=>({id:a.id,status:'UNCHANGED_BASELINE'})),productionAccepted:true,releaseChecks:'UNCHANGED_BASELINE',postReleaseVerified:[...new Set(records.map(r=>r.postReleaseVerified?.status))].filter(Boolean).join(',')||'NOT_RECHECKED',publication_authorized:false,unchanged_baseline:{base,head,checkout}});
    reusedIds.push(...assets.map(a=>a.id));
   }
   const legacyBaseline={...prior,publication:{...prior.publication},assets:prior.assets.filter(a=>!a.production_release)};delete legacyBaseline.publication.production_registry;
   return {mode:'incremental',base,head,checkout,registry,baseline,reusedIds,descriptors,clean,legacyBaseline};
  }catch(error){if(checkingGlobal)throw error;return full('Scope unavailable: '+error.message);}
 })();productionPlans.set(key,pending);return pending;
}

export async function productionValidationPlan(root='.') {
 const plan=await resolveProductionValidationPlan(root);if(plan.clean)assert(plan.clean(),'Tracked inputs changed after scope resolution');
 const {descriptors,clean,...summary}=plan;return structuredClone(summary);
}
const incrementalInspections=new Map(),incrementalCollections=new Map();
async function memoizedIncremental(cache,root,descriptorPath,registryPath,run){
 const plan=await resolveProductionValidationPlan(root);
 if(plan.mode!=='incremental')return run();
 assert(plan.clean(),'Tracked inputs changed after scope resolution');
 if(registryPath!==undefined)assert.equal(registryPath,plan.registry,'Different production registry contexts');
 const key=JSON.stringify([resolve(root),plan.checkout,descriptorPath,registryPath||plan.registry]);
 if(!cache.has(key))cache.set(key,run().catch(error=>{cache.delete(key);throw error;}));
 return structuredClone(await cache.get(key));
}
export async function inspectProductionRelease(root,descriptorPath,registryPath){
 const plan=await resolveProductionValidationPlan(root);
 if(plan.descriptors.has(descriptorPath)){if(registryPath!==undefined)assert.equal(registryPath,plan.registry,'Different production registry contexts');assert(plan.clean(),'Tracked inputs changed after scope resolution');return structuredClone(plan.descriptors.get(descriptorPath));}
 return memoizedIncremental(incrementalInspections,root,descriptorPath,registryPath,()=>inspectProductionReleaseFully(root,descriptorPath,registryPath));
}
async function inspectProductionReleaseFully(root,descriptorPath,registryPath){
 const raw=await read(root,descriptorPath),descriptor=JSON.parse(raw);
 if(descriptor.kind==='content-production-release-v1')return inspectContentProductionRelease(root,descriptorPath,raw);
 if(descriptor.kind==='typed-production-release-v1')return inspectTypedProductionRelease(root,descriptorPath,raw,registryPath);
 const compatibilityPins=await resolveImplementationCompatibility(root,descriptorPath,descriptor,raw,registryPath);
 assert.equal(descriptor.schema_version,1);assert.equal(descriptor.kind,'production-release-v1');assert.equal(descriptor.publication_authorized,false,'Production projection cannot grant publication');
 assert(/^[0-9a-f]{40}$/.test(descriptor.baseline_commit),'Exact production baseline required');
 assert(Array.isArray(descriptor.implementation)&&descriptor.implementation.length>0,'Bound adapter implementation required');for(const file of compatibilityPins||descriptor.implementation)await pinned(root,file);await pinned(root,descriptor.scope_document);
 identity(descriptor.producer,'Preparer');assert(Array.isArray(descriptor.assets)&&descriptor.assets.length,'Empty production release');
 const ids=new Set(),assets=[],records=[],audits=[];
 for(const item of descriptor.assets){
  assert(typeof item.id==='string'&&/^[a-z0-9][a-z0-9-]*$/.test(item.id)&&!ids.has(item.id),'Duplicate/invalid production ID');ids.add(item.id);
  const asset=JSON.parse(await pinned(root,item.metadata)),record=JSON.parse(await pinned(root,item.evidence));
  assert.equal(asset.id,item.id);assert.equal(record.asset_id,item.id);assert.equal(record.kind,'compact-production-release-v1');assert.equal(record.schema_version,1);
  assert.equal(asset.production_release,descriptorPath);assert.equal(asset.revision,record.revision);assert.equal(record.productionAccepted,true);
  identity(record.maker,'Maker');identity(record.original_acceptance?.reviewer,'Original production reviewer');independent(record.original_acceptance.reviewer,record.maker);
  assert(digest(record.original_acceptance.sha256),'Missing original independent production proof');
  assert.equal(record.original_acceptance.subject.glb_sha256,asset.sha256?.glb,'Independent proof belongs to a different GLB');
  if(record.original_acceptance.subject.revision)assert.equal(record.original_acceptance.subject.revision,asset.revision);
  if(record.original_acceptance.subject.blend_sha256)assert.equal(record.original_acceptance.subject.blend_sha256,asset.sha256?.blend);
  assert.equal(record.legacy_record.mutated,false);assert(digest(record.legacy_record.sha256));
  assert.deepEqual(record.blocking_findings,[],'Real quality finding remains blocking');productionStages(record);
  assert.deepEqual(Object.keys(record.roles).sort(),roles.slice().sort(),'All seven source roles required');
  for(const role of roles){await pinned(root,record.roles[role]);assert.equal(record.subject[role],record.roles[role].sha256,'Subject/role hash mismatch');}
  assert(Array.isArray(record.build_closure)&&record.build_closure.length>=2,'Source dependency closure required');for(const dependency of record.build_closure)await pinned(root,dependency);
  const proof=record.original_acceptance.subject;
  if(proof.scientific_brief_sha256)assert.equal(proof.scientific_brief_sha256,record.subject.brief);
  if(proof.references_sha256)assert.equal(proof.references_sha256,record.legacy_record.technical_references_sha256,'Legacy reference adapter binding changed');
  assert.equal(record.legacy_record.scientific_brief_sha256,record.subject.brief);assert.equal(record.legacy_record.scientific_references_sha256,record.subject.references);
  if(proof.brief_sha256)assert.equal(proof.brief_sha256,record.legacy_record.technical_brief_sha256,'Legacy subject brief binding changed');
  for(const [key,role]of [['glb','finalGLB'],['blend','finalBlend']]){assert.equal(asset[key],record.roles[role].path);assert.equal(asset.sha256?.[key],record.roles[role].sha256);}
  await pinned(root,record.preview);assert.equal(asset.preview,record.preview.path);assert.equal(asset.sha256.preview,record.preview.sha256);
  assert.equal(record.preview_provenance.source_glb_sha256,asset.sha256.glb);assert.equal(record.preview_provenance.independently_reviewed_original_preview,true);assert(digest(record.preview_provenance.review_sha256));
  bilingual(asset.name,'Name');bilingual(asset.description,'Description');bilingual(record.scientific_limits,'Scientific limits');assert.deepEqual(asset.description,record.scientific_limits,'Public uncertainty differs from reviewed scope');
  assert.equal(asset.license,'CC-BY-4.0');assert.equal(asset.units,'meters');assert.equal(asset.representation,'fossil-specimen');assert(typeof record.inventory_departure==='string'&&record.inventory_departure.trim());
  assert(Array.isArray(asset.reference_credits)&&asset.reference_credits.length);assert.equal(record.source_archive.status,'VERIFIED_PRIVATE_ARCHIVE');assert(digest(record.source_archive.receipt_sha256)&&digest(record.source_archive.index_sha256));
  const brief=JSON.parse(await pinned(root,record.roles.brief)),budget=brief.geometry_policy;assert(budget,'Frozen geometry budget required');
  for(const key of ['max_triangles','max_materials','max_primitives','max_glb_bytes'])assert.equal(record.frozen_budget[key],budget[key],'Frozen budget changed');
  const native=JSON.parse(execFileSync('python3',[resolve(dirname(fileURLToPath(import.meta.url)),'../scripts/qa_glb.py'),resolve(root,asset.glb),'--max-triangles',String(budget.max_triangles),'--max-materials',String(budget.max_materials),'--max-primitives',String(budget.max_primitives)],{encoding:'utf8',maxBuffer:2*1024*1024,env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}}));
  assert(!native.errors.length,'Native GLB failure');assert(native.bytes<=budget.max_glb_bytes);assert(native.materials<=budget.max_materials);assert(native.scene_primitives_estimated_base_draw_calls<=budget.max_primitives);
  assert.equal(native.scene_triangles,asset.triangles);assert.equal(asset.triangles,record.measurements.triangles);assert.deepEqual(native.bounds_m.size,asset.dimensions);assert.deepEqual(asset.dimensions,record.measurements.dimensions);
  assert(record.postReleaseVerified&&['NOT_PUBLISHED','QUEUED','RUNNING','PASS','FAIL','ENVIRONMENT_BLOCKED'].includes(record.postReleaseVerified.status));
  // Unknown browser evidence never becomes PASS. A known actual failure cannot be suppressed.
  assert.notEqual(record.postReleaseVerified.status,'FAIL','Known post-release failure needs resolution');
  assets.push(asset);records.push(record);audits.push({id:asset.id,status:'PASS',native});
 }
 return {descriptor,descriptor_sha256:hash(raw),assets,records,audits,productionAccepted:true,releaseChecks:'PENDING_INDEPENDENT_PROJECTION_REVIEW',postReleaseVerified:'NOT_PUBLISHED',publication_authorized:false};
}
export async function collectProductionRelease(root,descriptorPath,registryPath){
 return memoizedIncremental(incrementalCollections,root,descriptorPath,registryPath,()=>collectProductionReleaseFully(root,descriptorPath,registryPath));
}
async function collectProductionReleaseFully(root,descriptorPath,registryPath,results){
 const result=await inspectProductionRelease(root,descriptorPath,registryPath);assert(!result.records.some(record=>record.postReleaseVerified?.status==='FAIL'),'Known post-release failure needs resolution');if(result.unchanged_baseline){results?.set(descriptorPath,result);return result.assets;}
 const review=JSON.parse(await read(root,result.descriptor.review_path));
 assert.equal(review.schema_version,1);assert.equal(review.kind,'independent-production-projection-review-v1');assert.equal(review.status,'PASS','Independent production projection review is pending');
 assert.equal(review.reviewed_descriptor_sha256,result.descriptor_sha256,'Stale projection review');independent(review.reviewer,result.descriptor.producer);
 for(const record of result.records)independent(review.reviewer,record.maker);
 assert.deepEqual(review.blocking_findings,[]);for(const key of result.descriptor.kind==='content-production-release-v1'?CONTENT_PRODUCTION_CHECKS:PRODUCTION_CHECKS)assert.equal(review.checks?.[key],'PASS','Independent projection subcheck missing/nonpassing: '+key);
 assert.equal(review.publication_authorized,false,'Projection review never grants publication');
 const acceptances=[...new Set(result.records.map(r=>r.original_acceptance.sha256))].sort();assert.deepEqual(review.original_acceptance_sha256?.slice().sort(),acceptances,'Missing independent original acceptance binding');
 if(!result.unchanged_baseline)for(let i=0;i<result.assets.length;i++)await verifyProductionPosters(root,result.assets[i],result.records[i]);
 if(result.descriptor.kind==='typed-production-release-v1')await verifyTypedProjectionReviews(root,result,review);
 if(result.descriptor.kind==='content-production-release-v1')await verifyContentProjectionReviews(root,result,review);
 results?.set(descriptorPath,result);return result.assets;
}
export async function appendProductionRelease(root,base,descriptorPath,results){
 const added=await collectProductionReleaseFully(root,descriptorPath,undefined,results),ids=new Set(base.assets.map(a=>a.id));for(const a of added)assert(!ids.has(a.id),'Production release cannot silently duplicate or replace an existing inventory ID: '+a.id);
 return {...base,publication:{...base.publication,production_descriptor:descriptorPath},assets:[...base.assets,...added]};
}
// BEGIN_EXPLICIT_PRODUCTION_REGISTRY
/** Current independently reviewed batch set; never overwrite the old singular route. */
export async function appendProductionReleases(root,base,registryPath,results){
 assert(!base.publication?.production_descriptor&&!base.publication?.production_registry,'Production registry needs the canonical pre-production base, not a silently replaced batch');
 const registry=await loadProductionRegistry(root,registryPath);
 const paths=new Set(),ids=new Set(base.assets.map(a=>a.id)),added=[];
 assert.equal(ids.size,base.assets.length,'Duplicate base asset identity');
 for(const pin of registry.descriptors){
  assert(pin&&typeof pin==='object'&&!Array.isArray(pin));
  assert(!paths.has(pin.path),'Duplicate production descriptor path');paths.add(pin.path);await pinned(root,pin);
  for(const asset of await collectProductionReleaseFully(root,pin.path,registryPath,results)){assert(!ids.has(asset.id),'Production batch IDs must be disjoint from base and each other: '+asset.id);ids.add(asset.id);added.push(asset);}
 }
 assert.deepEqual(added.map(a=>a.id),registry.asset_ids,'Production registry has missing/extra/reordered assets');
 return {...base,publication:{...base.publication,production_registry:registryPath},assets:[...base.assets,...added]};
}
// END_EXPLICIT_PRODUCTION_REGISTRY
export async function verifyProductionPosters(root,asset,record){
 const p=record.final_posters;assert(p&&['blender-cycles-cpu-v1',PRODUCTION_WHEEL_ROUTE].includes(p.route),'Final poster route required');const mixed=p.route===PRODUCTION_WHEEL_ROUTE;assert.equal(p.source_glb_sha256,asset.sha256.glb);assert.equal(p.browser_capture,mixed);
 assert(digest(p.recipe_sha256)&&typeof p.blender_version==='string');
 const recipe=JSON.parse(await pinned(root,p.recipe));assert.equal(p.recipe.sha256,p.recipe_sha256);assert.equal(recipe.source_glb_sha256,asset.sha256.glb);assert.equal(recipe.blender_version,p.blender_version);assert.equal(recipe.rendered_unchanged_source,true);for(const source of recipe.files)await pinned(root,source);
 for(const [kind,size]of (mixed?[['detail',[512,512]]]:[['detail',[512,512]],['wheel',[768,432]]])){
  const config=JSON.parse(await pinned(root,p[kind].render_config));assert.equal(config.source_geometry_and_materials_unchanged,true);assert.equal(config.film_transparent,true);assert.equal(config.version,p.blender_version);assert.equal(config.renderer_sha256,recipe.files[0].sha256);assert.deepEqual(config.resolution,size);
  const b=await pinned(root,p[kind]);assert.equal(b.subarray(0,8).toString('hex'),'89504e470d0a1a0a');assert.deepEqual([b.readUInt32BE(16),b.readUInt32BE(20)],size);assert.equal(b[24],8,'8-bit final poster required');assert.equal(b[25],6,'RGBA final poster required');
  assert.deepEqual(p[kind].camera_degrees,[42,23.3]);assert.equal(p[kind].source_glb_sha256,asset.sha256.glb);assert(digest(p[kind].pixel_sha256));
 }
 if(mixed)await verifyProductionWheel(root,asset,record);
 assert.equal(asset.production_posters?.route,p.route);for(const kind of ['detail','wheel'])assert.equal(asset.production_posters[kind],p[kind].path);
 return p;
}

/** Extend only an independently checked explicit production scope; never rediscover assets. */
export async function productionGalleryResources(root,manifest,resources,results){
 const additions=manifest.assets.filter(a=>a.production_release);if(!additions.length)return resources;
 const next=structuredClone(resources),checked=new Map(),inspections=new Map();
 for(const asset of additions){if(!checked.has(asset.production_release))checked.set(asset.production_release,results?.get(asset.production_release)?.assets??await collectProductionRelease(root,asset.production_release));assertProductionMetadata(checked.get(asset.production_release).find(a=>a.id===asset.id),asset);
 if(!inspections.has(asset.production_release))inspections.set(asset.production_release,results?.get(asset.production_release)??await inspectProductionRelease(root,asset.production_release));
 const inspected=inspections.get(asset.production_release),record=inspected.records.find(r=>r.asset_id===asset.id),p=record.final_posters;const existing=next.posters[asset.id];
 const expected={render_route:p.route,source_glb_sha256:asset.sha256.glb,production_descriptor:asset.production_release,recipe_sha256:p.recipe_sha256,detail:p.detail.path.replace(/^site\/public\//,''),wheel:p.wheel.path.replace(/^site\/public\//,''),...(p.route===PRODUCTION_WHEEL_ROUTE?{wheelSpec:p.wheel.wheelSpec}:{})};
 if(existing)assert.deepEqual(existing,expected,'Cannot replace existing gallery poster');else next.posters[asset.id]=expected;
 for(const kind of ['detail','wheel']){const seal={path:expected[kind],sha256:p[kind].sha256,bytes:p[kind].bytes},old=next.files.find(f=>f.path===seal.path);if(old)assert.deepEqual(old,seal,'Changed production poster');else next.files.push(seal);}
 }return next;
}

export function assertProductionMetadata(reviewed,actual){
 assert(reviewed,'Missing independently reviewed production metadata');
 for(const key of Object.keys(reviewed))assert.deepEqual(actual[key],reviewed[key],'Unbound production metadata: '+key);
 const derived=new Set(['downloads','file_sizes','glb_bytes','blend_bytes','material_count','qa','worlds','packs']);
 for(const key of Object.keys(actual))assert(key in reviewed||derived.has(key),'Unexpected production metadata field: '+key);
}

/** Explicit optional route, called only from the existing compatibility hook. */
export async function appendProductionPosterInputState(root,assets,resources,legacy,results){
 const production=[],valid=[...legacy.valid];
 // Full inspections are reusable only inside this invocation; later calls revalidate files.
 const checked=new Map(),inspections=new Map();
 for(const asset of assets){
  if(!checked.has(asset.production_release))checked.set(asset.production_release,results?.get(asset.production_release)?.assets??await collectProductionRelease(root,asset.production_release));
  assertProductionMetadata(checked.get(asset.production_release).find(a=>a.id===asset.id),asset);
  if(!inspections.has(asset.production_release))inspections.set(asset.production_release,results?.get(asset.production_release)??await inspectProductionRelease(root,asset.production_release));
  const inspected=inspections.get(asset.production_release),p=inspected.records.find(r=>r.asset_id===asset.id).final_posters,poster=resources.posters[asset.id];
  assert(['blender-cycles-cpu-v1',PRODUCTION_WHEEL_ROUTE].includes(p.route),'Explicit final production poster route required');assert.equal(poster?.render_route,p.route);if(p.route===PRODUCTION_WHEEL_ROUTE)assert.deepEqual(poster.wheelSpec,p.wheel.wheelSpec);assert.equal(poster.recipe_sha256,p.recipe_sha256);assert.equal(poster.production_descriptor,asset.production_release);assert.equal(poster.source_glb_sha256,asset.sha256.glb);
  for(const kind of ['detail','wheel']){assert.equal(poster[kind],p[kind].path.replace(/^site\/public\//,''));const seal=resources.files.find(f=>f.path===poster[kind]);assert.equal(seal?.sha256,p[kind].sha256);assert.equal(seal?.bytes,p[kind].bytes);}
  assert(!valid.includes(asset.id),'Duplicate production input state');valid.push(asset.id);production.push(asset.id);
 }
 return {...legacy,valid,production};
}
export {productionSourceClosure} from './typed-production-release.mjs';

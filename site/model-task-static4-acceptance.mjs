/** Bounded static4 source adapter. It neither repairs source reports nor grants
 * full-formal, runtime, user, or publication approval. The old v2 route is intact. */
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {SOURCE_ROLES,sha256,parsePinnedDocument,pointerValue,assertProductionMaterial,preserveUnverifiedRuntimeStatus} from './inventory-type-acceptance.mjs';
import {V2_REPRESENTATION_LITERALS,normalizeV2Identity,validateV2Measurements} from './model-task-v2-acceptance.mjs';
import {STATIC4_SOURCE_PROFILES,STATIC4_HISTORY_CONTRACTS} from './static4-source-profiles.mjs';
export const STATIC4_ADAPTER='model-task-static4-split-source-v1';
export const STATIC4_RECEIPT='compact-model-task-static4-split-source-v1';
export const STATIC4_REVIEW_CHECKS=Object.freeze([
 'original_report_authenticity_and_complete_field_mapping','original_review_independence',
 'six_original_roles_and_final_native_glb','derived_dependency_inventory_and_import_closure',
 'exact_current_checklists_and_scope_limits','original_technical_visual_factual_specification',
 'origin_delta_and_historical_morphology_inheritance','brief_revision_inheritance',
 'representation_and_scientific_limits','fresh_final_glb_capture_and_current_ci_separate',
 'runtime_user_and_full_formal_status_not_promoted'
]);
const NATIVE_PROOFS={
 'v2-scoped-repair-status':{native:'/source_sha256',glb:'/glb_sha256',checks:{status:'PASS',triangles_match:true,bounds_match:true,errors:[]}},
 'scoped-static-exact-glb-report':{native:'/native_source_sha256',glb:'/exact_glb_sha256',checks:{status:'PASS_TECHNICAL_SCOPE',semantic_match:true,byte_identical:true,single_identity_asset_root:true,native_scene_has_only_export:true,applied_mesh_transforms:true,all_components_positive_volume_closed:true,'source_audit/errors':[],'source_audit/status':'pass','reexport_audit/errors':[],'reexport_audit/status':'pass'}}
};
const ORIGINAL_ROLES=SOURCE_ROLES.filter(r=>r!=='dependency-list');
const hash=x=>sha256(Buffer.from(JSON.stringify(x)));
const copy=x=>structuredClone(x);
const text=x=>typeof x==='string'&&!!x.trim();
const digest=x=>typeof x==='string'&&/^[a-f0-9]{64}$/.test(x);
const need=(x,m)=>assert(x,'HOLD: static4 '+m);
const equal=(a,b,m)=>assert.deepEqual(a,b,'HOLD: static4 '+m);
const exact=(x,keys,m)=>equal(Object.keys(x||{}).sort(),[...keys].sort(),m);
const publicOnly=x=>need(!/\/workspace\/|\/home\/|\/tmp\/|\/root\/|drive\.google\.com|docs\.google\.com/.test(JSON.stringify(x)),'private locator in receipt');
const pin=p=>{need(p&&digest(p.sha256)&&Number.isSafeInteger(p.bytes)&&p.bytes>0,'missing exact byte pin');return {sha256:p.sha256,bytes:p.bytes};};
const checked=(b,p)=>{pin(p);need(Buffer.isBuffer(b)||b instanceof Uint8Array,'missing original bytes');equal(b.length,p.bytes,'byte count changed');equal(sha256(b),p.sha256,'bytes changed');return Buffer.from(b);};
const value=(d,p)=>{need(text(p)&&p.startsWith('/'),'missing pointer');const v=pointerValue(d,p);need(v!==undefined,'missing source field '+p);return v;};
function actor(x){if(typeof x==='string')return normalizeV2Identity(x.replace(/ \(independent of maker\)$/,''));if(x&&typeof x==='object'){const all=[x.task_id,x.task,x.id].filter(text).map(normalizeV2Identity);need(all.length,'missing identity');need(new Set(all).size===1,'conflicting identity declarations');return all[0];}need(false,'original identity missing');}
function matchProfile(doc){
 const matches=STATIC4_SOURCE_PROFILES.filter(p=>JSON.stringify(Object.keys(doc).sort())===JSON.stringify(p.original_fields)&&Object.entries(p.declarations).every(([k,v])=>JSON.stringify(doc[k])===JSON.stringify(v)));
 need(matches.length===1,'unknown or ambiguous source schema');return matches[0];
}
/** Every current field is pinned. Historical HOLDs remain original historical
 * fields; only the explicitly enumerated current decision is scoped evidence. */
export function mapStatic4Decision(doc,{asset_id,revision,glb_sha256,native_sha256,maker,candidate,native_proof}={}){
 assertProductionMaterial(doc);const p=matchProfile(doc);
 equal(value(doc,p.decision_pointer),p.decision_value,'nonpassing current decision');
 for(const [path,expected]of Object.entries(p.checklists))equal(hash(value(doc,path)),expected,'changed/nonpassing current checklist '+path);
 need(digest(glb_sha256)&&digest(native_sha256),'final GLB/native binding missing');
 equal(value(doc,p.glb_pointer),glb_sha256,'reviewed final GLB mismatch');
 if(p.native_pointer)equal(value(doc,p.native_pointer),native_sha256,'reviewed native source mismatch');
 else {equal(native_proof?.checks,NATIVE_PROOFS[p.profile]?.checks,'nonpassing independent native checks');need(native_proof&&digest(native_proof.document_sha256)&&text(native_proof.pointer),'independent native evidence missing');equal(native_proof.value,native_sha256,'independent native source mismatch');}
 need(text(asset_id)&&text(revision),'missing release identity');
 if(doc.asset_id!==undefined)equal(doc.asset_id,asset_id,'source report asset mismatch');
 if(doc.revision!==undefined)equal(doc.revision,revision,'source report revision mismatch');
 need(candidate&&candidate.asset_id===asset_id&&candidate.revision===revision,'pinned current candidate identity missing');
 // Missing report identity is explicit, never fabricated from a filename.
 const who=actor(value(doc,p.reviewer_pointer)),makerIdentity=actor(maker);
 need(who!==makerIdentity,'maker self-review');
 if(doc.maker!==undefined)equal(actor(doc.maker),makerIdentity,'source maker conflicts with candidate');
 const scope=value(doc,p.scope_pointer);need(typeof scope==='string'||(scope&&typeof scope==='object'),'missing bounded scope');
 return {profile:p.profile,original_schema:copy(p.declarations),original_fields:Object.fromEntries(Object.entries(doc).map(([k,v])=>[k,hash(v)])),
  decision_pointer:p.decision_pointer,decision_value:p.decision_value,checklists:copy(p.checklists),
  identity_basis:doc.asset_id!==undefined&&doc.revision!==undefined?'EXPLICIT_ORIGINAL_REPORT':'PINNED_CANDIDATE_AND_EXACT_REVIEWED_GLB',
  reviewer_task_sha256:hash(who),maker_task_sha256:hash(makerIdentity),
  scope_pointer:p.scope_pointer,scope_sha256:hash(scope),glb_sha256,native_sha256,
  independent_native_proof:p.native_pointer?null:{document_sha256:native_proof.document_sha256,pointer_sha256:hash(native_proof.pointer),value_sha256:hash(native_proof.value),checks:copy(native_proof.checks)},
  origin_delta:p.origin_delta,claim:p.origin_delta?'BOUNDED_ORIGIN_DELTA_ONLY_REQUIRES_PRIOR_MORPHOLOGY':'BOUNDED_STATIC4_ORIGINAL_REVIEW_ONLY',
  full_formal_approval:false,runtime_approval:false,user_approval:false,publication_authorized:false};
}
function validateDecision(d){
 const p=STATIC4_SOURCE_PROFILES.find(p=>p.profile===d.profile);need(p&&p.reviewer_pointer,'unknown/anonymous current report');
 exact(d,['profile','original_schema','original_fields','decision_pointer','decision_value','checklists','identity_basis','reviewer_task_sha256','maker_task_sha256','scope_pointer','scope_sha256','glb_sha256','native_sha256','independent_native_proof','origin_delta','claim','full_formal_approval','runtime_approval','user_approval','publication_authorized'],'decision projection fields');
 equal(d.original_schema,p.declarations,'schema declaration changed');exact(d.original_fields,p.original_fields,'original report field coverage');need(Object.values(d.original_fields).every(digest),'source field hash missing');
 equal(d.decision_pointer,p.decision_pointer,'decision pointer changed');equal(d.decision_value,p.decision_value,'decision changed');equal(d.checklists,p.checklists,'original checklist changed');
 for(const [pointer,expected]of Object.entries(p.checklists))if(pointer.slice(1).indexOf('/')<0)equal(d.original_fields[pointer.slice(1)],expected,'checklist field binding changed');
 equal(d.scope_pointer,p.scope_pointer,'scope pointer changed');equal(d.scope_sha256,p.checklists[p.scope_pointer],'original scope changed');for(const k of ['reviewer_task_sha256','maker_task_sha256','scope_sha256','glb_sha256','native_sha256'])need(digest(d[k]),'decision pin missing '+k);need(d.reviewer_task_sha256!==d.maker_task_sha256,'self-review');
 need(['EXPLICIT_ORIGINAL_REPORT','PINNED_CANDIDATE_AND_EXACT_REVIEWED_GLB'].includes(d.identity_basis),'identity promoted');equal(d.origin_delta,p.origin_delta,'delta relabeled');equal(d.claim,p.origin_delta?'BOUNDED_ORIGIN_DELTA_ONLY_REQUIRES_PRIOR_MORPHOLOGY':'BOUNDED_STATIC4_ORIGINAL_REVIEW_ONLY','scope promoted');
 for(const k of ['full_formal_approval','runtime_approval','user_approval','publication_authorized'])equal(d[k],false,'approval promoted');
 if(p.native_pointer)equal(d.independent_native_proof,null,'ambiguous native binding');else {const b=d.independent_native_proof;exact(b,['document_sha256','pointer_sha256','value_sha256','checks'],'native proof');equal(b.checks,NATIVE_PROOFS[p.profile]?.checks,'native comparison failed');need(digest(b.document_sha256)&&digest(b.pointer_sha256),'native proof missing');equal(b.value_sha256,hash(d.native_sha256),'native proof changed');}
}
const representations={...V2_REPRESENTATION_LITERALS,'fossil-shell-reconstruction':'fossil-specimen','fossil-dorsal-exoskeleton-reconstruction':'fossil-specimen'};
export function mapStatic4Brief(brief,references,id,revision,mapping,briefBinding){
 equal(brief.template_version,'model-task-v2','brief schema');equal(brief.asset_id,id,'brief asset');need(text(brief.revision),'brief revision');
 exact(mapping,['source_pointer','original_value_sha256','representation','reconstruction_type'],'representation fields');equal(mapping.source_pointer,'/representation','representation pointer');const original=brief.representation;
 need(Object.hasOwn(representations,original),'unknown representation');equal(mapping.original_value_sha256,hash(original),'representation source changed');equal(mapping.representation,representations[original],'representation relabeled');equal(mapping.reconstruction_type,mapping.representation==='fossil-specimen'?'specimen':mapping.representation==='living-reconstruction'?'whole-organism':'artistic-concept','reconstruction relabeled');
 if(brief.revision!==revision){equal(brief.revision,'r001','unsupported inherited brief revision');equal(revision,'r002','unsupported target brief revision');need(briefBinding&&briefBinding.report_binds_original_brief===true&&briefBinding.report_revision===revision&&digest(briefBinding.report_sha256),'unproven inherited brief revision');}
 const budget=brief.geometry_policy;for(const k of ['max_triangles','max_materials','max_primitives','max_glb_bytes'])need(Number.isSafeInteger(budget?.[k])&&budget[k]>0,'missing frozen budget '+k);
 const refs=Array.isArray(references)?references:(references.sources??references.references);need(Array.isArray(refs)&&refs.length,'missing original references');need(text(brief.scope)||brief.morphology,'missing scientific scope');
 return {kind:'bounded-static4-brief-map-v1',asset_id:id,revision,original_brief_revision:brief.revision,inherited_brief:brief.revision!==revision,brief_revision_binding:brief.revision===revision?null:copy(briefBinding),representation_mapping:copy(mapping),original_brief_semantic_sha256:hash(brief),original_references_semantic_sha256:hash(references),frozen_budget:copy(budget),original_criteria_created:false,publication_authorized:false};
}
function parseManifest(raw){const entries=new Map();for(const line of raw.toString('utf8').split(/\r?\n/)){if(!line)continue;const m=/^([a-f0-9]{64}) [ *](.+)$/.exec(line);need(m,'unsupported original SHA256SUMS line');const path=m[2].replace(/^\.\//,'');need(!entries.has(path),'duplicate original manifest member');entries.set(path,m[1]);}need(entries.size>0,'empty original manifest');return entries;}
/** Parse source without importing/executing it. Local imports must have actual
 * byte-checked closure members; nonliteral dynamic imports are not supported. */
function verifyImportClosure(members,manifest,external){
 const code=String.raw`import ast,json,sys,pathlib
x=json.load(sys.stdin)
names={pathlib.PurePosixPath(p).stem for p in x['manifest'] if p.endswith('.py')}
provided={pathlib.PurePosixPath(p['path']).stem for p in x['files']}
for f in x['files']:
 tree=ast.parse(f['source'],filename=f['path'])
 modules=[]
 for n in ast.walk(tree):
  if isinstance(n,ast.Import): modules.extend(a.name.split('.')[0] for a in n.names)
  elif isinstance(n,ast.ImportFrom):
   if n.module: modules.append(n.module.split('.')[0])
   elif n.level: modules.extend(a.name for a in n.names)
  elif isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='__import__':
   assert n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str),'Nonliteral dynamic import'
   modules.append(n.args[0].value.split('.')[0])
  elif isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('import_module','spec_from_file_location'):
   raise AssertionError('Dynamic importlib source loading requires separate support')
 for m in modules:
  if m in names: assert m in provided,'Missing original local imported module '+m
  else: assert m in sys.stdlib_module_names or m in ('bpy','bmesh','mathutils') or (m=='numpy' and m in x['external']),'Unsupported external module '+m
print('PASS')`;
 const files=members.filter(p=>p.original_path.endsWith('.py')).map(p=>({path:p.original_path,source:Buffer.from(p.data).toString('utf8')}));
 equal(execFileSync('python3',['-c',code],{input:JSON.stringify({manifest:[...manifest.keys()],files,external:external||[]}),encoding:'utf8',maxBuffer:1024*1024}).trim(),'PASS','original import closure');
}
function docPin(doc){return {...pin(doc.pin),original_path_sha256:hash(doc.original_path)};}
/** No source manifest is invented: original six source roles must be members of
 * original SHA256SUMS. A new dependency inventory is explicitly derived evidence. */
export function compileStatic4Compatibility(input){
 const {asset_id:id,revision,documents,roles,role_data,scientific_limits:limits,representation_mapping:mapping}=input;
 need(documents?.acceptance&&documents.brief&&documents.references&&documents.candidate,'original documents missing');exact(roles,SOURCE_ROLES,'seven release roles');exact(role_data,SOURCE_ROLES,'seven actual role bytes');
 const docs={};for(const [k,v]of Object.entries(documents)){need(text(v.original_path),'original document path missing');docs[k]=parsePinnedDocument(v.bytes,v.pin);assertProductionMaterial(docs[k]);}
 const reviewManifest=input.review_manifest;need(text(reviewManifest?.original_path),'original QA manifest path missing');const reviewEntries=parseManifest(checked(reviewManifest.bytes,reviewManifest.pin));equal(reviewEntries.get(documents.acceptance.review_manifest_path),documents.acceptance.pin.sha256,'original report not in original QA seal');
 const sourceManifest=input.source_manifest;need(text(sourceManifest?.original_path),'original manifest path missing');const entries=parseManifest(checked(sourceManifest.bytes,sourceManifest.pin));
 for(const role of SOURCE_ROLES){const p=roles[role];pin(p);need(text(p.original_path)||(role==='dependency-list'&&text(p.path)),'role path missing');checked(role_data[role],p);if(role!=='dependency-list'){need(text(p.manifest_path),'original member path missing');equal(entries.get(p.manifest_path),p.sha256,'source not in original manifest '+role);}}
 for(const role of ['brief','references'])equal(pin(roles[role]),pin(documents[role].pin),'source doc binding '+role);
 for(const key of new Set(['candidate',input.maker_document||'candidate'])){need(documents[key]&&text(documents[key].source_manifest_path),'original maker/candidate source path required');equal(entries.get(documents[key].source_manifest_path),documents[key].pin.sha256,'maker/candidate not in original source seal');}
 equal(docs.candidate.asset_id,id,'candidate asset mismatch');equal(docs.candidate.revision,revision,'candidate revision mismatch');
 const makerDocument=input.maker_document||'candidate',makerPointer=input.maker_pointer||'/maker';need(docs[makerDocument],'original maker document missing');const maker=value(docs[makerDocument],makerPointer);
 // Native proof is an original pinned independent evidence document, not maker QA.
 let nativeProof;if(input.native_proof){const p=input.native_proof;need(docs[p.document],'native evidence document missing');equal(reviewEntries.get(documents[p.document].review_manifest_path),documents[p.document].pin.sha256,'native proof outside original QA seal');equal(value(docs[p.document],p.glb_pointer),roles.finalGLB.sha256,'native proof wrong final GLB');const contract=NATIVE_PROOFS[matchProfile(docs.acceptance).profile];need(contract,'unsupported independent native proof');equal(p.pointer,contract.native,'native pointer changed');equal(p.glb_pointer,contract.glb,'native GLB pointer changed');const checks=Object.fromEntries(Object.keys(contract.checks).map(k=>[k,value(docs[p.document],'/'+k)]));equal(checks,contract.checks,'native comparison failed');if(contract.native==='/native_source_sha256')equal(docs[p.document].native_reexport_sha256,roles.finalGLB.sha256,'native reexport hash changed');const direct=(docs.acceptance.evidence||[]).filter(e=>e&&typeof e==='object'&&e.path===documents[p.document].review_manifest_path);for(const ref of direct)equal(ref.sha256,documents[p.document].pin.sha256,'native proof differs from original report evidence');nativeProof={checks,document_sha256:documents[p.document].pin.sha256,pointer:p.pointer,value:value(docs[p.document],p.pointer)};need(Array.isArray(input.independent_evidence)&&input.independent_evidence.some(x=>x.document===p.document),'native proof not independent evidence');}
 const decision=mapStatic4Decision(docs.acceptance,{asset_id:id,revision,glb_sha256:roles.finalGLB.sha256,native_sha256:roles.finalBlend.sha256,maker,candidate:docs.candidate,native_proof:nativeProof});
 // Bind every disclosed CURRENT subject role, not just final geometry. Missing
 // declarations stay missing; source-seal membership supplies separate provenance.
 for(const role of ORIGINAL_ROLES){
  const aliases={brief:['brief_sha256'],references:['references_sha256'],config:['config_sha256','configuration_sha256'],generator:['generator_sha256'],finalGLB:['glb_sha256','exact_glb_sha256'],finalBlend:['source_sha256','blend_sha256','source_blend_sha256','native_sha256']}[role];
  for(const key of aliases)if(docs.acceptance.subject?.[key]!==undefined)equal(docs.acceptance.subject[key],roles[role].sha256,'independent subject role mismatch '+role);
  for(const key of [role,roles[role].manifest_path]){const declared=docs.acceptance.subject?.[key];if(declared!==undefined){const original=typeof declared==='object'?declared.sha256:declared;need(digest(original),'unknown current subject role layout '+role);equal(original,roles[role].sha256,'independent subject role mismatch '+role);}}
 }
 const independentEvidence=(input.independent_evidence||[]).map(b=>{need(docs[b.document],'independent evidence missing');equal(reviewEntries.get(documents[b.document].review_manifest_path),documents[b.document].pin.sha256,'independent evidence outside original QA seal');need(text(b.pointer),'evidence pointer missing');return {document_sha256:documents[b.document].pin.sha256,pointer_sha256:hash(b.pointer),value_sha256:hash(value(docs[b.document],b.pointer))};});
 need(independentEvidence.length>0,'original technical evidence pins required');
 const history=(input.inheritance||[]).map(h=>{need(docs[h.document]&&docs[h.delta_document],'historical QA/delta evidence missing');const old=docs[h.document],delta=docs[h.delta_document],contract=STATIC4_HISTORY_CONTRACTS[decision.profile];need(contract,'unsupported historical inheritance');for(const k of ['glb_pointer','morphology_pointer','prior_glb_pointer','current_glb_pointer'])equal(h[k],contract[k],'history pointer changed '+k);exact(old,contract.old_fields,'historical report schema');exact(delta,contract.delta_fields,'delta evidence schema');for(const [p,digest]of Object.entries(contract.original_checks))equal(hash(value(old,p)),digest,'historical morphology/current failure changed '+p);for(const [p,digest]of Object.entries(contract.delta_checks))equal(hash(value(delta,p)),digest,'delta invariant failed '+p);equal(reviewEntries.get(documents[h.delta_document].review_manifest_path),documents[h.delta_document].pin.sha256,'delta proof outside original QA seal');equal(old.asset_id,id,'prior review asset mismatch');need(text(old.revision)&&old.revision!==revision,'prior revision mismatch');equal(value(old,h.glb_pointer),value(delta,h.prior_glb_pointer),'delta prior GLB differs');equal(value(delta,h.current_glb_pointer),roles.finalGLB.sha256,'delta current GLB differs');need(digest(value(old,h.glb_pointer)),'prior GLB hash missing');const morphology=value(old,h.morphology_pointer);need(morphology!==undefined,'prior morphology missing');return {document:docPin(documents[h.document]),delta_document:docPin(documents[h.delta_document]),prior_revision:old.revision,prior_glb_sha256:value(old,h.glb_pointer),current_glb_sha256:roles.finalGLB.sha256,morphology_pointer_sha256:hash(h.morphology_pointer),morphology_value_sha256:hash(morphology),prior_report_fields_sha256:hash(old),delta_fields_sha256:hash(delta)};});
 need(!decision.origin_delta||history.length>0,'origin-only evidence lacks prior morphology/delta closure');
 const briefHashPath=['/subject/brief_sha256','/subject/brief/sha256','/subject/brief.json'].find(p=>pointerValue(docs.acceptance,p)===roles.brief.sha256);
 const briefBinding=briefHashPath?{report_binds_original_brief:true,report_revision:revision,report_sha256:documents.acceptance.pin.sha256,source_pointer_sha256:hash(briefHashPath)}:null;
 if(docs.brief.revision!==revision)need(['scoped-review-1','four-view-repair-scoped-review'].includes(decision.profile),'source schema has no inherited brief contract');
 const brief=mapStatic4Brief(docs.brief,docs.references,id,revision,mapping,briefBinding);
 const dep=JSON.parse(checked(role_data['dependency-list'],roles['dependency-list']));equal(dep.kind,'integration-derived-source-dependency-inventory-v1','dependency inventory must be explicitly derived');equal(dep.asset_id,id,'dependency asset');equal(dep.revision,revision,'dependency revision');
 equal(dep.generator_sha256,roles.generator.sha256,'dependency generator');equal(dep.configuration_sha256,roles.config.sha256,'dependency config');equal(dep.model_sha256,roles.finalGLB.sha256,'dependency GLB');equal(dep.native_source_sha256,roles.finalBlend.sha256,'dependency native');
 need(Array.isArray(dep.closure)&&dep.closure.length,'dependency import closure missing');need(new Set(dep.closure.map(p=>p.path)).size===dep.closure.length,'duplicate dependency member');
 const dependencyMembers=input.dependency_members;need(Array.isArray(dependencyMembers)&&dependencyMembers.length===dep.closure.length,'dependency original member mapping missing');
 for(const p of dependencyMembers){pin(p);need(text(p.original_path),'dependency source path');equal(entries.get(p.original_path),p.sha256,'dependency absent from original manifest');checked(p.data,p);need(dep.closure.some(b=>b.path===p.path&&b.sha256===p.sha256&&b.bytes===p.bytes),'dependency published pin mismatch');}
 verifyImportClosure(dependencyMembers,entries,dep.external_modules);
 need(dependencyMembers.some(p=>p.sha256===roles.generator.sha256),'entrypoint missing from dependency closure');equal(dep.requires_independent_projection_review,true,'dependency review waived');equal(dep.publication_authority,false,'dependency authority');
 for(const lang of ['en','zh'])need(text(limits?.[lang]),'scientific limits missing');
 const receipt={schema_version:1,kind:STATIC4_RECEIPT,asset_id:id,revision,original_acceptance_sha256:documents.acceptance.pin.sha256,original_document_pins:Object.fromEntries(Object.entries(documents).map(([k,d])=>[k,docPin(d)])),original_manifest:docPin(sourceManifest),original_review_manifest:docPin(reviewManifest),private_derivation_sha256:hash({asset_id:id,revision,documents:Object.fromEntries(Object.entries(documents).map(([k,d])=>[k,docPin(d)])),roles,decision,history,brief,scientific_limits:limits}),brief,decision,inheritance:history,independent_evidence:independentEvidence,scientific_limits:copy(limits),source_roles:Object.fromEntries(SOURCE_ROLES.map(r=>[r,{...pin(roles[r]),original_path_sha256:hash(roles[r].original_path??roles[r].path),provenance:r==='dependency-list'?'DERIVED_IMPORT_CLOSURE_INVENTORY':'ORIGINAL_SHA256SUMS_MEMBER',source_document_sha256:r==='dependency-list'?roles[r].sha256:sourceManifest.pin.sha256}])),dependency_files:dependencyMembers.map(p=>({...pin(p),original_path_sha256:hash(p.original_path)})),status:'COMPATIBLE_PENDING_FRESH_INDEPENDENT_PROJECTION_REVIEW',production_acceptance_created:false,legacy_records_mutated:false,publication_authorized:false,ci_scope:'BOUNDED_STATIC4_BINDING_ONLY_FRESH_CAPTURE_AND_FULL_CURRENT_CI_REQUIRED'};
 publicOnly(receipt);return receipt;
}
export function validateStatic4Receipt(receipt,record,asset,brief,references){
 for(const x of [receipt,record,asset])assertProductionMaterial(x);publicOnly(receipt);
 exact(receipt,['schema_version','kind','asset_id','revision','original_acceptance_sha256','original_document_pins','original_manifest','original_review_manifest','private_derivation_sha256','brief','decision','inheritance','independent_evidence','scientific_limits','source_roles','dependency_files','status','production_acceptance_created','legacy_records_mutated','publication_authorized','ci_scope'],'receipt fields');
 equal(receipt.schema_version,1,'receipt version');equal(receipt.kind,STATIC4_RECEIPT,'receipt schema');equal(asset.production_acceptance_adapter,STATIC4_ADAPTER,'explicit adapter required');equal(receipt.asset_id,asset.id,'asset identity');equal(record.asset_id,asset.id,'record identity');equal(receipt.revision,asset.revision,'asset revision');equal(record.revision,asset.revision,'record revision');
 equal(receipt.original_acceptance_sha256,record.original_acceptance?.sha256,'original acceptance changed');need(digest(receipt.private_derivation_sha256),'missing private derivation');
 for(const required of ['acceptance','brief','references','candidate'])need(receipt.original_document_pins[required],'document missing '+required);
 for(const p of [...Object.values(receipt.original_document_pins),receipt.original_manifest,receipt.original_review_manifest]){exact(p,['sha256','bytes','original_path_sha256'],'original doc pin fields');pin(p);need(digest(p.original_path_sha256),'original document path binding');}
 equal(receipt.original_document_pins.acceptance.sha256,receipt.original_acceptance_sha256,'acceptance document pin');
 equal(receipt.status,'COMPATIBLE_PENDING_FRESH_INDEPENDENT_PROJECTION_REVIEW','status promoted');for(const k of ['production_acceptance_created','legacy_records_mutated','publication_authorized'])equal(receipt[k],false,'authority/history promoted');equal(receipt.ci_scope,'BOUNDED_STATIC4_BINDING_ONLY_FRESH_CAPTURE_AND_FULL_CURRENT_CI_REQUIRED','current CI waived');
 validateDecision(receipt.decision);const d=receipt.decision;
 equal(receipt.brief,mapStatic4Brief(brief,references,asset.id,asset.revision,receipt.brief.representation_mapping,receipt.brief.brief_revision_binding),'brief mapping changed');equal(asset.representation,receipt.brief.representation_mapping.representation,'representation changed');equal(asset.reconstruction_type,receipt.brief.representation_mapping.reconstruction_type,'reconstruction changed');
 if(receipt.brief.inherited_brief){need(['scoped-review-1','four-view-repair-scoped-review'].includes(d.profile),'brief inheritance profile changed');}if(receipt.brief.inherited_brief)equal(receipt.brief.brief_revision_binding.report_sha256,receipt.original_acceptance_sha256,'brief inheritance report');
 equal(receipt.scientific_limits,record.scientific_limits,'scientific limits changed');
 exact(receipt.source_roles,SOURCE_ROLES,'source role set');equal(record.source_role_derivations??{}, {},'static4 source must stay exact');
 for(const r of SOURCE_ROLES){const p=receipt.source_roles[r];exact(p,['sha256','bytes','original_path_sha256','provenance','source_document_sha256'],'source role fields');pin(p);need(digest(p.original_path_sha256),'source path binding');equal(p.sha256,record.subject[r],'source subject '+r);equal(pin(p),pin(record.roles[r]),'source pin '+r);equal(p.provenance,r==='dependency-list'?'DERIVED_IMPORT_CLOSURE_INVENTORY':'ORIGINAL_SHA256SUMS_MEMBER','source provenance '+r);equal(p.source_document_sha256,r==='dependency-list'?p.sha256:receipt.original_manifest.sha256,'source authority '+r);}
 for(const r of ['brief','references'])equal(pin(receipt.original_document_pins[r]),pin(receipt.source_roles[r]),'original brief/reference pin');equal(d.glb_sha256,record.roles.finalGLB.sha256,'final GLB changed');equal(d.native_sha256,record.roles.finalBlend.sha256,'native changed');
 const originalDocs=new Set(Object.values(receipt.original_document_pins).map(p=>p.sha256));need(Array.isArray(receipt.independent_evidence)&&receipt.independent_evidence.length,'independent evidence missing');for(const b of receipt.independent_evidence){exact(b,['document_sha256','pointer_sha256','value_sha256'],'evidence fields');need(originalDocs.has(b.document_sha256)&&digest(b.pointer_sha256)&&digest(b.value_sha256),'unbound evidence');}
 if(d.independent_native_proof)need(receipt.independent_evidence.some(b=>['document_sha256','pointer_sha256','value_sha256'].every(k=>b[k]===d.independent_native_proof[k])),'native evidence omitted');
 need(Array.isArray(receipt.inheritance)&&(!d.origin_delta||receipt.inheritance.length>0),'origin delta missing inheritance');for(const h of receipt.inheritance){const contract=STATIC4_HISTORY_CONTRACTS[d.profile];need(contract,'unsupported inheritance');equal(h.morphology_pointer_sha256,hash(contract.morphology_pointer),'morphology pointer changed');equal(h.morphology_value_sha256,contract.morphology_value_sha256,'historical morphology changed');need(originalDocs.has(h.document.sha256)&&originalDocs.has(h.delta_document.sha256),'inheritance documents missing');equal(h.current_glb_sha256,d.glb_sha256,'inheritance final GLB');need(text(h.prior_revision)&&h.prior_revision!==asset.revision&&digest(h.prior_glb_sha256)&&h.prior_glb_sha256!==h.current_glb_sha256,'wrong prior revision');for(const k of ['morphology_pointer_sha256','morphology_value_sha256','prior_report_fields_sha256','delta_fields_sha256'])need(digest(h[k]),'inheritance binding missing');}
 need(Array.isArray(receipt.dependency_files)&&receipt.dependency_files.length,'dependency closure absent');need(new Set(receipt.dependency_files.map(p=>p.original_path_sha256)).size===receipt.dependency_files.length,'duplicate dependency');for(const p of receipt.dependency_files){pin(p);need(digest(p.original_path_sha256),'dependency path hash');need(record.build_closure?.some(b=>b.sha256===p.sha256&&b.bytes===p.bytes),'dependency closure not published');}
 return receipt.brief.frozen_budget;
}
export function verifyStatic4Review(receipt,record,asset,brief,references,review){
 const budget=validateStatic4Receipt(receipt,record,asset,brief,references);assertProductionMaterial(review);
 equal(review.kind,'independent-static4-split-source-projection-review-v1','fresh independent source projection review required');equal(review.status,'PASS','projection review failed');equal(review.asset_id,asset.id,'review asset mismatch');
 const reviewerIdentity=actor(review.reviewer),preparerIdentity=actor(record.maker);need(reviewerIdentity!==preparerIdentity,'producer self-review');need(hash(reviewerIdentity)!==receipt.decision.maker_task_sha256,'original maker self-review');
 equal(review.original_acceptance_sha256,receipt.original_acceptance_sha256,'review original report mismatch');equal(review.private_derivation_sha256,receipt.private_derivation_sha256,'review derivation mismatch');equal(review.compatibility_sha256,hash(receipt),'stale projection review');
 exact(review.checks,STATIC4_REVIEW_CHECKS,'review checks');for(const k of STATIC4_REVIEW_CHECKS)equal(review.checks[k],'PASS','review check '+k);
 equal(review.original_document_pins_sha256,hash(receipt.original_document_pins),'review document binding');equal(review.original_checklists_sha256,hash(receipt.decision.checklists),'review original checklist binding');equal(review.inheritance_sha256,hash(receipt.inheritance),'review inheritance binding');equal(review.dependency_files_sha256,hash(receipt.dependency_files),'review dependency binding');equal(review.blocking_findings,[],'review blockers');equal(review.publication_authorized,false,'review publication authority');return budget;
}
export function verifyStatic4SourceAvailability(record,receipt,roleBytes){
 const s=record.source_availability;equal(s?.kind,'static4-exact-source-and-derived-dependencies-v1','explicit source provenance required');equal(s.original_acceptance_sha256,receipt.original_acceptance_sha256,'source acceptance pin');exact(s.roles,SOURCE_ROLES,'source availability role set');
 for(const r of SOURCE_ROLES){equal(s.roles[r],receipt.source_roles[r],'source provenance '+r);checked(roleBytes[r],record.roles[r]);}
 const dep=JSON.parse(roleBytes['dependency-list']);equal(dep.kind,'integration-derived-source-dependency-inventory-v1','derived dependency schema');equal(dep.generator_sha256,record.roles.generator.sha256,'dependency entrypoint');equal(dep.configuration_sha256,record.roles.config.sha256,'dependency config');equal(dep.model_sha256,record.roles.finalGLB.sha256,'dependency model');equal(dep.native_source_sha256,record.roles.finalBlend.sha256,'dependency native');
 for(const p of dep.closure){need(record.build_closure.some(b=>b.path===p.path&&b.sha256===p.sha256&&b.bytes===p.bytes),'dependency closure member changed');}
 equal(dep.requires_independent_projection_review,true,'dependency review waived');equal(dep.publication_authority,false,'dependency approval promoted');
 return {status:'EXACT_SOURCE_BYTES_AVAILABLE',original_six_roles:true,dependency_inventory:'EXPLICITLY_DERIVED_NOT_ORIGINAL',publication_authorized:false};
}
export const validateStatic4Measurements=validateV2Measurements;
export function preserveStatic4Runtime(record,receipt){const state=preserveUnverifiedRuntimeStatus(record.postReleaseVerified);return {...state,original_static4_scope:receipt.decision.claim,original_report_sha256:receipt.original_acceptance_sha256};}

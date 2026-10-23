/** Explicit model-task-v2 projection. This does not rewrite source QA or fabricate
 * the legacy criteria/stages contract. Private originals need a fresh independent
 * projection review; public CI checks only the compact, hash-bound projection. */
import assert from 'node:assert/strict';
import {SOURCE_ROLES, INVENTORY_TYPES, sha256, parsePinnedDocument, pointerValue,
  assertProductionMaterial, preserveUnverifiedRuntimeStatus} from './inventory-type-acceptance.mjs';

const hash = x => sha256(Buffer.from(JSON.stringify(x)));
const clone = x => structuredClone(x);
export const normalizeV2Identity = x => x.trim().toLowerCase().replace(/^\/root\//,'');
const text = x => typeof x === 'string' && Boolean(x.trim());
const digest = x => typeof x === 'string' && /^[a-f0-9]{64}$/.test(x);
const need = (ok, why) => assert(ok, 'HOLD: v2 '+why);
const equal = (a,b,why) => assert.deepEqual(a,b,'HOLD: v2 '+why);
const exact = (x,keys,label) => equal(Object.keys(x||{}).sort(),keys.slice().sort(),'unknown/missing '+label+' fields');
const publicOnly = x => need(!/\/workspace\/|\/home\/|\/tmp\/|\/root\/|drive\.google\.com|docs\.google\.com/.test(JSON.stringify(x)), 'private locator in public receipt');
const pair = p => {need(p&&digest(p.sha256)&&Number.isSafeInteger(p.bytes)&&p.bytes>0,'exact document pin required');return {sha256:p.sha256,bytes:p.bytes};};
const runtimeKeys = ['gpu','scene','user','deployed'];
// Observed literal declarations only. None is reinterpreted as legacy gate PASS.
export const V2_TECHNICAL_DECLARATIONS = Object.freeze([
'PASS','PASS_LOCAL_GEOMETRY_FORMAT_REBUILD','PASS_LOCAL_GEOMETRY_FORMAT_REBUILD_LANDMARKS',
'PASS_SCOPED_SOURCE_GLB_KHRONOS_TWO_REBUILDS_TARGETED_GEOMETRY_PARSE_AND_INDEPENDENT_BINARY_CHECK',
'PASS_TECHNICAL','PASS_DECLARED_STATIC_SOURCE_FORMAT_GEOMETRY_REBUILD_SCOPE',
'PASS_TECHNICAL_AND_INDEPENDENT_REVIEW_SCOPE','PASS_WITH_REVIEWED_SOURCE_SMOOTH_SHADING_WARNING',
'PASS_LOCAL','PASS_SOURCE_GLB_KHRONOS_TWO_REBUILDS_THREEJS_PARSE','PASS_LOCAL_STATIC_AND_REBUILD',
'PASS_TECHNICAL_REVIEWED','PASS_TECHNICAL_SCOPE_ONLY','PASS_IN_SCOPE',
'PASS_WITH_DOCUMENTED_MIXED_NORMAL_WARNING','PASS_STATIC_FORMAT_REBUILD','PASS_SCOPED',
'PASS_SCOPED_MAKER_TECHNICAL','PASS_TECHNICAL_ONLY','PASS_WITH_SCOPED_UNRUN_GATES',
'PASS_WITH_EXPLICIT_SCOPE','PASS_WITH_SCOPE_LIMITS','PASS_BOUNDED_TECHNICAL','PASS_TECHNICAL_SCOPE',
'PASS_LOCAL_TECHNICAL_SCOPE','PASS_REUSED_SAME_BYTE_TECHNICAL_EVIDENCE','PASS_WITH_SCOPE',
'PASS_SCOPED_TECHNICAL','PASS_STATIC_TECHNICAL_AND_INDEPENDENT_VISUAL'
]);
const MAKING_DECLARATIONS=['COMPLETE','PASS','PASS_INDEPENDENT_PRODUCTION_CANDIDATE_QA','PASS_INDEPENDENT_QA','COMPLETE_MAKER','PASS_MAKER_SCOPE'];
// Exact observed wording-to-type map. Unknown scientific wording requires review and
// an explicit adapter update, never regex guesses or a model/species whitelist.
export const V2_REPRESENTATION_LITERALS = Object.freeze({
  "Preserve original genus-level fossil-form target: long tapering tower, numerous rounded tightly stacked whorls, and a real rounded basal aperture.": "fossil-specimen",
  "fossil-specimen": "fossil-specimen",
  "living-reconstruction": "living-reconstruction",
  "Original fossil-shell target retained: inflated smooth oval cowrie, anterior extension of the aperture as a short channel, and long toothed ventral slit. Not a living animal and not a generic unbroken oval pebble.": "fossil-specimen",
  "Original genus fossil-form target retained: broad cap shell with offset spiral summit and internal shelf. Add the directly observed strong radial ribs, not a featureless conical limpet.": "fossil-specimen",
  "fossil-specimen interpretation": "fossil-specimen",
  "whole-organism": "living-reconstruction",
  "Original fossil-form target retained: stout vase-shaped shell, strong shoulder projections and open flaring mouth. Species-informed Hystrivasum squamosum, not generic conch or another Vasum genus.": "fossil-specimen",
  "3D fossil skull study": "fossil-specimen",
  "original low-poly fossil-form reconstruction, composite evidence": "fossil-specimen",
  "original low-poly fossil-shell interpretation": "fossil-specimen",
  "original low-poly fossil interpretation": "fossil-specimen",
  "material-level interpretive fossil-shell reconstruction, not specimen facsimile": "fossil-specimen",
  "interpretive fossil shell, not an exact specimen facsimile": "fossil-specimen",
  "Conservative fossil-shell interpretation, not exact undamaged facsimile": "fossil-specimen",
  "Conservative whole-animal living reconstruction, not fossil slab or exact soft-tissue scan": "living-reconstruction",
  "fossil-specimen: internal mould of conjoined shell, not restored hollow living shell": "fossil-specimen",
  "Conservative whole living fish restoration, not a fossil slab and not an exact soft-tissue scan": "living-reconstruction",
  "Conservative complete living fish restoration, not fossil slab or exact individual scan": "living-reconstruction",
  "fossil-specimen, documented compressed lectotype-informed interpretation; includes explicitly disclosed historical plaster repair, not a pristine living shell": "fossil-specimen",
  "fossil-study": "fossil-specimen",
  "fossil-specimen, holotype-informed low-poly interpretation; unseen thickness inferred explicitly": "fossil-specimen",
  "geological-form": "geological-form",
  "trace-concept": "trace-concept"
});
export const V2_REVIEW_CHECKS = Object.freeze([
  'original_documents_and_membership','source_role_mapping','original_review_independence',
  'maker_identity_and_provenance','scientific_and_freeze_requirements',
  'production_gates_and_qualifications','legacy_failure_history_preserved',
  'private_to_public_mapping_no_gate_loss','representation_and_scope_mapping',
  'original_technical_visual_factual_specification_parse_evidence',
  'runtime_and_user_acceptance_not_promoted'
]);


// Only current authority fields are mapped. Prior/original decision objects and
// their REVISE history are preserved by the original document hash, not overwritten.
const CURRENT_PASS_FIELDS=['production_verdict','production_qa','independent_qa',
 'independent_acceptance','final_production_decision','qa','independent_visual',
 'independent_factual','independent_specification','visual','factual','specification'];
const CURRENT_EMPTY_FIELDS=['blocking_findings','blocking_issues','required_repairs',
 'critical_findings','mandatory_repairs','blockers','minimum_required_repairs',
 'required_revisions','remaining_issues'];
const FINAL_MAKING_VALUES=['PASS','PASS_BOUNDED_FOSSIL_STUDY',
 'PASS: complete living reconstruction accepted as a local fixed candidate.'];
const REVIEWER_VERDICTS=['PASS','PASS: KEL-01 independently verified closed; production candidate accepted',
 'R1 resolved by visibly interrupted right shell lip and shallow mineral-bearing fracture edge, with retained upper/left flare and body.'];
const TEST_DETAILS={source_geometry:'PASS',source_export_bounds:'PASS',official_khronos:'PASS_0_ERRORS_0_WARNINGS',
 threejs_0_180_0_parsing:'PASS',two_isolated_rebuilds:'PASS_BYTE_AND_SEMANTIC_IDENTICAL',
 blend_reopen:'PASS_NO_EXTERNAL_DEPENDENCIES',exact_glb_views:'PASS_INDEPENDENTLY_INSPECTED',dependency_inventory:'PASS'};
const CURRENT_CHECKS={source_glb:'PASS',khronos:'PASS_0_ERRORS_0_WARNINGS',
 isolated_two_rebuilds:'PASS_BYTE_AND_SEMANTIC_IDENTICAL',saved_source_geometry:'PASS_DIAGNOSTIC_SCOPE',
 threejs_parse:'PASS_PARSE_ONLY',independent_visual:'PASS',independent_factual:'PASS',
 independent_specification:'PASS',independent_hash_and_source_closure:'PASS',independent_decoded_glb:'PASS'};
export function mapV2CurrentRequirements(doc) {
 const result={};
 const record=(path,value)=>{result[path]=clone(value);};
 for(const [prefix,section]of [['',doc],['/reviewer',doc.reviewer||{}]]){
  for(const k of CURRENT_PASS_FIELDS)if(section[k]!==undefined){equal(section[k],'PASS','conflicting current '+prefix+'/'+k);record(prefix+'/'+k,section[k]);}
  for(const k of CURRENT_EMPTY_FIELDS)if(section[k]!==undefined){equal(section[k],[],'unresolved current '+prefix+'/'+k);record(prefix+'/'+k,section[k]);}
  if(section.accepted_for_brief!==undefined){equal(section.accepted_for_brief,true,'current brief acceptance false');record(prefix+'/accepted_for_brief',true);}
 }
 if(doc.final_making_decision!==undefined){need(FINAL_MAKING_VALUES.includes(doc.final_making_decision),'conflicting final maker decision');record('/final_making_decision',doc.final_making_decision);}
 if(doc.reviewer?.verdict!==undefined){need(REVIEWER_VERDICTS.includes(doc.reviewer.verdict),'conflicting current reviewer verdict');record('/reviewer/verdict',doc.reviewer.verdict);}
 if(doc.independent_review!==undefined){
  if(typeof doc.independent_review==='string')equal(doc.independent_review,'PASS','conflicting independent_review');
  else equal(doc.independent_review,{visual:'PASS',factual_boundaries:'PASS',specification:'PASS',hash_and_dependency_inventory:'PASS',technical_evidence:'REUSED_SAME_BYTES',blocking_issues:[]},'unsupported/nonpassing structured independent_review');
  record('/independent_review',doc.independent_review);
 }
 for(const key of ['revision_requests','resolved_issues','issues'])if(doc[key]!==undefined){
  need(Array.isArray(doc[key]),'invalid current '+key);
  const states=doc[key].map(issue=>{
   need(text(issue.id),'issue identity missing');
   const status=key==='issues'?issue.reviewer_status:issue.status;
   need((key==='issues'?['CLOSED']:['CLOSED_BY_INDEPENDENT_QA','RESOLVED_INDEPENDENTLY_VERIFIED','CLOSED_INDEPENDENTLY_VERIFIED']).includes(status),'current issue is not independently closed');
   return {id:issue.id,...(key==='issues'?{reviewer_status:status}:{status})};
  });
  record('/'+key,states);
 }
 if(doc.repair!==undefined){equal(doc.repair.independent_status,'RESOLVED','repair not independently resolved');record('/repair',{independent_status:'RESOLVED'});}
 if(doc.checks!==undefined){equal(doc.checks,CURRENT_CHECKS,'conflicting current checks');record('/checks',doc.checks);}
 if(doc.tests_detail!==undefined){equal(doc.tests_detail,TEST_DETAILS,'conflicting technical detail');record('/tests_detail',doc.tests_detail);}
 for(const key of ['technical','technical_summary'])if(doc[key]!==undefined){
  for(const field of ['source_errors','static_glb_errors','khronos_errors','khronos_warnings'])if(doc[key][field]!==undefined){equal(doc[key][field],0,'current technical error/warning');record('/'+key+'/'+field,0);}
  if(doc[key].rebuilds!==undefined){equal(doc[key].rebuilds,2,'missing original dual rebuild');record('/'+key+'/rebuilds',2);}
 }
 return result;
}
function validateV2CurrentRequirements(mapped) {
 need(mapped&&typeof mapped==='object'&&!Array.isArray(mapped),'missing current decision requirements');
 const restored={};
 for(const [pointer,value] of Object.entries(mapped)){
  need(/^\/[a-z_]+(?:\/[a-z_]+)*$/.test(pointer),'unsafe current requirement pointer');
  const parts=pointer.slice(1).split('/');let cursor=restored;
  for(const key of parts){need(!['__proto__','prototype','constructor'].includes(key),'unsafe current requirement field');}
  for(const key of parts.slice(0,-1))cursor=cursor[key]??={};
  cursor[parts.at(-1)]=clone(value);
 }
 equal(mapV2CurrentRequirements(restored),mapped,'current decision requirements changed');
}

/** No substring/PASS-prefix heuristic and no species whitelist. These are the
 * observed top-level layouts, with literal decision values. Unknown layouts HOLD. */
export function mapV2Decision(doc,id,revision) {
  equal(doc.asset_id,id,'decision asset mismatch');equal(doc.revision,revision,'decision revision mismatch');
  if(doc.template_version!==undefined)equal(doc.template_version,'model-task-v2','decision template mismatch');
  need(doc.schema===undefined&&doc.kind===undefined&&doc.schema_version===undefined,'ambiguous decision schema');
  need(MAKING_DECLARATIONS.includes(doc.making),'maker not complete');
  need(text(doc.tests),'missing original technical-scope declaration');
  // Preserve the exact technical declaration. It is not interpreted as five PASSes.
  need(V2_TECHNICAL_DECLARATIONS.includes(doc.tests),'unsupported/nonpassing technical declaration');
  equal(doc.maker?.role,'maker','maker role missing');equal(doc.reviewer?.role,'independent-QA','independent reviewer role missing');
  need(text(doc.maker.task)&&text(doc.reviewer.task),'maker/reviewer task missing');
  const identity = normalizeV2Identity;
  need(identity(doc.maker.task)!==identity(doc.reviewer.task),'maker cannot self-review');
  let profile,decisionPath,value;
  if(doc.status!==undefined){profile='status-v2';decisionPath='/status';value=doc.status;need(['PASS','PASS_IN_SCOPE'].includes(value),'nonpassing status');}
  else if(doc.decision!==undefined){profile='decision-v2';decisionPath='/decision';value=doc.decision;equal(value,'PASS','nonpassing decision');}
  else {profile='reviewer-and-making-v2';decisionPath='/reviewer/status';value=doc.reviewer.status;equal(value,'PASS','independent reviewer did not pass');equal(doc.final_making_decision,'PASS','unsupported maker-only layout');}
  if(doc.decision!==undefined)equal(doc.decision,'PASS','conflicting decision');
  if(doc.reviewer.status!==undefined)need(['PASS','PASS_IN_SCOPE','COMPLETE'].includes(doc.reviewer.status),'nonpassing reviewer status');
  if(value==='PASS_IN_SCOPE')equal(doc.reviewer.status,'PASS_IN_SCOPE','scoped result disagrees with reviewer');
  for(const key of ['blocking_findings','blocking_issues','required_repairs','critical_findings','mandatory_repairs','blockers']){
    if(doc[key]!==undefined)equal(doc[key],[],'unresolved '+key);
    if(doc.reviewer[key]!==undefined)equal(doc.reviewer[key],[],'unresolved reviewer '+key);
  }
  need(digest(doc.glb_sha256)&&digest(doc.preview_sha256),'missing exact reviewed GLB/preview');
  for(const key of ['reviewed_glb_sha256','glb_sha256'])if(doc.reviewer[key]!==undefined)equal(doc.reviewer[key],doc.glb_sha256,'reviewer GLB differs');
  for(const key of ['reviewed_preview_sha256','preview_sha256'])if(doc.reviewer[key]!==undefined)equal(doc.reviewer[key],doc.preview_sha256,'reviewer preview differs');
  for(const key of runtimeKeys)need(text(doc[key])||(key==='deployed'&&doc[key]===false),'missing original '+key+' state');
  need(Array.isArray(doc.evidence)&&doc.evidence.length>0,'original evidence list missing');
  const scopePointer=['/reviewer/summary','/reviewer/claim_scope','/reviewer/verdict','/reviewer/verdict_scope','/claim_scope'].find(p=>text(pointerValue(doc,p)));
  need(scopePointer,'independent review scope text missing');
  const qualifications={};
  for(const key of ['claim_scope','limitations','unresolved','not_authorized_or_performed'])if(doc[key]!==undefined)qualifications[key]=clone(doc[key]);
  // Full original acceptance remains pinned, including prior_status/original_*.
  return {current_requirements:mapV2CurrentRequirements(doc),current_requirements_sha256:hash(mapV2CurrentRequirements(doc)),profile,decision_pointer:decisionPath,decision_value:value,tests:doc.tests,
    reviewer_status:doc.reviewer.status??null,review_scope_pointer:scopePointer,review_scope_sha256:hash(pointerValue(doc,scopePointer)),maker_task_sha256:hash(identity(doc.maker.task)),
    reviewer_task_sha256:hash(identity(doc.reviewer.task)),glb_sha256:doc.glb_sha256,
    preview_sha256:doc.preview_sha256,runtime: Object.fromEntries(runtimeKeys.map(k=>[k,doc[k]])),
    qualifications_sha256:hash(qualifications),evidence_sha256:hash(doc.evidence),
    evidence_count:doc.evidence.length,original_fields_sha256:hash(doc),
    claim:'ORIGINAL_INDEPENDENT_LOCAL_SCOPE_ONLY_NOT_LEGACY_GATE_EQUIVALENCE'};
}

/** Free-text representation is never guessed. An explicit source pointer and
 * exact value preserve the original statement; the canonical mapping additionally
 * requires independent representation_and_scope_mapping review. */
export function mapV2Brief(brief,references,id,mapping) {
  equal(brief.template_version,'model-task-v2','unsupported brief template');equal(brief.asset_id,id,'brief identity mismatch');
  need(text(brief.revision),'brief revision missing');
  exact(mapping,['source_pointer','original_value_sha256','representation','reconstruction_type'],'representation mapping');
  need(['/representation','/target','/subject/representation'].includes(mapping.source_pointer),'unsupported representation pointer');
  const original=pointerValue(brief,mapping.source_pointer);need(text(original),'missing original representation statement');
  equal(hash(original),mapping.original_value_sha256,'original representation changed');
  need(INVENTORY_TYPES.includes(mapping.representation),'unsupported representation');
  need(Object.hasOwn(V2_REPRESENTATION_LITERALS,original),'unrecognized representation statement');
  equal(mapping.representation,V2_REPRESENTATION_LITERALS[original],'original representation relabeled');
  const reconstruction={'living-reconstruction':'whole-organism','fossil-specimen':'specimen','geological-form':'artistic-concept','trace-concept':'artistic-concept'}[mapping.representation];
  equal(mapping.reconstruction_type,reconstruction,'representation/reconstruction conflict');
  const budget=brief.geometry_policy;need(budget&&typeof budget==='object','missing frozen geometry budget');
  for(const key of ['max_triangles','max_materials','max_primitives','max_glb_bytes'])need(Number.isSafeInteger(budget[key])&&budget[key]>0,'invalid '+key);
  // Original science is preserved as source bytes, not translated into invented criteria.
  need(Object.keys(brief).some(k=>['scope','original_scope','target','diagnostic_targets','required_features','morphology','must_preserve','anatomy'].includes(k)),'missing original scientific scope');
  const sources=references.sources??references.references;
  need(Array.isArray(sources)&&sources.length>0,'missing reference sources');
  return {kind:'model-task-v2-brief-map-v1',asset_id:id,revision:brief.revision,
    representation_mapping:clone(mapping),original_brief_semantic_sha256:hash(brief),
    original_references_semantic_sha256:hash(references),frozen_budget:clone(budget),
    original_criteria_created:false,release_texture_policy:'NO_TEXTURES_SUPPORTED_BY_THIS_ADAPTER',
    publication_authorized:false};
}

/** Compile private, byte-checked inputs. The final manifest proves source/decision
 * membership, NOT that a maker manifest was independently approved. That separate
 * fact must be checked by the fresh independent reviewer against original evidence. */
export function compileModelTaskV2Compatibility(input) {
  const {asset_id:id,documents,roles,representation_mapping:mapping,scientific_limits:limits}=input;
  exact(documents,['brief','references','manifest','acceptance'],'input documents');
  exact(roles,SOURCE_ROLES,'seven source roles');
  const docs=Object.fromEntries(Object.entries(documents).map(([key,v])=>[key,parsePinnedDocument(v.bytes,v.pin)]));
  for(const doc of Object.values(docs))assertProductionMaterial(doc);
  const {brief,references,manifest,acceptance}=docs;
  equal(manifest.template_version,'model-task-v2','unsupported manifest');equal(manifest.asset_id,id,'manifest asset mismatch');equal(manifest.revision,brief.revision,'manifest revision mismatch');
  const briefMap=mapV2Brief(brief,references,id,mapping),decision=mapV2Decision(acceptance,id,brief.revision);
  for(const role of SOURCE_ROLES){const p=roles[role];pair(p);need(text(p.original_path),'source original path missing');equal(manifest.roles?.[role],p.original_path,'manifest role path mismatch '+role);equal(manifest.files?.[p.original_path],p.sha256,'manifest role hash mismatch '+role);}
  for(const role of ['brief','references'])equal(pair(documents[role].pin),pair(roles[role]),'source document pin mismatch '+role);
  need(text(manifest.roles?.decision),'manifest decision role missing');equal(manifest.files?.[manifest.roles.decision],documents.acceptance.pin.sha256,'decision not in final manifest');
  equal(decision.glb_sha256,roles.finalGLB.sha256,'independent decision GLB mismatch');
  need(text(manifest.roles?.preview),'manifest preview role missing');equal(manifest.files?.[manifest.roles.preview],decision.preview_sha256,'independent preview mismatch');
  for(const item of acceptance.evidence){const path=typeof item==='string'?item:item?.path;need(text(path)&&digest(manifest.files?.[path]),'decision evidence missing from manifest');if(typeof item==='object')equal(item.sha256,manifest.files[path],'decision evidence hash mismatch');}
  for(const lang of ['en','zh'])need(text(limits?.[lang]),'bilingual scientific limits missing');
  const privateDerivation={asset_id:id,documents:Object.fromEntries(Object.entries(documents).map(([k,v])=>[k,pair(v.pin)])),roles:clone(roles),brief:briefMap,decision,scientific_limits:clone(limits)};
  const receipt={schema_version:1,kind:'compact-model-task-v2-compatibility-v1',asset_id:id,revision:brief.revision,
    original_acceptance_sha256:documents.acceptance.pin.sha256,original_document_pins:privateDerivation.documents,
    private_derivation_sha256:hash(privateDerivation),brief:briefMap,decision,scientific_limits:clone(limits),
    original_evidence_pins:acceptance.evidence.map(item=>{const path=typeof item==='string'?item:item.path;return {path_sha256:hash(path),sha256:manifest.files[path]};}),
    source_roles:Object.fromEntries(SOURCE_ROLES.map(role=>[role,{...pair(roles[role]),original_path_sha256:hash(roles[role].original_path),source_document_sha256:documents.manifest.pin.sha256}])),
    status:'COMPATIBLE_PENDING_FRESH_INDEPENDENT_PROJECTION_REVIEW',production_acceptance_created:false,
    legacy_records_mutated:false,publication_authorized:false,
    ci_scope:'PUBLIC_COMPACT_STATIC_BINDING_ONLY_PRIVATE_ORIGINALS_REQUIRE_INDEPENDENT_REVIEW'};
  publicOnly(receipt);return receipt;
}

export function validateModelTaskV2Receipt(receipt,record,asset,brief,references) {
  for(const x of [receipt,record,asset])assertProductionMaterial(x);publicOnly(receipt);
  exact(receipt,['schema_version','kind','asset_id','revision','original_acceptance_sha256','original_document_pins','private_derivation_sha256','brief','decision','scientific_limits','original_evidence_pins','source_roles','status','production_acceptance_created','legacy_records_mutated','publication_authorized','ci_scope'],'receipt');
  equal(receipt.kind,'compact-model-task-v2-compatibility-v1','unsupported compact receipt');equal(receipt.schema_version,1,'unsupported version');
  equal(receipt.asset_id,asset.id,'receipt asset mismatch');equal(record.asset_id,asset.id,'record asset mismatch');equal(receipt.revision,asset.revision,'revision mismatch');
  equal(asset.production_acceptance_adapter,'model-task-v2','explicit adapter required');
  equal(receipt.brief,mapV2Brief(brief,references,asset.id,receipt.brief.representation_mapping),'original science mapping changed');
  equal(asset.representation,receipt.brief.representation_mapping.representation,'representation changed');equal(asset.reconstruction_type,receipt.brief.representation_mapping.reconstruction_type,'scope changed');
  equal(receipt.original_acceptance_sha256,record.original_acceptance?.sha256,'acceptance pin changed');need(digest(receipt.private_derivation_sha256),'missing private derivation pin');
  exact(receipt.original_document_pins,['brief','references','manifest','acceptance'],'document pins');for(const p of Object.values(receipt.original_document_pins)){exact(p,['sha256','bytes'],'document pin');pair(p);}
  equal(receipt.original_document_pins.acceptance.sha256,receipt.original_acceptance_sha256,'acceptance membership changed');
  equal(receipt.status,'COMPATIBLE_PENDING_FRESH_INDEPENDENT_PROJECTION_REVIEW','receipt promotion');for(const k of ['production_acceptance_created','legacy_records_mutated','publication_authorized'])equal(receipt[k],false,'authority/history changed');
  equal(receipt.ci_scope,'PUBLIC_COMPACT_STATIC_BINDING_ONLY_PRIVATE_ORIGINALS_REQUIRE_INDEPENDENT_REVIEW','scope changed');
  equal(receipt.scientific_limits,record.scientific_limits,'scientific limits changed');
  const d=receipt.decision;
  exact(d,['current_requirements','current_requirements_sha256','profile','decision_pointer','decision_value','tests','reviewer_status','review_scope_pointer','review_scope_sha256','maker_task_sha256','reviewer_task_sha256','glb_sha256','preview_sha256','runtime','qualifications_sha256','evidence_sha256','evidence_count','original_fields_sha256','claim'],'decision projection');
  validateV2CurrentRequirements(d.current_requirements);
  equal(hash(d.current_requirements),d.current_requirements_sha256,'current requirement coverage changed');
  const profiles={'status-v2':['/status',['PASS','PASS_IN_SCOPE']],'decision-v2':['/decision',['PASS']],'reviewer-and-making-v2':['/reviewer/status',['PASS']]};
  need(Object.hasOwn(profiles,d.profile),'unknown decision profile');equal(d.decision_pointer,profiles[d.profile][0],'decision source changed');need(profiles[d.profile][1].includes(d.decision_value),'nonpassing decision');
  need([null,'PASS','PASS_IN_SCOPE','COMPLETE'].includes(d.reviewer_status),'nonpassing reviewer');if(d.profile==='reviewer-and-making-v2')equal(d.reviewer_status,'PASS','maker-only approval');if(d.decision_value==='PASS_IN_SCOPE')equal(d.reviewer_status,'PASS_IN_SCOPE','scope mismatch');
  need(['/reviewer/summary','/reviewer/claim_scope','/reviewer/verdict','/reviewer/verdict_scope','/claim_scope'].includes(d.review_scope_pointer),'unsupported review scope pointer');
  for(const k of ['review_scope_sha256','maker_task_sha256','reviewer_task_sha256','glb_sha256','preview_sha256','qualifications_sha256','evidence_sha256','original_fields_sha256'])need(digest(d[k]),'decision '+k+' missing');need(d.maker_task_sha256!==d.reviewer_task_sha256,'self review');
  equal(d.claim,'ORIGINAL_INDEPENDENT_LOCAL_SCOPE_ONLY_NOT_LEGACY_GATE_EQUIVALENCE','acceptance promotion');need(V2_TECHNICAL_DECLARATIONS.includes(d.tests),'invalid tests declaration');need(Number.isSafeInteger(d.evidence_count)&&d.evidence_count>0,'no evidence');
  exact(d.runtime,runtimeKeys,'runtime');for(const k of runtimeKeys)need(text(d.runtime[k])||(k==='deployed'&&d.runtime[k]===false),'runtime missing');
  need(Array.isArray(receipt.original_evidence_pins)&&receipt.original_evidence_pins.length===d.evidence_count,'missing original evidence pins');
  for(const p of receipt.original_evidence_pins){exact(p,['path_sha256','sha256'],'evidence pin');need(digest(p.path_sha256)&&digest(p.sha256),'invalid evidence pin');}
  need(new Set(receipt.original_evidence_pins.map(p=>p.path_sha256)).size===receipt.original_evidence_pins.length,'duplicate evidence pin');
  exact(receipt.source_roles,SOURCE_ROLES,'source role set');
  for(const role of SOURCE_ROLES){const p=receipt.source_roles[role];exact(p,['sha256','bytes','original_path_sha256','source_document_sha256'],'source role');pair(p);need(digest(p.original_path_sha256),'source path hash missing');equal(p.source_document_sha256,receipt.original_document_pins.manifest.sha256,'source manifest changed');equal(p.sha256,record.subject[role],'subject changed '+role);equal(pair(p),pair(record.roles[role]),'published role changed '+role);}
  for(const role of ['brief','references'])equal(receipt.original_document_pins[role],pair(record.roles[role]),'document role changed '+role);
  equal(d.glb_sha256,record.roles.finalGLB.sha256,'reviewed GLB changed');
  equal(record.source_role_derivations??{}, {}, 'v2 source derivations require separate explicit support');
  return receipt.brief.frozen_budget;
}

export function verifyModelTaskV2Review(receipt,record,asset,brief,references,review) {
  const budget=validateModelTaskV2Receipt(receipt,record,asset,brief,references);assertProductionMaterial(review);
  equal(review.kind,'independent-model-task-v2-compatibility-review-v1','fresh v2 independent review required');equal(review.status,'PASS','independent review not passing');
  for(const k of ['id','task_id']){need(text(review.reviewer?.[k])&&text(record.maker?.[k]),'review identity missing');need(normalizeV2Identity(review.reviewer[k])!==normalizeV2Identity(record.maker[k]),'maker reviewed projection');}
  need(hash(normalizeV2Identity(review.reviewer.task_id))!==receipt.decision.maker_task_sha256,'original maker reviewed own projection');
  equal(review.original_acceptance_sha256,receipt.original_acceptance_sha256,'review acceptance changed');equal(review.private_derivation_sha256,receipt.private_derivation_sha256,'private derivation review changed');equal(review.compatibility_sha256,hash(receipt),'stale v2 review');
  for(const k of V2_REVIEW_CHECKS)equal(review.checks?.[k],'PASS','missing review check '+k);
  exact(review.evidence_bindings,['source_reproducibility','format_geometry','cpu_parse','independent_visual_factual_specification'],'review evidence bindings');
  const originalEvidence=new Set(receipt.original_evidence_pins.map(p=>p.sha256));
  for(const [scope,bindings] of Object.entries(review.evidence_bindings)){
    need(Array.isArray(bindings)&&bindings.length>0,'missing original evidence binding '+scope);
    for(const b of bindings){exact(b,['document_sha256','source_pointer','original_value_sha256'],'review evidence binding');need(digest(b.original_value_sha256)&&text(b.source_pointer)&&b.source_pointer.startsWith('/'),'missing bound evidence field');
      need(originalEvidence.has(b.document_sha256)||(scope==='independent_visual_factual_specification'&&b.document_sha256===receipt.original_acceptance_sha256),'evidence not in original acceptance/manifest');
    }
  }
  need(review.evidence_bindings.independent_visual_factual_specification.some(b=>b.document_sha256===receipt.original_acceptance_sha256&&b.source_pointer===receipt.decision.review_scope_pointer&&b.original_value_sha256===receipt.decision.review_scope_sha256),'original independent scope text not bound');
  equal(review.blocking_findings,[],'review blockers');equal(review.publication_authorized,false,'review cannot grant publication');return budget;
}

export function validateV2Measurements(native,asset,record,receipt) {
  const budget=receipt.brief.frozen_budget;equal(native.errors,[],'native GLB errors');
  for(const [name,max]of [['scene_triangles','max_triangles'],['materials','max_materials'],['scene_primitives_estimated_base_draw_calls','max_primitives'],['bytes','max_glb_bytes']])need(Number.isSafeInteger(native[name])&&native[name]>=0&&native[name]<=budget[max],'native budget '+name);
  equal(native.scene_triangles,asset.triangles,'native triangles changed');equal(asset.triangles,record.measurements.triangles,'record triangles changed');equal(native.bounds_m?.size,asset.dimensions,'native bounds changed');equal(asset.dimensions,record.measurements.dimensions,'record dimensions changed');
  equal(native.textures,0,'textured v2 models unsupported');equal(native.texture_images,0,'embedded image v2 models unsupported');return native;
}

/** Never turn unknown GPU/scene into PASS, even if metadata claims PASS. Known
 * failure is retained rather than erased. Other releases' runtime policy is unchanged. */
export function preserveV2Runtime(record,receipt) {
  const state=preserveUnverifiedRuntimeStatus(record.postReleaseVerified);
  if(['FAIL','REVISE','BLOCKED'].some(v=>[receipt.decision.runtime.gpu,receipt.decision.runtime.scene].includes(v)))return {...state,status:'FAIL',original_runtime:clone(receipt.decision.runtime)};
  return {...state,original_runtime:clone(receipt.decision.runtime)};
}

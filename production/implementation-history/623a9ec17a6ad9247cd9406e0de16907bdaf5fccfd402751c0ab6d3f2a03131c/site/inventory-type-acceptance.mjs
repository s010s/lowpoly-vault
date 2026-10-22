/** Bounded, additive inventory compatibility. This maps evidence; it does not create approval.
 * Raw source documents remain immutable. Original FAIL/approved=false and runtime unknowns
 * are not rewritten. A fresh independent projection review is still required to publish.
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

export const SOURCE_ROLES = Object.freeze(['brief','config','references','generator','dependency-list','finalGLB','finalBlend']);
export const INVENTORY_TYPES = Object.freeze(['living-reconstruction','fossil-specimen','geological-form','trace-concept']);
const PRODUCTION_STAGES = ['technical','visual','factual','specification','runtime_parse'];
const RUNTIME_STAGES = ['gpu','scene'];
export const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const digest = x => typeof x === 'string' && /^[a-f0-9]{64}$/.test(x);
const nonempty = x => typeof x === 'string' && Boolean(x.trim());
const object = x => x && typeof x === 'object' && !Array.isArray(x);
const at = (x,p) => p.split('.').reduce((v,k)=>v?.[k],x);
export const pointerValue = (x,p) => {
  need(typeof p==='string'&&p.startsWith('/'),'invalid source JSON pointer');
  return p.slice(1).split('/').map(k=>k.replace(/~1/g,'/').replace(/~0/g,'~')).reduce((v,k)=>v?.[k],x);
};
const clone = x => structuredClone(x);
/** Production boundary: test-only documents/identities cannot grant a real release. */
export function assertProductionMaterial(value) {
  if(typeof value==='string')need(!/test[ _-]*fixture/i.test(value),'test fixture identity/material cannot enter production');
  if(!value||typeof value!=='object')return;
  need(value.fixture_only!==true,'fixture_only material cannot enter production');
  for(const child of Object.values(value))assertProductionMaterial(child);
}
// END_PRODUCTION_MATERIAL_BOUNDARY
const need = (ok,why) => assert(ok,`HOLD: ${why}`);
const equal = (actual,expected,why) => assert.deepEqual(actual,expected,`HOLD: ${why}`);
const field = (out,doc,p) => { need(at(doc,p)!==undefined,`missing original field ${p}`); out[p]=clone(at(doc,p)); return at(doc,p); };

/** Byte checks are mandatory before parsing original acceptance or source evidence. */
export function parsePinnedDocument(bytes,pin) {
  need(Buffer.isBuffer(bytes)||bytes instanceof Uint8Array,'document bytes required');
  need(pin && digest(pin.sha256) && Number.isSafeInteger(pin.bytes) && pin.bytes>0,'exact document pin required');
  equal(bytes.length,pin.bytes,'document byte count changed');
  equal(sha256(bytes),pin.sha256,'document hash changed');
  const result=JSON.parse(Buffer.from(bytes).toString('utf8'));
  need(object(result)||Array.isArray(result),'document must be JSON object/manifest array');
  return result;
}

/** Two existing brief layouts, one shared contract. No species/ID whitelist. */
export function mapFrozenInventoryBrief(brief,references,assetId) {
  equal(brief.schema_version,1,'unsupported frozen brief schema');
  equal(brief.asset_id,assetId,'brief identity mismatch');
  equal(references.asset_id,assetId,'reference identity mismatch');
  equal(references.schema_version,1,'unsupported reference schema');
  const structured=object(brief.subject), representation=structured?brief.subject.representation:brief.representation;
  need(INVENTORY_TYPES.includes(representation),'unsupported inventory representation');
  const scienceFields={};
  for (const path of structured?['subject','claim_scope','distinctness','modeling_brief','reference_policy','scale','artistic_choices']:['subject','factual_scope','identifying_features','scale','prohibited']) {
    const value=field(scienceFields,brief,path);
    need(nonempty(value)||(Array.isArray(value)&&value.length>0)||(object(value)&&Object.keys(value).length>0),`empty scientific field ${path}`);
  }
  if(structured) {
    need(nonempty(brief.reference_policy.minimum_reference)&&nonempty(brief.reference_policy.reference_rights),'missing scientific/source requirement');
    need(nonempty(brief.claim_scope),'missing original claim scope');
    for(const key of ['distinctness','modeling_brief'])for(const lang of ['en','zh'])need(nonempty(brief[key]?.[lang]),'missing original scientific description '+key+'.'+lang);
    need(Number.isFinite(brief.scale.meters)&&brief.scale.meters>0&&nonempty(brief.scale.axis)&&nonempty(brief.scale.kind),'missing original scale/scope qualifier');
    need(Array.isArray(brief.artistic_choices)&&brief.artistic_choices.every(nonempty),'missing original artistic qualifications');
    const expected={
      'living-reconstruction':['taxon_inspiration','whole-organism'],
      'fossil-specimen':['taxon_inspiration','specimen'],
      'geological-form':['process_inspiration','artistic-concept'],
      'trace-concept':['process_inspiration','artistic-concept']
    }[representation];
    need(nonempty(brief.subject[expected[0]]),'missing original type-specific subject');
    equal(brief.subject.reconstruction_type,expected[1],'representation/reconstruction mismatch');
    if(representation==='trace-concept') need(nonempty(brief.subject.trace_display),'missing original trace convention');
  } else {
    // Only the observed reconstruction layout is supported. Other layouts need an explicit mapping.
    equal(representation,'living-reconstruction','unsupported scalar-subject brief layout');
    need(nonempty(brief.frozen_at),'missing original freeze timestamp');
    field(scienceFields,brief,'frozen_at');
    need(nonempty(brief.subject)&&nonempty(brief.factual_scope),'missing original reconstruction subject/scope');
    for(const key of ['identifying_features','prohibited'])need(Array.isArray(brief[key])&&brief[key].every(nonempty),'missing original reconstruction scientific requirements '+key);
    equal(brief.scale.units,'meters','unsupported original reconstruction scale units');
    need(nonempty(brief.scale.accuracy),'missing original reconstruction scale qualifier');
    const dimensions=brief.scale.nominal_art_dimensions_blender_xyz_m||brief.scale.art_target_bounds_blender_xyz_m;
    need(Array.isArray(dimensions)&&dimensions.length===3&&dimensions.every(v=>Number.isFinite(v)&&v>0),'missing original reconstruction scale dimensions');
  }
  const budget=brief.geometry_policy;
  need(object(budget),'missing original frozen geometry policy');
  for(const key of ['max_triangles','max_materials','max_primitives','max_glb_bytes']) need(Number.isSafeInteger(budget[key])&&budget[key]>0,`missing frozen ${key}`);
  need(object(brief.texture_policy),'missing original texture policy');
  for(const key of ['max_textures','max_dimension','max_total_bytes','max_decoded_bytes']) need(Number.isSafeInteger(brief.texture_policy[key])&&brief.texture_policy[key]>=0,`missing frozen texture ${key}`);
  equal(brief.publication_authority,'separate','production evidence cannot grant publication');
  need(Array.isArray(brief.required_stages),'missing original stages');
  equal([...brief.required_stages].sort(),[...PRODUCTION_STAGES,...RUNTIME_STAGES].sort(),'unsupported frozen stage set');
  need(Array.isArray(brief.criteria)&&brief.criteria.length>0,'missing frozen acceptance criteria');
  const ids=new Set();
  for(const criterion of brief.criteria) {
    need(nonempty(criterion.id)&&!ids.has(criterion.id),'duplicate/missing frozen criterion'); ids.add(criterion.id);
    need([...PRODUCTION_STAGES,...RUNTIME_STAGES].includes(criterion.stage),'unsupported original criterion stage');
    need(criterion.critical===true&&nonempty(criterion.description)&&Array.isArray(criterion.required_sources),'incomplete frozen criterion');
  }
  for(const stage of brief.required_stages) need(brief.criteria.some(c=>c.stage===stage),'missing original critical stage '+stage);
  need(brief.criteria.filter(c=>c.stage==='factual').some(c=>c.required_sources.length>0),'missing mandatory factual source requirement');
  need(Array.isArray(brief.required_views)&&brief.required_views.length>0&&new Set(brief.required_views).size===brief.required_views.length,'missing original frozen view requirements');
  need(Array.isArray(references.sources)&&references.sources.length>0,'missing source ledger');
  const sourceIds=new Set();
  for(const source of references.sources) {
    need(nonempty(source.id)&&!sourceIds.has(source.id),'duplicate/missing source identity');sourceIds.add(source.id);
    need(nonempty(source.title)&&nonempty(source.url)&&/^https?:\/\//.test(source.url),'missing/unsupported source title or URL');
    // Consulted-only is not a copying license. Unclear incorporation never becomes permission.
    if(source.incorporated===true) need(nonempty(source.license)&&source.license!=='consulted-only','incorporated media lacks real license');
    need(source.incorporated===false&&source.use==='consulted-only','incorporated/unknown source-media rights mapping not supported');
  }
  const requiredSources=[...new Set(brief.criteria.flatMap(c=>c.required_sources))].sort();
  for(const id of requiredSources) need(sourceIds.has(id),'missing mandatory scientific source '+id);
  return {kind:'derived-inventory-brief-map-v1',derived:true,asset_id:assetId,representation,
    source_layout:structured?'structured-subject-v1':'scalar-subject-reconstruction-v1',
    source_field_map:scienceFields,frozen_budget:clone(budget),frozen_texture_policy:clone(brief.texture_policy),
    original_criteria:clone(brief.criteria),required_source_ids:requiredSources,
    original_required_views:clone(brief.required_views),
    original_required_stages:clone(brief.required_stages),production_stages:PRODUCTION_STAGES.slice(),
    deferred_runtime_stages:RUNTIME_STAGES.slice(),publication_authorized:false};
}

const CORE_CRITERIA=['technical-integrity','normal-view-craft','basic-form-and-scope','deliverables-and-label','target-loader'];
const SOURCE_LINEAGE_CRITERIA=['exact-subject-and-source-lineage','technical-integrity-and-budget','closed-volumes-and-contact','basic-form-and-scientific-scope','normal-view-craft','canonical-cover','editable-source-and-reproducibility','delivery-label-and-provenance'];
const gateContracts=new WeakMap();
function criteria(out,doc,path,required,allowedExtras={}) {
  gateContracts.get(out)?.push({path,kind:'criteria',allowed:Object.fromEntries([...required.map(id=>[id,['PASS','pass']]),...Object.entries(allowedExtras)])});
  const list=field(out,doc,path);need(Array.isArray(list),'missing independent criteria');
  equal(list.map(c=>c.id).sort(),[...required,...Object.keys(allowedExtras)].sort(),'unsupported/missing independent criterion');
  for(const c of list) {
    const expected=allowedExtras[c.id]||['PASS','pass']; need(expected.includes(c.status),'nonpassing independent criterion '+c.id);
    need(Array.isArray(c.evidence)&&c.evidence.length>0,'independent criterion has no evidence '+c.id);
  }
}
function gates(out,doc,path,expected) {
  gateContracts.get(out)?.push({path,kind:'gates',allowed:clone(expected)});
  const found=field(out,doc,path);need(object(found),'missing independent gates');
  equal(Object.keys(found).sort(),Object.keys(expected).sort(),'unsupported/missing independent gate');
  for(const [key,allowed] of Object.entries(expected))need((Array.isArray(allowed)?allowed:[allowed]).includes(found[key]),'nonpassing/unknown independent gate '+key);
}
function checks(out,doc,expected) {for(const [p,v] of Object.entries(expected)){gateContracts.get(out)?.push({path:p,kind:'equal',expected:clone(v)});equal(field(out,doc,p),v,'independent requirement failed '+p);}}
function subjectHashes(doc) {
  const direct=doc.seven_roles||doc.identity?.seven_roles;
  if(direct)return Object.fromEntries(SOURCE_ROLES.map(r=>[r,direct[r]?.sha256]));
  const s=doc.subject||{};
  return {finalGLB:doc.final_glb?.sha256||doc.identity?.final_glb_sha256||s.glb_sha256||s.final_glb_sha256,
    finalBlend:doc.final_blend?.sha256||doc.identity?.final_blend_sha256||s.source_blend_sha256||s.final_blend_sha256,
    brief:doc.frozen_brief?.sha256||s.brief_sha256,config:s.config_sha256,references:s.references_sha256,generator:s.generator_sha256};
}

/** Exact observed schema shapes and exact status literals, never startsWith('PASS').
 * Additional JSON evidence is byte-bound by the caller and fresh projection review.
 */
export function mapIndependentProductionAcceptance(doc,assetId) {
  need(object(doc),'missing original independent acceptance');
  need(!(doc.schema!==undefined&&doc.kind!==undefined),'unsupported ambiguous original acceptance schema');
  if(doc.schema!==undefined)need(['independent-production-acceptance-v1','layered-independent-production-acceptance-v1'].includes(doc.schema),'unsupported original independent acceptance schema');
  if(doc.schema_version!==undefined)equal(doc.schema_version,1,'unsupported original independent acceptance version');
  if(doc.productionAccepted!==undefined)need([true,'PASS'].includes(doc.productionAccepted),'explicit nonpassing production acceptance');
  if(doc.productionAcceptance!==undefined)equal(doc.productionAcceptance,'PASS','explicit nonpassing production acceptance');
  if(doc.verdict!==undefined)equal(doc.verdict,'PASS','explicit nonpassing original verdict');
  if(doc.decision!==undefined)need(['PASS','PASS_PRODUCTION_DIFFERENTIAL_QA'].includes(doc.decision),'explicit nonpassing original decision');
  const fields={},contract=[], isSchema=doc.schema==='independent-production-acceptance-v1';gateContracts.set(fields,contract);let profile;
  if(doc.asset_id!==undefined)field(fields,doc,'asset_id');
  const actualId=doc.asset_id||doc.subject?.asset_id||doc.subject?.asset_ids?.[0]||doc.identity?.asset_ids?.[0];
  equal(actualId,assetId,'independent acceptance identity mismatch');
  if(doc.subject?.asset_ids)equal(doc.subject.asset_ids,[assetId],'multi-asset subject ambiguity');
  if(doc.identity?.asset_ids)equal(doc.identity.asset_ids,[assetId],'multi-asset identity ambiguity');
  if(isSchema && object(doc.production_gates)) {
    profile='named-gates-original-source-v1';
    checks(fields,doc,{'productionAcceptance':'PASS','mandatory_repairs':[], 'source_and_rebuild.two_fresh_clean_rebuilds':'PASS','source_and_rebuild.both_byte_match_original':true,'source_and_rebuild.actual_blend_reexport':'PASS','source_and_rebuild.reexport_byte_match_original':true,'standard_glb.errors':0,'standard_glb.warnings':0,'science.status':'PASS','visual.status':'PASS','budget.status':'PASS','provenance.required_seven_roles_present':true,'original_history_preserved.approved':false});
    gates(fields,doc,'production_gates',Object.fromEntries(['science','actual_visual_shape','geometry_and_budget','standard_glb','source_and_clean_rebuild','provenance_and_delivery'].map(k=>[k,'PASS'])));
    for(const p of ['science','reviewer','final_glb','final_blend','frozen_brief','original_history_preserved','postReleaseVerified','releaseChecks'])field(fields,doc,p);
    need(nonempty(doc.reviewer),'missing independent reviewer declaration');
  } else if(doc.kind==='additive-first-independent-per-model-production-acceptance'&&doc.schema_version===1) {
    profile='criteria-exact-subject-v1';checks(fields,doc,{'productionAccepted':true,'scope.minimum_required_repairs':[],'compatibility.fresh_profile_valid':true,'compatibility.fresh_profile_contract_status':'pass','compatibility.historical_approved_for_brief':false});
    criteria(fields,doc,'production_criteria',CORE_CRITERIA);
    for(const p of ['subject','reviewer','reproducibility_limits','compatibility','postReleaseVerified','releaseChecks'])field(fields,doc,p);
    need(nonempty(doc.reviewer.id)&&nonempty(doc.reviewer.task)&&nonempty(doc.reviewer.independent_of_maker),'missing independent reviewer identity');
  } else if(isSchema && object(doc.identity) && Array.isArray(doc.criteria)) {
    profile='criteria-seven-role-identity-v1';checks(fields,doc,{'productionAccepted':true,'productionVerdict':'PASS','required_repairs':[],'reproducibility.status':'PASS','historical_preservation.old_approved_false_unchanged':true,'historical_preservation.input_tree_unchanged':true});
    criteria(fields,doc,'criteria',CORE_CRITERIA,{'functional-render':['PASS_CPU_ONLY'],'representative-scene':['PASS_DECLARED_NEUTRAL_CPU_SCENE']});
    for(const p of ['identity','review_kind','scope','reproducibility','historical_preservation','postrelease'])field(fields,doc,p);
  } else if(isSchema && Array.isArray(doc.criteria) && doc.verdict!==undefined) {
    profile='criteria-source-lineage-v1';checks(fields,doc,{'productionAccepted':'PASS','verdict':'PASS','critical_findings':[],'required_repairs':[],'workflow.legacy_approved':false,'workflow.production_acceptance_is_additive_only':true});
    criteria(fields,doc,'criteria',SOURCE_LINEAGE_CRITERIA);
    for(const p of ['reviewer_role','final_glb','final_blend','maker_handoff_sha256','reference_verification','workflow','limitations'])field(fields,doc,p);
  } else if(doc.schema==='layered-independent-production-acceptance-v1') {
    profile='layered-qualified-gates-v1';checks(fields,doc,{'productionAccepted':true,'verdict':'PASS','required_repairs':[],'approved':false,'legacy_approved_preserved':false});
    gates(fields,doc,'production_gate_results',{technical_integrity:'PASS',normal_view_craft:'PASS_WITH_EXPLICIT_NONBLOCKING_PRESENTATION_QUALIFICATIONS',basic_form_and_scope:'PASS_WITH_ARTISTIC_INFERENCE_LABELS',deliverables_and_label:'PASS',target_loader:'PASS',functional_render:'PASS_CYCLES_CPU_EVIDENCE_INSPECTED',representative_scene:'PASS_16_COPIES_43520_TRIANGLES'});
    for(const p of ['subject','reviewer','qualifications','evidence','fresh_independent_checks','historical_freezes_failures','postrelease_browser'])field(fields,doc,p);
    need(doc.qualifications.length>0&&doc.evidence.length>0,'missing qualified science/source evidence');
  } else if(doc.schema===undefined&&doc.kind===undefined&&doc.schema_version===1&&object(doc.seven_stages)) {
    profile='differential-detached-subject-v1';checks(fields,doc,{'decision':'PASS_PRODUCTION_DIFFERENTIAL_QA','production_layer_independently_accepted':true,'all_production_gates_pass':true,'candidate_unchanged':true,'blockers':[],'full_seven_stage_formal_acceptance':false});
    gates(fields,doc,'seven_stages',{technical:'PASS',visual:'PASS',factual_frozen_feature_and_unchanged_prior_source_scope:'PASS_WITH_STATED_PRIOR_SOURCE_LIMITS',specification:'PASS',runtime_parse:'PASS',gpu:'NOT_RUN_SEPARATE_RELEASE_OR_POSTRELEASE_LAYER',scene:'NOT_RUN_SEPARATE_RELEASE_OR_POSTRELEASE_LAYER'});
    for(const p of ['subject_pins_sha256','reviewer','scope','separate_pending'])field(fields,doc,p);
    need(digest(doc.subject_pins_sha256),'missing detached original subject hash');
  } else if(doc.schema===undefined&&doc.kind===undefined&&doc.schema_version===1&&doc.review_type==='Fresh independent differential production/static acceptance') {
    profile='differential-inline-seven-roles-v1';checks(fields,doc,{'decision':'PASS','productionAccepted':true,'technical_summary.khronos_errors':0,'technical_summary.khronos_warnings':0,'technical_summary.fresh_rebuild_count':2,'technical_summary.fresh_rebuild_and_saved_source_reexport_byte_identical':true,'immutable_evidence.old_fail_preserved':true,'immutable_evidence.all_original_and_candidate_package_paths_sha_sizes_preserved':true});
    gates(fields,doc,'production_stages',{technical:'PASS',visual:'PASS',factual:'PASS_WITHIN_UNCHANGED_GENUS_LEVEL_SCOPE',specification:'PASS_FOR_PRODUCTION_LAYER',runtime_parse:'PASS'});
    for(const p of ['seven_roles','review_type','science_limits','root_pair_contact_adjudication','immutable_evidence','release_and_postrelease','evidence_files'])field(fields,doc,p);
  } else if(doc.schema===undefined&&doc.kind===undefined&&doc.schema_version===undefined&&object(doc.stages)&&doc.subject_pins==='subject-pins.json') {
    profile='independent-detached-stages-v1';checks(fields,doc,{'decision':'PASS','productionAccepted':true,'blocking_issues':[],'integrity.all_candidate_files_unchanged':true,'integrity.all_seven_roles_and_helper_hashes_verified':true,'technical.khronos_errors':0,'technical.khronos_warnings':0,'technical.fresh_rebuild_glb_semantics_source_metrics_exact':true,'technical.saved_blend_reexport_glb_byte_exact':true,'original_failure_preserved.new_result_does_not_modify_old_approved_state':true});
    gates(fields,doc,'stages',{technical:'PASS',visual:'PASS',factual:'PASS_WITH_SCOPE_LIMITS',specification:'PASS',runtime_parse:'PASS',gpu:'NOT_RUN_POST_RELEASE',scene:'NOT_RUN_POST_RELEASE'});
    need(Array.isArray(doc.technical.two_fresh_distinct_pids)&&new Set(doc.technical.two_fresh_distinct_pids).size===2,'missing two independent rebuild runs');
    for(const p of ['subject_pins','reviewer_role','frozen_science_scope','visual_evidence','technical','original_failure_preserved','nonblocking_limits','evidence_files','releaseChecks','postReleaseVerified'])field(fields,doc,p);
  } else need(false,'unsupported original independent acceptance schema/shape');
  const independentDeclaration=doc.reviewer||doc.reviewer_role||doc.review_kind||doc.review_type;
  need(nonempty(independentDeclaration)||object(independentDeclaration),'missing original independent review declaration');
  for(const key of ['blocking_findings','blocking_issues','required_repairs','critical_findings','mandatory_repairs','blockers'])if(doc[key]!==undefined)equal(doc[key],[],'unresolved independent findings '+key);
  return {kind:'derived-original-production-map-v1',derived:true,asset_id:assetId,profile,
    original_schema:doc.schema??doc.kind??null,original_schema_version:doc.schema_version??null,
    original_schema_field:doc.schema!==undefined?'schema':doc.kind!==undefined?'kind':null,
    original_fields:fields,gate_contract:contract,original_reviewer_declaration:clone(independentDeclaration),
    // A declaration is not an invented reviewer account ID. Fresh projection review resolves identity.
    reviewer_account_identity_established:Boolean(object(doc.reviewer)&&nonempty(doc.reviewer.id)&&nonempty(doc.reviewer.task)),
    directly_bound_subject_hashes:Object.fromEntries(Object.entries(subjectHashes(doc)).filter(([,v])=>v!==undefined)),production_layer:'PASS',
    legacy_approval_changed:false,publication_authorized:false};
}

export function revalidateAcceptanceDerivation(mapped,assetId) {
  need(object(mapped?.original_fields),'missing original acceptance field map');
  const source={};
  for(const [path,value] of Object.entries(mapped.original_fields)){
    const parts=path.split('.');let target=source;
    for(const key of parts.slice(0,-1)){need(!['__proto__','constructor','prototype'].includes(key),'unsafe mapped key');target=target[key]??={};}
    const last=parts.at(-1);need(!['__proto__','constructor','prototype'].includes(last),'unsafe mapped key');target[last]=clone(value);
  }
  if(mapped.original_schema_field!==null){need(['schema','kind'].includes(mapped.original_schema_field),'invalid original schema field');source[mapped.original_schema_field]=mapped.original_schema;}
  if(mapped.original_schema_version!==null)source.schema_version=mapped.original_schema_version;
  equal(mapIndependentProductionAcceptance(source,assetId),mapped,'original acceptance derivation changed');
  return source;
}

/** Produce a provenance index only after exact original bytes and seven source roles are verified.
 * roleEvidence entries are JSON-pointer derivations from independently reviewed source documents.
 * A separate original evidence-manifest membership proof must bind every supplemental document.
 */
export function compileInventoryCompatibility(input) {
  const {asset_id:id,roles,documents,role_evidence:bindings}=input;
  need(nonempty(id),'missing asset identity');
  equal(Object.keys(roles||{}).sort(),[...SOURCE_ROLES].sort(),'exact seven source roles required');
  const docs=new Map();
  for(const [key,value] of Object.entries(documents||{})) {
    const parsed=parsePinnedDocument(value.bytes,value.pin);docs.set(key,{parsed,pin:value.pin});
  }
  for(const key of ['brief','references','acceptance'])need(docs.has(key),'missing original '+key+' document');
  for(const role of SOURCE_ROLES)need(digest(roles[role]?.sha256)&&Number.isSafeInteger(roles[role]?.bytes)&&roles[role].bytes>0&&nonempty(roles[role].original_path),'invalid original role '+role);
  for(const role of ['brief','references']){equal(docs.get(role).pin.sha256,roles[role].sha256,'role/document hash mismatch '+role);equal(docs.get(role).pin.bytes,roles[role].bytes,'role/document byte count mismatch '+role);}
  const brief=mapFrozenInventoryBrief(docs.get('brief').parsed,docs.get('references').parsed,id);
  const acceptance=mapIndependentProductionAcceptance(docs.get('acceptance').parsed,id);
  equal(Object.keys(bindings||{}).sort(),[...SOURCE_ROLES].sort(),'missing explicit seven-role source derivation');
  const derivations={};
  for(const role of SOURCE_ROLES) {
    const binding=bindings[role],source=docs.get(binding.document);
    need(source&&nonempty(binding.pointer),'missing independent source-role evidence '+role);
    const value=pointerValue(source.parsed,binding.pointer);
    equal(value,roles[role].sha256,'independent subject hash mismatch '+role);
    if(binding.document!=='acceptance') {
      const membership=binding.membership,manifest=docs.get(membership?.document);
      need(manifest&&nonempty(membership.pointer),'supplemental evidence not bound by independent manifest '+role);
      equal(pointerValue(manifest.parsed,membership.pointer),source.pin.sha256,'stale independent evidence membership '+role);
      // Same original manifest must bind the acceptance, not a maker-only or unrelated manifest.
      need(nonempty(membership.acceptance_pointer),'missing acceptance/manifest link '+role);
      equal(pointerValue(manifest.parsed,membership.acceptance_pointer),docs.get('acceptance').pin.sha256,'unrelated original evidence manifest '+role);
    }
    derivations[role]={source_document_sha256:source.pin.sha256,source_pointer:binding.pointer,sha256:roles[role].sha256,bytes:roles[role].bytes,original_path:roles[role].original_path,
      ...(binding.membership?{membership:clone(binding.membership)}:{})};
    if(acceptance.directly_bound_subject_hashes[role]!==undefined)equal(acceptance.directly_bound_subject_hashes[role],roles[role].sha256,'direct original subject mismatch '+role);
  }
  // When a decision explicitly pins a detached subject, its exact document is required.
  const detached=docs.get('acceptance').parsed.subject_pins_sha256;
  if(detached)need([...docs.values()].some(d=>d.pin.sha256===detached),'missing exact detached subject document');
  return {schema_version:1,kind:'derived-inventory-compatibility-v1',derived:true,asset_id:id,
    representation:brief.representation,original_acceptance_sha256:docs.get('acceptance').pin.sha256,
    original_document_pins:Object.fromEntries([...docs].map(([k,d])=>[k,{sha256:d.pin.sha256,bytes:d.pin.bytes}])),
    brief,acceptance,source_roles:derivations,
    status:'COMPATIBLE_PENDING_FRESH_INDEPENDENT_PROJECTION_REVIEW',
    production_acceptance_created:false,legacy_records_mutated:false,publication_authorized:false,
    postReleaseVerified:'UNCHANGED_SEPARATE_NONBLOCKING_PRODUCTION'};
}

/** Projection-side check. No receipt is a release gate until an independent review binds it. */
export function validateInventoryCompatibilityReceipt(receipt,record,asset,brief,references) {
  for(const value of [receipt,record,asset])assertProductionMaterial(value);
  if(receipt.kind==='compact-inventory-compatibility-v1')return validateCompactReceipt(receipt,record,asset,brief,references);
  equal(receipt.kind,'derived-inventory-compatibility-v1','unsupported compatibility receipt');equal(receipt.schema_version,1,'unsupported receipt version');
  equal(receipt.derived,true,'compatibility is a derivation, not a replacement original');
  equal(receipt.status,'COMPATIBLE_PENDING_FRESH_INDEPENDENT_PROJECTION_REVIEW','unsupported/nonpassing compatibility status');
  equal(receipt.asset_id,asset.id,'receipt asset identity mismatch');equal(record.asset_id,asset.id,'record asset identity mismatch');
  equal(receipt.representation,asset.representation,'asset relabeled');
  equal(receipt.brief,mapFrozenInventoryBrief(brief,references,asset.id),'frozen scientific/source mapping changed');
  equal(receipt.original_acceptance_sha256,record.original_acceptance.sha256,'original proof changed');
  equal(receipt.original_document_pins?.acceptance?.sha256,record.original_acceptance.sha256,'original acceptance document pin changed');
  equal(receipt.acceptance.production_layer,'PASS','nonpassing independent production evidence');
  revalidateAcceptanceDerivation(receipt.acceptance,asset.id);
  equal(receipt.legacy_records_mutated,false,'legacy history rewritten');equal(receipt.production_acceptance_created,false,'derivation cannot create approval');equal(receipt.publication_authorized,false,'derivation cannot authorize publication');
  equal(Object.keys(receipt.source_roles||{}).sort(),[...SOURCE_ROLES].sort(),'receipt seven-role set changed');
  for(const role of SOURCE_ROLES){
    equal(receipt.source_roles?.[role]?.sha256,record.subject[role],'receipt subject mismatch '+role);equal(receipt.source_roles[role].sha256,record.roles[role].sha256,'receipt role mismatch '+role);
    equal(receipt.source_roles[role].bytes,record.roles[role].bytes,'receipt role byte count mismatch '+role);
    need(Object.values(receipt.original_document_pins).some(p=>p.sha256===receipt.source_roles[role].source_document_sha256),'missing original source document pin '+role);
  }
  for(const role of ['brief','references'])equal(receipt.original_document_pins[role],{sha256:record.roles[role].sha256,bytes:record.roles[role].bytes},'original role document pin changed '+role);
  return receipt.brief.frozen_budget;
}

export function verifyInventoryCompatibilityReceipt(receipt,record,asset,brief,references,review) {
  assertProductionMaterial(review);
  const budget=validateInventoryCompatibilityReceipt(receipt,record,asset,brief,references);
  need(review&&review.kind==='independent-inventory-compatibility-review-v1','fresh independent compatibility review required');
  equal(review.status,'PASS','independent compatibility review not passing');
  for(const key of ['id','task_id'])need(nonempty(review.reviewer?.[key])&&nonempty(record.maker?.[key]),'missing reviewer/maker identity');
  need(review.reviewer.id.trim().toLowerCase()!==record.maker.id.trim().toLowerCase()&&review.reviewer.task_id.trim().toLowerCase()!==record.maker.task_id.trim().toLowerCase(),'maker cannot review own projection');
  if(receipt.kind==='compact-inventory-compatibility-v1'){equal(review.checks?.private_to_public_mapping_no_gate_loss,'PASS','private-to-public independent review required');equal(review.private_derivation_sha256,receipt.private_derivation_sha256,'review binds wrong private derivation');}
  equal(review.original_acceptance_sha256,receipt.original_acceptance_sha256,'review binds wrong original');
  equal(review.compatibility_sha256,sha256(Buffer.from(JSON.stringify(receipt))),'stale compatibility review');
  for(const key of ['original_documents_and_membership','source_role_mapping','original_review_independence','maker_identity_and_provenance','scientific_and_freeze_requirements','production_gates_and_qualifications','legacy_failure_history_preserved'])equal(review.checks?.[key],'PASS','missing compatibility review '+key);
  if(Object.keys(record.source_role_derivations||{}).length){for(const key of ['derived_source_fields_nonexecuting','derived_source_semantics_preserved','published_source_rebuild_equivalent'])equal(review.checks?.[key],'PASS','missing derived-source independent review '+key);equal(review.source_role_derivations_sha256,compactHash(record.source_role_derivations),'stale derived-source review');}
  equal(review.blocking_findings,[],'independent review has blockers');equal(review.publication_authorized,false,'review cannot grant publication');
  return budget;
}

/** Source availability is measured, not inferred from private backup completion. */
export function verifyExactLocalSourceAvailability(record,receipt,roleBytes) {
  const source=record.source_availability;
  need(Object.keys(record.source_role_derivations||{}).every(r=>['references','dependency-list'].includes(r)),'unsupported derived source role');
  need(source?.kind==='exact-original-seven-role-local-v1','exact original local-source availability contract required');
  assertProductionMaterial(source);
  equal(source.original_acceptance_sha256,receipt.original_acceptance_sha256,'source availability binds wrong original QA');
  equal(Object.keys(source.roles||{}).sort(),[...SOURCE_ROLES].sort(),'source availability requires exact seven roles');
  for(const role of SOURCE_ROLES){
    const pin=source.roles[role],original=receipt.source_roles[role],bytes=roleBytes[role];
    need(Buffer.isBuffer(bytes)||bytes instanceof Uint8Array,'missing local source bytes '+role);
    if(original.original_path_sha256)equal(pin.original_path_sha256,original.original_path_sha256,'original local-source path hash changed '+role);else equal(pin.original_path,original.original_path,'original local-source path changed '+role);
    equal(pin.sha256,original.sha256,'original local-source hash changed '+role);equal(pin.sha256,record.subject[role],'local-source subject changed '+role);
    equal(pin.bytes,original.bytes,'original local-source size changed '+role);
    if(record.source_role_derivations?.[role])validateDerivedSourceRole(record.source_role_derivations[role],role,bytes,receipt,record);
    else {equal(bytes.length,pin.bytes,'local source bytes changed '+role);equal(sha256(bytes),pin.sha256,'local source hash changed '+role);}
    if(pin.git!==undefined){
      need(object(pin.git)&&/^[a-f0-9]{40}$/.test(pin.git.commit)&&/^[a-f0-9]{40}$/.test(pin.git.blob_sha1),'invalid original Git citation '+role);
      if(original.original_path_sha256)equal(compactHash(pin.git.path),original.original_path_sha256,'Git citation path differs from original '+role);else equal(pin.git.path,pin.original_path,'Git citation path differs from original '+role);
      need(nonempty(pin.git.url)&&pin.git.url.startsWith('https://')&&pin.git.url.endsWith('/blob/'+pin.git.commit+'/'+pin.git.path),'Git citation URL changed '+role);
      const actual=createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
      if(!record.source_role_derivations?.[role])equal(actual,pin.git.blob_sha1,'Git blob bytes changed '+role);
      else need(digest(record.source_role_derivations[role].original.sha256),'Original Git source separately bound by independent derivation review');
    }
  }
  // Current bytes + the original independent subject mapping prove local availability.
  // Optional Git citations retain historical identity; commit membership is reviewed separately.
  return {status:Object.keys(record.source_role_derivations||{}).length?'VERIFIED_LOCAL_SOURCE_WITH_DECLARED_DERIVATIONS':'VERIFIED_EXACT_LOCAL_SOURCE',original_acceptance_sha256:receipt.original_acceptance_sha256,source_role_count:7,backup_coverage:clone(record.source_archive??null),cleanup_eligible:false};
}

/** This production adapter does not perform or certify post-release runtime tests. */
export function preserveUnverifiedRuntimeStatus(reported) {
  need(object(reported)&&['UNKNOWN','NOT_PUBLISHED','QUEUED','RUNNING','PASS','FAIL','ENVIRONMENT_BLOCKED'].includes(reported.status),'unsupported runtime status');
  return reported.status==='PASS'
    ? {...clone(reported),status:'UNKNOWN',reported_status:'PASS',verification:'UNVERIFIED_RUNTIME_CLAIM_NOT_PROMOTED',blocks_production:false}
    : {...clone(reported),blocks_production:false};
}

export function validateNativeInventoryMeasurements(native,asset,record,receipt) {
  const budget=receipt.brief.frozen_budget,texture=receipt.brief.frozen_texture_policy;
  need(Array.isArray(native.errors)&&native.errors.length===0,'native GLB errors');
  for(const [actual,maximum]of [['scene_triangles','max_triangles'],['materials','max_materials'],['scene_primitives_estimated_base_draw_calls','max_primitives'],['bytes','max_glb_bytes']]){
    need(Number.isSafeInteger(native[actual])&&native[actual]>=0,'missing native measurement '+actual);
    need(native[actual]<=budget[maximum],'frozen native budget exceeded '+maximum);
  }
  equal(native.scene_triangles,asset.triangles,'native/asset triangles changed');equal(asset.triangles,record.measurements.triangles,'record triangles changed');
  equal(native.bounds_m?.size,asset.dimensions,'native dimensions changed');equal(asset.dimensions,record.measurements.dimensions,'record dimensions changed');
  // Original no-texture requirements remain hard requirements; never infer from file size.
  need(Number.isSafeInteger(native.textures)&&native.textures>=0,'native texture count missing');need(native.textures<=texture.max_textures,'frozen texture count exceeded');
  return native;
}

export function bindNativeInventoryGlb(bytes,native) {
  need(Buffer.isBuffer(bytes)&&bytes.length>=20,'invalid native GLB bytes');
  equal(bytes.readUInt32LE(0),0x46546c67,'GLB magic');equal(bytes.readUInt32LE(4),2,'unsupported GLB version');equal(bytes.readUInt32LE(8),bytes.length,'GLB length');equal(bytes.readUInt32LE(16),0x4e4f534a,'GLB JSON chunk missing');
  equal(native.sha256,sha256(bytes),'native report belongs to different GLB');
  const json=JSON.parse(bytes.subarray(20,20+bytes.readUInt32LE(12)).toString('utf8'));
  const textures=(json.textures||[]).length,images=(json.images||[]).length;
  // The inspected inventory has no textures. Supporting textured assets requires a measured
  // encoded/decoded-byte and dimension adapter, not blind future trust in the count ceiling.
  need(textures===0&&images===0,'textured GLB measurement mapping not supported');
  return {...native,textures,texture_images:images};
}

// Exact contracts extracted from shared original-schema validation; no model IDs.
export const PUBLIC_GATE_CONTRACTS = Object.freeze({"named-gates-original-source-v1":[{"path":"productionAcceptance","kind":"equal","expected":"PASS"},{"path":"mandatory_repairs","kind":"equal","expected":[]},{"path":"source_and_rebuild.two_fresh_clean_rebuilds","kind":"equal","expected":"PASS"},{"path":"source_and_rebuild.both_byte_match_original","kind":"equal","expected":true},{"path":"source_and_rebuild.actual_blend_reexport","kind":"equal","expected":"PASS"},{"path":"source_and_rebuild.reexport_byte_match_original","kind":"equal","expected":true},{"path":"standard_glb.errors","kind":"equal","expected":0},{"path":"standard_glb.warnings","kind":"equal","expected":0},{"path":"science.status","kind":"equal","expected":"PASS"},{"path":"visual.status","kind":"equal","expected":"PASS"},{"path":"budget.status","kind":"equal","expected":"PASS"},{"path":"provenance.required_seven_roles_present","kind":"equal","expected":true},{"path":"original_history_preserved.approved","kind":"equal","expected":false},{"path":"production_gates","kind":"gates","allowed":{"science":"PASS","actual_visual_shape":"PASS","geometry_and_budget":"PASS","standard_glb":"PASS","source_and_clean_rebuild":"PASS","provenance_and_delivery":"PASS"}}],"criteria-exact-subject-v1":[{"path":"productionAccepted","kind":"equal","expected":true},{"path":"scope.minimum_required_repairs","kind":"equal","expected":[]},{"path":"compatibility.fresh_profile_valid","kind":"equal","expected":true},{"path":"compatibility.fresh_profile_contract_status","kind":"equal","expected":"pass"},{"path":"compatibility.historical_approved_for_brief","kind":"equal","expected":false},{"path":"production_criteria","kind":"criteria","allowed":{"technical-integrity":["PASS","pass"],"normal-view-craft":["PASS","pass"],"basic-form-and-scope":["PASS","pass"],"deliverables-and-label":["PASS","pass"],"target-loader":["PASS","pass"]}}],"criteria-seven-role-identity-v1":[{"path":"productionAccepted","kind":"equal","expected":true},{"path":"productionVerdict","kind":"equal","expected":"PASS"},{"path":"required_repairs","kind":"equal","expected":[]},{"path":"reproducibility.status","kind":"equal","expected":"PASS"},{"path":"historical_preservation.old_approved_false_unchanged","kind":"equal","expected":true},{"path":"historical_preservation.input_tree_unchanged","kind":"equal","expected":true},{"path":"criteria","kind":"criteria","allowed":{"technical-integrity":["PASS","pass"],"normal-view-craft":["PASS","pass"],"basic-form-and-scope":["PASS","pass"],"deliverables-and-label":["PASS","pass"],"target-loader":["PASS","pass"],"functional-render":["PASS_CPU_ONLY"],"representative-scene":["PASS_DECLARED_NEUTRAL_CPU_SCENE"]}}],"criteria-source-lineage-v1":[{"path":"productionAccepted","kind":"equal","expected":"PASS"},{"path":"verdict","kind":"equal","expected":"PASS"},{"path":"critical_findings","kind":"equal","expected":[]},{"path":"required_repairs","kind":"equal","expected":[]},{"path":"workflow.legacy_approved","kind":"equal","expected":false},{"path":"workflow.production_acceptance_is_additive_only","kind":"equal","expected":true},{"path":"criteria","kind":"criteria","allowed":{"exact-subject-and-source-lineage":["PASS","pass"],"technical-integrity-and-budget":["PASS","pass"],"closed-volumes-and-contact":["PASS","pass"],"basic-form-and-scientific-scope":["PASS","pass"],"normal-view-craft":["PASS","pass"],"canonical-cover":["PASS","pass"],"editable-source-and-reproducibility":["PASS","pass"],"delivery-label-and-provenance":["PASS","pass"]}}],"layered-qualified-gates-v1":[{"path":"productionAccepted","kind":"equal","expected":true},{"path":"verdict","kind":"equal","expected":"PASS"},{"path":"required_repairs","kind":"equal","expected":[]},{"path":"approved","kind":"equal","expected":false},{"path":"legacy_approved_preserved","kind":"equal","expected":false},{"path":"production_gate_results","kind":"gates","allowed":{"technical_integrity":"PASS","normal_view_craft":"PASS_WITH_EXPLICIT_NONBLOCKING_PRESENTATION_QUALIFICATIONS","basic_form_and_scope":"PASS_WITH_ARTISTIC_INFERENCE_LABELS","deliverables_and_label":"PASS","target_loader":"PASS","functional_render":"PASS_CYCLES_CPU_EVIDENCE_INSPECTED","representative_scene":"PASS_16_COPIES_43520_TRIANGLES"}}],"differential-detached-subject-v1":[{"path":"decision","kind":"equal","expected":"PASS_PRODUCTION_DIFFERENTIAL_QA"},{"path":"production_layer_independently_accepted","kind":"equal","expected":true},{"path":"all_production_gates_pass","kind":"equal","expected":true},{"path":"candidate_unchanged","kind":"equal","expected":true},{"path":"blockers","kind":"equal","expected":[]},{"path":"full_seven_stage_formal_acceptance","kind":"equal","expected":false},{"path":"seven_stages","kind":"gates","allowed":{"technical":"PASS","visual":"PASS","factual_frozen_feature_and_unchanged_prior_source_scope":"PASS_WITH_STATED_PRIOR_SOURCE_LIMITS","specification":"PASS","runtime_parse":"PASS","gpu":"NOT_RUN_SEPARATE_RELEASE_OR_POSTRELEASE_LAYER","scene":"NOT_RUN_SEPARATE_RELEASE_OR_POSTRELEASE_LAYER"}}],"differential-inline-seven-roles-v1":[{"path":"decision","kind":"equal","expected":"PASS"},{"path":"productionAccepted","kind":"equal","expected":true},{"path":"technical_summary.khronos_errors","kind":"equal","expected":0},{"path":"technical_summary.khronos_warnings","kind":"equal","expected":0},{"path":"technical_summary.fresh_rebuild_count","kind":"equal","expected":2},{"path":"technical_summary.fresh_rebuild_and_saved_source_reexport_byte_identical","kind":"equal","expected":true},{"path":"immutable_evidence.old_fail_preserved","kind":"equal","expected":true},{"path":"immutable_evidence.all_original_and_candidate_package_paths_sha_sizes_preserved","kind":"equal","expected":true},{"path":"production_stages","kind":"gates","allowed":{"technical":"PASS","visual":"PASS","factual":"PASS_WITHIN_UNCHANGED_GENUS_LEVEL_SCOPE","specification":"PASS_FOR_PRODUCTION_LAYER","runtime_parse":"PASS"}}],"independent-detached-stages-v1":[{"path":"decision","kind":"equal","expected":"PASS"},{"path":"productionAccepted","kind":"equal","expected":true},{"path":"blocking_issues","kind":"equal","expected":[]},{"path":"integrity.all_candidate_files_unchanged","kind":"equal","expected":true},{"path":"integrity.all_seven_roles_and_helper_hashes_verified","kind":"equal","expected":true},{"path":"technical.khronos_errors","kind":"equal","expected":0},{"path":"technical.khronos_warnings","kind":"equal","expected":0},{"path":"technical.fresh_rebuild_glb_semantics_source_metrics_exact","kind":"equal","expected":true},{"path":"technical.saved_blend_reexport_glb_byte_exact","kind":"equal","expected":true},{"path":"original_failure_preserved.new_result_does_not_modify_old_approved_state","kind":"equal","expected":true},{"path":"stages","kind":"gates","allowed":{"technical":"PASS","visual":"PASS","factual":"PASS_WITH_SCOPE_LIMITS","specification":"PASS","runtime_parse":"PASS","gpu":"NOT_RUN_POST_RELEASE","scene":"NOT_RUN_POST_RELEASE"}}]});

const compactHash=x=>sha256(Buffer.from(JSON.stringify(x)));
function publicOnly(value){const serialized=JSON.stringify(value);need(!/\/workspace\/|\/home\/|\/tmp\/|\/root\/|drive\.google\.com|docs\.google\.com/.test(serialized),'private path/access locator cannot enter compact public proof');}
/** Public proof is an explicit projection, not a claim CI can inspect private QA. */
export function projectInventoryCompatibilityForPublic(privateReceipt,scientificLimits){
 revalidateAcceptanceDerivation(privateReceipt.acceptance,privateReceipt.asset_id);
 const a=privateReceipt.acceptance,raw=a.original_fields;
 equal(a.gate_contract,PUBLIC_GATE_CONTRACTS[a.profile],'unknown public QA contract');
 for(const lang of ['en','zh'])need(nonempty(scientificLimits?.[lang]),'public scientific limits required');
 const values=a.gate_contract.map(rule=>{const value=raw[rule.path];need(value!==undefined,'missing mapped public gate '+rule.path);return rule.kind==='criteria'?value.map(c=>({id:c.id,status:c.status,evidence_count:c.evidence.length,evidence_sha256:compactHash(c.evidence)})):clone(value);});
 const qualifications=[];
 function add(path,value){if(value!==undefined)qualifications.push({source_field:path,value:clone(value),original_value_sha256:compactHash(value)});}
 for(const path of ['qualifications','science_limits','reproducibility_limits','limitations','nonblocking_limits'])add(path,raw[path]);
 add('scope',raw.scope);
 for(const path of ['criteria','production_criteria'])for(const [i,c]of (raw[path]||[]).entries())if(c.id.includes('basic-form'))for(const key of ['finding','findings'])add(`${path}.${i}.${key}`,c[key]);
 for(const key of ['finding','uncertainty','not_established','inherited_source_limitations','applicability','frozen_scope_quotes'])add('science.'+key,raw.science?.[key]);
 for(const [i,source]of (raw.science?.sources||[]).entries())for(const key of ['url','citation','access','use','license'])add(`science.sources.${i}.${key}`,source[key]);
 for(const key of ['source_support','no_reference_media_copied','pages_independently_read'])add('reference_verification.'+key,raw.reference_verification?.[key]);
 const result={schema_version:1,kind:'compact-inventory-compatibility-v1',derived:true,asset_id:privateReceipt.asset_id,representation:privateReceipt.representation,
  original_acceptance_sha256:privateReceipt.original_acceptance_sha256,private_derivation_sha256:compactHash(privateReceipt),
  brief:clone(privateReceipt.brief),scientific_limits:clone(scientificLimits),acceptance:{profile:a.profile,original_schema:a.original_schema,original_schema_version:a.original_schema_version,production_layer:'PASS',gate_contract:clone(a.gate_contract),gate_values:values,scientific_qualifications:qualifications,original_field_hashes:Object.fromEntries(Object.entries(raw).map(([k,v])=>[k,compactHash(v)])),original_reviewer_identity:a.reviewer_account_identity_established?{original_value_sha256:compactHash(a.original_reviewer_declaration)}:null},
  source_roles:Object.fromEntries(SOURCE_ROLES.map(role=>{const p=privateReceipt.source_roles[role];return [role,{sha256:p.sha256,bytes:p.bytes,original_path_sha256:compactHash(p.original_path),source_document_sha256:p.source_document_sha256,source_pointer_sha256:compactHash(p.source_pointer)}];})),
  status:'COMPATIBLE_PENDING_FRESH_INDEPENDENT_PROJECTION_REVIEW',production_acceptance_created:false,legacy_records_mutated:false,publication_authorized:false,
  ci_scope:'PUBLIC_COMPACT_STATIC_BINDING_ONLY_PRIVATE_ORIGINALS_REQUIRE_INDEPENDENT_REVIEW'};
 publicOnly(result);return result;
}
function compactFields(value,keys,label){need(object(value),'compact '+label+' must be an object');equal(Object.keys(value).sort(),keys.slice().sort(),'unknown/missing compact '+label+' fields');}
function validateCompactReceipt(receipt,record,asset,brief,references){
 compactFields(receipt,['schema_version','kind','derived','asset_id','representation','original_acceptance_sha256','private_derivation_sha256','brief','scientific_limits','acceptance','source_roles','status','production_acceptance_created','legacy_records_mutated','publication_authorized','ci_scope'],'receipt');
 compactFields(receipt.acceptance,['profile','original_schema','original_schema_version','production_layer','gate_contract','gate_values','scientific_qualifications','original_field_hashes','original_reviewer_identity'],'acceptance');
 compactFields(receipt.scientific_limits,['en','zh'],'scientific limits');
 equal(receipt.ci_scope,'PUBLIC_COMPACT_STATIC_BINDING_ONLY_PRIVATE_ORIGINALS_REQUIRE_INDEPENDENT_REVIEW','compact CI scope changed');
 publicOnly(receipt);equal(receipt.schema_version,1,'unsupported compact version');equal(receipt.derived,true,'compact proof is derived');
 equal(receipt.asset_id,asset.id,'compact identity mismatch');equal(record.asset_id,asset.id,'compact record identity mismatch');equal(receipt.representation,asset.representation,'compact representation changed');
 equal(receipt.original_acceptance_sha256,record.original_acceptance.sha256,'compact original proof changed');need(digest(receipt.private_derivation_sha256),'private derivation binding required');
 equal(receipt.brief,mapFrozenInventoryBrief(brief,references,asset.id),'compact original brief changed');equal(receipt.scientific_limits,record.scientific_limits,'compact public scientific limits changed');
 equal(receipt.status,'COMPATIBLE_PENDING_FRESH_INDEPENDENT_PROJECTION_REVIEW','compact status promotion');for(const key of ['production_acceptance_created','legacy_records_mutated','publication_authorized'])equal(receipt[key],false,'compact history/authority changed');
 const a=receipt.acceptance,expected=PUBLIC_GATE_CONTRACTS[a?.profile];need(expected,'unsupported compact QA profile');equal(a.production_layer,'PASS','nonpassing compact production');equal(a.gate_contract,expected,'compact gate contract changed');
 equal(a.gate_values?.length,expected.length,'missing compact gates');
 for(const [i,rule]of expected.entries()){const value=a.gate_values[i];if(rule.kind==='equal')equal(value,rule.expected,'compact original gate failed '+rule.path);else if(rule.kind==='gates'){equal(Object.keys(value||{}).sort(),Object.keys(rule.allowed).sort(),'compact gate set changed');for(const [key,allowed]of Object.entries(rule.allowed))need((Array.isArray(allowed)?allowed:[allowed]).includes(value[key]),'compact nonpassing gate '+key);}else{need(Array.isArray(value),'compact criteria missing');equal(value.map(c=>c.id).sort(),Object.keys(rule.allowed).sort(),'compact criteria changed');for(const c of value){compactFields(c,['id','status','evidence_count','evidence_sha256'],'criterion');need(rule.allowed[c.id].includes(c.status),'compact nonpassing criterion');need(Number.isSafeInteger(c.evidence_count)&&c.evidence_count>0&&digest(c.evidence_sha256),'compact criterion evidence binding missing');}}}
 const shape=PUBLIC_PROFILE_FIELDS[a.profile];equal(a.original_schema,shape.original_schema,'compact original schema changed');equal(a.original_schema_version,shape.original_schema_version,'compact schema version changed');
 equal(Object.keys(a.original_field_hashes||{}).sort(),shape.original_fields,'original field mapping omitted/added');need(Object.values(a.original_field_hashes).every(digest),'original field map hash bindings missing');
 need(Array.isArray(a.scientific_qualifications),'compact qualifications missing');equal(new Set(a.scientific_qualifications.map(q=>q.source_field)).size,a.scientific_qualifications.length,'duplicate compact qualification');for(const path of shape.required_qualifications)need(a.scientific_qualifications.some(q=>q.source_field===path),'missing mandatory qualification '+path);for(const q of a.scientific_qualifications){compactFields(q,['source_field','value','original_value_sha256'],'qualification');need(nonempty(q.source_field)&&q.value!==undefined,'compact qualification source missing');equal(compactHash(q.value),q.original_value_sha256,'compact qualification changed');}
 // Only this original schema requires an actual reviewer id/task declaration.
 if(a.profile==='criteria-exact-subject-v1'){
  compactFields(a.original_reviewer_identity,['original_value_sha256'],'historical reviewer');need(digest(a.original_reviewer_identity.original_value_sha256),'historical reviewer digest missing');equal(a.original_reviewer_identity.original_value_sha256,a.original_field_hashes.reviewer,'historical reviewer digest is not the original mapped declaration');
 }else equal(a.original_reviewer_identity,null,'historical reviewer identity is unsupported/unknown in this source mapping');
 equal(Object.keys(receipt.source_roles||{}).sort(),[...SOURCE_ROLES].sort(),'compact seven-role set changed');
 for(const role of SOURCE_ROLES){const p=receipt.source_roles[role];compactFields(p,['sha256','bytes','original_path_sha256','source_document_sha256','source_pointer_sha256'],'source role');equal(p.sha256,record.subject[role],'compact subject changed '+role);if(!record.source_role_derivations?.[role]){equal(p.sha256,record.roles[role].sha256,'compact role changed '+role);equal(p.bytes,record.roles[role].bytes,'compact role bytes changed '+role);}for(const key of ['original_path_sha256','source_document_sha256','source_pointer_sha256'])need(digest(p[key]),'compact source field binding missing '+role);}
 return receipt.brief.frozen_budget;
}

const stableJSON=value=>JSON.stringify(value,(_key,item)=>object(item)?Object.fromEntries(Object.keys(item).sort().map(key=>[key,item[key]])):item);
const normalizedHash=value=>sha256(Buffer.from(stableJSON(value)));
function sourcePointer(doc,pointer){const parts=pointer.slice(1).split('/');let parent=doc;for(const key of parts.slice(0,-1)){need(parent&&Object.hasOwn(parent,key),'missing derived-source pointer');parent=parent[key];}return {parent,key:parts.at(-1)};}
function sourceChangeAllowed(role,change,published,referencePins){
 const {pointer,operation}=change;need(digest(change.original_value_sha256),'original locator hash missing');
 const {parent,key}=sourcePointer(published,pointer);
 if(role==='references'&&/^\/sources\/\d+\/consult_only_files\/\d+\/path$/.test(pointer)){
  equal(operation,'remove','consult locator must only be removed');need(!Object.hasOwn(parent,key),'private consult locator retained');return;
 }
 if(role==='dependency-list'&&['/blender_lock','/lock'].includes(pointer)){
  equal(operation,'remove','lock locator must only be removed');need(!Object.hasOwn(parent,key),'private lock locator retained');return;
 }
 if(role==='dependency-list'&&/^\/external_runtime\/\d+\/path$/.test(pointer)){
  equal(operation,'replace','runtime locator operation changed');need(nonempty(parent.package_relative_path)&&!parent.package_relative_path.startsWith('/')&&!parent.package_relative_path.split('/').includes('..'),'invalid package runtime path');
  equal(parent.path,parent.package_relative_path,'runtime path is not existing package-relative binding');equal(change.published_value,parent.path,'runtime projection value changed');return;
 }
 if(role==='dependency-list'&&/^\/files\/\d+\/(sha256|bytes)$/.test(pointer)){
  equal(operation,'replace','reference dependency operation changed');need(parent.path?.endsWith('/references.json')||parent.path==='references.json','only references dependency can be rebound');need(referencePins,'reference derivation pins required');
  equal(change.original_value,referencePins.original[key],'original reference dependency changed');equal(compactHash(change.original_value),change.original_value_sha256,'original reference dependency hash changed');equal(parent[key],referencePins.published[key],'published reference dependency changed');equal(change.published_value,parent[key],'reference rebind changed');return;
 }
 need(false,'unsupported source projection field '+pointer);
}
function normalizeSourceProjection(doc,changes){const normalized=clone(doc);for(const c of changes){const {parent,key}=sourcePointer(normalized,c.pointer);parent[key]={original_value_sha256:c.original_value_sha256};}return normalized;}
/** Derive only non-executing locators and the resulting reference-pin propagation. */
export function projectDerivedSourceRole(role,originalBytes,publishedBytes,referencePins){
 need(['references','dependency-list'].includes(role),'source role is not derivable');const original=JSON.parse(originalBytes),published=JSON.parse(publishedBytes),changes=[];
 function diff(a,b,path=''){
  if(stableJSON(a)===stableJSON(b))return;
  if(object(a)&&object(b)){for(const key of new Set([...Object.keys(a),...Object.keys(b)])){
   need(!key.includes('/')&&!key.includes('~'),'unsupported source pointer key');const pointer=path+'/'+key;
   if(!Object.hasOwn(b,key))changes.push({pointer,operation:'remove',original_value_sha256:compactHash(a[key])});
   else if(!Object.hasOwn(a,key))need(false,'source projection cannot add fields');else diff(a[key],b[key],pointer);
  }}else if(Array.isArray(a)&&Array.isArray(b)){equal(a.length,b.length,'source projection cannot change array membership');a.forEach((v,i)=>diff(v,b[i],path+'/'+i));}
  else {const c={pointer:path,operation:'replace',original_value_sha256:compactHash(a),published_value:clone(b)};if(/^\/files\/\d+\/(sha256|bytes)$/.test(path))c.original_value=clone(a);changes.push(c);}
 }
 diff(original,published);need(changes.length>0,'source derivation needs actual changes');changes.sort((a,b)=>a.pointer.localeCompare(b.pointer));for(const c of changes)sourceChangeAllowed(role,c,published,referencePins);
 const before=normalizedHash(normalizeSourceProjection(original,changes)),after=normalizedHash(normalizeSourceProjection(published,changes));equal(before,after,'source scientific/execution fields changed');
 const result={kind:'nonexecuting-locator-projection-v1',role,original:{sha256:sha256(originalBytes),bytes:originalBytes.length},published:{sha256:sha256(publishedBytes),bytes:publishedBytes.length},original_normalized_sha256:before,changes};publicOnly(result);return result;
}
export function validateDerivedSourceRole(derivation,role,publishedBytes,receipt,record){
 equal(Object.keys(derivation).sort(),['kind','role','original','published','original_normalized_sha256','changes'].sort(),'unknown derived-source fields');equal(derivation.kind,'nonexecuting-locator-projection-v1','unknown source derivation');equal(derivation.role,role,'derived role changed');need(['references','dependency-list'].includes(role),'unsupported derived role');
 equal(derivation.original,{sha256:receipt.source_roles[role].sha256,bytes:receipt.source_roles[role].bytes},'original source pin changed');equal(derivation.original.sha256,record.subject[role],'original subject changed');
 equal(derivation.published,{sha256:sha256(publishedBytes),bytes:publishedBytes.length},'published source bytes changed');equal(derivation.published,{sha256:record.roles[role].sha256,bytes:record.roles[role].bytes},'published role pin changed');
 need(Array.isArray(derivation.changes)&&derivation.changes.length>0,'missing source projection diff');equal(new Set(derivation.changes.map(c=>c.pointer)).size,derivation.changes.length,'duplicate source projection pointer');
 const published=JSON.parse(publishedBytes),referencePins=record.source_role_derivations?.references;
 for(const c of derivation.changes){equal(Object.keys(c).sort(),(c.operation==='remove'?['pointer','operation','original_value_sha256']:/^\/files\//.test(c.pointer)?['pointer','operation','original_value_sha256','published_value','original_value']:['pointer','operation','original_value_sha256','published_value']).sort(),'unknown source-change fields');sourceChangeAllowed(role,c,published,referencePins);}
 equal(normalizedHash(normalizeSourceProjection(published,derivation.changes)),derivation.original_normalized_sha256,'undeclared source fields changed');publicOnly(derivation);return derivation;
}

const PUBLIC_PROFILE_FIELDS={"differential-detached-subject-v1":{"original_schema":null,"original_schema_version":1,"original_fields":["all_production_gates_pass","asset_id","blockers","candidate_unchanged","decision","full_seven_stage_formal_acceptance","production_layer_independently_accepted","reviewer","scope","separate_pending","seven_stages","subject_pins_sha256"],"required_qualifications":["scope"]},"named-gates-original-source-v1":{"original_schema":"independent-production-acceptance-v1","original_schema_version":null,"original_fields":["asset_id","budget.status","final_blend","final_glb","frozen_brief","mandatory_repairs","original_history_preserved","original_history_preserved.approved","postReleaseVerified","productionAcceptance","production_gates","provenance.required_seven_roles_present","releaseChecks","reviewer","science","science.status","source_and_rebuild.actual_blend_reexport","source_and_rebuild.both_byte_match_original","source_and_rebuild.reexport_byte_match_original","source_and_rebuild.two_fresh_clean_rebuilds","standard_glb.errors","standard_glb.warnings","visual.status"],"required_qualifications":["science.finding","science.uncertainty","science.sources.0.url","science.sources.0.access","science.sources.0.use"]},"criteria-exact-subject-v1":{"original_schema":"additive-first-independent-per-model-production-acceptance","original_schema_version":1,"original_fields":["compatibility","compatibility.fresh_profile_contract_status","compatibility.fresh_profile_valid","compatibility.historical_approved_for_brief","postReleaseVerified","productionAccepted","production_criteria","releaseChecks","reproducibility_limits","reviewer","scope.minimum_required_repairs","subject"],"required_qualifications":["reproducibility_limits","production_criteria.2.finding"]},"layered-qualified-gates-v1":{"original_schema":"layered-independent-production-acceptance-v1","original_schema_version":null,"original_fields":["approved","evidence","fresh_independent_checks","historical_freezes_failures","legacy_approved_preserved","postrelease_browser","productionAccepted","production_gate_results","qualifications","required_repairs","reviewer","subject","verdict"],"required_qualifications":["qualifications"]},"criteria-seven-role-identity-v1":{"original_schema":"independent-production-acceptance-v1","original_schema_version":null,"original_fields":["criteria","historical_preservation","historical_preservation.input_tree_unchanged","historical_preservation.old_approved_false_unchanged","identity","postrelease","productionAccepted","productionVerdict","reproducibility","reproducibility.status","required_repairs","review_kind","scope"],"required_qualifications":["scope","criteria.2.findings"]},"independent-detached-stages-v1":{"original_schema":null,"original_schema_version":null,"original_fields":["asset_id","blocking_issues","decision","evidence_files","frozen_science_scope","integrity.all_candidate_files_unchanged","integrity.all_seven_roles_and_helper_hashes_verified","nonblocking_limits","original_failure_preserved","original_failure_preserved.new_result_does_not_modify_old_approved_state","postReleaseVerified","productionAccepted","releaseChecks","reviewer_role","stages","subject_pins","technical","technical.fresh_rebuild_glb_semantics_source_metrics_exact","technical.khronos_errors","technical.khronos_warnings","technical.saved_blend_reexport_glb_byte_exact","visual_evidence"],"required_qualifications":["nonblocking_limits"]},"differential-inline-seven-roles-v1":{"original_schema":null,"original_schema_version":1,"original_fields":["asset_id","decision","evidence_files","immutable_evidence","immutable_evidence.all_original_and_candidate_package_paths_sha_sizes_preserved","immutable_evidence.old_fail_preserved","productionAccepted","production_stages","release_and_postrelease","review_type","root_pair_contact_adjudication","science_limits","seven_roles","technical_summary.fresh_rebuild_and_saved_source_reexport_byte_identical","technical_summary.fresh_rebuild_count","technical_summary.khronos_errors","technical_summary.khronos_warnings"],"required_qualifications":["science_limits"]},"criteria-source-lineage-v1":{"original_schema":"independent-production-acceptance-v1","original_schema_version":null,"original_fields":["asset_id","criteria","critical_findings","final_blend","final_glb","limitations","maker_handoff_sha256","productionAccepted","reference_verification","required_repairs","reviewer_role","verdict","workflow","workflow.legacy_approved","workflow.production_acceptance_is_additive_only"],"required_qualifications":["limitations","reference_verification.source_support","reference_verification.no_reference_media_copied","reference_verification.pages_independently_read","criteria.3.finding"]}};
/** Additive current evidence binding; never an invented historical reviewer or new science acceptance. */
export function validateSupplementaryReviewBinding(binding,record,receipt){
 assertProductionMaterial(binding);publicOnly(binding);equal(binding.kind,'independent-source-review-binding-public-v1','unsupported supplemental review schema');equal(binding.asset_id,record.asset_id,'supplement identity mismatch');equal(binding.status,'PASS','supplemental review not passing');
 equal(binding.originalReviewerIdentity,'UNKNOWN','supplement cannot invent original reviewer');equal(binding.original_reviewer_field,null,'supplement must preserve absent historical reviewer');
 equal(binding.original_acceptance.sha256,receipt.original_acceptance_sha256,'supplement original acceptance changed');need(Number.isSafeInteger(binding.original_acceptance.bytes)&&binding.original_acceptance.bytes>0,'supplement original acceptance size required');
 const who=binding.current_reviewer;need(nonempty(who?.id),'supplement current reviewer missing');equal(who.identity_kind,'derived_opaque_current_review_context_not_account_or_historical_actor','unsupported reviewer identity claim');equal(who.binding?.kind,'private_current_attestation_content_digest','private current attestation binding missing');need(digest(who.binding.sha256)&&Number.isSafeInteger(who.binding.bytes)&&who.binding.bytes>0,'current attestation digest missing');
 need(who.id!==record.maker.id,'supplement maker self-review');equal(binding.subject.asset_id,record.asset_id,'supplement subject identity changed');equal(Object.keys(binding.subject.seven_roles).sort(),[...SOURCE_ROLES].sort(),'supplement seven-role coverage changed');
 for(const role of SOURCE_ROLES)equal(binding.subject.seven_roles[role],{sha256:receipt.source_roles[role].sha256,bytes:receipt.source_roles[role].bytes},'supplement original subject changed '+role);
 for(const key of ['complete_manifest_members_rehashed','original_report_membership_and_coordinator_readback','seven_original_and_release_role_pins','separate_current_reviewer_context','saved_source_and_model_pixels_actually_inspected','scientific_scope_and_existing_acceptance_present','unchanged_input_readback'])equal(binding.current_checks?.[key],'PASS','supplement current evidence check missing '+key);
 need(object(binding.current_checks.native_critical_geometry)&&Object.keys(binding.current_checks.native_critical_geometry).length>0&&Object.values(binding.current_checks.native_critical_geometry).every(v=>v===true),'supplement native checks not passing');
 const criteriaIndex=receipt.acceptance.gate_contract.findIndex(r=>r.kind==='criteria');need(criteriaIndex>=0,'supplement schema requires original criterion mapping');const expected=receipt.acceptance.gate_values[criteriaIndex].map(c=>({id:c.id,status:c.status}));equal(binding.original_gates_retained,expected,'supplement original gates changed');
 equal(binding.state,{legacy_approved:false,runtime:'UNKNOWN',postReleaseVerified:'UNKNOWN_NOT_RUN',releaseChecks:'NOT_ATTESTED',count_delta:0,user_acceptance_claim:false},'supplement promotes history/runtime/release');need(nonempty(binding.current_scope)&&Array.isArray(binding.limitations)&&binding.limitations.length>0&&Array.isArray(binding.reused_not_freshly_executed)&&binding.reused_not_freshly_executed.length>0,'supplement scope/reuse limits absent');equal(binding.blocking_findings,[],'supplement has blocking findings');return binding;
}

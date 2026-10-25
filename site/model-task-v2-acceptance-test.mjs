import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {compileModelTaskV2Compatibility,validateModelTaskV2Receipt,verifyModelTaskV2Review,
  mapV2Decision,mapV2Brief,preserveV2Runtime,validateV2Measurements,V2_REVIEW_CHECKS} from './model-task-v2-acceptance.mjs';
import {SOURCE_ROLES,sha256,mapFrozenInventoryBrief,mapIndependentProductionAcceptance} from './inventory-type-acceptance.mjs';
const hash=x=>sha256(Buffer.from(JSON.stringify(x)));
const bytes=x=>Buffer.from(JSON.stringify(x));
const document=x=>{const b=bytes(x);return {bytes:b,pin:{sha256:sha256(b),bytes:b.length}};};
const pin=(p,b)=>({original_path:p,sha256:sha256(b),bytes:b.length});

// Synthetic documents live only in the test process. No receipt/review is saved.
function fixture(){
 const brief={template_version:'model-task-v2',asset_id:'sample-animal',revision:'r001',representation:'living-reconstruction',scope:'Whole animal; reconstructed soft tissue.',geometry_policy:{max_triangles:100,max_materials:3,max_primitives:4,max_glb_bytes:10000}};
 const references={sources:[{title:'Reference',url:'https://example.org/reference',use:'consulted, not incorporated'}]};
 const roles=Object.fromEntries(SOURCE_ROLES.map(r=>[r,pin(r+'.dat',Buffer.from(r))]));
 roles.brief=pin('brief.json',bytes(brief));roles.references=pin('references.json',bytes(references));
 const decision={asset_id:brief.asset_id,revision:'r001',status:'PASS',making:'COMPLETE',tests:'PASS_TECHNICAL_SCOPE',glb_sha256:roles.finalGLB.sha256,preview_sha256:hash('preview'),gpu:'UNKNOWN',scene:'NOT_RUN',user:'NOT_ACCEPTED',deployed:false,maker:{role:'maker',task:'maker-context'},reviewer:{role:'independent-QA',task:'reviewer-context',status:'PASS',summary:'Independent visual, factual, specification and source evidence review.'},evidence:[{path:'qa/evidence/review.json',sha256:hash('original independent evidence')}],limitations:['Not actual GPU or populated-scene acceptance.']};
 const manifest={template_version:'model-task-v2',asset_id:brief.asset_id,revision:'r001',roles:{...Object.fromEntries(SOURCE_ROLES.map(r=>[r,roles[r].original_path])),decision:'qa/decision.json',preview:'preview.png'},files:{...Object.fromEntries(SOURCE_ROLES.map(r=>[roles[r].original_path,roles[r].sha256])),'qa/decision.json':hash(decision),'preview.png':decision.preview_sha256,'qa/evidence/review.json':hash('original independent evidence')}};
 const input={asset_id:brief.asset_id,documents:{brief:document(brief),references:document(references),manifest:document(manifest),acceptance:document(decision)},roles,representation_mapping:{source_pointer:'/representation',original_value_sha256:hash(brief.representation),representation:'living-reconstruction',reconstruction_type:'whole-organism'},scientific_limits:{en:'Original reconstruction; soft-tissue uncertain.',zh:'原创复原，软组织存在不确定性。'}};
 const receipt=compileModelTaskV2Compatibility(input);
 const asset={id:brief.asset_id,revision:'r001',representation:'living-reconstruction',reconstruction_type:'whole-organism',production_acceptance_adapter:'model-task-v2',triangles:80,dimensions:[1,2,3]};
 const record={asset_id:asset.id,maker:{id:'maker-context',task_id:'maker-context'},original_acceptance:{sha256:input.documents.acceptance.pin.sha256},roles:Object.fromEntries(SOURCE_ROLES.map(r=>[r,{path:'published/'+roles[r].original_path,sha256:roles[r].sha256,bytes:roles[r].bytes}])),subject:Object.fromEntries(SOURCE_ROLES.map(r=>[r,roles[r].sha256])),scientific_limits:input.scientific_limits,measurements:{triangles:80,dimensions:[1,2,3]},postReleaseVerified:{status:'NOT_PUBLISHED'}};
 const evidenceBinding={document_sha256:hash('original independent evidence'),source_pointer:'/status',original_value_sha256:hash('PASS')};
 const review={evidence_bindings:{source_reproducibility:[evidenceBinding],format_geometry:[evidenceBinding],cpu_parse:[evidenceBinding],independent_visual_factual_specification:[{document_sha256:receipt.original_acceptance_sha256,source_pointer:receipt.decision.review_scope_pointer,original_value_sha256:receipt.decision.review_scope_sha256}]},kind:'independent-model-task-v2-compatibility-review-v1',status:'PASS',reviewer:{id:'projection-review-context',task_id:'projection-review-context'},original_acceptance_sha256:receipt.original_acceptance_sha256,private_derivation_sha256:receipt.private_derivation_sha256,compatibility_sha256:hash(receipt),checks:Object.fromEntries(V2_REVIEW_CHECKS.map(k=>[k,'PASS'])),blocking_findings:[],publication_authorized:false};
 return {input,receipt,asset,record,review,brief,references,decision,manifest};
}
function changeDoc(f,key,mutate){const doc=JSON.parse(f.input.documents[key].bytes);mutate(doc);f.input.documents[key]=document(doc);return doc;}

test('v2 compiles exact originals without creating legacy criteria or runtime acceptance',()=>{
 const f=fixture(),before=hash(f.input);
 assert.deepEqual(validateModelTaskV2Receipt(f.receipt,f.record,f.asset,f.brief,f.references),f.brief.geometry_policy);
 assert.deepEqual(verifyModelTaskV2Review(f.receipt,f.record,f.asset,f.brief,f.references,f.review),f.brief.geometry_policy);
 assert.equal(hash(f.input),before);assert.equal(f.receipt.production_acceptance_created,false);
 assert.equal(f.receipt.brief.original_criteria_created,false);assert(!('production_layer' in f.receipt));
 assert.equal(f.receipt.decision.runtime.gpu,'UNKNOWN');assert.equal(f.receipt.decision.runtime.deployed,false);
});
test('three exact decision layouts, scoped pass retained, unknown literals rejected',()=>{
 const {decision:d}=fixture();
 assert.equal(mapV2Decision(d,d.asset_id,d.revision).profile,'status-v2');
 const e=structuredClone(d);delete e.status;e.decision='PASS';assert.equal(mapV2Decision(e,e.asset_id,e.revision).profile,'decision-v2');
 delete e.decision;e.final_making_decision='PASS';assert.equal(mapV2Decision(e,e.asset_id,e.revision).profile,'reviewer-and-making-v2');
 const h={...d,status:'PASS_IN_SCOPE',reviewer:{...d.reviewer,status:'PASS_IN_SCOPE'}};assert.equal(mapV2Decision(h,h.asset_id,h.revision).decision_value,'PASS_IN_SCOPE');
 for(const value of ['PASS_BUT_REVISE','PASS_UNRECOGNIZED','REVISE','FAIL','UNKNOWN'])assert.throws(()=>mapV2Decision({...d,status:value},d.asset_id,d.revision));
 assert.throws(()=>mapV2Decision({...d,tests:'PASS_MADE_UP'},d.asset_id,d.revision));
});
test('missing pin, tampered bytes, missing role, manifest membership, and wrong GLB fail closed',()=>{
 let f=fixture();delete f.input.documents.acceptance.pin.sha256;assert.throws(()=>compileModelTaskV2Compatibility(f.input));
 f=fixture();f.input.documents.brief.bytes=Buffer.concat([f.input.documents.brief.bytes,Buffer.from(' ')]);assert.throws(()=>compileModelTaskV2Compatibility(f.input));
 f=fixture();delete f.input.roles.finalBlend;assert.throws(()=>compileModelTaskV2Compatibility(f.input));
 f=fixture();changeDoc(f,'manifest',m=>delete m.files['qa/decision.json']);assert.throws(()=>compileModelTaskV2Compatibility(f.input));
 f=fixture();changeDoc(f,'acceptance',d=>d.glb_sha256='f'.repeat(64));assert.throws(()=>compileModelTaskV2Compatibility(f.input));
 f=fixture();changeDoc(f,'manifest',m=>delete m.files['qa/evidence/review.json']);assert.throws(()=>compileModelTaskV2Compatibility(f.input));
});
test('maker-only, self-review, failed or blocked independent evidence is rejected',()=>{
 const {decision:d}=fixture();
 for(const alter of [x=>delete x.reviewer,x=>x.reviewer.role='maker',x=>x.reviewer.task=x.maker.task,x=>x.reviewer.status='REVISE',x=>x.blockers=['fix'],x=>x.reviewer.blocking_findings=['fix'],x=>delete x.reviewer.summary,x=>x.evidence=[],x=>{delete x.status;delete x.reviewer.status;x.final_making_decision='PASS';}]){
  const x=structuredClone(d);alter(x);assert.throws(()=>mapV2Decision(x,d.asset_id,d.revision));
 }
 const x=structuredClone(d);x.maker.task='/root/maker-context';x.reviewer.task='maker-context';assert.throws(()=>mapV2Decision(x,d.asset_id,d.revision));
});
test('live animals cannot be relabeled as fossils; unknown free-text mappings HOLD',()=>{
 const f=fixture();assert.throws(()=>mapV2Brief(f.brief,f.references,f.asset.id,{...f.input.representation_mapping,representation:'fossil-specimen',reconstruction_type:'specimen'}));
 const b={...f.brief,representation:'whole-organism'};assert.throws(()=>mapV2Brief(b,f.references,f.asset.id,{...f.input.representation_mapping,original_value_sha256:hash('whole-organism'),representation:'fossil-specimen',reconstruction_type:'specimen'}));
 const unknown={...f.brief,representation:'a new ambiguous scientific scope'};assert.throws(()=>mapV2Brief(unknown,f.references,f.asset.id,{...f.input.representation_mapping,original_value_sha256:hash(unknown.representation)}));
});
test('public receipt changed pins, metadata, gate profile, or source are rejected',()=>{
 for(const alter of [f=>f.receipt.original_acceptance_sha256='f'.repeat(64),f=>f.receipt.source_roles.finalGLB.sha256='f'.repeat(64),f=>delete f.receipt.source_roles.config,f=>f.asset.representation='fossil-specimen',f=>f.receipt.decision.profile='arbitrary-pass',f=>f.receipt.decision.reviewer_task_sha256=f.receipt.decision.maker_task_sha256,f=>f.receipt.production_acceptance_created=true,f=>f.record.source_role_derivations={brief:{}},f=>f.brief.scope='changed',f=>f.receipt.decision.tests='PASS_NEW_UNKNOWN']){
  const f=fixture();alter(f);assert.throws(()=>validateModelTaskV2Receipt(f.receipt,f.record,f.asset,f.brief,f.references));
 }
});
test('projection review is mandatory, fresh, independent, complete, and not publication authority',()=>{
 for(const alter of [f=>delete f.review,f=>f.review.status='PENDING',f=>f.review.reviewer=f.record.maker,f=>f.review.compatibility_sha256='f'.repeat(64),f=>delete f.review.evidence_bindings.source_reproducibility,f=>f.review.evidence_bindings.cpu_parse=[],f=>f.review.evidence_bindings.independent_visual_factual_specification[0].original_value_sha256='f'.repeat(64),f=>delete f.review.checks.representation_and_scope_mapping,f=>f.review.publication_authorized=true,f=>f.review.blocking_findings=['scope not established']]){
  const f=fixture();alter(f);assert.throws(()=>verifyModelTaskV2Review(f.receipt,f.record,f.asset,f.brief,f.references,f.review));
 }
});
test('unknown GPU stays unknown, unverified PASS is not promoted, known FAIL survives',()=>{
 const f=fixture();assert.equal(preserveV2Runtime(f.record,f.receipt).status,'NOT_PUBLISHED');
 f.record.postReleaseVerified.status='PASS';assert.equal(preserveV2Runtime(f.record,f.receipt).status,'UNKNOWN');
 f.receipt.decision.runtime.gpu='FAIL';assert.equal(preserveV2Runtime(f.record,f.receipt).status,'FAIL');
 assert.equal(preserveV2Runtime(f.record,f.receipt).original_runtime.scene,'NOT_RUN');
});
test('native limits are checked and no frozen texture budget is invented',()=>{
 const f=fixture(),n={errors:[],scene_triangles:80,materials:2,scene_primitives_estimated_base_draw_calls:3,bytes:8000,bounds_m:{size:[1,2,3]},textures:0,texture_images:0};
 assert.equal(validateV2Measurements(n,f.asset,f.record,f.receipt),n);assert(!('frozen_texture_policy' in f.receipt.brief));
 for(const key of ['textures','texture_images'])assert.throws(()=>validateV2Measurements({...n,[key]:1},f.asset,f.record,f.receipt));
 assert.throws(()=>validateV2Measurements({...n,scene_triangles:101},f.asset,f.record,f.receipt));
});
test('old frozen-brief/QA dispatch remains strict and cannot silently accept v2',()=>{
 const f=fixture();assert.throws(()=>mapFrozenInventoryBrief(f.brief,f.references,f.asset.id),/unsupported frozen brief schema/);
 assert.throws(()=>mapIndependentProductionAcceptance(f.decision,f.asset.id),/unsupported original independent acceptance schema/);
});
test('content reuse still requires authenticated baseline, independently of code regression scope',async()=>{
 const code=await readFile(new URL('./production-release.mjs',import.meta.url),'utf8');
 assert(code.includes("if(!authenticated.capability)return full(authenticated.reasons.join('; '))"));
 assert(code.includes("Model content scope is independent of code regression scope"));
});

test('all current authority aliases and required repairs reject contradictions',()=>{
 const {decision:d}=fixture();
 const passFields=['production_verdict','production_qa','independent_qa','independent_review','independent_acceptance','final_production_decision','qa','independent_visual','independent_factual','independent_specification','visual','factual','specification'];
 const emptyFields=['minimum_required_repairs','required_revisions','remaining_issues','blocking_findings','blocking_issues','required_repairs','critical_findings','mandatory_repairs','blockers'];
 for(const key of passFields)assert.throws(()=>mapV2Decision({...d,[key]:'REVISE'},d.asset_id,d.revision),key);
 for(const key of emptyFields)assert.throws(()=>mapV2Decision({...d,[key]:['must fix']},d.asset_id,d.revision),key);
 for(const mutate of [x=>x.accepted_for_brief=false,x=>x.final_making_decision='REVISE',x=>x.reviewer.verdict='REVISE',x=>x.reviewer.required_revisions=['must fix'],x=>x.repair={independent_status:'PENDING'},x=>x.revision_requests=[{id:'R1',status:'OPEN'}],x=>x.issues=[{id:'R1',reviewer_status:'REVISE'}],x=>x.independent_review={visual:'FAIL'},x=>x.tests_detail={source_geometry:'FAIL'},x=>x.technical={khronos_errors:1}]){
  const x=structuredClone(d);mutate(x);assert.throws(()=>mapV2Decision(x,d.asset_id,d.revision));
 }
});
test('historical REVISE remains intact while currently closed repairs pass',()=>{
 const {decision:d}=fixture();
 const x={...d,prior_independent_verdict:{status:'REVISE'},original_maker_decision:{status:'REVISE'},repair_maker_decision:{status:'MAKER_REPAIRED_PENDING_INDEPENDENT_REREVIEW'},reviewer:{...d.reviewer,prior_status:'REVISE'},revision_requests:[{id:'R1',status:'CLOSED_BY_INDEPENDENT_QA'}],issues:[{id:'R2',reviewer_status:'CLOSED',maker_response_status:'REPAIRED_SUBMITTED_FOR_INDEPENDENT_REVIEW'}],repair:{maker_status:'ADDRESSED_PENDING_INDEPENDENT_RECHECK',independent_status:'RESOLVED'}};
 const before=hash(x);assert.equal(mapV2Decision(x,d.asset_id,d.revision).decision_value,'PASS');assert.equal(hash(x),before);assert.equal(x.prior_independent_verdict.status,'REVISE');
});
test('current requirement projection rejects deletion, unknown fields, and rewritten current values',()=>{
 const f=fixture();f.receipt.decision.current_requirements={'/production_verdict':'PASS'};f.receipt.decision.current_requirements_sha256=hash(f.receipt.decision.current_requirements);
 assert.doesNotThrow(()=>validateModelTaskV2Receipt(f.receipt,f.record,f.asset,f.brief,f.references));
 for(const mutate of [x=>delete x.receipt.decision.current_requirements,x=>delete x.receipt.decision.current_requirements['/production_verdict'],x=>x.receipt.decision.current_requirements['/unknown_gate']='PASS',x=>x.receipt.decision.current_requirements['/production_verdict']='REVISE']){
  const x=structuredClone(f);mutate(x);assert.throws(()=>validateModelTaskV2Receipt(x.receipt,x.record,x.asset,x.brief,x.references));
 }
});
test('projection self-review rejects /root alias and replacement record maker',()=>{
 let f=fixture();f.review.reviewer={id:'/root/maker-context',task_id:'/root/maker-context'};assert.throws(()=>verifyModelTaskV2Review(f.receipt,f.record,f.asset,f.brief,f.references,f.review));
 f=fixture();f.record.maker={id:'replacement-maker-context',task_id:'replacement-maker-context'};f.review.reviewer={id:'different-opaque-id',task_id:'/root/maker-context'};assert.throws(()=>verifyModelTaskV2Review(f.receipt,f.record,f.asset,f.brief,f.references,f.review));
});

test('current checks exact contract rejects every failed, omitted, or unknown gate',()=>{
 const {decision:d}=fixture();
 const checks={source_glb:'PASS',khronos:'PASS_0_ERRORS_0_WARNINGS',isolated_two_rebuilds:'PASS_BYTE_AND_SEMANTIC_IDENTICAL',saved_source_geometry:'PASS_DIAGNOSTIC_SCOPE',threejs_parse:'PASS_PARSE_ONLY',independent_visual:'PASS',independent_factual:'PASS',independent_specification:'PASS',independent_hash_and_source_closure:'PASS',independent_decoded_glb:'PASS'};
 const positive=mapV2Decision({...d,checks},d.asset_id,d.revision);assert.deepEqual(positive.current_requirements['/checks'],checks);
 for(const key of Object.keys(checks)){
  assert.throws(()=>mapV2Decision({...d,checks:{...checks,[key]:'REVISE'}},d.asset_id,d.revision));
  assert.throws(()=>mapV2Decision({...d,checks:{...checks,[key]:'FAIL'}},d.asset_id,d.revision));
  const omitted={...checks};delete omitted[key];assert.throws(()=>mapV2Decision({...d,checks:omitted},d.asset_id,d.revision));
 }
 assert.throws(()=>mapV2Decision({...d,checks:{...checks,unknown_gate:'PASS'}},d.asset_id,d.revision));
 const f=fixture();f.receipt.decision.current_requirements={'/checks':checks};f.receipt.decision.current_requirements_sha256=hash(f.receipt.decision.current_requirements);
 assert.doesNotThrow(()=>validateModelTaskV2Receipt(f.receipt,f.record,f.asset,f.brief,f.references));
 f.receipt.decision.current_requirements['/checks'].independent_factual='REVISE';f.receipt.decision.current_requirements_sha256=hash(f.receipt.decision.current_requirements);
 assert.throws(()=>validateModelTaskV2Receipt(f.receipt,f.record,f.asset,f.brief,f.references));
});

test('reviewed historical declaration aliases preserve literal scope, never confer independent PASS',()=>{
 const {decision:d}=fixture();
 const technical=['PASS_SOURCE_GLB_KHRONOS_REBUILDS_PARSE','PASS_LOCAL_TECHNICAL','PASS_SOURCE_STATIC_GLB_KHRONOS_TWO_REBUILDS_THREE_PARSE','PASS_WITH_INTENTIONAL_SMOOTH_STYLE_WARNING','PASS_SOURCE_GLB_KHRONOS_TWO_ISOLATED_REBUILDS_AND_THREEJS_PARSE','PASS_STATIC_FORMAT_SOURCE_REBUILD_PARSE_ONLY','PASS_STATIC_AND_REBUILD'];
 for(const making of ['PASS_MAKER_SELF_CHECK','PASS_MAKER_SELF_REVIEW'])for(const tests of technical){
  const x={...d,making,tests};const before=hash(x);const result=mapV2Decision(x,d.asset_id,d.revision);
  assert.equal(result.tests,tests);assert.equal(hash(x),before);assert.equal(result.runtime.gpu,'UNKNOWN');
  for(const status of ['FAIL','REVISE','PENDING','PASS_MADE_UP'])assert.throws(()=>mapV2Decision({...x,status},d.asset_id,d.revision));
  assert.throws(()=>mapV2Decision({...x,reviewer:{...d.reviewer,status:'FAIL'}},d.asset_id,d.revision));
 }
 for(const field of ['making','tests'])for(const value of ['PASS_BUT_FAIL','PASS_MADE_UP','NOT_PASS','FAIL','REVISE','UNKNOWN'])assert.throws(()=>mapV2Decision({...d,[field]:value},d.asset_id,d.revision));
});
test('reviewed whole-animal free text remains living with exact original wording pin',()=>{
 const f=fixture();
 for(const representation of ['living-reconstruction of whole animal, bounded by same-species real skeletons and preserved fin soft tissue','whole-animal living-reconstruction, not a slab or partial skull']){
  const brief={...f.brief,representation};const mapping={...f.input.representation_mapping,original_value_sha256:hash(representation)};
  assert.equal(mapV2Brief(brief,f.references,f.asset.id,mapping).representation_mapping.original_value_sha256,hash(representation));
  assert.throws(()=>mapV2Brief(brief,f.references,f.asset.id,{...mapping,representation:'fossil-specimen',reconstruction_type:'specimen'}));
  assert.throws(()=>mapV2Brief({...brief,representation:representation+' FAIL'},f.references,f.asset.id,{...mapping,original_value_sha256:hash(representation+' FAIL')}));
 }
});
test('historical independent issue closure layouts preserve evidence and reject all contradictory current aliases',()=>{
 const {decision:d}=fixture();
 const states=[{id:'QA-01',resolution_status:'CLOSED_BY_INDEPENDENT_RECHECK'},{id:'FORM-GATE-01',status:'CLOSED',supplement_status:'INDEPENDENTLY_ACCEPTED',resolution_evidence:'qa/evidence/review.json'}];
 for(const state of states){
  const x={...d,issues:[state]};const mapped=mapV2Decision(x,d.asset_id,d.revision);assert.deepEqual(mapped.current_requirements['/issues'],[state]);
  for(const field of ['reviewer_status','status','resolution_status'])for(const value of ['OPEN','FAIL','REVISE','PENDING','CLOSED_BY_MAKER'])assert.throws(()=>mapV2Decision({...x,issues:[{...state,[field]:value}]},d.asset_id,d.revision));
  const f=fixture();f.receipt.decision.current_requirements={'/issues':[state]};f.receipt.decision.current_requirements_sha256=hash(f.receipt.decision.current_requirements);
  assert.doesNotThrow(()=>validateModelTaskV2Receipt(f.receipt,f.record,f.asset,f.brief,f.references));
 }
 for(const issue of [{id:'X',status:'CLOSED'},{id:'X',status:'CLOSED',supplement_status:'MAKER_ACCEPTED',resolution_evidence:'qa/evidence/review.json'},{id:'X',resolution_status:'CLOSED_BY_INDEPENDENT_RECHECK',reviewer_status:'OPEN'}])assert.throws(()=>mapV2Decision({...d,issues:[issue]},d.asset_id,d.revision));
});
test('closed independent review retains explicit PASS and stable review identity without rewriting original',()=>{
 const f=fixture(),d=structuredClone(f.decision);d.reviewer.status='CLOSED';const before=JSON.stringify(d);const got=mapV2Decision(d,d.asset_id,d.revision);assert.equal(got.reviewer_status,'CLOSED');assert.equal(JSON.stringify(d),before);
 delete d.reviewer.task;d.reviewer.review_id='sample-independent-review-r001';assert.equal(mapV2Decision(d,d.asset_id,d.revision).reviewer_task_sha256,hash(d.reviewer.review_id));
 for(const edit of [x=>x.status='REVISE',x=>delete x.status,x=>x.reviewer.review_id='',x=>x.reviewer.review_id=x.maker.task,x=>x.blocking_findings=['open'],x=>x.reviewer.status='PENDING']){const bad=structuredClone(d);edit(bad);assert.throws(()=>mapV2Decision(bad,bad.asset_id,bad.revision));}
});
test('array-form original references retain original semantic binding and nonempty requirement',()=>{
 const f=fixture(),mapping=f.input.representation_mapping;const refs=[{title:'Reference',url:'https://example.org/reference'}];const got=mapV2Brief(f.brief,refs,f.brief.asset_id,mapping);assert.equal(got.original_references_semantic_sha256,hash(refs));assert.throws(()=>mapV2Brief(f.brief,[],f.brief.asset_id,mapping));
});

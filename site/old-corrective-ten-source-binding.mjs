/** Frozen native-edit source mapping for this exact ten-model / eleven-entry batch.
 * A compact derivation never changes an original verdict or grants publication.
 * Original private documents are consumed only by compilation; fresh independent
 * projection review must bind the resulting receipt and full public metadata.
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {SOURCE_PROFILES} from './old-corrective-ten-source-profiles.mjs';
export const CORRECTIVE_SOURCE_KIND='compact-old-corrective-ten-source-v1';
export const CORRECTIVE_SOURCE_IDS=Object.freeze(SOURCE_PROFILES.map(p=>p.entry_id));
const sha=b=>createHash('sha256').update(b).digest('hex');
const canonical=v=>JSON.stringify(v,(_,x)=>x&&typeof x==='object'&&!Array.isArray(x)?Object.fromEntries(Object.keys(x).sort().map(k=>[k,x[k]])):x);
export const correctiveSourceDigest=v=>sha(Buffer.from(canonical(v)));
const clone=structuredClone;
const exact=(v,keys,label)=>assert.deepEqual(Object.keys(v||{}).sort(),keys.slice().sort(),label+': unknown/missing fields');
const normalize=s=>s.trim().toLowerCase().replace(/^\/root\//,'');
function actor(x){exact(x,['id','task_id'],'Actor');for(const v of Object.values(x))assert(typeof v==='string'&&v.trim()&&!/^(unknown|pending|none|null|n\/a)$/i.test(v),'Known exact actor required');assert.equal(normalize(x.id),normalize(x.task_id),'Actor aliases differ');return normalize(x.id);}
function pointer(doc,p){assert(typeof p==='string'&&p.startsWith('/')&&p.length>1);return p.slice(1).split('/').map(k=>k.replaceAll('~1','/').replaceAll('~0','~')).reduce((x,k)=>{assert(x&&Object.hasOwn(x,k)&&!['__proto__','constructor','prototype'].includes(k),'Missing or unsafe original pointer');return x[k];},doc);}
function profile(id){const p=SOURCE_PROFILES.find(p=>p.entry_id===id);assert(p,'Entry outside the fixed corrective batch');return p;}
function publicSemantics(asset){const keys=Object.keys(profile(asset.id).public_semantics);return Object.fromEntries(keys.map(k=>{assert(Object.hasOwn(asset,k),'Missing explicit public semantic field '+k);return[k,asset[k]];}));}
function receiptFor(p){return{schema_version:1,kind:CORRECTIVE_SOURCE_KIND,entry_id:p.entry_id,stable_model_id:p.stable_model_id,configuration:p.configuration,operation:p.operation,profile_sha256:correctiveSourceDigest(p),original_documents:clone(p.original_documents),original_decision:clone(p.original_decision),maker:clone(p.maker),original_reviewer:clone(p.reviewer),source_subject:clone(p.subject),semantic_binding:clone(p.public_semantics),original_scoped_statements:clone(p.original_scoped_statements),identity_supplement:clone(p.identity_supplement),source_limits:p.source_limits,source_method:'EDITABLE_NATIVE_CORRECTIVE_SOURCE_NOT_NEW_GENERATOR_RECONSTRUCTION',original_teaching_near_preserved:p.original_teaching_near_preserved,original_reports_unchanged:true,production_acceptance_created:false,publication_authorized:false,world_accepted:false,physics_accepted:false,host_accepted:false,hardware_gpu_accepted:false,user_visual_acceptance:false};}
function mediaBytes(p,media){exact(media,['glb','blend'],'Exact native and exported media');for(const kind of ['glb','blend']){const b=media[kind];assert(Buffer.isBuffer(b),'Exact media bytes required');assert.equal(b.length,p.subject[kind].bytes,'Source media length changed');assert.equal(sha(b),p.subject[kind].sha256,'Source media bytes changed');}const g=media.glb;assert(g.length>=12&&g.toString('ascii',0,4)==='glTF'&&g.readUInt32LE(4)===2&&g.readUInt32LE(8)===g.length,'GLB2 required');assert(media.blend.length>12,'Editable native bytes required');}
export function compileCorrectiveSource({entry_id,documents,media,asset}){
 const p=profile(entry_id);assert.equal(asset.id,p.entry_id);assert.deepEqual(publicSemantics(asset),p.public_semantics,'Scientific scope or same-model identity changed');mediaBytes(p,media);
 exact(documents,Object.keys(p.original_documents),'Complete exact original document roles');const parsed={};
 for(const [role,pin]of Object.entries(p.original_documents)){const b=documents[role];assert(Buffer.isBuffer(b),'Original document bytes required');assert.equal(b.length,pin.bytes,'Original document length changed');assert.equal(sha(b),pin.sha256,'Original document bytes changed');if(role!=='maker_checksum'&&(role!=='original_review'||entry_id==='serac'))parsed[role]=JSON.parse(b);}
 const get=b=>pointer(parsed[b.document],b.pointer);
 assert.equal(get(p.original_decision),p.original_decision.value,'Original decision changed');
 assert.equal(pointer(parsed.original_qa_event,p.original_report_pointer),p.original_documents.original_review.sha256,'Original full review not bound by QA event');
 for(const kind of ['glb','blend'])assert.equal(get(p.subject_pointers[kind]),p.subject[kind].sha256,'Original QA subject mismatch');
 assert.equal(normalize(get(p.maker_pointer)),actor(p.maker),'Original maker differs');assert.equal(normalize(get(p.reviewer_pointer)),actor(p.reviewer),'Original reviewer differs');assert.notEqual(actor(p.maker),actor(p.reviewer),'Maker cannot self-review');
 if(p.identity_supplement){assert.equal(parsed.coordinator_snapshot.ledger.sha256,p.identity_supplement.original_ledger_sha256);const s=pointer(parsed.coordinator_snapshot,p.identity_supplement.original_pointer);assert.equal(s.maker_handoff_sha256,p.original_documents.original_maker_evidence.sha256);const role=p.configuration;assert(['lod0','lod1'].includes(role),'Only accepted paired native representation identity');assert.equal(s.candidate_current[role].glb_sha256,p.subject.glb.sha256);assert.equal(s.candidate_current[role].blend_sha256,p.subject.blend.sha256);}
 const link=p.maker_link;
 if(link.kind==='DIRECT_QA_EVENT_HANDOFF_HASH')assert.equal(pointer(parsed.original_qa_event,link.pointer),p.original_documents.original_maker_evidence.sha256);
 else if(link.kind==='QA_CHECKSUM_MANIFEST_HANDOFF_MEMBER'){assert.equal(pointer(parsed.original_qa_event,link.pointer),p.original_documents.maker_checksum.sha256);assert(documents.maker_checksum.toString('utf8').split(/\r?\n/).includes(p.original_documents.original_maker_evidence.sha256+'  '+link.member),'Maker absent from exact QA-accepted checksum manifest');}
 else{assert.equal(link.kind,'EXACT_COMMON_CANDIDATE_SEAL_AND_IDENTITY');assert.deepEqual(parsed.original_maker_evidence.identity,parsed.original_qa_event.identity);assert.deepEqual(parsed.original_maker_evidence.candidate_seal,parsed.original_qa_event.candidate_seal);assert.equal(pointer(parsed.original_review,link.pointer),pointer(parsed.original_qa_event,link.pointer));}
 return receiptFor(p);
}
export function validateCorrectiveSource(receipt,asset,media){const p=profile(asset.id);assert.deepEqual(receipt,receiptFor(p),'Receipt differs from frozen exact original mapping');assert.deepEqual(publicSemantics(asset),p.public_semantics,'Public scope or identity differs');for(const k of ['glb','blend']){assert.equal(asset[k],p.subject[k].path);assert.equal(asset.sha256[k],p.subject[k].sha256);}mediaBytes(p,media);return{status:'EXACT_SOURCE_MAPPING_ONLY',publication_authorized:false,independent_projection_review:'REQUIRED'};}
export const CORRECTIVE_SOURCE_REVIEW_CHECKS=Object.freeze(['full_original_private_report_and_event_bytes','original_scoped_decision_and_unresolved_limits','exact_candidate_native_and_glb_subject','actual_maker_and_distinct_original_reviewer_chain','same_model_representation_not_new_scientific_subject','full_public_metadata_and_no_inherited_approval','original_sources_and_reviews_preserved']);
export function verifyCorrectiveSourceReview({receipt,asset,media,review,producer}){
 validateCorrectiveSource(receipt,asset,media);exact(review,['schema_version','kind','status','reviewer','entry_id','receipt_sha256','metadata_sha256','original_documents','checks','blocking_findings','publication_authorized','world_accepted','physics_accepted'],'Independent corrective source review');
 assert.equal(review.schema_version,1);assert.equal(review.kind,'independent-old-corrective-ten-source-projection-v1');assert.equal(review.status,'PASS_SOURCE_PROJECTION_ONLY');assert.equal(review.entry_id,asset.id);assert.equal(review.receipt_sha256,correctiveSourceDigest(receipt));assert.equal(review.metadata_sha256,correctiveSourceDigest(asset));assert.deepEqual(review.original_documents,receipt.original_documents);
 const who=actor(review.reviewer);for(const x of [producer,receipt.maker])assert.notEqual(who,actor(x),'Preparer or maker cannot review its projection');exact(review.checks,CORRECTIVE_SOURCE_REVIEW_CHECKS,'Bounded source checks');for(const k of CORRECTIVE_SOURCE_REVIEW_CHECKS)assert.equal(review.checks[k],'PASS','Uncompleted source check '+k);assert.deepEqual(review.blocking_findings,[]);for(const k of ['publication_authorized','world_accepted','physics_accepted'])assert.equal(review[k],false,'Source projection cannot promote publication/runtime');return review;
}

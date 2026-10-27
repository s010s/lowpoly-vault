/** Synthetic new19 mechanism probes against exact historical602. Not production acceptance. */
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {resolve,join} from 'node:path';
import {mkdtempSync,writeFileSync,symlinkSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {digest,encode,hashBytes,recordReference,composeRegistry,assertRegistryAppend} from './model-registry.mjs';
import {readRegistry,readRegistryAtCommit} from './model-registry-cli.mjs';
import {inspectAppendContinuation,APPEND_IDS,APPEND_RELEASE,APPEND_BASELINE,APPEND_ROOT_PIN,APPEND_SELECTION_PIN,APPEND_CHECKS} from './same-id-append-continuation.mjs';
import {selectSuccessorManifest,composeSuccessorRegistry,successorContext,historicalManifestView,historicalGalleryView,historicalTurntableView,successorReader} from './same-id-successors.mjs';
import {exactDetailCohorts,selectedDetailAppend} from './detail-append-cohort.mjs';
const root=resolve(process.env.APPEND_TEST_SOURCE_ROOT||'.'),originalRead=successorReader(root),cache=new Map(),rootRead=p=>{if(!cache.has(p))cache.set(p,originalRead(p));return cache.get(p);};
const rootBase=JSON.parse(rootRead(APPEND_ROOT_PIN.path)),selection=JSON.parse(rootRead(APPEND_SELECTION_PIN.path));
const legacySelected=selectSuccessorManifest({baseManifest:rootBase,selection,selectionPin:APPEND_SELECTION_PIN,read:rootRead}),legacyRegistry=readRegistryAtCommit(root,APPEND_BASELINE),currentRegistry=readRegistry(root);
// Authenticate the old registry at the exact immutable main commit, never derive
// it by filtering a caller's changed current tree. Both pre/post-append trees work.
const currentAdded=assertRegistryAppend(legacyRegistry,currentRegistry);
assert.deepEqual(currentAdded,currentAdded.length?[...APPEND_IDS]:[],'Current test tree must be exact602 or this exact appended621');
const same=(a,b,label)=>assert.equal(digest(a),digest(b),label);
const flags={publication_authorized:false,reviewer_authority:false,world_accepted:false,physics_accepted:false};
const contentChecks=['independent_source_acceptance','exact_subject_and_source','scientific_scope_and_limits','geometry_and_topology','source_reproducibility','standard_glb_and_decode','final_preview_and_posters','compact_provenance_and_credits'];
function png(w,h,id){const b=Buffer.alloc(128);Buffer.from('89504e470d0a1a0a','hex').copy(b);b.write('IHDR',12);b.writeUInt32BE(w,16);b.writeUInt32BE(h,20);b[24]=8;b[25]=6;b.write(id,32);return b;}
function fixture(){
 const files=new Map(),save=(path,value)=>{const b=Buffer.isBuffer(value)?value:Buffer.from(encode(value));files.set(path,b);return {path,sha256:hashBytes(b),bytes:b.length};},read=p=>files.has(p)?files.get(p):rootRead(p);
 const producer={id:'synthetic-preparer',task_id:'/root/synthetic-preparer'},reviewer={id:'synthetic-independent-reviewer',task_id:'/root/synthetic-independent-reviewer'};
 const production={schema_version:1,kind:'content-production-release-v1',baseline_commit:APPEND_BASELINE,producer,assets:[],review_path:`production/${APPEND_RELEASE}/review.json`,scope_document:save(`production/${APPEND_RELEASE}/scope.json`,{fixture_only:true}),licenses:[],publication_authorized:false};
 const records=[],evidence=[];
 for(const id of APPEND_IDS){
  const dir=`assets/additions/${id}/${APPEND_RELEASE}-r001`,glb=Buffer.alloc(64);glb.write('glTF');glb.writeUInt32LE(2,4);glb.writeUInt32LE(glb.length,8);glb.write(id,12);
  const glbPin=save(dir+'/model.glb',glb),blendPin=save(dir+'/source.blend',Buffer.from('synthetic '+id)),detail=save('site/public/gallery/posters/'+id+'.png',png(512,512,id)),wheel=save('site/public/gallery/posters/'+id+'-wheel.png',png(768,432,id)),preview=save(dir+'/preview.png',read(detail.path));
  const asset={id,name:{en:id,zh:id},description:{en:'Synthetic test only',zh:'仅机制测试'},collection:'prehistoric',worlds:['prehistoric'],packs:[APPEND_RELEASE],category:'animals',license:'CC-BY-4.0',units:'meters',revision:'r001',dimensions:[1,1,1],triangles:1,glb:glbPin.path,blend:blendPin.path,preview:preview.path,sha256:{glb:glbPin.sha256,blend:blendPin.sha256,preview:preview.sha256},production_release:`production/${APPEND_RELEASE}/release.json`,production_acceptance_adapter:'model-task-static4-split-source-v1'};
  const config=save(`production/${APPEND_RELEASE}/${id}/render-config.json`,{fixture_only:true}),recipe=save(`production/${APPEND_RELEASE}/${id}/recipe.json`,{source_glb_sha256:glbPin.sha256,rendered_unchanged_source:true,files:[glbPin]});
  const final_posters={route:'blender-detail-preview-wheel-v1',source_glb_sha256:glbPin.sha256,browser_capture:true,recipe,detail:{...detail,render_config:config},wheel:{...wheel,render_config:config,capture_report:save(`production/${APPEND_RELEASE}/${id}/capture.json`,{fixture_only:true}),visual_review:save(`production/${APPEND_RELEASE}/${id}/visual.json`,{fixture_only:true}),wheelSpec:{fixture_only:true}}};
  const e={schema_version:1,kind:'compact-typed-production-release-v1',asset_id:id,revision:'r001',productionAccepted:true,maker:{id:'synthetic-maker-'+id,task_id:'/root/synthetic-maker-'+id},blocking_findings:[],legacy_record:{mutated:false,approval_rewritten:false},roles:{finalGLB:glbPin,finalBlend:blendPin,...Object.fromEntries(['brief','config','references','generator','dependency-list'].map(role=>[role,save(`production/${APPEND_RELEASE}/${id}/${role}.json`,{fixture_only:true,role})]))},typed_compatibility:save(`production/${APPEND_RELEASE}/${id}/compatibility.json`,{kind:'compact-model-task-static4-split-source-v1',asset_id:id,revision:'r001',production_acceptance_created:false,legacy_records_mutated:false,publication_authorized:false}),source_availability:{kind:'static4-exact-source-and-derived-dependencies-v1'},build_closure:[glbPin,blendPin],preview,preview_provenance:{source_glb_sha256:glbPin.sha256,route:'fresh_final_glb_poster',independently_reviewed_original_preview:false},final_posters,postReleaseVerified:{status:'NOT_PUBLISHED'}};
  const record={version:1,id,asset,catalog:{pack_ids:[APPEND_RELEASE],legacy_pack_ids:[]},gallery:{poster:{detail:detail.path.slice(12),wheel:wheel.path.slice(12),source_glb_sha256:glbPin.sha256,render_route:final_posters.route,wheelSpec:final_posters.wheel.wheelSpec},files:[detail,wheel].map(p=>({...p,path:p.path.slice(12)})),wheel_framing:null},turntable:{asset:null,poster:null}};
  records.push(record);evidence.push(e);production.assets.push({id,metadata:save(`production/${APPEND_RELEASE}/${id}/metadata.json`,asset),evidence:save(`production/${APPEND_RELEASE}/${id}/evidence.json`,e)});
 }
 const productionReview={schema_version:1,kind:'independent-production-projection-review-v1',status:'PASS',reviewer,checks:Object.fromEntries(contentChecks.map(k=>[k,'PASS'])),blocking_findings:[],publication_authorized:false};
 const descriptor={schema_version:1,kind:'same-id-successor-append-v1',release_id:APPEND_RELEASE,baseline_commit:APPEND_BASELINE,producer,selection:APPEND_SELECTION_PIN,base_manifest:APPEND_ROOT_PIN,base_count:602,entries:[],content_releases:[],review_path:`production/${APPEND_RELEASE}/append-review.json`,...flags};
 const review={schema_version:1,kind:'independent-same-id-successor-append-review-v1',status:'PASS',reviewer,selection_sha256:APPEND_SELECTION_PIN.sha256,base_manifest_sha256:APPEND_ROOT_PIN.sha256,new_ids:[...APPEND_IDS],checks:Object.fromEntries(APPEND_CHECKS.map(k=>[k,'PASS'])),blocking_findings:[],...flags};
 let appendPin;
 const resealDescriptor=()=>{appendPin=save(`production/${APPEND_RELEASE}/append.json`,descriptor);review.reviewed_append_sha256=appendPin.sha256;review.record_sha256=descriptor.entries.map(e=>e.record.sha256);review.content_descriptor_sha256=descriptor.content_releases.map(e=>e.descriptor.sha256);save(descriptor.review_path,review);return appendPin;};
 const seal=()=>{
  for(const [i,record]of records.entries()){production.assets[i].metadata=save(production.assets[i].metadata.path,record.asset);production.assets[i].evidence=save(production.assets[i].evidence.path,evidence[i]);}
  descriptor.entries=records.map(r=>({id:r.id,record:save(recordReference(r).path,r)}));
  const p=save(`production/${APPEND_RELEASE}/release.json`,production);productionReview.reviewed_descriptor_sha256=p.sha256;descriptor.content_releases=[{descriptor:p,review:save(production.review_path,productionReview)}];
  return resealDescriptor();
 };
 seal();
 const options=()=>({read,appendPin,selectionPin:APPEND_SELECTION_PIN,legacyBase:rootBase}),selected=()=>{const a=inspectAppendContinuation(options());return selectSuccessorManifest({baseManifest:a.base,selection,selectionPin:APPEND_SELECTION_PIN,appendPin,read});};
 return {files,read,save,records,evidence,production,productionReview,descriptor,review,seal,resealDescriptor,options,selected,get appendPin(){return appendPin;}};
}
test('synthetic19 appends to exact real602 with unchanged old selection and exact three inverse views',()=>{
 const f=fixture(),append=inspectAppendContinuation(f.options()),selected=f.selected();assert.equal(selected.assets.length,621);same(selected.assets.slice(0,602),legacySelected.assets,'old602');assert.deepEqual(selected.assets.slice(602).map(a=>a.id),APPEND_IDS);same(historicalManifestView({manifest:selected,read:f.read}),append.base,'manifest inverse');
 const registry=structuredClone(legacyRegistry);registry.records.push(...f.records);registry.batches.push({version:1,id:APPEND_RELEASE,records:f.records.map(recordReference),evidence:[{path:f.descriptor.content_releases[0].descriptor.path,sha256:f.descriptor.content_releases[0].descriptor.sha256}],definitions:{worlds:[],packs:[{...structuredClone(legacyRegistry.batches.flatMap(b=>b.definitions.packs).at(-1)),id:APPEND_RELEASE}]}});
 assert.deepEqual(assertRegistryAppend(legacyRegistry,registry),APPEND_IDS);
 const options={registry,baseManifest:append.base,selection,selectionPin:APPEND_SELECTION_PIN,appendPin:f.appendPin,read:f.read},output=composeSuccessorRegistry(options),unselected=composeRegistry(registry);
 same(output.manifest,selected,'selected composition');same(historicalGalleryView({manifest:selected,resources:output.gallery,read:f.read}),unselected.gallery,'gallery inverse');same(historicalTurntableView({manifest:selected,turntables:output.turntables,read:f.read}),unselected.turntables,'turntable inverse');
 const badGallery=structuredClone(output.gallery);badGallery.posters[APPEND_IDS[0]].detail='gallery/posters/unlisted.png';assert.throws(()=>historicalGalleryView({manifest:selected,resources:badGallery,read:f.read}),/Appended gallery pointer/);
 const badSeal=structuredClone(output.gallery);badSeal.files.find(row=>row.path===f.records[0].gallery.poster.detail).sha256='0'.repeat(64);assert.throws(()=>historicalGalleryView({manifest:selected,resources:badSeal,read:f.read}),/Appended gallery seal/);
 const badTurns=structuredClone(output.turntables);badTurns.assets.push({id:APPEND_IDS[0]});assert.throws(()=>historicalTurntableView({manifest:selected,turntables:badTurns,read:f.read}),/Appended turntable pointer/);
 const context=successorContext({manifest:selected,read:f.read});assert.equal(context.rootBase.assets.length,602);assert.equal(context.base.assets.length,621);assert.equal(context.entries.length,17);assert.equal(context.append.records.length,19);assert.equal(hashBytes(rootRead(APPEND_SELECTION_PIN.path)),APPEND_SELECTION_PIN.sha256);assert.equal(hashBytes(rootRead(APPEND_ROOT_PIN.path)),APPEND_ROOT_PIN.sha256);
 
 for(const alter of [m=>m.assets[0].triangles++,m=>m.assets.push(structuredClone(m.assets.at(-1))),m=>m.assets.reverse(),m=>m.publication.extra=true]){const bad=structuredClone(selected);alter(bad);assert.throws(()=>historicalManifestView({manifest:bad,read:f.read}),/exact successor selection/);}
});
test('recomputed descriptors reject extra/override/duplicate/reorder/omitted IDs or changed legacy pins',()=>{
 for(const alter of [f=>f.records[0].id='azolla',f=>f.records.reverse(),f=>f.records.pop(),f=>f.descriptor.selection={...APPEND_SELECTION_PIN,sha256:'0'.repeat(64)},f=>f.descriptor.base_manifest={...APPEND_ROOT_PIN,sha256:'0'.repeat(64)},f=>f.descriptor.baseline_commit='0'.repeat(40),f=>f.descriptor.extra=true]){const f=fixture();alter(f);assert.throws(()=>{f.seal();inspectAppendContinuation(f.options());});}
 const extra=fixture();extra.descriptor.entries.push(structuredClone(extra.descriptor.entries[0]));extra.resealDescriptor();assert.throws(()=>inspectAppendContinuation(extra.options()),/ordered new19/);
});
test('root602 extended header, old metadata, order, omission and arbitrary suffix fail closed',()=>{
 const f=fixture(),a=inspectAppendContinuation(f.options());for(const alter of [b=>b.assets[0].triangles++,b=>b.assets.reverse(),b=>b.assets.pop(),b=>b.assets.push({...b.assets.at(-1),id:'extra'}),b=>b.publication.extra=true]){const b=structuredClone(a.base);alter(b);assert.throws(()=>inspectAppendContinuation({...f.options(),extendedBase:b}),/extended base differs/);}
});
test('missing/stale/self/nonpassing reviews and authority flags never append',()=>{
 for(const alter of [f=>f.review.status='PENDING',f=>f.review.reviewer=f.descriptor.producer,f=>f.review.reviewer=f.evidence[0].maker,f=>f.productionReview.reviewer=f.evidence[0].maker,f=>f.review.checks.fresh_current_source_captures='PENDING',f=>f.review.blocking_findings=['blocked'],f=>f.review.publication_authorized=true,f=>f.review.world_accepted=true,f=>f.descriptor.reviewer_authority=true,f=>f.productionReview.status='FAIL',f=>f.productionReview.checks.final_preview_and_posters='PENDING',f=>f.evidence[0].maker.id='unknown',f=>f.review.reviewer={id:'synthetic-preparer',task_id:'synthetic-independent-reviewer'},f=>f.productionReview.reviewer={id:'synthetic-preparer',task_id:'synthetic-independent-reviewer'},f=>f.evidence[0].maker={id:'synthetic-independent-reviewer',task_id:'synthetic-maker-acanthodes'},f=>f.evidence[0].postReleaseVerified.status='PASS']){const f=fixture();alter(f);f.seal();assert.throws(()=>inspectAppendContinuation(f.options()));}
 const missing=fixture();missing.files.set(missing.descriptor.review_path,undefined);assert.throws(()=>inspectAppendContinuation(missing.options()),/Missing independent append review/);
 const stale=fixture();stale.review.reviewed_append_sha256='0'.repeat(64);stale.save(stale.descriptor.review_path,stale.review);assert.throws(()=>inspectAppendContinuation(stale.options()),/Stale append review/);
});
test('recomputed source/preview pins cannot admit wrong source or capture-only assets',()=>{
 for(const alter of [f=>f.evidence[0].productionAccepted=false,f=>f.evidence[0].roles.finalGLB=f.evidence[1].roles.finalGLB,f=>f.evidence[0].preview_provenance.source_glb_sha256='0'.repeat(64),f=>f.evidence[0].final_posters.source_glb_sha256='0'.repeat(64),f=>f.evidence[0].final_posters.browser_capture=false,f=>f.records[0].gallery.poster.source_glb_sha256='0'.repeat(64),f=>f.evidence[0].legacy_record.approval_rewritten=true]){const f=fixture();alter(f);f.seal();assert.throws(()=>inspectAppendContinuation(f.options()));}
 const bytes=fixture();bytes.files.set(bytes.records[0].asset.glb,Buffer.from('changed'));assert.throws(()=>inspectAppendContinuation(bytes.options()),/source\/preview changed/);
 const unsafe=fixture();unsafe.evidence[0].build_closure[0]={path:'../secret',sha256:'0'.repeat(64),bytes:1};unsafe.seal();assert.throws(()=>inspectAppendContinuation(unsafe.options()),/Safe exact append pin/);
});
test('exact original264 union selected19, never arbitrary283; actual new GLB and PNG binding',()=>{
 const f=fixture(),selected=f.selected(),legacyIds=JSON.parse(rootRead('qa/detail-presentation-scope-20261025.json')).cohorts.flatMap(c=>c.assets.map(a=>a.id)),index={presentations:{}};
 for(const id of APPEND_IDS){const record=f.records.find(r=>r.id===id),p=f.save('site/public/detail-presentations/'+id+'.png',png(1536,1536,id));index.presentations[id]={detail:p.path.slice(12),source_glb_sha256:record.asset.sha256.glb,png:p};}
 const append=selectedDetailAppend({manifest:selected,index,read:f.read});assert.deepEqual(append.ids,APPEND_IDS);const ids=[...legacyIds,...append.ids];assert.equal(exactDetailCohorts({legacyIds,appendIds:append.ids,indexIds:ids,affectedIds:ids}).length,283);
 for(const alter of [x=>x[0]='unknown-extra',x=>x.push('extra'),x=>x.pop(),x=>x[0]=x[1]]){const bad=[...ids];alter(bad);assert.throws(()=>exactDetailCohorts({legacyIds,appendIds:append.ids,indexIds:bad,affectedIds:ids}));}
 index.presentations[APPEND_IDS[0]].source_glb_sha256='0'.repeat(64);assert.throws(()=>selectedDetailAppend({manifest:selected,index,read:f.read}),/capture source changed/);
});

test('append uses the existing path reader: symlink and traversal reads reject',()=>{const dir=mkdtempSync(join(tmpdir(),'append-reader-mechanism-'));try{writeFileSync(join(dir,'ordinary.json'),'{}');symlinkSync(join(dir,'ordinary.json'),join(dir,'alias.json'));const read=successorReader(dir);assert.throws(()=>read('alias.json'),/symlink/);assert.throws(()=>read('../ordinary.json'),/Unsafe/);}finally{rmSync(dir,{recursive:true,force:true});}});

test('orphan append flag cannot escape through any historical/context entrypoint',()=>{const manifest={assets:[],publication:{same_id_successor_append:{path:'orphan'}}},read=()=>{throw Error('must not read');};for(const call of [()=>historicalManifestView({manifest,read}),()=>historicalGalleryView({manifest,resources:{},read}),()=>historicalTurntableView({manifest,turntables:{},read}),()=>successorContext({manifest,read})])assert.throws(call,/exact legacy successor selection/);});

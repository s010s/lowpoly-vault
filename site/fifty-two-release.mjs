import {historicalMediaComparison} from './historical-media-comparison.mjs';
import {assertRecordedGalleryRecipe} from './gallery-publication-recipe-compat.mjs';
/** Exact52 source/card preflight plus separate mandatory final-subject gallery gate. */
import assert from 'node:assert/strict';
import {readFile,realpath} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {assetFileAllowlist} from './asset-delivery.mjs';
import {CARD_RENDER_PRESET} from './render-preset.js';
import {posterInputKey,posterSharedInputs} from './gallery-poster-inputs.mjs';
import {digest} from './model-registry.mjs';
export const FIFTY_TWO_IDS = Object.freeze(["arroyo-wash", "badlands-ridge-network", "banded-gneiss-outcrop", "beach-cusp-field", "calamites", "caytonia", "charnia", "chondrites-branching-trace", "cinder-cone", "cloudina", "dickinsonia", "diplopora", "eophyllophyton", "ernietta", "glossopteris", "impact-crater", "inselberg", "kame-mound", "karst-polje", "kimberella", "lava-channel", "lava-tube-entrance", "lumbricaria-thread-like-coprolite", "namacalathus", "nathorstiana", "oncoid-bed", "patterned-stone-circles", "pediment", "pertica", "piedmont-glacier", "planolites-smooth-burrow", "playa-basin", "pseudobornia", "psilophyton", "pterosaur-manus-pes-trackway", "rhacophyton", "rosselia-concentrically-filled-burrow", "sauropod-manus-pes-trackway", "shield-volcano", "sigillaria", "skolithos-pipe-field", "spatter-cone", "spiral-coprolite", "spriggina", "stratovolcano", "teichichnus-spreite-wall", "thrombolite-mound", "tower-karst", "travertine-terrace-pools", "valley-glacier", "volcanic-neck", "zoophycos-spiral-spreite"]);
export const BASELINE295_CANONICAL_SHA256='71c012a78c6da89b58fb35bba49fcb508a7aadbfd42c82a953ce88ce026d7894';
const DESCRIPTOR_PATHS=Array.from({length:22},(_,i)=>`assets/releases/next52-g${String(i+1).padStart(2,'0')}-20261021.json`);
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const sortedIds=rows=>rows.map(row=>row.id).sort();
const passPresentation=value=>['PASS_BOUNDED_PRESENTATION','PASS_BOUNDED_PRESENTATION_R004','PASS_BOUNDED_PRESENTATION_WITH_NONBLOCKING_SHADOW_STIPPLING'].includes(value);
function reader(root) {
 const cache = new Map(), parsed = new Map();
 async function local(path) {
  assert(typeof path === 'string' && !path.split('/').some(p => !p || p === '.' || p === '..'), 'Unsafe release path');
  const absolute = resolve(root,path);
  assert.equal(await realpath(absolute),absolute,`Release symlinks forbidden: ${path}`);
  if (!cache.has(absolute)) cache.set(absolute,await readFile(absolute));
  return cache.get(absolute);
 }
 async function checked(pin) {
  assert(pin && /^(?:(?:assets|production|qa|scripts|schemas|LICENSES)\/[a-zA-Z0-9_./-]+|LICENSE|ATTRIBUTION\.md|package(?:-lock)?\.json)$/.test(pin.path), 'Invalid fixed52 evidence pin');
  assert(/^[a-f0-9]{64}$/.test(pin.sha256), 'Invalid fixed52 SHA-256');
  const bytes = await local(pin.path);
  assert.equal(sha(bytes),pin.sha256,`${pin.path}: exact fixed52 hash mismatch`);
  return bytes;
 }
 async function json(pin) {
  const bytes = await checked(pin), key = `${pin.path}:${pin.sha256}`;
  if (!parsed.has(key)) parsed.set(key,JSON.parse(bytes));
  return parsed.get(key);
 }
 return {local,checked,json};
}
function png(bytes, dimensions, label) {
 assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a',`${label}: PNG signature`);
 assert.deepEqual([bytes.readUInt32BE(16),bytes.readUInt32BE(20)],dimensions,`${label}: PNG dimensions`);
}
function bounded(scope) {
 assert.equal(scope.formal_profile_acceptance,'BLOCKED');
 assert.equal(scope.hardware_gpu_verified,false);
 assert.equal(scope.target_scene_verified,false);
}

function finalAsset(metadata,entry,release){
 return {...metadata,quality_status:'independent_qa_accepted_stylized_prop',approval_provenance:{
  source_commit:entry.reviewed_source_commit,review_commit:release.review_commit,
  review_sha256:entry.active_review.sha256,active_candidate:entry.active_candidate,
  delivery_source_commit:release.source_commit,original_lean_snapshot:entry.original_source_snapshot,
  source_contract:'bounded-stylized-study:8-fixed-views; pending static-stylized-v1 candidate; original records preserved',
  candidate_record_approved_for_brief:false,formal_profile_acceptance:'BLOCKED',hardware_gpu_verified:false,target_scene_verified:false,
  concept_chronology:'Exact provider generation timestamp unknown; original evidence preserved',
 }};
}
/** Immutable fixed52 consistency check. This does not authorize publication. */
export async function preflightFiftyTwoAdditions(root,descriptors){
 const {FIFTY_TWO_RELEASES:fixed}=await import('./accepted-fifty-two-release.mjs');
 assert.deepEqual(descriptors.map(pin=>pin.path),DESCRIPTOR_PATHS,'Only the exact22 fixed52 descriptors are allowed');
 assert.equal(fixed.length,22);
 const {local,checked,json}=reader(root),releases=[],additions=[],viewerHash=sha(await local('site/viewer.js'));
 for(let k=0;k<fixed.length;k++){
  assert.deepEqual(descriptors[k],fixed[k].descriptor,'Only exact fixed52 descriptor pins are allowed');
  const release=await json(descriptors[k]);assert.deepEqual(release,fixed[k].release,'Only fixed independently reviewed52 bytes and bounded claims are authorized');
  assert.equal(release.scope,`next52-g${String(k+1).padStart(2,'0')}-release-20261021`);
  assert.equal(release.authorization,'owner_authorized_fixed52_after_required_checks');assert.equal(release.acceptance_scope,'independent_qa_accepted_stylized_prop');
  bounded(release);assert.equal(release.provider_generation_timestamp,'unknown');
  for(const key of ['source_commit','review_commit'])assert(/^[a-f0-9]{40}$/.test(release[key]));
  const groupKey=r=>`${r.source_commit}:${dirname(r.additions[0].active_review.path)}`;
  assert(release.additions.every(e=>dirname(e.active_review.path)===dirname(release.additions[0].active_review.path)),'Each archive group requires one exact original active-review scope');
  if(k)assert(groupKey(releases[k-1])<groupKey(release),'Source/review groups must remain in fixed sorted order');releases.push(release);
  const policy=await json(release.publication_policy);assert.equal(policy.scope,'s010s/lowpoly-vault');assert.equal(policy.authority,'owner_authorized_qa_passed_batch_release');assert.equal(policy.candidate_gate_grants_publication,false);
  const bundle=await json(release.source_bundle);assert.equal(bundle.version,1);assert.equal(new Set(bundle.files.map(pin=>pin.path)).size,bundle.files.length);
  assert.deepEqual(bundle.files.map(({path,sha256})=>({path,sha256})),release.files.map(({path,sha256})=>({path,sha256})));
  for(const pin of [...bundle.files,...release.protected_source_inputs,...release.independent_reviews])await checked(pin);
  const capture=await json(release.capture.report),index=await json(release.capture.index),inputs=await json(release.capture.original_inputs),verification=await json(release.capture.artifact_verification),review=await json(release.capture.independent_review),reviewInputs=await json(release.capture.review_inputs),original=await json(release.capture.original_fixed52),identity=await json(release.capture.source_identity_mapping),aliases=await json(release.capture.profile_policy_aliases);
  await checked(release.capture.reviewer_evidence);await checked(release.capture.historical_concepts);
  assert.equal(sha(await local(release.capture.original_fixed52.path)),'01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac');
  assert.equal(capture.status,'pass');assert.equal(capture.target_renderer,'threejs-modelstage');assert.equal(capture.viewer_source_sha256,viewerHash);assert.equal(capture.render_preset_sha256,sha(JSON.stringify(CARD_RENDER_PRESET)));
  assert.equal(capture.chromium_version,capture.pinned_chromium_version);assert.equal(capture.chromium_version,'141.0.7390.37');
  assert.deepEqual(sortedIds(capture.assets),FIFTY_TWO_IDS);assert.deepEqual(inputs.selected_ids,FIFTY_TWO_IDS);assert.deepEqual(sortedIds(inputs.assets),FIFTY_TWO_IDS);
  assert.equal(verification.status,'PASS_EXACT_CARD_ARTIFACT_BINDING_NOT_VISUAL_ACCEPTANCE');
  for(const key of ['zip_matches_github_digest_and_size','entry_bytes_match_local_directory','source_glbs_match'])assert.equal(verification[key],true);
  assert.equal(verification.count,52);assert.equal(verification.actual_png_count,52);assert.equal(verification.card_webp_count,52);assert.equal(verification.gallery_png_count,0);assert.equal(verification.publication_authority,false);
  assert.equal(verification.capture_inputs_sha256,release.capture.original_inputs.sha256);assert.deepEqual(review.scope,reviewInputs.scope);assert.equal(review.input_manifest_sha256,release.capture.review_inputs.sha256);
  for(const key of ['head_sha','run_id','artifact_id','zip_sha256','zip_bytes','viewer_source_sha256','render_preset_sha256'])assert.equal(review.scope[key],verification[key]);
  assert.equal(reviewInputs.verification.sha256,release.capture.artifact_verification.sha256);assert.deepEqual(sortedIds(review.models),FIFTY_TWO_IDS);assert.deepEqual(sortedIds(verification.models),FIFTY_TWO_IDS);assert.equal(new Set(index.posters.map(r=>r.id)).size,index.posters.length);
  assert.deepEqual(original.assets.map(a=>a.asset_id).sort(),FIFTY_TWO_IDS);assert.deepEqual(identity.models.map(a=>a.id).sort(),FIFTY_TWO_IDS);
  for(const alias of aliases.mappings){
   assert.equal(alias.canonical_path,'production/policies/qa-passed-batch-publication-20261018.json');assert.equal(alias.sha256,release.publication_policy.sha256);
   assert.equal(alias.old_snapshot_alias_existed,false);assert.equal(alias.profile_changed,false);
   assert.deepEqual(await checked(alias.delivered_alias),await checked(release.publication_policy),'Policy alias must have the exact original canonical bytes');
  }
  for(const entry of release.additions){
   assert(FIFTY_TWO_IDS.includes(entry.id),'An asset outside exact fixed52 scope is forbidden');assert.equal(entry.accepted_disposition,'ACCEPT BOUNDED');assert.equal(entry.source_commit,release.source_commit);assert.equal(entry.review_commit,release.review_commit);
   const source=original.assets.find(a=>a.asset_id===entry.id),mapping=identity.models.find(a=>a.id===entry.id);
   assert.equal(entry.revision,source.revision);assert.equal(entry.original_source_snapshot,source.source_snapshot_for_release);assert.equal(entry.reviewed_source_commit,source.source_model_commit);assert.equal(mapping.original_source_snapshot,entry.original_source_snapshot);assert.equal(mapping.public_delivery_source_commit,release.source_commit);
   const a=await json(entry.metadata),candidate=await json(entry.active_candidate);assert.deepEqual(entry.candidate,entry.active_candidate);assert.equal(a.id,entry.id);assert.equal(candidate.asset_id,a.id);assert.equal(candidate.revision,entry.revision);assert.equal(candidate.approval.status,'pending');
   assert.deepEqual(Object.keys(candidate.stages).sort(),['factual','gpu','runtime_parse','scene','specification','technical','visual']);assert.deepEqual(Object.fromEntries(Object.entries(candidate.stages).map(([key,value])=>[key,value.status])),entry.original_stage_statuses,'Original candidate stage history is frozen, not rewritten');
   const folder=`assets/additions/${entry.id}/batch${entry.batch}-20261021`;assert.equal(entry.metadata.path,`${folder}/release-metadata.json`);assetFileAllowlist({assets:[a]});
   assert.equal(a.license,'CC-BY-4.0');assert.equal(a.author,'Leon Made This / s010s');assert.equal(a.units,'meters');assert.deepEqual(a.worlds,['prehistoric']);assert.deepEqual(a.packs,[`prehistoric-batch${entry.batch}-20261021`]);
   for(const key of ['name','description','scientific_scope'])for(const lang of ['en','zh'])assert(a[key]?.[lang]?.trim());
   for(const key of ['quality_status','approval_provenance','candidate_record','qa','publication_status','downloads','turntable','card_preview','profile','validation_profile','approval'])assert(!Object.hasOwn(a,key),`Reserved metadata ${key}`);
   for(const key of ['glb','blend','preview']){assert.equal(dirname(a[key]),folder);const bytes=await checked({path:a[key],sha256:a.sha256[key]});if(key==='glb')assert.equal(bytes.length,a.glb_bytes);}
   assert.equal(candidate.artifacts.glb.sha256,a.sha256.glb);assert.equal(candidate.artifacts.source.sha256,a.sha256.blend);assert.equal(source.artifact_bindings.glb.sha256,a.sha256.glb);assert.equal(source.artifact_bindings.source.sha256,a.sha256.blend);
   for(const pin of [...Object.values(candidate.artifacts),...candidate.evidence,...Object.values(candidate.raw_checks??{})])await checked(pin);
   if(candidate.supersedes)await checked(candidate.supersedes);
   const profile=await json(entry.active_profile);assert.deepEqual(profile.candidate,entry.active_candidate);assert.equal(profile.validation_profile,'static-stylized-v1');await checked(profile.publication_policy);const originalProfile=await json(entry.original_profile);if(entry.active_profile.path!==entry.original_profile.path){const audit=await json(release.capture.release_coordination_profiles),record=audit.models.find(x=>x.id===a.id);assert(record);assert.deepEqual(record.original_profile,entry.original_profile);assert.deepEqual(record.release_coordination_profile,entry.active_profile);assert.deepEqual(record.candidate,entry.active_candidate);for(const [field,value]of Object.entries(record.unchanged_fields)){assert.deepEqual(profile[field],value);assert.deepEqual(originalProfile[field],value);}assert.equal(record.runs[0].exit_code,1);assert.deepEqual(record.runs[0].result.errors,['profile contract: invalid separate publication policy']);assert.equal(record.runs[1].exit_code,0);assert.equal(record.runs[1].result.valid,true);assert.equal(record.runs[1].result.approved_for_brief,false);assert.deepEqual(profile.publication_policy,release.publication_policy);await checked(record.original_policy);}
   const native=await json(release.capture.native_current_profiles);assert.equal(native.count,52);assert.equal(native.original_maker_policy_failures_preserved,2);const outcome=native.rows.find(x=>x.id===a.id);assert.equal(outcome.profile_path,entry.active_profile.path);assert.equal(outcome.exit_code,0);assert.equal(outcome.result.valid,true);assert.equal(outcome.result.approved_for_brief,false);assert.deepEqual(outcome.result.errors,[]);for(const [role,pin]of Object.entries(candidate.artifacts))assert.equal(outcome.result.artifact_sha256[role],pin.sha256);
   assert.equal(entry.active_candidate.path,`${entry.candidate_root}/candidate.json`);
   assert.deepEqual(a.source_identity.candidate,entry.active_candidate);assert.equal(a.source_identity.revision,entry.revision);assert.equal(a.source_identity.batch,entry.batch);assert.equal(a.source_identity.model_commit,entry.reviewed_source_commit);assert.equal(a.source_identity.qa_commit,entry.review_commit);assert.equal(a.source_identity.original_lean_snapshot,entry.original_source_snapshot);assert.equal(a.source_identity.delivery_source_commit,release.source_commit);
   assert.equal(a.source_url,mapping.source_url);assert.equal(a.source_url,`https://github.com/s010s/lowpoly-vault/tree/${release.source_commit}/${entry.candidate_root}`);
   assert.deepEqual(entry.review,entry.active_review);await checked(entry.active_review);assert.deepEqual(a.source_identity.active_review,entry.active_review);assert.deepEqual(a.source_identity.required_independent_reviews,entry.required_qa_documents);for(const pin of entry.required_qa_documents)await checked(pin);
   const metrics=await json(entry.original_metrics),counts=await json(entry.source_counts);if(metrics.glb&&typeof metrics.glb==='object'){assert.equal(metrics.glb.sha256,a.sha256.glb);assert.equal(metrics.glb.scene_triangles,a.triangles);assert.deepEqual(metrics.measured_glb_xyz_m,a.dimensions);assert.deepEqual(metrics.glb.bounds_m,a.bounds_glb_m);assert.equal(metrics.glb.materials,a.material_count);assert.equal(metrics.glb.scene_primitives_estimated_base_draw_calls,a.primitives);}else{assert.equal(metrics.sha256.glb,a.sha256.glb);assert.equal(metrics.triangles,a.triangles);assert.deepEqual(metrics.dimensions,a.dimensions);}
   assert.equal(counts.source_sha256??counts.source_blend_sha256,a.sha256.blend);const totals=counts.totals??counts;if(totals.authored_vertices!==undefined){assert.equal(totals.authored_vertices,a.authored_source_vertices);assert.equal(totals.evaluated_vertices,a.evaluated_source_vertices);}else{assert.equal(counts.objects.reduce((n,x)=>n+x.authored_vertices,0),a.authored_source_vertices);assert.equal(counts.objects.reduce((n,x)=>n+x.evaluated_vertices,0),a.evaluated_source_vertices);}
   const brief=await json(candidate.artifacts.brief);assert.equal(brief.asset_id,a.id);assert.equal(brief.turntable_frames,0);assert.equal(brief.required_views.length,8);
   assert(candidate.evidence.some(e=>e.path===entry.proof.path&&e.sha256===entry.proof.sha256));const proof=await json(entry.proof);assert.deepEqual(proof.subject,{revision:entry.revision,glb_sha256:a.sha256.glb,brief_sha256:candidate.artifacts.brief.sha256,references_sha256:candidate.artifacts.references.sha256});assert.equal(proof.source_glb_sha256,a.sha256.glb);assert.equal(proof.frames.length,8);assert.equal(new Set(proof.frames.map(f=>f.path)).size,8);
   for(const frame of proof.frames){const bytes=await checked({path:`${dirname(entry.proof.path)}/${frame.path}`,sha256:frame.sha256});assert.equal(bytes.length,frame.bytes);png(bytes,[frame.width,frame.height],`${a.id}: source fixed8`);}
   await checked(entry.source_preview);
   const oldMetadata=await json(entry.capture_input_metadata),input=inputs.assets.find(x=>x.id===a.id),card=index.posters.find(x=>x.id===a.id),visual=review.models.find(x=>x.id===a.id),binding=verification.models.find(x=>x.id===a.id),originalPng=verification.pngs.find(x=>x.id===a.id);
   assert.equal(input.metadata.path,entry.metadata.path);assert.equal(input.metadata.sha256,entry.capture_input_metadata.sha256);assert.equal(binding.input_metadata_sha256,input.metadata.sha256);assert.equal(oldMetadata.id,a.id);assert.equal(oldMetadata.sha256.glb,a.sha256.glb);assert.equal(oldMetadata.sha256.preview,null);assert.equal(oldMetadata.preview_capture.status,'not_run');
   for(const value of [card.source_glb_sha256,visual.source_glb_sha256,binding.source_glb_sha256,capture.assets.find(x=>x.id===a.id).source_glb_sha256])assert.equal(value,a.sha256.glb);
   assert.equal(card.render_preset_sha256,capture.render_preset_sha256);assert.equal((await checked({path:card.path,sha256:card.sha256})).length,card.bytes);
   const reference=await checked(entry.capture_reference);png(reference,[768,768],`${a.id}: card reference`);assert.equal(entry.capture_reference.sha256,a.sha256.preview);assert.equal(originalPng.sha256,a.sha256.preview);assert.equal(originalPng.bytes,reference.length);
   assert.equal(visual.verdict,'PASS_BOUNDED_CARD_PRESENTATION');assert.equal(visual.original_png_viewed,true);assert.equal(visual.view_detail,'original');assert.deepEqual(visual.view_resolution,[768,768]);assert.deepEqual(visual.blocking_issues,[]);assert.equal(visual.png_sha256,a.sha256.preview);assert.equal(visual.webp_sha256,card.sha256);assert.equal(visual.input_metadata_sha256,input.metadata.sha256);
   assert.equal(a.preview_capture.status,'original_pixels_independently_reviewed_bounded_card_pass');assert.deepEqual(a.preview_capture.original_capture_metadata,entry.capture_input_metadata);assert.deepEqual(a.preview_capture.independent_card_review,release.capture.independent_review);assert.equal(a.preview_capture.capture_head,verification.head_sha);assert.equal(a.preview_capture.run_id,verification.run_id);assert.equal(a.preview_capture.artifact_id,verification.artifact_id);assert.equal(a.preview_capture.final_metadata_generation_proof,false);
   additions.push(finalAsset(a,entry,release));
  }
 }
 assert.deepEqual(sortedIds(additions),FIFTY_TWO_IDS,'Exact fixed52 membership, no missing/duplicate/extra models');return {releases,additions,publication_ready:false};
}
/** Shared by the publication gate and its negative tests. No re-signing or compatibility exception. */
export function assertFiftyTwoGallerySubjects(receipt,additions) {
 assert.deepEqual(sortedIds(additions),FIFTY_TWO_IDS,'Final gallery requires exact fixed52 assets');
 assert.deepEqual(receipt.selected_ids,FIFTY_TWO_IDS,'Final gallery selection must be exactly52, never the card-only');
 assert.deepEqual(sortedIds(receipt.rows),FIFTY_TWO_IDS,'Final gallery receipt must contain exactly52 rows');
 assert.equal(receipt.status,'pass'); assert.deepEqual(receipt.errors,[]);
 assert(/^[a-f0-9]{40}$/.test(receipt.head_sha),'Final gallery requires a valid capture head');
 assert.equal(receipt.physical_gpu_verified,false); assert.equal(receipt.target_scene_verified,false);
 assert.equal(receipt.formal_acceptance,'BLOCKED');
 for (const asset of additions) {
  const row = receipt.rows.find(item => item.id === asset.id);
  assert.equal(row.source_glb_sha256,asset.sha256.glb); assert.equal(row.poster.source_glb_sha256,asset.sha256.glb);
  assert.equal(row.poster.input_sha256,posterInputKey(asset,receipt.shared),`${asset.id}: final gallery subject mismatch; recapture final metadata, do not re-sign original pixels`);
  assert.equal(row.poster.browser_version,receipt.shared.browser);
 }
}

export async function collectFiftyTwoAdditions(root,descriptors) {
 const result = await preflightFiftyTwoAdditions(root,descriptors), {releases,additions} = result;
 const {local,checked,json} = reader(root), capture = releases[0].capture;
 for (const release of releases) for (const key of ['final_gallery_receipt','final_gallery_review','final_gallery_artifact_verification']) {
  assert(release.capture[key],`Fixed52 final gallery subject mismatch: ${key} is pending; card-only metadata cannot authorize final52 publication`);
  assert.deepEqual(release.capture[key],capture[key],'All fixed52 groups must bind the same final gallery evidence');
 }
 const receipt = await json(capture.final_gallery_receipt);
 assertFiftyTwoGallerySubjects(receipt,additions);
 await assertRecordedGalleryRecipe(receipt.shared,root);
 const verification = await json(capture.final_gallery_artifact_verification), review = await json(capture.final_gallery_review);
 assert.equal(verification.zip_matches_github_digest_and_size,true); assert.equal(verification.entry_bytes_match_local_directory,true);
 assert.equal(verification.head_sha,receipt.head_sha); assert.equal(String(verification.run_id),String(receipt.run_id));
 assert(/^[a-f0-9]{64}$/.test(verification.zip_sha256)); assert(Number.isSafeInteger(verification.artifact_id) && verification.artifact_id > 0);
 assert.equal(review.status,'accepted_for_scoped_website_delivery_only');
 assert.equal(review.independent_review_sources?.length,3,'Original independent review evidence must remain complete');
 for(const source of review.independent_review_sources)await checked(source);
 const originalReview=await json(review.independent_review_sources[0]);
 assert.equal(originalReview.status,'PASS_BOUNDED_PRESENTATION');assert.deepEqual(sortedIds(originalReview.models),FIFTY_TWO_IDS);
 assert.equal(originalReview.summary.original_pngs_actually_viewed,104);assert.equal(originalReview.summary.HOLD,0);assert.equal(originalReview.summary.REVISE,0);
 assert.equal(originalReview.capture_head,receipt.head_sha);assert.equal(String(originalReview.run_id),String(receipt.run_id));assert.equal(originalReview.artifact_id,verification.artifact_id);assert.equal(originalReview.zip_sha256,verification.zip_sha256);assert.equal(originalReview.receipt.sha256,capture.final_gallery_receipt.sha256);
 for(const mapped of review.models){const original=originalReview.models.find(row=>row.id===mapped.id);assert.equal(mapped.result,original.result);assert.equal(mapped.source_glb_sha256,original.source_glb_sha256);assert.deepEqual(mapped.observation,original.observation);assert.deepEqual(mapped.blocking_findings,original.blocking_findings);assert.deepEqual(mapped.limitations_and_nonblocking_observations,original.limitations_and_nonblocking_observations);for(const f of mapped.original_pngs){const old=original.original_pngs.find(x=>x.kind===f.kind);for(const key of ['sha256','bytes','dimensions','original_pixels_independently_reviewed'])assert.deepEqual(f[key],old[key],'Independent review mapping must not alter observed evidence');}}

 assert.equal(review.capture_head,receipt.head_sha); assert.equal(String(review.run_id),String(receipt.run_id));
 assert.equal(review.artifact_id,verification.artifact_id); assert.equal(review.zip_sha256,verification.zip_sha256);
 assert.deepEqual(review.receipt,capture.final_gallery_receipt);
 assert.equal(review.hardware_gpu_verified,false); assert.equal(review.target_scene_verified,false); assert.equal(review.formal_acceptance,'BLOCKED');
 assert.deepEqual(sortedIds(review.models),FIFTY_TWO_IDS);
 const gallery = JSON.parse(await local('site/public/gallery/resources.json'));
 const publicIndex = JSON.parse(await local('assets/turntables/index.json'));
 const media = historicalMediaComparison({root,turntables:publicIndex,gallery});
 const originalIndex = await json(capture.index);
 for (const asset of additions) {
  const pair = receipt.rows.find(row => row.id === asset.id), visual = review.models.find(row => row.id === asset.id);
  assert.deepEqual(media.cardRows(asset.id,originalIndex.posters.filter(row => row.id === asset.id)),originalIndex.posters.filter(row => row.id === asset.id),'Public card must equal the original exact-renderer card');
  assert(passPresentation(visual.result)); assert.equal(visual.source_glb_sha256,asset.sha256.glb);
  assert.deepEqual(visual.original_pngs.map(row => row.kind),['detail','wheel']);
  assert.deepEqual(media.galleryPoster(asset.id,pair.poster),pair.poster);
  assert.deepEqual(pair.files.map(file => file.path).sort(),[`gallery/posters/${asset.id}-wheel.png`,`gallery/posters/${asset.id}.png`].sort());
  for (const kind of ['detail','wheel']) {
   const path = `gallery/posters/${asset.id}${kind === 'wheel' ? '-wheel' : ''}.png`;
   assert.equal(pair.poster[kind],path);
   const file = pair.files.find(row => row.path === path), inspected = visual.original_pngs.find(row => row.kind === kind);
   const bytes = await local(`site/public/${path}`), dimensions = kind === 'detail' ? [512,512] : [768,432];
   assert.equal(sha(bytes),file.sha256); assert.equal(bytes.length,file.bytes); png(bytes,dimensions,`${asset.id}: final ${kind}`);
   assert.deepEqual(gallery.files.filter(row => row.path === path),[file]);
   assert.equal(inspected.sha256,file.sha256); assert.equal(inspected.bytes,file.bytes); assert.deepEqual(inspected.dimensions,dimensions);
   assert.equal(inspected.original_pixels_independently_reviewed,true);
  }
 }
 return {releases,additions};
}


export function assertFiftyTwoBaseline(base){
 assert.equal(base.assets?.length,295,'Fixed52 append requires exact295 baseline');
 assert.equal(digest(base),BASELINE295_CANONICAL_SHA256,'Fixed52 baseline295 complete canonical object changed');
 assert(!base.assets.some(a=>FIFTY_TWO_IDS.includes(a.id)),'Fixed52 cannot replace old assets');
}
export async function appendFiftyTwoRelease(root,base,descriptors){
 assertFiftyTwoBaseline(base);const before=JSON.stringify(base),{additions}=await collectFiftyTwoAdditions(root,descriptors);
 assert.equal(JSON.stringify(base),before,'Entire baseline295 must remain unchanged');
 const result={...base,assets:[...base.assets,...additions],publication:{...base.publication,fifty_two_descriptors:descriptors}};
 assert.equal(result.assets.length,347);assert.deepEqual(result.assets.slice(0,295),base.assets);return result;
}

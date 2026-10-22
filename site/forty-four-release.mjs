import {assertRecordedGalleryRecipe} from './gallery-publication-recipe-compat.mjs';
/** Exact 44-model append. Historical presentation review is not final-subject generation proof. */
import assert from 'node:assert/strict';
import {readFile, realpath} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {assetFileAllowlist} from './asset-delivery.mjs';
import {CARD_RENDER_PRESET} from './render-preset.js';
import {posterInputKey, posterSharedInputs} from './gallery-poster-inputs.mjs';

export const FORTY_FOUR_IDS = Object.freeze([
 'arete-ridge','baiera','banded-iron-formation','breccia-outcrop','coal-seam-outcrop',
 'desert-pavement','dike-wall','eldonia','eruptive-fissure','exfoliation-dome','fractofusus',
 'fumarole-vent','geode-cavity','glacial-horn','hanging-valley','hoodoo',
 'ice-wedge-polygon-ground','lava-dome','linear-dune','loess-bluff','louisella','maar-crater',
 'moulin-shaft','mudpot','parvancorina','pingo','pteridinium','rangea','rimstone-dam',
 'river-terrace','roche-moutonnee','rock-glacier','sandstone-fin','serac','sill-ledge',
 'slump-folded-bed','solifluction-lobe','stalagmite-group','striated-bedrock','thaumaptilon',
 'transverse-dune-ridge','tribrachidium','waputikia','wiwaxia',
]);
const EXCLUDED_IDS = ['braided-river-reach','crevasse-splay','kettle-basin'];
const STATIC_ONLY_IDS = ['eruptive-fissure','exfoliation-dome','glacial-horn','loess-bluff','moulin-shaft','parvancorina','pingo','pteridinium','rangea','rock-glacier','serac','sill-ledge','slump-folded-bed','solifluction-lobe'];
const ORIGINAL_IDS = [...FORTY_FOUR_IDS, ...EXCLUDED_IDS].sort();
const DESCRIPTOR_PATHS = Array.from({length:16}, (_,i) => `assets/releases/next44-g${String(i+1).padStart(2,'0')}-20261020.json`);
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const sortedIds = rows => rows.map(row => row.id).sort();
const passPresentation = value => ['PASS_BOUNDED_PRESENTATION','PASS_BOUNDED_PRESENTATION_R004','PASS_BOUNDED_PRESENTATION_WITH_NONBLOCKING_SHADOW_STIPPLING'].includes(value);

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
  assert(pin && /^(?:(?:assets|production|qa|scripts|schemas|LICENSES)\/[a-zA-Z0-9_./-]+|LICENSE|ATTRIBUTION\.md|package(?:-lock)?\.json)$/.test(pin.path), 'Invalid fixed44 evidence pin');
  assert(/^[a-f0-9]{64}$/.test(pin.sha256), 'Invalid fixed44 SHA-256');
  const bytes = await local(pin.path);
  assert.equal(sha(bytes),pin.sha256,`${pin.path}: exact fixed44 hash mismatch`);
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
function finalAsset(metadata,entry,release) {
 return {...metadata,quality_status:'independent_qa_accepted_stylized_prop',approval_provenance:{
  source_commit:entry.reviewed_source_commit,review_commit:release.review_commit,
  review_sha256:entry.active_review.sha256,active_candidate:entry.active_candidate,
  source_contract:'bounded-stylized-study:8-fixed-views; pending static-stylized-v1 candidate; historical records preserved',
  candidate_record_approved_for_brief:false,formal_profile_acceptance:'BLOCKED',
  hardware_gpu_verified:false,target_scene_verified:false,
  concept_chronology:'Exact provider generation timestamp unknown; original evidence preserved',
 }};
}

/** Source/card staging only. This result never grants publication or skips the final gallery gate. */
export async function preflightFortyFourAdditions(root,descriptors) {
 const {FORTY_FOUR_RELEASES:fixed} = await import('./accepted-forty-four-release.mjs');
 assert.deepEqual(descriptors.map(pin => pin.path),DESCRIPTOR_PATHS,'Only the exact 16 fixed44 descriptors are allowed');
 assert.equal(fixed.length,16);
 const {local,checked,json} = reader(root), releases = [], additions = [];
 const viewerHash = sha(await local('site/viewer.js'));
 for (let k=0;k<fixed.length;k++) {
  const accepted = fixed[k].release, release = await json(descriptors[k]);
  assert.deepEqual(descriptors[k],fixed[k].descriptor,'Only the exact fixed44 descriptor pins are allowed');
  assert.deepEqual(release,accepted,'Only fixed independently reviewed forty-four bytes and bounded claims are authorized');
  assert.equal(release.scope,`next44-g${String(k+1).padStart(2,'0')}-release-20261020`);
  assert.equal(release.acceptance_scope,'independent_qa_accepted_stylized_prop');
  bounded(release); assert.equal(release.provider_generation_timestamp,'unknown');
  assert(/^[a-f0-9]{40}$/.test(release.source_commit));
  assert.equal(release.source_commit,release.review_commit);
  if (k) assert(releases[k-1].source_commit < release.source_commit,'Source snapshots must remain in fixed sorted order');
  releases.push(release);
  const policy = await json(release.publication_policy);
  assert.equal(policy.authority,'owner_authorized_qa_passed_batch_release');
  assert.equal(policy.candidate_gate_grants_publication,false);
  const bundle = await json(release.source_bundle);
  assert.equal(bundle.version,1);
  assert.equal(bundle.files.length,release.files.length);
  assert.equal(new Set(bundle.files.map(pin => pin.path)).size,bundle.files.length);
  assert.deepEqual(bundle.files.map(({path,sha256}) => ({path,sha256})),release.files.map(({path,sha256}) => ({path,sha256})));
  for (const pin of bundle.files) await checked(pin);
  for (const pin of release.protected_source_inputs) await checked(pin);
  for (const pin of release.independent_reviews) await checked(pin);

  const capture = await json(release.capture.report), index = await json(release.capture.index);
  const original = await json(release.capture.original_gallery_receipt);
  const inputs = await json(release.capture.original_inputs);
  const review = await json(release.capture.independent_review);
  const verification = await json(release.capture.artifact_verification);
  const subset = await json(release.capture.subset);
  assert.equal(capture.status,'pass'); assert.equal(capture.target_renderer,'threejs-modelstage');
  assert.equal(capture.viewer_source_sha256,viewerHash);
  assert.equal(capture.render_preset_sha256,sha(JSON.stringify(CARD_RENDER_PRESET)));
  assert.equal(capture.chromium_version,capture.pinned_chromium_version);
  assert.equal(capture.chromium_version,'141.0.7390.37');
  assert.deepEqual(sortedIds(capture.assets),ORIGINAL_IDS);
  assert.equal(new Set(index.posters.map(row => row.id)).size,index.posters.length);
  assert.deepEqual(sortedIds(index.posters.filter(row => ORIGINAL_IDS.includes(row.id))),ORIGINAL_IDS);
  assert.deepEqual(inputs.selected_ids,ORIGINAL_IDS);
  assert.deepEqual(sortedIds(inputs.assets),ORIGINAL_IDS);
  assert.deepEqual(original.selected_ids,ORIGINAL_IDS);
  assert.deepEqual(sortedIds(original.rows),ORIGINAL_IDS);
  assert.equal(original.status,'pass'); assert.deepEqual(original.errors,[]);
  assert.equal(original.physical_gpu_verified,false); assert.equal(original.target_scene_verified,false);
  assert.equal(original.formal_acceptance,'BLOCKED');
  assert.equal(verification.status,'PASS_EXACT_ARTIFACT_BINDING_NOT_VISUAL_ACCEPTANCE');
  assert.equal(verification.zip_matches_github_digest_and_size,true);
  assert.equal(verification.entry_bytes_match_local_directory,true);
  assert.equal(verification.source_glbs_match,true); assert.deepEqual(verification.runtime_errors,[]);
  assert.equal(verification.publication_authority,false);
  assert.equal(verification.head_sha,original.head_sha);
  assert.equal(String(verification.run_id),String(original.run_id));
  assert.equal(verification.capture_inputs_sha256,release.capture.original_inputs.sha256);
  assert.equal(original.manifest_sha256,release.capture.original_inputs.sha256);
  assert.equal(verification.shared_sha256,original.shared.sha256);
  assert.equal(review.status,'COMPLETE_ORIGINAL_PNG_REVIEW_44_PASS_2_HOLD_1_PENDING');
  assert.equal(review.scope.head_sha,verification.head_sha);
  assert.equal(review.scope.artifact_id,verification.artifact_id);
  assert.equal(review.scope.zip_sha256,verification.zip_sha256);
  assert.equal(review.binding_verification.sha256,release.capture.artifact_verification.sha256);
  assert.deepEqual(review.accepted_presentation_ids,FORTY_FOUR_IDS);
  assert.deepEqual([...review.hold_ids,...review.pending_ids].sort(),EXCLUDED_IDS);
  assert.equal(subset.count,44);
  assert.deepEqual(subset.assets.map(row => row.asset_id).sort(),FORTY_FOUR_IDS);
  assert.equal(subset.visual_review.sha256,release.capture.independent_review.sha256);
  assert.equal(subset.capture_binding.zip_sha256,verification.zip_sha256);

  for (const entry of release.additions) {
   assert(FORTY_FOUR_IDS.includes(entry.id),'An asset outside the exact fixed44 scope is forbidden');
   assert.equal(entry.accepted_disposition,'ACCEPT BOUNDED');
   assert.equal(entry.source_commit,release.source_commit); assert.equal(entry.review_commit,release.review_commit);
   assert(/^[a-f0-9]{40}$/.test(entry.reviewed_source_commit));
   assert.deepEqual(entry.active_candidate,entry.candidate);
   const a = await json(entry.metadata), candidate = await json(entry.active_candidate);
   const folder = `assets/additions/${entry.id}/batch${entry.batch}-20261020`;
   assert.equal(entry.metadata.path,`${folder}/release-metadata.json`);
   assert.equal(a.id,entry.id); assert.equal(candidate.asset_id,a.id); assert.equal(candidate.revision,entry.revision);
   assert.equal(candidate.approval.status,'pending');
   assert.deepEqual(Object.keys(candidate.stages).sort(),['factual','gpu','runtime_parse','scene','specification','technical','visual']);
   for (const stage of Object.values(candidate.stages)) assert.equal(stage.status,'unknown');
   assert.equal(a.license,'CC-BY-4.0'); assert.equal(a.author,'Leon Made This / s010s'); assert.equal(a.units,'meters');
   assert.deepEqual(a.worlds,['prehistoric']); assert.deepEqual(a.packs,[`prehistoric-batch${entry.batch}-20261020`]);
   assetFileAllowlist({assets:[a]});
   for (const key of ['name','description','scientific_scope']) for (const lang of ['en','zh']) assert(a[key]?.[lang]?.trim());
   for (const key of ['quality_status','approval_provenance','candidate_record','qa','publication_status','downloads','turntable','card_preview','profile','validation_profile','approval']) assert(!Object.hasOwn(a,key),`Reserved metadata ${key}`);
   const metrics = await json(entry.original_metrics);
   assert.equal(metrics.glb.sha256,a.sha256.glb); assert.equal(a.triangles,metrics.glb.scene_triangles);
   assert.deepEqual(a.dimensions,metrics.measured_glb_xyz_m); assert.deepEqual(a.bounds_glb_m,metrics.glb.bounds_m);
   assert.deepEqual(a.blender_dimensions_m,metrics.measured_blender_xyz_m);
   assert.equal(a.material_count,metrics.glb.materials); assert.equal(a.primitives,metrics.glb.scene_primitives_estimated_base_draw_calls);
   assert.equal(a.glb_bytes,metrics.glb.bytes); assert.deepEqual(a.export_options,metrics.export_options);
   for (const key of ['glb','blend','preview']) {
    assert.equal(dirname(a[key]),folder); const bytes = await checked({path:a[key],sha256:a.sha256[key]});
    if (key === 'glb') assert.equal(bytes.length,a.glb_bytes);
   }
   assert.equal(candidate.artifacts.glb.sha256,a.sha256.glb); assert.equal(candidate.artifacts.source.sha256,a.sha256.blend);
   for (const artifact of Object.values(candidate.artifacts)) await checked(artifact);
   for (const evidence of candidate.evidence) await checked(evidence);
   for (const raw of Object.values(candidate.raw_checks ?? {})) await checked(raw);
   const profile = await json(entry.active_profile);
   assert.deepEqual(profile.candidate,entry.active_candidate); assert.equal(profile.validation_profile,'static-stylized-v1');
   assert.equal(entry.active_candidate.path,`${entry.candidate_root}/candidate.json`);
   assert.equal(entry.active_profile.path,`${entry.candidate_root}/profile-contract.json`);
   assert.deepEqual(a.source_identity.candidate,entry.active_candidate);
   assert.equal(a.source_identity.revision,entry.revision); assert.equal(a.source_identity.batch,entry.batch);
   assert.equal(a.source_identity.model_commit,entry.reviewed_source_commit); assert.equal(a.source_identity.qa_commit,release.review_commit);
   const brief = await json(candidate.artifacts.brief);
   assert.equal(brief.asset_id,a.id); assert.equal(brief.turntable_frames,0); assert.equal(brief.required_views.length,8);
   assert(candidate.evidence.some(e => e.path === entry.proof.path && e.sha256 === entry.proof.sha256));
   assert.deepEqual(entry.review,entry.active_review); await checked(entry.active_review);
   assert.deepEqual(a.source_identity.active_review,entry.active_review);
   assert.deepEqual(a.source_identity.required_independent_reviews,entry.required_qa_documents);
   for (const pin of entry.required_qa_documents) await checked(pin);
   const proof = await json(entry.proof);
   assert.deepEqual(proof.subject,{revision:entry.revision,glb_sha256:a.sha256.glb,brief_sha256:candidate.artifacts.brief.sha256,references_sha256:candidate.artifacts.references.sha256});
   assert.equal(proof.source_glb_sha256,a.sha256.glb); assert.equal(proof.frames.length,8);
   assert.equal(new Set(proof.frames.map(frame => frame.path)).size,8);
   for (const frame of proof.frames) {
    const bytes = await checked({path:`${dirname(entry.proof.path)}/${frame.path}`,sha256:frame.sha256});
    assert.equal(bytes.length,frame.bytes); png(bytes,[frame.width,frame.height],`${a.id}: fixed8`);
   }
   const card = index.posters.find(row => row.id === a.id), visual = review.models.find(row => row.id === a.id);
   const pair = original.rows.find(row => row.id === a.id), selected = subset.assets.find(row => row.asset_id === a.id);
   const oldMetadata = await json(entry.capture_input_metadata), input = inputs.assets.find(row => row.id === a.id);
   assert.equal(input.metadata.path,entry.metadata.path); assert.equal(input.metadata.sha256,entry.capture_input_metadata.sha256);
   assert.equal(oldMetadata.id,a.id); assert.equal(oldMetadata.sha256.glb,a.sha256.glb);
   assert.equal(pair.poster.input_sha256,posterInputKey(oldMetadata,original.shared),`${a.id}: original gallery subject must remain historical`);
   assert.equal(pair.source_glb_sha256,a.sha256.glb); assert.equal(pair.poster.source_glb_sha256,a.sha256.glb);
   assert.equal(capture.assets.find(row => row.id === a.id).source_glb_sha256,a.sha256.glb);
   assert.equal(card.source_glb_sha256,a.sha256.glb); assert.equal(card.render_preset_sha256,capture.render_preset_sha256);
   assert.equal((await checked({path:card.path,sha256:card.sha256})).length,card.bytes);
   assert.equal(entry.capture_reference.sha256,a.sha256.preview);
   const reference = await checked(entry.capture_reference); png(reference,[768,768],`${a.id}: card reference`);
   assert(passPresentation(visual.result)); assert.equal(visual.source_glb_sha256,a.sha256.glb);
   assert.deepEqual(visual.views,['card','detail','wheel']);
   assert.deepEqual(visual.original_pngs.map(row => row.kind),['card','detail','wheel']);
   assert.equal(selected.revision,entry.revision); assert.equal(selected.source_snapshot_for_release,release.source_commit);
   assert.equal(selected.source_glb_sha256,a.sha256.glb); assert.equal(selected.source_blend_sha256,a.sha256.blend);
   assert.equal(selected.independent_static_disposition,a.id === 'breccia-outcrop' ? 'ACCEPT BOUNDED source/model differential only' : STATIC_ONLY_IDS.includes(a.id) ? 'ACCEPT_STATIC_QA_ONLY' : 'ACCEPT BOUNDED'); assert.equal(selected.presentation_result,visual.result);
   assert.deepEqual(selected.original_pngs,visual.original_pngs);
   assert.deepEqual(selected.required_qa_documents,entry.required_qa_documents);
   assert.deepEqual(selected.source_artifact_bindings,candidate.artifacts);
   for (const picture of visual.original_pngs) {
    assert.equal(picture.original_pixels_independently_reviewed,true);
    const originalFile = verification.pngs.find(row => row.id === a.id && row.kind === picture.kind);
    for (const key of ['sha256','bytes','dimensions','path']) assert.deepEqual(picture[key],originalFile[key]);
    if (picture.kind === 'card') { assert.equal(picture.sha256,a.sha256.preview); assert.equal(picture.bytes,reference.length); }
    else {
     const path = pair.poster[picture.kind], file = pair.files.find(row => row.path === path);
     assert.equal(picture.sha256,file.sha256); assert.equal(picture.bytes,file.bytes);
    }
   }
   additions.push(finalAsset(a,entry,release));
  }
 }
 assert.deepEqual(sortedIds(additions),FORTY_FOUR_IDS,'Exact fixed44 membership, no omitted, duplicated, or extra IDs');
 return {releases,additions,publication_ready:false};
}

/** Shared by the publication gate and its negative tests. No re-signing or compatibility exception. */
export function assertFortyFourGallerySubjects(receipt,additions) {
 assert.deepEqual(sortedIds(additions),FORTY_FOUR_IDS,'Final gallery requires exact fixed44 assets');
 assert.deepEqual(receipt.selected_ids,FORTY_FOUR_IDS,'Final gallery selection must be exactly44, never the original47');
 assert.deepEqual(sortedIds(receipt.rows),FORTY_FOUR_IDS,'Final gallery receipt must contain exactly44 rows');
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

export async function collectFortyFourAdditions(root,descriptors) {
 const result = await preflightFortyFourAdditions(root,descriptors), {releases,additions} = result;
 const {local,checked,json} = reader(root), capture = releases[0].capture;
 for (const release of releases) for (const key of ['final_gallery_receipt','final_gallery_review','final_gallery_artifact_verification']) {
  assert(release.capture[key],`Fixed44 final gallery subject mismatch: ${key} is pending; original47 metadata cannot authorize final44 publication`);
  assert.deepEqual(release.capture[key],capture[key],'All fixed44 groups must bind the same final gallery evidence');
 }
 const receipt = await json(capture.final_gallery_receipt);
 assertFortyFourGallerySubjects(receipt,additions);
 await assertRecordedGalleryRecipe(receipt.shared,root);
 const verification = await json(capture.final_gallery_artifact_verification), review = await json(capture.final_gallery_review);
 assert.equal(verification.zip_matches_github_digest_and_size,true); assert.equal(verification.entry_bytes_match_local_directory,true);
 assert.equal(verification.head_sha,receipt.head_sha); assert.equal(String(verification.run_id),String(receipt.run_id));
 assert(/^[a-f0-9]{64}$/.test(verification.zip_sha256)); assert(Number.isSafeInteger(verification.artifact_id) && verification.artifact_id > 0);
 assert.equal(review.status,'accepted_for_scoped_website_delivery_only');
 assert.equal(review.capture_head,receipt.head_sha); assert.equal(String(review.run_id),String(receipt.run_id));
 assert.equal(review.artifact_id,verification.artifact_id); assert.equal(review.zip_sha256,verification.zip_sha256);
 assert.deepEqual(review.receipt,capture.final_gallery_receipt);
 assert.equal(review.hardware_gpu_verified,false); assert.equal(review.target_scene_verified,false); assert.equal(review.formal_acceptance,'BLOCKED');
 assert.deepEqual(sortedIds(review.models),FORTY_FOUR_IDS);
 const gallery = JSON.parse(await local('site/public/gallery/resources.json'));
 const publicIndex = JSON.parse(await local('assets/turntables/index.json'));
 const originalIndex = await json(capture.index);
 for (const asset of additions) {
  const pair = receipt.rows.find(row => row.id === asset.id), visual = review.models.find(row => row.id === asset.id);
  assert.deepEqual(publicIndex.posters.filter(row => row.id === asset.id),originalIndex.posters.filter(row => row.id === asset.id),'Public card must equal the original exact-renderer card');
  assert(passPresentation(visual.result)); assert.equal(visual.source_glb_sha256,asset.sha256.glb);
  assert.deepEqual(visual.original_pngs.map(row => row.kind),['detail','wheel']);
  assert.deepEqual(gallery.posters[asset.id],pair.poster);
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

export async function appendFortyFourRelease(root,base,descriptors) {
 assert.equal(base.assets.length,251,'Fixed44 append follows the exact251-model release');
 assert.equal(new Set(base.assets.map(asset => asset.id)).size,251,'Existing251 IDs must be unique');
 assert(!base.assets.some(asset => FORTY_FOUR_IDS.includes(asset.id)),'Fixed44 must not replace an existing251 asset');
 const before = JSON.stringify(base), {additions} = await collectFortyFourAdditions(root,descriptors);
 assert.equal(JSON.stringify(base),before,'The existing251 release must remain byte-equivalent');
 const result = {...base,assets:[...base.assets,...additions],publication:{...base.publication,forty_four_descriptors:descriptors}};
 assert.equal(result.assets.length,295);
 assert.deepEqual(result.assets.slice(0,251),base.assets,'No existing251 mutation');
 return result;
}

/** Exact owner-authorized limited website release; original formal gates remain unchanged. */
import assert from 'node:assert/strict';
import { readFile, realpath } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { CONCEPT_SEVEN_RELEASE as fixed } from './accepted-concept-seven-release.mjs';
import { collectRound13Release } from './small-life-round13-release.mjs';
import { assetFileAllowlist } from './asset-delivery.mjs';
export const CONCEPT_SEVEN_IDS = fixed.additions.map(a => a.id).sort();
export const CONCEPT_SEVEN_PACK = 'prehistoric-concept-seven-20261019';
const sha = b => createHash('sha256').update(b).digest('hex');
export async function collectConceptSevenRelease(root, descriptor) {
  const cache = new Map();
  async function checked(pin) {
    assert(pin && typeof pin.path === 'string' && /^(assets|production|qa|scripts)\//.test(pin.path) && !/[\\\u0000-\u001f?#%:]/.test(pin.path) && pin.path.split('/').every(p => p && p !== '.' && p !== '..'), 'Safe source path required');
    assert(/^[a-f0-9]{64}$/.test(pin.sha256), 'SHA-256 pin required');
    const path = resolve(root, pin.path);
    assert.equal(await realpath(path), path, 'Release symlinks forbidden');
    let bytes = cache.get(path); if (!bytes) { bytes = await readFile(path); cache.set(path, bytes); }
    assert.equal(sha(bytes), pin.sha256, `${pin.path}: release hash mismatch`);
    return bytes;
  }
  const json = async pin => JSON.parse(await checked(pin));
  const run = (script, args) => {
    const r = spawnSync('python3', [script, ...args], {cwd:root, encoding:'utf8', timeout:30000, maxBuffer:2*1024*1024});
    assert(!r.error, r.error?.message); assert([0,1].includes(r.status), r.stderr); return JSON.parse(r.stdout);
  };
  assert.equal(descriptor.path, 'assets/releases/concept-seven-20261019.json');
  const release = await json(descriptor);
  assert.deepEqual(release, fixed, 'Only the exact reviewed seven and their bounded publication scope are authorized');
  const policy = await json(release.publication_policy);
  assert.equal(policy.authority, 'owner_authorized_qa_passed_batch_release'); assert.equal(policy.candidate_gate_grants_publication, false);
  const bundle = await json(release.source_bundle);
  assert.equal(new Set(bundle.files.map(f => f.path)).size, bundle.files.length);
  for (const pin of bundle.files) await checked(pin);
  const frozen = path => { const pin = bundle.files.find(p => p.path === path); assert(pin, `Missing frozen evidence ${path}`); return json(pin); };
  const fishRoot = 'production/concept-small-fish-20261019';
  const fishQA = 'qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh';
  const fishPins = await frozen(`${fishQA}/evidence/artifact-hashes.json`);
  assert.equal(fishPins.candidate_commit, '3196c36c51d5a14487dcd4ebbebcafc00aa933d7');
  const decisions = await frozen(`${fishQA}/review-decisions.json`);
  assert.equal(decisions.formal_production_acceptance, 'not_approved');
  const scenes = await frozen(`${fishRoot}/closure-20261019/software-webgl/report.json`);
  assert.equal(scenes.status, 'pass'); assert.equal(scenes.tests.length, 20);
  for (const t of scenes.tests) { assert.equal(t.status,'pass'); assert.equal(t.gl_error,0); assert(t.render_triangles>0 && t.foreground_pixels>0); assert.equal(t.hardware_gpu_verified,false); await checked({path:`${fishRoot}/closure-20261019/software-webgl/${t.screenshot.path}`,sha256:t.screenshot.sha256}); }
  const closure = await frozen(`${fishRoot}/closure-20261019/closure-verification.json`);
  assert.equal(closure.first_concept_inspection_timestamp, 'unknown'); assert.equal(closure.formal_production_acceptance, 'not asserted');
  const marineQA = await frozen('qa/undersea-invertebrates-concept-20261019/review.json');
  assert.equal(marineQA.source_commit, 'fc2f6db4133b62e48b9764e4a33b0fd518e806df');
  assert.equal(marineQA.assets.find(a => a.asset_id === 'ctenoimbricata').factual, 'unknown_pending_original_figure_pixels');
  const marineScene = await frozen('qa/undersea-invertebrates-concept-20261019/evidence/browser-runtime-report.json');
  assert.equal(marineScene.status,'pass'); assert.deepEqual(marineScene.errors,[]); assert(marineScene.views.every(v => v.gl_error===0 && v.render_triangles>0 && v.foreground_pixels>0));
  const additions = [];
  for (const entry of release.additions) {
    const a = await json(entry.metadata), source = await json(entry.source_metadata), folder = `assets/additions/${entry.id}/concept-seven-20261019`;
    assert.equal(entry.metadata.path, `${folder}/release-metadata.json`); assert.equal(a.id, entry.id);
    assert.equal(a.category,'animals'); assert.equal(a.collection,'prehistoric'); assert.deepEqual(a.worlds,['prehistoric']); assert.deepEqual(a.packs,[CONCEPT_SEVEN_PACK]);
    assert.equal(a.license,'CC-BY-4.0'); assert.equal(a.author,'Leon Made This / s010s'); assert.equal(a.units,'meters');
    assert.deepEqual(a.sha256,entry.sha256); assetFileAllowlist({assets:[a]});
    for (const key of ['name','description','scientific_scope']) for (const lang of ['en','zh']) assert(a[key]?.[lang]?.trim());
    for (const key of ['quality_status','approval_provenance','candidate_record','qa','publication_status','downloads','turntable','card_preview']) assert(!Object.hasOwn(a,key), `Reserved metadata ${key}`);
    for (const key of ['triangles','dimensions','axes','bounds_glb_m','blender_dimensions_m','export_options','materials','generator','surface_profile']) assert.deepEqual(a[key],source[key], `Preserve reviewed ${key}`);
    for (const key of ['glb','blend','preview']) { assert.equal(dirname(a[key]),folder); await checked({path:a[key],sha256:entry.sha256[key]}); }
    for (const key of ['glb','blend']) { assert.equal(entry.artifacts[key].sha256,entry.sha256[key]); await checked(entry.artifacts[key]); }
    const references = await json(entry.artifacts.references); assert.deepEqual(a.sources,references.sources);
    const brief = await json(entry.artifacts.brief), limits = entry.limits;
    assert.deepEqual(limits,entry.group==='fish'?brief.budgets:brief.geometry_policy);
    const measured = run('scripts/qa_glb.py',[a.glb,'--max-triangles',String(limits.max_triangles),'--max-materials',String(limits.max_materials),'--max-primitives',String(limits.max_primitives)]);
    assert.deepEqual(measured.errors,[]); assert.equal(measured.sha256,a.sha256.glb); assert.equal(measured.scene_triangles,a.triangles); assert.deepEqual(measured.bounds_m.size,a.dimensions);
    assert(measured.materials<=limits.max_materials && measured.scene_primitives_estimated_base_draw_calls<=limits.max_primitives);
    assert((await checked(entry.artifacts.glb)).length<=(limits.max_glb_bytes??limits.soft_glb_bytes));
    for (const name of ['source_export','rebuild_1','rebuild_2','runtime_parse']) {
      const report = await json(entry.technical[name]); assert(['pass','pass_with_warnings'].includes(report.status)); assert(!report.errors?.length); assert.equal(report.glb_sha256??report.subject?.glb_sha256,a.sha256.glb);
      if (name==='source_export') { assert.equal(report.source_sha256,a.sha256.blend); assert.equal(report.triangles_match,true); assert.equal(report.bounds_match,true); }
      if (name.startsWith('rebuild')) { assert.equal(report.semantic_match,true); assert.equal(report.provenance_status,'bound_successful_build_run'); }
    }
    const format = await json(entry.technical.khronos); assert.equal(format.issues.numErrors,0); assert.equal(format.issues.numWarnings,0);
    const proof = await json(entry.proof); assert.equal(proof.source_glb_sha256,a.sha256.glb); assert.equal(proof.frames.length,entry.group==='fish'?11:37);
    for (const frame of proof.frames) { const bytes=await checked({path:`${dirname(entry.proof.path)}/${frame.path}`,sha256:frame.sha256}); assert.equal(bytes.length,frame.bytes); assert.equal(bytes.readUInt32BE(16),frame.width); assert.equal(bytes.readUInt32BE(20),frame.height); }
    if (entry.group==='fish') {
      const decision = decisions.assets[a.id]; assert(decision.decision.startsWith('pass')); assert.equal(decision.unresolved_blocker,false); assert.equal(decision.model_correction_recommended,false);
      for (const key of ['glb','blend','brief','references']) { const original=fishPins.files.find(p=>p.path===entry.artifacts[key].path); assert(original); assert.equal(original.sha256,entry.artifacts[key].sha256); }
      assert.equal(scenes.input_glb_sha256[a.id],a.sha256.glb); assert(scenes.tests.filter(t=>t.subject===a.id).length===4);
      assert.equal(a.mount_origin,'swimming body midline at (0,0,0), not floor contact');
      if (a.id==='dorypterus') { assert.equal(a.display_length_m,0.0996); assert(a.description.en.includes('0.0996')); }
      if (a.id==='pteraspis') { assert(a.description.en.includes('unverified')); assert.equal(decision.exact_reconstruction_anatomy,'unknown'); }
    } else {
      const review=marineQA.assets.find(r=>r.asset_id===a.id); assert(review); assert.equal(review.visual,'pass'); assert.equal(review.factual,'pass_for_genus_informed_scope'); assert.equal(review.model_revision_requested,false);
      assert.equal(review.glb_sha256,a.sha256.glb); assert.equal(review.blend_sha256,a.sha256.blend);
      assert.equal(marineScene.scene_assets.find(r=>r.asset_id===a.id).glb_sha256,a.sha256.glb);
      const candidatePath=`${dirname(entry.artifacts.glb.path)}/candidate.json`, candidate=await frozen(candidatePath);
      assert.equal(candidate.approval.status,'pending');
      const current=run('scripts/validate_candidate.py',[candidatePath,'--root',resolve(root),'--json']);
      assert.deepEqual(current,await frozen(`${dirname(candidatePath)}/evidence/candidate-integrity.json`));
      assert.equal(current.valid,true); assert.equal(current.approved_for_brief,false); assert.equal(current.validation_profile,'legacy-v1');
    }
    additions.push({...a,quality_status:'independent_qa_accepted_stylized_prop',approval_provenance:{source_commit:entry.source_commit,review_commit:entry.review_commit,review_sha256:entry.review.sha256,source_contract:entry.group==='fish'?'bounded-concept-study:11-views':'legacy-v1-production:13-views+24-turntable',candidate_record_approved_for_brief:false,formal_profile_acceptance:'BLOCKED',hardware_gpu_verified:false,target_scene_verified:false,concept_chronology:entry.group==='fish'?'first inspection time unknown':'frozen producer inspection records incomplete'}});
  }
  const base=await collectRound13Release(root,release.base_descriptor); assert.equal(base.assets.length,175);
  assert(!additions.some(a=>base.assets.some(b=>b.id===a.id))); assert(!additions.some(a=>release.excluded_ids.includes(a.id)));
  return {...base,assets:[...base.assets,...additions],publication:{...base.publication,concept_seven_descriptor:descriptor,approved_concept_seven_ids:CONCEPT_SEVEN_IDS}};
}

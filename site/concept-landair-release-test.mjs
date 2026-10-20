/** Bounded land/air quartet: exact revisions, immutable baseline and no formal promotion. */
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, writeFile, rm, rename, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { collectConceptLandairRelease, CONCEPT_LANDAIR_IDS, CONCEPT_LANDAIR_PACK } from './concept-landair-release.mjs';
import { CONCEPT_LANDAIR_RELEASE as fixed } from './accepted-concept-landair-release.mjs';
import { collectConceptQuartetsRelease } from './concept-quartets-release.mjs';

if (!process.argv.includes('--batches5657-only')) {
const BASE_COUNT = 186;
const revisions = { sapeornis: 'r001', longirostravis: 'r001', dunbaria: 'r001', chimerarachne: 'r001' };
const expectedIds = Object.keys(revisions).sort();
const descriptorPath = 'assets/releases/concept-landair-20261019.json';
const root = await mkdtemp(join(tmpdir(), 'vault-concept-landair-'));
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const pin = async path => ({ path, sha256: sha(await readFile(resolve(root, path))) });
const json = async path => JSON.parse(await readFile(resolve(root, path), 'utf8'));
let checks = 0;

async function mutate(path, change, action) {
  const full = resolve(root, path), bytes = await readFile(full);
  try {
    const value = JSON.parse(bytes);
    change(value);
    await writeFile(full, JSON.stringify(value));
    await action();
    checks++;
  } finally {
    await writeFile(full, bytes);
  }
}

async function tamper(path, action) {
  const full = resolve(root, path), bytes = await readFile(full);
  try {
    await writeFile(full, Buffer.concat([bytes, Buffer.from('\ntamper')]));
    await action();
    checks++;
  } finally {
    await writeFile(full, bytes);
  }
}

function validateCandidate(path, requireApproved = false) {
  const run = spawnSync('python3', [
    'scripts/validate_candidate.py', path, '--root', root, '--json',
    ...(requireApproved ? ['--require-approved'] : []),
  ], { cwd: root, encoding: 'utf8', timeout: 30000, maxBuffer: 2 * 1024 * 1024 });
  assert.ifError(run.error);
  assert([0, 1].includes(run.status), run.stderr);
  return { exitCode: run.status, report: JSON.parse(run.stdout) };
}

try {
  // Mutations are confined to an isolated copy; reviewed files in the checkout stay untouched.
  for (const path of ['assets', 'production', 'qa', 'scripts', 'experiments', 'package-lock.json']) {
    execFileSync('cp', ['-a', '--reflink=auto', path, resolve(root, path)]);
  }
  await mkdir(resolve(root, 'site'));
  await writeFile(resolve(root, 'site/viewer.js'), await readFile('site/viewer.js'));
  const collect = async () => collectConceptLandairRelease(root, await pin(descriptorPath));
  assert.deepEqual(CONCEPT_LANDAIR_IDS, expectedIds, 'Only the four independently reviewed land/air IDs are authorized');
  assert.deepEqual(fixed.additions.map(entry => entry.id).sort(), expectedIds);
  for (const entry of fixed.additions) {
    assert.equal(entry.revision, revisions[entry.id], `${entry.id}: exact reviewed revision`);
    assert.equal(entry.source_commit, 'e874e99d20b3b98c73cddb8496bcd7e89be4e28c');
    assert.equal(entry.review_commit, '3d024e53c36863d1887abd726998fa0f0d7b3831');
    assert.equal(entry.original_review_freeze, '68483aa3b8eed2d86f9e59a930128d99579b0838');
    assert.equal(entry.delivery_review_commit, 'b0426b7e3a696b30fea4de9e8b46c3772bab3f23');
    const sourceRoot = `production/concept-small-land-air-20261019/${entry.id}/r001`;
    assert.equal(entry.source_metadata.path, `${sourceRoot}/output/${entry.id}/metadata.json`);
    for (const key of ['glb', 'blend']) assert.equal(entry.artifacts[key].path, `${sourceRoot}/output/${entry.id}/${entry.id}.${key}`);
    assert.equal(entry.candidate.path, `${sourceRoot}/candidate.json`);
  }
  checks++;

  const baseline = await collectConceptQuartetsRelease(root, fixed.base_descriptor);
  const manifest = await collect();
  const before = await json('assets/manifest.json');
  assert.equal(baseline.assets.length, BASE_COUNT);
  assert.equal(manifest.assets.length, BASE_COUNT + CONCEPT_LANDAIR_IDS.length);
  assert.deepEqual(manifest.assets.slice(0, BASE_COUNT), baseline.assets, 'Every field of the existing 186 assets is preserved');
  assert.deepEqual(manifest.assets.slice(0, BASE_COUNT), before.assets.slice(0, BASE_COUNT), 'The existing published manifest is unchanged');
  assert.deepEqual(manifest.assets.slice(BASE_COUNT).map(asset => asset.id).sort(), expectedIds);
  assert.equal(new Set(manifest.assets.map(asset => asset.id)).size, manifest.assets.length);
  assert.deepEqual(manifest.publication.approved_concept_landair_ids, expectedIds);
  const { concept_landair_descriptor, approved_concept_landair_ids, ...previousPublication } = manifest.publication;
  assert.deepEqual(previousPublication, baseline.publication, 'Earlier publication provenance is preserved');
  assert.deepEqual(concept_landair_descriptor, await pin(descriptorPath));
  for (const id of fixed.excluded_ids) assert(!manifest.assets.some(asset => asset.id === id), `${id} remains excluded`);
  assert(!manifest.assets.some(asset => asset.id === 'ctenoimbricata'));
  for (const asset of baseline.assets) {
    for (const key of ['glb', 'blend', 'preview']) {
      const original = await readFile(asset[key]);
      assert.deepEqual(await readFile(resolve(root, asset[key])), original, `${asset.id}: pre-existing ${key} bytes are preserved`);
      assert.equal(sha(original), asset.sha256[key], `${asset.id}: baseline ${key} keeps its accepted digest`);
    }
  }
  checks++;

  for (const asset of manifest.assets.slice(BASE_COUNT)) {
    const entry = fixed.additions.find(item => item.id === asset.id);
    const source = await json(entry.source_metadata.path);
    assert.equal(asset.quality_status, 'independent_qa_accepted_stylized_prop');
    assert.deepEqual(asset.packs, [CONCEPT_LANDAIR_PACK]);
    assert.deepEqual(asset.sha256, entry.sha256);
    for (const key of ['triangles', 'dimensions', 'axes', 'bounds_glb_m', 'blender_dimensions_m', 'export_options', 'materials', 'generator']) {
      assert.deepEqual(asset[key], source[key], `${asset.id}: measured ${key} is unchanged`);
    }
    assert.deepEqual(asset.sources, (await json(entry.artifacts.references.path)).sources);
    assert(asset.sources.length > 0);
    for (const key of ['name', 'description', 'scientific_scope']) {
      for (const lang of ['en', 'zh']) assert(asset[key]?.[lang]?.trim(), `${asset.id}: ${key}.${lang}`);
    }
    const provenance = asset.approval_provenance;
    assert.equal(provenance.source_commit, entry.source_commit);
    assert.equal(provenance.review_commit, entry.review_commit);
    assert.equal(provenance.review_sha256, entry.review.sha256);
    assert.equal(provenance.delivery_review_commit, entry.delivery_review_commit);
    assert.equal(provenance.delivery_review_sha256, entry.delivery_review.sha256);
    assert.equal(provenance.candidate_record_approved_for_brief, false);
    assert.equal(provenance.formal_profile_acceptance, 'BLOCKED');
    assert.equal(provenance.hardware_gpu_verified, false);
    assert.equal(provenance.target_scene_verified, false);
    assert(!Object.hasOwn(provenance, 'validation_profile'));
    for (const key of ['candidate_record', 'validation_profile', 'profile', 'approved_for_brief', 'approval', 'qa', 'publication_status', 'downloads']) {
      assert(!Object.hasOwn(asset, key), `${asset.id}: candidate-only ${key} cannot collide with published metadata`);
    }
    const candidate = await json(entry.candidate.path);
    assert.equal(candidate.asset_id, entry.id);
    assert.equal(candidate.revision, revisions[entry.id]);
    assert.equal(candidate.approval.status, 'pending');
    for (const stage of Object.values(candidate.stages)) {
      assert.equal(stage.status, 'unknown', 'A bounded gallery release cannot silently approve a formal QA stage');
    }
    const { exitCode, report } = validateCandidate(entry.candidate.path, true);
    assert.equal(exitCode, 1, 'Limited website publication cannot satisfy the formal approval CLI gate');
    assert.equal(report.valid, true);
    assert.equal(report.approved_for_brief, false);
    assert.equal(report.validation_profile, 'legacy-v1');
    assert(report.approval_blockers.length > 0);
    for (const stage of ['factual', 'gpu', 'runtime_parse', 'scene', 'specification', 'technical', 'visual']) {
      assert(report.approval_blockers.includes(`${stage}: unknown`), `${stage}: formal stage stays unknown`);
    }
    assert.equal(report.measurements.materials, source.material_count, 'Actual exported material count is preserved separately from authored palette inventory');
    assert(source.materials.length >= source.material_count);
    const ordinary = validateCandidate(entry.candidate.path);
    assert.equal(ordinary.exitCode, 0);
    assert.deepEqual(ordinary.report, report);
    assert.deepEqual(report, await json(entry.candidate_validation.path));
    checks++;
  }

  // Even recomputing the outer descriptor hash must not authorize a different release.
  const descriptorChanges = [
    ['missing addition', value => value.additions.pop()],
    ['duplicate addition', value => value.additions.push(value.additions[0])],
    ['unreviewed ID', value => { value.additions[0].id = 'ctenoimbricata'; }],
    ['old revision', value => { value.additions[0].revision = 'r002'; }],
    ['missing authorization', value => { value.authorization = 'pending'; }],
    ['formal acceptance claim', value => { value.formal_profile_acceptance = 'PASS'; }],
    ['hardware acceptance claim', value => { value.hardware_gpu_verified = true; }],
    ['target scene acceptance claim', value => { value.target_scene_verified = true; }],
    ['different acceptance scope', value => { value.acceptance_scope = 'approved_for_brief'; }],
    ['source commit substitution', value => { value.additions[0].source_commit = '0'.repeat(40); }],
    ['delivery review commit substitution', value => { value.additions[0].delivery_review_commit = '0'.repeat(40); }],
    ['delivery review substitution', value => { value.additions[0].delivery_review.sha256 = '0'.repeat(64); }],
    ['review commit substitution', value => { value.additions[0].review_commit = '0'.repeat(40); }],
    ['review freeze substitution', value => { value.additions[0].original_review_freeze = '0'.repeat(40); }],
    ['added formal profile', value => { value.validation_profile = 'production-v1'; }],
    ['removed exclusions', value => { value.excluded_ids = []; }],
    ['source bundle substitution', value => { value.source_bundle.sha256 = '0'.repeat(64); }],
    ['unbound publication policy', value => { value.publication_policy.sha256 = '0'.repeat(64); }],
    ['base descriptor traversal', value => { value.base_descriptor.path = '../escape'; }],
    ['base descriptor substitution', value => { value.base_descriptor.sha256 = '0'.repeat(64); }],
    ['candidate validation promotion', value => { value.additions[0].approved_for_brief = true; }],
  ];
  for (const [label, change] of descriptorChanges) {
    await mutate(descriptorPath, change, () => assert.rejects(collect, /Only.*authorized/, label));
  }
  const originalDescriptor = await pin(descriptorPath);
  await assert.rejects(() => collectConceptLandairRelease(root, { ...originalDescriptor, sha256: '0'.repeat(64) }), /hash mismatch/);
  await assert.rejects(() => collectConceptLandairRelease(root, { ...originalDescriptor, path: '../escape' }));
  checks += 2;

  const entry = fixed.additions[0];
  for (const change of [
    value => { value.description.en = 'Exact scientific reconstruction'; },
    value => { value.scientific_scope.en = 'Formally approved for the target museum scene on physical hardware'; },
    value => { value.sources = []; },
    value => { value.sha256.glb = '0'.repeat(64); },
    value => { value.approval_provenance = { approved_for_brief: true }; },
    value => { value.quality_status = 'approved_for_brief'; },
    value => { value.packs = ['other']; },
    value => { value.dimensions = [1, 1, 1]; },
    value => { value.downloads = { glb: 'https://example.invalid/unreviewed.glb' }; },
    ...['validation_profile', 'profile', 'approved_for_brief', 'approval', 'candidate_record', 'qa', 'publication_status', 'turntable', 'card_preview', 'formal_profile_acceptance', 'hardware_gpu_verified', 'target_scene_verified'].map(key => value => { value[key] = key.endsWith('_verified') || key === 'approved_for_brief' ? true : 'forged-approval'; }),
  ]) {
    await mutate(entry.metadata.path, change, async () => {
      await assert.rejects(collect, /hash mismatch/, 'Changed metadata is rejected by its existing pin');
      const metadata = await pin(entry.metadata.path);
      await mutate(descriptorPath, value => { value.additions[0].metadata = metadata; }, () => assert.rejects(collect, /Only.*authorized/, 'Re-pinning metadata cannot expand frozen claims'));
    });
  }

  // A coordinated image/index rewrite must not reauthorize a different card image,
  // even when its new byte length and digest form a self-consistent public seal.
  const publicIndexPath = 'assets/turntables/index.json';
  const publicCards = (await json(publicIndexPath)).posters.filter(row => expectedIds.includes(row.id));
  assert.equal(publicCards.length, expectedIds.length);
  for (const [index, card] of publicCards.entries()) {
    const file = resolve(root, card.path), original = await readFile(file);
    const replacement = await readFile(resolve(root, publicCards[(index + 1) % publicCards.length].path));
    assert.notEqual(sha(replacement), card.sha256);
    try {
      await writeFile(file, replacement);
      await mutate(publicIndexPath, value => {
        const row = value.posters.find(row => row.id === card.id);
        row.sha256 = sha(replacement);
        row.bytes = replacement.length;
      }, () => assert.rejects(collect, /Public card must match/, `${card.id}: coordinated card/index substitution is rejected`));
    } finally {
      await writeFile(file, original);
    }
    await mutate(publicIndexPath, value => { value.posters.push(value.posters.find(row => row.id === card.id)); },
      () => assert.rejects(collect, /Public card must match/, `${card.id}: duplicate public card rows are rejected`));
    await mutate(publicIndexPath, value => { value.posters = value.posters.filter(row => row.id !== card.id); },
      () => assert.rejects(collect, /Public card must match/, `${card.id}: missing public card rows are rejected`));
  }

  // Exercise every quartet's public artifacts and the evidence used to support publication.
  const evidencePaths = new Set([fixed.source_bundle.path, fixed.publication_policy.path, fixed.base_descriptor.path, fixed.integration_audit.path, ...publicCards.map(card => card.path)]);
  for (const addition of fixed.additions) {
    const asset = manifest.assets.find(item => item.id === addition.id);
    for (const key of ['glb', 'blend', 'preview']) evidencePaths.add(asset[key]);
    for (const key of ['review', 'delivery_review', 'source_metadata', 'candidate', 'candidate_validation', 'proof', 'runtime']) evidencePaths.add(addition[key].path);
    for (const item of Object.values(addition.artifacts)) evidencePaths.add(item.path);
    for (const item of Object.values(addition.technical)) evidencePaths.add(item.path);
    for (const item of Object.values(addition.capture)) evidencePaths.add(item.path);
    const proof = await json(addition.proof.path);
    assert.equal(proof.frames.length, 11);
    const expectedProofDirectory = addition.id === 'chimerarachne' ? 'proof-macro-attempt02' : 'proof';
    assert.equal(addition.proof.path, `production/concept-small-land-air-20261019/${addition.id}/r001/${expectedProofDirectory}/render-manifest.json`);
    for (const frame of proof.frames) evidencePaths.add(`${dirname(addition.proof.path)}/${frame.path}`);
  }
  for (const path of evidencePaths) await tamper(path, () => assert.rejects(collect, /hash mismatch/, `${path}: tampering must fail closed`));

  await tamper('site/viewer.js', () => assert.rejects(collect, 'A changed viewer cannot retain the frozen capture attestation'));

  for (const addition of fixed.additions) {
    await mutate(addition.candidate.path, value => { value.approval.status = 'approved_for_brief'; }, async () => {
      const { exitCode, report } = validateCandidate(addition.candidate.path, true);
      assert.equal(exitCode, 1);
      assert.equal(report.valid, false);
      assert.equal(report.approved_for_brief, false, 'Forged candidate approval is never promoted');
      assert(report.errors.length > 0);
      await assert.rejects(collect, /hash mismatch/);
      const candidate = await pin(addition.candidate.path);
      await mutate(descriptorPath, value => { value.additions.find(item => item.id === addition.id).candidate = candidate; }, () => assert.rejects(collect, /Only.*authorized/));
    });
  }

  for (const path of [manifest.assets[BASE_COUNT].glb, publicCards[0].path, publicIndexPath]) {
    const artifact = resolve(root, path), saved = `${artifact}.saved`;
    await rename(artifact, saved);
    try {
      await symlink(saved, artifact);
      await assert.rejects(collect, /symlinks forbidden/i, `${path}: byte-identical symlink substitution is rejected`);
      checks++;
    } finally {
      await rm(artifact, { force: true });
      await rename(saved, artifact);
    }
  }
  assert.deepEqual(await collect(), manifest, 'Every destructive test restores the exact valid release');
  checks++;
  console.log(`Concept-landair release: ${checks} checks passed; exact reviewed quartet, unchanged ${BASE_COUNT}, frozen source/QA bindings, and blocked formal/hardware/scene gates preserved.`);
} finally {
  await rm(root, { recursive: true, force: true });
}

}
if(process.argv.includes('--batches5657-only')){
 const {collectBatches5657Additions}=await import('./concept-landair-release.mjs');
 const cwd=process.cwd(),manifest=JSON.parse(await readFile(resolve(cwd,'assets/manifest.json'))),descriptors=manifest.publication.batches56_57_descriptors;
 const collect=()=>collectBatches5657Additions(cwd,descriptors);const first=await collect();assert.equal(first.additions.length,7);assert(!first.additions.some(a=>a.id==='nidula-baltica'));assert.deepEqual(manifest.assets.slice(-7),first.additions);
 let passed=3;
 async function altered(path,change){const p=resolve(cwd,path),old=await readFile(p);try{await writeFile(p,change(old));await assert.rejects(collect);passed++;}finally{await writeFile(p,old);}}
 const r=first.releases[0],e=r.additions[0],a=first.additions[0];
 for(const path of [descriptors[0].path,e.metadata.path,e.candidate.path,e.frozen_brief.path,e.proof.path,e.review.path,r.source_bundle.path,r.capture.report.path,r.capture.zip_verification.path,a.glb,a.blend,a.preview])await altered(path,b=>Buffer.concat([b,Buffer.from(' ')]));
 await altered('assets/turntables/index.json',b=>{const x=JSON.parse(b);x.posters.find(p=>p.id===a.id).sha256='0'.repeat(64);return JSON.stringify(x);});
 const final=await collect();assert.deepEqual(final,first);passed++;
 console.log(`Batch56/57 bounded collector checks passed: ${passed}; exact sources restored, no model generation or repeated visual QA.`);
}

import {historicalManifestView,successorReader} from './same-id-successors.mjs';
/** Bounded marine quartet: exact revisions, immutable baseline and no formal promotion. */
import assert from 'node:assert/strict';
import { mkdtemp, readFile, writeFile, rm, rename, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { collectConceptQuartetsRelease, CONCEPT_QUARTETS_IDS, CONCEPT_QUARTETS_PACK } from './concept-quartets-release.mjs';
import { CONCEPT_QUARTETS_RELEASE as fixed } from './accepted-concept-quartets-release.mjs';
import { collectConceptSevenRelease } from './concept-seven-release.mjs';

const BASE_COUNT = 182;
const revisions = { burgessia: 'r002', emeraldella: 'r002', sanctacaris: 'r002', tuzoia: 'r003' };
const expectedIds = Object.keys(revisions).sort();
const descriptorPath = 'assets/releases/concept-quartets-20261019.json';
const root = await mkdtemp(join(tmpdir(), 'vault-concept-quartets-'));
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
  const collect = async () => collectConceptQuartetsRelease(root, await pin(descriptorPath));
  assert.deepEqual(CONCEPT_QUARTETS_IDS, expectedIds, 'Only the four independently reviewed marine IDs are authorized');
  assert.deepEqual(fixed.additions.map(entry => entry.id).sort(), expectedIds);
  for (const entry of fixed.additions) assert.equal(entry.revision, revisions[entry.id], `${entry.id}: exact reviewed revision`);
  checks++;

  const baseline = await collectConceptSevenRelease(root, fixed.base_descriptor);
  const manifest = await collect();
  const before = historicalManifestView({manifest:await json('assets/manifest.json'),read:successorReader(process.cwd())});
  assert.equal(baseline.assets.length, BASE_COUNT);
  assert.equal(manifest.assets.length, BASE_COUNT + CONCEPT_QUARTETS_IDS.length);
  assert.deepEqual(manifest.assets.slice(0, BASE_COUNT), baseline.assets, 'Every field of the existing 182 assets is preserved');
  assert.deepEqual(manifest.assets.slice(0, BASE_COUNT), before.assets.slice(0, BASE_COUNT), 'The existing published manifest is unchanged');
  assert.deepEqual(manifest.assets.slice(BASE_COUNT).map(asset => asset.id).sort(), expectedIds);
  assert.equal(new Set(manifest.assets.map(asset => asset.id)).size, manifest.assets.length);
  assert.deepEqual(manifest.publication.approved_concept_quartets_ids, expectedIds);
  const { concept_quartets_descriptor, approved_concept_quartets_ids, ...previousPublication } = manifest.publication;
  assert.deepEqual(previousPublication, baseline.publication, 'Earlier publication provenance is preserved');
  assert.deepEqual(concept_quartets_descriptor, await pin(descriptorPath));
  for (const id of fixed.excluded_ids) assert(!manifest.assets.some(asset => asset.id === id), `${id} remains excluded`);
  assert(!manifest.assets.some(asset => asset.id === 'ctenoimbricata'));
  checks++;

  for (const asset of manifest.assets.slice(BASE_COUNT)) {
    const entry = fixed.additions.find(item => item.id === asset.id);
    const source = await json(entry.source_metadata.path);
    assert.equal(asset.quality_status, 'independent_qa_accepted_stylized_prop');
    assert.deepEqual(asset.packs, [CONCEPT_QUARTETS_PACK]);
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
    assert.equal(provenance.candidate_record_approved_for_brief, false);
    assert.equal(provenance.formal_profile_acceptance, 'BLOCKED');
    assert.equal(provenance.hardware_gpu_verified, false);
    assert.equal(provenance.target_scene_verified, false);
    assert(!Object.hasOwn(provenance, 'validation_profile'));
    assert(!Object.hasOwn(asset, 'candidate_record'));
    const candidate = await json(entry.candidate.path);
    assert.equal(candidate.asset_id, entry.id);
    assert.equal(candidate.revision, revisions[entry.id]);
    assert.equal(candidate.approval.status, 'pending');
    const { exitCode, report } = validateCandidate(entry.candidate.path, true);
    assert.equal(exitCode, 1, 'Limited website publication cannot satisfy the formal approval CLI gate');
    assert.equal(report.valid, true);
    assert.equal(report.approved_for_brief, false);
    assert.equal(report.validation_profile, 'legacy-v1');
    assert(report.approval_blockers.length > 0);
    assert.deepEqual(report, await json(entry.candidate_validation.path));
    checks++;
  }

  // Even recomputing the outer descriptor hash must not authorize a different release.
  const descriptorChanges = [
    ['missing addition', value => value.additions.pop()],
    ['duplicate addition', value => value.additions.push(value.additions[0])],
    ['unreviewed ID', value => { value.additions[0].id = 'ctenoimbricata'; }],
    ['old revision', value => { value.additions[0].revision = 'r001'; }],
    ['missing authorization', value => { value.authorization = 'pending'; }],
    ['formal acceptance claim', value => { value.formal_profile_acceptance = 'PASS'; }],
    ['hardware acceptance claim', value => { value.hardware_gpu_verified = true; }],
    ['target scene acceptance claim', value => { value.target_scene_verified = true; }],
    ['different acceptance scope', value => { value.acceptance_scope = 'approved_for_brief'; }],
    ['source commit substitution', value => { value.additions[0].source_commit = '0'.repeat(40); }],
    ['review commit substitution', value => { value.additions[0].review_commit = '0'.repeat(40); }],
    ['review freeze substitution', value => { value.additions[0].original_review_freeze = '0'.repeat(40); }],
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
  await assert.rejects(() => collectConceptQuartetsRelease(root, { ...originalDescriptor, sha256: '0'.repeat(64) }), /hash mismatch/);
  await assert.rejects(() => collectConceptQuartetsRelease(root, { ...originalDescriptor, path: '../escape' }));
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
  const evidencePaths = new Set([fixed.source_bundle.path, fixed.publication_policy.path, fixed.base_descriptor.path, ...publicCards.map(card => card.path)]);
  for (const addition of fixed.additions) {
    const asset = manifest.assets.find(item => item.id === addition.id);
    for (const key of ['glb', 'blend', 'preview']) evidencePaths.add(asset[key]);
    for (const key of ['review', 'source_metadata', 'candidate', 'candidate_validation', 'proof', 'runtime']) evidencePaths.add(addition[key].path);
    for (const item of Object.values(addition.artifacts)) evidencePaths.add(item.path);
    for (const item of Object.values(addition.technical)) evidencePaths.add(item.path);
    const proof = await json(addition.proof.path);
    assert.equal(proof.frames.length, 12);
    evidencePaths.add(`${dirname(addition.proof.path)}/${proof.frames[0].path}`);
  }
  for (const path of evidencePaths) await tamper(path, () => assert.rejects(collect, /hash mismatch/, `${path}: tampering must fail closed`));

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
  console.log(`Concept-quartets release: ${checks} checks passed; exact reviewed quartet, unchanged ${BASE_COUNT}, frozen source/QA bindings, and blocked formal/hardware/scene gates preserved.`);
} finally {
  await rm(root, { recursive: true, force: true });
}

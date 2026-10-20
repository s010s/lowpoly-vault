/**
 * Opt-in adapter for an EXISTING independently successful main release scope.
 * It cannot admit a proposed batch ahead of its trusted publication/CI evidence.
 * No JSON receipt, accept flag, caller-supplied proof, or capture draft grants trust.
 */
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {resolve} from 'node:path';
import {realpathSync} from 'node:fs';
import {assertBuiltRenderInputs, computeModelInputs, planModelReuse} from './ci-model-proof.mjs';
import {fetchVerifiedBaseProof, assertTrustedMainRun, assertTrustedSuite} from './ci-model-cache.mjs';
import {posterInputKey, posterSharedInputs} from './gallery-poster-inputs.mjs';
import {assertPosterProof, assertPosterPNG, posterArtifactName, posterRuntime} from './gallery-poster-proof.mjs';
import {assertPosterArtifact, extractPosterArtifact, MAX_POSTER_ARCHIVE_BYTES} from './gallery-poster-cache.mjs';
import {composeRegistry, digest, registryDigest} from './model-registry.mjs';
import {localReader, readLegacySnapshot, composedFiles, writeFreshTree, assertRegistryBaselineSource} from './model-registry-cli.mjs';

const admissions = new WeakMap(), SHA = /^[a-f0-9]{40}$/;
const git = (root, ...args) => execFileSync('git', args, {cwd: root, encoding: 'utf8', maxBuffer: 128 * 1024 * 1024}).trim();
function exactSource(root, sourceCommit) {
  assert.equal(realpathSync(root), root, 'Admission root symlink rejected');
  assert(SHA.test(sourceCommit || ''), 'Exact source commit required');
  assert.equal(git(root, 'rev-parse', 'HEAD'), sourceCommit, 'Admission source commit changed');
  assert.equal(git(root, 'status', '--porcelain', '--untracked-files=no'), '', 'Admission requires unchanged tracked source');
}
function assertSourceProjection(registry, root) {
  const projection = composeRegistry(registry), {snapshot} = readLegacySnapshot(localReader(root));
  assert.deepEqual(projection, snapshot, 'Registry is not the exact existing release scope; additions remain pending independent admission');
  return snapshot.manifest;
}
async function downloadBounded(response) {
  assert(response.ok, 'Dedicated poster artifact download failed');
  const declared = Number(response.headers.get('content-length') || 0);
  assert(Number.isFinite(declared) && declared >= 0 && declared <= MAX_POSTER_ARCHIVE_BYTES, 'Oversized declared poster artifact');
  if (!response.body?.getReader) { const data = Buffer.from(await response.arrayBuffer()); assert(data.length <= MAX_POSTER_ARCHIVE_BYTES); return data; }
  const reader = response.body.getReader(), chunks = []; let size = 0;
  try {
    while (true) { const {done, value} = await reader.read(); if (done) break; size += value.length; assert(size <= MAX_POSTER_ARCHIVE_BYTES, 'Oversized streamed poster artifact'); chunks.push(Buffer.from(value)); }
  } finally { await reader.cancel(); }
  return Buffer.concat(chunks);
}
/** Direct independent reads of the separate poster artifact from the SAME trusted run. */
async function exactRunPosters({repository, sourceCommit, verifiedModel, manifest, inputs, shared, token, fetchImpl}) {
  assert(token, 'Read-only GitHub proof access unavailable');
  const origin = `https://api.github.com/repos/${repository}`, signal = AbortSignal.timeout(180000);
  const headers = {Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'};
  const api = async path => { const response = await fetchImpl(`${origin}${path ? '/' + path : ''}`, {headers, signal}); assert(response.ok, `Independent admission read failed (${response.status}) at ${path || 'repository'}`); return response.json(); };
  const repo = await api(''); assert.equal(repo.full_name, repository); assert.equal(repo.default_branch, 'main');
  const workflow = await api('actions/workflows/full-release-review.yml'); assert.equal(workflow.id, verifiedModel.workflow_id);
  const run = await api(`actions/runs/${verifiedModel.run_id}`);
  const expected = {repository, repositoryId: repo.id, sourceSha: sourceCommit, workflowId: workflow.id};
  assertTrustedMainRun(run, expected); assert.equal(run.run_attempt, verifiedModel.run_attempt); assert.equal(run.check_suite_id, verifiedModel.check_suite_id);
  const attempt = await api(`actions/runs/${run.id}/attempts/${run.run_attempt}`); assertTrustedMainRun(attempt, expected);
  for (const key of ['id', 'run_attempt', 'check_suite_id', 'event']) assert.equal(attempt[key], run[key], 'Independent attempt changed');
  assertTrustedSuite(await api(`check-suites/${run.check_suite_id}`), run);
  const listed = await api(`actions/runs/${run.id}/artifacts?per_page=100`);
  const matches = listed.artifacts.filter(item => item.name === posterArtifactName(run.run_attempt));
  assert.equal(matches.length, 1, 'Missing or ambiguous dedicated poster artifact');
  const metadata = await api(`actions/artifacts/${matches[0].id}`); assert.equal(metadata.id, matches[0].id);
  const redirect = await fetchImpl(`${origin}/actions/artifacts/${metadata.id}/zip`, {headers, signal, redirect: 'manual'});
  assert.equal(redirect.status, 302, 'Dedicated poster artifact redirect unavailable');
  const destination = new URL(redirect.headers.get('location'));
  assert.equal(destination.protocol, 'https:'); assert.equal(destination.username, ''); assert.equal(destination.password, '');
  const bytes = await downloadBounded(await fetchImpl(destination.href, {signal})); // Never forward credentials to storage.
  assertPosterArtifact(metadata, run, bytes);
  const bundle = extractPosterArtifact(bytes);
  assertPosterProof(bundle.proof, {repository, sourceSha: sourceCommit, runId: run.id, runAttempt: run.run_attempt, policy_sha256: inputs.policy_sha256, runtime: posterRuntime(shared), manifest});
  assert.equal(bundle.proof.shared_sha256, shared.sha256, 'Poster renderer recipe differs');
  assert.deepEqual(bundle.proof.posters.map(row => row.id).sort(), manifest.assets.map(asset => asset.id).sort(), 'Admission requires complete independent poster coverage');
  for (const asset of manifest.assets) assert.equal(bundle.proof.posters.find(row => row.id === asset.id).input_sha256, posterInputKey(asset, shared), `Poster proof input binding differs: ${asset.id}`);
  return {...bundle, verification: {artifact_id: metadata.id, artifact_sha256: metadata.digest, run_id: run.id, run_attempt: run.run_attempt}};
}
function assertRegistryPosters(registry, bundle) {
  for (const record of registry.records) {
    const row = bundle.proof.posters.find(row => row.id === record.id);
    assert(row, `Missing independently verified poster: ${record.id}`);
    assert.equal(row.source_glb_sha256, record.asset.sha256.glb, 'Poster proof GLB differs');
    assert.deepEqual(row.poster, record.gallery.poster, 'Registry poster differs from independently verified capture');
    assert.deepEqual([...row.files].sort((a, b) => a.path.localeCompare(b.path)), [...record.gallery.files].sort((a, b) => a.path.localeCompare(b.path)), 'Registry poster seals differ from independent artifact');
    for (const kind of ['detail', 'wheel']) assertPosterPNG(bundle.files.get(row.poster[kind]), row.files.find(file => file.path === row.poster[kind]), kind);
  }
}

/**
 * Transport injection is for protected-code tests, not a repository data option.
 * Source/build/publication validators are fixed imports/commands, never callbacks.
 */
export async function admitExistingRegistryRelease({root, registry, repository, sourceCommit, outputRoot = 'dist', templatePath = 'qa/ci-model-proof/vite-template.html', token = process.env.GITHUB_TOKEN, fetchImpl = fetch}) {
  root = resolve(root); assert(/^[\w.-]+\/[\w.-]+$/.test(repository || ''), 'Exact repository required');
  assert.equal(typeof fetchImpl, 'function'); exactSource(root, sourceCommit);
  const baseline = Object.freeze(assertRegistryBaselineSource({root, registry, sourceCommit}));
  const manifest = assertSourceProjection(registry, root), recordDigest = registryDigest(registry);
  const built = await assertBuiltRenderInputs({root, outputRoot, templatePath}), inputs = computeModelInputs({root, built});
  const found = await fetchVerifiedBaseProof({root, repository, baseSha: sourceCommit, currentSha: sourceCommit, inputs, token, fetchImpl, allowAncestor: false});
  assert(found.baseProof && found.verifiedBaseProof, `No independent exact-source model proof: ${found.reasons.join('; ')}`);
  assert.equal(found.verifiedBaseProof.source_commit, sourceCommit, 'Ancestor-only evidence cannot admit a new release scope');
  const plan = planModelReuse({inputs, ...found});
  assert.equal(plan.fresh_ids.length, 0, 'Not every model has an independently verified matching built-input proof');
  assert.equal(found.baseProof.payload_sha256, built.payload_sha256, 'Successful CI tested a different delivered payload');
  const shared = await posterSharedInputs(root);
  const posters = await exactRunPosters({repository, sourceCommit, verifiedModel: found.verifiedBaseProof, manifest, inputs, shared, token, fetchImpl});
  assertRegistryPosters(registry, posters);
  // The exact legacy source/candidate/publication chain remains mandatory. It is
  // deliberately separate from render evidence and cannot be replaced by status JSON.
  const env = {...process.env}; for (const key of ['NODE_OPTIONS', 'NODE_PATH', 'PYTHONPATH', 'PYTHONHOME']) delete env[key];
  execFileSync(process.execPath, ['site/initial-release.mjs', '--check'], {cwd: root, env, encoding: 'utf8', maxBuffer: 4 * 1024 * 1024, timeout: 600000});
  exactSource(root, sourceCommit); assertSourceProjection(registry, root);
  const finalBuilt = await assertBuiltRenderInputs({root, outputRoot, templatePath}), finalInputs = computeModelInputs({root, built: finalBuilt});
  assert.equal(digest(finalInputs), digest(inputs), 'Admission inputs changed during validation');
  assert.equal(registryDigest(registry), recordDigest, 'Registry changed during validation');
  const handle = Object.freeze({version: 1, kind: 'verified-existing-release-admission', repository, source_commit: sourceCommit, registry_sha256: recordDigest, model_count: registry.records.length,
    model_artifact_id: found.verifiedBaseProof.artifact_id, poster_artifact_id: posters.verification.artifact_id, baseline_provenance: baseline});
  admissions.set(handle, {root, sourceCommit, registry: structuredClone(registry), inputDigest: digest(inputs), outputRoot, templatePath});
  return handle;
}

/** Generic projection consumes the opaque in-process admission, never serialized claims. */
export async function collectAdmittedRegistry(admission) {
  const state = admissions.get(admission); assert(state, 'An independently verified in-process admission is required; JSON cannot authorize publication');
  exactSource(state.root, state.sourceCommit); assertSourceProjection(state.registry, state.root);
  const built = await assertBuiltRenderInputs({root: state.root, outputRoot: state.outputRoot, templatePath: state.templatePath});
  assert.equal(digest(computeModelInputs({root: state.root, built})), state.inputDigest, 'Admitted model/build inputs changed');
  return composeRegistry(structuredClone(state.registry));
}
export async function writeAdmittedRegistryProjection(admission, destination) {
  await collectAdmittedRegistry(admission);
  const state = admissions.get(admission); writeFreshTree(destination, composedFiles(state.registry));
  return {source_commit: state.sourceCommit, models: state.registry.records.length, deployed: false};
}

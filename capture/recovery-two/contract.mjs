/** Capture-only boundary checks. No browser import, network, or publication writes. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile, realpath, readdir} from 'node:fs/promises';
import {resolve, sep} from 'node:path';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';

export const INPUTS_SHA256 = '2cc64ed8fd46e13a20ca33e5c1248c970b9c038b9e19f9f7d8b923b2751ca8e3';
export const BASE_COMMIT = '8423d2aaf6de34be5ffe1a5fd02f04b12267f674';
export const PARENT_COMMIT = '718f8d4078b1942a15a92d70dff0053655f06dbe';
export const BRANCH = 'validation/recovery-two-webgl-20261022';
export const PREFIX = 'capture/recovery-two';
export const WORKFLOW = '.github/workflows/recovery-two-runtime-capture.yml';
export const PAYLOAD_PATHS = [WORKFLOW, ...['contract.mjs', 'inputs.json', 'page.mjs', 'probe.mjs', 'test.mjs', 'recipe.json', 'models/phragmoceras.glb', 'models/spyroceras.glb'].map(p => `${PREFIX}/${p}`)].sort();
export const REPAIR_PATHS = [WORKFLOW, ...['contract.mjs', 'page.mjs', 'probe.mjs', 'test.mjs', 'recipe.json'].map(p => `${PREFIX}/${p}`)].sort();
export const LAUNCH_ARGS = ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'];
export const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
export const isSha = value => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);

export function safePath(path) {
  assert.equal(typeof path, 'string');
  assert(path && !path.startsWith('/') && !path.includes('\\') && !path.includes('\0'));
  assert(path.split('/').every(p => p && p !== '.' && p !== '..'), 'Unsafe relative path');
  return path;
}
export async function readLocal(root, path) {
  const canonicalRoot = await realpath(resolve(root));
  const absolute = resolve(canonicalRoot, safePath(path));
  assert(absolute.startsWith(canonicalRoot + sep));
  assert.equal(await realpath(absolute), absolute, `Symlink rejected: ${path}`);
  return readFile(absolute);
}
export function verifyBytes(bytes, pin, label) {
  assert.equal(bytes.length, pin.bytes, `${label}: byte length mismatch`);
  assert.equal(sha256(bytes), pin.sha256, `${label}: SHA256 mismatch`);
}
export function verifySubject(subject) {
  assert.deepEqual(Object.keys(subject).sort(), ['brief_sha256', 'glb_sha256', 'references_sha256', 'revision']);
  assert(typeof subject.revision === 'string' && subject.revision.length > 0);
  for (const key of ['glb_sha256', 'brief_sha256', 'references_sha256']) assert(isSha(subject[key]), key);
}
export function parsePinnedGlb(bytes, item) {
  verifyBytes(bytes, {bytes: item.bytes, sha256: item.subject.glb_sha256}, item.id);
  assert.equal(bytes.toString('ascii', 0, 4), 'glTF');
  assert.equal(bytes.readUInt32LE(4), 2);
  assert.equal(bytes.readUInt32LE(8), bytes.length);
  const length = bytes.readUInt32LE(12);
  assert.equal(bytes.readUInt32LE(16), 0x4e4f534a);
  const gltf = JSON.parse(bytes.toString('utf8', 20, 20 + length));
  assert.equal(gltf.asset.version, '2.0');
  assert.equal(gltf.buffers.length, 1);
  assert(!gltf.buffers[0].uri, 'External buffer forbidden');
  assert((gltf.images ?? []).length === 0 && (gltf.textures ?? []).length === 0, 'Unexpected textures');
  assert((gltf.animations ?? []).length === 0 && (gltf.skins ?? []).length === 0);
  assert.equal(gltf.scenes.length, 1);
  assert.equal(gltf.scene, 0);
  assert(gltf.nodes.every(n => !['matrix', 'translation', 'rotation', 'scale', 'skin'].some(k => k in n)), 'Pinned static identity-node scope changed');
  let triangles = 0, meshes = 0;
  for (const mesh of gltf.meshes) for (const primitive of mesh.primitives) {
    assert.equal(primitive.mode ?? 4, 4);
    assert(!primitive.targets && !primitive.extensions);
    triangles += gltf.accessors[primitive.indices].count / 3;
    meshes++;
  }
  assert.equal(triangles, item.expected.triangles);
  assert.equal(meshes, item.expected.primitive_meshes);
  assert.equal(gltf.materials.length, item.expected.materials);
  return {triangles, primitive_meshes: meshes, materials: gltf.materials.length};
}
export function decodeInputs(bytes) {
  assert.equal(sha256(bytes), INPUTS_SHA256, 'Frozen input/subject manifest mismatch');
  const input = JSON.parse(bytes);
  assert.equal(input.schema_version, 1);
  assert.equal(input.kind, 'two-candidate-runtime-inputs');
  assert.equal(input.repository, 's010s/lowpoly-vault');
  assert.equal(input.base_commit, BASE_COMMIT);
  assert.equal(input.branch, BRANCH);
  assert.deepEqual(input.items.map(i => i.id), ['spyroceras', 'phragmoceras']);
  assert.equal(input.items.reduce((sum, i) => sum + i.bytes, 0), 917016);
  for (const item of input.items) {
    verifySubject(item.subject);
    assert.equal(item.path, `${PREFIX}/models/${item.id}.glb`);
    assert(Number.isSafeInteger(item.expected.triangles) && item.expected.triangles > 0);
  }
  assert.equal(input.scene.instances_per_asset, 1);
  return input;
}
export async function loadInputs(root) {
  const input = decodeInputs(await readLocal(root, `${PREFIX}/inputs.json`));
  const files = new Map();
  for (const item of input.items) {
    const bytes = await readLocal(root, item.path);
    parsePinnedGlb(bytes, item);
    files.set(item.id, bytes);
  }
  return {input, files};
}
export async function verifyRecipe(root, expectedDigest) {
  assert(isSha(expectedDigest), 'Workflow must supply exact reviewed recipe SHA256');
  const bytes = await readLocal(root, `${PREFIX}/recipe.json`);
  assert.equal(sha256(bytes), expectedDigest, 'Reviewed probe recipe changed');
  const recipe = JSON.parse(bytes);
  assert.equal(recipe.schema_version, 1);
  assert.equal(recipe.kind, 'capture-only-source-seal');
  assert.equal(recipe.parent_commit, PARENT_COMMIT, 'Repair recipe requires exact failed-run parent');
  assert.equal(recipe.base_commit, BASE_COMMIT, 'Scientific baseline cannot change');
  // Workflow embeds this digest, so it cannot also be part of this digest cycle.
  const expected = PAYLOAD_PATHS.filter(p => p !== WORKFLOW && p !== `${PREFIX}/recipe.json`);
  assert.deepEqual(recipe.files.map(f => f.path).sort(), expected);
  for (const pin of recipe.files) verifyBytes(await readLocal(root, pin.path), pin, pin.path);
  return expectedDigest;
}
export async function verifyBaseline(root, input) {
  for (const pin of input.unchanged_baseline_files) verifyBytes(await readLocal(root, pin.path), pin, pin.path);
  const expectedWorkflows = [...input.unchanged_baseline_files.filter(p => p.path.startsWith('.github/workflows/')).map(p => p.path.split('/').at(-1)), WORKFLOW.split('/').at(-1)].sort();
  assert.deepEqual((await readdir(resolve(root, '.github/workflows'))).sort(), expectedWorkflows, 'Unexpected inherited workflow');
  const lock = JSON.parse(await readLocal(root, 'package-lock.json'));
  for (const [name, version] of [['three', input.toolchain.three], ['playwright', input.toolchain.playwright], ['playwright-core', input.toolchain.playwright]]) {
    assert.equal(lock.packages[`node_modules/${name}`].version, version);
  }
}
export function verifyEvent(env, event, head, parents, changed, parentParents, repairChanged) {
  assert.equal(env.GITHUB_ACTIONS, 'true');
  assert.equal(env.GITHUB_EVENT_NAME, 'push', 'Only authorized normal push; no PR/dispatch/replay route');
  assert.equal(env.GITHUB_REPOSITORY, 's010s/lowpoly-vault');
  assert.equal(env.GITHUB_REF, `refs/heads/${BRANCH}`, 'Wrong candidate ref');
  assert(/^[a-f0-9]{40}$/.test(env.GITHUB_SHA ?? ''));
  assert.equal(head, env.GITHUB_SHA, 'Checkout differs from event head');
  assert.notEqual(head, PARENT_COMMIT);
  assert.notEqual(head, BASE_COMMIT);
  assert.deepEqual(parents, [PARENT_COMMIT], 'Exactly one FF repair commit on the preserved failed-run commit required');
  assert.deepEqual(parentParents, [BASE_COMMIT], 'Failed-run commit must remain direct child of the audited scientific baseline');
  assert.deepEqual(repairChanged.slice().sort(), REPAIR_PATHS.map(p => `M\t${p}`).sort(), 'Repair may modify only the exact six existing adapter paths');
  assert.equal(event.repository?.full_name, env.GITHUB_REPOSITORY);
  assert.equal(event.ref, env.GITHUB_REF);
  assert.equal(event.after, head);
  assert.equal(event.forced, false, 'Forced push not allowed');
  assert.equal(event.deleted, false);
  assert.equal(event.before, PARENT_COMMIT, 'Only the explicit failed-run head may be fast-forwarded');
  assert.equal(event.created, false, 'Repair cannot create/recreate the branch');
  assert.equal(env.GITHUB_WORKFLOW_REF, `${env.GITHUB_REPOSITORY}/${WORKFLOW}@${env.GITHUB_REF}`);
  assert.equal(env.GITHUB_WORKFLOW_SHA, head);
  assert(/^[1-9][0-9]*$/.test(env.GITHUB_RUN_ID ?? ''));
  assert.equal(env.GITHUB_RUN_ATTEMPT, '1', 'No automatic rerun/old-evidence replay');
  assert.deepEqual(changed.slice().sort(), PAYLOAD_PATHS.map(p => `A\t${p}`).sort(), 'Commit changes exceed exact new-file payload');
}
export function gitRead(root, args) {
  return execFileSync('git', ['-c', 'protocol.allow=never', ...args], {
    cwd: root, encoding: 'utf8', timeout: 15000,
    env: {...process.env, GIT_NO_LAZY_FETCH: '1', GIT_TERMINAL_PROMPT: '0', GIT_OPTIONAL_LOCKS: '0'},
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
}
export async function preflight(root = process.cwd(), env = process.env) {
  const {input, files} = await loadInputs(root);
  await verifyBaseline(root, input);
  const recipe = await verifyRecipe(root, env.RECOVERY_RECIPE_SHA256);
  assert.equal(process.versions.node.split('.')[0], String(input.toolchain.node_major), 'Use existing Node22 CI toolchain');
  assert(!env.CHROMIUM_PATH, 'Alternate browser binary not allowed');
  const head = gitRead(root, ['rev-parse', 'HEAD']);
  const parentLine = gitRead(root, ['rev-list', '--parents', '-n', '1', 'HEAD']).split(' ');
  assert.equal(parentLine[0], head);
  const changed = gitRead(root, ['diff', '--no-ext-diff', '--no-renames', '--name-status', BASE_COMMIT, head]).split('\n');
  const parentChain = gitRead(root, ['rev-list', '--parents', '-n', '1', PARENT_COMMIT]).split(' ');
  assert.equal(parentChain[0], PARENT_COMMIT);
  const repairChanged = gitRead(root, ['diff', '--no-ext-diff', '--no-renames', '--name-status', PARENT_COMMIT, head]).split('\n');
  const event = JSON.parse(await readFile(env.GITHUB_EVENT_PATH));
  verifyEvent(env, event, head, parentLine.slice(1), changed, parentChain.slice(1), repairChanged);
  assert.equal(gitRead(root, ['status', '--porcelain', '--untracked-files=no']), '', 'Tracked checkout is modified');
  return {input, files, provenance: {repository: input.repository, base_commit: BASE_COMMIT, parent_commit: PARENT_COMMIT, source_commit: head, ref: env.GITHUB_REF, event: env.GITHUB_EVENT_NAME, workflow_ref: env.GITHUB_WORKFLOW_REF, workflow_sha: env.GITHUB_WORKFLOW_SHA, workflow_sha256: sha256(await readLocal(root, WORKFLOW)), input_sha256: INPUTS_SHA256, recipe_sha256: recipe, run_id: env.GITHUB_RUN_ID, run_attempt: Number(env.GITHUB_RUN_ATTEMPT), run_url: `https://github.com/${input.repository}/actions/runs/${env.GITHUB_RUN_ID}`, node: process.version}};
}
export function checkMeasurement(measured, items, browserVersion) {
  assert.equal(measured.runtime.engine, 'Three.js');
  assert.equal(measured.runtime.version, '180');
  assert.equal(measured.runtime.browser, browserVersion);
  assert.equal(browserVersion, '141.0.7390.37');
  assert.equal(measured.runtime.context, 'WebGL2');
  assert.equal(measured.runtime.context_created, true);
  assert.equal(measured.runtime.rendered, true);
  assert.equal(measured.runtime.output_color_space, 'srgb');
  assert.equal(measured.runtime.tone_mapping, 'ACESFilmicToneMapping');
  assert.equal(measured.runtime.exposure, 1);
  assert.match(measured.runtime.device, /SwiftShader/i);
  assert.match(measured.runtime.renderer, /ANGLE/i);
  assert.equal(measured.runtime.rendered_frames, 3);
  assert.equal(measured.context_lost, false);
  assert.equal(measured.gl_error, 0);
  assert.deepEqual(measured.shader_errors, []);
  assert.equal(measured.runtime.triangles, items.reduce((n, i) => n + i.expected.triangles, 0));
  assert.equal(measured.runtime.draw_calls, items.reduce((n, i) => n + i.expected.primitive_meshes, 0));
  assert(measured.foreground_pixels > 500, 'Actual image must contain non-background model pixels');
  assert.deepEqual(measured.assets.map(i => i.id), items.map(i => i.id));
  assert.equal(measured.transport.method, 'native Fetch Response.arrayBuffer + Three r180 GLTFLoader.parseAsync');
  assert.deepEqual(measured.transport.transfers.map(t => t.asset_id), items.map(i => i.id));
  for (const item of items) {
    const transfer = measured.transport.transfers.find(t => t.asset_id === item.id);
    assert.equal(transfer.status, 200);
    assert.equal(transfer.bytes, item.bytes);
    assert.equal(transfer.content_length, String(item.bytes));
    assert.equal(transfer.sha256, item.subject.glb_sha256);
    assert.equal(transfer.phase, 'GLTFLoader-parse-complete');
  }
  for (let k = 0; k < items.length; k++) {
    const actual = measured.assets[k], expected = items[k];
    assert.equal(actual.glb_sha256, expected.subject.glb_sha256);
    assert.equal(actual.instances, 1);
    assert.equal(actual.triangles, expected.expected.triangles);
    assert.equal(actual.meshes, expected.expected.primitive_meshes);
    assert.equal(actual.materials, expected.expected.materials);
    assert.deepEqual(actual.presentation_scale, [1, 1, 1]);
    assert.deepEqual(actual.presentation_rotation, [0, 0, 0]);
    assert.equal(actual.all_meshes_in_frustum, true);
    assert.equal(actual.all_bounds_inside_clipping, true);
    for (const bound of ['min', 'max']) for (let n = 0; n < 3; n++) assert(Math.abs(actual.authored_bounds[bound][n] - expected.expected.bounds[bound][n]) < 1e-8, 'Authored bound changed');
  }
}
export function checkTransfers(records, items) {
  assert(records.length > 0, 'No network lifecycle evidence');
  for (const row of records) {
    assert.equal(row.terminal, 'finished', `Request not successfully complete: ${row.path}`);
    assert.equal(row.status, 200, `HTTP response failed: ${row.path}`);
    assert.equal(row.failure, null, `Request failed: ${row.path}`);
    assert.equal(row.response_finished, 'success', `Response completion failed/pending: ${row.path}`);
    assert(row.events.includes('response.finished'));
    assert(row.events.includes('request') && row.events.includes('response') && row.events.includes('requestfinished'));
    assert(!row.events.includes('requestfailed'), 'Any failed request remains fatal');
  }
  const models = records.filter(row => row.path.startsWith('/models/'));
  assert.deepEqual(models.map(row => row.path).sort(), items.map(item => `/models/${item.id}.glb`).sort(), 'Exactly one complete request for each exact model is required');
  for (const item of items) {
    const row = models.find(row => row.path === `/models/${item.id}.glb`);
    assert.equal(row.headers['content-length'], String(item.bytes), 'Response length header mismatch');
    assert.equal(row.headers['cache-control'], 'no-store');
    assert.equal(row.headers['content-type'], 'model/gltf-binary');
    assert(!row.headers['transfer-encoding'], 'Unexpected chunked model framing');
  }
}
export function makePendingReport({item, stage, frames, images, provenance, scene, warnings = []}) {
  assert(['gpu', 'scene'].includes(stage));
  assert(frames.length && images.length === frames.length);
  const required = images.map(e => ({id: e.id, sha256: e.sha256}));
  const report = {
    schema_version: 1, kind: `${stage}_report`, stage, subject: item.subject,
    status: 'unknown', measured_status: 'pass',
    method: 'Actual pinned Chromium / Three.js GLTFLoader / ANGLE SwiftShader WebGL2; no mocked context, no CPU fallback.',
    observations: frames.map(f => `${f.view}: ${f.runtime.rendered_frames} rendered frames; final frame ${f.runtime.draw_calls} draw calls, ${f.runtime.triangles} triangles, ${f.foreground_pixels} foreground pixels; GL error ${f.gl_error}.`),
    runtime: frames[0].runtime, runtime_scope: 'First measured view; each view has its own measured runtime in frames.', frames, screenshots: images.map(e => e.id),
    errors: [], warnings, warning_review: [], reviewed_evidence: [],
    review_required_evidence: required,
    independent_review: {status: 'pending', note: 'No reviewer identity or pixel-inspection attestation is supplied by this automated producer. A separate reviewer must inspect every image and decide frozen-brief coverage.'},
    provenance, formal_acceptance: 'BLOCKED', physical_gpu_verified: false,
  };
  if (stage === 'scene') {
    report.scene_description = scene.description;
    report.scene_assets = frames[0].assets;
  }
  return report;
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  assert.deepEqual(process.argv.slice(2), ['--preflight']);
  const {provenance} = await preflight();
  console.log(JSON.stringify({status: 'PASS_INPUTS_AND_CI_BOUNDARY_ONLY', rendered: false, provenance}, null, 2));
}

/** Unit/static tests only. Synthetic measurements here are not rendered evidence. */
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile, mkdtemp, writeFile, symlink, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createServer} from 'node:http';
import {runInNewContext} from 'node:vm';
import {webcrypto} from 'node:crypto';
import {BASE_COMMIT, PARENT_COMMIT, REPAIR_PATHS, BRANCH, PREFIX, WORKFLOW, PAYLOAD_PATHS, INPUTS_SHA256, sha256, safePath, readLocal, verifyBytes, verifySubject, decodeInputs, loadInputs, parsePinnedGlb, verifyRecipe, verifyEvent, checkMeasurement, checkTransfers, makePendingReport, LAUNCH_ARGS} from './contract.mjs';

const root = process.cwd();
const inputBytes = await readFile(`${PREFIX}/inputs.json`);
const input = decodeInputs(inputBytes);
const {files} = await loadInputs(root);
const clone = value => structuredClone(value);
test('exact two input bytes and full subjects are frozen', () => {
  assert.equal(sha256(inputBytes), INPUTS_SHA256);
  assert.equal(files.size, 2);
  assert.equal([...files.values()].reduce((n, b) => n + b.length, 0), 917016);
  for (const item of input.items) verifySubject(item.subject);
});
for (const item of input.items) {
  test(`${item.id}: exact GLB parses statically, no WebGL claim`, () => {
    assert.deepEqual(parsePinnedGlb(files.get(item.id), item), {triangles: item.expected.triangles, primitive_meshes: item.expected.primitive_meshes, materials: item.expected.materials});
  });
  test(`${item.id}: one changed byte rejected`, () => {
    const b = Buffer.from(files.get(item.id)); b[b.length - 1] ^= 1;
    assert.throws(() => parsePinnedGlb(b, item), /SHA256/);
  });
  test(`${item.id}: truncated GLB rejected`, () => assert.throws(() => parsePinnedGlb(files.get(item.id).subarray(0, -4), item), /length/));
  test(`${item.id}: other candidate bytes rejected`, () => assert.throws(() => parsePinnedGlb(files.get(input.items.find(i => i.id !== item.id).id), item)));
  for (const key of ['revision', 'glb_sha256', 'brief_sha256', 'references_sha256']) {
    test(`${item.id}: changed ${key} rejects entire manifest`, () => {
      const changed = clone(input); changed.items.find(i => i.id === item.id).subject[key] = key === 'revision' ? 'different-revision' : '0'.repeat(64);
      assert.throws(() => decodeInputs(Buffer.from(JSON.stringify(changed))), /manifest mismatch/);
    });
  }
}
for (const path of ['/absolute', '../escape', 'a/../b', 'a//b', 'a/./b', 'a\\b', 'a\0b', '']) test(`reject unsafe path ${JSON.stringify(path)}`, () => assert.throws(() => safePath(path)));
test('reject symbolic link inputs', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'recovery-path-test-'));
  try { await writeFile(join(dir, 'actual'), 'safe'); await symlink('actual', join(dir, 'alias')); await assert.rejects(readLocal(dir, 'alias'), /Symlink/); }
  finally { await rm(dir, {recursive: true, force: true}); }
});
test('hash validation rejects invalid bytes even if length matches', () => assert.throws(() => verifyBytes(Buffer.from('abc'), {bytes: 3, sha256: '0'.repeat(64)}, 'fixture'), /SHA256/));

// Explicitly synthetic CI contexts exercise denial boundaries only.
const head = '1'.repeat(40);
const env = {GITHUB_ACTIONS: 'true', GITHUB_EVENT_NAME: 'push', GITHUB_REPOSITORY: 's010s/lowpoly-vault', GITHUB_REF: `refs/heads/${BRANCH}`, GITHUB_SHA: head, GITHUB_WORKFLOW_REF: `s010s/lowpoly-vault/${WORKFLOW}@refs/heads/${BRANCH}`, GITHUB_WORKFLOW_SHA: head, GITHUB_RUN_ID: '123', GITHUB_RUN_ATTEMPT: '1'};
const event = {repository: {full_name: env.GITHUB_REPOSITORY}, ref: env.GITHUB_REF, after: head, before: PARENT_COMMIT, created: false, forced: false, deleted: false};
const changed = PAYLOAD_PATHS.map(p => `A\t${p}`);
const repairChanged = REPAIR_PATHS.map(p => `M\t${p}`);
const check = (e = env, v = event, h = head, parents = [PARENT_COMMIT], paths = changed, parentParents = [BASE_COMMIT], repairPaths = repairChanged) => verifyEvent(e, v, h, parents, paths, parentParents, repairPaths);
test('synthetic exact FF repair push shape passes boundary only', () => check());
for (const eventName of ['workflow_dispatch', 'pull_request', 'pull_request_target', 'workflow_call', 'schedule']) test(`reject ${eventName}`, () => assert.throws(() => check({...env, GITHUB_EVENT_NAME: eventName})));
for (const branch of ['main', 'publish/test', 'capture/test', 'render/test', BRANCH + '-other']) test(`reject wrong branch ${branch}`, () => assert.throws(() => check({...env, GITHUB_REF: `refs/heads/${branch}`})));
for (const [key, value] of [['GITHUB_ACTIONS', 'false'], ['GITHUB_REPOSITORY', 'other/repo'], ['GITHUB_SHA', '2'.repeat(40)], ['GITHUB_WORKFLOW_REF', 'wrong/workflow'], ['GITHUB_WORKFLOW_SHA', BASE_COMMIT], ['GITHUB_RUN_ID', ''], ['GITHUB_RUN_ATTEMPT', '2']]) test(`reject changed CI ${key}`, () => assert.throws(() => check({...env, [key]: value})));
for (const [key, value] of [['ref', 'refs/heads/main'], ['after', BASE_COMMIT], ['before', '3'.repeat(40)], ['forced', true], ['deleted', true], ['repository', {full_name: 'fork/lowpoly-vault'}]]) test(`reject changed event ${key}`, () => assert.throws(() => check(env, {...event, [key]: value})));
test('reject missing forced flag rather than assume false', () => { const v = clone(event); delete v.forced; assert.throws(() => check(env, v)); });
test('reject unrelated checkout head', () => assert.throws(() => check(env, event, BASE_COMMIT)));
test('reject wrong parent', () => assert.throws(() => check(env, event, head, ['4'.repeat(40)])));
test('reject merge parent', () => assert.throws(() => check(env, event, head, [BASE_COMMIT, '5'.repeat(40)])));
test('reject additional production file', () => assert.throws(() => check(env, event, head, [PARENT_COMMIT], [...changed, 'M\tassets/manifest.json'])));
test('reject missing payload file', () => assert.throws(() => check(env, event, head, [PARENT_COMMIT], changed.slice(1))));
test('reject modified existing path instead of new isolated file', () => assert.throws(() => check(env, event, head, [PARENT_COMMIT], changed.map((p, i) => i === 0 ? p.replace('A\t', 'M\t') : p))));
test('recipe binds every input/script and has no output/extra source', async () => {
  const workflow = await readFile(WORKFLOW, 'utf8');
  const digest = /^\s+RECOVERY_RECIPE_SHA256: '([a-f0-9]{64})'$/m.exec(workflow)?.[1];
  await verifyRecipe(root, digest);
  await assert.rejects(verifyRecipe(root, '0'.repeat(64)), /recipe changed/);
});
test('new workflow is read-only, push-only, nondeploying and sparse', async () => {
  const w = await readFile(WORKFLOW, 'utf8');
  assert.match(w, /'on':\n  push:\n    branches: \['validation\/recovery-two-webgl-20261022'\]/);
  assert.match(w, /permissions:\n  contents: read\n/);
  assert.equal((w.match(/^permissions:/gm) ?? []).length, 1);
  assert(!/pull_request|workflow_dispatch|workflow_call|secrets:|secrets\.|pages:|id-token:|contents: write|environment:|deploy-pages|upload-pages|npm run build|npm run publication|git push|continue-on-error/.test(w));
  assert.match(w, /persist-credentials: false/);
  assert.match(w, /fetch-depth: 3/);
  assert.match(w, /sparse-checkout-cone-mode: false/);
  assert.match(w, /npm ci --ignore-scripts/);
  assert.match(w, /node site\/ci-install-chromium.mjs/);
  assert.match(w, /if-no-files-found: error/);
  assert.deepEqual(LAUNCH_ARGS, ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']);
});

function syntheticMeasurement(items = input.items) {
  return {view: 'fixture-not-rendered', runtime: {engine: 'Three.js', version: '180', browser: input.toolchain.chromium, context: 'WebGL2', context_created: true, rendered: true, output_color_space: 'srgb', tone_mapping: 'ACESFilmicToneMapping', exposure: 1, renderer: 'ANGLE synthetic fixture', device: 'SwiftShader synthetic fixture', rendered_frames: 3, triangles: items.reduce((n, i) => n + i.expected.triangles, 0), draw_calls: items.reduce((n, i) => n + i.expected.primitive_meshes, 0)}, transport: {method: 'native Fetch Response.arrayBuffer + Three r180 GLTFLoader.parseAsync', transfers: items.map(i => ({asset_id: i.id, status: 200, bytes: i.bytes, content_length: String(i.bytes), sha256: i.subject.glb_sha256, phase: 'GLTFLoader-parse-complete'}))}, context_lost: false, gl_error: 0, shader_errors: [], foreground_pixels: 501, assets: items.map(i => ({id: i.id, glb_sha256: i.subject.glb_sha256, instances: 1, triangles: i.expected.triangles, meshes: i.expected.primitive_meshes, materials: i.expected.materials, presentation_scale: [1, 1, 1], presentation_rotation: [0, 0, 0], all_meshes_in_frustum: true, all_bounds_inside_clipping: true, authored_bounds: i.expected.bounds}))};
}
test('synthetic measurement validation is explicitly not a runtime result', () => checkMeasurement(syntheticMeasurement(), input.items, input.toolchain.chromium));
for (const [key, value] of [['engine', 'other'], ['version', '179'], ['browser', 'other'], ['context', 'WebGL1'], ['context_created', false], ['rendered', false], ['output_color_space', 'linear'], ['tone_mapping', 'None'], ['exposure', 0.5], ['device', 'unknown'], ['renderer', 'unknown'], ['rendered_frames', 0], ['draw_calls', 0], ['triangles', 1]]) test(`reject invalid measured runtime ${key}`, () => { const m = syntheticMeasurement(); m.runtime[key] = value; assert.throws(() => checkMeasurement(m, input.items, input.toolchain.chromium)); });
for (const [key, value] of [['context_lost', true], ['gl_error', 1282], ['shader_errors', ['compile failed']], ['foreground_pixels', 0]]) test(`reject invalid measurement ${key}`, () => { const m = syntheticMeasurement(); m[key] = value; assert.throws(() => checkMeasurement(m, input.items, input.toolchain.chromium)); });
for (const [key, value] of [['glb_sha256', '0'.repeat(64)], ['instances', 0], ['triangles', 0], ['meshes', 0], ['materials', 0], ['presentation_scale', [2, 2, 2]], ['presentation_rotation', [1, 0, 0]], ['all_meshes_in_frustum', false], ['all_bounds_inside_clipping', false]]) test(`reject invalid scene asset ${key}`, () => { const m = syntheticMeasurement(); m.assets[0][key] = value; assert.throws(() => checkMeasurement(m, input.items, input.toolchain.chromium)); });
test('reject rescaled authored bounds', () => { const m = syntheticMeasurement(); m.assets = clone(m.assets); m.assets[0].authored_bounds.max[1] *= 2; assert.throws(() => checkMeasurement(m, input.items, input.toolchain.chromium)); });
test('reject scene that omits one exact candidate', () => { const m = syntheticMeasurement(); m.assets.pop(); assert.throws(() => checkMeasurement(m, input.items, input.toolchain.chromium)); });
test('producer never creates reviewer identity or formal approval', () => {
  const item = input.items[0], images = [{id: 'fixture-image-not-rendered', sha256: '0'.repeat(64)}];
  for (const stage of ['gpu', 'scene']) {
    const report = makePendingReport({item, stage, frames: [syntheticMeasurement()], images, provenance: {synthetic_test: true}, scene: input.scene});
    assert.equal(report.schema_version, 1);
    assert.equal(report.status, 'unknown');
    assert.equal(report.formal_acceptance, 'BLOCKED');
    assert.equal(report.independent_review.status, 'pending');
    assert.deepEqual(report.reviewed_evidence, []);
    assert.deepEqual(report.review_required_evidence, images);
    assert(!('reviewer' in report) && !('reviewed_at' in report));
    if (stage === 'scene') { assert.equal(report.scene_description, input.scene.description); assert.equal(report.scene_assets.length, 2); }
  }
});
test('report cannot be assembled without image evidence', () => assert.throws(() => makePendingReport({item: input.items[0], stage: 'gpu', frames: [syntheticMeasurement()], images: []})));

// Narrow repair-chain negative cases. No general ancestor exception.
test('reject direct-baseline parent for r002', () => assert.throws(() => check(env, event, head, [BASE_COMMIT])));
test('reject failed-run parent with different baseline ancestry', () => assert.throws(() => check(env, event, head, [PARENT_COMMIT], changed, ['2'.repeat(40)])));
test('reject failed-run parent with merge ancestry', () => assert.throws(() => check(env, event, head, [PARENT_COMMIT], changed, [BASE_COMMIT, '2'.repeat(40)])));
test('reject branch creation or first-push replay', () => assert.throws(() => check(env, {...event, created: true, before: '0'.repeat(40)})));
test('reject replaying the failed-run head as the repair', () => assert.throws(() => check({...env, GITHUB_SHA: PARENT_COMMIT}, {...event, after: PARENT_COMMIT}, PARENT_COMMIT)));
test('reject changing a model in repair diff even within cumulative nine paths', () => assert.throws(() => check(env, event, head, [PARENT_COMMIT], changed, [BASE_COMMIT], [...repairChanged, 'M\tcapture/recovery-two/models/phragmoceras.glb'])));
test('reject omitting the reviewed repair path', () => assert.throws(() => check(env, event, head, [PARENT_COMMIT], changed, [BASE_COMMIT], repairChanged.slice(1))));
function completeTransferRows() {
  return input.items.map(i => ({path: `/models/${i.id}.glb`, terminal: 'finished', status: 200, failure: null, response_finished: 'success', events: ['request', 'response', 'requestfinished', 'response.finished'], headers: {'content-length': String(i.bytes), 'content-type': 'model/gltf-binary', 'cache-control': 'no-store'}}));
}
test('synthetic successful lifecycle structure only', () => checkTransfers(completeTransferRows(), input.items));
for (const [key, value] of [['terminal', 'pending'], ['terminal', 'failed'], ['status', 404], ['failure', 'net::ERR_ABORTED'], ['response_finished', 'failed'], ['response_finished', 'pending']]) test(`reject network ${key}=${value}`, () => { const rows = completeTransferRows(); rows[0][key] = value; assert.throws(() => checkTransfers(rows, input.items)); });
test('reject ERR_ABORTED even after an apparent finished event', () => { const rows = completeTransferRows(); rows[0].events.push('requestfailed'); assert.throws(() => checkTransfers(rows, input.items)); });
test('reject absent model request lifecycle', () => assert.throws(() => checkTransfers(completeTransferRows().slice(1), input.items)));
test('reject duplicate model fetch', () => { const rows = completeTransferRows(); rows.push(clone(rows[0])); assert.throws(() => checkTransfers(rows, input.items)); });
for (const [key, value] of [['content-length', '1'], ['cache-control', 'no-cache'], ['content-type', 'text/plain'], ['transfer-encoding', 'chunked']]) test(`reject model framing ${key}`, () => { const rows = completeTransferRows(); rows[0].headers[key] = value; assert.throws(() => checkTransfers(rows, input.items)); });
for (const [key, value] of [['bytes', 0], ['sha256', '0'.repeat(64)], ['phase', 'native-body-complete'], ['status', 404]]) test(`reject browser exact transport ${key}`, () => { const m = syntheticMeasurement(); m.transport.transfers[0][key] = value; assert.throws(() => checkMeasurement(m, input.items, input.toolchain.chromium)); });

// Execute the exact new browser transport helper against a real local HTTP server
// using Node native Fetch, without importing Three, rendering, or claiming Chromium proof.
const pageSource = await readFile(`${PREFIX}/page.mjs`, 'utf8');
const helperSource = pageSource.slice(pageSource.indexOf('export async function fetchPinnedModel'), pageSource.indexOf('export async function renderFrame')).replace('export async function', 'async function') + '\nfetchPinnedModel;';
async function testActualTransport(item, mode) {
  const original = files.get(item.id), mutated = Buffer.from(original); mutated[mutated.length - 1] ^= 1;
  const server = createServer((req, res) => {
    res.setHeader('Content-Type', 'model/gltf-binary');
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('Content-Length', String(item.bytes));
    if (mode === 'status') res.statusCode = 404;
    if (mode === 'length') res.setHeader('Content-Length', '1');
    if (mode === 'cache') res.setHeader('Cache-Control', 'no-cache');
    if (mode === 'truncated') { res.setHeader('Connection', 'close'); res.end(original.subarray(0, original.length - 4)); return; }
    res.end(mode === 'mutated' ? mutated : original);
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const context = {crypto: webcrypto, fetch: (path, options) => fetch(`http://127.0.0.1:${server.address().port}${path}`, options)};
  const load = runInNewContext(helperSource, context);
  try { return await load(item); }
  finally { server.closeAllConnections(); await new Promise(resolve => server.close(resolve)); }
}
for (const item of input.items) test(`actual local HTTP exact-body integrity ${item.id}, not Chromium or GPU`, async () => { const result = await testActualTransport(item, 'exact'); assert.equal(result.bytes.byteLength, item.bytes); assert.equal(result.transfer.sha256, item.subject.glb_sha256); assert.equal(result.transfer.phase, 'exact-bytes-verified'); });
for (const mode of ['status', 'length', 'cache', 'mutated', 'truncated']) test(`actual local HTTP rejects ${mode}`, async () => { await assert.rejects(testActualTransport(input.items[1], mode)); });

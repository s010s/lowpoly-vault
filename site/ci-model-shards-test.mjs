/** Sharding may change scheduling, never exact required coverage or artifact identity. */
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync, symlinkSync, existsSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';
import { modelPlan, expandModelTasks, modelReceipt, assertModelCoverage, readModelReceipts, payloadDigest, verifyBuild, auditBuild, BUILD_RECEIPT } from './ci-model-shards.mjs';
import { sha256 } from './ci-provenance.mjs';
import { classify } from './ci-scope.mjs';
const clone = value => structuredClone(value);
const manifest = { assets: Array.from({ length: 190 }, (_, index) => ({ id: `model-${String(index).padStart(3, '0')}`, glb: `assets/model-${index}.glb`, sha256: { glb: sha256(String(index)) } })) };
const plan = modelPlan(manifest, { runtime: true, ids: 'untrusted-selection-is-ignored' });
assert.equal(plan.length, 5);
assert.deepEqual(plan.map(shard => shard.ids.length), [38, 38, 38, 38, 38]);
assert.deepEqual(plan.flatMap(shard => shard.ids).sort(), manifest.assets.map(asset => asset.id));
assert.deepEqual(modelPlan({ assets: [...manifest.assets].reverse() }, { runtime: true }), plan);
const selected = modelPlan(manifest, { ids: 'model-041,model-004' });
assert.deepEqual(selected.flatMap(shard => shard.ids).sort(), ['model-004', 'model-041']);
assert.equal(modelPlan(manifest, { ids: 'model-004' }).length, 1);
for (const ids of ['', 'model-004,model-004', 'unpublished']) assert.throws(() => modelPlan(manifest, { ids }));
assert.throws(() => modelPlan({ assets: [manifest.assets[0], manifest.assets[0]] }, { runtime: true }));
const docs = classify(['docs/readme.md'], manifest);
assert.deepEqual(expandModelTasks(docs, manifest), ['none']);
const scoped = classify([manifest.assets[4].glb], manifest);
assert.deepEqual(expandModelTasks(scoped, manifest), ['models-1-of-1', 'previews']);
for (const path of ['site/ci-scope.mjs', '.github/workflows/pages.yml', 'unclassified/file']) {
  const full = classify([path], manifest);
  assert.equal(full.runtime, true);
  assert.equal(expandModelTasks(full, manifest).filter(task => task.startsWith('models-')).length, 5);
}
const identity = { source_commit: 'a'.repeat(40), source_tree: 'b'.repeat(40), control_sha256: 'c'.repeat(64), manifest_sha256: 'd'.repeat(64), runtime_config: { node_major: '22', site_base: '/lowpoly-vault/' }, run_id: '123', run_attempt: '1' };
const build = { version: 1, identity, payload_sha256: 'e'.repeat(64) };
const browserFor = shard => ({ status: 'pass', browser_status: 'pass', profile: 'strict-gpu', review_scope: 'models', commit: identity.source_commit, gpu: { status: 'pass' }, page_errors: [], resource_errors: [], selected_model_ids: shard.ids, models: shard.ids.map(id => ({ id, status: 'gpu-pass', glb_sha256: manifest.assets.find(asset => asset.id === id).sha256.glb })) });
const receipts = plan.map(shard => modelReceipt(manifest, plan, shard, browserFor(shard), build));
assert.equal(assertModelCoverage(manifest, plan, receipts, identity, build).ids.length, 190);
const refuse = change => { const next = clone(receipts); change(next); assert.throws(() => assertModelCoverage(manifest, plan, next, identity, build)); };
refuse(rows => rows.pop());
refuse(rows => rows.push(clone(rows[0])));
refuse(rows => { rows[1] = clone(rows[0]); });
refuse(rows => { rows[0].task = 'models-99-of-5'; });
refuse(rows => rows[0].models.pop());
refuse(rows => rows[0].models.push(clone(rows[0].models[0])));
refuse(rows => { rows[0].models[0].id = 'unpublished'; });
refuse(rows => { rows[0].models[0].glb_sha256 = '0'.repeat(64); });
refuse(rows => { rows[0].models[0].status = 'fallback-only'; });
refuse(rows => { rows[0].plan_sha256 = '0'.repeat(64); });
refuse(rows => { rows[0].payload_sha256 = '0'.repeat(64); });
refuse(rows => rows.forEach(row => { row.payload_sha256 = '0'.repeat(64); }));
for (const key of ['source_commit', 'source_tree', 'control_sha256', 'manifest_sha256', 'run_id', 'run_attempt']) refuse(rows => { rows[0].identity[key] = 'different'; });
refuse(rows => { rows[0].identity.runtime_config.node_major = '999'; });
assert.throws(() => assertModelCoverage(manifest, plan, receipts, identity));
assert.throws(() => assertModelCoverage(manifest, plan, receipts, identity, { ...build, identity: { ...identity, control_sha256: '0'.repeat(64) } }));
for (const mutate of [b => { b.status = 'fail'; }, b => { b.browser_status = 'blocked'; }, b => { b.profile = 'allow-webgl-fallback'; }, b => { b.models = []; }, b => { b.models[0].glb_sha256 = '0'.repeat(64); }, b => { b.selected_model_ids = ['model-099']; }, b => { b.page_errors = ['bad']; }]) {
  const browser = browserFor(plan[0]); mutate(browser);
  assert.throws(() => modelReceipt(manifest, plan, plan[0], browser, build));
}
const root = mkdtempSync(join(tmpdir(), 'lpv-model-shard-'));
try {
  const artifacts = join(root, 'artifacts'); mkdirSync(artifacts);
  for (const receipt of receipts) { const folder = join(artifacts, `model-shard-${receipt.task}`); mkdirSync(folder); writeFileSync(join(folder, `${receipt.task}.json`), JSON.stringify(receipt)); }
  assert.deepEqual(readModelReceipts(artifacts, plan), receipts);
  mkdirSync(join(artifacts, 'unexpected')); assert.throws(() => readModelReceipts(artifacts, plan)); rmSync(join(artifacts, 'unexpected'), { recursive: true });
  writeFileSync(join(artifacts, `model-shard-${plan[0].task}`, 'extra.json'), '{}'); assert.throws(() => readModelReceipts(artifacts, plan));
  rmSync(artifacts, { recursive: true });
  mkdirSync(join(root, 'assets')); writeFileSync(join(root, 'assets/model.glb'), 'model'); writeFileSync(join(root, 'index.html'), 'page');
  const sealed = { version: 1, identity, payload_sha256: payloadDigest(root) };
  writeFileSync(join(root, BUILD_RECEIPT), JSON.stringify(sealed));
  assert.deepEqual(verifyBuild(root, identity), sealed);
  writeFileSync(join(root, 'index.html'), 'changed'); assert.throws(() => verifyBuild(root, identity));
  writeFileSync(join(root, 'index.html'), 'page'); writeFileSync(join(root, 'extra'), 'unexpected'); assert.throws(() => verifyBuild(root, identity));
  rmSync(join(root, 'extra')); rmSync(join(root, 'assets/model.glb')); assert.throws(() => verifyBuild(root, identity));
  writeFileSync(join(root, 'assets/model.glb'), 'model');
  assert.throws(() => verifyBuild(root, { ...identity, source_tree: 'changed' }));
  const sealBytes = readFileSync(join(root, BUILD_RECEIPT));
  const sameSeal = () => assert.deepEqual(readFileSync(join(root, BUILD_RECEIPT)), sealBytes, 'Exact seal bytes restored after every audit result');
  const strictAudit = () => assert.deepEqual(readdirSync(root).sort(), ['assets', 'index.html'], 'Original deployment inventory does not allow an internal CI seal');
  assert.deepEqual(auditBuild(root, identity, strictAudit), sealed); sameSeal();
  assert.throws(() => auditBuild(root, identity, () => { strictAudit(); throw Error('Original audit failed'); }), /Original audit failed/); sameSeal();
  assert.throws(() => auditBuild(root, identity, () => { writeFileSync(join(root, 'index.html'), 'evil'); }), /Audit changed the sealed deployment payload/); sameSeal();
  writeFileSync(join(root, 'index.html'), 'page');
  assert.throws(() => auditBuild(root, identity, () => { writeFileSync(join(root, 'unexpected'), 'not allowed'); strictAudit(); }), /Original deployment inventory/); sameSeal(); rmSync(join(root, 'unexpected'));
  assert.throws(() => auditBuild(root, identity, () => writeFileSync(join(root, BUILD_RECEIPT), '{}')), /reserved build seal/); sameSeal();
  assert.throws(() => auditBuild(root, identity, () => symlinkSync('missing-target', join(root, BUILD_RECEIPT))), /reserved build seal/); sameSeal();
  let invoked = false; writeFileSync(join(root, 'extra'), 'unsealed');
  assert.throws(() => auditBuild(root, identity, () => { invoked = true; })); assert.equal(invoked, false); sameSeal(); rmSync(join(root, 'extra'));
  assert.throws(() => auditBuild(root, { ...identity, run_id: 'wrong' }, strictAudit)); sameSeal();
  symlinkSync('index.html', join(root, 'linked')); assert.throws(() => payloadDigest(root));
} finally { rmSync(root, { recursive: true, force: true }); }
// Exercise the real scope -> wrapper -> receipt path with a tiny fake browser,
// not the expensive GPU itself. This catches accidentally clearing shard IDs.
const fixture = mkdtempSync(join(tmpdir(), 'lpv-model-runner-'));
try {
  mkdirSync(join(fixture, 'assets')); mkdirSync(join(fixture, 'site')); mkdirSync(join(fixture, 'dist'));
  writeFileSync(join(fixture, '.gitignore'), 'dist/\nqa/\n');
  writeFileSync(join(fixture, 'assets/manifest.json'), JSON.stringify(manifest));
  writeFileSync(join(fixture, 'dist/index.html'), 'fixture-build');
  writeFileSync(join(fixture, 'site/redesign-browser-test.mjs'), `
    import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
    import assert from 'node:assert/strict';
    assert.equal(process.env.QA_REVIEW_SCOPE,'models');
    assert.equal(process.env.QA_ALLOW_WEBGL_FALLBACK,'0');
    if(process.env.FIXTURE_FAIL==='1')process.exit(29);
    const ids=process.env.QA_MODEL_IDS.split(',');assert(ids.length>0&&ids.length<190);
    const manifest=JSON.parse(readFileSync('assets/manifest.json'));
    const report={status:'pass',browser_status:'pass',profile:'strict-gpu',review_scope:'models',commit:process.env.GITHUB_SHA,gpu:{status:'pass'},page_errors:[],resource_errors:[],selected_model_ids:ids,models:ids.map(id=>({id,status:'gpu-pass',glb_sha256:manifest.assets.find(a=>a.id===id).sha256.glb}))};
    mkdirSync(process.env.QA_OUTPUT_DIR,{recursive:true});writeFileSync(process.env.QA_OUTPUT_DIR+'/report.json',JSON.stringify(report));
  `);
  writeFileSync(join(fixture, 'site/audit-release.mjs'), `
    import assert from 'node:assert/strict';
    import {readdirSync,writeFileSync} from 'node:fs';
    assert.equal(process.env.REQUIRE_COMPLETE_GALLERY, '1');
    assert.deepEqual(readdirSync('dist'), ['index.html']);
    if (process.env.AUDIT_FIXTURE_FAIL === '1') process.exit(37);
    if (process.env.AUDIT_FIXTURE_TAMPER === '1') writeFileSync('dist/index.html', 'changed-build');
  `);
  const git = (...args) => execFileSync('git', args, { cwd: fixture, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  git('init', '-q'); git('add', '.'); git('-c', 'user.name=CI fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture');
  const env = { ...process.env, GITHUB_SHA: git('rev-parse', 'HEAD'), GITHUB_RUN_ID: '123', GITHUB_RUN_ATTEMPT: '1', CI_RUNTIME: 'true', CI_REVIEW_TASK: plan[2].task, QA_MODEL_IDS: '' };
  const run = (script, args = [], extra = {}) => spawnSync(process.execPath, [resolve('site/' + script), ...args], { cwd: fixture, encoding: 'utf8', env: { ...env, ...extra } });
  let result = run('ci-model-shards.mjs', ['seal-build']); assert.equal(result.status, 0, result.stderr);
  const originalSeal = readFileSync(join(fixture, 'dist', BUILD_RECEIPT));
  result = run('ci-model-shards.mjs', ['audit-build']); assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(readFileSync(join(fixture, 'dist', BUILD_RECEIPT)), originalSeal);
  result = run('ci-model-shards.mjs', ['audit-build'], { AUDIT_FIXTURE_FAIL: '1' }); assert.notEqual(result.status, 0);
  assert.deepEqual(readFileSync(join(fixture, 'dist', BUILD_RECEIPT)), originalSeal);
  result = run('ci-model-shards.mjs', ['audit-build'], { AUDIT_FIXTURE_TAMPER: '1' }); assert.notEqual(result.status, 0);
  assert.deepEqual(readFileSync(join(fixture, 'dist', BUILD_RECEIPT)), originalSeal); writeFileSync(join(fixture, 'dist/index.html'), 'fixture-build');
  result = run('ci-review.mjs'); assert.equal(result.status, 0, result.stderr);
  const receiptPath = join(fixture, 'qa/ci-model-shards', plan[2].task + '.json');
  assert.deepEqual(JSON.parse(readFileSync(receiptPath)).models.map(row => row.id), plan[2].ids);
  result = run('ci-review.mjs', [], { FIXTURE_FAIL: '1' }); assert.equal(result.status, 29);
  assert.throws(() => readFileSync(receiptPath), 'Failed rerun cannot leave successful proof');
  result = run('ci-review.mjs', [], { CI_REVIEW_TASK: 'models-99-of-5' }); assert.notEqual(result.status, 0);
  result = run('ci-review.mjs', [], { CI_RUNTIME: 'false', QA_MODEL_IDS: 'model-004', CI_REVIEW_TASK: 'models-1-of-1' }); assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(JSON.parse(readFileSync(join(fixture, 'qa/ci-model-shards/models-1-of-1.json'))).models.map(row => row.id), ['model-004']);
} finally { rmSync(fixture, { recursive: true, force: true }); }
const workflow = readFileSync('.github/workflows/full-release-review.yml', 'utf8');
// Source-only contracts run once, before any shared build or browser consumer.
// Keep the existing DAG, checkout/runtime and per-run evidence boundaries.
const workflowJob = name => {
  const body = workflow.split(`\n  ${name}:\n`)[1];
  assert(body, `Missing workflow job ${name}`);
  const end = body.search(/\n  [a-zA-Z][\w-]*:/);
  return end < 0 ? body : body.slice(0, end);
};
const sourceJob = workflowJob('prepare-source'), prepareJob = workflowJob('prepare');
const browserJob = workflowJob('build'), auditJob = workflowJob('audit-prepared-build');
const sharedContracts = [
  'ci-browser-task-proof', 'ci-additions-browser-contract', 'ci-install-chromium',
  'catalog-data', 'ci-card-preview-proof', 'ci-model-proof', 'ci-model-cache',
  'ci-incremental-models', 'ci-scope', 'ci-model-shards', 'ci-timed', 'ci-scene-input',
].map(name => `site/${name}-test.mjs`);
const sourceContractStep = sourceJob.match(/      - name: Validate source contracts once before all proof consumers\n        run: ([^\n]+)\n/);
assert(sourceContractStep, 'Source contracts must be an unconditional, blocking step');
const contractCommand = sourceContractStep[1], contractPaths = contractCommand.split(' && ').map(command => {
  assert.match(command, /^node site\/[\w-]+-test\.mjs$/);
  return command.slice('node '.length);
});
assert.equal(new Set(contractPaths).size, contractPaths.length, 'No duplicate source contract commands');
for (const path of sharedContracts) {
  assert(contractPaths.includes(path), `Missing once-only source contract ${path}`);
  assert.equal(workflow.split(`node ${path}`).length - 1, 1, `Repeated source contract ${path}`);
}
assert(sourceJob.indexOf(sourceContractStep[0]) < sourceJob.indexOf('run: npm run build'));
assert.match(sourceJob, /\n    needs: scope\n/);
assert.match(prepareJob, /\n    needs: \[scope, prepare-source\]\n/);
assert.match(browserJob, /\n    needs: \[scope, prepare\]\n/);
assert.match(auditJob, /\n    needs: prepare\n/);
for (const job of [sourceJob, prepareJob, browserJob, auditJob]) {
  assert.match(job, /runs-on: ubuntu-latest/);
  assert.match(job, /uses: actions\/checkout@v4/);
  assert.match(job, /node-version: '22'/);
  assert.doesNotMatch(job, /\n\s+(?:ref|repository):/, 'No different checkout may inherit the source contracts');
  assert.doesNotMatch(job, /continue-on-error:/, 'Failures must remain blocking');
  assert.doesNotMatch(job.split('\n    steps:')[0], /always\(\)|failure\(\)|cancelled\(\)/, 'Failed dependencies cannot be bypassed');
}
assert.doesNotMatch(sourceJob, /always\(\)|failure\(\)|cancelled\(\)/);
assert.match(browserJob, /run: node site\/ci-model-shards\.mjs verify-build/);
assert.match(browserJob, /run: node site\/ci-install-chromium\.mjs/);
assert.match(browserJob, /run: node site\/ci-review\.mjs/);
assert.match(browserJob, /name: exact-model-plan/);
assert.match(browserJob, /name: card-preview-proof/);
assert.match(browserJob, /name: model-shard-\$\{\{ matrix\.task \}\}/);
// Execute the actual && command chain with a tiny Node-command stand-in.
// Every failure position must stop subsequent contracts and artifact production.
// This tests shell failure propagation; the DAG assertions above test wiring.
const contractFixture = mkdtempSync(join(tmpdir(), 'lpv-contract-once-'));
try {
  const bin = join(contractFixture, 'bin'); mkdirSync(bin);
  writeFileSync(join(bin, 'node'), '#!/bin/sh\nprintf "%s\\n" "$1" >> "$CONTRACT_TRACE"\nif [ "$1" = "$FAIL_CONTRACT" ]; then exit 23; fi\n', { mode: 0o755 });
  const trace = join(contractFixture, 'trace'), artifact = join(contractFixture, 'built');
  for (const failed of ['', ...contractPaths]) {
    writeFileSync(trace, ''); rmSync(artifact, { force: true });
    const result = spawnSync('bash', ['--noprofile', '--norc', '-e', '-o', 'pipefail', '-c', `${contractCommand} && printf built > "$CONTRACT_ARTIFACT"`], {
      cwd: contractFixture, encoding: 'utf8',
      env: { ...process.env, PATH: `${bin}:${process.env.PATH}`, FAIL_CONTRACT: failed, CONTRACT_TRACE: trace, CONTRACT_ARTIFACT: artifact },
    });
    assert.equal(result.status, failed ? 23 : 0, result.stderr);
    assert.deepEqual(readFileSync(trace, 'utf8').trim().split('\n'), failed ? contractPaths.slice(0, contractPaths.indexOf(failed) + 1) : contractPaths);
    assert.equal(existsSync(artifact), !failed, 'Failed source contracts cannot produce the downstream build');
  }
} finally { rmSync(contractFixture, { recursive: true, force: true }); }
console.log(`Full review contracts: 12 shared suites run once; all ${contractPaths.length} failure positions stop the command chain, with mandatory same-checkout/runtime DAG and browser/artifact checks retained.`);
assert.match(workflow, /max-parallel: 6/);
assert.match(workflow, /ci-model-shards\.mjs seal-build/);
assert.match(workflow, /ci-model-shards\.mjs verify-build/);
assert.match(workflow, /needs: \[scope, prepare, build, audit-prepared-build\]/);
assert.match(workflow, /if: always\(\) && needs\.scope\.result == 'success' && needs\.scope\.outputs\.models == 'true'/);
assert.match(workflow, /test "\$PREPARE_RESULT" = success && test "\$BUILD_RESULT" = success && test "\$AUDIT_RESULT" = success/);
assert.match(workflow, /ci-incremental-models\.mjs aggregate/);
const incremental=readFileSync('site/ci-incremental-models.mjs','utf8');
assert.match(incremental,/assertModelCoverage\(manifest,shards,receipts,identity,build\)/);
assert.match(incremental,/aggregateModelProof\(/);
assert.match(incremental,/await fetchVerifiedBaseProof\(\{inputs\}\)/);
assert.match(workflow,/PREVIEW_ASSET_IDS: \$\{\{ needs\.prepare\.outputs\.fresh_ids \}\}/);
assert.match(workflow,/name: card-preview-proof/);
assert.match(incremental,/freshCardRecords:cardRecords/);
assert.match(incremental,/Card proof build differs/);
assert.match(incremental,/Live render policy differs from the exact committed source/);
assert.match(workflow, /merge-multiple: false/);
assert.match(workflow, /ci-model-shards\.mjs audit-build/);
console.log('Sealed deployment audit: original strict inventory, exact seal restoration, original failure, unknown files, same-size payload mutation, forged/link seals and real child-process refusal passed.');
console.log('Model shards: deterministic 190/5 exact coverage, selective paths, wrong hashes/policy/run, incomplete GPU results and tampered build all fail closed.');

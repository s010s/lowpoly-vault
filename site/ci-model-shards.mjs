/** Bounded deterministic GPU partitions. Evidence is coverage, never publication approval. */
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync, readdirSync, lstatSync } from 'node:fs';
import { join, relative } from 'node:path';
import { pathToFileURL } from 'node:url';
import { sha256, git, controlDigest, runtimeConfig } from './ci-provenance.mjs';

export const MODEL_SHARD_LIMIT = 5;
export const BUILD_RECEIPT = 'ci-review-build.json';
export function modelPlan(manifest, { runtime = false, ids = '' } = {}) {
  const published = manifest?.assets?.map(asset => asset.id);
  assert(Array.isArray(published) && published.length > 0, 'A nonempty publication is required');
  assert(published.every(id => typeof id === 'string' && /^[a-z0-9-]+$/.test(id)), 'Invalid published ID');
  assert.equal(new Set(published).size, published.length, 'Duplicate published ID');
  const selected = runtime ? [...published] : ids.split(',').filter(Boolean);
  assert(selected.length > 0, 'Selected model coverage cannot be empty');
  assert.equal(new Set(selected).size, selected.length, 'Duplicate selected ID');
  assert(selected.every(id => published.includes(id)), 'Unpublished selected model');
  selected.sort();
  const count = Math.min(MODEL_SHARD_LIMIT, selected.length);
  return Array.from({ length: count }, (_, index) => ({
    task: `models-${index + 1}-of-${count}`,
    ids: selected.filter((_, offset) => offset % count === index),
  }));
}
export function expandModelTasks(scope, manifest) {
  if (!scope.tasks.includes('models')) return scope.tasks;
  const plan = modelPlan(manifest, { runtime: scope.runtime, ids: scope.ids });
  return scope.tasks.flatMap(task => task === 'models' ? plan.map(shard => shard.task) : [task]);
}
export function currentIdentity() {
  const source_commit = git('rev-parse', 'HEAD');
  assert.equal(source_commit, process.env.GITHUB_SHA, 'Runner checkout differs from workflow source');
  assert.equal(git('status', '--porcelain', '--untracked-files=no'), '', 'Shard proof requires unchanged tracked source');
  return {
    source_commit, source_tree: git('rev-parse', 'HEAD^{tree}'), control_sha256: controlDigest('HEAD'),
    manifest_sha256: sha256(readFileSync('assets/manifest.json')), runtime_config: runtimeConfig(),
    run_id: process.env.GITHUB_RUN_ID, run_attempt: process.env.GITHUB_RUN_ATTEMPT,
  };
}
export function payloadDigest(directory) {
  const rows = [];
  const visit = path => {
    for (const entry of readdirSync(path).sort()) {
      const target = join(path, entry), name = relative(directory, target).split('\\').join('/');
      const info = lstatSync(target);
      assert(!info.isSymbolicLink(), 'Shared review build may not contain links');
      if (info.isDirectory()) visit(target);
      else {
        assert(info.isFile(), 'Shared review build contains unsupported member');
        if (name !== BUILD_RECEIPT) rows.push([name, sha256(readFileSync(target))]);
      }
    }
  };
  visit(directory);
  assert(rows.length > 0, 'Shared review build is empty');
  return sha256(JSON.stringify(rows));
}
export function verifyBuild(directory, identity = currentIdentity()) {
  const receipt = JSON.parse(readFileSync(join(directory, BUILD_RECEIPT)));
  assert.equal(receipt.version, 1);
  assert.deepEqual(receipt.identity, identity, 'Shared build source, policy, manifest, runtime or run differs');
  assert.equal(receipt.payload_sha256, payloadDigest(directory), 'Shared build bytes differ');
  return receipt;
}
export function modelReceipt(manifest, plan, shard, browser, build) {
  assert(plan.some(entry => entry.task === shard.task), 'Unexpected model shard');
  assert.equal(browser.status, 'pass', 'Model browser suite did not pass');
  assert.equal(browser.browser_status, 'pass');
  assert.equal(browser.profile, 'strict-gpu');
  assert.equal(browser.review_scope, 'models');
  assert.equal(browser.commit, build.identity.source_commit, 'Browser tested another source');
  assert.equal(browser.gpu.status, 'pass');
  assert.deepEqual(browser.page_errors, []);
  assert.deepEqual(browser.resource_errors, []);
  assert.deepEqual([...browser.selected_model_ids].sort(), shard.ids, 'Browser selected wrong IDs');
  const models = browser.models.map(row => ({ id: row.id, glb_sha256: row.glb_sha256, status: row.status }));
  assert.deepEqual(models.map(row => row.id).sort(), shard.ids, 'Browser did not execute exact shard');
  for (const row of models) {
    assert.equal(row.status, 'gpu-pass', 'Fallback is not strict GPU coverage');
    const expected = manifest.assets.find(asset => asset.id === row.id)?.sha256?.glb;
    assert.match(expected || '', /^[a-f0-9]{64}$/);
    assert.equal(row.glb_sha256, expected, 'Model payload hash differs');
  }
  return { version: 1, kind: 'model-shard', task: shard.task, plan_sha256: sha256(JSON.stringify(plan)),
    identity: build.identity, payload_sha256: build.payload_sha256, models };
}
export function assertModelCoverage(manifest, plan, receipts, identity, build) {
  assert.equal(build?.version, 1, 'Missing independently prepared build seal');
  assert.deepEqual(build.identity, identity, 'Prepared build identity differs');
  assert.match(build.payload_sha256 || '', /^[a-f0-9]{64}$/);
  assert.equal(receipts.length, plan.length, 'Missing or extra model shard');
  assert.equal(new Set(receipts.map(row => row.task)).size, plan.length, 'Duplicate model shard');
  const payloads = new Set();
  for (const shard of plan) {
    const receipt = receipts.find(row => row.task === shard.task);
    assert(receipt, 'Missing expected model shard');
    assert.equal(receipt.version, 1);
    assert.equal(receipt.kind, 'model-shard');
    assert.deepEqual(receipt.identity, identity, 'Shard source, policy, manifest, runtime or run differs');
    assert.equal(receipt.plan_sha256, sha256(JSON.stringify(plan)), 'Model plan differs');
    assert.match(receipt.payload_sha256 || '', /^[a-f0-9]{64}$/);
    payloads.add(receipt.payload_sha256);
    assert.equal(receipt.payload_sha256, build.payload_sha256, 'Shard did not test the prepared build');
    assert.deepEqual(receipt.models.map(row => row.id).sort(), shard.ids, 'Missing, duplicate or unexpected model coverage');
    for (const row of receipt.models) {
      assert.equal(row.status, 'gpu-pass');
      const expected = manifest.assets.find(asset => asset.id === row.id)?.sha256?.glb;
      assert.match(expected || '', /^[a-f0-9]{64}$/);
      assert.equal(row.glb_sha256, expected, 'Model payload hash differs');
    }
  }
  assert.equal(payloads.size, 1, 'Shards tested different build artifacts');
  return { version: 1, kind: 'model-coverage', identity, payload_sha256: [...payloads][0],
    shards: plan.length, ids: plan.flatMap(shard => shard.ids).sort(), status: 'pass',
    scope: 'Existing strict GPU browser contracts only; not visual, factual or formal asset approval' };
}
export function readModelReceipts(directory, plan) {
  const expected = plan.map(shard => `model-shard-${shard.task}`).sort();
  assert.deepEqual(readdirSync(directory).sort(), expected, 'Missing or unexpected model shard artifacts');
  return plan.map(shard => {
    const folder = join(directory, `model-shard-${shard.task}`), filename = `${shard.task}.json`;
    assert(lstatSync(folder).isDirectory() && !lstatSync(folder).isSymbolicLink(), 'Invalid shard artifact directory');
    assert.deepEqual(readdirSync(folder), [filename], 'Missing or unexpected model shard artifact members');
    const file = join(folder, filename);
    assert(lstatSync(file).isFile() && !lstatSync(file).isSymbolicLink(), 'Invalid shard report file');
    return JSON.parse(readFileSync(file));
  });
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const command = process.argv[2], directory = process.env.GALLERY_DIR || 'dist';
  if (command === 'seal-build') {
    const receipt = { version: 1, identity: currentIdentity(), payload_sha256: payloadDigest(directory) };
    writeFileSync(join(directory, BUILD_RECEIPT), JSON.stringify(receipt, null, 2) + '\n');
    console.log(`Sealed shared review build ${receipt.payload_sha256}`);
  } else if (command === 'verify-build') {
    console.log(`Verified shared review build ${verifyBuild(directory).payload_sha256}`);
  } else if (command === 'aggregate') {
    const manifest = JSON.parse(readFileSync('assets/manifest.json'));
    const plan = modelPlan(manifest, { runtime: process.env.CI_RUNTIME === 'true', ids: process.env.QA_MODEL_IDS || '' });
    const inputs = process.argv[3] || 'qa/ci-model-shards';
    const receipts = readModelReceipts(inputs, plan);
    const build = JSON.parse(readFileSync('qa/ci-model-build/' + BUILD_RECEIPT));
    const result = assertModelCoverage(manifest, plan, receipts, currentIdentity(), build);
    mkdirSync('qa/ci-model-coverage', { recursive: true });
    writeFileSync('qa/ci-model-coverage/coverage.json', JSON.stringify(result, null, 2) + '\n');
    console.log(`Exact strict GPU coverage: ${result.ids.length} models across ${result.shards} shards.`);
  } else throw Error('Known model shard command required');
}

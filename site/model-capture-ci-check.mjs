/** Isolated real-runtime experiment. No publication or formal QA authority. */
import assert from 'node:assert/strict';
import {execFileSync, spawn} from 'node:child_process';
import {readFile, writeFile, mkdir, mkdtemp, readdir, lstat, cp, rm, realpath} from 'node:fs/promises';
import {resolve, dirname, join} from 'node:path';
import {tmpdir} from 'node:os';
import {createModelCaptureDraft, assertModelCaptureDraft, capturePackagePath} from './model-capture-package.mjs';
import {packageCaptureInputs, selectPackageModels} from './model-capture-runner.mjs';
import {localReader} from './model-registry-cli.mjs';
import {digest, hashBytes} from './model-registry.mjs';
import {CAPTURE_POLICY} from './gallery-poster-inputs.mjs';

const root = process.cwd(), selectedIDs = ['cave-shield', 'didymoceras', 'metaspriggina', 'psammichnites-ribbon-trace', 'spirematospermum', 'strophomena', 'waptia'].sort();
const git = (...args) => execFileSync('git', args, {cwd: root, encoding: 'utf8'}).trim();
assert.equal(process.versions.node.split('.')[0], CAPTURE_POLICY.node_major);
assert.equal(git('status', '--porcelain', '--untracked-files=no'), '');
const sourceCommit = git('rev-parse', 'HEAD'); assert.equal(sourceCommit, process.env.GITHUB_SHA);
const read = localReader(root), manifest = JSON.parse(read('assets/manifest.json')), assets = selectPackageModels(manifest, selectedIDs), shared = await packageCaptureInputs(root);
const output = resolve(root, 'qa/model-registry-capture-only/results');
await mkdir(dirname(output), {recursive: true}); await mkdir(output);
const input = await mkdtemp(join(process.env.RUNNER_TEMP || tmpdir(), 'model-capture-input-'));
async function sourceInventory() {
  const files = [];
  async function visit(path) {
    const full = resolve(root, path), info = await lstat(full); assert(!info.isSymbolicLink());
    if (info.isDirectory()) { for (const name of (await readdir(full)).sort()) await visit(`${path}/${name}`); }
    else { assert(info.isFile()); const bytes = read(path); files.push({path, bytes: bytes.length, sha256: hashBytes(bytes)}); }
  }
  for (const path of ['assets/manifest.json', 'site/catalog-data.json', 'assets/turntables/index.json', 'site/gallery/wheel-framing.json', 'site/public/gallery', ...assets.map(asset => asset.glb)]) await visit(path);
  return files;
}
const before = await sourceInventory();
try {
  await mkdir(join(input, 'assets'), {recursive: true}); await writeFile(join(input, 'assets/manifest.json'), JSON.stringify({assets}));
  for (const asset of assets) {
    assert.equal(hashBytes(read(asset.glb)), asset.sha256.glb);
    await mkdir(dirname(join(input, asset.glb)), {recursive: true}); await cp(resolve(root, asset.glb), join(input, asset.glb));
  }
  // Duplicate the first ID concurrently, then append six independent IDs.
  const jobs = [selectedIDs[0], ...selectedIDs], results = []; let cursor = 0;
  async function worker() {
    while (cursor < jobs.length) {
      const index = cursor++, id = jobs[index];
      const result = await new Promise((done, reject) => {
        const child = spawn(process.execPath, ['site/capture-gallery-posters.mjs', '--package-output', output, '--model-ids', id], {cwd: root, env: {...process.env, GALLERY_OUTPUT_DIR: input, GALLERY_URL: '', CHROMIUM_PATH: ''}, stdio: ['ignore', 'pipe', 'pipe']});
        let stdout = '', stderr = ''; child.stdout.on('data', data => { stdout += data; }); child.stderr.on('data', data => { stderr += data; });
        child.on('error', reject); child.on('close', status => done({status, stdout, stderr}));
      });
      await writeFile(join(output, `process-${index}-${id}.log`), result.stdout + result.stderr);
      assert.equal(result.status, 0, result.stderr);
      const report = JSON.parse(result.stdout); assert.equal(report.publication_authority, false); assert.deepEqual(report.models, [id]); assert.equal(report.packages.length, 1);
      results[index] = report.packages[0];
    }
  }
  const workers = await Promise.allSettled([worker(), worker()]);
  for (const worker of workers) if (worker.status === 'rejected') throw worker.reason;
  assert.deepEqual(await sourceInventory(), before, 'Capture experiment changed shared gallery, indices or source model bytes');
  assert.equal(git('rev-parse', 'HEAD'), sourceCommit); assert.equal(git('status', '--porcelain', '--untracked-files=no'), '');
  assert.deepEqual((await readdir(join(output, 'registry/captures'))).sort(), selectedIDs);
  assert.equal(results[0].path, results[1].path, 'Concurrent duplicate capture was not byte reproducible');
  assert.equal(results.filter(row => row.id === selectedIDs[0] && row.created).length, 1, 'Identical concurrent capture must install once');
  const verified = [];
  for (const asset of assets) {
    const row = results.find(result => result.id === asset.id), path = join(output, row.path);
    assert.equal((await readdir(join(output, 'registry/captures', asset.id))).length, 1, 'Unexpected alternate capture revision');
    assert.deepEqual((await readdir(path)).sort(), ['capture.json', 'detail.png', 'wheel.png']);
    assert.equal(await realpath(path), path);
    const record = JSON.parse(await readFile(join(path, 'capture.json'))), detail = await readFile(join(path, 'detail.png')), wheel = await readFile(join(path, 'wheel.png'));
    const draft = {record, images: new Map([[record.poster.detail, detail], [record.poster.wheel, wheel]])}; assertModelCaptureDraft(draft);
    assert.equal(capturePackagePath(draft), row.path);
    assert.deepEqual(createModelCaptureDraft({asset, shared, browserVersion: record.browser_version, pixels: {detail, wheel}, wheelSpec: record.poster.wheelSpec, read}).record, record);
    verified.push({id: asset.id, package_path: row.path, record_sha256: digest(record), source_glb_sha256: asset.sha256.glb, recipe_sha256: record.shared_sha256, input_sha256: record.input_sha256, browser: record.browser_version, files: record.files});
  }
  const report = {version: 1, kind: 'real-runtime-capture-experiment', publication_authority: false, formal_approval: false, source_commit: sourceCommit,
    run_id: Number(process.env.GITHUB_RUN_ID), run_attempt: Number(process.env.GITHUB_RUN_ATTEMPT), node: process.versions.node, browser: shared.browser,
    selected_ids: selectedIDs, producer_processes: jobs.length, max_concurrent_processes: 2, shared_gallery_and_source_unchanged: true,
    concurrent_duplicate_byte_identical: true, source_inventory_sha256: digest(before), recipe_sha256: shared.sha256, packages: verified};
  await writeFile(join(output, 'experiment-report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
} finally { await rm(input, {recursive: true, force: true}); }

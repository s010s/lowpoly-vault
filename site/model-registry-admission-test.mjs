/** API/byte fixtures verify authority boundaries, not production GPU or source quality. */
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync, existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {fixture, buildFixture, finish, identity} from './ci-model-proof-test.mjs';
import {assertBuiltRenderInputs, computeModelInputs, planModelReuse, hashBytes} from './ci-model-proof.mjs';
import {posterInputKey, posterSharedInputs} from './gallery-poster-inputs.mjs';
import {posterRuntime, posterArtifactName} from './gallery-poster-proof.mjs';
import {proofArtifactName} from './ci-model-cache.mjs';
import {importLegacySnapshot} from './model-registry.mjs';
import {localReader, readLegacySnapshot} from './model-registry-cli.mjs';
import {admitExistingRegistryRelease, collectAdmittedRegistry, writeAdmittedRegistryProjection} from './model-registry-admission.mjs';

const repository = 'owner/repo', clone = value => structuredClone(value);
function png(kind, id) { const bytes = Buffer.alloc(80); Buffer.from('89504e470d0a1a0a', 'hex').copy(bytes); bytes.writeUInt32BE(kind === 'detail' ? 512 : 768, 16); bytes.writeUInt32BE(kind === 'detail' ? 512 : 432, 20); bytes[25] = 6; bytes.write(id, 26); return bytes; }
function archive(proof, filename, files = new Map()) {
  const dir = mkdtempSync(join(tmpdir(), 'admission-zip-test-'));
  try {
    const members = [[filename, 'proof.json']]; writeFileSync(join(dir, 'proof.json'), JSON.stringify(proof));
    for (const [path, bytes] of files) { const name = `file-${members.length}`; members.push([path, name]); writeFileSync(join(dir, name), bytes); }
    writeFileSync(join(dir, 'members.json'), JSON.stringify(members));
    execFileSync('python3', ['-I', '-c', "import json,zipfile,sys,os\nr=sys.argv[1]\nwith zipfile.ZipFile(os.path.join(r,'artifact.zip'),'w',compression=zipfile.ZIP_DEFLATED) as z:\n for name,path in json.load(open(os.path.join(r,'members.json'))): z.write(os.path.join(r,path),name)", dir]);
    return readFileSync(join(dir, 'artifact.zip'));
  } finally { rmSync(dir, {recursive: true, force: true}); }
}
async function setup({gateFails = false} = {}) {
  const f = fixture(2), git = (...args) => execFileSync('git', args, {cwd: f.root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe']}).trim();
  f.put('.gitignore', 'dist/\nnode_modules/\nqa/ci-model-proof/\n.publication-gate-ran\n');
  f.put('vite.config.js', '// protected synthetic build fixture\n');
  f.put('site/capture-gallery-posters.mjs', '// protected synthetic capture fixture\n');
  f.put('site/gallery-poster-inputs.mjs', '// protected synthetic recipe fixture\n');
  f.put('site/initial-release.mjs', `import {writeFileSync} from 'node:fs'; if(process.argv[2]!=='--check')process.exit(7); writeFileSync('.publication-gate-ran','invoked'); process.exit(${gateFails ? 1 : 0});\n`);
  f.put('node_modules/playwright-core/browsers.json', {browsers: [{name: 'chromium', browserVersion: '141.0.7390.37', revision: '1194'}]});
  const shared = await posterSharedInputs(f.root), imageFiles = new Map(); f.resources.files = [];
  for (const asset of f.manifest.assets) {
    const poster = f.resources.posters[asset.id]; poster.input_sha256 = posterInputKey(asset, shared); poster.browser_version = shared.browser;
    for (const kind of ['detail', 'wheel']) {
      const path = poster[kind], bytes = png(kind, asset.id); f.put(`site/public/${path}`, bytes); imageFiles.set(path, bytes); f.resources.files.push({path, sha256: hashBytes(bytes), bytes: bytes.length});
    }
  }
  f.put('site/public/gallery/resources.json', f.resources); await buildFixture(f);
  git('init', '--initial-branch=main'); git('config', 'user.name', 'Fixture'); git('config', 'user.email', 'fixture@example.invalid'); git('add', '.'); git('commit', '-m', 'Synthetic trusted release source');
  const sourceCommit = git('rev-parse', 'HEAD'), built = await assertBuiltRenderInputs({root: f.root}), inputs = computeModelInputs({root: f.root, built});
  const modelProof = finish(inputs, planModelReuse({inputs}), {...identity(sourceCommit, 101), source_tree: git('rev-parse', 'HEAD^{tree}')});
  const posterProof = {version: 1, kind: 'gallery-poster-capture-proof', status: 'pass', repository, source_commit: sourceCommit, run_id: 101, run_attempt: 1, policy_sha256: inputs.policy_sha256, runtime: posterRuntime(shared), shared_sha256: shared.sha256,
    catalog_ids: f.manifest.assets.map(asset => asset.id).sort(), posters: f.manifest.assets.map(asset => ({id: asset.id, input_sha256: posterInputKey(asset, shared), source_glb_sha256: asset.sha256.glb, poster: f.resources.posters[asset.id], files: f.resources.files.filter(file => [f.resources.posters[asset.id].detail, f.resources.posters[asset.id].wheel].includes(file.path)), evidence: 'captured'}))};
  const {snapshot, sourcePins} = readLegacySnapshot(localReader(f.root)), registry = importLegacySnapshot(snapshot, {sourceCommit, sourcePins});
  const run = {id: 101, run_attempt: 1, event: 'push', head_branch: 'main', head_sha: sourceCommit, status: 'completed', conclusion: 'success', path: '.github/workflows/full-release-review.yml', workflow_id: 99, check_suite_id: 202, repository: {id: 12, full_name: repository}, head_repository: {id: 12, full_name: repository}};
  function transport({alterRun, alterSuite, alterModel, alterPoster, alterModelArtifact, alterPosterArtifact, missingModel = false, missingPoster = false, missingExactRun = false, apiFailure = false, tamperPosterDownload = false} = {}) {
    const r = clone(run), suite = {id: 202, status: 'completed', conclusion: 'success', head_sha: sourceCommit, app: {id: 15368, slug: 'github-actions', owner: {login: 'github'}}}; alterRun?.(r); alterSuite?.(suite);
    const model = clone(modelProof), poster = clone(posterProof); alterModel?.(model); alterPoster?.(poster);
    const modelBytes = archive(model, 'model-proof.json'), selectedImages = new Map([...imageFiles].filter(([path]) => poster.posters.some(row => row.files.some(file => file.path === path)))), posterBytes = archive(poster, 'gallery-poster-proof.json', selectedImages);
    const metadata = (id, name, bytes) => ({id, name, expired: false, digest: `sha256:${hashBytes(bytes)}`, workflow_run: {id: 101, head_sha: sourceCommit, repository_id: 12, head_repository_id: 12}});
    const m = metadata(303, proofArtifactName(1), modelBytes), p = metadata(404, posterArtifactName(1), posterBytes); alterModelArtifact?.(m); alterPosterArtifact?.(p);
    return async (url, options = {}) => {
      url = String(url);
      if (url.startsWith('https://storage.example.invalid/')) { assert.equal(options.headers, undefined, 'Credentials must not be sent to storage'); return new Response(url.endsWith('model.zip') ? modelBytes : tamperPosterDownload ? Buffer.from('forged') : posterBytes); }
      const origin = `https://api.github.com/repos/${repository}`; assert(url === origin || url.startsWith(`${origin}/`)); assert.equal(options.headers.Authorization, 'Bearer fixture-token');
      if (apiFailure) return new Response('unavailable', {status: 503});
      const path = url === origin ? '' : url.slice(origin.length + 1); let body;
      if (path === '') body = {id: 12, full_name: repository, default_branch: 'main'};
      else if (path === 'git/ref/heads/main') body = {ref: 'refs/heads/main', object: {sha: sourceCommit}};
      else if (path === 'actions/workflows/full-release-review.yml') body = {id: 99, path: '.github/workflows/full-release-review.yml'};
      else if (path.startsWith('actions/workflows/99/runs?')) body = {workflow_runs: missingExactRun ? [] : [{id: 101, head_sha: sourceCommit}]};
      else if (path === 'actions/runs/101' || path === 'actions/runs/101/attempts/1') body = r;
      else if (path === 'check-suites/202') body = suite;
      else if (path === 'actions/runs/101/artifacts?per_page=100') body = {artifacts: [...(missingModel ? [] : [m]), ...(missingPoster ? [] : [p])]};
      else if (path === 'actions/artifacts/303') body = m;
      else if (path === 'actions/artifacts/404') body = p;
      else if (path === 'actions/artifacts/303/zip' || path === 'actions/artifacts/404/zip') return new Response(null, {status: 302, headers: {location: `https://storage.example.invalid/${path.includes('/303/') ? 'model' : 'poster'}.zip`}});
      else if (path === `contents/assets/manifest.json?ref=${sourceCommit}`) body = {type: 'file', encoding: 'base64', content: Buffer.from(JSON.stringify(f.manifest)).toString('base64')};
      else throw new Error(`Unexpected fixture endpoint ${path}`);
      return new Response(JSON.stringify(body), {headers: {'content-type': 'application/json'}});
    };
  }
  const admit = (options = {}) => admitExistingRegistryRelease({root: f.root, registry, repository, sourceCommit, token: 'fixture-token', fetchImpl: transport(options)});
  return {...f, git, sourceCommit, inputs, registry, admit, transport, modelProof, posterProof};
}

const f = await setup();
try {
  await test('exact successful model+poster artifacts and source publication gate create opaque admission', async () => {
    const admission = await f.admit(); assert.equal(admission.model_count, 2); assert(existsSync(join(f.root, '.publication-gate-ran')));
    assert.deepEqual((await collectAdmittedRegistry(admission)).manifest, f.manifest);
    await assert.rejects(() => collectAdmittedRegistry(JSON.parse(JSON.stringify(admission))), /in-process admission/);
    await assert.rejects(() => collectAdmittedRegistry({accepted: true, status: 'pass', ...admission}), /in-process admission/);
    const out = join(f.root, 'projection'); await writeAdmittedRegistryProjection(admission, out); assert.equal(JSON.parse(readFileSync(join(out, 'assets/catalog.json'))).total, 2);
    rmSync(out, {recursive: true, force: true});
  });
  const refusals = [
    ['no model proof', {missingModel: true}], ['no poster proof', {missingPoster: true}], ['no exact-source run', {missingExactRun: true}], ['API failure', {apiFailure: true}],
    ['failed run', {alterRun: run => { run.conclusion = 'failure'; }}], ['fork run', {alterRun: run => { run.head_repository.id = 99; }}],
    ['wrong check-suite app', {alterSuite: suite => { suite.app.id = 7; }}],
    ['expired model artifact', {alterModelArtifact: artifact => { artifact.expired = true; }}], ['expired poster artifact', {alterPosterArtifact: artifact => { artifact.expired = true; }}],
    ['incomplete model coverage', {alterModel: proof => { proof.models.pop(); }}], ['different tested build payload', {alterModel: proof => { proof.payload_sha256 = 'f'.repeat(64); }}],
    ['incomplete poster coverage', {alterPoster: proof => { proof.posters.pop(); }}], ['different poster GLB', {alterPoster: proof => { proof.posters[0].source_glb_sha256 = 'f'.repeat(64); }}],
    ['different poster recipe', {alterPoster: proof => { proof.shared_sha256 = 'f'.repeat(64); }}], ['modified poster download', {tamperPosterDownload: true}],
    ['different reviewed poster input binding', {alterPoster: proof => { proof.posters[0].evidence = 'reviewed'; proof.posters[0].input_sha256 = 'f'.repeat(64); }}],
    ['different poster source', {alterPoster: proof => { proof.source_commit = 'f'.repeat(40); }}]
  ];
  for (const [label, options] of refusals) await test(`admission rejects ${label} without self-reported fallback`, async () => { await assert.rejects(() => f.admit(options)); });
  await test('source-only proof cannot substitute for verified built-input evidence', async () => {
    const sourceInputs = computeModelInputs({root: f.root});
    const sourceProof = finish(sourceInputs, planModelReuse({inputs: sourceInputs}), {...identity(f.sourceCommit, 101), source_tree: f.git('rev-parse', 'HEAD^{tree}')});
    await assert.rejects(() => f.admit({alterModel: proof => Object.assign(proof, sourceProof)}), /matching built-input proof/);
  });
  await test('proposed changed registry scope remains pending rather than inheriting old acceptance', async () => {
    const changed = clone(f.registry); changed.baseline.headers.manifest.quality_status = 'approved';
    await assert.rejects(() => admitExistingRegistryRelease({root: f.root, registry: changed, repository, sourceCommit: f.sourceCommit, token: 'fixture-token', fetchImpl: f.transport()}), /Baseline historical records|not the exact existing release scope/);
  });
  for (const [label, alter] of [
    ['forged historical commit', registry => { registry.baseline.source_commit = 'f'.repeat(40); }],
    ['forged historical source pin', registry => { registry.baseline.source_pins.manifest.sha256 = 'f'.repeat(64); }],
    ['forged historical semantic snapshot', registry => { registry.baseline.snapshot_sha256 = 'f'.repeat(64); }]
  ]) await test(`admission rejects ${label} even with unchanged projected content`, async () => {
    const registry = clone(f.registry); alter(registry); let reads = 0; const transport = f.transport();
    await assert.rejects(() => admitExistingRegistryRelease({root: f.root, registry, repository, sourceCommit: f.sourceCommit, token: 'fixture-token', fetchImpl: async (...args) => { reads++; return transport(...args); }}));
    assert.equal(reads, 0, 'Bad baseline provenance must fail before proof transport');
  });
  await test('admission cannot be reused after source or delivered build inputs change', async () => {
    const admission = await f.admit(), sourcePath = join(f.root, f.manifest.assets[0].glb), bytes = readFileSync(sourcePath);
    try { writeFileSync(sourcePath, 'changed source'); await assert.rejects(() => collectAdmittedRegistry(admission), /unchanged tracked source/); } finally { writeFileSync(sourcePath, bytes); }
    const outputPath = join(f.root, 'dist/assets/index-fixture.js'), output = readFileSync(outputPath);
    try { writeFileSync(outputPath, 'different renderer'); await assert.rejects(() => collectAdmittedRegistry(admission), /inputs changed/); } finally { writeFileSync(outputPath, output); }
  });
} finally { f.close(); }
await test('publication gate failure blocks admission even when external proof fixtures claim success', async () => {
  const failed = await setup({gateFails: true}); try { await assert.rejects(() => failed.admit(), /Command failed/); } finally { failed.close(); }
});

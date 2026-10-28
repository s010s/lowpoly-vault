import './old-corrective-ten-selection-test.mjs';
import './old-corrective-ten-detail-scope-test.mjs';
import './old-corrective-ten-visual-acceptance-test.mjs';
import './model-task-static4-acceptance-test.mjs';
/** Publication-boundary regressions use disposable copies, never mutate original assets or QA. */
import './same-id-append-continuation-test.mjs';
import './detail-append-visual-acceptance-test.mjs';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, copyFile, readFile, writeFile, rename, symlink, rm } from 'node:fs/promises';
import { dirname, join, resolve, basename } from 'node:path';
import { tmpdir } from 'node:os';
import { createHash } from 'node:crypto';
import { collectInitialRelease, checkPublishedManifest, INITIAL_ASSET_IDS } from './initial-release.mjs';
import { collectManifest } from './generate-manifest.mjs';

const expectedIDs = ['conifer-tree', 'cycad', 'dinosaur-nest', 'fern-cluster', 'horsetail-cluster', 'lepidodendron', 'natural-arch', 'stratified-cliff', 'three-toed-track', 'uprooted-log'];
const sourceRoot = process.cwd();
const root = await mkdtemp(join(tmpdir(), 'vault-initial-release-'));
const specPath = 'assets/initial-publication.json';
const manifestPath = 'assets/manifest.json';
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const snapshots = new Map();
let checks = 0;
const json = value => JSON.stringify(value, null, 2) + '\n';
async function check(name, action) {
  try { await action(); ++checks; }
  catch (error) { error.message = `${name}: ${error.message}`; throw error; }
}
async function mutateJSON(path, mutate, action) {
  const file = resolve(root, path), original = await readFile(file);
  const value = JSON.parse(original); mutate(value);
  try { await writeFile(file, json(value)); await action(); }
  finally { await writeFile(file, original); }
}
async function rejectSpec(name, mutate, pattern) {
  await check(name, () => mutateJSON(specPath, mutate, () => assert.rejects(() => collectInitialRelease(root), pattern)));
}
async function rejectManifest(name, mutate, pattern) {
  await check(name, () => mutateJSON(manifestPath, mutate, () => assert.rejects(() => checkPublishedManifest(root), pattern)));
}

try {
  assert.deepEqual(INITIAL_ASSET_IDS, expectedIDs, 'The initial collection must remain the original ten IDs');
  const approval = JSON.parse(await readFile(resolve(sourceRoot, specPath), 'utf8'));
  const paths = new Set([specPath]);
  for (const asset of approval.assets) {
    for (const key of ['glb', 'blend', 'preview']) paths.add(asset[key]);
    for (const name of ['metadata.json', 'qa.json']) paths.add(join(dirname(asset.glb), name));
  }
  for (const path of paths) {
    await mkdir(dirname(resolve(root, path)), { recursive: true });
    await copyFile(resolve(sourceRoot, path), resolve(root, path));
    snapshots.set(path, sha(await readFile(resolve(root, path))));
  }

  let manifest;
  await check('accept the pinned initial collection without changing its QA', async () => {
    manifest = await collectInitialRelease(root);
    assert.deepEqual(manifest.assets.map(a => a.id).sort(), expectedIDs);
    assert.equal(manifest.release_status, 'initial');
    assert.equal(manifest.quality_status, 'work_in_progress');
    assert.equal(manifest.review_only, undefined);
    assert.equal(manifest.publication.source_commit, '550ac6b1d4477d1fbd85ea9f8eb69502b20a42a7');
    for (const asset of manifest.assets) {
      assert.equal(asset.quality_status, 'work_in_progress');
      for (const key of ['glb', 'blend', 'preview']) {
        assert.match(asset.sha256[key], /^[a-f0-9]{64}$/);
        assert.equal(asset.sha256[key], sha(await readFile(resolve(root, asset[key]))));
      }
      const qa = JSON.parse(await readFile(resolve(root, dirname(asset.glb), 'qa.json')));
      assert.equal(qa.threejs_runtime.status, 'not_run');
    }
    await writeFile(resolve(root, manifestPath), json(manifest));
    assert.deepEqual(await checkPublishedManifest(root), manifest);
  });
  await check('formal QA gate remains strict', () => assert.rejects(() => collectManifest(root), /threejs_runtime QA is not_run/));

  for (const [field, value] of [['version', 2], ['release_status', 'approved'], ['quality_status', 'approved'], ['authorization', 'unspecified'], ['source_commit', '0'.repeat(40)]]) {
    await rejectSpec(`reject changed publication ${field}`, a => { a[field] = value; });
  }
  await rejectSpec('reject missing authorized ID', a => { a.assets.pop(); }, /Only the original ten/);
  await rejectSpec('reject extra authorized ID', a => { a.assets.push({ ...a.assets[0], id: 'unapproved-eleventh' }); }, /Only the original ten/);
  await rejectSpec('reject duplicate authorized ID', a => { a.assets[1].id = a.assets[0].id; }, /Only the original ten/);

  const first = approval.assets[0];
  const metadataPath = join(dirname(first.glb), 'metadata.json');
  const qaPath = join(dirname(first.glb), 'qa.json');
  await check('reject substituted discovered ID', () => mutateJSON(metadataPath, a => { a.id = 'unapproved-substitute'; }, () => assert.rejects(() => collectInitialRelease(root), /No extra or missing/)));
  await check('reject missing discovered asset', async () => {
    const file = resolve(root, metadataPath), hidden = file + '.hidden';
    await rename(file, hidden);
    try { await assert.rejects(() => collectInitialRelease(root), /No extra or missing/); }
    finally { await rename(hidden, file); }
  });
  await check('reject extra discovered asset', async () => {
    const folder = 'assets/test-only/unapproved-eleventh';
    const extra = JSON.parse(await readFile(resolve(root, metadataPath)));
    extra.id = 'unapproved-eleventh';
    await mkdir(resolve(root, folder), { recursive: true });
    try {
      for (const key of ['glb', 'blend', 'preview']) {
        extra[key] = `${folder}/${basename(first[key])}`;
        await copyFile(resolve(root, first[key]), resolve(root, extra[key]));
      }
      await writeFile(resolve(root, folder, 'metadata.json'), json(extra));
      await copyFile(resolve(root, qaPath), resolve(root, folder, 'qa.json'));
      await assert.rejects(() => collectInitialRelease(root), /No extra or missing/);
    } finally { await rm(resolve(root, 'assets/test-only'), { recursive: true, force: true }); }
  });

  for (const key of ['glb', 'blend', 'preview']) {
    await rejectSpec(`reject changed ${key} publication path`, a => { a.assets[0][key] += '.different'; }, /publication path changed/);
    await rejectSpec(`require ${key} publication hash`, a => { delete a.assets[0].sha256[key]; }, /fixed SHA-256/);
    await rejectSpec(`reject malformed ${key} publication hash`, a => { a.assets[0].sha256[key] = 'not-a-hash'; }, /fixed SHA-256/);
    await rejectSpec(`reject mismatched ${key} publication hash`, a => { a.assets[0].sha256[key] = '0'.repeat(64); }, /bytes changed/);
    await check(`reject changed ${key} bytes even if metadata is rehashed`, async () => {
      const file = resolve(root, first[key]), original = await readFile(file), changed = Buffer.from(original);
      changed[changed.length - 1] ^= 1;
      try {
        await writeFile(file, changed);
        await mutateJSON(metadataPath, a => { a.sha256 = { ...a.sha256, [key]: sha(changed) }; }, () => assert.rejects(() => collectInitialRelease(root), /bytes changed/));
      } finally { await writeFile(file, original); }
    });
    await check(`reject same-byte ${key} symlink substitution`, async () => {
      const file = resolve(root, first[key]), backup = file + '.test-original';
      await rename(file, backup);
      try {
        await symlink(backup, file);
        await assert.rejects(() => collectInitialRelease(root), /symlink substitutions/);
      } finally { await rm(file, { force: true }); await rename(backup, file); }
    });
  }

  for (const stage of ['source', 'glb', 'khronos_validator']) {
    await check(`reject failed ${stage} QA`, () => mutateJSON(qaPath, qa => { qa[stage].status = 'fail'; }, () => assert.rejects(() => collectInitialRelease(root))));
    await check(`reject unresolved ${stage} errors`, () => mutateJSON(qaPath, qa => { qa[stage].errors = ['Test-only unresolved error']; }, () => assert.rejects(() => collectInitialRelease(root))));
  }

  await rejectManifest('reject review-only stored manifest', m => { m.review_only = true; }, /review-only/);
  for (const [name, mutate] of [
    ['changed stored description', m => { m.assets[0].description.en += ' Modified'; }],
    ['changed stored file hash', m => { m.assets[0].sha256.glb = '0'.repeat(64); }],
    ['missing stored model', m => { m.assets.pop(); }],
    ['extra stored model', m => { m.assets.push({ ...m.assets[0], id: 'unapproved-eleventh' }); }],
    ['promoted quality claim', m => { m.quality_status = 'approved'; }],
    ['changed stored publication source', m => { m.publication.source_commit = '0'.repeat(40); }],
  ]) await rejectManifest(`reject ${name}`, mutate, /exactly match/);
  await rejectManifest('removing initial-release status cannot bypass formal QA', m => { delete m.release_status; }, /threejs_runtime QA is not_run/);

  await check('all copied sources, metadata, QA and publication approval remain unchanged', async () => {
    for (const [path, hash] of snapshots) assert.equal(sha(await readFile(resolve(root, path))), hash, path);
    assert.deepEqual(await checkPublishedManifest(root), manifest);
    assert.deepEqual(JSON.parse(await readFile(resolve(root, manifestPath))), manifest);
  });
  console.log(`Initial-release tests passed: ${checks} checks; exact ten original assets; three required hashes; scope/path/byte/symlink mutation refusal; QA preserved; stored-manifest equality; formal gate remains strict.`);
} finally { await rm(root, { recursive: true, force: true }); }

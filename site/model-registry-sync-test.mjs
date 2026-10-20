/** Tiny synthetic data tests the bridge, not scientific/visual approval or rendering. */
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {execFileSync, spawn} from 'node:child_process';
import {mkdtempSync, mkdirSync, readFileSync, readdirSync, rmSync, symlinkSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {LEGACY_OUTPUTS, composeRegistry, digest, encode, hashBytes, importLegacySnapshot, recordReference} from './model-registry.mjs';
import {localReader, readRegistry, registryFiles, writeFreshTree} from './model-registry-cli.mjs';
import {createModelCaptureDraft, writeModelCaptureDraft} from './model-capture-package.mjs';
import {installRegistryPosters, projectRegistryRelease, readCapturePackage, syncRegistry} from './model-registry-sync.mjs';
const clone = value => structuredClone(value), CONTEXT = 'b'.repeat(64);
function png(kind, id) { const bytes = Buffer.alloc(80); Buffer.from('89504e470d0a1a0a', 'hex').copy(bytes); bytes.writeUInt32BE(kind === 'detail' ? 512 : 768, 16); bytes.writeUInt32BE(kind === 'detail' ? 512 : 432, 20); bytes[25] = 6; bytes.write(id, 26); return bytes; }
function model(id) {
  const files = new Map(), asset = {id, name: {en: id, zh: id}, description: {en: 'bounded', zh: '保留未知'}, revision: 'r001', worlds: ['world'], packs: ['starter'], collection: 'world', category: 'test', triangles: 12, quality_status: 'work_in_progress', original_formal: 'unknown', sha256: {}};
  for (const kind of ['glb', 'blend', 'preview']) { const path = `assets/additions/${id}/r001/${id}.${kind === 'preview' ? 'png' : kind}`, bytes = Buffer.from(`${id} ${kind}`); asset[kind] = path; asset.sha256[kind] = hashBytes(bytes); files.set(path, bytes); }
  const draft = createModelCaptureDraft({asset, shared: {sha256: CONTEXT, browser: '141.0.7390.37'}, browserVersion: '141.0.7390.37', pixels: {detail: png('detail', id), wheel: png('wheel', id)}, wheelSpec: {zoom: 1.23}, read: path => files.get(path)});
  for (const [path, bytes] of draft.images) files.set(`site/public/${path}`, bytes);
  const record = {version: 1, id, asset, catalog: {pack_ids: ['starter'], legacy_pack_ids: []}, gallery: {poster: clone(draft.record.poster), files: clone(draft.record.files), wheel_framing: {manual_note: 'unchanged'}}, turntable: {asset: null, poster: null}};
  const evidence = {path: `assets/releases/${id}.json`, sha256: hashBytes(id)}; files.set(evidence.path, Buffer.from(id));
  const batch = {version: 1, id: `batch-${id}`, records: [recordReference(record)], definitions: {worlds: [], packs: []}, evidence: [evidence]};
  return {record, draft, files, batch};
}
function setup() {
  const root = mkdtempSync(join(tmpdir(), 'registry-lite-bridge-')), old = model('old-one');
  const snapshot = {manifest: {version: 1, publication: {scope: 'existing collector'}, assets: [old.record.asset]}, catalog: {version: 1, worlds: [{id: 'world', name: {en: 'World', zh: '世界'}}], packs: [{id: 'starter', name: {en: 'Starter', zh: '起始'}, description: {en: 'Starter', zh: '起始'}, asset_ids: ['old-one']}], legacy_memberships: []}, gallery: {version: 1, original: 'manual provenance', posters: {'old-one': old.record.gallery.poster}, files: old.record.gallery.files}, turntables: {version: 1, assets: [], posters: []}, framing: {'old-one': old.record.gallery.wheel_framing}};
  const sourcePins = Object.fromEntries(Object.entries(LEGACY_OUTPUTS).map(([key, path]) => [key, {path, sha256: hashBytes(encode(snapshot[key]))}]));
  const registry = importLegacySnapshot(snapshot, {sourceCommit: 'a'.repeat(40), sourcePins});
  const put = (path, bytes) => { mkdirSync(join(root, path, '..'), {recursive: true}); writeFileSync(join(root, path), bytes); };
  for (const [path, bytes] of old.files) put(path, bytes);
  for (const [key, path] of Object.entries(LEGACY_OUTPUTS)) put(path, `${JSON.stringify(snapshot[key])}\n`);
  return {root, old, snapshot, registry, put, cleanup: () => rmSync(root, {recursive: true, force: true})};
}
const add = (registry, ...values) => ({baseline: clone(registry.baseline), records: [...clone(registry.records), ...values.map(value => value.record)], batches: [...clone(registry.batches), ...values.map(value => value.batch)]});
const manifest = registry => ({...composeRegistry(registry).manifest, publication: {scope: 'existing checked collector, not bridge approval'}});

test('sync/check preserves all five old JSON bytes, unknowns, paths and manual metadata', () => {
  const f = setup(); try {
    const before = new Map(Object.values(LEGACY_OUTPUTS).map(path => [path, readFileSync(join(f.root, path))]));
    assert.deepEqual(syncRegistry({registry: f.registry, releaseManifest: f.snapshot.manifest, targetRoot: f.root}).written, []);
    syncRegistry({registry: f.registry, releaseManifest: f.snapshot.manifest, targetRoot: f.root, check: true});
    for (const [path, bytes] of before) assert.deepEqual(readFileSync(join(f.root, path)), bytes);
    assert.equal(composeRegistry(f.registry).manifest.assets[0].original_formal, 'unknown');
  } finally { f.cleanup(); }
});
test('two independent on-disk additions union without manually updating an aggregate', () => {
  const f = setup(); try {
    const a = model('new-a'), z = model('new-z'), merged = add(f.registry, z, a), regRoot = join(f.root, 'records');
    writeFreshTree(regRoot, registryFiles(f.registry));
    // Each worker contributes only disjoint immutable model/batch files.
    for (const value of [z, a]) {
      const branch = registryFiles(add(f.registry, value));
      for (const [path, json] of branch) if (!registryFiles(f.registry).has(path)) { mkdirSync(join(regRoot, path, '..'), {recursive: true}); writeFileSync(join(regRoot, path), encode(json), {flag: 'wx'}); }
      for (const [path, bytes] of value.files) f.put(path, bytes);
    }
    assert.equal(encode(composeRegistry(readRegistry(regRoot))), encode(composeRegistry(add(f.registry, a, z))));
    const expected = manifest(merged); expected.assets = [merged.records[0].asset, z.record.asset, a.record.asset];
    const reference = join(f.root, 'collector-manifest.json'); writeFileSync(reference, encode(expected));
    const command = [new URL('./model-registry-sync.mjs', import.meta.url).pathname, 'sync', '--registry-root', regRoot, '--release-manifest', reference, '--target-root', f.root];
    const report = JSON.parse(execFileSync(process.execPath, command, {encoding: 'utf8'}));
    assert.deepEqual(report.new_input_ids, ['new-a', 'new-z']); assert.equal(report.publication_authority, false);
    assert.deepEqual(JSON.parse(readFileSync(join(f.root, 'assets/manifest.json'))).assets.map(row => row.id), ['old-one', 'new-z', 'new-a']);
    assert.deepEqual(Object.keys(JSON.parse(readFileSync(join(f.root, 'site/public/gallery/resources.json'))).posters).sort(), ['new-a', 'new-z', 'old-one']);
    command[1] = 'check'; execFileSync(process.execPath, command, {stdio: 'pipe'});
    assert.equal(syncRegistry({registry: merged, releaseManifest: expected, targetRoot: f.root}).written.length, 0);
  } finally { f.cleanup(); }
});
test('collector mismatch, duplicate ID, modified historical record and missing input fail before writing', () => {
  const f = setup(); try {
    const before = readFileSync(join(f.root, 'assets/manifest.json')), a = model('new-a');
    assert.throws(() => projectRegistryRelease(add(f.registry, a), f.snapshot.manifest), /same IDs/);
    const changed = clone(f.snapshot.manifest); changed.assets[0].original_formal = 'approved'; assert.throws(() => projectRegistryRelease(f.registry, changed), /differs from existing/);
    assert.throws(() => projectRegistryRelease(add(f.registry, a, a), manifest(add(f.registry, a))), /duplicate/i);
    const history = clone(f.registry); history.records[0].asset.name.en = 'changed'; assert.throws(() => projectRegistryRelease(history, f.snapshot.manifest), /immutable record changed/);
    assert.throws(() => syncRegistry({registry: add(f.registry, a), releaseManifest: manifest(add(f.registry, a)), targetRoot: f.root}), /ENOENT/);
    assert.deepEqual(readFileSync(join(f.root, 'assets/manifest.json')), before);
  } finally { f.cleanup(); }
});
test('check rejects drift; sync rejects a competing lock and unsafe target symlink', () => {
  const f = setup(); try {
    f.put('site/catalog-data.json', '{}'); assert.throws(() => syncRegistry({registry: f.registry, releaseManifest: f.snapshot.manifest, targetRoot: f.root, check: true}), /indexes differ/);
    f.put('.model-registry-sync.lock', 'other writer'); assert.throws(() => syncRegistry({registry: f.registry, releaseManifest: f.snapshot.manifest, targetRoot: f.root}), /EEXIST/);
    assert.equal(readFileSync(join(f.root, '.model-registry-sync.lock'), 'utf8'), 'other writer'); rmSync(join(f.root, '.model-registry-sync.lock'));
    rmSync(join(f.root, 'site/catalog-data.json')); symlinkSync(join(f.root, 'assets/manifest.json'), join(f.root, 'site/catalog-data.json'));
    assert.throws(() => syncRegistry({registry: f.registry, releaseManifest: f.snapshot.manifest, targetRoot: f.root}), /symlink/);
  } finally { f.cleanup(); }
});
test('seven-model installation is append-only, idempotent and does not replace any shared gallery index', () => {
  const f = setup(); try {
    const values = Array.from({length: 7}, (_, i) => model(`new-${i}`)), registry = add(f.registry, ...values), source = new Map(values.flatMap(value => [...value.files]));
    const before = new Map(Object.values(LEGACY_OUTPUTS).map(path => [path, readFileSync(join(f.root, path))]));
    const oldBytes = readFileSync(join(f.root, 'site/public/gallery/posters/old-one.png'));
    const options = {registry, modelIds: values.map(value => value.record.id), targetRoot: f.root, read: path => source.get(path)};
    assert.equal(installRegistryPosters(options).installed.length, 14); assert.equal(installRegistryPosters(options).unchanged.length, 14);
    for (const [path, bytes] of before) assert.deepEqual(readFileSync(join(f.root, path)), bytes);
    assert.deepEqual(readFileSync(join(f.root, 'site/public/gallery/posters/old-one.png')), oldBytes);
    assert.equal(readdirSync(join(f.root, 'site/public/gallery/posters')).length, 16);
  } finally { f.cleanup(); }
});
test('package writer feeds installer only when its exact asset, poster and seals match the selected record', () => {
  const f = setup(); try {
    const a = model('new-a'), registry = add(f.registry, a), stored = writeModelCaptureDraft(a.draft, f.root), reference = `${a.record.id}/${stored.sha256}`;
    const draft = readCapturePackage(f.root, reference);
    const options = {registry, modelIds: ['new-a'], targetRoot: f.root, read: path => a.files.get(path), packages: [draft]};
    assert.equal(installRegistryPosters(options).installed.length, 2);
    const wrong = clone(draft.record); wrong.poster.wheelSpec.zoom = 4; assert.throws(() => installRegistryPosters({...options, packages: [{record: wrong, images: draft.images}]}), /differs from registered record/);
    writeFileSync(join(f.root, stored.path, 'extra'), 'unselected'); assert.throws(() => readCapturePackage(f.root, reference), /inventory/);
  } finally { f.cleanup(); }
});
test('installer rejects unknown IDs, changed source/pixels, existing different bytes and path symlinks', () => {
  const f = setup(); try {
    const a = model('new-a'), registry = add(f.registry, a), options = {registry, modelIds: ['new-a'], targetRoot: f.root, read: path => a.files.get(path)};
    assert.throws(() => installRegistryPosters({...options, modelIds: ['not-registered']}), /Unknown/);
    assert.throws(() => installRegistryPosters({...options, read: path => path === a.record.asset.glb ? Buffer.from('changed') : a.files.get(path)}), /GLB changed/);
    assert.throws(() => installRegistryPosters({...options, read: path => path.endsWith('.png') ? Buffer.from('changed') : a.files.get(path)}), /byte count/);
    f.put('site/public/gallery/posters/new-a.png', 'historical pixels'); assert.throws(() => installRegistryPosters(options), /Refusing to replace/);
    assert.equal(readFileSync(join(f.root, 'site/public/gallery/posters/new-a.png'), 'utf8'), 'historical pixels');
    rmSync(join(f.root, 'site/public/gallery/posters/new-a.png')); symlinkSync(join(f.root, 'assets/manifest.json'), join(f.root, 'site/public/gallery/posters/new-a.png'));
    assert.throws(() => installRegistryPosters(options), /symlink/);
  } finally { f.cleanup(); }
});
test('concurrent independent poster installers preserve both model namespaces', async () => {
  const f = setup(); try {
    const values = [model('new-a'), model('new-b')], registry = add(f.registry, ...values), regRoot = join(f.root, 'records'), sourceRoot = join(f.root, 'source');
    writeFreshTree(regRoot, registryFiles(registry));
    for (const value of values) for (const [path, bytes] of value.files) { mkdirSync(join(sourceRoot, path, '..'), {recursive: true}); writeFileSync(join(sourceRoot, path), bytes); }
    const run = id => new Promise((resolve, reject) => {
      const child = spawn(process.execPath, [new URL('./model-registry-sync.mjs', import.meta.url).pathname, 'install-posters', '--registry-root', regRoot, '--source-root', sourceRoot, '--target-root', f.root, '--model-ids', id], {stdio: ['ignore', 'ignore', 'pipe']}); let stderr = '';
      child.stderr.on('data', bytes => { stderr += bytes; }); child.on('error', reject); child.on('exit', code => code === 0 ? resolve() : reject(new Error(stderr)));
    });
    await Promise.all(['new-a', 'new-b', 'new-a'].map(run));
    assert.equal(readdirSync(join(f.root, 'site/public/gallery/posters')).length, 6);
  } finally { f.cleanup(); }
});

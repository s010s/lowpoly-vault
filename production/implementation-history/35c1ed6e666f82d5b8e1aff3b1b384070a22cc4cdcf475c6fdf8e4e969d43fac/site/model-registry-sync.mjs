/** Small storage/projection bridge. Never approves a model, captures proof, or runs Git/CI. */
import assert from 'node:assert/strict';
import {existsSync, linkSync, lstatSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, realpathSync, renameSync, rmSync, writeFileSync} from 'node:fs';
import {join, resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {LEGACY_OUTPUTS, composeRegistry, digest, encode, hashBytes, modelInputBinding, safePath} from './model-registry.mjs';
import {localReader, readRegistry} from './model-registry-cli.mjs';
import {assertModelCaptureDraft} from './model-capture-package.mjs';
import {assertPosterPNG} from './gallery-poster-proof.mjs';

const clone = value => structuredClone(value);
const present = path => { try { return lstatSync(path); } catch (error) { if (error.code === 'ENOENT') return null; throw error; } };
function rootPath(root) {
  const base = resolve(root); assert.equal(realpathSync(base), base, 'Target root symlink rejected'); assert(lstatSync(base).isDirectory()); return base;
}
function targetPath(base, path, create = false) {
  assert(safePath(path), 'Unsafe target path');
  let current = base;
  const parts = path.split('/');
  for (const part of parts.slice(0, -1)) {
    current = join(current, part); let info = present(current);
    if (!info && create) { try { mkdirSync(current); } catch (error) { if (error.code !== 'EEXIST') throw error; } info = lstatSync(current); }
    if (info) assert(info.isDirectory() && !info.isSymbolicLink() && realpathSync(current) === current, 'Target parent symlink/non-directory rejected');
  }
  const full = join(base, path), info = present(full);
  if (info) assert(info.isFile() && !info.isSymbolicLink() && realpathSync(full) === full, 'Target file symlink/non-file rejected');
  return full;
}

/** Keep the existing collector's exact model values, order and publication headers.
 * A supplied manifest is reference DATA, not proof that its collector/QA passed.
 * The unchanged publication:check must still validate this result before release. */
export function projectRegistryRelease(registry, releaseManifest) {
  const output = composeRegistry(registry), byID = new Map(output.manifest.assets.map(asset => [asset.id, asset]));
  assert(Array.isArray(releaseManifest?.assets) && !releaseManifest.review_only, 'Existing release manifest required');
  const ids = releaseManifest.assets.map(asset => asset.id);
  assert.equal(new Set(ids).size, ids.length, 'Duplicate release model ID');
  assert.deepEqual([...ids].sort(), [...byID.keys()].sort(), 'Registry and existing release collector must select the same IDs');
  for (const asset of releaseManifest.assets) assert.deepEqual(asset, byID.get(asset.id), `Registry differs from existing release collector: ${asset.id}`);
  output.manifest = {...clone(releaseManifest), assets: ids.map(id => clone(byID.get(id)))};
  return output;
}

/** Only new models are input-checked here; historical/model QA and release checks stay in place. */
export function assertNewRegistryInputs(registry, read) {
  const historical = new Set(registry.baseline.records.map(row => row.id));
  const context = digest(registry.baseline), checked = [];
  for (const record of registry.records) if (!historical.has(record.id)) {
    const batch = registry.batches.find(batch => batch.records.some(ref => ref.id === record.id));
    modelInputBinding(record, {sharedContextSha256: context, evidence: batch.evidence, read}); checked.push(record.id);
  }
  return checked.sort();
}

/** Coordinator operation: only five generated files; no gallery directory replacement.
 * Per-file renames are atomic, not a five-file transaction. After interruption rerun
 * sync/check before the existing release gates. A lock rejects simultaneous syncs. */
export function syncRegistry({registry, releaseManifest, targetRoot, check = false, readInputs}) {
  const output = projectRegistryRelease(registry, releaseManifest), base = rootPath(targetRoot);
  const checkedInputs = assertNewRegistryInputs(registry, readInputs || localReader(base));
  const files = Object.entries(LEGACY_OUTPUTS).map(([key, path]) => {
    const full = targetPath(base, path); return {path, value: output[key], full, before: existsSync(full) ? hashBytes(readFileSync(full)) : null};
  });
  const changed = files.filter(file => !existsSync(file.full) || digest(JSON.parse(readFileSync(file.full))) !== digest(file.value));
  if (check) {
    assert.equal(changed.length, 0, `Generated registry indexes differ: ${changed.map(file => file.path).join(', ')}`);
    return {checked: files.map(file => file.path), new_input_ids: checkedInputs, publication_authority: false};
  }
  const lock = join(base, '.model-registry-sync.lock');
  writeFileSync(lock, `${process.pid}\n`, {flag: 'wx'}); // Never delete another writer's lock.
  let staging;
  try {
    for (const file of files) {
      const full = targetPath(base, file.path);
      assert.equal(existsSync(full) ? hashBytes(readFileSync(full)) : null, file.before, 'Generated indexes changed while preparing; rerun sync');
    }
    staging = mkdtempSync(join(base, '.model-registry-sync-'));
    for (const [i, file] of changed.entries()) writeFileSync(join(staging, String(i)), encode(file.value), {flag: 'wx'});
    for (const [i, file] of changed.entries()) renameSync(join(staging, String(i)), targetPath(base, file.path, true));
  } finally { if (staging) rmSync(staging, {recursive: true, force: true}); rmSync(lock); }
  return {written: changed.map(file => file.path), unchanged: files.filter(file => !changed.includes(file)).map(file => file.path), new_input_ids: checkedInputs, publication_authority: false};
}

/** Read an explicitly selected immutable package; never discover or select an approved revision. */
export function readCapturePackage(root, reference) {
  assert(/^[a-z0-9]+(?:-[a-z0-9]+)*\/[a-f0-9]{64}$/.test(reference), 'Expected explicit model-id/package-sha256');
  const read = localReader(root), prefix = `registry/captures/${reference}`;
  const packageRoot = resolve(rootPath(root), prefix);
  assert.equal(realpathSync(packageRoot), packageRoot, 'Capture package directory symlink rejected');
  assert.deepEqual(readdirSync(packageRoot).sort(), ['capture.json', 'detail.png', 'wheel.png'], 'Capture package inventory differs');
  const bytes = read(`${prefix}/capture.json`), record = JSON.parse(bytes);
  assert.equal(reference, `${record.id}/${digest(record)}`, 'Capture package reference differs');
  assert.equal(hashBytes(bytes), digest(record), 'Capture package record bytes are not canonical');
  const images = new Map(['detail', 'wheel'].map(kind => [record.poster[kind], read(`${prefix}/${kind}.png`)]));
  return assertModelCaptureDraft({record, images});
}

/** Install only sealed registered PNGs. Existing different bytes are NEVER replaced.
 * read supplies a previously reviewed source tree; packages may alternatively come
 * from the opt-in writer. Neither source type confers QA/publication authority. */
export function installRegistryPosters({registry, modelIds, targetRoot, read, packages = []}) {
  composeRegistry(registry);
  assert.equal(typeof read, 'function', 'Exact source byte reader required');
  assert(Array.isArray(modelIds) && modelIds.length && new Set(modelIds).size === modelIds.length, 'Explicit unique model IDs required');
  const drafts = new Map();
  for (const draft of packages) { assertModelCaptureDraft(draft); assert(!drafts.has(draft.record.id), 'Duplicate capture package'); drafts.set(draft.record.id, draft); }
  assert([...drafts.keys()].every(id => modelIds.includes(id)), 'Unselected capture package');
  const base = rootPath(targetRoot), files = [];
  for (const id of [...modelIds].sort()) {
    const record = registry.records.find(record => record.id === id); assert(record, `Unknown registered model: ${id}`);
    assert.equal(hashBytes(read(record.asset.glb)), record.asset.sha256.glb, `Poster model GLB changed: ${id}`);
    const draft = drafts.get(id);
    if (draft) {
      assert.equal(draft.record.asset_sha256, digest(record.asset), 'Capture metadata differs from registered model');
      assert.deepEqual(draft.record.poster, record.gallery.poster, 'Capture poster differs from registered record');
      assert.deepEqual(draft.record.files, record.gallery.files, 'Capture seals differ from registered record');
    }
    for (const kind of ['detail', 'wheel']) {
      const path = record.gallery.poster[kind], seal = record.gallery.files.find(file => file.path === path);
      const bytes = draft ? draft.images.get(path) : read(`site/public/${path}`); assertPosterPNG(bytes, seal, kind);
      const relative = `site/public/${path}`, full = targetPath(base, relative);
      if (existsSync(full)) assert.deepEqual(readFileSync(full), bytes, `Refusing to replace existing poster: ${id}/${kind}`);
      files.push({path: relative, full, bytes});
    }
  }
  const staging = mkdtempSync(join(base, '.model-registry-posters-')), installed = [], unchanged = [];
  try {
    for (const [i, file] of files.entries()) {
      const temporary = join(staging, String(i)); writeFileSync(temporary, file.bytes, {flag: 'wx'});
      const target = targetPath(base, file.path, true);
      try { linkSync(temporary, target); installed.push(file.path); }
      catch (error) { if (error.code !== 'EEXIST') throw error; assert.deepEqual(readFileSync(targetPath(base, file.path)), file.bytes, 'Concurrent poster bytes differ'); unchanged.push(file.path); }
    }
  } finally { rmSync(staging, {recursive: true, force: true}); }
  return {installed, unchanged, model_ids: [...modelIds].sort(), publication_authority: false};
}

export function main(argv = process.argv.slice(2)) {
  const [command, ...rest] = argv, options = {};
  assert(rest.length % 2 === 0, 'Expected --key value options');
  for (let i = 0; i < rest.length; i += 2) {
    assert(/^--[a-z-]+$/.test(rest[i]) && rest[i + 1] && !Object.hasOwn(options, rest[i].slice(2)), 'Expected unique --key value options');
    options[rest[i].slice(2)] = rest[i + 1];
  }
  const required = command === 'sync' || command === 'check' ? ['registry-root', 'release-manifest', 'target-root'] :
    command === 'install-posters' ? ['model-ids', 'registry-root', 'source-root', 'target-root'] : null;
  assert(required, 'Use sync, check or install-posters');
  const optional = command === 'install-posters' ? ['packages-root', 'package-refs'] : [];
  assert(required.every(key => options[key]) && Object.keys(options).every(key => required.includes(key) || optional.includes(key)), 'Unexpected or missing options');
  const registry = readRegistry(options['registry-root']);
  let result;
  if (command !== 'install-posters') result = syncRegistry({registry, releaseManifest: JSON.parse(readFileSync(options['release-manifest'])), targetRoot: options['target-root'], check: command === 'check'});
  else {
    assert(Boolean(options['packages-root']) === Boolean(options['package-refs']), 'Package root and explicit references are required together');
    const packages = options['package-refs'] ? options['package-refs'].split(',').map(ref => readCapturePackage(options['packages-root'], ref)) : [];
    result = installRegistryPosters({registry, modelIds: options['model-ids'].split(','), targetRoot: options['target-root'], read: localReader(options['source-root']), packages});
  }
  console.log(JSON.stringify(result)); return result;
}
if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) main();

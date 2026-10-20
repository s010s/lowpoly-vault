/** Per-model capture storage only. A local package is NEVER publication or QA approval. */
import assert from 'node:assert/strict';
import {mkdirSync, mkdtempSync, lstatSync, readdirSync, readFileSync, realpathSync, renameSync, rmSync, writeFileSync} from 'node:fs';
import {resolve, join} from 'node:path';
import {assetFileAllowlist} from './asset-delivery.mjs';
import {posterInputKey} from './gallery-poster-inputs.mjs';
import {assertPosterPNG, assertPosterRecord} from './gallery-poster-proof.mjs';
import {digest, encode, hashBytes} from './model-registry.mjs';

const HASH = /^[a-f0-9]{64}$/, ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const ownKeys = (value, keys, label) => assert.deepEqual(Object.keys(value).sort(), [...keys].sort(), `${label}: unexpected or missing fields`);
function present(path) { try { return lstatSync(path); } catch (error) { if (error.code === 'ENOENT') return null; throw error; } }
function exactFile(path) { assert.equal(realpathSync(path), path, 'Capture package symlink rejected'); assert(lstatSync(path).isFile()); return readFileSync(path); }

/** The renderer can call this after producing one pair; it does not alter a full gallery. */
export function createModelCaptureDraft({asset, shared, browserVersion, pixels, wheelSpec, read}) {
  assert(ID.test(asset?.id || ''), 'Exact model ID required'); assetFileAllowlist({assets: [asset]});
  assert(HASH.test(asset.sha256?.glb || ''), 'Exact source GLB hash required');
  assert.equal(typeof read, 'function', 'Exact source reader required');
  assert.equal(hashBytes(read(asset.glb)), asset.sha256.glb, 'Capture source GLB bytes changed');
  assert(HASH.test(shared?.sha256 || '') && typeof shared.browser === 'string', 'Renderer recipe binding required');
  assert.equal(browserVersion, shared.browser, 'Capture browser differs from renderer recipe');
  ownKeys(pixels, ['detail', 'wheel'], 'Capture images');
  assert(wheelSpec && typeof wheelSpec === 'object' && !Array.isArray(wheelSpec), 'Captured wheel framing required');
  const id = asset.id, input_sha256 = posterInputKey(asset, shared), files = [], images = new Map();
  const poster = {source_glb_sha256: asset.sha256.glb, input_sha256, browser_version: browserVersion, wheelSpec: structuredClone(wheelSpec)};
  for (const kind of ['detail', 'wheel']) {
    const path = `gallery/posters/${id}${kind === 'wheel' ? '-wheel' : ''}.png`, bytes = pixels[kind];
    assert(Buffer.isBuffer(bytes), 'Capture images must be exact PNG buffers');
    const seal = {path, sha256: hashBytes(bytes), bytes: bytes.length}; assertPosterPNG(bytes, seal, kind);
    poster[kind] = path; files.push(seal); images.set(path, Buffer.from(bytes));
  }
  const record = {version: 1, kind: 'unverified-model-capture', publication_authority: false, id,
    asset_sha256: digest(asset), source_glb_sha256: asset.sha256.glb, shared_sha256: shared.sha256, input_sha256, browser_version: browserVersion, poster, files};
  const draft = {record, images}; assertModelCaptureDraft(draft); return draft;
}
export function assertModelCaptureDraft(draft) {
  ownKeys(draft, ['record', 'images'], 'Capture package');
  const row = draft.record;
  ownKeys(row, ['version', 'kind', 'publication_authority', 'id', 'asset_sha256', 'source_glb_sha256', 'shared_sha256', 'input_sha256', 'browser_version', 'poster', 'files'], 'Capture package record');
  assert(ID.test(row.id || ''), 'Exact capture model ID required');
  assert.equal(row.version, 1); assert.equal(row.kind, 'unverified-model-capture'); assert.equal(row.publication_authority, false, 'A local capture cannot grant publication authority');
  for (const key of ['asset_sha256', 'source_glb_sha256', 'shared_sha256', 'input_sha256']) assert(HASH.test(row[key] || ''), `Capture ${key} required`);
  assert.equal(row.browser_version, row.poster.browser_version);
  assertPosterRecord({...row, evidence: 'captured'});
  assert(draft.images instanceof Map); assert.deepEqual([...draft.images.keys()].sort(), row.files.map(file => file.path).sort(), 'Capture image inventory differs');
  for (const kind of ['detail', 'wheel']) assertPosterPNG(draft.images.get(row.poster[kind]), row.files.find(file => file.path === row.poster[kind]), kind);
  digest(row); return draft;
}
export function capturePackagePath(draft) { assertModelCaptureDraft(draft); return `registry/captures/${draft.record.id}/${digest(draft.record)}`; }

/** Append one immutable namespace. Independent IDs share no mutable metadata file. */
export function writeModelCaptureDraft(draft, root) {
  assertModelCaptureDraft(draft);
  const base = resolve(root); assert.equal(realpathSync(base), base, 'Capture root symlink rejected'); assert(lstatSync(base).isDirectory());
  const relative = capturePackagePath(draft), parts = relative.split('/'), leaf = parts.pop();
  let parent = base;
  for (const part of parts) {
    parent = join(parent, part); const info = present(parent);
    if (!info) { try { mkdirSync(parent); } catch (error) { if (error.code !== 'EEXIST') throw error; } }
    assert.equal(realpathSync(parent), parent, 'Capture parent symlink rejected'); assert(lstatSync(parent).isDirectory());
  }
  const target = join(parent, leaf);
  const expected = new Map([['capture.json', Buffer.from(encode(draft.record))], ['detail.png', draft.images.get(draft.record.poster.detail)], ['wheel.png', draft.images.get(draft.record.poster.wheel)]]);
  const checkExisting = () => {
    assert.equal(realpathSync(target), target, 'Capture package symlink rejected'); assert(lstatSync(target).isDirectory());
    assert.deepEqual(readdirSync(target).sort(), [...expected.keys()].sort(), 'Immutable capture package inventory changed');
    for (const [name, bytes] of expected) assert.deepEqual(exactFile(join(target, name)), bytes, 'Immutable capture package bytes changed');
  };
  if (present(target)) { checkExisting(); return {path: relative, sha256: digest(draft.record), created: false, publication_authority: false}; }
  const staging = mkdtempSync(join(parent, '.capture-staging-'));
  let created = false;
  try {
    for (const [name, bytes] of expected) writeFileSync(join(staging, name), bytes, {flag: 'wx'});
    // A concurrent identical producer may already have installed this content hash.
    if (present(target)) checkExisting();
    else { try { renameSync(staging, target); created = true; } catch (error) { if (!present(target)) throw error; checkExisting(); } }
  } finally { rmSync(staging, {recursive: true, force: true}); }
  return {path: relative, sha256: digest(draft.record), created, publication_authority: false};
}

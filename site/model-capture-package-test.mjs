/** Synthetic PNG headers test storage/seals only, not rendering or pixel quality. */
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync, mkdirSync, symlinkSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawn} from 'node:child_process';
import {createModelCaptureDraft, assertModelCaptureDraft, capturePackagePath, writeModelCaptureDraft} from './model-capture-package.mjs';
import {hashBytes, encode} from './model-registry.mjs';
function png(kind, id) { const bytes = Buffer.alloc(80); Buffer.from('89504e470d0a1a0a', 'hex').copy(bytes); bytes.writeUInt32BE(kind === 'detail' ? 512 : 768, 16); bytes.writeUInt32BE(kind === 'detail' ? 512 : 432, 20); bytes[25] = 6; bytes.write(id, 26); return bytes; }
function fixture(id = 'model-a') {
  const glb = Buffer.from(`${id} source GLB`), asset = {id, glb: `assets/additions/${id}/model.glb`, blend: `assets/additions/${id}/model.blend`, preview: `assets/additions/${id}/preview.png`, sha256: {glb: hashBytes(glb)}};
  const options = {asset, shared: {sha256: 'a'.repeat(64), browser: '141.0.7390.37'}, browserVersion: '141.0.7390.37', wheelSpec: {zoom: 1, offset: [0, 0]}, pixels: {detail: png('detail', id), wheel: png('wheel', id)}, read: () => glb};
  return {options, draft: createModelCaptureDraft(options)};
}
await test('one capture package owns only its model pair and remains unverified', () => {
  const {draft} = fixture(); assertModelCaptureDraft(draft); assert.equal(draft.record.kind, 'unverified-model-capture'); assert.equal(draft.record.publication_authority, false);
  assert.deepEqual([...draft.images.keys()], ['gallery/posters/model-a.png', 'gallery/posters/model-a-wheel.png']);
});
await test('capture package binds actual source bytes, renderer inputs and browser', () => {
  const {options} = fixture(); assert.throws(() => createModelCaptureDraft({...options, read: () => Buffer.from('changed')}), /source GLB bytes changed/);
  assert.throws(() => createModelCaptureDraft({...options, browserVersion: 'different'}), /browser differs/);
  const changed = createModelCaptureDraft({...options, shared: {...options.shared, sha256: 'b'.repeat(64)}});
  assert.notEqual(capturePackagePath(changed), capturePackagePath(createModelCaptureDraft(options)));
});
await test('malformed, opaque, wrong-size and swapped PNGs are rejected', () => {
  const {options} = fixture();
  for (const modify of [bytes => { bytes[0] = 0; }, bytes => { bytes[25] = 2; }, bytes => { bytes.writeUInt32BE(2, 16); }]) {
    const detail = Buffer.from(options.pixels.detail); modify(detail); assert.throws(() => createModelCaptureDraft({...options, pixels: {...options.pixels, detail}}));
  }
  assert.throws(() => createModelCaptureDraft({...options, pixels: {detail: options.pixels.wheel, wheel: options.pixels.detail}}), /dimensions differ/);
});
await test('capture receipt cannot self-promote or claim another model file', () => {
  const {draft} = fixture(); draft.record.publication_authority = true; assert.throws(() => assertModelCaptureDraft(draft), /cannot grant/);
  const other = fixture().draft; other.record.poster.detail = 'gallery/posters/other.png'; assert.throws(() => assertModelCaptureDraft(other), /Noncanonical/);
});
await test('immutable packages are idempotent and never replace source gallery data', () => {
  const root = mkdtempSync(join(tmpdir(), 'model-capture-test-'));
  try {
    mkdirSync(join(root, 'site/public/gallery'), {recursive: true}); writeFileSync(join(root, 'site/public/gallery/resources.json'), 'keep historical snapshot');
    const a = fixture('model-a').draft, b = fixture('model-b').draft;
    const first = writeModelCaptureDraft(a, root), second = writeModelCaptureDraft(b, root);
    assert.notEqual(first.path, second.path); assert.equal(writeModelCaptureDraft(a, root).created, false);
    assert.equal(readFileSync(join(root, 'site/public/gallery/resources.json'), 'utf8'), 'keep historical snapshot');
    assert.deepEqual(readdirSync(join(root, first.path)).sort(), ['capture.json', 'detail.png', 'wheel.png']);
    writeFileSync(join(root, first.path, 'detail.png'), 'changed'); assert.throws(() => writeModelCaptureDraft(a, root), /Immutable capture package bytes changed/);
  } finally { rmSync(root, {recursive: true, force: true}); }
});
await test('unexpected package files and symlink parents fail closed', () => {
  const root = mkdtempSync(join(tmpdir(), 'model-capture-test-'));
  try {
    const {draft} = fixture(), result = writeModelCaptureDraft(draft, root); writeFileSync(join(root, result.path, 'extra.json'), '{}');
    assert.throws(() => writeModelCaptureDraft(draft, root), /inventory changed/);
    const alias = join(root, 'alias'); mkdirSync(alias); symlinkSync(join(root, 'registry'), join(alias, 'registry'));
    assert.throws(() => writeModelCaptureDraft(draft, alias), /symlink rejected/);
  } finally { rmSync(root, {recursive: true, force: true}); }
});
await test('separate simultaneous producers append disjoint namespaces without a shared index', async () => {
  const root = mkdtempSync(join(tmpdir(), 'model-capture-test-'));
  try {
    const module = new URL('./model-capture-package.mjs', import.meta.url).href;
    const run = id => new Promise((resolve, reject) => {
      const {draft} = fixture(id), data = {record: draft.record, images: [...draft.images].map(([path, bytes]) => [path, bytes.toString('base64')])};
      const code = `import {writeModelCaptureDraft} from ${JSON.stringify(module)}; const value=${JSON.stringify(data)}; writeModelCaptureDraft({record:value.record,images:new Map(value.images.map(([p,b])=>[p,Buffer.from(b,'base64')]))},${JSON.stringify(root)});`;
      const child = spawn(process.execPath, ['--input-type=module', '-e', code], {stdio: ['ignore', 'ignore', 'pipe']}); let errors = '';
      child.stderr.on('data', value => { errors += value; }); child.on('error', reject); child.on('exit', code => code === 0 ? resolve() : reject(new Error(errors)));
    });
    await Promise.all(['model-a', 'model-b', 'model-c', 'model-a'].map(run));
    assert.deepEqual(readdirSync(join(root, 'registry/captures')).sort(), ['model-a', 'model-b', 'model-c']);
    for (const id of ['model-a', 'model-b', 'model-c']) assert.equal(readFileSync(join(root, capturePackagePath(fixture(id).draft), 'capture.json'), 'utf8'), encode(fixture(id).draft.record));
  } finally { rmSync(root, {recursive: true, force: true}); }
});

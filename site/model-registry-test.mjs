import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtempSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {LEGACY_OUTPUTS, assertInputBinding, assertIntegrationPlan, assertRegistryAppend, composeRegistry, createIntegrationPlan, digest, encode, hashBytes, importLegacySnapshot, modelInputBinding, recordReference, registryDigest} from './model-registry.mjs';
import {composedFiles, localReader, main, readRegistry, registryFiles, writeFreshTree} from './model-registry-cli.mjs';

const SHA = 'a'.repeat(40), CONTEXT = 'b'.repeat(64), copy = value => structuredClone(value);
function model(id, {pack = 'starter', legacy = false} = {}) {
  const files = new Map(), add = (path, body) => { const bytes = Buffer.from(body); files.set(path, bytes); return {path, sha256: hashBytes(bytes), bytes: bytes.length}; };
  const base = `assets/additions/${id}/r001`, glb = add(`${base}/${id}.glb`, `${id} GLB`), blend = add(`${base}/${id}.blend`, `${id} editable source`), preview = add(`${base}/preview.webp`, `${id} preview`);
  const gallery = ['detail', 'wheel'].map(kind => { const path = `gallery/posters/${id}${kind === 'wheel' ? '-wheel' : ''}.png`; const file = add(`site/public/${path}`, `${id} ${kind}`); return {...file, path}; });
  const asset = {id, revision: 'r001', glb: glb.path, blend: blend.path, preview: preview.path, sha256: {glb: glb.sha256, blend: blend.sha256, preview: preview.sha256}, name: {en: id, zh: id}, description: {en: 'bounded study', zh: '保留原始范围'}, worlds: ['world'], packs: [pack], collection: 'world', category: 'test', triangles: 12, quality_status: 'work_in_progress', unknown_formal_result: null};
  const record = {version: 1, id, asset, catalog: {pack_ids: [pack], legacy_pack_ids: legacy ? [pack] : []}, gallery: {poster: {source_glb_sha256: glb.sha256, detail: gallery[0].path, wheel: gallery[1].path, manual_note: 'keep original'}, files: gallery, wheel_framing: {zoom: 1.23}}, turntable: {asset: null, poster: null}};
  return {record, files};
}
function fixture() {
  const one = model('old-one', {legacy: true}), two = model('old-two', {legacy: true}), records = [two.record, one.record];
  const snapshot = {
    manifest: {version: 1, schema_version: 2, release_status: 'mixed', quality_status: 'mixed', publication: {original_unknown: 'unchanged'}, assets: records.map(row => row.asset)},
    catalog: {version: 1, worlds: [{id: 'world', name: {en: 'World', zh: '世界'}}], packs: [{id: 'starter', name: {en: 'Starter', zh: '起始'}, description: {en: 'original', zh: '原始'}, asset_ids: records.map(row => row.id)}], legacy_memberships: [{pack_id: 'starter', asset_ids: records.map(row => row.id)}]},
    gallery: {version: 1, notes: 'manual metadata is not regenerated', generated_capture: {assets: ['old-one'], published_total: 2}, posters: Object.fromEntries(records.map(row => [row.id, row.gallery.poster])), files: [...records.flatMap(row => row.gallery.files), {path: 'gallery/shared.txt', sha256: CONTEXT, bytes: 12}]},
    turntables: {version: 1, render_preset_sha256: CONTEXT, assets: [], posters: []},
    framing: Object.fromEntries(records.map(row => [row.id, row.gallery.wheel_framing]))
  };
  const sourcePins = Object.fromEntries(Object.entries(LEGACY_OUTPUTS).map(([key, path]) => [key, {path, sha256: hashBytes(encode(snapshot[key]))}]));
  return {snapshot, registry: importLegacySnapshot(snapshot, {sourceCommit: SHA, sourcePins}), files: new Map([...one.files, ...two.files])};
}
function addition(id) {
  const value = model(id, {pack: `pack-${id}`}), evidence = {path: `assets/releases/${id}.json`, sha256: hashBytes(`evidence ${id}`)};
  value.files.set(evidence.path, Buffer.from(`evidence ${id}`));
  const batch = {version: 1, id: `batch-${id}`, records: [recordReference(value.record)], definitions: {worlds: [], packs: [{id: `pack-${id}`, name: {en: id, zh: id}, description: {en: id, zh: id}}]}, evidence: [evidence]};
  return {...value, batch};
}
const append = (base, ...additions) => ({baseline: copy(base.baseline), records: [...copy(base.records), ...additions.map(a => copy(a.record))], batches: [...copy(base.batches), ...additions.map(a => copy(a.batch))]});
const context = files => ({sharedContextSha256: CONTEXT, read: path => { assert(files.has(path), `Missing fixture input ${path}`); return files.get(path); }});

await test('migration preserves all metadata, manual framing, URLs, ordering and formal unknowns', () => {
  const {snapshot, registry} = fixture(); assert.deepEqual(composeRegistry(registry), snapshot);
  assert.equal(composeRegistry(registry).manifest.assets[0].quality_status, 'work_in_progress');
});
await test('independent branches write disjoint model and batch files', () => {
  const {registry} = fixture(), a = addition('new-a'), b = addition('new-b');
  const changed = value => [...registryFiles(append(registry, value)).keys()].filter(path => !registryFiles(registry).has(path));
  assert.deepEqual(changed(a).filter(path => changed(b).includes(path)), []);
});
await test('parallel batch union is deterministic, lossless and independent of arrival order', () => {
  const {registry} = fixture(), a = addition('new-a'), b = addition('new-b');
  const ab = append(registry, a, b), ba = append(registry, b, a);
  assert.equal(encode(composeRegistry(ab)), encode(composeRegistry(ba)));
  assert.equal(registryDigest(ab), registryDigest(ba));
  assert.deepEqual(composeRegistry(ab).manifest.assets.map(row => row.id), ['old-two', 'old-one', 'new-a', 'new-b']);
  assert.equal(composeRegistry(ab).gallery.files.length, 9);
});
await test('historical catalog members retain ordering, additions have independent definitions', () => {
  const {registry} = fixture(), next = append(registry, addition('new-a'));
  assert.deepEqual(composeRegistry(next).catalog.packs[0].asset_ids, ['old-two', 'old-one']);
  assert.deepEqual(composeRegistry(next).catalog.packs[1].asset_ids, ['new-a']);
});
await test('existing undeclared editorial labels are preserved, not invented', () => {
  const {snapshot} = fixture(); snapshot.manifest.assets[0].packs.push('historical-unknown');
  const sourcePins = Object.fromEntries(Object.entries(LEGACY_OUTPUTS).map(([key, path]) => [key, {path, sha256: hashBytes(encode(snapshot[key]))}]));
  const registry = importLegacySnapshot(snapshot, {sourceCommit: SHA, sourcePins});
  assert.deepEqual(composeRegistry(registry), snapshot);
});
await test('duplicate model IDs cannot silently overwrite an earlier branch', () => {
  const {registry} = fixture(); assert.throws(() => composeRegistry(append(registry, addition('new-a'), addition('new-a'))), /duplicate/i);
});
await test('duplicate claims fail even when their content is identical', () => {
  const {registry} = fixture(), a = addition('new-a'), next = append(registry, a);
  next.batches.push({...copy(a.batch), id: 'another-batch'});
  assert.throws(() => composeRegistry(next), /Duplicate model ID/);
});
await test('duplicate pack definitions cannot overwrite prior editorial data', () => {
  const {registry} = fixture(), a = addition('new-a'); a.batch.definitions.packs[0].id = 'starter';
  assert.throws(() => composeRegistry(append(registry, a)), /duplicate starter/);
});
await test('changed immutable record is rejected before composition', () => {
  const {registry} = fixture(); registry.records[0].asset.quality_status = 'approved';
  assert.throws(() => composeRegistry(registry), /immutable record changed/);
});
await test('rehashed historic edits still invalidate append eligibility', () => {
  const {registry} = fixture(), a = addition('new-a'), previous = append(registry, a), next = copy(previous);
  next.records.at(-1).asset.description.en = 'changed'; next.batches[0].records = [recordReference(next.records.at(-1))];
  composeRegistry(next); assert.throws(() => assertRegistryAppend(previous, next), /Historical model changed/);
});
await test('history cannot be removed or the baseline silently refreshed', () => {
  const {registry} = fixture(), next = copy(registry); next.baseline.headers.manifest.publication.original_unknown = 'invented';
  assert.throws(() => assertRegistryAppend(registry, next), /Historical baseline changed/);
});
await test('unselected models cannot leak into generated indices', () => {
  const {registry} = fixture(); registry.records.push(addition('new-a').record);
  assert.throws(() => composeRegistry(registry), /Unselected model/);
});
await test('new asset bytes must be in their own stable-ID namespace', () => {
  const {registry} = fixture(), a = addition('new-a'); a.record.asset.glb = 'assets/additions/old-one/r001/old-one.glb'; a.batch.records = [recordReference(a.record)];
  assert.throws(() => composeRegistry(append(registry, a)), /another model owner/);
});
await test('gallery paths cannot cross model ownership', () => {
  const {registry} = fixture(), a = addition('new-a'); a.record.gallery.poster.detail = 'gallery/posters/old-one.png'; a.batch.records = [recordReference(a.record)];
  assert.throws(() => composeRegistry(append(registry, a)), /another model owner/);
});
await test('gallery proof must bind to the model GLB hash', () => {
  const {registry} = fixture(), a = addition('new-a'); a.record.gallery.poster.source_glb_sha256 = CONTEXT; a.batch.records = [recordReference(a.record)];
  assert.throws(() => composeRegistry(append(registry, a)), /different GLB/);
});
await test('new undeclared pack labels fail instead of fabricating definitions', () => {
  const {registry} = fixture(), a = addition('new-a'); a.record.asset.packs.push('unknown'); a.batch.records = [recordReference(a.record)];
  assert.throws(() => composeRegistry(append(registry, a)), /Missing metadata pack owner/);
});
await test('batches require evidence pins and never declare publication approval', () => {
  const {registry} = fixture(), a = addition('new-a'); a.batch.evidence = [];
  assert.throws(() => composeRegistry(append(registry, a)), /requires pinned external evidence/);
});
await test('exact asset, gallery and external evidence bytes bind to input digest', () => {
  const a = addition('new-a'), options = {...context(a.files), evidence: a.batch.evidence};
  const binding = modelInputBinding(a.record, options); assertInputBinding(binding, a.record, options);
  assert.equal(binding.purpose, 'input-binding-only');
  a.files.set(a.record.asset.glb, Buffer.from('different bytes'));
  assert.throws(() => assertInputBinding(binding, a.record, options), /Input bytes changed/);
});
await test('metadata or policy changes invalidate proof binding; unrelated additions do not', () => {
  const a = addition('new-a'), options = context(a.files), binding = modelInputBinding(a.record, options);
  const changed = copy(a.record); changed.gallery.wheel_framing.zoom = 2;
  assert.throws(() => assertInputBinding(binding, changed, options), /binding changed/);
  assert.throws(() => assertInputBinding(binding, a.record, {...options, sharedContextSha256: 'c'.repeat(64)}), /binding changed/);
  const {registry} = fixture(); composeRegistry(append(registry, a, addition('new-b')));
  assertInputBinding(binding, a.record, options);
});
await test('evidence swapping changes the binding and altered evidence bytes are rejected', () => {
  const a = addition('new-a'), options = {...context(a.files), evidence: a.batch.evidence}, binding = modelInputBinding(a.record, options);
  assert.throws(() => assertInputBinding(binding, a.record, context(a.files)), /binding changed/);
  a.files.set(a.batch.evidence[0].path, Buffer.from('forged approval'));
  assert.throws(() => assertInputBinding(binding, a.record, options), /Input bytes changed/);
});
await test('final integration is narrow, exact-head-bound and cannot self-approve', () => {
  const {registry} = fixture(), next = append(registry, addition('new-a')), plan = createIntegrationPlan(registry, next, {expectedHead: SHA});
  assert.deepEqual(plan.added_model_ids, ['new-a']); assert.equal(plan.retained_model_count, 2);
  assert.equal(plan.mode, 'requires-existing-release-gates');
  assertIntegrationPlan(plan, registry, next, {currentHead: SHA});
  assert.throws(() => assertIntegrationPlan(plan, registry, next, {currentHead: 'b'.repeat(40)}), /head moved/);
  assert.throws(() => assertIntegrationPlan(plan, registry, append(next, addition('new-b')), {currentHead: SHA}), /Integration inputs changed/);
});
await test('legacy projection emits complete deterministic catalog/details without changing URL paths', () => {
  const {registry, snapshot} = fixture(), files = composedFiles(registry);
  assert.equal(files.get('assets/catalog.json').total, 2);
  assert.equal(files.get('assets/catalog/details/old-one.json').glb, snapshot.manifest.assets[1].glb);
  assert.equal(files.get('assets/manifest.json').publication.original_unknown, 'unchanged');
});
await test('filesystem round-trip is immutable and refuses replacing an output tree', () => {
  const dir = mkdtempSync(join(tmpdir(), 'registry-test-'));
  try {
    const {registry} = fixture(), target = join(dir, 'registry'); writeFreshTree(target, registryFiles(registry));
    assert.equal(registryDigest(readRegistry(target)), registryDigest(registry));
    assert.throws(() => writeFreshTree(target, registryFiles(registry)), /Refusing to replace/);
    const ref = registry.baseline.records[0]; writeFileSync(join(target, ref.path), '{}');
    assert.throws(() => readRegistry(target), /digest mismatch/);
  } finally { rmSync(dir, {recursive: true, force: true}); }
});
await test('readers reject path traversal and symlink substitutions', () => {
  const dir = mkdtempSync(join(tmpdir(), 'registry-test-'));
  try {
    writeFileSync(join(dir, 'real.json'), '{}'); symlinkSync(join(dir, 'real.json'), join(dir, 'link.json'));
    const read = localReader(dir);
    assert.throws(() => read('link.json'), /symlink rejected/);
    assert.throws(() => read('../elsewhere'), /Unsafe input path/);
  } finally { rmSync(dir, {recursive: true, force: true}); }
});
await test('CLI refuses moving refs, missing flags and unknown flags', () => {
  assert.throws(() => main(['import', '--repo', '.', '--commit', 'main', '--out', '/tmp/not-created']), /exact 40-character/);
  assert.throws(() => main(['compose', '--registry-root', 'missing', '--out', '/tmp/not-created', '--force', 'true']), /Expected values/);
});

/**
 * Opt-in, data-only model registry. This is NOT a publication or cache authority.
 * Existing release, candidate, source, GPU, gallery and proof gates remain required.
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {posix} from 'node:path';
import {validateCatalogData} from './curation.js';

export const REGISTRY_VERSION = 1;
export const LEGACY_OUTPUTS = Object.freeze({
  manifest: 'assets/manifest.json', catalog: 'site/catalog-data.json',
  turntables: 'assets/turntables/index.json', gallery: 'site/public/gallery/resources.json',
  framing: 'site/gallery/wheel-framing.json'
});
const ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/, HASH = /^[a-f0-9]{64}$/, COMMIT = /^[a-f0-9]{40}$/;
const clone = value => structuredClone(value);
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const without = (value, keys) => Object.fromEntries(Object.entries(value).filter(([key]) => !keys.includes(key)));
const sorted = values => [...values].sort();
const compareID = (a, b) => a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
export const hashBytes = value => createHash('sha256').update(value).digest('hex');
export function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (object(value)) return Object.fromEntries(Object.keys(value).sort().map(key => {
    assert(!['__proto__', 'prototype', 'constructor'].includes(key), `Unsafe JSON key: ${key}`);
    return [key, canonical(value[key])];
  }));
  assert(value === null || ['string', 'boolean'].includes(typeof value) || typeof value === 'number' && Number.isFinite(value), 'Only finite JSON values are allowed');
  return value;
}
export const encode = value => `${JSON.stringify(canonical(value), null, 2)}\n`;
export const digest = value => hashBytes(encode(value));
export const safePath = path => typeof path === 'string' && /^[A-Za-z0-9_./-]+$/.test(path) && !path.startsWith('/') && path.split('/').every(part => part && part !== '.' && part !== '..');
function keys(value, expected, label) {
  assert(object(value), `${label}: object required`);
  assert.deepEqual(sorted(Object.keys(value)), sorted(expected), `${label}: unexpected or missing keys`);
}
function unique(values, label) {
  assert(Array.isArray(values) && new Set(values).size === values.length, `${label}: duplicate values`);
  return values;
}
function identifier(id, label = 'Model') { assert(ID.test(id || ''), `${label}: unsafe identifier ${id}`); }
function pin(value, label) {
  keys(value, ['path', 'sha256'], label);
  assert(safePath(value.path) && HASH.test(value.sha256 || ''), `${label}: safe path and exact SHA-256 required`);
}
function index(rows, key, label) {
  assert(Array.isArray(rows), `${label}: array required`);
  const out = new Map();
  for (const row of rows) { assert(!out.has(row[key]), `${label}: duplicate ${row[key]}`); out.set(row[key], row); }
  return out;
}
function orderRows(rows, historicOrder, key, label) {
  unique(historicOrder, label);
  const byId = index(rows, key, label);
  for (const id of historicOrder) assert(byId.has(id), `${label}: historical owner missing: ${id}`);
  return [...historicOrder, ...sorted([...byId.keys()].filter(id => !historicOrder.includes(id)))].map(id => byId.get(id));
}
function orderedOwners(ids, historical = []) { return orderRows(ids.map(id => ({id})), historical, 'id', 'Membership').map(row => row.id); }

/** Split a pinned historical snapshot without changing its metadata, unknowns or URLs. */
export function importLegacySnapshot(snapshot, {sourceCommit, sourcePins}) {
  assert(COMMIT.test(sourceCommit || ''), 'Import requires an exact source commit');
  keys(snapshot, Object.keys(LEGACY_OUTPUTS), 'Legacy snapshot');
  keys(sourcePins, Object.keys(LEGACY_OUTPUTS), 'Source pins');
  for (const [key, path] of Object.entries(LEGACY_OUTPUTS)) { pin(sourcePins[key], key); assert.equal(sourcePins[key].path, path); }
  const {manifest, catalog, turntables, gallery, framing} = snapshot;
  const models = index(manifest.assets, 'id', 'Manifest'), files = index(gallery.files, 'path', 'Gallery files');
  const turns = index(turntables.assets, 'id', 'Turntables'), cards = index(turntables.posters, 'id', 'Card posters');
  const ownedFiles = new Set();
  for (const [label, ids] of [['gallery', Object.keys(gallery.posters)], ['framing', Object.keys(framing)], ['turntables', [...turns.keys()]], ['cards', [...cards.keys()]]])
    for (const id of ids) assert(models.has(id), `${label}: unknown model ${id}`);
  for (const group of [...catalog.packs, ...catalog.legacy_memberships]) for (const id of unique(group.asset_ids, 'Pack owners')) assert(models.has(id), `Pack owns unknown model ${id}`);
  const records = manifest.assets.map(asset => {
    identifier(asset.id);
    const poster = gallery.posters[asset.id];
    assert(poster, `Missing gallery poster ${asset.id}`);
    const ownFiles = ['detail', 'wheel'].map(kind => {
      const path = poster[kind];
      assert(files.has(path) && !ownedFiles.has(path), `Missing or multiply owned gallery file: ${path}`);
      ownedFiles.add(path); return clone(files.get(path));
    });
    const record = {
      version: REGISTRY_VERSION, id: asset.id, asset: clone(asset),
      catalog: {pack_ids: catalog.packs.filter(pack => pack.asset_ids.includes(asset.id)).map(pack => pack.id), legacy_pack_ids: catalog.legacy_memberships.filter(pack => pack.asset_ids.includes(asset.id)).map(pack => pack.pack_id)},
      gallery: {poster: clone(poster), files: ownFiles, wheel_framing: clone(framing[asset.id] ?? null)},
      turntable: {asset: clone(turns.get(asset.id) ?? null), poster: clone(cards.get(asset.id) ?? null)}
    };
    validateModelRecord(record); return record;
  });
  const baseline = {
    version: REGISTRY_VERSION, mode: 'compatibility-only', source_commit: sourceCommit, source_pins: clone(sourcePins),
    headers: {manifest: without(manifest, ['assets']), gallery: without(gallery, ['posters', 'files']), turntables: without(turntables, ['assets', 'posters']), catalog: {version: catalog.version}},
    definitions: {worlds: clone(catalog.worlds), packs: catalog.packs.map(pack => without(pack, ['asset_ids']))},
    shared_gallery_files: gallery.files.filter(file => !ownedFiles.has(file.path)).map(clone),
    order: {
      models: manifest.assets.map(asset => asset.id), worlds: catalog.worlds.map(world => world.id), packs: catalog.packs.map(pack => pack.id),
      pack_members: Object.fromEntries(catalog.packs.map(pack => [pack.id, clone(pack.asset_ids)])), legacy_members: Object.fromEntries(catalog.legacy_memberships.map(pack => [pack.pack_id, clone(pack.asset_ids)])),
      legacy_packs: catalog.legacy_memberships.map(pack => pack.pack_id),
      gallery_files: gallery.files.map(file => file.path), turntables: turntables.assets.map(row => row.id), card_posters: turntables.posters.map(row => row.id)
    },
    records: records.map(recordReference), snapshot_sha256: digest(snapshot)
  };
  const registry = {baseline, records, batches: []};
  assert.equal(digest(composeRegistry(registry)), baseline.snapshot_sha256, 'Legacy import must round-trip without semantic changes');
  return registry;
}

/** Record identity is content-addressed; model identity is the stable human ID. */
export function recordReference(record) {
  identifier(record.id); const sha256 = digest(record);
  return {id: record.id, path: `registry/models/${record.id}/revisions/${sha256}/record.json`, sha256};
}
export function validateModelRecord(record) {
  keys(record, ['version', 'id', 'asset', 'catalog', 'gallery', 'turntable'], 'Model record');
  assert.equal(record.version, REGISTRY_VERSION); identifier(record.id);
  assert.equal(record.asset?.id, record.id, 'Model and metadata IDs differ');
  keys(record.catalog, ['pack_ids', 'legacy_pack_ids'], 'Model catalog');
  for (const values of Object.values(record.catalog)) { unique(values, 'Model membership'); values.forEach(id => identifier(id, 'Pack')); }
  keys(record.gallery, ['poster', 'files', 'wheel_framing'], 'Model gallery');
  keys(record.turntable, ['asset', 'poster'], 'Model turntable');
  for (const kind of ['glb', 'blend', 'preview']) {
    assert(safePath(record.asset[kind]) && record.asset[kind].startsWith('assets/'), `Unsafe ${kind} path for ${record.id}`);
    assert(HASH.test(record.asset.sha256?.[kind] || ''), `Missing ${kind} hash for ${record.id}`);
  }
  assert.equal(record.gallery.poster.source_glb_sha256, record.asset.sha256.glb, 'Gallery belongs to different GLB bytes');
  const files = index(record.gallery.files, 'path', 'Owned gallery files');
  assert.equal(files.size, 2, 'Exactly detail and wheel gallery files are owned');
  for (const kind of ['detail', 'wheel']) {
    const path = record.gallery.poster[kind];
    assert.equal(path, `gallery/posters/${record.id}${kind === 'wheel' ? '-wheel' : ''}.png`, `Gallery path has another model owner: ${record.id}`);
    const file = files.get(path); assert(file && HASH.test(file.sha256 || '') && Number.isSafeInteger(file.bytes) && file.bytes > 0, 'Gallery file pin required');
  }
  for (const row of Object.values(record.turntable)) if (row !== null) {
    assert.equal(row.id, record.id, 'Turntable belongs to another model');
    assert.equal(row.source_glb_sha256, record.asset.sha256.glb, 'Turntable belongs to different GLB bytes');
  }
  const variants = [''];
  if (typeof record.asset.revision === 'string' && /^[a-z0-9][a-z0-9._-]*$/.test(record.asset.revision) && !record.asset.revision.includes('..')) variants.push(record.asset.revision);
  const escape = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  if (record.turntable.asset) {
    const row = record.turntable.asset;
    pin({path: row.manifest, sha256: row.manifest_sha256}, 'Turntable descriptor');
    assert(variants.some(revision => new RegExp(`^assets/turntables/${escape(record.id)}/${revision ? escape(revision) + '/' : ''}v[0-9]+-[0-9]+-q[0-9]+/turntable\\.json$`).test(row.manifest)), `Turntable descriptor path has another model/revision owner: ${record.id}`);
  }
  if (record.turntable.poster) {
    const row = record.turntable.poster;
    pin({path: row.path, sha256: row.sha256}, 'Card poster');
    assert(variants.some(revision => new RegExp(`^assets/card-previews/${escape(record.id)}${revision ? '-' + escape(revision) : ''}-v[0-9]+-[0-9]+-q[0-9]+\\.webp$`).test(row.path)), `Card poster path has another model/revision owner: ${record.id}`);
    assert(Number.isSafeInteger(row.bytes) && row.bytes > 0, 'Card poster positive byte count required');
  }
  canonical(record); return record;
}

function collectRegistry(registry) {
  keys(registry, ['baseline', 'records', 'batches'], 'Registry');
  const {baseline, records, batches} = registry;
  assert.equal(baseline.version, REGISTRY_VERSION); assert.equal(baseline.mode, 'compatibility-only');
  const models = index(records, 'id', 'Registry model IDs');
  records.forEach(validateModelRecord);
  const claimed = new Set(), batchIDs = new Set();
  function claim(ref, owner) {
    keys(ref, ['id', 'path', 'sha256'], 'Record reference'); identifier(ref.id);
    assert(!claimed.has(ref.id), `Duplicate model ID across owners: ${ref.id}`); claimed.add(ref.id);
    const record = models.get(ref.id); assert(record, `${owner}: missing model ${ref.id}`);
    assert.deepEqual(ref, recordReference(record), `${owner}: immutable record changed: ${ref.id}`);
  }
  baseline.records.forEach(ref => claim(ref, 'Historical baseline'));
  for (const batch of batches) {
    keys(batch, ['version', 'id', 'records', 'definitions', 'evidence'], 'Batch');
    assert.equal(batch.version, REGISTRY_VERSION); identifier(batch.id, 'Batch');
    assert(!batchIDs.has(batch.id), `Duplicate batch ID: ${batch.id}`); batchIDs.add(batch.id);
    assert(Array.isArray(batch.records) && batch.records.length > 0, 'Empty batch refused');
    assert(Array.isArray(batch.evidence) && batch.evidence.length > 0, 'Batch requires pinned external evidence; pins are not approval');
    batch.evidence.forEach(value => pin(value, 'Batch evidence'));
    keys(batch.definitions, ['worlds', 'packs'], 'Batch definitions');
    assert(Array.isArray(batch.definitions.worlds) && Array.isArray(batch.definitions.packs));
    batch.records.forEach(ref => {
      claim(ref, batch.id);
      const record = models.get(ref.id);
      for (const kind of ['glb', 'blend', 'preview']) assert([`assets/additions/${ref.id}/`, `assets/models/${ref.id}/`].some(prefix => record.asset[kind].startsWith(prefix)), `New ${kind} has another model owner: ${ref.id}`);
    });
  }
  assert.equal(claimed.size, models.size, 'Unselected model records cannot enter composition');
  const assetOwners = new Map();
  for (const record of records) {
    const paths = ['glb', 'blend', 'preview'].map(kind => record.asset[kind]);
    paths.push(...record.gallery.files.map(file => `site/public/${file.path}`));
    if (record.turntable.asset) paths.push(record.turntable.asset.manifest);
    if (record.turntable.poster) paths.push(record.turntable.poster.path);
    for (const path of paths) {
      assert(!assetOwners.has(path) || assetOwners.get(path) === record.id, `Asset path shared by different model owners: ${path}`);
      assetOwners.set(path, record.id);
    }
  }
  return models;
}

/** Deterministic set union. No discovery, mutable counters, execution, or QA promotion. */
export function composeRegistry(registry) {
  const models = collectRegistry(registry), {baseline, batches} = registry, {headers, order} = baseline;
  const definitions = {worlds: clone(baseline.definitions.worlds), packs: clone(baseline.definitions.packs)};
  for (const batch of batches) for (const kind of ['worlds', 'packs']) definitions[kind].push(...clone(batch.definitions[kind]));
  for (const kind of ['worlds', 'packs']) {
    definitions[kind].forEach(row => { identifier(row.id, kind); assert(!Object.hasOwn(row, 'asset_ids'), 'Pack ownership comes from model records, not shared definitions'); });
    definitions[kind] = orderRows(definitions[kind], order[kind], 'id', kind);
  }
  const packIDs = new Set(definitions.packs.map(row => row.id)), worldIDs = new Set(definitions.worlds.map(row => row.id));
  const ordered = orderRows([...models.values()], order.models, 'id', 'Models');
  for (const record of ordered) {
    for (const id of record.catalog.pack_ids) assert(packIDs.has(id), `Unknown pack ${id}`);
    for (const id of record.asset.worlds || [record.asset.collection]) assert(worldIDs.has(id), `Unknown world ${id}`);
    const historical = order.models.includes(record.id);
    for (const id of record.asset.packs || []) {
      // Historic undeclared editorial labels are preserved, never filled in or promoted.
      if (!historical || packIDs.has(id)) assert(packIDs.has(id) && record.catalog.pack_ids.includes(id), `Missing metadata pack owner ${record.id}/${id}`);
    }
    for (const id of record.catalog.legacy_pack_ids) assert(order.legacy_packs.includes(id), 'New legacy membership is not an append operation');
  }
  const catalog = {...clone(headers.catalog), worlds: definitions.worlds, packs: definitions.packs.map(pack => ({...pack, asset_ids: orderedOwners(ordered.filter(row => row.catalog.pack_ids.includes(pack.id)).map(row => row.id), order.pack_members[pack.id] || [])})), legacy_memberships: order.legacy_packs.map(pack_id => ({pack_id, asset_ids: orderedOwners(ordered.filter(row => row.catalog.legacy_pack_ids.includes(pack_id)).map(row => row.id), order.legacy_members[pack_id])}))};
  const galleryFiles = [...clone(baseline.shared_gallery_files), ...ordered.flatMap(row => clone(row.gallery.files))];
  const result = {
    manifest: {...clone(headers.manifest), assets: ordered.map(row => clone(row.asset))}, catalog,
    gallery: {...clone(headers.gallery), posters: Object.fromEntries(ordered.map(row => [row.id, clone(row.gallery.poster)])), files: orderRows(galleryFiles, order.gallery_files, 'path', 'Gallery paths')},
    turntables: {...clone(headers.turntables), assets: orderRows(ordered.flatMap(row => row.turntable.asset ? [clone(row.turntable.asset)] : []), order.turntables, 'id', 'Turntables'), posters: orderRows(ordered.flatMap(row => row.turntable.poster ? [clone(row.turntable.poster)] : []), order.card_posters, 'id', 'Card posters')},
    framing: Object.fromEntries(ordered.filter(row => row.gallery.wheel_framing !== null).map(row => [row.id, clone(row.gallery.wheel_framing)]))
  };
  validateCatalogData(result.catalog, {manifest: result.manifest});
  return result;
}

/** No rewriting history, even when the caller recomputes a modified record's hash. */
export function assertRegistryAppend(previous, current) {
  collectRegistry(previous); collectRegistry(current);
  assert.equal(digest(previous.baseline), digest(current.baseline), 'Historical baseline changed');
  const nextModels = new Map(current.records.map(row => [row.id, row]));
  for (const row of previous.records) assert.equal(digest(nextModels.get(row.id) ?? null), digest(row), `Historical model changed or removed: ${row.id}`);
  const nextBatches = new Map(current.batches.map(batch => [batch.id, batch]));
  for (const batch of previous.batches) assert.equal(digest(nextBatches.get(batch.id) ?? null), digest(batch), `Historical batch changed or removed: ${batch.id}`);
  const old = new Set(previous.records.map(row => row.id));
  return sorted(current.records.map(row => row.id).filter(id => !old.has(id)));
}

/** Exact local inputs only. These bindings do NOT validate a CI run or grant reuse. */
export function modelInputBinding(record, {sharedContextSha256, evidence = [], read}) {
  validateModelRecord(record); assert(HASH.test(sharedContextSha256 || ''), 'Shared policy/toolchain context hash required');
  assert.equal(typeof read, 'function', 'Exact file reader required');
  const pins = ['glb', 'blend', 'preview'].map(kind => ({path: record.asset[kind], sha256: record.asset.sha256[kind]}));
  const lengths = new Map(record.gallery.files.map(file => [`site/public/${file.path}`, file.bytes]));
  for (const file of record.gallery.files) pins.push({path: `site/public/${file.path}`, sha256: file.sha256});
  if (record.turntable.asset) {
    const entry = {path: record.turntable.asset.manifest, sha256: record.turntable.asset.manifest_sha256};
    pin(entry, 'Turntable manifest');
    const bytes = read(entry.path); assert.equal(hashBytes(bytes), entry.sha256, `Input bytes changed: ${entry.path}`);
    const turntable = JSON.parse(bytes);
    assert(object(turntable), 'Turntable descriptor object required');
    // Legacy descriptors have no explicit ID: their exact owned path identifies them.
    // Any explicit identity claim must agree; missing fields are not synthesized.
    for (const key of ['id', 'asset_id', 'model_id']) if (Object.hasOwn(turntable, key)) assert.equal(turntable[key], record.id, `Turntable descriptor ${key} differs from its model owner`);
    assert.equal(turntable.source_glb_sha256, record.asset.sha256.glb, 'Turntable descriptor source GLB differs from its model');
    assert.equal(turntable.version, 1, 'Unsupported turntable descriptor version');
    assert(Array.isArray(turntable.frames) && turntable.frames.length > 0, 'Nonempty turntable frame inventory required');
    assert(Number.isSafeInteger(turntable.frame_count) && turntable.frame_count === turntable.frames.length, 'Declared turntable frame_count differs from inventory');
    assert(Number.isSafeInteger(turntable.poster_index) && turntable.poster_index >= 0 && turntable.poster_index < turntable.frame_count, 'Turntable poster index is outside frame inventory');
    assert(Number.isSafeInteger(turntable.total_bytes) && turntable.total_bytes > 0, 'Declared turntable total_bytes required');
    pins.push(entry); let total = 0;
    for (const [i, frame] of turntable.frames.entries()) {
      assert.equal(frame.path, `${posix.dirname(entry.path)}/frame-${String(i).padStart(3, '0')}.webp`, 'Turntable frame ownership/order differs');
      assert(Number.isSafeInteger(frame.bytes) && frame.bytes > 0, 'Turntable frame positive byte count required');
      pins.push({path: frame.path, sha256: frame.sha256}); lengths.set(frame.path, frame.bytes); total += frame.bytes;
    }
    assert(Number.isSafeInteger(total) && total === turntable.total_bytes, 'Declared turntable total_bytes differs from frame inventory');
  }
  if (record.turntable.poster) {
    pins.push({path: record.turntable.poster.path, sha256: record.turntable.poster.sha256});
    lengths.set(record.turntable.poster.path, record.turntable.poster.bytes);
  }
  for (const file of evidence) { pin(file, 'Evidence'); pins.push(file); }
  const inventory = new Map();
  for (const file of pins) {
    pin(file, 'Model input');
    if (inventory.has(file.path)) assert.equal(inventory.get(file.path).sha256, file.sha256, `Conflicting input pins: ${file.path}`);
    else {
      const bytes = read(file.path);
      assert.equal(hashBytes(bytes), file.sha256, `Input bytes changed: ${file.path}`);
      if (lengths.has(file.path)) assert.equal(bytes.length, lengths.get(file.path), `Input byte count changed: ${file.path}`);
      inventory.set(file.path, clone(file));
    }
  }
  const inputs = {version: REGISTRY_VERSION, purpose: 'input-binding-only', model_id: record.id, record_sha256: digest(record), shared_context_sha256: sharedContextSha256, files: [...inventory.values()].sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0)};
  return {...inputs, input_sha256: digest(inputs)};
}
export function assertInputBinding(binding, record, options) {
  assert.deepEqual(binding, modelInputBinding(record, options), 'Model input/proof binding changed');
}

/** Prepare/recheck only. Caller still needs the existing independent release gates. */
export function createIntegrationPlan(previous, next, {expectedHead}) {
  assert(COMMIT.test(expectedHead || ''), 'Exact integration head required');
  const added = assertRegistryAppend(previous, next), outputs = composeRegistry(next);
  return {version: REGISTRY_VERSION, mode: 'requires-existing-release-gates', expected_head: expectedHead,
    previous_registry_sha256: registryDigest(previous), next_registry_sha256: registryDigest(next),
    added_model_ids: added, retained_model_count: previous.records.length,
    outputs: Object.fromEntries(Object.entries(LEGACY_OUTPUTS).map(([key, path]) => [path, digest(outputs[key])]))};
}
export function registryDigest(registry) {
  collectRegistry(registry);
  return digest({baseline: registry.baseline, records: [...registry.records].sort(compareID), batches: [...registry.batches].sort(compareID)});
}
export function assertIntegrationPlan(plan, previous, next, {currentHead}) {
  assert.equal(currentHead, plan.expected_head, 'Integration head moved; recompose and recheck before merging');
  assert.deepEqual(plan, createIntegrationPlan(previous, next, {expectedHead: currentHead}), 'Integration inputs changed');
}

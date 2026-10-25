/** Explicit final-selection layer. Historical collectors/registry remain append-only.
 * A reviewed receipt is an attestation, not reviewer authentication or publication authority.
 * No filesystem writes, discovery, Git operations, world configuration, or QA promotion.
 */
import assert from 'node:assert/strict';
import {readFileSync, realpathSync, lstatSync} from 'node:fs';
import {resolve} from 'node:path';
import {isDeepStrictEqual} from 'node:util';
import {composeRegistry, digest, encode, hashBytes, recordReference, safePath, validateModelRecord} from './model-registry.mjs';

export const MESH_SUCCESSOR_IDS = Object.freeze(['azolla', 'waterfall-ledge', 'barchan-dune', 'onoclea', 'pertica', 'salvinia', 'deflation-hollow', 'oncoid-bed', 'welded-ignimbrite-outcrop', 'folded-strata-outcrop', 'rotational-landslide', 'arroyo-wash', 'hanging-valley', 'kame-mound']);
export const METADATA_SUCCESSOR_FIELDS = Object.freeze({
  'tafoni-outcrop': ['reconstruction_notes.en', 'reconstruction_notes.zh'],
  'desiccation-crack-surface': ['reconstruction_notes.en', 'reconstruction_notes.zh'],
  'geode-cavity': ['origin']
});
const MESH_FIELDS = new Set(['glb', 'blend', 'preview', 'sha256', 'triangles', 'dimensions', 'bounds_glb_m', 'revision', 'source_revision', 'glb_bytes', 'blend_bytes', 'file_sizes', 'downloads', 'card_preview', 'blender_dimensions_m', 'authored_source_vertices', 'evaluated_source_vertices', 'exported_position_accessor_vertices', 'primitives', 'material_count', 'successor_provenance']);
const HASH = /^[a-f0-9]{64}$/, ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SOURCE_DECISIONS = Object.freeze({azolla: 'PASS_BOUNDED_STATIC_REPAIR', 'waterfall-ledge': 'PASS', 'barchan-dune': 'PASS_BOUNDED_INDEPENDENT_STATIC_REVIEW', onoclea: 'PASS_BOUNDED_STATIC_BASAL_REPAIR', pertica: 'PASS_BOUNDED_STATIC_AXIS_REPAIR', salvinia: 'PASS_BOUNDED_STATIC_REPAIR', 'deflation-hollow': 'PASS_LOCAL_GEOMETRY_FIX', 'oncoid-bed': 'PASS_LOCAL_GEOMETRY_FIX', 'welded-ignimbrite-outcrop': 'PASS_LOCAL_TOPOLOGY_FIX', 'folded-strata-outcrop': 'PASS_LOCAL_GEOMETRY_FIX', 'rotational-landslide': 'PASS', 'arroyo-wash': 'PASS_BOUNDED_STATIC_LOCAL_REPAIR', 'hanging-valley': 'PASS_BOUNDED_STATIC_CONTACT_REPAIR', 'kame-mound': 'PASS_LOCAL_STATIC_INCREMENTAL_QA'});
const clone = value => structuredClone(value);
const exact = (value, fields, label) => assert.deepEqual(Object.keys(value || {}).sort(), [...fields].sort(), `${label}: unexpected or missing fields`);
const unique = (rows, label) => { assert(Array.isArray(rows) && new Set(rows).size === rows.length, `${label}: duplicate or missing values`); };
function identity(value) { exact(value, ['id', 'task_id'], 'Identity'); for (const text of Object.values(value)) assert(typeof text === 'string' && text.trim(), 'Explicit identity required'); }
function pin(value) {
  exact(value, ['path', 'sha256', 'bytes'], 'Pin');
  assert(safePath(value.path) && HASH.test(value.sha256) && Number.isSafeInteger(value.bytes) && value.bytes > 0, 'Safe path, SHA-256 and positive size required');
}
export function successorReader(root) {
  const base = realpathSync(root);
  return path => {
    assert(safePath(path), 'Unsafe successor path'); const full = resolve(base, path);
    assert.equal(realpathSync(full), full, 'Successor symlink rejected'); assert(lstatSync(full).isFile(), 'Regular successor file required');
    return readFileSync(full);
  };
}
function pinned(read, reference) {
  pin(reference); const raw = read(reference.path);
  assert(Buffer.isBuffer(raw), `Missing exact bytes: ${reference.path}`);
  assert.equal(raw.length, reference.bytes, `Successor size changed: ${reference.path}`);
  assert.equal(hashBytes(raw), reference.sha256, `Successor hash changed: ${reference.path}`); return raw;
}
function json(read, reference) { return JSON.parse(pinned(read, reference)); }
function changedLeaves(before, after, prefix = '') {
  if (isDeepStrictEqual(before, after)) return [];
  const object = value => value && typeof value === 'object' && !Array.isArray(value);
  if (!object(before) || !object(after)) return [prefix];
  return [...new Set([...Object.keys(before), ...Object.keys(after)])].sort().flatMap(key => changedLeaves(before[key], after[key], prefix ? `${prefix}.${key}` : key));
}
function uniqueAssets(manifest) {
  assert(Array.isArray(manifest?.assets) && !manifest.review_only, 'Published base manifest required');
  unique(manifest.assets.map(asset => asset.id), 'Manifest IDs'); return new Map(manifest.assets.map(asset => [asset.id, asset]));
}
function canonicalRecord(read, reference) {
  const raw = pinned(read, reference), record = JSON.parse(raw);
  assert.equal(hashBytes(raw), digest(record), 'Immutable record bytes must be canonical'); return record;
}
function validateNextRecord(record, previous, release) {
  exact(record, ['version', 'id', 'asset', 'catalog', 'gallery', 'turntable'], 'Successor model record');
  assert.equal(record.id, previous.id, 'Successor must keep exactly the same ID'); assert.equal(record.asset.id, previous.id, 'Successor metadata ID mismatch');
  assert.deepEqual(record.catalog, previous.catalog, 'Successor cannot change catalog memberships');
  // Reuse the original strict record shape validator. Only the isolated successor
  // route permits immutable versioned poster paths; do not relax legacy validation.
  const normalized = clone(record), mapping = new Map();
  for (const kind of ['detail', 'wheel']) {
    const path = record.gallery.poster[kind];
    if (path !== previous.gallery.poster[kind]) assert.equal(path, `gallery/successors/${release}/${record.id}/${kind}.png`, 'Successor poster must have an owned versioned path');
    const stable = `gallery/posters/${record.id}${kind === 'wheel' ? '-wheel' : ''}.png`;
    mapping.set(path, stable); normalized.gallery.poster[kind] = stable;
  }
  normalized.gallery.files = normalized.gallery.files.map(file => ({...file, path: mapping.get(file.path) ?? file.path}));
  validateModelRecord(normalized);
}
function verifyAssetInputs(record, previous, read, kind, release) {
  if (kind === 'metadata') return; // Exact unchanged record guard below forbids any media change.
  for (const key of ['glb', 'blend', 'preview']) {
    assert(record.asset[key].startsWith(`assets/successors/${release}/${record.id}/`), `New ${key} needs an immutable owned successor path`);
    assert.notEqual(record.asset[key], previous.asset[key], 'Historical media path cannot be overwritten');
    const raw = read(record.asset[key]); assert(Buffer.isBuffer(raw) && raw.length > 0, 'Missing successor media');
    assert.equal(hashBytes(raw), record.asset.sha256[key], `${key} subject bytes changed`);
    if (key === 'glb') assert(raw.length >= 12 && raw.toString('ascii', 0, 4) === 'glTF' && raw.readUInt32LE(4) === 2 && raw.readUInt32LE(8) === raw.length, 'Invalid GLB 2 bytes');
    if (key === 'glb' && record.asset.glb_bytes !== undefined) assert.equal(record.asset.glb_bytes, raw.length);
    if (key === 'blend' && record.asset.blend_bytes !== undefined) assert.equal(record.asset.blend_bytes, raw.length);
  }
  for (const kind of ['detail', 'wheel']) {
    const path = record.gallery.poster[kind], seal = record.gallery.files.find(row => row.path === path);
    assert.notEqual(path, previous.gallery.poster[kind], 'Mesh successor cannot reuse historical poster path');
    const raw = pinned(read, {path: `site/public/${path}`, sha256: seal.sha256, bytes: seal.bytes});
    assert(raw.length >= 26 && raw.subarray(0, 8).toString('hex') === '89504e470d0a1a0a', 'Successor PNG required');
    assert.deepEqual([raw.readUInt32BE(16), raw.readUInt32BE(20)], kind === 'wheel' ? [768, 432] : [512, 512], 'Successor poster dimensions differ');
    assert.equal(raw[24], 8, '8-bit poster required'); assert.equal(raw[25], 6, 'RGBA poster required');
  }
  // One newly rendered current-source static card, never an inherited sequence.
  assert.equal(record.turntable.asset, null, 'Successor route is static-card-only');
  const card = record.turntable.poster;
  assert(card && card.path === record.asset.card_preview, 'Exact current-source successor card required');
  assert.notEqual(card.path, previous.turntable.poster?.path, 'Historical card cannot be overwritten');
  assert.equal(card.source_glb_sha256, record.asset.sha256.glb, 'Stale successor card source');
  assert.equal(record.asset.sha256.preview, card.sha256, 'Canonical successor preview must be the exact newly captured card');
  pinned(read, {path: card.path, sha256: card.sha256, bytes: card.bytes});
  if (record.asset.downloads) {
    exact(record.asset.downloads, ['glb', 'blend'], 'Successor downloads');
    assert.equal(record.asset.downloads.glb, record.asset.glb); assert.equal(record.asset.downloads.blend, record.asset.blend);
  }
  if (record.asset.file_sizes) exact(record.asset.file_sizes, ['glb', 'blend'], 'Successor file sizes');
}
// A public projection is not the original byte stream. Only this frozen waterfall
// auxiliary can use the route, after the same independent final reviewer compares
// the private original to the projection. Never relabel its pending input verdict.
function waterfallPublicProjection(binding, original, next, review, read) {
  const projection = json(read, binding.blend_report);
  exact(projection, ['schema_version', 'kind', 'asset_id', 'original', 'omitted_fields', 'document'], 'Waterfall public projection');
  assert.equal(projection.schema_version, 1); assert.equal(projection.kind, 'waterfall-original-inputs-public-projection-v1'); assert.equal(projection.asset_id, 'waterfall-ledge');
  assert.deepEqual(projection.original, {sha256: '138a41b0cda2de9f4682ff041a1a1688dbf7a2c097c8607eb4dd070f86a8a63a', bytes: 17762}, 'Only the exact frozen private original may be projected');
  assert.equal(original.qa_inputs_sha256, projection.original.sha256, 'Unbound waterfall original digest');
  const omitted = [0, 1, 2].map(index => `/original_readonly_inputs/${index}/path`);
  assert.deepEqual(projection.omitted_fields, omitted, 'Only the three private location leaves may be omitted');
  const document = projection.document;
  assert.equal(document.asset_id, next.id); assert.equal(document.revision, 'world-r002'); assert.equal(document.subject_glb_sha256, next.asset.sha256.glb); assert.equal(document.decision, 'PENDING', 'Original pending input verdict must remain unchanged');
  assert(Array.isArray(document.original_readonly_inputs) && document.original_readonly_inputs.length === 3);
  for (const row of document.original_readonly_inputs) { exact(row, ['bytes', 'sha256'], 'Private location omission'); assert(HASH.test(row.sha256) && Number.isSafeInteger(row.bytes) && row.bytes > 0); }
  assert.equal(binding.blend_pointer, '/inputs/69/sha256', 'Frozen waterfall editable-source pointer required');
  assert.equal(document.inputs?.[69]?.path, 'candidate/lod0/waterfall-ledge/waterfall-ledge.blend');
  const proof = json(read, binding.blend_projection_review);
  exact(proof, ['schema_version', 'kind', 'status', 'reviewer', 'original', 'projection', 'original_decision', 'glb_sha256', 'blend_sha256', 'omitted_fields', 'checks', 'blocking_findings', 'publication_authorized', 'reviewer_authority', 'world_accepted', 'physics_accepted'], 'Public evidence projection review');
  assert.equal(proof.schema_version, 1); assert.equal(proof.kind, 'independent-waterfall-input-projection-review-v1'); assert.equal(proof.status, 'PASS', 'Independent original-to-public projection comparison required');
  identity(proof.reviewer); assert.deepEqual(proof.reviewer, review.reviewer, 'The final independent reviewer must bind the public evidence projection');
  assert.deepEqual(proof.original, projection.original); assert.deepEqual(proof.projection, binding.blend_report); assert.deepEqual(proof.original_decision, binding.report);
  assert.equal(proof.glb_sha256, next.asset.sha256.glb); assert.equal(proof.blend_sha256, next.asset.sha256.blend); assert.deepEqual(proof.omitted_fields, omitted);
  const checks = ['private_original_full_hash', 'original_decision_hash_chain', 'exact_three_location_omissions', 'all_other_fields_identical', 'candidate_source_byte_identity', 'private_original_preserved'];
  exact(proof.checks, checks, 'Projection comparison checks'); for (const check of checks) assert.equal(proof.checks[check], 'PASS', `Missing independent projection check: ${check}`);
  assert.deepEqual(proof.blocking_findings, []);
  for (const flag of ['publication_authorized', 'reviewer_authority', 'world_accepted', 'physics_accepted']) assert.equal(proof[flag], false, 'Projection review cannot promote authority or world/physics acceptance');
  return document;
}
function verifyReview(review, entry, selection, previous, next, read) {
  exact(review, ['schema_version', 'kind', 'status', 'reviewer', 'maker', 'subject', 'changed_fields', 'checks', 'evidence', 'blocking_findings', 'publication_authorized', 'reviewer_authority', 'world_accepted', 'physics_accepted'], 'Successor review');
  assert.equal(review.schema_version, 1); assert.equal(review.kind, 'independent-same-id-successor-review-v1'); assert.equal(review.status, 'PASS', 'Fresh bounded independent review required');
  identity(review.reviewer); identity(review.maker);
  for (const key of ['id', 'task_id']) {
    assert.notEqual(review.reviewer[key].trim().toLowerCase(), review.maker[key].trim().toLowerCase(), 'Maker cannot review itself');
    assert.notEqual(review.reviewer[key].trim().toLowerCase(), selection.producer[key].trim().toLowerCase(), 'Preparer cannot review itself');
  }
  assert.deepEqual(review.subject, {id: entry.id, kind: entry.kind, base_manifest_sha256: selection.base_manifest.sha256, previous_record_sha256: entry.previous.sha256, next_record_sha256: entry.next.sha256, previous_glb_sha256: previous.asset.sha256.glb, next_glb_sha256: next.asset.sha256.glb}, 'Stale or different-subject successor QA');
  assert.deepEqual(review.changed_fields, changedLeaves(previous, next), 'Review must describe exact changed record fields');
  const checks = ['same_id_and_count', 'immutable_history', 'collector_registry_parity', 'bounded_scope', ...(entry.kind === 'mesh' ? ['geometry_and_topology', 'source_acceptance', 'current_parser', 'preview_renderer', 'first_hover_parity', 'clipping'] : ['exact_metadata_correction', 'unchanged_media'])];
  exact(review.checks, checks, 'Bounded review checks'); for (const check of checks) assert.equal(review.checks[check], 'PASS', `Missing bounded check: ${check}`);
  const roles = entry.kind === 'mesh' ? ['source_acceptance', 'technical', 'current_parser', 'preview_renderer', 'card_preview'] : ['source_correction'];
  exact(review.evidence, roles, 'Bounded evidence'); for (const reference of Object.values(review.evidence)) pinned(read, reference);
  if (entry.kind === 'mesh') {
    for (const role of ['source_acceptance', 'technical']) {
      const binding = json(read, review.evidence[role]);
      const chainedBlend = Object.hasOwn(binding, 'blend_report'), publicProjection = Object.hasOwn(binding, 'blend_projection_review');
      assert(!publicProjection || chainedBlend, 'Projection review requires the exact auxiliary chain');
      exact(binding, ['schema_version', 'kind', 'role', 'asset_id', 'report', 'glb_pointer', 'blend_pointer', 'decision_field', ...(chainedBlend ? ['blend_report', 'blend_report_sha256_pointer'] : []), ...(publicProjection ? ['blend_projection_review'] : [])], 'Original source evidence binding');
      if (chainedBlend) assert.equal(entry.id, 'waterfall-ledge', 'Only the exact reviewed waterfall auxiliary chain is supported');
      assert.equal(binding.schema_version, 1); assert.equal(binding.kind, 'same-id-original-review-binding-v1'); assert.equal(binding.role, role); assert.equal(binding.asset_id, entry.id);
      const original = json(read, binding.report); assert.equal(original.asset_id, entry.id, 'Original review belongs to another asset');
      assert(['decision', 'status', 'verdict'].includes(binding.decision_field));
      assert.equal(original[binding.decision_field], SOURCE_DECISIONS[entry.id], 'Original review is failing, unaccepted or outside the frozen bounded decision');
      const pointer = (document, path) => {
        assert(typeof path === 'string' && path.startsWith('/') && path.length > 1, 'Explicit original subject pointer required');
        return path.slice(1).split('/').map(part => part.replaceAll('~1', '/').replaceAll('~0', '~')).reduce((value, part) => { assert(value && Object.hasOwn(value, part) && !['__proto__', 'constructor', 'prototype'].includes(part), 'Missing original subject pointer'); return value[part]; }, document);
      };
      assert.equal(pointer(original, binding.glb_pointer), next.asset.sha256.glb, 'Original review GLB subject differs');
      let blendDocument = original;
      if (chainedBlend) {
        assert.equal(binding.blend_report_sha256_pointer, '/qa_inputs_sha256', 'Unexpected waterfall decision-to-manifest link');
        if (publicProjection) blendDocument = waterfallPublicProjection(binding, original, next, review, read);
        else {
          assert.equal(pointer(original, binding.blend_report_sha256_pointer), binding.blend_report.sha256, 'Unbound waterfall auxiliary report');
          blendDocument = json(read, binding.blend_report);
        }
      }
      assert.equal(pointer(blendDocument, binding.blend_pointer), next.asset.sha256.blend, 'Original review editable-source subject differs');
    }
    const parser = json(read, review.evidence.current_parser);
    exact(parser, ['schema_version', 'kind', 'asset_id', 'status', 'glb_sha256', 'triangles', 'meshes', 'three_version', 'errors'], 'Current parser evidence');
    assert.equal(parser.schema_version, 1); assert.equal(parser.kind, 'same-id-current-parser-v1'); assert.equal(parser.asset_id, entry.id); assert.equal(parser.status, 'PASS');
    assert.equal(parser.glb_sha256, next.asset.sha256.glb, 'Current parser GLB subject differs'); assert.equal(parser.triangles, next.asset.triangles, 'Current parser measurements differ');
    assert(Number.isSafeInteger(parser.meshes) && parser.meshes > 0); assert.equal(parser.three_version, '0.180.0'); assert.deepEqual(parser.errors, [], 'Current parser has errors');
  }
  assert.deepEqual(review.blocking_findings, [], 'Unresolved successor finding');
  for (const flag of ['publication_authorized', 'reviewer_authority', 'world_accepted', 'physics_accepted']) assert.equal(review[flag], false, 'Successor QA cannot promote authority or world/physics acceptance');
}

export function assertFrozenSuccessorBatch(selection, base) {
  assert.equal(base.assets.length, 602, 'Frozen successor release requires the post-first8 602 baseline');
  assert.deepEqual(selection.entries.map(row => row.id).sort(), [...MESH_SUCCESSOR_IDS, ...Object.keys(METADATA_SUCCESSOR_FIELDS)].sort(), 'Frozen successor release requires all fourteen mesh and three metadata IDs exactly once');
}

/** Read and verify one explicit selection. No automatic latest-revision behavior. */
export function inspectSuccessorSelection({selection, baseManifest, read}) {
  exact(selection, ['schema_version', 'kind', 'release_id', 'baseline_commit', 'base_manifest', 'base_count', 'producer', 'entries', 'publication_authorized', 'reviewer_authority'], 'Successor selection');
  assert.equal(selection.schema_version, 1); assert.equal(selection.kind, 'same-id-successor-selection-v1');
  assert(ID.test(selection.release_id) && /^[a-f0-9]{40}$/.test(selection.baseline_commit), 'Exact release and baseline required');
  identity(selection.producer); assert.equal(selection.publication_authorized, false); assert.equal(selection.reviewer_authority, false);
  const base = json(read, selection.base_manifest); assert.deepEqual(baseManifest, base, 'Stale successor base manifest');
  const byID = uniqueAssets(base); assert.equal(selection.base_count, base.assets.length, 'Stale baseline count');
  assert(!base.publication?.same_id_successors, 'Nested successor selections need an explicit separately reviewed chain');
  assert(Array.isArray(selection.entries) && selection.entries.length > 0, 'Empty successor selection'); unique(selection.entries.map(row => row.id), 'Successor IDs');
  const entries = [];
  for (const entry of selection.entries) {
    exact(entry, ['id', 'kind', 'old_asset_sha256', 'old_glb_sha256', 'previous', 'next', 'review'], 'Successor entry');
    assert(entry.kind === 'mesh' ? MESH_SUCCESSOR_IDS.includes(entry.id) : entry.kind === 'metadata' && Object.hasOwn(METADATA_SUCCESSOR_FIELDS, entry.id), 'Unapproved successor ID or kind');
    const previous = canonicalRecord(read, entry.previous), next = canonicalRecord(read, entry.next);
    validateModelRecord(previous); assert.equal(previous.id, entry.id, 'Previous same-ID mismatch');
    assert.deepEqual({...recordReference(previous), bytes: entry.previous.bytes}, {...entry.previous, id: entry.id}, 'Original record path or hash differs');
    assert.equal(entry.next.path, `qa/same-id-successors/${selection.release_id}/${entry.id}/${entry.next.sha256}/record.json`, 'Next record must use an explicit immutable successor path');
    assert.deepEqual(previous.asset, byID.get(entry.id), 'Old record is not the selected baseline asset');
    assert.equal(entry.old_asset_sha256, digest(previous.asset), 'Stale old asset guard'); assert.equal(entry.old_glb_sha256, previous.asset.sha256.glb, 'Stale old GLB guard');
    validateNextRecord(next, previous, selection.release_id);
    if (entry.kind === 'metadata') {
      const changed = changedLeaves(previous, next), expected = METADATA_SUCCESSOR_FIELDS[entry.id].map(field => `asset.${field}`).sort();
      assert.deepEqual(changed, expected, 'Metadata successor changed unauthorized fields');
      for (const field of METADATA_SUCCESSOR_FIELDS[entry.id]) {
        const get = (value, path) => path.split('.').reduce((item, key) => item[key], value);
        const before = get(previous.asset, field), after = get(next.asset, field);
        assert(typeof after === 'string' && after.trim(), 'Corrected metadata text required');
        if (field !== 'origin') {
          const suffix = entry.id === 'tafoni-outcrop' ? (field.endsWith('.en') ? ' Cobbania mounts at the freshwater waterline with roots below it.' : 'Cobbania 以淡水水面挂点为原点，根部下垂。') : (field.endsWith('.en') ? ' Limnobiophyllum mounting origin is the freshwater waterline; its roots extend below it.' : 'Limnobiophyllum 原点为淡水水面，根部下垂。');
          assert.equal(before, after + suffix, 'Only the reviewed unrelated suffix may be removed');
        } else assert.equal(after, 'horizontal geometry-bounds center projected onto the ground plane (GLB Y=0; Blender Z=0), not the actual contact point', 'Only the reviewed origin wording is allowed');
      }
    } else {
      const changed = changedLeaves(previous.asset, next.asset);
      assert(changed.every(field => MESH_FIELDS.has(field.split('.')[0])), 'Mesh successor changed unauthorized metadata field');
      assert.notEqual(next.asset.sha256.glb, previous.asset.sha256.glb, 'Mesh successor must change GLB bytes');
      assert.deepEqual(next.asset.successor_provenance, {kind: 'same-id-mesh-successor-v1', release_id: selection.release_id, previous_record_sha256: entry.previous.sha256, previous_glb_sha256: previous.asset.sha256.glb, original_qa_unchanged: true, publication_authorized: false}, 'Exact successor provenance required; old approvals must not describe new geometry');
      assert(Number.isSafeInteger(next.asset.triangles) && next.asset.triangles > 0, 'Positive successor triangles required');
      assert(Array.isArray(next.asset.dimensions) && next.asset.dimensions.length === 3 && next.asset.dimensions.every(value => Number.isFinite(value) && value > 0), 'Measured successor dimensions required');
    }
    verifyAssetInputs(next, previous, read, entry.kind, selection.release_id);
    const review = json(read, entry.review); verifyReview(review, entry, selection, previous, next, read);
    entries.push({entry, previous, next, review});
  }
  return {selection, base, entries, publication_authorized: false, reviewer_authority: false};
}
function descriptorPin(selection, reference, read) { assert.deepEqual(json(read, reference), selection, 'Selected descriptor pin differs'); }
export function selectSuccessorManifest({baseManifest, selection, selectionPin, read}) {
  descriptorPin(selection, selectionPin, read);
  const inspected = inspectSuccessorSelection({selection, baseManifest, read}), replacements = new Map(inspected.entries.map(row => [row.next.id, row.next.asset]));
  const result = {...clone(baseManifest), publication: {...clone(baseManifest.publication), same_id_successors: clone(selectionPin)}, assets: baseManifest.assets.map(asset => clone(replacements.get(asset.id) || asset))};
  assert.equal(uniqueAssets(result).size, baseManifest.assets.length, 'Successor changed asset count'); return result;
}

/** Apply the identical selection after normal immutable registry composition. */
export function composeSuccessorRegistry({registry, baseManifest, selection, selectionPin, read}) {
  const output = composeRegistry(registry), records = new Map(registry.records.map(row => [row.id, row]));
  assert.deepEqual([...records.keys()].sort(), baseManifest.assets.map(row => row.id).sort(), 'Registry/base IDs differ');
  for (const asset of baseManifest.assets) assert.deepEqual(records.get(asset.id).asset, asset, 'Registry/base asset differs');
  const inspected = inspectSuccessorSelection({selection, baseManifest, read});
  output.manifest = selectSuccessorManifest({baseManifest, selection, selectionPin, read});
  for (const {previous, next} of inspected.entries) {
    assert.deepEqual(records.get(previous.id), previous, 'Successor old registry record mismatch');
    output.gallery.posters[next.id] = clone(next.gallery.poster);
    // Keep every original sealed image on disk AND in the resource inventory.
    // The active poster pointer changes; historical pixels are never overwritten.
    for (const file of next.gallery.files) {
      const existing = output.gallery.files.find(row => row.path === file.path);
      if (existing) assert.deepEqual(existing, file, 'Cannot overwrite historical gallery bytes'); else output.gallery.files.push(clone(file));
    }
    for (const [key, value] of [['assets', next.turntable.asset], ['posters', next.turntable.poster]]) {
      const index = output.turntables[key].findIndex(row => row.id === next.id);
      if (index >= 0) { if (value) output.turntables[key][index] = clone(value); else output.turntables[key].splice(index, 1); }
      else if (value) output.turntables[key].push(clone(value));
    }
    if (next.gallery.wheel_framing === null) delete output.framing[next.id]; else output.framing[next.id] = clone(next.gallery.wheel_framing);
  }
  unique(output.gallery.files.map(row => row.path), 'Final gallery paths');
  assert.deepEqual(output.manifest.assets.map(row => row.id), baseManifest.assets.map(row => row.id), 'Final selected IDs/order/count changed');
  return output;
}

/** Strict inverse view for old collectors/compatibility checks. It first proves that
 * the current manifest is precisely the complete authorized overlay, never arbitrary
 * caller-supplied legacy metadata. Existing historical gates must still validate it.
 */
export function historicalManifestView({manifest, read}) {
  const reference = manifest.publication?.same_id_successors;
  if (!reference) return clone(manifest);
  const selection = json(read, reference), base = json(read, selection.base_manifest);
  assert.deepEqual(manifest, selectSuccessorManifest({baseManifest: base, selection, selectionPin: reference, read}), 'Current manifest differs from exact successor selection');
  return base;
}
/** Exact gallery inverse, retaining historical seals and removing only the new
 * explicitly selected versioned files from the comparison view. No broad prefixes.
 */
export function historicalGalleryView({manifest, resources, read}) {
  const reference = manifest.publication?.same_id_successors;
  if (!reference) return clone(resources);
  const selection = json(read, reference), base = historicalManifestView({manifest, read});
  const inspected = inspectSuccessorSelection({selection, baseManifest: base, read});
  const result = clone(resources), added = new Set();
  unique(result.files.map(row => row.path), 'Gallery resource files');
  for (const {previous, next} of inspected.entries) {
    assert.deepEqual(result.posters[next.id], next.gallery.poster, 'Active gallery pointer differs from selected successor');
    for (const file of [...previous.gallery.files, ...next.gallery.files]) assert.deepEqual(result.files.find(row => row.path === file.path), file, 'Missing or modified immutable gallery seal');
    result.posters[next.id] = clone(previous.gallery.poster);
    for (const file of next.gallery.files) if (!previous.gallery.files.some(old => old.path === file.path)) added.add(file.path);
  }
  result.files = result.files.filter(row => !added.has(row.path)); return result;
}
/** Historical card routing for isolated rejection suites. Only exact selected
 * entries may be inverted; unrelated rows and source media bytes are untouched.
 */
export function historicalTurntableView({manifest, turntables, read}) {
  if (!manifest.publication?.same_id_successors) return clone(turntables);
  const context = successorContext({manifest, read}), result = clone(turntables);
  for (const key of ['assets', 'posters']) unique(result[key].map(row => row.id), 'Historical turntable IDs');
  for (const {previous, next} of context.entries) {
    for (const [key, field] of [['assets', 'asset'], ['posters', 'poster']]) {
      const index = result[key].findIndex(row => row.id === next.id), active = index < 0 ? null : result[key][index];
      assert.deepEqual(active, next.turntable[field], 'Active turntable pointer differs from selected successor');
      const old = previous.turntable[field];
      // This frozen batch never removes historical sequences: reject unsupported
      // index insertion rather than guessing the original sequence order.
      if (index < 0) assert.equal(old, null, 'Cannot reconstruct omitted historical sequence order');
      else if (old === null) result[key].splice(index, 1);
      else result[key][index] = clone(old);
    }
  }
  return result;
}
export function successorContext({manifest, read}) {
  const reference = manifest.publication?.same_id_successors;
  if (!reference) return null;
  const selection = json(read, reference), base = historicalManifestView({manifest, read});
  return {...inspectSuccessorSelection({selection, baseManifest: base, read}), selectionPin: reference};
}
/** New mesh wheels must pass the same current PreviewRenderer contract as new
 * animals. A string saying PASS or a historical image pin is insufficient.
 */
export async function verifySuccessorPresentation(root, context) {
  if (!context) return [];
  const read = successorReader(root), {PRODUCTION_WHEEL_ROUTE} = await import('./production-wheel-contract.mjs');
  const {verifyProductionPosters} = await import('./production-release.mjs');
  const checked = [];
  for (const {entry, next, review} of context.entries) {
    if (entry.kind !== 'mesh') continue;
    const presentation = json(read, review.evidence.preview_renderer);
    exact(presentation, ['schema_version', 'kind', 'asset_id', 'maker', 'final_posters', 'publication_authorized', 'reviewer_authority'], 'Successor presentation');
    assert.equal(presentation.schema_version, 1); assert.equal(presentation.kind, 'same-id-successor-presentation-v1'); assert.equal(presentation.asset_id, next.id);
    assert.deepEqual(presentation.maker, review.maker); assert.equal(presentation.publication_authorized, false); assert.equal(presentation.reviewer_authority, false);
    const posters = presentation.final_posters;
    assert.equal(posters.route, PRODUCTION_WHEEL_ROUTE); assert.equal(next.gallery.poster.render_route, PRODUCTION_WHEEL_ROUTE);
    assert.equal(posters.source_glb_sha256, next.asset.sha256.glb);
    for (const kind of ['detail', 'wheel']) {
      const file = next.gallery.files.find(row => row.path === next.gallery.poster[kind]);
      assert.equal(posters[kind].path, `site/public/${file.path}`); assert.equal(posters[kind].sha256, file.sha256); assert.equal(posters[kind].bytes, file.bytes);
    }
    assert.deepEqual(next.gallery.poster.wheelSpec, posters.wheel.wheelSpec, 'Active successor wheel spec differs');
    // Reuse the unchanged detail recipe/config/source checks AND the current wheel
    // checks. The temporary backlink does not mutate published successor metadata.
    await verifyProductionPosters(root, {...next.asset, production_posters: {route: posters.route, detail: posters.detail.path, wheel: posters.wheel.path}}, presentation);
    const {CARD_RENDER_PRESET} = await import('./render-preset.js'), {webpDimensions, webpHasAlpha} = await import('./turntable-delivery.mjs');
    const card = next.turntable.poster, cardCapture = json(read, review.evidence.card_preview), presetHash = hashBytes(JSON.stringify(CARD_RENDER_PRESET));
    exact(cardCapture, ['schema_version', 'kind', 'report', 'cards', 'publication_authorized', 'reviewer_authority'], 'Current card capture binding');
    assert.equal(cardCapture.schema_version, 1); assert.equal(cardCapture.kind, 'same-id-current-card-capture-v1');
    assert.equal(cardCapture.publication_authorized, false); assert.equal(cardCapture.reviewer_authority, false);
    assert(Array.isArray(cardCapture.cards)); unique(cardCapture.cards.map(row => row.id), 'Captured card IDs');
    assert.deepEqual(cardCapture.cards.find(row => row.id === next.id), {id: next.id, path: card.path, sha256: card.sha256, bytes: card.bytes}, 'Current card report does not bind the exact selected WebP');
    const cardReport = json(read, cardCapture.report);
    assert.deepEqual(cardCapture.cards.map(row => row.id).sort(), cardReport.assets.map(row => row.id).sort(), 'Card capture/report IDs differ');
    assert.equal(cardReport.status, 'pass'); assert.equal(cardReport.target_renderer, 'threejs-modelstage');
    assert.equal(cardReport.render_preset_sha256, presetHash); assert.deepEqual(cardReport.render_preset, CARD_RENDER_PRESET);
    assert.equal(cardReport.viewer_source_sha256, hashBytes(read('site/viewer.js')), 'Stale card renderer');
    assert.equal(cardReport.chromium_version, '141.0.7390.37'); assert.equal(cardReport.pinned_chromium_version, cardReport.chromium_version);
    assert.equal(cardReport.gpu?.peakRequests, 1); assert(Array.isArray(cardReport.assets)); unique(cardReport.assets.map(row => row.id), 'Card report IDs');
    assert(cardReport.assets.every(row => MESH_SUCCESSOR_IDS.includes(row.id)), 'Successor card report includes unrelated models');
    const cardResult = cardReport.assets.find(row => row.id === next.id); assert(cardResult, 'Current-source card capture missing');
    assert.equal(cardResult.source_glb_sha256, next.asset.sha256.glb); assert.equal(cardResult.frames, 1); assert.equal(cardResult.frame_bytes_total, 0); assert.equal(cardResult.poster_bytes, card.bytes);
    assert.equal(cardReport.reproducibility?.checked, cardReport.assets.length); assert.deepEqual(cardReport.reproducibility.mismatches, [], 'Successor shipped card must be reproduced exactly');
    assert.equal(card.render_preset_sha256, presetHash); assert.equal(card.width, CARD_RENDER_PRESET.image.width); assert.equal(card.height, CARD_RENDER_PRESET.image.height);
    const cardBytes = pinned(read, {path: card.path, sha256: card.sha256, bytes: card.bytes});
    assert.deepEqual(webpDimensions(cardBytes), [card.width, card.height]); assert(webpHasAlpha(cardBytes), 'Transparent successor card required');
    checked.push(next.id);
  }
  return checked;
}
export function successorSourceClosure({selection, selectionPin, read}) {
  const base = json(read, selection.base_manifest), result = inspectSuccessorSelection({selection, baseManifest: base, read}); descriptorPin(selection, selectionPin, read);
  const paths = new Set([selectionPin.path, selection.base_manifest.path]);
  for (const {entry, next, review} of result.entries) {
    for (const reference of [entry.previous, entry.next, entry.review, ...Object.values(review.evidence)]) paths.add(reference.path);
    if (entry.kind === 'mesh') { for (const kind of ['glb', 'blend', 'preview']) paths.add(next.asset[kind]); for (const file of next.gallery.files) paths.add(`site/public/${file.path}`); paths.add(next.turntable.poster.path); }
    if (entry.kind === 'mesh') {
      const cardCapture = json(read, review.evidence.card_preview); pinned(read, cardCapture.report); paths.add(cardCapture.report.path);
      const presentation = json(read, review.evidence.preview_renderer), wheel = presentation.final_posters?.wheel;
      // Refuse incomplete production evidence when computing a release closure.
      assert(wheel, 'Exact current presentation required for successor source closure');
      for (const reference of [wheel.render_config, wheel.capture_report, wheel.visual_review]) { pinned(read, reference); paths.add(reference.path); }
      const posters = presentation.final_posters;
      for (const reference of [posters.recipe, posters.detail.render_config]) { pinned(read, reference); paths.add(reference.path); }
      for (const reference of json(read, posters.recipe).files) { pinned(read, reference); paths.add(reference.path); }
      for (const role of ['source_acceptance', 'technical']) { const binding = json(read, review.evidence[role]); pinned(read, binding.report); paths.add(binding.report.path); if (binding.blend_report) { pinned(read, binding.blend_report); paths.add(binding.blend_report.path); } if (binding.blend_projection_review) { pinned(read, binding.blend_projection_review); paths.add(binding.blend_projection_review.path); } }
    }
  }
  return [...paths].sort();
}
export {changedLeaves as successorChangedFields};

/** Offline fixed-batch assembly. Never rewrites source/registry history or signs QA.
 * prepare emits PENDING review templates; seal refuses them until independently reviewed.
 */
import assert from 'node:assert/strict';
import {readFileSync, writeFileSync, mkdirSync, existsSync} from 'node:fs';
import {resolve, dirname} from 'node:path';
import {pathToFileURL} from 'node:url';
import {digest, encode, hashBytes, recordReference, LEGACY_OUTPUTS, safePath} from './model-registry.mjs';
import {readRegistry} from './model-registry-cli.mjs';
import {assertFrozenSuccessorBatch, MESH_SUCCESSOR_IDS, METADATA_SUCCESSOR_FIELDS, successorReader, successorChangedFields, successorContext, selectSuccessorManifest, composeSuccessorRegistry, verifySuccessorPresentation, successorSourceClosure} from './same-id-successors.mjs';

const pin = (path, bytes) => ({path, bytes: bytes.length, sha256: hashBytes(bytes)});
function freshWriter(directory) {
  assert(!existsSync(directory), 'Use a fresh output directory; never overwrite a preparation'); mkdirSync(directory, {recursive: true});
  return (path, bytes) => { assert(safePath(path)); const full = resolve(directory, path); mkdirSync(dirname(full), {recursive: true}); writeFileSync(full, bytes, {flag: 'wx'}); return pin(path, bytes); };
}
function correction(asset) {
  const next = structuredClone(asset);
  if (asset.id === 'geode-cavity') next.origin = 'horizontal geometry-bounds center projected onto the ground plane (GLB Y=0; Blender Z=0), not the actual contact point';
  else for (const language of ['en', 'zh']) {
    const suffix = asset.id === 'tafoni-outcrop' ? (language === 'en' ? ' Cobbania mounts at the freshwater waterline with roots below it.' : 'Cobbania 以淡水水面挂点为原点，根部下垂。') : (language === 'en' ? ' Limnobiophyllum mounting origin is the freshwater waterline; its roots extend below it.' : 'Limnobiophyllum 原点为淡水水面，根部下垂。');
    assert(next.reconstruction_notes?.[language]?.endsWith(suffix), 'Actual baseline text differs from the exact reviewed correction');
    next.reconstruction_notes[language] = next.reconstruction_notes[language].slice(0, -suffix.length);
  }
  return next;
}
export function prepareSuccessors({root, baseManifestPath, input, output}) {
  assert.equal(input.kind, 'same-id-successor-assembly-inputs-v1');
  assert(/^[a-f0-9]{40}$/.test(input.baseline_commit), 'Exact prospective base commit required; rebind after the 8-asset merge if it changes');
  assert(/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(input.release_id));
  const expected = [...MESH_SUCCESSOR_IDS, ...Object.keys(METADATA_SUCCESSOR_FIELDS)].sort();
  assert.deepEqual(input.items.map(row => row.id).sort(), expected, 'Assembly must contain exactly the frozen 14+3, once each');
  const registry = readRegistry(root), baseBytes = readFileSync(baseManifestPath), base = JSON.parse(baseBytes), read = successorReader(root), emit = freshWriter(output);
  assert.equal(base.assets.length, 602, 'This release follows the independent 8-animal release, at exactly 602');
  for (const record of registry.records) assert.deepEqual(record.asset, base.assets.find(asset => asset.id === record.id), 'Actual base registry/manifest differ');
  const prefix = `qa/same-id-successors/${input.release_id}`, basePin = emit(`${prefix}/base-manifest.json`, baseBytes), entries = [];
  for (const row of input.items) {
    const previous = registry.records.find(record => record.id === row.id); assert(previous, 'Unknown baseline ID');
    const next = structuredClone(previous), mesh = MESH_SUCCESSOR_IDS.includes(row.id), kind = mesh ? 'mesh' : 'metadata';
    const previousPin = pin(recordReference(previous).path, read(recordReference(previous).path));
    if (mesh) {
      assert(row.asset_patch && row.gallery && row.card, 'Mesh input needs measured metadata, current gallery and card pins');
      next.asset = {...next.asset, ...structuredClone(row.asset_patch), id: previous.id};
      next.asset.successor_provenance = {kind: 'same-id-mesh-successor-v1', release_id: input.release_id, previous_record_sha256: previousPin.sha256, previous_glb_sha256: previous.asset.sha256.glb, original_qa_unchanged: true, publication_authorized: false};
      next.asset.downloads = {glb: next.asset.glb, blend: next.asset.blend};
      next.asset.glb_bytes = read(next.asset.glb).length; next.asset.blend_bytes = read(next.asset.blend).length;
      next.asset.file_sizes = {glb: next.asset.glb_bytes, blend: next.asset.blend_bytes}; next.asset.card_preview = row.card.path;
      next.gallery = structuredClone(row.gallery); next.turntable = {asset: null, poster: structuredClone(row.card)};
    } else { assert(!row.asset_patch && !row.gallery && !row.card, 'Metadata-only inputs cannot change media'); next.asset = correction(next.asset); }
    const nextPin = emit(`${prefix}/${row.id}/${digest(next)}/record.json`, Buffer.from(encode(next)));
    const checks = ['same_id_and_count', 'immutable_history', 'collector_registry_parity', 'bounded_scope', ...(mesh ? ['geometry_and_topology', 'source_acceptance', 'current_parser', 'preview_renderer', 'first_hover_parity', 'clipping'] : ['exact_metadata_correction', 'unchanged_media'])];
    const review = {schema_version: 1, kind: 'independent-same-id-successor-review-v1', status: 'PENDING', reviewer: {id: 'PENDING', task_id: 'PENDING'}, maker: row.maker,
      subject: {id: row.id, kind, base_manifest_sha256: basePin.sha256, previous_record_sha256: previousPin.sha256, next_record_sha256: nextPin.sha256, previous_glb_sha256: previous.asset.sha256.glb, next_glb_sha256: next.asset.sha256.glb},
      changed_fields: successorChangedFields(previous, next), checks: Object.fromEntries(checks.map(key => [key, 'PENDING'])), evidence: row.evidence,
      blocking_findings: ['Independent exact-current-source release projection review is pending.'], publication_authorized: false, reviewer_authority: false, world_accepted: false, physics_accepted: false};
    const reviewPin = emit(`${prefix}/${row.id}/review.json`, Buffer.from(encode(review)));
    entries.push({id: row.id, kind, old_asset_sha256: digest(previous.asset), old_glb_sha256: previous.asset.sha256.glb, previous: previousPin, next: nextPin, review: reviewPin});
  }
  const selection = {schema_version: 1, kind: 'same-id-successor-selection-v1', release_id: input.release_id, baseline_commit: input.baseline_commit, base_manifest: basePin, base_count: base.assets.length, producer: input.producer, entries, publication_authorized: false, reviewer_authority: false};
  emit('selection.template.json', Buffer.from(encode(selection)));
  emit('PREPARATION-STATUS.json', Buffer.from(encode({status: 'PENDING_INDEPENDENT_REVIEW', count_delta: 0, expected_count: 602, exact_ids: expected, publication_authorized: false, reviewer_authority: false, production_selectable: false})));
  return {prepared: expected.length, output, status: 'PENDING_INDEPENDENT_REVIEW', publication_authorized: false};
}
export async function sealSuccessors({root, templatePath, baseManifestPath, expectedBaselineCommit, output}) {
  const read = successorReader(root), template = JSON.parse(readFileSync(templatePath)), base = JSON.parse(readFileSync(baseManifestPath));
  assertFrozenSuccessorBatch(template, base);
  assert.equal(template.baseline_commit, expectedBaselineCommit, 'Baseline moved; reprepare against the exact merged 602 catalog');
  const selection = {...template, entries: template.entries.map(entry => ({...entry, review: pin(entry.review.path, read(entry.review.path))}))};
  // Only review bytes can be finalized here. Any candidate/source change invalidates
  // its frozen pin and requires a new prepare/review, not a silently refreshed hash.
  const path = `qa/same-id-successors/${selection.release_id}/selection.json`, bytes = Buffer.from(encode(selection)), reference = pin(path, bytes);
  const layeredRead = value => value === path ? bytes : read(value);
  const manifest = selectSuccessorManifest({baseManifest: base, selection, selectionPin: reference, read: layeredRead});
  const context = successorContext({manifest, read: layeredRead}); await verifySuccessorPresentation(root, context);
  const files = composeSuccessorRegistry({registry: readRegistry(root), baseManifest: base, selection, selectionPin: reference, read: layeredRead});
  const closure = successorSourceClosure({selection, selectionPin: reference, read: layeredRead});
  // Same-ID successors cannot change editorial memberships or catalog data.
  // Preserve its exact existing bytes/order so historical generated-catalog goldens stay fixed.
  const catalogBytes = read(LEGACY_OUTPUTS.catalog);
  assert.deepEqual(JSON.parse(catalogBytes), files.catalog, 'Successors cannot change the existing catalog data');
  const emit = freshWriter(output); emit(path, bytes);
  for (const [kind, relative] of Object.entries(LEGACY_OUTPUTS)) emit(relative, kind === 'catalog' ? catalogBytes : Buffer.from(encode(files[kind])));
  emit('successor-seal.json', Buffer.from(encode({status: 'LOCAL_SELECTION_CHECKS_PASS', selection: reference, base_count: base.assets.length, final_count: manifest.assets.length, closure, publication_authorized: false, reviewer_authority: false, full_build: 'NOT_RUN', external_actions: 'NONE'})));
  return {output, selection: reference, final_count: manifest.assets.length, publication_authorized: false};
}
if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  const [command, ...args] = process.argv.slice(2), options = {};
  assert(args.length % 2 === 0, 'Use --key value arguments');
  for (let i = 0; i < args.length; i += 2) { assert(/^--[a-z-]+$/.test(args[i]) && !Object.hasOwn(options, args[i].slice(2))); options[args[i].slice(2)] = args[i + 1]; }
  const common = {root: options.root, baseManifestPath: options['base-manifest'], output: options.output};
  const result = command === 'prepare' ? prepareSuccessors({...common, input: JSON.parse(readFileSync(options.inputs))}) : command === 'seal' ? await sealSuccessors({...common, templatePath: options.template, expectedBaselineCommit: options['baseline-commit']}) : assert.fail('Use prepare or seal');
  console.log(JSON.stringify(result));
}

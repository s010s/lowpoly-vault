/** Focused synthetic mechanism tests, NOT acceptance of the real 14 models. */
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFileSync, mkdtempSync, mkdirSync, writeFileSync, copyFileSync, symlinkSync, existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {spawnSync} from 'node:child_process';
import {dirname, join, resolve} from 'node:path';
import {composeRegistry, digest, encode, hashBytes, importLegacySnapshot, LEGACY_OUTPUTS, recordReference} from './model-registry.mjs';
import {createCatalog} from './catalog-build.mjs';
import {composeSuccessorRegistry, historicalManifestView, historicalGalleryView, inspectSuccessorSelection, MESH_SUCCESSOR_IDS, METADATA_SUCCESSOR_FIELDS, selectSuccessorManifest, successorChangedFields, successorSourceClosure, successorContext, verifySuccessorPresentation} from './same-id-successors.mjs';

import baselineEvidence from './fixtures/same-id-successor-baseline.mjs';

const clone = structuredClone, RELEASE = 'world-revisions-20261025';
function png(kind, text) { const bytes = Buffer.alloc(128); Buffer.from('89504e470d0a1a0a', 'hex').copy(bytes); bytes.write('IHDR', 12); bytes.writeUInt32BE(kind === 'detail' ? 512 : 768, 16); bytes.writeUInt32BE(kind === 'detail' ? 512 : 432, 20); bytes[24] = 8; bytes[25] = 6; bytes.write(text, 26); return bytes; }
function glb(text) { const bytes = Buffer.alloc(64); bytes.write('glTF'); bytes.writeUInt32LE(2, 4); bytes.writeUInt32LE(bytes.length, 8); bytes.write(text, 12); return bytes; }
function fixture(count = 18) {
  const files = new Map();
  const save = (path, value) => { const raw = Buffer.isBuffer(value) ? value : Buffer.from(encode(value)); files.set(path, raw); return {path, sha256: hashBytes(raw), bytes: raw.length}; };
  const read = path => files.get(path), live = baselineEvidence;
  const ids = [...MESH_SUCCESSOR_IDS, ...Object.keys(METADATA_SUCCESSOR_FIELDS), 'unaffected-model', ...Array.from({length: count - 18}, (_, i) => `unaffected-extra-${i}`)];
  const records = ids.map(id => {
    const asset = {id, name: {en: id, zh: id}, description: {en: 'Bounded inherited scientific scope.', zh: '保持原有限定。'}, collection: 'world', worlds: ['world'], packs: ['starter'], category: 'test', license: 'CC-BY-4.0', units: 'meters', dimensions: [1, 2, 3], triangles: 10, quality_status: 'bounded_original', approval_provenance: {candidate_record_approved_for_brief: false}, sha256: {}};
    for (const kind of ['glb', 'blend', 'preview']) { const path = `assets/additions/${id}/r001/${id}.${kind}`; const seal = save(path, kind === 'glb' ? glb(id) : Buffer.from(`${id}-${kind}`)); asset[kind] = path; asset.sha256[kind] = seal.sha256; }
    if (METADATA_SUCCESSOR_FIELDS[id]) for (const top of new Set(METADATA_SUCCESSOR_FIELDS[id].map(path => path.split('.')[0]))) asset[top] = clone(live.assets.find(asset => asset.id === id)[top]);
    const poster = {source_glb_sha256: asset.sha256.glb}, owned = [];
    for (const kind of ['detail', 'wheel']) { const path = `gallery/posters/${id}${kind === 'wheel' ? '-wheel' : ''}.png`, seal = save(`site/public/${path}`, png(kind, id)); poster[kind] = path; owned.push({...seal, path}); }
    return {version: 1, id, asset, catalog: {pack_ids: ['starter'], legacy_pack_ids: []}, gallery: {poster, files: owned, wheel_framing: {zoom: 1}}, turntable: {asset: null, poster: null}};
  });
  const snapshot = {manifest: {version: 1, publication: {production_registry: 'production/registry.json'}, assets: records.map(row => row.asset)}, catalog: {version: 1, worlds: [{id: 'world', name: {en: 'World', zh: '世界'}}], packs: [{id: 'starter', name: {en: 'Starter', zh: '起始'}, description: {en: 'Starter', zh: '起始'}, asset_ids: ids}], legacy_memberships: []}, gallery: {version: 1, posters: Object.fromEntries(records.map(row => [row.id, row.gallery.poster])), files: records.flatMap(row => row.gallery.files)}, turntables: {version: 1, assets: [], posters: []}, framing: Object.fromEntries(records.map(row => [row.id, row.gallery.wheel_framing]))};
  const sourcePins = Object.fromEntries(Object.entries(LEGACY_OUTPUTS).map(([key, path]) => [key, {path, sha256: hashBytes(encode(snapshot[key]))}]));
  const registry = importLegacySnapshot(snapshot, {sourceCommit: 'a'.repeat(40), sourcePins}), base = snapshot.manifest;
  const selection = {schema_version: 1, kind: 'same-id-successor-selection-v1', release_id: RELEASE, baseline_commit: 'a'.repeat(40), base_manifest: save('qa/same-id-successors/base-manifest.json', base), base_count: base.assets.length, producer: {id: 'preparer', task_id: 'preparer-task'}, entries: [], publication_authorized: false, reviewer_authority: false};
  for (const previous of registry.records.filter(row => MESH_SUCCESSOR_IDS.includes(row.id) || Object.hasOwn(METADATA_SUCCESSOR_FIELDS, row.id))) {
    const next = clone(previous), kind = MESH_SUCCESSOR_IDS.includes(previous.id) ? 'mesh' : 'metadata';
    if (kind === 'mesh') {
      for (const media of ['glb', 'blend', 'preview']) { const path = `assets/successors/${RELEASE}/${next.id}/${media}.${media === 'preview' ? 'png' : media}`, seal = save(path, media === 'glb' ? glb(`new ${next.id}`) : Buffer.from(`new ${next.id} ${media}`)); next.asset[media] = path; next.asset.sha256[media] = seal.sha256; }
      next.asset.triangles = 12; next.asset.dimensions = [2, 3, 4]; next.asset.revision = 'world-r002';
      next.asset.successor_provenance = {kind: 'same-id-mesh-successor-v1', release_id: RELEASE, previous_record_sha256: digest(previous), previous_glb_sha256: previous.asset.sha256.glb, original_qa_unchanged: true, publication_authorized: false};
      next.gallery.poster.source_glb_sha256 = next.asset.sha256.glb; next.gallery.files = [];
      for (const media of ['detail', 'wheel']) { const path = `gallery/successors/${RELEASE}/${next.id}/${media}.png`, seal = save(`site/public/${path}`, png(media, `new ${next.id}`)); next.gallery.poster[media] = path; next.gallery.files.push({...seal, path}); }
      next.gallery.wheel_framing = {zoom: 1.2};
      const cardPath = `assets/card-previews/${next.id}-${next.asset.revision}-v2-768-q90.webp`, card = save(cardPath, Buffer.from(`new card ${next.id}`));
      next.asset.sha256.preview = save(next.asset.preview, read(cardPath)).sha256;
      next.asset.card_preview = cardPath; next.turntable.poster = {...card, id: next.id, source_glb_sha256: next.asset.sha256.glb, width: 768, height: 768, render_preset_sha256: 'b'.repeat(64)};
    } else if (next.id === 'geode-cavity') next.asset.origin = 'horizontal geometry-bounds center projected onto the ground plane (GLB Y=0; Blender Z=0), not the actual contact point';
    else for (const lang of ['en', 'zh']) { const marker = next.id === 'tafoni-outcrop' ? 'Cobbania' : 'Limnobiophyllum'; next.asset.reconstruction_notes[lang] = next.asset.reconstruction_notes[lang].slice(0, next.asset.reconstruction_notes[lang].indexOf(marker)).trimEnd(); }
    const previousPin = save(recordReference(previous).path, previous), nextPin = save(`qa/same-id-successors/${RELEASE}/${next.id}/${digest(next)}/record.json`, next);
    const entry = {id: next.id, kind, old_asset_sha256: digest(previous.asset), old_glb_sha256: previous.asset.sha256.glb, previous: previousPin, next: nextPin};
    const checks = ['same_id_and_count', 'immutable_history', 'collector_registry_parity', 'bounded_scope', ...(kind === 'mesh' ? ['geometry_and_topology', 'source_acceptance', 'current_parser', 'preview_renderer', 'first_hover_parity', 'clipping'] : ['exact_metadata_correction', 'unchanged_media'])];
    const roles = kind === 'mesh' ? ['source_acceptance', 'technical', 'current_parser', 'preview_renderer', 'card_preview'] : ['source_correction'];
    const review = {schema_version: 1, kind: 'independent-same-id-successor-review-v1', status: 'PASS', reviewer: {id: 'reviewer', task_id: 'reviewer-task'}, maker: {id: 'maker', task_id: 'maker-task'}, subject: {id: entry.id, kind, base_manifest_sha256: selection.base_manifest.sha256, previous_record_sha256: entry.previous.sha256, next_record_sha256: entry.next.sha256, previous_glb_sha256: previous.asset.sha256.glb, next_glb_sha256: next.asset.sha256.glb}, changed_fields: successorChangedFields(previous, next), checks: Object.fromEntries(checks.map(key => [key, 'PASS'])), evidence: Object.fromEntries(roles.map(role => [role, save(`qa/same-id-successors/${RELEASE}/${next.id}/${role}.json`, {synthetic_fixture_only: true, id: next.id, role})])), blocking_findings: [], publication_authorized: false, reviewer_authority: false, world_accepted: false, physics_accepted: false};
    if (kind === 'mesh') {
      const decisions = {azolla:'PASS_BOUNDED_STATIC_REPAIR','waterfall-ledge':'PASS','barchan-dune':'PASS_BOUNDED_INDEPENDENT_STATIC_REVIEW',onoclea:'PASS_BOUNDED_STATIC_BASAL_REPAIR',pertica:'PASS_BOUNDED_STATIC_AXIS_REPAIR',salvinia:'PASS_BOUNDED_STATIC_REPAIR','deflation-hollow':'PASS_LOCAL_GEOMETRY_FIX','oncoid-bed':'PASS_LOCAL_GEOMETRY_FIX','welded-ignimbrite-outcrop':'PASS_LOCAL_TOPOLOGY_FIX','folded-strata-outcrop':'PASS_LOCAL_GEOMETRY_FIX','rotational-landslide':'PASS','arroyo-wash':'PASS_BOUNDED_STATIC_LOCAL_REPAIR','hanging-valley':'PASS_BOUNDED_STATIC_CONTACT_REPAIR','kame-mound':'PASS_LOCAL_STATIC_INCREMENTAL_QA'};
      const original = save(`qa/synthetic-original/${next.id}.json`, {asset_id:next.id,decision:decisions[next.id],subject:{glb:next.asset.sha256.glb,blend:next.asset.sha256.blend}});
      for (const role of ['source_acceptance','technical']) review.evidence[role] = save(review.evidence[role].path, {schema_version:1,kind:'same-id-original-review-binding-v1',role,asset_id:next.id,report:original,glb_pointer:'/subject/glb',blend_pointer:'/subject/blend',decision_field:'decision'});
      review.evidence.current_parser = save(review.evidence.current_parser.path, {schema_version:1,kind:'same-id-current-parser-v1',asset_id:next.id,status:'PASS',glb_sha256:next.asset.sha256.glb,triangles:next.asset.triangles,meshes:1,three_version:'0.180.0',errors:[]});
    }
    entry.review = save(`qa/same-id-successors/${RELEASE}/${next.id}/review.json`, review); selection.entries.push(entry);
  }
  const selectionPin = () => save(`qa/same-id-successors/${RELEASE}/selection.json`, selection);
  const options = () => ({baseManifest: base, selection, selectionPin: selectionPin(), read});
  const changeNext = (id, mutate) => {
    const entry = selection.entries.find(entry => entry.id === id), next = JSON.parse(read(entry.next.path)); mutate(next);
    entry.next = save(`qa/same-id-successors/${RELEASE}/${id}/${digest(next)}/record.json`, next);
  };
  const changeReview = (id, mutate) => { const entry = selection.entries.find(entry => entry.id === id), review = JSON.parse(read(entry.review.path)); mutate(review); entry.review = save(entry.review.path, review); };
  return {files, save, read, registry, base, selection, selectionPin, options, changeNext, changeReview};
}

test('all 14 mesh + 3 metadata replacements select exactly once, preserving history, count and unrelated outputs', () => {
  const f = fixture(), beforeRegistry = encode(f.registry), beforeFiles = new Map([...f.files].map(([path, raw]) => [path, Buffer.from(raw)]));
  const manifest = selectSuccessorManifest(f.options()), result = composeSuccessorRegistry({...f.options(), registry: f.registry});
  assert.deepEqual(result.manifest, manifest); assert.equal(manifest.assets.length, 18); assert.deepEqual(manifest.assets.map(row => row.id), f.base.assets.map(row => row.id));
  assert.equal(encode(f.registry), beforeRegistry);
  for (const [path, raw] of beforeFiles) assert.deepEqual(f.read(path), raw, `Immutable original was mutated: ${path}`);
  for (const entry of f.selection.entries) {
    const next = JSON.parse(f.read(entry.next.path)); assert.deepEqual(manifest.assets.find(row => row.id === entry.id), next.asset);
    assert.deepEqual(result.gallery.posters[entry.id], next.gallery.poster);
    for (const file of next.gallery.files) assert.deepEqual(result.gallery.files.find(row => row.path === file.path), file);
  }
  const old = composeRegistry(f.registry); assert.deepEqual(result.catalog, old.catalog); assert.deepEqual(result.manifest.assets.at(-1), old.manifest.assets.at(-1));
  const built = createCatalog(result.manifest, {catalogData: result.catalog});
  for (const id of [...MESH_SUCCESSOR_IDS, ...Object.keys(METADATA_SUCCESSOR_FIELDS)]) {
    const details = [...built.details.values()]; assert(details.some(value => value.id === id && value.glb === manifest.assets.find(row => row.id === id).glb), `Detail output selects current ${id}`);
  }
  assert.deepEqual(historicalManifestView({manifest, read: f.read}), f.base);
  assert.deepEqual(historicalGalleryView({manifest, resources: result.gallery, read: f.read}), old.gallery);
  assert.throws(() => successorSourceClosure({...f.options()}), /Pin:|Exact current presentation/); // synthetic receipt must not enter real release closure
});
test('same-ID mismatch fails even with a recomputed record hash', () => { const f = fixture(); f.changeNext('azolla', row => { row.id = 'onoclea'; row.asset.id = 'onoclea'; }); assert.throws(() => selectSuccessorManifest(f.options()), /same ID|ID mismatch/); });
test('stale baseline bytes, count, asset hash and GLB guard all fail closed', () => {
  for (const mutate of [f => { f.base.assets[0].triangles++; }, f => { f.selection.base_count++; }, f => { f.selection.entries[0].old_asset_sha256 = '0'.repeat(64); }, f => { f.selection.entries[0].old_glb_sha256 = '0'.repeat(64); }]) {
    const f = fixture(); mutate(f); assert.throws(() => selectSuccessorManifest(f.options()), /Stale/);
  }
});
test('duplicate successors and duplicate baseline IDs fail closed', () => {
  const f = fixture(); f.selection.entries.push(clone(f.selection.entries[0])); assert.throws(() => selectSuccessorManifest(f.options()), /duplicate/);
  const g = fixture(); g.base.assets.push(clone(g.base.assets[0])); g.selection.base_manifest = g.save(g.selection.base_manifest.path, g.base); g.selection.base_count++; assert.throws(() => selectSuccessorManifest(g.options()), /duplicate/);
});
test('out-of-scope IDs and unauthorized mesh scientific/authority/membership fields cannot enter', () => {
  const f = fixture(); f.selection.entries[0].id = 'aglaophyton'; assert.throws(() => selectSuccessorManifest(f.options()), /Unapproved/);
  for (const mutate of [row => { row.asset.scientific_scope = 'verified'; }, row => { row.asset.approval_provenance.candidate_record_approved_for_brief = true; }, row => { row.catalog.pack_ids = []; }]) {
    const g = fixture(); g.changeNext('azolla', mutate); assert.throws(() => selectSuccessorManifest(g.options()), /unauthorized|memberships/);
  }
});
test('metadata-only path rejects geometry, media, arbitrary suffix rewrites, and false origin claims', () => {
  for (const [id, mutate] of [['tafoni-outcrop', row => { row.asset.triangles++; }], ['tafoni-outcrop', row => { row.asset.reconstruction_notes.en = 'Now scientifically proven'; }], ['geode-cavity', row => { row.asset.origin = 'Stable physical contact area'; }]]) {
    const f = fixture(); f.changeNext(id, mutate); assert.throws(() => selectSuccessorManifest(f.options()), /unauthorized|reviewed/);
  }
});
test('historical media paths, stale gallery hashes, non-RGBA wheel and stale source bytes fail', () => {
  const f = fixture(); f.changeNext('azolla', row => { row.asset.glb = f.base.assets[0].glb; }); assert.throws(() => selectSuccessorManifest(f.options()), /immutable owned/);
  const g = fixture(); g.changeNext('azolla', row => { row.gallery.poster.source_glb_sha256 = g.base.assets[0].sha256.glb; }); assert.throws(() => selectSuccessorManifest(g.options()), /different GLB/);
  const h = fixture(), entry = h.selection.entries[0], next = JSON.parse(h.read(entry.next.path)); h.files.set(next.asset.glb, glb('bad')); assert.throws(() => selectSuccessorManifest(h.options()), /subject bytes changed/);
  const preview = fixture(); preview.changeNext('azolla', row => { row.asset.sha256.preview = preview.save(row.asset.preview, Buffer.from('unbound preview')).sha256; }); assert.throws(() => selectSuccessorManifest(preview.options()), /exact newly captured card/);
  const j = fixture(); j.changeNext('azolla', row => { const path = row.gallery.poster.wheel; const bytes = Buffer.from(j.read(`site/public/${path}`)); bytes[25] = 2; const seal = j.save(`site/public/${path}`, bytes); row.gallery.files.find(file => file.path === path).sha256 = seal.sha256; }); assert.throws(() => selectSuccessorManifest(j.options()), /RGBA/);
});
test('fresh independent QA subject, required evidence, checks and authority flags are mandatory', () => {
  for (const mutate of [review => { review.subject.next_record_sha256 = '0'.repeat(64); }, review => { review.subject.base_manifest_sha256 = '0'.repeat(64); }, review => { review.reviewer = clone(review.maker); }, review => { review.checks.clipping = 'PENDING'; }, review => { delete review.evidence.current_parser; }, review => { review.world_accepted = true; }, review => { review.publication_authorized = true; }, review => { review.reviewer_authority = true; }]) {
    const f = fixture(); f.changeReview('azolla', mutate); assert.throws(() => selectSuccessorManifest(f.options()), /Stale|itself|Missing|fields|promote/);
  }
});
test('registry parity and inverse view reject any unrelated current manifest drift', () => {
  const f = fixture(), manifest = selectSuccessorManifest(f.options()); manifest.assets.at(-1).triangles++; assert.throws(() => historicalManifestView({manifest, read: f.read}), /exact successor selection/);
  const g = fixture(); g.registry.records[0].asset.triangles++; assert.throws(() => composeSuccessorRegistry({...g.options(), registry: g.registry}), /immutable record changed/);
});
test('unknown selection fields and authority true fail; no automatic revision-chain behavior', () => {
  for (const mutate of [f => { f.selection.extra = true; }, f => { f.selection.publication_authorized = true; }, f => { f.selection.reviewer_authority = true; }]) { const f = fixture(); mutate(f); assert.throws(() => selectSuccessorManifest(f.options())); }
  const f = fixture(); f.base.publication.same_id_successors = f.selectionPin(); f.selection.base_manifest = f.save('qa/new-base.json', f.base); assert.throws(() => inspectSuccessorSelection({selection: f.selection, baseManifest: f.base, read: f.read}), /Nested/);
});
test('re-pinning a failing or different-subject source/parser report cannot manufacture acceptance', () => {
  for (const change of ['source-status', 'source-subject', 'parser-status', 'parser-subject']) {
    const f = fixture();
    f.changeReview('azolla', review => {
      const role = change.startsWith('source') ? 'source_acceptance' : 'current_parser', value = JSON.parse(f.read(review.evidence[role].path));
      if (role === 'source_acceptance') { const original = JSON.parse(f.read(value.report.path)); if (change.endsWith('status')) original.decision = 'FAIL'; else original.subject.glb = '0'.repeat(64); value.report = f.save(value.report.path, original); }
      else if (change.endsWith('status')) value.status = 'FAIL'; else value.glb_sha256 = '0'.repeat(64);
      review.evidence[role] = f.save(review.evidence[role].path, value);
    });
    assert.throws(() => selectSuccessorManifest(f.options()), /Original review|parser GLB|PASS/);
  }
});
test('waterfall auxiliary Blend pin is accepted only through the primary decision exact hash chain', () => {
  const f = fixture(), entry = f.selection.entries.find(row => row.id === 'waterfall-ledge'), next = JSON.parse(f.read(entry.next.path));
  const auxiliary = f.save('qa/waterfall-auxiliary.json', {decision: 'PENDING', inputs: [{sha256: next.asset.sha256.blend}]}), original = f.save('qa/waterfall-primary.json', {asset_id: next.id, decision: 'PASS', subject_glb_sha256: next.asset.sha256.glb, qa_inputs_sha256: auxiliary.sha256});
  f.changeReview(next.id, review => { for (const role of ['source_acceptance', 'technical']) review.evidence[role] = f.save(review.evidence[role].path, {schema_version: 1, kind: 'same-id-original-review-binding-v1', role, asset_id: next.id, report: original, glb_pointer: '/subject_glb_sha256', blend_pointer: '/inputs/0/sha256', decision_field: 'decision', blend_report: auxiliary, blend_report_sha256_pointer: '/qa_inputs_sha256'}); });
  assert.equal(selectSuccessorManifest(f.options()).assets.length, 18);
  f.changeReview(next.id, review => { const binding = JSON.parse(f.read(review.evidence.source_acceptance.path)); binding.blend_report = f.save(auxiliary.path, {decision: 'PENDING', inputs: [{sha256: next.asset.sha256.blend}], unexpected: true}); review.evidence.source_acceptance = f.save(review.evidence.source_acceptance.path, binding); });
  assert.throws(() => selectSuccessorManifest(f.options()), /Unbound waterfall/);
});
test('602-asset preparer emits exactly14+3 PENDING candidates and seal refuses unreviewed templates without writing', async () => {
  const {registryFiles} = await import('./model-registry-cli.mjs'), {prepareSuccessors, sealSuccessors} = await import('./prepare-same-id-successors.mjs');
  const f = fixture(602), directory = mkdtempSync(join(tmpdir(), 'successor-preparer-only-')), root = join(directory, 'root'), output = join(directory, 'prepared'); mkdirSync(root);
  const put = (path, bytes) => { mkdirSync(dirname(join(root, path)), {recursive: true}); writeFileSync(join(root, path), bytes); };
  for (const [path, value] of registryFiles(f.registry)) put(path, encode(value)); for (const [path, bytes] of f.files) put(path, bytes); put('assets/manifest.json', encode(f.base));
  const items = f.selection.entries.map(entry => { const next = JSON.parse(f.read(entry.next.path)), review = JSON.parse(f.read(entry.review.path)); return {id: entry.id, maker: review.maker, evidence: review.evidence, ...(entry.kind === 'mesh' ? {asset_patch: next.asset, gallery: next.gallery, card: next.turntable.poster} : {})}; });
  const input = {kind: 'same-id-successor-assembly-inputs-v1', release_id: RELEASE, baseline_commit: 'a'.repeat(40), producer: f.selection.producer, items};
  const before = hashBytes(readFileSync(join(root, 'assets/manifest.json'))), prepared = prepareSuccessors({root, baseManifestPath: join(root, 'assets/manifest.json'), input, output}); assert.equal(prepared.prepared, 17);
  assert.equal(hashBytes(readFileSync(join(root, 'assets/manifest.json'))), before);
  const template = JSON.parse(readFileSync(join(output, 'selection.template.json'))); assert.equal(template.base_count, 602);
  for (const reference of [template.base_manifest, ...template.entries.flatMap(row => [row.next, row.review])]) put(reference.path, readFileSync(join(output, reference.path)));
  const sealed = join(directory, 'sealed');
  await assert.rejects(() => sealSuccessors({root, baseManifestPath: join(root, 'assets/manifest.json'), templatePath: join(output, 'selection.template.json'), expectedBaselineCommit: 'a'.repeat(40), output: sealed}), /Fresh bounded independent review/);
  assert(!existsSync(sealed));
  template.entries.pop(); put('partial-template.json', encode(template));
  await assert.rejects(() => sealSuccessors({root, baseManifestPath: join(root, 'assets/manifest.json'), templatePath: join(root, 'partial-template.json'), expectedBaselineCommit: 'a'.repeat(40), output: sealed}), /all fourteen mesh and three metadata/);
  assert(!existsSync(sealed));
});

test('integrated registry, card route and exact current wheel/card contracts accept a bounded synthetic receipt and reject stale captures', async () => {
  const {productionWheelRenderer, createProductionWheel, PRODUCTION_WHEEL_ROUTE} = await import('./production-wheel-contract.mjs');
  const {posterRendererFiles} = await import('./gallery-poster-inputs.mjs');
  const {CARD_RENDER_PRESET} = await import('./render-preset.js');
  const {projectRegistryRelease} = await import('./model-registry-sync.mjs');
  const {publishedImagePaths, collectTurntables} = await import('./turntable-delivery.mjs');
  const {historicalPosterSource} = await import('./gallery-poster-compat.mjs');
  const {main842PosterSource} = await import('./gallery-main842-compat.mjs');
  const f = fixture(), root = mkdtempSync(join(tmpdir(), 'successor-contract-only-')), source = new URL('..', import.meta.url).pathname;
  // Retain this tiny synthetic fixture as test evidence. It is not release QA.
  const put = (path, raw) => { mkdirSync(dirname(join(root, path)), {recursive: true}); writeFileSync(join(root, path), raw); };
  const rendererPaths = [...new Set([...await posterRendererFiles(source), 'site/capture-wheel-frame.js', 'package-lock.json', 'site/viewer.js'])];
  for (const path of rendererPaths) put(path, readFileSync(join(source, path)));
  mkdirSync(join(root, 'node_modules'), {recursive: true}); symlinkSync(resolve(source, 'node_modules/playwright-core'), join(root, 'node_modules/playwright-core'));
  const renderer = await productionWheelRenderer(root), spec = {azimuth: 42, elevation: 23.3, zoom: 1, aspect: 16 / 9, offset: [0, 0], floorCenter: [0.5, 0.8], floorPoints: [[0, 0], [1, 0], [0, 1]], projectedBounds: {left: -1, right: 1, top: 1, bottom: -1}};
  f.selection.entries = f.selection.entries.filter(row => row.id === 'azolla');
  f.changeNext('azolla', next => {
    next.gallery.poster.render_route = PRODUCTION_WHEEL_ROUTE; next.gallery.poster.wheelSpec = spec;
    const webp = Buffer.alloc(26); webp.write('RIFF'); webp.writeUInt32LE(18, 4); webp.write('WEBP', 8); webp.write('VP8L', 12); webp.writeUInt32LE(5, 16); webp[20] = 0x2f; webp.writeUInt32LE(767 | (767 << 14) | (1 << 28), 21);
    const card = f.save(next.asset.card_preview, webp); next.asset.sha256.preview = f.save(next.asset.preview, webp).sha256; Object.assign(next.turntable.poster, card, {render_preset_sha256: hashBytes(JSON.stringify(CARD_RENDER_PRESET))});
  });
  const entry = f.selection.entries[0], next = JSON.parse(f.read(entry.next.path)), old = JSON.parse(f.read(entry.previous.path));
  const detail = next.gallery.files.find(row => row.path === next.gallery.poster.detail), wheel = next.gallery.files.find(row => row.path === next.gallery.poster.wheel);
  const detailPin = {...detail, path: `site/public/${detail.path}`}, wheelPin = {...wheel, path: `site/public/${wheel.path}`}, wheelBytes = f.read(wheelPin.path);
  const capture = createProductionWheel({frame: {id: next.id, source_glb_sha256: next.asset.sha256.glb, dataURL: `data:image/png;base64,${wheelBytes.toString('base64')}`, wheelSpec: spec}, png: wheelBytes, asset: next.asset, sourceGLB: f.read(next.asset.glb), unchangedDetail: f.read(detailPin.path), rendererSha256: renderer.sha256, browserVersion: renderer.browser});
  const capturePin = f.save('qa/synthetic-current-capture.json', capture);
  const report = {version: 1, kind: 'new-production-wheel-capture-evidence', status: 'capture-and-geometry-check-pass', publication_authority: false, visual_review: 'pending', physical_gpu: 'unknown', errors: [], renderer_sha256: renderer.sha256, renderer_files: renderer.files, browser_version: renderer.browser, producer: {id: 'capture-maker', task_id: 'capture-task'}, cases: [{id: next.id, source_glb_sha256: next.asset.sha256.glb, wheel_sha256: wheel.sha256, first_frame_id: next.id, spec, status: 'geometry-check-pass', context_lost: false, gl_error: 0, mask_iou: 1, mean_rgb_absolute_error: 0, lifecycle: {context_lost: false, gl_error: 0, reentry_exact: true, frames: [0, 45, 90, 135, 180, 225, 270, 315].map(yaw => ({yaw, border_opaque_pixels: 0}))}}]};
  const reportPin = f.save('qa/synthetic-current-report.json', report), independent = {version: 1, kind: 'independent-production-wheel-review', status: 'PASS', reviewer: {id: 'visual-reviewer', task_id: 'visual-review-task'}, reviewed_capture_sha256: capturePin.sha256, reviewed_report_sha256: reportPin.sha256, source_glb_sha256: next.asset.sha256.glb, wheel_sha256: wheel.sha256, checks: Object.fromEntries(['same_source_detail', 'first_frame_parity', 'hover_reentry', 'turntable_no_clipping', 'visual_presentation'].map(key => [key, 'PASS'])), blocking_findings: [], publication_authority: false, physical_gpu: 'unknown'};
  const visualPin = f.save('qa/synthetic-current-visual.json', independent), maker = {id: 'maker', task_id: 'maker-task'};
  const rendererSource = f.save('qa/synthetic-detail-renderer.py', Buffer.from('# Synthetic contract fixture only.'));
  const recipePin = f.save('qa/synthetic-detail-recipe.json', {source_glb_sha256:next.asset.sha256.glb,blender_version:'4.3.2',rendered_unchanged_source:true,files:[rendererSource]});
  const detailConfig = f.save('qa/synthetic-detail-config.json', {source_geometry_and_materials_unchanged:true,film_transparent:true,version:'4.3.2',renderer_sha256:rendererSource.sha256,resolution:[512,512]});
  const presentationPin = f.save('qa/synthetic-presentation.json', {schema_version: 1, kind: 'same-id-successor-presentation-v1', asset_id: next.id, maker, final_posters: {route: PRODUCTION_WHEEL_ROUTE, browser_capture: true, source_glb_sha256: next.asset.sha256.glb, recipe:recipePin,recipe_sha256:recipePin.sha256,blender_version:'4.3.2',detail: {...detailPin,render_config:detailConfig,camera_degrees:[42,23.3],source_glb_sha256:next.asset.sha256.glb,pixel_sha256:'c'.repeat(64)}, wheel: {...wheelPin, source_glb_sha256: next.asset.sha256.glb, render_config: capturePin, capture_report: reportPin, visual_review: visualPin, renderer_sha256: renderer.sha256, browser_version: renderer.browser, wheelSpec: spec}}, publication_authorized: false, reviewer_authority: false});
  const cardReport = {status: 'pass', target_renderer: 'threejs-modelstage', render_preset: CARD_RENDER_PRESET, render_preset_sha256: next.turntable.poster.render_preset_sha256, viewer_source_sha256: hashBytes(f.files.get('site/viewer.js') || readFileSync(join(root, 'site/viewer.js'))), chromium_version: renderer.browser, pinned_chromium_version: renderer.browser, gpu: {peakRequests: 1}, assets: [{id: next.id, source_glb_sha256: next.asset.sha256.glb, frames: 1, frame_bytes_total: 0, poster_bytes: next.turntable.poster.bytes}], reproducibility: {checked: 1, mismatches: []}};
  const rawCardPin = f.save('qa/synthetic-card-reproduction.json', cardReport);
  const cardPin = f.save('qa/synthetic-card-capture.json', {schema_version:1,kind:'same-id-current-card-capture-v1',report:rawCardPin,cards:[{id:next.id,path:next.turntable.poster.path,sha256:next.turntable.poster.sha256,bytes:next.turntable.poster.bytes}],publication_authorized:false,reviewer_authority:false});
  f.changeReview('azolla', review => { review.subject.next_record_sha256 = entry.next.sha256; review.changed_fields = successorChangedFields(old, next); review.evidence.preview_renderer = presentationPin; review.evidence.card_preview = cardPin; });
  f.selectionPin(); for (const [path, raw] of f.files) put(path, raw);
  const manifest = selectSuccessorManifest(f.options()), context = successorContext({manifest, read: f.read});
  assert.deepEqual(await verifySuccessorPresentation(root, context), ['azolla']);
  const projected = projectRegistryRelease(f.registry, manifest, {read: f.read}); assert.deepEqual(projected.manifest, manifest);
  assert.equal(publishedImagePaths(next.asset, manifest).poster, next.asset.card_preview);
  put('assets/turntables/index.json', Buffer.from(JSON.stringify({version: 1, render_preset_sha256: next.turntable.poster.render_preset_sha256, assets: [], posters: [next.turntable.poster]})));
  assert.equal((await collectTurntables({...manifest, assets: [next.asset]}, root)).posters.get('azolla'), next.asset.card_preview);
  const closure = successorSourceClosure(f.options()); for (const pin of [capturePin, reportPin, visualPin, cardPin]) assert(closure.includes(pin.path));
  const current = readFileSync(join(source, 'site/gallery-poster-inputs.mjs'), 'utf8');
  assert.equal(hashBytes(historicalPosterSource(current, 'site/gallery-poster-inputs.mjs')), baselineEvidence.poster_input_stripped_sha256.historical182);
  assert.equal(hashBytes(main842PosterSource(current)), baselineEvidence.poster_input_stripped_sha256.main842);
  const wrongCard = structuredClone(context); wrongCard.entries[0].next.turntable.poster.sha256 = 'd'.repeat(64);
  await assert.rejects(() => verifySuccessorPresentation(root, wrongCard), /exact selected WebP/);
  put(reportPin.path, Buffer.from('{}')); await assert.rejects(() => verifySuccessorPresentation(root, context), /bytes changed|hash changed/);
});

test('card capture wrapper refuses incomplete scope before browser launch or evidence writes', () => {
  const output = join(mkdtempSync(join(tmpdir(), 'successor-card-reject-')), 'not-created');
  const result = spawnSync(process.execPath, [new URL('./capture-same-id-cards.mjs', import.meta.url).pathname], {env: {...process.env, VERIFY_SHIPPED_PREVIEWS: '1', PREVIEW_POSTERS_ONLY: '1', PREVIEW_ASSET_IDS: 'azolla', PREVIEW_OUTPUT: output}, encoding: 'utf8'});
  assert.notEqual(result.status, 0); assert.match(result.stderr, /exact frozen fourteen/); assert(!existsSync(output));
});

test('waterfall public projection remains explicit, exact-subject and independently bound', () => {
  function projectedFixture(mutate = () => {}) {
    const f = fixture(), entry = f.selection.entries.find(row => row.id === 'waterfall-ledge'), next = JSON.parse(f.read(entry.next.path));
    const originalIdentity = {sha256: '138a41b0cda2de9f4682ff041a1a1688dbf7a2c097c8607eb4dd070f86a8a63a', bytes: 17762};
    const original = f.save('qa/waterfall-primary.json', {asset_id: next.id, decision: 'PASS', subject_glb_sha256: next.asset.sha256.glb, qa_inputs_sha256: originalIdentity.sha256});
    const omitted = [0, 1, 2].map(index => `/original_readonly_inputs/${index}/path`);
    const projection = {schema_version: 1, kind: 'waterfall-original-inputs-public-projection-v1', asset_id: next.id, original: originalIdentity, omitted_fields: omitted,
      document: {asset_id: next.id, revision: 'world-r002', subject_glb_sha256: next.asset.sha256.glb, decision: 'PENDING', original_readonly_inputs: [1, 2, 3].map(bytes => ({bytes, sha256: 'e'.repeat(64)})), inputs: Array.from({length: 70}, (_, i) => ({path: i === 69 ? 'candidate/lod0/waterfall-ledge/waterfall-ledge.blend' : `synthetic/${i}`, sha256: i === 69 ? next.asset.sha256.blend : 'd'.repeat(64)}))}};
    const proof = {schema_version: 1, kind: 'independent-waterfall-input-projection-review-v1', status: 'PASS', reviewer: {id: 'reviewer', task_id: 'reviewer-task'}, original: clone(originalIdentity), original_decision: original, glb_sha256: next.asset.sha256.glb, blend_sha256: next.asset.sha256.blend, omitted_fields: clone(omitted), checks: Object.fromEntries(['private_original_full_hash', 'original_decision_hash_chain', 'exact_three_location_omissions', 'all_other_fields_identical', 'candidate_source_byte_identity', 'private_original_preserved'].map(key => [key, 'PASS'])), blocking_findings: [], publication_authorized: false, reviewer_authority: false, world_accepted: false, physics_accepted: false};
    mutate(projection, proof);
    const auxiliary = f.save('qa/waterfall-public-projection.json', projection); proof.projection = auxiliary;
    const proofPin = f.save('qa/waterfall-public-projection-review.json', proof);
    f.changeReview(next.id, review => { for (const role of ['source_acceptance', 'technical']) review.evidence[role] = f.save(review.evidence[role].path, {schema_version: 1, kind: 'same-id-original-review-binding-v1', role, asset_id: next.id, report: original, glb_pointer: '/subject_glb_sha256', blend_pointer: '/inputs/69/sha256', decision_field: 'decision', blend_report: auxiliary, blend_report_sha256_pointer: '/qa_inputs_sha256', blend_projection_review: proofPin}); });
    return {f, auxiliary};
  }
  const {f} = projectedFixture(); assert.equal(selectSuccessorManifest(f.options()).assets.length, 18);
  for (const mutate of [
    (projection, proof) => { projection.original.sha256 = '0'.repeat(64); proof.original.sha256 = projection.original.sha256; },
    projection => { projection.omitted_fields.pop(); },
    projection => { projection.omitted_fields[0] = '/inputs/69/sha256'; },
    projection => { projection.document.original_readonly_inputs[0].path = 'not-actually-omitted'; },
    projection => { projection.document.inputs[69].sha256 = '0'.repeat(64); },
    projection => { projection.document.decision = 'PASS'; },
    (_projection, proof) => { proof.reviewer = {id: 'maker', task_id: 'maker-task'}; },
    (_projection, proof) => { proof.checks.all_other_fields_identical = 'PENDING'; },
    (_projection, proof) => { proof.world_accepted = true; }
  ]) { const {f} = projectedFixture(mutate); assert.throws(() => selectSuccessorManifest(f.options())); }
  const tamper = projectedFixture(); tamper.f.files.set(tamper.auxiliary.path, Buffer.from('{}')); assert.throws(() => selectSuccessorManifest(tamper.f.options()), /Successor size changed|Successor hash changed/);
});

/** Offline parity through the exact source checkout's real production delivery functions. */
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {mkdtemp, readdir, readFile, realpath, lstat, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve, join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {composeRegistry, digest, hashBytes} from './model-registry.mjs';
import {readRegistry, localReader, readLegacySnapshot} from './model-registry-cli.mjs';

export async function verifyRegistryDeliveryParity({root, registry, scratchRoot = tmpdir()}) {
  root = resolve(root); assert.equal(await realpath(root), root, 'Source root symlink rejected');
  const git = (...args) => execFileSync('git', args, {cwd: root, encoding: 'utf8', maxBuffer: 128 * 1024 * 1024}).trim();
  const sourceCommit = git('rev-parse', 'HEAD'); assert.equal(git('status', '--porcelain', '--untracked-files=no'), '', 'Parity needs unchanged tracked source');
  const {snapshot} = readLegacySnapshot(localReader(root)), projection = composeRegistry(registry);
  assert.deepEqual(projection, snapshot, 'Parity is for the exact existing source scope, not unreviewed additions');
  const load = async path => {
    const full = resolve(root, path); assert.equal(await realpath(full), full, 'Production module symlink rejected');
    assert.equal(hashBytes(await readFile(full)), hashBytes(execFileSync('git', ['show', `${sourceCommit}:${path}`], {cwd: root})), 'Production module differs from exact source commit');
    return import(pathToFileURL(full).href);
  };
  const {deliverManifestAssets} = await load('site/asset-delivery.mjs');
  const {deliverTurntables} = await load('site/turntable-delivery.mjs');
  const {writeCatalog} = await load('site/catalog-build.mjs');
  const output = await mkdtemp(join(resolve(scratchRoot), 'registry-delivery-parity-'));
  async function summarize(directory) {
    const records = [];
    async function visit(path = '') {
      for (const name of (await readdir(resolve(directory, path))).sort()) {
        const relative = path ? `${path}/${name}` : name, full = resolve(directory, relative), info = await lstat(full);
        assert(!info.isSymbolicLink(), 'Delivered symlink refused');
        if (info.isDirectory()) await visit(relative);
        else {
          assert(info.isFile()); const bytes = await readFile(full);
          const generatedJSON = relative === 'assets/manifest.json' || relative === 'assets/catalog.json' || /^assets\/catalog\/(?:details|shards)\//.test(relative);
          records.push({path: relative, bytes: bytes.length, sha256: hashBytes(bytes), ...(generatedJSON ? {semantic_sha256: digest(JSON.parse(bytes))} : {})});
        }
      }
    }
    await visit(); return records;
  }
  async function deliver(source, directory) {
    const enriched = await deliverTurntables(await deliverManifestAssets(source.manifest, directory, {root}), directory, {root});
    await writeCatalog(enriched, directory, {approvedOnly: true, catalogData: source.catalog});
    return {manifest: enriched, files: await summarize(directory)};
  }
  try {
    // Sequential passes keep only one real delivery tree on disk at a time.
    const legacyDir = join(output, 'legacy'), projectedDir = join(output, 'registry');
    const legacy = await deliver(snapshot, legacyDir); await rm(legacyDir, {recursive: true, force: true});
    const proposed = await deliver(projection, projectedDir);
    assert.deepEqual(proposed.manifest, legacy.manifest, 'Production-enriched manifest fields changed');
    assert.deepEqual(proposed.files.map(file => file.path), legacy.files.map(file => file.path), 'Delivered inventory changed');
    const serializationOnly = []; let exactFiles = 0, exactBytes = 0, derivedJSON = 0;
    for (let i = 0; i < legacy.files.length; i++) {
      const before = legacy.files[i], after = proposed.files[i];
      if (before.semantic_sha256) {
        derivedJSON++; assert.equal(after.semantic_sha256, before.semantic_sha256, `Derived production JSON changed: ${before.path}`);
        if (after.sha256 !== before.sha256) serializationOnly.push(before.path);
      } else { assert.equal(after.sha256, before.sha256, `Delivered asset/download bytes changed: ${before.path}`); assert.equal(after.bytes, before.bytes); exactFiles++; exactBytes += before.bytes; }
    }
    assert.equal(git('rev-parse', 'HEAD'), sourceCommit, 'Source head moved during parity'); assert.equal(git('status', '--porcelain', '--untracked-files=no'), '', 'Source changed during parity');
    return {version: 1, source_commit: sourceCommit, models: registry.records.length, production_enriched_manifest_equal: true, production_catalog_semantically_equal: true, generated_json_files_checked: derivedJSON,
      byte_identical_asset_and_download_files: exactFiles, byte_identical_asset_and_download_bytes: exactBytes, generated_json_serialization_only_differences: serializationOnly,
      source_bytes_modified: false, full_site_build_or_browser_qa_claimed: false, deployed: false};
  } finally { await rm(output, {recursive: true, force: true}); }
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    const [root, registryRoot] = process.argv.slice(2); assert(root && registryRoot && process.argv.length === 4, 'Usage: model-registry-delivery-parity.mjs SOURCE_ROOT REGISTRY_ROOT');
    console.log(JSON.stringify(await verifyRegistryDeliveryParity({root, registry: readRegistry(registryRoot)}), null, 2));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}

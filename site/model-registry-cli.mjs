/** Offline migration/composition only: never writes live aggregates or changes Git. */
import {immutableGitEnv} from './ci-git.mjs';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, realpathSync, renameSync, rmSync, writeFileSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createCatalog} from './catalog-build.mjs';
import {LEGACY_OUTPUTS, composeRegistry, createIntegrationPlan, digest, encode, hashBytes, importLegacySnapshot, recordReference, safePath} from './model-registry.mjs';

export function gitReader(repo, commit) {
  assert(/^[a-f0-9]{40}$/.test(commit), 'Use an exact 40-character commit, never a moving branch');
  const env = immutableGitEnv();
  assert.equal(execFileSync('git', ['rev-parse', `${commit}^{commit}`], {cwd: repo, env, encoding: 'utf8'}).trim(), commit);
  return path => {
    assert(safePath(path), `Unsafe Git path: ${path}`);
    const tree = execFileSync('git', ['ls-tree', '-z', commit, '--', path], {cwd: repo, env, encoding: 'utf8'});
    assert(tree.startsWith('100644 blob ') && tree.split('\0').filter(Boolean).length === 1 && tree.slice(0, -1).endsWith(`\t${path}`), `Not an exact regular Git file: ${path}`);
    return execFileSync('git', ['show', `${commit}:${path}`], {cwd: repo, env, maxBuffer: 128 * 1024 * 1024});
  };
}
export function localReader(root) {
  const base = realpathSync(root);
  return path => {
    assert(safePath(path), `Unsafe input path: ${path}`);
    const full = resolve(base, path);
    assert.equal(realpathSync(full), full, `Input symlink rejected: ${path}`);
    assert(lstatSync(full).isFile(), `Not a regular input: ${path}`);
    return readFileSync(full);
  };
}
export function readLegacySnapshot(read) {
  const sourcePins = {}, snapshot = {};
  for (const [key, path] of Object.entries(LEGACY_OUTPUTS)) { const bytes = read(path); sourcePins[key] = {path, sha256: hashBytes(bytes)}; snapshot[key] = JSON.parse(bytes); }
  return {snapshot, sourcePins};
}
/** Authenticate historical import labels against actual immutable Git objects.
 * This proves source provenance, not model quality or user publication approval. */
export function assertRegistryBaselineSource({root, registry, sourceCommit}) {
  assert(/^[a-f0-9]{40}$/.test(sourceCommit || ''), 'Exact current source commit required');
  const baselineCommit = registry?.baseline?.source_commit;
  const {snapshot, sourcePins} = readLegacySnapshot(gitReader(root, baselineCommit));
  execFileSync('git', ['merge-base', '--is-ancestor', baselineCommit, sourceCommit], {cwd: root, env: immutableGitEnv(), stdio: 'pipe'});
  assert.deepEqual(registry.baseline.source_pins, sourcePins, 'Baseline source pins differ from exact Git snapshot');
  const imported = importLegacySnapshot(snapshot, {sourceCommit: baselineCommit, sourcePins});
  assert.deepEqual(registry.baseline, imported.baseline, 'Baseline historical records or metadata differ from exact Git import');
  return {source_commit: baselineCommit, snapshot_sha256: imported.baseline.snapshot_sha256, provenance: 'verified-exact-git-import', publication_authority: false};
}
export function registryFiles(registry) {
  // Composition validates every reference before emitting anything.
  composeRegistry(registry);
  return new Map([
    ['registry/baseline.json', registry.baseline],
    ...registry.records.map(record => [recordReference(record).path, record]),
    ...registry.batches.map(batch => [`registry/batches/${batch.id}.json`, batch])
  ]);
}
export function readRegistry(root) {
  const read = localReader(root), baseline = JSON.parse(read('registry/baseline.json'));
  const dir = resolve(realpathSync(root), 'registry/batches');
  let batches = [];
  if (existsSync(dir)) {
    assert.equal(realpathSync(dir), dir, 'Batch directory symlink rejected');
    batches = readdirSync(dir).sort().map(name => {
      assert(/^[a-z0-9]+(?:-[a-z0-9]+)*\.json$/.test(name), `Unexpected batch file: ${name}`);
      const batch = JSON.parse(read(`registry/batches/${name}`));
      assert.equal(`${batch.id}.json`, name, 'Batch file owner mismatch'); return batch;
    });
  }
  const refs = [...baseline.records, ...batches.flatMap(batch => batch.records)];
  const selectedPaths = new Set(refs.map(ref => ref.path)), storedPaths = [];
  const base = realpathSync(root);
  function inventory(path) {
    const full = resolve(base, path), stat = lstatSync(full);
    assert(!stat.isSymbolicLink() && realpathSync(full) === full, `Registry inventory symlink rejected: ${path}`);
    if (stat.isDirectory()) {
      for (const name of readdirSync(full).sort()) inventory(`${path}/${name}`);
    } else {
      assert(stat.isFile() && /^registry\/models\/[a-z0-9]+(?:-[a-z0-9]+)*\/revisions\/[a-f0-9]{64}\/record\.json$/.test(path), `Unexpected model inventory file: ${path}`);
      assert(selectedPaths.has(path), `Unselected on-disk model record: ${path}`);
      storedPaths.push(path);
    }
  }
  inventory('registry/models');
  assert.deepEqual(storedPaths.sort(), [...selectedPaths].sort(), 'Selected model inventory differs from stored records');
  const records = refs.map(ref => {
    const bytes = read(ref.path), record = JSON.parse(bytes);
    assert.equal(digest(record), ref.sha256, `Record content digest mismatch: ${ref.path}`);
    assert.equal(hashBytes(bytes), ref.sha256, `Record must use canonical immutable bytes: ${ref.path}`); return record;
  });
  const registry = {baseline, batches, records}; composeRegistry(registry); return registry;
}
/** A fresh output tree only, atomically renamed after every file is ready. */
export function writeFreshTree(destination, files) {
  const target = resolve(destination), parent = dirname(target);
  assert(existsSync(parent), 'Output parent must already exist');
  assert.equal(realpathSync(parent), parent, 'Output parent symlink rejected');
  assert(!existsSync(target), `Refusing to replace existing output: ${target}`);
  const temp = `${target}.staging-${process.pid}`;
  mkdirSync(temp); // Never rm a pre-existing staging directory.
  try {
    for (const [path, value] of files) {
      assert(safePath(path), `Unsafe output path: ${path}`);
      const full = resolve(temp, path); mkdirSync(dirname(full), {recursive: true});
      writeFileSync(full, encode(value), {flag: 'wx'});
    }
    assert(!existsSync(target), 'Output appeared while preparing; refusing to replace it');
    renameSync(temp, target);
  } finally { rmSync(temp, {recursive: true, force: true}); }
}
export function composedFiles(registry) {
  const snapshot = composeRegistry(registry);
  const files = new Map(Object.entries(LEGACY_OUTPUTS).map(([key, path]) => [path, snapshot[key]]));
  const catalog = createCatalog(snapshot.manifest, {catalogData: snapshot.catalog});
  files.set('assets/catalog.json', catalog.index);
  for (const [path, value] of [...catalog.shards, ...catalog.details]) files.set(path, value);
  return files;
}
function args(argv) {
  const [command, ...rest] = argv, options = {};
  for (let i = 0; i < rest.length; i += 2) {
    assert(/^--[a-z-]+$/.test(rest[i]) && rest[i + 1] && !Object.hasOwn(options, rest[i].slice(2)), 'Expected unique --key value options');
    options[rest[i].slice(2)] = rest[i + 1];
  }
  return {command, options};
}
export function main(argv = process.argv.slice(2)) {
  const {command, options} = args(argv);
  if (command === 'import') {
    assert.deepEqual(Object.keys(options).sort(), ['commit', 'out', 'repo']);
    const {snapshot, sourcePins} = readLegacySnapshot(gitReader(options.repo, options.commit));
    const registry = importLegacySnapshot(snapshot, {sourceCommit: options.commit, sourcePins});
    writeFreshTree(options.out, registryFiles(registry));
    console.log(`Imported ${registry.records.length} immutable per-model records; legacy metadata round-trip verified. No asset bytes copied and no publication authority changed.`);
  } else if (command === 'compose') {
    assert.deepEqual(Object.keys(options).sort(), ['out', 'registry-root']);
    const registry = readRegistry(options['registry-root']); writeFreshTree(options.out, composedFiles(registry));
    console.log(`Composed ${registry.records.length} models into a new staging tree, including catalog/index/detail projections. Existing release gates still required.`);
  } else if (command === 'plan') {
    assert.deepEqual(Object.keys(options).sort(), ['head', 'next', 'out', 'previous']);
    const plan = createIntegrationPlan(readRegistry(options.previous), readRegistry(options.next), {expectedHead: options.head});
    writeFreshTree(options.out, new Map([['integration-plan.json', plan]]));
    console.log(`Prepared head-bound plan for ${plan.added_model_ids.length} additions. This does not merge, approve, or publish.`);
  } else throw new Error('Usage: model-registry-cli.mjs import --repo PATH --commit SHA --out NEW_DIR | compose --registry-root PATH --out NEW_DIR | plan --previous PATH --next PATH --head SHA --out NEW_DIR');
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try { main(); } catch (error) { console.error(error.message); process.exitCode = 1; }
}

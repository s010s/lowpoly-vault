/** Explicit, checksum-pinned mixed publication. Acceptance never grants publication authority. */
import assert from 'node:assert/strict';
import { readFile, realpath, stat, writeFile, rename } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { collectInitialRelease, INITIAL_ASSET_IDS } from './initial-release.mjs';
import { assetFileAllowlist } from './asset-delivery.mjs';
import { catalogMembership } from './curation.js';

import { REFINABLE_ASSET_IDS } from './refinable-asset-ids.mjs';
export { REFINABLE_ASSET_IDS };
export const INITIAL_PUBLICATION_SHA256 = '4043e9a35d43773660c2dee061b0e2ca0897aa430427e430d0ca5f331f967275';
const initialPin = {path:'assets/initial-publication.json', sha256:INITIAL_PUBLICATION_SHA256};
const runFile = promisify(execFile);
const candidateGate = fileURLToPath(new URL('../scripts/validate_candidate.py', import.meta.url));
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const hashPattern = /^[a-f0-9]{64}$/;
const slugPattern = /^[a-z0-9][a-z0-9._-]*$/;
const authorization = 'owner_requested_publication_of_accepted_revisions';

function exactKeys(value, keys, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label}: object required`);
  assert.deepEqual(Object.keys(value).sort(), [...keys].sort(), `${label}: missing or unknown fields`);
}
function nonempty(value, label) {
  assert(typeof value === 'string' && value.trim().length > 0 && !/[\u0000-\u001f]/.test(value), `${label}: nonempty single-line text required`);
}
function sourceURL(value, label) {
  nonempty(value, label);
  const url = new URL(value);
  assert(['https:', 'http:'].includes(url.protocol) && !url.username && !url.password, `${label}: public HTTP(S) source URL required`);
}
function safePath(path) {
  assert(typeof path === 'string' && !path.startsWith('/') && !/[\\\u0000-\u001f?#%:]/.test(path) &&
    path.split('/').every(part => part && part !== '.' && part !== '..'), 'Safe repository-relative path required');
}
async function checkedBytes(root, path, expectedHash) {
  safePath(path);
  assert.match(expectedHash || '', hashPattern, `${path}: fixed SHA-256 required`);
  const full = resolve(root, path);
  assert.equal(await realpath(full), full, `${path}: symlink substitutions are not allowed`);
  const info = await stat(full);
  assert(info.isFile() && info.size > 0, `${path}: nonempty file required`);
  const bytes = await readFile(full);
  assert.equal(sha(bytes), expectedHash, `${path}: SHA-256 mismatch (stale publication input)`);
  return bytes;
}
async function checkedJSON(root, pin, label) {
  exactKeys(pin, ['path', 'sha256'], label);
  return JSON.parse(await checkedBytes(root, pin.path, pin.sha256));
}
function checkMetadata(asset, entry, folder) {
  assert.equal(asset.id, entry.id, 'Release metadata belongs to another asset');
  assert.equal(asset.revision, entry.revision, `${entry.id}: metadata revision differs`);
  assert.equal(asset.author, entry.provenance.author, `${entry.id}: creator provenance differs`);
  assert.equal(asset.source_url, entry.provenance.source_url, `${entry.id}: source provenance differs`);
  for (const key of ['name', 'description']) for (const lang of ['en', 'zh']) nonempty(asset[key]?.[lang], `${entry.id}: bilingual ${key}.${lang}`);
  assert.equal(asset.license, 'CC-BY-4.0', `${entry.id}: asset license must remain CC-BY-4.0`);
  assert(Number.isSafeInteger(asset.triangles) && asset.triangles > 0, `${entry.id}: positive triangle count required`);
  assert(Array.isArray(asset.dimensions) && asset.dimensions.length === 3 && asset.dimensions.every(n => Number.isFinite(n) && n > 0), `${entry.id}: positive meter dimensions required`);
  const membership = catalogMembership(asset);
  assert(membership.worlds.length && membership.worlds.every(id => /^[a-z0-9-]+$/.test(id)), `${entry.id}: valid world required`);
  assert(typeof asset.category === 'string' && /^[a-z0-9-]+$/.test(asset.category), `${entry.id}: valid category required`);
  assert(membership.packs.every(id => /^[a-z0-9-]+$/.test(id)), `${entry.id}: valid packs required`);
  // Derived state, private QA paths and alternate file delivery routes cannot be supplied by metadata.
  for (const key of ['review_only', 'release_status', 'quality_status', 'publication', 'downloads', 'qa', 'candidate_record', 'turntable', 'card_preview', 'revision_provenance']) {
    assert(!Object.hasOwn(asset, key), `${entry.id}: reserved metadata field ${key}`);
  }
  assert.deepEqual(asset.sha256, entry.sha256, `${entry.id}: metadata file hashes differ from publication descriptor`);
  assetFileAllowlist({assets:[asset]});
  for (const key of ['glb', 'blend', 'preview']) {
    safePath(asset[key]);
    assert.equal(dirname(asset[key]), folder, `${entry.id}: released ${key} must stay in its immutable revision directory`);
  }
  assert.equal(asset.glb,`${folder}/${entry.id}.glb`,`${entry.id}: revision GLB basename must preserve catalog identity`);
  return membership;
}

export async function collectRefinedRelease(root = process.cwd(), descriptor) {
  const base = await realpath(resolve(root));
  exactKeys(descriptor, ['path', 'sha256'], 'Publication descriptor pin');
  assert(/^assets\/releases\/[a-z0-9][a-z0-9-]*\.json$/.test(descriptor.path), 'Publication descriptor must be under assets/releases/');
  const publication = await checkedJSON(base, descriptor, 'Publication descriptor pin');
  exactKeys(publication, ['version', 'release_id', 'release_status', 'authorization', 'authorized_on', 'initial_publication', 'approved_asset_ids', 'revisions'], 'Publication descriptor');
  assert.equal(publication.version, 1);
  assert.equal(publication.release_status, 'mixed');
  assert.equal(publication.authorization, authorization, 'Separate owner publication authorization required');
  assert.equal(descriptor.path, `assets/releases/${publication.release_id}.json`, 'Publication release ID must match descriptor filename');
  assert(typeof publication.authorized_on === 'string' && /^\d{4}-\d\d-\d\dT.*(?:Z|[+-]\d\d:\d\d)$/.test(publication.authorized_on) && Number.isFinite(Date.parse(publication.authorized_on)), 'Publication authorization needs an ISO timestamp with timezone');
  assert.deepEqual(publication.initial_publication, initialPin, 'The original initial-publication approval is immutable');
  await checkedJSON(base, initialPin, 'Original publication pin');
  assert(Array.isArray(publication.approved_asset_ids) && publication.approved_asset_ids.length > 0 &&
    publication.approved_asset_ids.every(id => REFINABLE_ASSET_IDS.includes(id)) &&
    new Set(publication.approved_asset_ids).size === publication.approved_asset_ids.length, 'Only explicitly approved, unique refinement IDs may be replaced');
  assert(Array.isArray(publication.revisions), 'Explicit revision entries required');
  assert.deepEqual(publication.revisions.map(entry => entry.id).sort(), [...publication.approved_asset_ids].sort(), 'Revision entries must exactly match approved IDs without duplicates');

  // Recheck ALL ten originals, including those being replaced in the catalog. Nothing mutates them.
  // release-metadata.json is intentionally not discovered by the legacy metadata.json scanner.
  const initial = await collectInitialRelease(base);
  const replacements = new Map();
  for (const entry of publication.revisions) {
    exactKeys(entry, ['id', 'revision', 'metadata', 'candidate_root', 'candidate', 'sha256', 'provenance'], 'Revision entry');
    assert(typeof entry.revision === 'string' && slugPattern.test(entry.revision), `${entry.id}: safe immutable revision required`);
    exactKeys(entry.sha256, ['glb', 'blend', 'preview'], 'Revision file hashes');
    for (const key of ['glb', 'blend', 'preview']) assert.match(entry.sha256[key] || '', hashPattern, `${entry.id}: fixed ${key} SHA-256 required`);
    exactKeys(entry.provenance, ['author', 'source_url', 'changes'], 'Revision provenance');
    nonempty(entry.provenance.author, 'Revision creator');
    sourceURL(entry.provenance.source_url, 'Revision source');
    nonempty(entry.provenance.changes, 'Revision change statement');
    const folder = `assets/revisions/${entry.id}/${entry.revision}`;
    assert.equal(entry.metadata?.path, `${folder}/release-metadata.json`, `${entry.id}: immutable release-metadata.json path required`);
    const asset = await checkedJSON(base, entry.metadata, 'Release metadata pin');
    const membership = checkMetadata(asset, entry, folder);
    // Frozen briefs may use an asset-local bundle root. Never rewrite those paths to publish.
    if (entry.candidate_root !== '.') safePath(entry.candidate_root);
    const candidateRoot = resolve(base, entry.candidate_root);
    assert.equal(await realpath(candidateRoot), candidateRoot, `${entry.id}: candidate_root symlinks are not allowed`);
    assert((await stat(candidateRoot)).isDirectory(), `${entry.id}: candidate_root must be a directory`);
    await checkedJSON(candidateRoot, entry.candidate, 'Candidate record pin');
    for (const key of ['glb', 'blend', 'preview']) await checkedBytes(base, asset[key], entry.sha256[key]);
    let validation;
    try {
      const {stdout} = await runFile('python3', [candidateGate, entry.candidate.path, '--root', candidateRoot, '--require-approved', '--json'], {maxBuffer:2 * 1024 * 1024});
      validation = JSON.parse(stdout);
    } catch (error) {
      throw new Error(`${entry.id}: candidate evidence gate refused mixed release: ${error.stdout || error.stderr || error.message}`);
    }
    assert(validation.valid && validation.approved_for_brief && validation.profile === 'production', `${entry.id}: approved production brief required`);
    assert.equal(validation.asset_id, entry.id, `${entry.id}: candidate record belongs to another asset`);
    assert.equal(validation.revision, entry.revision, `${entry.id}: candidate revision differs`);
    assert.equal(validation.subject?.glb_sha256, entry.sha256.glb, `${entry.id}: candidate approves different GLB bytes`);
    assert.equal(validation.artifact_sha256?.source, entry.sha256.blend, `${entry.id}: candidate approves different editable source bytes`);
    assert(validation.approved_visual_image_sha256?.includes(entry.sha256.preview), `${entry.id}: published preview is absent from approved visual evidence`);
    assert.equal(validation.measurements?.triangles, asset.triangles, `${entry.id}: published triangle count differs from measured candidate`);
    const original = initial.assets.find(item => item.id === entry.id);
    replacements.set(entry.id, {...asset, ...membership, collection:asset.collection || membership.worlds[0], quality_status:'accepted_for_brief',
      revision_provenance:{...entry.provenance, original_author:original.author || initial.author, original_source_url:initial.attribution_url, original_glb_sha256:original.sha256.glb}});
  }
  const assets = initial.assets.map(asset => replacements.get(asset.id) || asset);
  assert.deepEqual(assets.map(asset => asset.id).sort(), INITIAL_ASSET_IDS, 'The mixed catalog must retain exactly the original ten unique IDs');
  assetFileAllowlist({assets});
  return {...initial, release_status:'mixed', quality_status:'mixed', publication:{
    authorization, authorized_on:publication.authorized_on, release_id:publication.release_id, descriptor:{...descriptor}, initial_publication:{...initialPin},
    approved_asset_ids:[...publication.approved_asset_ids].sort(), work_in_progress_asset_ids:assets.filter(asset => asset.quality_status === 'work_in_progress').map(asset => asset.id).sort()
  }, assets};
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    const args = process.argv.slice(2), descriptorPath = args[0];
    assert(args[1] === '--sha256' && hashPattern.test(args[2] || '') && (args.length === 3 || (args.length === 4 && args[3] === '--check')),
      'Usage: node site/refined-release.mjs assets/releases/<release-id>.json --sha256 <approved-descriptor-sha256> [--check]');
    const manifest = await collectRefinedRelease(process.cwd(), {path:descriptorPath, sha256:args[2]});
    if (!args.includes('--check')) {
      const destination = resolve('assets/manifest.json'), temp = `${destination}.tmp`;
      await writeFile(temp, JSON.stringify(manifest, null, 2) + '\n', {flag:'wx'});
      await rename(temp, destination);
    }
    console.log(`Mixed publication checked: ${manifest.publication.approved_asset_ids.length} individually accepted revisions; ${manifest.publication.work_in_progress_asset_ids.length} unchanged WIP originals.${args.includes('--check') ? ' No file was written.' : ''}`);
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}

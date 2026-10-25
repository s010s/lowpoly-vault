/** Exact fourteen current-source card reproduction. Invokes the existing renderer;
 * never manufactures acceptance from a supplied or historical report.
 */
import assert from 'node:assert/strict';
import {readFileSync, writeFileSync, existsSync} from 'node:fs';
import {resolve, relative} from 'node:path';
import {spawnSync} from 'node:child_process';
import {MESH_SUCCESSOR_IDS, successorReader} from './same-id-successors.mjs';
import {hashBytes, safePath} from './model-registry.mjs';
const root = process.cwd(), captureRoot = resolve(process.env.GALLERY_DIR || 'dist'), output = resolve(process.env.PREVIEW_OUTPUT || 'qa/same-id-card-output');
assert.equal(process.env.VERIFY_SHIPPED_PREVIEWS, '1', 'Exact shipped reproduction is mandatory');
assert.equal(process.env.PREVIEW_POSTERS_ONLY, '1', 'Successors are static cards only');
assert.deepEqual((process.env.PREVIEW_ASSET_IDS || '').split(',').sort(), [...MESH_SUCCESSOR_IDS].sort(), 'Capture only the exact frozen fourteen');
assert(!existsSync(output), 'Use a fresh card verification output directory');
assert(safePath(relative(root, output)), 'Evidence output must be repository relative');
const captureRead = successorReader(captureRoot), manifest = JSON.parse(captureRead('assets/manifest.json'));
const selected = MESH_SUCCESSOR_IDS.map(id => { const assets = manifest.assets.filter(row => row.id === id); assert.equal(assets.length, 1); const a = assets[0]; assert.equal(hashBytes(captureRead(a.glb)), a.sha256.glb); return {id, glb: a.glb, glb_sha256: a.sha256.glb}; });
const result = spawnSync(process.execPath, ['site/render-web-previews.mjs'], {cwd: root, env: {...process.env, PREVIEW_OUTPUT: output, GALLERY_DIR: captureRoot}, stdio: 'inherit'});
assert.equal(result.status, 0, 'Actual pinned card reproduction subprocess failed');
const read = successorReader(root), reportPath = relative(root, resolve(output, 'render-report.json')), reportBytes = read(reportPath), report = JSON.parse(reportBytes), index = JSON.parse(read(relative(root, resolve(output, 'assets/turntables/index.json'))));
assert.equal(report.status, 'pass'); assert.deepEqual(report.assets.map(row => row.id).sort(), [...MESH_SUCCESSOR_IDS].sort());
assert.equal(report.reproducibility?.checked, 14); assert.deepEqual(report.reproducibility.mismatches, []);
const cards = selected.map(a => {
  assert.equal(hashBytes(captureRead(a.glb)), a.glb_sha256, 'Capture input changed during reproduction');
  const rows = index.posters.filter(row => row.id === a.id); assert.equal(rows.length, 1); const row = rows[0];
  assert.equal(row.source_glb_sha256, a.glb_sha256); assert.equal(report.assets.find(r => r.id === a.id).source_glb_sha256, a.glb_sha256);
  const bytes = read(relative(root, resolve(output, row.path))); assert.equal(bytes.length, row.bytes); assert.equal(hashBytes(bytes), row.sha256);
  assert.equal(hashBytes(captureRead(row.path)), row.sha256, 'Shipped card changed during reproduction');
  return {id: a.id, path: row.path, sha256: row.sha256, bytes: row.bytes};
});
const receipt = {schema_version: 1, kind: 'same-id-current-card-capture-v1', report: {path: reportPath, sha256: hashBytes(reportBytes), bytes: reportBytes.length}, cards, publication_authorized: false, reviewer_authority: false};
writeFileSync(resolve(output, 'same-id-card-capture.json'), JSON.stringify(receipt, null, 2) + '\n', {flag: 'wx'});
console.log(JSON.stringify({status: 'EXACT_FOURTEEN_CARD_REPRODUCTION_RECORDED', receipt: relative(root, resolve(output, 'same-id-card-capture.json')), publication_authorized: false}));

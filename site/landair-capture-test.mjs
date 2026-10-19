/** Candidate capture and export must not relax or mutate the publication contract. */
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve, join, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { prepareLandairCapture } from './prepare-landair-capture.mjs';
import { LANDAIR_CAPTURE as fixed } from './accepted-landair-capture.mjs';
import { QUARTETS_CAPTURE as marine } from './accepted-quartets-capture.mjs';

const scratch = await mkdtemp(join(tmpdir(), 'lpv-candidate-capture-'));
const path = 'qa/landair-release-20261019/capture-inputs.json';
const published = await readFile('assets/manifest.json');
const exporter = resolve('site/export-captured-posters.mjs');
const captureRoot = join(scratch, 'export');
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
let checks = 0;

async function fixture(contract) {
  const report = { status: 'pass', chromium_version: 'fixture', pinned_chromium_version: 'fixture', assets: [] };
  const index = { posters: [] };
  for (const entry of contract.assets) {
    const bytes = Buffer.from(`isolated capture export fixture: ${entry.id}`);
    const path = `assets/turntables/${entry.id}.png`;
    await mkdir(dirname(resolve(captureRoot, path)), { recursive: true });
    await writeFile(resolve(captureRoot, path), bytes);
    report.assets.push({ id: entry.id, source_glb_sha256: entry.glb.sha256 });
    index.posters.push({ id: entry.id, path, bytes: bytes.length, sha256: sha(bytes), source_glb_sha256: entry.glb.sha256 });
  }
  return { report, index, ids: contract.assets.map(entry => entry.id) };
}

async function exportCapture(value) {
  await writeFile(join(captureRoot, 'render-report.json'), JSON.stringify(value.report));
  await writeFile(join(captureRoot, 'assets/turntables/index.json'), JSON.stringify(value.index));
  const run = spawnSync(process.execPath, [exporter], {
    cwd: scratch,
    env: { ...process.env, PREVIEW_OUTPUT: captureRoot, PREVIEW_ASSET_IDS: value.ids.join(',') },
    encoding: 'utf8', timeout: 30000, maxBuffer: 1024 * 1024,
  });
  assert.ifError(run.error);
  assert.equal(run.signal, null);
  checks++;
  return run;
}

try {
  await mkdir(dirname(resolve(scratch, path)), { recursive: true });
  for (const change of [
    d => { d.publication_authority = true; },
    d => { d.assets.pop(); },
    d => { d.assets.push(d.assets[0]); },
    d => { d.assets[0].glb.path = '../escape'; },
    d => { d.assets[0].glb.sha256 = '0'.repeat(64); },
    d => { d.review.sha256 = '0'.repeat(64); },
    d => { d.delivery_review.sha256 = '0'.repeat(64); },
  ]) {
    const descriptor = structuredClone(fixed);
    change(descriptor);
    await writeFile(resolve(scratch, path), JSON.stringify(descriptor));
    await assert.rejects(() => prepareLandairCapture({ root: scratch, outDir: resolve(scratch, 'capture') }));
    checks++;
  }

  for (const contract of [marine, fixed]) {
    const valid = await fixture(contract);
    const run = await exportCapture(valid);
    assert.equal(run.status, 0, run.stderr);
    assert.equal(run.stdout.split('\n').filter(line => line.startsWith('PUBLICATION_CAPTURE_FILE ')).length, 4);
    const exported = JSON.parse(run.stdout.split('\n').find(line => line.startsWith('PUBLICATION_CAPTURE_REPORT ')).slice('PUBLICATION_CAPTURE_REPORT '.length));
    assert.equal(exported.capture_only, true);
    assert.deepEqual(exported.report, valid.report);
    assert.deepEqual(exported.index, valid.index);
    for (const [label, change] of [
      ['report failure', d => { d.report.status = 'fail'; }],
      ['unpinned Chromium', d => { d.report.chromium_version = 'different'; }],
      ['missing report asset', d => { d.report.assets.pop(); }],
      ['missing poster', d => { d.index.posters.pop(); }],
      ['duplicate IDs', d => { d.ids[1] = d.ids[0]; }],
      ['unknown quartet', d => { d.ids = ['unreviewed-a', 'unreviewed-b', 'unreviewed-c', 'unreviewed-d']; }],
      ['mixed quartet', d => { d.ids = [fixed.assets[0].id, marine.assets[0].id, marine.assets[1].id, marine.assets[2].id]; }],
      ...contract.assets.flatMap((entry, i) => [
        [`${entry.id}: report source changed`, d => { d.report.assets[i].source_glb_sha256 = '0'.repeat(64); }],
        [`${entry.id}: poster source changed`, d => { d.index.posters[i].source_glb_sha256 = '0'.repeat(64); }],
        [`${entry.id}: missing source binding`, d => { delete d.index.posters[i].source_glb_sha256; }],
      ]),
    ]) {
      const value = structuredClone(valid);
      change(value);
      const rejected = await exportCapture(value);
      assert.notEqual(rejected.status, 0, `${label}: capture export must fail closed`);
      assert(!rejected.stdout.includes('PUBLICATION_CAPTURE_FILE '), `${label}: no poster is exported before scope/source validation`);
    }
    for (const [label, change] of [
      ['changed poster digest', d => { d.index.posters[0].sha256 = '0'.repeat(64); }],
      ['changed poster length', d => { d.index.posters[0].bytes++; }],
    ]) {
      const value = structuredClone(valid);
      change(value);
      assert.notEqual((await exportCapture(value)).status, 0, `${label}: exported bytes must match evidence`);
    }
  }
  assert.deepEqual(await readFile('assets/manifest.json'), published);
  console.log(`Candidate capture: ${checks} checks passed; authority/scope/source mutations rejected, exact marine and land/air exports bound to frozen GLBs, publication unchanged.`);
} finally {
  await rm(scratch, { recursive: true, force: true });
}

/** Actual runtime capture only. Never mutates original candidate records or approval. */
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile, writeFile, mkdir, realpath} from 'node:fs/promises';
import {resolve, sep} from 'node:path';
import {preflight, PREFIX, LAUNCH_ARGS, sha256, readLocal, checkMeasurement, makePendingReport} from './contract.mjs';

// Finish every input/event/source check before importing or launching a browser.
const root = process.cwd();
const {input, files, provenance} = await preflight(root);
const {chromium} = await import('playwright');
const out = resolve(root, 'qa/ci-recovery-two-runtime');
await mkdir(resolve(root, 'qa'), {recursive: true});
await mkdir(out); // Refuse stale output reuse.
const writeJson = async (path, data) => writeFile(resolve(out, path), JSON.stringify(data, null, 2) + '\n', {flag: 'wx'});
const receipt = {schema_version: 1, kind: 'two-candidate-runtime-capture', measured_status: 'running', formal_acceptance: 'BLOCKED', independent_pixel_review: 'pending', physical_gpu_verified: false, external_target_scene_verified: false, started_at: new Date().toISOString(), provenance, limitations: input.limitations, errors: [], warnings: [], captures: [], stages: []};
const pageSource = await readLocal(root, `${PREFIX}/page.mjs`);
const moduleRoot = await realpath(resolve(root, 'node_modules/three'));
const html = '<!doctype html><html><head><meta charset="utf-8"><link rel="icon" href="data:,"><style>html,body{margin:0;background:#e8e4dc}canvas{display:block}</style><script type="importmap">{"imports":{"three":"/modules/build/three.module.js"}}</script></head><body></body></html>';
const server = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://127.0.0.1');
    assert.equal(req.method, 'GET');
    assert.equal(url.search, '');
    const path = decodeURIComponent(url.pathname);
    assert(!path.includes('\\') && !path.includes('\0'));
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    if (path === '/') { res.setHeader('Content-Type', 'text/html'); res.end(html); return; }
    if (path === '/page.mjs') { res.setHeader('Content-Type', 'text/javascript'); res.end(pageSource); return; }
    const model = /^\/models\/([a-z]+)\.glb$/.exec(path);
    if (model && files.has(model[1])) { res.setHeader('Content-Type', 'model/gltf-binary'); res.end(files.get(model[1])); return; }
    assert(/^\/modules\/[a-zA-Z0-9_./-]+\.js$/.test(path));
    const relative = path.slice('/modules/'.length);
    assert(relative.split('/').every(s => s && s !== '..' && s !== '.'));
    const file = resolve(moduleRoot, relative);
    assert(file.startsWith(moduleRoot + sep));
    assert.equal(await realpath(file), file);
    res.setHeader('Content-Type', 'text/javascript');
    res.end(await readFile(file));
  } catch (error) {
    receipt.errors.push(`HTTP resource rejected: ${req.url}: ${error.message}`);
    res.writeHead(404).end();
  }
});
let browser;
const evidence = [];
try {
  const threePackage = JSON.parse(await readFile(resolve(moduleRoot, 'package.json')));
  const playwrightPackage = JSON.parse(await readLocal(root, 'node_modules/playwright/package.json'));
  const browsers = JSON.parse(await readLocal(root, 'node_modules/playwright-core/browsers.json'));
  assert.equal(threePackage.version, input.toolchain.three);
  assert.equal(playwrightPackage.version, input.toolchain.playwright);
  assert.equal(browsers.browsers.find(b => b.name === 'chromium').browserVersion, input.toolchain.chromium);
  receipt.installed_toolchain = {three: threePackage.version, playwright: playwrightPackage.version, browsers_json_sha256: sha256(await readLocal(root, 'node_modules/playwright-core/browsers.json')), launch_args: LAUNCH_ARGS};
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  browser = await chromium.launch({headless: true, args: LAUNCH_ARGS});
  assert.equal(browser.version(), input.toolchain.chromium);
  receipt.browser = browser.version();
  async function capture(items, view, prefix, stage) {
    const width = stage === 'scene' ? 1280 : 768, height = stage === 'scene' ? 720 : 768;
    const page = await browser.newPage({viewport: {width, height}, deviceScaleFactor: 1, reducedMotion: 'reduce', serviceWorkers: 'block'});
    page.setDefaultTimeout(60000);
    const errors = [], warnings = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('requestfailed', request => errors.push(`requestfailed: ${request.url()}: ${request.failure()?.errorText}`));
    page.on('response', response => { if (response.status() >= 400) errors.push(`HTTP ${response.status()}: ${response.url()}`); });
    page.on('console', message => {
      if (message.type() === 'error') errors.push(message.text());
      if (message.type() === 'warning') warnings.push(message.text());
    });
    await page.route('**/*', route => new URL(route.request().url()).origin === origin ? route.continue() : route.abort('blockedbyclient'));
    try {
      await page.goto(origin + '/', {waitUntil: 'networkidle'});
      const measured = await page.evaluate(async args => (await import('/page.mjs')).renderFrame(args), {items, view, browserVersion: browser.version(), width, height, gap: input.scene.gap_m});
      checkMeasurement(measured, items, browser.version());
      assert.deepEqual(errors, [], 'Browser errors');
      const path = `${prefix}-${view}.png`;
      const bytes = await page.locator('canvas').screenshot({type: 'png'});
      assert.equal(bytes.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
      assert.deepEqual([bytes.readUInt32BE(16), bytes.readUInt32BE(20)], [width, height]);
      assert.deepEqual(errors, [], 'Capture errors');
      await writeFile(resolve(out, path), bytes, {flag: 'wx'});
      const shot = {path, bytes: bytes.length, sha256: sha256(bytes), width, height};
      measured.screenshot = shot;
      measured.errors = errors;
      measured.warnings = warnings;
      receipt.captures.push({stage, assets: items.map(i => i.id), view, screenshot: shot, measured});
      receipt.warnings.push(...warnings.map(warning => ({capture: path, warning})));
      console.log(`Measured and captured ${path}: ${measured.runtime.draw_calls} calls, ${measured.runtime.triangles} triangles, ${measured.foreground_pixels} non-background pixels.`);
      return measured;
    } finally { await page.close(); }
  }
  async function writeStage(item, stage, frames) {
    const images = frames.map(frame => ({id: `${item.id}-${stage}-${frame.view}`, kind: 'rendered_image', stage, subject: item.subject, ...frame.screenshot}));
    const report = makePendingReport({item, stage, frames, images, provenance, scene: input.scene, warnings: [...new Set(frames.flatMap(f => f.warnings))]});
    const path = `${item.id}-${stage}-report.json`;
    const reportBytes = Buffer.from(JSON.stringify(report, null, 2) + '\n');
    await writeFile(resolve(out, path), reportBytes, {flag: 'wx'});
    const reportEvidence = {id: `${item.id}-${stage}-report`, kind: `${stage}_report`, stage, subject: item.subject, path, bytes: reportBytes.length, sha256: sha256(reportBytes)};
    evidence.push(...images, reportEvidence);
    receipt.stages.push({asset_id: item.id, stage, measured_status: 'pass', formal_status: 'unknown', report: reportEvidence});
    return {status: 'unknown', subject: item.subject, note: 'Actual software-WebGL measurements captured. Independent actual-pixel review, warning rationale and frozen-brief coverage decision are pending; not a candidate approval.', evidence: [...images.map(e => e.id), reportEvidence.id], inspected_references: [], criteria: [{id: item.criteria[stage], status: 'unknown', note: 'Independent acceptance decision pending.', evidence: [...images.map(e => e.id), reportEvidence.id]}]};
  }
  const pending = new Map(input.items.map(item => [item.id, {asset_id: item.id, subject: item.subject, stages: {}}]));
  for (const item of input.items) {
    const frames = [];
    for (const view of input.gpu_views) frames.push(await capture([item], view, `${item.id}-gpu`, 'gpu'));
    pending.get(item.id).stages.gpu = await writeStage(item, 'gpu', frames);
  }
  const sceneFrames = [];
  for (const view of input.scene.views) sceneFrames.push(await capture(input.items, view, 'two-candidate-scene', 'scene'));
  for (const item of input.items) pending.get(item.id).stages.scene = await writeStage(item, 'scene', sceneFrames);
  assert.equal(receipt.captures.length, 18);
  assert.equal(receipt.stages.length, 4);
  assert.deepEqual(receipt.errors, []);
  await writeJson('evidence-index.json', {schema_version: 1, kind: 'runtime-evidence-index', provenance, evidence});
  await writeJson('pending-stage-handoff.json', {schema_version: 1, kind: 'not-an-approval-additive-handoff', provenance, candidates: [...pending.values()], independent_review: 'pending', formal_acceptance: 'BLOCKED', instructions: 'Verify exact run/commit/input/recipe and all output digests. Inspect all actual PNG pixels. Decide software-WebGL and representative-scene coverage against unchanged frozen briefs. Supply real reviewer identity, reviewed_at, reviewed_evidence and warning rationales in new separately authored reports/stage records only after review. Do not mutate original preserved reports or assume a CI green check approves release.'});
  receipt.measured_status = 'pass';
} catch (error) {
  receipt.measured_status = 'fail';
  receipt.errors.push(error.stack ?? String(error));
  process.exitCode = 1;
  console.error(error);
} finally {
  receipt.finished_at = new Date().toISOString();
  await writeJson('capture-receipt.json', receipt);
  await browser?.close();
  if (server.listening) await new Promise(resolve => server.close(resolve));
}

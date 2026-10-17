/** Real browser regression coverage for image-to-GLB continuity and interrupted navigation. */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import assert from 'node:assert/strict';

const root = resolve(process.env.GALLERY_DIR || 'dist');
const output = resolve(process.env.QA_OUTPUT_DIR || 'qa/handoff-continuity');
const prefix = '/lowpoly-vault/';
const report = { status: 'running', commit: process.env.GITHUB_SHA || null, checks: [], cases: [], page_errors: [], screenshots: [], videos: [], note: 'Chromium software rendering and emulated viewport sizes; no physical-device performance claim.' };
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.webp': 'image/webp', '.png': 'image/png', '.glb': 'model/gltf-binary' };
const server = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    if (!url.pathname.startsWith(prefix)) throw new Error('Wrong site root');
    let path = resolve(root, decodeURIComponent(url.pathname.slice(prefix.length)) || 'index.html');
    if (path !== root && !path.startsWith(root + sep)) throw new Error('Outside site root');
    if ((await stat(path)).isDirectory()) path = resolve(path, 'index.html');
    const bytes = await readFile(path);
    res.writeHead(200, { 'Content-Type': mime[extname(path)] || 'application/octet-stream', 'Content-Length': bytes.length }).end(bytes);
  } catch { res.writeHead(404).end(); }
});

let browser, base, current;
const requests = [];
async function makeContext(label, options = {}) {
  const viewport = options.viewport || { width: 1440, height: 1000 };
  const context = await browser.newContext({ viewport, reducedMotion: 'no-preference', recordVideo: { dir: output, size: viewport }, ...options });
  const page = await context.newPage(); current = page;
  page.on('pageerror', error => report.page_errors.push({ label, error: error.message }));
  page.on('request', request => requests.push({ label, url: request.url(), time: Date.now() }));
  return { page, async close() { const video = page.video(); await context.close(); if (video) report.videos.push({ label, file: (await video.path()).split(/[\\/]/).at(-1) }); } };
}
async function screenshot(page, name) {
  await page.screenshot({ path: resolve(output, name + '.png'), fullPage: true });
  report.screenshots.push(name + '.png');
}
async function catalog(page) {
  await page.goto(base + prefix + 'models/');
  await page.waitForFunction(() => document.querySelector('#grid')?.getAttribute('aria-busy') === 'false');
}
async function ready(page, id) {
  await page.waitForFunction(id => {
    const host = document.querySelector('#canvas-host');
    return document.querySelector('#viewer-dialog')?.open && host?.dataset.modelState === 'ready' && host.dataset.presentedUrl?.endsWith('/' + id + '.glb') && Number(host.dataset.renderTriangles) > 0;
  }, id, { timeout: 30000 });
}
async function angles(page) { return page.locator('#canvas-host').evaluate(host => ({ azimuth: Number(host.dataset.viewAzimuth), elevation: Number(host.dataset.viewElevation), distance: Number(host.dataset.viewDistance) })); }
const deltaAngle = (a, b) => Math.abs(((a - b + 540) % 360) - 180);
async function startSampler(page) {
  await page.evaluate(() => {
    window.__handoffReview = { phase: 'open', frames: [] };
    const visible = element => {
      if (!element || !element.isConnected) return false;
      const box = element.getBoundingClientRect();
      if (box.width < 1 || box.height < 1) return false;
      if (getComputedStyle(element).visibility === 'hidden') return false;
      for (let node = element; node && node !== document.body; node = node.parentElement) {
        const css = getComputedStyle(node);
        if (css.display === 'none' || Number(css.opacity) <= 0.001) return false;
      }
      return element.tagName !== 'IMG' || element.naturalWidth > 0;
    };
    const sample = () => {
      const host = document.querySelector('#canvas-host'), flight = document.querySelector('.stage-flight');
      if (document.querySelector('#viewer-dialog')?.open) {
        const stationaryVisible = [...host.querySelectorAll('canvas,img')].some(visible);
        const hasVisual = stationaryVisible || visible(flight);
        const entry = { phase: window.__handoffReview.phase, hasVisual, stationaryVisible, state: host.dataset.modelState };
        if (flight && visible(flight)) {
          const r = flight.getBoundingClientRect(), iw = flight.naturalWidth || flight.width, ih = flight.naturalHeight || flight.height;
          const contentScale = Math.min(r.width / iw, r.height / ih);
          entry.flight = { square: Math.min(iw, ih) * contentScale, x: r.x + r.width / 2, y: r.y + r.height / 2, width: iw, height: ih };
        }
        window.__handoffReview.frames.push(entry);
      }
      window.__handoffReviewRAF = requestAnimationFrame(sample);
    };
    sample();
  });
}
async function endSampler(page) {
  return page.evaluate(() => { cancelAnimationFrame(window.__handoffReviewRAF); return window.__handoffReview.frames; });
}

async function directDetails() {
  const context = await makeContext('direct-auto-load'); const { page } = context;
  try {
    const url = base + prefix + 'models/natural-arch/';
    await page.goto(url); await ready(page, 'natural-arch');
    assert.equal(page.url(), url, 'Direct enhancement keeps its canonical URL');
    await page.reload(); await ready(page, 'natural-arch');
    assert(requests.some(request => request.label === 'direct-auto-load' && request.url.endsWith('/natural-arch.glb')));
    await page.locator('#close').click(); await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open);
    await page.waitForURL(base + prefix + 'models/');
    assert(await page.locator('#catalog-page').isVisible(), 'Closing a direct route returns to the model catalog');
    report.checks.push('Direct detail URL and reload automatically load the real GLB without an Explore in 3D click.');
  } finally { await context.close(); }
}

async function roundTrip(label, options = {}) {
  const context = await makeContext(label, options); const { page } = context;
  try {
    await catalog(page);
    const card = page.locator('#grid .asset-card[data-id="natural-arch"]');
    await card.scrollIntoViewIfNeeded(); await card.focus(); await page.keyboard.press('Home');
    for (let i = 0; i < 7; i++) await page.keyboard.press('ArrowRight');
    await page.waitForFunction(() => document.querySelector('#grid [data-id="natural-arch"]').dataset.scrubFrame === '7');
    await page.evaluate(() => { window.__originalReviewCard = document.querySelector('#grid [data-id="natural-arch"]'); });
    await page.route('**/*.glb', async route => { await new Promise(resolve => setTimeout(resolve, 450)); await route.continue().catch(() => {}); });
    await startSampler(page);
    await page.keyboard.press('Enter'); await ready(page, 'natural-arch');
    const initial = await angles(page);
    assert(deltaAngle(initial.azimuth, 147) < 0.001, 'The 7/24 preview angle enters actual 3D unchanged');
    await page.waitForTimeout(350);
    await page.locator('#canvas-host').focus(); await page.keyboard.press('ArrowRight'); await page.keyboard.press('ArrowUp');
    await page.waitForFunction(previous => Math.abs(Number(document.querySelector('#canvas-host').dataset.viewAzimuth) - previous) > 0.1, initial.azimuth);
    await page.locator('#zoom-in').click();
    await page.waitForFunction(previous => Number(document.querySelector('#canvas-host').dataset.viewDistance) < previous * 0.99, initial.distance);
    const beforeClose = await angles(page);
    await screenshot(page, label + '-detail-before-close');
    await page.evaluate(() => { window.__handoffReview.phase = 'close'; });
    await page.locator('#close').click(); await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open);
    await page.waitForTimeout(150);
    assert(await card.evaluate(node => node === window.__originalReviewCard), 'Same-list close keeps the original card DOM');
    assert.equal(await card.locator('.image-scrub-canvas').count(), 1, 'The returned card retains the actual current detail image');
    const returned = await card.locator('.image-scrub-canvas').evaluate(node => {
      const r = node.getBoundingClientRect(); return { square: Math.min(r.width, r.height), x: r.x + r.width / 2, y: r.y + r.height / 2 };
    });
    assert.equal(await page.evaluate(() => document.activeElement?.dataset.id), 'natural-arch');
    await screenshot(page, label + '-retained-card');
    await page.evaluate(() => { window.__handoffReview.phase = 'reopen'; });
    await page.keyboard.press('Enter'); await ready(page, 'natural-arch'); await page.waitForTimeout(350);
    const reopened = await angles(page);
    assert(deltaAngle(beforeClose.azimuth, reopened.azimuth) < 0.001, 'Close/reopen preserves the actual camera azimuth');
    assert(Math.abs(beforeClose.elevation - reopened.elevation) < 0.001, 'Close/reopen preserves the actual camera elevation');
    assert(Number.isFinite(beforeClose.distance) && Math.abs(beforeClose.distance - reopened.distance) < 0.00001, 'Close/reopen preserves the actual camera zoom distance');
    const frames = await endSampler(page), closeFlights = frames.filter(frame => frame.phase === 'close' && frame.flight);
    assert.equal(frames.filter(frame => !frame.hasVisual).length, 0, 'Open/close/reopen must never show an empty visual frame');
    if (options.reducedMotion !== 'reduce') {
      assert(closeFlights.length > 1, 'The ordinary-motion reverse transition must actually animate');
      assert.equal(frames.filter(frame => frame.flight && frame.stationaryVisible).length, 0, 'A flying model must not duplicate a stationary model behind it');
      const last = closeFlights.at(-1).flight;
      assert(Math.abs(last.square / returned.square - 1) < 0.12, 'Reverse-flight model scale must match the retained card at completion');
      assert(Math.hypot(last.x - returned.x, last.y - returned.y) < 12, 'Reverse-flight center must match the retained card');
    }
    report.cases.push({ label, beforeClose, reopened, returned, frames });
    report.checks.push(`${label}: rotated preview, real 3D, current-angle close/reopen, no blank frame, and reverse-flight scale continuity.`);
  } finally { await context.close(); }
}

async function interruptedHistory() {
  const context = await makeContext('interrupted-history'); const { page } = context;
  try {
    await page.goto(base + prefix); await page.locator('.primary-nav [data-route="catalog"]').click();
    await page.waitForFunction(() => document.querySelector('#grid')?.getAttribute('aria-busy') === 'false');
    const card = page.locator('#grid .asset-card[data-id="natural-arch"]');
    await card.scrollIntoViewIfNeeded(); await card.click(); await ready(page, 'natural-arch'); await page.waitForTimeout(350);
    await page.evaluate(() => { history.back(); setTimeout(() => history.back(), 35); });
    await page.waitForURL(base + prefix);
    await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open, null, { timeout: 5000 });
    assert(await page.locator('#home-page').isVisible());
    assert.equal(await page.locator('.stage-flight').count(), 0);
    assert.equal(await page.evaluate(() => window.__vaultGPU.liveScenes), 0);
    report.checks.push('Two rapid Back actions during reverse animation leave no open dialog, stale flight, or live GLB scene.');
  } finally { await context.close(); }
}

async function supersededImport() {
  const context = await makeContext('superseded-same-id-import', { reducedMotion: 'reduce' }); const { page } = context;
  let releaseImport;
  const gate = new Promise(resolve => { releaseImport = resolve; });
  try {
    await page.route('**/viewer-*.js', async route => { await gate; await route.continue().catch(() => {}); });
    await catalog(page);
    await page.locator('#grid .asset-card[data-id="natural-arch"]').click();
    await page.waitForFunction(() => document.querySelector('#viewer-dialog')?.open);
    await page.evaluate(() => history.back());
    await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open && location.pathname.endsWith('/models/'));
    await page.evaluate(() => history.forward());
    await page.waitForFunction(() => document.querySelector('#viewer-dialog')?.open && location.pathname.endsWith('/natural-arch/'));
    // Dynamic import is deliberately non-abortable. Both route changes must arrive
    // while the Forward route still awaits it, reproducing the same-ID stale guard.
    await page.evaluate(() => { history.back(); setTimeout(() => history.forward(), 35); });
    await page.waitForTimeout(140); releaseImport();
    await ready(page, 'natural-arch');
    assert.equal(await page.locator('#canvas-host .model-canvas').count(), 1);
    assert.equal(await page.evaluate(() => window.__vaultGPU.liveScenes), 1);
    report.checks.push('Back/Forward during a delayed viewer import retries the final same-ID selection instead of leaving its aborted request pending.');
  } finally { releaseImport(); await context.close(); }
}

try {
  await mkdir(output, { recursive: true }); await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  base = `http://127.0.0.1:${server.address().port}`;
  browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  report.chromium_version = browser.version();
  await directDetails();
  await roundTrip('desktop-motion');
  await roundTrip('mobile-motion', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await roundTrip('desktop-reduced-motion', { reducedMotion: 'reduce' });
  await interruptedHistory();
  await supersededImport();
  assert.deepEqual(report.page_errors, []); report.status = 'pass';
  console.log(JSON.stringify({ status: report.status, checks: report.checks }, null, 2));
} catch (error) {
  report.status = 'fail'; report.error = error.stack; process.exitCode = 1; console.error(error);
  try { if (current && !current.isClosed()) await screenshot(current, 'failure'); } catch {}
} finally {
  report.requests = requests; await browser?.close();
  if (server.listening) await new Promise(resolve => server.close(resolve));
  await mkdir(output, { recursive: true }); await writeFile(resolve(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
}

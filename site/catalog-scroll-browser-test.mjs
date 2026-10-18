/** Native scrolling + stationary catalog geometry through real-model details. */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import assert from 'node:assert/strict';
const root = resolve(process.env.GALLERY_DIR || 'dist');
const output = resolve(process.env.QA_OUTPUT_DIR || 'qa/catalog-scroll');
const prefix = '/lowpoly-vault/';
const report = { cases: [], page_errors: [], limitations: ['Linux Chromium/SwiftShader; mobile/touch and overlay modes are emulated, not physical Safari, Windows or macOS acceptance. Overlay flags are recorded with measured geometry, not assumed effective.'] };
const server = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    if (!url.pathname.startsWith(prefix)) throw Error('Wrong root');
    let file = resolve(root, decodeURIComponent(url.pathname.slice(prefix.length)) || 'index.html');
    if (file !== root && !file.startsWith(root + sep)) throw Error('Outside root');
    if ((await stat(file)).isDirectory()) file = resolve(file, 'index.html');
    res.setHeader('Content-Type', { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.webp': 'image/webp', '.glb': 'model/gltf-binary' }[extname(file)] || 'application/octet-stream');
    res.end(await readFile(file));
  } catch { res.writeHead(404).end(); }
});
let browser, base;
async function listing(page, path = 'models/') {
  const url=new URL(path,base+prefix);if(!url.search)url.searchParams.set('pack','prehistoric-starter');
  await page.goto(url.href);
  await page.waitForFunction(() => document.querySelector('#grid')?.ariaBusy === 'false');
  await page.waitForFunction(() => document.querySelector('.catalog-scroll-cue'));
}
const cueVisible = page => page.locator('.catalog-scroll-cue').isVisible();
async function ready(page) {
  await page.waitForFunction(() => document.querySelector('#viewer-dialog')?.open && document.querySelector('#canvas-host')?.dataset.modelState === 'ready' && !document.querySelector('.stage-flight'));
}
async function closed(page) {
  await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open && !document.querySelector('.stage-flight'));
  await page.waitForFunction(() => document.querySelector('#grid').ariaBusy === 'false');
}
async function geometry(page) {
  return page.evaluate(() => {
    const rect = selector => { const r = document.querySelector(selector).getBoundingClientRect(); return { x: r.x, width: r.width }; };
    return { width: innerWidth, scrollY, root: rect('html'), header: rect('.topbar'), grid: rect('#grid'), cue: !document.querySelector('.catalog-scroll-cue').hidden };
  });
}
async function scrollbarProbe(page) {
  return page.evaluate(() => {
    const probe = document.createElement('div');
    probe.style.cssText = 'position:fixed;width:100px;height:100px;overflow:scroll;visibility:hidden';
    document.body.append(probe); const width = probe.offsetWidth - probe.clientWidth; probe.remove(); return width;
  });
}
async function arm(page) {
  await page.evaluate(() => {
    window.__catalogScrollSampling = true; window.__catalogScrollFrames = [];
    function tick() {
      const rect = selector => { const r = document.querySelector(selector).getBoundingClientRect(); return { x: r.x, width: r.width }; };
      window.__catalogScrollFrames.push({ time: performance.now(), scrollY, root: rect('html'), header: rect('.topbar'), grid: rect('#grid'), open: document.querySelector('#viewer-dialog').open });
      if (window.__catalogScrollSampling) requestAnimationFrame(tick);
    }
    tick();
  });
}
async function finishSamples(page, result, before) {
  result.frames = await page.evaluate(() => { window.__catalogScrollSampling = false; return window.__catalogScrollFrames; });
  assert(result.frames.some(frame => frame.open), 'Samples include the open detail');
  const deviations = result.frames.flatMap(frame => ['root', 'header', 'grid'].flatMap(key => ['x', 'width'].map(axis => Math.abs(frame[key][axis] - before[key][axis]))));
  result.maximum_horizontal_shift_px = Math.max(...deviations);
  assert(result.maximum_horizontal_shift_px <= .5, 'Background and flight coordinates must never reflow horizontally');
  assert(Math.abs((await geometry(page)).scrollY - before.scrollY) <= 1, 'Catalog scroll position is restored');
}
async function roundtrip(page, result, method = 'button') {
  const card = page.locator('#grid [data-id="natural-arch"]');
  await card.scrollIntoViewIfNeeded(); await page.mouse.move(1, 1);
  const r = await card.locator('.asset-image').boundingBox();
  const before = await geometry(page); await arm(page);
  await page.mouse.click(r.x + r.width / 2, r.y + r.height / 2);
  await ready(page); assert.equal(await cueVisible(page), false, 'Catalog cue is absent under details');
  assert.notEqual(await page.locator('#viewer-dialog').evaluate(el => getComputedStyle(el).scrollbarWidth), 'none', 'Detail scrollbar stays available');
  if (method === 'escape') await page.keyboard.press('Escape');
  else if (method === 'backdrop') await page.mouse.click(2, 2);
  else if (method === 'back') await page.goBack();
  else await page.locator('#close').click();
  await closed(page); await finishSamples(page, result, before);
  assert.equal(await page.locator('[data-detail-origin],.stage-flight').count(), 0, 'No stranded source or flight');
}
async function test(name, fn, options = {}) {
  const result = { name }; report.cases.push(result);
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, ...options });
  const page = await context.newPage(); page.on('pageerror', error => report.page_errors.push({ name, error: error.message }));
  try { await listing(page); await fn(page, result, context); result.pass = true; }
  catch (error) { result.pass = false; result.error = error.stack; await page.screenshot({ path: resolve(output, name + '-failure.png') }).catch(() => {}); }
  finally { await context.close(); console.log(`${result.pass ? 'PASS' : 'FAIL'} ${name}${result.error ? '\n' + result.error : ''}`); }
}
async function launch(overlay = false) {
  return chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, ignoreDefaultArgs: ['--hide-scrollbars'], args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--disable-gpu-rasterization', overlay ? '--enable-features=OverlayScrollbar,OverlayScrollbars' : '--disable-features=OverlayScrollbar,OverlayScrollbars'] });
}
try {
  await mkdir(output, { recursive: true }); await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  base = `http://127.0.0.1:${server.address().port}`; browser = await launch(); report.browser = browser.version();
  await test('native-scroll-and-cue', async (page, result) => {
    result.initial = await geometry(page); assert(await cueVisible(page));
    result.native_scrollbar_width_px = await scrollbarProbe(page);
    assert.equal(await page.locator('html').evaluate(el => getComputedStyle(el).scrollbarWidth), 'none');
    assert.equal(result.initial.root.width, result.initial.width, 'No invisible reserved gutter on catalog');
    assert.equal(await page.locator('.catalog-scroll-cue').evaluate(el => getComputedStyle(el).pointerEvents), 'none');
    await page.mouse.move(8, 650); await page.mouse.wheel(0, 350); await page.waitForFunction(() => scrollY > 0);
    result.wheel_scroll_y = await page.evaluate(() => scrollY);
    await page.keyboard.press('End'); await page.waitForFunction(() => document.querySelector('.catalog-scroll-cue').hidden);
    result.bottom = await geometry(page); assert(result.bottom.scrollY > 0);
    await page.keyboard.press('Home'); await page.waitForFunction(() => scrollY === 0 && !document.querySelector('.catalog-scroll-cue').hidden);
    await page.screenshot({ path: resolve(output, '01-catalog-cue.png') });
  });
  for (const method of ['button', 'escape', 'backdrop', 'back']) await test(`stationary-roundtrip-${method}`, (page, result) => roundtrip(page, result, method));
  await test('repeated-open-close-and-history', async (page, result) => {
    result.roundtrips = [];
    for (let i = 0; i < 3; i++) { const round = {}; result.roundtrips.push(round); await roundtrip(page, round, i % 2 ? 'escape' : 'button'); }
    await page.goForward(); await ready(page); assert.equal(await cueVisible(page), false);
    await page.goBack(); await closed(page); assert(await page.locator('html').evaluate(el => el.hasAttribute('data-catalog-scroll')));
  });
  await test('short-filter-and-resize', async (page, result) => {
    await page.setViewportSize({ width: 1440, height: 1400 });
    await page.locator('#filters [data-category="wood"]').click();
    await page.waitForFunction(() => document.querySelector('#grid').ariaBusy === 'false' && document.documentElement.scrollHeight <= innerHeight);
    await page.waitForFunction(() => document.querySelector('.catalog-scroll-cue').hidden); result.short = await geometry(page);
    await page.setViewportSize({ width: 390, height: 320 });
    await page.waitForFunction(() => !document.querySelector('.catalog-scroll-cue').hidden);
    await page.setViewportSize({ width: 1440, height: 1400 });
    await page.waitForFunction(() => document.querySelector('.catalog-scroll-cue').hidden);
    await page.locator('#filters [data-category="all"]').click();
    await page.setViewportSize({ width: 1440, height: 700 });
    await page.waitForFunction(() => document.querySelector('#grid').ariaBusy === 'false' && !document.querySelector('.catalog-scroll-cue').hidden);
    result.restored = await geometry(page);
  });
  await test('localized-dark-reduced-motion', async (page, result) => {
    await listing(page, 'zh-CN/models/');
    assert.equal(await page.locator('.catalog-scroll-cue').textContent(), '向下浏览 ↓');
    assert.equal(await page.locator('.catalog-scroll-cue').evaluate(el => el.getAnimations({ subtree: true }).length), 0);
    await page.screenshot({ path: resolve(output, '02-dark-chinese-cue.png') });
    await roundtrip(page, result);
  }, { colorScheme: 'dark', reducedMotion: 'reduce' });
  await test('mobile-touch-and-orientation', async (page, result, context) => {
    const cdp = await context.newCDPSession(page);
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: 8, y: 700 }] });
    for (let y = 650; y >= 250; y -= 50) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: 8, y }] }); await page.waitForTimeout(20); }
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await page.waitForFunction(() => scrollY > 0); await page.waitForTimeout(300); result.touch_scroll_y = await page.evaluate(() => scrollY);
    await page.keyboard.press('Home'); await page.waitForFunction(() => scrollY === 0);
    await roundtrip(page, result, 'escape');
    await page.setViewportSize({ width: 844, height: 390 });
    await page.waitForFunction(() => document.documentElement.scrollWidth <= innerWidth);
    result.landscape = await geometry(page);
    await page.screenshot({ path: resolve(output, '03-mobile-landscape.png') });
  }, { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await test('scope-and-home-modal', async (page, result) => {
    await page.locator('.primary-nav [data-route="home"]').click();
    await page.waitForFunction(() => !document.documentElement.hasAttribute('data-catalog-scroll'));
    assert.equal(await cueVisible(page), false);
    result.home_scrollbar = await page.locator('html').evaluate(el => ({ width: getComputedStyle(el).scrollbarWidth, gutter: getComputedStyle(el).scrollbarGutter, measured_gutter_px: innerWidth - el.getBoundingClientRect().width }));
    assert.equal(result.home_scrollbar.width, 'auto');
    const before = await geometry(page); await arm(page); await page.locator('#hero-inspect').click(); await ready(page);
    await page.locator('#close').click(); await closed(page); await finishSamples(page, result, before);
    assert.equal(await cueVisible(page), false);
  });
  await browser.close(); browser = await launch(true);
  report.overlay_requested_flags = ['OverlayScrollbar', 'OverlayScrollbars'];
  await test('overlay-requested-roundtrip', async (page, result) => { result.initial = await geometry(page); result.native_scrollbar_width_px = await scrollbarProbe(page); await roundtrip(page, result); });
  report.pass = report.cases.every(result => result.pass) && report.page_errors.length === 0;
  assert(report.pass, 'See catalog-scroll report for failed checks');
} finally {
  if (browser) await browser.close(); await new Promise(resolve => server.close(resolve));
  await writeFile(resolve(output, 'report.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ pass: report.pass, cases: report.cases.map(({ name, pass }) => ({ name, pass })), output }, null, 2));
}

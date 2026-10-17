/** Real browser regression coverage for shared-model card/detail continuity and interrupted navigation. */
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
  const before = await previewDiagnostics(page);
  await page.screenshot({ path: resolve(output, name + '.png'), fullPage: false });
  const after = await previewDiagnostics(page);
  (report.screenshot_states ||= []).push({ name, before, after });
  report.screenshots.push(name + '.png');
  assert.equal(after.viewport.width, before.viewport.width, 'Evidence capture must not resize the tested viewport');
  assert.equal(after.viewport.height, before.viewport.height, 'Evidence capture must not resize the tested viewport');
  assert(Math.abs(after.scroll.y - before.scroll.y) < 1, 'Evidence capture must not scroll away from the retained card');
  assert.equal(after.preview?.activeId, before.preview?.activeId, 'Evidence capture must not stop the active model preview');
}
async function previewDiagnostics(page) {
  return page.evaluate(() => {
    const card = document.querySelector('#grid [data-id="natural-arch"]'), r = card?.getBoundingClientRect(), host = document.querySelector('#canvas-host');
    return {
      url: location.href, scroll: { x: scrollX, y: scrollY }, viewport: { width: innerWidth, height: innerHeight },
      focusedId: document.activeElement?.dataset.id || null, focusedElement: document.activeElement?.id || document.activeElement?.tagName,
      preview: window.__vaultPreview ? { ...window.__vaultPreview } : null,
      gpu: window.__vaultGPU ? { ...window.__vaultGPU } : null,
      card: card ? { state: card.dataset.previewState, frame: window.__vaultPreview?.activeId === card.dataset.id ? window.__vaultPreview.frame : null, azimuth: card.dataset.previewAzimuth, canvases: card.querySelectorAll('canvas').length, rect: { x: r.x, y: r.y, width: r.width, height: r.height }, inView: r.bottom > 0 && r.top < innerHeight } : null,
      detail: host ? { state: host.dataset.modelState, presentedUrl: host.dataset.presentedUrl, azimuth: host.dataset.viewAzimuth, elevation: host.dataset.viewElevation, distance: host.dataset.viewDistance } : null,
    };
  });
}
async function canvasPixels(page, selector) {
  return page.locator(selector).evaluate(canvas => {
    // A WebGL context cannot also supply a 2D context. Read its synchronously
    // copied draw, captured before the non-preserved drawing buffer clears.
    if (canvas.classList.contains('model-canvas')) {
      const signature = window.__handoffReview?.pixelSignatures.get(canvas);
      if (!signature) throw new Error('The actual card draw must be captured synchronously');
      return signature;
    }
    const bytes = canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data;
    let hash = 2166136261, transparent = 0;
    for (let i = 0; i < bytes.length; i++) { hash = Math.imul(hash ^ bytes[i], 16777619) >>> 0; if (i % 4 === 3 && bytes[i] <= 3) transparent++; }
    const corners = [3, (canvas.width - 1) * 4 + 3, ((canvas.height - 1) * canvas.width) * 4 + 3, bytes.length - 1].map(i => bytes[i]);
    return { width: canvas.width, height: canvas.height, rgba_hash: hash.toString(16).padStart(8, '0'), transparent_fraction: transparent / (bytes.length / 4), corner_alpha_max: Math.max(...corners) };
  });
}
async function pixelParity(page, label, caseReport) {
  // Capture the actual browser-composited WebGL pixels. Avoid full-page captures,
  // which change mobile layout and trigger intentional offscreen preview cleanup.
  const screenshotName = label + '-actual-detail-pixels.png';
  const canvas = page.locator('#canvas-host .model-canvas');
  await canvas.scrollIntoViewIfNeeded();
  const bounds = await canvas.boundingBox(), dpr = await page.evaluate(() => devicePixelRatio);
  // Locator screenshots round fractional bounds outward. That includes a pixel
  // of the adjacent dark metadata column on macOS, which is not model geometry.
  // Keep the screenshot inside the canvas; trim less than one device pixel per
  // edge, with no model mask and the same strict color/bounds/centroid checks.
  const x = Math.ceil(bounds.x * dpr) / dpr, y = Math.ceil(bounds.y * dpr) / dpr;
  const clip = { x, y, width: Math.floor((bounds.x + bounds.width) * dpr) / dpr - x,
    height: Math.floor((bounds.y + bounds.height) * dpr) / dpr - y };
  assert(clip.width > 0 && clip.height > 0);
  caseReport.pixel_capture = { bounds, clip, deviceScaleFactor: dpr };
  const png = await page.screenshot({ path: resolve(output, screenshotName), type: 'png', clip });
  report.screenshots.push(screenshotName);
  const result = await page.evaluate(async ({ png, prefix }) => {
    const size = 320;
    const load = async src => { const image = new Image(); image.src = src; await image.decode(); return image; };
    const catalog = await (await fetch(prefix + 'assets/catalog.json')).json();
    let asset = catalog.initial.find(asset => asset.id === 'natural-arch');
    if (!asset) for (const shard of catalog.shards) { const items = (await (await fetch(prefix + shard.path)).json()).items; asset = items.find(asset => asset.id === 'natural-arch'); if (asset) break; }
    if (!asset?.turntable?.manifest) throw new Error('Natural Arch must advertise its exact versioned turntable descriptor');
    const manifest = await (await fetch(prefix + asset.turntable.manifest)).json();
    const referencePath = manifest.frames[7].path;
    const [actualImage, expectedImage] = await Promise.all([load('data:image/png;base64,' + png), load(prefix + referencePath)]);
    const host = document.querySelector('#canvas-host'), layers = [];
    for (let node = host; node; node = node.parentElement) layers.push(getComputedStyle(node).backgroundColor);
    const backgroundCanvas = document.createElement('canvas'); backgroundCanvas.width = backgroundCanvas.height = 1;
    const backgroundContext = backgroundCanvas.getContext('2d'); backgroundContext.fillStyle = '#fff'; backgroundContext.fillRect(0, 0, 1, 1);
    for (const color of layers.reverse()) { backgroundContext.fillStyle = color; backgroundContext.fillRect(0, 0, 1, 1); }
    const stageRGB = backgroundContext.getImageData(0, 0, 1, 1).data;
    const stageBackground = 'rgb(' + stageRGB[0] + ',' + stageRGB[1] + ',' + stageRGB[2] + ')';
    const normalize = (image, composite = true) => {
      const canvas = document.createElement('canvas'); canvas.width = canvas.height = size;
      const side = Math.min(image.naturalWidth, image.naturalHeight), context = canvas.getContext('2d');
      if (composite) { context.fillStyle = stageBackground; context.fillRect(0, 0, size, size); }
      context.drawImage(image, (image.naturalWidth - side) / 2, (image.naturalHeight - side) / 2, side, side, 0, 0, size, size);
      return { canvas, pixels: context.getImageData(0, 0, size, size).data };
    };
    const actual = normalize(actualImage), expected = normalize(expectedImage), background = [...expected.pixels.slice(0, 3)];
    const rawReference = normalize(expectedImage, false), alphaBytes = rawReference.pixels.filter((_, i) => i % 4 === 3);
    const referenceAlpha = { transparent_fraction: alphaBytes.filter(a => a <= 3).length / alphaBytes.length,
      corner_alpha_max: Math.max(rawReference.pixels[3], rawReference.pixels[(size - 1) * 4 + 3], rawReference.pixels[((size - 1) * size) * 4 + 3], rawReference.pixels.at(-1)) };
    const foreground = pixels => {
      let left = size, right = -1, top = size, bottom = -1, count = 0, sx = 0, sy = 0;
      for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
        const i = (y * size + x) * 4;
        if (Math.max(...background.map((value, c) => Math.abs(pixels[i + c] - value))) <= 12) continue;
        left = Math.min(left, x); right = Math.max(right, x); top = Math.min(top, y); bottom = Math.max(bottom, y); count++; sx += x; sy += y;
      }
      return { bbox: { left, top, right, bottom }, centroid: { x: sx / count, y: sy / count }, pixels: count };
    };
    let error = 0;
    for (let i = 0; i < actual.pixels.length; i += 4) for (let c = 0; c < 3; c++) error += Math.abs(actual.pixels[i + c] - expected.pixels[i + c]);
    const actualForeground = foreground(actual.pixels), expectedForeground = foreground(expected.pixels);
    const bboxDelta = Math.max(...Object.keys(actualForeground.bbox).map(key => Math.abs(actualForeground.bbox[key] - expectedForeground.bbox[key])));
    const centroidDelta = Math.hypot(actualForeground.centroid.x - expectedForeground.centroid.x, actualForeground.centroid.y - expectedForeground.centroid.y);
    return { descriptorPath: asset.turntable.manifest, referencePath, referenceDimensions: [expectedImage.naturalWidth, expectedImage.naturalHeight], normalizedSize: size, mean_rgb_absolute_error: error / (size * size * 3 * 255), bbox_delta_px: bboxDelta, centroid_delta_px: centroidDelta, actualForeground, expectedForeground, background, stageBackground, referenceAlpha, liveAlpha: window.__handoffReview.latestLiveAlpha,
      theme: document.documentElement.dataset.theme || 'system', actual_png: actual.canvas.toDataURL('image/png'), expected_png: expected.canvas.toDataURL('image/png'), reference_alpha_png: rawReference.canvas.toDataURL('image/png') };
  }, { png: png.toString('base64'), prefix });
  const { actual_png, expected_png, reference_alpha_png, ...measurements } = result;
  caseReport.pixel_parity = measurements;
  await writeFile(resolve(output, label + '-normalized-detail.png'), Buffer.from(actual_png.split(',')[1], 'base64'));
  await writeFile(resolve(output, label + '-reference-frame007.png'), Buffer.from(expected_png.split(',')[1], 'base64'));
  await writeFile(resolve(output, label + '-reference-alpha.png'), Buffer.from(reference_alpha_png.split(',')[1], 'base64'));
  report.screenshots.push(label + '-normalized-detail.png', label + '-reference-frame007.png', label + '-reference-alpha.png');
  assert.deepEqual(measurements.referenceDimensions, [768, 768], 'Parity must use the current 768 px proxy, resolved through its catalog descriptor');
  assert(measurements.referenceAlpha.transparent_fraction > 0.2 && measurements.referenceAlpha.corner_alpha_max <= 3, 'Versioned turntable image must have a genuinely transparent background');
  assert(measurements.liveAlpha?.transparent_fraction > 0.2 && measurements.liveAlpha.corner_alpha_max <= 3, 'Real WebGL rendering must preserve transparent background pixels');
  assert(measurements.actualForeground.pixels > 100 && measurements.expectedForeground.pixels > 100, 'Pixel checks require a real model silhouette');
  assert(measurements.mean_rgb_absolute_error < 0.04, 'Actual detail pixels must match the card-frame lighting and framing within a cross-GPU tolerance');
  assert(measurements.bbox_delta_px <= 8, 'The actual model silhouette bounds must match the card frame within 8 pixels');
  assert(measurements.centroid_delta_px <= 8, 'The actual model silhouette center must match the card frame within 8 pixels');
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
    window.__handoffReview = { phase: 'preview', frames: [], draws: [], probe_errors: [], pixelSignatures: new WeakMap() };
    const alphaCache = new WeakMap(), sampleCanvas = document.createElement('canvas');
    const rectOf = element => { const r = element.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height }; };
    const readAlpha = source => {
      const sw = source.naturalWidth || source.width, sh = source.naturalHeight || source.height;
      if (!sw || !sh) return null;
      const ratio = Math.min(1, 384 / Math.max(sw, sh));
      sampleCanvas.width = Math.max(1, Math.round(sw * ratio)); sampleCanvas.height = Math.max(1, Math.round(sh * ratio));
      const width = sampleCanvas.width, height = sampleCanvas.height, context = sampleCanvas.getContext('2d', { willReadFrequently: true });
      context.clearRect(0, 0, width, height); context.drawImage(source, 0, 0, width, height);
      const pixels = context.getImageData(0, 0, width, height).data;
      let left = width, right = -1, top = height, bottom = -1, count = 0, transparent = 0, weight = 0, cx = 0, cy = 0;
      for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
        const alpha = pixels[(y * width + x) * 4 + 3];
        if (alpha <= 3) transparent++;
        if (alpha <= 16) continue;
        left = Math.min(left, x); right = Math.max(right, x); top = Math.min(top, y); bottom = Math.max(bottom, y); count++; weight += alpha; cx += (x + 0.5) * alpha; cy += (y + 0.5) * alpha;
      }
      return { source: [sw, sh], sampled: [width, height], pixels: count, transparent_fraction: transparent / (width * height),
        corner_alpha_max: Math.max(pixels[3], pixels[(width - 1) * 4 + 3], pixels[((height - 1) * width) * 4 + 3], pixels.at(-1)),
        bbox: count ? { left: left / width, top: top / height, right: (right + 1) / width, bottom: (bottom + 1) / height } : null,
        centroid: count ? { x: cx / weight / width, y: cy / weight / height } : null };
    };
    const alphaFor = element => {
      if (!element) return null;
      if (!alphaCache.has(element) && !element.classList.contains('model-canvas')) alphaCache.set(element, readAlpha(element));
      return alphaCache.get(element) || null;
    };
    const pixelSignature = source => {
      // Match ModelStage.snapshot's bounded copy without retaining another GLB,
      // renderer, or scene. These are the actual current WebGL draw's pixels.
      const scale = Math.min(1, 1024 / Math.max(source.width, source.height));
      const canvas = document.createElement('canvas');
      canvas.width = Math.round(source.width * scale); canvas.height = Math.round(source.height * scale);
      const context = canvas.getContext('2d', { willReadFrequently: true });
      context.drawImage(source, 0, 0, canvas.width, canvas.height);
      const bytes = context.getImageData(0, 0, canvas.width, canvas.height).data;
      let hash = 2166136261, transparent = 0;
      for (let i = 0; i < bytes.length; i++) { hash = Math.imul(hash ^ bytes[i], 16777619) >>> 0; if (i % 4 === 3 && bytes[i] <= 3) transparent++; }
      const corners = [3, (canvas.width - 1) * 4 + 3, ((canvas.height - 1) * canvas.width) * 4 + 3, bytes.length - 1].map(i => bytes[i]);
      return { width: canvas.width, height: canvas.height, rgba_hash: hash.toString(16).padStart(8, '0'), transparent_fraction: transparent / (bytes.length / 4), corner_alpha_max: Math.max(...corners) };
    };
    const projected = (element, alpha) => {
      if (!element || !alpha?.bbox) return null;
      const r = rectOf(element), css = getComputedStyle(element), [iw, ih] = alpha.source;
      let width = r.width, height = r.height, x = r.x, y = r.y;
      if (css.objectFit === 'contain') { const scale = Math.min(width / iw, height / ih); width = iw * scale; height = ih * scale; x += (r.width - width) / 2; y += (r.height - height) / 2; }
      const b = alpha.bbox;
      return { left: x + b.left * width, top: y + b.top * height, right: x + b.right * width, bottom: y + b.bottom * height,
        width: (b.right - b.left) * width, height: (b.bottom - b.top) * height, x: x + alpha.centroid.x * width, y: y + alpha.centroid.y * height };
    };
    const cssBackgroundAlpha = element => {
      const color = getComputedStyle(element).backgroundColor;
      if (color === 'transparent') return 0;
      const match = color.match(/^rgba\([^,]+,[^,]+,[^,]+,\s*([\d.]+)\)$/);
      return match ? Number(match[1]) : 1;
    };
    // Sample synchronously after the actual draw, before the non-preserved WebGL
    // buffer can clear or ready can release the still-present handoff.
    window.__vaultFrameProbe = ({ canvas, host, view }) => {
      try {
        const alpha = readAlpha(canvas); alphaCache.set(canvas, alpha);
        if (host.id !== 'canvas-host') {
          window.__handoffReview.pixelSignatures.set(canvas, pixelSignature(canvas));
          return;
        }
        window.__handoffReview.latestLiveAlpha = alpha;
        const overlay = host.querySelector('.model-handoff'), overlayAlpha = alphaFor(overlay);
        window.__handoffReview.draws.push({ time: performance.now(), phase: window.__handoffReview.phase, host: rectOf(host), alpha, object: projected(canvas, alpha), view,
          overlay: overlay ? { alpha: overlayAlpha, object: projected(overlay, overlayAlpha) } : null });
      } catch (error) { window.__handoffReview.probe_errors.push(error.message); }
    };
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
    const sample = (schedule = true) => {
      const host = document.querySelector('#canvas-host'), flight = document.querySelector('.stage-flight'), overlay = host.querySelector('.model-handoff'), model = host.querySelector('.model-canvas');
      if (document.querySelector('#viewer-dialog')?.open) {
        const stationaryVisible = [...host.querySelectorAll('canvas,img')].some(visible);
        const hasVisual = stationaryVisible || visible(flight);
        const entry = { time: performance.now(), phase: window.__handoffReview.phase, hasVisual, stationaryVisible, state: host.dataset.modelState, host: rectOf(host),
          model: model ? { alpha: alphaFor(model), object: projected(model, alphaFor(model)), visible: visible(model) } : null,
          overlay: overlay ? { alpha: alphaFor(overlay), object: projected(overlay, alphaFor(overlay)), opacity: Number(getComputedStyle(overlay).opacity), css_background_alpha: cssBackgroundAlpha(overlay) } : null };
        if (flight && visible(flight)) {
          const r = flight.getBoundingClientRect(), iw = flight.naturalWidth || flight.width, ih = flight.naturalHeight || flight.height;
          const contentScale = Math.min(r.width / iw, r.height / ih);
          const alpha = alphaFor(flight);
          entry.flight = { square: Math.min(iw, ih) * contentScale, x: r.x + r.width / 2, y: r.y + r.height / 2, width: iw, height: ih,
            alpha, object: projected(flight, alpha), css_background_alpha: cssBackgroundAlpha(flight), css_background_image: getComputedStyle(flight).backgroundImage };
        }
        window.__handoffReview.frames.push(entry);
      }
      if (schedule) window.__handoffReviewRAF = requestAnimationFrame(() => sample());
    };
    // rAF is not guaranteed to land on the final frame of a short flight. Sample
    // its real filled endpoint before the app's await continuation removes it.
    // Keep the existing center/scale tolerances, rather than widening them for
    // a penultimate sample on a loaded software-rendered CI runner.
    const animate = Element.prototype.animate;
    window.__handoffOriginalAnimate = animate;
    Element.prototype.animate = function (...args) {
      const animation = animate.apply(this, args);
      if (this.classList.contains('stage-flight')) animation.finished.then(() => sample(false), () => {});
      return animation;
    };
    sample();
  });
}
async function endSampler(page) {
  return page.evaluate(() => { cancelAnimationFrame(window.__handoffReviewRAF); delete window.__vaultFrameProbe; if (window.__handoffOriginalAnimate) Element.prototype.animate = window.__handoffOriginalAnimate; return window.__handoffReview.frames; });
}

async function dynamicContinuity(page, caseReport, frames) {
  const { draws, probe_errors } = await page.evaluate(() => ({ draws: window.__handoffReview.draws, probe_errors: window.__handoffReview.probe_errors }));
  const comparisons = [], phases = [];
  const requireBounds = (object, label) => {
    assert(object && ['x', 'y', 'width', 'height'].every(key => Number.isFinite(object[key])) && object.width > 0 && object.height > 0,
      label + ' must contain measured, finite, nonempty model bounds');
  };
  const compare = (a, b, reason, phase) => {
    requireBounds(a, phase + ': ' + reason + ' before');
    requireBounds(b, phase + ': ' + reason + ' after');
    comparisons.push({ phase, reason, y_step_px: Math.abs(a.y - b.y), center_step_px: Math.hypot(a.x - b.x, a.y - b.y),
      scale_step: Math.max(Math.abs(a.width / b.width - 1), Math.abs(a.height / b.height - 1)) });
  };
  assert.deepEqual(probe_errors, [], 'Synchronous rendered-alpha sampling must succeed');
  for (const phase of ['open', 'reopen']) {
    const samples = frames.filter(frame => frame.phase === phase), renderSamples = draws.filter(draw => draw.phase === phase);
    assert(renderSamples.length > 0, phase + ' must include an actual synchronous draw');
    for (let i = 0; i < renderSamples.length; i++) {
      const draw = renderSamples[i];
      requireBounds(draw.object, phase + ': actual draw ' + i);
      assert(draw.alpha?.transparent_fraction > 0.2 && draw.alpha.corner_alpha_max <= 3,
        phase + ': every actual draw must preserve a transparent surrounding area');
      if (i > 0) compare(renderSamples[i - 1].object, draw.object, 'consecutive-actual-draws', phase);
    }
    // The first synchronous hook sees the handoff before ready can fade/remove it,
    // even if a cached reopen completes before the next RAF sampler callback.
    compare(renderSamples[0].overlay?.object, renderSamples[0].object, 'handoff-versus-first-actual-draw', phase);
    const hostRects = [...samples.map(frame => frame.host), ...renderSamples.map(draw => draw.host)];
    const ranges = Object.fromEntries(['x', 'y', 'width', 'height'].map(key => [key, Math.max(...hostRects.map(rect => rect[key])) - Math.min(...hostRects.map(rect => rect[key]))]));
    let releases = 0;
    for (let i = 0; i < samples.length; i++) {
      const frame = samples[i], previous = samples[i - 1];
      if (frame.state === 'ready' && frame.overlay && frame.model) compare(frame.overlay.object, frame.model.object, 'overlay-versus-ready-draw', phase);
      if (previous?.overlay && !frame.overlay && frame.model) { releases++; compare(previous.overlay.object, frame.model.object, 'overlay-release-boundary', phase); }
      if (previous && !previous.flight && !frame.flight) {
        const previousObject = previous.overlay?.opacity > 0.5 ? previous.overlay.object : previous.model?.object;
        const nextObject = frame.overlay?.opacity > 0.5 ? frame.overlay.object : frame.model?.object;
        compare(previousObject, nextObject, 'consecutive-stationary-frames', phase);
      }
    }
    phases.push({ phase, samples: samples.length, draws: renderSamples.length, ready_seen: samples.some(frame => frame.state === 'ready'), release_boundaries: releases, host_rect_range_px: ranges });
  }
  const surfaces = frames.flatMap(frame => [frame.overlay && { kind: 'handoff', ...frame.overlay }, frame.flight && { kind: 'flight', ...frame.flight }].filter(Boolean));
  caseReport.dynamic_continuity = { phases, comparisons, draws, probe_errors, transparent_surfaces_sampled: surfaces.length,
    max_y_step_px: Math.max(0, ...comparisons.map(item => item.y_step_px)),
    max_center_step_px: Math.max(0, ...comparisons.map(item => item.center_step_px)),
    max_scale_step: Math.max(0, ...comparisons.map(item => item.scale_step)) };
  for (const phase of phases) {
    assert(phase.samples > 1 && phase.draws > 0 && phase.ready_seen, phase.phase + ' must cover loading, an actual draw, and settled ready frames');
    assert(phase.release_boundaries > 0, phase.phase + ' must sample the actual overlay-release boundary');
    for (const [axis, range] of Object.entries(phase.host_rect_range_px)) assert(range <= 1, phase.phase + ': canvas host ' + axis + ' changed by ' + range.toFixed(2) + ' px during loading/ready/release');
  }
  assert(surfaces.length > 0, 'Transparency must be checked on actual handoff surfaces');
  for (const surface of surfaces) {
    assert(surface.css_background_alpha === 0, surface.kind + ' must not transform an opaque CSS background rectangle');
    if (surface.kind === 'flight') assert.equal(surface.css_background_image, 'none', 'A flight must not carry a background image');
    assert(surface.alpha?.transparent_fraction > 0.2 && surface.alpha.corner_alpha_max <= 3, surface.kind + ' pixels must retain a transparent surrounding area');
  }
  for (const comparison of comparisons) {
    assert(comparison.y_step_px <= 3, comparison.phase + ': ' + comparison.reason + ' moved model Y by ' + comparison.y_step_px.toFixed(2) + ' px');
    assert(comparison.center_step_px <= 3, comparison.phase + ': ' + comparison.reason + ' moved model center by ' + comparison.center_step_px.toFixed(2) + ' px');
    assert(comparison.scale_step <= 0.03, comparison.phase + ': ' + comparison.reason + ' changed model scale by ' + (comparison.scale_step * 100).toFixed(2) + '%');
  }
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
  const caseReport = { label, status: 'running' }; report.cases.push(caseReport);
  try {
    await catalog(page);
    const card = page.locator('#grid .asset-card[data-id="natural-arch"]');
    await card.scrollIntoViewIfNeeded(); await card.focus();
    await startSampler(page);
    await page.keyboard.press('Home');
    for (let i = 0; i < 7; i++) await page.keyboard.press('ArrowRight');
    await page.waitForFunction(() => {
      const card = document.querySelector('#grid [data-id="natural-arch"]');
      return card?.dataset.previewState === 'ready' && window.__vaultPreview?.kind === 'shared-real-model' &&
        window.__vaultPreview.activeId === 'natural-arch' && window.__vaultPreview.frame === 7 &&
        Math.abs(Number(card.dataset.previewAzimuth) - 147) < 0.001 && card.querySelector('.asset-image .model-canvas');
    });
    caseReport.preview_pixels = await canvasPixels(page, '#grid [data-id="natural-arch"] .asset-image .model-canvas');
    caseReport.preview_resources = await page.evaluate(() => ({ ...window.__vaultGPU }));
    assert.equal(caseReport.preview_resources.rendererCount, 1, 'The card uses the shared renderer');
    assert.equal(caseReport.preview_resources.parseCount, 1, 'The card decodes exactly one GLB');
    assert.equal(caseReport.preview_resources.networkRequests, 1, 'The card requests exactly one GLB');
    assert.equal(caseReport.preview_resources.cachedScenes, 1, 'The decoded card resource is retained for detail');
    await page.evaluate(() => {
      window.__originalReviewCard = document.querySelector('#grid [data-id="natural-arch"]');
      window.__openingCardSurface = window.__originalReviewCard.querySelector('.asset-image .model-canvas');
      window.__handoffReview.phase = 'open';
    });
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => document.querySelector('#viewer-dialog')?.open);
    assert(await page.evaluate(() => {
      const handoff = document.querySelector('#viewer-dialog .stage-flight, #canvas-host .model-handoff');
      return handoff instanceof HTMLCanvasElement && handoff !== window.__openingCardSurface;
    }), 'The opening handoff copies the current draw so the shared WebGL canvas can attach to detail');
    caseReport.handoff_pixels = await canvasPixels(page, '#viewer-dialog .stage-flight, #canvas-host .model-handoff');
    assert.deepEqual(caseReport.handoff_pixels, caseReport.preview_pixels, 'The exact currently painted card pixels must enter the detail handoff');
    assert(caseReport.handoff_pixels.transparent_fraction > 0.2 && caseReport.handoff_pixels.corner_alpha_max <= 3, 'The initial handoff must not contain a baked opaque background');
    await ready(page, 'natural-arch');
    assert(await page.locator('#canvas-host .model-canvas').evaluate(canvas => canvas === window.__openingCardSurface), 'Detail must attach the exact shared WebGL canvas used by the card');
    caseReport.open_resources = await page.evaluate(() => ({ ...window.__vaultGPU }));
    assert.equal(caseReport.open_resources.parseCount, caseReport.preview_resources.parseCount, 'Opening detail must reuse the decoded card resource');
    assert.equal(caseReport.open_resources.networkRequests, caseReport.preview_resources.networkRequests, 'Opening detail must not fetch the GLB again');
    assert.equal(caseReport.open_resources.rendererCreations, caseReport.preview_resources.rendererCreations, 'Opening detail must not allocate another renderer');
    assert.equal(caseReport.open_resources.liveScenes, 1, 'The shared resource has one attached scene');
    assert.equal(caseReport.open_resources.cachedScenes, caseReport.preview_resources.cachedScenes, 'Opening detail must not add a duplicate decoded scene');
    assert(caseReport.open_resources.resourceReuses > caseReport.preview_resources.resourceReuses, 'Detail must acquire the retained decoded resource');
    const initial = await angles(page);
    assert(deltaAngle(initial.azimuth, 147) < 0.001, 'The 7/24 preview angle enters actual 3D unchanged');
    await page.waitForTimeout(350);
    await page.waitForFunction(() => !document.querySelector('#canvas-host .model-handoff') && !document.querySelector('.stage-flight'));
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    await page.evaluate(() => { window.__handoffReview.phase = 'inspect'; });
    await pixelParity(page, label, caseReport);
    await page.evaluate(() => { window.__handoffReview.phase = 'interact'; });
    await page.locator('#canvas-host').focus(); await page.keyboard.press('ArrowRight'); await page.keyboard.press('ArrowUp');
    await page.waitForFunction(previous => Math.abs(Number(document.querySelector('#canvas-host').dataset.viewAzimuth) - previous) > 0.1, initial.azimuth);
    await page.locator('#zoom-in').click();
    await page.waitForFunction(previous => Number(document.querySelector('#canvas-host').dataset.viewDistance) < previous * 0.99, initial.distance);
    const beforeClose = await angles(page);
    caseReport.beforeClose = beforeClose;
    await screenshot(page, label + '-detail-before-close');
    await page.evaluate(() => { window.__handoffReview.phase = 'close'; });
    await page.locator('#close').click(); await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open);
    await page.waitForTimeout(150);
    assert(await card.evaluate(node => node === window.__originalReviewCard), 'Same-list close keeps the original card DOM');
    assert.equal(await card.locator('.model-preview-snapshot').count(), 1, 'The returned card retains the actual current detail image');
    const returned = await card.locator('.model-preview-snapshot').evaluate(node => {
      const r = node.getBoundingClientRect(); return { square: Math.min(r.width, r.height), x: r.x + r.width / 2, y: r.y + r.height / 2 };
    });
    assert.equal(await page.evaluate(() => document.activeElement?.dataset.id), 'natural-arch');
    caseReport.returned = returned;
    caseReport.beforeRetainedScreenshot = await previewDiagnostics(page);
    await screenshot(page, label + '-retained-card');
    caseReport.beforeReopen = await previewDiagnostics(page);
    assert.equal(caseReport.beforeReopen.preview.activeId, 'natural-arch', 'The retained card must still be active immediately before reopening');
    assert.equal(caseReport.beforeReopen.card.canvases, 1, 'The retained image must remain painted immediately before reopening');
    await page.evaluate(() => { window.__handoffReview.phase = 'reopen'; });
    await page.keyboard.press('Enter'); await ready(page, 'natural-arch'); await page.waitForTimeout(350);
    await page.waitForFunction(() => !document.querySelector('#canvas-host .model-handoff') && !document.querySelector('.stage-flight'));
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    await page.evaluate(() => { window.__handoffReview.phase = 'inspect-reopen'; });
    const reopened = await angles(page);
    caseReport.reopened = reopened;
    assert(await page.locator('#canvas-host .model-canvas').evaluate(canvas => canvas === window.__openingCardSurface), 'Reopening keeps the same shared WebGL canvas');
    caseReport.reopen_resources = await page.evaluate(() => ({ ...window.__vaultGPU }));
    assert.equal(caseReport.reopen_resources.parseCount, caseReport.preview_resources.parseCount, 'Reopening must not decode the GLB again');
    assert.equal(caseReport.reopen_resources.networkRequests, caseReport.preview_resources.networkRequests, 'Reopening must not fetch the GLB again');
    assert.equal(caseReport.reopen_resources.rendererCreations, caseReport.preview_resources.rendererCreations, 'Reopening must not allocate another renderer');
    assert.equal(caseReport.reopen_resources.cachedScenes, caseReport.preview_resources.cachedScenes, 'Reopening must not duplicate decoded resources');

    assert(deltaAngle(beforeClose.azimuth, reopened.azimuth) < 0.001, 'Close/reopen preserves the actual camera azimuth');
    assert(Math.abs(beforeClose.elevation - reopened.elevation) < 0.001, 'Close/reopen preserves the actual camera elevation');
    assert(Number.isFinite(beforeClose.distance) && Math.abs(beforeClose.distance - reopened.distance) < 0.00001, 'Close/reopen preserves the actual camera zoom distance');
    const frames = await endSampler(page), closeFlights = frames.filter(frame => frame.phase === 'close' && frame.flight);
    caseReport.frames = frames;
    await dynamicContinuity(page, caseReport, frames);
    assert.equal(frames.filter(frame => !frame.hasVisual).length, 0, 'Open/close/reopen must never show an empty visual frame');
    if (options.reducedMotion !== 'reduce') {
      assert(closeFlights.length > 1, 'The ordinary-motion reverse transition must actually animate');
      assert.equal(frames.filter(frame => frame.flight && frame.stationaryVisible).length, 0, 'A flying model must not duplicate a stationary model behind it');
      const last = closeFlights.at(-1).flight;
      assert(Math.abs(last.square / returned.square - 1) < 0.12, 'Reverse-flight model scale must match the retained card at completion');
      assert(Math.hypot(last.x - returned.x, last.y - returned.y) < 12, 'Reverse-flight center must match the retained card');
    }
    Object.assign(caseReport, { status: 'pass', frames });
    report.checks.push(`${label}: rotated preview, real 3D, current-angle close/reopen, no blank frame, and reverse-flight scale continuity.`);
  } catch (error) {
    caseReport.status = 'fail'; caseReport.error = error.stack;
    caseReport.failure_diagnostics = await previewDiagnostics(page).catch(() => null);
    caseReport.frames = await endSampler(page).catch(() => []);
    await page.screenshot({ path: resolve(output, label + '-failure.png'), fullPage: false }).then(() => report.screenshots.push(label + '-failure.png')).catch(() => {});
    throw error;
  } finally { await context.close(); }
}

async function contextLossRecovery() {
  const label = 'context-loss-recovery', context = await makeContext(label, { reducedMotion: 'reduce' }), { page } = context;
  const caseReport = { label, status: 'running' }; report.cases.push(caseReport);
  try {
    await page.goto(base + prefix + 'models/natural-arch/'); await ready(page, 'natural-arch');
    await page.waitForFunction(() => !document.querySelector('#canvas-host .model-handoff'));
    const before = await angles(page); caseReport.before = before;
    const supported = await page.locator('#canvas-host .model-canvas').evaluate(canvas => {
      const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
      const extension = gl?.getExtension('WEBGL_lose_context');
      if (!extension) return false;
      window.__contextLossReview = { extension, canvas, renderedFrames: window.__vaultGPU.renderedFrames };
      extension.loseContext();
      return true;
    });
    if (!supported) {
      Object.assign(caseReport, { status: 'skipped', reason: 'WEBGL_lose_context is unavailable in this browser.' });
      report.checks.push('Context-loss recovery not exercised: WEBGL_lose_context is unavailable in this browser.');
      return;
    }
    await page.waitForFunction(() => document.querySelector('#canvas-host')?.dataset.modelState === 'error');
    caseReport.lost = await page.locator('#canvas-host').evaluate(host => {
      const canvas = host.querySelector('.model-canvas'), poster = host.querySelector('.model-poster');
      return {
        canvas_visibility: canvas ? getComputedStyle(canvas).visibility : null,
        poster_visibility: poster ? getComputedStyle(poster).visibility : null,
        poster_loaded: Boolean(poster?.complete && poster.naturalWidth > 0),
        controls_disabled: [...document.querySelectorAll('.viewer-controls button')].every(button => button.disabled),
        handoffs: host.querySelectorAll('.model-handoff').length,
      };
    });
    assert.equal(caseReport.lost.canvas_visibility, 'hidden', 'Lost WebGL context must hide the invalid canvas');
    assert.equal(caseReport.lost.poster_visibility, 'visible', 'Context loss after ready must restore the static poster despite prior inline hiding');
    assert(caseReport.lost.poster_loaded, 'Context-loss fallback must contain a decoded image');
    assert(caseReport.lost.controls_disabled, 'Unavailable 3D controls must be disabled');
    assert.equal(caseReport.lost.handoffs, 0, 'The fallback check must exercise a settled viewer without a retained handoff');
    await screenshot(page, label + '-fallback');
    await page.evaluate(() => window.__contextLossReview.extension.restoreContext());
    await ready(page, 'natural-arch');
    await page.waitForFunction(() => window.__vaultGPU.renderedFrames > window.__contextLossReview.renderedFrames);
    const recovered = await angles(page); caseReport.recovered = recovered;
    assert(deltaAngle(before.azimuth, recovered.azimuth) < 0.001, 'Context restoration preserves camera azimuth');
    assert(Math.abs(before.elevation - recovered.elevation) < 0.001, 'Context restoration preserves camera elevation');
    assert(Math.abs(before.distance - recovered.distance) < 0.00001, 'Context restoration preserves camera zoom distance');
    assert.equal(await page.locator('#canvas-host .model-canvas').evaluate(canvas => getComputedStyle(canvas).visibility), 'visible');
    assert.equal(await page.locator('#canvas-host .model-poster').evaluate(poster => getComputedStyle(poster).visibility), 'hidden');
    assert.equal(await page.locator('#canvas-host .model-canvas').count(), 1);
    assert.equal(await page.evaluate(() => window.__vaultGPU.liveScenes), 1);
    await screenshot(page, label + '-recovered');
    caseReport.status = 'pass';
    report.checks.push('WebGL context loss restores the static poster; recovery redraws one real scene with the same camera and zoom.');
  } catch (error) {
    caseReport.status = 'fail'; caseReport.error = error.stack;
    caseReport.failure_diagnostics = await previewDiagnostics(page).catch(() => null);
    throw error;
  } finally { await context.close(); }
}

async function earlyLoadFailure() {
  const label = 'early-load-failure', context = await makeContext(label), { page } = context;
  const caseReport = { label, status: 'running' }; report.cases.push(caseReport);
  try {
    // Warm the viewer import/renderer without caching the asset that will fail.
    await page.goto(base + prefix + 'models/conifer-tree/'); await ready(page, 'conifer-tree');
    await page.locator('#close').click(); await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open);
    await page.waitForFunction(() => document.querySelector('#grid')?.getAttribute('aria-busy') === 'false');
    const card = page.locator('#grid .asset-card[data-id="natural-arch"]');
    await card.scrollIntoViewIfNeeded(); await card.focus(); await page.keyboard.press('Home');
    await page.keyboard.press('ArrowRight');
    await page.waitForFunction(() => {
      const card = document.querySelector('#grid [data-id="natural-arch"]');
      return card?.dataset.previewState === 'ready' && card.querySelector('.asset-image .model-canvas')?.width > 0 &&
        Math.abs(Number(card.dataset.previewAzimuth) - 57) < 0.001;
    });
    caseReport.before_failure_resources = await page.evaluate(() => ({ ...window.__vaultGPU }));
    // The card deliberately warmed its GLB. Give only the detail response a new
    // resource key so an immediate network failure cannot be hidden by that LRU.
    await page.route('**/assets/catalog/details/natural-arch.json', async route => {
      const response = await route.fetch();
      const detail = await response.json();
      await route.fulfill({ response, json: { ...detail, glb: 'assets/__qa__/handoff-failure/natural-arch.glb' } });
    });
    let coldFailures = 0;
    await page.evaluate(() => {
      const host = document.querySelector('#canvas-host');
      window.__earlyFailureDuringFlight = null;
      const observer = new MutationObserver(() => {
        if (host.dataset.modelState !== 'error') return;
        window.__earlyFailureDuringFlight = Boolean(document.querySelector('#viewer-dialog .stage-flight'));
        observer.disconnect();
      });
      observer.observe(host, { attributes: true, attributeFilter: ['data-model-state'] });
    });
    await page.route('**/assets/__qa__/handoff-failure/natural-arch.glb', route => { coldFailures++; return route.abort('failed'); });
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => document.querySelector('#canvas-host').dataset.modelState === 'error');
    assert.equal(coldFailures, 1, 'The injected failure must exercise a genuinely cold GLB request');
    assert.equal(await page.evaluate(() => window.__vaultGPU.networkRequests), caseReport.before_failure_resources.networkRequests + 1, 'The detail failure must bypass the warmed preview resource');
    assert.equal(await page.evaluate(() => window.__earlyFailureDuringFlight), true, 'The failure must occur while the retained bitmap is in flight');
    await page.waitForFunction(() => !document.querySelector('.stage-flight, #canvas-host .model-handoff'));
    caseReport.fallback = await page.locator('#canvas-host').evaluate(host => {
      const poster = host.querySelector('.model-poster');
      return { poster_loaded: Boolean(poster?.complete && poster.naturalWidth > 0),
        poster_visibility: poster ? getComputedStyle(poster).visibility : null,
        controls_disabled: [...document.querySelectorAll('.viewer-controls button')].every(button => button.disabled),
        live_scenes: window.__vaultGPU?.liveScenes ?? 0 };
    });
    assert(caseReport.fallback.poster_loaded, 'The failed model must reveal a decoded fallback poster');
    assert.equal(caseReport.fallback.poster_visibility, 'visible');
    assert(caseReport.fallback.controls_disabled);
    assert.equal(caseReport.fallback.live_scenes, 0);
    await screenshot(page, label + '-fallback');
    await page.keyboard.press('Escape');
    await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open);
    assert.equal(await page.locator('.stage-flight, .model-handoff').count(), 0);
    assert.equal(await page.evaluate(() => document.querySelectorAll('[data-detail-origin]').length), 0);
    caseReport.status = 'pass';
    report.checks.push('An immediate GLB failure during opening retires the copied bitmap after flight and reveals the decoded poster without stale overlays or live scenes.');
  } catch (error) { caseReport.status = 'fail'; caseReport.error = error.stack; throw error; }
  finally { await context.close(); }
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
  await roundTrip('desktop-retina-motion', { deviceScaleFactor: 2 });
  await roundTrip('mobile-motion', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await roundTrip('desktop-reduced-motion', { reducedMotion: 'reduce' });
  await roundTrip('desktop-dark-motion', { colorScheme: 'dark' });
  await contextLossRecovery();
  await earlyLoadFailure();
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

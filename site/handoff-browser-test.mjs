/** Real browser regression coverage for shared-model card/detail continuity and interrupted navigation. */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import assert from 'node:assert/strict';
import { CARD_RENDER_PRESET } from './render-preset.js';

const root = resolve(process.env.GALLERY_DIR || 'dist');
const output = resolve(process.env.QA_OUTPUT_DIR || 'qa/handoff-continuity');
const prefix = '/lowpoly-vault/';
const cpuDOMRaster = !/^(0|false)$/i.test(process.env.QA_CPU_DOM_RASTER || '1');
const report = { dom_raster_mode: cpuDOMRaster ? 'cpu' : 'browser-default', status: 'running', commit: process.env.GITHUB_SHA || null, checks: [], cases: [], page_errors: [], screenshots: [], videos: [], note: 'Chromium software rendering and emulated viewport sizes; no physical-device performance claim.' };
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
  const { returnTiming = false, returnStyles, ...contextOptions } = options;
  const viewport = contextOptions.viewport || { width: 1440, height: 1000 };
  // Timing-sensitive return evidence uses real DOM/draw samples and screenshots.
  // Video encoding must not consume the short 120 ms travel / 60 ms fade budget.
  const context = await browser.newContext({ viewport, reducedMotion: 'no-preference',
    ...(returnTiming ? {} : { recordVideo: { dir: output, size: viewport } }), ...contextOptions });
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
  await page.goto(base + prefix + 'models/?pack=prehistoric-starter');
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
    window.__handoffReview = { phase: 'preview', frames: [], draws: [], returnDraws: [], probe_errors: [], pixelSignatures: new WeakMap() };
    const alphaCache = new WeakMap(), sampleCanvas = document.createElement('canvas');
    const returnCaptures = [], returnFrameCaptures = [];
    let initialCompositeCapture;
    const alphaCaptures = [], signatureCaptures = [], projectionCaptures = [];
    const rectOf = element => { const r = element.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height }; };
    const alphaSampleSize = source => {
      const sw = source.naturalWidth || source.width, sh = source.naturalHeight || source.height;
      const ratio = Math.min(1, 384 / Math.max(sw, sh));
      return [Math.max(1, Math.round(sw * ratio)), Math.max(1, Math.round(sh * ratio))];
    };
    const readAlpha = (source, sampledSize) => {
      const sw = source.naturalWidth || source.width, sh = source.naturalHeight || source.height;
      if (!sw || !sh) return null;
      [sampleCanvas.width, sampleCanvas.height] = sampledSize || alphaSampleSize(source);
      const width = sampleCanvas.width, height = sampleCanvas.height, context = sampleCanvas.getContext('2d', { willReadFrequently: true });
      context.clearRect(0, 0, width, height); context.drawImage(source, 0, 0, width, height);
      const pixels = context.getImageData(0, 0, width, height).data;
      let left = width, right = -1, top = height, bottom = -1, count = 0, transparent = 0, weight = 0, cx = 0, cy = 0, alphaMass = 0, nonzero = 0;
      for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
        const alpha = pixels[(y * width + x) * 4 + 3];
        alphaMass += alpha; if (alpha > 0) nonzero++;
        if (alpha <= 3) transparent++;
        if (alpha <= 16) continue;
        left = Math.min(left, x); right = Math.max(right, x); top = Math.min(top, y); bottom = Math.max(bottom, y); count++; weight += alpha; cx += (x + 0.5) * alpha; cy += (y + 0.5) * alpha;
      }
      return { source: [sw, sh], sampled: [width, height], pixels: count, nonzero_fraction: nonzero / (width * height), mean_alpha: alphaMass / (width * height * 255), transparent_fraction: transparent / (width * height),
        corner_alpha_max: Math.max(pixels[3], pixels[(width - 1) * 4 + 3], pixels[((height - 1) * width) * 4 + 3], pixels.at(-1)),
        bbox: count ? { left: left / width, top: top / height, right: (right + 1) / width, bottom: (bottom + 1) / height } : null,
        centroid: count ? { x: cx / weight / width, y: cy / weight / height } : null };
    };
    const alphaFor = element => {
      if (!element || !(element.naturalWidth || element.width) || !(element.naturalHeight || element.height)) return null;
      if (!alphaCache.has(element) && !element.classList.contains('model-canvas')) {
        const alpha = {}, sampled = alphaSampleSize(element);
        alphaCache.set(element, alpha);
        alphaCaptures.push({ alpha, source: [element.naturalWidth || element.width, element.naturalHeight || element.height], copy: copyPixels(element, sampled) });
      }
      return alphaCache.get(element) || null;
    };
    const pixelSignature = source => {
      // Match ModelStage.snapshot's bounded copy without retaining another GLB,
      // renderer, or scene. These are the actual current WebGL draw's pixels.
      const side = Math.min(source.width, source.height), scale = Math.min(1, 1024 / side);
      const canvas = document.createElement('canvas');
      canvas.width = canvas.height = Math.round(side * scale);
      const context = canvas.getContext('2d', { willReadFrequently: true });
      context.drawImage(source, (source.width - side) / 2, (source.height - side) / 2,
        side, side, 0, 0, canvas.width, canvas.height);
      const bytes = context.getImageData(0, 0, canvas.width, canvas.height).data;
      let hash = 2166136261, transparent = 0;
      for (let i = 0; i < bytes.length; i++) { hash = Math.imul(hash ^ bytes[i], 16777619) >>> 0; if (i % 4 === 3 && bytes[i] <= 3) transparent++; }
      const corners = [3, (canvas.width - 1) * 4 + 3, ((canvas.height - 1) * canvas.width) * 4 + 3, bytes.length - 1].map(i => bytes[i]);
      return { width: canvas.width, height: canvas.height, rgba_hash: hash.toString(16).padStart(8, '0'), transparent_fraction: transparent / (bytes.length / 4), corner_alpha_max: Math.max(...corners) };
    };
    const projectedAt = (r, objectFit, alpha) => {
      if (!alpha?.bbox) return null;
      const [iw, ih] = alpha.source;
      let width = r.width, height = r.height, x = r.x, y = r.y;
      if (objectFit === 'contain') { const scale = Math.min(width / iw, height / ih); width = iw * scale; height = ih * scale; x += (r.width - width) / 2; y += (r.height - height) / 2; }
      const b = alpha.bbox;
      return { left: x + b.left * width, top: y + b.top * height, right: x + b.right * width, bottom: y + b.bottom * height,
        width: (b.right - b.left) * width, height: (b.bottom - b.top) * height, x: x + alpha.centroid.x * width, y: y + alpha.centroid.y * height };
    };
    const projected = (element, alpha) => {
      if (!element || !alpha) return null;
      const object = {}, rect = rectOf(element), objectFit = getComputedStyle(element).objectFit;
      projectionCaptures.push({ object, rect, objectFit, alpha });
      return object;
    };
    const copyPixels = (source, sampledSize) => {
      const copy = document.createElement('canvas');
      if (sampledSize) {
        [copy.width, copy.height] = sampledSize;
        copy.getContext('2d').drawImage(source, 0, 0, copy.width, copy.height);
      } else {
        const side = Math.min(source.width, source.height), scale = Math.min(1, 1024 / side);
        copy.width = copy.height = Math.round(side * scale);
        copy.getContext('2d').drawImage(source, (source.width - side) / 2, (source.height - side) / 2, side, side, 0, 0, copy.width, copy.height);
      }
      return copy;
    };
    const captureSignature = source => {
      const signature = {};
      signatureCaptures.push({ signature, copy: copyPixels(source) });
      return signature;
    };
    // Opening uses the same immutable-pixel strategy as return. In the CI
    // reports, synchronous readback/hashing blocked the next opening RAF for
    // about one second and consumed the entire real 160 ms complementary fade.
    // Keep actual pixels and DOM geometry now; measure them only after settling.
    window.__handoffReview.flushOpeningCaptures = () => {
      for (const capture of alphaCaptures) {
        if (capture.processed) continue;
        Object.assign(capture.alpha, readAlpha(capture.copy, [capture.copy.width, capture.copy.height]), { source: capture.source });
        capture.copy.width = capture.copy.height = 0; capture.processed = true;
      }
      for (const capture of signatureCaptures) {
        if (capture.processed) continue;
        Object.assign(capture.signature, pixelSignature(capture.copy));
        capture.copy.width = capture.copy.height = 0; capture.processed = true;
      }
      for (const capture of projectionCaptures) {
        if (capture.processed) continue;
        Object.assign(capture.object, projectedAt(capture.rect, capture.objectFit, capture.alpha));
        capture.processed = true;
      }
    };
    const dissolveStyle = (host, lower, upper) => ({
      isolation: getComputedStyle(host).isolation, hostOpacity: Number(getComputedStyle(host).opacity),
      liveOpacity: lower ? Number(getComputedStyle(lower).opacity) : null,
      posterOpacity: upper ? Number(getComputedStyle(upper).opacity) : null,
      liveBlend: lower ? getComputedStyle(lower).mixBlendMode : null,
      posterBlend: upper ? getComputedStyle(upper).mixBlendMode : null,
      posterVisibility: upper ? getComputedStyle(upper).visibility : null,
      advertisedOpacity: host.dataset.returnOpacity === undefined ? null : Number(host.dataset.returnOpacity),
      posterCanvas: upper instanceof HTMLCanvasElement && !upper.classList.contains('model-canvas'),
      posterDimensions: upper ? [upper.width, upper.height] : null,
    });
    const returnStyle = (host, canvas) => {
      const composite = host.querySelector('.return-composite'), weight = host.dataset.returnOpacity === undefined ? 1 : Number(host.dataset.returnOpacity);
      const origin = window.__originalReviewCard?.querySelector('.asset-image > img');
      return { hostOpacity: Number(getComputedStyle(host).opacity), advertisedOpacity: weight,
        liveOpacity: weight, posterOpacity: 1 - weight,
        liveAttached: canvas?.parentElement === host, liveVisibility: canvas ? getComputedStyle(canvas).visibility : null,
        liveCSSOpacity: canvas ? Number(getComputedStyle(canvas).opacity) : null,
        liveBlend: canvas ? getComputedStyle(canvas).mixBlendMode : null,
        compositeCount: host.querySelectorAll('.return-composite').length,
        compositeCanvas: composite instanceof HTMLCanvasElement,
        compositeVisibility: composite ? getComputedStyle(composite).visibility : null,
        compositeOpacity: composite ? Number(getComputedStyle(composite).opacity) : null,
        compositeBlend: composite ? getComputedStyle(composite).mixBlendMode : null,
        compositeDimensions: composite ? [composite.width, composite.height] : null,
        legacyPosterCount: host.querySelectorAll('.return-poster').length,
        originImage: origin instanceof HTMLImageElement, originDimensions: origin ? [origin.naturalWidth, origin.naturalHeight] : null };
    };
    const blendPixels = (live, poster, liveOpacity, posterOpacity, operation = 'lighter') => {
      const composite = document.createElement('canvas'); composite.width = live.width; composite.height = live.height;
      const context = composite.getContext('2d'); context.globalCompositeOperation = operation;
      // Match blendVisual exactly: actual lower WebGL snapshot, then upper poster.
      context.globalAlpha = liveOpacity; context.drawImage(live, 0, 0);
      context.globalAlpha = posterOpacity; context.drawImage(poster, 0, 0, composite.width, composite.height);
      return composite;
    };
    // Retain actual pixels synchronously, but defer CPU readback, alpha loops,
    // hashing and PNG encoding until motion has settled. Those probes otherwise
    // consumed more than the complete 180 ms motion on software-rendered CI.
    window.__handoffReview.flushReturnCaptures = () => {
      for (const capture of returnCaptures) {
        if (capture.processed) continue;
        const { draw, alphaCopy, source, rect, objectFit, pixels, composite } = capture;
        draw.alpha = readAlpha(alphaCopy, [alphaCopy.width, alphaCopy.height]); draw.alpha.source = source;
        draw.object = projectedAt(rect, objectFit, draw.alpha);
        if (pixels) draw.pixels = pixelSignature(pixels);
        if (composite) {
          draw.visiblePixels = pixelSignature(composite);
          draw.visibleAlpha = readAlpha(composite, capture.sampled);
        }
        if (window.__handoffReview.returnEndpoint?.draw === draw) window.__handoffReview.returnEndpoint.png = pixels.toDataURL('image/png');
        capture.processed = true;
        // Keep bounded layer copies until the RAF fade samples are measured.
        if (pixels) pixels.width = pixels.height = 0;
        if (composite) composite.width = composite.height = 0;
      }
      for (const capture of returnFrameCaptures) {
        if (capture.processed) continue;
        const { flight, draw, composite, posterCopy, sampled } = capture;
        flight.alpha = composite ? readAlpha(composite, sampled) : draw.alpha;
        flight.object = projectedAt(capture.rect, capture.objectFit, flight.alpha);
        if (composite) {
          flight.visiblePixels = pixelSignature(composite); flight.visibleAlpha = flight.alpha;
          const live = capture.layer.pixelsForFade, style = flight.dissolve;
          const a = readAlpha(live, sampled), b = readAlpha(posterCopy, sampled);
          const sourceOver = blendPixels(live, posterCopy, style.liveOpacity, style.posterOpacity, 'source-over');
          const oldPoster = blendPixels(posterCopy, live, 1, style.liveOpacity, 'source-over');
          flight.alpha_mass = {
            source: 'actual displayed return-composite pixels; immutable canonical draw and actual origin IMG endpoints',
            denominator_pixels: sampled[0] * sampled[1],
            quantization_tolerance: 2 / 255 * Math.min(1, a.nonzero_fraction + b.nonzero_fraction),
            live: a.mean_alpha, poster: b.mean_alpha,
            live_weight: style.liveOpacity, poster_weight: style.posterOpacity,
            expected: a.mean_alpha * style.liveOpacity + b.mean_alpha * style.posterOpacity,
            actual: flight.alpha.mean_alpha,
            complementary_source_over: readAlpha(sourceOver, sampled).mean_alpha,
            old_full_poster_source_over: readAlpha(oldPoster, sampled).mean_alpha,
            displayed_rgba_hash: flight.visiblePixels.rgba_hash,
          };
          composite.width = composite.height = 0; posterCopy.width = posterCopy.height = 0;
        }
        capture.processed = true;
      }
      if (initialCompositeCapture && !initialCompositeCapture.processed) {
        const { copy, draw, weight } = initialCompositeCapture;
        window.__handoffReview.firstComposite = { pixels: pixelSignature(copy), canonicalPixels: draw.pixels,
          weight, sameTask: true, dimensions: [copy.width, copy.height] };
        copy.width = copy.height = 0; initialCompositeCapture.processed = true;
      }
      for (const capture of returnCaptures) if (capture.pixelsForFade) capture.pixelsForFade.width = capture.pixelsForFade.height = 0;
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
        if (host.classList.contains('stage-flight')) {
          const review = window.__handoffReview, progress = Number(host.dataset.returnProgress), returnPhase = host.dataset.returnPhase;
          const draw = { time: performance.now(), phase: review.phase, progress, returnPhase,
            host: rectOf(host), view, actualSharedCanvas: canvas === window.__openingCardSurface,
            originHidden: Boolean(document.querySelector('[data-detail-origin]')),
            opacity: Number(getComputedStyle(canvas).opacity),
            dissolve: returnStyle(host, canvas),
            styleResources: { referenceObjects: window.__vaultGPU.referenceObjects, returnOverlayMeshes: window.__vaultGPU.returnOverlayMeshes || 0, returnOverlayMaterials: window.__vaultGPU.returnOverlayMaterials || 0 } };
          // ModelStage probes after rendering but before its same-task reveal.
          // Check that first hidden draw again before paint, without relaxing
          // the ordinary RAF visibility assertions below.
          if (!review.returnDraws.length && progress === 0 && draw.dissolve.liveVisibility === 'hidden') {
            queueMicrotask(() => { draw.afterDrawReveal = { visibility: getComputedStyle(canvas).visibility,
              sameHost: canvas.parentElement === host, compositeCount: host.querySelectorAll('.return-composite').length }; });
          }
          const sampled = alphaSampleSize(canvas), firstEndpoint = progress >= 1 && !review.returnEndpoint;
          const reversalDraw = Boolean(review.reversalRequested || (window.__reverseReturnAtProgress && progress >= window.__reverseReturnAtProgress && progress < 1));
          const capture = { draw, sampled, source: [canvas.width, canvas.height], rect: rectOf(canvas),
            objectFit: getComputedStyle(canvas).objectFit, alphaCopy: copyPixels(canvas, sampled),
            pixels: firstEndpoint || reversalDraw ? copyPixels(canvas) : null };
          if (firstEndpoint) capture.pixelsForFade = copyPixels(canvas);
          returnCaptures.push(capture); review.returnDraws.push(draw);
          if (firstEndpoint) {
            review.returnEndpoint = { draw };
            // setView's draw is deliberately before onAligned reveals the card.
            // Observe the resulting DOM only after that synchronous task returns.
            queueMicrotask(() => { if (host.isConnected) sample(false); });
          }
          if (window.__reverseReturnAtProgress && !review.reversalRequested && progress >= window.__reverseReturnAtProgress && progress < 1) {
            review.reversalRequested = true;
            setTimeout(() => { review.phase = 'reversal'; history.forward(); }, 0);
          }
          return;
        }
        if (host.id !== 'canvas-host') {
          // Card evidence is read before motion starts and is immediately used
          // by canvasPixels; it does not compete with the opening fade.
          alphaCache.set(canvas, readAlpha(canvas));
          window.__handoffReview.pixelSignatures.set(canvas, pixelSignature(canvas));
          return;
        }
        const time = performance.now(), alpha = {}, sampled = alphaSampleSize(canvas);
        alphaCaptures.push({ alpha, source: [canvas.width, canvas.height], copy: copyPixels(canvas, sampled) });
        alphaCache.set(canvas, alpha);
        const signature = captureSignature(canvas);
        window.__handoffReview.pixelSignatures.set(canvas, signature);
        window.__handoffReview.latestLiveAlpha = alpha;
        const overlay = host.querySelector('.model-handoff'), overlayAlpha = alphaFor(overlay);
        if (['open', 'reversal'].includes(window.__handoffReview.phase) && overlay && !window.__handoffReview[window.__handoffReview.phase === 'reversal' ? 'reversalHandoff' : 'openingHandoff']) {
          // A reduced-motion cached show can retire its overlay before the next
          // Playwright task. Observe the actual copy before ready releases it.
          window.__handoffReview[window.__handoffReview.phase === 'reversal' ? 'reversalHandoff' : 'openingHandoff'] = {
            copied: overlay instanceof HTMLCanvasElement && overlay !== window.__openingCardSurface,
            pixels: captureSignature(overlay), alpha: overlayAlpha,
          };
        }
        window.__handoffReview.draws.push({ time, phase: window.__handoffReview.phase, host: rectOf(host), alpha, object: projected(canvas, alpha), view, pixels: signature,
          overlay: overlay ? { alpha: overlayAlpha, object: projected(overlay, overlayAlpha) } : null,
          dissolve: overlay ? dissolveStyle(host, canvas, overlay) : null });
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
        const canonicalPosterVisible = flight?.dataset.returnPhase === 'fading' && visible(flight.querySelector('.return-composite'));
        const originPosterVisible = visible(window.__originalReviewCard?.querySelector('.asset-image > img'));
        const hasVisual = stationaryVisible || visible(flight) || canonicalPosterVisible;
        const entry = { time: performance.now(), phase: window.__handoffReview.phase, sampledBy: schedule ? 'raf' : 'synchronous', hasVisual, stationaryVisible, canonicalPosterVisible, originPosterVisible,
          dissolve: overlay ? dissolveStyle(host, model || host.querySelector('.model-poster'), overlay) : null, state: host.dataset.modelState, host: rectOf(host),
          model: model ? { alpha: alphaFor(model), object: projected(model, alphaFor(model)), visible: visible(model) } : null,
          overlay: overlay ? { alpha: alphaFor(overlay), object: projected(overlay, alphaFor(overlay)), opacity: Number(getComputedStyle(overlay).opacity), css_background_alpha: cssBackgroundAlpha(overlay) } : null };
        if (flight && visible(flight)) {
          // Opening may use a copied canvas; return must measure the actual
          // shared model-canvas inside its moving DIV, never the wrapper as pixels.
          const surface = flight.querySelector('.model-canvas') || flight;
          const r = surface.getBoundingClientRect(), iw = surface.naturalWidth || surface.width, ih = surface.naturalHeight || surface.height;
          const contentScale = Math.min(r.width / iw, r.height / ih), alpha = alphaFor(surface);
          entry.flight = { square: Math.min(iw, ih) * contentScale, x: r.x + r.width / 2, y: r.y + r.height / 2, width: iw, height: ih,
            kind: flight instanceof HTMLCanvasElement ? 'bitmap-open' : 'live-return', actualSharedCanvas: surface === window.__openingCardSurface,
            progress: Number(flight.dataset.returnProgress), returnPhase: flight.dataset.returnPhase,
            opacity: flight.classList.contains('live-model-return') ? Number(flight.dataset.returnOpacity) : Number(getComputedStyle(surface).opacity),
            dissolve: flight.classList.contains('live-model-return') ? returnStyle(flight, surface) : null,
            originHidden: Boolean(document.querySelector('[data-detail-origin]')),
            alpha, object: projected(surface, alpha), css_background_alpha: cssBackgroundAlpha(flight), css_background_image: getComputedStyle(flight).backgroundImage };
          if (entry.flight.kind === 'live-return') {
            const draw = window.__handoffReview.returnDraws.at(-1);
            if (draw) {
              const composite = flight.querySelector('.return-composite');
              const layer = returnCaptures.find(capture => capture.draw === draw);
              const sampled = alphaSampleSize(composite || surface), origin = window.__originalReviewCard?.querySelector('.asset-image > img');
              const posterCopy = composite ? document.createElement('canvas') : null;
              if (posterCopy) { posterCopy.width = composite.width; posterCopy.height = composite.height; posterCopy.getContext('2d').drawImage(origin, 0, 0, posterCopy.width, posterCopy.height); }
              returnFrameCaptures.push({ flight: entry.flight, draw, layer, sampled,
                composite: composite ? copyPixels(composite) : null, posterCopy,
                rect: rectOf(composite || surface), objectFit: getComputedStyle(composite || surface).objectFit });
            }
          }
        }
        window.__handoffReview.frames.push(entry);
        if (window.__reverseReturnPhase === 'fading' && !window.__handoffReview.reversalRequested && entry.flight?.returnPhase === 'fading' && entry.flight.opacity > 0 && entry.flight.opacity < 1) {
          window.__handoffReview.reversalRequested = true;
          window.__handoffReview.reversalVisible = entry.flight;
          window.__handoffReview.phase = 'reversal'; history.forward();
        }
      }
      if (schedule) window.__handoffReviewRAF = requestAnimationFrame(() => sample());
    };
    // rAF is not guaranteed to land on the final frame of a short flight. Sample
    // its real filled endpoint before the app's await continuation removes it.
    // Keep the existing center/scale tolerances, rather than widening them for
    // a penultimate sample on a loaded software-rendered CI runner.
    // onAligned appends before its first onFade repaint. Preserve that exact
    // same-task surface, before a microtask or RAF can observe changed weights.
    const append = Element.prototype.append;
    window.__handoffOriginalAppend = append;
    Element.prototype.append = function (...nodes) {
      const result = append.apply(this, nodes);
      if (this.classList.contains('live-model-return') && !initialCompositeCapture) {
        const composite = nodes.find(node => node instanceof HTMLCanvasElement && node.classList.contains('return-composite'));
        if (composite) initialCompositeCapture = { copy: copyPixels(composite),
          draw: window.__handoffReview.returnEndpoint.draw, weight: Number(this.dataset.returnOpacity) };
      }
      return result;
    };
    // Reduced-motion warm reopens can draw and release in the same task.
    // Observe the actual operation on both sides; a RAF cannot invent that edge.
    const remove = Element.prototype.remove;
    window.__handoffOriginalRemove = remove;
    Element.prototype.remove = function (...args) {
      const host = this.parentElement;
      const boundary = host?.id === 'canvas-host' && this.classList.contains('model-handoff') &&
        host.dataset.modelState === 'ready' && Boolean(host.querySelector('.model-canvas'));
      if (boundary) sample(false);
      const result = remove.apply(this, args);
      if (boundary) sample(false);
      return result;
    };
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
  return page.evaluate(() => { cancelAnimationFrame(window.__handoffReviewRAF); window.__handoffReview.flushOpeningCaptures(); window.__handoffReview.flushReturnCaptures(); delete window.__vaultFrameProbe; if (window.__handoffOriginalAnimate) Element.prototype.animate = window.__handoffOriginalAnimate; if (window.__handoffOriginalAppend) Element.prototype.append = window.__handoffOriginalAppend; if (window.__handoffOriginalRemove) Element.prototype.remove = window.__handoffOriginalRemove; return window.__handoffReview.frames; });
}

function assertDissolve(style, label) {
  assert(style, label + ' must expose measured compositor styles');
  assert.equal(style.isolation, 'isolate', label + ' must isolate its additive children');
  assert(Math.abs(style.hostOpacity - 1) < 0.001, label + ' host must stay fully opaque');
  assert.equal(style.liveBlend, 'plus-lighter', label + ' live child must use plus-lighter');
  assert.equal(style.posterBlend, 'plus-lighter', label + ' bitmap child must use plus-lighter');
  assert(style.liveOpacity >= 0 && style.liveOpacity <= 1 && style.posterOpacity >= 0 && style.posterOpacity <= 1,
    label + ' child weights must stay bounded');
  assert(Math.abs(style.liveOpacity + style.posterOpacity - 1) < 0.001, label + ' child weights must be complementary');
}

function assertReturnDissolve(style, label, aligned = false, firstDrawReveal = null) {
  assert(style, label + ' must expose actual composite weights and styles');
  assert(Math.abs(style.hostOpacity - 1) < 0.001, label + ' host stays fully opaque');
  assert(style.liveAttached, label + ' keeps the actual WebGL canvas attached');
  assert.equal(style.legacyPosterCount, 0, label + ' must not retain a separate return-poster');
  assert.equal(style.liveBlend, 'normal', label + ' does not use additive CSS live children');
  assert(style.liveOpacity >= 0 && style.liveOpacity <= 1 && style.posterOpacity >= 0 && style.posterOpacity <= 1);
  assert(Math.abs(style.liveOpacity + style.posterOpacity - 1) < 0.000001, label + ' logical weights are complementary');
  assert.equal(style.liveOpacity, style.advertisedOpacity, label + ' reports the actual logical live weight');
  assert(style.originImage, label + ' uses the original card IMG as its upper source');
  assert.deepEqual(style.originDimensions, [768, 768], label + ' uses the decoded canonical origin image');
  if (aligned) {
    assert.equal(style.compositeCount, 1, label + ' presents exactly one composite');
    assert(style.compositeCanvas && style.compositeVisibility === 'visible');
    assert.equal(style.compositeOpacity, 1, label + ' presents the fully opaque 2D surface');
    assert.equal(style.compositeBlend, 'normal', label + ' uses canvas lighter rather than CSS blending');
    assert.equal(style.liveVisibility, 'hidden', label + ' hides the attached WebGL canvas only after capture');
    assert(style.compositeDimensions.every(side => side > 0 && side <= 1024), label + ' bounds immutable composite pixels');
  } else {
    assert.equal(style.compositeCount, 0, label + ' travels using the actual live canvas');
    if (style.liveVisibility === 'hidden' && firstDrawReveal) {
      assert.deepEqual(firstDrawReveal, { visibility: 'visible', sameHost: true, compositeCount: 0 },
        label + ' reveals the first synchronous draw in the same task before paint');
    } else assert.equal(style.liveVisibility, 'visible', label + ' keeps travelling WebGL pixels visible');
    assert.equal(style.liveCSSOpacity, 1);
  }
}

async function dynamicContinuity(page, caseReport, frames, options = {}) {
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
    const dissolves = samples.filter(frame => frame.dissolve && !frame.flight);
    for (const frame of dissolves) assertDissolve(frame.dissolve, phase + ' handoff');
    if (options.reducedMotion !== 'reduce' && samples.some(frame => frame.flight) && dissolves.length) {
      assert(dissolves.some(frame => frame.sampledBy === 'raf' && frame.dissolve.liveOpacity > 0 && frame.dissolve.liveOpacity < 1), phase + ' must sample the real complementary opening fade');
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

async function canonicalReturnCoverage(page, label, caseReport, canonical, beforeClose, options) {
  const evidence = await page.evaluate(() => { window.__handoffReview.flushReturnCaptures(); return { draws: window.__handoffReview.returnDraws, endpoint: window.__handoffReview.returnEndpoint, firstComposite: window.__handoffReview.firstComposite }; });
  caseReport.canonical_return = { draws: evidence.draws, endpoint: evidence.endpoint?.draw || null, same_task_capture: evidence.firstComposite || null };
  if (options.reducedMotion === 'reduce') {
    assert(evidence.draws.every(draw => draw.progress === 0 || draw.progress === 1), 'Reduced motion skips intermediate camera return poses');
    // Synchronous endpoint draws may occur inside one unpainted task; no motion
    // may survive into the browser-painted RAF sequence.
    return;
  }
  const draws = evidence.draws;
  assert(draws.length > 2, 'Ordinary close must draw the actual live model while returning');
  assert(draws.every(draw => draw.actualSharedCanvas), 'Every returning draw uses the original shared WebGL canvas');
  const first = draws[0], last = draws.at(-1), intermediate = draws.filter(draw => draw.progress > 0 && draw.progress < 1);
  assert.equal(first.progress, 0, 'The first returning frame begins at the inspected pose');
  assert(intermediate.length > 0, 'Camera return must include an actual intermediate draw before the canonical endpoint');
  const expectedAngleStep = ((canonical.azimuth - beforeClose.azimuth + 540) % 360) - 180;
  for (let i = 0; i < draws.length; i++) {
    const draw = draws[i], p = draw.progress, k = 1 - (1 - p) ** 3;
    assert(Number.isFinite(p) && p >= 0 && p <= 1, 'Each real return draw advertises bounded analytic progress');
    assert(!i || p >= draws[i - 1].progress, 'Return progress must never move backwards');
    assert(deltaAngle(draw.view.azimuth_deg, beforeClose.azimuth + expectedAngleStep * k) < 0.001,
      'Actual rendered camera azimuth must follow shortest-arc cubic interpolation');
    assert(Math.abs(draw.view.elevation_deg - (beforeClose.elevation + (canonical.elevation - beforeClose.elevation) * k)) < 0.001,
      'Actual rendered camera elevation must follow cubic interpolation');
    assert(Math.abs(draw.view.distance - (beforeClose.distance + (canonical.distance - beforeClose.distance) * k)) < 0.00001,
      'Actual rendered camera distance must follow cubic interpolation');
    assert(draw.alpha.transparent_fraction > 0.2 && draw.alpha.corner_alpha_max <= 3, 'Every live return frame preserves transparent surrounding pixels');
    assertReturnDissolve(draw.dissolve, 'actual live return draw', false, i === 0 && p === 0 ? draw.afterDrawReveal : null);
    assert(draw.originHidden, 'The origin card IMG stays hidden until the final swap');
    assert.equal(draw.dissolve.liveOpacity, 1, 'Canonical capture occurs before the logical fade starts');
    if (p < 1) {
      assert.equal(draw.returnPhase, 'moving');
      assert(draw.originHidden, 'The origin card poster stays hidden throughout the moving return');
      assert(Math.abs(draw.opacity - 1) < 0.001, 'The current pose remains fully visible while moving');
    } else {
      assert.equal(draw.returnPhase, 'fading');
    }
  }
  assert(deltaAngle(first.view.azimuth_deg, beforeClose.azimuth) < 0.001 && Math.abs(first.view.distance - beforeClose.distance) < 0.00001,
    'Closing must not instantly reset the inspected pose');
  assert(deltaAngle(last.view.azimuth_deg, canonical.azimuth) < 0.001 && Math.abs(last.view.elevation_deg - canonical.elevation) < 0.001 && Math.abs(last.view.distance - canonical.distance) < 0.00001,
    'The actual live camera must reach the canonical poster pose before detaching');
  assert(evidence.endpoint?.png, 'Canonical endpoint pixels must come from the actual synchronous WebGL draw');
  assert(evidence.firstComposite, 'The same-task first displayed composite must be captured');
  assert(evidence.firstComposite.sameTask, 'Initial composite is captured synchronously at onAligned append');
  assert.equal(evidence.firstComposite.weight, 1, 'The first composite preserves the full raw canonical draw');
  assert.deepEqual(evidence.firstComposite.canonicalPixels, evidence.endpoint.draw.pixels, 'Capture identity originates in the exact synchronous canonical draw');
  assert.deepEqual(evidence.firstComposite.pixels, evidence.endpoint.draw.pixels, 'Raw same-task canonical pixels enter the first composite unchanged');
  if (options.returnStyles) {
    assert.equal(first.styleResources.referenceObjects, 1, 'The first returning draw preserves the inspected scale reference');
    assert(intermediate.some(draw => draw.styleResources.returnOverlayMeshes > 0 && draw.styleResources.returnOverlayMaterials > 0), 'Styled close must actually blend its original wireframe layer during camera travel');
    assert.equal(last.styleResources.referenceObjects, 0, 'Canonical endpoint removes the scale reference before fading');
    assert.equal(last.styleResources.returnOverlayMeshes, 0, 'Canonical endpoint removes temporary wireframe meshes before fading');
    assert.equal(last.styleResources.returnOverlayMaterials, 0, 'Canonical endpoint disposes temporary wireframe materials before fading');
  }
  const parity = await page.evaluate(async ({ png, posterSrc, projectionSize }) => {
    const size = 320, load = async src => { const image = new Image(); image.src = src; await image.decode(); return image; };
    const [actualImage, poster] = await Promise.all([load(png), load(posterSrc)]);
    const normalize = image => {
      const canvas = document.createElement('canvas'); canvas.width = canvas.height = size;
      const side = Math.min(image.naturalWidth, image.naturalHeight), context = canvas.getContext('2d');
      context.drawImage(image, (image.naturalWidth - side) / 2, (image.naturalHeight - side) / 2, side, side, 0, 0, size, size);
      const pixels = context.getImageData(0, 0, size, size).data;
      let left = size, right = -1, top = size, bottom = -1, count = 0, sx = 0, sy = 0, transparent = 0;
      for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
        const alpha = pixels[(y * size + x) * 4 + 3];
        if (alpha <= 3) transparent++;
        if (alpha <= 16) continue;
        left = Math.min(left, x); right = Math.max(right, x); top = Math.min(top, y); bottom = Math.max(bottom, y); count++; sx += x; sy += y;
      }
      return { canvas, pixels, foreground: { bbox: { left, top, right, bottom }, centroid: { x: sx / count, y: sy / count }, pixels: count },
        alpha: { transparent_fraction: transparent / (size * size), corner_alpha_max: Math.max(pixels[3], pixels[(size - 1) * 4 + 3], pixels[((size - 1) * size) * 4 + 3], pixels.at(-1)) } };
    };
    // Screen-space alignment must compare the same alpha-weighted pixel-center
    // statistic at the same raster footprint as the synchronously captured draw.
    // Keep the independent 320 px unweighted pixel-parity oracle unchanged.
    const projectionCanvas = document.createElement('canvas');
    [projectionCanvas.width, projectionCanvas.height] = projectionSize;
    const projectionContext = projectionCanvas.getContext('2d');
    projectionContext.drawImage(poster, 0, 0, ...projectionSize);
    const projectionPixels = projectionContext.getImageData(0, 0, ...projectionSize).data;
    const [pw, ph] = projectionSize;
    let pl = pw, pr = -1, pt = ph, pb = -1, weight = 0, cx = 0, cy = 0;
    for (let y = 0; y < ph; y++) for (let x = 0; x < pw; x++) {
      const alpha = projectionPixels[(y * pw + x) * 4 + 3];
      if (alpha <= 16) continue;
      pl = Math.min(pl, x); pr = Math.max(pr, x); pt = Math.min(pt, y); pb = Math.max(pb, y);
      weight += alpha; cx += (x + 0.5) * alpha; cy += (y + 0.5) * alpha;
    }
    const posterProjection = { sampled: projectionSize, bbox: { left: pl / pw, top: pt / ph, right: (pr + 1) / pw, bottom: (pb + 1) / ph },
      centroid: { x: cx / weight / pw, y: cy / weight / ph } };
    const actual = normalize(actualImage), expected = normalize(poster);
    // Composite both transparent sources on the same white backing. Alpha-aware
    // RGB comparison excludes undefined RGB in fully transparent WebP pixels.
    let error = 0;
    for (let i = 0; i < actual.pixels.length; i += 4) for (let c = 0; c < 3; c++) {
      const a = actual.pixels[i + 3] / 255, b = expected.pixels[i + 3] / 255;
      error += Math.abs(actual.pixels[i + c] * a + 255 * (1 - a) - expected.pixels[i + c] * b - 255 * (1 - b));
    }
    return { posterSrc, posterDimensions: [poster.naturalWidth, poster.naturalHeight], normalizedSize: size,
      mean_rgb_absolute_error: error / (size * size * 3 * 255),
      bbox_delta_px: Math.max(...Object.keys(actual.foreground.bbox).map(key => Math.abs(actual.foreground.bbox[key] - expected.foreground.bbox[key]))),
      centroid_delta_px: Math.hypot(actual.foreground.centroid.x - expected.foreground.centroid.x, actual.foreground.centroid.y - expected.foreground.centroid.y),
      actualForeground: actual.foreground, expectedForeground: expected.foreground, liveAlpha: actual.alpha, posterAlpha: expected.alpha, posterProjection,
      actual_png: actual.canvas.toDataURL('image/png'), poster_png: expected.canvas.toDataURL('image/png') };
  }, { png: evidence.endpoint.png, posterSrc: caseReport.returned.src, projectionSize: evidence.endpoint.draw.alpha.sampled });
  const { actual_png, poster_png, ...measurements } = parity;
  caseReport.canonical_return.pixel_parity = measurements;
  await writeFile(resolve(output, label + '-canonical-live-endpoint.png'), Buffer.from(actual_png.split(',')[1], 'base64'));
  await writeFile(resolve(output, label + '-canonical-poster-reference.png'), Buffer.from(poster_png.split(',')[1], 'base64'));
  report.screenshots.push(label + '-canonical-live-endpoint.png', label + '-canonical-poster-reference.png');
  assert(measurements.actualForeground.pixels > 100 && measurements.expectedForeground.pixels > 100, 'Canonical parity measures a real model silhouette');
  assert(measurements.liveAlpha.transparent_fraction > 0.2 && measurements.liveAlpha.corner_alpha_max <= 3, 'The live canonical endpoint must retain true alpha');
  assert(measurements.posterAlpha.transparent_fraction > 0.2 && measurements.posterAlpha.corner_alpha_max <= 3, 'Normal browsing must use a transparent canonical poster');
  assert(measurements.mean_rgb_absolute_error < 0.04, 'The actual live canonical endpoint must match the visible poster lighting and pixels');
  assert(measurements.bbox_delta_px <= 8, 'The actual canonical endpoint silhouette must match the poster within 8 pixels');
  assert(measurements.centroid_delta_px <= 8, 'The actual canonical endpoint center must match the poster within 8 pixels');
  const endpoint = evidence.endpoint.draw.object, reference = measurements.posterProjection, returned = caseReport.returned;
  assert.deepEqual(reference.sampled, evidence.endpoint.draw.alpha.sampled, 'Live and poster alignment use the same raster footprint');
  const expectedOnCard = {
    x: returned.x + (reference.centroid.x - 0.5) * returned.square,
    y: returned.y + (reference.centroid.y - 0.5) * returned.square,
    width: (reference.bbox.right - reference.bbox.left) * returned.square,
    height: (reference.bbox.bottom - reference.bbox.top) * returned.square,
  };
  const alignment = { center_step_px: Math.hypot(endpoint.x - expectedOnCard.x, endpoint.y - expectedOnCard.y),
    scale_step: Math.max(Math.abs(endpoint.width / expectedOnCard.width - 1), Math.abs(endpoint.height / expectedOnCard.height - 1)) };
  caseReport.canonical_return.poster_alignment = alignment;
  assert(alignment.center_step_px <= 3, 'The canonical live endpoint must align with the poster model center before fading');
  assert(alignment.scale_step <= 0.03, 'The canonical live endpoint must align with the poster silhouette scale before fading');
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
  const context = await makeContext(label, { ...options, returnTiming: true }); const { page } = context;
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
    await page.waitForFunction(() => Boolean(window.__handoffReview.openingHandoff), null, { timeout: 30000 });
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
    const canonical = { azimuth: CARD_RENDER_PRESET.camera.azimuth_deg, elevation: CARD_RENDER_PRESET.camera.elevation_deg, distance: initial.distance };
    caseReport.canonical = canonical;
    assert(deltaAngle(initial.azimuth, 147) < 0.001, 'The 7/24 preview angle enters actual 3D unchanged');
    await page.waitForTimeout(350);
    await page.waitForFunction(() => !document.querySelector('#canvas-host .model-handoff') && !document.querySelector('.stage-flight'));
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    const openingCleanup = await page.locator('#canvas-host .model-canvas').evaluate(canvas => ({
      opacity: Number(getComputedStyle(canvas).opacity), animations: canvas.getAnimations().length,
      blend: getComputedStyle(canvas).mixBlendMode,
    }));
    assert.deepEqual(openingCleanup, { opacity: 1, animations: 0, blend: 'normal' }, 'Opening must retire both complementary animations and release the additive child styling');
    const opening = await page.evaluate(() => { window.__handoffReview.flushOpeningCaptures(); return window.__handoffReview.openingHandoff; });
    assert(opening.copied, 'The opening handoff copies the current draw so the shared WebGL canvas can attach to detail');
    caseReport.handoff_pixels = opening.pixels;
    assert.deepEqual(caseReport.handoff_pixels, caseReport.preview_pixels, 'The exact currently painted card pixels must enter the detail handoff');
    assert(caseReport.handoff_pixels.transparent_fraction > 0.2 && caseReport.handoff_pixels.corner_alpha_max <= 3, 'The initial handoff must not contain a baked opaque background');
    await page.evaluate(() => { window.__handoffReview.phase = 'inspect'; });
    await pixelParity(page, label, caseReport);
    await page.evaluate(() => { window.__handoffReview.phase = 'interact'; });
    await page.locator('#canvas-host').focus(); await page.keyboard.press('ArrowRight'); await page.keyboard.press('ArrowUp');
    await page.waitForFunction(previous => Math.abs(Number(document.querySelector('#canvas-host').dataset.viewAzimuth) - previous) > 0.1, initial.azimuth);
    await page.locator('#zoom-in').click();
    await page.waitForFunction(previous => Number(document.querySelector('#canvas-host').dataset.viewDistance) < previous * 0.99, initial.distance);
    if (options.returnStyles) {
      await page.locator('#wireframe').click(); await page.locator('#scale-reference').click();
      await page.waitForFunction(() => document.querySelector('#wireframe').ariaPressed === 'true' && document.querySelector('#scale-reference').ariaPressed === 'true' && window.__vaultGPU.referenceObjects === 1);
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    }
    const beforeClose = await angles(page);
    caseReport.beforeClose = beforeClose;
    await screenshot(page, label + '-detail-before-close');
    await page.evaluate(() => { window.__handoffReview.phase = 'close'; });
    await page.locator('#close').click(); await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open);
    await page.waitForTimeout(150);
    assert(await card.evaluate(node => node === window.__originalReviewCard), 'Same-list close keeps the original card DOM');
    await page.waitForFunction(() => !document.querySelector('.stage-flight, [data-detail-origin]'));
    assert.equal(await card.locator('.model-preview-snapshot, .model-canvas').count(), 0, 'Completed close leaves only the canonical poster on the card');
    const returned = await card.locator('.asset-image > img').evaluate(node => {
      const r = node.getBoundingClientRect();
      return { square: Math.min(r.width, r.height), x: r.x + r.width / 2, y: r.y + r.height / 2,
        src: node.currentSrc, visible: getComputedStyle(node).visibility, loaded: node.complete && node.naturalWidth > 0 };
    });
    assert(returned.loaded && returned.visible === 'visible', 'Completed close reveals the decoded canonical poster');
    assert.equal(await page.evaluate(() => document.activeElement?.dataset.id), 'natural-arch');
    caseReport.returned = returned;
    caseReport.afterClose = await previewDiagnostics(page);
    assert.equal(caseReport.afterClose.preview.activeId, null, 'Completed close releases preview.current');
    assert.equal(caseReport.afterClose.gpu.liveScenes, 0, 'Completed close detaches the live model scene');
    assert.equal(caseReport.afterClose.gpu.rendererCreations, caseReport.preview_resources.rendererCreations, 'Returning the actual model must not allocate a renderer');
    assert.equal(caseReport.afterClose.gpu.parseCount, caseReport.preview_resources.parseCount, 'Returning the actual model must not decode another scene');
    assert.equal(caseReport.afterClose.gpu.networkRequests, caseReport.preview_resources.networkRequests, 'Returning the actual model must not fetch a model again');
    assert.equal(caseReport.afterClose.card.canvases, 0, 'Normal browsing keeps no returned bitmap or live canvas');
    await canonicalReturnCoverage(page, label, caseReport, canonical, beforeClose, options);
    await screenshot(page, label + '-canonical-poster-card');
    caseReport.beforeReopen = await previewDiagnostics(page);
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

    assert(deltaAngle(canonical.azimuth, reopened.azimuth) < 0.001, 'Reopening from the canonical poster starts at its azimuth');
    assert(Math.abs(canonical.elevation - reopened.elevation) < 0.001, 'Reopening from the canonical poster starts at its elevation');
    assert(Math.abs(canonical.distance - reopened.distance) < 0.00001, 'Reopening from the canonical poster starts at its fitted distance');
    const frames = await endSampler(page), closeFlights = frames.filter(frame => frame.phase === 'close' && frame.flight);
    caseReport.frames = frames;
    await dynamicContinuity(page, caseReport, frames, options);
    assert.equal(frames.filter(frame => !frame.hasVisual).length, 0, 'Open/close/reopen must never show an empty visual frame');
    if (options.reducedMotion !== 'reduce') {
      assert(closeFlights.length > 1, 'The ordinary-motion return must actually animate');
      assert(closeFlights.every(frame => frame.flight.kind === 'live-return' && frame.flight.actualSharedCanvas), 'Close animates the actual shared live model inside a DIV');
      const aligned = closeFlights.filter(frame => frame.flight.progress === 1 && frame.flight.returnPhase === 'fading');
      assert(aligned.length > 0 && aligned.every(frame => frame.flight.dissolve.compositeVisibility === 'visible'), 'Aligned fade exposes the actual single return-composite');
      assert(closeFlights.every(frame => frame.flight.originHidden && !frame.originPosterVisible), 'The original card IMG stays hidden throughout the flight and dissolve');
      for (const frame of closeFlights) assertReturnDissolve(frame.flight.dissolve, 'painted live return', frame.flight.returnPhase === 'fading');
      assert(aligned.some(frame => frame.sampledBy === 'raf' && frame.flight.opacity > 0 && frame.flight.opacity < 1), 'Aligned fade must actually paint a real RAF sample with partial logical weights in the single composite');
      const masses = aligned.filter(frame => frame.flight.opacity > 0 && frame.flight.opacity < 1).map(frame => frame.flight.alpha_mass);
      assert(masses.length > 0 && masses.every(Boolean), 'Partial fade alpha mass must use captured actual displayed composite pixels');
      caseReport.alpha_preserving_dissolve = { source: masses[0].source, samples: masses, tolerance: 'two alpha-byte errors per covered pixel, divided by every raster pixel' };
      for (const mass of masses) {
        assert(mass.denominator_pixels > 0, 'Alpha mass keeps every pixel in its unchanged raster denominator');
        assert(Math.abs(mass.actual - mass.expected) <= mass.quantization_tolerance + 1e-9, 'Actual-composite lighter alpha mass must follow the weighted endpoints without a hump or dip');
        assert(mass.actual >= Math.min(mass.live, mass.poster) - mass.quantization_tolerance - 1e-9 && mass.actual <= Math.max(mass.live, mass.poster) + mass.quantization_tolerance + 1e-9, 'Dissolve alpha mass must stay inside its actual endpoint envelope');
      }
      const fading = aligned.map(frame => frame.flight.opacity);
      assert(fading.every(opacity => opacity >= 0 && opacity <= 1), 'Aligned logical live weight stays bounded during the fade');
      assert.equal(frames.filter(frame => frame.flight && frame.stationaryVisible).length, 0, 'A flying model must not duplicate a stationary model behind it');
      const last = closeFlights.at(-1).flight;
      assert(Math.abs(last.square / returned.square - 1) < 0.12, 'Live return scale must match the canonical poster at completion');
      assert(Math.hypot(last.x - returned.x, last.y - returned.y) < 12, 'Live return center must match the canonical poster');
    } else {
      assert.equal(closeFlights.filter(frame => frame.sampledBy === 'raf').length, 0, 'Reduced motion paints the canonical poster immediately without an animated flight');
    }
    Object.assign(caseReport, { status: 'pass', frames });
    report.checks.push(`${label}: current-hover open, real 3D camera return, canonical poster pixel/framing match, no blank frame, and renderer/resource reuse.`);
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
    await catalog(page); await page.locator('#grid [data-id="conifer-tree"]').click(); await ready(page, 'conifer-tree');
    await page.waitForFunction(() => !document.querySelector('.stage-flight, .model-handoff'));
    await page.locator('#close').click(); await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open);
    await page.waitForFunction(() => document.querySelector('#grid')?.getAttribute('aria-busy') === 'false' && !document.querySelector('.stage-flight'));
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
    // Filter replaces the catalog entry, retaining the intended home → catalog → detail Back history.
    await page.locator('.catalog-refine summary').click();await page.locator('#pack-filter').selectOption('prehistoric-starter');
    await page.waitForFunction(() => document.querySelector('#grid')?.getAttribute('aria-busy') === 'false');await page.locator('.catalog-refine summary').click();
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

async function interruptedCanonicalReturn(returnPhase = 'moving') {
  const label = 'interrupted-canonical-return-' + returnPhase, context = await makeContext(label, { returnTiming: true }), { page } = context;
  const caseReport = { label, status: 'running' }; report.cases.push(caseReport);
  try {
    await catalog(page);
    const card = page.locator('#grid .asset-card[data-id="natural-arch"]');
    await card.scrollIntoViewIfNeeded(); await card.focus(); await startSampler(page);
    await page.keyboard.press('Home');
    for (let i = 0; i < 7; i++) await page.keyboard.press('ArrowRight');
    await page.waitForFunction(() => Number(document.querySelector('#grid [data-id="natural-arch"]').dataset.previewAzimuth) === 147);
    await page.evaluate(() => {
      window.__originalReviewCard = document.querySelector('#grid [data-id="natural-arch"]');
      window.__openingCardSurface = window.__originalReviewCard.querySelector('.model-canvas');
      window.__handoffReview.phase = 'open';
    });
    await page.keyboard.press('Enter'); await ready(page, 'natural-arch');
    await page.waitForFunction(() => !document.querySelector('.stage-flight, #canvas-host .model-handoff'));
    await page.locator('#canvas-host').focus(); await page.keyboard.press('ArrowRight'); await page.keyboard.press('ArrowUp'); await page.locator('#zoom-in').click();
    caseReport.inspected = await angles(page);
    const resources = await page.evaluate(() => ({ ...window.__vaultGPU }));
    await page.evaluate(returnPhase => {
      // Reverse from the first measured intermediate draw, so the assertion
      // targets real camera state rather than a guessed timeout on a slow GPU.
      if (returnPhase === 'moving') window.__reverseReturnAtProgress = 0.01;
      else window.__reverseReturnPhase = 'fading';
      window.__handoffReview.phase = 'close'; history.back();
    }, returnPhase);
    await page.waitForFunction(() => window.__handoffReview.reversalRequested, null, { timeout: 5000 });
    await page.waitForURL(base + prefix + 'models/natural-arch/'); await ready(page, 'natural-arch');
    await page.waitForFunction(() => !document.querySelector('.stage-flight, #canvas-host .model-handoff'));
    await page.waitForTimeout(80);
    const frames = await endSampler(page);
    const evidence = await page.evaluate(() => ({ returns: window.__handoffReview.returnDraws, draws: window.__handoffReview.draws,
      handoff: window.__handoffReview.reversalHandoff, visible: window.__handoffReview.reversalVisible, errors: window.__handoffReview.probe_errors, gpu: { ...window.__vaultGPU } }));
    Object.assign(caseReport, { frames, ...evidence });
    assert.deepEqual(evidence.errors, []);
    const lastReturn = evidence.returns.at(-1), displayedReturn = evidence.visible, firstReopened = evidence.draws.find(draw => draw.phase === 'reversal');
    if (returnPhase === 'moving') assert(lastReturn?.progress > 0 && lastReturn.progress < 1, 'Forward must interrupt an actual intermediate camera pose');
    else assert(displayedReturn?.returnPhase === 'fading' && displayedReturn.progress === 1 && displayedReturn.opacity > 0 && displayedReturn.opacity < 1, 'Forward must interrupt the actual aligned partially weighted displayed composite');
    assert(firstReopened, 'Interrupted Forward must produce an actual live detail draw');
    assert(deltaAngle(lastReturn.view.azimuth_deg, firstReopened.view.azimuth_deg) < 0.001, 'Reversal preserves the actual intermediate azimuth');
    assert(Math.abs(lastReturn.view.elevation_deg - firstReopened.view.elevation_deg) < 0.001, 'Reversal preserves the actual intermediate elevation');
    assert(Math.abs(lastReturn.view.distance - firstReopened.view.distance) < 0.00001, 'Reversal preserves the actual intermediate camera distance');
    assert(evidence.handoff?.copied, 'Reversal retains a copy of the real intermediate draw while reparenting the shared canvas');
    if (returnPhase === 'moving') assert.deepEqual(evidence.handoff.pixels, lastReturn.pixels, 'The exact intermediate rendered pixels enter the reversal handoff');
    else {
      assert(displayedReturn.visiblePixels && displayedReturn.visibleAlpha, 'Fade reversal captures the actual displayed return-composite');
      assert.deepEqual(evidence.handoff.pixels, displayedReturn.visiblePixels, 'The exact visible composite enters the fade reversal handoff');
      const before = displayedReturn.visibleAlpha, after = evidence.handoff.alpha;
      const bboxDelta = Math.max(...Object.keys(before.bbox).map(key => Math.abs(before.bbox[key] - after.bbox[key]) * 320));
      const centroidDelta = Math.hypot(before.centroid.x - after.centroid.x, before.centroid.y - after.centroid.y) * 320;
      caseReport.composite_continuity = { bbox_delta_px: bboxDelta, centroid_delta_px: centroidDelta,
        rgba_hash: displayedReturn.visiblePixels.rgba_hash, live_opacity: displayedReturn.opacity };
      assert(before.transparent_fraction > 0.2 && after.transparent_fraction > 0.2 && before.corner_alpha_max <= 3 && after.corner_alpha_max <= 3, 'Both fade composite and reversal handoff preserve true alpha');
      assert(bboxDelta <= 8 && centroidDelta <= 8, 'Fade composite silhouette and center retain strict pixel parity');
      const a = firstReopened.overlay?.object, b = firstReopened.object;
      assert(a && b, 'Fade reversal measures the composite handoff and first actual model draw');
      const center = Math.hypot(a.x - b.x, a.y - b.y), scale = Math.max(Math.abs(a.width / b.width - 1), Math.abs(a.height / b.height - 1));
      Object.assign(caseReport.composite_continuity, { handoff_to_live_center_step_px: center, handoff_to_live_scale_step: scale });
      assert(center <= 3 && scale <= 0.03, 'Fade reversal composite aligns with its first actual live draw within 3px and 3%');
    }
    assert.equal(frames.filter(frame => !frame.hasVisual).length, 0, 'Interrupted return/Forward must never paint an empty visual frame');
    assert(await page.locator('#canvas-host .model-canvas').evaluate(canvas => canvas === window.__openingCardSurface), 'Reversal reattaches the same actual shared canvas');
    assert.equal(evidence.gpu.liveScenes, 1); assert.equal(evidence.gpu.rendererCreations, resources.rendererCreations);
    assert.equal(evidence.gpu.parseCount, resources.parseCount); assert.equal(evidence.gpu.networkRequests, resources.networkRequests);
    assert.equal(await page.locator('.model-preview-snapshot, .live-model-return').count(), 0, 'Cancelled return leaves no stale bitmap or live flight');
    const reversalCleanup = await page.locator('#canvas-host .model-canvas').evaluate(canvas => ({
      opacity: Number(getComputedStyle(canvas).opacity), animations: canvas.getAnimations().length,
      blend: getComputedStyle(canvas).mixBlendMode,
    }));
    assert.deepEqual(reversalCleanup, { opacity: 1, animations: 0, blend: 'normal' }, 'Reversal must clean up both complementary handoff animations');
    caseReport.status = 'pass';
    report.checks.push(`Forward during canonical ${returnPhase} preserves the actual camera and exact visible handoff pixels while reusing one canvas, renderer, and decoded resource.`);
  } catch (error) {
    caseReport.status = 'fail'; caseReport.error = error.stack;
    caseReport.frames = await endSampler(page).catch(() => []); throw error;
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
  browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', ...(cpuDOMRaster ? ['--disable-gpu-rasterization'] : [])] });
  report.chromium_version = browser.version();
  await directDetails();
  await roundTrip('desktop-motion');
  if (process.env.QA_HANDOFF_SMOKE !== '1') {
  await roundTrip('desktop-styled-motion', { returnStyles: true });
  await roundTrip('desktop-retina-motion', { deviceScaleFactor: 2 });
  await roundTrip('mobile-motion', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await roundTrip('desktop-reduced-motion', { reducedMotion: 'reduce' });
  await roundTrip('desktop-dark-motion', { colorScheme: 'dark' });
  await contextLossRecovery();
  await earlyLoadFailure();
  await interruptedHistory();
  await interruptedCanonicalReturn();
  await interruptedCanonicalReturn('fading');
  await supersededImport();
  }
  report.scope = process.env.QA_HANDOFF_SMOKE === '1' ? 'smoke-direct-and-desktop-roundtrip' : 'full';
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

/**
 * Real Chromium regression/evidence for modal chrome, shared live-model return,
 * and canonical transparent-poster coordination.
 * Run after the normal production build:
 *   QA_OUTPUT_DIR=qa/modal-motion node site/modal-motion-browser-test.mjs
 * Run this identical file against the previous build with BASELINE=1. Baseline mode
 * records (but does not enforce) the new motion contract; navigation still must work.
 * GALLERY_DIR, CHROMIUM_PATH and optional BASELINE_REPORT are supported.
 * QA_CASES selects a comma-separated local diagnostic scope, declared in reports;
 * CI leaves it unset. QA_TRACE_RASTER records the separate history timing pass.
 * Timing comes from capture-phase DOM input events and requestAnimationFrame, never
 * from how long a Playwright click takes. Compositor PNG evidence is a separate pass.
 */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep, basename } from 'node:path';
import assert from 'node:assert/strict';
import { CARD_RENDER_PRESET } from './render-preset.js';

const root = resolve(process.env.GALLERY_DIR || 'dist');
const output = resolve(process.env.QA_OUTPUT_DIR || 'qa/modal-motion');
const baseline = /^(1|true)$/i.test(process.env.BASELINE || '');
const traceRaster = /^(1|true)$/i.test(process.env.QA_TRACE_RASTER || '');
// Keep the actual GLB in SwiftShader, but raster DOM content with Skia's CPU
// path. Software GPU DOM raster batches can block the shared queue for hundreds
// of ms before WebGL is allowed to draw. QA_CPU_DOM_RASTER=0 retains the control.
const cpuDOMRaster = !/^(0|false)$/i.test(process.env.QA_CPU_DOM_RASTER || '1');
const onlyCases = (process.env.QA_CASES || '').split(',').map(value => value.trim()).filter(Boolean);
const prefix = '/lowpoly-vault/';
const cardSelector = '#grid .asset-card[data-id="natural-arch"]';
const report = {
  status: 'running', mode: baseline ? 'baseline' : 'regression', commit: process.env.GITHUB_SHA || null,
  scope: onlyCases.length ? onlyCases : 'full',
  dom_raster_mode: cpuDOMRaster ? 'cpu' : 'browser-default',
  targets_ms: { chrome_open: 240, all_content_open: 300, chrome_close: 140, return_move: 120, canonical_fade: 60, reverse_flight: 180 },
  note: 'Actual Chromium rAF/computed-style/alpha measurements, software WebGL, and trusted emulated touch input. Not physical-device performance. Real-time video runs in separate contexts from timing assertions. Pixel/GLB geometry is covered by the independent handoff browser regression, avoiding readback stalls in motion evidence.',
  cases: [], page_errors: [], screenshots: [], videos: [],
};
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.webp': 'image/webp', '.glb': 'model/gltf-binary', '.svg': 'image/svg+xml' };
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
let browser, base;

// Installed before the app. The draw hook reads pixels synchronously before the
// non-preserved WebGL buffer clears; ordinary rAF sampling only reads cached alpha.
function installProbe() {
  let active = false, raf, observer, phase, pixelProbe = false, previousDrawProbe;
  let frames = [], events = [], draws = [], bitmapDraws = [], errors = [];
  const lastDraw = new WeakMap(), capture = new WeakMap();
  let nextDrawId = 0;
  const longTasks = [];
  if (PerformanceObserver.supportedEntryTypes.includes('longtask')) {
    new PerformanceObserver(list => { for (const entry of list.getEntries()) longTasks.push({ start: entry.startTime, duration: entry.duration }); }).observe({ type: 'longtask', buffered: true });
  }
  const alphaCache = new WeakMap();
  const viewCache = new WeakMap(), elementIds = new WeakMap();
  let nextElementId = 0;
  const elementId = element => {
    if (!element) return null;
    if (!elementIds.has(element)) elementIds.set(element, ++nextElementId);
    return elementIds.get(element);
  };
  const view = element => {
    if (!element) return null;
    const canvas = element.matches('.model-canvas') ? element : element.querySelector('.model-canvas');
    if (canvas && viewCache.has(canvas)) return viewCache.get(canvas);
    if (element.__presentation) return { ...element.__presentation };
    // An idle model may not draw after arming. Its last rendered camera is
    // published on the owning host, rather than on the shared canvas itself.
    const host = canvas?.parentElement || element;
    if (!host.dataset.viewDistance) return null;
    return { azimuth_deg: Number(host.dataset.viewAzimuth), elevation_deg: Number(host.dataset.viewElevation), distance: Number(host.dataset.viewDistance) };
  };
  const scratch = document.createElement('canvas');
  // Lightweight identity/weight tracing, with no pixel readback in timing runs.
  // A same-task copy must still refer to the exact synchronous canonical draw.
  const nativeDrawImage = CanvasRenderingContext2D.prototype.drawImage;
  CanvasRenderingContext2D.prototype.drawImage = function (source, ...args) {
    const result = nativeDrawImage.call(this, source, ...args);
    if (!active || this.canvas === scratch) return result;
    const live = source?.classList?.contains('model-canvas') && source.parentElement?.classList.contains('stage-flight');
    const origin = source?.matches?.('#grid [data-id="natural-arch"] .asset-image > img');
    const retained = capture.get(source), composite = source?.classList?.contains('return-composite');
    if (live || retained || composite || this.canvas.classList.contains('return-composite') || origin) {
      const draw = lastDraw.get(source);
      const copied = live ? { draw_id: draw?.draw_id, draw_time: draw?.time, same_task: draw?.same_task === true,
        canvas_id: elementId(source), source_size: [source.width, source.height] } : retained || null;
      if (copied) capture.set(this.canvas, copied);
      bitmapDraws.push({ time: performance.now(), target_id: elementId(this.canvas), source_id: elementId(source),
        source_kind: live ? 'live' : composite ? 'composite' : origin ? 'origin-img' : 'retained',
        target_size: [this.canvas.width, this.canvas.height], args, weight: this.globalAlpha,
        operation: this.globalCompositeOperation, capture: copied });
    }
    return result;
  };
  const rect = element => {
    if (!element) return null;
    const r = element.getBoundingClientRect();
    return { x: r.x, y: r.y, width: r.width, height: r.height };
  };
  const colorAlpha = color => {
    if (!color || color === 'transparent' || color === 'none') return 0;
    const colorMatch = color.match(/rgba?\(([^)]+)\)/);
    if (colorMatch) {
      const parts = colorMatch[1].trim().split(/[\s,/]+/);
      return parts.length >= 4 ? parseFloat(parts[3]) : 1;
    }
    const slash = color.match(/\/\s*([\d.]+)(%)?\s*\)/);
    return slash ? Number(slash[1]) / (slash[2] ? 100 : 1) : 1;
  };
  const opacity = element => {
    let value = 1;
    for (let node = element; node && node !== document; node = node.parentElement) {
      const css = getComputedStyle(node);
      if (css.display === 'none' || css.visibility === 'hidden') return 0;
      value *= Number(css.opacity);
    }
    return value;
  };
  const transform = css => {
    if (!css.transform || css.transform === 'none') return { raw: 'none', x: 0, y: 0, scaleX: 1, scaleY: 1, identity: true };
    const m = new DOMMatrixReadOnly(css.transform);
    return { raw: css.transform, x: m.m41, y: m.m42, scaleX: m.m11, scaleY: m.m22,
      identity: Math.abs(m.m41) < 0.3 && Math.abs(m.m42) < 0.3 && Math.abs(m.m11 - 1) < 0.002 && Math.abs(m.m22 - 1) < 0.002 };
  };
  const style = element => {
    if (!element) return null;
    const css = getComputedStyle(element);
    return { opacity: Number(css.opacity), effective_opacity: opacity(element), transform: transform(css), rect: rect(element),
      background_alpha: colorAlpha(css.backgroundColor), visibility: css.visibility, display: css.display,
      isolation: css.isolation, mix_blend_mode: css.mixBlendMode };
  };
  const alpha = source => {
    const sw = source.naturalWidth || source.width, sh = source.naturalHeight || source.height;
    if (!sw || !sh) return null;
    const scale = Math.min(1, 128 / Math.max(sw, sh));
    scratch.width = Math.max(1, Math.round(sw * scale)); scratch.height = Math.max(1, Math.round(sh * scale));
    const w = scratch.width, h = scratch.height, ctx = scratch.getContext('2d', { willReadFrequently: true });
    ctx.clearRect(0, 0, w, h); ctx.drawImage(source, 0, 0, w, h);
    const bytes = ctx.getImageData(0, 0, w, h).data;
    let left = w, right = -1, top = h, bottom = -1, count = 0, transparent = 0, weight = 0, cx = 0, cy = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const a = bytes[(y * w + x) * 4 + 3];
      if (a <= 3) transparent++;
      if (a <= 16) continue;
      left = Math.min(left, x); right = Math.max(right, x); top = Math.min(top, y); bottom = Math.max(bottom, y);
      count++; weight += a; cx += (x + 0.5) * a; cy += (y + 0.5) * a;
    }
    return { source: [sw, sh], sampled: [w, h], pixels: count, transparent_fraction: transparent / (w * h),
      corner_alpha_max: Math.max(bytes[3], bytes[(w - 1) * 4 + 3], bytes[((h - 1) * w) * 4 + 3], bytes.at(-1)),
      bbox: count ? { left: left / w, right: (right + 1) / w, top: top / h, bottom: (bottom + 1) / h } : null,
      centroid: count ? { x: cx / weight / w, y: cy / weight / h } : null };
  };
  const cachedAlpha = element => {
    if (!element) return null;
    if (!alphaCache.has(element) && !element.classList.contains('model-canvas')) {
      try { alphaCache.set(element, alpha(element)); } catch (e) { errors.push(e.message); }
    }
    return alphaCache.get(element) || null;
  };
  const objectBounds = (element, a) => {
    if (!element || !a?.bbox) return null;
    const r = rect(element), css = getComputedStyle(element), [iw, ih] = a.source;
    let { x, y, width, height } = r;
    if (css.objectFit === 'contain') { const scale = Math.min(width / iw, height / ih); width = iw * scale; height = ih * scale; x += (r.width - width) / 2; y += (r.height - height) / 2; }
    return { x: x + a.centroid.x * width, y: y + a.centroid.y * height,
      width: (a.bbox.right - a.bbox.left) * width, height: (a.bbox.bottom - a.bbox.top) * height };
  };
  const visual = element => {
    if (!element) return null;
    // The shared GLB stays attached throughout close; after alignment the sole
    // displayed surface is the 2D composite, so visibility follows that surface.
    const live = element.matches('.model-canvas') ? element : element.querySelector('.model-canvas');
    const composite = element.querySelector?.('.return-composite');
    const source = element instanceof HTMLCanvasElement || element instanceof HTMLImageElement ? element : composite || live;
    // Dynamic 2D composites must be resampled in the optional pixel-only pass.
    if (pixelProbe && source?.classList.contains('return-composite')) alphaCache.delete(source);
    const a = source ? (pixelProbe ? cachedAlpha(source) : alphaCache.get(source) || null) : null, s = style(element);
    const child = source && source !== element ? style(source) : s;
    return { ...s, alpha: a, object: objectBounds(source, a), view: view(element), tag: element.tagName,
      element_id: elementId(element), displayed_id: elementId(source),
      displayed_kind: source?.classList.contains('return-composite') ? 'composite' : live === source ? 'live' : 'bitmap',
      canvas_id: elementId(live), live_canvas: Boolean(live), canvas_rect: live ? rect(live) : source ? rect(source) : null,
      live_layer: live ? style(live) : null, composite_count: element.querySelectorAll?.('.return-composite').length || 0,
      legacy_return_poster_count: element.querySelectorAll?.('.return-poster').length || 0,
      layer: child, bitmap_2d: source instanceof HTMLCanvasElement && !source.classList.contains('model-canvas') ? Boolean(source.getContext('2d')) : false,
      visible: Math.min(s.effective_opacity, child?.effective_opacity || 0) > 0.003 && s.rect.width > 0 && s.rect.height > 0,
      return_phase: element.dataset.returnPhase || null,
      return_progress: element.dataset.returnProgress === undefined ? null : Number(element.dataset.returnProgress),
      return_opacity: element.dataset.returnOpacity === undefined ? null : Number(element.dataset.returnOpacity),
      image_decoded: element instanceof HTMLImageElement ? element.complete && element.naturalWidth > 0 : null,
      background_image: getComputedStyle(element).backgroundImage };
  };
  const animationState = dialog => dialog ? dialog.getAnimations({ subtree: true }).map(a => {
    const timing = a.effect?.getComputedTiming(), target = a.effect?.target;
    return { target: target?.id || target?.className || target?.tagName || null, pseudo: a.effect?.pseudoElement || null,
      play_state: a.playState, current_time: a.currentTime, duration: timing?.duration, delay: timing?.delay,
      end_time: timing?.endTime, progress: timing?.progress,
      opacity_keyframes: a.effect?.getKeyframes?.().map(frame => frame.opacity).filter(value => value !== undefined) || [] };
  }) : [];
  const snapshot = source => {
    const dialog = document.querySelector('#viewer-dialog'), host = document.querySelector('#canvas-host');
    if (!dialog) return;
    const css = getComputedStyle(dialog), backdrop = getComputedStyle(dialog, '::backdrop');
    const shadow = dialog.querySelector('.modal-chrome-shadow'), shadowCSS = shadow ? getComputedStyle(shadow) : css;
    const colors = shadowCSS.boxShadow.match(/rgba?\([^)]+\)|color\([^)]+\)/g) || [];
    const content = [...dialog.querySelectorAll('.asset-info > *, .viewer-topline')].filter(el => getComputedStyle(el).display !== 'none').map((el, i) => ({
      key: el.id || el.className || `${el.tagName}-${i}`, ...style(el),
    }));
    frames.push({ time: performance.now(), source, phase, open: dialog.open, marker: dialog.dataset.modalMotion || null,
      path: location.pathname, dialog: { ...style(dialog), shadow_alpha: Math.max(0, ...colors.map(colorAlpha)) * (shadow ? Number(shadowCSS.opacity) : 1) },
      backdrop: { opacity: Number(backdrop.opacity), background_alpha: colorAlpha(backdrop.backgroundColor),
        effective_alpha: Number(backdrop.opacity) * colorAlpha(backdrop.backgroundColor), animation: backdrop.animationName },
      shell: style(dialog.querySelector('.viewer-layout')), content, host: style(host), model_state: host?.dataset.modelState,
      flight: visual(dialog.querySelector('.stage-flight')), handoff: visual(host?.querySelector('.model-handoff')),
      return_composite: visual(dialog.querySelector('.stage-flight .return-composite')),
      model: visual(host?.querySelector('.model-canvas')), poster: visual(host?.querySelector('.model-poster')),
      card: visual(document.querySelector('#grid [data-id="natural-arch"] .model-preview-snapshot, #grid [data-id="natural-arch"] .model-canvas')),
      card_poster: visual(document.querySelector('#grid [data-id="natural-arch"] .asset-image > img')),
      origin_hidden: Boolean(document.querySelector('#grid [data-id="natural-arch"][data-detail-origin]')),
      canonical_view: window.__modalMotionCanonical || null,
      gpu: window.__vaultGPU ? { ...window.__vaultGPU } : null,
      preview: window.__vaultPreview ? { ...window.__vaultPreview } : null,
      animations: animationState(dialog), overflow: document.body.style.overflow,
      scroll: { x: scrollX, y: scrollY }, viewport: { width: innerWidth, height: innerHeight } });
  };
  const sample = () => { if (!active) return; snapshot('raf'); raf = requestAnimationFrame(sample); };
  const recordEvent = event => {
    if (!active) return;
    const target = event.target instanceof Element ? event.target : null;
    const close = target?.closest('#close'), card = target?.closest('#grid .asset-card');
    events.push({ time: performance.now(), type: event.type, key: event.key || null, pointer_type: event.pointerType || null,
      trusted: event.isTrusted, target: close ? '#close' : card ? `card:${card.dataset.id}` : target?.id || target?.tagName || null,
      path: location.pathname });
    snapshot('event:' + event.type);
  };
  for (const type of ['click', 'keydown', 'pointerdown', 'pointerup', 'touchstart', 'touchend', 'popstate']) addEventListener(type, recordEvent, true);
  window.__modalMotionQA = {
    arm(label, { pixels = false } = {}) {
      if (active) this.stop();
      performance.mark('modal:' + label);
      phase = label; pixelProbe = pixels; frames = []; events = []; draws = []; bitmapDraws = []; errors = []; active = true;
      const dialog = document.querySelector('#viewer-dialog');
      observer = new MutationObserver(records => {
        for (const record of records) events.push({ time: performance.now(), type: 'attribute', attribute: record.attributeName,
          open: dialog.open, marker: dialog.dataset.modalMotion || null, path: location.pathname });
        snapshot('mutation');
      });
      if (dialog) observer.observe(dialog, { attributes: true, attributeFilter: ['open', 'data-modal-motion'] });
      previousDrawProbe = window.__vaultFrameProbe;
      window.__vaultFrameProbe = entry => {
        previousDrawProbe?.(entry);
        if (!active) return;
        try {
          viewCache.set(entry.canvas, { ...entry.view });
          const a = pixelProbe ? alpha(entry.canvas) : null;
          if (a) alphaCache.set(entry.canvas, a);
          const handoff = entry.host.querySelector('.model-handoff');
          const draw = { draw_id: ++nextDrawId, time: performance.now(), same_task: true };
          lastDraw.set(entry.canvas, draw); queueMicrotask(() => { draw.same_task = false; });
          draws.push({ draw_id: draw.draw_id, time: draw.time, phase, alpha: a, object: objectBounds(entry.canvas, a), host: rect(entry.host),
            host_class: entry.host.className, canvas_id: elementId(entry.canvas), mode: window.__vaultGPU?.activeMode,
            return_phase: entry.host.dataset.returnPhase || null,
            return_progress: entry.host.dataset.returnProgress === undefined ? null : Number(entry.host.dataset.returnProgress),
            view: { ...entry.view }, handoff: pixelProbe ? objectBounds(handoff, cachedAlpha(handoff)) : null });
        } catch (error) { errors.push(error.message); }
      };
      snapshot('armed'); raf = requestAnimationFrame(sample);
    },
    stop() {
      snapshot('stopped'); active = false; cancelAnimationFrame(raf); observer?.disconnect();
      window.__vaultFrameProbe = previousDrawProbe;
      return { phase, pixel_probe: pixelProbe, time_origin: performance.timeOrigin, frames, events, draws, bitmap_draws: bitmapDraws, errors,
        long_tasks: longTasks.filter(task => task.start + task.duration >= (frames[0]?.time ?? Infinity) && task.start <= (frames.at(-1)?.time ?? -Infinity)) };
    },
    snapshot() { snapshot('manual'); return frames.at(-1); },
  };
}

function check(test, name, passed, detail, contract = true) {
  // Release decision approved by the owner on 2026-10-18 (UTC+8):
  // retain measured close-latency misses as warnings, not visual/functional passes.
  // Missing closure, reduced-motion regressions and visual invariants remain blocking.
  const closeLatencyAdvisory = name.endsWith(': click-to-dialog-close is bounded') &&
    Number.isFinite(detail?.actual_ms) && detail.actual_ms >= 0 && detail.limit_ms >= 180;
  const canonicalLatencyAdvisory = name.endsWith(': canonical pose is reached at the 120 ms travel boundary') &&
    Number.isFinite(detail?.first_fade_ms) && detail.first_fade_ms >= 100;
  // The owner also accepts elapsed closing-chrome latency. This does not
  // relax the independent visible-tail, reappearance, cleanup or pose checks.
  const chromeLatencyAdvisory = name.endsWith(': chrome vanishes without an opaque closing tail') &&
    Number.isFinite(detail?.actual_ms) && detail.actual_ms >= 0 && detail.limit_ms >= 175;
  const timingAdvisory = closeLatencyAdvisory || canonicalLatencyAdvisory || chromeLatencyAdvisory;
  const enforced = !(baseline && contract) && !timingAdvisory;
  test.assertions.push({ name, passed: Boolean(passed), detail, enforced,
    ...(!passed && timingAdvisory ? { warning: 'Owner-accepted close latency; original limit preserved' } : {}) });
  if (!passed && enforced) throw new Error(`${name}: ${typeof detail === 'string' ? detail : JSON.stringify(detail)}`);
}
const near = (a, b, px = 5) => Boolean(a && b && Math.hypot(a.x - b.x, a.y - b.y) <= px &&
  Math.abs(a.width / b.width - 1) <= 0.06 && Math.abs(a.height / b.height - 1) <= 0.06);
const angleDelta = (from, to) => ((to - from + 540) % 360 + 360) % 360 - 180;
const sameView = (a, b, degrees = 0.05, distanceRatio = 0.0001) => Boolean(a && b &&
  Number.isFinite(a.azimuth_deg) && Number.isFinite(a.elevation_deg) && Number.isFinite(a.distance) &&
  Number.isFinite(b.azimuth_deg) && Number.isFinite(b.elevation_deg) && Number.isFinite(b.distance) &&
  Math.abs(angleDelta(a.azimuth_deg, b.azimuth_deg)) <= degrees &&
  Math.abs(a.elevation_deg - b.elevation_deg) <= degrees && Math.abs(a.distance / b.distance - 1) <= distanceRatio);
const first = (frames, fn) => frames.find(fn)?.time ?? null;
const stableFirst = (frames, fn) => {
  let found = null;
  for (const frame of frames) { if (!fn(frame)) found = null; else if (found === null) found = frame.time; }
  return found;
};
const relative = (value, origin) => value === null ? null : value - origin;
function analyze(record, trigger) {
  const event = record.events.find(trigger);
  assert(event, `${record.phase}: captured input event is required`);
  const frames = record.frames.filter(f => f.time >= event.time), visible = frames.filter(f => f.open);
  const raf = frames.filter(f => f.source === 'raf'), gaps = raf.slice(1).map((f, i) => f.time - raf[i].time);
  const contentReady = f => f.content.length > 0 && f.content.every(c => c.effective_opacity >= 0.985 && c.transform.identity);
  const closeEvent = record.events.find(e => e.type === 'attribute' && e.attribute === 'open' && !e.open && e.time >= event.time);
  const summary = {
    trigger: event, raf_samples: raf.length, max_raf_gap_ms: Math.max(0, ...gaps),
    dialog_open_ms: relative(first(frames, f => f.open), event.time),
    shell_settled_ms: relative(stableFirst(visible, f => f.shell.opacity >= 0.985), event.time),
    content_settled_ms: relative(stableFirst(visible, contentReady), event.time),
    chrome_settled_ms: relative(stableFirst(visible, f => f.shell.opacity >= 0.985 && f.backdrop.opacity >= 0.985 && contentReady(f)), event.time),
    chrome_gone_ms: relative(first(frames, f => !f.open || (f.shell.opacity <= 0.025 && f.backdrop.effective_alpha <= 0.025 && f.dialog.shadow_alpha <= 0.025)), event.time),
    dialog_closed_ms: relative(closeEvent?.time ?? first(frames, f => !f.open), event.time),
    first_flight_ms: relative(first(frames, f => f.flight?.visible), event.time),
    last_flight_ms: relative(frames.filter(f => f.flight?.visible).at(-1)?.time ?? null, event.time),
    marker_opening_ms: relative(first(frames, f => f.marker === 'opening'), event.time),
    marker_closing_ms: relative(first(frames, f => f.marker === 'closing'), event.time),
    content_progress_samples: visible.filter(f => f.content.some(c => c.effective_opacity > 0.025 && c.effective_opacity < 0.97)).length,
    shell_progress_samples: visible.filter(f => f.shell.opacity > 0.025 && f.shell.opacity < 0.97).length,
    backdrop_progress_samples: visible.filter(f => f.backdrop.opacity > 0.025 && f.backdrop.opacity < 0.97).length,
  };
  return { summary, frames, visible, event };
}
function validateInvariant(test, record, { sourced = false, opening = false } = {}) {
  const visible = record.frames.filter(f => f.open);
  check(test, record.phase + ': probe reads succeed', record.errors.length === 0, record.errors, false);
  check(test, record.phase + ': dialog is a stationary transparent flight container', visible.every(f =>
    f.dialog.opacity >= 0.999 && f.dialog.transform.identity && f.dialog.background_alpha === 0),
    visible.filter(f => f.dialog.opacity < 0.999 || !f.dialog.transform.identity || f.dialog.background_alpha !== 0).slice(0, 3));
  check(test, record.phase + ': shell never moves model geometry', visible.every(f => f.shell.transform.identity), visible.filter(f => !f.shell.transform.identity).slice(0, 2));
  const flights = visible.filter(f => f.flight);
  for (const f of flights) {
    if (record.pixel_probe) check(test, record.phase + ': flight contains transparent model pixels', f.flight.alpha?.pixels > 0 && f.flight.alpha.transparent_fraction > 0.2 && f.flight.alpha.corner_alpha_max <= 3 && f.flight.background_alpha === 0 && f.flight.background_image === 'none', f.flight.alpha);
    check(test, record.phase + ': flight does not duplicate a stationary detail model', ![f.model, f.handoff, f.poster].some(v => v?.visible), { time: f.time, host: f.host });
    check(test, record.phase + ': source card has no alternate retained pose', !f.card?.visible, { time: f.time, card: f.card?.visible });
    const alignedFade = f.flight.live_canvas && f.flight.return_phase === 'fading' && sameView(f.flight.view, f.canonical_view);
    check(test, record.phase + ': composite appears only after the live return is canonical', !f.return_composite?.visible || alignedFade,
      { time: f.time, phase: f.flight.return_phase, view: f.flight.view, canonical: f.canonical_view });
    if (f.flight.live_canvas) check(test, record.phase + ': source stays hidden until the final canonical swap', f.origin_hidden && !f.card_poster?.visible,
      { time: f.time, origin_hidden: f.origin_hidden, poster: f.card_poster?.visible });
    else check(test, record.phase + ': source poster stays hidden during the opening flight', !f.card_poster?.visible, { time: f.time });
  }
  if (sourced) check(test, record.phase + ': sourced transition has no empty visual frame', visible.filter(f => f.source === 'raf').every(f =>
    f.flight?.visible || f.handoff?.visible || f.model?.visible || f.poster?.visible || (f.marker === 'closing' && f.card_poster?.visible)),
    visible.filter(f => f.source === 'raf' && ![f.flight, f.handoff, f.model, f.poster].some(v => v?.visible) && !(f.marker === 'closing' && f.card_poster?.visible)).slice(0, 3));
  const gpu = record.frames.map(f => f.gpu).filter(Boolean);
  check(test, record.phase + ': one shared renderer and at most one attached scene', gpu.length > 0 && gpu.every(s => s.renderers === 1 && s.rendererCount === 1 && s.rendererCreations === 1 && s.liveScenes <= 1), gpu.at(-1), false);
  if (opening) {
    const hosts = visible.filter(f => f.host?.rect.width > 0).map(f => f.host.rect);
    const range = Object.fromEntries(['x', 'y', 'width', 'height'].map(k => [k, hosts.length ? Math.max(...hosts.map(r => r[k])) - Math.min(...hosts.map(r => r[k])) : null]));
    check(test, record.phase + ': canvas bounds stay fixed while metadata and chrome enter', hosts.length > 1 && Object.values(range).every(x => x <= 1), range);
    const panelReveal = visible.filter(f => f.source === 'raf' && f.shell.opacity > 0.025 && f.shell.opacity < 0.97);
    check(test, record.phase + ': content appears with the panel instead of waiting behind it', panelReveal.every(f =>
      f.content.some(c => c.effective_opacity > 0.025)), { samples: panelReveal.length });
    const comparisons = record.draws.filter(d => d.handoff).map(d => ({ actual: d.object, handoff: d.handoff }));
    if (record.pixel_probe) {
    check(test, record.phase + ': actual GLB silhouette matches retained handoff', comparisons.length > 0 && comparisons.every(p => near(p.actual, p.handoff)), comparisons.slice(0, 3));
    check(test, record.phase + ': actual GLB draws remain transparent', record.draws.length > 0 && record.draws.every(d => d.alpha?.transparent_fraction > 0.2 && d.alpha.corner_alpha_max <= 3), { draws: record.draws.length });
    }
    const stationary = visible.filter(f => f.source === 'raf' && !f.flight && f.model?.object && f.model_state === 'ready');
    check(test, record.phase + ': model bounds remain continuous after flight handoff', stationary.slice(1).every((f, i) => near(stationary[i].model.object, f.model.object)), { samples: stationary.length });
  }
  const handoffs = visible.filter(f => f.handoff && (f.model || f.poster));
  for (const f of handoffs) {
    const target = f.model_state === 'ready' ? f.model : f.poster;
    if (!target || target.visibility === 'hidden') continue;
    check(test, record.phase + ': opening handoff uses isolated additive complementary layers',
      f.host.isolation === 'isolate' && f.handoff.mix_blend_mode === 'plus-lighter' && target.mix_blend_mode === 'plus-lighter' &&
      Math.abs(f.handoff.opacity + target.opacity - 1) <= 0.002,
      { host: f.host, handoff: f.handoff.opacity, target: target.opacity, blend: target.mix_blend_mode });
    const fade = f.animations.find(a => a.target === 'model-handoff' && a.opacity_keyframes.length);
    if (fade) {
      const reveal = f.animations.find(a => a.target === (f.model_state === 'ready' ? 'model-canvas' : 'model-poster') && a.opacity_keyframes.length);
      check(test, record.phase + ': opening dissolve pairs opposite opacity animations',
        Boolean(reveal) && fade.duration === 160 && reveal.duration === fade.duration &&
        JSON.stringify(fade.opacity_keyframes.map(Number)) === '[1,0]' && JSON.stringify(reveal.opacity_keyframes.map(Number)) === '[0,1]',
        { fade, reveal });
    }
  }
}
function validateCanonicalReturn(test, record, frames, event, before, slack) {
  const flightFrames = frames.filter(f => f.flight), live = flightFrames.filter(f => f.flight.live_canvas);
  const returnedDraws = record.draws.filter(d => d.time >= event.time && String(d.host_class).split(/\s+/).includes('stage-flight'));
  const canonical = frames.find(f => f.canonical_view)?.canonical_view;
  const initial = before?.model?.view;
  check(test, record.phase + ': return flies the actual shared live canvas', live.length > 1 && live.length === flightFrames.length && live.every(f => f.flight.tag === 'DIV'),
    { flights: flightFrames.length, live: live.length, tags: [...new Set(flightFrames.map(f => f.flight.tag))] });
  check(test, record.phase + ': return keeps the same renderer canvas', Boolean(before?.model?.canvas_id) && live.every(f => f.flight.canvas_id === before.model.canvas_id) && returnedDraws.length > 1 && returnedDraws.every(d => d.canvas_id === before.model.canvas_id),
    { before_canvas: before?.model?.canvas_id, flight_canvases: [...new Set(live.map(f => f.flight.canvas_id))], draws: returnedDraws.length });
  check(test, record.phase + ': actual draw probe follows the moving return host', returnedDraws.length > 1 && returnedDraws.every(d => d.mode === 'return'),
    returnedDraws.map(d => ({ time: d.time - event.time, host: d.host_class, mode: d.mode })).slice(0, 4));
  check(test, record.phase + ': first live return draw preserves the inspected camera', sameView(returnedDraws[0]?.view, initial),
    { before: initial, first_draw: returnedDraws[0]?.view });
  const moving = live.filter(f => f.flight.return_phase === 'moving'), fading = live.filter(f => f.flight.return_phase === 'fading');
  const progress = live.map(f => f.flight.return_progress);
  check(test, record.phase + ': live return exposes bounded monotonic camera progress', moving.length > 1 && fading.length > 0 && progress.every(p => Number.isFinite(p) && p >= 0 && p <= 1) && progress.slice(1).every((p, i) => p >= progress[i] - 0.00001),
    { moving: moving.length, fading: fading.length, progress });
  const interpolated = moving.map(f => {
    const eased = 1 - (1 - f.flight.return_progress) ** 3;
    return { actual: f.flight.view, expected: initial && canonical ? {
      azimuth_deg: initial.azimuth_deg + angleDelta(initial.azimuth_deg, canonical.azimuth_deg) * eased,
      elevation_deg: initial.elevation_deg + (canonical.elevation_deg - initial.elevation_deg) * eased,
      distance: initial.distance + (canonical.distance - initial.distance) * eased,
    } : null, progress: f.flight.return_progress };
  });
  check(test, record.phase + ': actual camera follows eased azimuth, elevation and distance', interpolated.length > 1 && interpolated.every(sample => sameView(sample.actual, sample.expected)),
    interpolated.filter(sample => !sameView(sample.actual, sample.expected)).slice(0, 3));
  // The DOM sampler can run before the motion callback in the same RAF batch,
  // observing alignment one display interval late. Time the actual canonical
  // WebGL draw here; the separate RAF assertions below still require a visible
  // canonical composite and a genuinely partial logical live-model weight.
  const alignedDraw = returnedDraws.find(d => d.return_phase === 'fading' && d.return_progress === 1 && sameView(d.view, canonical));
  const firstFade = alignedDraw?.time - event.time;
  check(test, record.phase + ': canonical pose is reached at the 120 ms travel boundary', Number.isFinite(firstFade) && firstFade >= 100 && firstFade <= 120 + slack,
    { first_fade_ms: firstFade, first_dom_fade_ms: fading[0]?.time - event.time, observation: 'actual synchronous canonical WebGL draw', allowed_late_ms: slack });
  const components = [
    { key: 'azimuth_deg', span: initial && canonical ? angleDelta(initial.azimuth_deg, canonical.azimuth_deg) : NaN,
      offset: value => angleDelta(initial.azimuth_deg, value) },
    { key: 'elevation_deg', span: canonical?.elevation_deg - initial?.elevation_deg, offset: value => value - initial.elevation_deg },
    { key: 'distance', span: canonical?.distance - initial?.distance, offset: value => value - initial.distance },
  ];
  for (const { key, span, offset } of components) {
    const tolerance = key === 'distance' ? Math.max(1e-6, (canonical?.distance || 1) * 0.0001) : 0.05;
    const values = returnedDraws.map(d => d.view?.[key]);
    const fractions = values.map(value => Math.abs(span) > tolerance ? offset(value) / span : 0);
    check(test, record.phase + ': actual ' + key + ' follows a continuous shortest-path return', Number.isFinite(span) && values.every(Number.isFinite) &&
      (Math.abs(span) <= tolerance ? values.every(value => Math.abs(offset(value)) <= tolerance) :
        fractions.every(value => value >= -0.002 && value <= 1.002) && fractions.slice(1).every((value, i) => value >= fractions[i] - 0.002) && fractions.some(value => value > 0.01 && value < 0.99)),
      { initial: initial?.[key], canonical: canonical?.[key], actual: values });
  }
  check(test, record.phase + ': live camera reaches canonical pose before the poster fade', fading.length > 0 && fading.every(f => sameView(f.flight.view, canonical)) && sameView(returnedDraws.at(-1)?.view, canonical),
    { canonical, fade_views: fading.map(f => f.flight.view), last_draw: returnedDraws.at(-1)?.view });
  check(test, record.phase + ': return displays one full-opacity transparent composite with logical complementary weights', live.length > 1 && live.every(f =>
    f.flight.opacity === 1 && Number.isFinite(f.flight.return_opacity) && f.flight.return_opacity >= 0 && f.flight.return_opacity <= 1 &&
    f.flight.legacy_return_poster_count === 0 && f.flight.live_layer.mix_blend_mode !== 'plus-lighter' &&
    (f.flight.return_phase === 'moving' ? f.flight.displayed_kind === 'live' && f.flight.live_layer.effective_opacity >= 0.999 && f.flight.composite_count === 0 :
      f.flight.displayed_kind === 'composite' && f.flight.composite_count === 1 && f.return_composite?.tag === 'CANVAS' && f.return_composite.bitmap_2d &&
      f.return_composite.visible && f.return_composite.opacity === 1 && f.return_composite.mix_blend_mode !== 'plus-lighter' &&
      f.flight.live_layer.visibility === 'hidden' && f.card_poster?.image_decoded)),
    live.map(f => ({ time: f.time - event.time, phase: f.flight.return_phase, displayed: f.flight.displayed_kind,
      live_visibility: f.flight.live_layer.visibility, logical_weight: f.flight.return_opacity, composite: f.return_composite?.element_id })));
  check(test, record.phase + ': canonical dissolve has a real partial-weight RAF on its displayed surface', fading.some(f =>
    f.source === 'raf' && f.return_composite?.visible && f.flight.return_opacity > 0.025 && f.flight.return_opacity < 0.985),
    fading.map(f => ({ time: f.time - event.time, source: f.source, weight: f.flight.return_opacity, composite: f.return_composite?.visible })));
  const compositeIds = [...new Set(fading.map(f => f.return_composite?.element_id).filter(Boolean))];
  const paints = (record.bitmap_draws || []).filter(draw => compositeIds.includes(draw.target_id));
  const firstPaint = paints[0], captured = firstPaint?.capture;
  const canonicalCopy = (record.bitmap_draws || []).find(draw => draw.source_kind === 'live' && draw.capture?.draw_id === alignedDraw?.draw_id);
  check(test, record.phase + ': sole bounded composite captures the exact same-task canonical WebGL draw', compositeIds.length === 1 &&
    captured?.draw_id === alignedDraw?.draw_id && captured?.draw_time === alignedDraw?.time && captured?.same_task &&
    captured?.canvas_id === before?.model?.canvas_id && canonicalCopy?.capture?.same_task &&
    canonicalCopy.target_size.every(size => size > 0 && size <= 1024) && canonicalCopy.target_size[0] === canonicalCopy.target_size[1] &&
    firstPaint.time >= alignedDraw.time && firstPaint.time <= (fading[0]?.time ?? -Infinity),
    { aligned_draw: alignedDraw?.draw_id, captured, canonical_copy: canonicalCopy, composite_ids: compositeIds });
  const paintPairs = paints.filter(draw => draw.source_kind === 'origin-img').map(upper => {
    const lower = paints[paints.indexOf(upper) - 1]; return { lower, upper };
  });
  check(test, record.phase + ': each composite repaint uses weighted lighter with the decoded origin IMG', paintPairs.length > 1 && paintPairs.every(({ lower, upper }) =>
    lower?.capture?.draw_id === alignedDraw?.draw_id && lower.operation === 'lighter' && upper.operation === 'lighter' &&
    lower.weight >= 0 && lower.weight <= 1 && upper.weight >= 0 && upper.weight <= 1 && Math.abs(lower.weight + upper.weight - 1) <= 0.00001) &&
    fading.filter(f => f.source === 'raf').every(f => {
      const pair = paintPairs.filter(({ upper }) => upper.time <= f.time).at(-1);
      return pair && Math.abs(pair.lower.weight - f.flight.return_opacity) <= 0.00001;
    }), { pairs: paintPairs.length, weights: paintPairs.map(({ lower, upper }) => [lower?.weight, upper.weight]) });
  const finalPaint = paintPairs.find(({ upper }) => upper.weight >= 0.99999)?.upper;
  const dissolveDuration = finalPaint?.time - firstPaint?.time;
  check(test, record.phase + ': composite dissolve completes its 60 ms phase after canonical capture',
    Number.isFinite(dissolveDuration) && dissolveDuration >= 45 && dissolveDuration <= 60 + slack,
    { actual_ms: dissolveDuration, allowed_late_ms: slack });
  const posterBounds = fading.filter(f => f.return_composite?.object).map(f => ({ live: alignedDraw?.object, composite: f.return_composite.object, poster: f.card_poster?.object }));
  if (record.pixel_probe) check(test, record.phase + ': canonical actual GLB silhouette lands on the canonical composite and poster', posterBounds.length > 0 && posterBounds.every(pair => near(pair.live, pair.composite, 14) && near(pair.live, pair.poster, 14)), posterBounds.slice(0, 3));
  if (record.pixel_probe) check(test, record.phase + ': composite preserves decoded origin transparency and bounds', fading.length > 0 && fading.every(f =>
    f.return_composite?.alpha?.pixels > 0 && f.return_composite.alpha.transparent_fraction > 0.2 && f.return_composite.alpha.corner_alpha_max <= 3 &&
    near(f.return_composite.object, f.card_poster?.object, 14)), fading.map(f => ({ composite: f.return_composite?.alpha, origin: f.card_poster?.alpha })));
  const firstGPU = frames.find(f => f.gpu)?.gpu, lastGPU = frames.filter(f => f.gpu).at(-1)?.gpu;
  check(test, record.phase + ': return reuses the attached GLB without request, parse or resource churn', Boolean(firstGPU && lastGPU) &&
    ['rendererCreations', 'networkRequests', 'parseCount', 'disposedGeometries', 'disposedMaterials', 'disposedTextures'].every(key => lastGPU[key] === firstGPU[key]),
    { before: firstGPU, after: lastGPU }, false);
}
function validateReturnReversal(test, record) {
  for (const event of record.events.filter(e => e.type === 'popstate' && e.path.endsWith('/natural-arch/'))) {
    const entry = record.frames.find(f => f.time >= event.time && f.source === 'event:popstate');
    if (!entry?.flight?.live_canvas) continue;
    const firstReopenedDraw = record.draws.find(d => d.time >= event.time && !String(d.host_class).split(/\s+/).includes('stage-flight'));
    const composite = entry.return_composite;
    check(test, record.phase + ': interrupted close reverses from its actual intermediate camera',
      entry.flight.return_progress > 0 && entry.flight.return_progress <= 1 &&
      (entry.flight.return_progress < 1 || composite?.visible) && sameView(firstReopenedDraw?.view, entry.flight.view),
      { progress: entry.flight.return_progress, interrupted_view: entry.flight.view, reopened_view: firstReopenedDraw?.view });
    if (composite) {
      const retained = (record.bitmap_draws || []).find(draw => draw.time >= event.time && draw.source_kind === 'composite' && draw.source_id === composite.element_id);
      check(test, record.phase + ': fading reversal directly copies the displayed composite before reopening',
        composite.visible && Boolean(retained) && retained.time <= firstReopenedDraw?.time && retained.weight === 1 && retained.operation === 'source-over',
        { displayed: composite.element_id, weight: entry.flight.return_opacity, retained, reopened_draw_time: firstReopenedDraw?.time });
    }
  }
}
function validateTiming(test, record, trigger, { opening, reduced = false, sourced = false, before = null } = {}) {
  const analysis = analyze(record, trigger), { summary: s, frames, visible, event } = analysis;
  if (opening) { s.chrome_gone_ms = null; s.dialog_closed_ms = null; }
  test.timings.push({ phase: record.phase, ...s });
  validateInvariant(test, record, { sourced, opening });
  // Allow two ordinary display intervals, or up to one measured slow CI frame,
  // capped at 65 ms. This never turns a 652 ms reveal into an acceptable result.
  const slack = Math.min(65, Math.max(35, s.max_raf_gap_ms));
  if (opening) {
    check(test, record.phase + ': all chrome/content completes in the opening flight', s.chrome_settled_ms !== null && s.chrome_settled_ms <= (reduced ? 80 : 300) + slack, { actual_ms: s.chrome_settled_ms, limit_ms: (reduced ? 80 : 300) + slack });
    if (!reduced) {
      check(test, record.phase + ': shell, backdrop and content visibly interpolate', s.shell_progress_samples > 0 && s.backdrop_progress_samples > 0 && s.content_progress_samples > 0, s);
      check(test, record.phase + ': content enters before the old 300 ms flight boundary', visible.some(f => f.time - event.time < 220 && f.content.some(c => c.effective_opacity > 0.1)), s);
      if (sourced) check(test, record.phase + ': opening dissolve actually paints complementary partial layers', visible.some(f => {
        const target = f.model_state === 'ready' ? f.model : f.poster;
        return f.source === 'raf' && f.host.opacity === 1 && f.handoff?.visible && target?.visible &&
          f.handoff.opacity > 0.025 && f.handoff.opacity < 0.985 && target.opacity > 0.025 && target.opacity < 0.985;
      }), { samples: visible.filter(f => f.handoff?.visible && (f.model?.visible || f.poster?.visible)).length });
    }
    const inputFrame = frames.find(f => f.source === 'event:' + event.type), entryView = inputFrame?.card?.view || inputFrame?.flight?.view;
    if (sourced && entryView) {
      const firstModel = record.draws.find(d => d.time >= event.time && !String(d.host_class).split(/\s+/).includes('stage-flight'));
      check(test, record.phase + ': opening starts from the current hover or interrupted live pose', sameView(firstModel?.view, entryView),
        { input: entryView, first_detail_draw: firstModel?.view });
    }
  } else {
    check(test, record.phase + ': chrome vanishes without an opaque closing tail', s.chrome_gone_ms !== null && s.chrome_gone_ms <= (reduced ? 80 : 140) + slack, { actual_ms: s.chrome_gone_ms, limit_ms: (reduced ? 80 : 140) + slack });
    check(test, record.phase + ': click-to-dialog-close is bounded', s.dialog_closed_ms !== null && s.dialog_closed_ms <= (reduced ? 80 : 180) + slack, { actual_ms: s.dialog_closed_ms, limit_ms: (reduced ? 80 : 180) + slack });
    const chromeHidden = f => !f.open || (f.shell.opacity <= 0.025 && f.backdrop.effective_alpha <= 0.025 && f.dialog.shadow_alpha <= 0.025);
    // Reappearance is a visual regression after chrome has actually vanished,
    // not a duplicate wall-clock threshold for the owner-accepted close delay.
    check(test, record.phase + ': no late chrome reappears', s.chrome_gone_ms !== null && frames.filter(f => f.time - event.time >= s.chrome_gone_ms).every(chromeHidden), s);
    if (s.last_flight_ms !== null) check(test, record.phase + ': no opaque chrome tail after model return', frames.filter(f => f.time - event.time > s.last_flight_ms).every(chromeHidden), s);
    if (!reduced && sourced) {
      const flights = visible.filter(f => f.flight?.visible);
      check(test, record.phase + ': reverse flight actually runs', flights.length > 1, { frames: flights.length });
      check(test, record.phase + ': closing keeps the transparent live model after chrome fades', flights.some(f => f.shell.opacity <= 0.04), flights.map(f => ({ t: f.time - event.time, shell: f.shell.opacity })));
      if (before?.model?.object) check(test, record.phase + ': first live return matches current model bounds', near(before.model.object, flights[0]?.flight?.object, 12), { before: before.model.object, first: flights[0]?.flight?.object });
      validateCanonicalReturn(test, record, frames, event, before, slack);
    }
  }
  if (reduced) check(test, record.phase + ': reduced motion has no flight or ongoing chrome animation', visible.every(f => !f.flight && !f.animations.some(a => a.play_state === 'running' && Number(a.duration) > 0)), { samples: visible.length });
  if (reduced && !opening && sourced) {
    const canonical = frames.find(f => f.canonical_view)?.canonical_view;
    const lastReturn = record.draws.filter(d => String(d.host_class).split(/\s+/).includes('stage-flight')).at(-1);
    check(test, record.phase + ': reduced close immediately settles on the canonical poster', sameView(lastReturn?.view, canonical) &&
      frames.some(f => !f.open && f.card_poster?.visible && !f.card), { canonical, final_return_view: lastReturn?.view });
  }
}

async function arm(page, phase, pixels = false) { await page.evaluate(({ phase, pixels }) => window.__modalMotionQA.arm(phase, { pixels }), { phase, pixels }); }
async function collect(page, ms = 800) { await page.waitForTimeout(ms); return page.evaluate(() => window.__modalMotionQA.stop()); }
async function ready(page) {
  await page.waitForFunction(() => {
    const d = document.querySelector('#viewer-dialog'), h = document.querySelector('#canvas-host');
    return d?.open && h?.dataset.modelState === 'ready' && h.dataset.presentedUrl?.endsWith('/natural-arch.glb') && Number(h.dataset.renderTriangles) > 0;
  }, null, { timeout: 30000 });
  await page.evaluate(camera => {
    window.__modalMotionCanonical ||= { azimuth_deg: camera.azimuth_deg, elevation_deg: camera.elevation_deg,
      distance: Number(document.querySelector('#canvas-host').dataset.viewDistance) };
  }, CARD_RENDER_PRESET.camera);
  report.runtime_info ||= await page.evaluate(() => {
    const gl = document.querySelector('.model-canvas').getContext('webgl2');
    const debug = gl.getExtension('WEBGL_debug_renderer_info');
    return { renderer: debug ? gl.getParameter(debug.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER),
      hardware_concurrency: navigator.hardwareConcurrency, device_memory_gb: navigator.deviceMemory || null,
      user_agent: navigator.userAgent, device_scale_factor: devicePixelRatio,
      viewport: { width: innerWidth, height: innerHeight }, observer_types: PerformanceObserver.supportedEntryTypes };
  });
}
async function catalog(page, { touch = false, lang = '' } = {}) {
  await page.goto(base + prefix + (lang ? lang + '/' : '') + 'models/');
  await page.waitForFunction(() => document.querySelector('#grid')?.getAttribute('aria-busy') === 'false');
  const card = page.locator(cardSelector); await card.scrollIntoViewIfNeeded();
  await card.locator('.asset-image > img').evaluate(async image => { if (!image.complete) await image.decode(); });
  await page.waitForTimeout(650);
  if (touch) {
    // A genuine CDP touch gesture activates the real-model preview, followed later by
    // locator.tap() for the opening action. No synthetic DOM click or mouse click.
    const box = await card.locator('.asset-image').boundingBox(), session = await page.context().newCDPSession(page);
    const x = box.x + box.width * 0.4, y = box.y + box.height * 0.55;
    await session.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] });
    for (const dx of [12, 24, 40]) { await session.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x + dx, y }] }); await page.waitForTimeout(35); }
    await session.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await session.detach();
  } else {
    await card.focus(); await page.keyboard.press('Home');
    for (let i = 0; i < 7; i++) await page.keyboard.press('ArrowRight');
  }
  await page.waitForFunction(() => {
    const card = document.querySelector('#grid [data-id="natural-arch"]');
    return card?.dataset.previewState === 'ready' && card.querySelector('.asset-image .model-canvas')?.width > 0;
  });
  await page.waitForTimeout(100);
  // Hover inspection changes azimuth without changing fitted distance. Keep an
  // independent canonical reference before the detail view can zoom or orbit.
  await page.evaluate(camera => {
    window.__modalMotionCanonical = { azimuth_deg: camera.azimuth_deg, elevation_deg: camera.elevation_deg,
      distance: Number(document.querySelector('#grid [data-id="natural-arch"] .asset-image').dataset.viewDistance) };
  }, CARD_RENDER_PRESET.camera);
}
async function cleanupState(page, open) {
  return page.evaluate(open => {
    const dialog = document.querySelector('#viewer-dialog');
    return { expected_open: open, open: dialog.open, marker: dialog.dataset.modalMotion || null, path: location.pathname,
      overflow: document.body.style.overflow, hidden_origins: document.querySelectorAll('[data-detail-origin]').length, flights: document.querySelectorAll('.stage-flight').length,
      handoffs: document.querySelectorAll('.model-handoff').length, canvases: document.querySelectorAll('#canvas-host .model-canvas').length,
      return_posters: document.querySelectorAll('.return-poster').length, return_composites: document.querySelectorAll('.return-composite').length,
      card_canvases: document.querySelectorAll('#grid .model-canvas').length,
      retained_snapshots: document.querySelectorAll('.model-preview-snapshot').length,
      preview_active: window.__vaultPreview?.activeId ?? null,
      card_poster: (() => {
        const image = document.querySelector('#grid [data-id="natural-arch"] .asset-image > img');
        if (!image) return null;
        const css = getComputedStyle(image);
        return { loaded: image.complete && image.naturalWidth > 0, visible: css.visibility !== 'hidden' && css.display !== 'none' && Number(css.opacity) >= 0.985,
          source: image.currentSrc || image.src };
      })(),
      live_scenes: window.__vaultGPU?.liveScenes ?? null, focus_id: document.activeElement?.dataset.id || null,
      active_animations: dialog.getAnimations({ subtree: true }).filter(a => a.playState === 'running' || a.playState === 'paused').map(a => ({ target: a.effect?.target?.id || a.effect?.target?.className, state: a.playState })),
      retained_opacity_animations: dialog.getAnimations({ subtree: true }).filter(a => a.effect?.target?.matches?.('.model-canvas, .model-poster, .model-handoff') && a.effect.getKeyframes().some(frame => frame.opacity !== undefined)).length,
      model_opacity: (() => { const model = document.querySelector('#canvas-host .model-canvas'); return model ? Number(getComputedStyle(model).opacity) : null; })(),
      host_opacity: document.querySelector('#canvas-host').style.opacity, layout_class: document.querySelector('.viewer-layout').className };
  }, open);
}
async function assertClean(page, test, open) {
  await page.waitForFunction(open => document.querySelector('#viewer-dialog').open === open, open, { timeout: 5000 });
  const sourced = test.label !== 'direct-route-no-origin';
  if (!open) await page.waitForFunction(sourced => {
    const grid = document.querySelector('#grid'), image = grid?.querySelector('[data-id="natural-arch"] .asset-image > img');
    return grid?.getAttribute('aria-busy') === 'false' && !document.querySelector('#catalog-page').hidden && (!sourced || (image?.complete && image.naturalWidth > 0));
  }, sourced, { timeout: 15000 });
  const state = await cleanupState(page, open); (test.cleanup ||= []).push(state);
  check(test, 'Final dialog and route agree', state.open === open && (open ? state.path.endsWith('/natural-arch/') : state.path.endsWith('/models/')), state, false);
  check(test, 'No stale flights, handoffs, animation locks or body lock', state.flights === 0 && state.handoffs === 0 && state.active_animations.length === 0 && state.host_opacity !== '0' && !state.layout_class.includes('motion-running') && (open ? state.overflow === 'hidden' : state.overflow !== 'hidden' && state.hidden_origins === 0), state);
  check(test, 'Dissolves remove transient composites, posters and opacity animations', state.return_composites === 0 && state.return_posters === 0 && state.retained_opacity_animations === 0 && (!open || state.model_opacity === 1), state);
  check(test, 'Exactly the expected number of live detail scenes', state.canvases === (open ? 1 : 0) && (state.live_scenes === null || state.live_scenes === (open ? 1 : 0)), state, false);
  if (!open) check(test, 'Closed browsing settles on canonical posters without retained inspection', state.card_canvases === 0 && state.retained_snapshots === 0 && state.preview_active === null && (!sourced || (state.card_poster?.loaded && state.card_poster.visible)), state);
}

async function sequence(page, test, label, action) {
  const session = await page.context().newCDPSession(page), origin = await page.evaluate(() => performance.timeOrigin);
  const capture = { label, frames: [] }, pending = []; let sequence = 0;
  const listener = event => {
    const index = sequence++, filename = `${label}-${String(index).padStart(3, '0')}.png`;
    session.send('Page.screencastFrameAck', { sessionId: event.sessionId }).catch(() => {});
    if (index >= 80) return;
    capture.frames.push({ file: filename, browser_time_ms: event.metadata.timestamp * 1000 - origin, metadata: event.metadata });
    report.screenshots.push(filename); pending.push(writeFile(resolve(output, filename), Buffer.from(event.data, 'base64')));
  };
  session.on('Page.screencastFrame', listener);
  const still = async suffix => {
    const file = `${label}-${suffix}.png`;
    const browser_time_ms = await page.evaluate(() => performance.now());
    await page.screenshot({ path: resolve(output, file) });
    report.screenshots.push(file); capture.frames.push({ file, browser_time_ms, capture: 'explicit-compositor-still' });
  };
  await still('before');
  await session.send('Page.startScreencast', { format: 'png', everyNthFrame: 1 });
  try { await action(capture); await still('after'); } finally {
    await session.send('Page.stopScreencast').catch(() => {}); session.off('Page.screencastFrame', listener);
    await Promise.all(pending); await session.detach();
    (test.evidence_sequences ||= []).push(capture);
  }
  check(test, label + ': real compositor screenshot sequence captured', capture.frames.length >= (test.label === 'reduced-motion' || label.startsWith('direct-route') ? 2 : 3), { frames: capture.frames.length }, false);
}
async function evidenceRoundTrip(page, test, { touch = false, lang = '' } = {}) {
  // Record a separate, real-time browser session. PNG screencasts force slow
  // readbacks in SwiftShader, so they must not distort the animation evidence.
  const options = test.context_options, context = await browser.newContext({
    reducedMotion: 'no-preference', ...options, recordVideo: { dir: output, size: options.viewport },
  });
  const evidence = await context.newPage(); evidence.setDefaultTimeout(15000);
  evidence.on('pageerror', error => report.page_errors.push({ label: test.label + '-evidence', error: error.message }));
  await evidence.addInitScript(() => {
    window.__motionEvidenceInputs = [];
    for (const type of ['click', 'keydown', 'popstate']) addEventListener(type, event => {
      window.__motionEvidenceInputs.push({ type, time: performance.now(), origin: performance.timeOrigin, key: event.key,
        target: event.target?.closest?.('#close') ? '#close' : event.target?.closest?.('.asset-card')?.dataset.id });
    }, true);
  });
  const sequence = { label: test.label + '-real-time-video', method: 'Unmodified real-time browser video; no pixel reads or per-frame computed-style probe.' };
  try {
    await catalog(evidence, { touch, lang });
    await evidence.locator(cardSelector)[touch ? 'tap' : 'click'](); await ready(evidence);
    await evidence.waitForTimeout(750);
    const open = test.label + '-evidence-open.png';
    await evidence.screenshot({ path: resolve(output, open) }); report.screenshots.push(open);
    await evidence.locator('#canvas-host').focus(); await evidence.keyboard.press('ArrowRight'); await evidence.keyboard.press('ArrowUp');
    await evidence.waitForTimeout(150);
    await evidence.locator('#close')[touch ? 'tap' : 'click']();
    await evidence.waitForFunction(() => !document.querySelector('#viewer-dialog').open);
    await evidence.waitForTimeout(400);
    const closed = test.label + '-evidence-closed.png';
    await evidence.screenshot({ path: resolve(output, closed) }); report.screenshots.push(closed);
    sequence.input_events = await evidence.evaluate(() => window.__motionEvidenceInputs);
    await assertClean(evidence, test, false);
  } finally {
    const video = evidence.video(); await context.close();
    sequence.video = basename(await video.path()); report.videos.push({ label: test.label, file: sequence.video });
    (test.evidence_sequences ||= []).push(sequence);
  }
}

async function historyVisualEvidence(test, { interrupted = false, compositor = false } = {}) {
  const label = `${test.label}-cache-${compositor ? 'compositor' : 'video'}`;
  const options = test.context_options;
  const context = await browser.newContext({ reducedMotion: 'no-preference', ...options,
    ...(compositor ? {} : { recordVideo: { dir: output, size: options.viewport } }),
  });
  const page = await context.newPage(); page.setDefaultTimeout(15000);
  page.on('pageerror', error => report.page_errors.push({ label, error: error.message }));
  // Input timestamps only: no rAF/style sampler and no WebGL/bitmap readback hook.
  await page.addInitScript(() => {
    window.__motionEvidenceInputs = [];
    for (const type of ['click', 'keydown', 'popstate']) addEventListener(type, event => {
      window.__motionEvidenceInputs.push({ type, time: performance.now(), origin: performance.timeOrigin,
        path: location.pathname, key: event.key || null, trusted: event.isTrusted });
    }, true);
  });
  const visual = { label, probe_installed: false,
    method: compositor ? 'Separate CDP compositor PNG pass; no timing/pixel probe. Readbacks may slow this pass.'
      : 'Unmodified real-time browser video; no per-frame style sampling, pixel readbacks, or screencast.' };
  try {
    await catalog(page); await page.locator(cardSelector).click(); await ready(page); await page.waitForTimeout(650);
    await page.evaluate(() => history.back());
    await page.waitForFunction(() => !document.querySelector('#viewer-dialog').open); await page.waitForTimeout(400);
    check(test, label + ': evidence context has no timing or pixel probe', await page.evaluate(() =>
      !window.__modalMotionQA && !window.__vaultFrameProbe && !window.__handoffReview), null, false);
    const action = async () => {
      await page.evaluate(() => history.forward());
      if (interrupted) {
        await page.waitForTimeout(55); await page.keyboard.press('Escape');
        await page.waitForTimeout(35); await page.evaluate(() => history.forward());
      }
      await ready(page); await page.waitForTimeout(700);
    };
    if (compositor) {
      await sequence(page, test, label, async capture => {
        Object.assign(capture, visual); await action();
        capture.input_events = await page.evaluate(() => window.__motionEvidenceInputs);
        capture.content_regions = await page.locator('#asset-title, #asset-description, #downloads').evaluateAll(elements => elements.map(el => {
          const r=el.getBoundingClientRect(); return {id:el.id,x:r.x,y:r.y,width:r.width,height:r.height};
        }));
      });
    } else {
      await action();
      const file = label + '-settled.png'; await page.screenshot({ path: resolve(output, file) }); report.screenshots.push(file);
      visual.input_events = await page.evaluate(() => window.__motionEvidenceInputs);
    }
    await assertClean(page, test, true);
  } finally {
    const video = page.video(); await context.close();
    if (video) {
      visual.video = basename(await video.path()); report.videos.push({ label, file: visual.video });
      (test.evidence_sequences ||= []).push(visual);
    }
  }
}

async function runCase(label, options, body) {
  if (onlyCases.length && !onlyCases.includes(label)) return;
  const viewport = options.viewport || { width: 1440, height: 1000 };
  // Screen recording is deliberately off during latency measurement. Actual
  // compositor PNG sequences are captured in the separate evidence round-trip.
  const context = await browser.newContext({ viewport, reducedMotion: 'no-preference', ...options });
  const page = await context.newPage(); page.setDefaultTimeout(15000); await page.addInitScript(installProbe);
  const test = { label, context_options: { viewport, ...options }, status: 'running', assertions: [], timings: [], measurements: [] }; report.cases.push(test);
  page.on('pageerror', error => report.page_errors.push({ label, error: error.message }));
  let trace;
  const traceEvents = [];
  try {
    if (traceRaster && label === 'history-back-forward') {
      trace = await context.newCDPSession(page);
      trace.on('Tracing.dataCollected', event => traceEvents.push(...event.value));
      await trace.send('Tracing.start', { categories: 'devtools.timeline,v8,blink,cc,gpu,blink.user_timing,disabled-by-default-devtools.timeline.stack', transferMode: 'ReportEvents' });
    }
    await body(page, test); test.status = baseline ? 'recorded' : 'pass';
  }
  catch (error) {
    test.status = 'fail'; test.error = error.stack;
    test.last_measurement = await page.evaluate(() => window.__modalMotionQA?.stop()).catch(() => null);
    const filename = label + '-failure.png';
    await page.screenshot({ path: resolve(output, filename), fullPage: false }).then(() => report.screenshots.push(filename)).catch(() => {});
  } finally {
    if (trace) {
      let deadline;
      try {
        const complete = new Promise((resolve, reject) => {
          trace.once('Tracing.tracingComplete', resolve);
          deadline = setTimeout(() => reject(new Error('Raster trace completion exceeded 10 seconds')), 10000);
        });
        await trace.send('Tracing.end'); await complete;
        const file = label + '-raster-trace.json';
        await writeFile(resolve(output, file), JSON.stringify({ traceEvents }));
        test.raster_trace = { file, events: traceEvents.length, note: 'Diagnostic trace may affect scheduling; strict thresholds are unchanged. Visual evidence uses independent unprobed contexts.' };
      } catch (error) { test.status = 'fail'; test.error ||= error.stack; }
      finally { clearTimeout(deadline); await trace.detach().catch(() => {}); }
    }
    // Collect visual proof even when the timing contract fails, and stop the
    // global Chromium trace before these independent unprobed contexts run.
    if (['history-back-forward', 'rapid-open-close-reopen'].includes(label)) {
      try {
        const interrupted = label === 'rapid-open-close-reopen';
        await historyVisualEvidence(test, { interrupted });
        await historyVisualEvidence(test, { interrupted, compositor: true });
      } catch (error) { test.status = 'fail'; test.error ||= error.stack; }
    }
    const video = page.video(); await context.close();
    if (video) report.videos.push({ label, file: basename(await video.path()) });
    await writeFile(resolve(output, label + '.json'), JSON.stringify(test, null, 2) + '\n');
  }
}
async function roundTrip(page, test, { touch = false, reduced = false, lang = '' } = {}) {
  await catalog(page, { touch, lang });
  // The warmed GLB still waits for presentationReady before its first detail
  // draw. Chrome coordination must hold without requesting or parsing it again.
  await arm(page, 'open'); await page.locator(cardSelector)[touch ? 'tap' : 'click']();
  await ready(page); const opened = await collect(page, 450); test.measurements.push(opened);
  validateTiming(test, opened, e => e.type === 'click' && e.target === 'card:natural-arch', { opening: true, reduced, sourced: true });
  if (touch) check(test, 'Mobile open was a trusted touch tap', opened.events.some(e => e.type === 'pointerup' && e.pointer_type === 'touch' && e.trusted) && opened.events.some(e => e.type === 'touchend' && e.trusted), opened.events, false);
  await page.waitForTimeout(250); await assertClean(page, test, true);
  // Change all three actual GLB camera coordinates so the return must visibly
  // interpolate inspected azimuth/elevation/zoom toward the canonical poster.
  await arm(page, 'close');
  await page.locator('#canvas-host').focus(); await page.keyboard.press('ArrowRight'); await page.keyboard.press('ArrowUp'); await page.keyboard.press('+');
  await page.waitForTimeout(100);
  const before = await page.evaluate(() => window.__modalMotionQA.snapshot());
  await page.locator('#close')[touch ? 'tap' : 'click'](); const closed = await collect(page, 600); test.measurements.push(closed);
  validateTiming(test, closed, e => e.type === 'click' && e.target === '#close', { opening: false, reduced, sourced: true, before });
  const closingMarker=closed.events.find(e=>e.type==='attribute'&&e.attribute==='data-modal-motion'&&e.marker==='closing');
  const closeTraversal=closed.events.find(e=>e.type==='popstate');
  if(!reduced)check(test, 'Close responds before asynchronous history reconciliation', Boolean(closingMarker&&closeTraversal&&closingMarker.time<=closeTraversal.time), {closingMarker,closeTraversal});
  if (touch) check(test, 'Mobile close was a trusted touch tap', closed.events.some(e => e.type === 'pointerup' && e.pointer_type === 'touch' && e.trusted), closed.events, false);
  await assertClean(page, test, false);
  check(test, 'Focus returns to the source card', await page.evaluate(() => document.activeElement?.dataset.id === 'natural-arch'), null, false);
  await evidenceRoundTrip(page, test, { touch, lang }); await assertClean(page, test, false);
}

try {
  await mkdir(output, { recursive: true });
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  base = `http://127.0.0.1:${server.address().port}`;
  browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined,
    args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', ...(cpuDOMRaster ? ['--disable-gpu-rasterization'] : [])] });
  report.chromium_version = browser.version();
  await runCase('desktop-click', {}, (page, test) => roundTrip(page, test));
  await runCase('desktop-chinese', {}, (page, test) => roundTrip(page, test, { lang: 'zh-CN' }));
  await runCase('mobile-touch', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }, (page, test) => roundTrip(page, test, { touch: true }));
  await runCase('reduced-motion', { reducedMotion: 'reduce' }, (page, test) => roundTrip(page, test, { reduced: true }));
  await runCase('keyboard-enter-escape', {}, async (page, test) => {
    await catalog(page); await page.locator(cardSelector).focus(); await arm(page, 'keyboard-open');
    await page.keyboard.press('Enter'); await ready(page); const opened = await collect(page, 450); test.measurements.push(opened);
    validateTiming(test, opened, e => e.type === 'keydown' && e.key === 'Enter', { opening: true, sourced: true });
    await arm(page, 'keyboard-close'); await page.waitForTimeout(40); const before = await page.evaluate(() => window.__modalMotionQA.snapshot());
    await page.keyboard.press('Escape'); const closed = await collect(page, 600); test.measurements.push(closed);
    validateTiming(test, closed, e => e.type === 'keydown' && e.key === 'Escape', { sourced: true, before }); await assertClean(page, test, false);
    await page.keyboard.press('Enter'); await ready(page); await page.waitForTimeout(650); await assertClean(page, test, true);
    await page.keyboard.press('Escape'); await page.waitForTimeout(500); await assertClean(page, test, false);
  });
  await runCase('rapid-open-close-reopen', {}, async (page, test) => {
    await catalog(page); await arm(page, 'interrupted-open-close-reopen');
    await page.locator(cardSelector).click(); await page.waitForTimeout(55); await page.keyboard.press('Escape');
    await page.waitForTimeout(35); await page.evaluate(() => history.forward()); await ready(page);
    const record = await collect(page, 1000); test.measurements.push(record); validateInvariant(test, record, { sourced: true }); validateReturnReversal(test, record);
    const forward = record.events.filter(e => e.type === 'popstate' && e.path.endsWith('/natural-arch/')).at(-1);
    check(test, 'Fast reversal includes the final detail traversal', Boolean(forward), record.events, false);
    const reopening = { ...record, phase: 'interrupted-reopen', frames: record.frames.filter(f => f.time >= forward.time),
      events: record.events.filter(e => e.time >= forward.time), draws: record.draws.filter(d => d.time >= forward.time) };
    validateTiming(test, reopening, e => e.type === 'popstate', { opening: true, sourced: true });
    check(test, 'Interrupted sequence exercised open, close and forward', record.events.some(e => e.key === 'Escape') && record.events.filter(e => e.type === 'popstate').length >= 2, record.events, false);
    await assertClean(page, test, true);
    await page.keyboard.press('Escape'); await page.waitForTimeout(600); await assertClean(page, test, false);
  });
  await runCase('history-back-forward', {}, async (page, test) => {
    await catalog(page); await page.locator(cardSelector).click(); await ready(page); await page.waitForTimeout(650);
    await arm(page, 'history-close'); await page.waitForTimeout(40); const before = await page.evaluate(() => window.__modalMotionQA.snapshot());
    await page.evaluate(() => history.back()); const closed = await collect(page, 600); test.measurements.push(closed);
    validateTiming(test, closed, e => e.type === 'popstate', { sourced: true, before }); await assertClean(page, test, false);
    await arm(page, 'history-reopen'); await page.evaluate(() => history.forward()); await ready(page); const opened = await collect(page, 450); test.measurements.push(opened);
    validateTiming(test, opened, e => e.type === 'popstate', { opening: true, sourced: true }); await assertClean(page, test, true);
    // Fixed warm-cache coverage: every cycle must pass, with no retry branch.
    for (let cycle = 1; cycle <= 3; cycle++) {
      await arm(page, `warm-cache-close-${cycle}`); const before = await page.evaluate(() => window.__modalMotionQA.snapshot());
      await page.evaluate(() => history.back()); const closed = await collect(page, 600); test.measurements.push(closed);
      validateTiming(test, closed, e => e.type === 'popstate', { sourced: true, before }); await assertClean(page, test, false);
      await arm(page, `warm-cache-reopen-${cycle}`); await page.evaluate(() => history.forward()); await ready(page);
      const opened = await collect(page, 450); test.measurements.push(opened);
      validateTiming(test, opened, e => e.type === 'popstate', { opening: true, sourced: true }); await assertClean(page, test, true);
    }
    await arm(page, 'history-interruption');
    await page.evaluate(() => { history.back(); setTimeout(() => history.forward(), 35); });
    await ready(page); const interrupted = await collect(page, 1000); test.measurements.push(interrupted); validateInvariant(test, interrupted); validateReturnReversal(test, interrupted); await assertClean(page, test, true);
    await page.keyboard.press('Escape'); await page.waitForTimeout(600); await assertClean(page, test, false);
  });
  await runCase('direct-route-no-origin', {}, async (page, test) => {
    await page.goto(base + prefix + 'models/natural-arch/'); await ready(page); await page.waitForTimeout(650);
    await arm(page, 'direct-close'); await page.locator('#close').click(); const closed = await collect(page, 700); test.measurements.push(closed);
    validateTiming(test, closed, e => e.type === 'click' && e.target === '#close', { sourced: false });
    check(test, 'Direct route closes without an invented origin flight', closed.frames.every(f => !f.flight), null, false); await assertClean(page, test, false);
    await page.goto(base + prefix + 'models/natural-arch/'); await ready(page); await page.waitForTimeout(650);
    await sequence(page, test, 'direct-route-close-evidence', async capture => {
      await arm(page, 'direct-evidence-close'); await page.locator('#close').click(); const record = await collect(page, 600);
      capture.input_events = record.events; test.evidence_measurements = record;
    });
  });
  assert(onlyCases.every(label => report.cases.some(test => test.label === label)), 'QA_CASES includes an unknown case');
  report.status = report.cases.some(test => test.status === 'fail') || report.page_errors.length ? 'fail' : baseline ? 'recorded' : 'pass';
} catch (error) { report.status = 'fail'; report.error = error.stack; }
finally {
  await browser?.close(); if (server.listening) await new Promise(resolve => server.close(resolve));
  const summary = { status: report.status, mode: report.mode, scope: report.scope, dom_raster_mode: report.dom_raster_mode, runtime_info: report.runtime_info, commit: report.commit, targets_ms: report.targets_ms,
    cases: report.cases.map(test => ({ label: test.label, status: test.status, timings: test.timings, violations: test.assertions.filter(a => !a.passed).map(({ name, enforced }) => ({ name, enforced })), error: test.error })),
    page_errors: report.page_errors, videos: report.videos, screenshot_count: report.screenshots.length };
  if (process.env.BASELINE_REPORT) {
    try {
      const previous = JSON.parse(await readFile(resolve(process.env.BASELINE_REPORT), 'utf8'));
      summary.comparison = summary.cases.flatMap(test => test.timings.map(timing => {
        const old = previous.cases.find(c => c.label === test.label)?.timings?.find(t => t.phase === timing.phase);
        return { case: test.label, phase: timing.phase, deltas_ms: old ? Object.fromEntries(['chrome_settled_ms', 'content_settled_ms', 'chrome_gone_ms', 'dialog_closed_ms'].map(k => [k, Number.isFinite(timing[k]) && Number.isFinite(old[k]) ? timing[k] - old[k] : null])) : null };
      }));
    } catch (error) { summary.comparison_error = error.message; report.status = summary.status = 'fail'; }
  }
  await mkdir(output, { recursive: true });
  await writeFile(resolve(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  await writeFile(resolve(output, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
  console.log(JSON.stringify(summary, null, 2)); if (report.status === 'fail') process.exitCode = 1;
}

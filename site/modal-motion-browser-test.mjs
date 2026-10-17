/**
 * Real Chromium regression/evidence for modal chrome and bitmap-flight coordination.
 * Run after the normal production build:
 *   QA_OUTPUT_DIR=qa/modal-motion node site/modal-motion-browser-test.mjs
 * Run this identical file against the previous build with BASELINE=1. Baseline mode
 * records (but does not enforce) the new motion contract; navigation still must work.
 * GALLERY_DIR, CHROMIUM_PATH and optional BASELINE_REPORT are supported.
 * Timing comes from capture-phase DOM input events and requestAnimationFrame, never
 * from how long a Playwright click takes. Compositor PNG evidence is a separate pass.
 */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep, basename } from 'node:path';
import assert from 'node:assert/strict';

const root = resolve(process.env.GALLERY_DIR || 'dist');
const output = resolve(process.env.QA_OUTPUT_DIR || 'qa/modal-motion');
const baseline = /^(1|true)$/i.test(process.env.BASELINE || '');
const prefix = '/lowpoly-vault/';
const cardSelector = '#grid .asset-card[data-id="natural-arch"]';
const report = {
  status: 'running', mode: baseline ? 'baseline' : 'regression', commit: process.env.GITHUB_SHA || null,
  targets_ms: { chrome_open: 240, all_content_open: 300, chrome_close: 140, reverse_flight: 180 },
  note: 'Actual Chromium rAF/computed-style/alpha measurements, software WebGL, and trusted emulated touch input. Not physical-device performance. PNG screencasts and synchronous GPU-pixel probes run separately from timing assertions to avoid readback stalls.',
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
  let frames = [], events = [], draws = [], errors = [];
  const alphaCache = new WeakMap();
  const scratch = document.createElement('canvas');
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
      background_alpha: colorAlpha(css.backgroundColor), visibility: css.visibility, display: css.display };
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
    const a = cachedAlpha(element), s = style(element);
    return { ...s, alpha: a, object: objectBounds(element, a), visible: s.effective_opacity > 0.003 && s.rect.width > 0 && s.rect.height > 0,
      background_image: getComputedStyle(element).backgroundImage };
  };
  const animationState = dialog => dialog ? dialog.getAnimations({ subtree: true }).map(a => {
    const timing = a.effect?.getComputedTiming(), target = a.effect?.target;
    return { target: target?.id || target?.className || target?.tagName || null, pseudo: a.effect?.pseudoElement || null,
      play_state: a.playState, current_time: a.currentTime, duration: timing?.duration, delay: timing?.delay,
      end_time: timing?.endTime, progress: timing?.progress };
  }) : [];
  const snapshot = source => {
    const dialog = document.querySelector('#viewer-dialog'), host = document.querySelector('#canvas-host');
    if (!dialog) return;
    const css = getComputedStyle(dialog), backdrop = getComputedStyle(dialog, '::backdrop');
    const colors = css.boxShadow.match(/rgba?\([^)]+\)|color\([^)]+\)/g) || [];
    const content = [...dialog.querySelectorAll('.asset-info > *, .viewer-topline')].filter(el => getComputedStyle(el).display !== 'none').map((el, i) => ({
      key: el.id || el.className || `${el.tagName}-${i}`, ...style(el),
    }));
    frames.push({ time: performance.now(), source, phase, open: dialog.open, marker: dialog.dataset.modalMotion || null,
      path: location.pathname, dialog: { ...style(dialog), shadow_alpha: Math.max(0, ...colors.map(colorAlpha)) },
      backdrop: { opacity: Number(backdrop.opacity), background_alpha: colorAlpha(backdrop.backgroundColor),
        effective_alpha: Number(backdrop.opacity) * colorAlpha(backdrop.backgroundColor), animation: backdrop.animationName },
      shell: style(dialog.querySelector('.viewer-layout')), content, host: style(host), model_state: host?.dataset.modelState,
      flight: visual(dialog.querySelector('.stage-flight')), handoff: visual(host?.querySelector('.model-handoff')),
      model: visual(host?.querySelector('.model-canvas')), poster: visual(host?.querySelector('.model-poster')),
      card: visual(document.querySelector('#grid [data-id="natural-arch"] .image-scrub-canvas')),
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
      phase = label; pixelProbe = pixels; frames = []; events = []; draws = []; errors = []; active = true;
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
        if (!active || !pixelProbe) return;
        try {
          const a = alpha(entry.canvas); alphaCache.set(entry.canvas, a);
          const handoff = entry.host.querySelector('.model-handoff');
          draws.push({ time: performance.now(), phase, alpha: a, object: objectBounds(entry.canvas, a), host: rect(entry.host),
            view: entry.view, handoff: objectBounds(handoff, cachedAlpha(handoff)) });
        } catch (error) { errors.push(error.message); }
      };
      snapshot('armed'); raf = requestAnimationFrame(sample);
    },
    stop() {
      snapshot('stopped'); active = false; cancelAnimationFrame(raf); observer?.disconnect();
      window.__vaultFrameProbe = previousDrawProbe;
      return { phase, pixel_probe: pixelProbe, time_origin: performance.timeOrigin, frames, events, draws, errors };
    },
    snapshot() { snapshot('manual'); return frames.at(-1); },
  };
}

function check(test, name, passed, detail, contract = true) {
  test.assertions.push({ name, passed: Boolean(passed), detail, enforced: !(baseline && contract) });
  if (!passed && !(baseline && contract)) throw new Error(`${name}: ${typeof detail === 'string' ? detail : JSON.stringify(detail)}`);
}
const near = (a, b, px = 5) => Boolean(a && b && Math.hypot(a.x - b.x, a.y - b.y) <= px &&
  Math.abs(a.width / b.width - 1) <= 0.06 && Math.abs(a.height / b.height - 1) <= 0.06);
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
    check(test, record.phase + ': flight contains transparent model pixels', f.flight.alpha?.pixels > 0 && f.flight.alpha.transparent_fraction > 0.2 && f.flight.alpha.corner_alpha_max <= 3 && f.flight.background_alpha === 0 && f.flight.background_image === 'none', f.flight.alpha);
    check(test, record.phase + ': moving bitmap does not duplicate a stationary model', ![f.model, f.handoff, f.poster].some(v => v?.visible), { time: f.time, host: f.host });
  }
  if (sourced) check(test, record.phase + ': sourced transition has no empty visual frame', visible.filter(f => f.source === 'raf').every(f =>
    f.flight?.visible || f.handoff?.visible || f.model?.visible || f.poster?.visible), visible.filter(f => f.source === 'raf' && ![f.flight, f.handoff, f.model, f.poster].some(v => v?.visible)).slice(0, 3));
  if (opening) {
    const hosts = visible.filter(f => f.host?.rect.width > 0).map(f => f.host.rect);
    const range = Object.fromEntries(['x', 'y', 'width', 'height'].map(k => [k, hosts.length ? Math.max(...hosts.map(r => r[k])) - Math.min(...hosts.map(r => r[k])) : null]));
    check(test, record.phase + ': canvas bounds stay fixed while metadata and chrome enter', hosts.length > 1 && Object.values(range).every(x => x <= 1), range);
    const comparisons = record.draws.filter(d => d.handoff).map(d => ({ actual: d.object, handoff: d.handoff }));
    if (record.pixel_probe) {
    check(test, record.phase + ': actual GLB silhouette matches retained handoff', comparisons.length > 0 && comparisons.every(p => near(p.actual, p.handoff)), comparisons.slice(0, 3));
    check(test, record.phase + ': actual GLB draws remain transparent', record.draws.length > 0 && record.draws.every(d => d.alpha?.transparent_fraction > 0.2 && d.alpha.corner_alpha_max <= 3), { draws: record.draws.length });
    }
    const stationary = visible.filter(f => f.source === 'raf' && !f.flight && f.model?.object && f.model_state === 'ready');
    check(test, record.phase + ': model bounds remain continuous after flight handoff', stationary.slice(1).every((f, i) => near(stationary[i].model.object, f.model.object)), { samples: stationary.length });
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
    }
  } else {
    check(test, record.phase + ': chrome vanishes without an opaque closing tail', s.chrome_gone_ms !== null && s.chrome_gone_ms <= (reduced ? 80 : 140) + slack, { actual_ms: s.chrome_gone_ms, limit_ms: (reduced ? 80 : 140) + slack });
    check(test, record.phase + ': click-to-dialog-close is bounded', s.dialog_closed_ms !== null && s.dialog_closed_ms <= (reduced ? 80 : 180) + slack, { actual_ms: s.dialog_closed_ms, limit_ms: (reduced ? 80 : 180) + slack });
    check(test, record.phase + ': no late chrome reappears', frames.filter(f => f.time - event.time >= (reduced ? 80 : 140) + slack).every(f => !f.open || (f.shell.opacity <= 0.025 && f.backdrop.effective_alpha <= 0.025 && f.dialog.shadow_alpha <= 0.025)), s);
    if (!reduced && sourced) {
      const flights = visible.filter(f => f.flight?.visible);
      check(test, record.phase + ': reverse flight actually runs', flights.length > 1, { frames: flights.length });
      check(test, record.phase + ': closing keeps the transparent bitmap after chrome fades', flights.some(f => f.shell.opacity <= 0.04), flights.map(f => ({ t: f.time - event.time, shell: f.shell.opacity })));
      const flightDurations = flights.flatMap(f => f.animations.filter(a => String(a.target).includes('stage-flight')).map(a => a.duration));
      check(test, record.phase + ': reverse flight is an 180 ms animation', flightDurations.length > 0 && flightDurations.every(ms => typeof ms === 'number' && ms <= 180 && ms >= 160), flightDurations);
      if (before?.model?.object) check(test, record.phase + ': first reverse bitmap matches current model bounds', near(before?.model?.object, flights[0]?.flight?.object, 12), { before: before?.model?.object, first: flights[0]?.flight?.object });
      const retained = frames.filter(f => !f.open && f.card?.object).at(-1)?.card?.object;
      check(test, record.phase + ': reverse bitmap lands on the retained card', near(flights.at(-1)?.flight?.object, retained, 14), { last: flights.at(-1)?.flight?.object, retained });
    }
  }
  if (reduced) check(test, record.phase + ': reduced motion has no flight or ongoing chrome animation', visible.every(f => !f.flight && !f.animations.some(a => a.play_state === 'running' && Number(a.duration) > 0)), { samples: visible.length });
}

async function arm(page, phase, pixels = false) { await page.evaluate(({ phase, pixels }) => window.__modalMotionQA.arm(phase, { pixels }), { phase, pixels }); }
async function collect(page, ms = 800) { await page.waitForTimeout(ms); return page.evaluate(() => window.__modalMotionQA.stop()); }
async function ready(page) {
  await page.waitForFunction(() => {
    const d = document.querySelector('#viewer-dialog'), h = document.querySelector('#canvas-host');
    return d?.open && h?.dataset.modelState === 'ready' && h.dataset.presentedUrl?.endsWith('/natural-arch.glb') && Number(h.dataset.renderTriangles) > 0;
  }, null, { timeout: 30000 });
}
async function catalog(page, { touch = false, lang = '' } = {}) {
  await page.goto(base + prefix + (lang ? lang + '/' : '') + 'models/');
  await page.waitForFunction(() => document.querySelector('#grid')?.getAttribute('aria-busy') === 'false');
  const card = page.locator(cardSelector); await card.scrollIntoViewIfNeeded();
  await card.locator('.asset-image > img').evaluate(async image => { if (!image.complete) await image.decode(); });
  await page.waitForTimeout(650);
  if (touch) {
    // A genuine CDP touch gesture activates the image preview, followed later by
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
  await page.waitForFunction(() => document.querySelector('#grid [data-id="natural-arch"] .image-scrub-canvas')?.width > 0);
  await page.waitForTimeout(100);
}
async function cleanupState(page, open) {
  return page.evaluate(open => {
    const dialog = document.querySelector('#viewer-dialog');
    return { expected_open: open, open: dialog.open, marker: dialog.dataset.modalMotion || null, path: location.pathname,
      overflow: document.body.style.overflow, flights: document.querySelectorAll('.stage-flight').length,
      handoffs: document.querySelectorAll('.model-handoff').length, canvases: document.querySelectorAll('#canvas-host .model-canvas').length,
      live_scenes: window.__vaultGPU?.liveScenes ?? null, focus_id: document.activeElement?.dataset.id || null,
      active_animations: dialog.getAnimations({ subtree: true }).filter(a => a.playState === 'running' || a.playState === 'paused').map(a => ({ target: a.effect?.target?.id || a.effect?.target?.className, state: a.playState })),
      host_opacity: document.querySelector('#canvas-host').style.opacity, layout_class: document.querySelector('.viewer-layout').className };
  }, open);
}
async function assertClean(page, test, open) {
  await page.waitForFunction(open => document.querySelector('#viewer-dialog').open === open, open, { timeout: 5000 });
  const state = await cleanupState(page, open); (test.cleanup ||= []).push(state);
  check(test, 'Final dialog and route agree', state.open === open && (open ? state.path.endsWith('/natural-arch/') : state.path.endsWith('/models/')), state, false);
  check(test, 'No stale flights, handoffs, animation locks or body lock', state.flights === 0 && state.handoffs === 0 && state.active_animations.length === 0 && state.host_opacity !== '0' && !state.layout_class.includes('motion-running') && (open ? state.overflow === 'hidden' : state.overflow !== 'hidden'), state);
  check(test, 'Exactly the expected number of live detail scenes', state.canvases === (open ? 1 : 0) && (state.live_scenes === null || state.live_scenes === (open ? 1 : 0)), state, false);
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
  await session.send('Page.startScreencast', { format: 'png', everyNthFrame: 1 });
  try { await action(capture); } finally {
    await session.send('Page.stopScreencast').catch(() => {}); session.off('Page.screencastFrame', listener);
    await Promise.all(pending); await session.detach();
    (test.evidence_sequences ||= []).push(capture);
  }
  check(test, label + ': real compositor screenshot sequence captured', capture.frames.length >= (test.label === 'reduced-motion' || label.startsWith('direct-route') ? 2 : 3), { frames: capture.frames.length }, false);
}
async function evidenceRoundTrip(page, test, { touch = false } = {}) {
  await sequence(page, test, test.label + '-evidence', async capture => {
    await arm(page, 'evidence-open', true);
    await page.locator(cardSelector)[touch ? 'tap' : 'click']();
    const opened = await collect(page, 850); await ready(page);
    await page.waitForTimeout(200);
    await arm(page, 'evidence-close', true); await page.locator('#close')[touch ? 'tap' : 'click']();
    const closed = await collect(page, 500);
    capture.input_events = [...opened.events, ...closed.events];
    capture.frames.forEach(frame => { frame.since_open_ms = frame.browser_time_ms - (opened.events.find(e => e.type === 'click' && e.target === 'card:natural-arch')?.time ?? 0); frame.since_close_ms = frame.browser_time_ms - (closed.events.find(e => e.type === 'click' && e.target === '#close')?.time ?? 0); });
    test.evidence_measurements = { open: opened, close: closed };
    validateInvariant(test, opened, { opening: true, sourced: true });
  });
}
async function runCase(label, options, body) {
  const viewport = options.viewport || { width: 1440, height: 1000 };
  const context = await browser.newContext({ viewport, reducedMotion: 'no-preference', recordVideo: { dir: output, size: viewport }, ...options });
  const page = await context.newPage(); page.setDefaultTimeout(15000); await page.addInitScript(installProbe);
  const test = { label, status: 'running', assertions: [], timings: [], measurements: [] }; report.cases.push(test);
  page.on('pageerror', error => report.page_errors.push({ label, error: error.message }));
  try { await body(page, test); test.status = baseline ? 'recorded' : 'pass'; }
  catch (error) {
    test.status = 'fail'; test.error = error.stack;
    test.last_measurement = await page.evaluate(() => window.__modalMotionQA?.stop()).catch(() => null);
    const filename = label + '-failure.png';
    await page.screenshot({ path: resolve(output, filename), fullPage: false }).then(() => report.screenshots.push(filename)).catch(() => {});
  } finally {
    const video = page.video(); await context.close();
    if (video) report.videos.push({ label, file: basename(await video.path()) });
    await writeFile(resolve(output, label + '.json'), JSON.stringify(test, null, 2) + '\n');
  }
}
async function roundTrip(page, test, { touch = false, reduced = false, lang = '' } = {}) {
  await catalog(page, { touch, lang });
  // A short network gate exercises chrome independent of the actual GLB load.
  await page.route('**/*.glb', async route => { await new Promise(resolve => setTimeout(resolve, 380)); await route.continue().catch(() => {}); });
  await arm(page, 'open'); await page.locator(cardSelector)[touch ? 'tap' : 'click']();
  await ready(page); const opened = await collect(page, 450); test.measurements.push(opened);
  validateTiming(test, opened, e => e.type === 'click' && e.target === 'card:natural-arch', { opening: true, reduced, sourced: true });
  if (touch) check(test, 'Mobile open was a trusted touch tap', opened.events.some(e => e.type === 'pointerup' && e.pointer_type === 'touch' && e.trusted) && opened.events.some(e => e.type === 'touchend' && e.trusted), opened.events, false);
  await page.waitForTimeout(250); await assertClean(page, test, true);
  // Change the actual GLB camera so close cannot silently substitute the poster.
  await arm(page, 'close');
  await page.locator('#canvas-host').focus(); await page.keyboard.press('ArrowRight'); await page.keyboard.press('ArrowUp');
  await page.waitForTimeout(100);
  const before = await page.evaluate(() => window.__modalMotionQA.snapshot());
  await page.locator('#close')[touch ? 'tap' : 'click'](); const closed = await collect(page, 600); test.measurements.push(closed);
  validateTiming(test, closed, e => e.type === 'click' && e.target === '#close', { opening: false, reduced, sourced: true, before });
  if (touch) check(test, 'Mobile close was a trusted touch tap', closed.events.some(e => e.type === 'pointerup' && e.pointer_type === 'touch' && e.trusted), closed.events, false);
  await assertClean(page, test, false);
  check(test, 'Focus returns to the source card', await page.evaluate(() => document.activeElement?.dataset.id === 'natural-arch'), null, false);
  await evidenceRoundTrip(page, test, { touch }); await assertClean(page, test, false);
}

try {
  await mkdir(output, { recursive: true });
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  base = `http://127.0.0.1:${server.address().port}`;
  browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined,
    args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
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
    const record = await collect(page, 1000); test.measurements.push(record); validateInvariant(test, record);
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
    await arm(page, 'history-interruption');
    await page.evaluate(() => { history.back(); setTimeout(() => history.forward(), 35); });
    await ready(page); const interrupted = await collect(page, 1000); test.measurements.push(interrupted); validateInvariant(test, interrupted); await assertClean(page, test, true);
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
  report.status = report.cases.some(test => test.status === 'fail') || report.page_errors.length ? 'fail' : baseline ? 'recorded' : 'pass';
} catch (error) { report.status = 'fail'; report.error = error.stack; }
finally {
  await browser?.close(); if (server.listening) await new Promise(resolve => server.close(resolve));
  const summary = { status: report.status, mode: report.mode, commit: report.commit, targets_ms: report.targets_ms,
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

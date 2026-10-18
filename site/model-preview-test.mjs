// Controller contracts with deterministic DOM/stage stand-ins. Real GLB resource
// ownership is tested by viewer-resource-test; rasterization requires browser QA.
import assert from 'node:assert/strict';
import { SharedModelPreview } from './model-preview.js';
import { CARD_RENDER_PRESET } from './render-preset.js';

const listeners = new Map(), frames = new Map();
let nextFrame = 0, checks = 0;
const deferred = () => { let resolve, reject; const promise = new Promise((a, b) => { resolve = a; reject = b; }); return { promise, resolve, reject }; };
const tick = () => new Promise(resolve => setTimeout(resolve, 0));
const flush = time => { const pending = [...frames.values()]; frames.clear(); pending.forEach(callback => callback(time)); };
const canvas = () => ({ width: 320, height: 320, dataset: {}, setAttribute() {}, remove() { this.removed = true; }, getContext: () => ({ drawImage() {}, clearRect() {} }) });
globalThis.matchMedia = () => ({ matches: true }); // Legacy controller contracts use reduced motion; reveal has dedicated raster coverage.
globalThis.document = { hidden: false, addEventListener: (name, callback) => listeners.set(name, callback), removeEventListener: name => listeners.delete(name), createElement: canvas };
globalThis.requestAnimationFrame = callback => { frames.set(++nextFrame, callback); return nextFrame; };
globalThis.cancelAnimationFrame = id => frames.delete(id);
globalThis.IntersectionObserver = class { constructor(callback) { this.callback = callback; } observe(target) { this.target = target; } disconnect() { this.target = null; } };
function card(id) {
  const status = { textContent: '' }, host = { children: [], append(node) { this.children.push(node); } };
  return { id, isConnected: true, dataset: {}, status, host, querySelector: selector => selector === '.card-status' ? status : host };
}
const asset = id => ({ id, glb: `assets/${id}/${id}.glb`, turntable: { manifest: `never-fetch/${id}.json` } });
function harness({ stageGate, showGate, failure } = {}) {
  let gets = 0;
  const shows = [], views = [];
  const stage = {
    _host: null, hidden: 0, snapshots: 0, showGate, failure,
    presentationInfo: { azimuth_deg: CARD_RENDER_PRESET.camera.azimuth_deg, elevation_deg: CARD_RENDER_PRESET.camera.elevation_deg, distance: 6 },
    async show(host, url, options) {
      shows.push({ host, url, options });
      options.onStatus('loading');
      if (this.showGate) { const gate = this.showGate; this.showGate = null; await gate.promise; }
      if (options.signal.aborted) return false;
      if (this.failure) { options.onStatus('error'); throw this.failure; }
      this._host = host;
      if (options.initialView) this.presentationInfo = { ...options.initialView };
      options.onStatus('ready'); return true;
    },
    setView(azimuth, elevation, distance) {
      this.presentationInfo = { azimuth_deg: ((azimuth % 360) + 360) % 360, elevation_deg: elevation, distance: distance ?? this.presentationInfo.distance };
      views.push({ ...this.presentationInfo });
    },
    snapshot(options) { this.snapshots++; this.snapshotOptions = options; const result = canvas(); result.__presentation = { ...this.presentationInfo }; return result; },
    hide() { this.hidden++; this._host = null; },
  };
  const controller = new SharedModelPreview({ resolvePath: path => '/lowpoly-vault/' + path, getStage: async () => { gets++; return stageGate ? stageGate.promise : stage; } });
  return { controller, stage, shows, views, get gets() { return gets; } };
}
function dispose(h) { h.controller.dispose(); assert.equal(frames.size, 0); assert.equal(listeners.size, 0); checks++; }

{
  const h = harness(), c = h.controller, a = card('arch');
  assert.equal(h.gets, 0, 'Creating the controller leaves the viewer lazy');
  assert.equal(c.stats.kind, 'shared-real-model');
  assert.equal(c.activate(a, {}), false); a.isConnected = false;
  assert.equal(c.activate(a, asset('arch')), false); a.isConnected = true;
  assert(c.activate(a, asset('arch'))); c.request(1); c.request(3.5); c.request(7.25);
  await c.pending; assert.equal(h.shows.length, 1); assert.equal(h.gets, 1);
  assert.equal(h.shows[0].url, '/lowpoly-vault/assets/arch/arch.glb');
  assert.equal(h.shows[0].options.mode, 'hover');
  assert.equal(a.dataset.previewState, 'ready'); assert.equal(frames.size, 1);
  flush(); assert.equal(h.views.length, 1, 'Loading/pointer intents coalesce to one latest draw');
  assert.equal(h.stage.presentationInfo.azimuth_deg, 150.75); assert.equal(c.stats.frame, 7.25);
  assert.equal(c.stats.frameRequests, 0); assert.equal(c.stats.manifestRequests, 0);
  c.activate(a, asset('arch')); assert.equal(h.gets, 1, 'Repeated activation of live card is a no-op');
  for (const n of [2, 8, 11.5]) c.request(n);
  assert.equal(frames.size, 1); flush(); assert.equal(h.views.length, 2); assert.equal(h.stage.presentationInfo.azimuth_deg, 214.5);
  c.request(23); c.step(1); flush(); assert.equal(h.stage.presentationInfo.azimuth_deg, 42, 'Orbit wraps physically at 360 degrees');
  assert.equal(frames.size, 0, 'No autoplay or idle animation loop');
  c.stop(); assert.equal(c.stats.activeId, null); assert.equal(a.dataset.previewState, undefined); assert.equal(h.stage.hidden, 1);
  dispose(h);
}
{
  const gate = deferred(), h = harness({ stageGate: gate }), c = h.controller;
  const a = card('arch'), b = card('tree');
  c.activate(a, asset('arch')); const old = c.pending;
  c.activate(b, asset('tree')); gate.resolve(h.stage);
  assert.equal(await old, false); assert.equal(await c.pending, true);
  assert.equal(h.shows.length, 1, 'A superseded lazy import cannot start stale GLB work');
  assert.equal(h.shows[0].host, b.host); assert.equal(a.dataset.previewState, undefined);
  assert.equal(c.stats.activeId, 'tree'); dispose(h);
}
{
  const gate = deferred(), h = harness({ showGate: gate }), c = h.controller;
  const a = card('arch'), b = card('tree');
  c.activate(a, asset('arch')); await tick(); const old = c.pending, oldOptions = h.shows[0].options;
  c.activate(b, asset('tree')); await c.pending;
  assert(oldOptions.signal.aborted); oldOptions.onStatus('ready');
  assert.equal(a.dataset.previewState, undefined, 'A stale ready callback cannot resurrect the old card');
  assert.equal(c.stats.activeId, 'tree'); gate.resolve(); assert.equal(await old, false);
  assert.equal(b.dataset.previewState, 'ready'); dispose(h);
}
{
  const h = harness(), c = h.controller, a = card('arch');
  c.activate(a, asset('arch')); await c.pending; c.request(7);
  const snapshot = c.capture({ transfer: true });
  assert.deepEqual(h.stage.snapshotOptions, { square: true }, 'Card handoff captures the centered framing square, without rectangular card margins.');
  assert.equal(frames.size, 0); assert.equal(snapshot.view.azimuth_deg, 147, 'Capture synchronously flushes latest pointer intent');
  assert.equal(snapshot.canvas.__presentation.azimuth_deg, 147); assert.equal(snapshot.id, 'arch');
  c.stop(); assert(!snapshot.canvas.removed, 'A copied live draw belongs to the modal after capture');
  const view = { azimuth_deg: 186, elevation_deg: 29, distance: 4.2 };
  c.retainSnapshot(a, asset('arch'), snapshot.canvas, view, { transfer: true });
  assert.equal(c.canvas, snapshot.canvas); assert.equal(c.canvas.className, 'model-preview-snapshot');
  assert.equal(c.stats.frame, 9.6); assert.equal(c.stats.activeId, 'arch');
  const captured = c.capture({ transfer: true }); assert.equal(captured.canvas, snapshot.canvas); assert.equal(c.canvas, null);
  c.stop(); assert(!captured.canvas.removed, 'Transferring retained snapshot does not zero its backing');
  c.retainSnapshot(a, asset('arch'), captured.canvas, view, { transfer: true });
  const gate = deferred(); h.stage.showGate = gate; c.activate(a, asset('arch')); await tick();
  assert.equal(c.canvas, captured.canvas); assert(!captured.canvas.removed, 'Retained bitmap stays visible until first ready draw');
  assert.deepEqual(h.shows.at(-1).options.initialView, view);
  gate.resolve(); await c.pending;
  assert(captured.canvas.removed); assert.equal(captured.canvas.width, 0); assert.equal(c.canvas, null);
  assert.deepEqual(h.stage.presentationInfo, view, 'Returned azimuth, elevation and zoom survive reacquisition');
  dispose(h);
}
{
  const h = harness({ failure: new Error('Intentional model failure') }), c = h.controller, a = card('arch');
  c.activate(a, asset('arch')); assert.equal(await c.pending, false);
  assert.equal(a.dataset.previewState, 'fallback'); assert.equal(c.stats.errors, 1);
  c.request(5); flush(); assert.equal(h.shows.length, 1, 'Idle/request input cannot create a retry loop');
  h.stage.failure = null; c.activate(a, asset('arch')); assert.equal(await c.pending, true);
  assert.equal(a.dataset.previewState, 'ready'); dispose(h);
}
{
  const h = harness(), c = h.controller, a = card('arch');
  c.activate(a, asset('arch')); await c.pending; c.request(4);
  c.intersection.callback([{ target: a, isIntersecting: false }]);
  assert.equal(c.stats.activeId, null); assert.equal(frames.size, 0);
  c.activate(a, asset('arch')); await c.pending; document.hidden = true; listeners.get('visibilitychange')();
  assert.equal(c.stats.activeId, null); assert.equal(frames.size, 0); document.hidden = false;
  // Stopping a card controller cannot hide a stage already handed to detail.
  c.activate(a, asset('arch')); await c.pending; const hidden = h.stage.hidden;
  h.stage._host = {}; c.stop(); assert.equal(h.stage.hidden, hidden);
  dispose(h);
}
{
  globalThis.matchMedia = () => ({ matches: false });
  const h = harness(), c = h.controller, a = card('arch'), poster = canvas();
  const query = a.querySelector;
  a.querySelector = selector => selector === '.asset-image img' ? poster : query(selector);
  c.activate(a, asset('arch')); c.request(7); await c.pending;
  assert(c.revealMotion, 'Actual reveal retains held orbit input');
  assert.equal(h.stage.presentationInfo.azimuth_deg, 42);
  assert.equal(c.capture().view.azimuth_deg, 42, 'Mid-reveal capture keeps displayed pose, not held intent');
  let time = performance.now();
  while (c.revealMotion) { time += 50; flush(time); }
  assert.equal(h.stage.presentationInfo.azimuth_deg, 147, 'Reveal endpoint commits held intent synchronously');
  assert.equal(frames.size, 0, 'No invisible pending orbit RAF remains for Enter to flush');
  assert.equal(c.capture().view.azimuth_deg, 147, 'Immediate endpoint capture matches visible live pose');
  dispose(h); globalThis.matchMedia = () => ({ matches: true });
}
console.log(JSON.stringify({ status: 'pass', checks, covers: ['lazy GLB acquisition and invalid targets', 'continuous latest-intent camera orbit', 'no frame/manifest fetches', 'superseded import/show callbacks', 'copy/transfer snapshot ownership', 'retained pose and zoom', 'failure fallback and explicit recovery', 'visibility/offscreen stop and detail ownership'] }, null, 2));

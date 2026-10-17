import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { RETURN_TIMING, shortestAngleDelta, interpolateReturnView, startModelReturn } from './return-motion.js';

const rafs = new Map(), timers = new Map();
const listeners = new Map();
let id = 0, now = 1000;
globalThis.performance = { now: () => now };
globalThis.requestAnimationFrame = callback => { rafs.set(++id, callback); return id; };
globalThis.cancelAnimationFrame = key => rafs.delete(key);
globalThis.setTimeout = callback => { timers.set(++id, callback); return id; };
globalThis.clearTimeout = key => timers.delete(key);
globalThis.document = { hidden: false, addEventListener: (name, fn) => listeners.set(name, fn), removeEventListener: name => listeners.delete(name) };
const frame = elapsed => { now = 1000 + elapsed; const pending = [...rafs.values()]; rafs.clear(); pending.forEach(fn => fn(now)); };
const near = (a, b) => assert(Math.abs(a - b) < 1e-9, `${a} != ${b}`);
const from = { left: 100, top: 80, width: 600, height: 600 }, to = { left: 720, top: 620, width: 240, height: 240 };
const initialView = { azimuth_deg: 350, elevation_deg: 61, distance: 3 }, canonicalView = { azimuth_deg: 42, elevation_deg: 23.3, distance: 5 };
function setup(extra = {}) {
  now = 1000;
  const host = { style: { setProperty(name, value) { this[name] = value; } }, dataset: {} }, calls = [], aligned = [];
  const stage = { _host: host, setView(...view) { calls.push({ view, phase: host.dataset.returnPhase, progress: host.dataset.returnProgress, transform: host.style.transform }); } };
  const motion = startModelReturn({ stage, host, from, to, initialView, canonicalView, onAligned: () => aligned.push(calls.at(-1)), ...extra });
  return { host, stage, calls, aligned, motion };
}
assert.equal(shortestAngleDelta(350, 42), 52);
assert.equal(shortestAngleDelta(43, 42), -1);
near(shortestAngleDelta(41.999, 42), .001);
assert.equal(shortestAngleDelta(10, 350), -20);
assert.deepEqual(interpolateReturnView(initialView, canonicalView, 0), initialView);
const a = setup();
frame(0); assert.deepEqual(a.calls.at(-1).view, [350, 61, 3]);
frame(60); const middle = interpolateReturnView(initialView, canonicalView, .5);
assert.deepEqual(a.calls.at(-1).view, [middle.azimuth_deg, middle.elevation_deg, middle.distance]);
assert(a.calls.at(-1).transform.includes('542.5px'), 'Camera and shrink use the same eased progress before the actual draw.');
frame(120); assert.deepEqual(a.calls.at(-1).view, [42, 23.3, 5]);
assert.equal(a.calls.at(-1).phase, 'fading'); assert.equal(a.calls.at(-1).progress, '1');
assert.equal(a.aligned.length, 1); assert.equal(a.host.dataset.returnOpacity, '1');
const alignedDraws = a.calls.length;
frame(150); assert.equal(a.host.dataset.returnOpacity, '.5'.replace(/^\./, '0.')); assert.equal(a.calls.length, alignedDraws, 'Aligned fade starts no model rotation or idle render loop.');
frame(180); assert.equal(await a.motion.finished, true); assert.equal(a.host.dataset.returnOpacity, '0');
assert.equal(rafs.size, 0); assert.equal(timers.size, 0); assert.equal(a.aligned.length, 1);
const b = setup(); b.motion.cancel(); assert.equal(await b.motion.finished, false); frame(180);
assert.equal(b.calls.length, 0); assert.equal(b.aligned.length, 0); assert.equal(rafs.size, 0); assert.equal(timers.size, 0);
const c = setup(); c.stage._host = {}; frame(30); assert.equal(await c.motion.finished, false); assert.equal(c.calls.length, 0, 'A late return callback cannot draw into a newer owner.');
const d = setup({ reduced: true }); assert.equal(await d.motion.finished, true); assert.deepEqual(d.calls[0].view, [42, 23.3, 5]);
assert.equal(d.calls[0].phase, 'fading'); assert.equal(rafs.size, 0); assert.equal(timers.size, 0);
const e = setup(); document.hidden = true; [...timers.values()][0](); assert.equal(await e.motion.finished, true); assert.equal(rafs.size, 0); assert.equal(timers.size, 0, 'Hidden-tab deadline also releases finite animation callbacks.'); document.hidden = false;
const f = setup(); frame(250); assert.equal(f.host.dataset.returnOpacity, '1', 'A delayed canonical draw still starts a complete visible fade.');
[...timers.values()][0](); assert.equal(f.motion.playState, 'running', 'A visible-page deadline cannot erase the aligned fade.');
frame(280); near(Number(f.host.dataset.returnOpacity), .5); frame(310); assert.equal(await f.motion.finished, true);
assert.equal(rafs.size, 0); assert.equal(timers.size, 0); assert.equal(listeners.size, 0);
const g = setup(); document.hidden = true; listeners.get('visibilitychange')(); assert.equal(await g.motion.finished, true); document.hidden = false;
assert.equal(rafs.size, 0); assert.equal(timers.size, 0); assert.equal(listeners.size, 0, 'Hiding a page retires all finite-motion callbacks immediately.');
// Execute the production capture helper against premultiplied sample pixels.
// Stacking two half-alpha copies source-over would produce alpha .75, not .5.
const main = readFileSync(new URL('./main.js', import.meta.url), 'utf8');
const helper = main.slice(main.indexOf('function paintVisualBlend('), main.indexOf('function currentDetailVisual('));
const pixelDocument = { createElement() {
  const canvas = { dataset: {}, pixel: [0, 0, 0, 0], setAttribute() {} };
  const context = { globalAlpha: 1, globalCompositeOperation: 'source-over', clearRect() { canvas.pixel = [0, 0, 0, 0]; }, drawImage(source) {
    const a = source.pixel[3] * this.globalAlpha;
    const value = [...source.pixel.slice(0, 3).map(c => c * this.globalAlpha), a];
    canvas.pixel = canvas.pixel.map((c, i) => this.globalCompositeOperation === 'lighter' ? c + value[i] : value[i] + c * (1 - a));
  } };
  canvas.getContext = () => context; return canvas;
} };
const blend = new Function('document', helper + ';return blendVisual;')(pixelDocument);
const lower = { width: 320, height: 320, pixel: [.2, .1, .05, .5], dataset: { assetId: 'conifer-tree' }, __presentation: canonicalView };
const upper = { ...lower, pixel: [.21, .11, .06, .5] };
for (const weight of [0, .001667, .25, .5, .75, 1]) {
  const result = blend(lower, upper, weight);
  near(result.pixel[3], .5);
  result.pixel.forEach((value, i) => near(value, lower.pixel[i] * (1 - weight) + upper.pixel[i] * weight));
  assert.equal(result.dataset.assetId, lower.dataset.assetId); assert.equal(result.__presentation, canonicalView);
}
assert.deepEqual(lower.pixel, [.2, .1, .05, .5], 'Weighted captures never mutate retained model pixels.');
console.log(JSON.stringify({ status: 'pass', timing: RETURN_TIMING, covers: ['shortest-angle interpolation', 'shared camera and square-flight easing', 'exact canonical alignment before poster fade', 'finite close-only RAF', 'cancel/new-owner safety', 'instant reduced motion', 'hidden-tab deadline'] }, null, 2));

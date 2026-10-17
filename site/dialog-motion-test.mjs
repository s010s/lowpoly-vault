import assert from 'node:assert/strict';
import { DialogMotion, DIALOG_TIMING } from './dialog-motion.js';

const pending = [];
const deadlines = new Map(); let nextDeadline = 0;
globalThis.setTimeout = (callback, delay) => { deadlines.set(++nextDeadline, { callback, delay }); return nextDeadline; };
globalThis.clearTimeout = id => deadlines.delete(id);
function element(name) {
  return { name, style: {}, opacity: '1', shadow: '0px 35px 150px rgba(0, 0, 0, 0.6)', animate(frames, options) {
    let resolve;
    const animation = { name, frames, options, finished: new Promise(done => { resolve = done; }),
      cancelled: false, cancel() { this.cancelled = true; resolve(); }, finish() { resolve(); } };
    pending.push(animation);
    return animation;
  } };
}
const shadow = element('shadow'), panel = element('panel'), content = [element('theme'), element('close')];
const dialog = Object.assign(element('dialog'), {
  open: false, dataset: {}, backdrop: '1', properties: new Map(),
  ownerDocument: { documentElement: {} },
  querySelector: selector => selector === '.modal-chrome-shadow' ? shadow : panel,
  querySelectorAll(selector) {
    assert.equal(selector, ':scope > button', 'Panel descendants share its fade instead of acquiring nested opacity surfaces');
    return content;
  },
  getBoundingClientRect: () => ({left: 20, top: 32, width: 1000, height: 600}),
  removeAttribute(name) { if (name === 'data-modal-motion') delete this.dataset.modalMotion; },
});
dialog.style = { setProperty: (name, value) => dialog.properties.set(name, value), removeProperty: name => dialog.properties.delete(name) };
const listeners = new Set();
const reduced = { matches: false, addEventListener(type, fn) { listeners.add(fn); }, removeEventListener(type, fn) { listeners.delete(fn); } };
globalThis.ResizeObserver = class { observe() {} disconnect() {} };
globalThis.getComputedStyle = (node, pseudo) => pseudo ? { opacity: node.backdrop } : { opacity: node.opacity, boxShadow: node.shadow };
const motion = new DialogMotion(dialog, reduced);
assert.equal(motion.capture(), null, 'A closed dialog starts transparent');
dialog.open = true;
const opening = motion.start();
assert.equal(dialog.dataset.modalMotion, 'opening');
assert.equal(pending.length, 4, 'Only the panel, two outer buttons and shadow own opacity animations');
assert.equal(dialog.properties.get('--modal-backdrop-start'), '0');
assert.equal(dialog.properties.get('--modal-backdrop-duration'), '220ms');
assert.equal(pending[0].options.duration, DIALOG_TIMING.panelOpen);
assert.deepEqual(pending[0].frames, [{ opacity: 0 }, { opacity: 1 }]);
assert(pending.every(animation => animation.options.fill === 'both'));
assert(pending.every(animation => animation.frames.every(frame => !('transform' in frame))), 'Chrome cannot move the canvas or its containing block');
assert(pending.every(animation => animation.frames.every(frame => !('boxShadow' in frame))), 'Blur stays static on its own opacity-composited layer');
assert.deepEqual(shadow.style, { left: '20px', top: '32px', width: '1000px', height: '600px' });
assert(pending.filter(animation => animation.name !== 'shadow').every(animation => animation.options.duration + (animation.options.delay || 0) <= 240));

// Reverse from the current painted opacity, not from an opaque modal flash.
panel.opacity = '.42'; content.forEach(node => node.opacity = '.19'); dialog.backdrop = '.55';
const captured = motion.capture();
const closing = motion.start({ reverse: true, from: captured });
assert.equal(dialog.dataset.modalMotion, 'closing');
assert.equal(dialog.properties.get('--modal-backdrop-start'), '0.55');
const closingAnimations = [...motion.active];
assert.deepEqual(closingAnimations[0].frames, [{ opacity: .42 }, { opacity: 0 }]);
assert(closingAnimations.every(animation => animation.options.duration <= 140 && !animation.options.delay));
assert.equal([...deadlines.values()][0].delay, 140, 'A busy compositor cannot add a scheduling tail to the chrome dismissal');
await opening;
assert.equal(dialog.dataset.modalMotion, 'closing', 'A superseded opener cannot clear the closing state');
[...deadlines.values()][0].callback();
await closing;
assert.equal(dialog.properties.get('--modal-backdrop-duration'), '0ms', 'The CSS backdrop shares the dismissal deadline');
assert.equal(deadlines.size, 0, 'Completed exit releases its deadline');
assert.equal(dialog.dataset.modalMotion, 'closing', 'Exit opacity stays at zero until dialog.close()');

const reopening = motion.start({ from: motion.capture() });
const latest = [...motion.active]; latest.forEach(animation => animation.finish()); await reopening;
assert.equal(dialog.dataset.modalMotion, 'open');
assert.equal(motion.active.size, 0, 'Settled open leaves no owned animations');
assert.equal(dialog.properties.size, 0);

reduced.matches = true;
const count = pending.length;
await motion.start(); await motion.start({ reverse: true });
assert.equal(pending.length, count, 'Reduced motion starts no chrome animation');
reduced.matches = false;
const changingPreference = motion.start(); reduced.matches = true; listeners.forEach(fn => fn()); await changingPreference;
assert.equal(motion.active.size, 0, 'Changing to reduced motion finishes an in-flight opener');
motion.dispose(); assert.equal(listeners.size, 0);
assert.equal(deadlines.size, 0);
console.log('Dialog motion: overlapping entry, short exit, interrupted reversal, stale completion, reduced motion, and disposal pass.');

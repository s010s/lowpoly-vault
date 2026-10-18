import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createCatalogScroll } from './catalog-scroll.js';

const observers = [];
globalThis.ResizeObserver = globalThis.MutationObserver = class {
  constructor(callback) { this.callback = callback; this.targets = []; observers.push(this); }
  observe(target, options) { this.targets.push({ target, options }); }
  disconnect() { this.disconnected = true; }
};
function element() {
  return { hidden: false, attributes: new Map(), children: [],
    setAttribute(key, value) { this.attributes.set(key, value); },
    removeAttribute(key) { this.attributes.delete(key); },
    toggleAttribute(key, value) { if (value) this.attributes.set(key, ''); else this.attributes.delete(key); },
    append(child) { this.children.push(child); }, remove() { this.removed = true; },
  };
}
const root = Object.assign(element(), { scrollHeight: 1800 });
const body = element(), catalog = { getBoundingClientRect: () => ({ bottom }) };
const dialog = { open: false }, listeners = new Map(), frames = new Map();
let bottom = 1800, text = 'Scroll to explore', nextFrame = 0;
const view = { innerHeight: 900,
  requestAnimationFrame(callback) { frames.set(++nextFrame, callback); return nextFrame; },
  cancelAnimationFrame(id) { frames.delete(id); },
  addEventListener(type, callback, options) { listeners.set(type, { callback, options }); },
  removeEventListener(type, callback) { assert.equal(listeners.get(type).callback, callback); listeners.delete(type); },
};
const doc = { documentElement: root, body, createElement: element };
const controller = createCatalogScroll({ catalog, dialog, label: () => text, doc, view });
const cue = body.children[0];
function flush() { const pending = [...frames.values()]; frames.clear(); pending.forEach(callback => callback()); }
assert(cue.hidden);
assert.equal(cue.attributes.get('aria-hidden'), 'true');
assert([...listeners.values()].every(listener => listener.options.passive), 'Scroll/resize listeners never prevent native input');
controller.setActive(true);
assert(root.attributes.has('data-catalog-scroll'));
assert(!cue.hidden);
assert.equal(cue.children[0].textContent, 'Scroll to explore ↓');
for (let i = 0; i < 8; i++) listeners.get('scroll').callback();
assert.equal(frames.size, 1, 'One refresh per frame, rather than per wheel event');
bottom = 900; flush(); assert(cue.hidden, 'Bottom reached');
bottom = 1500; listeners.get('scroll').callback(); flush(); assert(!cue.hidden, 'Scrolling up restores orientation');
root.scrollHeight = 900; observers[0].callback(); flush(); assert(cue.hidden, 'Short/non-overflowing results need no hint');
root.scrollHeight = bottom = 1600; observers[0].callback(); flush(); assert(!cue.hidden, 'New taller results update automatically');
dialog.open = true; observers[1].callback(); flush();
assert(cue.hidden, 'The hint cannot appear behind a detail');
assert(root.attributes.has('data-catalog-scroll'), 'Modal keeps the same viewport width');
dialog.open = false; observers[1].callback(); flush(); assert(!cue.hidden);
text = '向下浏览'; observers[1].callback(); flush(); assert.equal(cue.children[0].textContent, '向下浏览 ↓');
for (let i = 0; i < 5; i++) { controller.setActive(false); assert(cue.hidden); controller.setActive(true); assert(!cue.hidden); }
controller.setActive(false); assert(!root.attributes.has('data-catalog-scroll'));
listeners.get('resize').callback(); controller.dispose();
assert.equal(frames.size, 0); assert.equal(listeners.size, 0); assert(observers.every(observer => observer.disconnected)); assert(cue.removed);

const css = await readFile(new URL('./style.css', import.meta.url), 'utf8');
assert.match(css, /html\[data-catalog-scroll\]\{scrollbar-gutter:auto;scrollbar-width:none\}/);
assert.match(css, /html\[data-catalog-scroll\]::-webkit-scrollbar\{display:none\}/);
assert.match(css, /\.catalog-scroll-cue\{[\s\S]*?pointer-events:none/);
assert(!/\.catalog-scroll-cue[^}]*\b(?:animation|transition):/.test(css), 'The cue has no movement, including reduced-motion mode');
console.log('Catalog scroll: native passive input, scoped scrollbar, bottom/short/resize/filter/localization/modal state, refresh coalescing and disposal pass.');

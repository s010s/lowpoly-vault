import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {thumbnailPlaceholderMarkup} from '../thumbnail-placeholder.js';
const markup=thumbnailPlaceholderMarkup(),css=await readFile(new URL('../thumbnail-placeholder.css',import.meta.url),'utf8');
assert.equal((markup.match(/class="thumbnail-placeholder-face /g)||[]).length,6);assert(markup.includes('aria-hidden="true"'));assert(!/img|canvas|svg|src=/.test(markup));
assert(css.includes('img[data-thumbnail-state]:not([data-thumbnail-state=ready]){visibility:hidden}'),'Pending image boxes stay hidden until decoded without changing layout or native fallback');
assert(css.includes('width:18px;height:18px'));assert(css.includes('background:transparent'));assert(css.includes('16s linear'));assert(css.includes('prefers-reduced-motion'));assert(css.includes('animation-play-state:paused'));assert(css.includes('[data-thumbnail-state=decoding]'));assert(css.includes('[data-thumbnail-visible=false]'));assert(!/url\(/.test(css));
console.log('Thumbnail placeholder: original empty wireframe, bounded geometry, no asset requests, decode/visibility/reduced-motion gates passed.');

import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {thumbnailPlaceholderMarkup,synchronizeThumbnailPlaceholders} from '../thumbnail-placeholder.js';
const markup=thumbnailPlaceholderMarkup(),css=await readFile(new URL('../thumbnail-placeholder.css',import.meta.url),'utf8');
assert.equal((markup.match(/class="thumbnail-placeholder-face /g)||[]).length,6);assert(markup.includes('aria-hidden="true"'));assert(!/img|canvas|svg|src=/.test(markup));
assert(css.includes('img[data-thumbnail-state]:not([data-thumbnail-state=ready]){visibility:hidden}'),'Pending image boxes stay hidden until decoded without changing layout or native fallback');
assert(css.includes('width:18px;height:18px'));assert(css.includes('background:transparent'));assert(css.includes('16s linear'));assert(css.includes('prefers-reduced-motion'));assert(css.includes('animation-play-state:paused'));assert(css.includes('[data-thumbnail-state=decoding]'));assert(css.includes('[data-thumbnail-visible=false]'));assert(!/url\(/.test(css));
console.log('Thumbnail placeholder: original empty wireframe, bounded geometry, no asset requests, decode/visibility/reduced-motion gates passed.');

const animation=(startTime,playState='running')=>({animationName:'thumbnail-wireframe-turn',startTime,playState});
const first=animation(100),later=animation(5400),paused=animation(200,'paused'),other={animationName:'unrelated',startTime:10,playState:'running'};
const cube=(...animations)=>({getAnimations:()=>animations});
synchronizeThumbnailPlaceholders([cube(first),cube(later),cube(paused),cube(other)]);
assert.equal(first.startTime,0);assert.equal(later.startTime,0,'New rows join the original epoch rather than restart');assert.equal(paused.startTime,200,'Offscreen/paused animations are not restarted');assert.equal(other.startTime,10);
const reentry=animation(9000);synchronizeThumbnailPlaceholders([cube(first),cube(reentry),cube()]);assert.equal(reentry.startTime,0,'Reentered rows share the same phase');
synchronizeThumbnailPlaceholders([cube()]);const restored=animation(12000);synchronizeThumbnailPlaceholders([cube(restored)]);assert.equal(restored.startTime,0,'Leaving reduced motion rejoins the shared epoch');
console.log('Thumbnail phase: one document epoch for new/reentered/restored cubes, no JS frame loop, inactive animations untouched.');

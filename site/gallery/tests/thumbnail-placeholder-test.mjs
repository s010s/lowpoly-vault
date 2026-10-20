import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {thumbnailPlaceholderMarkup,synchronizeThumbnailPlaceholders} from '../thumbnail-placeholder.js';
const markup=thumbnailPlaceholderMarkup(),css=await readFile(new URL('../thumbnail-placeholder.css',import.meta.url),'utf8');
const sharedCSS=await readFile(new URL('../style.css',import.meta.url),'utf8');
assert.equal((markup.match(/class="thumbnail-placeholder-face /g)||[]).length,6);assert(markup.includes('aria-hidden="true"'));assert(!/img|canvas|svg|src=/.test(markup));
assert(sharedCSS.includes('img[data-thumbnail-state]:not([data-thumbnail-state=ready]){visibility:hidden}'),'Pending image boxes stay hidden until decoded without changing layout or native fallback');
assert(sharedCSS.includes('img[data-thumbnail-state]{opacity:0;transition:none}'),'Cancellation and errors reset opacity without a reverse fade');
assert(sharedCSS.includes('img[data-thumbnail-state=ready][data-thumbnail-reveal=entering]{transition:opacity 160ms var(--ui-ease-out)}'),'Only decoded images fade in, with the existing ease-out token');
assert.match(sharedCSS,/@media\(prefers-reduced-motion:reduce\)\{[^}]*transition:none!important/,'Reduced motion disables the reveal without overriding its ready opacity');
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

// A loaded poster's later 3D alpha handoff must remain independent of this
// arrival transition, including interrupted/replaced hover presentations.
const {HoverPresentation}=await import('../hover-presentation.js');
const originals=Object.fromEntries(['document','requestAnimationFrame','cancelAnimationFrame'].map(key=>[key,globalThis[key]]));
const poster={style:{},complete:true,naturalWidth:96},host={querySelector:()=>poster,append(){}};
const context={clearRect(){},drawImage(){}};
globalThis.document={createElement:()=>({style:{},width:96,height:64,setAttribute(){},getContext:()=>context,remove(){this.removed=true;}})};
let nextFrame=0;const frames=new Map();globalThis.requestAnimationFrame=fn=>{frames.set(++nextFrame,fn);return nextFrame;};globalThis.cancelAnimationFrame=id=>frames.delete(id);
const advance=time=>{const batch=[...frames.values()];frames.clear();batch.forEach(fn=>fn(time));};
const hover=new HoverPresentation(host);assert.equal(poster.style.transition,'none');hover.hasFrame=true;const shown=hover.reveal();advance(0);advance(160);assert.equal(await shown,true);assert.equal(poster.style.opacity,'0');
hover.dispose();assert.equal(poster.style.opacity,'');assert.equal(poster.style.transition,'','The unchanged renderer releases inline styles; settled UI state suppresses a second fade');assert(hover.canvas.removed);
const previous=new HoverPresentation(host);previous.hasFrame=true;const stale=previous.reveal();advance(200);const replacement=new HoverPresentation(host);assert.equal(await stale,false);previous.dispose();assert.equal(host.__hoverPresentation,replacement,'Old disposal cannot reset a newer hover');replacement.dispose();assert.equal(frames.size,0);
for(const [key,value] of Object.entries(originals)){if(value===undefined)delete globalThis[key];else globalThis[key]=value;}
console.log('Thumbnail/hover boundary: loaded poster enters/exits/replaces the existing alpha presentation with no second opacity transition or stale owner.');

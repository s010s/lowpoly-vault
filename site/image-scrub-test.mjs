import assert from 'node:assert/strict';
import { FrameLRU, ImageScrubPreview, PREVIEW_LIMITS, validateTurntable } from './image-scrub.js';
const pause=()=>new Promise(resolve=>setTimeout(resolve,0));
const deferred=()=>{let resolve,reject;const promise=new Promise((a,b)=>{resolve=a;reject=b;});return {promise,resolve,reject};};
let checks=0;const check=()=>checks++;
const sha='a'.repeat(64);
function fixture(id='arch',count=24){const descriptor={manifest:`assets/turntables/${id}/turntable.json`,source_glb_sha256:sha,frame_count:count,width:768,height:768,poster_index:0};return {asset:{id,turntable:descriptor},manifest:{version:1,source_glb_sha256:sha,frame_count:count,width:768,height:768,poster_index:0,frames:Array.from({length:count},(_,i)=>({path:`assets/turntables/${id}/${i}.webp`,bytes:1,sha256:sha}))}};}
const normal=fixture();validateTurntable(normal.manifest,normal.asset.turntable);check();
for(const mutate of [m=>m.version=2,m=>m.source_glb_sha256='b'.repeat(64),m=>m.frame_count=23,m=>m.width=1025,m=>m.height=0,m=>m.poster_index=24,m=>m.frames.pop(),m=>m.frames[1].path=m.frames[0].path,m=>m.frames[0].path='https://bad.example/x.webp',m=>m.frames[0].path='assets/turntables/arch/../x.webp',m=>m.frames[0].bytes=0,m=>m.frames[0].sha256='x']){const value=structuredClone(normal.manifest);mutate(value);assert.throws(()=>validateTurntable(value,normal.asset.turntable));check();}
validateTurntable(fixture('arch',36).manifest,fixture('arch',36).asset.turntable);check();
const removed=[];const lru=new FrameLRU({maxEntries:2,maxBytes:5,onDelete:value=>removed.push(value)});lru.set('a','A',2);lru.set('b','B',2);assert.equal(lru.get('a'),'A');lru.set('c','C',2);assert.deepEqual([...lru.entries.keys()],['a','c']);assert.deepEqual(removed,['B']);lru.set('d','D',4);assert.deepEqual([...lru.entries.keys()],['d']);assert.equal(lru.bytes,4);assert.equal(lru.set('large','L',6),false);lru.clear();assert.equal(lru.bytes,0);assert.equal(removed.at(-1),'D');check();
const documentListeners=new Map();
globalThis.document={hidden:false,addEventListener:(type,fn)=>documentListeners.set(type,fn),removeEventListener:type=>documentListeners.delete(type),createElement:()=>({width:0,height:0,dataset:{},setAttribute(){},getContext:()=>({clearRect(){},drawImage(bitmap){assert(!bitmap.closed);}}),remove(){this.removed=true;}})};
globalThis.IntersectionObserver=class {constructor(fn){this.fn=fn;}observe(){}disconnect(){}};
function card(){const status={textContent:''},container={append(){}};return {dataset:{},querySelector:selector=>selector==='.card-status'?status:container};}
function harness({fetchHook,decodeHook}={}){const routes=new Map(),requests=[],bitmaps=[];let live=0,peak=0;const make=id=>{const f=fixture(id);routes.set(f.asset.turntable.manifest,new Blob([JSON.stringify(f.manifest)]));for(const frame of f.manifest.frames)routes.set(frame.path,new Blob(['a']));return f;};const a=make('arch'),b=make('tree'),c=make('fern');
 const controller=new ImageScrubPreview({resolvePath:x=>x,fetchImpl:async(path,{signal})=>{requests.push(path);live++;peak=Math.max(peak,live);try{await fetchHook?.(path,signal);if(signal.aborted)throw new DOMException('Aborted','AbortError');return {ok:routes.has(path),blob:async()=>routes.get(path)};}finally{live--;}},decode:async(blob)=>{if(decodeHook)await decodeHook(blob);const bitmap={width:768,height:768,closed:false,close(){assert(!this.closed);this.closed=true;}};bitmaps.push(bitmap);return bitmap;}});
 return {controller,a,b,c,requests,bitmaps,routes,get peak(){return peak;}};
}
async function idle(c){for(let n=0;n<1000&&c.running;n++)await pause();assert.equal(c.running,null,'Preview pump should settle');}
{
 const h=harness(),c=h.controller,one=card();c.activate(one,h.a.asset);await idle(c);assert.equal(one.dataset.scrubFrame,'0');assert.equal(h.requests.filter(p=>p.endsWith('.webp')).length,3,'Only current + 2 neighbors load');assert.equal(c.stats.decodedBytes,3*768*768*4);assert.equal(c.stats.canvasBytes,768*768*4);assert.equal(c.stats.peakRequests,1);check();
 for(let frame=1;frame<=24;frame++){c.request(frame);await idle(c);assert(c.stats.encodedEntries<=12);assert(c.stats.decodedEntries<=3);assert(c.stats.peakDecodedBytes<=3*768*768*4);}assert.equal(one.dataset.scrubFrame,'0');assert.equal(h.peak,1);check();
 const before=h.requests.length;c.stop();assert.equal(c.stats.decodedEntries,0);assert.equal(c.stats.canvasBytes,0);assert(h.bitmaps.every(b=>b.closed));assert.equal(one.dataset.scrubState,undefined);c.activate(one,h.a.asset);await idle(c);assert(h.requests.length-before<=3);c.dispose();assert.equal(c.stats.encodedBytes,0);assert.equal(c.stats.activeId,null);check();
}
{
 const h=harness(),c=h.controller,one=card();c.activate(one,h.a.asset);await idle(c);
 const painted=c.canvas,view={azimuth_deg:147,elevation_deg:28};c.current.snapshotView=view;
 const captured=c.capture({transfer:true});assert.equal(captured.canvas,painted,'Detail reuses the exact card surface without another raster/copy');assert.equal(captured.view,view);assert.equal(captured.canvas.__presentation,view);assert.equal(c.stats.canvasBytes,0);
 c.stop();assert(!captured.canvas.removed,'Preview cleanup cannot remove the transferred flight');assert(h.bitmaps.every(b=>b.closed));
 painted.width=painted.height=1024;c.retainSnapshot(one,h.a.asset,painted,view,{transfer:true});assert.equal(c.canvas,painted,'Returning the flight to its card also avoids a new canvas copy');assert.equal(c.stats.canvasBytes,1024*1024*4);
 c.request(1);await idle(c);assert.equal(c.canvas.width,768);assert.equal(c.canvas.height,768);assert(c.stats.decodedBytes+c.stats.canvasBytes<=9*1024*1024,'New scrub frames restore the original decoded memory budget');c.dispose();check();
}
{
 const hold=deferred();let aborted=false;const h=harness({fetchHook:async(path,signal)=>{if(path.includes('/arch/'))await new Promise((resolve,reject)=>{signal.addEventListener('abort',()=>{aborted=true;reject(new DOMException('Aborted','AbortError'));});hold.promise.then(resolve);});}}),c=h.controller,one=card(),two=card();c.activate(one,h.a.asset);await pause();c.activate(two,h.b.asset);hold.resolve();await idle(c);assert(aborted);assert.equal(one.dataset.scrubState,undefined);assert.equal(two.dataset.scrubState,'ready');assert.equal(c.stats.activeId,'tree');assert.equal(c.stats.peakRequests,1);assert(h.requests.filter(p=>p.endsWith('.webp')).every(p=>p.includes('/tree/')));c.dispose();check();
}
{
 const hold=deferred();let entered=false;const h=harness({decodeHook:async()=>{if(!entered){entered=true;await hold.promise;}}}),c=h.controller,one=card(),two=card();c.activate(one,h.a.asset);while(!entered)await pause();c.activate(two,h.b.asset);hold.resolve();await idle(c);assert(h.bitmaps[0].closed,'Superseded decode releases its bitmap');assert.equal(one.dataset.scrubState,undefined);assert.equal(two.dataset.scrubState,'ready');assert.equal(c.stats.errors,0);c.dispose();check();
}
{
 const hold=deferred();let entered=false;const h=harness({fetchHook:async path=>{if(path.endsWith('/0.webp')&&!entered){entered=true;await hold.promise;}}}),c=h.controller,one=card();c.activate(one,h.a.asset);while(!entered)await pause();for(let frame=1;frame<24;frame++)c.request(frame);hold.resolve();await idle(c);assert.equal(one.dataset.scrubFrame,'23','Latest pointer position wins');assert(h.requests.filter(p=>p.endsWith('.webp')).length<=4,'Intermediate positions are coalesced');c.dispose();check();
}
{
 const h=harness(),c=h.controller,one=card();h.routes.delete(h.a.manifest.frames[0].path);c.activate(one,h.a.asset);await idle(c);assert.equal(one.dataset.scrubState,'fallback');assert.equal(c.stats.canvasBytes,0);assert.equal(c.stats.decodedEntries,0);const before=h.requests.length;c.request(5);await idle(c);assert.equal(h.requests.length,before,'Failed card does not retry continuously');c.stop();c.activate(one,h.b.asset);await idle(c);assert.equal(one.dataset.scrubState,'ready');c.dispose();check();
}
{
 const h=harness(),c=h.controller,one=card();c.activate(one,h.a.asset);await idle(c);c.intersection.fn([{target:one,isIntersecting:false}]);assert.equal(c.stats.activeId,null);assert.equal(c.stats.decodedBytes,0);c.activate(one,h.a.asset);await idle(c);document.hidden=true;documentListeners.get('visibilitychange')();assert.equal(c.stats.canvasBytes,0);document.hidden=false;c.dispose();check();
}
console.log(JSON.stringify({status:'pass',checks,limits:PREVIEW_LIMITS,covers:['24–36 frames','unsafe metadata','encoded LRU','one active request','abort stale fetch','close stale decode','latest pointer wins','image failure restores static','visibility/offscreen cleanup']}));

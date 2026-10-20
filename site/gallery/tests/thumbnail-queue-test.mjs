import assert from 'node:assert/strict';
import {ThumbnailQueue} from '../thumbnail-queue.js';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
// Browser timer functions reject a foreign receiver. Node's permissive timers
// and injected arrow fakes must not conceal an illegal Window API invocation.
const timerReceivers=[];
const browserQueue=vm.runInNewContext(readFileSync(new URL('../thumbnail-queue.js',import.meta.url),'utf8').replace('export class','class')+';new ThumbnailQueue()', {
 setTimeout:function(){assert.equal(this,undefined,'Native timer must not receive the queue as its receiver');timerReceivers.push('set');return 1;},
 clearTimeout:function(){assert.equal(this,undefined,'Native timer must not receive the queue as its receiver');timerReceivers.push('clear');}
});
browserQueue.update([{image:{dataset:{}},url:'/one.png'}]);browserQueue.clear();
assert.deepEqual(timerReceivers,['clear','set','clear']);
let next=0;const timers=new Map(),calls=[];
const queue=new ThumbnailQueue({setTimer:callback=>{timers.set(++next,callback);return next;},clearTimer:id=>timers.delete(id)});
const tick=()=>{const callbacks=[...timers.values()];timers.clear();callbacks.forEach(callback=>callback());};
function item(id,visible=true){const image={dataset:{},onload:null,onerror:null,removeAttribute(){calls.push(['cancel',id]);},set src(value){calls.push(['load',id,value]);}};return{image,url:`/${id}.png`,fallback:`/${id}-fallback.png`,visible};}
const first=Array.from({length:12},(_,i)=>item(i,i<3));queue.update(first);assert.equal(calls.length,0);assert.equal(queue.stats.budget,3);tick();assert.equal(queue.active.size,3);
assert.equal(queue.stats.started,3,'Overscan images do not consume visible loading slots');
queue.update(first);assert.equal(timers.size,0,'Unchanged virtual frame does not defer work forever');
first[0].image.onload();await Promise.resolve();assert.equal(queue.stats.started,3);assert.equal(queue.active.size,2);
const later=Array.from({length:8},(_,i)=>item(i+20,i<5));queue.update(later);assert.equal(queue.stats.budget,5,'A taller visible area increases the budget');assert.equal(queue.active.size,0);assert.equal(queue.stats.cancelled,2);
queue.update([item('skipped')]);queue.update(later);tick();assert.equal(queue.stats.started,8);assert.equal(queue.active.size,5,'Every visible pending image may load concurrently');assert(!calls.some(call=>call[1]==='skipped'),'Fast-passed rows never start a request');
later[0].image.onerror();assert.deepEqual(calls.at(-1),['load',20,'/20-fallback.png']);later[0].image.onload();await Promise.resolve();assert.equal(queue.active.size,4);
queue.update(later.slice(0,2));assert.equal(queue.stats.budget,2,'Shrinking the viewport reduces the budget');assert.equal(queue.active.size,1,'Offscreen in-flight jobs are cancelled immediately');tick();assert.equal(queue.active.size,1);
queue.clear();assert.equal(queue.active.size,0);assert.equal(timers.size,0);assert.equal(queue.stats.budget,0);
const decode=item('decode');let decodeReady;decode.image.decode=()=>new Promise(done=>decodeReady=done);queue.update([decode]);tick();decode.image.onload();assert.equal(decode.image.dataset.thumbnailState,'decoding');assert.equal(decode.image.dataset.thumbnailVisible,'true');decodeReady();await Promise.resolve();assert.equal(decode.image.dataset.thumbnailState,'ready');
const cancelled=item('cancel-decode');let cancelReady;cancelled.image.decode=()=>new Promise(done=>cancelReady=done);queue.update([cancelled]);tick();cancelled.image.onload();queue.clear();cancelReady();await Promise.resolve();assert.equal(cancelled.image.dataset.thumbnailState,'idle');assert.equal(cancelled.image.dataset.thumbnailVisible,'false');
queue.update([cancelled]);assert.equal(cancelled.image.dataset.thumbnailState,'pending','Reentered cancelled row shows pending feedback immediately');queue.clear();
console.log('Thumbnail queue: viewport-derived budget, all visible requests, no overscan, resize cancellation, settle-only starts, decode and fallback passed.');

const cached=item('cached');let cachedDecodes=0,cacheReady;cached.image.complete=true;cached.image.naturalWidth=32;cached.image.decode=()=>{cachedDecodes++;return new Promise(done=>cacheReady=done);};
queue.update([cached]);tick();assert.equal(cached.image.dataset.thumbnailState,'decoding','A cached image does not wait indefinitely for load');cached.image.onload();assert.equal(cachedDecodes,1,'The cached fast path and delayed load event share one decode');cacheReady();await Promise.resolve();assert.equal(cached.image.dataset.thumbnailState,'ready');
const cachedStarts=queue.stats.started;queue.clear();queue.update([cached]);tick();assert.equal(cached.image.dataset.thumbnailState,'ready');assert.equal(queue.stats.started,cachedStarts,'Returning to an already decoded row does not hide or refetch it');queue.clear();
for(const mode of ['reject','throw']){
 const bad=item('decode-'+mode);bad.image.decode=()=>{if(mode==='throw')throw Error('bad image');return Promise.reject(Error('bad image'));};queue.update([bad]);tick();bad.image.onload();await Promise.resolve();assert.equal(bad.image.dataset.thumbnailState,'error');assert.equal(queue.active.size,0);queue.clear();
}
const failed=item('network-failure');queue.update([failed]);tick();failed.image.onerror();failed.image.onerror();assert.equal(failed.image.dataset.thumbnailState,'error');assert.equal(queue.active.size,0);queue.clear();
const reused=item('reused');const completions=[];reused.image.decode=()=>new Promise(done=>completions.push(done));queue.update([reused]);tick();reused.image.onload();queue.update([]);queue.update([reused]);tick();reused.image.onload();completions[0]();await Promise.resolve();assert.equal(reused.image.dataset.thumbnailState,'decoding','A cancelled decode cannot reveal a rapidly reentered image');completions[1]();await Promise.resolve();assert.equal(reused.image.dataset.thumbnailState,'ready');queue.clear();
console.log('Thumbnail readiness: cached fast path, duplicate load, decode rejection/throw, network fallback failure, rapid reuse and decoded navigation return passed.');

// UI-only reveal ownership: active hover cancels the opacity transition; missing
// events and cached/reduced-motion no-transition cases must all settle opaque.
const globalNames=['setTimeout','clearTimeout','requestAnimationFrame','cancelAnimationFrame'],savedGlobals=Object.fromEntries(globalNames.map(key=>[key,globalThis[key]]));
const revealTimers=new Map(),revealFrames=new Map();let revealID=0;
globalThis.setTimeout=(fn,delay)=>{assert.equal(delay,250,'Reveal fallback remains bounded at 250 ms');revealTimers.set(++revealID,fn);return revealID;};globalThis.clearTimeout=id=>revealTimers.delete(id);
globalThis.requestAnimationFrame=fn=>{revealFrames.set(++revealID,fn);return revealID;};globalThis.cancelAnimationFrame=id=>revealFrames.delete(id);
try{
 for(const mode of ['transitionend','transitioncancel','missing-event','no-transition','missing-api-timeout','missing-api-event']){
  const sample=item('reveal-'+mode),listeners=new Map();sample.image.addEventListener=(type,fn)=>listeners.set(type,fn);sample.image.removeEventListener=(type,fn)=>{if(listeners.get(type)===fn)listeners.delete(type);};if(!mode.startsWith('missing-api'))sample.image.getAnimations=()=>mode==='no-transition'?[]:[{transitionProperty:'opacity'}];
  queue.update([sample]);tick();sample.image.onload();await Promise.resolve();assert.equal(sample.image.dataset.thumbnailState,'ready');assert.equal(sample.image.dataset.thumbnailReveal,'entering');
  for(const [id,fn]of [...revealFrames]){revealFrames.delete(id);fn();}
  if(mode.startsWith('missing-api'))assert.equal(sample.image.dataset.thumbnailReveal,'entering','Missing animation inspection must preserve the real transition until its event or bounded fallback');
  if(mode==='missing-event'||mode==='missing-api-timeout'){for(const [id,fn]of [...revealTimers]){revealTimers.delete(id);fn();}}
  else if(mode!=='no-transition'){const ended=listeners.get(mode==='missing-api-event'?'transitionend':mode);ended({target:sample.image,propertyName:'transform'});assert.equal(sample.image.dataset.thumbnailReveal,'entering');ended({target:sample.image,propertyName:'opacity'});}
  assert.equal(sample.image.dataset.thumbnailState,'ready','Reveal cleanup never makes a decoded image pending/transparent again');assert.equal(sample.image.dataset.thumbnailReveal,'settled');assert.equal(listeners.size,0);assert.equal(revealTimers.size,0);assert.equal(revealFrames.size,0);queue.clear();
 }
}finally{for(const key of globalNames){if(savedGlobals[key]===undefined)delete globalThis[key];else globalThis[key]=savedGlobals[key];}}
console.log('Thumbnail reveal cleanup: opacity end/cancel, hover interruption, bounded missing-event/missing-API fallback, API-less transition events and cached/reduced no-transition paths settle without renderer changes.');

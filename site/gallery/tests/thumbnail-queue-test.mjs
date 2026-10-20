import assert from 'node:assert/strict';
import {ThumbnailQueue} from '../thumbnail-queue.js';
let next=0;const timers=new Map(),calls=[];
const queue=new ThumbnailQueue({concurrency:3,setTimer:callback=>{timers.set(++next,callback);return next;},clearTimer:id=>timers.delete(id)});
const tick=()=>{const callbacks=[...timers.values()];timers.clear();callbacks.forEach(callback=>callback());};
function item(id){const image={dataset:{},onload:null,onerror:null,removeAttribute(){calls.push(['cancel',id]);},set src(value){calls.push(['load',id,value]);}};return{image,url:`/${id}.png`,fallback:`/${id}-fallback.png`};}
const first=Array.from({length:12},(_,i)=>item(i));queue.update(first);assert.equal(calls.length,0);tick();assert.equal(queue.active.size,3);assert.equal(queue.stats.maxActive,3);
queue.update(first);assert.equal(timers.size,0,'Unchanged virtual frame does not defer work forever');
first[0].image.onload();assert.equal(queue.stats.started,4);assert.equal(queue.active.size,3);
const later=Array.from({length:8},(_,i)=>item(i+20));queue.update(later);assert.equal(queue.active.size,0);assert.equal(queue.stats.cancelled,3);assert.equal(queue.stats.started,4,'New rows await settling, even when cancelled jobs finish');
queue.update([item('skipped')]);queue.update(later);tick();assert.equal(queue.stats.started,7);assert(!calls.some(call=>call[1]==='skipped'),'Fast-passed rows never start a request');
later[0].image.onerror();assert.deepEqual(calls.at(-1),['load',20,'/20-fallback.png']);later[0].image.onload();assert.equal(queue.active.size,3);
queue.clear();assert.equal(queue.active.size,0);assert.equal(timers.size,0);assert.equal(queue.stats.maxActive,3);
console.log('Thumbnail queue: settle-only starts, bounded concurrency, cancellation, dropped transient rows and fallback passed.');

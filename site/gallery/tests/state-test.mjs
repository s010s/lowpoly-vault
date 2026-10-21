import assert from 'node:assert/strict';
import { filterItems, WheelSettler } from '../state.js';

const items = [
  { id: 'a', name: {en:'Amber Tree',zh:'琥珀树'}, theme:['prehistoric'], type:'flora', specification:['small'] },
  { id: 'b', name: {en:'Stone',zh:'石头'}, theme:['prehistoric'], type:'geology', specification:['large'] },
  { id: 'c', name: {en:'Fern',zh:'蕨'}, theme:['forest'], type:'flora', specification:['small'] },
];
assert.deepEqual(filterItems(items, '', {type:['flora','geology'],theme:['prehistoric']}).map(x=>x.id), ['a','b']);
assert.deepEqual(filterItems(items, '琥珀', {specification:['small']}).map(x=>x.id), ['a']);
assert.equal(filterItems(items, '', {theme:['prehistoric'],type:['flora'],specification:['large']}).length, 0);
assert.equal(filterItems(items, '  AMBER ').length, 1);
assert.equal(filterItems(items, '', {type:[]}).length, 3);

let time = 0, position = 78, next = 0, writes = [], centered, reduced = false;
const callbacks = new Map();
const wheel = new WheelSettler({read:()=>position, write:value=>{writes.push(value);position=value;},
  targets:()=>[{id:'a',offset:0},{id:'b',offset:100},{id:'c',offset:200}],center:id=>{centered=id;},
  now:()=>time, reduced:()=>reduced, frame:fn=>{callbacks.set(++next,fn);return next;},cancel:id=>callbacks.delete(id)});
const advance = milliseconds => {time+=milliseconds;const pending=[...callbacks.values()];callbacks.clear();pending.forEach(fn=>fn());};
wheel.input(); wheel.scrolled();
advance(100);
assert.equal(writes.length,0,'input is native, without a compensating scroll write');
position=83;wheel.scrolled();advance(100);
assert.equal(writes.length,0,'inertial movement extends settling');
advance(51);advance(80);
assert.ok(position>83 && position<100,'settling eases towards nearest center');
assert.equal(centered,'b');
const count=writes.length;
wheel.input();position=150;wheel.scrolled();advance(100);
assert.equal(writes.length,count,'new input immediately interrupts a running snap');
position=170;wheel.scrolled();advance(151);advance(281);
assert.equal(position,200);
assert.equal(centered,'c');
assert.equal(wheel.state,'idle');
position=65;reduced=true;wheel.input();wheel.scrolled();advance(151);
assert.equal(position,65,'reduced motion preserves the natural stopping position');
reduced=false;position=150;wheel.scrolled();
assert.equal(centered,'b','ties retain the prior browse center');
wheel.pointerDown();advance(500);
assert.equal(position,150,'held pointer prevents automatic snapping');
position=146;wheel.scrolled();wheel.pointerUp();advance(151);advance(221);
assert.equal(position,100);
position=67;wheel.input();advance(151);assert.equal(position,67,'a click without scrolling cannot trigger centering');
wheel.input();wheel.dispose();advance(500);
assert.equal(callbacks.size,0);
console.log('PASS: bilingual search, facet OR/AND, empty selections, native inertia, interruptible settling, reduced motion and disposal. Center callback has no selection operation.');

// Keep hover recovery in the existing gallery state gate without changing the
// package file sealed into the historical poster-renderer recipe.
await import('./hover-intent-test.mjs');

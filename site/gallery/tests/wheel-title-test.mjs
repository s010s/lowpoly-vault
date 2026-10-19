import assert from 'node:assert/strict';
import {WheelTitle} from '../wheel-title.js';

function fixture() {
  let time = 0, position = 0, serial = 0, renders = 0;
  let targets = Array.from({length:8}, (_, i) => ({id:String(i), offset:i*128}));
  const timers = new Map(), changes = [];
  let visible;
  const title = new WheelTitle({read:()=>position,targets:()=>targets,now:()=>time,
    schedule:(fn,delay)=>{timers.set(++serial,{fn,at:time+delay});return serial;},
    cancel:id=>timers.delete(id),change:()=>{renders++;render();}});
  function render() { visible = title.update(); if (changes.at(-1) !== visible) changes.push(visible); return visible; }
  function advance(ms) {
    const end = time + ms;
    while (true) {
      const next = [...timers].filter(([,timer])=>timer.at<=end).sort((a,b)=>a[1].at-b[1].at)[0];
      if (!next) break;
      time = next[1].at; timers.delete(next[0]); next[1].fn();
    }
    time = end;
  }
  render();
  return {title,timers,changes,render,advance,move(value,ms=16){advance(ms);position=value;return render();},
    replace(value){targets=value;return render();},get visible(){return visible;},get renders(){return renders;}};
}

const checks = [];
{
  const f=fixture();
  for(let i=0;i<100;i++)assert.equal(f.move(i%2 ? .5 : 2), '0');
  assert.deepEqual(f.changes,['0']);assert.equal(f.timers.size,0);
  checks.push('Repeated tiny movement preserves the visible title and schedules no title work');
}
{
  const f=fixture();
  for(const p of [63,65,61,67,64,75,64])assert.equal(f.move(p,75),'0');
  f.advance(500);assert.equal(f.visible,'0');assert.deepEqual(f.changes,['0']);
  f.move(77);f.advance(199);assert.equal(f.visible,'0');f.advance(1);assert.equal(f.visible,'1');
  assert.deepEqual(f.changes,['0','1']);assert.equal(f.timers.size,0);
  checks.push('12 px boundary hysteresis prevents midpoint jitter; new centre takes over at 200 ms');
}
{
  const f=fixture();f.move(80);f.advance(100);f.move(45);f.advance(250);
  assert.deepEqual(f.changes,['0']);assert.equal(f.timers.size,0);
  f.move(90);f.advance(200);assert.equal(f.visible,'1');
  for(const p of [63,57,66,52])assert.equal(f.move(p,80),'1');
  f.move(51);f.advance(199);assert.equal(f.visible,'1');f.advance(1);assert.equal(f.visible,'0');
  checks.push('Reversal cancels an uncommitted candidate and has the same dead band in both directions');
}
{
  const f=fixture();
  for(const p of [100,210,340,470,590,720]){f.move(p,40);assert.equal(f.visible,'0');}
  f.advance(199);assert.equal(f.visible,'0');f.advance(1);assert.equal(f.visible,'6');
  assert.deepEqual(f.changes,['0','6']);
  checks.push('Fast scrolling skips transient item names and commits only the final stable candidate');
}
{
  const f=fixture();f.move(80);f.advance(170);f.move(170,10);f.advance(20);
  assert.equal(f.visible,'0','Fast movement inside one candidate must not commit at the first deadline');
  f.advance(59);assert.equal(f.visible,'0');f.advance(1);assert.equal(f.visible,'1');
  assert.equal(f.timers.size,0);checks.push('A recently fast candidate waits for 80 ms of quiet before handoff');
}
{
  const f=fixture();f.move(90);f.advance(60);f.title.reset();
  f.replace([{id:'new',offset:0}]);f.advance(500);assert.equal(f.visible,'new');assert.equal(f.timers.size,0);
  f.replace([]);assert.equal(f.visible,null);f.advance(500);assert.equal(f.timers.size,0);
  f.replace([{id:'restored',offset:0}]);assert.equal(f.visible,'restored');
  checks.push('Filter/reorder reset, removed owner, empty results and restoration cannot leave stale pending work');
}
{
  const f=fixture();f.move(90);assert.equal(f.timers.size,1);f.title.dispose();f.advance(1000);
  assert.equal(f.renders,0);assert.equal(f.timers.size,0);assert.equal(f.render(),null);
  checks.push('Disposal cancels pending callbacks and refuses further title updates');
}
console.log(JSON.stringify({status:'passed',checks},null,2));

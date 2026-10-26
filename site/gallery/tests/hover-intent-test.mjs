import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import {HoverIntent,hoverRowAt} from '../hover-intent.js';
import {WheelSettler} from '../state.js';
import {validDetailPresentation,detailScreenFrame} from '../detail-presentation-policy.js';
const source=readFileSync(new URL('../main.js',import.meta.url),'utf8');
const flush=async()=>{for(let i=0;i<8;i++)await Promise.resolve();};
const deferred=()=>{let resolve,reject;const promise=new Promise((a,b)=>{resolve=a;reject=b;});return {promise,resolve,reject};};
function fixture(){
 let now=0,next=0,enabled=true,ready=true,target;
 const timers=new Map(),frames=new Map(),sessions=[],slots={};
 const a={id:'selected',isConnected:true,parentElement:slots},b={id:'unselected',isConnected:true,parentElement:slots};target=a;
 const wheel=new EventTarget();Object.assign(wheel,{clientHeight:300,scrollTop:0,getBoundingClientRect:()=>({left:0,right:300,top:0,bottom:300})});
 const doc={elementFromPoint:()=>target&&{closest:()=>target}};
 const hover=new HoverIntent({hit:point=>hoverRowAt(doc,wheel,slots,point),enabled:()=>enabled,ready:()=>ready,idle:()=>settler.state==='idle',
  schedule:fn=>{timers.set(++next,{at:now+300,fn});return next;},cancel:id=>timers.delete(id),
  create:row=>{const load=deferred(),reveal=deferred();const session={row,load,revealGate:reveal,stops:0,readies:0,reveals:0,animations:0,
   prepare:()=>load.promise,ready(){this.readies++;},reveal(){this.reveals++;return reveal.promise;},animate(){this.animations++;},stop(){this.stops++;}};sessions.push(session);return session;}});
 const settler=new WheelSettler({read:()=>wheel.scrollTop,write:value=>{wheel.scrollTop=value;},targets:()=>[{id:'a',offset:0},{id:'b',offset:128}],center:()=>{},settled:()=>hover.refresh(),now:()=>now,frame:fn=>{frames.set(++next,fn);return next;},cancel:id=>frames.delete(id)});
 // Execute the actual wheel event bindings, not a duplicate implementation.
 const start=source.indexOf("wheel.addEventListener('scroll'");const end=source.indexOf("wheel.addEventListener('keydown'",start);
 const window=new EventTarget();
 vm.runInNewContext(source.slice(start,end),{wheel,window,hover,settler,stopHover:()=>hover.clear(),collectionScroll:0,restoringHistory:false,programmaticPosition:null,renderWheel:()=>{},saveCurrentHistory:()=>{}});
 const event=(type,properties={})=>Object.assign(new Event(type),properties);
 return {hover,settler,wheel,window,a,b,sessions,timers,frames,
  move:(pointerType='mouse',x=50,y=50)=>hover.pointer({pointerType,clientX:x,clientY:y}),
  leave:()=>hover.pointer({pointerType:'mouse',clientX:400,clientY:50}),
  wheelInput:()=>wheel.dispatchEvent(event('wheel')),
  scroll:value=>{wheel.scrollTop=value;wheel.dispatchEvent(event('scroll'));},
  setTarget:value=>{target=value;},setReady:value=>{ready=value;},setEnabled:value=>{enabled=value;},
  advance:async milliseconds=>{now+=milliseconds;const callbacks=[...frames.values()];frames.clear();callbacks.forEach(fn=>fn());for(const [id,timer] of [...timers])if(timer.at<=now){timers.delete(id);timer.fn();}await flush();},
  complete:async session=>{session.load.resolve(true);await flush();session.revealGate.resolve(true);await flush();}
 };
}
let checks=0;
async function test(name,run){await run();checks++;console.log('PASS:',name);}
await test('stationary mouse resumes on actual wheel/scroll settling and hit-tests the new row',async()=>{
 const f=fixture();f.move();await f.advance(300);await f.complete(f.sessions[0]);
 f.wheelInput();f.scroll(75);f.setTarget(f.b);assert.equal(f.sessions[0].stops,1);
 await f.advance(151);assert.equal(f.settler.state,'snapping');await f.advance(221);assert.equal(f.settler.state,'idle');
 await f.advance(299);assert.equal(f.sessions.length,1);await f.advance(1);assert.equal(f.sessions[1].row,f.b);await f.complete(f.sessions[1]);assert.equal(f.sessions[1].animations,1);
});
await test('wheel at boundary still settles; continuous input cannot restart early',async()=>{
 const f=fixture();f.move();f.wheelInput();await f.advance(100);f.wheelInput();await f.advance(100);assert.equal(f.sessions.length,0);
 await f.advance(51);await f.advance(299);assert.equal(f.sessions.length,0);await f.advance(1);assert.equal(f.sessions.length,1);
});
for(const selected of [true,false])await test(`loading to ready restores ${selected?'selected':'unselected'} row without another pointermove`,async()=>{
 const f=fixture();f.setTarget(selected?f.a:f.b);f.setReady(false);f.move();await f.advance(600);assert.equal(f.sessions.length,0);assert.equal(f.timers.size,0);
 f.setReady(true);f.hover.refresh();await f.advance(300);await f.complete(f.sessions[0]);assert.equal(f.sessions[0].animations,1);
});
await test('leave before selected load completes does not resurrect hover',async()=>{
 const f=fixture();f.setReady(false);f.move();f.leave();f.setReady(true);f.hover.refresh();await f.advance(600);assert.equal(f.sessions.length,0);
});
await test('obsolete prepare and reveal promises cannot reveal, animate or stop newer hover',async()=>{
 const f=fixture();f.move();await f.advance(300);const old=f.sessions[0];
 f.setTarget(f.b);f.move();await f.advance(300);const current=f.sessions[1];await f.complete(old);assert.equal(old.reveals,0);assert.equal(current.stops,0);
 current.load.resolve(true);await flush();assert.equal(current.reveals,1);f.hover.pause();f.setTarget(f.a);f.hover.refresh();await f.advance(300);const last=f.sessions[2];current.revealGate.resolve(true);await flush();assert.equal(current.animations,0);assert.equal(last.stops,0);await f.complete(last);assert.equal(last.animations,1);
});
await test('repeated selection pauses preserve only current intent and await readiness',async()=>{
 const f=fixture();f.move();await f.advance(300);const old=f.sessions[0];f.hover.pause();f.setReady(false);f.hover.refresh();f.hover.pause();await f.advance(1000);assert.equal(f.sessions.length,1);
 f.setReady(true);f.hover.refresh();await f.advance(300);await f.complete(old);assert.equal(old.reveals,0);await f.complete(f.sessions[1]);assert.equal(f.sessions[1].animations,1);
});
for(const reason of ['touch','reduced/fine-pointer','hidden','pagehide/cancel','removed','outside','overlay'])await test(`${reason} prevents pending hover and late results`,async()=>{
 const f=fixture();f.move();await f.advance(300);const old=f.sessions[0];
 if(reason==='touch')f.move('touch');
 else if(reason==='reduced/fine-pointer'||reason==='hidden'){f.setEnabled(false);f.hover.clear();}
 else if(reason==='pagehide/cancel')f.hover.clear();
 else if(reason==='removed'){f.a.isConnected=false;f.hover.refresh();}
 else if(reason==='outside')f.leave();else {f.setTarget(null);f.hover.refresh();}
 await f.complete(old);assert.equal(old.reveals,0);assert.equal(old.animations,0);assert.equal(old.stops,1);
 f.hover.refresh();await f.advance(1000);assert.equal(f.sessions.length,1);
});
for(const failure of ['false','throw','reveal'])await test(`${failure} failure cleans up once without retry loop`,async()=>{
 const f=fixture();f.move();await f.advance(300);const old=f.sessions[0];
 if(failure==='throw')old.load.reject(new Error('failed'));else old.load.resolve(failure!=='false');await flush();
 if(failure==='reveal'){old.revealGate.reject(new Error('cancelled'));await flush();}
 assert.equal(old.stops,1);assert.equal(old.animations,0);f.move();f.hover.refresh();await f.advance(10000);assert.equal(f.sessions.length,1);assert.equal(f.timers.size,0);
 f.leave();f.move();await f.advance(300);assert.equal(f.sessions.length,2);
});
await test('disposal, pointer hold and cancellation do not schedule phantom recovery',async()=>{
 const f=fixture();f.move();f.wheel.dispatchEvent(Object.assign(new Event('pointerdown'),{pointerType:'mouse'}));await f.advance(1000);assert.equal(f.sessions.length,0);
 f.hover.clear();f.window.dispatchEvent(new Event('pointercancel'));await f.advance(200);await f.advance(500);assert.equal(f.sessions.length,0);
 f.settler.dispose();assert.equal(f.frames.size,0);
});
await test('main wiring cancels lifecycle changes and resumes only current selection success',async()=>{
 assert.match(source,/if\(version!==selectionVersion\|\|!ready\)return;currentReady=true;hover.refresh\(\)/);
 for(const binding of ["document.addEventListener('visibilitychange',stopHover)","window.addEventListener('pagehide',stopHover)","window.addEventListener('pointercancel',stopHover)"])assert.ok(source.includes(binding));
 assert.ok(!source.includes('hoverRow===row'));
});
await test('actual main pointer wiring and choose ready callback recover the selected card',async()=>{
 const document=new EventTarget(),window=new EventTarget(),media=new EventTarget();media.matches=true;
 const slots={},row={dataset:{id:'a'},isConnected:true,parentElement:slots,querySelector:()=>({})};
 const wheel={clientHeight:300,getBoundingClientRect:()=>({left:0,right:300,top:0,bottom:300})};
 Object.assign(document,{hidden:false,documentElement:new EventTarget(),elementFromPoint:()=>({closest:()=>row})});
 let timerId=0;const timers=new Map(),loads=[],previews=[];
 const asset={id:'a',name:{en:'A'},category:'geology',triangles:1};
 const frameClears=[];
 const node=()=>({dataset:{},style:{removeProperty(name){frameClears.push(name);delete this[name==='transform-origin'?'transformOrigin':name];}},classList:{add(){},remove(){}},setAttribute(){}}),nodes=new Map();
 const $=id=>{if(!nodes.has(id))nodes.set(id,node());return nodes.get(id);};
 const renderer={wire:false,detail:{metric:{available:true}},stops:0,reveals:0,animations:0,
  select(){assert.deepEqual(frameClears,['transform-origin','transform'],'real poster frame update precedes model selection');const load=deferred();loads.push(load);return load.promise;},
  preview(){const load=deferred();previews.push(load);this.hover={};return load.promise;},
  stopHover(){this.stops++;this.hover=null;},revealHover(){this.reveals++;return Promise.resolve(true);},animateHover(){this.animations++;}};
 const settler={state:'idle',stop(){this.state='idle';},centerOn(){}};
 const context=vm.createContext({HoverIntent:class extends HoverIntent{constructor(args){super({...args,schedule:fn=>{timers.set(++timerId,fn);return timerId;},cancel:id=>timers.delete(id)});}},hoverRowAt,
  HoverTurntable:class{ready(){}stop(){}},renderer,document,window,wheel,slots,settler,matchMedia:()=>media,reduced:()=>false,
  currentReady:true,selectionVersion:0,selectionLoadingTimer:0,state:{selected:'a',results:[asset],lang:'en'},sample:[asset],
  ui:{resetCopy(){}},closeInfo(){},saveCurrentHistory(){},pushHistory(){},selectPoster:asset=>{const image=$('#detail-poster');Object.assign(image.dataset,{modelId:asset.id,source:'canonical',presentationFrame:'native-viewport-v2'});Object.assign(image.style,{transform:'stale',transformOrigin:'0 0'});return {ready:Promise.resolve(true)};},
  validDetailPresentation,detailScreenFrame,
  infoContent(){},renderSummary(){},renderWheel(){},syncMobileView(){},mobile:()=>false,modelHeight:()=>'',short:()=> 'A',
  t:en=>en,categories:{geology:['Geology','地质']},urlAsset:value=>value,$,cancelSelectedPoster:null,
  setTimeout:()=>0,clearTimeout(){}});
 const hoverStart=source.indexOf('const hover=new HoverIntent('),hoverEnd=source.indexOf('function renderWheel(){',hoverStart);
 const chooseStart=source.indexOf('async function choose('),chooseEnd=source.indexOf('function syncMobileView(){',chooseStart);
 const frameStart=source.indexOf('function updateSelectedPosterFrame(){'),frameEnd=source.indexOf('function selectPoster(',frameStart);assert(frameStart>=0&&frameEnd>frameStart);
 vm.runInContext(source.slice(frameStart,frameEnd)+source.slice(hoverStart,hoverEnd)+source.slice(chooseStart,chooseEnd),context);
 const move=(x=50,type='mouse')=>document.dispatchEvent(Object.assign(new Event('pointermove'),{clientX:x,clientY:50,pointerType:type}));
 move();const choice=vm.runInContext("choose('a',{center:true})",context);assert.equal(timers.size,0);
 if(!loads.length)await choice;assert.equal(loads.length,1,'actual choose reaches renderer selection');
 loads[0].resolve(true);await choice;assert.equal($('#detail-poster').style.transform,undefined);assert.equal($('#detail-poster').dataset.presentationFrame,undefined);assert.equal(timers.size,1,'real choose readiness retries retained pointer');
 for(const fn of timers.values())fn();timers.clear();assert.equal(previews.length,1);previews[0].resolve(true);await flush();assert.equal(renderer.animations,1);
 document.hidden=true;document.dispatchEvent(new Event('visibilitychange'));assert.equal(renderer.hover,null);
 document.hidden=false;document.dispatchEvent(new Event('visibilitychange'));assert.equal(timers.size,0);
 move();for(const fn of timers.values())fn();timers.clear();assert.equal(previews.length,2);
 window.dispatchEvent(new Event('pagehide'));previews[1].resolve(true);await flush();assert.equal(renderer.animations,1,'late pagehide promise cannot restart');
 move(50,'touch');assert.equal(timers.size,0);
});
console.log(`PASS: ${checks} bounded hover recovery scenarios (logic/event tests, not WebGL visual validation).`);

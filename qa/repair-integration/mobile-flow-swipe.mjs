import {chromium} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const out=process.env.QA_OUTPUT_DIR, origin=process.env.QA_CANDIDATE;
assert(out&&origin,'Set QA_CANDIDATE and QA_OUTPUT_DIR');
assert(['127.0.0.1','localhost'].includes(new URL(origin).hostname),'Use a loopback QA build');
await mkdir(out,{recursive:true});
const b=await chromium.launch({headless:true,chromiumSandbox:true}),results=[];
const hash=x=>createHash('sha256').update(x).digest('hex');
const sl=(ms)=>new Promise(r=>setTimeout(r,ms));
try{
const p=await b.newPage({viewport:{width:667,height:375},isMobile:true,hasTouch:true,reducedMotion:'reduce'});
const cd=await p.context().newCDPSession(p),id='paratingia';
const go=async y=>{await p.evaluate(y=>window.scrollTo(0,y),y);await sl(180);};
const frame=async label=>{
 const v=await p.evaluate(()=>{const r=window.__preview.renderer,d=document.querySelector('#detail');return {y:scrollY,stage:d.getBoundingClientRect().toJSON(),frames:r.stats.frames,visible:r.visible,q:r.detail.orientation?.quaternion?.toArray()||null,touch:getComputedStyle(d).touchAction,state:d.dataset.state,doc:document.documentElement.scrollHeight,innerH:innerHeight,IW:innerWidth,motion:matchMedia('(prefers-reduced-motion:reduce)').matches,canvas:r.renderer.domElement.toDataURL()};});
 const {canvas,...data}=v;const row={...data,label,canvasSha:hash(canvas)};results.push(row);
 await p.screenshot({path:`${out}/swipe-${label}.png`});return row;
};
const swipe=async(x,y0,y1)=>{
 await cd.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y:y0}]});
 for(let i=1;i<=10;i++){await cd.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x,y:y0+(y1-y0)*i/10}]});await sl(25);}
 await cd.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await sl(340);
};
await p.goto(origin+'/models/');await p.locator('#search').fill(id);await p.locator('#option-'+id).tap();
await p.waitForFunction(()=>document.querySelector('#detail-poster').dataset.state==='ready'&&document.querySelector('#detail').dataset.state==='static');
await go(45);const staticStart=await frame('static-start');assert(staticStart.touch==='pan-y');
await swipe(330,340,240);const staticEnd=await frame('static-scroll');assert(staticEnd.y>staticStart.y+20,'center swipe must scroll when not inspecting');
await go(0);await p.locator('#mobile-interact').tap();await p.waitForFunction(()=>document.querySelector('#detail').dataset.state==='ready');
await go(0);const initial=await frame('ready-initial');
await go(100);const middle=await frame('ready-programmatic-scroll');
assert(middle.y===100&&Math.abs(initial.stage.top-middle.stage.top-100)<.01);
assert(middle.frames>initial.frames&&middle.canvasSha!==initial.canvasSha,'frame must follow document scroll');
assert.deepEqual(initial.q,middle.q);
await swipe(330,345,240);const center=await frame('active-center-orbit');
assert(Math.abs(center.y-middle.y)<=4,'active media center must retain orbit');assert.notDeepEqual(center.q,middle.q);
const edgeHit=await p.evaluate(()=>document.elementFromPoint(12,310).className);assert.equal(edgeHit,'detail-media');
await swipe(12,340,220);const edge=await frame('active-edge-scroll');
assert(edge.y>center.y+20,'edge swipe must scroll while inspecting');
assert.deepEqual(edge.q,center.q);assert(edge.frames>center.frames&&edge.canvasSha!==center.canvasSha);
await go(0);await p.setViewportSize({width:667,height:150});await sl(400);
const outView=await frame('active-outside-viewport');assert(!outView.visible&&outView.stage.top>outView.innerH);
await go(210);const inside=await frame('active-reentered-viewport');
assert(inside.visible&&inside.frames>outView.frames&&inside.canvasSha!==outView.canvasSha);assert.deepEqual(outView.q,inside.q);
await p.setViewportSize({width:390,height:844});await sl(450);const portrait=await frame('active-resized-portrait');
assert.equal(portrait.stage.width,390);assert.deepEqual(inside.q,portrait.q);assert(portrait.frames>inside.frames&&portrait.motion);
await go(0);await p.locator('#mobile-interact').tap();await p.waitForFunction(()=>document.querySelector('#detail').dataset.state==='static'&&document.querySelector('#detail-poster').dataset.state==='ready');
await p.setViewportSize({width:667,height:375});await sl(400);await go(45);
const exit=await frame('exit-reading-start');assert(exit.touch==='pan-y');
await swipe(330,340,240);const scrolled=await frame('exit-reading-scroll');assert(scrolled.y>exit.y+20);
await go(0);await p.locator('#mobile-back').focus();assert.equal(await p.evaluate(()=>document.activeElement.id),'mobile-back');
await p.keyboard.press('Enter');await p.locator('#search').waitFor({state:'visible'});
console.log('SWIPE_SCROLL_ROTATION_REDUCED_MOTION_PASS',results.length);
}finally{await writeFile(out+'/SWIPE-SCROLL.json',JSON.stringify(results,null,2));await b.close();}

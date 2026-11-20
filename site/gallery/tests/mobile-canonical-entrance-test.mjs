import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFile} from 'node:fs/promises';
import {canonicalEntrancePlan} from '../canonical-entrance.js';
import {createMobileActivationIntent} from '../mobile-activation-intent.js';

const subject = {id:'sample',sha256:{glb:'a'.repeat(64)},galleryPosters:{detail:'gallery/example/detail.png'}};
const phone = {asset:subject,isPhone:true,openMobile:true,activateMobile:false,opening:{id:'sample',art:{},title:{}}};
const defer = () => {let resolve;const ready=new Promise(r=>resolve=r);return {ready,resolve};};
const tick = async () => {await Promise.resolve();await Promise.resolve();};

test('only a real published mobile entry with a local model-bound canonical right suppresses wheel art',()=>{
 const r=canonicalEntrancePlan(phone);assert(r.canonicalFirst);assert.equal(r.opening.art,null);assert.equal(r.opening.title,phone.opening.title);
 for(const override of [{reviewOnly:true},{isPhone:false},{opening:null},{activateMobile:true},
  {asset:{...subject,galleryPosters:{detail:'assets/preview.png'}}},{asset:{...subject,galleryPosters:{detail:'gallery/../escape.png'}}}]){
  const options={...phone,...override},skipped=canonicalEntrancePlan(options);
  assert.equal(skipped.canonicalFirst,false);assert.equal(skipped.opening,options.opening);
 }
});
test('expired or replaced pending intent cannot activate a newer generation of same ID; fresh valid press opens once',async()=>{
 const first=defer(),second=defer(),a={id:'sample',version:1},b={id:'sample',version:2},starts=[];
 let active=a,painted=false;
 const q=createMobileActivationIntent({eligible:(c,mode)=>c===active&&(mode==='pending'||mode==='ready'&&painted),activate:c=>starts.push(c)});
 q.bind(a,first.ready);assert.equal(q.request(),'pending');assert.equal(q.request(),'pending');
 q.clear();active=b;q.bind(b,second.ready);
 first.resolve(true);await tick();assert.deepEqual(starts,[]);
 painted=true;second.resolve(true);await tick();assert.deepEqual(starts,[]);
 assert.equal(q.request(),'activated');assert.equal(q.request(),'ignored');assert.deepEqual(starts,[b]);
});
test('decode failure clears pending without opening; fallback requires a fresh explicit request and real error identity',async()=>{
 const p=defer(),log=[],starts=[];let failed=false;
 const q=createMobileActivationIntent({eligible:(_,mode)=>mode==='pending'||mode==='missing'&&failed,activate:c=>starts.push(c),announce:x=>log.push(x)});
 q.bind('current',p.ready);assert.equal(q.request(),'pending');
 failed=true;p.resolve(false);await tick();
 assert.deepEqual(starts,[]);assert.deepEqual(log,['pending','unavailable']);
 assert.equal(q.request(),'fallback');assert.deepEqual(starts,['current']);
});
test('fixed real heading is limited to canonical-first openings; original typed title remains focusable',async()=>{
 const main=await readFile(new URL('../main.js',import.meta.url),'utf8');
 const motion=await readFile(new URL('../detail-continuity.js',import.meta.url),'utf8');
 assert.match(main,/phoneContinuity\.travel\(opening,\{opening:true,poster:selectedPoster\.bridge,staticTitle:canonicalFirst\}\)/);
 assert.match(main,/title\.tabIndex=-1/);assert.match(main,/title\.focus\(\{preventScroll:true\}\)/);
 assert.match(motion,/const fixedTitle = opening && staticTitle;/);
 assert.match(motion,/fixedTitle \? null : titleFrame\(targetTitle\)/);
 assert.match(motion,/opening && !motion\.title && !fixedTitle\) entries\.push\(title\)/);
});

test('visible pending feedback is a disposable child of empty stage status and never covers a visible model',async()=>{
 const main=await readFile(new URL('../main.js',import.meta.url),'utf8');
 const a=main.indexOf('const mobilePendingCopy='),b=main.indexOf('const mobileIntent=createMobileActivationIntent');
 assert(a>=0&&b>a);
 let child=null,ownedByOrdinaryPage='',bridge=null;
 const img={dataset:{modelId:'sample',source:'canonical',state:'loading'},style:{visibility:'hidden'}};
 const loading={get textContent(){return ownedByOrdinaryPage+(child?.textContent||'');},append(node){child=node;}};
 const {runInNewContext}=await import('node:vm');
 const sandbox={document:{createElement:()=>({attributes:{},setAttribute(k,v){this.attributes[k]=v;},remove(){if(child===this)child=null;}})},
  stage:{dataset:{state:'static'}},state:{selected:'sample'},stagePoster:{frame:()=>bridge},$:q=>q==='#detail-poster'?img:loading,t:(_,zh)=>zh};
 const helper=main.slice(a,b)+'globalThis.controls=[showMobilePendingCopy,clearMobilePendingCopy]';
 runInNewContext(helper,sandbox);const [show,clear]=sandbox.controls;
 show();assert.equal(child.textContent,'正在准备模型预览…');assert.equal(child.attributes['aria-hidden'],'true');
 ownedByOrdinaryPage='a different current status';child=null;clear();assert.equal(loading.textContent,ownedByOrdinaryPage);
 show();assert.equal(child,null);
 ownedByOrdinaryPage='';img.style.visibility='visible';show();assert.equal(child,null);
 img.style.visibility='hidden';bridge={};show();assert.equal(child,null);
 bridge=null;img.dataset.modelId='superseded';show();assert.equal(child,null);
 assert.match(main,/if\(!active\(\)\)\{finish\(false\);return;\}if\(revealing\)return;revealing=true;clearMobilePendingCopy\(\)/);
 assert.match(main,/image\.onerror=\(\)=>\{\n  if\(!active\(\)\)return;\n  clearMobilePendingCopy\(\)/);
});

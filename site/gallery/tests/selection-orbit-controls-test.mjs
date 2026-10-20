// Executes the real main.js event wiring in a minimal DOM, not a browser/layout test.
import * as dimensionPresentation from '../model-dimensions.js';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import * as THREE from 'three';
import {PreviewRenderer} from '../renderer.js';
import {ViewTransition} from '../view-transition.js';
import {WheelTitle} from '../wheel-title.js';
import {filterItems,WheelSettler} from '../state.js';
import {publishedModels,assetURL as fixtureAssetURL,repositoryURL,installGeometryOnlyTextureFixture} from './geometry-fixtures.mjs';
import {prepareModels,siteRoot,assetURL,readGalleryQuery,galleryURL,emptyFacets,detailHref} from '../catalog-source.js';
import {PACK_LABELS,WORLD_LABELS} from '../../curation.js';
import {modelShortName} from '../presentation-labels.js';
import {ThumbnailQueue} from '../thumbnail-queue.js';
import {thumbnailPlaceholderMarkup,synchronizeThumbnailPlaceholders} from '../thumbnail-placeholder.js';
import {parseRoute} from '../../routes.js';
const rawModels=await publishedModels(),resources=JSON.parse(await readFile(new URL('../../public/gallery/resources.json',import.meta.url),'utf8'));
const models=prepareModels({assets:rawModels},resources),catalog={manifest:{assets:rawModels,review_only:false},route:{lang:'en',page:0}};
const restoreTextureLoader=installGeometryOnlyTextureFixture();
let time=0,serial=0,reduced=false,mobile=false,selectCalls=0,pushes=0,latestHistorySnapshot;
const timers=new Map(),media=new Map(),elements=new Map();
const schedule=(fn,delay=0)=>{timers.set(++serial,{fn,at:time+delay});return serial;};
function advance(ms){const end=time+ms;for(let count=0;;count++){assert(count<10000,'timer loop');const next=[...timers].filter(([,t])=>t.at<=end).sort((a,b)=>a[1].at-b[1].at)[0];if(!next)break;time=next[1].at;timers.delete(next[0]);next[1].fn();}time=end;}
class Element{
 set src(value){this._src=value;queueMicrotask(()=>{if(this._src===value)this.onload?.();});}
 get src(){return this._src;}
 constructor(){this.children=[];this.events=new Map();this.dataset={};this.attributes={};this.style={setProperty(key,value){this[key]=value;}};this.scrollTop=0;this.clientHeight=600;this.hidden=false;this.value='';this.textContent='';this.classes=new Set();this.classList={add:(...v)=>v.forEach(x=>this.classes.add(x)),remove:(...v)=>v.forEach(x=>this.classes.delete(x)),contains:v=>this.classes.has(v),toggle:(v,on)=>on?this.classes.add(v):this.classes.delete(v)};}
 addEventListener(name,fn){if(!this.events.has(name))this.events.set(name,[]);this.events.get(name).push(fn);}
 dispatch(name,details={}){const e={target:this,preventDefault(){},stopPropagation(){},...details};for(const fn of this.events.get(name)||[])fn(e);}
 append(...items){for(const item of items){if(typeof item==='string')continue;item.parent=this;this.children.push(item);}}
 replaceChildren(...items){this.children=[];this.append(...items);}
 prepend(...items){for(const item of items.reverse()){item.parent=this;this.children.unshift(item);if(item.id)elements.set('#'+item.id,item);}}
 replaceWith(item){if(this.parent){const index=this.parent.children.indexOf(this);this.parent.children[index]=item;item.parent=this.parent;}if(item.id)elements.set('#'+item.id,item);this.parent=null;}

 remove(){if(this.parent)this.parent.children=this.parent.children.filter(el=>el!==this);}
 setAttribute(name,value){this.attributes[name]=value;}
 removeAttribute(name){delete this.attributes[name];}
 focus(){} contains(){return false;} matches(){return false;}
 set innerHTML(value){this.children=[];if(value.includes('slot-image')){this.parts=new Map(['img','strong','small','.current','.slot-image','.slot-copy'].map(key=>[key,new Element()]));}}
 get innerHTML(){return '';}
 querySelector(selector){if(selector==='[data-en]'){if(!this.copyText){this.copyText=new Element();this.copyText.dataset={en:'Copy attribution · CC BY 4.0',zh:'复制署名 · CC BY 4.0'};}return this.copyText;}return this.parts?.get(selector)||null;}
 getBoundingClientRect(){return {left:0,top:0,right:600,bottom:600,width:600,height:600};}
 insertBefore(node,before){node.remove();node.parent=this;const index=this.children.indexOf(before);if(index<0)this.children.push(node);else this.children.splice(index,0,node);}
 get isConnected(){return !!this.parent;}
}
Element.prototype.removeEventListener=function(n,fn){this.events.set(n,(this.events.get(n)||[]).filter(f=>f!==fn));};Element.prototype.getRootNode=function(){return document;};Element.prototype.setPointerCapture=function(){};Element.prototype.releasePointerCapture=function(){};Element.prototype.getBoundingClientRect=function(){return {left:0,top:0,right:600,bottom:600,width:600,height:600};};
function $(selector){if(selector.startsWith('#option-'))return elements.get('#slots')?.children.find(el=>el.id===selector.slice(1))||null;if(!elements.has(selector))elements.set(selector,new Element());return elements.get(selector);}
const document=new Element();Object.assign(document,{documentElement:new Element(),body:new Element(),baseURI:siteRoot.href,querySelector:$,querySelectorAll:()=>[],createElement:()=>new Element(),createTextNode:text=>({textContent:text})});
const window=new Element();
function matchMedia(query){if(!media.has(query)){const value=new Element();Object.defineProperty(value,'matches',{get:()=>query.includes('reduced-motion')?reduced:query.includes('max-width')?mobile:query.includes('hover:hover')});media.set(query,value);}return media.get(query);}
const now=()=>time;
class TestTitle extends WheelTitle{constructor(args){super({...args,now,schedule,cancel:id=>timers.delete(id)});}}
class TestThumbnails extends ThumbnailQueue{constructor(){super({setTimer:schedule,clearTimer:id=>timers.delete(id)});}}
class TestSettler extends WheelSettler{constructor(args){super({...args,now,frame:fn=>schedule(fn,16),cancel:id=>timers.delete(id)});}}
const network=[],draws=[];let clears=0;

Object.defineProperty(globalThis,'performance',{value:{now},configurable:true});
globalThis.document=document;globalThis.matchMedia=matchMedia;globalThis.innerWidth=1200;globalThis.innerHeight=800;
globalThis.requestAnimationFrame=fn=>schedule(()=>fn(time),16);globalThis.cancelAnimationFrame=id=>timers.delete(id);
globalThis.fetch=async(url,{signal}={})=>{
 const path=new URL(url).pathname.slice(1);
 if(path.startsWith('gallery/scale-reference/')){const bytes=await readFile(new URL('site/public/'+path,repositoryURL));return {ok:true,arrayBuffer:async()=>bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength)};}
 return new Promise((resolve,reject)=>network.push({path,signal,reject,async resolve(){const bytes=await readFile(fixtureAssetURL(path));resolve({ok:true,arrayBuffer:async()=>bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength)});}}));
};
const r=Object.create(PreviewRenderer.prototype);r.stats={requests:0,aborted:0,stale:0,cacheByteLimit:48*1024*1024};r.cache=new Map();r.pending=new Map();r.token=r.referenceToken=0;r.wire=false;r.stopHover=()=>{};
r.detail={scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera(38,1,.01,100),contact:new THREE.Object3D(),target:new THREE.Vector3()};r.detail.scene.fog=new THREE.Fog('#c5bdb3',6,18);r.controls={target:new THREE.Vector3(),enabled:false,update(){}};
r.renderer={domElement:{style:{}},setScissorTest(){},setClearColor(){},clear(){clears++;}};
r.host=$('#detail');r.visible=true;
// Mock the completed GPU render, then exercise the real tokenized RAF acknowledgement.
r.draw=()=>{if(!r.lost){r.renderer.domElement.style.visibility='visible';if(r.detail.model)r.acknowledgeDetailFrame();}draws.push({id:r.detail.asset?.id,model:!!r.detail.model,visibility:r.renderer.domElement.style.visibility});};
r.host=$('#detail');r.controls=r.createControls(r.host);
r.viewMotion=new ViewTransition({read:()=>r.viewState(),write:(state,ownership)=>r.applyState(state,ownership),reduced:()=>reduced});
const location=new URL('models/',siteRoot);
const history={state:null,replaceState(value,_,url){this.state=structuredClone(value);latestHistorySnapshot=this.state;if(url)location.href=url;},pushState(value,_,url){this.replaceState(value,_,url);pushes++;}};
const context=vm.createContext({...dimensionPresentation,modelShortName,thumbnailPlaceholderMarkup,synchronizeThumbnailPlaceholders,parseRoute,ThumbnailQueue:TestThumbnails,requestAnimationFrame:globalThis.requestAnimationFrame,cancelAnimationFrame:globalThis.cancelAnimationFrame,AbortController,window,document,location,localStorage:{getItem:()=>null,setItem(){}},URL,matchMedia,models,catalog,siteRoot,assetURL,readGalleryQuery,galleryURL,emptyFacets,detailHref,PACK_LABELS,WORLD_LABELS,WheelTitle:TestTitle,WheelSettler:TestSettler,filterItems,HoverTurntable:class{},PreviewRenderer:class{constructor(){return r;}},POSTER_IMAGE_SCALE:1,performance:{now},setTimeout:schedule,clearTimeout:id=>timers.delete(id),structuredClone,history,console:{warn(){}},navigator:{}});
let source=await readFile(new URL('../main.js',import.meta.url),'utf8');
assert(source.includes('export async function mountGallery(){'),'The app must mount explicitly after startup prerequisites');
// Unwrap only the mount boundary so the existing deterministic probes can still
// inspect its lexical state. All application event wiring remains the real code.
source=source.replace('export async function mountGallery(){','').replace('mountIcons(document);','').replace(/\n}\s*$/,'');
source=source.replace(/^import .*;$/gm,'').replace(/^if\(import\.meta\.hot\).*$/gm,'').replace(/if\(state.selected\)await choose\(/m,'if(state.selected)void choose(');
// Execute the actual UI helper inside this deterministic DOM harness too.
const uiSource=(await readFile(new URL('../ui-feedback.js',import.meta.url),'utf8')).replace(/^export /gm,'');
const guideSource=(await readFile(new URL('../wheel-guides.js',import.meta.url),'utf8')).replace(/^export /gm,'');
vm.runInContext(uiSource+'\n'+guideSource+'\n'+source,context);

const p=window.__preview,checks=[];
const flush=async()=>{for(let i=0;i<3;i++){await new Promise(resolve=>setImmediate(resolve));advance(40);}};
const settle=async promise=>{
 let done=false,value,error;Promise.resolve(promise).then(v=>{done=true;value=v;},e=>{done=true;error=e;});
 // RAF uses the deterministic clock, while source SHA256 uses Node's real async
 // worker pool. A fixed number of immediates can finish before that work runs.
 const deadline=Date.now()+15000;
 while(!done&&Date.now()<deadline){await flush();if(!done)await new Promise(resolve=>setTimeout(resolve,1));}
 assert(done,`Selection ${p.state.selected} did not settle within 15 real seconds after matching render/RAF (status ${r.stats.detailStatus})`);
 if(error)throw error;return value;
};
const settleChoice=(...args)=>settle(p.choose(...args));
const model=id=>models.find(a=>a.id===id),request=id=>network.findLast(n=>n.path===model(id).glb);
const active=id=>{assert.equal(p.state.selected,id);assert.equal($('#detail').dataset.modelId,id);assert.equal($('#detail-poster').dataset.modelId,id);assert.equal($('#detail-poster').src,assetURL(model(id).galleryPosters?.detail||model(id).preview));};
const baseline=()=>{const actual=r.viewState(),wanted=r.singleState();for(const key of ['position','target','modelPosition','modelQuaternion'])actual[key].forEach((x,i)=>assert(Math.abs(x-wanted[key][i])<1e-7,key));assert.equal(actual.zoom,1);assert.equal(r.comparison,false);assert.equal(r.companion,null);assert.equal(r.cameraFrame,0);assert.equal(r.referenceFrame,0);assert.equal(r.controls.enabled,true);};
const first=p.state.selected;await request(first).resolve();await flush();assert.equal($('#detail').dataset.state,'ready');baseline();
$('#wheel').scrollTop=0;p.renderWheel();await settleChoice(first,{center:true});advance(600);assert.equal($('#wheel').scrollTop,p.state.results.findIndex(asset=>asset.id===first)*128);assert.equal(p.settler.state,'idle');
checks.push('Non-reduced-motion desktop activation completes its centering RAF after collection visibility is synchronized');
// Inspect each transient handoff boundary, instead of only its ready endpoint.
const handoff=p.choose(first);const handoffPoster=$('#detail-poster');let decodeHandoff;handoffPoster.decode=()=>new Promise(resolve=>decodeHandoff=resolve);await new Promise(resolve=>setImmediate(resolve));assert.equal(r.detail.model,null);assert.equal(handoffPoster.style.visibility,'hidden');decodeHandoff();await new Promise(resolve=>setImmediate(resolve));assert.equal(handoffPoster.style.visibility,'visible');assert.equal(handoffPoster.classList.contains('ready'),false);assert.equal(r.detail.model,null);advance(16);assert.equal(r.detail.model,null);advance(16);await new Promise(resolve=>setImmediate(resolve));assert(r.detail.model);assert.equal(r.controls.enabled,false);assert.equal(handoffPoster.classList.contains('ready'),false);advance(16);assert.equal(handoffPoster.classList.contains('ready'),false);advance(16);await handoff;assert.equal(handoffPoster.classList.contains('ready'),true);baseline();
checks.push('Cached handoff exposes selected decoded poster, waits its presentation, renders matching mesh, then waits two frame boundaries before crossfade/interaction');
const oldPoster=$('#detail-poster');oldPoster.style.visibility='visible';r.rotate(173,72);r.zoom(.35);r.detail.camera.zoom=2;
const B='calceola',C='cycad';const pb=p.choose(B);active(B);const posterB=$('#detail-poster'),staleBLoad=posterB.onload,staleBError=posterB.onerror;
assert.notEqual(posterB,oldPoster);assert.equal(oldPoster.onload,null);assert.equal(posterB.style.visibility,'hidden');assert.equal(r.detail.model,null);assert.equal(r.renderer.domElement.style.visibility,'visible');assert.equal(r.controls.enabled,false);
const pc=p.choose(C);active(C);const posterC=$('#detail-poster');assert.notEqual(posterB,posterC);assert.equal(r.detail.model,null);staleBLoad();staleBError();await flush();active(C);assert.equal(posterC.style.visibility,'visible');
await request(B).resolve();await settle(pb);active(C);assert.equal($('#detail').dataset.state,'loading');assert.equal(r.detail.model,null);
await request(C).resolve();await settle(pc);active(C);baseline();assert.equal($('#detail').dataset.state,'ready');
checks.push('Actual main.js plus PreviewRenderer A→B→C cold selection clears the old model/poster while retaining the stage and rejects stale GLB/image callbacks');
// The image decode itself may finish after selection changes.
let finishDecode;posterC.decode=()=>new Promise(resolve=>finishDecode=resolve);const loadC=posterC.onload;loadC();
r.rotate(80,50);r.zoom(2);const cached=p.choose(first,{preserve:true,view:{azimuth:170,elevation:70}});const currentPoster=$('#detail-poster');finishDecode();await settle(cached);await flush();active(first);baseline();assert.equal(currentPoster.style.visibility,'visible');assert.equal(posterC.onload,null);
checks.push('Cached selection ignores legacy preserve/hover pose options and delayed image decode cannot reveal the previous poster');
// Stale errors never flip the newest loading/ready UI into fallback.
const badB=p.choose(B);const cachedC=p.choose(C);request(B).reject(new Error('late old network failure'));await settle(Promise.all([badB,cachedC]));active(C);assert.equal($('#detail').dataset.state,'ready');baseline();
checks.push('A stale request error cannot overwrite the newest cached asset status');
const D='fern-cluster';const failed=p.choose(D);request(D).reject(new Error('current network failure'));await settle(failed);active(D);assert.equal($('#detail').dataset.state,'fallback');assert.equal(r.detail.model,null);assert.equal(r.renderer.domElement.style.visibility,'visible');assert.equal($('#retry').hidden,false);const failedPoster=$('#detail-poster');failedPoster.onerror();assert.equal(failedPoster.src,new URL(model(D).preview,document.baseURI).href);failedPoster.onerror();assert.equal(failedPoster.style.visibility,'hidden');
const retry=p.choose(D,{push:false});await request(D).resolve();await settle(retry);baseline();active(D);assert.equal($('#detail').dataset.state,'ready');
checks.push('Current failure keeps only the selected asset fallback, image fallback is ID-scoped, and Retry starts from a clean baseline');
await settleChoice(C);r.rotate(90,12);r.zoom(.4);r.compare(true);await r.referenceReady;advance(250);assert(r.cameraFrame);assert(r.referenceFrame);const toA=p.choose(first);assert.equal(r.companion,null);assert.equal(r.cameraFrame,0);assert.equal(r.referenceFrame,0);await settle(toA);advance(4000);baseline();active(first);assert(Math.abs(r.detail.scene.fog.near-Math.max(6,r.viewState().distance*1.5))<1e-10);
checks.push('Compare during entry → switch cancels both RAF owners/reference and resets fog, framing and zoom for the new model');
reduced=true;r.rotate(180,55);r.zoom(3);await settleChoice(C);baseline();active(C);assert.equal($('#detail').dataset.state,'ready');reduced=false;
checks.push('Reduced-motion selection follows the same independent baseline without transition callbacks');
// Browser context loss is modelled by the same suspend path used by the real handler.
const E='opabinia',lost=p.choose(E);r.lost=true;r.suspend();r.onError(new Error('WebGL context lost'),{assetId:E,token:r.token});await request(E).resolve();await settle(lost);active(E);assert.equal($('#detail').dataset.state,'fallback');assert.equal(r.detail.model,null);assert.equal(r.controls.enabled,false);assert.equal(r.renderer.domElement.style.visibility,'hidden');r.lost=false;
checks.push('Context loss during pending load invalidates selection, so late success cannot hide the fallback or enable controls');
// Context loss after a cached GLB resolves must also release a pending poster decode.
const blockedPoster=p.choose(D);const waitingImage=$('#detail-poster');let unblockPoster;waitingImage.decode=()=>new Promise(resolve=>unblockPoster=resolve);await new Promise(resolve=>setImmediate(resolve));assert.equal(r.detail.model,null);r.lost=true;r.suspend();r.onError(new Error('WebGL context lost'),{assetId:D,token:r.token});await settle(blockedPoster);advance(1000);assert.equal($('#detail').dataset.state,'fallback');assert.equal($('#loading').textContent,'Static preview · 3D unavailable');r.lost=false;unblockPoster?.();await flush();
checks.push('Context loss between cached GLB completion and poster decode releases select and cannot resurrect delayed loading text');
// Older async popstate continuations must not restore their stale wheel/keyboard/mobile state.
const F='waptia',historyA={gallery:true,view:'detail',selected:F,keyboard:F,scroll:128,mobileOpen:true},historyB={gallery:true,view:'collection',selected:first,keyboard:first,scroll:512,mobileOpen:false};
const pops=window.events.get('popstate');assert.equal(pops.length,1);
location.href=new URL('models/?model='+F,siteRoot).href;const back=pops[0]({state:historyA});location.href=new URL('models/',siteRoot).href;const forward=pops[0]({state:historyB});await request(first).resolve();await settle(forward);await request(F).resolve();await settle(back);assert.equal(p.state.selected,first);assert.equal(p.state.keyboard,first);assert.equal($('#wheel').scrollTop,512);assert.equal(p.state.mobileOpen,false);baseline();
checks.push('Rapid Back/Forward rejects the old post-await navigation continuation as well as its old GLB');

const host=$('#detail');const pointer=(name,id,type,x,y)=>host.dispatch(name,{pointerId:id,pointerType:type,button:0,clientX:x,clientY:y,pageX:x,pageY:y});
for(const type of ['mouse','touch']){
 await settleChoice(first);const before=r.controls;
 pointer('pointerdown',21,type,100,100);pointer('pointermove',21,type,150,130);
 assert(r.detail.orientation.quaternion.angleTo(new THREE.Quaternion())>.01,type+' should actually rotate');
 const loading=p.choose(C);assert.notEqual(r.controls,before);assert.equal((host.events.get('pointermove')||[]).length,0);await settle(loading);baseline();
 pointer('pointermove',21,type,210,170);baseline();pointer('pointerup',21,type,210,170);
 pointer('pointerdown',22,type,110,110);pointer('pointermove',22,type,160,140);assert(r.detail.orientation.quaternion.angleTo(new THREE.Quaternion())>.01,type+' fresh gesture must work');pointer('pointerup',22,type,160,140);
 assert.equal((host.events.get('pointerdown')||[]).length,1);assert.equal((host.events.get('pointermove')||[]).length,0);
}
checks.push('Actual OrbitControls mouse/touch held gestures are discarded on selection; fresh gestures work and listeners stay singular');
mobile=true;await settleChoice(C);assert.equal(host.style.touchAction,'pan-y');assert.equal($('#detail').dataset.state,'static');assert.equal(r.detail.model,null);assert.equal(r.controls.enabled,false);
pointer('pointerdown',31,'touch',100,100);pointer('pointermove',31,'touch',150,120);assert.equal((host.events.get('pointermove')||[]).length,0);
await settleChoice(C,{activateMobile:true});baseline();assert.equal(host.style.touchAction,'none');pointer('pointermove',31,'touch',220,120);baseline();
pointer('pointerdown',32,'touch',100,100);pointer('pointermove',32,'touch',140,130);assert(r.detail.orientation.quaternion.angleTo(new THREE.Quaternion())>.01);
await settleChoice(C);assert.equal(host.style.touchAction,'pan-y');assert.equal(r.controls.enabled,false);assert.equal((host.events.get('pointermove')||[]).length,0);
await settleChoice(C,{activateMobile:true});baseline();pointer('pointermove',32,'touch',180,150);baseline();pointer('pointerup',32,'touch',180,150);
assert.equal((host.events.get('pointerdown')||[]).length,1);assert.equal((host.events.get('pointercancel')||[]).length,1);
checks.push('Actual controls mobile static/interact/static/interact keeps pan-y/none policy, rejects held touch, and has no duplicate listeners');
await settleChoice(first,{openMobile:false});p.state.mobileOpen=false;$('#wheel').scrollTop=0;
const savedList={gallery:true,view:'collection',lang:p.state.lang,page:0,selected:first,query:'',facets:emptyFacets(),sort:'curated',scroll:0,keyboard:C,mobileOpen:false};
location.href=new URL('models/',siteRoot).href;await pops[0]({state:savedList});
assert.equal(p.state.mobileOpen,false);assert.equal(latestHistorySnapshot.mobileOpen,false);
assert.equal(p.state.keyboard,C);assert.equal(latestHistorySnapshot.keyboard,C);
assert.equal($('#wheel').scrollTop,0);assert.equal(latestHistorySnapshot.scroll,0);
checks.push('Mobile Back/Forward persists the fully restored list/keyboard/scroll snapshot even when unchanged scroll emits no event');
mobile=false;

// Sorting UI must preserve URL aliases and reorder only locale-aware sorts.
p.state.sort=readGalleryQuery(new URLSearchParams('sort=triangles-asc')).sort;
vm.runInContext('applyResults(false)',context);$('#filters').onclick();
const aliasSelect=$('#filter-form').children.at(-1).children[1];
assert.equal(aliasSelect.value,'triangles');assert(aliasSelect.children.some(option=>option.value===aliasSelect.value));
assert.equal(vm.runInContext('draft.sort',context),'triangles-asc');
const ascendingIds=p.state.results.map(asset=>asset.id);$('#filter-apply').onclick();
assert.equal(p.state.sort,'triangles-asc');assert.deepEqual(p.state.results.map(asset=>asset.id),ascendingIds);
checks.push('The triangles-asc URL alias displays the available ascending option without changing its query meaning or order when filters are applied');
const selectedBeforeSort=p.state.selected,meshBeforeSort=r.detail.model,rendererTokenBeforeSort=r.token,selectionVersionBeforeSort=vm.runInContext('selectionVersion',context),requestsBeforeSort=r.stats.requests;
const assertSortKeepsSelection=()=>{assert.equal(p.state.selected,selectedBeforeSort);assert.equal(r.detail.model,meshBeforeSort);assert.equal(r.token,rendererTokenBeforeSort);assert.equal(vm.runInContext('selectionVersion',context),selectionVersionBeforeSort);assert.equal(r.stats.requests,requestsBeforeSort);};
for(const sort of ['name','name-desc']){
 p.state.lang='en';p.state.sort=sort;vm.runInContext('applyResults(false)',context);
 const anchor=p.state.results[50].id,keyboard=p.state.results[5].id,offset=11.25;
 p.state.keyboard=keyboard;$('#wheel').scrollTop=50*128+offset;p.renderWheel();assert.equal(p.state.center,anchor);
 for(const lang of ['zh','en']){
  const previousIds=Array.from(p.state.results,asset=>asset.id);$('#language').onclick();
  assert.equal(p.state.lang,lang);
  const expected=Array.from(vm.runInContext('compute().map(asset=>asset.id)',context));
  assert.notDeepEqual(expected,previousIds,'Published localized names must exercise an actual reorder');
  assert.deepEqual(Array.from(p.state.results,asset=>asset.id),expected);
  assert.equal(p.state.center,anchor);assert.equal(p.state.keyboard,keyboard);
  assert.equal($('#wheel').scrollTop,expected.indexOf(anchor)*128+offset);
  assert.equal(latestHistorySnapshot.scroll,$('#wheel').scrollTop);assert.equal(latestHistorySnapshot.lang,lang);
  assertSortKeepsSelection();
 }
}
for(const sort of ['curated','triangles','triangles-asc','triangles-desc']){
 p.state.lang='en';p.state.sort=sort;vm.runInContext('applyResults(false)',context);
 $('#wheel').scrollTop=42*128+17.25;p.renderWheel();
 const results=p.state.results,ids=Array.from(results,asset=>asset.id),scroll=$('#wheel').scrollTop,center=p.state.center;
 for(const lang of ['zh','en']){
  $('#language').onclick();assert.equal(p.state.lang,lang);assert.equal(p.state.results,results);
  assert.deepEqual(Array.from(p.state.results,asset=>asset.id),ids);assert.equal($('#wheel').scrollTop,scroll);assert.equal(p.state.center,center);assertSortKeepsSelection();
 }
}
p.state.sort='curated';vm.runInContext('applyResults(false)',context);
checks.push('Language changes re-sort name/name-desc in both directions while preserving the browse anchor, fractional scroll offset, keyboard and selected mesh; other sorts retain their exact result array and scroll with no selection or GLB request');

const requestsBeforePreload=r.stats.requests;for(let i=0;i<models.length;i++){$('#wheel').scrollTop=i*128;p.renderWheel();await new Promise(resolve=>setImmediate(resolve));assert(vm.runInContext('detailPosterCache.size<=DETAIL_POSTER_CACHE_LIMIT',context));assert(vm.runInContext('[...detailPosterCache].every(([id,entry])=>entry.image.src===poster(sample.find(asset=>asset.id===id)))',context));}assert.equal(r.stats.requests,requestsBeforePreload);
checks.push('Browsing warms only declared detail poster/fallback paths in a bounded eight-entry cache and makes no GLB requests');
const originalCrypto=Object.getOwnPropertyDescriptor(globalThis,'crypto'),nativeCrypto=globalThis.crypto;let delayedDigests=0;
assert(nativeCrypto?.subtle&&originalCrypto.configurable,'Native configurable Web Crypto is required for reviewed-source identity checks');
try{
 Object.defineProperty(globalThis,'crypto',{configurable:true,value:{subtle:{async digest(...args){delayedDigests++;await new Promise(resolve=>setTimeout(resolve,40));return nativeCrypto.subtle.digest(...args);}}}});
 const started=Date.now(),delayed=p.choose('confuciusornis',{push:false,openMobile:false});await request('confuciusornis').resolve();
 assert.equal(r.controls.enabled,false);assert.equal(r.detail.model,null);
 await settle(delayed);active('confuciusornis');baseline();assert.equal(delayedDigests,1);assert(Date.now()-started>=35);assert(r.detail.supportRule,'Delayed source identity must still validate the reviewed foot support');
 checks.push('A real asynchronous source digest delayed beyond immediate-loop cadence still gates mesh readiness and validates reviewed support before selection completes');
}finally{Object.defineProperty(globalThis,'crypto',originalCrypto);}
// History owns synchronous route restoration, never the lifetime of a GLB.
const pendingStart=network.length,restoreId='canadaspis';location.href=new URL('models/?model='+restoreId,siteRoot).href;
const delayedRestore=pops[0]({state:{gallery:true,view:'detail',selected:restoreId,keyboard:restoreId,scroll:256,mobileOpen:false}});
assert.equal(vm.runInContext('restoringHistory',context),false,'Pending GLB must not lock list scrolling/history');
$('#wheel').scrollTop=1024;$('#wheel').dispatch('scroll');assert.equal(latestHistorySnapshot.scroll,1024);
const contextRetry=r.onRestore();assert.equal(vm.runInContext('restoringHistory',context),false);
for(const pending of network.slice(pendingStart))await pending.resolve();await settle(Promise.all([delayedRestore,contextRetry]));
assert.equal(vm.runInContext('restoringHistory',context),false);assert.equal($('#wheel').scrollTop,1024);assert.equal(latestHistorySnapshot.scroll,1024);baseline();
checks.push('Delayed history GLB permits scrolling and push:false context retry without a stuck guard or stale scroll rewind');

let fullCatalogSelections=0;
for(const asset of models){
 const beforeRequests=network.length,selection=p.choose(asset.id,{push:false,openMobile:false});
 for(const pending of network.slice(beforeRequests))await pending.resolve();
 await settle(selection);active(asset.id);baseline();
 assert.equal(r.stats.detailFirstFrameId,asset.id,'Only the current rendered model may acknowledge readiness');
 assert.equal($('#detail').dataset.state,'ready');
 assert.equal($('#dimensions').textContent,dimensionPresentation.modelHeight(asset));
 fullCatalogSelections++;
}
assert.equal(fullCatalogSelections,models.length);
checks.push('Every published GLB completes actual selection parsing, poster gating, frame acknowledgement and a fresh interactive baseline; geometry-only texture fixtures are not browser decode coverage');
assert(clears>=12);r.suspend();p.settler.dispose();window.dispatch('pagehide',{persisted:false});
await mkdir(new URL('./evidence/',import.meta.url),{recursive:true});await writeFile(new URL('./evidence/selection-orbit-controls-report.json',import.meta.url),JSON.stringify({status:'passed',scope:'Actual main.js, PreviewRenderer and OrbitControls with real GLB parsing in deterministic DOM/network harness; geometry-only texture placeholders; browser parser remains authoritative for texture decoding; no browser raster verification',checks,fullCatalogSelections,canvasClears:clears},null,2));console.log(JSON.stringify({passed:checks.length,checks,fullCatalogSelections,canvasClears:clears},null,2));

restoreTextureLoader();

// Deterministic geometric audit, not browser/raster coverage. No app mutation.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {ScaleCompanion} from '../scale-reference.js';
import {ViewTransition} from '../view-transition.js';
import {PreviewRenderer} from '../renderer.js';
import {publishedModels,assetURL,referencesURL,parseGeometry,repositoryURL} from './geometry-fixtures.mjs';
const source=await readFile(new URL('../renderer.js',import.meta.url),'utf8');
class Element{
 constructor(){this.events=new Map();this.style={};this.clientHeight=900;this.clientWidth=1440;}
 addEventListener(name,fn,options={}){if(!this.events.has(name))this.events.set(name,[]);this.events.get(name).push({fn,capture:options===true||!!options.capture});}
 removeEventListener(name,fn){this.events.set(name,(this.events.get(name)||[]).filter(e=>e.fn!==fn));}
 dispatch(name,details={}){let stopped=false;const event={target:this,cancelable:true,defaultPrevented:false,preventDefault(){this.defaultPrevented=true;},stopPropagation(){},stopImmediatePropagation(){stopped=true;},...details};for(const {fn} of [...(this.events.get(name)||[])].sort((a,b)=>Number(b.capture)-Number(a.capture))){if(stopped)break;fn(event);}return event;}
 getRootNode(){return document;}
 setPointerCapture(){} releasePointerCapture(){}
 getBoundingClientRect(){return {left:0,top:0,right:1440,bottom:900,width:1440,height:900};}
}
let now=0,raf=0;const queue=new Map();
Object.defineProperty(globalThis,'performance',{value:{now:()=>now},configurable:true});
globalThis.document=Object.assign(new Element(),{baseURI:'https://example.test/'});
globalThis.matchMedia=()=>({matches:false});
globalThis.requestAnimationFrame=fn=>{queue.set(++raf,fn);return raf;};
globalThis.cancelAnimationFrame=id=>queue.delete(id);
const step=ms=>{now+=ms;const callbacks=[...queue.values()];queue.clear();callbacks.forEach(fn=>fn(now));};
const parse=async path=>(await parseGeometry(path)).scene;
const models=await publishedModels();
const refs={hand:await parse(new URL('hand-18cm-technical.glb',referencesURL)),human:await parse(new URL('human-180cm.glb',referencesURL))};
const entries=new Map();
for(const asset of models){const root=await parse(assetURL(asset.glb)),box=new THREE.Box3().setFromObject(root);entries.set(asset.id,{root,box,size:box.getSize(new THREE.Vector3()),sha256:createHash('sha256').update(await readFile(assetURL(asset.glb))).digest('hex')});}
function fixture(asset){
 const r=Object.create(PreviewRenderer.prototype);r.stats={};r.referenceToken=0;r.cameraInputGeneration=0;r.stopHover=()=>{};r.draw=()=>{};
 r.detail={scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera(38,1440/900,.01,100),contact:new THREE.Object3D(),target:new THREE.Vector3()};
 r.attach(r.detail,asset,entries.get(asset.id));r.host=new Element();r.controls=r.createControls(r.host);r.controls.enabled=true;
 r.viewMotion=new ViewTransition({read:()=>r.viewState(),write:(state,ownership)=>r.applyState(state,ownership)});r.applyState(r.singleState());r.resizeCamera(r.detail,1440,900);
 return r;
}
function compare(r){
 const kind=Math.max(...r.detail.entry.size.toArray())<.6?'hand':'human';const c=new ScaleCompanion(refs[kind].clone(true),kind);
 r.companion=c;r.reference=c.root;r.comparison=true;r.syncControlMode?.();r.detail.scene.add(c.root);c.apply(c.settled());r.comparisonState=r.comparisonLayout(c);r.applyState(r.comparisonState);return c;
}
function sample(r){
 r.detail.scene.updateMatrixWorld(true);r.detail.camera.updateMatrixWorld(true);
 const anchor=r.companion?r.companion.root.localToWorld(new THREE.Vector3()):new THREE.Vector3();
 const projected=anchor.clone().project(r.detail.camera),box=new THREE.Box3().setFromObject(r.detail.model,true);
 return {position:r.detail.camera.position.toArray(),target:r.controls.target.toArray(),modelPosition:r.detail.model.position.toArray(),modelQuaternion:r.detail.orientation.quaternion.toArray(),modelMinY:box.min.y,modelMaxY:box.max.y,referenceWorld:anchor.toArray(),referenceProjected:projected.toArray(),referenceMinY:r.companion?new THREE.Box3().setFromObject(r.companion.body,true).min.y:null,distance:r.viewState().distance,zoom:r.detail.camera.zoom,screenShiftY:r.detail.screenShiftY??r.detail.screenLift??null,viewState:r.viewState(),scale:r.detail.model.scale.toArray(),referenceScale:r.companion?.root.scale.toArray()};
}
const delta=(a,b)=>({targetY:b.target[1]-a.target[1],modelY:b.modelPosition[1]-a.modelPosition[1],referencePixelsY:-(b.referenceProjected[1]-a.referenceProjected[1])*450});
const pointer=(r,name,id,type,x,y)=>r.host.dispatch(name,{pointerId:id,pointerType:type,button:0,clientX:x,clientY:y,pageX:x,pageY:y});
function drag(r,type='mouse',dx=130,dy=95){pointer(r,'pointerdown',1,type,200,220);pointer(r,'pointermove',1,type,200+dx,220+dy);pointer(r,'pointerup',1,type,200+dx,220+dy);}
const measures=[];
for(const asset of models){
 const r=fixture(asset);compare(r);const before=sample(r);drag(r);const after=sample(r);
 assert(Math.abs(after.modelMinY)<1e-6,asset.id+' model ground');assert(Math.abs(after.referenceMinY)<1e-6,asset.id+' reference ground');
 assert.deepEqual(after.referenceScale,after.scale);assert.deepEqual(before.referenceWorld,after.referenceWorld);
 measures.push({id:asset.id,kind:r.companion.kind,...delta(before,after),before,after});r.controls.dispose();r.viewMotion.cancelAll();r.removeReference();
}
const asset=models.find(a=>a.id==='waptia');const r=fixture(asset);compare(r);
const scenarios=[];
const run=(name,action)=>{const before=sample(r);action();const after=sample(r);scenarios.push({name,...delta(before,after),before,after});};
run('single-touch diagonal drag',()=>drag(r,'touch'));
run('two-touch pinch',()=>{pointer(r,'pointerdown',31,'touch',100,100);pointer(r,'pointerdown',32,'touch',200,100);pointer(r,'pointermove',32,'touch',280,100);pointer(r,'pointermove',31,'touch',60,100);pointer(r,'pointerup',32,'touch',280,100);pointer(r,'pointerup',31,'touch',60,100);});
run('keyboard yaw only',()=>r.rotate(40,0));
run('keyboard elevation only',()=>r.rotate(0,30));
run('manual shared camera zoom',()=>r.zoom(.7));
const beforeReset=sample(r);r.compare(true);step(250);const duringReset=sample(r);drag(r);const afterInterrupt=sample(r);step(1000);const settledInterrupt=sample(r);scenarios.push({name:'repeat Compare reset interrupted by drag',beforeReset,duringReset,afterInterrupt,settledInterrupt,cameraWriteAfterInterrupt:settledInterrupt.position.map((n,i)=>n-afterInterrupt.position[i]),orientationWriteAfterInterrupt:settledInterrupt.modelQuaternion.map((n,i)=>n-afterInterrupt.modelQuaternion[i])});
r.reset();step(250);run('drag while reference fades during Reset',()=>drag(r));step(1000);
r.controls.dispose();r.viewMotion.cancelAll();r.removeReference();
const regular=fixture(asset);const regularBefore=sample(regular);drag(regular);const regularAfter=sample(regular);regular.controls.dispose();regular.viewMotion.cancelAll();
const localFetch=async(url,{signal}={})=>{signal?.throwIfAborted();const b=await readFile(new URL('site/public/'+new URL(url).pathname.slice(1),repositoryURL));signal?.throwIfAborted();return {ok:true,arrayBuffer:async()=>b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength)};};
globalThis.fetch=localFetch;
const entryInterruptions=[];
for(const at of [0,100,350,699]){
 const e=fixture(asset);e.rotate(137,11);e.compare(true);await e.referenceReady;step(at);drag(e);step(700);e.finishReference();
 const before=sample(e);e.zoom(.7);const after=sample(e);entryInterruptions.push({atMilliseconds:at,...delta(before,after),target:before.target,before,after});e.controls.dispose();e.viewMotion.cancelAll();e.removeReference();
}
const cold=fixture(asset);cold.rotate(137,11);let release;
globalThis.fetch=(url,options)=>new Promise((resolve,reject)=>{release=()=>localFetch(url,options).then(resolve,reject);});
cold.compare(true);drag(cold);cold.zoom(.8);await release();await cold.referenceReady;step(700);cold.finishReference();
const pendingBefore=sample(cold);cold.zoom(.7);const pendingAfter=sample(cold);const pendingReferenceInput={...delta(pendingBefore,pendingAfter),before:pendingBefore,after:pendingAfter};cold.controls.dispose();cold.viewMotion.cancelAll();cold.removeReference();globalThis.fetch=localFetch;
const report={mode:'current',rendererSHA256:createHash('sha256').update(source).digest('hex'),scope:'Actual GLB geometry, production renderer and actual Three.js OrbitControls in deterministic event harness; geometry-only texture placeholders; browser parser remains authoritative for texture decoding; no browser/raster validation',models:measures,scenarios,entryInterruptions,pendingReferenceInput,ordinaryInspection:{before:regularBefore,after:regularAfter},summary:{models:measures.length,worstReferencePixelDrift:Math.max(...measures.map(m=>Math.abs(m.referencePixelsY))),meanReferencePixelDrift:measures.reduce((sum,m)=>sum+Math.abs(m.referencePixelsY),0)/measures.length,pinchDistanceChange:scenarios[1].after.distance-scenarios[1].before.distance,pinchZoomChange:scenarios[1].after.zoom-scenarios[1].before.zoom}};
const output=new URL('./evidence/compare-ground/current-audit.json',import.meta.url);await mkdir(new URL('./evidence/compare-ground/',import.meta.url),{recursive:true});await writeFile(output,JSON.stringify(report,null,2));console.log(JSON.stringify({...report.summary,mode:report.mode,entryInterruptedZoom:entryInterruptions.map(({atMilliseconds,target,referencePixelsY})=>({atMilliseconds,target,referencePixelsY})),pendingLoadZoomDrift:pendingReferenceInput.referencePixelsY,worstModels:measures.sort((a,b)=>Math.abs(b.referencePixelsY)-Math.abs(a.referencePixelsY)).slice(0,8).map(({id,kind,targetY,referencePixelsY})=>({id,kind,targetY,referencePixelsY})),scenarios:scenarios.map(({name,targetY,referencePixelsY})=>({name,targetY,referencePixelsY})),output:output.pathname},null,2));

export {fixture,compare,sample,delta,drag,pointer,step,models,report,source,localFetch};

import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {entryAt,exitAt,DURATION,ENTRY_TIMING} from '../reference-entry.js';
import {ScaleCompanion} from '../scale-reference.js';
import {PreviewRenderer} from '../renderer.js';

// Real decoded meshes and production animation methods, driven by a deterministic
// frame queue. This verifies state/geometry, never claims browser raster coverage.
const close=(a,b,epsilon=1e-9)=>assert(Math.abs(a-b)<=epsilon,`${a} != ${b}`);
const checks=[],sequences=[],frameEvidence=[],prelightEvidence=[];
const numericKeys=['move','y','glow','opacity','gathered','open','articulation'];
const finiteState=state=>{
 for(const key of [...numericKeys,'progress'])assert(Number.isFinite(state[key]),`${key} is finite`);
 for(const key of ['move','glow','opacity','gathered','open','articulation'])assert(state[key]>=0&&state[key]<=1,`${key} is bounded`);
 assert(state.y>=0);assert.equal(state.gathered,0);close(state.articulation,state.open);
 assert.equal(state.visible,state.opacity>0);
};
const scalarState=state=>Object.fromEntries(numericKeys.map(key=>[key,state[key]]));
const samePose=(a,b)=>numericKeys.forEach(key=>close(a[key],b[key]));
const captureMaterialModes=fixture=>{
 const modes=fixture.materials.map(({material})=>({transparent:material.transparent,depthWrite:material.depthWrite,alphaTest:material.alphaTest,side:material.side,version:material.version}));
 const shadows=[];fixture.body.traverse(object=>{if(object.isMesh)shadows.push({object,castShadow:object.castShadow});});
 assert(shadows.some(({castShadow})=>castShadow),'solid body shadow is prepared before its first visible frame');
 const depths=[];
 for(const {object} of shadows)if(!object.userData.referenceTopology){
  assert.equal(object.castShadow,true);assert.equal(object.material.transparent,true);assert.equal(object.material.depthWrite,true);assert.equal(object.material.side,THREE.FrontSide);assert(object.material.alphaTest>0&&object.material.alphaTest<.02);
  const material=object.customDepthMaterial;assert(material?.isMeshDepthMaterial);assert.equal(material.depthPacking,THREE.RGBADepthPacking);
  const entry={object,material,disposed:0,mode:{transparent:material.transparent,depthWrite:material.depthWrite,alphaTest:material.alphaTest,side:material.side,version:material.version,depthPacking:material.depthPacking}};
  material.addEventListener('dispose',()=>entry.disposed++);depths.push(entry);
 }
 return {modes,shadows,depths};
};
const assertMaterialModes=(fixture,{modes,shadows,depths})=>{
 fixture.materials.forEach(({material},index)=>{for(const key of Object.keys(modes[index]))assert.equal(material[key],modes[index][key],`material ${key} must not switch during animation`);});
 for(const {object,castShadow} of shadows)assert.equal(object.castShadow,castShadow,'no delayed shadow-caster pop');
 for(const {object,material,mode,disposed} of depths){assert.equal(object.customDepthMaterial,material);assert.equal(disposed,0);for(const key of Object.keys(mode))assert.equal(material[key],mode[key],`custom depth material ${key} must not switch during animation`);}
 assert.equal(fixture.shadow.visible,fixture.state.opacity>0);assert.equal(fixture.contact.visible,fixture.state.opacity>0);
};
const smooth=t=>{t=Math.max(0,Math.min(1,t));return t*t*(3-2*t);};
const humanBaseline=(time,height,reduced=false)=>{
 const t=reduced?4.10:Math.max(0,Math.min(4.10,time)),open=1-smooth((t-1.95)/1.40);
 return {move:smooth(t/.70),y:height*.03*smooth((t-.95)/.95)*(1-smooth((t-2.20)/1.30)),glow:smooth((t-.10)/.80)*(1-smooth((t-2.70)/1.10)),opacity:smooth((t-.95)/.60),gathered:0,open,articulation:open,visible:smooth((t-.95)/.60)>0,progress:t/4.10,phase:t<.95?'掌根柔光':t<2.20?'轻升 · 手指舒展':t<3.50?'放松 · 平稳落下':'同一空间 · 真实比例'};
};

assert.deepEqual(ENTRY_TIMING,{
 layoutDuration:.70,glowDelay:.10,glowFadeInDuration:.80,
 revealStart:.95,revealDuration:.60,riseDuration:.95,
 settleStart:2.20,settleDuration:1.30,
 landedAt:3.50,handRelaxDuration:.60,
 humanRelaxStart:1.95,humanRelaxDuration:1.40,
 glowFadeOutStart:2.70,glowFadeOutDuration:1.10,total:4.10
});
assert.equal(DURATION,4.10);assert(Object.isFrozen(ENTRY_TIMING));
for(const kind of ['hand','human']){
 const height=kind==='hand'?.18:1.8;
 for(const [time,expectedGlow] of [[0,0],[.10,0],[.30,.15625],[.50,.5],[.70,.84375],[.90,1],[.95,1]]){
  const state=entryAt(time,height,false,kind);finiteState(state);close(state.glow,expectedGlow);
  assert.equal(state.opacity,0,'the full prelight must finish before the body appears');
  assert.equal(state.y,0);assert.equal(state.open,1);assert.equal(state.visible,false);
  prelightEvidence.push({kind,time,...scalarState(state),visible:state.visible});
 }
 // Smoothstep must ease both ends instead of merely stretching a linear fade.
 assert(entryAt(.11,height,false,kind).glow<.001);
 assert(1-entryAt(.89,height,false,kind).glow<.001);
 assert(entryAt(.96,height,false,kind).opacity>0);
 assert.equal(entryAt(.70,height,false,kind).move,1,'the main layout still completes at 700 ms');
}
for(const [time,expectedY,expectedOpen,expectedGlow] of [[1.90,.18*.03,1,1],[2.20,.18*.03,1,1],[3.50,0,1,1-smooth(.80/1.10)],[3.80,0,.5,0],[4.10,0,0,0]]){
 const state=entryAt(time,.18);close(state.y,expectedY);close(state.open,expectedOpen);close(state.glow,expectedGlow);assert.equal(state.opacity,1);
}
checks.push('An explicit 100 ms delay and 800 ms eased prelight reach 15.625%, 50%, 84.375% and 100% glow while either body stays hidden through 950 ms; the main layout still completes at 700 ms');

const maxStep={glow:0,opacity:0,open:0,y:0};
for(const fps of [30,60,120]){
 let previous=null,visibilityChanges=0;
 for(let frame=0;frame<=Math.ceil(DURATION*fps);frame++){
  const time=Math.min(frame/fps,DURATION),state=entryAt(time,.18);
  finiteState(state);assert.equal(state.gathered,0);
  if(time<=3.5)assert.equal(state.open,1,'open from hidden initialization through ground landing');
  if(state.open<1)assert.equal(state.y,0,'no relaxation before landing');
  if(previous){
   assert(state.opacity>=previous.opacity,'entrance alpha never reverses');
   assert(state.open<=previous.open,'pose only relaxes once');
   if(state.visible!==previous.visible)visibilityChanges++;
   for(const key of Object.keys(maxStep))maxStep[key]=Math.max(maxStep[key],Math.abs(state[key]-previous[key]));
   assert(Math.abs(state.glow-previous.glow)<=1.876/fps);
   if(time<=.95){assert.equal(state.opacity,0);assert.equal(state.y,0);assert.equal(state.visible,false);}
   assert(Math.abs(state.opacity-previous.opacity)<=2.51/fps);
   assert(Math.abs(state.open-previous.open)<=2.51/fps);
   assert(Math.abs(state.y-previous.y)<=.0086/fps);
  }
  if(fps===120)frameEvidence.push({sequence:'fresh-120hz',time,...scalarState(state),visible:state.visible});
  previous=state;
 }
 assert.equal(visibilityChanges,1);
}
for(const boundary of [0,.10,.70,.90,.95,1.55,1.90,1.95,2.20,2.70,3.35,3.50,3.80,DURATION]){
 const a=entryAt(boundary-1e-6,.18),b=entryAt(boundary+1e-6,.18);
 for(const key of numericKeys)assert(Math.abs(a[key]-b[key])<1e-5,`${key} jumps at ${boundary}`);
}
checks.push('30/60/120 Hz entrance is continuous: open before visibility, open through rise and full landing, then one smooth finger relaxation; opacity never reverses');

for(let frame=-1;frame<=Math.ceil(DURATION*120)+1;frame++){
 const time=frame/120;
 assert.deepEqual(entryAt(time,1.8,false,'human'),humanBaseline(time,1.8));
 assert.deepEqual(entryAt(time,1.8,true,'human'),humanBaseline(time,1.8,true));
 // Compare the old articulation formula at the same age after appearance,
 // independently of the changed shared prelight and layout timing.
 const previousTime=Math.max(0,Math.min(3.8,time-.30)),state=entryAt(time,1.8,false,'human');
 close(state.open,1-smooth((previousTime-1.65)/1.40));
 close(state.y,1.8*.03*smooth((previousTime-.65)/.95)*(1-smooth((previousTime-1.90)/1.30)));
 close(state.opacity,smooth((previousTime-.65)/.60));
}
checks.push('Human uses the same delayed prelight while preserving its prior articulation, rise, landing and reveal exactly 300 ms later; phases and reduced-motion endpoints match the independent expected formula');

for(const startTime of [0,.5,.95,.96,1.1,1.55,1.9,2.2,2.8,3.5,3.8,4.1]){
 const start=entryAt(startTime,.18);samePose(exitAt(0,.18,start),start);
 let previous=start;
 for(let frame=0;frame<=132;frame++){
  const state=exitAt(frame/120,.18,start);finiteState(state);
  assert(state.opacity<=previous.opacity);assert(state.y<=previous.y);
  close(state.open,start.open);assert.equal(state.gathered,0);
  if(previous.opacity>0&&state.opacity>0)assert(Math.abs(state.opacity-previous.opacity)<=.014);
  previous=state;
 }
 assert.equal(previous.opacity,0);assert.equal(previous.y,0);
}
checks.push('Exits interrupted at twelve entry stages preserve the presented morph, fade monotonically and land without negative-Y slicing');

let now=0,nextFrame=0,reduced=false;
const callbacks=new Map();
Object.defineProperty(globalThis,'performance',{value:{now:()=>now},configurable:true});
globalThis.matchMedia=()=>({matches:reduced});
globalThis.requestAnimationFrame=callback=>{callbacks.set(++nextFrame,callback);return nextFrame;};
globalThis.cancelAnimationFrame=id=>callbacks.delete(id);
const parse=async kind=>{
 const path=kind==='hand'?'hand-18cm-technical.glb':'human-180cm.glb';
 const bytes=await readFile(new URL('../../public/gallery/scale-reference/'+path,import.meta.url));
 return new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
};
const gltf=await parse('hand'),hand=new ScaleCompanion(gltf.scene,'hand');
const handMaterialModes=captureMaterialModes(hand);
hand.setDisplayScale(7.25);hand.root.position.set(1.2,0,-.3);
const rootQ=hand.root.quaternion.clone(),bodyQ=hand.body.quaternion.clone(),scale=hand.root.scale.clone(),rootPosition=hand.root.position.clone(),bodyPosition=hand.body.position.clone();
const renderer=Object.create(PreviewRenderer.prototype);
Object.assign(renderer,{companion:hand,comparison:true,referenceFrame:0,referenceAnimation:null,referenceToken:0,stats:{}});
let label='initial',draws=0,minimumWorldY=Infinity;
const samples=[];
renderer.draw=()=>{
 draws++;const state=hand.state;finiteState(state);
 assert(hand.root.quaternion.equals(rootQ));assert(hand.body.quaternion.equals(bodyQ));assert(hand.root.scale.equals(scale));
 assert(hand.root.position.equals(rootPosition),'the reference root must stay fixed above the same ground');
 close(hand.body.position.x,bodyPosition.x);close(hand.body.position.z,bodyPosition.z);close(hand.body.position.y,state.y);assert(hand.body.position.y>=0);
 assert.equal(hand.body.visible,state.opacity>0);
 assertMaterialModes(hand,handMaterialModes);
 for(const {object,openIndex,gatheredIndex} of hand.morphs){close(object.morphTargetInfluences[openIndex],state.open);close(object.morphTargetInfluences[gatheredIndex],0);}
 hand.root.updateMatrixWorld(true);const minY=new THREE.Box3().setFromObject(hand.body,true).min.y;
 minimumWorldY=Math.min(minimumWorldY,minY);assert(minY>=-1e-7,'all actual-mesh frames stay grounded or above ground');
 for(const {material,opacity} of hand.materials)close(material.opacity,opacity,1e-7);
 const sample={sequence:label,time:now/1000,...scalarState(state),visible:hand.body.visible,minWorldY:minY};
 samples.push(sample);frameEvidence.push(sample);
};
const step=milliseconds=>{
 now+=milliseconds;const pending=[...callbacks.values()];callbacks.clear();
 for(const callback of pending)callback(now);
 assert(callbacks.size<=1,'at most one reference callback can own the animation');
};
const run=milliseconds=>{const end=now+milliseconds;while(now<end)step(Math.min(1000/60,end-now));};
const begin=(enter,name)=>{
 label=name;renderer.comparison=enter;const before={...hand.state};renderer.animateReference(enter);
 samePose(hand.state,before);assert.equal(callbacks.size,1);return before;
};
const assertMonotonic=(items,key,direction)=>{for(let i=1;i<items.length;i++)assert((items[i][key]-items[i-1][key])*direction>=-1e-9,`${items[i].sequence} ${key} reverses`);};
const assertContinuity=items=>{
 for(let i=1;i<items.length;i++){
  const previous=items[i-1],state=items[i];
  if(previous.opacity>0&&state.opacity>0){assert(Math.abs(state.opacity-previous.opacity)<.15,'visible alpha step is bounded');assert(Math.abs(state.open-previous.open)<.15,'visible morph step is bounded');}
 }
};

for(let cycle=0;cycle<3;cycle++){
 let start=samples.length;begin(true,`complete-entry-${cycle}`);
 assert.equal(renderer.referenceAnimation.duration,4100,'the production renderer must adopt the longer entry duration');
 run(3900);assert(hand.state.open>0,'finger relaxation is still in progress after the old completion time');assert.equal(hand.state.y,0);assert.equal(callbacks.size,1);assert(renderer.referenceAnimation);
 run(DURATION*1000+100-3900);let frames=samples.slice(start);
 assertMonotonic(frames,'opacity',1);assertContinuity(frames);samePose(hand.state,hand.settled());assert.equal(renderer.referenceFrame,0);
 assert(frames.filter(s=>s.y>1e-12).every(s=>s.open===1));
 start=samples.length;begin(false,`complete-exit-${cycle}`);run(1200);frames=samples.slice(start);assertMonotonic(frames,'opacity',-1);assertContinuity(frames);assert.equal(hand.state.opacity,0);assert.equal(callbacks.size,0);
 sequences.push(`complete entry/exit cycle ${cycle+1}`);
}
checks.push('Three real-renderer full entry/exit cycles preserve opacity, morph synchronization, visibility, fixed orientation, shared scale and actual mesh ground clearance');
checks.push('Body uses prepared transparent depth-writing front faces with a small fixed alpha threshold; visible/custom-depth material modes and shader versions, plus shadow-caster flags, never switch during any sampled frame');

for(const interruptAt of [200,900,960,1100,1550,2200,3600,3900]){
 begin(true,`interrupted-entry-${interruptAt}`);run(interruptAt);
 let from=begin(false,`interrupted-exit-${interruptAt}`);step(0);samePose(hand.state,from);run(140);
 from=begin(true,`resumed-entry-${interruptAt}`);step(0);samePose(hand.state,from);
 const start=samples.length;run(800);const frames=samples.slice(start);assertContinuity([from,...frames]);assertMonotonic(frames,'opacity',1);
 for(const state of frames)if(state.y>1e-12)close(state.open,from.open,1e-9);
 samePose(hand.state,hand.settled());assert.equal(callbacks.size,0);
 begin(false,`cleanup-exit-${interruptAt}`);run(1200);
 sequences.push(`interrupt/re-entry at ${interruptAt} ms`);
}
checks.push('Eight interrupted entry→exit→re-entry flows retain their exact presented first frame and keep fingers unchanged until the hand has landed');

// Deliberately deliver a callback that was dequeued just before cancellation.
// It must not write, clear, or duplicate the newer animation's frame ownership.
begin(true,'stale-entry');const staleEntry=callbacks.get(renderer.referenceFrame);run(1100);
begin(false,'current-exit');const currentFrame=renderer.referenceFrame,currentAnimation=renderer.referenceAnimation,currentState={...hand.state},drawsBefore=draws;
staleEntry(now+16);
assert.equal(draws,drawsBefore);assert.equal(renderer.referenceFrame,currentFrame);assert.equal(renderer.referenceAnimation,currentAnimation);assert.equal(callbacks.size,1);samePose(hand.state,currentState);
run(1200);
begin(true,'stale-before-finish');const staleFinish=callbacks.get(renderer.referenceFrame);run(1200);renderer.finishReference();const settledState={...hand.state},finishDraws=draws;staleFinish(now+16);assert.equal(draws,finishDraws);samePose(hand.state,settledState);assert.equal(callbacks.size,0);assert.equal(renderer.referenceFrame,0);
checks.push('Canceled queued RAF callbacks cannot mutate or duplicate a newer animation, and cannot revive an explicitly finished entrance');

// A draw callback can synchronously start another command. The previous owner
// must not overwrite its frame handle after draw returns.
hand.apply(hand.absent());const ordinaryDraw=renderer.draw;let retargetOnDraw=true;
renderer.draw=()=>{ordinaryDraw();if(retargetOnDraw){retargetOnDraw=false;begin(false,'draw-reentrant-exit');}};
begin(true,'draw-reentrant-entry');step(20);assert.equal(renderer.referenceAnimation.enter,false);assert.equal(callbacks.size,1);run(1200);renderer.draw=ordinaryDraw;
checks.push('A re-entrant command during draw retains the newer animation and exactly one RAF owner');

for(const kind of ['hand','human']){
 const fixture=kind==='hand'?hand:new ScaleCompanion((await parse('human')).scene,'human');
 const modes=kind==='hand'?handMaterialModes:captureMaterialModes(fixture);
 if(kind==='human')for(let frame=0;frame<=Math.ceil(DURATION*60);frame++){fixture.apply(entryAt(frame/60,1.8,false,'human'));assertMaterialModes(fixture,modes);}
 renderer.companion=fixture;renderer.draw=()=>{finiteState(fixture.state);assert.equal(fixture.state.y,0);close(fixture.state.open,0);assert.equal(fixture.body.visible,fixture.state.opacity>0);assertMaterialModes(fixture,modes);};
 fixture.apply(fixture.absent());reduced=true;renderer.comparison=true;renderer.animateReference(true);step(90);close(fixture.state.opacity,.5);reduced=false;step(90);assert.equal(fixture.state.opacity,1);assert.equal(callbacks.size,0);
 reduced=true;renderer.comparison=false;renderer.animateReference(false);step(90);close(fixture.state.opacity,.5);reduced=false;step(90);assert.equal(fixture.state.opacity,0);assert.equal(callbacks.size,0);
 if(kind==='human'){fixture.dispose();for(const depth of modes.depths)assert.equal(depth.disposed,1);}
}
renderer.companion=hand;
checks.push('Hand and human reduced-motion entrance/exit remain grounded and relaxed, including a preference change during their captured 180 ms fade');

// Mid-flight normal→reduced uses the renderer's same finish path as its media listener.
renderer.draw=()=>{};reduced=false;hand.apply(hand.absent());renderer.comparison=true;renderer.animateReference(true);run(1200);reduced=true;renderer.finishReference();samePose(hand.state,hand.settled());assert.equal(callbacks.size,0);
reduced=false;renderer.comparison=false;renderer.animateReference(false);run(200);reduced=true;renderer.finishReference();samePose(hand.state,hand.absent());assert.equal(callbacks.size,0);
checks.push('Normal→reduced completion cancels motion and selects the correct settled or absent endpoint');

reduced=false;renderer.comparison=true;renderer.animateReference(true);const staleRemoved=callbacks.get(renderer.referenceFrame);renderer.removeReference();const beforeRemoval=draws;staleRemoved(now+16);assert.equal(renderer.companion,null);assert.equal(renderer.referenceFrame,0);assert.equal(callbacks.size,0);assert.equal(draws,beforeRemoval);
for(const depth of handMaterialModes.depths)assert.equal(depth.disposed,1);
checks.push('Reference disposal cancels callbacks and releases each custom depth material exactly once; a stale callback cannot reattach or revive a removed mesh');

await mkdir(new URL('./evidence/',import.meta.url),{recursive:true});
const report={status:'passed',timing:ENTRY_TIMING,prelightEvidence,checks,sequenceCount:sequences.length,sequences,frameCount:frameEvidence.length,maxSampleStepAcross30To120Hz:maxStep,minimumWorldY,browserRasterVerified:false,scope:'Production entry/exit formulas, decoded GLB geometry and production renderer animation lifecycle under a deterministic frame queue. No browser or WebGL pixel claim.'};
await writeFile(new URL('./evidence/reference-entry-continuity-report.json',import.meta.url),JSON.stringify(report,null,2));
await writeFile(new URL('./evidence/reference-entry-frame-evidence.json',import.meta.url),JSON.stringify(frameEvidence));
console.log(JSON.stringify(report,null,2));

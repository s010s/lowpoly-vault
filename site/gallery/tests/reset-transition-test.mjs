import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {ViewTransition,interpolateView,shortestAngle} from '../view-transition.js';
import {PreviewRenderer} from '../renderer.js';
import {ScaleCompanion} from '../scale-reference.js';
const checks=[];const check=(name,fn)=>{fn();checks.push(name);};
const close=(a,b,e=1e-8)=>assert(Math.abs(a-b)<e,`${a} != ${b}`);
const deepClose=(a,b)=>a.forEach((value,i)=>close(value,b[i]));
const orbit=(theta,phi=1.1,r=6)=>new THREE.Vector3().setFromSpherical(new THREE.Spherical(r,phi,theta)).toArray();
const origin={position:orbit(179*Math.PI/180),target:[0,0,0],zoom:2,modelPosition:[0,0,0],modelQuaternion:new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0),350*Math.PI/180).toArray()};
const goal={position:orbit(-179*Math.PI/180,.9,12),target:[0,1,0],zoom:1,modelPosition:[-2,0,0],modelQuaternion:[0,0,0,1]};
check('shortest angle across ±180°',()=>close(shortestAngle(179*Math.PI/180,-179*Math.PI/180),2*Math.PI/180));
check('shortest model quaternion path',()=>{const mid=interpolateView(origin,goal,.5);assert(new THREE.Quaternion().fromArray(mid.modelQuaternion).angleTo(new THREE.Quaternion())<.09);});
check('orbit radius stays positive and finite',()=>{for(let i=0;i<=100;i++){const s=interpolateView(origin,goal,i/100);const r=new THREE.Vector3().fromArray(s.position).distanceTo(new THREE.Vector3().fromArray(s.target));assert(r>5.9&&r<13);}});
let time=0,next=0,frames=new Map(),value=structuredClone(origin),motionReduced=false;
const request=fn=>{frames.set(++next,fn);return next;};const cancel=id=>frames.delete(id);
const advance=t=>{time=t;const list=[...frames.values()];frames.clear();list.forEach(fn=>fn(t));};
const transition=new ViewTransition({read:()=>structuredClone(value),write:s=>value=structuredClone(s),clock:()=>time,request,cancel,reduced:()=>motionReduced});
check('Reset begins at current rendered pose, no first-frame teleport',()=>{transition.start(goal);assert.deepEqual(value,origin);assert.equal(frames.size,1);});
check('camera reset and model-left movement run together',()=>{advance(350);assert(value.modelPosition[0]<-.9);assert.notDeepEqual(value.position,origin.position);assert.notDeepEqual(value.position,goal.position);});
check('repeated Reset retargets exact current frame',()=>{const before=structuredClone(value);transition.start(origin);assert.deepEqual(value,before);advance(700);assert(value.modelPosition[0]>before.modelPosition[0]);});
check('drag/zoom interrupts camera only; layout still settles',()=>{transition.interruptCamera();value.position=[9,8,7];value.target=[1,2,3];value.zoom=3;advance(1050);assert.deepEqual(value.position,[9,8,7]);assert.deepEqual(value.target,[1,2,3]);assert.equal(value.zoom,3);deepClose(value.modelPosition,origin.modelPosition);assert.equal(frames.size,0);});
check('new comparison/reset can regain camera ownership',()=>{transition.start(goal);advance(1750);assert.deepEqual(value.position,goal.position);assert.deepEqual(value.target,goal.target);assert.equal(value.zoom,1);assert.equal(frames.size,0);});
check('asset switch cancellation prevents old callback writes',()=>{transition.start(origin);const before=structuredClone(value);transition.cancelAll();advance(2000);assert.deepEqual(value,before);assert.equal(frames.size,0);});
check('reduced motion performs one settled state without spatial loop',()=>{motionReduced=true;transition.start(origin);assert.deepEqual(value.position,origin.position);assert.equal(frames.size,0);motionReduced=false;});
check('changing preference mid-flight settles the intended destination',()=>{transition.start(goal);advance(2200);transition.finish();assert.deepEqual(value.position,goal.position);assert.equal(frames.size,0);});

const root=new URL('../../',import.meta.url);const dist=new URL('../../../',import.meta.url).pathname;
const models=JSON.parse(await readFile(new URL('../../../assets/manifest.json',import.meta.url),'utf8')).assets;
const parse=async path=>{const bytes=await readFile(path);// This suite checks geometry/matrices only. The separate mandatory browser parser decodes real textures.
return new GLTFLoader().register(()=>({name:'GeometryOnlyTextureFixture',loadTexture:()=>Promise.resolve(new THREE.Texture())})).parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');};
globalThis.matchMedia=()=>({matches:false});globalThis.document={baseURI:'http://localhost/'};
const refs={};for(const kind of ['hand','human'])refs[kind]=(await parse(new URL('../../public/gallery/scale-reference/'+(kind==='hand'?'hand-18cm-technical.glb':'human-180cm.glb'),import.meta.url))).scene;
const results=[];
for(const asset of models){
 const gltf=await parse(dist+asset.glb),box=new THREE.Box3().setFromObject(gltf.scene),size=box.getSize(new THREE.Vector3());
 const p=Object.create(PreviewRenderer.prototype);p.stats={};p.draw=()=>{};p.detail={scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera(38,1,.01,100),contact:new THREE.Object3D(),target:new THREE.Vector3()};
 p.attach(p.detail,asset,{root:gltf.scene,box,size});p.controls={target:p.detail.target.clone(),update(){}};
 const kind=Math.max(...size.toArray())<.6?'hand':'human',companion=new ScaleCompanion(refs[kind].clone(true),kind);
 const initialScale=p.detail.model.scale.toArray(),authoredMatrix=gltf.scene.matrix.clone(),destination=p.comparisonLayout(companion);p.detail.scene.add(companion.root);companion.apply(companion.settled());p.applyState(destination);
 assert.deepEqual(p.detail.model.scale.toArray(),initialScale);assert.deepEqual(companion.root.scale.toArray(),initialScale);assert(gltf.scene.matrix.equals(authoredMatrix));
 // Fit both complete real GLB envelopes in every actual tested viewport.
 let worst=0;
 for(const [width,height] of [[1440,900],[700,700],[390,640],[2048,1175]]){
  p.resizeCamera(p.detail,width,height);p.detail.camera.updateMatrixWorld(true);p.detail.scene.updateMatrixWorld(true);
  for(const mesh of [p.detail.model,companion.body]){
   const bounds=new THREE.Box3().setFromObject(mesh);
   for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){
    const projected=new THREE.Vector3(x,y,z).project(p.detail.camera);worst=Math.max(worst,Math.abs(projected.x),Math.abs(projected.y));assert(Math.abs(projected.x)<=1&&Math.abs(projected.y)<=1,asset.id+' comparison clipped');
   }
  }
 }
 const left=new THREE.Vector3().fromArray(destination.modelPosition).dot(new THREE.Vector3(Math.cos(42*Math.PI/180),0,-Math.sin(42*Math.PI/180)));assert(left<0);
 results.push({id:asset.id,kind,commonScale:p.detail.scale,referenceMeters:companion.height,worstNDC:worst,dimensionsMeters:size.toArray()});
}
checks.push('all published actual GLBs retain dimensions and share exactly the reference scalar');checks.push('all published paired baseline frames fit at 4 viewport sizes');
await mkdir(new URL('./evidence/',import.meta.url),{recursive:true});
await writeFile(new URL('./evidence/reset-test-report.json',import.meta.url),JSON.stringify({checks,models:results,browserCoverage:false},null,2));
console.log(JSON.stringify({passed:checks.length,models:models.length,viewports:4,checks},null,2));

// Exercise the actual renderer's asynchronous compare/reset/select lifecycle.
let fakeNow=0,rafId=0,rafCallbacks=new Map(),writes=0;
Object.defineProperty(globalThis,'performance',{value:{now:()=>fakeNow},configurable:true});
globalThis.requestAnimationFrame=callback=>{rafCallbacks.set(++rafId,callback);return rafId;};
globalThis.cancelAnimationFrame=id=>rafCallbacks.delete(id);
const step=milliseconds=>{fakeNow+=milliseconds;const callbacks=[...rafCallbacks.values()];rafCallbacks.clear();for(const callback of callbacks)callback(fakeNow);};
const fixtureEntries=new Map();
for(const id of ['calceola','cycad']){const asset=models.find(a=>a.id===id);const gltf=await parse(dist+asset.glb);const box=new THREE.Box3().setFromObject(gltf.scene);fixtureEntries.set(id,{root:gltf.scene,box,size:box.getSize(new THREE.Vector3())});}
const renderer=Object.create(PreviewRenderer.prototype);renderer.stats={stale:0,aborted:0};renderer.token=0;renderer.referenceToken=0;renderer.draw=()=>{writes++;if(renderer.detail?.model)renderer.acknowledgeDetailFrame();};renderer.host={getBoundingClientRect:()=>({left:0,top:0,right:600,bottom:600,width:600,height:600})};renderer.visible=true;globalThis.innerWidth=1200;globalThis.innerHeight=800;renderer.stopHover=()=>{};renderer.trim=()=>{};renderer.resource=async asset=>fixtureEntries.get(asset.id);
const selectRendered=async(...args)=>{const promise=renderer.select(...args);await new Promise(resolve=>setImmediate(resolve));step(16);step(16);return promise;};
renderer.detail={scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera(38,1,.01,100),contact:new THREE.Object3D(),target:new THREE.Vector3()};renderer.controls={target:new THREE.Vector3(),update(){}};
renderer.viewMotion=new ViewTransition({read:()=>renderer.viewState(),write:(state,ownership)=>renderer.applyState(state,ownership),reduced:()=>false});
renderer.attach(renderer.detail,models.find(a=>a.id==='calceola'),fixtureEntries.get('calceola'));renderer.controls.target.copy(renderer.detail.target);
let fetchCount=0;globalThis.fetch=async(url,{signal}={})=>{fetchCount++;const bytes=await readFile(new URL('../../public/'+new URL(url).pathname.slice(1),import.meta.url));signal?.throwIfAborted();return {ok:true,arrayBuffer:async()=>bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength)};};
renderer.rotate(137,11);renderer.zoom(.74);const inspected=renderer.viewState();
assert.equal(renderer.compare(true).meters,.18);await renderer.referenceReady;assert.deepEqual(renderer.viewState().position,inspected.position);step(350);assert(renderer.detail.model.position.length()>0);assert.notDeepEqual(renderer.viewState().position,inspected.position);step(350);deepClose(renderer.viewState().position,renderer.comparisonState.position);checks.push('real renderer comparison starts from inspected pose and jointly returns baseline/moves left');
step(1000);const visibleBefore={...renderer.companion.state};renderer.reset();assert.equal(renderer.comparison,false);assert.deepEqual(renderer.companion.state,visibleBefore);step(200);const leavingOpacity=renderer.companion.state.opacity;renderer.compare(true);assert.equal(renderer.companion.state.opacity,leavingOpacity);assert.equal(fetchCount,1);step(700);assert.equal(renderer.companion.state.opacity,1);checks.push('toggle-off/on interruption preserves presented reference opacity and reuses one decoded reference');
renderer.reset();step(1100);assert.equal(renderer.companion.state.opacity,0);deepClose(renderer.detail.model.position.toArray(),[0,0,0]);deepClose(renderer.viewState().position,renderer.singleState().position);checks.push('standalone Reset and toggle-off end at identical baseline with zero model displacement');
renderer.compare(true);step(350);renderer.zoom(.7);const manualZoom=renderer.viewState().zoom;step(350);deepClose(renderer.viewState().position,renderer.comparisonState.position);close(renderer.viewState().zoom,manualZoom);close(renderer.controls.target.y,0);checks.push('comparison zoom stays user-owned while ground framing and main-model placement finish');
await selectRendered(models.find(a=>a.id==='cycad'));assert.equal(renderer.companion,null);assert.equal(renderer.referenceFrame,0);assert.equal(renderer.cameraFrame,0);assert.equal(renderer.comparison,false);assert.equal(rafCallbacks.size,0);deepClose(renderer.detail.contact.position.toArray(),[0,0,0]);checks.push('actual asset selection cancels camera, reference animation and shifted contact shadow');
renderer.compare(true);const pending=renderer.referenceReady;renderer.reset();await pending;assert.equal(renderer.companion,null);assert.equal(renderer.comparison,false);step(700);assert.equal(rafCallbacks.size,0);checks.push('Reset during reference fetch aborts safely without stale attachment');
renderer.compare(true);await renderer.referenceReady;assert.equal(renderer.companion.height,1.8);assert.equal(renderer.companion.root.scale.x,renderer.detail.model.scale.x);renderer.suspend();assert.equal(renderer.companion,null);assert.equal(renderer.detail.model,null);assert.equal(rafCallbacks.size,0);checks.push('human calibration is 1.8 m; suspend cancels both motion owners and disposes reference');
const report={checks,models:results,browserCoverage:false};await writeFile(new URL('./evidence/reset-test-report.json',import.meta.url),JSON.stringify(report,null,2));console.log('PASS actual renderer lifecycle: '+checks.length+' total assertions groups.');
await selectRendered(models.find(a=>a.id==='calceola'));
let releaseFetch;const normalFetch=globalThis.fetch;
globalThis.fetch=(url,options)=>new Promise(resolve=>{releaseFetch=()=>normalFetch(url,options).then(resolve);});
renderer.compare(true);renderer.rotate(55,8);renderer.zoom(.8);const duringLoad=renderer.viewState();
await releaseFetch();await renderer.referenceReady;step(700);close(renderer.viewState().zoom,duringLoad.zoom);close(renderer.viewState().modelYaw,duringLoad.modelYaw);close(renderer.controls.target.y,0);assert(renderer.detail.orientation.quaternion.angleTo(new THREE.Quaternion())<1e-7);assert(renderer.detail.model.position.length()>0);checks.push('cold-reference input retains yaw/zoom while required ground framing and old tilt reset complete');
renderer.suspend();globalThis.fetch=normalFetch;
await writeFile(new URL('./evidence/reset-test-report.json',import.meta.url),JSON.stringify({checks,models:results,browserCoverage:false},null,2));console.log('PASS pending-load camera ownership: '+checks.length+' total check groups.');
let mediaReduced=true;globalThis.matchMedia=()=>({matches:mediaReduced});renderer.viewMotion.reduced=()=>mediaReduced;
await selectRendered(models.find(a=>a.id==='calceola'));
globalThis.fetch=(url,options)=>new Promise(resolve=>{releaseFetch=()=>normalFetch(url,options).then(resolve);});
renderer.compare(true);renderer.rotate(30,7);renderer.zoom(.75);const reducedPending=renderer.viewState();
await releaseFetch();await renderer.referenceReady;close(renderer.viewState().zoom,reducedPending.zoom);close(renderer.viewState().modelYaw,reducedPending.modelYaw);close(renderer.controls.target.y,0);assert(renderer.detail.model.position.length()>0);assert.equal(renderer.cameraFrame,0);checks.push('cold-load ownership also survives synchronous reduced-motion completion');
step(90);assert(renderer.companion.state.opacity>.4&&renderer.companion.state.opacity<.6);mediaReduced=false;step(90);assert.equal(renderer.companion.state.opacity,1);assert.equal(renderer.referenceFrame,0);checks.push('reduce-to-normal preference change completes the started entrance fade');
mediaReduced=true;renderer.reset();step(90);assert(renderer.companion.state.opacity>.4&&renderer.companion.state.opacity<.6);mediaReduced=false;step(90);assert.equal(renderer.companion.state.opacity,0);assert.equal(renderer.referenceFrame,0);checks.push('reduce-to-normal preference change completes the started withdrawal fade');
renderer.suspend();globalThis.fetch=normalFetch;
await writeFile(new URL('./evidence/reset-test-report.json',import.meta.url),JSON.stringify({checks,models:results,browserCoverage:false},null,2));console.log('PASS dynamic preference and pending ownership: '+checks.length+' total check groups.');
mediaReduced=false;await selectRendered(models.find(a=>a.id==='calceola'));renderer.compare(true);await renderer.referenceReady;step(4000);renderer.zoom(8);const farCompare=renderer.viewState().distance,wideZoom=renderer.viewState().zoom;close(wideZoom,.125);renderer.reset();renderer.zoom(.999);close(renderer.viewState().distance,farCompare*.999);step(700);close(renderer.viewState().zoom,wideZoom);checks.push('ordinary zoom during return releases the projection reset too, without a size snap');renderer.suspend();
await writeFile(new URL('./evidence/reset-test-report.json',import.meta.url),JSON.stringify({checks,models:results,browserCoverage:false},null,2));console.log('PASS transition-safe zoom bounds: '+checks.length+' total check groups.');

// V4: inspection belongs to the main pivot, never the reference or camera orbit.
mediaReduced=false;await selectRendered(models.find(a=>a.id==='calceola'),{preserve:false});
const identity=new THREE.Quaternion(),canonical=renderer.detail.camera.quaternion.clone();
const angle=(a,b)=>new THREE.Quaternion().fromArray(a).angleTo(new THREE.Quaternion().fromArray(b));
const grounded=()=>close(new THREE.Box3().setFromObject(renderer.detail.model,true).min.y,0,1e-7);
renderer.rotate(137,11);renderer.zoom(.74);
assert(renderer.detail.orientation.quaternion.angleTo(identity)>1);assert(renderer.detail.model.quaternion.equals(identity));assert(renderer.detail.camera.quaternion.angleTo(canonical)<1e-7);grounded();
checks.push('user rotation is isolated to main-model inspection pivot; actual mesh remains grounded');
const beforeMain=renderer.detail.orientation.quaternion.clone();renderer.compare(true);await renderer.referenceReady;
const companion=renderer.companion,referenceWorld=companion.body.getWorldQuaternion(new THREE.Quaternion()),referenceCamera=canonical.clone().invert().multiply(referenceWorld);
const unchangedReference=()=>{renderer.detail.scene.updateMatrixWorld(true);const q=companion.body.getWorldQuaternion(new THREE.Quaternion());assert(q.angleTo(referenceWorld)<1e-7);assert(renderer.detail.camera.quaternion.clone().invert().multiply(q).angleTo(referenceCamera)<1e-7);assert(renderer.detail.camera.quaternion.angleTo(canonical)<1e-7);assert(renderer.detail.model.quaternion.equals(identity));grounded();};
step(350);assert(renderer.detail.orientation.quaternion.angleTo(identity)<beforeMain.angleTo(identity));assert(renderer.detail.orientation.quaternion.angleTo(identity)>.01);assert(renderer.detail.model.position.x<0);assert.equal(companion.state.opacity,0);unchangedReference();
step(350);assert(renderer.detail.orientation.quaternion.angleTo(identity)<1e-7);deepClose(renderer.detail.model.position.toArray(),renderer.comparisonState.modelPosition);unchangedReference();
checks.push('main orientation reset and left shift finish together; camera orientation and hidden reference stay fixed');
for(let i=0;i<96;i++){step(1000/30);unchangedReference();}assert.equal(companion.state.opacity,1);
checks.push('all 96 sampled appearance frames preserve world and camera-relative reference orientation');
// Simulate OrbitControls temporary camera orbit as its real change listener consumes it.
renderer.cancelCamera();const radius=renderer.viewState().distance;renderer.detail.camera.position.copy(renderer.controls.target).add(new THREE.Vector3().setFromSpherical(new THREE.Spherical(radius,1.05,1.5)));renderer.detail.camera.lookAt(renderer.controls.target);renderer.consumeMainOrbit();
assert(Math.abs(renderer.detail.comparisonYaw.rotation.y)>.1);assert(renderer.detail.orientation.quaternion.angleTo(identity)<1e-7);unchangedReference();
const liveYaw=renderer.detail.comparisonYaw.rotation.y;renderer.compare(true);step(200);assert(Math.abs(renderer.detail.comparisonYaw.rotation.y-liveYaw)>.01);unchangedReference();
renderer.rotate(18,3);const interruptedYaw=renderer.detail.comparisonYaw.rotation.y;step(700);close(renderer.detail.comparisonYaw.rotation.y,interruptedYaw);unchangedReference();
checks.push('comparison pointer/keyboard orbit changes only base-axis yaw; new drag owns yaw without stranding ground framing');
renderer.reset();const resetFromYaw=renderer.detail.comparisonYaw.rotation.y;assert(Math.abs(resetFromYaw)>.01);step(350);assert(Math.abs(renderer.detail.comparisonYaw.rotation.y)<Math.abs(resetFromYaw));assert(Math.abs(renderer.detail.comparisonYaw.rotation.y)>1e-7);unchangedReference();step(750);close(renderer.detail.comparisonYaw.rotation.y,0);assert(renderer.detail.orientation.quaternion.angleTo(identity)<1e-7);assert.equal(companion.state.opacity,0);unchangedReference();
checks.push('standalone Reset uses same eased main-only recovery while fading a fixed reference');
renderer.suspend();
await writeFile(new URL('./evidence/reset-test-report.json',import.meta.url),JSON.stringify({checks,models:results,browserCoverage:false},null,2));console.log('PASS independent main/reference orientation: '+checks.length+' total check groups.');
await selectRendered(models.find(a=>a.id==='calceola'),{preserve:false});renderer.rotate(90,7);renderer.compare(true);await renderer.referenceReady;step(200);
// A pointer was already held when Compare began: another change has no new start event.
renderer.detail.camera.position.copy(renderer.controls.target).add(new THREE.Vector3().setFromSpherical(new THREE.Spherical(renderer.viewState().distance,1.03,1.44)));renderer.detail.camera.lookAt(renderer.controls.target);renderer.consumeMainOrbit();
assert.equal(renderer.viewMotion.active.yaw,false);assert.equal(renderer.viewMotion.active.orientation,true);const heldYaw=renderer.detail.comparisonYaw.rotation.y;step(700);close(renderer.detail.comparisonYaw.rotation.y,heldYaw);assert(renderer.detail.orientation.quaternion.angleTo(identity)<1e-7);close(renderer.controls.target.y,0);checks.push('held-pointer input owns comparison yaw while old inspection tilt and ground framing still finish');
const view=renderer.detail,originalBackground=new THREE.Color('#c5bdb3');view.scene.background=originalBackground;view.camera.layers.enable(4);const originalMask=view.camera.layers.mask;
const calls=[];renderer.renderer={autoClear:true,render(scene,camera){calls.push({mask:camera.layers.mask,background:scene.background,autoClear:this.autoClear});}};
renderer.renderScenePasses(view);assert.equal(calls.length,2);assert.deepEqual(calls.map(c=>c.mask),[1,2]);assert.equal(calls[0].background,originalBackground);assert.equal(calls[1].background,null);assert(calls.every(c=>c.autoClear===false));assert.equal(view.camera.layers.mask,originalMask);assert.equal(view.scene.background,originalBackground);assert.equal(renderer.renderer.autoClear,true);
renderer.companion.root.traverse(object=>assert.equal(object.layers.mask,2));view.model.traverse(object=>assert.equal(object.layers.mask,1));assert.equal(renderer.companion.shadow.material.depthWrite,false);assert.equal(renderer.companion.contact.material.depthWrite,false);
checks.push('reference uses a separate depth-preserving light pass; original main and reference layers never share a rig');
let renderCount=0;renderer.renderer.render=()=>{if(++renderCount===2)throw new Error('render probe');};assert.throws(()=>renderer.renderScenePasses(view),/render probe/);assert.equal(view.camera.layers.mask,originalMask);assert.equal(view.scene.background,originalBackground);assert.equal(renderer.renderer.autoClear,true);
renderer.renderer.render=()=>renderCount++;renderCount=0;renderer.renderScenePasses({scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera()});assert.equal(renderCount,1);checks.push('render-pass state is restored on failure and hover remains a single unchanged pass');
renderer.suspend();await writeFile(new URL('./evidence/reset-test-report.json',import.meta.url),JSON.stringify({checks,models:results,browserCoverage:false},null,2));console.log('PASS held pointer and isolated lighting: '+checks.length+' total check groups.');
const rotatedFits=[];
for(const asset of models){
 const g=await parse(dist+asset.glb),b=new THREE.Box3().setFromObject(g.scene),p=Object.create(PreviewRenderer.prototype);p.stats={};p.draw=()=>{};
 p.detail={scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera(38,1,.01,100),contact:new THREE.Object3D(),target:new THREE.Vector3()};p.controls={target:new THREE.Vector3(),update(){}};
 p.attach(p.detail,asset,{root:g.scene,box:b,size:b.getSize(new THREE.Vector3())});p.controls.target.copy(p.detail.target);
 let worst=0;for(const [az,el,count] of [[0,5,12],[5,0,24],[-7,-4,12],[137,11,1]]){
  for(let i=0;i<count;i++)p.rotate(az,el);
  close(new THREE.Box3().setFromObject(p.detail.model,true).min.y,0,1e-7);
  for(const [width,height] of [[1440,900],[700,700],[390,640],[2048,1175]]){
   p.resizeCamera(p.detail,width,height);p.detail.scene.updateMatrixWorld(true);p.detail.camera.updateMatrixWorld(true);const point=new THREE.Vector3();
   p.detail.model.traverse(o=>{if(!o.isMesh)return;const position=o.geometry.attributes.position;for(let i=0;i<position.count;i++){point.fromBufferAttribute(position,i).applyMatrix4(o.matrixWorld).project(p.detail.camera);worst=Math.max(worst,Math.abs(point.x),Math.abs(point.y));assert(Math.abs(point.x)<=1&&Math.abs(point.y)<=1,asset.id+' inspected rotation clips');}});
  }
 }
 p.applyState(p.singleState());for(let i=0;i<36;i++)p.rotate(0,5);
 const upsideDown=p.viewState(),baseline=p.singleState();let resetWorst=0;
 for(let i=0;i<=20;i++){
  p.applyState(interpolateView(upsideDown,baseline,i/20),{cameraOwned:true});
  for(const [width,height] of [[1440,900],[700,700],[390,640],[2048,1175]]){
   p.resizeCamera(p.detail,width,height);p.detail.scene.updateMatrixWorld(true);p.detail.camera.updateMatrixWorld(true);const point=new THREE.Vector3();
   p.detail.model.traverse(o=>{if(!o.isMesh)return;const position=o.geometry.attributes.position;for(let k=0;k<position.count;k++){point.fromBufferAttribute(position,k).applyMatrix4(o.matrixWorld).project(p.detail.camera);resetWorst=Math.max(resetWorst,Math.abs(point.x),Math.abs(point.y));assert(Math.abs(point.x)<=1&&Math.abs(point.y)<=1,asset.id+' 180-degree Reset intermediate clips');}});
  }
 }
 rotatedFits.push({id:asset.id,worstNDC:worst,upsideDownResetWorstNDC:resetWorst});
}
checks.push('all published actual meshes remain grounded and fit after repeated yaw/elevation inspection at 4 viewport sizes');
checks.push('all published meshes remain framed through 21 samples of a 180-degree Reset at 4 viewport sizes');
await writeFile(new URL('./evidence/reset-test-report.json',import.meta.url),JSON.stringify({checks,models:results,rotatedFits,browserCoverage:false},null,2));console.log('PASS actual rotated framing: '+checks.length+' total check groups.');

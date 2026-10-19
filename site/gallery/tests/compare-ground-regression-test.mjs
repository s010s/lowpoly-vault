import assert from 'node:assert/strict';
import {writeFile} from 'node:fs/promises';
import * as THREE from 'three';
import {ViewTransition} from '../view-transition.js';
const {fixture,compare,sample,drag,pointer,step,models,report,source}=await import('./compare-ground-drift-audit.mjs');
const checks=[];const close=(a,b,message='',eps=1e-7)=>assert(Math.abs(a-b)<=eps,`${message}: ${a} != ${b}`);
const arrays=(a,b,message='')=>a.forEach((v,i)=>close(v,b[i],message+' ['+i+']'));
const cleanup=r=>{r.controls.dispose();r.viewMotion.cancelAll();r.removeReference();};
assert(report.summary.worstReferencePixelDrift<1e-7);
for(const item of report.models){close(item.after.modelMinY,0,item.id+' main grounded');close(item.after.referenceMinY,0,item.id+' reference grounded');arrays(item.before.target,item.after.target,item.id+' camera target');arrays(item.before.position,item.after.position,item.id+' camera position');arrays(item.before.modelPosition,item.after.modelPosition,item.id+' layout');arrays(item.before.modelQuaternion,item.after.modelQuaternion,item.id+' inspection pitch unchanged');arrays(item.after.scale,item.after.referenceScale,item.id+' shared scale');assert(Math.abs(item.after.viewState.modelYaw-item.before.viewState.modelYaw)>.1);}
checks.push('all published actual GLBs: real mouse drag changes base-axis yaw only; both grounded, camera/target/layout/reference screen Y and shared scalar invariant');
for(const item of report.entryInterruptions){close(item.before.target[1],0,'entry settled at ground');close(item.referencePixelsY,0,'entry-interrupted zoom root Y');arrays(item.before.modelQuaternion,[0,0,0,1],'old pitch recovers');}
close(report.pendingReferenceInput.before.target[1],0);close(report.pendingReferenceInput.referencePixelsY,0);arrays(report.pendingReferenceInput.before.modelQuaternion,[0,0,0,1]);
checks.push('Cold reference input and entry interruption at 0/100/350/699 ms finish ground framing and pitch recovery before subsequent anchor-stable zoom');
close(report.summary.pinchDistanceChange,0);assert(report.summary.pinchZoomChange>1);checks.push('Actual two-pointer pinch changes shared projection zoom and keeps physical camera radius fixed');
let yawSamples=0;
for(const asset of models){
 const r=fixture(asset);compare(r);const scalar=r.detail.model.scale.toArray(),authored=r.detail.authoredRoot.position.toArray();
 for(const [width,height] of [[1440,900],[700,700],[390,640],[2048,1175]]){
  r.resizeCamera(r.detail,width,height);const initial=sample(r);const mainY=()=>{r.detail.camera.updateMatrixWorld(true);r.detail.model.updateMatrixWorld(true);return r.detail.comparisonYaw.localToWorld(new THREE.Vector3()).project(r.detail.camera).y;};const anchor=mainY();
  for(let i=0;i<24;i++){r.rotate(15,50);const before=sample(r);r.zoom(i%2?.8:1.25);const after=sample(r);close(before.referenceProjected[1],after.referenceProjected[1],asset.id+' reference zoom');close(mainY(),anchor,asset.id+' main base');close(after.referenceProjected[1],initial.referenceProjected[1],asset.id+' reference yaw');close(after.modelMinY,0,asset.id+' yaw ground');arrays(after.scale,scalar);arrays(after.referenceScale,scalar);arrays(r.detail.authoredRoot.position.toArray(),authored);yawSamples++;}
 }
 cleanup(r);
}
checks.push('A complete 24-step yaw/zoom sweep across all published real GLBs and four viewport sizes keep both ground anchors fixed, meshes grounded and source/model/reference scale unchanged');
const asset=models.find(a=>a.id==='waptia');
const r=fixture(asset);compare(r);const callback=source.match(/detail\.addEventListener\('wheel',event=>\{([\s\S]*?)\},\{passive:false,capture:true\}\);/);assert(callback,'production wheel capture callback must be identifiable');
r.host.addEventListener('wheel',new Function('detail','return event=>{'+callback[1]+'};').call(r,r.host),{passive:false,capture:true});
let before=sample(r);const wheel=r.host.dispatch('wheel',{deltaY:100,deltaMode:0,clientX:300,clientY:300});let after=sample(r);close(after.zoom,before.zoom/Math.exp(.1),'one custom wheel change only');close(after.distance,before.distance);assert(wheel.defaultPrevented);
for(const key of ['ctrlKey','metaKey']){before=sample(r);const event=r.host.dispatch('wheel',{deltaY:100,deltaMode:0,[key]:true,clientX:300,clientY:300});after=sample(r);close(after.zoom,before.zoom,key+' does not also zoom model');assert(!event.defaultPrevented,key+' browser default retained');}
checks.push('Actual production wheel capture callback prevents native double zoom and preserves ctrl/meta browser-default behavior');
// Repeated Compare must regain independently interrupted yaw and projection zoom.
r.applyState(r.comparisonState);r.compare(true);step(150);r.rotate(37,0);r.zoom(.6);const manual=sample(r);r.compare(true);step(700);close(r.detail.comparisonYaw.rotation.y,0,'Repeated Compare reclaims yaw');close(r.detail.camera.zoom,1,'Repeated Compare reclaims projection zoom');assert(Math.abs(manual.viewState.modelYaw)>.1);checks.push('Repeated Compare after mid-entry yaw/zoom retargets and resets both interrupted ownership channels');
// During withdrawal, ordinary inspection/zoom freezes recovery at user input.
r.rotate(60,0);r.zoom(.5);r.reset();step(210);r.zoom(.8);const interrupted=sample(r);step(900);const ended=sample(r);arrays(interrupted.position,ended.position,'exit user distance');close(interrupted.zoom,ended.zoom,'exit user projection');drag(r);assert(r.detail.orientation.quaternion.angleTo(new THREE.Quaternion())>.1);close(sample(r).modelMinY,0);checks.push('Reset interruption gives ordinary distance/projection ownership to user; full pitch inspection remains grounded');cleanup(r);
// Ordinary input after a partial Reset must stay in screen/world inspection axes.
for(const angle of [-90,90,173]){
 const axis=fixture(asset);compare(axis);axis.rotate(angle,0);axis.reset();step(100);
 const combined=()=>axis.detail.comparisonYaw.quaternion.clone().multiply(axis.detail.orientation.quaternion);
 const wanted=axis.orientationForView(42,33.3).multiply(combined());axis.rotate(0,10);close(combined().angleTo(wanted),0,'ordinary keyboard axis after partial Reset');
 const beforePointer=combined();const distance=axis.viewState().distance;axis.detail.camera.position.copy(axis.controls.target).add(new THREE.Vector3().setFromSpherical(new THREE.Spherical(distance,(90-33.3)*Math.PI/180,42*Math.PI/180)));axis.detail.camera.lookAt(axis.controls.target);
 const delta=axis.cameraPose().multiply(axis.detail.camera.quaternion.clone().invert());const pointerWanted=delta.multiply(beforePointer);axis.consumeMainOrbit();close(combined().angleTo(pointerWanted),0,'ordinary pointer axis after partial Reset');cleanup(axis);
}
checks.push('Ordinary keyboard/pointer pitch keeps the intended world axis after interrupted Reset with -90/90/173 degree comparison yaw');
// Native two-touch dolly obeys the same ordinary-mode bounds as wheel/keyboard.
const touch=fixture(asset);let gestureId=100;
const pinch=(renderer,span)=>{const a=gestureId++,b=gestureId++;pointer(renderer,'pointerdown',a,'touch',100,200);pointer(renderer,'pointerdown',b,'touch',200,200);pointer(renderer,'pointermove',b,'touch',100+span,200);pointer(renderer,'pointerup',b,'touch',100+span,200);pointer(renderer,'pointerup',a,'touch',100,200);};
const near=touch.detail.fitDistance*.15,far=touch.detail.fitDistance*8;pinch(touch,1000000);close(touch.viewState().distance,near,'native pinch near bound');pinch(touch,.001);close(touch.viewState().distance,far,'native pinch far bound');
for(let i=0;i<6;i++){pinch(touch,i%2?1000000:.001);assert(touch.viewState().distance>=near-1e-7&&touch.viewState().distance<=far+1e-7);close(sample(touch).modelMinY,0,'ordinary pinch stays grounded');}
cleanup(touch);checks.push('Actual ordinary two-touch pinch respects .15× to 8× fit-distance limits across repeated extreme gestures');
const limited=fixture(asset);compare(limited);const limitBase=sample(limited);pinch(limited,1000000);close(limited.detail.camera.zoom,1/.15,'comparison zoom max');pinch(limited,.001);close(limited.detail.camera.zoom,.125,'comparison zoom min');const limitAfter=sample(limited);close(limitAfter.distance,limitBase.distance);close(limitAfter.referenceProjected[1],limitBase.referenceProjected[1]);cleanup(limited);checks.push('Extreme comparison pinch is projection-clamped, leaves physical distance unchanged, and preserves the reference ground line');
// ViewTransition retains user-controlled yaw/zoom when reduced motion completes.
let state={position:[0,2,5],target:[0,0,0],zoom:1,screenShift:0,screenShiftY:-.2,modelPosition:[0,0,0],modelQuaternion:[0,0,0,1],modelYaw:0};
const v=new ViewTransition({read:()=>structuredClone(state),write:s=>state=structuredClone(s),request:()=>1,cancel(){},clock:()=>0});v.start({...state,position:[0,3,7]});v.interruptComparisonInput();v.interruptZoom();state.modelYaw=.7;state.zoom=2;v.finish();close(state.modelYaw,.7);close(state.zoom,2);arrays(state.position,[0,3,7]);checks.push('Finishing a reduced-motion transition completes required framing without overwriting user yaw/zoom');
const result={status:'passed',scope:'Deterministic production renderer, real Three.js OrbitControls and real GLB geometry; geometry-only texture placeholders; browser parser remains authoritative for texture decoding; no browser/raster coverage',checks,yawZoomSteps:yawSamples,worstReferencePixelDrift:report.summary.worstReferencePixelDrift};await writeFile(new URL('./evidence/compare-ground/regression-report.json',import.meta.url),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));

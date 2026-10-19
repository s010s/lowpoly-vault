import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {PreviewRenderer} from '../renderer.js';
import {ViewTransition,interpolateView} from '../view-transition.js';
import {publishedModels,assetURL,geometryOnlyLoader} from './geometry-fixtures.mjs';
const models=await publishedModels();
const sizes=[[1032,838],[694,706],[700,700],[390,640],[2048,1175]],results=[];
globalThis.matchMedia=()=>({matches:false});
let totalVertices=0,maxPixelError=0;
for(const asset of models){
 const bytes=await readFile(assetURL(asset.glb)),gltf=await geometryOnlyLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
 const box=new THREE.Box3().setFromObject(gltf.scene),size=box.getSize(new THREE.Vector3());
 const p=Object.create(PreviewRenderer.prototype);p.stats={};p.draw=()=>{};p.detail={scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera(38,1,.01,100),contact:new THREE.Object3D(),target:new THREE.Vector3()};p.controls={target:new THREE.Vector3(),update(){}};
 p.attach(p.detail,asset,{root:gltf.scene,box,size,sha256:createHash('sha256').update(bytes).digest('hex')});
 // The existing posters are canonical 512px square renders, object-fit:contain.
 const poster=p.detail.camera.clone();p.resizeCamera({camera:poster},512,512);poster.clearViewOffset();poster.updateMatrixWorld(true);
 p.applyState(p.singleState());p.detail.scene.updateMatrixWorld(true);let error=0,vertices=0;
 for(const [width,height] of sizes){
  p.resizeCamera(p.detail,width,height);p.detail.camera.updateMatrixWorld(true);
  const shorter=Math.min(width,height),world=new THREE.Vector3(),actual=new THREE.Vector3(),canonical=new THREE.Vector3();
  p.detail.model.traverse(mesh=>{if(!mesh.isMesh)return;const points=mesh.geometry.attributes.position;for(let i=0;i<points.count;i++){
   world.fromBufferAttribute(points,i).applyMatrix4(mesh.matrixWorld);actual.copy(world).project(p.detail.camera);canonical.copy(world).project(poster);
   const actualX=(actual.x+1)*width/2,actualY=(1-actual.y)*height/2;
   const expectedX=width/2+canonical.x*shorter/2-.06*shorter,expectedY=height/2-canonical.y*shorter/2;
   const delta=Math.hypot(actualX-expectedX,actualY-expectedY);assert(delta<1e-7,asset.id+' pixel alignment at '+width+'x'+height+': '+delta);error=Math.max(error,delta);vertices++;
  }});
 }
 totalVertices+=vertices;maxPixelError=Math.max(maxPixelError,error);results.push({id:asset.id,vertices,maxPixelError:error});
}
const baseline={position:[3,2,4],target:[0,1,0],zoom:1,screenShift:.06,modelPosition:[0,0,0],modelQuaternion:[0,0,0,1]};
const compare={...baseline,position:[6,3,8],target:[0,2,0],screenShift:0,modelPosition:[-1,0,0]};
assert.equal(interpolateView(baseline,compare,.5).screenShift,.03);assert.equal(interpolateView(baseline,compare,1).screenShift,0);
let state=structuredClone(baseline),time=0,frame=0;const pending=new Map();
const motion=new ViewTransition({read:()=>structuredClone(state),write:value=>{state=value;},clock:()=>time,request:fn=>{pending.set(++frame,fn);return frame;},cancel:id=>pending.delete(id)});
motion.start(compare);time=350;motion.tick(time);const shift=state.screenShift;motion.interruptInspection();state.zoom=1.7;time=700;motion.tick(time);assert.equal(state.screenShift,shift);assert.equal(state.zoom,1.7);assert.deepEqual(state.modelPosition,compare.modelPosition);
motion.start(baseline);motion.finish();assert.equal(state.screenShift,.06);
const report={status:'passed',browserVerified:false,method:'Actual GLB vertex projection compared to canonical square poster with CSS contain and 6% short-axis translation; geometry-only texture placeholders; browser parser remains authoritative for texture decoding; no raster/browser claim.',models:models.length,viewports:sizes,totalVertices,maxPixelError,transitionChecks:4,results};
await mkdir(new URL('./evidence/',import.meta.url),{recursive:true});await writeFile(new URL('./evidence/poster-projection-report.json',import.meta.url),JSON.stringify(report,null,2));
console.log(`PASS: ${models.length} actual GLBs × ${sizes.length} viewports, ${totalVertices} projected vertices; maximum poster handoff error ${maxPixelError}px. Projection interpolation, input interruption and reset verified.`);

import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {PreviewRenderer} from '../renderer.js';
import {publishedModels,assetURL,geometryOnlyLoader} from './geometry-fixtures.mjs';
const models=await publishedModels();
const approved=JSON.parse(await readFile(new URL('../../public/gallery/approved-resources.json',import.meta.url),'utf8')).posters;
let approvedCameraChecks=0;
const sizes=[[1032,838],[694,706],[700,700],[390,640],[2048,1175]],results=[];
globalThis.matchMedia=()=>({matches:false});
for(const asset of models){
 const bytes=await readFile(assetURL(asset.glb)),gltf=await geometryOnlyLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
 const box=new THREE.Box3().setFromObject(gltf.scene),size=box.getSize(new THREE.Vector3());
 const p=Object.create(PreviewRenderer.prototype);p.stats={};p.draw=()=>{};p.detail={scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera(38,1,.01,100),contact:new THREE.Object3D(),target:new THREE.Vector3()};p.controls={target:new THREE.Vector3(),update(){}};
 p.attach(p.detail,asset,{root:gltf.scene,box,size,sha256:createHash('sha256').update(bytes).digest('hex')});
 if(Object.hasOwn(approved,asset.id)){
  const radius=size.clone().multiplyScalar(p.detail.scale).length()/2,legacyDistance=radius/Math.sin(38*Math.PI/360)*1.08;
  const azimuth=42*Math.PI/180,elevation=23.3*Math.PI/180;
  const direction=new THREE.Vector3(Math.sin(azimuth)*Math.cos(elevation),Math.sin(elevation),Math.cos(azimuth)*Math.cos(elevation));
  assert.deepEqual(p.detail.camera.position.toArray(),p.detail.target.clone().add(direction.multiplyScalar(legacyDistance)).toArray(),asset.id+' approved canonical camera must remain bit-for-bit unchanged');
  assert.equal(p.detail.fitDistance,legacyDistance,asset.id+' approved canonical distance must remain bit-for-bit unchanged');
  approvedCameraChecks++;
 }
 const scale=p.detail.model.scale.clone();p.applyState(p.singleState());let worst=0;
 for(const [width,height] of sizes){
  p.resizeCamera(p.detail,width,height);p.detail.camera.updateMatrixWorld(true);p.detail.scene.updateMatrixWorld(true);
  const center=p.detail.target.clone().project(p.detail.camera),expected=-.12/Math.max(1,width/height);assert(Math.abs(center.x-expected)<1e-7,asset.id+' has an incorrect horizontal baseline');assert(Math.abs(center.y)<1e-7);
  const expectedPixels=Math.min(width,height)*.06;assert(Math.abs(-center.x*width/2-expectedPixels)<1e-5);
  p.detail.model.traverse(mesh=>{if(!mesh.isMesh)return;const points=mesh.geometry.attributes.position,point=new THREE.Vector3();for(let i=0;i<points.count;i++){point.fromBufferAttribute(points,i).applyMatrix4(mesh.matrixWorld).project(p.detail.camera);worst=Math.max(worst,Math.abs(point.x),Math.abs(point.y));assert(Math.abs(point.x)<1&&Math.abs(point.y)<1,asset.id+' clipped at '+width+'x'+height);}});
 }
 assert(p.detail.model.scale.equals(scale));assert(p.detail.orientation.quaternion.equals(new THREE.Quaternion()));assert(Math.abs(p.viewState().cameraAzimuth-42)<1e-7);assert(Math.abs(p.viewState().cameraElevation-23.3)<1e-7);
 results.push({id:asset.id,worstNDC:worst,commonScale:scale.x});
}
await mkdir(new URL('./evidence/',import.meta.url),{recursive:true});
assert.equal(approvedCameraChecks,Object.keys(approved).length);
await writeFile(new URL('./evidence/single-framing-test-report.json',import.meta.url),JSON.stringify({status:'passed',browserVerified:false,scope:'Real geometry with geometry-only texture placeholders; browser parser remains authoritative for texture decoding',models:models.length,approvedCameraChecks,viewports:sizes,leftShift:'6% of the shorter viewport dimension',results},null,2));
console.log('PASS: all '+models.length+' actual GLBs fit the left-shifted single baseline at '+sizes.length+' viewport sizes; 6% short-axis shift, authored scale and camera angles verified.');

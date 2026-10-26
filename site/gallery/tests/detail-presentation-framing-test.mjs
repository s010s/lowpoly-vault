/** Real published geometry, no browser/texture or new approval claim. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import * as THREE from 'three';
import {PreviewRenderer} from '../renderer.js';
import {DetailRenderer} from '../detail-renderer.js';
import {detailPresentationPolicy} from '../detail-presentation-policy.js';
import {publishedModels,assetURL,geometryOnlyLoader} from './geometry-fixtures.mjs';
globalThis.matchMedia=()=>({matches:false});
const resources=JSON.parse(await readFile(new URL('../../public/gallery/resources.json',import.meta.url))),models=await publishedModels();
const sizes=[[1033,838],[570,1138],[390,789],[1920,1080],[320,568]],rows=[];
const build=(Type,asset,entry)=>{const r=Object.create(Type.prototype);r.stats={};r.draw=()=>{};r.detail={scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera(38,1,.01,100),contact:new THREE.Object3D(),target:new THREE.Vector3()};r.controls={target:new THREE.Vector3(),update(){}};r.attach(r.detail,asset,entry);r.applyState(r.singleState());return r;};
const snapshot=r=>({position:r.detail.camera.position.toArray(),quaternion:r.detail.camera.quaternion.toArray(),projection:r.detail.camera.projectionMatrix.toArray(),near:r.detail.camera.near,far:r.detail.camera.far,fit:r.detail.fitDistance,model:r.detail.model.matrixWorld.toArray()});
let ordinary=0,affected=0,wheelUnchanged=0;
for(const asset of models){
 const bytes=await readFile(assetURL(asset.glb)),gltf=await geometryOnlyLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),''),box=new THREE.Box3().setFromObject(gltf.scene),entry={root:gltf.scene,box,size:box.getSize(new THREE.Vector3()),sha256:createHash('sha256').update(bytes).digest('hex')};
 const optIn=['blender-cycles-cpu-v1','blender-detail-preview-wheel-v1'].includes(resources.posters[asset.id]?.render_route),candidate=optIn?{...asset,detailPresentation:detailPresentationPolicy(1536)}:asset;
 const before=build(PreviewRenderer,asset,entry),after=build(DetailRenderer,candidate,entry);let minimum=1;const canonicalFit=after.detail.fitDistance;
 for(const [width,height]of sizes){
  for(const r of [before,after]){r.resizeCamera(r.detail,width,height);r.detail.camera.updateMatrixWorld(true);r.detail.model.updateMatrixWorld(true);}
  if(!optIn)assert.deepEqual(snapshot(after),snapshot(before),asset.id+' ordinary runtime must remain bit-for-bit unchanged');
  else {const point=new THREE.Vector3();after.detail.model.traverse(mesh=>{if(!mesh.isMesh)return;const positions=mesh.geometry.attributes.position;for(let i=0;i<positions.count;i++){point.fromBufferAttribute(positions,i).applyMatrix4(mesh.matrixWorld).project(after.detail.camera);const margin=Math.min((1-Math.abs(point.x))*width,(1-Math.abs(point.y))*height)/(2*Math.min(width,height));minimum=Math.min(minimum,margin);assert(margin>=.025-1e-7,asset.id+' safe short-axis margin');}});}
 }
 // Reuse the actual camera after a portrait draw: its FOV is wider than 38.
 assert(after.detail.camera.fov>38);
 after.attach(after.detail,candidate,entry);after.applyState(after.singleState());
 assert.equal(after.detail.fitDistance,canonicalFit,asset.id+' warm portrait selection must use canonical square fit');
 after.resizeCamera(after.detail,390,789);after.detail.camera.updateMatrixWorld(true);after.detail.model.updateMatrixWorld(true);
 if(optIn){const point=new THREE.Vector3();after.detail.model.traverse(mesh=>{if(!mesh.isMesh)return;const positions=mesh.geometry.attributes.position;for(let i=0;i<positions.count;i++){point.fromBufferAttribute(positions,i).applyMatrix4(mesh.matrixWorld).project(after.detail.camera);assert(Math.min((1-Math.abs(point.x))*390,(1-Math.abs(point.y))*789)/(2*390)>=.025-1e-7,asset.id+' warm safe margin');}});}
 // A flagged asset in a non-detail view must still use the exact old attachment.
 const a=build(PreviewRenderer,asset,entry),b=build(DetailRenderer,asset,entry);
 const av={scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera(38,1,.01,100),contact:new THREE.Object3D(),target:new THREE.Vector3()},bv={scene:new THREE.Scene(),camera:new THREE.PerspectiveCamera(38,1,.01,100),contact:new THREE.Object3D(),target:new THREE.Vector3()};
 a.attach(av,asset,entry);b.attach(bv,candidate,entry);assert.deepEqual(bv.camera.position.toArray(),av.camera.position.toArray());assert.equal(bv.fitDistance,av.fitDistance);wheelUnchanged++;
 optIn?affected++:ordinary++;rows.push({id:asset.id,opt_in:optIn,distance_changed:before.detail.fitDistance!==after.detail.fitDistance,minimum_short_axis_margin:optIn?minimum:null});
}
assert.equal(models.length,602);assert.equal(affected,264);assert.equal(ordinary,338);assert.equal(wheelUnchanged,602);
await mkdir('qa/detail-hires-geometry',{recursive:true});await writeFile('qa/detail-hires-geometry/report.json',JSON.stringify({status:'PASS_GEOMETRY_ONLY',browser:'NOT_RUN',affected,ordinary,wheelUnchanged,viewports:sizes,rows},null,2));
console.log(JSON.stringify({status:'PASS_GEOMETRY_ONLY',affected,ordinary_bit_exact:ordinary,wheel_attach_bit_exact:wheelUnchanged,changed_ids:rows.filter(r=>r.distance_changed).map(r=>r.id)}));

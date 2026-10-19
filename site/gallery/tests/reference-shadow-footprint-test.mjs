import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import * as T from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {ScaleCompanion} from '../scale-reference.js';
import {entryAt} from '../reference-entry.js';
const cases=[];
for(const kind of ['hand','human']){
 const bytes=await readFile(new URL('../../public/gallery/scale-reference/'+(kind==='hand'?'hand-18cm-technical.glb':'human-180cm.glb'),import.meta.url));
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');const companion=new ScaleCompanion(gltf.scene,kind);
 for(const scale of [.25,1,5,10]){
  companion.setDisplayScale(scale);companion.root.position.set(3,0,-1);let oldClipped=0,tested=0,minMargin=Infinity,maximumShadowNdc=0;const footprint=new T.Box3(),headFootprint=new T.Box3();
  for(const time of [0,.95,1.15,1.35,1.9,2.9,3.5,3.8,4.1]){
   companion.apply(entryAt(time,companion.height,false,kind));companion.root.updateMatrixWorld(true);companion.key.shadow.updateMatrices(companion.key);
   const key=new T.Vector3(),target=new T.Vector3(),origin=new T.Vector3();companion.key.getWorldPosition(key);companion.key.target.getWorldPosition(target);companion.root.getWorldPosition(origin);const ray=target.sub(key).normalize(),floor=companion.shadow.getWorldPosition(new T.Vector3()).y;
   companion.body.traverse(mesh=>{if(!mesh.isMesh||mesh.userData.referenceTopology)return;assert(mesh.castShadow);assert(mesh.customDepthMaterial);
    for(let i=0;i<mesh.geometry.attributes.position.count;i++){
     const world=mesh.getVertexPosition(i,new T.Vector3()).applyMatrix4(mesh.matrixWorld),ground=world.clone().addScaledVector(ray,(floor-world.y)/ray.y),relative=ground.clone().sub(origin),extent=companion.height*scale;
     const edge=Math.max(Math.abs(relative.x),Math.abs(relative.z));if(edge>extent*.85+1e-7)oldClipped++;const margin=extent*1.6-edge;assert(margin>=-1e-7,`${kind}scale${scale}time${time} footprint outside receiver`);minMargin=Math.min(minMargin,margin);tested++;
     footprint.expandByPoint(relative.clone().divideScalar(scale));if(world.y-origin.y>extent*.88)headFootprint.expandByPoint(relative.clone().divideScalar(scale));
     const ndc=ground.clone().project(companion.key.shadow.camera);maximumShadowNdc=Math.max(maximumShadowNdc,Math.abs(ndc.x),Math.abs(ndc.y),Math.abs(ndc.z));assert(Math.max(Math.abs(ndc.x),Math.abs(ndc.y),Math.abs(ndc.z))<=1+1e-6,'shadow light frustum clips footprint');
    }
   });
  }
  cases.push({kind,scale,testedVerticesAcrossPoses:tested,oldReceiverClippedVertices:oldClipped,newReceiverMinimumMarginWorld:minMargin,maximumShadowNdc,footprintMeters:{min:footprint.min.toArray(),max:footprint.max.toArray()},upper12PercentFootprintMeters:{min:headFootprint.min.toArray(),max:headFootprint.max.toArray()}});
 }
 companion.dispose();
}
assert(cases.find(c=>c.kind==='human'&&c.scale===1).oldReceiverClippedVertices>0);
const report={status:'passed',cause:'Old receiver 1.7h square clipped projected upper-body/head shadow; light camera frustum contains it. Enlarged reference-only shadow receiver3.2h contains every tested posed body vertex at four common scalars.',browserVerified:false,cases};await writeFile(new URL('./evidence/reference-shadow-footprint-report.json',import.meta.url),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));

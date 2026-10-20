import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import * as THREE from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/build/three.module.js';
import { GLTFLoader } from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import * as validator from '/workspace/shared/lowpoly-landair-web-integration/node_modules/gltf-validator/module.mjs';

if (!globalThis.self) globalThis.self=globalThis;
if (!globalThis.ProgressEvent) globalThis.ProgressEvent=class ProgressEvent extends Event { constructor(type,init={}){ super(type); this.lengthComputable=!!init.lengthComputable; this.loaded=init.loaded||0; this.total=init.total||0; } };
const W='/workspace/shared/lowpoly-batch75-20261020';
const O='/workspace/shared/lowpoly-round30-qa75';
const cases=[
 ['parvancorina','r001','6d121aa830daae492b81ff6a4fd99dd491f74105c0273ecb034a907de2b4fd35'],
 ['glacial-horn','r002','dc476400091e3a9375de913d3684cceb8a8400ea9a4af18228516899bb5ed92b'],
 ['eruptive-fissure','r003','5c01f576cfdb26179b4002bebc0c27997f41e805cf2fb9d9075b022291f83caf'],
 ['banded-gneiss-outcrop','r003','ead8a0740aae860dce43f982ebb9a0ba72800b976a322c37ea18cef17630e638'],
];
const loader=new GLTFLoader();
const result={created_at:new Date().toISOString(),three_version:THREE.REVISION,three_expected:'180',khronos_validator_version:validator.version(),checks:[]};
for (const [id,rev,expected] of cases) {
 const p=path.join(W,'production/continuous-small-life-round30-20261020/work/batch-75/assets',id,rev,'model.glb');
 const bytes=fs.readFileSync(p); const sha=crypto.createHash('sha256').update(bytes).digest('hex');
 const glb=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
 const khronos=await validator.validateBytes(new Uint8Array(bytes),{uri:path.basename(p),format:'glb',writeTimestamp:false,maxIssues:0});
 const loaded=await new Promise((resolve,reject)=>loader.parse(glb,'',resolve,reject));
 const scene=loaded.scene; scene.updateMatrixWorld(true);
 const box=new THREE.Box3().setFromObject(scene);
 const min=box.min.toArray(),max=box.max.toArray(),size=box.getSize(new THREE.Vector3()).toArray();
 let drawPrimitives=0,triangles=0,positionVertices=0,textureCount=0,meshObjects=0,errors=[];
 scene.traverse(o=>{
   if(o.isMesh){meshObjects++; const g=o.geometry; const p=g.getAttribute('position'); if(p) positionVertices+=p.count;
     const mats=Array.isArray(o.material)?o.material:[o.material];
     if(Array.isArray(o.material)) drawPrimitives+=o.material.length; else drawPrimitives++;
     if(g.index) triangles+=g.index.count/3; else if(p) triangles+=p.count/3;
     for(const m of mats){ if(!m) continue; for(const k of ['map','normalMap','roughnessMap','metalnessMap','aoMap','emissiveMap','alphaMap','bumpMap','displacementMap','lightMap']) if(m[k]) textureCount++; }
   }
 });
 const issues=khronos.issues;
 result.checks.push({asset_id:id,revision:rev,path:p,sha256:sha,expected_sha256:expected,hash_match:sha===expected,bytes:bytes.byteLength,three:{version:THREE.REVISION,scene_mesh_objects:meshObjects,primitive_groups:drawPrimitives,triangles,position_vertices:positionVertices,textures:loaded.parser.json.textures?.length||0,materials:loaded.parser.json.materials?.length||0,bounds_min_xyz:min,bounds_max_xyz:max,bounds_size_xyz:size},khronos:{version:validator.version(),numErrors:issues.numErrors,numWarnings:issues.numWarnings,numInfos:issues.numInfos,numHints:issues.numHints,messages:issues.messages,info:khronos.info}});
}
fs.writeFileSync(path.join(O,'fresh-parse.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({three_version:result.three_version,khronos_validator_version:result.khronos_validator_version,assets:result.checks.map(c=>({asset:c.asset_id,revision:c.revision,hash_match:c.hash_match,three:c.three,khronos_errors:c.khronos.numErrors,khronos_warnings:c.khronos.numWarnings}))},null,2));

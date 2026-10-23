// SPDX-License-Identifier: MIT
// Exact delivered GLB parse only. No WebGL/GPU claims.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
const [glb,threeRoot,out]=process.argv.slice(2);
const {GLTFLoader}=await import(pathToFileURL(path.join(threeRoot,'examples/jsm/loaders/GLTFLoader.js')));
const THREE=await import(pathToFileURL(path.join(threeRoot,'build/three.module.js')));
const bytes=fs.readFileSync(glb);
const scene=await new Promise((resolve,reject)=>new GLTFLoader().parse(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'',g=>resolve(g.scene),reject));
scene.updateMatrixWorld(true);
const box=new THREE.Box3().setFromObject(scene);let meshes=0,triangles=0,materials=new Set(),wrongSided=[];
scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;for(const m of (Array.isArray(o.material)?o.material:[o.material])){materials.add(m.uuid);if(m.side!==THREE.FrontSide)wrongSided.push(m.name);}}});
const r={status:wrongSided.length?'fail':'pass',scope:'Three.js GLTFLoader CPU parse; NOT GPU rendering or populated-scene performance',three_version:THREE.REVISION,node_version:process.version,glb_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),mesh_primitives:meshes,triangles,materials:materials.size,bounds_glb_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new THREE.Vector3()).toArray()},unexpected_double_sided:wrongSided,gpu:'NOT_RUN',scene_performance:'NOT_RUN'};
fs.writeFileSync(out,JSON.stringify(r,null,2)+'\n');console.log(JSON.stringify(r));
if(r.status!=='pass')process.exit(1);

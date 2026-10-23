// SPDX-License-Identifier: MIT
// Exact GLTFLoader parse only. No WebGL context or GPU rendering is created.
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto'; import {pathToFileURL} from 'node:url';
const [glb,out,threeRoot]=process.argv.slice(2);
const three=await import(pathToFileURL(path.join(threeRoot,'build/three.module.js')).href);
const {GLTFLoader}=await import(pathToFileURL(path.join(threeRoot,'examples/jsm/loaders/GLTFLoader.js')).href);
const data=fs.readFileSync(glb); const ab=data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength);
const asset=await new Promise((resolve,reject)=>new GLTFLoader().parse(ab,'',resolve,reject));
asset.scene.updateMatrixWorld(true); let meshes=0, triangles=0; const materials=new Set();
asset.scene.traverse(o=>{if(o.isMesh){meshes++; triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3; for(const m of Array.isArray(o.material)?o.material:[o.material]) materials.add(m.uuid);}});
const b=new three.Box3().setFromObject(asset.scene), size=b.getSize(new three.Vector3());
const report={status:'PASS_PARSE_ONLY',claim_scope:'Three.js GLTFLoader parsing, scene traversal and bounds only; GPU and populated scene unrun.',glb_sha256:crypto.createHash('sha256').update(data).digest('hex'),three_version:three.REVISION,node_version:process.version,meshes,triangles,materials:materials.size,bounds_gltf_m:{min:b.min.toArray(),max:b.max.toArray(),size:size.toArray()},gpu:'NOT_RUN',populated_scene:'NOT_RUN'};
fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n'); console.log(JSON.stringify(report));

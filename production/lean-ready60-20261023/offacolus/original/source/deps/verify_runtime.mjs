// SPDX-License-Identifier: MIT
// Node parse/bounds evidence only, explicitly not GPU or populated-scene evidence.
// node verify_runtime.mjs THREE_PACKAGE_DIR MODEL_GLB OUTPUT_JSON
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {pathToFileURL} from 'node:url';
const [pkg,glb,output]=process.argv.slice(2),base=path.resolve(pkg);
const THREE=await import(pathToFileURL(path.join(base,'build/three.module.js')).href);
const {GLTFLoader}=await import(pathToFileURL(path.join(base,'examples/jsm/loaders/GLTFLoader.js')).href);
const bytes=fs.readFileSync(glb),array=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
const doc=await new Promise((resolve,reject)=>new GLTFLoader().parse(array,'',resolve,reject));doc.scene.updateMatrixWorld(true);
const box=new THREE.Box3().setFromObject(doc.scene),meshes=[];
doc.scene.traverse(o=>{if(o.isMesh){const a=o.geometry.attributes.position;for(const v of a.array)if(!Number.isFinite(v))throw Error('Nonfinite position');meshes.push({name:o.name,vertices:a.count,triangles:(o.geometry.index?o.geometry.index.count:a.count)/3,material:o.material.name,side:o.material.side,normals:!!o.geometry.attributes.normal});}});
const result={status:'PASS',claim_scope:'GLTFLoader parse, finite geometry, bounds and material inspection in Node. No browser, GPU, shader, or scene performance claim.',threejs_version:THREE.REVISION,package_version:JSON.parse(fs.readFileSync(path.join(base,'package.json'))).version,glb_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),bounds_gltf_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new THREE.Vector3()).toArray()},meshes,total_triangles:meshes.reduce((s,m)=>s+m.triangles,0),gpu:'NOT_RUN',scene:'NOT_RUN'};
fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));

// SPDX-License-Identifier: MIT
// Read-only Three.js GLTFLoader parsing. Does not claim WebGL/GPU rendering.
import fs from 'node:fs';import crypto from 'node:crypto';import path from 'node:path';import {pathToFileURL} from 'node:url';
const [model,output,threePackage]=process.argv.slice(2);
const THREE=await import(pathToFileURL(path.resolve(threePackage,'build/three.module.js')));
const {GLTFLoader}=await import(pathToFileURL(path.resolve(threePackage,'examples/jsm/loaders/GLTFLoader.js')));
const bytes=fs.readFileSync(model);const modelData=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
const gltf=await new GLTFLoader().parseAsync(modelData,'');gltf.scene.updateMatrixWorld(true);
let meshes=0,triangles=0,materials=new Set(),badMatrices=0;gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;materials.add(o.material.uuid);if(o.matrixWorld.determinant()<=0)badMatrices++;}});
const bounds=new THREE.Box3().setFromObject(gltf.scene);const result={status:badMatrices?'FAIL':'PASS',scope:'GLTFLoader parse and world-space bounds only. No graphics context, GPU render, shader or populated-scene performance claim.',three_revision:THREE.REVISION,glb_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),mesh_primitives:meshes,materials:materials.size,triangles,nonpositive_matrices:badMatrices,bounds_glb_m:{min:bounds.min.toArray(),max:bounds.max.toArray(),size:bounds.getSize(new THREE.Vector3()).toArray()},gpu:'NOT_RUN',populated_scene:'NOT_RUN'};fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));

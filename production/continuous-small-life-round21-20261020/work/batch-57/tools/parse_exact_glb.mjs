// SPDX-License-Identifier: MIT
import fs from 'node:fs';
import crypto from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Box3,Vector3} from 'three';
for(const path of process.argv.slice(2)) {
 const bytes=fs.readFileSync(path);let report={kind:'runtime_parse',target_renderer:'threejs-gltfloader-node',three_version:'0.180.0',glb_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),gpu:'not_run',scene:'not_run'};
 try {const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');gltf.scene.updateMatrixWorld(true);let triangles=0,meshes=0;gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});report={...report,status:'pass',triangles,meshes,dimensions_gltf_xyz_m:new Box3().setFromObject(gltf.scene).getSize(new Vector3()).toArray(),errors:[]};}catch(e){report={...report,status:'fail',errors:[e.message]};}
 fs.writeFileSync(path.replace(/[^/]+$/, 'runtime-parse.report.json'),JSON.stringify(report,null,2));console.log(path,report.status);
}

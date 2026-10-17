// SPDX-License-Identifier: MIT
// Exact file parse only. No GPU rendering or visual approval is inferred.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Box3,Vector3,REVISION} from 'three';
for(const slug of ['bothriolepis','waptia']){
 const base=`assets/prehistoric/fauna/${slug}`, bytes=await fs.readFile(`${base}/${slug}.glb`);
 const hash=crypto.createHash('sha256').update(bytes).digest('hex');
 const meta=JSON.parse(await fs.readFile(`${base}/metadata.json`,'utf8'));
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
 gltf.scene.updateMatrixWorld(true);let triangles=0,primitives=0,positionVertices=0;const materials=new Set();
 gltf.scene.traverse(o=>{if(o.isMesh){primitives++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;positionVertices+=o.geometry.attributes.position.count;for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m);}});
 const dims=new Box3().setFromObject(gltf.scene).getSize(new Vector3()).toArray();
 const delta=Math.max(...dims.map((v,i)=>Math.abs(v-meta.dimensions[i])));
 const errors=[];if(triangles!==meta.triangles)errors.push('triangle count mismatch');if(delta>1e-4)errors.push('bounds mismatch');if(gltf.animations.length)errors.push('unexpected animation');
 const report={schema_version:1,check:'threejs-exact-glb-parse',status:errors.length?'fail':'pass',glb_sha256:hash,three_revision:REVISION,three_package:'0.180.0',node:process.version,loader:'GLTFLoader.parseAsync',triangles,primitives,position_vertices:positionVertices,materials:materials.size,dimensions_glb_m:dims,bounds_max_error_m:delta,animations:gltf.animations.length,errors,gpu_rendering:'not_tested',visual_review:'pending',scene_performance:'not_tested'};
 await fs.writeFile(`${base}/threejs-parse.report.json`,JSON.stringify(report,null,2)+'\n');console.log(slug,report.status,triangles,primitives);if(errors.length)process.exitCode=1;
}

import fs from 'node:fs';import crypto from 'node:crypto';
import validator from '/workspace/shared/lowpoly-landair-web-integration/node_modules/gltf-validator/index.js';
import {GLTFLoader} from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import {Box3,Vector3,REVISION} from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/build/three.module.js';
const R='/workspace/shared/lowpoly-batch88-20261020',Q='/workspace/shared/lowpoly-batch88-independent-qa-20261020';
for(const a of JSON.parse(fs.readFileSync(R+'/production/batch88/handoff-assets.json'))){
 const p=R+'/'+a.path+'/model.glb',b=fs.readFileSync(p),hash=crypto.createHash('sha256').update(b).digest('hex');
 const val=await validator.validateBytes(new Uint8Array(b),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw Error('Unexpected external '+uri)}});
 const gltf=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');gltf.scene.updateMatrixWorld(true);let triangles=0,meshes=0;let materials=new Set();gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m.uuid)}});
 const report={asset_id:a.asset_id,revision:a.revision,glb_sha256:hash,created_at:new Date().toISOString(),khronos:{version:validator.version(),issues:val.issues},runtime_parse:{status:'PASS',three_revision:REVISION,triangles,meshes,materials:materials.size,bounds_glb_xyz_m:new Box3().setFromObject(gltf.scene).getSize(new Vector3()).toArray()},gpu:'NOT_RUN',scene:'NOT_RUN'};fs.writeFileSync(Q+'/'+a.asset_id+'/runtime-check.json',JSON.stringify(report,null,2)+'\n');console.log(a.asset_id,val.issues.numErrors,val.issues.numWarnings,triangles);
}

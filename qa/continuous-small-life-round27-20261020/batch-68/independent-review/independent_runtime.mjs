import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import validator from 'gltf-validator';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { Box3, Vector3, REVISION } from 'three';
const ids=['thaumaptilon','sandstone-fin','lava-dome','ice-wedge-polygon-ground'];
const root='/workspace/shared/lowpoly-batch68-20261020/assets/candidates/continuous-small-life-round27-20261020/batch-68';
const out='/workspace/shared/lowpoly-round27-qa68';
const results=[];
for(const id of ids){
 const p=path.join(root,id,'r001','model.glb'); const bytes=fs.readFileSync(p);
 const sha=crypto.createHash('sha256').update(bytes).digest('hex');
 const vr=await validator.validateBytes(new Uint8Array(bytes),{uri:path.basename(p),format:'glb',writeTimestamp:false,maxIssues:0});
 const buf=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
 const gltf=await new GLTFLoader().parseAsync(buf,'');
 gltf.scene.updateMatrixWorld(true); let triangles=0,meshes=0,primitives=0;
 gltf.scene.traverse(o=>{if(o.isMesh){meshes++;primitives++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});
 const size=new Box3().setFromObject(gltf.scene).getSize(new Vector3()).toArray();
 results.push({asset_id:id,glb_sha256:sha,bytes:bytes.length,khronos:{version:validator.version(),errors:vr.issues.numErrors,warnings:vr.issues.numWarnings,infos:vr.issues.numInfos,hints:vr.issues.numHints,issues:vr.issues.messages},three:{revision:REVISION,parser:'Node GLTFLoader.parseAsync',status:'pass',triangles,mesh_count:meshes,primitive_count:primitives,bounds_glb_xyz_m:size,gpu:'not_run',scene:'not_run'}});
 console.log(id,'Khronos errors/warnings',vr.issues.numErrors,vr.issues.numWarnings,'Three triangles',triangles,'meshes',meshes,'bounds',size);
}
fs.writeFileSync(path.join(out,'independent-runtime-checks.json'),JSON.stringify({schema_version:1,executed_at:new Date().toISOString(),runtime:'Node CPU only; no GPU or composed scene',assets:results},null,2)+'\n');

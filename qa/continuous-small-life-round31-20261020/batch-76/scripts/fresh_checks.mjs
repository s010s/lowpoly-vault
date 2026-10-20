import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Box3,Vector3,REVISION} from 'three';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url); const validator=require('gltf-validator');
const root='/workspace/shared/lowpoly-batch76-20261020/production/continuous-small-life-round31-20261020/assets';
const out='/workspace/shared/lowpoly-round31-qa76';
const candidates=[['rangea','r002'],['serac','r001'],['moulin-shaft','r002'],['solifluction-lobe','r002']];
for(const [id,rev] of candidates){
 const d=path.join(root,id,rev), input=path.join(d,'model.glb'), bytes=await fs.readFile(input), digest=crypto.createHash('sha256').update(bytes).digest('hex');
 const k=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw new Error('Unexpected external resource: '+uri)}});
 const messages=k.issues.messages||[], kr={kind:'fresh-official-khronos-validation',asset_id:id,revision:rev,sha256:digest,validator_version:validator.version(),status:k.issues.numErrors?'fail':k.issues.numWarnings?'pass_with_warnings':'pass',num_errors:k.issues.numErrors,num_warnings:k.issues.numWarnings,errors:messages.filter(x=>x.severity===0),warnings:messages.filter(x=>x.severity===1),truncated:Boolean(k.issues.truncated)};
 await fs.writeFile(path.join(out,'khronos',`${id}-${rev}.json`),JSON.stringify(kr,null,2)+'\n');
 const ab=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength), gltf=await new GLTFLoader().parseAsync(ab,''); gltf.scene.updateMatrixWorld(true); let triangles=0,meshes=0;
 gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});
 const bounds=new Box3().setFromObject(gltf.scene).getSize(new Vector3()).toArray();
 const tr={kind:'fresh-node-three-gltfloader-parse',asset_id:id,revision:rev,sha256:digest,three_revision:REVISION,parser:'GLTFLoader.parseAsync',status:'pass',triangles,meshes,bounds_glb_xyz_m:bounds,gpu:'not_run',scene:'not_run',limitations:'Node parser only; not browser, graphics-device, GPU, user, populated-scene or website proof.'};
 await fs.writeFile(path.join(out,'three',`${id}-${rev}.json`),JSON.stringify(tr,null,2)+'\n');
 gltf.scene.traverse(o=>{o.geometry?.dispose();for(const m of (Array.isArray(o.material)?o.material:[o.material]))m?.dispose();});
 console.log(JSON.stringify({id,rev,khronos:kr.status,errors:kr.num_errors,warnings:kr.num_warnings,triangles,meshes,bounds}));
}

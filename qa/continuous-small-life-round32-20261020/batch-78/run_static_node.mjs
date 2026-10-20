import fs from 'node:fs'; import crypto from 'node:crypto'; import {pathToFileURL} from 'node:url'; import path from 'node:path';
const nm='/workspace/shared/lowpoly-landair-web-integration/node_modules';
const {GLTFLoader}=await import(pathToFileURL(path.join(nm,'three/examples/jsm/loaders/GLTFLoader.js')).href);
const {Box3,Vector3,REVISION}=await import(pathToFileURL(path.join(nm,'three/build/three.module.js')).href);
const require=(await import('node:module')).createRequire(import.meta.url); const validator=require(path.join(nm,'gltf-validator'));
const base='/workspace/shared/lowpoly-batch78-20261020/production/continuous-small-life-round32-20261020/assets';
const list=[['pteridinium','r003'],['pingo','r002'],['sill-ledge','r001'],['exfoliation-dome','r002']];
for(const [id,rev] of list){
 const dir=path.join(base,id,rev), b=fs.readFileSync(path.join(dir,'model.glb')), hash=crypto.createHash('sha256').update(b).digest('hex');
 const parsed=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),''); parsed.scene.updateMatrixWorld(true); let tri=0, meshes=0; parsed.scene.traverse(o=>{if(o.isMesh){meshes++;tri+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});
 const three={kind:'fresh_three_parse',status:'pass',asset_id:id,revision:rev,glb_sha256:hash,three_revision:REVISION,triangles:tri,meshes,bounds_glb_xyz_m:new Box3().setFromObject(parsed.scene).getSize(new Vector3()).toArray(),gpu:'not_run',scene:'not_run',limitations:'Fresh Node GLTFLoader parse only; not an actual GPU renderer or composed scene.'};
 fs.writeFileSync(`/workspace/shared/lowpoly-round32-qa78/reports/${id}-three.json`,JSON.stringify(three,null,2)+'\n');
 const val=await validator.validateBytes(new Uint8Array(b),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw new Error('External resource disallowed: '+uri)}}); const v={kind:'fresh_khronos_gltf_validator',asset_id:id,revision:rev,glb_sha256:hash,validator_version:validator.version(),errors:val.issues.messages.filter(x=>x.severity===0),warnings:val.issues.messages.filter(x=>x.severity===1),num_errors:val.issues.numErrors,num_warnings:val.issues.numWarnings,truncated:!!val.issues.truncated,status:val.issues.numErrors?'fail':val.issues.numWarnings?'pass_with_warnings':'pass',limitations:'Format validation only; no GPU/scene or factual approval.'};
 fs.writeFileSync(`/workspace/shared/lowpoly-round32-qa78/reports/${id}-khronos.json`,JSON.stringify(v,null,2)+'\n'); console.log(id,JSON.stringify({three:tri,khronos:v.status,errors:v.num_errors,warnings:v.num_warnings,hash}));
}

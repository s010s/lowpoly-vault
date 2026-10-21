import fs from 'node:fs';import crypto from 'node:crypto';import {createRequire} from 'node:module';
import {GLTFLoader} from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import {Box3,Vector3,REVISION} from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/build/three.module.js';
const req=createRequire('/workspace/shared/lowpoly-landair-web-integration/package.json'),validator=req('gltf-validator');
const root='/workspace/shared/lowpoly-batch96-20261020',out='/workspace/shared/lowpoly-batch96-independent-qa-20261021';
const h=JSON.parse(fs.readFileSync(root+'/production/batch96/maker-handoff.json'));
for (const a of h.selected_assets){
 const b=fs.readFileSync(root+'/'+a.path+'/model.glb'),hash=crypto.createHash('sha256').update(b).digest('hex');
 const val=await validator.validateBytes(new Uint8Array(b),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async u=>{throw new Error(u)}});
 fs.writeFileSync(`${out}/${a.asset_id}/khronos.json`,JSON.stringify({recorded_at:new Date().toISOString(),glb_sha256:hash,version:validator.version(),report:val},null,2));
 const gl=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');gl.scene.updateMatrixWorld(true);let triangles=0,meshes=0,vertices=0;
 gl.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;vertices+=o.geometry.attributes.position.count;}});
 const report={recorded_at:new Date().toISOString(),glb_sha256:hash,three_revision:REVISION,triangles,meshes,position_vertices:vertices,bounds_m:new Box3().setFromObject(gl.scene).getSize(new Vector3()).toArray(),gpu:'not_run',scene:'not_run'};
 fs.writeFileSync(`${out}/${a.asset_id}/runtime-parse.json`,JSON.stringify(report,null,2));
 if(val.issues.numErrors||val.issues.numWarnings||triangles!==a.triangles)throw new Error(a.asset_id+' validation failed');console.log(a.asset_id,'Khronos 0/0; Three triangles',triangles);
}

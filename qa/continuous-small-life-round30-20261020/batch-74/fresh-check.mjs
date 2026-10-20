import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {Box3, Vector3, REVISION} from '/workspace/shared/lowpoly-batch74-20261020/node_modules/three/build/three.module.js';
import {GLTFLoader} from '/workspace/shared/lowpoly-batch74-20261020/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
const require=createRequire(import.meta.url);
const validator=require('/workspace/shared/lowpoly-batch74-20261020/node_modules/gltf-validator');
const root='/workspace/shared/lowpoly-batch74-20261020/production/continuous-small-life-round30-20261020/assets';
const out='/workspace/shared/lowpoly-round30-qa74';
const selected=[['tribrachidium','r002'],['arete-ridge','r001'],['crevasse-splay','r002'],['coal-seam-outcrop','r002']];
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const ts=()=>new Date().toISOString();
const log=[];
for (const [id,rev] of selected) {
 const dir=`${root}/${id}/${rev}`; const file=`${dir}/model.glb`; const b=fs.readFileSync(file); const sha=hash(b);
 const khr=await validator.validateBytes(new Uint8Array(b),{uri:path.basename(file),maxIssues:10000,externalResourceFunction:async uri=>{throw new Error('standalone GLB requested external resource: '+uri)}});
 const messages=khr.issues?.messages||[]; const errors=messages.filter(x=>x.severity===0); const warnings=messages.filter(x=>x.severity===1);
 const kreport={schema_version:1,kind:'independent_khronos_gltf_validation',target:`${id}/${rev}`,glb_sha256:sha,validator_version:validator.version(),created_at:ts(),status:errors.length?'fail':warnings.length?'pass_with_warnings':'pass',issues:{num_errors:errors.length,num_warnings:warnings.length,truncated:Boolean(khr.issues?.truncated),errors,warnings},limitations:'Independent run of Khronos glTF Validator; static format validation only.'};
 fs.writeFileSync(`${out}/khronos/${id}-${rev}.json`,JSON.stringify(kreport,null,2)+'\n');
 const dv=new DataView(b.buffer,b.byteOffset,b.byteLength); const magic=dv.getUint32(0,true), version=dv.getUint32(4,true), declared=dv.getUint32(8,true), chunkLen=dv.getUint32(12,true), chunkType=dv.getUint32(16,true); const json=JSON.parse(new TextDecoder().decode(b.subarray(20,20+chunkLen)).replace(/\0+$/,'').trim());
 const loader=new GLTFLoader(); const ab=b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength); const gltf=await loader.parseAsync(ab,''); gltf.scene.updateMatrixWorld(true); let triangles=0,meshes=0,positions=0; gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;positions+=o.geometry.attributes.position.count;}}); const dims=new Box3().setFromObject(gltf.scene).getSize(new Vector3()).toArray();
 const report={schema_version:1,kind:'independent_threejs_gltfloader_parse',target:`${id}/${rev}`,glb_sha256:sha,three_revision:REVISION,parser:'GLTFLoader.parseAsync',created_at:ts(),status:'pass',glb_header:{magic_hex:'0x'+magic.toString(16),magic_ok:magic===0x46546c67,version,declared_length:declared,actual_length:b.byteLength,json_chunk_length:chunkLen,json_chunk_type_hex:'0x'+chunkType.toString(16),header_ok:magic===0x46546c67&&version===2&&declared===b.byteLength&&chunkType===0x4e4f534a},summary:{scene_meshes:meshes,triangles,position_vertices:positions,material_definitions:json.materials?.length||0,primitives:(json.meshes||[]).reduce((s,m)=>s+m.primitives.length,0),textures:json.textures?.length||0,images:json.images?.length||0,extensions_used:json.extensionsUsed||[],bounds_glb_xyz_m:dims},errors:[],limitations:'Independent Node Three.js parser only; does not establish GPU rendering or composed-scene integration.'};
 fs.writeFileSync(`${out}/three/${id}-${rev}.json`,JSON.stringify(report,null,2)+'\n');
 log.push(`${ts()} pid=${process.pid} ${id}/${rev} sha256=${sha} Khronos=${kreport.status} errors=${errors.length} warnings=${warnings.length} Three=${report.status} triangles=${triangles} meshes=${meshes} bounds=${dims.join(',')}\n`);
}
fs.writeFileSync(`${out}/fresh-checks.log`,log.join(''));
console.log(log.join(''));

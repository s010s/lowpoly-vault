import fs from 'node:fs';import crypto from 'node:crypto';import {createRequire} from 'node:module';
import * as THREE from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/build/three.module.js';
import {GLTFLoader} from '/workspace/shared/lowpoly-landair-web-integration/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
const require=createRequire(import.meta.url);const validator=require('/workspace/shared/lowpoly-landair-web-integration/node_modules/gltf-validator');
const ROOT='/workspace/shared/lowpoly-batch93-20261020',OUT='/workspace/shared/lowpoly-batch93-independent-qa-20261020';
for(const [a,v] of [['omphalophloios','r004'],['chaloneria','r001'],['nathorstiana','r002'],['diplopora','r002']]) {
 const file=`${ROOT}/production/small-life-batch93/${a}/${v}/artifacts/${a}.glb`,b=fs.readFileSync(file),sha=crypto.createHash('sha256').update(b).digest('hex'),started=new Date().toISOString();
 const kr=await validator.validateBytes(new Uint8Array(b),{uri:`${a}.glb`,maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async u=>{throw new Error('external resource '+u)}});
 fs.writeFileSync(`${OUT}/${a}/khronos.json`,JSON.stringify({glb_sha256:sha,started_at:started,finished_at:new Date().toISOString(),pid:process.pid,validator_version:validator.version(),report:kr},null,2)+'\n',{flag:'wx'});
 const st=performance.now();const g=await new Promise((resolve,reject)=>new GLTFLoader().parse(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'',resolve,reject));g.scene.updateMatrixWorld(true);
 let triangles=0,positions=0,meshes=0,mats=new Set(),box=new THREE.Box3();const vertices=[];
 g.scene.traverse(o=>{if(!o.isMesh)return;meshes++;const geo=o.geometry,p=geo.attributes.position;triangles+=(geo.index?geo.index.count:p.count)/3;positions+=p.count;for(const m of Array.isArray(o.material)?o.material:[o.material])mats.add(m.uuid);for(let i=0;i<p.count;i++){const v=new THREE.Vector3().fromBufferAttribute(p,i).applyMatrix4(o.matrixWorld);box.expandByPoint(v);vertices.push(v.toArray())}});
 const r={asset_id:a,revision:v,glb_sha256:sha,started_at:started,finished_at:new Date().toISOString(),pid:process.pid,three_revision:THREE.REVISION,meshes,triangles,position_vertices:positions,materials:mats.size,bounds_world_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new THREE.Vector3()).toArray()},parse_ms:performance.now()-st,animations:g.animations.length,status:'pass',gpu:'unknown/unrun',scene:'unknown/unrun',method:'Actual GLTFLoader parsing and transformed POSITION data iteration in Node, not box metadata only. Not a GPU or composed-scene run.'};
 fs.writeFileSync(`${OUT}/${a}/three-parse.json`,JSON.stringify(r,null,2)+'\n',{flag:'wx'});console.log(a,'Khronos',kr.issues.numErrors,kr.issues.numWarnings,'Three',triangles,positions);
}

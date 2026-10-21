const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ROOT='/workspace/shared/lowpoly-batch89-20261020',OUT='/workspace/shared/lowpoly-batch89-independent-qa-20261020',MOD='/workspace/shared/lowpoly-landair-web-integration/node_modules';
const validator=require(MOD+'/gltf-validator');
(async()=>{
const THREE=await import('file://'+MOD+'/three/build/three.module.js');const {GLTFLoader}=await import('file://'+MOD+'/three/examples/jsm/loaders/GLTFLoader.js');
const hand=JSON.parse(fs.readFileSync(ROOT+'/production/small-life-batch89/maker-handoff.json','utf8'));
for(const item of hand.items){const file=ROOT+'/'+item.artifacts.glb.path,b=fs.readFileSync(file),sha=crypto.createHash('sha256').update(b).digest('hex');if(sha!==item.artifacts.glb.sha256)throw Error('hash mismatch');
const val=await validator.validateBytes(new Uint8Array(b),{uri:path.basename(file),maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw Error('External resource blocked: '+uri)}});
fs.writeFileSync(OUT+'/'+item.asset_id+'/own-khronos-validation.json',JSON.stringify({glb_sha256:sha,created_at:new Date().toISOString(),validator_version:validator.version(),report:val},null,2)+'\n');
const t=performance.now();const result=await new Promise((resolve,reject)=>new GLTFLoader().parse(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'',resolve,reject));let meshes=0,triangles=0,materials=new Set();result.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m.uuid)}});let box=new THREE.Box3().setFromObject(result.scene);
const r={schema_version:1,glb_sha256:sha,created_at:new Date().toISOString(),three_revision:THREE.REVISION,loader:'GLTFLoader',meshes,triangles,materials:materials.size,bounds:{min:box.min.toArray(),max:box.max.toArray()},parse_ms:performance.now()-t,errors:[],gpu:'not_run',scene:'not_run',status:'pass',limitations:'Own Node parse of exact bytes. No GPU render or composed-scene test performed.'};fs.writeFileSync(OUT+'/'+item.asset_id+'/own-three-parse.json',JSON.stringify(r,null,2)+'\n');console.log(item.asset_id,'Khronos errors',val.issues.numErrors,'warnings',val.issues.numWarnings,'Three',triangles,meshes,materials.size);
if(val.issues.numErrors)process.exitCode=1;
}
})().catch(e=>{console.error(e);process.exit(1)});

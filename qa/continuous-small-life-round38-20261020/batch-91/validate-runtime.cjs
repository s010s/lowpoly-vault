const fs=require('fs'),crypto=require('crypto'),path=require('path');
const S='/workspace/shared/lowpoly-batch91-20261020',D='/workspace/shared/lowpoly-batch91-independent-qa-20261020';
const validator=require(S+'/node_modules/gltf-validator');
(async()=>{
const THREE=await import(S+'/node_modules/three/build/three.module.js');const {GLTFLoader}=await import(S+'/node_modules/three/examples/jsm/loaders/GLTFLoader.js');
for(const item of JSON.parse(fs.readFileSync(S+'/production/small-life-batch91/maker-handoff.json')).items){
 const file=S+'/'+item.artifacts.glb.path,b=fs.readFileSync(file),t=performance.now();
 const v=await validator.validateBytes(new Uint8Array(b),{uri:path.basename(file),maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async(uri)=>{throw new Error('No external resources allowed: '+uri)}});
 const scene=await new Promise((resolve,reject)=>new GLTFLoader().parse(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'',resolve,reject));let meshes=0,tri=0,mats=new Set();scene.scene.traverse(o=>{if(o.isMesh){meshes++;tri+=(o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])mats.add(m.uuid)}});let box=new THREE.Box3().setFromObject(scene.scene);
 const r={created_at:new Date().toISOString(),node:process.version,pid:process.pid,glb_sha256:crypto.createHash('sha256').update(b).digest('hex'),khronos:{version:validator.version(),report:v},runtime_parse:{three_revision:THREE.REVISION,loader:'GLTFLoader',meshes,triangles:tri,materials:mats.size,bounds:{min:box.min.toArray(),max:box.max.toArray()},elapsed_ms:performance.now()-t},gpu:'not_run',scene:'not_run'};
 fs.writeFileSync(D+'/'+item.asset_id+'/khronos-three.report.json',JSON.stringify(r,null,2)+'\n');console.log(item.asset_id,v.issues.numErrors,v.issues.numWarnings,tri);
 if(v.issues.numErrors)process.exitCode=1;
}})().catch(e=>{console.error(e);process.exit(1)});

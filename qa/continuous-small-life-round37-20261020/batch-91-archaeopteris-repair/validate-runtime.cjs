const fs=require('fs'),crypto=require('crypto'),path=require('path');
const N='/workspace/shared/lowpoly-landair-web-integration/node_modules', O='/workspace/shared/lowpoly-batch91-archaeopteris-repair-independent-qa-20261021';
(async()=>{
const validator=require(N+'/gltf-validator');const THREE=await import(N+'/three/build/three.module.js');const {GLTFLoader}=await import(N+'/three/examples/jsm/loaders/GLTFLoader.js');
const file='/workspace/shared/lowpoly-batch91-archaeopteris-repair-20261020/production/batch91-archaeopteris-repair/archaeopteris/r002/artifacts/archaeopteris.glb',b=fs.readFileSync(file),t=performance.now();
const v=await validator.validateBytes(new Uint8Array(b),{uri:path.basename(file),maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async(uri)=>{throw new Error('Unexpected external resource: '+uri)}});
const scene=await new Promise((resolve,reject)=>new GLTFLoader().parse(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'',resolve,reject));let meshes=0,triangles=0,mats=new Set();scene.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])mats.add(m.uuid)}});let box=new THREE.Box3().setFromObject(scene.scene);
const r={created_at:new Date().toISOString(),node:process.version,pid:process.pid,glb_sha256:crypto.createHash('sha256').update(b).digest('hex'),khronos:{version:validator.version(),report:v},runtime_parse:{three_revision:THREE.REVISION,loader:'GLTFLoader',meshes,triangles,materials:mats.size,bounds:{min:box.min.toArray(),max:box.max.toArray()},elapsed_ms:performance.now()-t},gpu:'not_run',scene:'not_run'};
fs.writeFileSync(O+'/khronos-three.report.json',JSON.stringify(r,null,2)+'\n');console.log(v.issues, r.runtime_parse);if(v.issues.numErrors)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});

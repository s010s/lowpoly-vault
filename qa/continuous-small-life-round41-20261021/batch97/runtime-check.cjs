const fs=require('fs'),path=require('path'),crypto=require('crypto');
const N='/workspace/shared/lowpoly-landair-web-integration/node_modules';
const validator=require(N+'/gltf-validator');
(async()=>{const THREE=await import(N+'/three/build/three.module.js');const {GLTFLoader}=await import(N+'/three/examples/jsm/loaders/GLTFLoader.js');
for (const [aid,rev] of [['ginkgo','r002'],['dicranophyllum','r003'],['noeggerathia','r002'],['bjuvia','r001']]) {
 const f=`/workspace/shared/lowpoly-batch97-20261020/production/small-life-batch97/${aid}/${rev}/artifacts/${aid}.glb`,out=path.join(__dirname,aid),b=fs.readFileSync(f),sha=crypto.createHash('sha256').update(b).digest('hex');
 const raw=await validator.validateBytes(new Uint8Array(b),{uri:path.basename(f),maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async()=>{throw new Error('External resources forbidden')}});
 fs.writeFileSync(path.join(out,'khronos-independent.json'),JSON.stringify({asset_id:aid,glb_sha256:sha,observed_at:new Date().toISOString(),pid:process.pid,validator_version:validator.version(),report:raw},null,2)+'\n',{flag:'wx'});
 const s=performance.now(),result=await new Promise((resolve,reject)=>new GLTFLoader().parse(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'',resolve,reject));let meshes=0,triangles=0,mats=new Set();result.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])mats.add(m.uuid)}});const box=new THREE.Box3().setFromObject(result.scene);
 const r={asset_id:aid,glb_sha256:sha,observed_at:new Date().toISOString(),pid:process.pid,three_revision:THREE.REVISION,node_version:process.version,loader:'GLTFLoader',parsed:true,meshes,triangles,materials:mats.size,bounds:{min:box.min.toArray(),max:box.max.toArray()},parse_ms:performance.now()-s,errors:[],gpu:'unknown',scene:'unknown',limitations:'Actual Node GLTFLoader parse; no hardware graphics context or composed scene.'};
 fs.writeFileSync(path.join(out,'three-independent.json'),JSON.stringify(r,null,2)+'\n',{flag:'wx'});console.log(aid,sha,raw.issues,r.triangles)
}
})().catch(e=>{console.error(e);process.exit(1)});

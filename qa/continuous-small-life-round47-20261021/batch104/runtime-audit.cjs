const fs=require('fs'),path=require('path'),crypto=require('crypto');
(async()=>{
 const validator=require('/workspace/shared/lowpoly-landair-web-integration/node_modules/gltf-validator');
 const THREE=await import('/workspace/shared/lowpoly-landair-web-integration/node_modules/three/build/three.module.js');
 const {GLTFLoader}=await import('/workspace/shared/lowpoly-landair-web-integration/node_modules/three/examples/jsm/loaders/GLTFLoader.js');
 const intake=JSON.parse(fs.readFileSync(path.join(__dirname,'final-intake.json'),'utf8'));
 for(const item of intake.assets){
  const aid=item.asset_id,rev=item.revision,p=path.join(intake.worktree,item.glb),out=path.join(__dirname,aid),bytes=fs.readFileSync(p),sha=crypto.createHash('sha256').update(bytes).digest('hex');
  const official=await validator.validateBytes(new Uint8Array(bytes),{uri:path.basename(p),maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw new Error('Unexpected external resource '+uri)}});
  fs.writeFileSync(out+'/khronos-independent.json',JSON.stringify({glb_sha256:sha,report:official},null,2)+'\n');
  const gltf=await new Promise((resolve,reject)=>new GLTFLoader().parse(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'',resolve,reject));let meshes=0,tris=0,mats=new Set();gltf.scene.updateMatrixWorld(true);gltf.scene.traverse(o=>{if(o.isMesh){meshes++;tris+=(o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count)/3;for(let m of Array.isArray(o.material)?o.material:[o.material])mats.add(m.uuid)}});let box=new THREE.Box3().setFromObject(gltf.scene);fs.writeFileSync(out+'/three-independent.json',JSON.stringify({asset_id:aid,revision:rev,glb_sha256:sha,three_revision:THREE.REVISION,status:'pass',meshes,triangles:tris,materials:mats.size,bounds:{min:box.min.toArray(),max:box.max.toArray()},gpu:'unknown',scene:'unknown',checked_at:new Date().toISOString()},null,2)+'\n');console.log(aid,official.issues.numErrors,official.issues.numWarnings,tris);
 }
})().catch(e=>{console.error(e);process.exit(1)});

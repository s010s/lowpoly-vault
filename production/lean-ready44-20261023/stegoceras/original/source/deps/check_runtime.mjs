// SPDX-License-Identifier: MIT
// Explicit Node runtimes provided by --runtime-dir; no generation dependency.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const [rootArg,runtimeArg]=process.argv.slice(2);const root=path.resolve(rootArg),runtime=path.resolve(runtimeArg);
const require=createRequire(import.meta.url);const validator=require(path.join(runtime,'gltf-validator'));
const THREE=await import(pathToFileURL(path.join(runtime,'three/build/three.module.js')));
const {GLTFLoader}=await import(pathToFileURL(path.join(runtime,'three/examples/jsm/loaders/GLTFLoader.js')));
const bytes=fs.readFileSync(path.join(root,'model.glb'));const hash=crypto.createHash('sha256').update(bytes).digest('hex');
const validation=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:()=>Promise.reject(new Error('External resource forbidden'))});
fs.writeFileSync(path.join(root,'qa/evidence/khronos.json'),JSON.stringify({glb_sha256:hash,validator_version:validator.version(),...validation},null,2)+'\n');
const result=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');result.scene.updateMatrixWorld(true);
let triangles=0,nonfinite=0,degenerate=0,misaligned=0,maxNormalError=0;const mats=new Set(),meshes=[];
result.scene.traverse(o=>{if(!o.isMesh)return;const g=o.geometry,p=g.attributes.position,n=g.attributes.normal,idx=g.index,ts=(idx?idx.count:p.count)/3;triangles+=ts;
 for(const x of p.array)if(!Number.isFinite(x))nonfinite++;
 const A=new THREE.Vector3(),B=new THREE.Vector3(),C=new THREE.Vector3(),N=new THREE.Vector3(),cross=new THREE.Vector3();
 for(let k=0;k<n.count;k++){N.fromBufferAttribute(n,k);maxNormalError=Math.max(maxNormalError,Math.abs(N.length()-1));}
 for(let k=0;k<ts*3;k+=3){const ii=[0,1,2].map(v=>idx?idx.getX(k+v):k+v);A.fromBufferAttribute(p,ii[0]);B.fromBufferAttribute(p,ii[1]);C.fromBufferAttribute(p,ii[2]);cross.crossVectors(B.sub(A),C.sub(A));if(cross.length()<1e-10)degenerate++;for(const i of ii){N.fromBufferAttribute(n,i);if(cross.dot(N)<-1e-9)misaligned++;}}
 const materials=Array.isArray(o.material)?o.material:[o.material];for(const m of materials)mats.add(m);
 meshes.push({name:o.name,triangles:ts,positive_determinant:o.matrixWorld.determinant()>0});
});
const b=new THREE.Box3().setFromObject(result.scene);const build=JSON.parse(fs.readFileSync(path.join(root,'qa/evidence/build.json'),'utf8'));
const report={glb_sha256:hash,three_revision:THREE.REVISION,three_version:JSON.parse(fs.readFileSync(path.join(runtime,'three/package.json'),'utf8')).version,scope:'Actual GLTFLoader parse and CPU geometry/normal checks only. Not browser, GPU, scene performance or independent visual acceptance.',triangles,primitives:meshes.length,materials:mats.size,meshes,nonfinite_positions:nonfinite,degenerate_triangles:degenerate,normal_winding_misalignment:misaligned,max_normal_length_error:maxNormalError,bounds_m:{min:b.min.toArray(),max:b.max.toArray(),size:b.getSize(new THREE.Vector3()).toArray()},animations:result.animations.length,cameras:result.cameras.length};
report.pass=validation.issues.numErrors===0&&validation.issues.numWarnings===0&&triangles===build.glb.scene_triangles&&mats.size===6&&meshes.length===7&&nonfinite===0&&degenerate===0&&misaligned===0&&meshes.every(m=>m.positive_determinant);
fs.writeFileSync(path.join(root,'qa/evidence/three-parse.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({pass:report.pass,validator:validation.issues,triangles,primitives:meshes.length}));if(!report.pass)process.exitCode=1;

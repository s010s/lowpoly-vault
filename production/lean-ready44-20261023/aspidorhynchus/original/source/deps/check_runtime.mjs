// SPDX-License-Identifier: MIT
// Official format validator and Three.js CPU parser; no GPU claim.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const [glbPath,outDir,moduleRoot]=process.argv.slice(2);
if(!glbPath||!outDir||!moduleRoot) throw new Error('Usage: node check_runtime.mjs model.glb evidence-dir installed-package-root');
const req=createRequire(path.join(path.resolve(moduleRoot),'package.json'));
const validator=req('gltf-validator');
const three=await import(pathToFileURL(req.resolve('three')));
const {GLTFLoader}=await import(pathToFileURL(req.resolve('three/addons/loaders/GLTFLoader.js')));
const bytes=fs.readFileSync(glbPath),hash=crypto.createHash('sha256').update(bytes).digest('hex');
const report=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async()=>{throw new Error('External resources not allowed');}});
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,'khronos-report.json'),JSON.stringify({glb_sha256:hash,validator_version:validator.version(),report},null,2)+'\n');
if(report.issues.numErrors)throw new Error('Official validator errors');
const ab=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
const gltf=await new Promise((resolve,reject)=>new GLTFLoader().parse(ab,'',resolve,reject));
gltf.scene.updateMatrixWorld(true);let meshes=0,triangles=0;const materials=new Set();const sides=new Set();
gltf.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material]){materials.add(m.uuid);sides.add(m.side);}}});
const box=new three.Box3().setFromObject(gltf.scene);
const parsed={glb_sha256:hash,three_version:three.REVISION,expected_version:'0.180.0',status:'PASS_CPU_PARSE_ONLY',meshes,triangles,materials:materials.size,material_sides:[...sides],bounds_m:{min:box.min.toArray(),max:box.max.toArray(),size:box.getSize(new three.Vector3()).toArray()},gpu:'UNKNOWN',scene:'UNKNOWN',scope:'GLTFLoader CPU parsing, graph, materials, triangle count and bounds only. No WebGLRenderer, browser pixels, shader compilation or populated scene test.'};
if(three.REVISION!=='180')throw new Error('Unexpected Three.js version');
fs.writeFileSync(path.join(outDir,'three-parser.json'),JSON.stringify(parsed,null,2)+'\n');
console.log(JSON.stringify({validator:report.issues,parser:parsed},null,2));

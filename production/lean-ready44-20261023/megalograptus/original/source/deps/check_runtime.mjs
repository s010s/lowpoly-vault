// SPDX-License-Identifier: MIT
// Actual glTF parsing and official Khronos validation; does not create a GPU renderer.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const [file,modules,out] = process.argv.slice(2);
const require=createRequire(path.join(path.resolve(modules),'qa-entry.cjs'));
const validator=require('gltf-validator');
const threeRoot=path.dirname(path.dirname(require.resolve('three')));
const THREE=await import(pathToFileURL(path.join(threeRoot,'build/three.module.js')));
const loaderFile=path.join(threeRoot,'examples/jsm/loaders/GLTFLoader.js');
const {GLTFLoader}=await import(pathToFileURL(loaderFile));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const bytes=fs.readFileSync(file);const sha256=hash(bytes);fs.mkdirSync(out,{recursive:true});
const validation=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw new Error('Forbidden external resource: '+uri)}});
fs.writeFileSync(path.join(out,'khronos.json'),JSON.stringify({status:validation.issues.numErrors?'FAIL':'PASS',glb_sha256:sha256,validator_version:validator.version(),report:validation},null,2)+'\n');
if(validation.issues.numErrors||validation.issues.numWarnings)throw new Error('Khronos errors or warnings require review');
const ab=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
const parsed=await new Promise((resolve,reject)=>new GLTFLoader().parse(ab,'',resolve,reject));
parsed.scene.updateMatrixWorld(true);let meshes=0,triangles=0;const materials=new Set();
parsed.scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count)/3;for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m.name);}});
const bb=new THREE.Box3().setFromObject(parsed.scene);
fs.writeFileSync(path.join(out,'three-parse.json'),JSON.stringify({status:'PASS',glb_sha256:sha256,scope:'Actual Node GLTFLoader parse and transformed bounds. Not a browser, GPU, or populated-scene performance test.',three_version:JSON.parse(fs.readFileSync(path.join(threeRoot,'package.json'))).version,package_sha256:hash(fs.readFileSync(path.join(threeRoot,'package.json'))),loader_sha256:hash(fs.readFileSync(loaderFile)),node_version:process.version,meshes,triangles,materials:[...materials].sort(),bounds_glb_m:{min:bb.min.toArray(),max:bb.max.toArray()},gpu:'UNKNOWN',scene:'UNKNOWN'},null,2)+'\n');
console.log('Khronos 0 errors / 0 warnings; Three GLTFLoader parsed',meshes,'meshes',triangles,'triangles');

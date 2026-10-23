// SPDX-License-Identifier: MIT
// npm runtime dependencies: three@0.180.0 and gltf-validator@2.0.0-dev.3.10.
// Usage: node check_runtime.mjs model.glb node_modules output.json
// This is GLTFLoader CPU parsing, NOT browser/WebGL or scene performance QA.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const [glb,modules,out]=process.argv.slice(2);
const require=createRequire(path.resolve(modules,'runtime-anchor.cjs'));
const validator=require('gltf-validator');
const three=await import(pathToFileURL(path.resolve(modules,'three/build/three.module.js')));
const {GLTFLoader}=await import(pathToFileURL(path.resolve(modules,'three/examples/jsm/loaders/GLTFLoader.js')));
const bytes=fs.readFileSync(glb);const hash=crypto.createHash('sha256').update(bytes).digest('hex');
const report=await validator.validateBytes(new Uint8Array(bytes),{uri:path.basename(glb),maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw Error('External resource prohibited: '+uri);}});
const parsed=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
parsed.scene.updateMatrixWorld(true);
const bounds=new three.Box3().setFromObject(parsed.scene);const meshes=[];let tri=0;
parsed.scene.traverse(o=>{if(o.isMesh){const t=(o.geometry.index?o.geometry.index.count:o.geometry.attributes.position.count)/3;tri+=t;meshes.push({name:o.name,triangles:t,material:o.material.name,side:o.material.side,transparent:o.material.transparent});}});
const value={glb_sha256:hash,khronos:{validator_version:validator.version(),status:report.issues.numErrors===0?'PASS':'FAIL',report},threejs:{version:three.REVISION,status:'PASS_PARSE_ONLY',bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()},triangles:tri,meshes,scope:'CPU GLTFLoader parsing and world bounds; no GPU or browser.'},gpu:'NOT_RUN',populated_scene:'NOT_RUN'};
fs.writeFileSync(out,JSON.stringify(value,null,2)+'\n');if(report.issues.numErrors)process.exitCode=1;console.log(JSON.stringify({glb_sha256:hash,errors:report.issues.numErrors,warnings:report.issues.numWarnings,meshes:meshes.length,triangles:tri}));

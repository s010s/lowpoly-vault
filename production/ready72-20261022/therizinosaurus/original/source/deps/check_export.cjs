// SPDX-License-Identifier: MIT
// Usage: node check_export.cjs model.glb output.json /path/to/node_modules/gltf-validator
const fs=require('node:fs'),crypto=require('node:crypto');
const [file,out,modulePath]=process.argv.slice(2);const validator=require(modulePath||'gltf-validator');
(async()=>{const bytes=fs.readFileSync(file);const report=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,externalResourceFunction:async uri=>{throw Error('External resource forbidden: '+uri)}});const value={status:report.issues.numErrors?'FAIL':'PASS',claim_scope:'Official Khronos glTF format validation only',glb_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),validator_version:validator.version(),report};fs.writeFileSync(out,JSON.stringify(value,null,2)+'\n');if(report.issues.numErrors)process.exitCode=1;console.log(JSON.stringify(report.issues));})();

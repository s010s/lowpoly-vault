// SPDX-License-Identifier: MIT
// Official Khronos validator wrapper; install pinned gltf-validator runtime separately.
const fs=require('node:fs'),crypto=require('node:crypto'),validator=require('gltf-validator');
const [file,out]=process.argv.slice(2);const data=fs.readFileSync(file);
validator.validateBytes(new Uint8Array(data),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async()=>{throw Error('External resource forbidden for standalone model');}}).then(report=>{
 const result={validator:'Khronos glTF Validator',version:validator.version(),glb_sha256:crypto.createHash('sha256').update(data).digest('hex'),status:report.issues.numErrors===0?'PASS':'FAIL',report};
 fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result.report.issues));process.exitCode=report.issues.numErrors?1:0;
}).catch(e=>{console.error(e);process.exitCode=2;});

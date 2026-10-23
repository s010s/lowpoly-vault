#!/usr/bin/env node
// SPDX-License-Identifier: MIT
// Repeatable official format check. npm runtime: gltf-validator 2.0.0-dev.3.10.
const fs=require('node:fs'),crypto=require('node:crypto'),validator=require('gltf-validator');
(async()=>{
 const bytes=fs.readFileSync(process.argv[2]);
 const report=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw Error('External resource forbidden: '+uri)}});
 const result={status:report.issues.numErrors?'FAIL':report.issues.numWarnings?'PASS_WITH_WARNINGS':'PASS',validator_version:validator.version(),glb_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),report};
 fs.writeFileSync(process.argv[3],JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({status:result.status,version:result.validator_version,issues:report.issues}));process.exitCode=report.issues.numErrors?1:0;
})().catch(e=>{console.error(e);process.exitCode=2});

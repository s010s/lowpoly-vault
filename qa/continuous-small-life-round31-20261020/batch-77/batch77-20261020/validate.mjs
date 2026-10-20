import fs from 'node:fs';
import crypto from 'node:crypto';
import validator from '/workspace/shared/lowpoly-landair-web-integration/node_modules/gltf-validator/index.js';
for (const target of process.argv.slice(2)) {
 const b=fs.readFileSync(target),sha=crypto.createHash('sha256').update(b).digest('hex');
 const report=await validator.validateBytes(new Uint8Array(b),{uri:target.split('/').at(-1),maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw new Error('External resource request: '+uri)}});
 const out={kind:'fresh_khronos_validation',path:target,sha256:sha,bytes:b.length,validator_version:validator.version(),errors:report.issues.numErrors,warnings:report.issues.numWarnings,truncated:report.issues.truncated,messages:report.issues.messages||[]};
 console.log(JSON.stringify(out));
}

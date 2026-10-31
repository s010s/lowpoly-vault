/** Read-only Khronos validation of the exact 36 transformed delivery files. */
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import validator from 'gltf-validator';
const folder='production/creature36-20261031',ledger=JSON.parse(await readFile(folder+'/integration-ledger.json')),results=[];
for(const row of ledger.models){
 const bytes=await readFile(row.glb);assert.equal(createHash('sha256').update(bytes).digest('hex'),row.glb_sha256);
 const report=await validator.validateBytes(new Uint8Array(bytes),{uri:row.id+'.glb',maxIssues:1000,externalResourceFunction:async()=>{throw Error('External resource forbidden');}});
 results.push({id:row.id,glb_sha256:row.glb_sha256,errors:report.issues.numErrors,warnings:report.issues.numWarnings,truncated:report.issues.truncated,messages:report.issues.messages});
}
await writeFile(folder+'/evidence/format-validation.json',JSON.stringify({validator:validator.version(),models:results},null,2)+'\n');
console.log(JSON.stringify(results.map(({id,errors,warnings})=>({id,errors,warnings}))));assert(results.every(r=>r.errors===0&&!r.truncated));

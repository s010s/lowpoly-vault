const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const validator = require('/workspace/shared/lowpoly-batch73-20261020/node_modules/gltf-validator');
const root = '/workspace/shared/lowpoly-batch73-20261020/production/continuous-small-life-round29-20261020/work/batch-73/assets';
const jobs = [
 ['fractofusus','r002'],['striated-bedrock','r003'],['fumarole-vent','r003'],['banded-iron-formation','r003']
];
(async()=>{
 let rows=[];
 for(const [id,rev] of jobs){
  const p=path.join(root,id,rev,'model.glb'); const bytes=fs.readFileSync(p); const sha256=crypto.createHash('sha256').update(bytes).digest('hex');
  const report=await validator.validateBytes(new Uint8Array(bytes),{uri:'model.glb',maxIssues:10000,externalResourceFunction:async uri=>{throw new Error('Unexpected external URI: '+uri)}});
  const messages=report.issues.messages||[]; const errors=messages.filter(x=>x.severity===0); const warnings=messages.filter(x=>x.severity===1);
  rows.push({asset_id:id,revision:rev,path:p,bytes:bytes.length,sha256,validator_version:validator.version(),errors,warnings,num_errors:report.issues.numErrors,num_warnings:report.issues.numWarnings,truncated:!!report.issues.truncated,status:report.issues.numErrors===0&&report.issues.numWarnings===0&&!report.issues.truncated?'pass':'review'});
 }
 const out='/workspace/shared/lowpoly-round29-qa73/fresh-khronos-validation.json'; fs.writeFileSync(out,JSON.stringify({schema_version:1,check:'exact_target_khronos_validation',validator:'gltf-validator',validator_version:validator.version(),target_assets:rows,limitations:'Format validation only; not visual/factual, GPU, browser or composed-scene acceptance.'},null,2)+'\n');
 console.log(JSON.stringify(rows.map(x=>({asset_id:x.asset_id,sha256:x.sha256,status:x.status,bytes:x.bytes,errors:x.num_errors,warnings:x.num_warnings})),null,2));
 if(rows.some(x=>x.status!=='pass')) process.exitCode=1;
})().catch(e=>{console.error(e.stack||String(e));process.exitCode=1});

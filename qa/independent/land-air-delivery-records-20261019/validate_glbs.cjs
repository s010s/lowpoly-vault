// SPDX-License-Identifier: MIT
// Independent fresh official validator; writes adjacent audit evidence only.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const validator=require('gltf-validator');
(async()=>{for(const asset of ['sapeornis','longirostravis','dunbaria','chimerarachne']){
 const filename=path.resolve('production/concept-small-land-air-20261019',asset,'r001/output',asset,asset+'.glb');
 const bytes=fs.readFileSync(filename); const sha256=crypto.createHash('sha256').update(bytes).digest('hex');
 const report=await validator.validateBytes(new Uint8Array(bytes),{uri:path.basename(filename),maxIssues:10000,severityOverrides:{ACCESSOR_INDEX_TRIANGLE_DEGENERATE:0},externalResourceFunction:async uri=>{throw new Error('External resources disallowed: '+uri)}});
 const result={checked_at:new Date().toISOString(),asset_id:asset,revision:'r001',glb_sha256:sha256,validator_version:validator.version(),scope:'Fresh official format validation only; no candidate approval',report};
 const out=path.join(__dirname,asset+'-fresh-khronos.json');if(fs.existsSync(out))throw new Error('Refusing evidence overwrite');
 fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');
 console.log(asset,report.issues.numErrors+' errors',report.issues.numWarnings+' warnings');
 if(report.issues.numErrors||report.issues.numWarnings||report.issues.truncated)process.exitCode=1;
}})().catch(e=>{console.error(e);process.exitCode=1;});

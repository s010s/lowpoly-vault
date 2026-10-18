/** Same mandatory commands and fail-fast semantics, with per-phase CI timings. */
import {spawnSync} from 'node:child_process';
import {mkdirSync,writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const mode=process.argv[2];
const suites=['initial-release','refined-release','small-life-release','small-fauna-release','small-life-batch-release','small-life-round02-release','small-life-round03-release','small-life-round04-release','small-life-round05-release','small-life-round06-release','small-life-round07-release'];
const commands={
 publication:suites.map(name=>({name,command:process.execPath,args:[`site/${name}-test.mjs`]})),
 build:[{name:'publication-check',command:process.execPath,args:['site/initial-release.mjs','--check']},{name:'vite',command:process.execPath,args:['node_modules/vite/bin/vite.js','build']},{name:'copy-and-package',command:process.execPath,args:['site/copy-assets.mjs']},{name:'full-release-audit',command:process.execPath,args:['site/audit-release.mjs']}]
};
assert(Object.hasOwn(commands,mode),'Known timing mode required');
const report={version:1,mode,source_commit:process.env.GITHUB_SHA||null,phases:[],status:'running'};
try{
 for(const step of commands[mode]){
  const started=performance.now(),run=spawnSync(step.command,step.args,{stdio:'inherit',env:process.env});
  const row={name:step.name,seconds:Math.round((performance.now()-started))/1000,exit_code:run.status,signal:run.signal};report.phases.push(row);console.log('CI timing:',JSON.stringify(row));
  if(run.error||run.status!==0){if(run.error)console.error(run.error.message);report.status='fail';process.exitCode=run.status||1;break;}
 }
 if(report.status==='running')report.status='pass';
}finally{mkdirSync('qa/ci-timings',{recursive:true});writeFileSync(`qa/ci-timings/${mode}.json`,JSON.stringify(report,null,2)+'\n');}

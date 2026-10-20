/** Same mandatory commands and fail-fast semantics; optional CI shards run sequentially on isolated runners. */
import {spawnSync} from 'node:child_process';
import {mkdirSync,writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {PUBLICATION_SUITES,readPublicationPlan,assertPublicationPlan,publicationShardSuites,createPublicationShardReport,writePublicationEvidence} from './ci-publication-shards.mjs';
const mode=process.argv[2],options=process.argv.slice(3);
let plan=null,shard=null,output=null;
if(options.length){
 assert.equal(mode,'publication','Only publication supports shards');
 assert.equal(options.length,6,'Specify --plan PATH --shard INDEX --output PATH');
 assert.deepEqual(options.filter((_,index)=>index%2===0),['--plan','--shard','--output']);
 assert(/^[0-3]$/.test(options[3]),'Publication shard must be an integer from 0 to 3');
 plan=readPublicationPlan(options[1]);shard=Number(options[3]);output=options[5];
}
const selected=plan?publicationShardSuites(plan,shard):PUBLICATION_SUITES.map(name=>({name}));
const commands={
 publication:selected.map(suite=>({name:suite.name,sha256:suite.sha256,command:process.execPath,args:[`site/${suite.name}-test.mjs`]})),
 build:[{name:'publication-check',command:process.execPath,args:['site/ci-publication.mjs']},{name:'vite',command:process.execPath,args:['node_modules/vite/bin/vite.js','build']},{name:'copy-and-package',command:process.execPath,args:['site/copy-assets.mjs']},{name:'full-release-audit',command:process.execPath,args:['site/audit-release.mjs']}]
};
assert(Object.hasOwn(commands,mode),'Known timing mode required');
const report={version:1,mode,source_commit:process.env.GITHUB_SHA||null,phases:[],status:'running'};
try{
 for(const step of commands[mode]){
  const started=performance.now(),run=spawnSync(step.command,step.args,{stdio:'inherit',env:process.env});
  const row={name:step.name,seconds:Math.round((performance.now()-started))/1000,exit_code:run.status,signal:run.signal,...(plan?{script_sha256:step.sha256}:{})};report.phases.push(row);console.log('CI timing:',JSON.stringify(row));
  if(run.error||run.status!==0){if(run.error)console.error(run.error.message);report.status='fail';process.exitCode=run.status||1;break;}
 }
 if(plan)assertPublicationPlan(plan);
 if(report.status==='running')report.status='pass';
}catch(error){report.status='fail';process.exitCode=process.exitCode||1;console.error(error.message);
}finally{
 if(plan)writePublicationEvidence(output,createPublicationShardReport(plan,shard,report.phases,report.status));
 else{mkdirSync('qa/ci-timings',{recursive:true});writeFileSync(`qa/ci-timings/${mode}.json`,JSON.stringify(report,null,2)+'\n');}
}

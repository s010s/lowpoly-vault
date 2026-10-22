/** Existing job names remain. Reused regression evidence is never a fresh suite PASS. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,readdirSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {verifiedFastScope} from './ci-release-fast-base.mjs';
import {runtimeConfig} from './ci-provenance.mjs';
import {assertReusedPublicationReports,publicationRuntimeCompatible} from './ci-release-publication-evidence.mjs';
import {PUBLICATION_SUITES,publicationIdentity} from './ci-publication-shards.mjs';
const [mode,...args]=process.argv.slice(2),put=(p,x)=>{mkdirSync(dirname(p),{recursive:true});writeFileSync(p,JSON.stringify(x,null,2)+'\n');};
const scope=publicationRuntimeCompatible(runtimeConfig())?await verifiedFastScope():{eligible:false,reasons:['No matching root-runtime baseline; full coverage retained']};
const identity=publicationIdentity();
const expected=scope.eligible?{version:1,kind:'publication-unchanged-baseline-v1',status:'REUSED_BASELINE',identity,baseline:scope.baseline,added_ids:scope.added_ids,suites:PUBLICATION_SUITES}:null;
function run(file,argv){const r=spawnSync(process.execPath,[file,...argv],{stdio:'inherit',env:process.env});assert.equal(r.status,0,`${file} failed`);}
if(mode==='plan'){
 assert.equal(args.length,1);
 if(expected)put(args[0],expected);else run('site/ci-publication-shards.mjs',['plan',...args]);
}else if(mode==='shard'){
 assert.equal(args.length,3);const [planPath,index,output]=args,plan=JSON.parse(readFileSync(planPath));assert(/^[0-3]$/.test(index));
 if(plan.kind==='publication-unchanged-baseline-v1'){
  assert(expected,'Baseline is no longer authenticated; cannot silently change planned coverage');assert.deepEqual(plan,expected);
  put(output,{...expected,shard_index:Number(index),suites:PUBLICATION_SUITES.filter((_,i)=>i%4===Number(index)),executed_suites:[],fresh_pass:false});
 }else run('site/ci-timed.mjs',['publication','--plan',planPath,'--shard',index,'--output',output]);
}else if(mode==='aggregate'){
 assert.equal(args.length,3);const [planPath,directory,output]=args,plan=JSON.parse(readFileSync(planPath));
 if(plan.kind==='publication-unchanged-baseline-v1'){
  assert(expected,'Baseline no longer independently authenticated');assert.deepEqual(plan,expected);
  const folders=readdirSync(directory).sort();assert.equal(folders.length,4);const reports=[];
  for(let i=0;i<4;i++){const folder=`publication-shard-${i}-${process.env.GITHUB_RUN_ATTEMPT}`;assert(folders.includes(folder));const files=readdirSync(resolve(directory,folder));assert.deepEqual(files,[`shard-${i}.json`]);
   reports.push(JSON.parse(readFileSync(resolve(directory,folder,files[0]))));assert.deepEqual(reports.at(-1),{...expected,shard_index:i,suites:PUBLICATION_SUITES.filter((_,j)=>j%4===i),executed_suites:[],fresh_pass:false});}
  assertReusedPublicationReports(expected,reports);put(output,{...expected,executed_suites:[],fresh_pass:false});console.log('REUSED_BASELINE: unchanged regression code and historical inputs; new models are validated by build production gates.');
 }else run('site/ci-publication-shards.mjs',['aggregate',...args]);
}else throw Error('Expected plan, shard or aggregate');

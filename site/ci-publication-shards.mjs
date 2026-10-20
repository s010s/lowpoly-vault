/** Execution evidence for all mandatory rejection suites, never publication authorization. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,readdirSync,lstatSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {dirname,join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {git,sha256,controlDigest,runtimeConfig} from './ci-provenance.mjs';

export const PUBLICATION_SUITES=Object.freeze(['initial-release','refined-release','small-life-release','small-fauna-release','small-life-batch-release','small-life-round02-release','small-life-round03-release','small-life-round04-release','small-life-round05-release','small-life-round06-release','small-life-round07-release','small-life-round08-release','small-life-round09-release','small-life-round10-release','small-life-round11-release','small-life-round12-release','small-life-round13-release','concept-seven-release','quartets-capture','concept-quartets-release','landair-capture','concept-landair-release']);
export const PUBLICATION_SHARD_COUNT=4;
const seal=body=>({...body,report_sha256:sha256(JSON.stringify(body))});
function assertSeal(value){
 assert(value&&typeof value==='object'&&!Array.isArray(value),'Missing evidence object');
 const {report_sha256,...body}=value;
 assert.equal(report_sha256,sha256(JSON.stringify(body)),'Evidence SHA-256 mismatch');
}
export function publicationIdentity(){
 assert.equal(git('status','--porcelain','--untracked-files=no'),'','Publication shards require unchanged tracked source');
 const source_commit=git('rev-parse','HEAD');
 if(process.env.GITHUB_SHA)assert.equal(source_commit,process.env.GITHUB_SHA,'Checkout differs from workflow source');
 return {source_commit,source_tree:git('rev-parse','HEAD^{tree}'),control_sha256:controlDigest(source_commit),
  repository:process.env.GITHUB_REPOSITORY||null,run_id:process.env.GITHUB_RUN_ID||null,run_attempt:process.env.GITHUB_RUN_ATTEMPT||null,workflow:process.env.GITHUB_WORKFLOW||null,
  runtime_config:{...runtimeConfig(),node_version:process.versions.node,python_version:execFileSync('python3',['--version'],{encoding:'utf8'}).trim()}};
}
export function createPublicationPlan(){
 const suites=PUBLICATION_SUITES.map((name,index)=>({name,path:`site/${name}-test.mjs`,sha256:sha256(readFileSync(`site/${name}-test.mjs`)),shard:index%PUBLICATION_SHARD_COUNT}));
 return seal({version:1,kind:'publication-plan',identity:publicationIdentity(),shard_count:PUBLICATION_SHARD_COUNT,suites});
}
export function assertPublicationPlan(plan){
 assertSeal(plan);
 assert.deepEqual(plan,createPublicationPlan(),'Publication plan does not match this exact checkout, control plane, runtime or run');
 return plan;
}
export function readPublicationPlan(path){return assertPublicationPlan(JSON.parse(readFileSync(path,'utf8')));}
export function publicationShardSuites(plan,index){
 assert(Number.isInteger(index)&&index>=0&&index<PUBLICATION_SHARD_COUNT,'Invalid publication shard');
 return plan.suites.filter(suite=>suite.shard===index);
}
export function createPublicationShardReport(plan,index,phases,status){
 return seal({version:1,kind:'publication-shard',identity:plan.identity,plan_sha256:plan.report_sha256,shard_count:plan.shard_count,shard_index:index,
  suites:publicationShardSuites(plan,index),phases,status});
}
export function aggregatePublicationReports(plan,reports){
 assertPublicationPlan(plan);
 assert(Array.isArray(reports)&&reports.length===PUBLICATION_SHARD_COUNT,'Missing or unexpected publication shard');
 const seen=new Set(),covered=[];
 for(const report of reports){
  assertSeal(report);
  assert.equal(report.version,1);assert.equal(report.kind,'publication-shard');
  assert.deepEqual(report.identity,plan.identity,'Shard source/control/runtime/run mismatch');
  assert.equal(report.plan_sha256,plan.report_sha256,'Shard plan hash mismatch');
  assert.equal(report.shard_count,plan.shard_count,'Shard count mismatch');
  const index=report.shard_index,expected=publicationShardSuites(plan,index);
  assert(!seen.has(index),'Duplicate publication shard');seen.add(index);
  assert.equal(report.status,'pass','Publication shard failed or incomplete');
  assert.deepEqual(report.suites,expected,'Shard suite assignment or source hash mismatch');
  assert(Array.isArray(report.phases),'Missing suite outcomes');
  assert.deepEqual(report.phases.map(phase=>phase.name),expected.map(suite=>suite.name),'Missing, duplicate, out-of-order or unexpected publication suite');
  for(const [i,phase]of report.phases.entries()){
   assert.equal(phase.exit_code,0,`${phase.name}: failed suite`);
   assert.equal(phase.signal,null,`${phase.name}: interrupted suite`);
   assert.equal(phase.script_sha256,expected[i].sha256,`${phase.name}: source hash mismatch`);
   assert(Number.isFinite(phase.seconds)&&phase.seconds>=0,`${phase.name}: invalid timing`);
   covered.push(phase.name);
  }
 }
 assert.equal(seen.size,PUBLICATION_SHARD_COUNT,'Missing publication shard');
 assert.deepEqual(covered.sort(),[...PUBLICATION_SUITES].sort(),'Publication suite coverage is not exact');
 return seal({version:1,kind:'publication-aggregate',identity:plan.identity,plan_sha256:plan.report_sha256,shard_count:plan.shard_count,
  suites:[...PUBLICATION_SUITES],shards:reports.map(report=>({shard_index:report.shard_index,report_sha256:report.report_sha256})).sort((a,b)=>a.shard_index-b.shard_index),
  status:'pass',validation:'awaiting-independent-github-conclusion'});
}
export function readPublicationShardReports(directory,plan){
 const attempt=plan.identity.run_attempt;
 assert(typeof attempt==='string'&&/^[1-9][0-9]*$/.test(attempt),'GitHub run attempt required for artifact aggregation');
 const expected=Array.from({length:PUBLICATION_SHARD_COUNT},(_,index)=>`publication-shard-${index}-${attempt}`).sort();
 assert.deepEqual(readdirSync(directory).sort(),expected,'Missing, duplicate or unexpected shard artifacts');
 return expected.map((name,index)=>{
  const folder=join(directory,name),file=`shard-${index}.json`;
  assert(lstatSync(folder).isDirectory()&&!lstatSync(folder).isSymbolicLink(),'Shard artifact must be an ordinary directory');
  assert.deepEqual(readdirSync(folder),[file],'Missing or unexpected shard artifact members');
  const path=join(folder,file);assert(lstatSync(path).isFile()&&!lstatSync(path).isSymbolicLink(),'Shard report must be an ordinary file');
  const report=JSON.parse(readFileSync(path,'utf8'));
  assert.equal(report.shard_index,index,'Shard artifact identity mismatch');return report;
 });
}
export function writePublicationEvidence(path,value){mkdirSync(dirname(path),{recursive:true});writeFileSync(path,JSON.stringify(value,null,2)+'\n');}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 const [mode,...args]=process.argv.slice(2);
 if(mode==='plan'){
  assert.equal(args.length,1,'Usage: ci-publication-shards.mjs plan OUTPUT');
  const plan=createPublicationPlan();writePublicationEvidence(args[0],plan);
  console.log(`Planned all ${plan.suites.length} unchanged publication suites across ${plan.shard_count} isolated runners.`);
 }else if(mode==='aggregate'){
  assert.equal(args.length,3,'Usage: ci-publication-shards.mjs aggregate PLAN ARTIFACT_DIRECTORY OUTPUT');
  const plan=readPublicationPlan(args[0]),aggregate=aggregatePublicationReports(plan,readPublicationShardReports(args[1],plan));
  writePublicationEvidence(args[2],aggregate);console.log(`Passed exact coverage of all ${aggregate.suites.length} publication suites; GitHub workflow success is still required.`);
 }else throw new Error('Expected publication plan or aggregate command');
}

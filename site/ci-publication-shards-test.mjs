/** Small git fixtures only: exact coverage and independent workflow gates, no asset mutation copies. */
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,readFileSync,writeFileSync,rmSync,renameSync,symlinkSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {execFileSync,spawnSync} from 'node:child_process';
import {sha256} from './ci-provenance.mjs';
import {PUBLICATION_SUITES,PUBLICATION_SHARD_COUNT,createPublicationPlan,assertPublicationPlan,publicationShardSuites,createPublicationShardReport,aggregatePublicationReports,readPublicationShardReports,writePublicationEvidence} from './ci-publication-shards.mjs';
const checkout=process.cwd(),runner=resolve('site/ci-timed.mjs'),cli=resolve('site/ci-publication-shards.mjs');
const originalEnv={...process.env},root=mkdtempSync(join(tmpdir(),'lpv-publication-shards-'));
const git=(...args)=>execFileSync('git',args,{encoding:'utf8'}).trim();
const reseal=value=>{const {report_sha256,...body}=value;return {...body,report_sha256:sha256(JSON.stringify(body))};};
const change=(value,edit)=>{const clone=structuredClone(value);edit(clone);return reseal(clone);};
let checks=0;
const rejects=fn=>{assert.throws(fn);checks++;};
try{
 process.chdir(root);
 for(const key of ['GITHUB_SHA','GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE'])delete process.env[key];
 Object.assign(process.env,{GITHUB_REPOSITORY:'fixture/publication',GITHUB_RUN_ID:'123',GITHUB_RUN_ATTEMPT:'1',GITHUB_WORKFLOW:'Fixture publication'});
 mkdirSync('site');mkdirSync('.github/workflows',{recursive:true});
 writeFileSync('.gitignore','events\nartifacts/\nqa/\nplan.json\naggregate.json\n');
 writeFileSync('.github/workflows/fixture.yml','trusted workflow\n');writeFileSync('package.json','{}');
 for(const name of PUBLICATION_SUITES)writeFileSync(`site/${name}-test.mjs`,`import {appendFileSync} from 'node:fs';appendFileSync('events',${JSON.stringify(name+'\n')});\n`);
 git('init','-q');git('config','user.name','Publication fixture');git('config','user.email','fixture@example.invalid');git('add','.');git('commit','-qm','fixture');
 process.env.GITHUB_SHA=git('rev-parse','HEAD');
 let plan=createPublicationPlan();assertPublicationPlan(plan);checks++;
 assert.equal(PUBLICATION_SHARD_COUNT,4);assert.equal(plan.suites.length,25);assert.equal(plan.suites.at(-1).name,'final-five-release');
 assert.deepEqual(Array.from({length:4},(_,index)=>publicationShardSuites(plan,index)).flat().map(suite=>suite.name).sort(),[...PUBLICATION_SUITES].sort());checks++;
 rejects(()=>publicationShardSuites(plan,-1));rejects(()=>publicationShardSuites(plan,4));rejects(()=>publicationShardSuites(plan,'0'));
 const passing=()=>Array.from({length:4},(_,index)=>createPublicationShardReport(plan,index,publicationShardSuites(plan,index).map(suite=>({name:suite.name,seconds:0.001,exit_code:0,signal:null,script_sha256:suite.sha256})),'pass'));
 let reports=passing();
 const aggregate=aggregatePublicationReports(plan,[...reports].reverse());
 assert.deepEqual(aggregate.suites,PUBLICATION_SUITES);assert.equal(aggregate.status,'pass');assert.equal(aggregate.validation,'awaiting-independent-github-conclusion');checks++;
 rejects(()=>aggregatePublicationReports(plan,reports.slice(1)));
 rejects(()=>aggregatePublicationReports(plan,[...reports,reports[0]]));
 rejects(()=>aggregatePublicationReports(plan,[reports[0],reports[0],reports[2],reports[3]]));
 for(const edit of [
  r=>r.shard_index=9,r=>r.shard_index=0.5,r=>r.shard_count=3,r=>r.kind='publication-aggregate',r=>r.version=2,
  r=>r.status='fail',r=>r.status='running',r=>r.phases.pop(),r=>r.phases.push(r.phases[0]),r=>r.phases.reverse(),
  r=>r.phases[0].name='unrequested-release',r=>r.phases[0].exit_code=1,r=>r.phases[0].exit_code=null,
  r=>r.phases[0].signal='SIGTERM',r=>r.phases[0].seconds=-1,r=>r.phases[0].seconds='0',
  r=>r.phases[0].script_sha256='0'.repeat(64),r=>r.suites[0].sha256='0'.repeat(64),r=>r.suites.pop(),
  r=>r.identity.source_commit='0'.repeat(40),r=>r.identity.source_tree='0'.repeat(40),r=>r.identity.control_sha256='0'.repeat(64),
  r=>r.identity.runtime_config.node_version='0.0.0',r=>r.identity.runtime_config.python_version='Python 0.0',
  r=>r.identity.runtime_config.site_base='/other/',r=>r.identity.run_id='124',r=>r.identity.run_attempt='2',
  r=>r.identity.repository='other/repository',r=>r.identity.workflow='Other workflow',r=>r.plan_sha256='0'.repeat(64),
 ])rejects(()=>aggregatePublicationReports(plan,[change(reports[0],edit),...reports.slice(1)]));
 rejects(()=>aggregatePublicationReports(plan,[{...reports[0],report_sha256:'0'.repeat(64)},...reports.slice(1)]));
 for(const edit of [p=>p.suites.pop(),p=>p.suites.push(p.suites[0]),p=>p.suites[0].shard=1,p=>p.identity.source_tree='0'.repeat(40),p=>p.identity.control_sha256='0'.repeat(64),p=>p.identity.runtime_config.node_major='1'])rejects(()=>assertPublicationPlan(change(plan,edit)));
 rejects(()=>assertPublicationPlan({...plan,report_sha256:'0'.repeat(64)}));
 // Run all 25 entrypoints, including fifty-two-release, in four separate sequential fixture invocations.
 writePublicationEvidence('plan.json',plan);
 for(let index=0;index<4;index++){
  const file=`artifacts/publication-shard-${index}-1/shard-${index}.json`;
  const run=spawnSync(process.execPath,[runner,'publication','--plan','plan.json','--shard',String(index),'--output',file],{encoding:'utf8'});
  assert.equal(run.status,0,run.stdout+run.stderr);
 }
 reports=readPublicationShardReports('artifacts',plan);assert.equal(aggregatePublicationReports(plan,reports).status,'pass');
 assert.deepEqual(readFileSync('events','utf8').trim().split('\n').sort(),[...PUBLICATION_SUITES].sort());checks++;
 const collected=spawnSync(process.execPath,[cli,'aggregate','plan.json','artifacts','aggregate.json'],{encoding:'utf8'});
 assert.equal(collected.status,0,collected.stdout+collected.stderr);assert.equal(JSON.parse(readFileSync('aggregate.json')).suites.length,25);checks++;
 // Filesystem aggregation must not hide duplicate or unexpected artifact members.
 writeFileSync('artifacts/extra.json','{}');rejects(()=>readPublicationShardReports('artifacts',plan));rmSync('artifacts/extra.json');
 writeFileSync('artifacts/publication-shard-0-1/extra.json','{}');rejects(()=>readPublicationShardReports('artifacts',plan));rmSync('artifacts/publication-shard-0-1/extra.json');
 renameSync('artifacts/publication-shard-0-1/shard-0.json','saved-report');rejects(()=>readPublicationShardReports('artifacts',plan));
 symlinkSync(resolve('saved-report'),'artifacts/publication-shard-0-1/shard-0.json');rejects(()=>readPublicationShardReports('artifacts',plan));rmSync('artifacts/publication-shard-0-1/shard-0.json');renameSync('saved-report','artifacts/publication-shard-0-1/shard-0.json');
 const correct=readFileSync('artifacts/publication-shard-0-1/shard-0.json');writePublicationEvidence('artifacts/publication-shard-0-1/shard-0.json',reports[1]);rejects(()=>readPublicationShardReports('artifacts',plan));writeFileSync('artifacts/publication-shard-0-1/shard-0.json',correct);
 // A failed suite stops only its runner immediately, preserves status, and cannot aggregate.
 const names=publicationShardSuites(plan,0).map(suite=>suite.name),failed=names[1];
 writeFileSync(`site/${failed}-test.mjs`,readFileSync(`site/${failed}-test.mjs`,'utf8')+'process.exit(23);\n');
 rejects(()=>assertPublicationPlan(plan));git('add','.');git('commit','-qm','fixture failure');process.env.GITHUB_SHA=git('rev-parse','HEAD');
 plan=createPublicationPlan();writePublicationEvidence('plan.json',plan);writeFileSync('events','');
 const fail=spawnSync(process.execPath,[runner,'publication','--plan','plan.json','--shard','0','--output','qa/fail.json'],{encoding:'utf8'});
 assert.equal(fail.status,23);const failedReport=JSON.parse(readFileSync('qa/fail.json'));
 assert.equal(failedReport.status,'fail');assert.deepEqual(failedReport.phases.map(phase=>phase.name),names.slice(0,2));
 assert.equal(readFileSync('events','utf8'),names.slice(0,2).join('\n')+'\n');
 rejects(()=>aggregatePublicationReports(plan,[failedReport,...passing().slice(1)]));
 rmSync(`site/${failed}-test.mjs`);writeFileSync('events','');
 const missing=spawnSync(process.execPath,[runner,'publication','--plan','plan.json','--shard','0','--output','qa/missing.json'],{encoding:'utf8'});
 assert.notEqual(missing.status,0);assert.equal(readFileSync('events','utf8'),'');checks++;
 for(const index of ['-1','4','0.5','0junk'])assert.notEqual(spawnSync(process.execPath,[runner,'publication','--plan','plan.json','--shard',index,'--output','qa/invalid.json'],{encoding:'utf8'}).status,0);
 process.chdir(checkout);
 // Fail-closed graph: the caller can never deploy while a publication shard is missing.
 const workflow=readFileSync('.github/workflows/publication-regressions.yml','utf8');
 assert.match(workflow,/workflow_call:/);assert.match(workflow,/max-parallel: 4/);assert.match(workflow,/shard: \[0, 1, 2, 3\]/);assert.match(workflow,/fail-fast: false/);
 assert.match(workflow,/shards:[\s\S]*needs: plan[\s\S]*runs-on: ubuntu-latest/);
 assert.match(workflow,/aggregate:[\s\S]*if: always\(\)[\s\S]*needs: \[plan, shards\]/);
 assert.match(workflow,/node site\/ci-timed\.mjs publication --plan/);assert.match(workflow,/node site\/ci-publication-shards\.mjs aggregate/);
 assert.match(workflow,/merge-multiple: false/);assert.match(workflow,/PLAN_RESULT: \$\{\{ needs\.plan\.result \}\}/);assert.match(workflow,/SHARDS_RESULT: \$\{\{ needs\.shards\.result \}\}/);
 assert.match(workflow,/test "\$PLAN_RESULT" = success && test "\$SHARDS_RESULT" = success/);
 assert.doesNotMatch(workflow,/continue-on-error:|steps\.reuse|npm run test:publication/);checks++;
 const pages=readFileSync('.github/workflows/pages.yml','utf8'),pipeline=readFileSync('.github/workflows/asset-pipeline.yml','utf8');
 const job=(yaml,name)=>{const body=yaml.split(`\n  ${name}:\n`)[1]||'',end=body.search(/\n  [a-zA-Z][\w-]*:/);return end===-1?body:body.slice(0,end);};
 for(const caller of [pages,pipeline]){assert.match(job(caller,'publication'),/uses: \.\/\.github\/workflows\/publication-regressions\.yml/);assert.doesNotMatch(job(caller,'publication'),/\bif:|needs:/);assert.doesNotMatch(caller,/run: npm run test:publication/);}
 assert.match(job(pages,'deploy'),/needs: \[build, publication\]/);assert.doesNotMatch(job(pages,'deploy').split('    steps:')[0],/always\(\)|continue-on-error/);assert.doesNotMatch(job(pages,'deploy'),/continue-on-error/);
 assert.doesNotMatch(pages,/node site\/ci-reuse\.mjs|node site\/ci-provenance\.mjs pages/,'Old browser-bound build reuse cannot bypass new static gates');assert.match(pages,/run: npm run build/);
 assert.match(pipeline,/workflow_dispatch:/);assert.match(pipeline,/branches: \[main, 'quality\/\*\*'\]/);
 assert.match(pipeline,/site\/ci-publication-shards\*\.mjs/);assert.match(pipeline,/\.github\/workflows\/publication-regressions\.yml/);checks++;
 assert.equal(JSON.parse(readFileSync('package.json')).scripts['test:publication'],'node site/ci-timed.mjs publication');checks++;
 console.log(`Publication shards: ${checks} fixture checks passed; exact 25-suite coverage, four isolated runners, first failure, source/control/runtime/hash rejection and mandatory deployment gate.`);
}finally{
 process.chdir(checkout);
 for(const key of Object.keys(process.env))if(!(key in originalEnv))delete process.env[key];
 Object.assign(process.env,originalEnv);rmSync(root,{recursive:true,force:true});
}

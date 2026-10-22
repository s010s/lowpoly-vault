/** Offline API/provenance contracts only. No network/model/quality acceptance. */
import assert from 'node:assert/strict';
import {mkdtempSync,writeFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {fetchVerifiedProductionBase,authenticatedProductionBase} from './ci-production-baseline.mjs';

const root=mkdtempSync(join(tmpdir(),'production-base-auth-'));
const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
git('init','-q');git('config','user.name','Offline fixture');git('config','user.email','fixture@example.invalid');
writeFileSync(join(root,'input'),'base');git('add','.');git('commit','-qm','base');
const baseSha=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}');
writeFileSync(join(root,'addition'),'new');git('add','.');git('commit','-qm','head');
const currentSha=git('rev-parse','HEAD'),repository='fixture/repo',repositoryId=100,workflowId=200,runId=300,attemptId=2,suiteId=400,jobId=500;
const context={root,repository,baseSha,currentSha};
const run={id:runId,run_attempt:attemptId,check_suite_id:suiteId,event:'push',head_branch:'main',head_sha:baseSha,status:'completed',conclusion:'success',path:'.github/workflows/pages.yml',workflow_id:workflowId,repository:{id:repositoryId,full_name:repository},head_repository:{id:repositoryId,full_name:repository}};
const steps=['Validate production science, source, standard GLB and final media','All six mandatory production/static build phases','Complete non-browser source and delivery contracts'].map((name,index)=>({name,number:10+index,status:'completed',conclusion:'success'}));
const job={id:jobId,name:'build',run_id:runId,run_attempt:attemptId,head_sha:baseSha,status:'completed',conclusion:'success',steps};
const runList=`actions/workflows/${workflowId}/runs?branch=main&event=push&head_sha=${baseSha}&status=success&per_page=100`;
const jobList=`actions/runs/${runId}/attempts/${attemptId}/jobs?per_page=100`;
const responses=()=>new Map([
 ['',{id:repositoryId,full_name:repository,default_branch:'main'}],
 ['git/ref/heads/main',{ref:'refs/heads/main',object:{type:'commit',sha:baseSha}}],
 [`git/commits/${baseSha}`,{sha:baseSha,tree:{sha:tree}}],
 ['actions/workflows/pages.yml',{id:workflowId,path:'.github/workflows/pages.yml',name:'Validate and deploy asset gallery',state:'active'}],
 [runList,{workflow_runs:[run]}],
 [`actions/runs/${runId}`,run],
 [`actions/runs/${runId}/attempts/${attemptId}`,run],
 [`check-suites/${suiteId}`,{id:suiteId,head_sha:baseSha,status:'completed',conclusion:'success',app:{slug:'github-actions',id:15368,owner:{login:'github'}}}],
 [jobList,{total_count:1,jobs:[job]}],
 [`actions/jobs/${jobId}`,job]
].map(([path,value])=>[path,structuredClone(value)]));
let count=0;
async function test(name,mutate=()=>{},accept=false){
 const map=responses(),calls=[];const settings={...context,token:'offline-fixture-not-a-secret',timeoutMs:5000,onTiming:()=>{}};
 mutate(map,settings);
 settings.fetchImpl=async(url,options)=>{
  const prefix=`https://api.github.com/repos/${repository}`,path=url===prefix?'':url.slice(prefix.length+1);
  assert(url===prefix||url.startsWith(prefix+'/'));assert.equal(options.redirect,'error');assert.equal(options.headers.Authorization,'Bearer offline-fixture-not-a-secret');calls.push(path);
  if(settings.hang)return new Promise(()=>{});
  if(settings.transportError)throw Error('simulated failure');
  assert(map.has(path),'Unexpected API request '+path);
  let body=structuredClone(map.get(path));
  if(settings.transform)body=settings.transform(path,body,calls);
  return {ok:!settings.httpError,status:settings.httpError||200,json:async()=>body};
 };
 const found=await fetchVerifiedProductionBase(settings);
 if(accept){assert(found.capability,name+': capability missing '+found.reasons.join('; '));assert.equal(authenticatedProductionBase(found.capability,context).run_id,runId);assert.throws(()=>authenticatedProductionBase(found.summary,context));assert.throws(()=>authenticatedProductionBase(structuredClone(found.capability),context));assert.throws(()=>authenticatedProductionBase(found.capability,{...context,baseSha:'a'.repeat(40)}));assert.throws(()=>authenticatedProductionBase(found.capability,{...context,repository:'other/repo'}));}
 else{assert.equal(found.capability,null,name+': untrusted base accepted');assert.equal(found.summary,null);assert(found.reasons.length>0);}
 console.log('PASS '+name);count++;
 return {found,calls};
}
try{
 await test('exact successful main production run mints bound opaque capability',()=>{},true);
 await test('no token cannot authenticate',(m,s)=>{s.token='';});
 await test('API error fails closed',(m,s)=>{s.httpError=403;});
 await test('transport error fails closed',(m,s)=>{s.transportError=true;});
 await test('total budget rejects nonsettling transport',(m,s)=>{s.timeoutMs=30;s.hang=true;});
 await test('wrong repository numeric identity',(m)=>{m.get(`actions/runs/${runId}`).repository.id++;});
 await test('fork baseline',(m)=>{m.get(`actions/runs/${runId}`).head_repository.id++;});
 await test('wrong source SHA',(m)=>{m.get(`actions/runs/${runId}`).head_sha='a'.repeat(40);});
 await test('PR run is not a full main baseline',(m)=>{m.get(`actions/runs/${runId}`).event='pull_request';});
 await test('manual dispatch is not a full main baseline',(m)=>{m.get(`actions/runs/${runId}`).event='workflow_dispatch';});
 await test('nonmain branch',(m)=>{m.get(`actions/runs/${runId}`).head_branch='feature';});
 await test('wrong workflow path',(m)=>{m.get(`actions/runs/${runId}`).path='.github/workflows/other.yml';});
 await test('wrong workflow ID',(m)=>{m.get(`actions/runs/${runId}`).workflow_id++;});
 await test('failed latest run',(m)=>{m.get(`actions/runs/${runId}`).conclusion='failure';});
 await test('attempt mismatch',(m)=>{m.get(`actions/runs/${runId}/attempts/${attemptId}`).run_attempt++;});
 await test('attempt suite mismatch',(m)=>{m.get(`actions/runs/${runId}/attempts/${attemptId}`).check_suite_id++;});
 await test('non-GitHub suite app',(m)=>{m.get(`check-suites/${suiteId}`).app.id=1;});
 await test('suite belongs to another source',(m)=>{m.get(`check-suites/${suiteId}`).head_sha='a'.repeat(40);});
 await test('base Git/API tree mismatch',(m)=>{m.get(`git/commits/${baseSha}`).tree.sha='a'.repeat(40);});
 await test('skipped production step',(m)=>{m.get(`actions/jobs/${jobId}`).steps[0].conclusion='skipped';});
 await test('failed build step',(m)=>{m.get(`actions/jobs/${jobId}`).steps[1].conclusion='failure';});
 await test('missing delivery step',(m)=>{m.get(`actions/jobs/${jobId}`).steps.pop();});
 await test('duplicate production step',(m)=>{m.get(`actions/jobs/${jobId}`).steps.push({...steps[0],number:20});});
 await test('job from other attempt',(m)=>{m.get(`actions/jobs/${jobId}`).run_attempt++;});
 await test('job from other SHA',(m)=>{m.get(`actions/jobs/${jobId}`).head_sha='a'.repeat(40);});
 await test('incomplete paginated jobs',(m)=>{m.get(jobList).total_count=101;});
 await test('ambiguous build jobs',(m)=>{m.get(jobList).jobs.push({...job,id:501});m.get(jobList).total_count=2;});
 await test('new rerun invalidates authentication snapshot',(m,s)=>{s.transform=(path,body,calls)=>{if(path===`actions/runs/${runId}`&&calls.filter(p=>p===path).length===2)body.run_attempt++;return body;};});
 await test('missing successful exact base cannot use other commit',(m)=>{m.set(runList,{workflow_runs:[{...run,head_sha:'a'.repeat(40)}]});});
 await test('base not on independently verified main',(m)=>{m.get('git/ref/heads/main').object.sha='b'.repeat(40);m.set(`compare/${baseSha}...${'b'.repeat(40)}`,{status:'diverged',merge_base_commit:{sha:'c'.repeat(40)}});});
 await test('main advances but authenticated base remains ancestor',(m)=>{m.get('git/ref/heads/main').object.sha='b'.repeat(40);m.set(`compare/${baseSha}...${'b'.repeat(40)}`,{status:'ahead',merge_base_commit:{sha:baseSha}});},true);
 const replacement=git('commit-tree',git('rev-parse','HEAD^{tree}'),'-m','unrelated replacement');git('replace',baseSha,replacement);
 assert.notEqual(git('rev-parse',`${baseSha}^{tree}`),tree);
 await test('Git replace refs cannot substitute the authenticated base tree',()=>{},true);git('replace','-d',baseSha);
 const {found}=await test('post-auth clean state is rechecked',()=>{},true);writeFileSync(join(root,'input'),'tampered');assert.throws(()=>authenticatedProductionBase(found.capability,context));git('checkout','--','input');
 console.log(`${count} offline authentication cases passed; no network requests or real quality acceptance.`);
}finally{rmSync(root,{recursive:true,force:true});}

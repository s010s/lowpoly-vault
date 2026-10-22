/** Exact-base production trust comes from GitHub Actions, never checkout JSON.
 * This authenticates execution provenance only. Callers must still prove the
 * complete unchanged source/control closure and always-run global invariants.
 * It never authorizes publication or treats reuse as a newly executed PASS.
 */
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {resolve} from 'node:path';
import {proofGet} from './ci-proof-fetch.mjs';
import {proofReadBudget} from './ci-proof-budget.mjs';
import {immutableGitEnv} from './ci-git.mjs';

const WORKFLOW_PATH='.github/workflows/pages.yml';
const WORKFLOW_NAME='Validate and deploy asset gallery';
const REQUIRED_STEPS=Object.freeze([
 'Validate production science, source, standard GLB and final media',
 'All six mandatory production/static build phases',
 'Complete non-browser source and delivery contracts'
]);
const SHA=/^[a-f0-9]{40}$/;
const exactSha=x=>typeof x==='string'&&SHA.test(x)&&!/^0+$/.test(x);
const positive=x=>Number.isSafeInteger(x)&&x>0;
const capabilities=new WeakMap();
const git=(root,budget,...args)=>execFileSync('git',args,{cwd:root,env:immutableGitEnv(),encoding:'utf8',stdio:['ignore','pipe','pipe'],timeout:budget?.remaining(),maxBuffer:16*1024*1024}).trim();

function assertRun(run,{repository,repositoryId,baseSha,workflowId}){
 assert(run&&positive(run.id)&&positive(run.run_attempt)&&positive(run.check_suite_id),'Incomplete run identity');
 assert.equal(run.event,'push','Only full main-push production checks establish a baseline');
 assert.equal(run.head_branch,'main');assert.equal(run.head_sha,baseSha);
 assert.equal(run.status,'completed');assert.equal(run.conclusion,'success');
 assert.equal(run.path,WORKFLOW_PATH);assert.equal(run.workflow_id,workflowId);
 for(const key of ['repository','head_repository']){assert.equal(run[key]?.full_name,repository);assert.equal(run[key]?.id,repositoryId);}
}
function assertSuite(suite,run){
 assert.equal(suite.id,run.check_suite_id);assert.equal(suite.head_sha,run.head_sha);
 assert.equal(suite.status,'completed');assert.equal(suite.conclusion,'success');
 assert.equal(suite.app?.slug,'github-actions');assert.equal(suite.app?.id,15368);assert.equal(suite.app?.owner?.login,'github');
}
function assertJob(job,run){
 assert(positive(job.id),'Missing production job identity');assert.equal(job.name,'build');
 assert.equal(job.run_id,run.id);assert.equal(job.run_attempt,run.run_attempt);assert.equal(job.head_sha,run.head_sha);
 assert.equal(job.status,'completed');assert.equal(job.conclusion,'success');assert(Array.isArray(job.steps));
 const numbers=[];
 for(const name of REQUIRED_STEPS){const matches=job.steps.filter(step=>step.name===name);assert.equal(matches.length,1,'Missing or ambiguous mandatory production step: '+name);const step=matches[0];assert.equal(step.status,'completed');assert.equal(step.conclusion,'success');assert(positive(step.number));numbers.push(step.number);}
 assert(numbers.every((number,index)=>index===0||number>numbers[index-1]),'Mandatory production step order changed');
}

/** No exported pure-data validator can mint a capability. fetchImpl replaces
 * transport for offline tests only and still traverses every API validation. */
export async function fetchVerifiedProductionBase({root=process.cwd(),repository=process.env.GITHUB_REPOSITORY,baseSha,currentSha=process.env.GITHUB_SHA,token=process.env.GITHUB_TOKEN,fetchImpl=fetch,timeoutMs=60000,onTiming}={}){
 const reasons=[];root=resolve(root);
 try{
  assert(exactSha(baseSha)&&exactSha(currentSha),'Exact nonzero base/current commit required');
  assert(typeof repository==='string'&&/^[\w.-]+\/[\w.-]+$/.test(repository),'Exact repository required');
  assert(typeof token==='string'&&token.length>0,'Read-only GitHub proof token unavailable');
  const budget=proofReadBudget(timeoutMs,{maximumMs:60000,onTiming});
  const head=()=>git(root,budget,'rev-parse','HEAD');
  assert.equal(head(),currentSha,'Current checkout changed');assert.equal(git(root,budget,'status','--porcelain','--untracked-files=no'),'','Dirty tracked checkout');
  git(root,budget,'merge-base','--is-ancestor',baseSha,currentSha);
  const baseTree=git(root,budget,'rev-parse',`${baseSha}^{tree}`),currentTree=git(root,budget,'rev-parse',`${currentSha}^{tree}`);
  const headers={Authorization:`Bearer ${token}`,Accept:'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'};
  const api=path=>budget.measureAsync(`production API ${path.split('?')[0]||'repository'}`,async()=>{
   const stage=`production API ${path.split('?')[0]||'repository'}`;
   const response=await proofGet(`https://api.github.com/repos/${repository}${path?'/'+path:''}`,{headers,signal:budget.signal,redirect:'error'},{fetchImpl,stage,checkBudget:budget.check});
   assert(response.ok,`GitHub production proof read failed (${response.status})`);
   return response.json();
  });
  const repo=await api('');assert.equal(repo.full_name,repository);assert.equal(repo.default_branch,'main');assert(positive(repo.id));
  const main=await api('git/ref/heads/main');assert.equal(main.ref,'refs/heads/main');assert.equal(main.object?.type,'commit');assert(exactSha(main.object.sha));
  if(main.object.sha!==baseSha){const comparison=await api(`compare/${baseSha}...${main.object.sha}`);assert(['ahead','identical'].includes(comparison.status));assert.equal(comparison.merge_base_commit?.sha,baseSha,'Base is not independently proven on main');}
  const source=await api(`git/commits/${baseSha}`);assert.equal(source.sha,baseSha);assert.equal(source.tree?.sha,baseTree,'API and original Git base trees differ');
  const workflow=await api('actions/workflows/pages.yml');assert.equal(workflow.path,WORKFLOW_PATH);assert.equal(workflow.name,WORKFLOW_NAME);assert.equal(workflow.state,'active');assert(positive(workflow.id));
  const listed=await api(`actions/workflows/${workflow.id}/runs?branch=main&event=push&head_sha=${baseSha}&status=success&per_page=100`);
  assert(Array.isArray(listed.workflow_runs),'Missing workflow run list');
  const candidates=listed.workflow_runs.filter(run=>run.head_sha===baseSha&&positive(run.id)).slice(0,100);
  for(const summary of candidates){
   budget.check();
   try{
    const expected={repository,repositoryId:repo.id,baseSha,workflowId:workflow.id};
    const run=await api(`actions/runs/${summary.id}`);assert.equal(run.id,summary.id);assertRun(run,expected);
    const attempt=await api(`actions/runs/${run.id}/attempts/${run.run_attempt}`);assertRun(attempt,expected);
    for(const key of ['id','run_attempt','check_suite_id','event'])assert.equal(attempt[key],run[key],'Run attempt identity differs');
    assertSuite(await api(`check-suites/${run.check_suite_id}`),run);
    const jobs=await api(`actions/runs/${run.id}/attempts/${run.run_attempt}/jobs?per_page=100`);
    assert(Array.isArray(jobs.jobs)&&Number.isSafeInteger(jobs.total_count)&&jobs.total_count===jobs.jobs.length&&jobs.total_count<=100,'Incomplete job list');
    const builds=jobs.jobs.filter(job=>job.name==='build');assert.equal(builds.length,1,'Missing or ambiguous build job');
    // Re-read the exact job, so a list item alone is not sufficient evidence.
    assert(positive(builds[0].id));const job=await api(`actions/jobs/${builds[0].id}`);assert.equal(job.id,builds[0].id);assertJob(job,run);
    // A rerun started while authenticating invalidates this snapshot.
    const latest=await api(`actions/runs/${run.id}`);assertRun(latest,expected);
    for(const key of ['id','run_attempt','check_suite_id'])assert.equal(latest[key],run[key],'Run changed during authentication');
    assert.equal(head(),currentSha);assert.equal(git(root,budget,'status','--porcelain','--untracked-files=no'),'','Tracked input changed during authentication');
    const summaryProof={kind:'github-exact-main-production-baseline-v1',repository,repository_id:repo.id,source_commit:baseSha,source_tree:baseTree,current_commit:currentSha,current_tree:currentTree,workflow_id:workflow.id,workflow_path:WORKFLOW_PATH,run_id:run.id,run_attempt:run.run_attempt,check_suite_id:run.check_suite_id,job_id:job.id,steps:[...REQUIRED_STEPS],publication_authorized:false};
    const capability=Object.freeze({});capabilities.set(capability,{root,baseSha,currentSha,repository,summary:summaryProof});
    return {capability,summary:structuredClone(summaryProof),reasons};
   }catch(error){reasons.push(`Production run ${summary.id} rejected: ${error.message}`);budget.check();}
  }
  throw Error('No authenticated successful exact-base full main production run');
 }catch(error){return {capability:null,summary:null,reasons:[...reasons,error.message]};}
}

export function authenticatedProductionBase(capability,{root=process.cwd(),repository=process.env.GITHUB_REPOSITORY,baseSha,currentSha=process.env.GITHUB_SHA}={}){
 const state=capabilities.get(capability);root=resolve(root);
 assert(state&&state.root===root&&state.repository===repository&&state.baseSha===baseSha&&state.currentSha===currentSha,'Baseline requires exact process-local GitHub authentication, never JSON');
 assert.equal(git(root,null,'rev-parse','HEAD'),currentSha,'Authenticated checkout changed');
 assert.equal(git(root,null,'status','--porcelain','--untracked-files=no'),'','Authenticated tracked inputs changed');
 return structuredClone(state.summary);
}

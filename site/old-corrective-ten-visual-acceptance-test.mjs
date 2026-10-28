/** Synthetic API envelopes test checks only, never stand in for GitHub authentication. */
import test from'node:test';import assert from'node:assert/strict';
import {readFileSync}from'node:fs';import{createHash}from'node:crypto';
import{CORRECTIVE_BASE_ACCEPTANCE as P,CORRECTIVE_CONTRACT_PATHS,CORRECTIVE_RUNNER_PINS,assertCorrectiveRunnerBytes,assertCorrectiveBaselineRun as checkRun,assertCorrectiveBaselineJob as checkJob,assertCorrectiveBaselineArtifact as checkArtifact,assertCorrectiveBaselineAcceptance,downloadCorrectiveBaselineArchive}from'./old-corrective-ten-visual-acceptance.mjs';
import{main842PosterSource}from'./gallery-main842-compat.mjs';
const names=['Run actions/checkout@v4','Run npm ci','Run affected regressions','Validate source, build once and audit final dist','Install pinned browser for mandatory right-detail first-frame acceptance','Authenticated same-runtime evidence and explicit independent visual acceptance','Retain supplemental right-detail pixels outside Git','Stamp exact source build after all six mandatory audit phases'];
const run={id:P.run,run_attempt:1,head_sha:P.source,head_branch:'main',event:'push',path:P.workflow_path,workflow_id:P.workflow,check_suite_id:P.suite,status:'completed',conclusion:'success',repository:{id:P.repository_id,full_name:P.repository},head_repository:{id:P.repository_id,full_name:P.repository}},job={id:P.job,run_id:P.run,run_attempt:1,head_sha:P.source,name:'build',status:'completed',conclusion:'success',steps:names.map(name=>({name,conclusion:'success',started_at:'2026-10-27T15:00:00Z',completed_at:'2026-10-27T15:01:00Z'}))},artifact={id:P.artifact,name:P.artifact_name,expired:false,size_in_bytes:P.zip_bytes,digest:'sha256:'+P.zip_sha256,workflow_run:{id:P.run,head_sha:P.source,head_branch:'main',repository_id:P.repository_id,head_repository_id:P.repository_id},created_at:'2026-10-27T15:00:30Z'};
test('fixed accepted baseline requires exact run, successful job, artifact and historical status seals',()=>{
 checkRun(run);checkJob(job);checkArtifact(artifact,job);
 for(const [value,fn,keys]of [[run,checkRun,['id','run_attempt','head_sha','head_branch','event','path','workflow_id','check_suite_id','status','conclusion']],[job,checkJob,['id','run_id','run_attempt','head_sha','name','status','conclusion']],[artifact,x=>checkArtifact(x,job),['id','name','expired','size_in_bytes','digest','created_at']]])for(const key of keys){const x=structuredClone(value);x[key]=typeof x[key]==='number'?x[key]+1:typeof x[key]==='boolean'?!x[key]:'wrong';assert.throws(()=>fn(x));}
 for(const name of names){const x=structuredClone(job);x.steps.find(s=>s.name===name).conclusion='skipped';assert.throws(()=>checkJob(x));}
 assert.throws(()=>assertCorrectiveBaselineAcceptance(Buffer.from('{}')));
 assert.equal(new Set(CORRECTIVE_CONTRACT_PATHS).size,CORRECTIVE_CONTRACT_PATHS.length);assert(!CORRECTIVE_CONTRACT_PATHS.some(p=>p.includes('renderer.js')||p.startsWith('.github/')));
});
test('fixed archive download rejects unsafe redirect and strips token from body request',async()=>{
 for(const url of ['http://example.com/x','https://evil.example/x','https://user:secret@x.blob.core.windows.net/x'])await assert.rejects(downloadCorrectiveBaselineArchive({token:'UNIT_TOKEN',fetchImpl:async()=>new Response(null,{status:302,headers:{location:url}})}));
 const calls=[];await assert.rejects(downloadCorrectiveBaselineArchive({token:'UNIT_TOKEN',fetchImpl:async(url,opts)=>{calls.push({url,opts});return calls.length===1?new Response(null,{status:302,headers:{location:'https://unit.blob.core.windows.net/x'}}):new Response('short');}}));assert.equal(calls.length,2);assert.equal(calls[1].opts.headers,undefined);assert.equal(calls[1].opts.redirect,'error');
 await assert.rejects(downloadCorrectiveBaselineArchive({token:'UNIT_TOKEN',timeoutMs:180001,fetchImpl:()=>{throw Error('must not fetch')}}));
});
test('old poster recipe strips only literal corrective dispatch, retaining old byte proof',()=>{
 const source=readFileSync('site/gallery-poster-inputs.mjs','utf8'),stripped=main842PosterSource(source),hash=s=>createHash('sha256').update(s).digest('hex');
 // This immutable pre-main842 source identity is already required by its original recipe.
 const base=readFileSync('site/gallery-main842-compat.mjs','utf8');assert(!stripped.includes('old-corrective-ten-selection.mjs'));
 assert.notEqual(hash(main842PosterSource(source+'\n// unreviewed tail')),hash(stripped));
 const changed=source.replace('await verifyCorrectivePresentation(root,context);','/* skipped */');assert.notEqual(hash(main842PosterSource(changed)),hash(stripped));assert(base.includes('MAIN842_POSTER_RECIPE'));
});

test('only exact historical-card test and two one-line runner repairs are classified',()=>{
 assert.equal(CORRECTIVE_CONTRACT_PATHS.length,30);
 assert.equal(CORRECTIVE_CONTRACT_PATHS.filter(p=>p==='site/historical-media-comparison-test.mjs').length,1);
 assert(!CORRECTIVE_CONTRACT_PATHS.includes('site/unreviewed-test.mjs'));
 assert.deepEqual(Object.keys(CORRECTIVE_RUNNER_PINS),['.github/workflows/publication-poster-capture.yml','.github/workflows/postrelease-fixture-regression.yml']);
 for(const path of Object.keys(CORRECTIVE_RUNNER_PINS)){
  const bytes=readFileSync(new URL('../'+path,import.meta.url)),before=Buffer.from(bytes.toString().replace('runs-on: ubuntu-24.04','runs-on: ubuntu-latest'));
  assertCorrectiveRunnerBytes(path,bytes,before);
  for(const bad of [before,Buffer.from(bytes.toString().replace('contents: read','contents: write')),Buffer.concat([bytes,Buffer.from('\n# unreviewed')])])assert.throws(()=>assertCorrectiveRunnerBytes(path,bad,before));
  assert.throws(()=>assertCorrectiveRunnerBytes(path,bytes,Buffer.concat([before,Buffer.from('\n')])));
  assert.throws(()=>assertCorrectiveRunnerBytes('.github/workflows/other.yml',bytes,before));
 }
});

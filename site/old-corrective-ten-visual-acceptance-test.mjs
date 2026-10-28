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

test('only exact contract files including static delivery and two literal runner repairs are classified',()=>{
 assert.equal(CORRECTIVE_CONTRACT_PATHS.length,33);
 assert.equal(CORRECTIVE_CONTRACT_PATHS.filter(p=>p==='site/historical-media-comparison-test.mjs').length,1);
 assert.equal(CORRECTIVE_CONTRACT_PATHS.filter(p=>p==='site/detail-visual-disposition-test.mjs').length,1);
 assert.equal(CORRECTIVE_CONTRACT_PATHS.filter(p=>p==='site/turntable-delivery.mjs').length,1);
 assert.equal(CORRECTIVE_CONTRACT_PATHS.filter(p=>p==='site/turntable-delivery-test.mjs').length,1);
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

import{execFileSync}from'node:child_process';
import{immutableGitEnv}from'./ci-git.mjs';
import{CORRECTIVE_CODE_PARENT,CORRECTIVE_CODE_BASE,CORRECTIVE_CODE_BEFORE,CORRECTIVE_CODE_REVISION_PATH,CORRECTIVE_CODE_REVIEW_PATH,assertCorrectiveCodeRevision}from'./old-corrective-ten-visual-acceptance.mjs';
const digest=b=>createHash('sha256').update(b).digest('hex'),encode=x=>Buffer.from(JSON.stringify(x,null,2)+'\n');
function codeRevisionFixture(){
 const parentRead=p=>execFileSync('git',['show',CORRECTIVE_CODE_PARENT.tree+':'+p],{env:immutableGitEnv(),maxBuffer:8*1024*1024}),data=new Map(CORRECTIVE_CODE_BEFORE.map(p=>[p.path,readFileSync(p.path)]));
 const revision={schema_version:1,kind:'exact-corrective-code-revision-v1',parent:{...CORRECTIVE_CODE_PARENT},base_ledger:{...CORRECTIVE_CODE_BASE.ledger},base_review:{...CORRECTIVE_CODE_BASE.review},producer:{id:'test-code-author',task_id:'test-code-author'},changes:CORRECTIVE_CODE_BEFORE.map(p=>({path:p.path,before:{sha256:p.sha256,bytes:p.bytes},after:{sha256:digest(data.get(p.path)),bytes:data.get(p.path).length},mode:'100644'})),publication_authorized:false};
 const revisionReview={schema_version:1,kind:'independent-corrective-code-revision-v1',status:'PASS_BOUNDED_CODE_REVISION_AND_PRESERVED_BASE',reviewer:{id:'test-independent-reviewer',task_id:'test-independent-reviewer'},revision_sha256:digest(encode(revision)),parent:{...CORRECTIVE_CODE_PARENT},checks:Object.fromEntries(['immutable_parent_and_complete_base_ledger','exact_five_code_delta_and_modes','unchanged_source_model_image_and_runtime','independent_code_and_negative_tests','all_existing_dist_and_public_gates_preserved'].map(k=>[k,'PASS'])),execution_status:{current_ci:'NOT_RUN_BY_CODE_REVIEW',public:'NOT_RUN_BY_CODE_REVIEW'},blocking_findings:[],publication_authorized:false};
 const revisionChanges=[...CORRECTIVE_CODE_BEFORE.map(p=>({path:p.path,status:'M',before_mode:'100644',after_mode:'100644'})),...[CORRECTIVE_CODE_REVISION_PATH,CORRECTIVE_CODE_REVIEW_PATH].map(path=>({path,status:'A',before_mode:null,after_mode:'100644'}))].sort((a,b)=>a.path.localeCompare(b.path));
 const fixture={revision,revisionReview,revisionChanges,parentRead,context:{entries:[{receipt:{maker:{id:'test-model-maker',task_id:'test-model-maker'}}}]},data};
 fixture.sync=()=>{data.set(CORRECTIVE_CODE_REVISION_PATH,encode(revision));data.set(CORRECTIVE_CODE_REVIEW_PATH,encode(revisionReview));};
 fixture.read=p=>data.has(p)?data.get(p):parentRead(p);fixture.check=()=>{fixture.sync();return assertCorrectiveCodeRevision(fixture);};return fixture;
}
test('code-only revision verifies immutable parent originals and exactly five current files without copying asset references',()=>{
 const f=codeRevisionFixture(),r=f.check();assert.equal(r.code_files,5);assert.equal(r.parent,CORRECTIVE_CODE_PARENT.commit);
 assert.equal(f.revision.changes.length,5);assert(f.revision.changes.every(r=>r.path.startsWith('site/')&&r.path.endsWith('.mjs')));
 assert.equal(f.parentRead(CORRECTIVE_CODE_BASE.ledger.path).length,54989);assert.equal(f.parentRead(CORRECTIVE_CODE_BASE.review.path).length,6823);
});
test('code-only revision rejects base/bytes/identity/scope/order/mode/removal/rename and stale reviews',()=>{
 const cases=[
 f=>{f.parentRead=()=>{throw new Error('missing immutable parent object');};},
 f=>f.revision.parent.commit='0'.repeat(40),f=>f.revision.parent.tree='0'.repeat(40),
 f=>f.revision.base_ledger.sha256='0'.repeat(64),f=>f.revision.base_review.bytes++,
 f=>f.data.set(CORRECTIVE_CODE_BASE.ledger.path,Buffer.from('{}')),f=>f.data.set(CORRECTIVE_CODE_BASE.review.path,Buffer.from('{}')),
 f=>{const old=f.parentRead;f.parentRead=p=>p===CORRECTIVE_CODE_BEFORE[0].path?Buffer.from('not parent'):old(p);},
 f=>f.revision.changes.pop(),f=>f.revision.changes.push(f.revision.changes[0]),f=>f.revision.changes.reverse(),f=>f.revision.changes[0].path='site/other.mjs',
 f=>f.revision.changes[0].before.sha256='0'.repeat(64),f=>f.revision.changes[0].before.bytes++,f=>f.revision.changes[0].after.bytes++,f=>f.revision.changes[0].after.sha256='0'.repeat(64),f=>f.revision.changes[0].mode='100755',
 f=>f.data.set(CORRECTIVE_CODE_BEFORE[0].path,Buffer.from('changed after review')),
 f=>f.revisionChanges.pop(),f=>f.revisionChanges.push(f.revisionChanges[0]),f=>f.revisionChanges.push({path:'site/other.mjs',status:'M',before_mode:'100644',after_mode:'100644'}),
 f=>f.revisionChanges[2].status='D',f=>f.revisionChanges[2].status='R100',f=>f.revisionChanges[2].after_mode='100755',f=>f.revisionChanges[2].before_mode='120000',
 f=>f.revisionReview.revision_sha256='0'.repeat(64),f=>f.revisionReview.parent.commit='0'.repeat(40),f=>f.revisionReview.status='PASS',
 f=>f.revisionReview.reviewer={id:'/root/test-code-author',task_id:'test-code-author'},
 f=>f.revisionReview.reviewer={id:'test-independent-reviewer',task_id:'test-code-author'},
 f=>f.revisionReview.reviewer={id:'test-model-maker',task_id:'/root/test-model-maker'},
 f=>f.revisionReview.checks.all_existing_dist_and_public_gates_preserved='NOT_RUN',f=>delete f.revisionReview.checks.exact_five_code_delta_and_modes,
 f=>f.revisionReview.execution_status.current_ci='PASS',f=>f.revisionReview.blocking_findings=['unresolved'],f=>f.revisionReview.publication_authorized=true,
 f=>f.revision.publication_authorized=true,f=>f.revision.asset_references=['extra'],f=>f.revisionReview.allow_any_hash=true,
 f=>{const read=f.read;f.read=p=>p===CORRECTIVE_CODE_REVIEW_PATH?Buffer.from('{}'):read(p);},
 f=>{const read=f.read;f.read=p=>p===CORRECTIVE_CODE_REVISION_PATH?Buffer.concat([read(p),Buffer.from(' ')]):read(p);}
 ];
 for(const [i,mutate]of cases.entries()){const f=codeRevisionFixture();mutate(f);assert.throws(()=>f.check(),`negative ${i}`);}
 assert.equal(cases.length,41);
});

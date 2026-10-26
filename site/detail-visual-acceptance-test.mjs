import assert from 'node:assert/strict';
import {VISUAL_REVIEW as p,assertRuntimeDiff,assertRun,assertJob,assertArtifact,assertAcceptedDeployment,compareRuntimeTrees,ACCEPTANCE_CONTROL_HASHES,assertAcceptanceControls} from './detail-visual-acceptance.mjs';
let count=0;const test=(name,fn)=>{fn();count++;console.log('PASS '+name);};
const run={id:p.run,run_attempt:1,head_sha:p.head,head_branch:'fix/right-preview-repair-20261025',workflow_id:p.workflow,path:'.github/workflows/pages.yml',event:'pull_request',status:'completed',conclusion:'failure',check_suite_id:p.suite,repository:{id:p.repository_id,full_name:p.repository},head_repository:{id:p.repository_id,full_name:p.repository}};
const job={id:p.job,run_id:p.run,run_attempt:1,head_sha:p.head,name:'build',status:'completed',conclusion:'failure',steps:['Run actions/checkout@v4','Run actions/setup-node@v4','Run npm ci','Run affected regressions','Validate source, build once and audit final dist','Install pinned browser for mandatory right-detail first-frame acceptance','Retain supplemental right-detail pixels outside Git'].map(name=>({name,conclusion:'success',started_at:'2026-10-26T03:53:40Z',completed_at:'2026-10-26T03:54:01Z'})).concat([{name:'Actual built-page right poster and native first-frame parity',conclusion:'failure'}])};
const artifact={id:p.artifact,name:`right-detail-dist-${p.source}-${p.run}-1`,expired:false,size_in_bytes:p.zip_bytes,digest:'sha256:'+p.zip_sha256,workflow_run:{id:p.run,head_sha:p.head,repository_id:p.repository_id,head_repository_id:p.repository_id,head_branch:'fix/right-preview-repair-20261025'},created_at:'2026-10-26T03:54:01Z'};
test('exact original failed run/job/artifact accepted as evidence, not a pass',()=>{assertRun(run);assertJob(job);assertArtifact(artifact,job);});
for(const key of ['id','run_attempt','head_sha','head_branch','workflow_id','path','event','status','conclusion','check_suite_id'])test('reject changed run '+key,()=>{const d=structuredClone(run);d[key]=typeof d[key]==='number'?d[key]+1:'changed';assert.throws(()=>assertRun(d));});
for(const key of ['id','run_id','run_attempt','head_sha','name','status','conclusion'])test('reject changed job '+key,()=>{const d=structuredClone(job);d[key]='changed';assert.throws(()=>assertJob(d));});
test('cannot forgive source/build or additional failures',()=>{const d=structuredClone(job);d.steps[4].conclusion='failure';assert.throws(()=>assertJob(d));});
test('missing mandatory prior step fails',()=>{const d=structuredClone(job);d.steps.splice(4,1);assert.throws(()=>assertJob(d));});
for(const key of ['id','name','expired','size_in_bytes','digest','created_at'])test('reject changed artifact '+key,()=>{const d=structuredClone(artifact);d[key]='changed';assert.throws(()=>assertArtifact(d,job));});
for(const path of ['site/gallery/renderer.js','site/gallery/main.js','site/gallery/detail-presentation-policy.js','site/public/detail-presentations/pertica.png','assets/models/test.glb','assets/manifest.json','package-lock.json','site/detail-presentation-quality.mjs','site/detail-capture-authority.mjs'])test('runtime or scientific control mutation fails '+path,()=>assert.throws(()=>assertRuntimeDiff([path])));
test('only explicit acceptance layer can differ',()=>assertRuntimeDiff(['site/detail-visual-acceptance.mjs',p.review_path]));
const context={runId:123,runAttempt:2,head:'f'.repeat(40)},deployedRun={id:123,run_attempt:2,head_sha:context.head,event:'push',head_branch:'main',path:'.github/workflows/pages.yml',workflow_id:p.workflow,status:'completed',conclusion:'success',repository:{full_name:p.repository},head_repository:{id:p.repository_id}},deployedJob={run_id:123,run_attempt:2,head_sha:context.head,name:'build',conclusion:'success',steps:['Validate source, build once and audit final dist','Authenticated same-runtime evidence and explicit independent visual acceptance','Stamp exact source build after all six mandatory audit phases'].map(name=>({name,conclusion:'success'}))};
test('public must bind actual accepted deployment run and acceptance step',()=>assertAcceptedDeployment(deployedRun,deployedJob,context));
for(const mutate of [r=>r.head_sha=p.head,r=>r.run_attempt=1,r=>r.event='pull_request',r=>r.conclusion='failure'])test('wrong deployed run identity is rejected',()=>{const d=structuredClone(deployedRun);mutate(d);assert.throws(()=>assertAcceptedDeployment(d,deployedJob,context));});
for(const mutate of [j=>j.head_sha=p.head,j=>j.steps[1].conclusion='skipped',j=>j.steps.splice(1,1),j=>j.run_attempt=1])test('no accepted dist step means no public review reuse',()=>{const d=structuredClone(deployedJob);mutate(d);assert.throws(()=>assertAcceptedDeployment(deployedRun,d,context));});
const h=n=>n.toString(16).padStart(40,'0'),entry=(path,sha,type='blob',mode='100644')=>({path,sha,type,mode});
const treeFixture=()=>({old:new Map([[h(1),{sha:h(1),truncated:false,tree:[entry('site',h(3),'tree','040000'),entry('assets',h(10),'tree','040000')]}],[h(3),{sha:h(3),truncated:false,tree:[entry('detail-presentation-browser-test.mjs',h(5)),entry('gallery',h(11),'tree','040000')]}]]),next:new Map([[h(2),{sha:h(2),truncated:false,tree:[entry('site',h(4),'tree','040000'),entry('assets',h(10),'tree','040000')]}],[h(4),{sha:h(4),truncated:false,tree:[entry('detail-presentation-browser-test.mjs',h(6)),entry('gallery',h(11),'tree','040000')]}]])});
const compareFixture=f=>compareRuntimeTrees({oldRoot:h(1),newRoot:h(2),oldTree:async id=>f.old.get(id),newTree:async id=>f.next.get(id)});
assert.deepEqual(await compareFixture(treeFixture()),['site/detail-presentation-browser-test.mjs']);console.log('PASS immutable equal subtrees and exact acceptance leaf');count++;
for(const [name,mutate]of [
 ['tab-suffixed pseudo-allowleaf',f=>f.next.get(h(4)).tree.push(entry('detail-visual-acceptance.mjs\tunexpected',h(55)))],
 ['adjacent new runtime',f=>f.next.get(h(4)).tree.push(entry('new-runtime.js',h(8)))],
 ['adjacent deleted runtime',f=>f.next.get(h(4)).tree.pop()],
 ['adjacent mode change',f=>f.next.get(h(4)).tree[1].mode='160000'],
 ['unreviewed asset subtree',f=>f.next.get(h(2)).tree[1].sha=h(99)],
 ['ancestor symlink',f=>{f.next.get(h(2)).tree[0].type='blob';f.next.get(h(2)).tree[0].mode='120000';}],
 ['ancestor gitlink',f=>{f.next.get(h(2)).tree[0].type='commit';f.next.get(h(2)).tree[0].mode='160000';}],
 ['allowed leaf symlink',f=>f.next.get(h(4)).tree[0].mode='120000'],
 ['wrong API tree identity',f=>f.old.get(h(1)).sha=h(44)],
 ['truncated API tree',f=>f.old.get(h(1)).truncated=true],
 ['duplicate tree entry',f=>f.next.get(h(4)).tree.push(f.next.get(h(4)).tree[0])]
 ]){const f=treeFixture();mutate(f);await assert.rejects(compareFixture(f));console.log('PASS reject '+name);count++;}
test('only exact reviewed acceptance control hashes can reuse evidence',()=>assertAcceptanceControls({...ACCEPTANCE_CONTROL_HASHES}));
for(const key of Object.keys(ACCEPTANCE_CONTROL_HASHES))test('future acceptance source change fails '+key,()=>assert.throws(()=>assertAcceptanceControls({...ACCEPTANCE_CONTROL_HASHES,[key]:'0'.repeat(64)})));
console.log(`PASS ${count} visual evidence identity tests; actual network/public NOT_RUN`);

/** Real adversarial process fixtures only. No browser, remote requests or approvals. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,mkdtempSync,rmSync,statSync,existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve,dirname} from 'node:path';
import {execFileSync,spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {assertDeploymentReceipt,pushIdentity,stampDeployment,verifyBuildMarker,waitForDeployedBuild,hash,MARKER_PATH} from './ci-deployment-contract.mjs';
import {createReleaseScope,verifyReleaseScope} from './ci-layered-release-scope.mjs';
import {projectHistoricalManifest,runHistoricalSuite} from './ci-historical-publication.mjs';
let checks=0;const root=mkdtempSync(join(process.cwd(),'.deployment-contract-'));
const put=(p,v)=>{mkdirSync(dirname(join(root,p)),{recursive:true});writeFileSync(join(root,p),typeof v==='string'?v:JSON.stringify(v,null,2)+'\n');};
const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
const commit=msg=>{git('add','.');git('commit','-qm',msg);return git('rev-parse','HEAD');};
try{
 git('init','-q');git('config','user.name','Deployment contract fixture');git('config','user.email','fixture@example.invalid');
 const originalManifest={assets:[{id:'old',glb:'assets/old.glb',sha256:{glb:'g',blend:'b',preview:'p'},name:{en:'Old'}}]};
 for(const p of ['.github/workflows/pages.yml','.github/workflows/full-release-review.yml','site/ci-scope.mjs','site/ci-layered-release-scope.mjs','site/ci-deployment-contract.mjs','site/ci-post-release-browser.mjs','site/ci-post-release-shared.mjs','site/live-release-contract.mjs'])put(p,readFileSync(p,'utf8'));
 put('assets/manifest.json',originalManifest);const ancestor=commit('ancestor');put('note.txt','base');const base=commit('true push before');
 const current={assets:[{...originalManifest.assets[0],name:{en:'New name, same model bytes'}},{id:'new',glb:'assets/new.glb',sha256:{glb:'g2',blend:'b2',preview:'p2'}}]};put('assets/manifest.json',current);const head=commit('true head');
 const identity={base,head,runId:101,runAttempt:2,repository:'s010s/lowpoly-vault'};
 put('dist/index.html','<script src="assets/main-fixture.js"></script>');put('dist/assets/main-fixture.js','current JavaScript');put('dist/assets/manifest.json',current);
 put('qa/ci-timings/build.json',{status:'pass',phases:['publication-check','registry-check','vite','seal-render-template','copy-and-package','full-release-audit'].map(name=>({name,exit_code:0,signal:null}))});
 const {marker,marker_sha256}=stampDeployment({root,identity});checks++;
 const plan=createReleaseScope({root,...identity}),raw=JSON.stringify(plan,null,2)+'\n';
 const receipt={schema_version:1,kind:'successful-pages-deployment-v1',deploy_outcome:'success',source_event:'push',source_ref:'refs/heads/main',...identity,same_commit_push:false,page_url:'https://deployment.example.invalid/project/',build_digest:marker.build_digest,marker_sha256,scope_sha256:hash(raw)};
 const event={repository:{full_name:identity.repository},workflow_run:{id:identity.runId,run_attempt:identity.runAttempt,head_sha:head,event:'push',head_branch:'main',head_repository:{full_name:identity.repository},conclusion:'success'}};
 const context=assertDeploymentReceipt(receipt,event);assert.equal(context.pageURL,receipt.page_url);assert.deepEqual(verifyReleaseScope(plan,{root,expected:context}),plan);assert.deepEqual(verifyBuildMarker({root,context}),marker);checks++;
 for(const change of [r=>r.head=base,r=>r.runId++,r=>r.runAttempt++,r=>r.deploy_outcome='failure',r=>r.same_commit_push=true,r=>r.repository='foreign/repo',r=>r.page_url='http://unsafe.invalid/',r=>r.scope_sha256='invalid']){const bad=structuredClone(receipt);change(bad);assert.throws(()=>assertDeploymentReceipt(bad,event));checks++;}
 for(const wrong of [ancestor,head]){const recomputed=createReleaseScope({root,...identity,base:wrong});assert.throws(()=>verifyReleaseScope(recomputed,{root,expected:context}),/original push base/);checks++;}
 assert.throws(()=>verifyReleaseScope(plan,{root}),/expected source/);checks++;
 // A genuine no-model-change / same-commit source event is explicit, not blanket rejected.
 const sameIdentity={...identity,base:head},sameReceipt={...receipt,base:head,same_commit_push:true};const sameContext=assertDeploymentReceipt(sameReceipt,event);const samePlan=createReleaseScope({root,...sameIdentity});assert.deepEqual(verifyReleaseScope(samePlan,{root,expected:sameContext}).affected_ids,[]);checks++;
 const env={GITHUB_EVENT_NAME:'push',GITHUB_REF:'refs/heads/main',GITHUB_SHA:head,GITHUB_REPOSITORY:identity.repository,GITHUB_RUN_ID:'101',GITHUB_RUN_ATTEMPT:'2'};
 assert.deepEqual(pushIdentity({ref:env.GITHUB_REF,after:head,before:base,repository:{full_name:identity.repository}},env),identity);checks++;
 const bodies=new Map(marker.files.map(f=>[f.path,readFileSync(join(root,'dist',f.path))]));bodies.set(MARKER_PATH,readFileSync(join(root,'dist',MARKER_PATH)));
 const requests=[];const fetcher=async url=>{assert(url.startsWith(receipt.page_url),'Must use official deployment URL');requests.push(url);const path=url.slice(receipt.page_url.length),bytes=bodies.get(path);return {ok:!!bytes,status:bytes?200:404,arrayBuffer:async()=>bytes};};
 const remote=()=>waitForDeployedBuild({baseURL:context.pageURL,marker,markerSHA256:context.markerSHA256,timeout:0,interval:0,fetcher});
 assert.equal((await remote()).status,'PASS');assert(requests.some(u=>u.endsWith('assets/main-fixture.js')));checks++;
 // F1: unchanged model payloads no longer make an old commit or stale UI pass.
 const savedMarker=bodies.get(MARKER_PATH);bodies.set(MARKER_PATH,Buffer.from(JSON.stringify({...marker,head:base})));await assert.rejects(remote,/marker/);bodies.set(MARKER_PATH,savedMarker);checks++;
 const savedJS=bodies.get('assets/main-fixture.js');bodies.set('assets/main-fixture.js',Buffer.from('outdatedJavaScript!'));await assert.rejects(remote,/resource (size|hash)/);bodies.set('assets/main-fixture.js',savedJS);checks++;
 const savedManifest=bodies.get('assets/manifest.json');bodies.set('assets/manifest.json',Buffer.from(JSON.stringify({...current,assets:current.assets.map(a=>({...a,name:{en:'STALE'}}))})));await assert.rejects(remote,/resource (size|hash)/);bodies.set('assets/manifest.json',savedManifest);checks++;
 bodies.delete(MARKER_PATH);await assert.rejects(remote,/HTTP 404/);bodies.set(MARKER_PATH,savedMarker);checks++;
 // F3: missing scope is rejected inside a structured report, before any browser launch.
 put('event.json',event);put('receipt.json',receipt);
 for(const script of ['ci-post-release-browser','ci-post-release-shared']){
  const out=join(root,script),result=spawnSync(process.execPath,[fileURLToPath(new URL('./'+script+'.mjs',import.meta.url))],{cwd:process.cwd(),encoding:'utf8',env:{...process.env,GITHUB_EVENT_NAME:'workflow_run',GITHUB_EVENT_PATH:join(root,'event.json'),DEPLOYMENT_RECEIPT:join(root,'receipt.json'),POST_RELEASE_SCOPE:join(root,'missing-plan.json'),DEPLOYED_SHA:head,UPSTREAM_RUN_ID:'101',UPSTREAM_RUN_ATTEMPT:'2',QA_OUTPUT_DIR:out}});
  assert.notEqual(result.status,0);const report=JSON.parse(readFileSync(join(out,'report.json')));assert.equal(report.status.toLowerCase(),'fail');assert.equal(report.failed_phase,'receipt-scope-build-verification');assert.equal(report.expected.source_commit,head);assert.equal(report.checks[script.endsWith('browser')?'browser':'shared'],'NOT_RUN');checks++;
 }
 // F2: complete exact historical input and a deliberately mutating process probe.
 const source=join(root,'historical-source');mkdirSync(source);const hg=(...args)=>execFileSync('git',args,{cwd:source,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();hg('init','-q');hg('config','user.name','Private-copy fixture');hg('config','user.email','fixture@example.invalid');
 const actual=JSON.parse(readFileSync('assets/manifest.json')),historical=projectHistoricalManifest(actual,actual.assets.filter(a=>a.production_release));
 const hp=(p,b)=>{mkdirSync(dirname(join(source,p)),{recursive:true});writeFileSync(join(source,p),b);};hp('.gitignore','node_modules/\n');hp('assets/manifest.json',JSON.stringify(historical));hp('sentinel.txt','ORIGINAL');hp('site/final-five-release-test.mjs',"import {writeFileSync} from 'node:fs';writeFileSync('sentinel.txt','MUTATED');writeFileSync('node_modules/probe.txt','MUTATED');\n");mkdirSync(join(source,'node_modules'));hg('add','.');hg('commit','-qm','Exact historical source and process-control mutation');hp('node_modules/probe.txt','ORIGINAL DEPENDENCY');
 for(const temporary of [tmpdir(),root]){assert.equal(await runHistoricalSuite('final-five-release',{source,temporary}),0);assert.equal(readFileSync(join(source,'sentinel.txt'),'utf8'),'ORIGINAL');assert.equal(readFileSync(join(source,'node_modules/probe.txt'),'utf8'),'ORIGINAL DEPENDENCY');checks++;}
 console.log('Private-copy portability devices:',JSON.stringify({source:statSync(source).dev,default_temp:statSync(tmpdir()).dev}));
 // A test deliberately writing the absolute original source is detected, not accepted.
 hp('site/final-five-release-test.mjs',`import {writeFileSync} from 'node:fs';writeFileSync(${JSON.stringify(join(source,'sentinel.txt'))},'EXTERNAL MUTATION');\n`);hg('add','.');hg('commit','-qm','Source-mutation detection negative');await assert.rejects(()=>runHistoricalSuite('final-five-release',{source}),/Source bytes changed: sentinel/);hp('sentinel.txt','ORIGINAL');checks++;
 rmSync(join(source,'sentinel.txt'));await assert.rejects(()=>runHistoricalSuite('final-five-release',{source}),/Complete checkout required/);checks++;
 const workflow=readFileSync('.github/workflows/full-release-review.yml','utf8');assert.match(workflow,/Always summarize every prerequisite and runtime outcome[\s\S]*if: always\(\)/);assert.match(workflow,/id: shared\n        if: always\(\) && steps.verify.outcome == 'success' && steps.install.outcome == 'success'/);assert(!workflow.includes('continue-on-error'));assert.match(workflow,/Explicitly retain artifact upload failures/);checks++;
 const summaryScript=(yaml,tag)=>{const text=yaml.split(`python3 - <<'${tag}'\n`)[1].split('          '+tag)[0];return text.split('\n').map(line=>line.startsWith('          ')?line.slice(10):line).join('\n');};
 const runtimeSummary=summaryScript(workflow,'PY_SUMMARY'),productionSummary=summaryScript(readFileSync('.github/workflows/pages.yml','utf8'),'PY_STATIC_SUMMARY');
 for(const [script,names,folder,extra]of [[runtimeSummary,['checkout','setup','dependencies','receipt','scope','build','verify','install','runtime_regression','browser','shared','right_detail'],'post-release-summary',{UPSTREAM_CONCLUSION:'success',DEPLOYED_SHA:head,UPSTREAM_RUN_ID:'101',UPSTREAM_RUN_ATTEMPT:'2'}],[productionSummary,['checkout','setup','dependencies','contracts','build','right_detail_install','right_detail','right_detail_artifact','stamp','scope','scope_upload','built_upload','pages_artifact'],'production-summary',{GITHUB_EVENT_NAME:'push',GITHUB_REF:'refs/heads/main',GITHUB_SHA:head,GITHUB_RUN_ID:'101',GITHUB_RUN_ATTEMPT:'2'}]]){
  for(let index=0;index<names.length;index++){
   const steps=Object.fromEntries(names.map((name,i)=>[name,{outcome:i<index?'success':i===index?'failure':'skipped'}]));
   // Shared regressions still run after an independently failed public browser.
   if(names[index]==='browser')steps.shared.outcome='success';
   const result=spawnSync('python3',['-c',script],{encoding:'utf8',env:{...process.env,...extra,STEP_OUTCOMES:JSON.stringify(steps),RUNNER_TEMP:root,GITHUB_STEP_SUMMARY:join(root,'summary.txt')}});assert.equal(result.status,0,result.stderr);
   const report=JSON.parse(readFileSync(join(root,folder,'report.json')));assert.equal(report.status,'FAIL');assert.equal(report.failed_phase,names[index]);assert.equal(report.expected_source,head);
   if(folder==='post-release-summary'&&index<8)assert.deepEqual(report.downstream,{browser:'NOT_RUN',shared:'NOT_RUN',right_detail:'NOT_RUN'});
   if(names[index]==='browser')assert.deepEqual(report.downstream,{browser:'FAIL',shared:'success',right_detail:'NOT_RUN'});checks++;
  }
 }
 console.log(`PASS deployment repair: ${checks} adversarial checks for exact official deployment/build, expected event base/run/attempt, private cross-filesystem fixtures, source mutation refusal and early reports.`);
}finally{rmSync(root,{recursive:true,force:true});}

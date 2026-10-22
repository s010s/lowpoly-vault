/** Deterministic contracts: no browser launch, upload, deployment or synthetic approval. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,mkdtempSync,rmSync} from 'node:fs';
import {join,dirname} from 'node:path';
import {tmpdir} from 'node:os';
import {execFileSync} from 'node:child_process';
import {affectedModelScope,createReleaseScope,verifyReleaseScope} from './ci-layered-release-scope.mjs';
import {projectHistoricalManifest,runHistoricalSuite,HISTORICAL_PUBLICATION_SUITES} from './ci-historical-publication.mjs';
let checks=0;const ok=(condition,label)=>{assert(condition,label);checks++;};
const old={assets:[{id:'old',glb:'assets/old.glb',sha256:{glb:'a'}}]},current={assets:[...old.assets,{id:'new',glb:'assets/new.glb',sha256:{glb:'b'},production_release:'production/new/release.json'}]};
const scope=affectedModelScope(['site/main.js','assets/manifest.json'],current,old);
assert.deepEqual(scope.affected_ids,['new']);assert.deepEqual(scope.capture_ids,['new']);ok(scope.shared_runtime_required,'Shared code remains fully tested');
assert.deepEqual(affectedModelScope(['assets/old.glb'],old,old).capture_ids,['old']);
assert.deepEqual(affectedModelScope(['production/new/source.py'],current,current).capture_ids,['new']);
assert.deepEqual(affectedModelScope(['site/style.css'],old,old).capture_ids,[]);
assert.throws(()=>affectedModelScope([],current,null));checks+=4;
const pages=readFileSync('.github/workflows/pages.yml','utf8'),review=readFileSync('.github/workflows/full-release-review.yml','utf8'),publication=readFileSync('.github/workflows/publication-regressions.yml','utf8');
const job=(yaml,name)=>{const s=yaml.split(`\n  ${name}:\n`)[1];assert(s,`Missing ${name}`);const end=s.search(/\n  [a-zA-Z][\w-]*:/);return end<0?s:s.slice(0,end);};
function assertLayeredGraph(pages,review){
 const build=job(pages,'build'),deploy=job(pages,'deploy'),runtime=job(review,'deployed-runtime');
 assert.match(deploy,/needs: \[build, publication\]/);assert.doesNotMatch(deploy,/needs:.*(?:runtime|review|browser)|(?:run|uses):.*(?:runtime|review|browser)|continue-on-error/);
 assert.doesNotMatch(build,/ci-install-chromium\.mjs|capture-gallery-posters\.mjs|gallery:posters|site\/[a-z0-9-]*-browser-test\.mjs|npm run [a-z:]*:browser|run: .*test:parser|ci-reuse\.mjs|continue-on-error/);
 assert.match(build,/run: node site\/ci-release-fast-path\.mjs build/);assert.match(build,/run: node site\/ci-production-release-check\.mjs/);
 assert.match(build,/node site\/ci-release-fast-path\.mjs contracts/); assert.match(readFileSync("site/ci-release-fast-path.mjs","utf8"),/npm run test:manifest.*npm run test:gallery/);
 const trigger=review.slice(0,review.indexOf('permissions:'));assert.match(trigger,/workflow_run:/);assert.doesNotMatch(trigger,/\n  push:|\n  pull_request:/);
 assert.match(runtime,/id: checkout\n        if: github.event.workflow_run.conclusion == 'success'/);assert.match(runtime,/workflow_run\.event == 'push'/);assert.match(runtime,/workflow_run\.head_repository\.full_name == github\.repository/);
 assert.match(runtime,/ref: \$\{\{ github.event.workflow_run.head_sha \}\}/);assert.match(runtime,/run-id: \$\{\{ github.event.workflow_run.id \}\}/);
 assert.match(runtime,/ci-layered-release-scope\.mjs verify/);assert.match(runtime,/ci-post-release-browser\.mjs/);assert.match(runtime,/ci-post-release-shared\.mjs/);
 assert.doesNotMatch(runtime,/needs:|pages: write|id-token: write|contents: write|continue-on-error|gallery:posters|ci-incremental-models/);
 assert.match(job(review,'scope'),/if: github.event_name == 'workflow_dispatch'/);
 assert.match(review,/npm run gallery:posters && node site\/gallery-assets\.mjs --dist --complete/,'Historical browser proof path preserved, not rewritten');
}
assertLayeredGraph(pages,review);checks++;
for(const [p,r]of [[pages.replace('needs: [build, publication]','needs: [build, publication, deployed-runtime]'),review],[pages.replace('run: node site/ci-release-fast-path.mjs build','run: npm run gallery:posters'),review],[pages,review.replace('workflow_run:', 'pull_request:')],[pages,review.replace("workflow_run.conclusion == 'success'","workflow_run.conclusion != 'success'")]]){assert.throws(()=>assertLayeredGraph(p,r));checks++;}
ok(publication.includes("CI_ISOLATE_HISTORICAL: '1'"),'CI explicitly uses isolated historical fixtures');
ok(publication.includes('needs: [plan, shards]')&&!publication.includes('continue-on-error'),'All 25 rejection suites remain blocking');
const timed=readFileSync('site/ci-timed.mjs','utf8');
for(const phase of ['publication-check','registry-check','vite','seal-render-template','copy-and-package','full-release-audit'])ok(timed.includes(`name:'${phase}'`),'Mandatory build phase '+phase);
assert.deepEqual(HISTORICAL_PUBLICATION_SUITES,['concept-landair-release','forty-four-release','fifty-two-release','final-five-release']);
const manifest=JSON.parse(readFileSync('assets/manifest.json')),before=JSON.stringify(manifest),production=manifest.assets.filter(a=>a.production_release);
const historical=projectHistoricalManifest(manifest,production);ok([347,352].includes(historical.assets.length),'Only fixed historical manifests are supported');assert.equal(JSON.stringify(manifest),before);
for(const mutate of [m=>m.assets[0].description.en+=' altered',m=>m.publication.unbound='extra',m=>m.assets.reverse()]){const bad=structuredClone(manifest);mutate(bad);assert.throws(()=>projectHistoricalManifest(bad,production));checks++;}
if(production.length){const wrong=structuredClone(production);wrong[0].sha256.glb='0'.repeat(64);assert.throws(()=>projectHistoricalManifest(manifest,wrong));checks++;}
const fixture=mkdtempSync(join(tmpdir(),'layered-scope-'));
try{
 const put=(path,value)=>{mkdirSync(dirname(join(fixture,path)),{recursive:true});writeFileSync(join(fixture,path),typeof value==='string'?value:JSON.stringify(value));};
 const git=(...args)=>execFileSync('git',args,{cwd:fixture,encoding:'utf8'}).trim();git('init','-q');git('config','user.name','Local scope test');git('config','user.email','scope@example.invalid');
 for(const path of ['.github/workflows/pages.yml','.github/workflows/full-release-review.yml','site/ci-scope.mjs','site/ci-layered-release-scope.mjs','site/ci-deployment-contract.mjs','site/ci-post-release-browser.mjs','site/ci-post-release-shared.mjs','site/live-release-contract.mjs'])put(path,readFileSync(path,'utf8'));
 put('assets/manifest.json',old);put('dist/index.html','sealed output');git('add','.');git('commit','-qm','base');const base=git('rev-parse','HEAD');
 put('assets/manifest.json',current);put('site/main.js','shared code edit');git('add','.');git('commit','-qm','new model and shared runtime');const head=git('rev-parse','HEAD');
 const identity={base,head,runId:101,runAttempt:2,repository:'s010s/lowpoly-vault'};const plan=createReleaseScope({root:fixture,...identity});assert.deepEqual(plan.affected_ids,['new']);assert.deepEqual(verifyReleaseScope(plan,{root:fixture,expected:identity}),plan);checks++;
 for(const mutate of [p=>p.source_commit=base,p=>p.base_commit='0'.repeat(40),p=>p.affected_ids=['old','new'],p=>p.capture_ids=[],p=>p.manifest_sha256='0'.repeat(64),p=>p.controls[0].sha256='0'.repeat(64),p=>p.build_inventory[0].sha256='0'.repeat(64),p=>p.shared_runtime_required=false]){const bad=structuredClone(plan);mutate(bad);assert.throws(()=>verifyReleaseScope(bad,{root:fixture,expected:identity}));checks++;}
 put('dist/index.html','wrong output');assert.throws(()=>verifyReleaseScope(plan,{root:fixture,expected:identity}));put('dist/index.html','sealed output');checks++;
 put('assets/manifest.json',{...current,forged:true});assert.throws(()=>verifyReleaseScope(plan,{root:fixture,expected:identity}));put('assets/manifest.json',current);checks++;
 put('site/ci-scope.mjs','changed consumer');assert.throws(()=>verifyReleaseScope(plan,{root:fixture,expected:identity}));checks++;
}finally{rmSync(fixture,{recursive:true,force:true});}
const runnerFixture=mkdtempSync(join(tmpdir(),'historical-runner-contract-'));
try{
 const git=(...args)=>execFileSync('git',args,{cwd:runnerFixture,encoding:'utf8'}).trim();git('init','-q');git('config','user.name','Local fixture test');git('config','user.email','fixture@example.invalid');
 mkdirSync(join(runnerFixture,'assets'));mkdirSync(join(runnerFixture,'site'));mkdirSync(join(runnerFixture,'node_modules'));
 const bytes=JSON.stringify(historical,null,2)+'\n';writeFileSync(join(runnerFixture,'assets/manifest.json'),bytes);
 // Process-control probes only: neither probe writes or claims an approval.
 const script=join(runnerFixture,'site/final-five-release-test.mjs');writeFileSync(script,'process.exit(23);\n');git('add','.');git('commit','-qm','Exact historical manifest and failure probe');
 assert.equal(await runHistoricalSuite('final-five-release',{source:runnerFixture}),23);assert.equal(readFileSync(join(runnerFixture,'assets/manifest.json'),'utf8'),bytes);checks++;
 writeFileSync(script,'process.exit(0);\n');git('add','.');git('commit','-qm','Success process-control probe');assert.equal(await runHistoricalSuite('final-five-release',{source:runnerFixture}),0);checks++;
 await assert.rejects(()=>runHistoricalSuite('unlisted-suite',{source:runnerFixture}));checks++;
}finally{rmSync(runnerFixture,{recursive:true,force:true});}
console.log(`PASS layered release: ${checks} graph, exact scope, historical projection, source/hash/subject/build tamper and no-browser-production contracts.`);

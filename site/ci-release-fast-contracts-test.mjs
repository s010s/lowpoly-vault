import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,rmSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {canReuseBuildContracts} from './ci-release-fast-contracts.mjs';
const root=mkdtempSync(join(tmpdir(),'fast-contracts-')),path=join(root,'qa/ci-timings/build.json');mkdirSync(join(root,'qa/ci-timings'),{recursive:true});
const identity={source_commit:'a'.repeat(40),run_id:2,run_attempt:1,repository:'fixture/repo',runtime:{site_base:'/repo/',site_origin:'https://example.invalid'}},scope={eligible:true,baseline:{source_commit:'b'.repeat(40),run_id:1},added_ids:['new']};
const report=()=>({version:1,...structuredClone(identity),mode:'additive',status:'pass',baseline:structuredClone(scope.baseline),added_ids:['new'],artifact_id:3,artifact_digest:'sha256:'+'c'.repeat(64),reused:['vite','historical-package-generation'],phases:['publication-check','registry-check','incremental-copy-and-package','full-release-audit'].map(name=>({name,exit_code:0,signal:null}))});
const check=(r,expected,label)=>{writeFileSync(path,JSON.stringify(r));assert.equal(canReuseBuildContracts(scope,{root,identity}),expected,label);};
try{
 assert.equal(canReuseBuildContracts(scope,{root,identity}),false,'No build result');writeFileSync(path,'broken JSON');assert.equal(canReuseBuildContracts(scope,{root,identity}),false);let n=2;
 check(report(),true,'Only completed additive execution permits reuse');n++;
 for(const label of ['missing artifact -> full fallback','corrupt artifact -> full fallback','failed additive attempt -> full fallback']){
  writeFileSync(join(root,'qa/ci-timings/additive-attempt.json'),JSON.stringify({...report(),status:'fail'}));check({...report(),mode:'build'},false,label);n++;
 }
 for(const edit of [r=>r.status='running',r=>r.status='fail',r=>r.source_commit='d'.repeat(40),r=>r.run_id++,r=>r.run_attempt++,r=>r.repository='other/repo',r=>r.runtime.site_base='/',r=>r.baseline.run_id++,r=>r.added_ids=[],r=>r.artifact_id=0,r=>r.artifact_digest='unverified',r=>r.phases.pop(),r=>r.phases[0].exit_code=1,r=>r.reused=[]]){const r=report();edit(r);check(r,false,'reject invalid report');n++;}
 writeFileSync(path,JSON.stringify(report()));assert.equal(canReuseBuildContracts({eligible:false},{root,identity}),false,'Local report cannot authorize scope');n++;
 console.log(`Build-to-contract handoff: ${n} additive/fallback/stale/tamper cases passed.`);
}finally{rmSync(root,{recursive:true,force:true});}

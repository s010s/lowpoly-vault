import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {stampDeployment} from './ci-deployment-contract.mjs';
const root=mkdtempSync(join(tmpdir(),'fast-deploy-'));
try{
 const git=(...a)=>execFileSync('git',a,{cwd:root,encoding:'utf8',stdio:'pipe'}).trim();git('init','-q');git('config','user.name','Offline fixture');git('config','user.email','fixture@example.invalid');writeFileSync(join(root,'source'),'base');git('add','.');git('commit','-qm','base');const base=git('rev-parse','HEAD');writeFileSync(join(root,'source'),'head');git('add','.');git('commit','-qm','head');const head=git('rev-parse','HEAD');
 mkdirSync(join(root,'dist'));writeFileSync(join(root,'dist/index.html'),'audited fixture');mkdirSync(join(root,'qa/ci-timings'),{recursive:true});
 const make=()=>({mode:'additive',status:'pass',baseline:{source_commit:base},artifact_id:3,artifact_digest:'sha256:'+'a'.repeat(64),reused:['vite','historical-package-generation'],phases:['publication-check','registry-check','incremental-copy-and-package','full-release-audit'].map(name=>({name,exit_code:0,signal:null}))});
 const run=r=>{writeFileSync(join(root,'qa/ci-timings/build.json'),JSON.stringify(r));return stampDeployment({root,identity:{head,base,runId:1,runAttempt:1,repository:'fixture/repo'}});};
 assert.equal(run(make()).marker.head,head);rmSync(join(root,'dist/release-build.json'));let n=1;
 for(const edit of [r=>delete r.baseline,r=>r.artifact_id=0,r=>r.artifact_digest='unverified',r=>r.status='fail',r=>r.phases.pop(),r=>r.phases[0].exit_code=1,r=>r.reused=[],r=>r.phases[2].name='vite']){const r=make();edit(r);assert.throws(()=>run(r));n++;}
 console.log(`Additive deployment stamp: ${n} honest-stage and fail-closed cases passed.`);
}finally{rmSync(root,{recursive:true,force:true});}

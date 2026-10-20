/** Real memo implementation in an isolated Git fixture; no real publication validator is weakened. */
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,copyFileSync,rmSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {tmpdir} from 'node:os';
import {execFileSync,spawnSync} from 'node:child_process';
const root=mkdtempSync(join(tmpdir(),'publication-memo-')),runner=mkdtempSync(join(tmpdir(),'publication-runner-'));
try{
 mkdirSync(join(root,'site'));mkdirSync(join(root,'assets'));
 for(const file of ['ci-publication.mjs','ci-provenance.mjs'])copyFileSync(resolve('site',file),join(root,'site',file));
 writeFileSync(join(root,'site/initial-release.mjs'),`import {readFileSync,writeFileSync,existsSync} from 'node:fs';export async function checkPublishedManifest(){let count=existsSync('.calls')?Number(readFileSync('.calls')):0;writeFileSync('.calls',String(count+1));return JSON.parse(readFileSync('assets/manifest.json'));}`);
 writeFileSync(join(root,'assets/manifest.json'),'{"assets":[{"id":"one"}]}');writeFileSync(join(root,'tracked'),'original');writeFileSync(join(root,'.gitignore'),'.calls\n');
 const git=(...args)=>execFileSync('git',args,{cwd:root,stdio:'pipe'});git('init','-q');git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid');git('add','.');git('commit','-qm','fixture');
 const env={...process.env,GITHUB_ACTIONS:'true',GITHUB_RUN_ID:'12',GITHUB_RUN_ATTEMPT:'1',RUNNER_TEMP:runner,CI_PUBLICATION_RECEIPT:join(runner,'memo.json')};
 const run=(args,changes={})=>execFileSync(process.execPath,args,{cwd:root,env:{...env,...changes},stdio:'pipe'});
 const record=()=>run(['site/ci-publication.mjs']);
 const check=(changes={})=>run(['--input-type=module','-e',"import {checkedPublication} from './site/ci-publication.mjs';await checkedPublication();"],changes);
 const calls=()=>Number(readFileSync(join(root,'.calls')));
 record();assert.equal(calls(),1);check();assert.equal(calls(),1,'Unchanged same-job input may reuse');
 writeFileSync(join(root,'tracked'),'changed');check();assert.equal(calls(),2,'Dirty source must rerun');git('checkout','--','tracked');
 check({GITHUB_RUN_ATTEMPT:'2'});assert.equal(calls(),3,'Stale attempt must rerun');
 record();assert.equal(calls(),4,'Every new build starts with the original gate');
 const forged=join(root,'forged.json');copyFileSync(env.CI_PUBLICATION_RECEIPT,forged);check({CI_PUBLICATION_RECEIPT:forged});assert.equal(calls(),5,'Repository-authored memo must never be accepted');
 rmSync(forged);writeFileSync(env.CI_PUBLICATION_RECEIPT,'broken');check();assert.equal(calls(),6,'Malformed memo falls back');
 check({GITHUB_ACTIONS:'false'});assert.equal(calls(),7,'Non-CI execution cannot reuse runner memo');
 console.log('Publication memo: first gate always executes; clean hit; dirty source, stale attempt, repository-authored, malformed and non-CI receipts fall back.');
 // Real direct entry, not the memo stub: a same-module dynamic import used to
 // deadlock this 217-release path inside the initial/refined static import cycle.
 const publication=JSON.parse(readFileSync('assets/manifest.json')).publication;
 writeFileSync(join(root,'assets/manifest.json'),JSON.stringify({publication:{batches52_53_descriptors:publication.batches52_53_descriptors,batches52_53_base_descriptor:publication.batches52_53_base_descriptor}}));
 const direct=()=>spawnSync(process.execPath,[resolve('site/initial-release.mjs'),'--check'],{cwd:root,encoding:'utf8',timeout:10000});
 let result=direct();assert.equal(result.status,1,result.stderr);
 assert.match(result.stderr,/ENOENT.*batch54-20261020\.json/s,'Direct gate must reach the actual missing source-byte check');
 assert(!result.stderr.includes('unsettled top-level await'));
 mkdirSync(join(root,'assets/releases'));writeFileSync(join(root,'assets/releases/batch54-20261020.json'),'{}');
 result=direct();assert.equal(result.status,1,result.stderr);assert.match(result.stderr,/Batch54 hash mismatch/,'Direct gate still rejects modified descriptor bytes');
 console.log('Direct publication entry: missing and tampered Batch54 source bytes fail normally, without an unresolved module cycle.');
}finally{rmSync(root,{recursive:true,force:true});rmSync(runner,{recursive:true,force:true});}

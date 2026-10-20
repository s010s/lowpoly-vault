/** Small exact-byte archives exercise reuse without scanning repository history. */
import assert from 'node:assert/strict';
import childProcess from 'node:child_process';
import {syncBuiltinESMExports} from 'node:module';
import {readFileSync} from 'node:fs';
import {join} from 'node:path';
import {fixture} from './ci-model-proof-test.mjs';
import {archiveFixture} from './ci-archival-inputs-test.mjs';
import {assertArchivalAppend} from './ci-archival-inputs.mjs';
import {modelPolicyDigest,modelPolicyDigestAtCommit,modelPolicySnapshotAtCommit,modelArchivalInputsAtCommit,assertModelArchivalAppendAtCommit} from './ci-model-proof.mjs';
import {proofReadBudget} from './ci-proof-budget.mjs';
import {proofGet} from './ci-proof-fetch.mjs';

const f=fixture(2),archive=archiveFixture(),execFileSync=childProcess.execFileSync;
try{
 const batch=archive.addBatch('snapshot',f.manifest.assets.map(row=>row.id),{models:f.manifest.assets,readModel:path=>readFileSync(join(f.root,path))});
 for(const [path,bytes]of archive.files)f.put(path,bytes);
 const git=(...args)=>execFileSync('git',args,{cwd:f.root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
 git('init','-q');git('add','.');git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','-c','core.hooksPath=/dev/null','commit','-qm','Exact snapshot fixture');
 const sha=git('rev-parse','HEAD'),digest=modelPolicyDigest(f.root);
 let scans=0,shows=0;
 childProcess.execFileSync=(command,args,options)=>{if(command==='git'&&options?.cwd===f.root){if(args[0]==='ls-tree')scans++;if(args[0]==='show')shows++;}return execFileSync(command,args,options);};syncBuiltinESMExports();
 const legacyDigest=modelPolicyDigestAtCommit(sha,{root:f.root});assertModelArchivalAppendAtCommit(sha,{root:f.root});
 assert.equal(scans,2,'Legacy separate digest/append calls scan the same commit twice');const legacyShows=shows;scans=0;shows=0;
 const snapshot=modelPolicySnapshotAtCommit(sha,{root:f.root}),snapshotShows=shows;
 assert.equal(snapshotShows*2,legacyShows,'One snapshot halves the exact-commit Git reads');
 assert(snapshotShows>archive.files.size/2,'Fixture must exercise actual archived Git objects');
 assert.equal(modelPolicyDigestAtCommit(sha,{root:f.root,snapshot}),digest);assert.equal(digest,legacyDigest,'Snapshot preserves the exact previous digest algorithm');
 const before=modelArchivalInputsAtCommit(sha,{root:f.root,snapshot});
 assert(Object.isFrozen(snapshot)&&Object.isFrozen(before)&&Object.isFrozen(before.files[0]));
 assert.throws(()=>{snapshot.digest='0'.repeat(64);},TypeError);assert.throws(()=>{before.files[0].sha256='0'.repeat(64);},TypeError);
 assertModelArchivalAppendAtCommit(sha,{root:f.root,snapshot});assertModelArchivalAppendAtCommit(sha,{root:f.root,snapshot});
 assert.equal(scans,1,'Digest and archival checks share one exact-commit policy scan');assert.equal(shows,snapshotShows,'Reusing a snapshot performs no more Git object reads');
 for(const forged of [{...snapshot},JSON.parse(JSON.stringify(snapshot)),{}])assert.throws(()=>modelPolicyDigestAtCommit(sha,{root:f.root,snapshot:forged}),/verified root and exact commit/);
 assert.throws(()=>modelPolicyDigestAtCommit('f'.repeat(40),{root:f.root,snapshot}),/verified root and exact commit/);
 assert.throws(()=>modelPolicyDigestAtCommit(sha,{root:join(f.root,'other'),snapshot}),/verified root and exact commit/);
 assert.throws(()=>assertArchivalAppend(structuredClone(before),before,{beforePaths:before.repositoryPaths,oldIDs:before.modelIDs,newIDs:[]}),/independently verified inventories/);
 f.put(batch.generator.path,'# changed after first successful append check');
 assert.throws(()=>assertModelArchivalAppendAtCommit(sha,{root:f.root,snapshot}),/SHA-256 mismatch/,'A cached historical snapshot must not cache the mutable worktree');
 assert.equal(modelPolicyDigestAtCommit(sha,{root:f.root,snapshot}),digest,'Worktree mutation cannot change the committed snapshot');
 const budget=proofReadBudget(10,{maximumMs:10,onTiming:()=>{}});let calls=0;
 // Block without yielding: the timer has not fired, but the total budget expired.
 Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,20);assert.equal(budget.signal.aborted,false);
 assert.throws(()=>budget.check(),error=>error.name==='TimeoutError');
 const beforeExpiredReads=shows;assert.throws(()=>modelPolicySnapshotAtCommit(sha,{root:f.root,budget}),error=>error.name==='TimeoutError');assert.equal(shows,beforeExpiredReads,'Expired budget starts no Git object reads');
 await assert.rejects(()=>proofGet('https://example.invalid',{signal:budget.signal},{checkBudget:budget.check,fetchImpl:async()=>{calls++;return new Response('no');}}),error=>error.name==='TimeoutError');
 assert.equal(calls,0,'No network request starts after synchronous work exhausts the budget');
 assert.throws(()=>proofReadBudget(11,{maximumMs:10}),/only shorten/);
 console.log(`Policy snapshot: digest equality; one scan/${snapshotShows} Git reads versus legacy two/${legacyShows}; immutable authenticated archives; wrong-root/commit/JSON/worktree tampering rejected; exhausted budget sends zero GETs.`);
}finally{childProcess.execFileSync=execFileSync;syncBuiltinESMExports();f.close();}

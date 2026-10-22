/** Exact changed-model selection is independent of conservative shared-code test scope.
 * This is a queue description, NOT production acceptance or reusable browser evidence.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,readdirSync,lstatSync,appendFileSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {classify} from './ci-scope.mjs';
import {assertIdentity,pushIdentity,readDeploymentContext,verifyBuildMarker} from './ci-deployment-contract.mjs';
const hash=b=>createHash('sha256').update(b).digest('hex');
const sha=x=>typeof x==='string'&&/^[a-f0-9]{40}$/.test(x)&&!/^0+$/.test(x);
const git=(root,...args)=>execFileSync('git',args,{cwd:root,maxBuffer:32*1024*1024}).toString();
export function affectedModelScope(paths,current,previous){
 assert(Array.isArray(current?.assets)&&Array.isArray(previous?.assets),'Exact previous and current manifest required');
 for(const m of [current,previous])assert.equal(new Set(m.assets.map(a=>a.id)).size,m.assets.length,'Duplicate model ID');
 const classification=classify(paths,current,false,{previousManifest:previous});
 const ids=new Set(classification.affectedIds);
 for(const asset of current.assets)if(!isDeepStrictEqual(asset,previous.assets.find(a=>a.id===asset.id)))ids.add(asset.id);
 // A production dependency, record or media edit affects its explicit release,
 // but never broadens captures to unrelated catalog models.
 for(const asset of current.assets)if(asset.production_release&&paths.some(p=>p===asset.production_release||p.startsWith(dirname(asset.production_release)+'/')))ids.add(asset.id);
 return {shared_runtime_required:classification.runtime,shared_tasks:classification.tasks.filter(t=>t!=='models'&&t!=='previews'&&t!=='none'),affected_ids:[...ids].sort(),removed_ids:previous.assets.filter(a=>!current.assets.some(b=>a.id===b.id)).map(a=>a.id).sort(),capture_ids:[...ids].sort()};
}
export function createReleaseScope({root='.',base,head,runId,runAttempt,repository}={}){
 assertIdentity({base,head,runId,runAttempt,repository});
 assert(sha(base)&&sha(head),'Exact nonzero source and base commits required');
 assert.equal(git(root,'rev-parse','HEAD').trim(),head,'Wrong source checkout');
 git(root,'merge-base','--is-ancestor',base,head);
 const source=readFileSync(resolve(root,'assets/manifest.json')),committed=git(root,'show',head+':assets/manifest.json');
 assert.equal(hash(source),hash(committed),'Uncommitted release manifest');
 const prior=git(root,'show',base+':assets/manifest.json'),paths=git(root,'diff','--name-only','-z',base,head).split('\0').filter(Boolean).sort();
 const control_paths=['.github/workflows/pages.yml','.github/workflows/full-release-review.yml','site/ci-scope.mjs','site/ci-layered-release-scope.mjs','site/ci-deployment-contract.mjs','site/ci-post-release-browser.mjs','site/ci-post-release-shared.mjs','site/live-release-contract.mjs'];
 const controls=control_paths.map(path=>{const bytes=readFileSync(resolve(root,path));assert.equal(hash(bytes),hash(git(root,'show',head+':'+path)),'Uncommitted scope consumer: '+path);return {path,sha256:hash(bytes)};});
 const inventory=[];const walk=folder=>{for(const name of readdirSync(resolve(root,folder)).sort()){const path=folder+'/'+name,stat=lstatSync(resolve(root,path));assert(!stat.isSymbolicLink(),'Build symlink rejected');if(stat.isDirectory())walk(path);else{assert(stat.isFile());const b=readFileSync(resolve(root,path));inventory.push({path,bytes:b.length,sha256:hash(b)});}}};walk('dist');assert(inventory.length,'Empty deployed build');
 return {schema_version:1,kind:'post-release-runtime-scope-v2',run_id:runId,run_attempt:runAttempt,repository,build_inventory:inventory,source_commit:head,base_commit:base,manifest_sha256:hash(source),previous_manifest_sha256:hash(prior),controls,changed_paths:paths,...affectedModelScope(paths,JSON.parse(source),JSON.parse(prior)),production_acceptance:false,reusable_browser_proof:false};
}
export function verifyReleaseScope(plan,{root='.',expected}={}){
 assertIdentity(expected);
 assert.equal(plan?.source_commit,expected.head,'Wrong deployed subject');
 assert.equal(plan.base_commit,expected.base,'Wrong original push base');
 assert.equal(plan.run_id,expected.runId,'Wrong source run');assert.equal(plan.run_attempt,expected.runAttempt,'Wrong source attempt');assert.equal(plan.repository,expected.repository);
 const actual=createReleaseScope({root,...expected});assert.deepEqual(plan,actual,'Scope bytes, model IDs, hashes or consumer policy changed');return actual;
}
export function loadVerifiedRelease({root='.',planPath=process.env.POST_RELEASE_SCOPE,receiptPath,eventPath}={}){
 const context=readDeploymentContext({receiptPath,eventPath}),raw=readFileSync(planPath);assert.equal(hash(raw),context.scopeSHA256,'Scope artifact does not match the successful deploy receipt');
 const scope=verifyReleaseScope(JSON.parse(raw),{root,expected:context}),marker=verifyBuildMarker({root,context});return {context,scope,marker};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 const report={status:'RUNNING',phase:'initialize',expected:{head:process.env.DEPLOYED_SHA||process.env.GITHUB_SHA||null,run_id:process.env.UPSTREAM_RUN_ID||process.env.GITHUB_RUN_ID||null,run_attempt:process.env.UPSTREAM_RUN_ATTEMPT||process.env.GITHUB_RUN_ATTEMPT||null},downstream:{browser:'NOT_RUN',shared:'NOT_RUN'}};
 try{
  const [mode,file]=process.argv.slice(2);assert(file&&['create','verify'].includes(mode),'Usage: create|verify FILE');report.phase='event-context';
  if(mode==='create'){
   const identity=pushIdentity(JSON.parse(readFileSync(process.env.GITHUB_EVENT_PATH)));report.phase='create-scope';const plan=createReleaseScope(identity);mkdirSync(dirname(file),{recursive:true});const raw=JSON.stringify(plan,null,2)+'\n';writeFileSync(file,raw);if(process.env.GITHUB_OUTPUT)appendFileSync(process.env.GITHUB_OUTPUT,`scope_sha256=${hash(raw)}\n`);report.scope_sha256=hash(raw);report.affected_ids=plan.affected_ids;
  }else{report.phase='receipt-scope-build-verification';const {scope}=loadVerifiedRelease({planPath:file});report.affected_ids=scope.affected_ids;}
  report.status='PASS';report.phase='complete';
 }catch(error){report.status='FAIL';report.failed_phase=report.phase;report.error=error.stack;process.exitCode=1;console.error(error);}
 finally{mkdirSync('qa/post-release-preflight',{recursive:true});writeFileSync('qa/post-release-preflight/report.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}
}

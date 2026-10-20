/** Read-only transport diagnostic. Never emits a release/cache proof. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {resolve} from 'node:path';
import {execFileSync} from 'node:child_process';
const ROOT=process.cwd(),REPOSITORY='s010s/lowpoly-vault';
const CURRENT='c8714ec3eba2925d1669663556445f8c43e40030',BASE='f8a793082a2167cfc8fe5cbf1c9d7ebc742b70d1';
assert.equal(process.env.GITHUB_REPOSITORY,REPOSITORY);assert(process.env.GITHUB_TOKEN);
assert.equal(execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),CURRENT);
assert.equal(execFileSync('git',['status','--porcelain','--untracked-files=no'],{encoding:'utf8'}).trim(),'');
const inputsBytes=readFileSync(new URL('./observed-model-inputs.json',import.meta.url));
assert.equal(createHash('sha256').update(inputsBytes).digest('hex'),'6dc8d7be65ce03dc26b01ec0f3854ab419b1b7fd2ff8347e59a3e8e98363b9ae');
const inputs=JSON.parse(inputsBytes);assert.equal(inputs.models.length,202);
assert.equal(inputs.policy_sha256,'d73901566ebe7b3276d8b614330e4d42df600674611885d5bdf3d718fca2cb5c');
const start=Date.now(),events=[],summaries=[];let sequence=0,lastEnd=start,trial='';
function save(){writeFileSync(resolve(process.env.RUNNER_TEMP,'proof-transport-observations.json'),JSON.stringify({kind:'read-only-transport-diagnostic',transport_trial:'event-loop-yield-and-bounded-socket-get-retry',not_release_evidence:true,source:CURRENT,base:BASE,inputs_sha256:createHash('sha256').update(inputsBytes).digest('hex'),events,summaries},null,2)+'\n');}
function emit(row){const event={trial,ms:Date.now()-start,...row};events.push(event);console.log(JSON.stringify(event));save();}
const atom=value=>typeof value==='string'&&/^[A-Za-z0-9_. -]{1,80}$/.test(value)?value:undefined;
function safeError(error,depth=0){if(!error||depth>3)return null;return {name:atom(error.name),code:atom(error.code),errno:typeof error.errno==='number'?error.errno:undefined,syscall:atom(error.syscall),cause:safeError(error.cause,depth+1),errors:Array.isArray(error.errors)?error.errors.slice(0,4).map(e=>safeError(e,depth+1)):undefined};}
function endpoint(url){const u=new URL(url);assert.equal(u.protocol,'https:');assert.equal(u.username,'');assert.equal(u.password,'');if(u.hostname==='api.github.com'){assert(u.pathname.startsWith(`/repos/${REPOSITORY}`));return {kind:'github-api',path:u.pathname.slice(`/repos/${REPOSITORY}`.length)||'repository-metadata'};}assert(/\.blob\.core\.windows\.net$|\.actions\.githubusercontent\.com$/.test(u.hostname),'Unexpected artifact storage host');return {kind:'artifact-storage',host:u.hostname};}
async function boundedReadFetch(url,options={}){
 // Diagnostic-only trial: same GET, same signal/deadline and credentials.
 // Yield after synchronous validation so queued socket-close events can run.
 for(let attempt=1;attempt<=3;attempt++){
  await new Promise(setImmediate);
  options.signal?.throwIfAborted();
  try{return await fetch(url,options);}catch(error){
   if(attempt===3||options.signal?.aborted||(options.method||'GET').toUpperCase()!=='GET'||error?.cause?.code!=='UND_ERR_SOCKET')throw error;
   emit({stage:'transport-retry',attempt,error:safeError(error)});
  }
 }
}
async function tracedFetch(url,options={}){
 const target=endpoint(url),id=++sequence,began=Date.now();
 if(target.kind==='artifact-storage')assert(!options.headers,'Storage must never receive repository credentials');
 emit({stage:'request',id,...target,idle_ms:began-lastEnd,signal_aborted:options.signal?.aborted===true});
 try{
  const response=await boundedReadFetch(url,options);lastEnd=Date.now();emit({stage:'response',id,status:response.status,elapsed_ms:lastEnd-began});
  return new Proxy(response,{get(object,key){
   if(key==='body'&&object.body?.getReader)return new Proxy(object.body,{get(body,bodyKey){
    if(bodyKey==='getReader')return (...args)=>{const reader=body.getReader(...args);let received=0;return new Proxy(reader,{get(target,readerKey){
     if(readerKey==='read'||readerKey==='cancel')return async(...readerArgs)=>{try{const value=await target[readerKey](...readerArgs);lastEnd=Date.now();if(readerKey==='read'){received+=value.value?.byteLength||0;if(value.done)emit({stage:'body-complete',id,format:'stream',bytes:received});}return value;}catch(error){emit({stage:'body-error',id,format:'stream',operation:readerKey,error:safeError(error),signal_aborted:options.signal?.aborted===true});throw error;}};
     const value=Reflect.get(target,readerKey,target);return typeof value==='function'?value.bind(target):value;
    }});};
    const value=Reflect.get(body,bodyKey,body);return typeof value==='function'?value.bind(body):value;
   }});
   if(['json','arrayBuffer'].includes(key))return async()=>{const at=Date.now();try{const value=await object[key]();lastEnd=Date.now();emit({stage:'body-complete',id,format:key,elapsed_ms:lastEnd-at});return value;}catch(error){emit({stage:'body-error',id,error:safeError(error),signal_aborted:options.signal?.aborted===true});throw error;}};const value=Reflect.get(object,key,object);return typeof value==='function'?value.bind(object):value;}});
 }catch(error){lastEnd=Date.now();emit({stage:'request-error',id,elapsed_ms:lastEnd-began,error:safeError(error),signal_aborted:options.signal?.aborted===true});throw error;}
}
const {fetchVerifiedBaseProof}=await import(pathToFileURL(resolve(ROOT,'site/ci-model-cache.mjs')));
const {fetchVerifiedPosterBaseline,readVerifiedPosterBundle}=await import(pathToFileURL(resolve(ROOT,'site/gallery-poster-cache.mjs')));
const {posterSharedInputs}=await import(pathToFileURL(resolve(ROOT,'site/gallery-poster-inputs.mjs')));
function classify(reasons){return reasons.map(text=>text.includes('fetch failed')?'fetch failed':text.includes('timeout')?'timeout':text.includes('Protected source')||text.includes('control plane')?'policy mismatch':text.includes('Base has no v2')?'legacy policy':text.includes('No successful')||text.includes('No independently')?'no compatible proof':text.includes('ancestor')?'ancestry rejected':'other validation rejection');}
for(const domain of ['model-1','gallery','model-2']){
 trial=domain;emit({stage:'trial-start',source:CURRENT,base:BASE,node:process.version});
 if(domain==='gallery'){
  const shared=await posterSharedInputs(ROOT),found=await fetchVerifiedPosterBaseline({root:ROOT,repository:REPOSITORY,baseSha:BASE,currentSha:CURRENT,shared,policy_sha256:inputs.policy_sha256,fetchImpl:tracedFetch});
  const bundle=readVerifiedPosterBundle(found.verified);const summary={trial,verified:!!found.verified,run_id:found.verified?.run_id,artifact_id:found.verified?.artifact_id,pairs:bundle?.proof.posters.length,reasons:classify(found.reasons)};summaries.push(summary);emit({stage:'trial-result',...summary});
 }else{
  const found=await fetchVerifiedBaseProof({root:ROOT,repository:REPOSITORY,baseSha:BASE,currentSha:CURRENT,inputs,fetchImpl:tracedFetch});
  const summary={trial,verified:!!found.verifiedBaseProof,run_id:found.verifiedBaseProof?.run_id,artifact_id:found.verifiedBaseProof?.artifact_id,models:found.baseProof?.models.length,reasons:classify(found.reasons)};summaries.push(summary);emit({stage:'trial-result',...summary});
 }
}
writeFileSync(resolve(process.env.RUNNER_TEMP,'proof-transport-observations.json'),JSON.stringify({kind:'read-only-transport-diagnostic',transport_trial:'event-loop-yield-and-bounded-socket-get-retry',not_release_evidence:true,source:CURRENT,base:BASE,inputs_sha256:createHash('sha256').update(inputsBytes).digest('hex'),events,summaries},null,2)+'\n');
assert(summaries.every(row=>row.verified),'One or more diagnostic lookups failed; observations preserved, no release evidence emitted');

import assert from 'node:assert/strict';
import {proofGet} from './ci-proof-fetch.mjs';
const url='https://api.github.com/repos/owner/repo/actions/runs/1';
const socket=()=>Object.assign(new TypeError('secret signed URL must not be logged'),{cause:{code:'UND_ERR_SOCKET'}});
const options={headers:{Authorization:'Bearer test-only-secret'},signal:AbortSignal.timeout(10000)};
let calls=0;
const response=new Response('exact bytes');
assert.equal(await proofGet(url,options,{stage:'model API actions/runs/1',fetchImpl:async(actualURL,actualOptions)=>{
 calls++;assert.equal(actualURL,url);assert.equal(actualOptions,options);
 if(calls===1)throw socket();return response;
}}),response);
assert.equal(calls,2);assert.equal(await response.text(),'exact bytes');
calls=0;
await assert.rejects(()=>proofGet(url,options,{stage:'model API actions/runs/1',fetchImpl:async()=>{calls++;throw socket();}}),error=>{
 assert.equal(error.message,'Proof GET transport failed at model API actions/runs/1 (UND_ERR_SOCKET)');
 assert(!JSON.stringify(error).includes('secret'));assert.equal(error.cause,undefined);return true;
});assert.equal(calls,3);
for(const code of ['CERT_HAS_EXPIRED','UND_ERR_CONNECT_TIMEOUT','ECONNRESET','EACCES']){
 calls=0;await assert.rejects(()=>proofGet(url,options,{fetchImpl:async()=>{calls++;throw Object.assign(new TypeError('secret'),{cause:{code}});}}),new RegExp(code));assert.equal(calls,1);
}
for(const code of ['https://storage.invalid/?signature=secret','secret\nAuthorization: token']){
 calls=0;await assert.rejects(()=>proofGet(url,options,{fetchImpl:async()=>{calls++;throw Object.assign(new TypeError('secret'),{cause:{code}});}}),error=>{
  assert.equal(error.message,'Proof GET transport failed at proof read (TRANSPORT_ERROR)');assert.equal(error.cause,undefined);return true;
 });assert.equal(calls,1);
}
for(const status of [401,403,404,429,500,503]){
 calls=0;const rejected=new Response('reject',{status});
 assert.equal(await proofGet(url,options,{fetchImpl:async()=>{calls++;return rejected;}}),rejected);assert.equal(calls,1);
}
calls=0;
for(const bad of [{method:'POST'},{body:'not allowed'}])await assert.rejects(()=>proofGet(url,bad,{fetchImpl:async()=>{calls++;}}));
assert.equal(calls,0);
const controller=new AbortController(),reason=new Error('explicit cancellation');
controller.abort(reason);await assert.rejects(()=>proofGet(url,{signal:controller.signal},{fetchImpl:async()=>{calls++;}}),error=>error===reason);assert.equal(calls,0);
const mid=new AbortController();calls=0;
await assert.rejects(()=>proofGet(url,{signal:mid.signal},{fetchImpl:async()=>{calls++;mid.abort(reason);throw socket();}}),error=>error===reason);assert.equal(calls,1);
calls=0;const deadline=AbortSignal.timeout(1);
await new Promise(resolve=>setTimeout(resolve,5));
await assert.rejects(()=>proofGet(url,{signal:deadline},{fetchImpl:async()=>{calls++;}}),error=>error.name==='TimeoutError');assert.equal(calls,0);
calls=0;
const malformed=await proofGet(url,options,{fetchImpl:async()=>{calls++;return new Response('not JSON');}});
await assert.rejects(()=>malformed.json());assert.equal(calls,1,'Body/content failures are not transport retries');
calls=0;const bodyError=socket();
const brokenBody=await proofGet(url,options,{fetchImpl:async()=>{calls++;return new Response(new ReadableStream({start(controller){controller.error(bodyError);}}));}});
await assert.rejects(()=>brokenBody.arrayBuffer(),error=>error===bodyError);assert.equal(calls,1,'A body socket error is not a replayable request failure');
let yielded=false;setImmediate(()=>{yielded=true;});
await proofGet(url,options,{fetchImpl:async()=>{assert(yielded,'A request must yield after synchronous validation');return new Response('ok');}});
console.log('Proof GET transport: event-loop yield, bounded same-request socket retry, unchanged signal/deadline, safe errors and non-retry guards pass.');

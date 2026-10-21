import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
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
// Separate processes have no runner/server handle accidentally keeping the
// timeout alive. Exit 13 is a failure, never a successful fallback.
const budgetURL=new URL('./ci-proof-budget.mjs',import.meta.url).href;
const child=(body,{timeout=2000}={})=>{
 const result=spawnSync(process.execPath,['--input-type=module','-e',`import assert from 'node:assert/strict';import {proofReadBudget} from ${JSON.stringify(budgetURL)};${body}`],{encoding:'utf8',timeout});
 assert.equal(result.error,undefined,result.error?.message);assert.equal(result.signal,null,result.stderr);assert.equal(result.status,0,result.stderr);assert.match(result.stdout,/settled/);
};
for(const operation of [
 "new Promise((resolve,reject)=>budget.signal.addEventListener('abort',()=>reject(budget.signal.reason),{once:true}))",
 'new Promise(()=>{})',
 "new Response(new ReadableStream({start(){}})).json()"
])child(`const budget=proofReadBudget(40,{maximumMs:40,onTiming:()=>{}});await assert.rejects(()=>budget.measureAsync('pending read',()=>${operation}),error=>error.name==='TimeoutError');console.log('settled');`);
for(const operation of ['Promise.resolve(7)',"Promise.reject(new Error('read failed'))"])
 child(`const budget=proofReadBudget(10000,{maximumMs:10000,onTiming:()=>{}});try{await budget.measureAsync('quick read',()=>${operation});}catch(error){assert.equal(error.message,'read failed');}console.log('settled');`,{timeout:1500});
child(`const budget=proofReadBudget(100,{maximumMs:100,onTiming:()=>{}});await budget.measureAsync('first read',()=>new Promise(resolve=>setTimeout(resolve,65)));assert(budget.remaining()<60,'A stage cannot reset the total deadline');await assert.rejects(()=>budget.measureAsync('second read',()=>new Promise(()=>{})),error=>error.name==='TimeoutError');console.log('settled');`);
child(`const budget=proofReadBudget(20,{maximumMs:20,onTiming:()=>{}});await assert.rejects(()=>budget.measureAsync('blocked read',()=>{Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,30);return 'late';}),error=>error.name==='TimeoutError');console.log('settled');`);
child(`const budget=proofReadBudget(20,{maximumMs:20,onTiming:()=>{}});await assert.rejects(()=>budget.measureAsync('late rejection',()=>new Promise((_,reject)=>setTimeout(()=>reject(new Error('late read')),50))),error=>error.name==='TimeoutError');await new Promise(resolve=>setTimeout(resolve,65));console.log('settled');`);
child(`const {getEventListeners}=await import('node:events');const controller=new AbortController(),reason=new Error('explicit abort'),original=AbortSignal.timeout;let budget;try{AbortSignal.timeout=()=>controller.signal;budget=proofReadBudget(10000,{maximumMs:10000,onTiming:()=>{}});}finally{AbortSignal.timeout=original;}setTimeout(()=>controller.abort(reason),10);await assert.rejects(()=>budget.measureAsync('cancelled read',()=>new Promise(()=>{})),error=>error===reason);assert.equal(getEventListeners(budget.signal,'abort').length,0);console.log('settled');`,{timeout:1500});
child(`const {getEventListeners}=await import('node:events');const budget=proofReadBudget(10000,{maximumMs:10000,onTiming:()=>{}});for(let i=0;i<20;i++){assert.equal(await budget.measureAsync('quick read',()=>7),7);assert.equal(getEventListeners(budget.signal,'abort').length,0);}await assert.rejects(()=>budget.measureAsync('failed read',()=>{throw new Error('read failed');}),/read failed/);assert.equal(getEventListeners(budget.signal,'abort').length,0);console.log('settled');`,{timeout:1500});
console.log('Proof GET transport: event-loop yield, bounded same-request socket retry, unchanged signal/deadline, safe errors and non-retry guards pass.');
console.log('Proof async budget: child-process abort, uncooperative read/body, shared deadline, synchronous expiry, late rejection and timer cleanup pass.');

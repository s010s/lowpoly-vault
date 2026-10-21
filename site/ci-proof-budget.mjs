/** One total read budget, including synchronous local validation. */
import assert from 'node:assert/strict';
import {performance} from 'node:perf_hooks';

export function proofReadBudget(timeoutMs,{maximumMs,onTiming=entry=>console.info(`Proof lookup timing: ${entry.stage} ${entry.elapsed_ms}ms (${entry.total_ms}ms total).`)}={}){
 assert(Number.isSafeInteger(timeoutMs)&&timeoutMs>=0&&timeoutMs<=maximumMs,'Proof lookup may only shorten its total budget');
 const started=performance.now(),deadline=started+timeoutMs,signal=AbortSignal.timeout(timeoutMs);
 const check=()=>{
  signal.throwIfAborted();
  // AbortSignal timers cannot fire while synchronous Git/validation blocks the
  // event loop. Check monotonic elapsed time too, before doing any more work.
  if(performance.now()>=deadline)throw new DOMException('Proof lookup total budget exhausted','TimeoutError');
 };
 const remaining=()=>{check();return Math.max(1,Math.ceil(deadline-performance.now()));};
 const safeStage=stage=>assert(typeof stage==='string'&&/^[A-Za-z0-9_./ -]{1,180}$/.test(stage),'Safe proof timing stage required');
 const report=(stage,start)=>onTiming({stage,elapsed_ms:Math.round(performance.now()-start),total_ms:Math.round(performance.now()-started)});
 const measure=(stage,operation)=>{
  check();safeStage(stage);const start=performance.now();
  try{const result=operation();check();return result;}
  finally{report(stage,start);}
 };
 const measureAsync=async(stage,operation)=>{
  check();safeStage(stage);const start=performance.now();
  let timer,onAbort;
  try{
   // AbortSignal.timeout is unreferenced. A pending transport/body promise can
   // otherwise outlive every active handle and terminate top-level await before
   // the caller receives a timeout. Keep only this await alive, and independently
   // settle it even if the operation never handles abort. All stages share the
   // original deadline; successful/error paths must not retain this timer.
   const expired=new Promise((_,reject)=>{
    const milliseconds=remaining();onAbort=()=>reject(signal.reason);
    signal.addEventListener('abort',onAbort,{once:true});
    timer=setTimeout(()=>reject(signal.aborted?signal.reason:new DOMException('Proof lookup total budget exhausted','TimeoutError')),milliseconds);
    if(signal.aborted)onAbort();
   });
   const result=await Promise.race([Promise.resolve().then(()=>{check();return operation();}),expired]);check();return result;
  }finally{clearTimeout(timer);if(onAbort)signal.removeEventListener('abort',onAbort);report(stage,start);}
 };
 return {signal,check,remaining,measure,measureAsync};
}

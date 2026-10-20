/** Transport only. A successful read never substitutes for provenance or hashes. */
import assert from 'node:assert/strict';

const codeFor=error=>{
 const code=error?.cause?.code||error?.code;
 return typeof code==='string'&&/^[A-Z][A-Z0-9_]{0,63}$/.test(code)?code:'TRANSPORT_ERROR';
};
export async function proofGet(url,options={},{
 fetchImpl=fetch,stage='proof read'
}={}){
 assert.equal((options.method||'GET').toUpperCase(),'GET','Proof transport permits GET only');
 assert.equal(options.body,undefined,'Proof GET cannot have a body');
 assert(typeof stage==='string'&&/^[A-Za-z0-9_./ -]{1,180}$/.test(stage),'Safe proof request stage required');
 for(let attempt=1;attempt<=3;attempt++){
  // Long synchronous policy/archive checks can leave a closed keep-alive socket
  // queued on the event loop. Process its close event before the next read.
  await new Promise(setImmediate);
  options.signal?.throwIfAborted();
  try{return await fetchImpl(url,options);}
  catch(error){
   // Keep the original total deadline and abort reason. Never retry a response,
   // TLS/auth failure, body decode, digest mismatch or other validation failure.
   if(options.signal?.aborted)throw options.signal.reason;
   if(error?.name==='AbortError'||error?.name==='TimeoutError')throw error;
   const code=codeFor(error);
   if(attempt===3||error?.cause?.code!=='UND_ERR_SOCKET')
    throw new Error(`Proof GET transport failed at ${stage} (${code})`);
   console.warn(`Proof GET socket closed at ${stage}; retry ${attempt+1}/3.`);
  }
 }
}

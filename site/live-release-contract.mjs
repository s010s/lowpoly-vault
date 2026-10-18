/** Poll the actual HTTP manifest until the exact deployed payload is visible. */
import assert from 'node:assert/strict';
export const payloadScope = manifest => manifest.assets.map(a=>({id:a.id,glb:a.sha256.glb,blend:a.sha256.blend,preview:a.sha256.preview}));
export async function waitForDeployedRelease(url,expected,{timeout=180000,interval=5000}={}) {
 const deadline=Date.now()+timeout;
 let lastError;
 while(true) {
  try {
   const response=await fetch(url,{cache:'no-store',signal:AbortSignal.timeout(Math.min(15000,Math.max(1,deadline-Date.now())))});
   // WHATWG Response uses a boolean .ok; Playwright APIResponse uses .ok().
   assert(response.ok,`Deployed manifest HTTP ${response.status}`);
   const current=await response.json();assert.deepEqual(payloadScope(current),payloadScope(expected));return current;
  }catch(error){
   if(error instanceof SyntaxError || error instanceof TypeError && error.message!=='fetch failed')throw error;
   if(error.name!=='TimeoutError'||!lastError)lastError=error;
   if(Date.now()>=deadline)throw lastError;
   await new Promise(r=>setTimeout(r,Math.min(interval,Math.max(1,deadline-Date.now()))));
  }
 }
}

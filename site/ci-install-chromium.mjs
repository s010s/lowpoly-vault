/** Retry only browser installation, never application checks or apt security. */
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {setTimeout as delay} from 'node:timers/promises';
import {pathToFileURL} from 'node:url';

export const CHROMIUM_INSTALL=Object.freeze(['npx','playwright','install','--with-deps','chromium']);
export async function installChromium({run=spawnSync,sleep=delay,log=console.log}={}){
 for(let attempt=1;attempt<=3;attempt++){
  log(`Chromium installation attempt ${attempt}/3: ${CHROMIUM_INSTALL.join(' ')}`);
  let result;try{result=run(CHROMIUM_INSTALL[0],CHROMIUM_INSTALL.slice(1),{stdio:'inherit',shell:false});}catch(error){result={error,status:null};}
  if(result?.status===0&&!result.error&&!result.signal){log(`Chromium installation attempt ${attempt}/3 succeeded.`);return 0;}
  const status=Number.isInteger(result?.status)&&result.status>0&&result.status<=255?result.status:1;
  log(`Chromium installation attempt ${attempt}/3 failed: ${result?.signal||result?.error?.message||`exit ${status}`}`);
  // Respect cancellation instead of restarting a deliberately stopped process.
  if(result?.signal)return result.signal==='SIGINT'?130:result.signal==='SIGTERM'?143:1;
  if(status===130||status===143)return status;
  if(attempt===3)return status;
  const wait=attempt*10000;log(`Retrying the unchanged installer in ${wait/1000}s.`);await sleep(wait);
 }
 throw Error('Unreachable installer state');
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 assert.equal(process.argv.length,2,'The Chromium installer accepts no alternate command or arguments');
 process.exitCode=await installChromium();
}

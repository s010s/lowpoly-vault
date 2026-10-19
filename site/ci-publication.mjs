/** In-job memoization only. The first publication gate always runs; output audits never skip. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,rmSync} from 'node:fs';
import {resolve,dirname,sep} from 'node:path';
import {pathToFileURL} from 'node:url';
import {checkPublishedManifest} from './initial-release.mjs';
import {git,sha256,runtimeConfig} from './ci-provenance.mjs';
const fingerprint=()=>({source_commit:git('rev-parse','HEAD'),source_tree:git('rev-parse','HEAD^{tree}'),manifest_sha256:sha256(readFileSync('assets/manifest.json')),runtime_config:runtimeConfig()});
function receiptPath(){
  // Never consume a repository-authored receipt, including one hidden by .gitignore.
  const temp=process.env.RUNNER_TEMP,path=process.env.CI_PUBLICATION_RECEIPT;
  if(process.env.GITHUB_ACTIONS!=='true'||!temp||!path)return null;
  const target=resolve(path),outside=resolve(temp)+sep;
  assert(target.startsWith(outside)&&!target.startsWith(process.cwd()+sep),'Publication receipt must be in runner temporary storage');
  return target;
}
function clean(){return git('status','--porcelain')==='';}
export async function checkedPublication(){
  try{
    const path=receiptPath();
    if(path&&clean()){
      const receipt=JSON.parse(readFileSync(path));
      assert.equal(receipt.version,1);assert.equal(receipt.run_id,process.env.GITHUB_RUN_ID);assert.equal(receipt.run_attempt,process.env.GITHUB_RUN_ATTEMPT);
      assert.deepEqual(receipt.input,fingerprint());
      console.log('Publication gate: reused this job’s successful unchanged-source check; complete output audit still runs.');
      return JSON.parse(readFileSync('assets/manifest.json'));
    }
  }catch{ /* Any missing, stale or malformed receipt falls back to the original gate. */ }
  return checkPublishedManifest();
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  const path=receiptPath();if(path)rmSync(path,{force:true});
  const before=clean()?fingerprint():null;
  const manifest=await checkPublishedManifest();
  if(path&&before&&clean()){
    assert.deepEqual(before,fingerprint(),'Publication inputs changed during validation');
    mkdirSync(dirname(path),{recursive:true});writeFileSync(path,JSON.stringify({version:1,run_id:process.env.GITHUB_RUN_ID,run_attempt:process.env.GITHUB_RUN_ATTEMPT,input:before})+'\n',{mode:0o600});
  }
  console.log(`Publication gate passed: ${manifest.assets.length} checked assets.`);
}

/** Local build result is necessary, never sufficient authority for contract reuse.
 * The caller must independently authenticate scope in this process. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {runtimeConfig} from './ci-provenance.mjs';
export const fastBuildIdentity=()=>({source_commit:process.env.GITHUB_SHA,run_id:Number(process.env.GITHUB_RUN_ID),run_attempt:Number(process.env.GITHUB_RUN_ATTEMPT),repository:process.env.GITHUB_REPOSITORY,runtime:runtimeConfig()});
export function canReuseBuildContracts(scope,{root=process.cwd(),identity=fastBuildIdentity()}={}){
 try{
  assert(scope?.eligible&&scope.baseline);
  assert(/^[a-f0-9]{40}$/.test(identity.source_commit)&&!/^0+$/.test(identity.source_commit));
  assert(Number.isSafeInteger(identity.run_id)&&identity.run_id>0&&Number.isSafeInteger(identity.run_attempt)&&identity.run_attempt>0);
  assert(typeof identity.repository==='string'&&/^[\w.-]+\/[\w.-]+$/.test(identity.repository));
  const r=JSON.parse(readFileSync(resolve(root,'qa/ci-timings/build.json')));
  assert.equal(r.version,1);assert.equal(r.mode,'additive');assert.equal(r.status,'pass');
  for(const key of Object.keys(identity))assert.deepEqual(r[key],identity[key]);
  assert.deepEqual(r.baseline,scope.baseline);assert.deepEqual(r.added_ids,scope.added_ids);
  assert(Number.isSafeInteger(r.artifact_id)&&r.artifact_id>0);assert.match(r.artifact_digest||'',/^sha256:[a-f0-9]{64}$/);
  assert.deepEqual(r.reused,['vite','historical-package-generation']);
  assert.deepEqual(r.phases.map(p=>p.name),['publication-check','registry-check','incremental-copy-and-package','full-release-audit']);
  for(const p of r.phases){assert.equal(p.exit_code,0);assert.equal(p.signal,null);}
  return true;
 }catch{return false;}
}

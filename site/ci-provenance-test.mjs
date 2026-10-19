import assert from 'node:assert/strict';
import {assertReceipt,sha256} from './ci-provenance.mjs';
import {assertTrustedRun,assertArtifact} from './ci-reuse.mjs';
const hash='a'.repeat(64),head='b'.repeat(40),base='c'.repeat(40),tree='d'.repeat(40),repository='owner/repository';
const expected={kind:'pages',source_tree:tree,repository,run_id:12,run_attempt:1,comparison_base:base,head_sha:head,pull_request:5,validation_ref:'refs/pull/5/merge',control_sha256:hash,runtime_config:{site_base:'/gallery/',site_origin:'https://example.test',node_major:'22'}};
const receipt={...expected,version:1,source_commit:'e'.repeat(40),base_control_sha256:hash,event:'pull_request'};
assert.doesNotThrow(()=>assertReceipt(receipt,expected));
for(const patch of [null,{source_tree:'0'.repeat(40)},{head_sha:'0'.repeat(40)},{comparison_base:'0'.repeat(40)},{run_id:13},{run_attempt:2},{base_control_sha256:'0'.repeat(64)},{control_sha256:'0'.repeat(64)},{runtime_config:{}},{event:'push'}]){
 assert.throws(()=>assertReceipt(patch===null?null:{...receipt,...patch},expected),JSON.stringify(patch));
}
const run={id:12,run_attempt:1,event:'pull_request',status:'completed',conclusion:'success',path:'.github/workflows/pages.yml',repository:{full_name:repository},head_repository:{full_name:repository},head_sha:head,check_suite_id:42,pull_requests:[{number:5,base:{sha:base,repo:{id:7}},head:{sha:head,repo:{id:7}}}]};
const runExpected={repository,head,workflow:'pages.yml',pr:5,base};
assert.doesNotThrow(()=>assertTrustedRun(run,runExpected));
for(const patch of [{event:'push'},{status:'in_progress'},{conclusion:'failure'},{path:'.github/workflows/forged.yml'},{head_repository:{full_name:'fork/repository'}},{head_sha:'0'.repeat(40)},{repository:{full_name:'other/repository'}},{check_suite_id:null}])assert.throws(()=>assertTrustedRun({...run,...patch},runExpected));
const bytes=Buffer.from('immutable artifact'),artifact={expired:false,digest:`sha256:${sha256(bytes)}`,workflow_run:{id:12,head_sha:head,repository_id:7,head_repository_id:7}};
assert.doesNotThrow(()=>assertArtifact(artifact,run,bytes));
assert.throws(()=>assertArtifact(artifact,run,Buffer.from('tampered')));
for(const patch of [{expired:true},{digest:null},{workflow_run:{...artifact.workflow_run,id:13}},{workflow_run:{...artifact.workflow_run,head_repository_id:8}}])assert.throws(()=>assertArtifact({...artifact,...patch},run,bytes));
console.log('CI provenance: exact-tree hit; changed merge tree, stale source/base/attempt/config, policy forgery, missing receipt, fork, failed checks and tampered/missing artifact digest rejected.');

/** Shared-code regressions stay conservative; per-model work remains explicitly bounded. */
import assert from 'node:assert/strict';
import {readFileSync,existsSync,mkdirSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {loadVerifiedRelease} from './ci-layered-release-scope.mjs';
const out=resolve(process.env.QA_SHARED_OUTPUT_DIR||process.env.QA_OUTPUT_DIR||'qa/post-release-shared');
const report={status:'RUNNING',phase:'initialize',expected:{source_commit:process.env.DEPLOYED_SHA||null,run_id:process.env.UPSTREAM_RUN_ID||null,run_attempt:process.env.UPSTREAM_RUN_ATTEMPT||null},checks:{scope:'NOT_RUN',shared:'NOT_RUN'},results:[],production_acceptance:false,reusable_browser_proof:false,scope_note:'Local-server regressions against exact downloaded deployed build, not public-origin acceptance.'};
try{
 report.phase='receipt-scope-build-verification';
const {scope,context:deployment}=loadVerifiedRelease();report.checks.scope='PASS';Object.assign(report,{source_commit:scope.source_commit,base_commit:scope.base_commit,run_id:deployment.runId,run_attempt:deployment.runAttempt,affected_ids:scope.affected_ids,shared_runtime_required:scope.shared_runtime_required});
const manifest=JSON.parse(readFileSync('assets/manifest.json'));
const ids=scope.affected_ids.length?scope.affected_ids:[manifest.assets[0].id];
const env={...process.env,GITHUB_SHA:scope.source_commit,GALLERY_DIR:'dist',QA_MODEL_IDS:ids.join(','),CI_RUNTIME:'false',CI_MODEL_PROOF_ACTIVE:'false'};
const commands=scope.shared_runtime_required?[
 ...(existsSync('site/brand-browser-test.mjs')?[['site/brand-browser-test.mjs']]:[]),
 ['site/gallery-browser-test.mjs'],['site/concept-seven-browser-test.mjs'],['site/concept-quartets-browser-test.mjs'],['site/concept-landair-browser-test.mjs'],
 ...scope.shared_tasks.map(task=>['site/ci-review.mjs',task])
]:[];

 report.phase='shared-browser-regressions';
 for(const [script,task]of commands){const child=spawnSync(process.execPath,[script],{stdio:'inherit',env:{...env,...(task?{CI_REVIEW_TASK:task}:{})}});report.results.push({script,task:task||null,exit_code:child.status,signal:child.signal});assert(!child.error&&child.status===0,script+(task?':'+task:''));}
 report.checks.shared='PASS';report.status='PASS';report.phase='complete';
}catch(error){report.status='FAIL';report.failed_phase=report.phase;report.error=error.stack;process.exitCode=1;}
finally{mkdirSync(out,{recursive:true});writeFileSync(resolve(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}

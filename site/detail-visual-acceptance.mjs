/** One immutable PR73 visual disposition. Never rewrites the original failed run/report. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,mkdtemp,rm} from 'node:fs/promises';
import {resolve,join} from 'node:path';
import {tmpdir} from 'node:os';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {detailAuthorityTransport} from './detail-capture-authority.mjs';
import {immutableGitEnv} from './ci-git.mjs';
export const VISUAL_REVIEW=Object.freeze({repository:'s010s/lowpoly-vault',repository_id:1422307926,head:'a62081a02c3fc8c28a7d1689948d1d5b0b08cb99',base:'c5624cfcdbb811aa532696725ea0fe9278cc9295',source:'13a427f3ed11ed5f73436ab02664c7da66f95222',run:40260183787,attempt:1,workflow:387257789,job:121370670061,suite:109114860220,artifact:12626805402,zip_bytes:442546023,zip_sha256:'00edb50320b0effc1a1deacdbb57c2574899fc6c4f0e509a7c0fc62cef833774',report_sha256:'9fdd81660e6c95108eb62747bdb5dc6497346614364c3eea7d018bc0fa8f6d9a',review_path:'qa/detail-presentation-evidence/reviews/40260183787-visual-disposition.json',review_sha256:'dc124ae6f55d6484b132eb82f5ba94bf203cda70488787538266fe9ac1a2a88a',workflow_sha256:'20c213331c505f0ad3ebcd69dca64a2850893607c3750a082f36b38c1d0b6e43',browser_sha256:'d326298909154f343a0d924f714792e92e4b2a45a61bf61f3bc1bbc078b53ee3'});
// Only acceptance-layer changes are excluded. Every other tracked byte, including
// all 602 GLBs, 264/338 posters, renderer, CSS, app, lockfile and metadata must match.
export const ACCEPTANCE_PATHS=Object.freeze(['.github/workflows/pages.yml','.github/workflows/full-release-review.yml','site/detail-visual-acceptance.mjs','site/detail-visual-acceptance-test.mjs','site/detail-presentation-browser-test.mjs','site/detail-visual-disposition-test.mjs',VISUAL_REVIEW.review_path]);
export const ACCEPTANCE_CONTROL_HASHES=Object.freeze({
 'site/detail-presentation-browser-test.mjs':'d436cc05a1b83e63dcc0043a4bd807d16acd5133592d9846532053dac0cfe615',
 '.github/workflows/pages.yml':'8621b482813e0944f145f3f27dde873a9dcd1cd2af9b11e49d90c84cedc6bf43',
 '.github/workflows/full-release-review.yml':'b626703e64ff2c7fc5feb91dccf8f9716c6246462bdb3a30f544ed1723e8dc2d'
});
export function assertAcceptanceControls(hashes){assert.deepEqual(hashes,ACCEPTANCE_CONTROL_HASHES,'One-time acceptance executable changed; new independent review required');}
const sha=b=>createHash('sha256').update(b).digest('hex');
const git=(root,...args)=>execFileSync('git',args,{cwd:root,env:immutableGitEnv(),maxBuffer:32*1024*1024,timeout:60000});
export function assertRuntimeDiff(paths){assert.equal(new Set(paths).size,paths.length);for(const p of paths)assert(ACCEPTANCE_PATHS.includes(p),'Reviewed runtime changed: '+p);}
export function assertRun(run){const p=VISUAL_REVIEW;assert.equal(run.id,p.run);assert.equal(run.run_attempt,p.attempt);assert.equal(run.head_sha,p.head);assert.equal(run.head_branch,'fix/right-preview-repair-20261025');assert.equal(run.workflow_id,p.workflow);assert.equal(run.path,'.github/workflows/pages.yml');assert.equal(run.event,'pull_request');assert.equal(run.status,'completed');assert.equal(run.conclusion,'failure','Original failure must remain visible');assert.equal(run.check_suite_id,p.suite);for(const key of ['repository','head_repository']){assert.equal(run[key].id,p.repository_id);assert.equal(run[key].full_name,p.repository);}}
export function assertJob(job){const p=VISUAL_REVIEW;assert.equal(job.id,p.job);assert.equal(job.run_id,p.run);assert.equal(job.run_attempt,1);assert.equal(job.head_sha,p.head);assert.equal(job.name,'build');assert.equal(job.status,'completed');assert.equal(job.conclusion,'failure');const needed=['Run actions/checkout@v4','Run actions/setup-node@v4','Run npm ci','Run affected regressions','Validate source, build once and audit final dist','Install pinned browser for mandatory right-detail first-frame acceptance','Retain supplemental right-detail pixels outside Git'];for(const name of needed){const steps=job.steps.filter(s=>s.name===name);assert.equal(steps.length,1);assert.equal(steps[0].conclusion,'success');}assert.deepEqual(job.steps.filter(s=>s.conclusion==='failure').map(s=>s.name),['Actual built-page right poster and native first-frame parity']);}
export function assertArtifact(a,job){const p=VISUAL_REVIEW;assert.equal(a.id,p.artifact);assert.equal(a.name,`right-detail-dist-${p.source}-${p.run}-1`);assert.equal(a.expired,false);assert.equal(a.size_in_bytes,p.zip_bytes);assert.equal(a.digest,'sha256:'+p.zip_sha256);assert.equal(a.workflow_run.id,p.run);assert.equal(a.workflow_run.head_sha,p.head);assert.equal(a.workflow_run.repository_id,p.repository_id);assert.equal(a.workflow_run.head_repository_id,p.repository_id);assert.equal(a.workflow_run.head_branch,'fix/right-preview-repair-20261025');const upload=job.steps.find(s=>s.name==='Retain supplemental right-detail pixels outside Git'),t=Date.parse(a.created_at);assert(Number.isFinite(t)&&t>=Date.parse(upload.started_at)&&t<=Date.parse(upload.completed_at));}
export async function compareRuntimeTrees({oldRoot,newRoot,oldTree,newTree}){
 const changes=[];
 const entries=async(reader,id)=>{if(id===null)return new Map();const tree=await reader(id);assert.equal(tree.sha,id,'Tree response identity changed');assert.equal(tree.truncated,false,'Truncated tree is not proof');const map=new Map();for(const e of tree.tree){assert(typeof e.path==='string'&&e.path&&!e.path.includes('/')&&!['.','..'].includes(e.path));assert(!map.has(e.path));assert(/^[0-9a-f]{40}$/.test(e.sha));assert(['blob','tree','commit'].includes(e.type));map.set(e.path,e);}return map;};
 const walk=async(a,b,prefix='')=>{if(a===b)return;const [old,current]=await Promise.all([entries(oldTree,a),entries(newTree,b)]);for(const name of new Set([...old.keys(),...current.keys()])){const path=prefix+name,x=old.get(name),y=current.get(name);if(x&&y&&x.sha===y.sha&&x.mode===y.mode&&x.type===y.type)continue;if(ACCEPTANCE_PATHS.includes(path)){assert(y&&y.type==='blob'&&y.mode==='100644','Acceptance leaf must remain a regular file');changes.push(path);continue;}assert(ACCEPTANCE_PATHS.some(p=>p.startsWith(path+'/')),'Reviewed runtime changed: '+path);for(const e of [x,y])if(e)assert(e.type==='tree'&&e.mode==='040000','Ancestor cannot become symlink/gitlink/file');await walk(x?.sha??null,y?.sha??null,path+'/');}};
 await walk(oldRoot,newRoot);return changes.sort();
}
export async function assertReviewedRuntime({root=process.cwd(),api,currentSha=process.env.GITHUB_SHA}={}){
 const p=VISUAL_REVIEW;assertAcceptanceControls(Object.fromEntries(await Promise.all(Object.keys(ACCEPTANCE_CONTROL_HASHES).map(async path=>[path,sha(await readFile(join(root,path)))]))));assert(/^[0-9a-f]{40}$/.test(currentSha||''));assert.equal(git(root,'rev-parse','HEAD').toString().trim(),currentSha);assert.equal(git(root,'status','--porcelain','--untracked-files=no').toString().trim(),'');
 const source=await api.json('git/commits/'+p.source);assert.equal(source.sha,p.source);assert.deepEqual(source.parents.map(x=>x.sha),[p.base,p.head]);
 const currentTree=git(root,'rev-parse',currentSha+'^{tree}').toString().trim();
 const paths=await compareRuntimeTrees({oldRoot:source.tree.sha,newRoot:currentTree,oldTree:id=>api.json('git/trees/'+id),newTree:async id=>({sha:id,truncated:false,tree:git(root,'ls-tree','-z',id).toString().split('\0').filter(Boolean).map(row=>{const at=row.indexOf('\t');assert(at>0);const header=row.slice(0,at),path=row.slice(at+1),[mode,type,sha]=header.split(' ');return {mode,type,sha,path};})})});
 assert.equal(sha(await api.source('.github/workflows/pages.yml',p.source)),p.workflow_sha256);
 // This exact historical executable ran the complete PNG/609-control verifier,
 // accumulated all failures, and wrote the immutable report only afterward.
 assert.equal(sha(await api.source('site/detail-presentation-browser-test.mjs',p.source)),p.browser_sha256);
 assert.equal(sha(await readFile(join(root,p.review_path))),p.review_sha256);
 return {current_source:currentSha,tested_source:p.source,tested_tree:source.tree.sha,acceptance_only_changes:paths,runtime_identity:'ALL_OTHER_TRACKED_BYTES_IDENTICAL'};
}
export const extractPython=String.raw`import zipfile,sys,pathlib,stat
z=zipfile.ZipFile(sys.argv[1]); root=pathlib.Path(sys.argv[2]); seen=set(); total=0
for f in z.infolist():
 p=pathlib.PurePosixPath(f.filename)
 assert not f.is_dir() and not p.is_absolute() and '..' not in p.parts and len(p.parts)==1
 assert f.filename not in seen and not stat.S_ISLNK(f.external_attr>>16)
 assert f.filename in ('report.json','report.sha256') or f.filename.endswith('.png')
 assert 0<=f.file_size<=600*1024*1024
 seen.add(f.filename); total+=f.file_size
 assert total<=2*1024*1024*1024 and len(seen)<=2300
 with z.open(f) as src, open(root/f.filename,'xb') as out:
  while True:
   b=src.read(1024*1024)
   if not b: break
   out.write(b)
assert len([x for x in seen if x.endswith('.png')])==2295
assert 'report.json' in seen and 'report.sha256' in seen
`;
export async function authenticateVisualEvidence({root=process.cwd(),api,currentSha=process.env.GITHUB_SHA,out=resolve('qa/detail-browser-dist')}={}){
 const manifest=JSON.parse(await readFile(join(root,'assets/manifest.json')));
 if(manifest.publication?.same_id_successor_append){const {authenticateAppendVisualEvidence}=await import('./detail-append-visual-acceptance.mjs');return authenticateAppendVisualEvidence({root,api,currentSha,out,legacy:{VISUAL_REVIEW,ACCEPTANCE_CONTROL_HASHES,compareRuntimeTrees,assertRun,assertJob,assertArtifact,extractPython}});}
 const p=VISUAL_REVIEW,binding=await assertReviewedRuntime({root,api,currentSha});const run=await api.json(`actions/runs/${p.run}`);assertRun(run);assertRun(await api.json(`actions/runs/${p.run}/attempts/1`));const suite=await api.json(`check-suites/${p.suite}`);assert.equal(suite.id,p.suite);assert.equal(suite.head_sha,p.head);assert.equal(suite.app?.id,15368);assert.equal(suite.app?.slug,'github-actions');assert.equal(suite.status,'completed');assert.equal(suite.conclusion,'failure');const job=await api.json(`actions/jobs/${p.job}`);assertJob(job);const artifact=await api.json(`actions/artifacts/${p.artifact}`);assertArtifact(artifact,job);
 const dir=await mkdtemp(join(tmpdir(),'right-visual-review-'));try{const zip=await api.archive(p.artifact,{revision:2});assert.equal(zip.length,p.zip_bytes);assert.equal(sha(zip),p.zip_sha256);const archive=join(dir,'original.zip');await writeFile(archive,zip);await mkdir(out,{recursive:true});execFileSync('python3',['-c',extractPython,archive,out],{maxBuffer:1024*1024});assert.equal(sha(await readFile(join(out,'report.json'))),p.report_sha256);
  execFileSync(process.execPath,['site/detail-presentation-browser-test.mjs','--verify-visual-disposition-seals'],{cwd:root,env:{...immutableGitEnv(),DETAIL_BROWSER_PROFILE:'full264-v2',DETAIL_BROWSER_TARGET:'dist',DETAIL_EXPECTED_SOURCE_COMMIT:p.source,QA_OUTPUT_DIR:out,DETAIL_VISUAL_DISPOSITION_PATH:join(root,p.review_path)},stdio:'inherit'});
  assertRun(await api.json(`actions/runs/${p.run}`));const result={status:'ACCEPTED_WITH_INDEPENDENT_AI_VISUAL_REVIEW',original_run_status:'FAIL',original_report_status:'fail',evidence_verification:'AUTHENTICATED_ORIGINAL_COMPLETE_VERIFIER_AND_CURRENT_BYTE_SEALS; NOT_RECOMPUTED_PIXEL_MATH',review_sha256:p.review_sha256,report_sha256:p.report_sha256,artifact_sha256:p.zip_sha256,artifact_id:p.artifact,run_id:p.run,...binding,public_acceptance:'NOT_RUN'};await writeFile(join(out,'acceptance.json'),JSON.stringify(result,null,2)+'\n');return result;
 }finally{await rm(dir,{recursive:true,force:true});}
}
export function assertAcceptedDeployment(run,job,context){
 assert.equal(run.id,context.runId);assert.equal(run.run_attempt,context.runAttempt);assert.equal(run.head_sha,context.head);assert.equal(run.event,'push');assert.equal(run.head_branch,'main');assert.equal(run.path,'.github/workflows/pages.yml');assert.equal(run.workflow_id,VISUAL_REVIEW.workflow);assert.equal(run.status,'completed');assert.equal(run.conclusion,'success');assert.equal(run.repository.full_name,VISUAL_REVIEW.repository);assert.equal(run.head_repository.id,VISUAL_REVIEW.repository_id);
 assert.equal(job.run_id,context.runId);assert.equal(job.run_attempt,context.runAttempt);assert.equal(job.head_sha,context.head);assert.equal(job.name,'build');assert.equal(job.conclusion,'success');
 for(const name of ['Validate source, build once and audit final dist','Authenticated same-runtime evidence and explicit independent visual acceptance','Stamp exact source build after all six mandatory audit phases']){const steps=job.steps.filter(s=>s.name===name);assert.equal(steps.length,1);assert.equal(steps[0].conclusion,'success');}
}
export async function authenticatePublicBinding({root=process.cwd(),api}={}){
 const {loadVerifiedRelease}=await import('./ci-layered-release-scope.mjs');const {context}=loadVerifiedRelease({root});assert.equal(context.repository,VISUAL_REVIEW.repository);
 const appended=!!JSON.parse(await readFile(join(root,'assets/manifest.json'))).publication?.same_id_successor_append;
 const bridge=appended?await import('./detail-append-visual-acceptance.mjs'):null;
 const binding=appended?await bridge.assertAppendVisualRuntime({root,api,currentSha:context.head,legacy:{VISUAL_REVIEW,ACCEPTANCE_CONTROL_HASHES,compareRuntimeTrees}}):await assertReviewedRuntime({root,api,currentSha:context.head});const run=await api.json(`actions/runs/${context.runId}/attempts/${context.runAttempt}`),jobs=await api.json(`actions/runs/${context.runId}/attempts/${context.runAttempt}/jobs?per_page=100`);assert.equal(jobs.total_count,jobs.jobs.length);const candidates=jobs.jobs.filter(j=>j.name==='build');assert.equal(candidates.length,1);const job=await api.json('actions/jobs/'+candidates[0].id);assertAcceptedDeployment(run,job,context);
 if(appended){const fresh=await bridge.verifyExecutedAppendPublic({root,api,currentSha:context.head,out:resolve(process.env.QA_OUTPUT_DIR||'qa/detail-browser-public')});return {status:'AUTHENTICATED_DEPLOYED_APPEND_WITH_FIXED_EXECUTED19_SCIENCE',legacy_appearance:'REUSED_EXACT_264_DIST_VISUAL_REVIEW',new19:fresh,deployed_run_id:context.runId,deployed_run_attempt:context.runAttempt,...binding,public_state:'REQUIRES_FOLLOWING_OLD8_PLUS19_PUBLIC_STATE_RUN'};}
 return {status:'AUTHENTICATED_DEPLOYED_SOURCE_WITH_ACCEPTED_DIST_REVIEW',appearance:'REUSED_DIST_VISUAL_REVIEW',review_sha256:VISUAL_REVIEW.review_sha256,reviewed_report_sha256:VISUAL_REVIEW.report_sha256,deployed_run_id:context.runId,deployed_run_attempt:context.runAttempt,...binding,public_state:'PENDING_ACTUAL_BROWSER'};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){const api=detailAuthorityTransport({repository:VISUAL_REVIEW.repository,token:process.env.GITHUB_TOKEN});const result=process.argv.includes('--public-binding')?await authenticatePublicBinding({api}):await authenticateVisualEvidence({api});console.log(JSON.stringify(result));}

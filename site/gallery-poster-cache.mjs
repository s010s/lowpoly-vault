/** Fetch a separate poster artifact, with independent GitHub provenance and bytes. */
import assert from 'node:assert/strict';
import {mkdtempSync,writeFileSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve,dirname,sep} from 'node:path';
import {mkdir,writeFile,rm} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {appendFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {modelPolicyDigest,modelPolicyDigestAtCommit} from './ci-model-proof.mjs';
import {controlDigest} from './ci-provenance.mjs';
import {posterSharedInputs,posterInputKey} from './gallery-poster-inputs.mjs';
import {assertTrustedMainRun,assertTrustedSuite} from './ci-model-cache.mjs';
import {POSTER_PROOF_FILE,posterArtifactName,posterHash,posterObjectHash,posterRuntime,assertPosterPNG,assertPosterProof} from './gallery-poster-proof.mjs';

// Only independently verified in-process handles are usable; JSON cannot forge one.
const verifiedBundles=new WeakMap();
export function readVerifiedPosterBundle(handle){const bundle=verifiedBundles.get(handle);return bundle?{proof:structuredClone(bundle.proof),files:new Map([...bundle.files].map(([path,bytes])=>[path,Buffer.from(bytes)]))}:null;}
function authenticatePosterBundle(proof,files,verification){const handle=Object.freeze({...verification});verifiedBundles.set(handle,{proof:structuredClone(proof),files:new Map([...files].map(([path,bytes])=>[path,Buffer.from(bytes)]))});return handle;}

const SHA=/^[a-f0-9]{40}$/,WORKFLOW='.github/workflows/full-release-review.yml';
export const MAX_POSTER_ARCHIVE_BYTES=96*1024*1024;
/** Validate the whole allowlisted archive before exposing any extracted bytes. */
export function extractPosterArtifact(bytes){
 assert(Buffer.isBuffer(bytes)&&bytes.length<=MAX_POSTER_ARCHIVE_BYTES,'Oversized poster archive');
 const directory=mkdtempSync(join(tmpdir(),'gallery-proof-'));
 try{
  const archive=join(directory,'artifact.zip');writeFileSync(archive,bytes);
  // Reject links, duplicate names, path traversal, bombs and code before extraction.
  execFileSync('python3',['-I','-c',`import zipfile,sys,stat,re,json,os\nroot=sys.argv[2]\nwith zipfile.ZipFile(sys.argv[1]) as z:\n members=z.infolist(); assert 1<=len(members)<=2001, 'Invalid poster member count'\n names=[m.filename for m in members]; assert len(names)==len(set(names)), 'Duplicate poster member'\n assert 'gallery-poster-proof.json' in names, 'Missing poster proof'\n assert sum(m.file_size for m in members)<=192*1024*1024, 'Oversized expanded poster artifact'\n for m in members:\n  assert not m.is_dir() and not m.flag_bits&1, 'Unsafe poster member'\n  assert stat.S_IFMT(m.external_attr>>16) in (0,stat.S_IFREG), 'Nonregular poster member'\n  assert m.filename=='gallery-poster-proof.json' or re.fullmatch(r'gallery/posters/[a-z0-9-]+(?:-wheel)?\\.png',m.filename), 'Unexpected poster member'\n  assert 0<m.file_size<=8*1024*1024 and m.compress_type in (0,8), 'Invalid poster member size/type'\n proof=json.loads(z.read('gallery-poster-proof.json')); expected=['gallery-poster-proof.json']\n for row in proof['posters']:\n  for f in row['files']: expected.append(f['path'])\n assert sorted(expected)==sorted(names), 'Poster artifact allowlist mismatch'\n for m in members:\n  b=z.read(m); assert len(b)==m.file_size\n  path=os.path.join(root,m.filename); os.makedirs(os.path.dirname(path),exist_ok=True); open(path,'wb').write(b)`,archive,directory],{maxBuffer:1024*1024,stdio:['ignore','pipe','pipe']});
  const proof=JSON.parse(readFileSync(join(directory,POSTER_PROOF_FILE),'utf8')),files=new Map();
  for(const row of proof.posters)for(const kind of ['detail','wheel']){
   const path=row.poster[kind],seal=row.files.find(file=>file.path===path);assert.equal(path,`gallery/posters/${row.id}${kind==='wheel'?'-wheel':''}.png`,'Unsafe poster path');
   const data=readFileSync(join(directory,path));assertPosterPNG(data,seal,kind);files.set(path,data);
  }
  return {proof,files};
 }finally{rmSync(directory,{recursive:true,force:true});}
}
export function assertPosterArtifact(metadata,run,bytes){
 assert.equal(metadata.name,posterArtifactName(run.run_attempt));assert.equal(metadata.expired,false,'Expired gallery artifact');assert(Number.isSafeInteger(metadata.id)&&metadata.id>0);
 assert.equal(metadata.workflow_run?.id,run.id);assert.equal(metadata.workflow_run?.head_sha,run.head_sha);assert.equal(metadata.workflow_run?.repository_id,run.repository.id);assert.equal(metadata.workflow_run?.head_repository_id,run.repository.id,'Fork poster artifact');
 assert.match(metadata.digest||'',/^sha256:[a-f0-9]{64}$/,'Missing independent gallery digest');assert(bytes.length<=MAX_POSTER_ARCHIVE_BYTES);assert.equal(`sha256:${posterHash(bytes)}`,metadata.digest,'Independent gallery artifact digest differs');
}
function client({repository,token=process.env.GITHUB_TOKEN,fetchImpl=fetch}){
 assert(/^[\w.-]+\/[\w.-]+$/.test(repository||''));assert(token,'Read-only GitHub poster token unavailable');
 const signal=AbortSignal.timeout(180000),url=path=>`https://api.github.com/repos/${repository}/${path}`,headers={Authorization:`Bearer ${token}`,Accept:'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'};
 const api=async path=>{const response=await fetchImpl(url(path),{headers,signal});assert(response.ok,`GitHub poster read failed (${response.status})`);return response.json();};
 const artifact=async run=>{
  const listed=await api(`actions/runs/${run.id}/artifacts?per_page=100`),matches=listed.artifacts.filter(item=>item.name===posterArtifactName(run.run_attempt));assert.equal(matches.length,1,'Missing or ambiguous dedicated gallery artifact');
  const metadata=await api(`actions/artifacts/${matches[0].id}`);assert.equal(metadata.id,matches[0].id);
  const redirect=await fetchImpl(url(`actions/artifacts/${metadata.id}/zip`),{headers,signal,redirect:'manual'});assert.equal(redirect.status,302,'Missing gallery download redirect');
  const destination=new URL(redirect.headers.get('location'));assert.equal(destination.protocol,'https:');assert.equal(destination.username,'');assert.equal(destination.password,'');
  const download=await fetchImpl(destination.href,{signal});assert(download.ok,'Gallery artifact download failed');assert(Number(download.headers.get('content-length')||0)<=MAX_POSTER_ARCHIVE_BYTES);
  const chunks=[];let length=0;
  if(download.body?.getReader){const reader=download.body.getReader();try{while(true){const {done,value}=await reader.read();if(done)break;length+=value.length;assert(length<=MAX_POSTER_ARCHIVE_BYTES,'Oversized streamed gallery artifact');chunks.push(Buffer.from(value));}}finally{await reader.cancel();}}
  else {const value=Buffer.from(await download.arrayBuffer());assert(value.length<=MAX_POSTER_ARCHIVE_BYTES);chunks.push(value);}
  const data=Buffer.concat(chunks);assertPosterArtifact(metadata,run,data);return {...extractPosterArtifact(data),metadata};
 };
 return {api,artifact};
}
async function assertAncestor(api,base,head){assert(SHA.test(base)&&SHA.test(head),'Exact poster source commits required');if(base===head)return;const compare=await api(`compare/${base}...${head}`);assert(['ahead','identical'].includes(compare.status)&&compare.merge_base_commit?.sha===base,'Poster baseline ancestry not established');}
async function sourceManifest(api,sha){
 const file=await api(`contents/assets/manifest.json?ref=${sha}`);assert.equal(file.type,'file');const blob=file.encoding==='base64'?file:await api(`git/blobs/${file.sha}`);
 assert.equal(blob.encoding,'base64');if(blob!==file)assert.equal(blob.sha,file.sha);return JSON.parse(Buffer.from(blob.content.replace(/\s/g,''),'base64').toString('utf8'));
}
/** Ordering is local only; every candidate still needs independent API ancestry. */
export function rankPosterCandidates(candidates,{root,baseSha}){
 const distance=sha=>{try{assert(SHA.test(sha||''));execFileSync('git',['merge-base','--is-ancestor',sha,baseSha],{cwd:root,stdio:'ignore'});return Number(execFileSync('git',['rev-list','--count',`${sha}..${baseSha}`],{cwd:root,encoding:'utf8'}));}catch{return Number.MAX_SAFE_INTEGER;}};
 const distances=new Map(candidates.map(run=>[run.head_sha,distance(run.head_sha)]));
 return [...candidates].sort((a,b)=>distances.get(a.head_sha)-distances.get(b.head_sha)||b.id-a.id);
}
export async function fetchVerifiedPosterBaseline({root=process.cwd(),repository=process.env.GITHUB_REPOSITORY,baseSha=process.env.BASE_SHA,currentSha=process.env.GITHUB_SHA,shared,policy_sha256=modelPolicyDigest(root),runtime=posterRuntime(shared),token,fetchImpl}={}){
 const reasons=[];
 try{
  assert(!process.env.CHROMIUM_PATH,'Custom browser executable cannot reuse poster proof');
  assert(SHA.test(baseSha||'')&&!/^0+$/.test(baseSha),'No exact poster comparison base');assert(SHA.test(currentSha||''));
  const {api,artifact}=client({repository,token,fetchImpl}),repo=await api('');assert.equal(repo.full_name,repository);assert.equal(repo.default_branch,'main');
  const main=await api('git/ref/heads/main');assert.equal(main.ref,'refs/heads/main');await assertAncestor(api,baseSha,currentSha);await assertAncestor(api,baseSha,main.object.sha);
  const workflow=await api('actions/workflows/full-release-review.yml');assert.equal(workflow.path,WORKFLOW);assert(Number.isSafeInteger(workflow.id));
  const listed=await api(`actions/workflows/${workflow.id}/runs?branch=main&status=success&per_page=100`),candidates=rankPosterCandidates(listed.workflow_runs.filter(run=>run.head_sha!==currentSha).slice(0,100),{root,baseSha});
  for(const summary of candidates){try{
   await assertAncestor(api,summary.head_sha,baseSha);assert.equal(modelPolicyDigestAtCommit(summary.head_sha,{root}),policy_sha256,'Poster protected control plane changed; full baseline required');
   const run=await api(`actions/runs/${summary.id}`);assertTrustedMainRun(run,{repository,repositoryId:repo.id,sourceSha:summary.head_sha,workflowId:workflow.id});
   const attempt=await api(`actions/runs/${run.id}/attempts/${run.run_attempt}`);assertTrustedMainRun(attempt,{repository,repositoryId:repo.id,sourceSha:run.head_sha,workflowId:workflow.id});assert.equal(attempt.id,run.id);assert.equal(attempt.run_attempt,run.run_attempt);assert.equal(attempt.check_suite_id,run.check_suite_id);assert.equal(attempt.event,run.event);
   await assertTrustedSuite(await api(`check-suites/${run.check_suite_id}`),run);
   const bundle=await artifact(run),manifest=await sourceManifest(api,run.head_sha);
   assertPosterProof(bundle.proof,{repository,sourceSha:run.head_sha,runId:run.id,runAttempt:run.run_attempt,policy_sha256,runtime,manifest});
   const verification={version:1,kind:'independently-verified-gallery-artifact',repository,source_commit:run.head_sha,comparison_base:baseSha,run_id:run.id,run_attempt:run.run_attempt,workflow_id:workflow.id,check_suite_id:run.check_suite_id,artifact_id:bundle.metadata.id,artifact_sha256:bundle.metadata.digest,proof_sha256:posterObjectHash(bundle.proof)};
   return {verified:authenticatePosterBundle(bundle.proof,bundle.files,verification),reasons};
  }catch(error){reasons.push(`Poster candidate ${summary.id} rejected: ${error.message}`);}}
  throw Error('No independently successful compatible main poster baseline');
 }catch(error){return {verified:null,reasons:[...reasons,error.message]};}
}

/** Promote only the separately successful exact-tree PR poster artifact. A model
 * proof cannot stand in for this artifact, even when its build tree is identical. */
export async function promoteVerifiedPRPosterProof({root=process.cwd(),repository=process.env.GITHUB_REPOSITORY,currentSha=process.env.GITHUB_SHA,shared,policy_sha256=modelPolicyDigest(root),runtime=posterRuntime(shared),token,fetchImpl,runId=Number(process.env.GITHUB_RUN_ID),runAttempt=Number(process.env.GITHUB_RUN_ATTEMPT)}={}){
 const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',maxBuffer:128*1024*1024}).trim();
 assert.equal(process.env.GITHUB_EVENT_NAME,'push');assert.equal(process.env.GITHUB_REF,'refs/heads/main');assert.equal(git('rev-parse','HEAD'),currentSha);assert.equal(git('status','--porcelain','--untracked-files=no'),'');
 const mainTree=git('rev-parse','HEAD^{tree}'),control=controlDigest(currentSha),{api,artifact}=client({repository,token,fetchImpl}),repo=await api('');assert.equal(repo.full_name,repository);assert.equal(repo.default_branch,'main');
 const pulls=await api(`commits/${currentSha}/pulls`),pr=pulls.find(row=>row.merged_at&&row.base.ref==='main'&&row.merge_commit_sha===currentSha&&row.head.repo?.full_name===repository&&row.base.repo.full_name===repository);assert(pr,'No exact merged same-repository PR for poster promotion');
 const workflow=await api('actions/workflows/full-release-review.yml');assert.equal(workflow.path,WORKFLOW);
 const listed=await api(`actions/workflows/${workflow.id}/runs?event=pull_request&head_sha=${pr.head.sha}&per_page=100`);let last='No exact-tree PR poster artifact';
 for(const summary of listed.workflow_runs){try{
  const run=await api(`actions/runs/${summary.id}`);assert.equal(run.event,'pull_request');assert.equal(run.status,'completed');assert.equal(run.conclusion,'success');assert.equal(run.path,WORKFLOW);assert.equal(run.workflow_id,workflow.id);assert.equal(run.head_sha,pr.head.sha);
  for(const key of ['repository','head_repository']){assert.equal(run[key]?.full_name,repository);assert.equal(run[key]?.id,repo.id);}
  const attempt=await api(`actions/runs/${run.id}/attempts/${run.run_attempt}`);for(const key of ['id','run_attempt','event','status','conclusion','path','workflow_id','head_sha','check_suite_id'])assert.equal(attempt[key],run[key],'PR poster attempt differs');
  for(const key of ['repository','head_repository']){assert.equal(attempt[key]?.full_name,repository);assert.equal(attempt[key]?.id,repo.id);}
  assertTrustedSuite(await api(`check-suites/${run.check_suite_id}`),run);
  const bundle=await artifact(run),proof=bundle.proof;assert(SHA.test(proof.source_commit||''));
  const source=await api(`git/commits/${proof.source_commit}`);assert.equal(source.tree.sha,mainTree);assert.equal(source.parents.length,2);assert.equal(source.parents[1].sha,pr.head.sha);
  const base=source.parents[0].sha;await assertAncestor(api,base,currentSha);assert.equal(controlDigest(base),control,'PR changed its exact-tree control plane');assert.equal(modelPolicyDigestAtCommit(base,{root}),policy_sha256,'PR changed protected poster policy');
  const manifest=await sourceManifest(api,proof.source_commit);assertPosterProof(proof,{repository,sourceSha:proof.source_commit,runId:run.id,runAttempt:run.run_attempt,policy_sha256,runtime,manifest});
  assert.equal(proof.shared_sha256,shared.sha256,'PR renderer recipe differs');assert.equal(proof.posters.length,proof.catalog_ids.length,'Incomplete PR poster proof cannot establish a main baseline');
  for(const row of proof.posters){const asset=manifest.assets.find(asset=>asset.id===row.id);assert.equal(row.input_sha256,posterInputKey(asset,shared),'PR poster input differs');}
  assert(Number.isSafeInteger(runId)&&runId>0&&Number.isSafeInteger(runAttempt)&&runAttempt>0);
  const promoted={...proof,source_commit:currentSha,run_id:runId,run_attempt:runAttempt,captured_ids:[],reused_ids:proof.catalog_ids,posters:proof.posters.map(row=>({...row,evidence:row.evidence==='reviewed'?'reviewed':'reused'})),
   promoted_from:{source_commit:proof.source_commit,run_id:run.id,run_attempt:run.run_attempt,artifact_id:bundle.metadata.id,artifact_sha256:bundle.metadata.digest,check_suite_id:run.check_suite_id}};
  return {proof:promoted,files:bundle.files};
 }catch(error){last=error.message;}}
 throw Error(`Exact-tree PR poster proof cannot be promoted: ${last}`);
}
export async function writePromotedPosterArtifact({proof,files},{root=process.cwd(),directory=process.env.CI_GALLERY_PROOF_DIR||'qa/ci-gallery-proof'}={}){
 const target=resolve(root,directory);assert(target.startsWith(resolve(root)+sep),'Poster proof output must stay under the checkout');assert(!['site','assets','production','qa'].includes(directory),'Unsafe poster proof output');
 await rm(target,{recursive:true,force:true});await mkdir(target,{recursive:true});
 for(const row of proof.posters)for(const kind of ['detail','wheel']){const path=row.poster[kind],seal=row.files.find(file=>file.path===path),bytes=files.get(path);assertPosterPNG(bytes,seal,kind);const file=resolve(target,path);assert(file.startsWith(target+sep));await mkdir(dirname(file),{recursive:true});await writeFile(file,bytes);}
 await writeFile(resolve(target,POSTER_PROOF_FILE),JSON.stringify(proof,null,2)+'\n');
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 assert.equal(process.argv[2],'promote','Expected poster cache promote');
 const directory=process.env.CI_GALLERY_PROOF_DIR||'qa/ci-gallery-proof';
 try{const shared=await posterSharedInputs(),bundle=await promoteVerifiedPRPosterProof({shared});await writePromotedPosterArtifact(bundle,{directory});if(process.env.GITHUB_OUTPUT)appendFileSync(process.env.GITHUB_OUTPUT,'promoted=true\n');console.log(`Promoted ${bundle.proof.posters.length} independently verified exact-tree PR poster pairs.`);}
 catch(error){if(process.env.GITHUB_OUTPUT)appendFileSync(process.env.GITHUB_OUTPUT,'promoted=false\n');console.log(error.message);}
}

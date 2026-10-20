/** GitHub authenticates cache provenance; JSON in a checkout never authorizes reuse. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,mkdtempSync,rmSync,appendFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {computeModelInputs,modelPolicyDigestAtCommit,assertModelArchivalAppendAtCommit,catalogIDs,hashBytes,hashObject,assertBaseModelProof,planModelReuse,MODEL_PROOF_FILE,MODEL_PROOF_WORKFLOW,GPU_POLICY} from './ci-model-proof.mjs';
import {controlDigest} from './ci-provenance.mjs';

const SHA=/^[a-f0-9]{40}$/,MAX_ARTIFACT_BYTES=16*1024*1024;
export const proofArtifactName=attempt=>`model-proof-v2-${attempt}`;
const git=(root,...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',maxBuffer:128*1024*1024}).trim();
export function assertTrustedMainRun(run,{repository,repositoryId,sourceSha,workflowId}){
  assert(['push','workflow_dispatch'].includes(run.event),'Only main release review runs supply a baseline');
  assert.equal(run.head_branch,'main','Non-main baseline');assert.equal(run.status,'completed');assert.equal(run.conclusion,'success');
  assert.equal(run.path,MODEL_PROOF_WORKFLOW,'Wrong release review workflow');assert.equal(run.workflow_id,workflowId,'Wrong workflow identity');
  assert.equal(run.repository?.full_name,repository);assert.equal(run.head_repository?.full_name,repository,'Fork baseline');
  assert.equal(run.repository?.id,repositoryId);assert.equal(run.head_repository?.id,repositoryId,'Fork repository identity');
  assert.equal(run.head_sha,sourceSha);assert(Number.isSafeInteger(run.id)&&run.id>0);assert(Number.isSafeInteger(run.run_attempt)&&run.run_attempt>0);assert(Number.isSafeInteger(run.check_suite_id)&&run.check_suite_id>0);
}
export function assertTrustedSuite(suite,run){
  assert.equal(suite.id,run.check_suite_id);assert.equal(suite.status,'completed');assert.equal(suite.conclusion,'success');assert.equal(suite.head_sha,run.head_sha);
  assert.equal(suite.app?.slug,'github-actions');assert.equal(suite.app?.id,15368,'Not GitHub-owned Actions checks');assert.equal(suite.app?.owner?.login,'github','Not GitHub-owned checks');
}
export function assertImmutableModelArtifact(artifact,run,bytes){
  assert.equal(artifact.name,proofArtifactName(run.run_attempt));assert.equal(artifact.expired,false,'Expired model proof');
  assert.equal(artifact.workflow_run?.id,run.id);assert.equal(artifact.workflow_run?.head_sha,run.head_sha);
  assert.equal(artifact.workflow_run?.repository_id,run.repository.id);assert.equal(artifact.workflow_run?.head_repository_id,run.repository.id,'Fork artifact');
  assert(Number.isSafeInteger(artifact.id)&&artifact.id>0);assert.match(artifact.digest||'',/^sha256:[a-f0-9]{64}$/,'Missing independent GitHub artifact digest');
  assert(bytes.length<=MAX_ARTIFACT_BYTES,'Oversized proof artifact');assert.equal(`sha256:${hashBytes(bytes)}`,artifact.digest,'Independent artifact digest mismatch');
}
export function extractModelProof(bytes){
  const temp=mkdtempSync(join(tmpdir(),'model-proof-v2-'));
  try{
    const archive=join(temp,'proof.zip');writeFileSync(archive,bytes);
    // The only permitted member is small UTF-8 JSON. Never extract paths, links,
    // executable files, encrypted members, duplicate entries or artifact code.
    const output=execFileSync('python3',['-I','-c',`import zipfile,sys,stat\nwith zipfile.ZipFile(sys.argv[1]) as z:\n members=z.infolist(); assert len(members)==1, 'Expected exactly one proof member'\n m=members[0]; assert m.filename=='model-proof.json', 'Unexpected proof member'\n assert not m.is_dir() and not m.flag_bits&1, 'Unsafe proof member'\n mode=m.external_attr>>16; assert stat.S_IFMT(mode) in (0,stat.S_IFREG), 'Nonregular proof member'\n assert 0<m.file_size<=16000000 and m.compress_type in (0,8), 'Oversized or unsupported proof member'\n b=z.read(m); assert len(b)==m.file_size; sys.stdout.buffer.write(b)`,archive],{maxBuffer:MAX_ARTIFACT_BYTES,stdio:['ignore','pipe','pipe']});
    return JSON.parse(output.toString('utf8'));
  }finally{rmSync(temp,{recursive:true,force:true});}
}
function client({repository,token=process.env.GITHUB_TOKEN,fetchImpl=fetch,signal=AbortSignal.timeout(120000)}){
  assert(/^[\w.-]+\/[\w.-]+$/.test(repository||''),'Missing repository');assert(token,'Read-only GitHub proof token unavailable');
  const url=path=>`https://api.github.com/repos/${repository}/${path}`;
  const headers={Authorization:`Bearer ${token}`,Accept:'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'};
  const api=async path=>{const response=await fetchImpl(url(path),{headers,signal});assert(response.ok,`GitHub proof read failed (${response.status})`);return response.json();};
  const artifact=async(run)=>{
    const listed=await api(`actions/runs/${run.id}/artifacts?per_page=100`);
    const matches=listed.artifacts.filter(item=>item.name===proofArtifactName(run.run_attempt));assert.equal(matches.length,1,'Missing or ambiguous v2 model artifact');
    // Re-read the immutable artifact metadata independently, not just list fields.
    const metadata=await api(`actions/artifacts/${matches[0].id}`);assert.equal(metadata.id,matches[0].id);
    const redirect=await fetchImpl(url(`actions/artifacts/${metadata.id}/zip`),{headers,signal,redirect:'manual'});assert.equal(redirect.status,302,'Artifact redirect unavailable');
    const destination=new URL(redirect.headers.get('location'));assert.equal(destination.protocol,'https:');assert.equal(destination.username,'');assert.equal(destination.password,'');
    const download=await fetchImpl(destination.href,{signal}); // Never forward repository credentials to storage.
    assert(download.ok,'Artifact download failed');const size=Number(download.headers.get('content-length')||0);assert(size<=MAX_ARTIFACT_BYTES,'Oversized artifact');
    const data=Buffer.from(await download.arrayBuffer());assertImmutableModelArtifact(metadata,run,data);
    return {proof:extractModelProof(data),metadata};
  };
  return {api,artifact};
}
async function assertAncestor(api,base,head){
  assert(SHA.test(base)&&SHA.test(head),'Exact source commits required');if(base===head)return;
  const comparison=await api(`compare/${base}...${head}`);
  assert(['ahead','identical'].includes(comparison.status),'Baseline is not an ancestor');assert.equal(comparison.merge_base_commit?.sha,base,'Baseline ancestry is not proven');
}
async function sourceManifest(api,sha){
  const file=await api(`contents/assets/manifest.json?ref=${sha}`);assert.equal(file.type,'file');
  // The real 190-model manifest is already larger than the Contents API's 1 MiB
  // inline-data limit. Its independently returned blob SHA still identifies it.
  const blob=file.encoding==='base64'?file:await api(`git/blobs/${file.sha}`);
  assert.equal(blob.encoding,'base64');if(blob!==file)assert.equal(blob.sha,file.sha);
  return JSON.parse(Buffer.from(blob.content.replace(/\s/g,''),'base64').toString('utf8'));
}
export async function fetchVerifiedBaseProof({root=process.cwd(),repository=process.env.GITHUB_REPOSITORY,baseSha=process.env.BASE_SHA,currentSha=process.env.GITHUB_SHA,inputs=computeModelInputs({root}),token,fetchImpl,allowAncestor=true}={}){
  const reasons=[];
  try{
    assert(SHA.test(baseSha||'')&&!/^0+$/.test(baseSha),'No exact trusted comparison base');assert(SHA.test(currentSha||''),'No current source commit');
    const {api,artifact}=client({repository,token,fetchImpl});
    const repo=await api('');assert.equal(repo.full_name,repository);assert.equal(repo.default_branch,'main');
    const main=await api('git/ref/heads/main');assert.equal(main.ref,'refs/heads/main');
    await assertAncestor(api,baseSha,currentSha);await assertAncestor(api,baseSha,main.object.sha);
    const workflow=await api('actions/workflows/full-release-review.yml');assert.equal(workflow.path,MODEL_PROOF_WORKFLOW);assert(Number.isSafeInteger(workflow.id));
    const listed=await api(`actions/workflows/${workflow.id}/runs?branch=main&status=success&per_page=100`);
    const candidates=listed.workflow_runs.filter(run=>run.head_sha===baseSha||(allowAncestor&&run.head_sha!==currentSha)).slice(0,100);
    // A later rerun of an older commit must not hide the newer 194-model proof.
    // This local graph distance only orders candidates; the API still proves
    // ancestry independently before any candidate can authorize reuse.
    const distance=sha=>{try{assert(SHA.test(sha||''));git(root,'merge-base','--is-ancestor',sha,baseSha);return Number(git(root,'rev-list','--count',`${sha}..${baseSha}`));}catch{return Number.MAX_SAFE_INTEGER;}};
    const distances=new Map(candidates.map(run=>[run.head_sha,distance(run.head_sha)]));
    candidates.sort((a,b)=>distances.get(a.head_sha)-distances.get(b.head_sha)||b.id-a.id);
    for(const summary of candidates){
      try{
        assert(SHA.test(summary.head_sha||''));await assertAncestor(api,summary.head_sha,baseSha);
        // A PR cannot authorize its own changed verifier or acceptance boundary.
        assert.equal(modelPolicyDigestAtCommit(summary.head_sha,{root}),inputs.policy_sha256,'Protected source changed; new full main baseline required');
        assertModelArchivalAppendAtCommit(summary.head_sha,{root});
        const run=await api(`actions/runs/${summary.id}`);assertTrustedMainRun(run,{repository,repositoryId:repo.id,sourceSha:summary.head_sha,workflowId:workflow.id});
        const attempt=await api(`actions/runs/${run.id}/attempts/${run.run_attempt}`);assertTrustedMainRun(attempt,{repository,repositoryId:repo.id,sourceSha:summary.head_sha,workflowId:workflow.id});assert.equal(attempt.id,run.id);assert.equal(attempt.run_attempt,run.run_attempt);
        const suite=await api(`check-suites/${run.check_suite_id}`);assertTrustedSuite(suite,run);
        const {proof,metadata}=await artifact(run),manifest=await sourceManifest(api,run.head_sha);
        assertBaseModelProof(proof,{repository,baseSha:run.head_sha,sourceTree:git(root,'rev-parse',`${run.head_sha}^{tree}`),runId:run.id,runAttempt:run.run_attempt,policy_sha256:inputs.policy_sha256,runtime_config:inputs.runtime_config,catalog_ids:catalogIDs(manifest)});
        return {baseProof:proof,verifiedBaseProof:{schema:2,repository,source_commit:run.head_sha,comparison_base:baseSha,run_id:run.id,run_attempt:run.run_attempt,check_suite_id:run.check_suite_id,workflow_id:workflow.id,artifact_id:metadata.id,artifact_sha256:metadata.digest,proof_sha256:hashObject(proof)},reasons};
      }catch(error){reasons.push(`Candidate ${summary.id} rejected: ${error.message}`);}
    }
    throw Error('No successful compatible main-ancestor v2 model proof');
  }catch(error){return {baseProof:null,verifiedBaseProof:null,reasons:[...reasons,error.message]};}
}
/** Import only the independently successful exact-tree PR proof already eligible
 * for ci-reuse; this never weakens or changes that separate exact-tree contract. */
export async function promoteVerifiedPRProof({root=process.cwd(),repository=process.env.GITHUB_REPOSITORY,currentSha=process.env.GITHUB_SHA,inputs=computeModelInputs({root}),token,fetchImpl,runId=Number(process.env.GITHUB_RUN_ID),runAttempt=Number(process.env.GITHUB_RUN_ATTEMPT)}={}){
  assert.equal(process.env.GITHUB_EVENT_NAME,'push');assert.equal(process.env.GITHUB_REF,'refs/heads/main');
  assert.equal(git(root,'rev-parse','HEAD'),currentSha);assert.equal(git(root,'status','--porcelain','--untracked-files=no'),'');
  const mainTree=git(root,'rev-parse','HEAD^{tree}'),control=controlDigest(currentSha),{api,artifact}=client({repository,token,fetchImpl});
  const repo=await api(''),pulls=await api(`commits/${currentSha}/pulls`);
  const pr=pulls.find(row=>row.merged_at&&row.base.ref==='main'&&row.merge_commit_sha===currentSha&&row.head.repo?.full_name===repository&&row.base.repo.full_name===repository);assert(pr,'No exact merged same-repository PR');
  const workflow=await api('actions/workflows/full-release-review.yml');assert.equal(workflow.path,MODEL_PROOF_WORKFLOW);
  const listed=await api(`actions/workflows/${workflow.id}/runs?event=pull_request&head_sha=${pr.head.sha}&per_page=100`);
  let last='No PR v2 proof';
  for(const summary of listed.workflow_runs){try{
    const run=await api(`actions/runs/${summary.id}`);
    assert.equal(run.event,'pull_request');assert.equal(run.status,'completed');assert.equal(run.conclusion,'success');assert.equal(run.path,MODEL_PROOF_WORKFLOW);assert.equal(run.workflow_id,workflow.id);assert.equal(run.head_sha,pr.head.sha);
    for(const key of ['repository','head_repository']){assert.equal(run[key]?.full_name,repository);assert.equal(run[key]?.id,repo.id);}
    const attempt=await api(`actions/runs/${run.id}/attempts/${run.run_attempt}`);assert.equal(attempt.id,run.id);assert.equal(attempt.run_attempt,run.run_attempt);assert.equal(attempt.conclusion,'success');assert.equal(attempt.head_sha,run.head_sha);
    assertTrustedSuite(await api(`check-suites/${run.check_suite_id}`),run);
    const {proof,metadata}=await artifact(run);assert(SHA.test(proof.source_commit||''));
    const source=await api(`git/commits/${proof.source_commit}`);assert.equal(source.tree.sha,mainTree);assert.equal(source.parents.length,2);assert.equal(source.parents[1].sha,pr.head.sha);
    const base=source.parents[0].sha;await assertAncestor(api,base,currentSha);assert.equal(controlDigest(base),control,'PR changed the exact-tree control plane');
    assert.equal(modelPolicyDigestAtCommit(base,{root}),inputs.policy_sha256);assert.equal(proof.policy_sha256,inputs.policy_sha256);
    assertBaseModelProof(proof,{repository,baseSha:proof.source_commit,sourceTree:mainTree,runId:run.id,runAttempt:run.run_attempt,policy_sha256:inputs.policy_sha256,runtime_config:inputs.runtime_config,catalog_ids:inputs.models.map(row=>row.id).sort()});
    assert.equal(proof.models.length,inputs.models.length,'Incomplete PR proof cannot establish a complete main baseline');
    for(const input of inputs.models){const prior=proof.models.find(row=>row.id===input.id);for(const key of ['input_key','input_sha256','glb_sha256'])assert.equal(prior[key],input[key],`PR ${key} differs`);}
    assert(Number.isSafeInteger(runId)&&runId>0&&Number.isSafeInteger(runAttempt)&&runAttempt>0);
    return {...proof,source_commit:currentSha,source_tree:mainTree,run_id:runId,run_attempt:runAttempt,fresh_ids:[],reused_ids:proof.catalog_ids,
      models:proof.models.map(row=>({...row,evidence:'reused',reused_from:{source_commit:proof.source_commit,run_id:run.id,run_attempt:run.run_attempt,artifact_id:metadata.id}})),
      promoted_from:{source_commit:proof.source_commit,run_id:run.id,run_attempt:run.run_attempt,artifact_id:metadata.id,artifact_sha256:metadata.digest,check_suite_id:run.check_suite_id}};
  }catch(error){last=error.message;}}
  throw Error(`Exact-tree PR model proof cannot be promoted: ${last}`);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  const directory=process.env.CI_MODEL_PROOF_DIR||'qa/ci-model-proof';mkdirSync(directory,{recursive:true});
  const inputs=computeModelInputs();
  if(process.argv[2]==='promote'){
    rmSync(join(directory,MODEL_PROOF_FILE),{force:true});
    try{const proof=await promoteVerifiedPRProof({inputs});writeFileSync(join(directory,MODEL_PROOF_FILE),JSON.stringify(proof,null,2)+'\n');if(process.env.GITHUB_OUTPUT)appendFileSync(process.env.GITHUB_OUTPUT,'promoted=true\n');console.log(`Imported ${proof.models.length} independently verified exact-tree PR model results.`);}
    catch(error){if(process.env.GITHUB_OUTPUT)appendFileSync(process.env.GITHUB_OUTPUT,'promoted=false\n');console.log(error.message);}
  }else if(process.argv[2]==='plan'||!process.argv[2]){
    rmSync(join(directory,'base-proof.json'),{force:true});
    const force=process.env.CI_MODEL_FORCE_FULL==='true'||process.env.GITHUB_EVENT_NAME==='workflow_dispatch';
    const found=force?{baseProof:null,verifiedBaseProof:null,reasons:['Explicit full-model verification or uncertain dependency ownership']}:await fetchVerifiedBaseProof({inputs}),plan=planModelReuse({inputs,...found});
    writeFileSync(join(directory,'inputs.json'),JSON.stringify(inputs,null,2)+'\n');writeFileSync(join(directory,'plan.json'),JSON.stringify(plan,null,2)+'\n');
    if(found.baseProof)writeFileSync(join(directory,'base-proof.json'),JSON.stringify(found.baseProof,null,2)+'\n');
    if(process.env.GITHUB_OUTPUT)for(const [key,value]of Object.entries({fresh_ids:plan.fresh_ids.join(','),reused_ids:plan.reused_ids.join(','),fresh_count:plan.fresh_ids.length,reused_count:plan.reused_ids.length}))appendFileSync(process.env.GITHUB_OUTPUT,`${key}=${value}\n`);
    console.log(JSON.stringify(plan,null,2));
  }else throw Error('Expected plan or promote');
}

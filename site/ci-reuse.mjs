/** Main-only, fail-closed reuse. No artifact code is executed; all API proof is independent of its receipt. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,appendFileSync,rmSync,mkdtempSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {sha256,git,controlDigest,runtimeConfig,assertReceipt} from './ci-provenance.mjs';

export function assertTrustedRun(run,{repository,head,workflow}){
  assert.equal(run.event,'pull_request','Fork/push runs cannot supply a PR receipt');
  assert.equal(run.status,'completed');assert.equal(run.conclusion,'success');
  assert.equal(run.path,`.github/workflows/${workflow}`,'Wrong workflow');
  assert.equal(run.repository.full_name,repository);assert.equal(run.head_repository.full_name,repository,'Fork artifact rejected');
  assert.equal(run.head_sha,head);
  assert(Number.isSafeInteger(run.check_suite_id),'Missing check suite');
}
export function assertArtifact(artifact,run,bytes){
  assert.equal(artifact.expired,false,'Expired artifact');
  assert.equal(artifact.workflow_run.id,run.id);assert.equal(artifact.workflow_run.head_sha,run.head_sha);
  assert.equal(artifact.workflow_run.repository_id,artifact.workflow_run.head_repository_id,'Fork artifact rejected');
  assert.match(artifact.digest || '',/^sha256:[a-f0-9]{64}$/,'Missing GitHub artifact digest');
  assert.equal(`sha256:${sha256(bytes)}`,artifact.digest,'GitHub artifact digest mismatch');
}
export async function reuse(){
  if(process.env.GITHUB_EVENT_NAME!=='push'||process.env.GITHUB_REF!=='refs/heads/main')return {reused:false,reason:'Only main push may reuse validated PR outputs'};
  const repository=process.env.GITHUB_REPOSITORY,token=process.env.GITHUB_TOKEN;
  assert(token&&/^[\w.-]+\/[\w.-]+$/.test(repository || ''),'GitHub proof access unavailable');
  const api=async path=>{
    const response=await fetch(`https://api.github.com/repos/${repository}/${path}`,{headers:{Authorization:`Bearer ${token}`,Accept:'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}});
    assert(response.ok,`GitHub proof request failed (${response.status})`);return response.json();
  };
  const main=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}'),control=controlDigest(main);
  const pulls=await api(`commits/${main}/pulls`);
  const pr=pulls.find(row=>row.merged_at&&row.base.ref==='main'&&row.merge_commit_sha===main&&row.head.repo?.full_name===repository&&row.base.repo.full_name===repository);
  assert(pr,'No merged same-repository PR for this exact main commit');
  const proofs=[],temp=mkdtempSync(join(tmpdir(),'release-proof-'));
  try{
    for(const [kind,workflow] of [['pages','pages.yml'],['review','full-release-review.yml']]){
      const runs=await api(`actions/workflows/${workflow}/runs?event=pull_request&head_sha=${pr.head.sha}&per_page=100`);
      const candidates=runs.workflow_runs.filter(run=>run.status==='completed'&&run.conclusion==='success');
      assert(candidates.length,'Required successful PR workflow missing');
      let proof;
      for(const summary of candidates){
        try{
          const run=await api(`actions/runs/${summary.id}`);
          assertTrustedRun(run,{repository,head:pr.head.sha,workflow});
          const suite=await api(`check-suites/${run.check_suite_id}`);
          assert.equal(suite.app?.slug,'github-actions');assert.equal(suite.conclusion,'success');assert.equal(suite.head_sha,run.head_sha);
          const artifacts=await api(`actions/runs/${run.id}/artifacts?per_page=100`);
          const matches=artifacts.artifacts.filter(item=>item.name===`validated-${kind}-${run.run_attempt}`);
          assert.equal(matches.length,1,'Missing or ambiguous validation receipt');const artifact=matches[0];
          const redirect=await fetch(`https://api.github.com/repos/${repository}/actions/artifacts/${artifact.id}/zip`,{redirect:'manual',headers:{Authorization:`Bearer ${token}`}});
          assert.equal(redirect.status,302);const location=new URL(redirect.headers.get('location'));assert.equal(location.protocol,'https:');
          // Never forward the repository token to artifact storage.
          const download=await fetch(location);assert(download.ok,'Artifact download failed');
          const bytes=Buffer.from(await download.arrayBuffer());assertArtifact(artifact,run,bytes);
          const archive=join(temp,`${kind}.zip`),target=join(temp,kind);writeFileSync(archive,bytes);mkdirSync(target);
          execFileSync('python3',['-c',`import zipfile,sys,pathlib\nwith zipfile.ZipFile(sys.argv[1]) as z:\n names=z.namelist(); expected=['receipt.json','dist.tar'] if sys.argv[3]=='pages' else ['receipt.json']\n assert sorted(names)==sorted(expected), 'Unexpected artifact members'\n for name in names:\n  info=z.getinfo(name); assert info.file_size < 2000000000 and not ((info.external_attr >> 16) & 0o170000)==0o120000\n  pathlib.Path(sys.argv[2],name).write_bytes(z.read(name))`,archive,target,kind]);
          const receipt=JSON.parse(readFileSync(join(target,'receipt.json')));
          assert.match(receipt.source_commit || '',/^[0-9a-f]{40}$/,'Missing tested source commit');
          const commit=await api(`git/commits/${receipt.source_commit}`);
          assert.equal(commit.tree.sha,tree,'Merge tree differs from validated tree');
          assert.equal(commit.parents.length,2,'PR merge commit must have base/head parents');
          const base=commit.parents[0].sha;
          assert.equal(commit.parents[1].sha,run.head_sha,'Receipt is not the tested PR head');
          execFileSync('git',['merge-base','--is-ancestor',base,main]);
          // PR run relations disappear on merge and their SHAs mutate while open.
          // Git commit parents and the base control files are independent, immutable proof.
          assert.equal(controlDigest(base),control,'PR changed the independently verified base control plane');
          assertReceipt(receipt,{kind,source_tree:tree,repository,run_id:run.id,run_attempt:run.run_attempt,comparison_base:base,head_sha:run.head_sha,pull_request:pr.number,validation_ref:`refs/pull/${pr.number}/merge`,control_sha256:control,runtime_config:runtimeConfig()});
          if(kind==='pages')assert.equal(sha256(readFileSync(join(target,'dist.tar'))),receipt.payload_sha256,'Payload tampered');
          proof={kind,run_id:run.id,check_suite_id:run.check_suite_id,result:suite.conclusion,artifact_id:artifact.id,artifact_sha256:artifact.digest,receipt};break;
        }catch(error){console.log(`Receipt candidate ${summary.id} rejected: ${error.message}`);rmSync(join(temp,kind),{recursive:true,force:true});}
      }
      assert(proof,`No trusted exact-tree ${kind} receipt`);proofs.push(proof);
    }
    assert.equal(proofs[0].receipt.source_commit,proofs[1].receipt.source_commit,'Workflows tested different merge commits');
    // Validate every archive member before extraction. No links, devices, absolute paths or traversal.
    rmSync('dist',{recursive:true,force:true});mkdirSync('dist');
    execFileSync('python3',['-c',`import tarfile,pathlib,sys\nwith tarfile.open(sys.argv[1]) as t:\n for m in t.getmembers():\n  p=pathlib.PurePosixPath(m.name); assert not p.is_absolute() and '..' not in p.parts and (m.isfile() or m.isdir()), 'Unsafe payload member'\n t.extractall('dist',filter='data')`,join(temp,'pages','dist.tar')]);
    const result={reused:true,source_commit:main,source_tree:tree,runtime_config:runtimeConfig(),proofs};
    mkdirSync('qa/ci-provenance',{recursive:true});writeFileSync('qa/ci-provenance/reuse.json',JSON.stringify(result,null,2)+'\n');return result;
  }finally{rmSync(temp,{recursive:true,force:true});}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  let result;try{result=await reuse();}catch(error){rmSync('dist',{recursive:true,force:true});result={reused:false,reason:error.message};}
  if(process.env.GITHUB_OUTPUT)appendFileSync(process.env.GITHUB_OUTPUT,`reused=${result.reused}\n`);
  const summary=result.reused?`Reusing exact validated tree ${result.source_tree}; deploy and live smoke remain mandatory.`:`Full verification required: ${result.reason}`;
  console.log(summary);if(process.env.GITHUB_STEP_SUMMARY)appendFileSync(process.env.GITHUB_STEP_SUMMARY,summary+'\n');
}

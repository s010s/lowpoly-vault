/** Fresh GitHub main authentication; no checkout JSON or prior task can mint trust. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,mkdtempSync,rmSync,cpSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {tmpdir} from 'node:os';
import {createHash} from 'node:crypto';
import {fetchVerifiedProductionBase,authenticatedProductionBase} from './ci-production-baseline.mjs';
import {releaseAppendFromGit} from './ci-release-fast-scope.mjs';
import {runtimeConfig} from './ci-provenance.mjs';
import {immutableGitEnv} from './ci-git.mjs';
import {proofGet} from './ci-proof-fetch.mjs';
export const fastArtifactName=(sha,run,attempt)=>`release-fast-base-${sha}-${run}-${attempt}`;
const authenticatedScopes=new WeakSet();
const sha=b=>createHash('sha256').update(b).digest('hex');
const controlDigest=(ref,root=process.cwd())=>{const entries=execFileSync('git',['ls-tree','-r',ref],{cwd:root,env:immutableGitEnv(),encoding:'utf8',maxBuffer:128*1024*1024}).trim().split('\n').filter(line=>{const path=line.split('\t')[1];return /^(?:\.github\/|scripts\/|schemas\/|package(?:-lock)?\.json$|vite\.config\.js$)/.test(path)||/^site\/.*\.mjs$/.test(path)||/^qa\/.*\.(?:mjs|js|py)$/.test(path)||path==='site/gallery/approved-poster-inputs.json';});assert(entries.length);return sha(entries.join('\n'));};
export async function verifiedFastScope({root=process.cwd(),baseSha=process.env.BASE_SHA,currentSha=process.env.GITHUB_SHA,repository=process.env.GITHUB_REPOSITORY,fetchImpl=fetch}={}){
 if(process.env.FULL_REVIEW==='true')return {eligible:false,reasons:['Explicit full validation requested']};
 if((process.env.GITHUB_EVENT_NAME==='push'&&process.env.GITHUB_REF!=='refs/heads/main')||!['push','pull_request'].includes(process.env.GITHUB_EVENT_NAME))return {eligible:false,reasons:['Manual/unknown events require full validation']};
 const scope=releaseAppendFromGit(baseSha,{root,currentSha});if(!scope.eligible)return scope;
 const found=await fetchVerifiedProductionBase({root,baseSha,currentSha,repository,fetchImpl});
 if(!found.capability)return {eligible:false,reasons:found.reasons};
 const baseline=authenticatedProductionBase(found.capability,{root,baseSha,currentSha,repository});
 const result={...scope,baseline};authenticatedScopes.add(result);return result;
}
export function assertFastArtifact(metadata,baseline,bytes){
 assert.equal(metadata.name,fastArtifactName(baseline.source_commit,baseline.run_id,baseline.run_attempt));assert.equal(metadata.expired,false);
 assert.equal(metadata.workflow_run?.id,baseline.run_id);assert.equal(metadata.workflow_run?.head_sha,baseline.source_commit);
 assert.equal(metadata.workflow_run?.repository_id,baseline.repository_id);assert.equal(metadata.workflow_run?.head_repository_id,baseline.repository_id);
 assert(Number.isSafeInteger(metadata.id)&&metadata.id>0);assert(bytes.length>0&&bytes.length<2*1024**3,'Artifact size out of bounds');
 assert.equal(metadata.digest,`sha256:${sha(bytes)}`,'Independent GitHub artifact digest mismatch');
}
/** Pure extraction integrity only; never baseline authority. */
export function extractFastArchive(bytes,temp){
  writeFileSync(join(temp,'bundle.zip'),bytes);
  // Validate every path, type and size before writing. Never extract arbitrary artifact code.
  execFileSync('python3',['-I','-c',`import zipfile,tarfile,sys,pathlib,stat,json,hashlib\nr=pathlib.Path(sys.argv[1]);z=zipfile.ZipFile(r/'bundle.zip');ms=z.infolist();assert len(ms)==1 and ms[0].filename=='base.tar.gz';assert ms[0].file_size<2*1024**3;assert not ms[0].flag_bits&1;assert stat.S_IFMT(ms[0].external_attr>>16) in (0,stat.S_IFREG);(r/'base.tar.gz').write_bytes(z.read(ms[0]))\nwith tarfile.open(r/'base.tar.gz','r:gz') as t:\n ms=t.getmembers();seen=set();total=0\n for m in ms:\n  p=pathlib.PurePosixPath(m.name);assert not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and '\\\\' not in m.name;assert m.name==p.as_posix() and all(x not in ('','.','..') for x in m.name.split('/'));canonical=p.as_posix();assert canonical not in seen;seen.add(canonical);assert m.isfile();assert m.name in ('receipt.json','template.html') or m.name.startswith('dist/');total+=m.size;assert total<4*1024**3 and len(ms)<30000\n for m in ms:\n  p=r/'extracted'/m.name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(t.extractfile(m).read())\n`,temp],{timeout:120000,stdio:'pipe'});
 return join(temp,'extracted');
}
export async function restoreFastBase(scope,{root=process.cwd(),fetchImpl=fetch}={}){
 assert(scope?.eligible&&scope.baseline&&authenticatedScopes.has(scope),'Expected process-local authenticated scope, never JSON');const b=scope.baseline;
 const headers={Authorization:`Bearer ${process.env.GITHUB_TOKEN}`,Accept:'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'},signal=AbortSignal.timeout(120000);
 const api=async path=>{const r=await proofGet(`https://api.github.com/repos/${b.repository}/${path}`,{headers,signal,redirect:'error'},{fetchImpl});assert(r.ok,`Fast artifact API ${r.status}`);return r.json();};
 const listed=await api(`actions/runs/${b.run_id}/artifacts?per_page=100`);assert(listed.total_count===listed.artifacts.length&&listed.total_count<=100);
 const matches=listed.artifacts.filter(a=>a.name===fastArtifactName(b.source_commit,b.run_id,b.run_attempt));assert.equal(matches.length,1,'No unique compatible build artifact; full fallback');
 const metadata=await api(`actions/artifacts/${matches[0].id}`);assert.equal(metadata.id,matches[0].id);
 const redirect=await proofGet(`https://api.github.com/repos/${b.repository}/actions/artifacts/${metadata.id}/zip`,{headers,signal,redirect:'manual'},{fetchImpl});assert.equal(redirect.status,302);
 const url=new URL(redirect.headers.get('location'));assert.equal(url.protocol,'https:');assert(!url.username&&!url.password);
 const response=await proofGet(url.href,{signal,redirect:'error'},{fetchImpl});assert(response.ok);assert(Number(response.headers.get('content-length')||0)<2*1024**3);
 const bytes=Buffer.from(await response.arrayBuffer());assertFastArtifact(metadata,b,bytes);
 const latest=await api(`actions/runs/${b.run_id}`);assert.equal(latest.run_attempt,b.run_attempt);assert.equal(latest.head_sha,b.source_commit);assert.equal(latest.status,'completed');assert.equal(latest.conclusion,'success');
 const temp=mkdtempSync(join(tmpdir(),'release-fast-'));
 try{
  extractFastArchive(bytes,temp);
  const dir=join(temp,'extracted'),receipt=JSON.parse(readFileSync(join(dir,'receipt.json')));
  assert.equal(receipt.version,1);assert.equal(receipt.source_commit,b.source_commit);assert.equal(receipt.source_tree,b.source_tree);assert.equal(receipt.run_id,b.run_id);assert.equal(receipt.run_attempt,b.run_attempt);
  assert.deepEqual(receipt.runtime,runtimeConfig(),'Build runtime differs');assert.equal(receipt.control,controlDigest(process.env.GITHUB_SHA,root),'Protected control plane differs');
  assert.equal(receipt.template_sha256,sha(readFileSync(join(dir,'template.html'))));
  const {inventory}=await import('./ci-deployment-contract.mjs');assert.deepEqual(inventory(join(dir,'dist')),receipt.files,'Restored byte inventory mismatch');
  rmSync(resolve(root,'dist'),{recursive:true,force:true});cpSync(join(dir,'dist'),resolve(root,'dist'),{recursive:true});
  for(const marker of ['release-build.json','ci-review-build.json'])rmSync(resolve(root,'dist',marker),{force:true});
  mkdirSync(resolve(root,'qa/ci-model-proof'),{recursive:true});cpSync(join(dir,'template.html'),resolve(root,'qa/ci-model-proof/vite-template.html'));
  return {...scope,artifact_id:metadata.id,artifact_digest:metadata.digest};
 }finally{rmSync(temp,{recursive:true,force:true});}
}
export async function writeFastBase({root=process.cwd()}={}){
 const {inventory}=await import('./ci-deployment-contract.mjs');const target=resolve(root,'qa/release-fast-base');mkdirSync(target,{recursive:true});
 const receipt={version:1,source_commit:process.env.GITHUB_SHA,source_tree:execFileSync('git',['rev-parse','HEAD^{tree}'],{cwd:root,env:immutableGitEnv(),encoding:'utf8'}).trim(),run_id:Number(process.env.GITHUB_RUN_ID),run_attempt:Number(process.env.GITHUB_RUN_ATTEMPT),runtime:runtimeConfig(),control:controlDigest(process.env.GITHUB_SHA,root),template_sha256:sha(readFileSync(resolve(root,'qa/ci-model-proof/vite-template.html'))),files:inventory(resolve(root,'dist'))};
 writeFileSync(join(target,'receipt.json'),JSON.stringify(receipt));
 execFileSync('python3',['-I','-c',`import tarfile,pathlib,sys\nr=pathlib.Path(sys.argv[1]);o=r/'qa/release-fast-base/base.tar.gz'\nwith tarfile.open(o,'w:gz',compresslevel=1) as t:\n t.add(r/'qa/release-fast-base/receipt.json',arcname='receipt.json');t.add(r/'qa/ci-model-proof/vite-template.html',arcname='template.html')\n for p in sorted((r/'dist').rglob('*')):\n  if p.is_file():t.add(p,arcname=p.relative_to(r).as_posix(),recursive=False)\n`,root],{timeout:120000,stdio:'pipe'});
}

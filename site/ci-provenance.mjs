/** Small, dependency-free source and artifact receipts; never a substitute for GitHub check results. */
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
export const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
export const git = (...args) => execFileSync('git', args, { encoding:'utf8' }).trim();
export const runtimeConfig = () => ({site_base:process.env.SITE_BASE || '/',site_origin:process.env.SITE_ORIGIN || '',node_major:process.versions.node.split('.')[0],platform:process.platform,arch:process.arch});
export function controlDigest(ref) {
  // A PR may not authorize its own weakened classifier, tests, receipt producer or workflow.
  const entries=git('ls-tree','-r',ref).split('\n').filter(line=>{
    const path=line.split('\t')[1];
    return /^(?:\.github\/|scripts\/|schemas\/|package(?:-lock)?\.json$|vite\.config\.js$)/.test(path)||/^site\/.*\.mjs$/.test(path)||path==='site/gallery/approved-poster-inputs.json';
  });
  assert(entries.length>0,'Missing trusted control plane');
  return sha256(entries.join('\n'));
}
export function sourceReceipt(kind) {
  const source=git('rev-parse','HEAD'), tree=git('rev-parse','HEAD^{tree}');
  assert.equal(git('status','--porcelain','--untracked-files=no'),'','Receipts require unchanged tracked source');
  const base=process.env.BASE_SHA;
  assert(/^[0-9a-f]{40}$/.test(base || ''),'A verified comparison base is required');
  return {version:1,kind,source_commit:source,source_tree:tree,comparison_base:base,repository:process.env.GITHUB_REPOSITORY,
    run_id:Number(process.env.GITHUB_RUN_ID),run_attempt:Number(process.env.GITHUB_RUN_ATTEMPT),
    event:process.env.GITHUB_EVENT_NAME,head_sha:process.env.CI_HEAD_SHA || source,
    control_sha256:controlDigest(source),base_control_sha256:controlDigest(base),runtime_config:runtimeConfig(),
    validation:'awaiting-independent-github-conclusion'};
}
export function assertReceipt(receipt, expected) {
  assert(receipt&&receipt.version===1,'Missing or unsupported receipt');
  for(const key of ['kind','source_tree','repository','run_id','run_attempt','comparison_base','head_sha'])assert.equal(receipt[key],expected[key],`Receipt ${key} mismatch`);
  assert.match(receipt.source_commit || '',/^[0-9a-f]{40}$/);
  assert.equal(receipt.control_sha256,expected.control_sha256,'Untrusted control plane');
  assert.equal(receipt.base_control_sha256,expected.control_sha256,'PR modified its own validation policy');
  assert.deepEqual(receipt.runtime_config,expected.runtime_config,'Runtime configuration mismatch');
  assert.equal(receipt.event,'pull_request','Only same-repository PR validation is reusable');
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  const kind=process.argv[2];assert(['pages','review'].includes(kind));
  const receipt=sourceReceipt(kind),directory=`qa/ci-provenance/${kind}`;mkdirSync(directory,{recursive:true});
  if(kind==='pages'){
    execFileSync('tar',['--sort=name','--mtime=@0','--owner=0','--group=0','--numeric-owner','-cf',`${directory}/dist.tar`,'-C','dist','.']);
    receipt.payload_sha256=sha256(readFileSync(`${directory}/dist.tar`));
  }
  writeFileSync(`${directory}/receipt.json`,JSON.stringify(receipt,null,2)+'\n');
  console.log(`Recorded ${kind} source tree ${receipt.source_tree}; independent GitHub success is still required.`);
}

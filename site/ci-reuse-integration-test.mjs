/** Exercise the real lookup/extraction path against independent fake GitHub API evidence. No network. */
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {reuse} from './ci-reuse.mjs';
import {git,sha256,controlDigest,runtimeConfig} from './ci-provenance.mjs';
const originalCwd=process.cwd(),originalFetch=global.fetch,environment={...process.env};
const repository='owner/repository';
async function scenario({policy=false,tampered=false,wrongTree=false,failed=false,missing=false,unsafe=false}={}){
 const root=mkdtempSync(join(tmpdir(),'reuse-integration-'));
 try{
  process.chdir(root);git('init','-q');git('config','user.name','CI fixture');git('config','user.email','ci@example.invalid');
  mkdirSync('.github/workflows',{recursive:true});mkdirSync('site');
  writeFileSync('.github/workflows/pages.yml','trusted pages');writeFileSync('.github/workflows/full-release-review.yml','trusted review');writeFileSync('site/ci-policy.mjs','trusted');writeFileSync('asset','v1');
  git('add','.');git('commit','-qm','base');const base=git('rev-parse','HEAD');
  writeFileSync('asset','v2');if(policy)writeFileSync('.github/workflows/pages.yml','weakened pages');git('add','.');git('commit','-qm','head');const head=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}');
  const source=git('commit-tree',tree,'-p',base,'-p',head,'-m','GitHub PR test merge'),main=git('commit-tree',tree,'-p',base,'-p',head,'-m','Main merge');git('checkout','--detach',main);
  Object.assign(process.env,{GITHUB_EVENT_NAME:'push',GITHUB_REF:'refs/heads/main',GITHUB_REPOSITORY:repository,GITHUB_TOKEN:'fixture-token'});
  const control=controlDigest(main),archives={},runs={},artifacts={};
  mkdirSync('payload');writeFileSync('payload/index.html','tested output');
  execFileSync('tar',['-cf','payload.tar','-C','payload','.']);
  if(unsafe)execFileSync('python3',['-c',"import tarfile,io\nwith tarfile.open('payload.tar','w') as t:\n m=tarfile.TarInfo('../escape');m.size=1;t.addfile(m,io.BytesIO(b'x'))"]);
  for(const [index,kind]of ['pages','review'].entries()){
   const id=12+index,workflow=kind==='pages'?'pages.yml':'full-release-review.yml';
   runs[id]={id,run_attempt:1,event:'pull_request',status:'completed',conclusion:'success',path:`.github/workflows/${workflow}`,repository:{full_name:repository},head_repository:{full_name:repository},head_sha:head,check_suite_id:42+index,pull_requests:[]};
   const receipt={version:1,kind,source_commit:source,source_tree:wrongTree?'0'.repeat(40):tree,comparison_base:base,head_sha:head,repository,run_id:id,run_attempt:1,event:'pull_request',pull_request:5,validation_ref:'refs/pull/5/merge',control_sha256:control,base_control_sha256:control,runtime_config:runtimeConfig()};
   if(kind==='pages')receipt.payload_sha256=sha256(readFileSync('payload.tar'));
   writeFileSync(`${kind}.json`,JSON.stringify(receipt));
   execFileSync('python3',['-c',"import zipfile,sys\nwith zipfile.ZipFile(sys.argv[1]+'.zip','w') as z:\n z.write(sys.argv[1]+'.json','receipt.json')\n if sys.argv[1]=='pages':z.write('payload.tar','dist.tar')",kind]);
   const bytes=readFileSync(`${kind}.zip`);archives[kind]=tampered&&kind==='pages'?Buffer.from('tampered'):bytes;
   artifacts[id]={id:100+index,name:`validated-${kind}-1`,expired:false,digest:`sha256:${sha256(bytes)}`,workflow_run:{id,head_sha:head,repository_id:7,head_repository_id:7}};
  }
  const json=data=>new Response(JSON.stringify(data),{status:200,headers:{'Content-Type':'application/json'}});
  global.fetch=async(url,options={})=>{
   url=String(url);
   if(url.startsWith('https://artifacts.test/')){assert(!options.headers?.Authorization,'Repository token must not reach artifact storage');return new Response(archives[url.split('/').at(-1)]);}
   assert.equal(options.headers.Authorization,'Bearer fixture-token');const path=url.split(`/repos/${repository}/`)[1];
   if(path===`commits/${main}/pulls`)return json([{number:5,merged_at:'2026-01-01',merge_commit_sha:main,base:{ref:'main',repo:{full_name:repository}},head:{sha:head,repo:{full_name:repository}}}]);
   if(path.startsWith('actions/workflows/'))return json({workflow_runs:[runs[path.includes('/pages.yml/')?12:13]]});
   let match;if((match=path.match(/^actions\/runs\/(\d+)$/)))return json(runs[match[1]]);
   if((match=path.match(/^check-suites\/(\d+)$/)))return json({app:{slug:'github-actions'},conclusion:failed?'failure':'success',head_sha:head});
   if((match=path.match(/^actions\/runs\/(\d+)\/artifacts/)))return json({artifacts:missing?[]:[artifacts[match[1]]]});
   if((match=path.match(/^actions\/artifacts\/(\d+)\/zip$/)))return new Response(null,{status:302,headers:{location:`https://artifacts.test/${Number(match[1])===100?'pages':'review'}`}});
   if(path===`git/commits/${source}`)return json({tree:{sha:tree},parents:[{sha:base},{sha:head}]});
   throw Error(`Unexpected API request ${path}`);
  };
  const rejects=policy||tampered||wrongTree||failed||missing||unsafe;
  if(rejects)await assert.rejects(reuse);
  else{const result=await reuse();assert.equal(result.reused,true);assert.equal(readFileSync('dist/index.html','utf8'),'tested output');assert.equal(result.proofs.length,2);}
 }finally{process.chdir(originalCwd);global.fetch=originalFetch;for(const key of Object.keys(process.env))if(!Object.hasOwn(environment,key))delete process.env[key];Object.assign(process.env,environment);rmSync(root,{recursive:true,force:true});}
}
await scenario();
for(const options of [{policy:true},{tampered:true},{wrongTree:true},{failed:true},{missing:true},{unsafe:true}])await scenario(options);
console.log('Reuse integration: exact-tree hit after merged PR relations disappear; forged base policy, tampered ZIP, changed tree, failed suite, missing receipt and traversal payload rejected; storage never receives repository token.');

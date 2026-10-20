/** API fixtures exercise independent GitHub provenance, not repository receipts. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,rmSync,mkdtempSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {fixture,identity,finish,verification} from './ci-model-proof-test.mjs';
import {computeModelInputs,modelPolicyDigest,modelPolicyDigestAtCommit,hashBytes,planModelReuse} from './ci-model-proof.mjs';
import {fetchVerifiedBaseProof,extractModelProof,proofArtifactName} from './ci-model-cache.mjs';

const zip=(proof,{name='model-proof.json',duplicate=false,symlink=false}={})=>{
  const dir=mkdtempSync(join(tmpdir(),'proof-zip-test-'));
  try{const input=join(dir,'input.json'),output=join(dir,'proof.zip');writeFileSync(input,JSON.stringify(proof));
    execFileSync('python3',['-c',`import sys,zipfile\nb=open(sys.argv[1],'rb').read()\nwith zipfile.ZipFile(sys.argv[2],'w',compression=zipfile.ZIP_DEFLATED) as z:\n i=zipfile.ZipInfo(sys.argv[3]); i.external_attr=(0o120777 if sys.argv[5]=='1' else 0o100644)<<16; z.writestr(i,b)\n if sys.argv[4]=='1': z.writestr(sys.argv[3],b)`,input,output,name,String(Number(duplicate)),String(Number(symlink))],{stdio:['ignore','pipe','ignore']});return readFileSync(output);
  }finally{rmSync(dir,{recursive:true,force:true});}
};
const f=fixture(190),repository='owner/repo';
try{
  const git=(...args)=>execFileSync('git',args,{cwd:f.root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
  git('init','--initial-branch=main');git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid');git('add','.');git('commit','-m','Successful protected main baseline');
  const baseSha=git('rev-parse','HEAD'),baseInputs=computeModelInputs({root:f.root});assert.equal(modelPolicyDigest(f.root),modelPolicyDigestAtCommit(baseSha,{root:f.root}));
  const baseProof=finish(baseInputs,planModelReuse({inputs:baseInputs}),{...identity(baseSha,101),source_tree:git('rev-parse','HEAD^{tree}')});
  f.add(4);git('add','.');git('commit','-m','Four new data-only models');const currentSha=git('rev-parse','HEAD'),inputs=computeModelInputs({root:f.root});
  const run={id:101,run_attempt:1,event:'push',head_branch:'main',head_sha:baseSha,status:'completed',conclusion:'success',path:'.github/workflows/full-release-review.yml',workflow_id:99,check_suite_id:202,repository:{id:12,full_name:repository},head_repository:{id:12,full_name:repository}};
  const suite={id:202,status:'completed',conclusion:'success',head_sha:baseSha,app:{id:15368,slug:'github-actions',owner:{login:'github'}}};
  const originalZip=zip(baseProof),metadata={id:303,name:proofArtifactName(1),expired:false,digest:`sha256:${hashBytes(originalZip)}`,workflow_run:{id:101,head_sha:baseSha,repository_id:12,head_repository_id:12}};
  const baseManifest=JSON.parse(git('show',`${baseSha}:assets/manifest.json`));
  async function lookup({alterRun,alterSuite,alterArtifact,download=originalZip,extraMember,attempt=1,sourceManifest=baseManifest,missing=false,apiFailure=false,newer=false,ancestor=true,largeManifest=false}={}){
    const r=structuredClone(run),s=structuredClone(suite),a=structuredClone(metadata);alterRun?.(r);alterSuite?.(s);alterArtifact?.(a);const requests=[];
    const fetchImpl=async(url,options={})=>{
      url=String(url);requests.push({url,options});
      if(url==='https://storage.example.invalid/immutable.zip'){
        assert.equal(options.headers,undefined,'Repository token must never be forwarded to storage');return new Response(download);
      }
      assert.equal(options.headers.Authorization,'Bearer test-read-token');
      const path=url.split(`/repos/${repository}/`)[1];let body;
      if(apiFailure)return new Response('unavailable',{status:503});
      if(path==='')body={id:12,full_name:repository,default_branch:'main'};
      else if(path==='git/ref/heads/main')body={ref:'refs/heads/main',object:{sha:currentSha}};
      else if(path.startsWith('compare/'))body={status:ancestor?'ahead':'diverged',merge_base_commit:{sha:baseSha}};
      else if(path==='actions/workflows/full-release-review.yml')body={id:99,path:'.github/workflows/full-release-review.yml'};
      else if(path.startsWith('actions/workflows/99/runs?'))body={workflow_runs:missing?[]:[{id:101,head_sha:newer?currentSha:baseSha}]};
      else if(path==='actions/runs/101')body=r;
      else if(path===`actions/runs/101/attempts/${r.run_attempt}`)body={...r,run_attempt:attempt};
      else if(path==='check-suites/202')body=s;
      else if(path==='actions/runs/101/artifacts?per_page=100')body={artifacts:[a]};
      else if(path==='actions/artifacts/303')body=a;
      else if(path==='actions/artifacts/303/zip')return new Response(null,{status:302,headers:{location:'https://storage.example.invalid/immutable.zip'}});
      else if(path===`contents/assets/manifest.json?ref=${baseSha}`)body=largeManifest?{type:'file',encoding:'none',sha:'a'.repeat(40)}:{type:'file',encoding:'base64',content:Buffer.from(JSON.stringify(sourceManifest)).toString('base64')};
      else if(path===`git/blobs/${'a'.repeat(40)}`)body={sha:'a'.repeat(40),encoding:'base64',content:Buffer.from(JSON.stringify(sourceManifest)).toString('base64')};
      else throw Error(`Unexpected fixture API path: ${path}`);
      return new Response(JSON.stringify(body),{headers:{'content-type':'application/json'}});
    };
    const result=await fetchVerifiedBaseProof({root:f.root,repository,baseSha,currentSha,inputs,token:'test-read-token',fetchImpl});return {...result,requests};
  }
  const valid=await lookup();assert(valid.verifiedBaseProof,valid.reasons.join('\n'));const planned=planModelReuse({inputs,...valid});assert.equal(planned.fresh_ids.length,4);assert.equal(planned.reused_ids.length,190);
  assert((await lookup({largeManifest:true})).verifiedBaseProof,'Large GitHub manifest must use exact blob fallback');
  const rejects=[
    {missing:true},{apiFailure:true},{ancestor:false},{newer:true},
    {alterRun:r=>r.conclusion='failure'},{alterRun:r=>r.status='in_progress'},
    {alterRun:r=>r.event='pull_request'},{alterRun:r=>r.head_branch='feature'},
    {alterRun:r=>r.path='.github/workflows/not-full-review.yml'},{alterRun:r=>r.workflow_id=100},
    {alterRun:r=>r.head_repository={id:13,full_name:'fork/repo'}},{attempt:2},
    {alterSuite:s=>s.app.owner.login='attacker'},{alterSuite:s=>s.app.id=7},{alterSuite:s=>s.conclusion='failure'},
    {alterArtifact:a=>a.expired=true},{alterArtifact:a=>a.name='model-proof-v2-2'},
    {alterArtifact:a=>a.workflow_run.head_repository_id=13},{alterArtifact:a=>delete a.digest},
    {download:Buffer.from('tampered')},
    {sourceManifest:{...baseManifest,assets:baseManifest.assets.slice(1)}}
  ];
  for(const options of rejects){const result=await lookup(options);assert.equal(result.verifiedBaseProof,null,JSON.stringify(options));assert.equal(planModelReuse({inputs,...result}).reused_ids.length,0);}
  // Rewriting receipt keys and the receipt's own alleged hashes cannot rewrite
  // the independently obtained immutable GitHub archive SHA-256.
  const forged=structuredClone(baseProof);forged.models[0].input_key=inputs.models[0].input_key;forged.models[0].glb_sha256='0'.repeat(64);forged.claimed_artifact_sha256=hashBytes(JSON.stringify(forged));
  assert.equal((await lookup({download:zip(forged)})).verifiedBaseProof,null);
  for(const options of [{name:'../model-proof.json'},{name:'/tmp/model-proof.json'},{name:'script.mjs'},{duplicate:true},{symlink:true}])assert.throws(()=>extractModelProof(zip(baseProof,options)));
  const unknown=structuredClone(baseProof);unknown.models.push({...unknown.models[0],id:'not-in-source-catalog'});const unknownZIP=zip(unknown);
  assert.equal((await lookup({download:unknownZIP,alterArtifact:a=>a.digest=`sha256:${hashBytes(unknownZIP)}`})).verifiedBaseProof,null,'Even authenticated malformed artifacts cannot add unknown proof records');
  const badVersion=zip({...baseProof,version:1});assert.equal((await lookup({download:badVersion,alterArtifact:a=>a.digest=`sha256:${hashBytes(badVersion)}`})).verifiedBaseProof,null);
  const missingRecord=structuredClone(baseProof);missingRecord.models.pop();const partialZIP=zip(missingRecord),partial=await lookup({download:partialZIP,alterArtifact:a=>a.digest=`sha256:${hashBytes(partialZIP)}`});assert(partial.verifiedBaseProof);assert.equal(planModelReuse({inputs,...partial}).reused_ids.length,189);
  f.put('site/ci-model-proof.mjs','// PR tries to weaken its own verifier');const changedInputs=computeModelInputs({root:f.root});assert.notEqual(changedInputs.policy_sha256,inputs.policy_sha256);assert.equal(modelPolicyDigestAtCommit(baseSha,{root:f.root}),baseInputs.policy_sha256);
  assert.equal(planModelReuse({inputs:changedInputs,baseProof,verifiedBaseProof:verification(baseProof)}).reused_ids.length,0);
  console.log('Model cache v2: independent run/suite/artifact/attempt/source/ancestry checks, archive safety, large manifest and coordinated-forgery fixtures pass.');
}finally{f.close();}

/** Synthetic 190+4 tests execute the real independent lookup and capture selector. */
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {modelPolicyDigest,modelPolicyDigestAtCommit} from './ci-model-proof.mjs';
import {posterInputKey} from './gallery-poster-inputs.mjs';
import {posterHash,posterArtifactName,posterRuntime,selectPosterCaptures,importVerifiedPosters,writePosterProof} from './gallery-poster-proof.mjs';
import {rankPosterCandidates,extractPosterArtifact,fetchVerifiedPosterBaseline,promoteVerifiedPRPosterProof,writePromotedPosterArtifact} from './gallery-poster-cache.mjs';
import {historicalPosterSource,assertHistoricalPosterRecipe} from './gallery-poster-compat.mjs';
import {posterSharedInputs} from './gallery-poster-inputs.mjs';

const root=mkdtempSync(join(tmpdir(),'poster-cache-test-')),repository='owner/gallery';
const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
const put=(path,data)=>{mkdirSync(join(root,path,'..'),{recursive:true});writeFileSync(join(root,path),typeof data==='string'||Buffer.isBuffer(data)?data:JSON.stringify(data));};
function png(kind,id){const bytes=Buffer.alloc(64);Buffer.from('89504e470d0a1a0a','hex').copy(bytes);bytes.writeUInt32BE(kind==='detail'?512:768,16);bytes.writeUInt32BE(kind==='detail'?512:432,20);bytes[25]=6;bytes.write(id,26);return bytes;}
const assets=Array.from({length:194},(_,index)=>({id:`model-${String(index).padStart(3,'0')}`,glb:`assets/model-${index}.glb`,sha256:{glb:posterHash(String(index))}}));
const baseManifest={assets:assets.slice(0,190)},manifest={assets},shared={version:3,sha256:'a'.repeat(64),browser:'141.0.7390.37'},runtime=posterRuntime(shared);
const data=new Map(),records=baseManifest.assets.map(asset=>{
 const poster={source_glb_sha256:asset.sha256.glb,input_sha256:posterInputKey(asset,shared),browser_version:shared.browser,wheelSpec:{azimuth:0,elevation:1,zoom:1,aspect:16/9,offset:[0,0],floorCenter:[0,0],floorPoints:[[0,0],[1,0],[1,1]],projectedBounds:{left:0,right:1,top:0,bottom:1}}},files=[];
 for(const kind of ['detail','wheel']){const path=`gallery/posters/${asset.id}${kind==='wheel'?'-wheel':''}.png`,bytes=png(kind,asset.id);poster[kind]=path;data.set(path,bytes);files.push({path,bytes:bytes.length,sha256:posterHash(bytes)});}
 return {id:asset.id,input_sha256:poster.input_sha256,source_glb_sha256:asset.sha256.glb,poster,files,evidence:'captured'};
});
function archive(proof,{badPNG=false,extra,duplicate=false,symlink=false}={}){
 const dir=mkdtempSync(join(tmpdir(),'poster-archive-'));
 try{
  writeFileSync(join(dir,'proof.json'),JSON.stringify(proof));mkdirSync(join(dir,'input'));
  const entries=[];for(const row of proof.posters)for(const seal of row.files){const bytes=Buffer.from(data.get(seal.path));if(badPNG&&entries.length===0)bytes[26]^=1;const name=String(entries.length);writeFileSync(join(dir,'input',name),bytes);entries.push([seal.path,name]);}
  writeFileSync(join(dir,'entries.json'),JSON.stringify(entries));
  execFileSync('python3',['-c',`import zipfile,json,sys,os\nr=sys.argv[1]\nwith zipfile.ZipFile(os.path.join(r,'proof.zip'),'w',compression=zipfile.ZIP_DEFLATED) as z:\n z.write(os.path.join(r,'proof.json'),'gallery-poster-proof.json')\n for path,name in json.load(open(os.path.join(r,'entries.json'))): z.write(os.path.join(r,'input',name),path)\n if sys.argv[2]: z.writestr(sys.argv[2],b'x')\n if sys.argv[3]=='1': z.writestr('gallery-poster-proof.json',b'{}')\n if sys.argv[4]=='1':\n  i=zipfile.ZipInfo('gallery/posters/link.png');i.external_attr=0o120777<<16;z.writestr(i,b'target')`,dir,extra||'',String(Number(duplicate)),String(Number(symlink))],{stdio:['ignore','pipe','ignore']});return readFileSync(join(dir,'proof.zip'));
 }finally{rmSync(dir,{recursive:true,force:true});}
}
try{
 put('site/ci-model-proof.mjs','// Protected fixture policy');put('site/gallery/renderer.js','// Renderer v1');put('.github/workflows/full-release-review.yml','name: Review');put('package.json','{}');put('package-lock.json','{}');put('vite.config.js','// fixed');put('assets/manifest.json',baseManifest);
 git('init','--initial-branch=main');git('config','user.name','Poster fixture');git('config','user.email','fixture@example.invalid');git('add','.');git('commit','-m','Trusted 190 baseline');
 const baseSha=git('rev-parse','HEAD'),policy_sha256=modelPolicyDigest(root);assert.equal(policy_sha256,modelPolicyDigestAtCommit(baseSha,{root}));
 const proof={version:1,kind:'gallery-poster-capture-proof',status:'pass',repository,source_commit:baseSha,run_id:101,run_attempt:1,policy_sha256,runtime,shared_sha256:shared.sha256,catalog_ids:baseManifest.assets.map(asset=>asset.id).sort(),posters:records};
 put('assets/manifest.json',manifest);git('add','.');git('commit','-m','Four new data-only models');const currentSha=git('rev-parse','HEAD');assert.equal(modelPolicyDigest(root),policy_sha256);
 const run={id:101,run_attempt:1,event:'push',head_branch:'main',head_sha:baseSha,status:'completed',conclusion:'success',path:'.github/workflows/full-release-review.yml',workflow_id:99,check_suite_id:202,repository:{id:12,full_name:repository},head_repository:{id:12,full_name:repository}};
 const suite={id:202,status:'completed',conclusion:'success',head_sha:baseSha,app:{id:15368,slug:'github-actions',owner:{login:'github'}}};
 const original=archive(proof);
 const shadow=mkdtempSync(join(tmpdir(),'poster-python-shadow-')),previousCwd=process.cwd(),previousPythonPath=process.env.PYTHONPATH;
 try{for(const module of ['zipfile','json'])writeFileSync(join(shadow,`${module}.py`),'raise RuntimeError("Untrusted checkout module executed")\n');process.chdir(shadow);process.env.PYTHONPATH=shadow;assert.deepEqual(extractPosterArtifact(original).proof,proof,'Isolated poster decoding ignores checkout/PYTHONPATH modules');}
 finally{process.chdir(previousCwd);if(previousPythonPath===undefined)delete process.env.PYTHONPATH;else process.env.PYTHONPATH=previousPythonPath;rmSync(shadow,{recursive:true,force:true});}
 async function lookup({document=proof,download,alterRun,alterSuite,alterArtifact,missing=false,source=baseManifest,ancestry=true,currentPolicy=policy_sha256,actualRuntime=runtime,independentDigest,attempt=1,apiFailure=false,socketAt,socketFailures=0,retryCandidate=false,timeoutMs,onTiming}={}){
  const bytes=download||archive(document),r=structuredClone(run),s=structuredClone(suite),a={id:303,name:posterArtifactName(1),expired:false,digest:independentDigest||`sha256:${posterHash(bytes)}`,workflow_run:{id:101,head_sha:baseSha,repository_id:12,head_repository_id:12}};
  alterRun?.(r);alterSuite?.(s);alterArtifact?.(a);const requests=[],timings=[];let socketCalls=0,firstSocketOptions;
  const fetchImpl=async(url,options={})=>{
   url=String(url);requests.push(url);
   if(socketAt&&url.endsWith(socketAt)){
    socketCalls++;if(firstSocketOptions)assert.equal(options,firstSocketOptions,'Retries keep the original signal/options');else firstSocketOptions=options;
    if(socketCalls<=socketFailures)throw Object.assign(new TypeError('sensitive transport text'),{cause:{code:'UND_ERR_SOCKET'}});
   }
   if(url==='https://storage.example.invalid/posters.zip'){assert.equal(options.headers,undefined,'Token forwarded to storage');return new Response(bytes);}
   assert.equal(options.headers.Authorization,'Bearer fixture-token');
   const rootURL=`https://api.github.com/repos/${repository}`;
   assert(url===rootURL||url.startsWith(`${rootURL}/`),'Wrong GitHub API origin or repository');
   assert.notEqual(url,`${rootURL}/`,'GitHub repository metadata endpoint rejects a trailing slash');
   const path=url===rootURL?'':url.slice(rootURL.length+1);let value;
   if(apiFailure)return new Response('unavailable',{status:503});
   if(path==='')value={id:12,full_name:repository,default_branch:'main'};
   else if(path==='git/ref/heads/main')value={ref:'refs/heads/main',object:{sha:currentSha}};
   else if(path.startsWith('compare/'))value={status:ancestry?'ahead':'diverged',merge_base_commit:{sha:baseSha}};
   else if(path==='actions/workflows/full-release-review.yml')value={id:99,path:'.github/workflows/full-release-review.yml'};
   else if(path.startsWith('actions/workflows/99/runs?'))value={workflow_runs:missing?[]:[...(retryCandidate?[{id:102,head_sha:baseSha}]:[]),{id:101,head_sha:baseSha}]};
   else if(path==='actions/runs/102')value={...r,id:102,conclusion:'failure'};
   else if(path==='actions/runs/101')value=r;
   else if(path===`actions/runs/101/attempts/${r.run_attempt}`)value={...r,run_attempt:attempt};
   else if(path==='check-suites/202')value=s;
   else if(path==='actions/runs/101/artifacts?per_page=100')value={artifacts:[a]};
   else if(path==='actions/artifacts/303')value=a;
   else if(path==='actions/artifacts/303/zip')return new Response(null,{status:302,headers:{location:'https://storage.example.invalid/posters.zip'}});
   else if(path===`contents/assets/manifest.json?ref=${baseSha}`)value={type:'file',encoding:'none',sha:'b'.repeat(40)};
   else if(path===`git/blobs/${'b'.repeat(40)}`)value={sha:'b'.repeat(40),encoding:'base64',content:Buffer.from(JSON.stringify(source)).toString('base64')};
   else throw Error(`Unexpected fixture URL ${url}`);
   return new Response(JSON.stringify(value),{headers:{'content-type':'application/json'}});
  };
  const result=await fetchVerifiedPosterBaseline({root,repository,baseSha,currentSha,shared,policy_sha256:currentPolicy,runtime:actualRuntime,token:'fixture-token',fetchImpl,timeoutMs,onTiming:entry=>{timings.push(entry);onTiming?.(entry);}});return {...result,socketCalls,requests,timings};
 }
 const rerun=await lookup({retryCandidate:true});assert(rerun.verified,rerun.reasons.join('; '));
 assert.equal(rerun.timings.filter(row=>row.stage==='poster committed policy').length,1,'Same-commit reruns share one authenticated policy snapshot');
 assert.equal(rerun.timings.filter(row=>row.stage==='poster current archive append').length,2,'Mutable worktree is not cached');
 const noBudget=await lookup({timeoutMs:0});assert.equal(noBudget.verified,null);assert.equal(noBudget.requests.length,0);
 const exhaustedLocal=await lookup({retryCandidate:true,timeoutMs:1000,onTiming:entry=>{if(entry.stage==='poster committed policy')Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,1010);}});
 assert.equal(exhaustedLocal.verified,null);assert.equal(exhaustedLocal.reasons.filter(reason=>reason.startsWith('Poster candidate ')).length,1,'Budget exhaustion stops the candidate loop');
 assert(!exhaustedLocal.requests.some(url=>/\/actions\/runs\//.test(url)),'No run metadata GET starts after local validation exhausts the total budget');
 // The final authenticated bundle copy is synchronous too: expiry there must
 // not return a reusable handle after the last API and validation checks.
 const originalClone=globalThis.structuredClone;let tailCopies=0;
 globalThis.structuredClone=(value,...options)=>{if(value?.kind==='gallery-poster-capture-proof'){tailCopies++;Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,1010);}return originalClone(value,...options);};
 try{
  const exhaustedTail=await lookup({download:original,timeoutMs:1000});
  assert.equal(tailCopies,1,'Exercise the final authenticated bundle copy');
  assert.equal(exhaustedTail.verified,null,'Synchronous final copying cannot return a handle past the total deadline');
  assert(exhaustedTail.reasons.some(reason=>reason.includes('budget exhausted')));
 }finally{globalThis.structuredClone=originalClone;}
 const found=await lookup();assert(found.verified,found.reasons.join('; '));
 assert((await lookup({apiFailure:true})).reasons.some(reason=>reason==='GitHub poster read failed (503) at repository metadata'),'A failed read reports the safe endpoint, not credentials');
 for(const socketAt of ['/actions/runs/101','/actions/artifacts/303/zip','/posters.zip']){
  const retried=await lookup({socketAt,socketFailures:1});assert(retried.verified,retried.reasons.join('; '));assert.equal(retried.socketCalls,2);
  const exhausted=await lookup({socketAt,socketFailures:3});assert.equal(exhausted.verified,null);assert.equal(exhausted.socketCalls,3);assert(exhausted.reasons.some(reason=>reason.includes('UND_ERR_SOCKET')));assert(!exhausted.reasons.join().includes('sensitive'));
 }
 const select=(options={})=>selectPosterCaptures({manifest,shared,policy_sha256,runtime,verified:found.verified,...options});
 assert.deepEqual(select().capture,assets.slice(190).map(asset=>asset.id),'Only the four new actual capture IDs are selected');assert.equal(select().reused.length,190);
 assert.equal(select({shared:{...shared,sha256:'b'.repeat(64)}}).capture.length,194,'Changed renderer selects every non-golden ID');
 assert.equal(select({verified:JSON.parse(JSON.stringify(found.verified))}).capture.length,194,'A matching repository JSON receipt is not an authenticated capability');
 assert.equal(select({verified:{...found.verified,kind:'strict-gpu-model-proof'}}).reused.length,0,'GPU proof does not authorize posters');
 const resources={version:1,posters:{},files:[]},outputRoot=join(root,'out');mkdirSync(outputRoot);
 const imported=await importVerifiedPosters({manifest,shared,resources,outputRoot,verified:found.verified,policy_sha256,runtime});assert.deepEqual(imported.selection.capture,select().capture);assert.equal(Object.keys(imported.resources.posters).length,190);
 for(const row of records)for(const seal of row.files)assert.equal(posterHash(readFileSync(join(outputRoot,seal.path))),seal.sha256,'Imported PNG bytes must exactly match independent artifact');
 const partial=structuredClone(proof);partial.posters.pop();const missingEntry=await lookup({document:partial});assert(missingEntry.verified);assert.deepEqual(select({manifest:baseManifest,verified:missingEntry.verified}).capture,['model-189'],'A missing entry selects exactly one old capture');
 const changed=structuredClone(proof);changed.posters[0].input_sha256=changed.posters[0].poster.input_sha256='f'.repeat(64);const differentInput=await lookup({document:changed});assert(differentInput.verified);assert.equal(select({manifest:baseManifest,verified:differentInput.verified}).capture.length,1);
 const failures=[
  {missing:true},{apiFailure:true},{ancestry:false},{attempt:2},{alterRun:r=>r.event='pull_request'},{alterRun:r=>r.conclusion='failure'},{alterRun:r=>r.path='other.yml'},{alterRun:r=>r.head_branch='feature'},{alterRun:r=>r.head_repository.id=13},
  {alterSuite:s=>s.app.id=7},{alterSuite:s=>s.app.owner.login='forged'},{alterSuite:s=>s.conclusion='failure'},
  {alterArtifact:a=>delete a.digest},{alterArtifact:a=>a.expired=true},{alterArtifact:a=>a.name='model-proof-v2-1'},{alterArtifact:a=>a.workflow_run.head_sha='f'.repeat(40)},
  {download:Buffer.from('tampered'),independentDigest:`sha256:${posterHash(original)}`},
  {download:archive(proof,{badPNG:true})},{document:{...proof,policy_sha256:'f'.repeat(64)}},{currentPolicy:'f'.repeat(64)},
  {actualRuntime:{...runtime,browser:'different'}},{document:{...proof,source_commit:'f'.repeat(40)}},{source:{assets:baseManifest.assets.slice(1)}}
 ];
 for(const options of failures){const failed=await lookup(options);assert.equal(failed.verified,null,JSON.stringify(options));assert.equal(select({verified:failed.verified}).capture.length,194);}
 for(const options of [{extra:'../escape'},{extra:'/tmp/escape'},{extra:'arbitrary.js'},{duplicate:true},{symlink:true}])assert.throws(()=>extractPosterArtifact(archive(proof,options)));
 const hashMismatch=structuredClone(proof);hashMismatch.posters[0].files[0].sha256='f'.repeat(64);assert.equal((await lookup({document:hashMismatch})).verified,null);
 const byteMismatch=structuredClone(proof);byteMismatch.posters[0].files[0].bytes++;assert.equal((await lookup({document:byteMismatch})).verified,null);
 await assert.rejects(()=>writePosterProof({root,outputRoot,manifest,resources:imported.resources,shared,policy_sha256,runtime,directory:'emitted',identity:{repository,source_commit:currentSha,run_id:105,run_attempt:1},verified:found.verified,captured:[]}),/generation coverage/);
 const emitted=await writePosterProof({root,outputRoot,manifest:baseManifest,resources:imported.resources,shared,policy_sha256,runtime,directory:'emitted',identity:{repository,source_commit:currentSha,run_id:105,run_attempt:1},verified:found.verified,captured:[]});assert.equal(emitted.posters.length,190);assert.equal(emitted.reused_ids.length,190);
 // Exact-tree main promotion carries a separately verified PR poster artifact,
 // including when the main workflow itself reuses all previous acceptance work.
 put('assets/manifest.json',baseManifest);git('add','.');git('commit','-m','Poster promotion fixture');
 const prHead=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}');
 const prMerge=git('commit-tree',tree,'-p',baseSha,'-p',prHead,'-m','PR tested merge');
 const mainMerge=git('commit-tree',tree,'-p',baseSha,'-p',prHead,'-m','Merged main');git('checkout','--detach',mainMerge);
 const savedCwd=process.cwd(),savedEvent=process.env.GITHUB_EVENT_NAME,savedRef=process.env.GITHUB_REF;
 process.chdir(root);process.env.GITHUB_EVENT_NAME='push';process.env.GITHUB_REF='refs/heads/main';
 try{
  async function promote({wrongTree=false,failed=false,missing=false,partial=false,wrongAttempt=false}={}){
   const doc={...proof,source_commit:prMerge,...(partial?{posters:proof.posters.slice(1)}:{})},bytes=archive(doc);
   const r={...run,event:'pull_request',head_branch:'feature',head_sha:prHead,conclusion:failed?'failure':'success'};
   const meta={id:303,name:posterArtifactName(1),expired:false,digest:`sha256:${posterHash(bytes)}`,workflow_run:{id:101,head_sha:prHead,repository_id:12,head_repository_id:12}};
   const fetchImpl=async(url,options={})=>{
    url=String(url);if(url==='https://storage.example.invalid/promote.zip'){assert.equal(options.headers,undefined);return new Response(bytes);}
    const rootURL=`https://api.github.com/repos/${repository}`;
    assert(url===rootURL||url.startsWith(`${rootURL}/`),'Wrong GitHub API origin or repository');
    assert.notEqual(url,`${rootURL}/`,'GitHub repository metadata endpoint rejects a trailing slash');
    const path=url===rootURL?'':url.slice(rootURL.length+1);let body;
    if(path==='')body={id:12,full_name:repository,default_branch:'main'};
    else if(path===`commits/${mainMerge}/pulls`)body=[{merged_at:'2026-10-20',merge_commit_sha:mainMerge,base:{ref:'main',repo:{full_name:repository}},head:{sha:prHead,repo:{full_name:repository}}}];
    else if(path==='actions/workflows/full-release-review.yml')body={id:99,path:run.path};
    else if(path.startsWith('actions/workflows/99/runs?'))body={workflow_runs:[{id:101}]};
    else if(path==='actions/runs/101')body=r;
    else if(path==='actions/runs/101/attempts/1')body={...r,run_attempt:wrongAttempt?2:1};
    else if(path==='check-suites/202')body={...suite,head_sha:prHead};
    else if(path==='actions/runs/101/artifacts?per_page=100')body={artifacts:missing?[]:[meta]};
    else if(path==='actions/artifacts/303')body=meta;
    else if(path==='actions/artifacts/303/zip')return new Response(null,{status:302,headers:{location:'https://storage.example.invalid/promote.zip'}});
    else if(path===`git/commits/${prMerge}`)body={tree:{sha:wrongTree?'f'.repeat(40):tree},parents:[{sha:baseSha},{sha:prHead}]};
    else if(path.startsWith('compare/'))body={status:'ahead',merge_base_commit:{sha:baseSha}};
    else if(path===`contents/assets/manifest.json?ref=${prMerge}`)body={type:'file',encoding:'base64',content:Buffer.from(JSON.stringify(baseManifest)).toString('base64')};
    else throw Error(`Unexpected promotion fixture path ${path}`);
    return new Response(JSON.stringify(body),{headers:{'content-type':'application/json'}});
   };
   return promoteVerifiedPRPosterProof({root,repository,currentSha:mainMerge,shared,policy_sha256,runtime,token:'fixture-token',fetchImpl,runId:301,runAttempt:2});
  }
  const promoted=await promote();assert.equal(promoted.proof.source_commit,mainMerge);assert.equal(promoted.proof.run_id,301);assert.equal(promoted.proof.posters.length,190);assert.equal(promoted.proof.promoted_from.source_commit,prMerge);assert(promoted.proof.posters.every(row=>row.evidence==='reused'));
  await writePromotedPosterArtifact(promoted,{root,directory:'qa/promoted-posters'});assert.equal(posterHash(readFileSync(join(root,'qa/promoted-posters',records[0].poster.detail))),records[0].files[0].sha256);
  for(const options of [{wrongTree:true},{failed:true},{missing:true},{partial:true},{wrongAttempt:true}])await assert.rejects(()=>promote(options),/cannot be promoted/);
 }finally{process.chdir(savedCwd);if(savedEvent===undefined)delete process.env.GITHUB_EVENT_NAME;else process.env.GITHUB_EVENT_NAME=savedEvent;if(savedRef===undefined)delete process.env.GITHUB_REF;else process.env.GITHUB_REF=savedRef;}
 // A late rerun of old190 must not outrank the nearer194 ancestor after a docs-only base.
 const docsBase=git('commit-tree',git('rev-parse',`${currentSha}^{tree}`),'-p',currentSha,'-m','Docs-only comparison base');
 assert.deepEqual(rankPosterCandidates([{id:999,head_sha:baseSha},{id:1,head_sha:currentSha}],{root,baseSha:docsBase}).map(run=>run.id),[1,999]);
 // Actual repository regression: no legacy approval, renderer, source PNG or GLB
 // is rewritten. Removing the additive supported hooks reproduces BOTH old scripts.
 const repo=process.cwd(),baseline=JSON.parse(readFileSync('site/gallery/approved-poster-inputs.json','utf8'));
 const currentShared=await posterSharedInputs(repo);assert.equal(currentShared.version,3);await assertHistoricalPosterRecipe({root:repo,baseline,shared:currentShared});
 for(const path of ['site/capture-gallery-posters.mjs','site/gallery-poster-inputs.mjs'])assert.equal(posterHash(historicalPosterSource(readFileSync(path,'utf8'),path)),baseline.shared.files.find(row=>row[0]===path)[1]);
 await assert.rejects(()=>assertHistoricalPosterRecipe({root:repo,baseline,shared:{...currentShared,browser:'changed'}}),/browser changed/);
 const forgedShared=structuredClone(currentShared);forgedShared.files.find(row=>row[0]==='site/gallery/renderer.js')[1]='f'.repeat(64);await assert.rejects(()=>assertHistoricalPosterRecipe({root:repo,baseline,shared:forgedShared}),/actual renderer/);
 console.log('Gallery poster proof: 190 trusted pairs + four exact new capture IDs; renderer all, missing one, independent GitHub/artifact/PNG/byte/control/runtime/source failures closed; untrusted JSON and GPU evidence rejected; legacy golden programs remain byte-identical outside explicit additive v3 hooks.');
}finally{rmSync(root,{recursive:true,force:true});}

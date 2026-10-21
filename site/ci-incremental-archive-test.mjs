/** Authenticated immutable archive inheritance. GPU/card reports are fixtures,
 * never evidence of rendered production assets or whole-workflow speed. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdtempSync,rmSync,chmodSync,symlinkSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import childProcess,{execFileSync} from 'node:child_process';
import {syncBuiltinESMExports} from 'node:module';
import {performance} from 'node:perf_hooks';
import {fixture,buildFixture,finish,identity} from './ci-model-proof-test.mjs';
import {archiveFixture} from './ci-archival-inputs-test.mjs';
import {computeModelInputs,assertBuiltRenderInputs,planModelReuse,hashBytes,modelArchivalInputs,modelPolicyDigest,modelPolicyDigestAtCommit,prepareModelPolicyContext} from './ci-model-proof.mjs';
import {prepareModelSource,proofArtifactName,authenticatedModelBaseline} from './ci-model-cache.mjs';
import {prepareArchivalInheritance} from './ci-archival-inputs.mjs';
import {eligibilityFromGit} from './ci-incremental-models.mjs';
const repository='owner/repo';
function zip(proof){
 const dir=mkdtempSync(join(tmpdir(),'archive-proof-zip-'));
 try{writeFileSync(join(dir,'proof.json'),JSON.stringify(proof));execFileSync('python3',['-I','-c','import sys,zipfile\nwith zipfile.ZipFile(sys.argv[2],"w",compression=zipfile.ZIP_DEFLATED) as z:z.write(sys.argv[1],"model-proof.json")',join(dir,'proof.json'),join(dir,'proof.zip')]);return readFileSync(join(dir,'proof.zip'));}
 finally{rmSync(dir,{recursive:true,force:true});}
}
async function exercise(count){
 const f=fixture(count),archive=archiveFixture(),reads=[],requests=[];
 const git=(...args)=>execFileSync('git',args,{cwd:f.root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
 const copyArchive=()=>{for(const [path,data]of archive.files)f.put(path,data);};
 const addArchive=(name,models)=>{const batch=archive.addBatch(name,models.map(row=>row.id),{models,readModel:path=>readFileSync(join(f.root,path))});batch.archive(`${batch.sourceRoot}/unique-body.bin`,Buffer.from(`actual inert archive bytes: ${name}`));batch.sync();return batch;};
 try{
  for(let start=0;start<count;start+=4)addArchive(`old-${start}`,f.manifest.assets.slice(start,start+4));
  copyArchive();f.put('.gitignore','dist/\nqa/ci-model-proof/\n');
  git('init','-q');git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid');git('add','.');git('commit','-qm','Complete baseline');
  const baseSha=git('rev-parse','HEAD'),oldManifest=structuredClone(f.manifest),oldArchives=modelArchivalInputs(f.root);
  await buildFixture(f);const before=computeModelInputs({root:f.root,built:await assertBuiltRenderInputs({root:f.root})});
  const baseline=finish(before,planModelReuse({inputs:before}),{...identity(baseSha,101),source_tree:git('rev-parse','HEAD^{tree}')});
  f.add(4);const added=f.manifest.assets.slice(-4),newIDs=added.map(row=>row.id);
  f.catalog.packs[0].asset_ids=oldManifest.assets.map(row=>row.id);
  f.catalog.packs.push({id:'new-four',name:{en:'New four',zh:'新增四件'},description:{en:'Fixture only',zh:'仅测试'},asset_ids:newIDs});
  for(const asset of added)asset.packs=['new-four'];
  f.put('assets/manifest.json',f.manifest);f.put('site/catalog-data.json',f.catalog);
  addArchive('new-four',added);copyArchive();git('add','.');git('commit','-qm','Four new models');
  const head=git('rev-parse','HEAD');await buildFixture(f);const built=await assertBuiltRenderInputs({root:f.root});
  const run={id:101,run_attempt:1,event:'push',head_branch:'main',head_sha:baseSha,status:'completed',conclusion:'success',path:'.github/workflows/full-release-review.yml',workflow_id:99,check_suite_id:202,repository:{id:12,full_name:repository},head_repository:{id:12,full_name:repository}};
  async function lookup({proof=baseline,alterRun,alterSuite,alterArtifact,apiFailure=false}={}){
   const data=zip(proof),r=structuredClone(run),suite={id:202,status:'completed',conclusion:'success',head_sha:baseSha,app:{id:15368,slug:'github-actions',owner:{login:'github'}}};alterRun?.(r);alterSuite?.(suite);
   const metadata={id:303,name:proofArtifactName(1),expired:false,digest:`sha256:${hashBytes(data)}`,workflow_run:{id:101,head_sha:baseSha,repository_id:12,head_repository_id:12}};alterArtifact?.(metadata);
   reads.length=0;requests.length=0;const currentSha=git('rev-parse','HEAD');
   const fetchImpl=async url=>{
    url=String(url);requests.push(url);if(apiFailure)return new Response('unavailable',{status:503});
    if(url==='https://storage.example.invalid/archive.zip')return new Response(data);
    const path=url.replace(`https://api.github.com/repos/${repository}`,'').replace(/^\//,'');let body;
    if(!path)body={id:12,full_name:repository,default_branch:'main'};
    else if(path==='git/ref/heads/main')body={ref:'refs/heads/main',object:{sha:baseSha}};
    else if(path.startsWith('compare/'))body={status:'ahead',merge_base_commit:{sha:baseSha}};
    else if(path==='actions/workflows/full-release-review.yml')body={id:99,path:run.path};
    else if(path.startsWith('actions/workflows/99/runs?'))body={workflow_runs:[{id:101,head_sha:baseSha}]};
    else if(path==='actions/runs/101')body=r;
    else if(path==='actions/runs/101/attempts/1')body=r;
    else if(path==='check-suites/202')body=suite;
    else if(path==='actions/runs/101/artifacts?per_page=100')body={artifacts:[metadata]};
    else if(path==='actions/artifacts/303')body=metadata;
    else if(path==='actions/artifacts/303/zip')return new Response(null,{status:302,headers:{location:'https://storage.example.invalid/archive.zip'}});
    else if(path===`contents/assets/manifest.json?ref=${baseSha}`)body={type:'file',encoding:'base64',content:Buffer.from(JSON.stringify(oldManifest)).toString('base64')};
    else throw Error(`Unexpected fixture request: ${path}`);
    return new Response(JSON.stringify(body));
   };
   return prepareModelSource({root:f.root,repository,baseSha,currentSha,token:'fixture-token',fetchImpl,onTiming:()=>{},onInputRead:row=>{assert(requests.includes('https://storage.example.invalid/archive.zip'),'Archive access preceded authenticated artifact download');reads.push(row);}});
  }
  const lookupStarted=performance.now(),found=await lookup(),lookupMs=Math.round(performance.now()-lookupStarted);assert(found.sourceContext,found.reasons.join('; '));
  const oldInert=new Set(oldArchives.checkedInputs.filter(row=>!row.document&&!row.final&&oldArchives.excludedPaths.includes(row.path)).map(row=>row.path));
  assert(oldInert.size>count,'Fixture must contain significant old archive bodies');
  assert.equal(reads.filter(row=>oldInert.has(row.path)).length,0,'Old inert archive bodies must never be read in either exact tree');
  const fullArchives=modelArchivalInputs(f.root),newBodies=fullArchives.checkedInputs.filter(row=>!row.document&&!row.final&&row.path.startsWith('production/new-four/'));
  for(const row of newBodies)assert(reads.some(read=>read.commit===head&&read.path===row.path),`New archive bytes were not verified: ${row.path}`);
  for(const asset of oldManifest.assets)assert(reads.some(row=>row.commit===head&&row.path===asset.glb),'Old final delivered pins remain actual byte checks');
  const optimized=computeModelInputs({root:f.root,built,sourceContext:found.sourceContext}),full=computeModelInputs({root:f.root,built});assert.deepEqual(optimized,full,'Archive shortcut must preserve every model/policy input');
  const plan=planModelReuse({inputs:optimized,...found});assert.equal(plan.reused_ids.length,count);assert.equal(plan.fresh_ids.length,4);
  const complete=finish(optimized,plan,{...identity(head,102),source_tree:git('rev-parse','HEAD^{tree}')},baseline);
  assert.equal(complete.models.length,count+4);assert.equal(complete.catalog_ids.length,count+4);
  console.log(JSON.stringify({fixture:'authenticated-archive-append',old_models:count,new_models:4,old_inert_paths:oldInert.size,old_inert_reads:0,new_archive_body_paths:newBodies.length,immutable_read_calls:reads.length,immutable_read_bytes:reads.reduce((n,row)=>n+row.bytes,0),rss_bytes:process.memoryUsage().rss,peak_rss_kib:process.resourceUsage().maxRSS,lookup_ms:lookupMs,complete_model_records:complete.models.length}));
  const beforeReads=reads.length,beforeRequests=requests.length,now=performance.now.bind(performance),ownNow=Object.getOwnPropertyDescriptor(performance,'now');
  Object.defineProperty(performance,'now',{configurable:true,value:()=>now()+120001});
  try{
   assert.equal(modelPolicyDigest(f.root,{sourceContext:found.sourceContext}),full.policy_sha256,'Authenticated context survives the expired lookup-only budget');
   const eligible=eligibilityFromGit(baseSha,{root:f.root,sourceContext:found.sourceContext,sourceCommit:baseSha});
   assert(eligible.eligible,eligible.reasons.join('; '));
   assert.equal(modelPolicyDigestAtCommit(baseSha,{root:f.root,sourceContext:found.sourceContext}),full.policy_sha256);
  }finally{if(ownNow)Object.defineProperty(performance,'now',ownNow);else delete performance.now;}
  assert.equal(reads.length,beforeReads,'Post-authentication consumers do not read committed archive bodies or metadata again');
  assert.equal(requests.length,beforeRequests,'Post-authentication context does not start network requests');
  if(count!==190)return;
  for(const context of [{},structuredClone(found.sourceContext)]){
   assert.throws(()=>modelPolicyDigest(f.root,{sourceContext:context}),/independently verified root/);
   assert.throws(()=>prepareArchivalInheritance(context),/authenticated process-local/);
   assert.throws(()=>authenticatedModelBaseline(context,{root:f.root,currentSha:head}),/independently authenticated/);
   assert.throws(()=>prepareModelPolicyContext(context,{root:f.root,currentSha:head}),/independently authenticated/);
  }
  assert.throws(()=>modelPolicyDigestAtCommit('f'.repeat(40),{root:f.root,sourceContext:found.sourceContext}),/another exact commit/);
  assert.throws(()=>modelPolicyDigestAtCommit(baseSha,{root:join(f.root,'other'),sourceContext:found.sourceContext}),/same independently verified root/);
  const partial=structuredClone(baseline);partial.models.pop();assert.equal((await lookup({proof:partial})).sourceContext,undefined);
  const overlap=structuredClone(baseline);overlap.reused_ids=[overlap.fresh_ids[0]];assert.equal((await lookup({proof:overlap})).sourceContext,undefined);
  const missingCoverage=structuredClone(baseline);missingCoverage.fresh_ids.pop();assert.equal((await lookup({proof:missingCoverage})).sourceContext,undefined);
  for(const patch of [{source_tree:'f'.repeat(40)},{policy_sha256:'f'.repeat(64)},{runtime_config:{}},{gpu_policy:{}}])assert.equal((await lookup({proof:{...baseline,...patch}})).sourceContext,undefined);
  for(const options of [{alterRun:r=>r.head_branch='feature'},{alterRun:r=>r.head_repository.id=13},{alterRun:r=>r.conclusion='failure'},{alterSuite:s=>s.app.id=7},{alterArtifact:a=>a.digest='sha256:'+ 'f'.repeat(64)},{apiFailure:true}]){assert.equal((await lookup(options)).sourceContext,undefined);assert.equal(reads.length,0,'Untrusted provenance must not start archive declaration reads');}
  git('replace',baseSha,head);
  try{assert((await lookup()).sourceContext,'Replace refs cannot rewrite an authenticated source tree');}
  finally{git('replace','-d',baseSha);}
  f.put('.git/info/grafts',head+'\n');
  try{assert((await lookup()).sourceContext,'Local grafts cannot rewrite authenticated ancestry/tree');}
  finally{rmSync(join(f.root,'.git/info/grafts'));}
  const originalExec=childProcess.execFileSync;
  for(const failFetch of [true,false]){
   let missing=true,fetched=0;
   childProcess.execFileSync=(command,args,options)=>{
    if(command==='git'&&options?.cwd===f.root){
     if(args[0]==='ls-tree')assert(!args.includes('-l'),'Tree identity inventory must not request old blob sizes');
     if(args[0]==='cat-file'&&args[1]==='-e'&&args[2]===`${baseSha}^{commit}`&&missing){missing=false;throw Error('Fixture shallow checkout lacks authenticated ancestor');}
     if(args[0]==='fetch'){
      fetched++;assert.deepEqual(args,['fetch','--no-tags','--depth=1','--filter=blob:none',`https://github.com/${repository}.git`,baseSha]);
      assert.equal(options.env.GIT_NO_REPLACE_OBJECTS,'1');assert.equal(options.env.GIT_GRAFT_FILE,'/dev/null');
      if(failFetch)throw Error('Fixture exact-object fetch failed');return Buffer.alloc(0);
     }
    }
    return originalExec(command,args,options);
   };syncBuiltinESMExports();
   try{const acquired=await lookup();assert.equal(Boolean(acquired.sourceContext),!failFetch);assert.equal(fetched,1);if(failFetch)assert.equal(reads.length,0,'Failed exact-object acquisition cannot grant archive trust');}
   finally{childProcess.execFileSync=originalExec;syncBuiltinESMExports();}
  }
  const oldBody=[...oldInert].find(path=>path.endsWith('unique-body.bin')),original=readFileSync(join(f.root,oldBody));
  f.put(oldBody,'mutable changed archive');assert.throws(()=>modelArchivalInputs(f.root),/SHA-256 mismatch/);
  assert.equal(modelPolicyDigest(f.root,{sourceContext:found.sourceContext}),full.policy_sha256,'Explicit immutable context does not claim mutable archive validation');f.put(oldBody,original);
  const viewer=readFileSync(join(f.root,'site/viewer.js'));f.put('site/viewer.js',viewer+'\n// changed live executed code\n');assert.throws(()=>computeModelInputs({root:f.root,built,sourceContext:found.sourceContext}),/Live render policy differs/);f.put('site/viewer.js',viewer);
  f.put('site/viewer.js',`import '../${archive.batches[0].generator.path}';\n`+viewer);assert.throws(()=>modelPolicyDigest(f.root,{sourceContext:found.sourceContext}),/Live execution dependencies differ/);f.put('site/viewer.js',viewer);
  f.put('qa/unknown/new-script.py','# unowned execution sibling');assert.throws(()=>modelPolicyDigest(f.root,{sourceContext:found.sourceContext}),/Live render policy differs/);rmSync(join(f.root,'qa/unknown'),{recursive:true});
  const glb=f.manifest.assets[0].glb,glbBytes=readFileSync(join(f.root,glb));f.put(glb,'modified actual final model');assert.throws(()=>computeModelInputs({root:f.root,built,sourceContext:found.sourceContext}),/Actual glb bytes/);f.put(glb,glbBytes);
  f.put('dist/'+glb,'modified delivered final model');await assert.rejects(()=>assertBuiltRenderInputs({root:f.root}),/Delivered glb bytes differ/);f.put('dist/'+glb,glbBytes);
  async function mutation(change){change();git('add','-A');git('commit','-qm','Rejected historical mutation');assert.equal((await lookup()).sourceContext,undefined);git('reset','--hard',head);}
  await mutation(()=>f.put(oldBody,Buffer.alloc(original.length,120)));
  await mutation(()=>chmodSync(join(f.root,oldBody),0o755));
  await mutation(()=>{rmSync(join(f.root,oldBody));symlinkSync('readme.txt',join(f.root,oldBody));});
  await mutation(()=>f.put(archive.batches[0].descriptor.additions[0].metadata.path,'{}'));
  await mutation(()=>f.put(glb,Buffer.alloc(glbBytes.length,120)));
  await mutation(()=>f.put('site/viewer.js',viewer+'\n// changed protected committed renderer\n'));
  // A source context is invalid once HEAD moves, even if its old JSON is kept.
  f.put('docs-marker.txt','new commit');git('add','.');git('commit','-qm','Head drift');assert.throws(()=>modelPolicyDigest(f.root,{sourceContext:found.sourceContext}),/HEAD changed/);
  console.log('Archive shortcut negatives: complete coverage, provenance/policy/runtime, ordinary JSON, wrong root/ref/HEAD, direct metadata/final pins, blob/mode/symlink, live execution and delivered payload rejected; mutable default rereads.');
 }finally{f.close();}
}
await exercise(190);
await exercise(996);

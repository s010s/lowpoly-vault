/** Exact per-model evidence is reusable only across an owned append-only data diff. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,existsSync,appendFileSync,readdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {inspectCatalogDataAppend} from './curation.js';
import {computeModelInputs,planModelReuse,aggregateModelProof,assertBuiltRenderInputs,PUBLICATION_ONLY_MODULES,modelPolicyDigestAtCommit,modelArchivalInputs,modelArchivalInputsAtCommit} from './ci-model-proof.mjs';
import {assertArchivalAppend,ARCHIVAL_REGISTRY_PATH} from './ci-archival-inputs.mjs';
import {fetchVerifiedBaseProof} from './ci-model-cache.mjs';
import {modelPlan,readModelReceipts,assertModelCoverage,currentIdentity,BUILD_RECEIPT} from './ci-model-shards.mjs';
const read=path=>JSON.parse(readFileSync(path));
const git=(...args)=>execFileSync('git',args,{encoding:'utf8',maxBuffer:128*1024*1024});
const equal=(actual,expected,label)=>assert.deepEqual(actual,expected,label);
function appendRecords(before,after,newIDs,key='id'){
 const retained=after.filter(row=>!newIDs.has(row[key]));equal(retained,before,'Existing mapped records changed');
 const added=after.filter(row=>newIDs.has(row[key]));assert.equal(new Set(added.map(row=>row[key])).size,added.length,'Duplicate new mapped record');
}
export function assessIncrementalDiff({paths,before,after,readBefore,readAfter,authorizationOnlyPaths=[],archivalState=null}){
 try{
  assert(Array.isArray(before.assets)&&Array.isArray(after.assets));
  const oldIDs=new Set(before.assets.map(a=>a.id)),added=after.assets.filter(a=>!oldIDs.has(a.id)),newIDs=new Set(added.map(a=>a.id));
  assert.equal(newIDs.size,added.length,'Duplicate new ID');equal(after.assets.filter(a=>oldIDs.has(a.id)),before.assets,'Published model records must remain unchanged');
  const {assets:oldAssets,publication:oldPublication,...oldShared}=before,{assets:newAssets,publication:newPublication,...newShared}=after;
  equal(newShared,oldShared,'Shared manifest policy changed');
  // Publication metadata is validated by the complete unchanged publication gate.
  // It cannot grant cache trust: input keys and successful-main proof do that.
  inspectCatalogDataAppend(readBefore('site/catalog-data.json'),readAfter('site/catalog-data.json'),{addedAssetIds:[...newIDs],previousManifest:before,currentManifest:after});
  const ownAsset=path=>added.some(asset=>[asset.glb,asset.blend,asset.preview].includes(path)||path.startsWith(`assets/additions/${asset.id}/`)||path.startsWith(`assets/turntables/${asset.id}/`)||path.startsWith(`assets/card-previews/${asset.id}-`)||path===`site/public/gallery/posters/${asset.id}.png`||path===`site/public/gallery/posters/${asset.id}-wheel.png`);
  const authorization=new Set(authorizationOnlyPaths),archives=new Set();
  if(archivalState){
   for(const path of assertArchivalAppend(archivalState.before,archivalState.after,{beforePaths:archivalState.beforePaths,oldIDs:[...oldIDs],newIDs:[...newIDs]}))archives.add(path);
   if(archivalState.before.registryMasked===true&&archivalState.after.registryMasked===true)archives.add(ARCHIVAL_REGISTRY_PATH);
  }
  for(const path of paths){
   if(/^(?:README(?:\.zh-CN)?\.md|docs\/[a-zA-Z0-9_./-]+\.md)$/.test(path)&&!path.split('/').includes('..'))continue;
   if(authorization.has(path)||archives.has(path))continue;
   if(path==='assets/manifest.json'||path==='site/catalog-data.json')continue;
   // These namespaces are inert evidence. Executable or unknown extensions do not qualify.
   if(/^(?:assets\/releases\/|production\/|qa\/)[A-Za-z0-9_./-]+\.(?:json|md|png|webp|jpg|jpeg|glb|blend)$/.test(path)&&!path.split('/').includes('..'))continue;
   if(ownAsset(path)&&/\.(?:json|png|webp|jpg|jpeg|glb|blend)$/.test(path))continue;
   if(path==='assets/turntables/index.json'){
    const {assets:a,posters:p,...shared}=readBefore(path),{assets:aa,posters:pp,...ss}=readAfter(path);equal(ss,shared,'Shared turntable recipe changed');appendRecords(a,aa,newIDs);appendRecords(p,pp,newIDs);continue;
   }
   if(path==='site/gallery/wheel-framing.json'){
    const a=readBefore(path),b=readAfter(path);for(const [id,value]of Object.entries(a))equal(b[id],value,'Existing framing changed');assert(Object.keys(b).every(id=>Object.hasOwn(a,id)||newIDs.has(id)));continue;
   }
   if(path==='site/public/gallery/resources.json'){
    const {posters:a,files:f,...shared}=readBefore(path),{posters:b,files:g,...ss}=readAfter(path);equal(ss,shared,'Shared gallery recipe changed');
    for(const [id,value]of Object.entries(a))equal(b[id],value,'Existing poster metadata changed');assert(Object.keys(b).every(id=>Object.hasOwn(a,id)||newIDs.has(id)));
    const newPaths=new Set([...newIDs].flatMap(id=>[`gallery/posters/${id}.png`,`gallery/posters/${id}-wheel.png`]));equal(g.filter(row=>!newPaths.has(row.path)),f,'Existing gallery seals changed');continue;
   }
   throw Error(`Unknown or shared dependency: ${path}`);
  }
  return {eligible:true,added_ids:[...newIDs].sort(),reasons:['Owned additions or known publication-only change; full publication gates remain mandatory']};
 }catch(error){return {eligible:false,added_ids:[],reasons:[error.message]};}
}
export function eligibilityFromGit(baseSha){
 try{
  assert.match(baseSha||'',/^[a-f0-9]{40}$/);const before=path=>JSON.parse(git('show',`${baseSha}:${path}`)),after=path=>JSON.parse(readFileSync(path));
  const paths=git('diff','--name-only','-z',baseSha,'HEAD').split('\0').filter(Boolean);
  const archivalState={before:modelArchivalInputsAtCommit(baseSha),after:modelArchivalInputs(),beforePaths:git('ls-tree','-r','--name-only','-z',baseSha).split('\0').filter(Boolean)};
  return assessIncrementalDiff({paths,before:before('assets/manifest.json'),after:after('assets/manifest.json'),readBefore:before,readAfter:after,authorizationOnlyPaths:PUBLICATION_ONLY_MODULES,archivalState});
 }catch(error){return {eligible:false,added_ids:[],reasons:[`Diff provenance unavailable: ${error.message}`]};}
}
export function tasksForModelPlan(tasks,plan,manifest){
 const remaining=tasks.filter(task=>task!=='models'&&!task.startsWith('models-')&&task!=='previews');
 const shards=plan.fresh_ids.length?modelPlan(manifest,{ids:plan.fresh_ids.join(',')}):[];
 return [...shards.map(row=>row.task),...(plan.fresh_ids.length?['previews']:[]),...remaining];
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 const directory='qa/ci-model-proof';mkdirSync(directory,{recursive:true});
 const built=await assertBuiltRenderInputs({}),inputs=computeModelInputs({built}),manifest=read('assets/manifest.json');
 assert.equal(inputs.policy_sha256,modelPolicyDigestAtCommit(git('rev-parse','HEAD').trim()),'Live render policy differs from the exact committed source; untracked/generated code cannot establish a reusable baseline');
 if(process.argv[2]==='plan'){
  const eligibility=eligibilityFromGit(process.env.BASE_SHA),force=process.env.FULL_REVIEW==='true'||!eligibility.eligible;
  const found=force?{reasons:['Full validation required',...eligibility.reasons]}:await fetchVerifiedBaseProof({inputs});
  const plan=planModelReuse({inputs,...found}),tasks=tasksForModelPlan(JSON.parse(process.env.CI_REVIEW_TASKS),plan,manifest);
  writeFileSync(`${directory}/plan.json`,JSON.stringify({...plan,eligibility,tasks},null,2)+'\n');writeFileSync(`${directory}/inputs.json`,JSON.stringify(inputs,null,2)+'\n');
  if(found.baseProof)writeFileSync(`${directory}/base-proof.json`,JSON.stringify(found.baseProof,null,2)+'\n');
  for(const[key,value]of Object.entries({tasks:JSON.stringify(tasks),fresh_ids:plan.fresh_ids.join(','),fresh_count:plan.fresh_ids.length,reused_count:plan.reused_ids.length}))if(process.env.GITHUB_OUTPUT)appendFileSync(process.env.GITHUB_OUTPUT,`${key}=${value}\n`);
  console.log(JSON.stringify({fresh:plan.fresh_ids.length,reused:plan.reused_ids.length,eligibility,reasons:plan.reasons}));
 }else if(process.argv[2]==='aggregate'){
  const plan=read(`${directory}/plan.json`);equal(inputs,read(`${directory}/inputs.json`),'Model inputs changed since planning');
  // Saved JSON is not authority: independently re-fetch provenance before combining evidence.
  const found=plan.reused_ids.length?await fetchVerifiedBaseProof({inputs}):{};
  if(plan.reused_ids.length){assert(found.verifiedBaseProof,'Baseline proof no longer independently verifiable');equal(found.verifiedBaseProof,plan.verified_base_proof,'Baseline provenance changed');}
  const build=read('qa/ci-model-build/'+BUILD_RECEIPT),identity=currentIdentity();
  let records=[],cardRecords=[];
  if(plan.fresh_ids.length){const shards=modelPlan(manifest,{ids:plan.fresh_ids.join(',')}),receipts=readModelReceipts('qa/ci-model-shards',shards);assertModelCoverage(manifest,shards,receipts,identity,build);records=receipts.flatMap(row=>row.proof_records||[]);}
  else {equal(build.identity,identity);assert(!existsSync('qa/ci-model-shards')||!execFileSync('find',['qa/ci-model-shards','-type','f'],{encoding:'utf8'}).trim(),'Unexpected fresh shard evidence');}
  const cardDirectory='qa/ci-card-preview-proof';
  if(plan.fresh_ids.length){
    equal(readdirSync(cardDirectory).sort(),['receipt.json'],'Unexpected or missing separate card proof files');
    const card=read(`${cardDirectory}/receipt.json`);assert.equal(card.version,1);assert.equal(card.kind,'card-preview-shard');equal(card.identity,identity,'Card proof source/run differs');assert.equal(card.payload_sha256,build.payload_sha256,'Card proof build differs');cardRecords=card.records;
  }else assert(!existsSync(cardDirectory)||!readdirSync(cardDirectory).length,'Unexpected fresh card evidence');
  const proof=aggregateModelProof({inputs,scopePlan:plan,freshRecords:records,freshCardRecords:cardRecords,identity,build,baseProof:found.baseProof});
  writeFileSync(`${directory}/model-proof.json`,JSON.stringify(proof,null,2)+'\n');console.log(`Complete exact model proof: ${proof.fresh_ids.length} freshly tested + ${proof.reused_ids.length} trusted unchanged = ${proof.catalog_ids.length}.`);
 }else throw Error('Expected plan or aggregate');
}

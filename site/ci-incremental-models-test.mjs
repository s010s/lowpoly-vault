import assert from 'node:assert/strict';
import {LEGACY_OUTPUTS,encode,hashBytes,importLegacySnapshot,recordReference} from './model-registry.mjs';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {assessIncrementalDiff,eligibilityFromGit,tasksForModelPlan,acceptanceExecutionPlan} from './ci-incremental-models.mjs';
import {fixture,identity as fixtureIdentity,finish as finishModelFixture,verification} from './ci-model-proof-test.mjs';
import {computeModelInputs,planModelReuse} from './ci-model-proof.mjs';
import {planBrowserTasks,aggregateBrowserCoverage,assertBrowserCoverage,HISTORICAL_BROWSER_PACKS} from './ci-browser-task-proof.mjs';
const clone=value=>structuredClone(value),read=path=>JSON.parse(readFileSync(path));
const before=read('assets/manifest.json'),catalog=read('site/catalog-data.json'),after=clone(before),newCatalog=clone(catalog);
const paths=['assets/manifest.json','site/catalog-data.json','assets/releases/existing-reviewed-descriptor.json'];
const pack={id:'incremental-fixture-pack',name:{en:'Fixture pack',zh:'测试模型组合'},description:{en:'No real publication',zh:'未发布的测试数据'},asset_ids:[]};
for(let n=1;n<=4;n++){
 const a=clone(before.assets[0]);a.id=`incremental-model-${n}`;a.packs=[pack.id];a.worlds=['prehistoric'];
 for(const key of ['glb','blend','preview'])a[key]=`assets/additions/${a.id}/fixture/model.${key==='preview'?'png':key}`;
 after.assets.push(a);pack.asset_ids.push(a.id);paths.push(...['glb','blend','preview'].map(k=>a[k]));
}
newCatalog.packs.push(pack);after.publication.fixture_descriptor={path:paths[2],sha256:'a'.repeat(64)};
const base={paths,before,after,readBefore:path=>{assert.equal(path,'site/catalog-data.json');return catalog;},readAfter:path=>{assert.equal(path,'site/catalog-data.json');return newCatalog;}};
const good=assessIncrementalDiff(base);assert.equal(good.eligible,true,good.reasons.join('; '));assert.equal(good.added_ids.length,4);assert.equal(after.assets.length,before.assets.length+4);
const reject=(edit,label)=>{const input={...base,paths:[...paths],before:clone(before),after:clone(after)};edit(input);assert.equal(assessIncrementalDiff(input).eligible,false,label);};
reject(input=>input.paths.push('qa/unclassified/test.py'),'Unknown executable');reject(input=>input.paths.push('site/viewer.js'),'Renderer');reject(input=>input.paths.push('site/new-unreviewed-release.mjs'),'Unknown collector');reject(input=>input.after.assets[0].sha256.glb='f'.repeat(64),'Old model changed');reject(input=>input.after.assets.shift(),'Old model removed');reject(input=>input.after.assets.push(clone(input.after.assets.at(-1))),'Duplicate new ID');reject(input=>input.paths.push('site/gallery/approved-poster-inputs.json'),'Golden metadata');
const auth={...base,paths:[...paths,'site/known-publication-only.mjs'],authorizationOnlyPaths:['site/known-publication-only.mjs']};assert.equal(assessIncrementalDiff(auth).eligible,true,'Explicit policy-supplied auth-only role; never from repository data');
// Real old190 resource metadata plus four owned additions. Capture diagnostics
// must not invalidate unchanged pixels, nor hide a renderer/recipe change.
const galleryPath='site/public/gallery/resources.json',oldGallery=read(galleryPath),newGallery=clone(oldGallery);
newGallery.generated_capture.assets=good.added_ids;newGallery.generated_capture.published_total=after.assets.length;
for(const id of good.added_ids){
 const source=Object.values(oldGallery.posters)[0],poster={...source,source_glb_sha256:after.assets.find(asset=>asset.id===id).sha256.glb,detail:`gallery/posters/${id}.png`,wheel:`gallery/posters/${id}-wheel.png`};
 newGallery.posters[id]=poster;
 for(const path of [poster.detail,poster.wheel])newGallery.files.push({...oldGallery.files[0],path});
}
const withGallery=value=>({...base,paths:[...paths,galleryPath],readBefore:path=>path===galleryPath?oldGallery:base.readBefore(path),readAfter:path=>path===galleryPath?value:base.readAfter(path)});
assert.equal(assessIncrementalDiff(withGallery(newGallery)).eligible,true,'Canonical four-only capture diagnostics preserve incremental eligibility');
for(const edit of [
 value=>value.generated_capture.browser='different-browser',
 value=>value.generated_capture.source_renderer_sha256='f'.repeat(64),
 value=>value.generated_capture.runtime_renderer_sha256='f'.repeat(64),
 value=>value.generated_capture.unknown_recipe_option=true,
 value=>value.generated_capture.assets.push(good.added_ids[0]),
 value=>value.generated_capture.assets.push('not-published'),
 value=>value.generated_capture.published_total=after.assets.length+1,
 value=>value.generated_capture.published_total=-1,
 value=>value.posters[before.assets[0].id].detail='gallery/posters/changed.png',
 value=>value.files[0].sha256='f'.repeat(64),
]){const changed=clone(newGallery);edit(changed);assert.equal(assessIncrementalDiff(withGallery(changed)).eligible,false,'Invalid diagnostics, changed recipe or old pixels must require full checks');}
// Native registry additions are inert metadata, not a new proof or publication role.
// Use real historical JSON and the same four synthetic additions as above.
const legacyBefore=Object.fromEntries(Object.entries(LEGACY_OUTPUTS).map(([key,path])=>[key,read(path)]));
const legacyAfter={...clone(legacyBefore),manifest:after,catalog:newCatalog,gallery:newGallery};
const imported=importLegacySnapshot(legacyAfter,{sourceCommit:'a'.repeat(40),sourcePins:Object.fromEntries(Object.entries(LEGACY_OUTPUTS).map(([key,path])=>[key,{path,sha256:hashBytes(encode(legacyAfter[key]))}]))});
const addedRecords=imported.records.filter(record=>good.added_ids.includes(record.id));
const {asset_ids:ignoredMembers,...definition}=pack;
const newBatches=[0,1].map(index=>({version:1,id:`independent-${index}`,records:addedRecords.slice(index*2,index*2+2).map(recordReference),definitions:{worlds:[],packs:index===0?[definition]:[]},evidence:[{path:paths[2],sha256:'a'.repeat(64)}]}));
const recordFiles=new Map([...addedRecords.map(record=>[recordReference(record).path,record]),...newBatches.map(batch=>[`registry/batches/${batch.id}.json`,batch])]);
const legacyKey=path=>Object.entries(LEGACY_OUTPUTS).find(([,value])=>value===path)?.[0];
const registryInput={...withGallery(newGallery),paths:[...paths,galleryPath,...recordFiles.keys()],
 readBefore:path=>{assert(legacyKey(path),'Unexpected prior metadata read');return legacyBefore[legacyKey(path)];},
 readAfter:path=>recordFiles.has(path)?recordFiles.get(path):legacyAfter[legacyKey(path)],
 registryState:{beforePaths:['registry/baseline.json'],readAfterBytes:path=>Buffer.from(encode(recordFiles.get(path)))}};
const registryGood=assessIncrementalDiff(registryInput);assert.equal(registryGood.eligible,true,registryGood.reasons.join('; '));assert.deepEqual(registryGood.added_ids,good.added_ids);
const rejectRegistry=(edit,label)=>{const input={...registryInput,paths:[...registryInput.paths],registryState:{...registryInput.registryState,beforePaths:[...registryInput.registryState.beforePaths]}};edit(input);assert.equal(assessIncrementalDiff(input).eligible,false,label);};
rejectRegistry(input=>input.registryState=null,'Registry data cannot self-authorize without exact prior inventory');
rejectRegistry(input=>input.paths.push('registry/baseline.json'),'Historical registry baseline remains shared');
rejectRegistry(input=>input.registryState.beforePaths.push([...recordFiles.keys()][0]),'Existing immutable record modification is not an addition');
rejectRegistry(input=>input.registryState.beforePaths.push('registry/batches/independent-0.json'),'Existing batch modification is not an addition');
rejectRegistry(input=>input.paths.push('registry/models/incremental-model-1/run.js'),'Executable cannot hide in a model namespace');
rejectRegistry(input=>input.paths=input.paths.filter(path=>path!==[...recordFiles.keys()][0]),'Missing per-model record cannot grant incremental reuse');
rejectRegistry(input=>input.registryState.readAfterBytes=path=>Buffer.from(encode({...recordFiles.get(path),forged:true})),'Changed record bytes invalidate their content-addressed path');
rejectRegistry(input=>input.readAfter=path=>path==='registry/batches/independent-0.json'?{...recordFiles.get(path),accept:true}:registryInput.readAfter(path),'Batch cannot grant itself approval');
rejectRegistry(input=>input.readAfter=path=>path==='registry/batches/independent-1.json'?{...recordFiles.get(path),records:newBatches[0].records}:registryInput.readAfter(path),'Duplicate cross-batch model ownership is refused');
console.log('Registry append scope: two independent batches select exactly four new IDs; historical, unbound, malformed and executable registry changes stay full.');
assert.deepEqual(tasksForModelPlan(['models-1-of-5','models-2-of-5','handoff'],{fresh_ids:good.added_ids},after),['models-1-of-4','models-2-of-4','models-3-of-4','models-4-of-4','previews','handoff']);assert.deepEqual(tasksForModelPlan(['models-1-of-5','previews','handoff'],{fresh_ids:[]},after),['handoff']);
console.log('Incremental eligibility: exact owned additions, old-record preservation, explicit known publication role; unknown code/renderer/golden changes require full.');

// Root and authenticated-proof source are separate from the PR comparison base.
// This uses normal full-byte APIs, not a fabricated archive shortcut capability.
const history=fixture(1);
try{
 const git=(...args)=>execFileSync('git',args,{cwd:history.root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
 const commit=message=>{git('add','.');git('commit','-qm',message);return git('rev-parse','HEAD');};
 const addOwned=()=>{
  history.add(1);const asset=history.manifest.assets.at(-1),id=`owned-${asset.id}`;
  history.catalog.packs[0].asset_ids.pop();asset.packs=[id];
  history.catalog.packs.push({id,name:{en:id,zh:id},description:{en:'Fixture',zh:'测试'},asset_ids:[asset.id]});
  history.put('assets/manifest.json',history.manifest);history.put('site/catalog-data.json',history.catalog);
 };
 git('init','-q');git('config','user.name','Incremental source fixture');git('config','user.email','fixture@example.invalid');
 const proofSource=commit('Successful proof source');
 history.put('README.md','Comparison base may be newer than the successful proof.\n');const comparisonBase=commit('Documentation comparison base');
 addOwned();commit('One owned model addition');
 const scoped=eligibilityFromGit(comparisonBase,{root:history.root,sourceCommit:proofSource});
 assert.equal(scoped.eligible,true,scoped.reasons.join('; '));assert.deepEqual(scoped.added_ids,['model-002']);
 assert(scoped.reasons.some(reason=>reason.includes(proofSource)&&reason.includes(comparisonBase)),'Explain the distinct authenticated ancestor and comparison base');
 assert.equal(eligibilityFromGit(comparisonBase,{root:history.root,sourceContext:{},sourceCommit:proofSource}).eligible,false,'Ordinary JSON cannot authorize an archive source');
 history.put('site/viewer.js','export const syntheticViewer = "changed";\n');const rendererBase=commit('Renderer changed after old proof');
 addOwned();commit('Another owned model addition');
 assert.equal(eligibilityFromGit(rendererBase,{root:history.root}).eligible,true,'The immediate comparison diff alone is append-only');
 assert.equal(eligibilityFromGit(rendererBase,{root:history.root,sourceCommit:proofSource}).eligible,false,'Older proof comparison must include intervening protected changes');
}finally{history.close();}

// Real orchestrator, synthetic evidence: a valid GPU/card baseline cannot bypass
// missing or incompatible browser coverage. No browser execution is claimed.
const f=fixture(before.assets.length);
try{
 const oldInputs=computeModelInputs({root:f.root});oldInputs.render_inputs='verified-built-render-v1';oldInputs.built_payload_sha256='e'.repeat(64);
 const oldIDs=before.assets.map(row=>row.id).sort();oldInputs.models.forEach((row,index)=>{row.id=oldIDs[index];});
 const first=planModelReuse({inputs:oldInputs}),id=fixtureIdentity(),proof=finishModelFixture(oldInputs,first,id);
 const inputs=clone(oldInputs);for(const asset of after.assets.filter(row=>!oldIDs.includes(row.id))){const row=clone(inputs.models[0]);row.id=asset.id;row.input_key=asset.id.charCodeAt(asset.id.length-1).toString(16).padStart(2,'0').repeat(32);inputs.models.push(row);}inputs.models.sort((a,b)=>a.id.localeCompare(b.id));
 const options={inputs,manifest:after,eligibility:good,requestedTasks:['models']};
 const unavailable=acceptanceExecutionPlan({...options,eligibility:{eligible:false}});
 const laterEligible=acceptanceExecutionPlan(options);
 assert.deepEqual(laterEligible.browser_plan,unavailable.browser_plan,'Full fresh coverage remains identical if an archive baseline becomes available during execution');
 assert.deepEqual(laterEligible.tasks,unavailable.tasks);
 const testFull=(base,label)=>{const verifiedBaseProof=verification(base);assert.equal(planModelReuse({inputs,baseProof:base,verifiedBaseProof}).reused_ids.length,before.assets.length,'GPU/card proof is independently compatible in this fixture');const result=acceptanceExecutionPlan({...options,baseProof:base,verifiedBaseProof});assert.deepEqual(result.reused_ids,[],label);assert.equal(result.fresh_ids.length,after.assets.length,label);assert.equal(result.browser_plan.mode,'full');assert.deepEqual(result.browser_plan.fresh_pack_tasks,HISTORICAL_BROWSER_PACKS.map(row=>row.task));};
 testFull(proof,'Missing browser coverage forces every catalog model fresh');
 const fullBrowser=planBrowserTasks({inputs:oldInputs,manifest:before,modelPlan:first,eligibility:{eligible:false},requestedTasks:['models']});
 const fullTasks=tasksForModelPlan(fullBrowser.tasks,first,before),origin={source_commit:id.source_commit,source_tree:id.source_tree,run_id:Number(id.run_id),run_attempt:Number(id.run_attempt),payload_sha256:proof.payload_sha256};
 proof.browser_task_coverage=aggregateBrowserCoverage({inputs:oldInputs,modelPlan:first,browserPlan:fullBrowser,freshModelRecords:oldInputs.models.map(row=>({id:row.id,input_key:row.input_key,status:'pass',viewports:['desktop','touch'],report_sha256:'e'.repeat(64),origin})),identity:id,payload_sha256:proof.payload_sha256,executedTasks:fullTasks,expectedTasks:fullTasks});assertBrowserCoverage(proof);
 const valid=acceptanceExecutionPlan({...options,baseProof:proof,verifiedBaseProof:verification(proof)});assert.equal(valid.reused_ids.length,before.assets.length);assert.deepEqual(valid.fresh_ids,good.added_ids);assert.equal(valid.browser_plan.mode,'append');
 const registryPlan=acceptanceExecutionPlan({...options,eligibility:registryGood,baseProof:proof,verifiedBaseProof:verification(proof)});assert.equal(registryPlan.reused_ids.length,before.assets.length);assert.deepEqual(registryPlan.fresh_ids,registryGood.added_ids);assert.equal(registryPlan.browser_plan.mode,'append','Registry files alone do not force full model work with an independently compatible baseline');
 const changedBuiltInputs=clone(inputs);for(const row of changedBuiltInputs.models)row.input_key='9'.repeat(64);const allChanged=acceptanceExecutionPlan({...options,inputs:changedBuiltInputs,baseProof:proof,verifiedBaseProof:verification(proof)});assert.equal(allChanged.verified_base_proof,null,'Full fallback must discard baseline authority even when every model key is already fresh');assert.equal(allChanged.fresh_ids.length,after.assets.length);
 const incomplete=clone(proof);incomplete.browser_task_coverage.models.pop();testFull(incomplete,'Incomplete browser coverage forces every catalog model fresh');
 const incompatible=clone(proof);incompatible.browser_task_coverage.policy_sha256='f'.repeat(64);testFull(incompatible,'Incompatible browser policy forces every catalog model fresh');
 console.log(`Acceptance orchestrator: compatible baseline for ${before.assets.length} models plus missing/incompatible browser coverage forces ${after.assets.length} fresh; complete coverage including registry metadata selects exactly ${good.added_ids.length} fresh.`);
}finally{f.close();}

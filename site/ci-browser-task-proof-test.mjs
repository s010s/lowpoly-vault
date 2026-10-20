/** Synthetic task/provenance fixtures, never claims of actual browser execution. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {HISTORICAL_BROWSER_PACKS,FULL_SHARED_TASKS,COMPACT_SHARED_TASKS,browserProofHash,planBrowserTasks,aggregateBrowserCoverage,assertBrowserCoverage} from './ci-browser-task-proof.mjs';
const clone=value=>structuredClone(value),hash=value=>browserProofHash(value);
const original=JSON.parse(readFileSync('assets/manifest.json'));
const makeInputs=manifest=>({policy_sha256:'a'.repeat(64),runtime_config:{node_major:'22'},gpu_policy:{browser:{chromium:'141.0.7390.37'}},render_inputs:'verified-built-render-v1',models:manifest.assets.map(asset=>({id:asset.id,input_key:hash(asset)})).sort((a,b)=>a.id.localeCompare(b.id))});
const identity=n=>({source_commit:String(n).repeat(40),source_tree:'b'.repeat(40),run_id:100+n,run_attempt:1,payload_sha256:'c'.repeat(64)});
const verified=proof=>({schema:2,source_commit:proof.source_commit,run_id:proof.run_id,run_attempt:proof.run_attempt,artifact_id:500+proof.run_id,artifact_sha256:`sha256:${'d'.repeat(64)}`,proof_sha256:hash(proof)});
const execution=(plan,browser)=>{const count=Math.min(5,plan.fresh_ids.length);return [...Array.from({length:count},(_,i)=>`models-${i+1}-of-${count}`),...(count?['previews']:[]),...browser.tasks];};
function modelPlan(inputs,base){const prior=new Set(base?.catalog_ids||[]);return {fresh_ids:inputs.models.filter(row=>!prior.has(row.id)).map(row=>row.id),reused_ids:inputs.models.filter(row=>prior.has(row.id)).map(row=>row.id),verified_base_proof:base?verified(base):null};}
function finish(inputs,plan,browser,n,base){
 const id=identity(n),tasks=execution(plan,browser),fresh=plan.fresh_ids.map(key=>({id:key,input_key:inputs.models.find(row=>row.id===key).input_key,status:'pass',viewports:['desktop','touch'],report_sha256:'e'.repeat(64),origin:id}));
 const proof={...id,policy_sha256:inputs.policy_sha256,catalog_ids:inputs.models.map(row=>row.id),fresh_ids:plan.fresh_ids,reused_ids:plan.reused_ids,models:inputs.models.map(row=>({...row,origin:plan.fresh_ids.includes(row.id)?id:base.models.find(model=>model.id===row.id).origin}))};
 proof.browser_task_coverage=aggregateBrowserCoverage({inputs,baseProof:base,modelPlan:plan,browserPlan:browser,freshModelRecords:fresh,identity:id,payload_sha256:id.payload_sha256,executedTasks:tasks,expectedTasks:tasks});assertBrowserCoverage(proof);return proof;
}
const requested=FULL_SHARED_TASKS.concat(HISTORICAL_BROWSER_PACKS.map(row=>row.task),'models','previews');
assert.equal(HISTORICAL_BROWSER_PACKS.length,15);assert.equal(new Set(HISTORICAL_BROWSER_PACKS.flatMap(row=>row.ids)).size,165);assert.equal(HISTORICAL_BROWSER_PACKS.filter(row=>row.scene).reduce((n,row)=>n+row.ids.length,0),96);
for(const row of HISTORICAL_BROWSER_PACKS){assert(Object.isFrozen(row)&&Object.isFrozen(row.ids));assert.deepEqual(original.assets.filter(asset=>asset.packs?.includes(row.pack)).map(asset=>asset.id).sort(),row.ids);}
let manifest=clone(original),inputs=makeInputs(manifest),plan=modelPlan(inputs),browser=planBrowserTasks({inputs,manifest,modelPlan:plan,eligibility:{eligible:true,added_ids:[]},requestedTasks:['models']});
assert.equal(browser.mode,'full');assert.deepEqual(browser.fresh_pack_tasks,HISTORICAL_BROWSER_PACKS.map(row=>row.task),'Missing baseline schedules every historical task even if scope omitted them');
let base=finish(inputs,plan,browser,1);
const add=(manifest,start)=>{const result=clone(manifest);for(let i=start;i<start+4;i++)result.assets.push({...clone(original.assets[0]),id:`new-browser-model-${i}`,packs:[`new-browser-pack-${start}`]});return result;};
for(const [start,n]of [[1,2],[5,3]]){
 manifest=add(manifest,start);inputs=makeInputs(manifest);plan=modelPlan(inputs,base);const eligibility={eligible:true,added_ids:plan.fresh_ids};
 browser=planBrowserTasks({inputs,manifest,modelPlan:plan,baseProof:base,eligibility,requestedTasks:requested});
 assert.equal(browser.mode,'append');assert.equal(plan.fresh_ids.length,4);assert.equal(plan.reused_ids.length,manifest.assets.length-4);assert.deepEqual(browser.fresh_pack_tasks,[]);assert.equal(browser.reused_pack_tasks.length,15);assert.deepEqual(browser.shared_tasks,COMPACT_SHARED_TASKS);assert.equal(browser.folded_shared_tasks.length,7);assert.equal(execution(plan,browser).length,8);
 const rejectPlan=(change,label)=>{const args={inputs:clone(inputs),manifest:clone(manifest),modelPlan:clone(plan),baseProof:clone(base),eligibility:clone(eligibility),requestedTasks:[...requested]};change(args);assert.equal(planBrowserTasks(args).mode,'full',label);};
 rejectPlan(a=>a.baseProof.browser_task_coverage.packs.pop(),'Incomplete pack evidence');rejectPlan(a=>a.baseProof.browser_task_coverage.models.pop(),'Incomplete model browser evidence');rejectPlan(a=>a.baseProof.browser_task_coverage.models[0].status='fail','Forged old evidence');
 rejectPlan(a=>a.inputs.policy_sha256='f'.repeat(64),'UI/harness changed after prior additions');rejectPlan(a=>a.inputs.models[0].input_key='f'.repeat(64),'Old actual bytes changed');rejectPlan(a=>a.eligibility.eligible=false,'Unknown code/diff');rejectPlan(a=>a.modelPlan.reused_ids.pop(),'Not all old models reusable');rejectPlan(a=>a.eligibility.added_ids.pop(),'Missing newly added ID');rejectPlan(a=>a.inputs.render_inputs='source-only','Source claims are not built proof');
 rejectPlan(a=>a.manifest.assets.at(-1).packs=[HISTORICAL_BROWSER_PACKS[0].pack],'Changed historical membership');
 const good=finish(inputs,plan,browser,n,base),coverage=good.browser_task_coverage;
 for(const mutate of [p=>p.browser_task_coverage.models[0].origin.source_commit='f'.repeat(40),p=>p.browser_task_coverage.models[0].reused_from.source_commit='f'.repeat(40),p=>p.browser_task_coverage.packs[0].reused_from.run_id++,p=>p.browser_task_coverage.executed_tasks.pop(),p=>p.browser_task_coverage.executed_tasks.push('unknown'),p=>p.browser_task_coverage.executed_tasks.push(p.browser_task_coverage.executed_tasks[0]),p=>p.browser_task_coverage.fresh_pack_tasks.push('small-life'),p=>p.browser_task_coverage.models.find(row=>row.evidence==='fresh').origin.payload_sha256='f'.repeat(64)]){const bad=clone(good);mutate(bad);assert.throws(()=>assertBrowserCoverage(bad));}
 const id=identity(n),tasks=execution(plan,browser),fresh=coverage.models.filter(row=>row.evidence==='fresh');
 for(const executedTasks of [tasks.slice(1),[...tasks,'unknown'],[...tasks,tasks[0]]])assert.throws(()=>aggregateBrowserCoverage({inputs,baseProof:base,modelPlan:plan,browserPlan:browser,freshModelRecords:fresh,identity:id,payload_sha256:id.payload_sha256,executedTasks,expectedTasks:tasks}));
 for(const edit of [rows=>rows.pop(),rows=>rows.push(clone(rows[0])),rows=>rows[0].origin.run_id++,rows=>rows[0].viewports.pop()]){const rows=clone(fresh);edit(rows);assert.throws(()=>aggregateBrowserCoverage({inputs,baseProof:base,modelPlan:plan,browserPlan:browser,freshModelRecords:rows,identity:id,payload_sha256:id.payload_sha256,executedTasks:tasks,expectedTasks:tasks}));}
 base=good;
}
assert.equal(base.catalog_ids.length,original.assets.length+8);assert.equal(base.browser_task_coverage.models.filter(row=>row.evidence==='reused').length,original.assets.length+4);
const changed=clone(inputs);changed.policy_sha256='9'.repeat(64);const changedPlan={fresh_ids:changed.models.map(row=>row.id),reused_ids:[],verified_base_proof:null};assert.equal(planBrowserTasks({inputs:changed,manifest,modelPlan:changedPlan,eligibility:{eligible:false,added_ids:[]},requestedTasks:requested}).mode,'full');
// The compact wheel route executes the same group union, not old pack loops.
const source=path=>readFileSync(path,'utf8');
assert(source('site/small-life-browser-test.mjs').includes("from './ci-browser-task-proof.mjs'"));assert(!/from ['"].*release\.mjs['"]/.test(source('site/small-life-browser-test.mjs')));
assert(source('site/redesign-browser-test.mjs').includes("['routes','interaction','scroll','scale','modal','fallback']"));
const wheelGroups=path=>{const match=source(path).match(/runGalleryBrowserTests\(\{groups:\[([^\]]+)\]/);assert(match,`Explicit wheel groups missing: ${path}`);return [...match[1].matchAll(/['"]([^'"]+)['"]/g)].map(row=>row[1]).sort();};
const shared=wheelGroups('site/shared-model-browser-test.mjs');assert.deepEqual(shared,['detail','handoff','resources']);
const conifer=wheelGroups('qa/conifer-doc1-integration/conifer-handoff-browser-test.mjs');assert.deepEqual(conifer,shared);
const compactUnion=new Set(['routes','interaction','scroll','scale','modal','fallback',...shared,...conifer]);
for(const [path,expected]of Object.entries({
 'site/image-scrub-browser-test.mjs':['interaction','handoff','scroll'],
 'site/handoff-browser-test.mjs':['handoff','detail'],
 'site/modal-motion-browser-test.mjs':['modal','detail','handoff'],
 'site/interaction-motion-browser-test.mjs':['interaction','detail'],
 'site/catalog-scroll-browser-test.mjs':['scroll','detail'],
 'site/hover-reveal-browser-test.mjs':['resources','handoff'],
})){const groups=wheelGroups(path);assert.deepEqual(groups,expected.sort(),`Folded wrapper changed: ${path}`);for(const group of groups)assert(compactUnion.has(group),`Folded group is not retained: ${group}`);}
assert(source('site/redesign-browser-test.mjs').includes("forceFallback?['fallback']"),'Dedicated fallback behavior remains within matrix group union');
assert(source('qa/conifer-doc1-integration/conifer-handoff-browser-test.mjs').includes("modelId:'conifer-tree'"));
console.log('Browser task proof: exact15 historical tasks/165 models,190→194→198 desktop/touch lineage, full fallback, pack/old byte/harness mutation, forged/missing proof and exact matrix partition negatives passed.');

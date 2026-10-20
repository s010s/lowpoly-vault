/** Protected historical task inventory. This grants no asset publication authority. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
export const HISTORICAL_BROWSER_PACKS=Object.freeze([
  {
    "task": "small-life",
    "pack": "prehistoric-small-life",
    "ids": [
      "asteroxylon",
      "bothriolepis",
      "confuciusornis",
      "ichthyornis",
      "juracimbrophlebia",
      "waptia"
    ],
    "scene": false
  },
  {
    "task": "fauna",
    "pack": "prehistoric-small-fauna",
    "ids": [
      "burgessomedusa",
      "diplomystus",
      "kalligramma"
    ],
    "scene": false
  },
  {
    "task": "batch",
    "pack": "prehistoric-small-life-20261018",
    "ids": [
      "aglaophyton",
      "alienopterus",
      "archaeocidaris",
      "archaeopteryx",
      "canadaspis",
      "cephalaspis",
      "ceratomyrmex",
      "hydropteris",
      "longipteryx",
      "onoclea",
      "saccocoma",
      "urasterella"
    ],
    "scene": false
  },
  {
    "task": "round02",
    "pack": "prehistoric-small-life-round02-20261018",
    "ids": [
      "aulopora",
      "calceola",
      "choia",
      "favosites",
      "fenestella",
      "goniophyllum",
      "hallucigenia",
      "halysites",
      "marrella",
      "opabinia",
      "proteroctopus",
      "thamnopora"
    ],
    "scene": false
  },
  {
    "task": "round03",
    "pack": "prehistoric-small-life-round03-20261018",
    "ids": [
      "bosworthia",
      "buthograptus",
      "halimeda",
      "haplophrentis",
      "heliophyllum",
      "isoxys",
      "leptomitus",
      "meandrina",
      "pirania",
      "syringopora",
      "thecosmilia",
      "vauxia"
    ],
    "scene": false
  },
  {
    "task": "round04",
    "pack": "prehistoric-small-life-round04-20261018",
    "ids": [
      "coquina-outcrop",
      "cystiphyllum",
      "desiccation-crack-surface",
      "flabellum",
      "gogia",
      "horneophyton",
      "limnobiophyllum",
      "micrabacia",
      "naraoia",
      "sengelia",
      "wave-ripple-surface",
      "wielandiella"
    ],
    "scene": false
  },
  {
    "task": "round05",
    "pack": "prehistoric-small-life-round05-20261018",
    "ids": [
      "acrocyathus",
      "aysheaia",
      "beelzebufo",
      "cobbania",
      "leanchoilia",
      "montlivaltia",
      "paratingia",
      "pluricarpellatia",
      "sawdonia",
      "septarian-concretion",
      "stromatolite-mound",
      "tafoni-outcrop"
    ],
    "scene": false
  },
  {
    "task": "round06",
    "pack": "prehistoric-small-life-round06-20261018",
    "ids": [
      "araucaria-mirabilis",
      "flint-nodule",
      "gypsum-desert-rose",
      "isastraea",
      "matonidium",
      "odontogriphus",
      "onychonycteris",
      "pillow-lava-outcrop",
      "pleurodictyum",
      "spinolestes",
      "trapa",
      "yohoia"
    ],
    "scene": true
  },
  {
    "task": "round07",
    "pack": "prehistoric-small-life-round07-20261018",
    "ids": [
      "bedrock-pothole",
      "cambroraster",
      "canadia",
      "coelurosauravus",
      "columnar-jointed-outcrop",
      "cooksonia",
      "dollocaris",
      "leclercqia",
      "load-cast-bedding",
      "montsechia",
      "quartz-prism-cluster",
      "salvinia"
    ],
    "scene": true
  },
  {
    "task": "round08",
    "pack": "prehistoric-small-life-round08-20261018",
    "ids": [
      "conglomerate-outcrop",
      "ctenorhabdotus",
      "florissantia",
      "halkieria",
      "metasequoia",
      "nordenskioldia",
      "ovatiovermis",
      "pahoehoe-lava-surface",
      "stanleycaris",
      "staurolite-cross-twin",
      "waterfall-ledge",
      "williamsonia"
    ],
    "scene": true
  },
  {
    "task": "round09",
    "pack": "prehistoric-small-life-round09-20261018",
    "ids": [
      "anomalocaris",
      "arenicolites-u-burrow",
      "clypeina",
      "echinochiton",
      "eocladus",
      "hydrothermal-chimney",
      "jimaodanus",
      "limestone-pavement",
      "ottoia",
      "sollasina",
      "thalassinoides-branching-burrow",
      "tidal-flat"
    ],
    "scene": true
  },
  {
    "task": "round10",
    "pack": "prehistoric-small-life-round10-20261018",
    "ids": [
      "azolla",
      "capinatator",
      "cothurnocystis",
      "fulgurite-tube",
      "hurdia",
      "marsilea",
      "odaraia",
      "pachypteris",
      "peltaspermum",
      "pyrite-cube-cluster",
      "sand-spit",
      "sea-stack"
    ],
    "scene": true
  },
  {
    "task": "round11",
    "pack": "prehistoric-small-life-round11-20261018",
    "ids": [
      "asaphus",
      "baculites",
      "cross-bedded-sandstone",
      "cruziana-crawling-furrow",
      "ctenocystis",
      "estuary-basin",
      "flute-cast-slab",
      "hazelia",
      "mucrospirifer",
      "paleodictyon-mesh-trace",
      "sea-cave",
      "wave-cut-platform"
    ],
    "scene": true
  },
  {
    "task": "round12",
    "pack": "prehistoric-small-life-round12-20261018",
    "ids": [
      "asteriacites-resting-impression",
      "cave-drapery",
      "cooperoceras",
      "folded-strata-outcrop",
      "gryphaea",
      "helicocystis",
      "reticulite-clast",
      "river-dominated-delta",
      "sabalites",
      "takakkawia",
      "teredolites-wood-boring-cast",
      "volcanic-bomb"
    ],
    "scene": true
  },
  {
    "task": "round13",
    "pack": "prehistoric-small-life-round13-20261018",
    "ids": [
      "aa-lava-front",
      "angular-unconformity-outcrop",
      "clavagella",
      "diplomoceras",
      "entobia-sponge-boring-network",
      "marine-terrace",
      "native-copper-dendrite",
      "nelumbo",
      "nereites-lobed-meander",
      "pentremites",
      "schizoneura",
      "tombolo"
    ],
    "scene": true
  }
].map(row=>Object.freeze({...row,ids:Object.freeze(row.ids)})));
export const FULL_SHARED_TASKS=Object.freeze(['matrix','fallback','list','shared','handoff','conifer','modal','interaction','scroll','hover']);
export const COMPACT_SHARED_TASKS=Object.freeze(['matrix','shared','conifer']);
const HASH=/^[a-f0-9]{64}$/,SHA=/^[a-f0-9]{40}$/;
const canonical=value=>Array.isArray(value)?value.map(canonical):value&&typeof value==='object'?Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])])):value;
export const browserProofHash=value=>createHash('sha256').update(JSON.stringify(canonical(value))).digest('hex');
const sorted=value=>[...value].sort();
function exactIDs(actual,expected,label){assert(Array.isArray(actual),label);assert.equal(new Set(actual).size,actual.length,`${label}: duplicate`);assert.deepEqual(sorted(actual),sorted(expected),label);}
const origin=id=>({source_commit:id.source_commit,source_tree:id.source_tree,run_id:Number(id.run_id),run_attempt:Number(id.run_attempt),payload_sha256:id.payload_sha256});
function assertOrigin(value){assert(SHA.test(value?.source_commit||''));assert(SHA.test(value?.source_tree||''));assert(Number.isSafeInteger(value?.run_id)&&value.run_id>0);assert(Number.isSafeInteger(value?.run_attempt)&&value.run_attempt>0);assert(HASH.test(value?.payload_sha256||''));}
export function historicalBrowserInputs({inputs,manifest}){
 const byID=new Map(inputs.models.map(model=>[model.id,model]));
 exactIDs([...byID.keys()],manifest.assets.map(asset=>asset.id),'Browser inputs cover exact catalog');
 return HISTORICAL_BROWSER_PACKS.map(({task,pack,ids,scene})=>{
  const currentIDs=manifest.assets.filter(asset=>asset.packs?.includes(pack)).map(asset=>asset.id).sort();
  const membership_valid=JSON.stringify(currentIDs)===JSON.stringify(ids);
  const members=currentIDs.map(id=>{const model=byID.get(id);assert(model,`Missing historical model ${id}`);assert(HASH.test(model.input_key));return {id,input_key:model.input_key};});
  return {task,pack,ids:currentIDs,membership_valid,scene,input_key:browserProofHash({version:1,policy_sha256:inputs.policy_sha256,runtime_config:inputs.runtime_config,browser:inputs.gpu_policy.browser,task,pack,members,scene})};
 });
}
export function assertBrowserCoverage(proof){
 const coverage=proof?.browser_task_coverage;assert.equal(coverage?.version,1,'Missing browser task coverage baseline');assert.equal(coverage.status,'pass');
 assert.equal(coverage.policy_sha256,proof.policy_sha256);assert.deepEqual(coverage.origin,origin(proof));assertOrigin(coverage.origin);
 exactIDs(coverage.models?.map(row=>row.id),proof.catalog_ids,'Baseline desktop/touch coverage');
 exactIDs(coverage.packs?.map(row=>row.task),HISTORICAL_BROWSER_PACKS.map(row=>row.task),'Baseline historical task coverage');
 for(const row of [...coverage.models,...coverage.packs]){assert.equal(row.status,'pass');assert(HASH.test(row.input_key||''));assertOrigin(row.origin);assert(['fresh','reused'].includes(row.evidence));}
 const expectedShared=coverage.mode==='append'?COMPACT_SHARED_TASKS:FULL_SHARED_TASKS;assert(['append','full'].includes(coverage.mode));
 if(coverage.mode==='full'){assert.deepEqual(proof.reused_ids,[],'Full browser fallback must revalidate every model');assert.equal(coverage.baseline,null,'Full browser fallback cannot carry a baseline');}
 exactIDs(coverage.shared_tasks,expectedShared,'Baseline shared task coverage');
 exactIDs(coverage.folded_shared_tasks,FULL_SHARED_TASKS.filter(task=>!expectedShared.includes(task)),'Baseline folded shared tasks');
 exactIDs(coverage.fresh_pack_tasks,coverage.mode==='full'?HISTORICAL_BROWSER_PACKS.map(row=>row.task):[],'Baseline fresh pack task coverage');
 exactIDs(coverage.reused_pack_tasks,coverage.mode==='append'?HISTORICAL_BROWSER_PACKS.map(row=>row.task):[],'Baseline reused pack task coverage');
 exactIDs(coverage.models.filter(row=>row.evidence==='fresh').map(row=>row.id),proof.fresh_ids,'Fresh browser model partition');
 exactIDs(coverage.models.filter(row=>row.evidence==='reused').map(row=>row.id),proof.reused_ids,'Reused browser model partition');
 exactIDs(coverage.packs.filter(row=>row.evidence==='fresh').map(row=>row.task),coverage.fresh_pack_tasks,'Fresh pack partition');
 exactIDs(coverage.packs.filter(row=>row.evidence==='reused').map(row=>row.task),coverage.reused_pack_tasks,'Reused pack partition');
 const count=Math.min(5,proof.fresh_ids.length),modelTasks=Array.from({length:count},(_,index)=>`models-${index+1}-of-${count}`);
 exactIDs(coverage.executed_tasks,[...modelTasks,...(count?['previews']:[]),...coverage.shared_tasks,...coverage.fresh_pack_tasks],'Baseline executed matrix coverage');
 for(const row of [...coverage.models,...coverage.packs]){
  if(row.evidence==='fresh'){assert.deepEqual(row.origin,coverage.origin,'Fresh browser origin differs');assert.equal(row.reused_from,undefined);}
  else {assertOrigin(coverage.baseline?.origin);assert.deepEqual(row.reused_from,coverage.baseline.origin,'Reused browser lineage differs');assert(HASH.test(coverage.baseline.proof_sha256||''));assert(/^sha256:[a-f0-9]{64}$/.test(coverage.baseline.artifact_sha256||''));assert(Number.isSafeInteger(coverage.baseline.artifact_id)&&coverage.baseline.artifact_id>0);assert.notDeepEqual(coverage.baseline.origin,coverage.origin,'A proof cannot reuse itself');}
 }
 for(const row of coverage.packs){const group=HISTORICAL_BROWSER_PACKS.find(item=>item.task===row.task);for(const id of group.ids)assert.deepEqual(row.origin,origin(proof.models.find(model=>model.id===id)?.origin||{}),'Pack browser origin differs from matching model evidence');}
 for(const row of coverage.models){assert.deepEqual(row.origin,origin(proof.models.find(model=>model.id===row.id)?.origin||{}),'Browser origin differs from matching GPU/card evidence');assert(HASH.test(row.report_sha256||''));assert.deepEqual(row.viewports,['desktop','touch']);assert.equal(row.input_key,proof.models.find(model=>model.id===row.id)?.input_key,'Browser model input differs from GPU/card input');}
 return coverage;
}
/** An authenticated main proof is supplied only by the independent cache lookup. */
export function planBrowserTasks({inputs,manifest,modelPlan,baseProof=null,eligibility,requestedTasks=[]}){
 const packInputs=historicalBrowserInputs({inputs,manifest});
 const known=new Set([...FULL_SHARED_TASKS,...packInputs.map(row=>row.task),'models','previews']);
 assert.equal(new Set(requestedTasks).size,requestedTasks.length,'Duplicate requested task');
 for(const task of requestedTasks)assert(known.has(task)||/^models-[1-5]-of-[1-5]$/.test(task),`Unknown requested browser task: ${task}`);
 let reusable=false,reason='Full browser acceptance is required';
 try{
  assert(eligibility?.eligible,'Diff is not a verified append');assert.equal(inputs.render_inputs,'verified-built-render-v1','Browser reuse needs independently verified built inputs');assert(packInputs.every(row=>row.membership_valid),'Frozen historical pack membership changed');assert(baseProof&&modelPlan.verified_base_proof,'Missing authenticated main proof');
  assert.equal(modelPlan.verified_base_proof.proof_sha256,browserProofHash(baseProof),'Browser baseline proof was modified');
  assert.equal(baseProof.policy_sha256,inputs.policy_sha256,'Browser harness/UI policy changed');
  exactIDs(modelPlan.reused_ids,baseProof.catalog_ids,'Every previous model must have unchanged verified input');
  exactIDs(modelPlan.fresh_ids,eligibility.added_ids,'Fresh browser IDs must be exactly the additions');
  const coverage=assertBrowserCoverage(baseProof);
  for(const row of packInputs)assert.equal(coverage.packs.find(prior=>prior.task===row.task)?.input_key,row.input_key,`Historical browser inputs changed: ${row.task}`);
  for(const row of coverage.models)assert.equal(inputs.models.find(model=>model.id===row.id)?.input_key,row.input_key,`Old browser input changed: ${row.id}`);
  reusable=true;reason='Authenticated complete browser baseline; old pack bytes and membership unchanged';
 }catch(error){reason=error.message;}
 const fresh_pack_tasks=reusable?[]:packInputs.map(row=>row.task),reused_pack_tasks=reusable?packInputs.map(row=>row.task):[];
 return {version:1,mode:reusable?'append':'full',requires_full_models:!reusable,reason,pack_inputs:packInputs,
  fresh_pack_tasks,reused_pack_tasks,shared_tasks:reusable?[...COMPACT_SHARED_TASKS]:[...FULL_SHARED_TASKS],
  folded_shared_tasks:reusable?FULL_SHARED_TASKS.filter(task=>!COMPACT_SHARED_TASKS.includes(task)):[],
  tasks:[...(reusable?COMPACT_SHARED_TASKS:FULL_SHARED_TASKS),...fresh_pack_tasks]};
}
/** Aggregate receives independently checked report records, not candidate claims. */
export function aggregateBrowserCoverage({inputs,baseProof,modelPlan,browserPlan,freshModelRecords,identity,payload_sha256,executedTasks,expectedTasks}){
 exactIDs(executedTasks,expectedTasks,'Actual matrix must execute the exact planned task set');
 for(const task of [...browserPlan.shared_tasks,...browserPlan.fresh_pack_tasks])assert(executedTasks.includes(task),`Missing mandatory browser task: ${task}`);
 exactIDs([...browserPlan.fresh_pack_tasks,...browserPlan.reused_pack_tasks],HISTORICAL_BROWSER_PACKS.map(row=>row.task),'Historical task partition');
 exactIDs([...browserPlan.shared_tasks,...browserPlan.folded_shared_tasks],FULL_SHARED_TASKS,'Shared group task partition');
 exactIDs(freshModelRecords.map(row=>row.id),modelPlan.fresh_ids,'Exact fresh desktop/touch coverage');
 const currentOrigin=origin({...identity,payload_sha256});assertOrigin(currentOrigin);
 const baseline=modelPlan.reused_ids.length?assertBrowserCoverage(baseProof):null;
 const models=inputs.models.map(input=>{
  const fresh=modelPlan.fresh_ids.includes(input.id),row=fresh?freshModelRecords.find(record=>record.id===input.id):baseline.models.find(record=>record.id===input.id);
  assert(row,'Missing browser model evidence');assert.equal(row.input_key,input.input_key);assert.equal(row.status,'pass');assert.deepEqual(row.viewports,['desktop','touch']);assert(HASH.test(row.report_sha256||''));assertOrigin(row.origin);
  if(fresh)assert.deepEqual(row.origin,currentOrigin,'Fresh browser tested a different source/run/build');
  return {...row,evidence:fresh?'fresh':'reused',...(!fresh?{reused_from:origin(baseProof)}:{})};
 });
 const packs=browserPlan.pack_inputs.map(input=>{
  assert(input.membership_valid,'Cannot mint changed historical membership coverage');
  const fresh=browserPlan.fresh_pack_tasks.includes(input.task),row=fresh?{task:input.task,input_key:input.input_key,status:'pass',origin:currentOrigin}:baseline.packs.find(record=>record.task===input.task);
  assert.equal(row?.input_key,input.input_key,'Historical task evidence differs');assertOrigin(row.origin);
  return {...row,evidence:fresh?'fresh':'reused',...(!fresh?{reused_from:origin(baseProof)}:{})};
 });
 return {version:1,status:'pass',mode:browserPlan.mode,policy_sha256:inputs.policy_sha256,origin:currentOrigin,models,packs,
  baseline:baseline?{origin:origin(baseProof),proof_sha256:modelPlan.verified_base_proof.proof_sha256,artifact_id:modelPlan.verified_base_proof.artifact_id,artifact_sha256:modelPlan.verified_base_proof.artifact_sha256}:null,
  executed_tasks:sorted(executedTasks),fresh_pack_tasks:browserPlan.fresh_pack_tasks,reused_pack_tasks:browserPlan.reused_pack_tasks,
  shared_tasks:browserPlan.shared_tasks,folded_shared_tasks:browserPlan.folded_shared_tasks,
  scope:'Exact desktop/touch functional checks and historical pack/scene coverage; not visual or formal asset approval'};
}

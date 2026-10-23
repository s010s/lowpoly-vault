/** Actual Git fixture coverage of the original-checker optimization. Synthetic graphs are NOT quality acceptance. */
import assert from 'node:assert/strict';
import {mockMainRun} from './test-production-main-run.mjs';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {LEGACY_OUTPUTS,importLegacySnapshot,composeRegistry,recordReference,encode,hashBytes} from './model-registry.mjs';
import {registryFiles} from './model-registry-cli.mjs';
import {productionValidationPlan,inspectProductionRelease} from './production-release.mjs';
const roots=[],sha=b=>createHash('sha256').update(b).digest('hex');let count=0;
async function run(name,edit,expected){
 const root=mkdtempSync(join(tmpdir(),'incremental-chain-'));roots.push(root);
 const git=(...a)=>execFileSync('git',a,{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
 const put=(path,data)=>{const bytes=Buffer.from(typeof data==='string'?data:JSON.stringify(data));mkdirSync(dirname(join(root,path)),{recursive:true});writeFileSync(join(root,path),bytes);return {path,bytes:bytes.length,sha256:sha(bytes)};};
 const make=id=>{
  const prefix=`production/${id}`,base=`assets/additions/${id}/r001`,glb=put(`${base}/${id}.glb`,'glb'),blend=put(`${base}/${id}.blend`,'blend'),preview=put(`${base}/preview.png`,'preview');
  const detail=put(`site/public/gallery/posters/${id}.png`,'detail'),wheel=put(`site/public/gallery/posters/${id}-wheel.png`,'wheel'),render=put(`${prefix}/render.json`,{}),recipe=put(`${prefix}/recipe.json`,{files:[]});
  const asset={id,production_release:`${prefix}/descriptor.json`,glb:glb.path,blend:blend.path,preview:preview.path,sha256:{glb:glb.sha256,blend:blend.sha256,preview:preview.sha256},worlds:['world'],packs:['starter'],collection:'world'};
  const metadata=put(`${prefix}/metadata.json`,asset),record=put(`${prefix}/evidence.json`,{asset_id:id,roles:{finalGLB:glb,finalBlend:blend},build_closure:[],preview,final_posters:{recipe,detail:{...detail,render_config:render},wheel:{...wheel,render_config:render}}}),scope=put(`${prefix}/scope.md`,'scope');put(`${prefix}/review.json`,{status:'PASS'});
  const descriptor=put(`${prefix}/descriptor.json`,{assets:[{id,metadata,evidence:record}],implementation:[],scope_document:scope,review_path:`${prefix}/review.json`});
  const model={version:1,id,asset,catalog:{pack_ids:['starter'],legacy_pack_ids:[]},gallery:{poster:{source_glb_sha256:glb.sha256,detail:detail.path.replace('site/public/',''),wheel:wheel.path.replace('site/public/','')},files:[detail,wheel].map(p=>({...p,path:p.path.replace('site/public/','')})),wheel_framing:null},turntable:{asset:null,poster:null}};
  return {asset,descriptor,model,evidence:{path:record.path,sha256:record.sha256}};
 };
 git('init','-q');git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid');git('config','advice.graftFileDeprecated','false');const old=make('old'),manifest={publication:{production_registry:'production/registry.json'},assets:[old.asset]},registry={schema_version:1,kind:'production-release-set-v1',descriptors:[old.descriptor],asset_ids:['old']};
 const snapshot={manifest,catalog:{version:1,worlds:[{id:'world',name:{en:'World',zh:'世界'}}],packs:[{id:'starter',name:{en:'Starter',zh:'起始'},description:{en:'Original',zh:'原始'},asset_ids:['old']}],legacy_memberships:[]},gallery:{version:1,posters:{old:old.model.gallery.poster},files:old.model.gallery.files},turntables:{version:1,assets:[],posters:[]},framing:{}};
 const sourcePins=Object.fromEntries(Object.entries(LEGACY_OUTPUTS).map(([k,path])=>[k,{path,sha256:hashBytes(encode(snapshot[k]))}]));const models=importLegacySnapshot(snapshot,{sourceCommit:'a'.repeat(40),sourcePins});
 const sync=()=>{for(const [path,value]of registryFiles(models))put(path,encode(value));const projection=composeRegistry(models);for(const [kind,path]of Object.entries(LEGACY_OUTPUTS))put(path,kind==='manifest'?manifest:projection[kind]);put('production/registry.json',registry);};sync();git('add','.');git('commit','-qm','trusted-baseline-fixture');const base=git('rev-parse','HEAD');
 const addBatch=(ids)=>{const ns=ids.map(make);manifest.assets.push(...ns.map(n=>n.asset));registry.descriptors.push(...ns.map(n=>n.descriptor));registry.asset_ids.push(...ids);models.records.push(...ns.map(n=>n.model));models.batches.push({version:1,id:`batch-${ids[0]}`,records:ns.map(n=>recordReference(n.model)),definitions:{packs:[],worlds:[]},evidence:ns.map(n=>n.evidence)});sync();return ns;};
 const opts={root,git,put,make,manifest,registry,base,addBatch,sync,models};await edit(opts);git('add','-A');git('commit','--allow-empty','-qm','candidate');const head=git('rev-parse','HEAD');if(opts.mergeCheckout){const merge=git('commit-tree',git('rev-parse','HEAD^{tree}'),'-p',base,'-p',head,'-m','merge checkout');git('reset','--hard',merge);}
 globalThis.fetch=mockMainRun({base,tree:git('rev-parse',`${base}^{tree}`),mutate:opts.authMutate});process.env.GITHUB_TOKEN='offline-fixture-not-a-secret';
 process.env.GITHUB_EVENT_NAME='pull_request';process.env.GITHUB_REPOSITORY='fixture/repo';process.env.GITHUB_SHA=git('rev-parse','HEAD');let event={pull_request:{base:{ref:'main',sha:base,repo:{full_name:'fixture/repo'}},head:{sha:head,repo:{full_name:'fixture/repo'}}}};
 if(opts.push){process.env.GITHUB_EVENT_NAME='push';process.env.GITHUB_REF='refs/heads/main';event={ref:'refs/heads/main',before:base,after:head,repository:{full_name:'fixture/repo'}};}
 if(opts.eventMutate)opts.eventMutate(event);const eventPath=join(tmpdir(),`incremental-event-${roots.length}-${process.pid}.json`);writeFileSync(eventPath,JSON.stringify(event));process.env.GITHUB_EVENT_PATH=eventPath;
 if(opts.afterCommit)opts.afterCommit();let plan;try{plan=await productionValidationPlan(root);}catch(error){plan={mode:'REJECT',error};}await expected(plan,opts);rmSync(eventPath);console.log('PASS '+name);count++;
}
try{
 await run('pure descriptor append reuses unchanged old closure',o=>o.addBatch(['new']),async(p,o)=>{assert.equal(p.mode,'incremental');assert.deepEqual(p.reusedIds,['old']);assert((await inspectProductionRelease(o.root,'production/old/descriptor.json')).unchanged_baseline);await assert.rejects(inspectProductionRelease(o.root,'production/new/descriptor.json'));});
 await run('normal ten new IDs with registry/catalog/gallery changes reuse only old',o=>o.addBatch(Array.from({length:10},(_,i)=>`new-${i}`)),async(p,o)=>{assert.equal(p.mode,'incremental');assert.deepEqual(p.reusedIds,['old']);for(let i=0;i<10;i++)await assert.rejects(inspectProductionRelease(o.root,`production/new-${i}/descriptor.json`));});
 await run('forged candidate PASS cannot replace successful main run',o=>{o.authMutate=m=>m.get('actions/runs/300').conclusion='failure';o.put('fake-pass.json',{status:'PASS'});},p=>assert.equal(p.mode,'full'));
 await run('wrong explicit registry context rejected before old reuse',()=>{},async(p,o)=>{assert.equal(p.mode,'incremental');await assert.rejects(inspectProductionRelease(o.root,'production/old/descriptor.json','production/wrong.json'),/Different production registry/);});
 await run('exact PR merge checkout binds both parents',o=>{o.addBatch(['new']);o.mergeCheckout=true;},p=>{assert.equal(p.mode,'incremental');assert.deepEqual(p.reusedIds,['old']);assert.notEqual(p.checkout,p.head);});
 await run('main push reuses authenticated unchanged content',o=>{o.push=true;o.addBatch(['new']);},p=>{assert.equal(p.mode,'incremental');assert.deepEqual(p.reusedIds,['old']);});
 await run('wrong push ref cannot reuse',o=>{o.push=true;o.eventMutate=e=>e.ref='refs/heads/other';},p=>assert.equal(p.mode,'full'));
 await run('event environment changes cannot reuse cached scope',()=>{},async(p,o)=>{assert.equal(p.mode,'incremental');process.env.GITHUB_REPOSITORY='changed/repository';await assert.rejects(productionValidationPlan(o.root),/Tracked inputs changed/);});
 await run('event file changes cannot reuse cached scope',()=>{},async(p,o)=>{assert.equal(p.mode,'incremental');writeFileSync(process.env.GITHUB_EVENT_PATH,'{}');await assert.rejects(productionValidationPlan(o.root),/Tracked inputs changed/);});
 await run('caller cannot mutate internal reused IDs',o=>o.addBatch(['new']),async(p,o)=>{p.reusedIds.push('new');assert.deepEqual((await productionValidationPlan(o.root)).reusedIds,['old']);await assert.rejects(inspectProductionRelease(o.root,'production/new/descriptor.json'));});
 await run('owned media change selects old descriptor',o=>o.put('site/public/gallery/posters/old.png','changed'),p=>{assert.equal(p.mode,'incremental');assert.deepEqual(p.reusedIds,[]);});
 await run('owned media deletion never reuses',o=>rmSync(join(o.root,'site/public/gallery/posters/old.png')),p=>assert.deepEqual(p.reusedIds,[]));
 await run('rename to unknown path falls back',o=>o.git('mv','site/public/gallery/posters/old.png','site/public/gallery/posters/renamed.png'),p=>assert.equal(p.mode,'full'));
 await run('shared validator change tests code without reaccepting unchanged model bytes',o=>o.put('site/checker.mjs','changed'),p=>{assert.equal(p.mode,'incremental');assert.deepEqual(p.reusedIds,['old']);});
 await run('code changes cannot authorize historical bridge replacement',o=>{o.put('site/checker.mjs','changed');o.registry.descriptors[0].compatibility=o.put('production/new-bridge.json',{kind:'deliberately-invalid-fixture'});o.sync();},p=>assert.equal(p.mode,'REJECT'));
 await run('bridge refresh alone cannot silently reuse old acceptance',o=>{o.registry.descriptors[0].compatibility=o.put('production/new-bridge.json',{kind:'deliberately-invalid-fixture'});o.sync();},p=>assert.equal(p.mode,'REJECT'));
 await run('unreferenced shared generator change preserves model content scope',o=>o.put('scripts/shared.py','changed'),p=>{assert.equal(p.mode,'incremental');assert.deepEqual(p.reusedIds,['old']);});
 await run('unknown input falls back',o=>o.put('unknown.json',{}),p=>assert.equal(p.mode,'full'));
 await run('forged derived gallery rejected',o=>o.put('site/public/gallery/resources.json',{}),p=>assert.equal(p.mode,'REJECT'));
 await run('duplicate ID rejected by always-on global invariants',o=>{o.manifest.assets.push(o.manifest.assets[0]);o.put('assets/manifest.json',o.manifest);},p=>assert.equal(p.mode,'REJECT'));
 await run('historical manifest fake PASS rejected',o=>{o.manifest.assets[0].status='PASS';o.put('assets/manifest.json',o.manifest);},p=>assert.equal(p.mode,'REJECT'));
 await run('manifest format change retains exact semantic baseline',o=>o.put('assets/manifest.json',JSON.stringify(o.manifest,null,2)),p=>assert.deepEqual(p.reusedIds,['old']));
 await run('missing base falls back',o=>{o.eventMutate=e=>e.pull_request.base.sha='f'.repeat(40);},p=>assert.equal(p.mode,'full'));
 await run('head/checkout mismatch falls back',o=>{o.eventMutate=e=>e.pull_request.head.sha='e'.repeat(40);},p=>assert.equal(p.mode,'full'));
 await run('dirty tracked inputs fall back',o=>{o.afterCommit=()=>o.put('site/public/gallery/posters/old.png','dirty');},p=>assert.equal(p.mode,'full'));
 await run('assume-unchanged cannot hide modified old media',o=>{o.afterCommit=()=>{o.git('update-index','--assume-unchanged','site/public/gallery/posters/old.png');o.put('site/public/gallery/posters/old.png','hidden');};},p=>assert.equal(p.mode,'full'));
 await run('skip-worktree cannot authorize reuse',o=>{o.afterCommit=()=>o.git('update-index','--skip-worktree','site/public/gallery/posters/old.png');},p=>assert.equal(p.mode,'full'));
 await run('fork context conservatively full',o=>{o.eventMutate=e=>e.pull_request.head.repo.full_name='other/repo';},p=>assert.equal(p.mode,'full'));
 const workflow=name=>readFileSync(new URL(`../.github/workflows/${name}.yml`,import.meta.url),'utf8');
 const pages=workflow('pages'),blocks=pages.split('\n      - '),token=/GITHUB_TOKEN: \$\{\{ github.token \}\}/;
 for(const id of ['build'])assert(token.test(blocks.find(b=>b.includes(`id: ${id}\n`))||''),'Production consumer step needs existing read-only token: '+id);
 assert(/fetch-depth: 0/.test(pages));
 const reusable=workflow('publication-regressions');assert(/actions: read/.test(reusable)&&/fetch-depth: 0/.test(reusable)&&token.test(reusable));
 const pipeline=workflow('asset-pipeline');assert(/actions: read/.test(pipeline)&&/fetch-depth: 0/.test(pipeline)&&/ci-lean-regressions.mjs pipeline/.test(pipeline));
 console.log('PASS all production consumer workflow contexts preserve proof access and Git base');count++;
 console.log(`${count} local scope/integration seam cases passed; no real model acceptance or workflow execution.`);
}finally{for(const root of roots)rmSync(root,{recursive:true,force:true});}

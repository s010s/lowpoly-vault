/** Small byte fixtures, not a claim to have rendered the production catalog. */
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync,copyFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,dirname} from 'node:path';
import {pathToFileURL} from 'node:url';
import {computeModelInputs,hashBytes,hashObject,planModelReuse,freshModelRecords,aggregateModelProof,assertBaseModelProof,PINNED_BROWSER,assertBuiltRenderInputs,modelPolicyDigest,PUBLICATION_ONLY_MODULES} from './ci-model-proof.mjs';
import {enrichManifest,creditText} from './asset-delivery.mjs';
import {writeCatalog} from './catalog-build.mjs';
import {writeStaticRoutes} from './static-routes.mjs';
import {collectTurntables,publishedImagePaths} from './turntable-delivery.mjs';
import {CARD_RENDER_PRESET} from './render-preset.js';
import {freshCardPreviewRecords} from './ci-card-preview-proof.mjs';

// Header/dimension fixtures only, deliberately not decodable rendered images.
// These exercise seals and build projection, never production GPU/WebP quality.
function tinyCardBytes(id){
  const marker=Buffer.from(`synthetic card ${id}`),data=Buffer.alloc(38+marker.length+(marker.length%2));
  data.write('RIFF',0);data.writeUInt32LE(data.length-8,4);data.write('WEBP',8);data.write('VP8X',12);data.writeUInt32LE(10,16);
  data.writeUIntLE(CARD_RENDER_PRESET.image.width-1,24,3);data.writeUIntLE(CARD_RENDER_PRESET.image.height-1,27,3);
  data.write('TEST',30);data.writeUInt32LE(marker.length,34);marker.copy(data,38);return data;
}

export function fixture(count=190){
  const root=mkdtempSync(join(tmpdir(),'model-proof-test-'));
  const put=(path,value)=>{mkdirSync(dirname(join(root,path)),{recursive:true});writeFileSync(join(root,path),typeof value==='string'||Buffer.isBuffer(value)?value:JSON.stringify(value));};
  put('site/ci-model-proof.mjs','// protected verifier fixture\n');put('site/redesign-browser-test.mjs','// strict GPU harness fixture\n');
  put('site/ci-card-preview-proof.mjs','// protected separate card proof fixture\n');
  put('site/viewer.js','export const syntheticViewer = true; // no real rendering\n');put('site/render-preset.js',`export const CARD_RENDER_PRESET = Object.freeze(${JSON.stringify(CARD_RENDER_PRESET)});\n`);
  put('site/gallery/renderer.js','export const camera = 42;\n');put('site/style.css','canvas { display:block }\n');put('site/index.html','<!doctype html><body></body>');
  put('.github/workflows/full-release-review.yml','name: Full release review\n');put('qa/conifer-doc1-integration/conifer-handoff-browser-test.mjs','// Executed QA root\n');
  put('package.json',{devDependencies:{playwright:'1.56.1'},dependencies:{three:'0.180.0'}});put('package-lock.json',{lockfileVersion:3,packages:{'node_modules/playwright-core':{version:'1.56.1',integrity:'pinned-package-integrity'}}});
  const manifest={version:1,author:'fixture',assets:[]},catalog={version:1,worlds:[{id:'prehistoric',name:{en:'Prehistoric',zh:'史前'}}],packs:[{id:'starter',name:{en:'Starter',zh:'入门'},description:{en:'Fixture',zh:'测试'},asset_ids:[]}],legacy_memberships:[]},resources={version:1,references:{},posters:{},files:[]},framing={},cards={version:1,render_preset_sha256:hashBytes(JSON.stringify(CARD_RENDER_PRESET)),assets:[],posters:[]};
  const add=number=>{
    for(let index=0;index<number;index++){
      const id=`model-${String(manifest.assets.length+1).padStart(3,'0')}`,paths={glb:`assets/additions/${id}/model.glb`,blend:`assets/additions/${id}/model.blend`,preview:`assets/additions/${id}/preview.webp`},sha256={};
      for(const [kind,path]of Object.entries(paths)){const value=`${kind} fixture bytes for ${id}`;put(path,value);sha256[kind]=hashBytes(value);}
      manifest.assets.push({id,name:{en:id,zh:id},dimensions:[1,2,3],category:'plants',collection:'prehistoric',worlds:['prehistoric'],packs:['starter'],...paths,sha256});catalog.packs[0].asset_ids.push(id);
      const cardPath=publishedImagePaths(manifest.assets.at(-1),manifest).poster,card=tinyCardBytes(id);put(cardPath,card);
      cards.posters.push({id,path:cardPath,sha256:hashBytes(card),bytes:card.length,width:CARD_RENDER_PRESET.image.width,height:CARD_RENDER_PRESET.image.height,source_glb_sha256:sha256.glb,render_preset_sha256:cards.render_preset_sha256});
      const poster={detail:`gallery/posters/${id}.png`,wheel:`gallery/posters/${id}-wheel.png`,source_glb_sha256:sha256.glb,wheelSpec:{azimuth:42}};resources.posters[id]=poster;
      for(const path of [poster.detail,poster.wheel]){const value=`poster bytes for ${path}`;put(`site/public/${path}`,value);resources.files.push({path,sha256:hashBytes(value),bytes:value.length});}
      framing[id]={azimuth:42};
    }
    put('assets/manifest.json',manifest);put('site/catalog-data.json',catalog);put('site/public/gallery/resources.json',resources);put('site/gallery/wheel-framing.json',framing);put('assets/turntables/index.json',cards);
  };
  add(count);
  return {root,put,add,manifest,catalog,resources,framing,cards,close:()=>rmSync(root,{recursive:true,force:true})};
}
export const identity=(commit='a'.repeat(40),run=101)=>({source_commit:commit,source_tree:'b'.repeat(40),control_sha256:'c'.repeat(64),manifest_sha256:'d'.repeat(64),runtime_config:{},run_id:String(run),run_attempt:'1'});
export const seal=id=>({version:1,identity:id,payload_sha256:'e'.repeat(64)});
export function stubGPU(inputs,ids,id,executions=[]){
  executions.push([...ids]);
  return {status:'pass',browser_status:'pass',profile:'strict-gpu',review_scope:'models',commit:id.source_commit,chromium_version:PINNED_BROWSER.chromium,
    selected_model_ids:[...ids],models:ids.map(key=>({id:key,glb_sha256:inputs.models.find(row=>row.id===key).glb_sha256,status:'gpu-pass',checks:['fixture runner invoked']})),
    gpu:{status:'pass',rendered_models:[...ids],fallback_models:[]},page_errors:[],resource_errors:[]};
}
/** Synthetic report, not evidence that any actual browser reproduced a WebP. */
export function stubCards(inputs,ids,executions=[]){
  executions.push([...ids]);
  return {status:'pass',target_renderer:'threejs-modelstage',render_preset:structuredClone(CARD_RENDER_PRESET),...inputs.card_preview_renderer,
    chromium_version:PINNED_BROWSER.chromium,pinned_chromium_version:PINNED_BROWSER.chromium,
    assets:ids.map(id=>{const input=inputs.models.find(row=>row.id===id);return {id,source_glb_sha256:input.glb_sha256,frames:1,frame_bytes_total:0,poster_bytes:input.card_preview.bytes};}),
    gpu:{peakRequests:1},reproducibility:{checked:ids.length,mismatches:[]}};
}
export const verification=proof=>({schema:2,repository:proof.repository,source_commit:proof.source_commit,run_id:proof.run_id,run_attempt:proof.run_attempt,artifact_id:500+proof.run_id,artifact_sha256:`sha256:${'f'.repeat(64)}`,proof_sha256:hashObject(proof)});
export function finish(inputs,plan,id,baseProof=null,executions=[],cardExecutions=[]){
  const build={...seal(id),...(inputs.built_payload_sha256?{payload_sha256:inputs.built_payload_sha256}:{})},freshRecords=plan.fresh_ids.length?freshModelRecords({inputs,selectedIDs:plan.fresh_ids,browser:stubGPU(inputs,plan.fresh_ids,id,executions),identity:id,payload_sha256:build.payload_sha256}):[];
  const freshCardRecords=plan.fresh_ids.length?freshCardPreviewRecords({inputs,selectedIDs:plan.fresh_ids,report:stubCards(inputs,plan.fresh_ids,cardExecutions),identity:id,payload_sha256:build.payload_sha256}):[];
  return aggregateModelProof({inputs,scopePlan:plan,freshRecords,freshCardRecords,identity:id,build,baseProof,repository:'owner/repo'});
}
/** Small complete delivered surfaces exercise real protected generators, not Vite/GPU. */
export async function buildFixture(f){
  const output=join(f.root,'dist');rmSync(output,{recursive:true,force:true});mkdirSync(output,{recursive:true});
  const write=(path,value)=>f.put(`dist/${path}`,value);
  const template='<!doctype html><html lang="en"><head><title>Fixture</title></head><body><main id="home-page"></main><script type="module" src="/assets/index-fixture.js"></script></body></html>';
  f.put('qa/ci-model-proof/vite-template.html',template);write('index.html',template);
  write('assets/index-fixture.js','export const renderer = 42;');write('assets/index-fixture.css','canvas { display:block }');
  const delivered=await enrichManifest(f.manifest,f.root),turntables=await collectTurntables(delivered,f.root);
  for(const asset of delivered.assets){
    if(turntables.posters.has(asset.id))asset.card_preview=turntables.posters.get(asset.id);
    if(turntables.descriptors.has(asset.id))asset.turntable=turntables.descriptors.get(asset.id);
    for(const kind of ['glb','blend','preview']){mkdirSync(dirname(join(output,asset[kind])),{recursive:true});copyFileSync(join(f.root,asset[kind]),join(output,asset[kind]));}
    const archive=`fake ZIP fixture for ${asset.id}`;write(asset.downloads.bundle,archive);asset.file_sizes.bundle=Buffer.byteLength(archive);
    write(asset.downloads.credits,creditText(asset,delivered));
    for(const path of [f.resources.posters[asset.id].detail,f.resources.posters[asset.id].wheel])write(path,readFileSync(join(f.root,'site/public',path)));
  }
  for(const path of turntables.files)write(path,readFileSync(join(f.root,path)));
  write('assets/manifest.json',JSON.stringify(delivered,null,2)+'\n');write('gallery/resources.json',f.resources);
  await writeCatalog(delivered,output,{approvedOnly:true,catalogData:f.catalog});
  await writeStaticRoutes(delivered,output,{catalogData:f.catalog});
  return output;
}
export async function runBuiltRenderProofTests(){
  const f=fixture(190),executions=[],cardExecutions=[];
  try{
    f.put('site/initial-release.mjs','export const checkPublishedManifest = () => true;\n');
    f.resources.generated_capture={renderer:'approved PreviewRenderer.poster',browser:PINNED_BROWSER.chromium,source_renderer_sha256:'a'.repeat(64),runtime_renderer_sha256:'b'.repeat(64),assets:f.manifest.assets.slice(0,8).map(asset=>asset.id),published_total:190};
    f.put('site/public/gallery/resources.json',f.resources);
    await buildFixture(f);
    const first=computeModelInputs({root:f.root,built:await assertBuiltRenderInputs({root:f.root})});
    const base=finish(first,planModelReuse({inputs:first}),identity(),null,executions,cardExecutions);
    assert.equal(first.render_inputs,'verified-built-render-v1');
    const sourceOnly=computeModelInputs({root:f.root});assert.notEqual(sourceOnly.models[0].input_key,first.models[0].input_key,'Source-only evidence cannot match built evidence');
    const originalPolicy=modelPolicyDigest(f.root);
    f.put('site/initial-release.mjs','export const checkPublishedManifest = () => { /* stronger authorization */ return true; };\n');
    assert.equal(modelPolicyDigest(f.root),originalPolicy,'Authorization-only code is not the render policy');
    const checked=computeModelInputs({root:f.root,built:await assertBuiltRenderInputs({root:f.root})});
    assert.equal(planModelReuse({inputs:checked,baseProof:base,verifiedBaseProof:verification(base)}).reused_ids.length,190);
    assert.notEqual(computeModelInputs({root:f.root}).models[0].input_key,sourceOnly.models[0].input_key,'No build verification means authorization source remains conservative');
    f.add(4);f.resources.generated_capture.assets=f.manifest.assets.slice(-4).map(asset=>asset.id);f.resources.generated_capture.published_total=194;f.put('site/public/gallery/resources.json',f.resources);await buildFixture(f);
    const next=computeModelInputs({root:f.root,built:await assertBuiltRenderInputs({root:f.root})}),plan=planModelReuse({inputs:next,baseProof:base,verifiedBaseProof:verification(base)});
    assert.equal(plan.reused_ids.length,190);assert.equal(plan.fresh_ids.length,4,'Real generated catalog/HTML append should preserve all 190 old inputs');
    const combined=finish(next,plan,identity('c'.repeat(40),102),base,executions,cardExecutions);
    assert.deepEqual(executions.map(ids=>ids.length),[190,4]);assert.deepEqual(cardExecutions,executions,'Both independent stub tasks must execute exactly 190 + 4 built-input IDs');
    assert.equal(combined.models.find(row=>row.id==='model-001').card_preview_proof.origin.run_id,101);
    assert.equal(combined.models.find(row=>row.id==='model-194').card_preview_proof.origin.run_id,102);
    const changedRecipe=structuredClone(f.resources);changedRecipe.generated_capture.runtime_renderer_sha256='c'.repeat(64);f.put('dist/gallery/resources.json',changedRecipe);
    const recipeInputs=computeModelInputs({root:f.root,built:await assertBuiltRenderInputs({root:f.root})});assert.equal(planModelReuse({inputs:recipeInputs,baseProof:base,verifiedBaseProof:verification(base)}).reused_ids.length,0,'Capture renderer diagnostics stay shared render inputs');
    changedRecipe.generated_capture.runtime_renderer_sha256='b'.repeat(64);changedRecipe.generated_capture.unknown_recipe_option=true;f.put('dist/gallery/resources.json',changedRecipe);
    const unknownRecipe=computeModelInputs({root:f.root,built:await assertBuiltRenderInputs({root:f.root})});assert.equal(planModelReuse({inputs:unknownRecipe,baseProof:base,verifiedBaseProof:verification(base)}).reused_ids.length,0,'Unknown capture fields cannot disappear');
    f.put('dist/gallery/resources.json',f.resources);
    // A publication script could change dist only. Shared runtime bytes still
    // invalidate every model even with identical source and a legitimate seal.
    f.put('dist/assets/index-fixture.js','export const renderer = 99;');
    const badRuntime=computeModelInputs({root:f.root,built:await assertBuiltRenderInputs({root:f.root})});
    assert.equal(planModelReuse({inputs:badRuntime,baseProof:base,verifiedBaseProof:verification(base)}).reused_ids.length,0);
    await buildFixture(f);
    for(const path of ['models/index.html','models/model-001/index.html','assets/catalog.json','assets/catalog/details/model-001.json','assets/manifest.json']){
      const original=readFileSync(join(f.root,'dist',path));f.put(`dist/${path}`,original+'<script>globalThis.poisoned = true</script>');
      await assert.rejects(()=>assertBuiltRenderInputs({root:f.root}),/Delivered|JSON|Unexpected/);f.put(`dist/${path}`,original);
    }
    const oldPoster=f.resources.posters['model-001'].detail,posterBytes='different verified poster bytes';
    f.put(`dist/${oldPoster}`,posterBytes);
    const changedResources=structuredClone(f.resources),seal=changedResources.files.find(row=>row.path===oldPoster);seal.sha256=hashBytes(posterBytes);seal.bytes=Buffer.byteLength(posterBytes);f.put('dist/gallery/resources.json',changedResources);
    const changedPoster=computeModelInputs({root:f.root,built:await assertBuiltRenderInputs({root:f.root})}),posterPlan=planModelReuse({inputs:changedPoster,baseProof:base,verifiedBaseProof:verification(base)});
    assert.equal(posterPlan.reused_ids.length,189);assert(posterPlan.fresh_ids.includes('model-001'),'Changed actual poster affects its model, not all 190');
    await buildFixture(f);
    const card=f.cards.posters[0],originalCard=readFileSync(join(f.root,card.path));
    f.put(`dist/${card.path}`,Buffer.concat([originalCard,Buffer.from('tampered')]));
    await assert.rejects(()=>assertBuiltRenderInputs({root:f.root}),/Delivered turntable differs/,'Delivered WebP cannot differ from checked source card');await buildFixture(f);
    const changedCard=Buffer.from(originalCard);changedCard[changedCard.length-1]^=1;
    f.put(card.path,changedCard);card.sha256=hashBytes(changedCard);f.put('assets/turntables/index.json',f.cards);await buildFixture(f);
    const cardInputs=computeModelInputs({root:f.root,built:await assertBuiltRenderInputs({root:f.root})}),cardPlan=planModelReuse({inputs:cardInputs,baseProof:base,verifiedBaseProof:verification(base)});
    assert.equal(cardPlan.reused_ids.length,189);assert(cardPlan.fresh_ids.includes('model-001'),'Changed sealed shipped card invalidates exactly its model, independently of gallery PNGs');
    f.put(card.path,originalCard);card.sha256=hashBytes(originalCard);f.put('assets/turntables/index.json',f.cards);await buildFixture(f);
    f.put('site/gallery/renderer.js',"import '../initial-release.mjs'; export const camera = 42;\n");
    const reachableBefore=modelPolicyDigest(f.root);f.put('site/initial-release.mjs','export const checkPublishedManifest = () => false;\n');
    assert.notEqual(modelPolicyDigest(f.root),reachableBefore,'An authorization module imported by rendering is protected again');
    f.put('site/gallery/renderer.js','export const camera = 42;\n');
    const policyBefore=modelPolicyDigest(f.root);f.put('site/small-life-round99-release.mjs','export const unknown = true;\n');
    assert(!PUBLICATION_ONLY_MODULES.includes('site/small-life-round99-release.mjs'));assert.notEqual(modelPolicyDigest(f.root),policyBefore,'Unknown executable cannot self-classify as authorization');
    // Both ESM createRequire aliases and CJS bridges execute imports; extension
    // alone must never conceal a formerly authorization-only module.
    f.put('site/copy-assets.mjs',"import {createRequire as makeRequire} from 'node:module'; const req = makeRequire(import.meta.url); req('./initial-release.mjs');\n");
    let requirePolicy=modelPolicyDigest(f.root);f.put('site/initial-release.mjs','export const authorizationRevision = 2;\n');
    assert.notEqual(modelPolicyDigest(f.root),requirePolicy,'createRequire alias promotes authorization dependencies');
    f.put('site/copy-assets.mjs',"import './bridge.cjs';\n");f.put('site/bridge.cjs',"const release = require('./initial-release.mjs'); module.exports = release;\n");
    requirePolicy=modelPolicyDigest(f.root);f.put('site/initial-release.mjs','export const authorizationRevision = 3;\n');
    assert.notEqual(modelPolicyDigest(f.root),requirePolicy,'CJS bridge promotes authorization dependencies');
    for(const source of ["const name = './initial-release.mjs'; require(name);", "require.bind(null)('./initial-release.mjs');", "module['require']('./initial-release.mjs');", "const loaders=[require]; loaders[0]('./initial-release.mjs');", "const {createRequire}=require('node:module'); const loaders={factory:createRequire}; loaders.factory(__filename)('./initial-release.mjs');", "require('#authorization');"]){
      f.put('site/bridge.cjs',source);assert.throws(()=>modelPolicyDigest(f.root),/Computed|Unsupported|Unresolved/,'Unresolved require cannot be ignored');
    }
    f.put('site/bridge.cjs',"module.exports = require('./initial-release.mjs');\n");
    for(const [path,source] of [['production/new-collector.py','print("new")'],['assets/releases/new-collector.js','export const added = true;']]){
      const before=modelPolicyDigest(f.root);f.put(path,source);assert.notEqual(modelPolicyDigest(f.root),before,`Unknown executable must invalidate proof and poster policy: ${path}`);
    }
    assert.throws(()=>computeModelInputs({root:f.root,built:{...next}}),/independent in-process/,'A JSON projection is not build verification');
    console.log('Built render proof: exact generated HTML/catalog, independent GPU/card 190 + 4 stub execution, authorization-only isolation, shared runtime tamper, per-model gallery/card changes and unknown/runtime-reachable code fixtures pass.');
  }finally{f.close();}
}
export function runModelProofTests(){
  const f=fixture(),executions=[],cardExecutions=[];
  try{
    const first=computeModelInputs({root:f.root}),all=planModelReuse({inputs:first});assert.equal(all.fresh_ids.length,190);assert.equal(all.reused_ids.length,0);
    const base=finish(first,all,identity(),null,executions,cardExecutions);assert.equal(executions[0].length,190);
    f.add(4);const second=computeModelInputs({root:f.root});
    const next=planModelReuse({inputs:second,baseProof:base,verifiedBaseProof:verification(base)});
    assert.equal(next.fresh_ids.length,4);assert.equal(next.reused_ids.length,190);assert.deepEqual(next.fresh_ids,['model-191','model-192','model-193','model-194']);
    const proof194=finish(second,next,identity('c'.repeat(40),102),base,executions,cardExecutions);assert.deepEqual(executions[1],next.fresh_ids);
    assert.equal(proof194.models.find(row=>row.id==='model-001').origin.run_id,101);assert.equal(proof194.models.find(row=>row.id==='model-194').origin.run_id,102);
    f.add(4);const third=computeModelInputs({root:f.root}),thirdPlan=planModelReuse({inputs:third,baseProof:proof194,verifiedBaseProof:verification(proof194)});
    assert.equal(thirdPlan.fresh_ids.length,4);assert.equal(thirdPlan.reused_ids.length,194);
    finish(third,thirdPlan,identity('d'.repeat(40),103),proof194,executions,cardExecutions);assert.deepEqual(executions[2],['model-195','model-196','model-197','model-198']);
    assert.equal(executions.flat().length,198,'Stub runner must execute every ID exactly once across data-only batches');
    assert.deepEqual(cardExecutions,executions,'Separate GPU and card stub runners must each execute every ID exactly once');
    const missing=structuredClone(base);missing.models.pop();const missingPlan=planModelReuse({inputs:second,baseProof:missing,verifiedBaseProof:verification(missing)});assert.equal(missingPlan.reused_ids.length,189);assert(missingPlan.fresh_ids.includes('model-190'));
    for(const mutation of [proof=>proof.models.push({...proof.models[0],id:'unknown-id'}),proof=>proof.models.push(proof.models[0]),proof=>proof.models[0].status='fallback-only']){
      const forged=structuredClone(base);mutation(forged);assert.equal(planModelReuse({inputs:second,baseProof:forged,verifiedBaseProof:verification(forged)}).reused_ids.length,0);
    }
    const forged=structuredClone(base);forged.models[0].input_key='0'.repeat(64);assert.equal(planModelReuse({inputs:second,baseProof:forged,verifiedBaseProof:verification(base)}).reused_ids.length,0,'Receipt mutation cannot preserve verification');
    const input0=third.models[0],glb=f.manifest.assets[0].glb;f.put(glb,'changed actual GLB');assert.throws(()=>computeModelInputs({root:f.root}),/Actual glb bytes/);f.put(glb,`glb fixture bytes for ${input0.id}`);
    for(const path of ['site/gallery/renderer.js','site/viewer.js','site/render-preset.js','site/ci-card-preview-proof.mjs','site/style.css','site/redesign-browser-test.mjs','package-lock.json','qa/conifer-doc1-integration/conifer-handoff-browser-test.mjs']){
      const original=readFileSync(join(f.root,path));f.put(path,path.endsWith('.json')?original.toString().replace('pinned-package-integrity','changed-integrity'):original+'\n// changed');
      const changed=computeModelInputs({root:f.root});assert.equal(planModelReuse({inputs:changed,baseProof:proof194,verifiedBaseProof:verification(proof194)}).reused_ids.length,0,path);f.put(path,original);
    }
    f.framing['model-001'].azimuth=99;f.put('site/gallery/wheel-framing.json',f.framing);const camera=computeModelInputs({root:f.root});assert.notEqual(camera.models[0].input_key,third.models[0].input_key);assert.equal(camera.models[1].input_key,third.models[1].input_key);f.framing['model-001'].azimuth=42;f.put('site/gallery/wheel-framing.json',f.framing);
    f.manifest.assets[0].dimensions=[4,5,6];f.put('assets/manifest.json',f.manifest);const dimensions=computeModelInputs({root:f.root});assert.notEqual(dimensions.models[0].input_key,third.models[0].input_key);assert.equal(dimensions.models[1].input_key,third.models[1].input_key);f.manifest.assets[0].dimensions=[1,2,3];f.put('assets/manifest.json',f.manifest);
    const id=identity('c'.repeat(40),102),build=seal(id),browser=stubGPU(second,next.fresh_ids,id),records=freshModelRecords({inputs:second,selectedIDs:next.fresh_ids,browser,identity:id,payload_sha256:build.payload_sha256});
    const cardRecords=freshCardPreviewRecords({inputs:second,selectedIDs:next.fresh_ids,report:stubCards(second,next.fresh_ids),identity:id,payload_sha256:build.payload_sha256});
    assert(records.every(row=>row.card_preview_proof===undefined),'GPU workers finish provisionally without waiting for the separate card reproduction job');
    for(const bad of [{...browser,profile:'allow-webgl-fallback'},{...browser,chromium_version:'142.0.0.0'},{...browser,models:[...browser.models,browser.models[0]]},{...browser,gpu:{...browser.gpu,fallback_models:[next.fresh_ids[0]]}}])assert.throws(()=>freshModelRecords({inputs:second,selectedIDs:next.fresh_ids,browser:bad,identity:id,payload_sha256:build.payload_sha256}));
    for(const bad of [records.slice(1),[...records,records[0]],records.map((row,index)=>index?row:{...row,origin:{...row.origin,payload_sha256:'0'.repeat(64)}})])assert.throws(()=>aggregateModelProof({inputs:second,scopePlan:next,freshRecords:bad,freshCardRecords:cardRecords,identity:id,build,baseProof:base}));
    assert.throws(()=>aggregateModelProof({inputs:second,scopePlan:{...next,reused_ids:[...next.reused_ids,next.fresh_ids[0]]},freshRecords:records,freshCardRecords:cardRecords,identity:id,build,baseProof:base}));
    assert.throws(()=>aggregateModelProof({inputs:second,scopePlan:next,freshRecords:records,identity:id,build,baseProof:base}),/Actually reproduced card previews/,'GPU/gallery evidence alone cannot finalize a model proof');
    const aggregateArgs={inputs:second,scopePlan:next,freshRecords:records,identity:id,build,baseProof:base};
    for(const bad of [cardRecords.slice(1),[...cardRecords,cardRecords[0]],records])assert.throws(()=>aggregateModelProof({...aggregateArgs,freshCardRecords:bad}),'Exact separate card coverage is mandatory');
    for(const [label,mutate] of [
      ['card bytes',row=>row.card_preview.sha256='0'.repeat(64)],['card path',row=>row.card_preview.path='assets/card-previews/other.webp'],
      ['card size',row=>row.card_preview.bytes++],['viewer',row=>row.result.viewer_source_sha256='0'.repeat(64)],
      ['preset',row=>{row.result.render_preset.image.quality=0.8;row.result.render_preset_sha256=hashBytes(JSON.stringify(row.result.render_preset));}],
      ['source',row=>row.origin.source_commit='e'.repeat(40)],['tree',row=>row.origin.source_tree='e'.repeat(40)],
      ['run',row=>row.origin.run_id++],['attempt',row=>row.origin.run_attempt++],['build',row=>row.origin.payload_sha256='0'.repeat(64)],
      ['input key',row=>row.input_key='0'.repeat(64)],['input hash',row=>row.input_sha256='0'.repeat(64)],
      ['GLB',row=>{row.glb_sha256='0'.repeat(64);row.result.source_glb_sha256=row.glb_sha256;}],
      ['gallery renderer',row=>row.result.target_renderer='PreviewRenderer.poster'],['mismatch',row=>row.result.reproducibility.mismatches.push({matches:false})]
    ]){
      const bad=structuredClone(cardRecords);mutate(bad[0]);assert.throws(()=>aggregateModelProof({...aggregateArgs,freshCardRecords:bad}),undefined,`Fresh ${label} must fail closed`);
      const forged=structuredClone(base);mutate(forged.models[0].card_preview_proof);
      assert.equal(planModelReuse({inputs:second,baseProof:forged,verifiedBaseProof:verification(forged)}).reused_ids.length,0,`Historical ${label} must fail closed even with an authenticated receipt`);
      assert.throws(()=>assertBaseModelProof(forged,baselineArguments(forged)),undefined,`Baseline rejects ${label}`);
    }
    for(const mutate of [proof=>delete proof.card_preview_renderer,proof=>delete proof.models[0].card_preview_proof,proof=>delete proof.models[0].card_preview,proof=>delete proof.models[0].card_preview.bytes,proof=>proof.models[0].card_preview_proof=proof.models[0].result]){
      const missing=structuredClone(base);mutate(missing);assert.equal(planModelReuse({inputs:second,baseProof:missing,verifiedBaseProof:verification(missing)}).reused_ids.length,0);
      assert.throws(()=>assertBaseModelProof(missing,baselineArguments(missing)),'No grandfathered GPU-only or gallery-only baseline');
    }
    assertBaseModelProof(base,baselineArguments(base));
    const card=f.cards.posters[0],originalCard=readFileSync(join(f.root,card.path)),originalIndex=readFileSync(join(f.root,'assets/turntables/index.json'));
    f.put(card.path,'different actual WebP');assert.throws(()=>computeModelInputs({root:f.root}),/Actual card-preview bytes/);f.put(card.path,originalCard);
    for(const mutate of [value=>value.posters.pop(),value=>value.posters.push(value.posters[0]),value=>value.posters[0].source_glb_sha256='0'.repeat(64),value=>value.posters[0].render_preset_sha256='0'.repeat(64),value=>value.posters[0].path='assets/card-previews/other.webp']){
      const bad=structuredClone(f.cards);mutate(bad);f.put('assets/turntables/index.json',bad);assert.throws(()=>computeModelInputs({root:f.root}));f.put('assets/turntables/index.json',originalIndex);
    }
    rmSync(join(f.root,'assets/turntables/index.json'));assert.throws(()=>computeModelInputs({root:f.root}),/ENOENT/);f.put('assets/turntables/index.json',originalIndex);
    const changedCard=Buffer.from(originalCard);changedCard[changedCard.length-1]^=1;f.put(card.path,changedCard);card.sha256=hashBytes(changedCard);f.put('assets/turntables/index.json',f.cards);
    const cardChange=computeModelInputs({root:f.root}),cardPlan=planModelReuse({inputs:cardChange,baseProof:proof194,verifiedBaseProof:verification(proof194)});
    assert.equal(cardPlan.reused_ids.length,193);assert(cardPlan.fresh_ids.includes('model-001'));assert.equal(cardChange.models[1].input_key,third.models[1].input_key);
    f.put(card.path,originalCard);card.sha256=hashBytes(originalCard);f.put('assets/turntables/index.json',originalIndex);
    assert.throws(()=>assertBaseModelProof({...base,version:1},{repository:'owner/repo'}),/v2 baseline/);
    console.log('Model proof v2: independent GPU/card 190 → 194 → 198 exact stub execution; missing/forged cards, renderer/source/run/build/input mismatches, actual WebP bytes and exact-union adversarial fixtures pass.');
  }finally{f.close();}
}
function baselineArguments(proof){return {repository:proof.repository,baseSha:proof.source_commit,sourceTree:proof.source_tree,runId:proof.run_id,runAttempt:proof.run_attempt,policy_sha256:proof.policy_sha256,runtime_config:proof.runtime_config,catalog_ids:proof.catalog_ids};}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){runModelProofTests();await runBuiltRenderProofTests();}

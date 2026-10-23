// Bounded synthetic fixture: no catalog assets, credentials, Git or network required.
// Test-only instrumentation delegates to the actual inspector/collector unchanged.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,mkdtemp,rm} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {tmpdir} from 'node:os';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const here=dirname(fileURLToPath(import.meta.url));
const source=await readFile(resolve(here,process.env.PRODUCTION_MEMO_TEST_SOURCE||'production-release.mjs'),'utf8');
const instrumented=resolve(here,`.poster-memo-test-${process.pid}.mjs`);
const marker='export async function inspectProductionRelease(root,descriptorPath,registryPath){';
assert.equal(source.split(marker).length,2,'Inspector instrumentation must match exactly once');
await writeFile(instrumented,source.replace(marker,`export const inspectionCounts=new Map();
export async function inspectProductionRelease(root,descriptorPath,registryPath){
 inspectionCounts.set(descriptorPath,(inspectionCounts.get(descriptorPath)||0)+1);
 return inspectProductionReleaseActual(root,descriptorPath,registryPath);
}
async function inspectProductionReleaseActual(root,descriptorPath,registryPath){`));
const api=await import(pathToFileURL(instrumented));
const hash=b=>createHash('sha256').update(b).digest('hex');
const h='a'.repeat(64),text={en:'TEST ONLY triangle',zh:'仅测试三角形'};
const budget={max_triangles:10,max_materials:2,max_primitives:2,max_glb_bytes:10000};
const glb=execFileSync('python3',['-c','from test_qa_glb import fixture,encode; import sys; sys.stdout.buffer.write(encode(*fixture()))'],{cwd:resolve(here,'../scripts'),env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
async function fixture(){
 const root=await mkdtemp(resolve(tmpdir(),'poster-memo-'));
 async function put(path,bytes){bytes=Buffer.isBuffer(bytes)?bytes:Buffer.from(typeof bytes==='string'?bytes:JSON.stringify(bytes));await mkdir(dirname(resolve(root,path)),{recursive:true});await writeFile(resolve(root,path),bytes);return {path,sha256:hash(bytes),bytes:bytes.length};}
 const implementation=await put('implementation.txt','TEST ONLY implementation');
 const scope=await put('scope.txt','TEST ONLY scope');
 const assets=[],records=[],descriptors=[];const resources={posters:{},files:[]};
 for(const [group,ids] of [['first',['one','two']],['second',['three']]]){
  const descriptorPath=`${group}/release.json`,items=[];
  for(const id of ids){
   const roles={};for(const role of ['brief','config','references','generator','dependency-list','finalGLB','finalBlend'])roles[role]=await put(`${id}/${role}`,role==='finalGLB'?glb:role==='brief'?{geometry_policy:budget}:`TEST ONLY ${id} ${role}`);
   const preview=await put(`${id}/preview.png`,'TEST ONLY preview');
   const renderer=await put(`${id}/renderer.py`,'TEST ONLY renderer');
   const recipe=await put(`${id}/recipe.json`,{source_glb_sha256:roles.finalGLB.sha256,blender_version:'TEST ONLY',rendered_unchanged_source:true,files:[renderer]});
   const posters={route:'blender-cycles-cpu-v1',source_glb_sha256:roles.finalGLB.sha256,browser_capture:false,blender_version:'TEST ONLY',recipe,recipe_sha256:recipe.sha256};
   for(const [kind,size] of [['detail',[512,512]],['wheel',[768,432]]]){
    const png=Buffer.alloc(26);Buffer.from('89504e470d0a1a0a','hex').copy(png);png.writeUInt32BE(size[0],16);png.writeUInt32BE(size[1],20);png[24]=8;png[25]=6;
    const pin=await put(`site/public/${id}-${kind}.png`,png);
    const config=await put(`${id}/${kind}.json`,{source_geometry_and_materials_unchanged:true,film_transparent:true,version:'TEST ONLY',renderer_sha256:renderer.sha256,resolution:size});
    posters[kind]={...pin,render_config:config,camera_degrees:[42,23.3],source_glb_sha256:roles.finalGLB.sha256,pixel_sha256:h};
   }
   const asset={id,revision:'test',production_release:descriptorPath,glb:roles.finalGLB.path,blend:roles.finalBlend.path,preview:preview.path,sha256:{glb:roles.finalGLB.sha256,blend:roles.finalBlend.sha256,preview:preview.sha256},name:text,description:text,license:'CC-BY-4.0',units:'meters',representation:'fossil-specimen',reference_credits:['TEST ONLY'],triangles:1,dimensions:[1,1,0],production_posters:{route:posters.route,detail:posters.detail.path,wheel:posters.wheel.path}};
   const record={asset_id:id,revision:'test',schema_version:1,kind:'compact-production-release-v1',productionAccepted:true,maker:{id:'test-maker',task_id:'test-maker'},original_acceptance:{kind:'layered-production-acceptance-v001',reviewer:{id:'test-original-reviewer',task_id:'test-original-reviewer'},sha256:h,subject:{glb_sha256:asset.sha256.glb}},legacy_record:{mutated:false,sha256:h,scientific_brief_sha256:roles.brief.sha256,scientific_references_sha256:roles.references.sha256},blocking_findings:[],production_gates:Object.fromEntries(['factual','visual','technical','standard_glb','source_reproducibility','runtime_parse','specification'].map(k=>[k,{status:'PASS',source_evidence_sha256:[h]}])),roles,subject:Object.fromEntries(Object.entries(roles).map(([k,v])=>[k,v.sha256])),build_closure:[roles.generator,roles.config],preview,preview_provenance:{source_glb_sha256:asset.sha256.glb,independently_reviewed_original_preview:true,review_sha256:h},scientific_limits:text,inventory_departure:'TEST ONLY',source_archive:{status:'VERIFIED_PRIVATE_ARCHIVE',receipt_sha256:h,index_sha256:h},frozen_budget:budget,measurements:{triangles:1,dimensions:[1,1,0]},postReleaseVerified:{status:'NOT_PUBLISHED'},final_posters:posters};
   items.push({id,metadata:await put(`${id}/metadata.json`,asset),evidence:await put(`${id}/evidence.json`,record)});assets.push(asset);records.push(record);
   resources.posters[id]={render_route:posters.route,recipe_sha256:recipe.sha256,production_descriptor:descriptorPath,source_glb_sha256:asset.sha256.glb};
   for(const kind of ['detail','wheel']){const p=posters[kind];const path=p.path.replace(/^site\/public\//,'');resources.posters[id][kind]=path;resources.files.push({path,sha256:p.sha256,bytes:p.bytes});}
  }
  const descriptor={schema_version:1,kind:'production-release-v1',publication_authorized:false,baseline_commit:'b'.repeat(40),implementation:[implementation],scope_document:scope,producer:{id:'test-preparer',task_id:'test-preparer'},assets:items,review_path:`${group}/review.json`};
  const pin=await put(descriptorPath,descriptor);
  await put(descriptor.review_path,{schema_version:1,kind:'independent-production-projection-review-v1',status:'PASS',reviewed_descriptor_sha256:pin.sha256,reviewer:{id:'test-projection-reviewer',task_id:'test-projection-reviewer'},blocking_findings:[],checks:Object.fromEntries(api.PRODUCTION_CHECKS.map(k=>[k,'PASS'])),publication_authorized:false,original_acceptance_sha256:[h]});descriptors.push(descriptor);
 }
 return {root,assets,resources,records,descriptors,put};
}
const legacy={valid:['legacy'],opaque:'preserved'};
try{
 await test('invocation-local production poster inspections',async t=>{
  const f=await fixture();const run=(assets=f.assets,resources=f.resources)=>api.appendProductionPosterInputState(f.root,assets,resources,legacy);
  try{
   await t.test('two descriptors: one explicit inspect plus retained collect inspection each; correct per-asset output',async()=>{
    api.inspectionCounts.clear();const before=structuredClone([f.assets,f.resources,legacy]);assert.deepEqual(await run(),{...legacy,valid:['legacy','one','two','three'],production:['one','two','three']});
    assert.deepEqual([...api.inspectionCounts],[['first/release.json',2],['second/release.json',2]]);assert.deepEqual([f.assets,f.resources,legacy],before);
   });
   await t.test('interleaved descriptor members retain input order and single inspection',async()=>{api.inspectionCounts.clear();assert.deepEqual((await run([f.assets[0],f.assets[2],f.assets[1]])).production,['one','three','two']);assert.deepEqual([...api.inspectionCounts],[['first/release.json',2],['second/release.json',2]]);});
   await t.test('another invocation re-inspects each descriptor',async()=>{api.inspectionCounts.clear();await run();assert.deepEqual([...api.inspectionCounts],[['first/release.json',2],['second/release.json',2]]);});
   async function tamper(path,change,pattern){const original=await readFile(resolve(f.root,path));try{await writeFile(resolve(f.root,path),change(original));await assert.rejects(run,pattern);}finally{await writeFile(resolve(f.root,path),original);}}
   await t.test('changed GLB in second member fails on later call',()=>tamper('two/finalGLB',b=>Buffer.concat([b,Buffer.from('x')]),/Production size changed/));
   await t.test('changed source bytes fail on later call',()=>tamper('two/generator',b=>Buffer.concat([b,Buffer.from('x')]),/Production size changed/));
   await t.test('changed descriptor fails fresh detached review binding',()=>tamper('first/release.json',b=>Buffer.concat([b,Buffer.from(' ')]),/Stale projection review/));
   await t.test('altered source pin fails closed',()=>tamper('first/release.json',b=>{const d=JSON.parse(b);d.scope_document.sha256='0'.repeat(64);return JSON.stringify(d);},/Production hash changed/));
   await t.test('collect still rejects failed independent review',()=>tamper('first/review.json',b=>{const d=JSON.parse(b);d.status='FAIL';return JSON.stringify(d);},/projection review is pending/));
   await t.test('collect still verifies poster bytes',()=>tamper('site/public/two-wheel.png',b=>Buffer.concat([b,Buffer.from('x')]),/Production size changed/));
   await t.test('collect inspects all descriptor members even if caller selects only first',async()=>{const b=await readFile(resolve(f.root,'two/generator'));try{await writeFile(resolve(f.root,'two/generator'),'changed');await assert.rejects(()=>run([f.assets[0]]),/Production size changed/);}finally{await writeFile(resolve(f.root,'two/generator'),b);}});
   for(const [label,mutate] of [
    ['recipe',r=>r.posters.two.recipe_sha256='0'.repeat(64)],['route',r=>r.posters.two.render_route='browser'],['descriptor',r=>r.posters.two.production_descriptor='wrong'],['source GLB',r=>r.posters.two.source_glb_sha256='0'.repeat(64)],['detail path',r=>r.posters.two.detail='wrong'],['wheel path',r=>r.posters.two.wheel='wrong'],['seal hash',r=>r.files.find(p=>p.path==='two-detail.png').sha256='0'.repeat(64)],['seal bytes',r=>r.files.find(p=>p.path==='two-wheel.png').bytes++],['missing seal',r=>r.files=r.files.filter(p=>p.path!=='two-detail.png')]])await t.test(`second member poster ${label} mismatch rejected`,async()=>{const r=structuredClone(f.resources);mutate(r);await assert.rejects(()=>run(f.assets,r));});
   await t.test('per-asset metadata mismatch rejected',async()=>{const a=structuredClone(f.assets);a[1].description.en='changed';await assert.rejects(()=>run(a),/Unbound production metadata/);});
   await t.test('duplicate production ID rejected',async()=>{await assert.rejects(()=>run([...f.assets,f.assets[1]]),/Duplicate production input state/);});
   await t.test('duplicate legacy ID rejected',async()=>{await assert.rejects(()=>api.appendProductionPosterInputState(f.root,f.assets,f.resources,{valid:['two']}),/Duplicate production input state/);});
   await t.test('empty production preserves legacy without inspections',async()=>{api.inspectionCounts.clear();assert.deepEqual(await run([]),{...legacy,production:[]});assert.equal(api.inspectionCounts.size,0);});
   await t.test('restored fixture succeeds after failures; no rejected result retained',async()=>{assert.deepEqual((await run()).production,['one','two','three']);});
  }finally{await rm(f.root,{recursive:true,force:true});}
 });
}finally{await rm(instrumented,{force:true});}

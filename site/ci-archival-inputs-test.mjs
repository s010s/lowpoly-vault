import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {ARCHIVAL_REGISTRY_PATH,ARCHIVAL_REGISTRY_EXPORT,parseStaticPublicationExports,collectArchivalInputs,assertArchivalAppend} from './ci-archival-inputs.mjs';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const sourceCommit='a'.repeat(40),reviewCommit='b'.repeat(40);
export function archiveFixture(){
 const files=new Map(),modes=new Map(),registry=[],batches=[],manifest={assets:[]};
 const put=(path,value)=>{const bytes=Buffer.isBuffer(value)?value:Buffer.from(typeof value==='string'?value:JSON.stringify(value));files.set(path,bytes);modes.set(path,'100644');return {path,sha256:hash(bytes)};};
 const writeRegistry=()=>put(ARCHIVAL_REGISTRY_PATH,`export const ${ARCHIVAL_REGISTRY_EXPORT} = ${JSON.stringify(registry)};\n`);
 writeRegistry();
 function addBatch(name='new-four',ids=['model-191','model-192','model-193','model-194'],{models,readModel,candidateRoot}={}){
  const sourceRoot=candidateRoot||`production/${name}`,reviewRoot=`qa/independent/${name}`,sourceBundlePath=`qa/${name}-release/source-bundle.json`,descriptorPath=`assets/releases/${name}.json`;
  const descriptor={version:1,source_bundle:null,files:[],additions:[]},bundle={version:1,scope:'Exact archived source and independent review, not approval',files:[]};
  const archive=(path,bytes,origin='source',owner='$batch')=>{
   const pin=put(path,bytes);descriptor.files.push({...pin,origin,owner});bundle.files.push({...pin,...(origin==='release'?{}:{source_commit:origin==='source'?sourceCommit:reviewCommit})});return pin;
  };
  const generator=archive(`${sourceRoot}/generator.py`,'# Preserved generator. Never imported or run by this verifier.\nraise RuntimeError("archival generator must never execute")\n');
  archive(`${reviewRoot}/scene-check.mjs`,'throw new Error("archived QA must never execute");\n','review');
  archive(`${reviewRoot}/scene-check.cjs`,'throw new Error("archived CJS must never execute");\n','review');
  archive(`${reviewRoot}/preview.html`,'<script>throw new Error("archived HTML must never execute")</script>','review');
  archive(`${sourceRoot}/final-handoff.jsonl`,'{"status":"preserved"}\n');
  archive(`${sourceRoot}/build.log`,'Original output\n');archive(`${sourceRoot}/readme.txt`,'Original source notes\n');archive(`${sourceRoot}/.queue.lock`,'');archive(`${sourceRoot}/source.sha256`,'original source hash record\n');
  archive(`${sourceRoot}/extensionless`,'arbitrary preserved bytes, not an executable root\n');
  const review=archive(`${reviewRoot}/report.json`,{status:'limited-review'},'review');
  for(const id of ids){
   const supplied=models?.find(row=>row.id===id),model=supplied?structuredClone(supplied):{id,sha256:{}};
   for(const [kind,suffix]of [['glb','glb'],['blend','blend'],['preview','webp']]){
    const file=supplied?put(model[kind],readModel(model[kind])):put(`assets/additions/${id}/${name}/${id}.${suffix}`,`exact ${kind} bytes for ${id}`);
    if(supplied)assert.equal(file.sha256,model.sha256[kind]);else{model[kind]=file.path;model.sha256[kind]=file.sha256;}
   }
   const metadata=put(`assets/additions/${id}/${name}/release-metadata.json`,model);
   const glb=archive(`${sourceRoot}/${id}/r001/output/${id}.glb`,files.get(model.glb),'source',id);
   const candidate=archive(`${sourceRoot}/${id}/r001/candidate.json`,{asset_id:id,revision:'r001',artifacts:{generator,glb}},'source',id);
   descriptor.additions.push({id,revision:'r001',candidate,review,metadata});manifest.assets.push(model);
  }
  const entry={descriptor:null,asset_ids:[...ids].sort(),source_commit:sourceCommit,independent_review_commit:reviewCommit};
  registry.push(entry);
  const sync=()=>{descriptor.source_bundle=put(sourceBundlePath,bundle);entry.descriptor=put(descriptorPath,descriptor);writeRegistry();};sync();
  const batch={name,ids,descriptor,bundle,entry,archive,sync,sourceRoot,reviewRoot,generator};batches.push(batch);return batch;
 }
 const collect=(protectedPaths=[])=>collectArchivalInputs({paths:[...files.keys()],read:path=>files.get(path),mode:path=>modes.get(path),manifest,protectedPaths});
 return {files,modes,registry,batches,manifest,put,writeRegistry,addBatch,collect};
}
export function runArchivalInputTests(){
 const literal=parseStaticPublicationExports('export const A = {x:[null,true,-3,"ok"]}; export const B = [];');assert.deepEqual(literal,{A:{x:[null,true,-3,'ok']},B:[]});assert(Object.isFrozen(literal.A.x));
 for(const source of [
  'import "./archive.mjs"; export const A = [];',
  'export const A = (globalThis.executed = true);',
  'export const A = JSON.parse("[]");',
  'export const A = Object.freeze([]);',
  'export const A = [await import("./archive.mjs")];',
  'export const A = {["computed"]: 1};',
  'export const A = {get x(){return 1}};',
  'export const A = {...other};',
  'export const A = {x:undefined};',
  'export const A = {"__proto__":{}};',
  'export const A = {x:1,x:2};',
  'export const A = [,];',
  'export const A = /pattern/;',
  'export const A = 1n;',
  'export const A = `text`;',
  'export let A = [];',
  'const A = []; export {A};',
  'export default [];',
  'export function A(){}',
  'export const A = []; console.log("executed");'
 ])assert.throws(()=>parseStaticPublicationExports(source),undefined,source);
 const empty=archiveFixture(),baseline=empty.collect();assert.deepEqual(baseline.files,[]);
 const oldPaths=[...empty.files.keys()],batch=empty.addBatch(),next=empty.collect();
 assert.equal(next.files.length,batch.bundle.files.length);assert.equal(next.excludedPaths.length,next.files.length,'Exact source/review programs are read/hash-only archives');
 for(const id of batch.ids){assert(next.byModel[id].files.some(row=>row.path===batch.generator.path));assert(next.byModel[id].files.every(row=>row.owners.includes(id)));}
 for(const suffix of ['generator.py','final-handoff.jsonl','build.log','readme.txt','.queue.lock','source.sha256','extensionless'])assert(next.excludedPaths.includes(`${batch.sourceRoot}/${suffix}`));
 assert(next.excludedPaths.includes(`${batch.reviewRoot}/scene-check.mjs`));assert(next.excludedPaths.includes(`${batch.reviewRoot}/scene-check.cjs`));assert(next.excludedPaths.includes(`${batch.reviewRoot}/preview.html`));
 assertArchivalAppend(baseline,next,{beforePaths:oldPaths,oldIDs:[],newIDs:batch.ids});
 assert.throws(()=>assertArchivalAppend(structuredClone(baseline),next,{beforePaths:oldPaths,oldIDs:[],newIDs:batch.ids}),/independently verified/,'Saved JSON cannot grant archive trust');
 const sourcePaths=[...empty.files.keys()];const second=empty.addBatch('another-four',['model-195','model-196','model-197','model-198']),last=empty.collect();
 assertArchivalAppend(next,last,{beforePaths:sourcePaths,oldIDs:batch.ids,newIDs:second.ids});
 assert.deepEqual(last.byModel['model-191'],next.byModel['model-191'],'Appending another complete batch cannot alter old per-model archive inputs');
 const imported=empty.collect([batch.generator.path,`${batch.reviewRoot}/scene-check.mjs`]);assert(!imported.excludedPaths.includes(batch.generator.path));assert(!imported.excludedPaths.includes(`${batch.reviewRoot}/scene-check.mjs`));
 assert.throws(()=>assertArchivalAppend(last,imported,{beforePaths:[...empty.files.keys()],oldIDs:empty.manifest.assets.map(a=>a.id),newIDs:[]}),/reachability changed/,'Archives in protected execution closure are re-protected');
 empty.put(`${batch.sourceRoot}/unowned.py`,'# Not a declared archive\n');assert(!empty.collect().excludedPaths.includes(`${batch.sourceRoot}/unowned.py`),'Unknown sibling code does not inherit archival status');
 function broken(change,pattern){const f=archiveFixture(),b=f.addBatch();change(f,b);assert.throws(()=>f.collect(),pattern);}
 broken((f,b)=>f.put(b.generator.path,'# tampered\n'),/SHA-256 mismatch/);
 broken((f,b)=>f.files.delete(b.generator.path),/Missing or unsafe/);
 broken((f,b)=>f.modes.set(b.generator.path,'100755'),/regular mode 100644/);
 broken((f,b)=>f.modes.set(b.generator.path,'120000'),/regular mode 100644/);
 broken((f,b)=>f.modes.set(ARCHIVAL_REGISTRY_PATH,'100755'),/regular mode 100644/);
 broken((f,b)=>{b.descriptor.files[0].owner='unpublished-model';b.sync();},/Unowned/);
 broken((f,b)=>{b.entry.asset_ids=['unpublished-model'];b.sync();},/Unknown or multiply owned/);
 broken((f,b)=>{b.entry.asset_ids.reverse();b.sync();},/unique and sorted/);
 broken((f,b)=>{b.bundle.files[0].source_commit='c'.repeat(40);b.sync();},/origin commit differs/);
 broken((f,b)=>{b.descriptor.files[0].sha256='c'.repeat(64);b.sync();},/differs from pinned source bundle/);
 broken((f,b)=>{b.bundle.files.push(b.bundle.files[0]);b.sync();},/complete source bundle/);
 broken((f,b)=>{b.descriptor.files.push(b.descriptor.files[0]);b.bundle.files.push(b.bundle.files[0]);b.sync();},/Duplicate source-bundle/);
 broken((f,b)=>{b.descriptor.files.pop();b.sync();},/complete source bundle/);
 broken((f,b)=>{b.descriptor.additions[0].review={path:'qa/someone-else/report.json',sha256:'e'.repeat(64)};b.sync();},/outside its owner's review scope|Missing owned review/);
 broken((f,b)=>{b.descriptor.additions[0].candidate.sha256='e'.repeat(64);b.sync();},/SHA-256 mismatch/);
 broken((f,b)=>{b.archive('scripts/validate_candidate.py','# never an archive\n');b.sync();},/bounded source-bundle member/);
 broken((f,b)=>{b.archive('site/viewer.js','// never an archive\n');b.sync();},/bounded source-bundle member/);
 broken((f,b)=>{b.archive('qa/conifer-doc1-integration/harness.mjs','// never an archive\n','review');b.sync();},/bounded source-bundle member/);
 broken((f,b)=>{b.archive('qa/ci-model-proof/harness.mjs','// never an archive\n','review');b.sync();},/bounded source-bundle member/);
 broken((f,b)=>{b.archive(`${b.sourceRoot}/../escape.py`,'# unsafe\n');b.sync();},/bounded source-bundle member/);
 broken((f,b)=>{b.archive('qa/unrelated-policy/harness.py','# unrelated policy\n','review');b.sync();},/outside its owner's review scope/);
 broken((f,b)=>{b.archive('production/unrelated-policy/harness.py','# unrelated policy\n');b.sync();},/outside its owner's source scope/);
 broken((f,b)=>{f.manifest.assets[0].sha256.glb='e'.repeat(64);},/Published glb hash differs/);
 broken((f,b)=>{f.manifest.assets[0].glb='assets/additions/other/model.glb';},/Published glb path differs/);
 broken((f,b)=>{f.put(ARCHIVAL_REGISTRY_PATH,`import "../production/new-four/generator.py"; export const ${ARCHIVAL_REGISTRY_EXPORT} = [];`);},/only exported literal/);
 broken((f,b)=>{b.entry.authorization='self-approved';b.sync();},/unexpected or missing fields/);
 const release=archiveFixture(),releaseBatch=release.addBatch();
 releaseBatch.archive('qa/new-four-release/capture.mjs','throw Error("unreviewed release executable")','release');
 releaseBatch.archive('qa/new-four-release/unknown','unknown release payload','release');
 releaseBatch.archive('qa/new-four-release/capture.log','release output only','release');releaseBatch.sync();
 const releaseInventory=release.collect();assert(!releaseInventory.excludedPaths.includes('qa/new-four-release/capture.mjs'));assert(!releaseInventory.excludedPaths.includes('qa/new-four-release/unknown'));assert(releaseInventory.excludedPaths.includes('qa/new-four-release/capture.log'));
 function rejectMutation(change,pattern){const f=archiveFixture(),b=f.addBatch(),before=f.collect(),beforePaths=[...f.files.keys()];change(f,b);const after=f.collect();assert.throws(()=>assertArchivalAppend(before,after,{beforePaths,oldIDs:b.ids,newIDs:[]}),pattern);}
 rejectMutation((f,b)=>{const row=b.descriptor.files.find(row=>row.path.endsWith('/build.log')),pin=f.put(row.path,'newly edited original\n');row.sha256=pin.sha256;b.bundle.files.find(file=>file.path===row.path).sha256=pin.sha256;b.sync();},/Existing archive declaration/);
 rejectMutation((f,b)=>{b.descriptor.files.find(row=>row.path.endsWith('/build.log')).owner=b.ids[0];b.sync();},/Existing archive declaration/);
 rejectMutation((f,b)=>{f.registry.length=0;f.writeRegistry();},/Existing archive declaration/);
 rejectMutation((f,b)=>{b.descriptor.files=b.descriptor.files.filter(row=>!row.path.endsWith('/build.log'));b.bundle.files=b.bundle.files.filter(row=>!row.path.endsWith('/build.log'));b.sync();},/Existing archive declaration/);
 const existing=archiveFixture();existing.put('production/new-four/generator.py','# Already present before declaration\n');const existingPaths=[...existing.files.keys()],beforeExisting=existing.collect(),newBatch=existing.addBatch();
 assert.throws(()=>assertArchivalAppend(beforeExisting,existing.collect(),{beforePaths:existingPaths,oldIDs:[],newIDs:newBatch.ids}),/Existing code\/data cannot become/);
 const oldModel=archiveFixture(),oldBefore=oldModel.collect(),oldModelPaths=[...oldModel.files.keys()],oldBatch=oldModel.addBatch();
 assert.throws(()=>assertArchivalAppend(oldBefore,oldModel.collect(),{beforePaths:oldModelPaths,oldIDs:[oldBatch.ids[0]],newIDs:oldBatch.ids.slice(1)}),/exclusively/);
 const companionSource='assets/candidates/example-collection/batch-54',companionRoot='production/example-collection/work/batch-54';
 const companion=archiveFixture(),companionBefore=companion.collect(),companionBeforePaths=[...companion.files.keys()],companionBatch=companion.addBatch('companion-four',undefined,{candidateRoot:companionSource});
 const companionProgram=companionBatch.archive(`${companionRoot}/render_exact_glb.py`,'raise RuntimeError("source evidence only")\n');
 companionBatch.archive(`${companionRoot}/concepts/prompt.txt`,'Frozen concept prompt\n');
 companionBatch.archive(`${companionRoot}/runs/result.json`,{status:'recorded'});companionBatch.sync();
 const companionAfter=companion.collect();assert(companionAfter.excludedPaths.includes(companionProgram.path));
 assertArchivalAppend(companionBefore,companionAfter,{beforePaths:companionBeforePaths,oldIDs:[],newIDs:companionBatch.ids});
 assert(!companion.collect([companionProgram.path]).excludedPaths.includes(companionProgram.path),'Consumed companion program is protected');
 companion.put(`${companionRoot}/unlisted.py`,'# unknown sibling\n');assert(!companion.collect().excludedPaths.includes(`${companionRoot}/unlisted.py`));
 for(const path of ['production/example-collection/work/batch-55/archive.py','production/other-collection/work/batch-54/archive.py','production/example-collection/work/archive.py','production/example-collection/other/batch-54/archive.py']){
  const f=archiveFixture(),b=f.addBatch('wrong-companion',undefined,{candidateRoot:companionSource});b.archive(path,'# not owned\n');b.sync();assert.throws(()=>f.collect(),/outside its owner's source scope/);
 }
 const nested=archiveFixture(),nestedBatch=nested.addBatch('nested',undefined,{candidateRoot:companionSource+'/extra'});nestedBatch.archive(`${companionRoot}/archive.py`,'# no partial match\n');nestedBatch.sync();assert.throws(()=>nested.collect(),/outside its owner's source scope/);
 const prior=archiveFixture();prior.put(`${companionRoot}/render_exact_glb.py`,'# pre-existing\n');const priorPaths=[...prior.files.keys()],priorBefore=prior.collect(),priorBatch=prior.addBatch('prior',undefined,{candidateRoot:companionSource});priorBatch.archive(`${companionRoot}/render_exact_glb.py`,'# pre-existing\n');priorBatch.sync();assert.throws(()=>assertArchivalAppend(priorBefore,prior.collect(),{beforePaths:priorPaths,oldIDs:[],newIDs:priorBatch.ids}),/Existing code\/data cannot become/);
 // Memoization belongs to one actual byte snapshot, never a persistent verdict
 // keyed by a mutable worktree path. The existing ownership/pin cases above
 // exercise repeated references to each batch's shared generator and review.
 const memo=archiveFixture(),memoBatch=memo.addBatch('memo-four'),readCounts=new Map();
 const collectMemo=()=>collectArchivalInputs({paths:[...memo.files.keys()],read:path=>{readCounts.set(path,(readCounts.get(path)||0)+1);return Buffer.from(memo.files.get(path));},mode:path=>memo.modes.get(path),manifest:memo.manifest});
 const memoFirst=collectMemo();assert([...readCounts.values()].every(count=>count===1),'Every distinct input is read once in one collection');
 assert.deepEqual(collectMemo(),memoFirst);assert([...readCounts.values()].every(count=>count===2),'A new collection rechecks actual bytes');
 const generatorBytes=memo.files.get(memoBatch.generator.path);memo.files.set(memoBatch.generator.path,Buffer.from(generatorBytes.toString().replace('Preserved','Tampered!')));
 assert.throws(collectMemo,/SHA-256 mismatch/,'Same-length mutation cannot reuse a prior digest');memo.files.set(memoBatch.generator.path,generatorBytes);
 memo.modes.set(memoBatch.generator.path,'100755');assert.throws(collectMemo,/regular mode 100644/,'Mode changes cannot reuse prior verification');memo.modes.set(memoBatch.generator.path,'100644');
 const badJSON=archiveFixture(),badJSONBatch=badJSON.addBatch('bad-json');
 badJSONBatch.entry.descriptor=badJSON.put(badJSONBatch.entry.descriptor.path,'{not valid JSON');badJSON.writeRegistry();
 assert.throws(()=>badJSON.collect(),SyntaxError,'Matching hash does not replace JSON parsing');
 const largeJSON=archiveFixture(),largeJSONBatch=largeJSON.addBatch('large-json');
 largeJSONBatch.entry.descriptor=largeJSON.put(largeJSONBatch.entry.descriptor.path,JSON.stringify(largeJSONBatch.descriptor)+' '.repeat(16*1024*1024));largeJSON.writeRegistry();
 assert.throws(()=>largeJSON.collect(),/Oversized archive JSON/,'JSON retains its separate 16MiB limit');
 console.log('Archive digest memo: one read per path, fresh byte/mode checks, repeated-pin equality, malformed JSON and the 16MiB JSON bound passed.');
 console.log('Companion archives: exact same-collection/batch derivation, complete pins, new ownership and imported-code protection; adjacent/foreign/parent/nested/pre-existing/unlisted paths refused.');
 console.log('Archival source inputs: literal-only registry, exact complete pins, ownership, modes, real append, per-model isolation and protected reachability passed.');
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)runArchivalInputTests();

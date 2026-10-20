/**
 * Exact, owned source-bundle bytes, not execution or publication authority.
 *
 * Only the fixed literal accepted-batch registry can introduce an archive. The
 * caller must run in the independent, clean proof-consumer job, validate the
 * actual delivered inputs, and pass its protected execution dependency closure.
 * These inputs are only read and hashed. Nothing here imports, evaluates or runs
 * an archived program. Publication collector processes must not share this job.
 * Unknown paths/owners/origins remain protected; full publication and candidate
 * validation are separate mandatory gates, unchanged by this classification.
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {parseAst} from 'rollup/parseAst';
import {posix} from 'node:path';
import {authenticatedArchiveInheritance} from './ci-model-proof.mjs';

export const ARCHIVAL_REGISTRY_PATH='site/accepted-bounded-batches.mjs';
export const ARCHIVAL_REGISTRY_EXPORT='ACCEPTED_BOUNDED_BATCHES';
export const ARCHIVAL_REGISTRY_SKELETON=`export const ${ARCHIVAL_REGISTRY_EXPORT} = [];\n`;
const SHA=/^[a-f0-9]{40}$/,HASH=/^[a-f0-9]{64}$/,ID=/^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const MAX_BATCHES=64,MAX_FILES=20000,MAX_JSON_BYTES=16*1024*1024,MAX_FILE_BYTES=128*1024*1024,MAX_TOTAL_BYTES=1024*1024*1024;
const verifiedInventories=new WeakSet(),declarationInventories=new WeakSet(),inheritanceContexts=new WeakMap();
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const regular=mode=>mode==='100644'||mode===0o100644;
const own=(value,key)=>Object.hasOwn(value,key);
const object=value=>value&&typeof value==='object'&&!Array.isArray(value);
const safePath=path=>typeof path==='string'&&/^[A-Za-z0-9_./-]+$/.test(path)&&!path.startsWith('/')&&path.split('/').every(part=>part&&part!=='.'&&part!=='..');
const exactKeys=(value,keys,label)=>{assert(object(value),`${label}: object required`);assert.deepEqual(Object.keys(value).sort(),[...keys].sort(),`${label}: unexpected or missing fields`);};
const safeArchivePath=path=>safePath(path)&&/^(?:production\/[^/]+\/|qa\/[^/]+\/|assets\/candidates\/[^/]+\/)/.test(path)&&!/^qa\/(?:conifer-doc1-integration|ci-[^/]+)\//.test(path);
const executionSuffix=/\.(?:mjs|cjs|js|jsx|ts|tsx|py|pyc|pyo|sh|bash|ps1|wasm|html|htm)$/i;
function freeze(value){if(value&&typeof value==='object'){for(const child of Object.values(value))freeze(child);Object.freeze(value);}return value;}
function pin(value,label){exactKeys(value,['path','sha256'],label);assert(safePath(value.path),`${label}: unsafe path`);assert(HASH.test(value.sha256||''),`${label}: exact SHA-256 required`);}
function sortedIDs(ids,label){assert(Array.isArray(ids)&&ids.length&&ids.every(id=>typeof id==='string'&&ID.test(id)),`${label}: nonempty valid IDs required`);assert.deepEqual(ids,[...new Set(ids)].sort(),`${label}: IDs must be unique and sorted`);}

/** Parse only JSON-shaped exported const data. No source is ever evaluated. */
export function parseStaticPublicationExports(source,{label='Accepted data module'}={}){
 assert(typeof source==='string'&&Buffer.byteLength(source)<=MAX_JSON_BYTES,`${label}: oversized module`);
 const tree=parseAst(source),out={};
 let count=0;
 function literal(node,depth=0){
  assert(node&&depth<=64&&++count<=500000,`${label}: invalid or excessive literal data`);
  if(node.type==='Literal'){
   assert(node.value===null||typeof node.value==='boolean'||typeof node.value==='string'||typeof node.value==='number'&&Number.isFinite(node.value),`${label}: unsupported literal`);
   assert(!node.regex&&!own(node,'bigint'),`${label}: executable/non-JSON literal`);return node.value;
  }
  if(node.type==='UnaryExpression'&&node.operator==='-'&&node.argument.type==='Literal'&&typeof node.argument.value==='number'&&Number.isFinite(node.argument.value))return -node.argument.value;
  if(node.type==='ArrayExpression')return node.elements.map(element=>literal(element,depth+1));
  assert.equal(node.type,'ObjectExpression',`${label}: only literal data is allowed`);
  const result={};
  for(const property of node.properties){
   assert(property.type==='Property'&&property.kind==='init'&&!property.computed&&!property.method&&!property.shorthand,`${label}: executable/computed property`);
   const key=property.key.type==='Identifier'?property.key.name:property.key.type==='Literal'&&typeof property.key.value==='string'?property.key.value:null;
   assert(typeof key==='string'&&!['__proto__','prototype','constructor'].includes(key)&&!own(result,key),`${label}: unsafe or duplicate property`);
   Object.defineProperty(result,key,{value:literal(property.value,depth+1),enumerable:true});
  }
  return result;
 }
 for(const statement of tree.body){
  assert(statement.type==='ExportNamedDeclaration'&&!statement.source&&statement.specifiers.length===0&&statement.declaration?.type==='VariableDeclaration'&&statement.declaration.kind==='const',`${label}: only exported literal constants are allowed`);
  for(const declaration of statement.declaration.declarations){
   assert(declaration.id.type==='Identifier'&&!own(out,declaration.id.name),`${label}: duplicate or indirect export`);
   Object.defineProperty(out,declaration.id.name,{value:literal(declaration.init),enumerable:true});
  }
 }
 assert(Object.keys(out).length,`${label}: missing literal exports`);
 return freeze(out);
}

/**
 * read(path) must return exact bytes and reject symlink components. mode(path)
 * must describe the same inventory snapshot (git 100644 or lstat 0100644).
 * protectedPaths is the execution closure, NOT every conservatively code-shaped
 * path: otherwise source-bundle programs could never qualify as inert archives.
 */
export function collectArchivalDeclarations(options){
 assert(!options.inheritance,'Declaration parsing cannot consume an inheritance capability');
 return collect(options,{declarationsOnly:true});
}

/**
 * This is an internal immutable-tree bridge, not an authorization factory.
 * The protected proof verifier must independently authenticate the source proof
 * before its process-local resolver will return this exact snapshot context.
 * Ordinary objects, declaration JSON and caller-supplied object IDs cannot mint
 * the opaque collector capability.
 */
export function prepareArchivalInheritance(context){
 const trusted=authenticatedArchiveInheritance(context);
 assert(object(trusted)&&declarationInventories.has(trusted.before),'Archive inheritance requires authenticated declaration inventory');
 const {before,beforeIdentities,afterIdentities,options}=trusted;
 assert(beforeIdentities instanceof Map&&afterIdentities instanceof Map,'Archive inheritance requires exact immutable object inventories');
 assert(object(options)&&Array.isArray(options.paths)&&typeof options.read==='function'&&typeof options.mode==='function','Archive inheritance requires an exact immutable source binding');
 const after=trusted.after??collectArchivalDeclarations(options);
 assert(declarationInventories.has(after),'Archive inheritance requires an authenticated current declaration inventory');
 const afterChecked=new Map(after.checkedInputs.map(row=>[row.path,row]));
 const oldIDs=before.modelIDs,newIDs=after.modelIDs.filter(id=>!oldIDs.includes(id));
 assertArchivalAppendStructure(before,after,{beforePaths:before.repositoryPaths,oldIDs,newIDs});
 for(const input of before.checkedInputs){
  // The literal registry may append new entries; the exact old declarations are
  // preserved by the structural append comparison above, not its whole blob.
  if(input.path===ARCHIVAL_REGISTRY_PATH)continue;
  const previous=beforeIdentities.get(input.path),current=afterIdentities.get(input.path);
  assert(previous&&current&&SHA.test(previous.oid||'')&&previous.type==='blob'&&regular(previous.mode),`Missing or invalid immutable archive identity: ${input.path}`);
  assert(current.oid===previous.oid&&current.mode===previous.mode&&current.type===previous.type,`Existing immutable archive input changed: ${input.path}`);
  const declared=afterChecked.get(input.path);
  assert(declared&&declared.sha256===input.sha256&&declared.document===input.document&&declared.final===input.final,`Existing archive checked pin changed: ${input.path}`);
 }
 const oldChecked=new Map(before.checkedInputs.map(row=>[row.path,row])),skip=new Map();
 for(const row of before.files){
  const input=oldChecked.get(row.path);
  assert(input,`Missing immutable archive checked pin: ${row.path}`);
  if(row.excluded&&!input.document&&!input.final)skip.set(row.path,{sha256:input.sha256,bytes:input.bytes});
 }
 const token=Object.freeze({});
 inheritanceContexts.set(token,{before,after,options,paths:[...options.paths],protectedPaths:[...(options.protectedPaths||[])],manifest:JSON.stringify(options.manifest),skip});
 return token;
}

export function collectArchivalInputs(options){
 let inherited=null;
 if(options.inheritance!==undefined){
  inherited=inheritanceContexts.get(options.inheritance);
  assert(inherited,'Archive inheritance requires an authenticated process-local capability');
  for(const field of ['paths','read','mode','manifest','protectedPaths','prefetch'])assert.equal(options[field],inherited.options[field],`Archive inheritance has a different ${field} binding`);
  assert.deepEqual(options.paths,inherited.paths,'Archive inheritance source paths changed');
  assert.deepEqual([...(options.protectedPaths||[])],inherited.protectedPaths,'Archive inheritance execution protection changed');
  assert.equal(JSON.stringify(options.manifest),inherited.manifest,'Archive inheritance model manifest changed');
 }
 return collect(options,{inherited});
}

function collect({paths,read,mode,manifest,protectedPaths=[],onWorkUnit,prefetch},{declarationsOnly=false,inherited=null}={}){
 assert(Array.isArray(paths)&&new Set(paths).size===paths.length,'Archive inventory must contain unique repository paths');
 assert(onWorkUnit===undefined||typeof onWorkUnit==='function','Archive work-unit observer must be a function');
 assert(prefetch===undefined||typeof prefetch==='function','Archive prefetch must be a function');
 // Only exact-byte summaries survive a read. The default mutable collection has
 // no cross-call cache; immutable substitution requires the private capability.
 const available=new Set(paths),protectedSet=new Set(protectedPaths),cache=new Map(),documents=new Map(),checkedInputs=new Map();
 let unit={batches:0,inputs:0,bytes:0},batchUsage=null,unitIndex=0;
 const finishUnit=()=>{if(unit.inputs||unit.batches){onWorkUnit?.(Object.freeze({index:unitIndex++,...unit}));unit={batches:0,inputs:0,bytes:0};}};
 const account=(bytes)=>{
  const usage=batchUsage||unit;usage.inputs++;usage.bytes+=bytes;
  assert(usage.inputs<=MAX_FILES,'Archive batch exceeds fresh input bound');
  assert(usage.bytes<=MAX_TOTAL_BYTES,'Archive batch exceeds fresh byte bound');
 };
 const finishBatch=()=>{
  assert(batchUsage&&batchUsage.batches===1,'Archive batch accounting is incomplete');
  if(unit.batches+1>MAX_BATCHES||unit.inputs+batchUsage.inputs>MAX_FILES||unit.bytes+batchUsage.bytes>MAX_TOTAL_BYTES)finishUnit();
  unit.batches++;unit.inputs+=batchUsage.inputs;unit.bytes+=batchUsage.bytes;batchUsage=null;
 };
 const checkPath=path=>{
  assert(safePath(path)&&available.has(path),`Missing or unsafe archive input: ${path}`);
  assert(typeof mode==='function'&&regular(mode(path)),`Archive input is not regular mode 100644: ${path}`);
 };
 // Optional immutable-source I/O batching only. Prefetch cannot certify a pin,
 // change the fresh-work counters, or replace the mandatory read/hash below.
 const warm=paths=>{
  if(!prefetch)return;
  const unique=[...new Set(paths)].filter(path=>!cache.has(path));
  for(const path of unique)checkPath(path);
  if(unique.length)prefetch(unique);
 };
 const record=(path,summary,{document=false,final=false}={})=>{
  const previous=checkedInputs.get(path);
  if(previous)assert.equal(summary.sha256,previous.sha256,`Conflicting archive pins: ${path}`);
  checkedInputs.set(path,{path,...summary,document:document||!!previous?.document,final:final||!!previous?.final});
 };
 const checkedBytes=path=>{
  checkPath(path);
  const value=read(path);assert(Buffer.isBuffer(value)||typeof value==='string',`Archive input bytes required: ${path}`);
  const bytes=Buffer.isBuffer(value)?value:Buffer.from(value);assert(bytes.length<=MAX_FILE_BYTES,`Oversized archive input: ${path}`);
  const summary={sha256:hash(bytes),bytes:bytes.length},previous=cache.get(path);
  if(!previous||previous.bytes===null){
   if(previous)assert.equal(summary.sha256,previous.sha256,`Archive SHA-256 mismatch: ${path}`);
   account(bytes.length);cache.set(path,summary);
  }else assert.deepEqual(summary,previous,`Archive input changed during collection: ${path}`);
  record(path,summary);return bytes;
 };
 const checked=(entry,{final=false}={})=>{
  pin(entry,'Archive pin');checkPath(entry.path);
  if(!cache.has(entry.path)){
   const old=inherited?.skip.get(entry.path);
   if(declarationsOnly||old&&!final&&!protectedSet.has(entry.path)){
    if(old)assert.equal(entry.sha256,old.sha256,`Inherited archive pin changed: ${entry.path}`);
    cache.set(entry.path,{sha256:entry.sha256,bytes:null});
   }else checkedBytes(entry.path);
  }
  // A pin that also refers to delivered content is always read, even if first
  // encountered as an inert bundle member in another declaration.
  if(final&&!declarationsOnly&&cache.get(entry.path).bytes===null)checkedBytes(entry.path);
  const summary=cache.get(entry.path);assert.equal(summary.sha256,entry.sha256,`Archive SHA-256 mismatch: ${entry.path}`);
  record(entry.path,summary,{final});return summary;
 };
 const json=entry=>{
  pin(entry,'Archive pin');
  if(documents.has(entry.path)){checked(entry);return documents.get(entry.path);}
  const bytes=checkedBytes(entry.path);checked(entry);record(entry.path,cache.get(entry.path),{document:true});
  assert(bytes.length<=MAX_JSON_BYTES,`Oversized archive JSON: ${entry.path}`);
  const value=JSON.parse(bytes);documents.set(entry.path,value);return value;
 };
 let registry=[];
 if(available.has(ARCHIVAL_REGISTRY_PATH)){
  const exports=parseStaticPublicationExports(checkedBytes(ARCHIVAL_REGISTRY_PATH).toString(),{label:ARCHIVAL_REGISTRY_PATH});
  assert.deepEqual(Object.keys(exports),[ARCHIVAL_REGISTRY_EXPORT],'Archive registry has unexpected exports');
  registry=exports[ARCHIVAL_REGISTRY_EXPORT];assert(Array.isArray(registry),'Invalid bounded-batch registry');
  record(ARCHIVAL_REGISTRY_PATH,cache.get(ARCHIVAL_REGISTRY_PATH),{document:true});
 }
 const models=new Map((manifest?.assets||[]).map(row=>[row.id,row])),modelIDs=new Set(models.keys()),claimedIDs=new Set(),claimedPaths=new Set(),descriptors=new Set(),batches=[],rows=[];
 if(registry.length){assert(Array.isArray(manifest?.assets)&&modelIDs.size===manifest.assets.length,'Archive owners require a unique model manifest');}
 for(const entry of registry){
  batchUsage={batches:1,inputs:0,bytes:0};
  exactKeys(entry,['descriptor','asset_ids','source_commit','independent_review_commit'],'Accepted archive batch');
  pin(entry.descriptor,'Accepted descriptor');assert(/^assets\/releases\/[^/]+\.json$/.test(entry.descriptor.path),'Archive descriptor must be a direct release descriptor');
  assert(!descriptors.has(entry.descriptor.path),'Duplicate archive descriptor');descriptors.add(entry.descriptor.path);
  sortedIDs(entry.asset_ids,'Archive batch owners');assert(entry.asset_ids.length<=64,'Archive batch owner bound exceeded');
  for(const id of entry.asset_ids){assert(modelIDs.has(id)&&!claimedIDs.has(id),`Unknown or multiply owned archive model: ${id}`);claimedIDs.add(id);}
  assert(SHA.test(entry.source_commit||'')&&SHA.test(entry.independent_review_commit||''),'Exact source and independent-review commits required');
  const descriptor=json(entry.descriptor);assert(object(descriptor),'Archive descriptor object required');
  assert(Array.isArray(descriptor.additions)&&descriptor.additions.length===entry.asset_ids.length,'Archive additions must match exact batch owners');
  assert.deepEqual(descriptor.additions.map(row=>row.id).sort(),entry.asset_ids,'Archive additions differ from exact batch owners');
  if(prefetch){
   pin(descriptor.source_bundle,'Accepted source bundle');assert(/^(?:qa|production)\/[^/]+\/source-bundle\.json$/.test(descriptor.source_bundle.path),'Source bundle must have a bounded canonical path');
   const nextPaths=[descriptor.source_bundle.path];
   for(const addition of descriptor.additions){
    assert(typeof addition.revision==='string'&&/^r[0-9]{3}$/.test(addition.revision),`Archive revision required: ${addition.id}`);
    pin(addition.candidate,`Archive candidate: ${addition.id}`);pin(addition.metadata,`Published metadata: ${addition.id}`);
    const suffix=`/${addition.id}/${addition.revision}/candidate.json`;
    assert(safeArchivePath(addition.candidate.path)&&addition.candidate.path.endsWith(suffix),`Candidate is outside its exact model/revision: ${addition.id}`);
    assert(/^(?:production\/[^/]+|assets\/candidates\/[^/]+)(?:\/[^/]+)*$/.test(addition.candidate.path.slice(0,-suffix.length)),`Candidate source scope is not bounded: ${addition.id}`);
    assert(addition.metadata.path.startsWith(`assets/additions/${addition.id}/`)&&addition.metadata.path.endsWith('/release-metadata.json'),`Published metadata has no exact model owner: ${addition.id}`);
    nextPaths.push(addition.candidate.path,addition.metadata.path);
    if(!declarationsOnly){
     const model=models.get(addition.id);
     for(const kind of ['glb','blend','preview']){pin({path:model[kind],sha256:model.sha256?.[kind]},`Published ${kind}: ${addition.id}`);nextPaths.push(model[kind]);}
    }
   }
   warm(nextPaths);
  }
  const scopes=new Map();
  for(const addition of descriptor.additions){
   assert(typeof addition.revision==='string'&&/^r[0-9]{3}$/.test(addition.revision),`Archive revision required: ${addition.id}`);
   pin(addition.candidate,`Archive candidate: ${addition.id}`);pin(addition.review,`Archive independent review: ${addition.id}`);
   assert(safeArchivePath(addition.candidate.path)&&safeArchivePath(addition.review.path),`Archive evidence must remain in bounded source/QA namespaces: ${addition.id}`);
   const suffix=`/${addition.id}/${addition.revision}/candidate.json`;
   assert(addition.candidate.path.endsWith(suffix),`Candidate is outside its exact model/revision: ${addition.id}`);
   const sourceRoot=addition.candidate.path.slice(0,-suffix.length),sourceRoots=new Set([sourceRoot]);
   assert(/^(?:production\/[^/]+|assets\/candidates\/[^/]+)(?:\/[^/]+)*$/.test(sourceRoot),`Candidate source scope is not bounded: ${addition.id}`);
   // Frozen candidate batches may preserve shared concepts, diagnostic source
   // and run records in the matching production work batch. Derive this one
   // companion scope from the complete candidate root, never a descriptor root.
   // Membership is still exact, hash-pinned, source-owned and append-only below.
   const companion=/^assets\/candidates\/([^/]+)\/(batch-[0-9]+)$/.exec(sourceRoot);
   if(companion)sourceRoots.add(`production/${companion[1]}/work/${companion[2]}`);
   const reviewRoot=posix.dirname(addition.review.path);
   assert(safeArchivePath(`${reviewRoot}/member`)&&reviewRoot!=='qa/independent',`Independent-review scope is not bounded: ${addition.id}`);
   const candidate=json(addition.candidate);assert.equal(candidate.asset_id,addition.id,`Candidate model differs: ${addition.id}`);assert.equal(candidate.revision,addition.revision,`Candidate revision differs: ${addition.id}`);
   pin(addition.metadata,`Published metadata: ${addition.id}`);
   assert(addition.metadata.path.startsWith(`assets/additions/${addition.id}/`)&&addition.metadata.path.endsWith('/release-metadata.json'),`Published metadata has no exact model owner: ${addition.id}`);
   const metadata=json(addition.metadata),model=models.get(addition.id);assert.equal(metadata.id,addition.id,`Metadata model differs: ${addition.id}`);
   if(prefetch&&!declarationsOnly){
    pin(candidate.artifacts?.glb,`Candidate GLB: ${addition.id}`);
    assert.equal(candidate.artifacts.glb.sha256,model.sha256.glb,`Candidate GLB differs from published model: ${addition.id}`);
    const artifactPaths=[];
    for(const kind of ['glb','source','generator','config'])if(candidate.artifacts?.[kind]){
     const artifact=candidate.artifacts[kind];pin(artifact,`Candidate ${kind}: ${addition.id}`);
     if(!inherited?.skip.has(artifact.path)||protectedSet.has(artifact.path))artifactPaths.push(artifact.path);
    }
    warm(artifactPaths);
   }
   for(const kind of ['glb','blend','preview']){
    assert.equal(metadata[kind],model[kind],`Published ${kind} path differs: ${addition.id}`);
    assert.equal(metadata.sha256?.[kind],model.sha256?.[kind],`Published ${kind} hash differs: ${addition.id}`);
    checked({path:metadata[kind],sha256:metadata.sha256?.[kind]},{final:true});
   }
   pin(candidate.artifacts?.glb,`Candidate GLB: ${addition.id}`);
   assert.equal(candidate.artifacts.glb.sha256,model.sha256.glb,`Candidate GLB differs from published model: ${addition.id}`);checked(candidate.artifacts.glb);
   // Extra preserved candidate trees may accompany a source-scope generator.
   // Derive those scopes only from exact hash-checked frozen artifact pins, never
   // from a directory or an executable extension supplied as an exemption.
   for(const kind of ['source','generator','config'])if(candidate.artifacts?.[kind]){
    const artifact=candidate.artifacts[kind];pin(artifact,`Candidate ${kind}: ${addition.id}`);checked(artifact);
    const scope=/^(production\/[^/]+|assets\/candidates\/[^/]+)\//.exec(artifact.path)?.[1];
    assert(scope,`Candidate ${kind} has no bounded source scope: ${addition.id}`);sourceRoots.add(scope);
   }
   if(addition.source_commit!==undefined)assert.equal(addition.source_commit,entry.source_commit,'Addition source commit differs from batch');
   if(addition.review_commit!==undefined)assert.equal(addition.review_commit,entry.independent_review_commit,'Addition review commit differs from batch');
   scopes.set(addition.id,{source:[...sourceRoots],review:[reviewRoot],candidate,metadata:addition.metadata});
  }
  pin(descriptor.source_bundle,'Accepted source bundle');assert(/^(?:qa|production)\/[^/]+\/source-bundle\.json$/.test(descriptor.source_bundle.path),'Source bundle must have a bounded canonical path');
  const bundle=json(descriptor.source_bundle);
  assert(object(bundle)&&bundle.version===1&&Array.isArray(bundle.files)&&bundle.files.length&&bundle.files.length<=MAX_FILES,'Invalid source-bundle inventory');
  assert(Array.isArray(descriptor.files)&&descriptor.files.length===bundle.files.length,'Archive descriptor must cover the complete source bundle');
  const bundleFiles=new Map();
  for(const file of bundle.files){
   assert(object(file)&&safeArchivePath(file.path)&&HASH.test(file.sha256||''),'Invalid bounded source-bundle member');
   assert(!bundleFiles.has(file.path),'Duplicate source-bundle member');bundleFiles.set(file.path,file);
  }
  const batchRows=[];
  for(const file of descriptor.files){
   exactKeys(file,['path','sha256','origin','owner'],'Archive member');assert(safeArchivePath(file.path),'Archive member is outside source/QA namespaces');
   assert(HASH.test(file.sha256||''),'Archive member needs exact SHA-256');
   assert(!claimedPaths.has(file.path),'Duplicate archive member across batches');claimedPaths.add(file.path);
   assert(['source','review','release'].includes(file.origin),'Unknown archive origin');
   const owners=file.owner==='$batch'?[...entry.asset_ids]:[file.owner];assert(owners.every(id=>entry.asset_ids.includes(id)),'Unowned archive member');
   for(const id of owners){const roots=file.origin==='release'?[posix.dirname(descriptor.source_bundle.path)]:scopes.get(id)[file.origin];assert(roots.some(root=>file.path.startsWith(`${root}/`)),`Archive member is outside its owner's ${file.origin} scope: ${file.path}`);}
   const original=bundleFiles.get(file.path);assert(original&&original.sha256===file.sha256,`Archive member differs from pinned source bundle: ${file.path}`);
   // This binds the accepted source/review commit claim. It does not claim that
   // a historical Git object was fetched or independently reconstructed here.
   if(file.origin!=='release')assert.equal(original.source_commit,file.origin==='source'?entry.source_commit:entry.independent_review_commit,`Archive origin commit differs: ${file.path}`);
   // A release-authored program has no immutable source/review provenance. It
   // remains a shared execution input, even if listed in an otherwise valid bundle.
   const excluded=!protectedSet.has(file.path)&&(file.origin!=='release'||!executionSuffix.test(file.path)&&/\.(?:json|jsonl|md|txt|log|lock|sha256|png|webp|jpg|jpeg|glb|blend)$/.test(file.path));
   checked({path:file.path,sha256:file.sha256});
   const row={path:file.path,sha256:file.sha256,origin:file.origin,owners,source_commit:file.origin==='release'?null:original.source_commit,descriptor:entry.descriptor.path,excluded};
   rows.push(row);batchRows.push(row);
  }
  assert.deepEqual([...new Set(descriptor.files.map(file=>file.path))].sort(),[...bundleFiles.keys()].sort(),'Source-bundle member coverage is not exact');
  // Pinned candidate and review evidence must actually belong to this exact
  // bundle and this model, not merely share a convenient directory prefix.
  for(const addition of descriptor.additions)for(const [role,evidence]of [['candidate',addition.candidate],['review',addition.review]]){
   const row=batchRows.find(row=>row.path===evidence.path);assert(row&&row.sha256===evidence.sha256&&row.owners.includes(addition.id),`Missing owned ${role} in archive bundle: ${addition.id}`);
   assert.equal(row.origin,role==='candidate'?'source':'review',`Wrong ${role} archive origin: ${addition.id}`);
  }
  for(const addition of descriptor.additions)for(const kind of ['glb','source','generator','config'])if(scopes.get(addition.id).candidate.artifacts?.[kind]){
   const evidence=scopes.get(addition.id).candidate.artifacts[kind],row=batchRows.find(row=>row.path===evidence.path);
   assert(row&&row.sha256===evidence.sha256&&row.owners.includes(addition.id)&&row.origin==='source',`Candidate ${kind} is not an owned exact source-bundle member: ${addition.id}`);
  }
  batches.push({descriptor:entry.descriptor,asset_ids:entry.asset_ids,source_commit:entry.source_commit,independent_review_commit:entry.independent_review_commit,source_bundle:descriptor.source_bundle,files:batchRows.map(({excluded,...rest})=>rest)});
  // Parsed descriptors/candidates are only needed while validating this batch.
  documents.clear();finishBatch();
 }
 finishUnit();
 rows.sort((a,b)=>a.path.localeCompare(b.path));batches.sort((a,b)=>a.descriptor.path.localeCompare(b.descriptor.path));
 const byModel={};for(const batch of batches)for(const id of batch.asset_ids)byModel[id]={descriptor:batch.descriptor,source_bundle:batch.source_bundle,files:batch.files.filter(row=>row.owners.includes(id))};
 const result=freeze({version:1,registry,registryPath:ARCHIVAL_REGISTRY_PATH,registrySkeleton:ARCHIVAL_REGISTRY_SKELETON,registryMasked:available.has(ARCHIVAL_REGISTRY_PATH)&&!protectedSet.has(ARCHIVAL_REGISTRY_PATH),repositoryPaths:[...paths],modelIDs:[...modelIDs].sort(),excludedPaths:rows.filter(row=>row.excluded).map(row=>row.path),files:rows,batches,byModel,checkedInputs:[...checkedInputs.values()].sort((a,b)=>a.path.localeCompare(b.path))});
 if(inherited){
  assert.deepEqual(result.batches,inherited.after.batches,'Immutable archive declarations changed during collection');
  assert.deepEqual(result.files,inherited.after.files,'Immutable archive protection changed during collection');
  verifiedInventories.add(inherited.before);
 }
 if(declarationsOnly)declarationInventories.add(result);else verifiedInventories.add(result);
 return result;
}

/** Only new batch IDs and genuinely new paths may gain archival classification. */
export function assertArchivalAppend(before,after,{beforePaths,oldIDs,newIDs}){
 assert(verifiedInventories.has(before)&&verifiedInventories.has(after),'Archive append requires independently verified inventories, never JSON self-approval');
 return assertArchivalAppendStructure(before,after,{beforePaths,oldIDs,newIDs});
}
function assertArchivalAppendStructure(before,after,{beforePaths,oldIDs,newIDs}){
 const existingPaths=new Set(beforePaths),oldModels=new Set(oldIDs),newModels=new Set(newIDs);
 assert([...newModels].every(id=>!oldModels.has(id)),'Archive old/new owner sets overlap');
 const afterBatches=new Map(after.batches.map(batch=>[batch.descriptor.path,batch])),beforeBatches=new Map(before.batches.map(batch=>[batch.descriptor.path,batch]));
 for(const batch of before.batches){assert.deepEqual(afterBatches.get(batch.descriptor.path),batch,`Existing archive declaration/pins/owners changed: ${batch.descriptor.path}`);}
 for(const batch of after.batches){
  if(beforeBatches.has(batch.descriptor.path))continue;
  assert(!existingPaths.has(batch.descriptor.path)&&!existingPaths.has(batch.source_bundle.path),'An existing descriptor or bundle cannot self-reclassify as a new archive');
  assert(batch.asset_ids.every(id=>newModels.has(id)&&!oldModels.has(id)),'New archives must belong exclusively to independently identified added models');
  for(const file of batch.files)assert(!existingPaths.has(file.path),`Existing code/data cannot become an archive: ${file.path}`);
 }
 const beforeFiles=new Map(before.files.map(file=>[file.path,file]));
 for(const file of after.files)if(beforeFiles.has(file.path))assert.deepEqual(file,beforeFiles.get(file.path),`Existing archive execution reachability changed: ${file.path}`);
 return after.excludedPaths;
}

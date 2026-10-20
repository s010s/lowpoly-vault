/** Content-addressed strict-GPU evidence. Catalog membership is never a cache key. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync,readdirSync,lstatSync,realpathSync,existsSync,mkdtempSync,writeFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {resolve,dirname,relative,sep,join} from 'node:path';
import {parseAst} from 'rollup/parseAst';
import {execFileSync} from 'node:child_process';
import {validateCatalogData,catalogDataForAsset} from './curation.js';
import {createCatalog} from './catalog-build.mjs';
import {writeStaticRoutes} from './static-routes.mjs';
import {enrichManifest,creditText} from './asset-delivery.mjs';
import {collectTurntables,publishedImagePaths} from './turntable-delivery.mjs';
import {payloadDigest} from './ci-model-shards.mjs';
import {CARD_RENDER_PRESET} from './render-preset.js';
import {assertCardPreviewRecord} from './ci-card-preview-proof.mjs';
import {collectArchivalInputs,assertArchivalAppend,ARCHIVAL_REGISTRY_PATH} from './ci-archival-inputs.mjs';

export const MODEL_PROOF_VERSION=2;
export const MODEL_PROOF_FILE='model-proof.json';
export const MODEL_PROOF_WORKFLOW='.github/workflows/full-release-review.yml';
export const PINNED_BROWSER={playwright:'1.56.1',chromium:'141.0.7390.37',revision:'1194'};
export const GPU_POLICY={version:2,profile:'strict-gpu',scope:'models',browser:PINNED_BROWSER,
  args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'],
  viewport:{width:1440,height:1000},reducedMotion:'reduce',fallback:false};
// Fixed publication-only inventory, not a filename convention a candidate can join.
// New release modules, arbitrary qa code, proof producers/verifiers and workflow
// changes remain protected. A real render/build/harness import promotes any listed
// module back into the protected dependency closure. Publication gates still run.
const releaseNames=['initial','refined','small-life','small-fauna','small-life-batch',
  'small-life-round02','small-life-round03','small-life-round04','small-life-round05',
  'small-life-round06','small-life-round07','small-life-round08','small-life-round09',
  'small-life-round10','small-life-round11','small-life-round12','small-life-round13',
  'concept-seven','concept-quartets','concept-landair'];
export const PUBLICATION_ONLY_MODULES=Object.freeze([
  ...releaseNames.flatMap(name=>[`site/${name}-release.mjs`,`site/${name}-release-test.mjs`]),
  ...['02','03','04','05','06','07','08','09','10','11','12','13'].map(round=>`site/accepted-round${round}-release.mjs`),
  'site/accepted-small-life-batch-data.mjs','site/accepted-concept-seven-release.mjs',
  'site/accepted-concept-quartets-release.mjs','site/accepted-concept-landair-release.mjs',
  'site/accepted-landair-capture.mjs','site/accepted-quartets-capture.mjs'
]);
const publicationOnly=new Set(PUBLICATION_ONLY_MODULES);
export const isPublicationOnlyModelPath=path=>publicationOnly.has(path);
export const EXECUTED_QA_ROOTS=['qa/conifer-doc1-integration/'];
// Protect the entire historical QA directory's bytes, but traverse imports only
// from the exact command CI executes. Its old review-only assembly is not run by
// any proof producer; importing it from an executed root still promotes it.
export const EXECUTED_QA_ENTRYPOINTS=Object.freeze(['qa/conifer-doc1-integration/conifer-handoff-browser-test.mjs']);
// Cache producers and independent consumers, including the unit-contract
// programs run before GPU/card production. Unrelated matrix jobs have their own
// isolated runners and do not produce this evidence. Publication processes must
// not execute on the gallery/model/card producer or aggregate runner.
export const MODEL_PROOF_ENTRYPOINTS=Object.freeze(['vite.config.js','site/copy-assets.mjs','site/capture-gallery-posters.mjs','site/redesign-browser-test.mjs',
  'site/ci-clean-gallery.mjs','site/ci-review.mjs','site/render-web-previews.mjs','site/ci-incremental-models.mjs','site/gallery-assets.mjs',
  'site/ci-model-proof.mjs','site/ci-model-cache.mjs','site/ci-model-shards.mjs','site/ci-card-preview-proof.mjs',
  'site/gallery-poster-inputs.mjs','site/gallery-poster-proof.mjs','site/gallery-poster-cache.mjs','site/gallery-poster-orchestration.mjs',
  'site/ci-provenance.mjs','site/ci-timed.mjs','site/ci-scene-browser-test.mjs',
  ...['catalog-data','ci-card-preview-proof','ci-model-proof','ci-model-cache','ci-incremental-models','ci-scope','ci-model-shards','ci-timed','ci-scene-input','ci-archival-inputs','ci-clean-gallery','ci-archival-models'].map(name=>`site/${name}-test.mjs`)]);
const POLICY_ROOTS=['site','.github','scripts','schemas','qa','package.json','package-lock.json','vite.config.js'];
const verifiedBuiltInputs=new WeakSet();
const HASH=/^[a-f0-9]{64}$/,SHA=/^[a-f0-9]{40}$/,ID=/^[a-z0-9-]+$/;
export const hashBytes=value=>createHash('sha256').update(value).digest('hex');
export const canonical=value=>value&&typeof value==='object'?(Array.isArray(value)?value.map(canonical):Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])]))):value;
export const hashObject=value=>hashBytes(JSON.stringify(canonical(value)));
const safePath=path=>typeof path==='string'&&!/[\\\u0000-\u001f?#%:]/.test(path)&&!path.startsWith('/')&&path.split('/').every(part=>part&&part!=='.'&&part!=='..');
function bytes(root,path){
  assert(safePath(path),`Unsafe input path: ${path}`);
  const full=resolve(root,path);assert.equal(realpathSync(full),full,`Input symlink rejected: ${path}`);
  assert(lstatSync(full).isFile(),`Input is not a regular file: ${path}`);return readFileSync(full);
}
const json=(root,path)=>JSON.parse(bytes(root,path));
function files(root,path){
  if(!existsSync(resolve(root,path)))return [];
  const full=resolve(root,path),stat=lstatSync(full);assert(!stat.isSymbolicLink(),`Input symlink rejected: ${path}`);
  if(stat.isFile())return [path];assert(stat.isDirectory());
  return readdirSync(full).sort().flatMap(name=>files(root,`${path}/${name}`));
}
export function protectedModelPath(path){
  if(publicationOnly.has(path))return false;
  return /^(?:\.github\/|scripts\/|schemas\/)/.test(path)||/^(?:package(?:-lock)?\.json|vite\.config\.js)$/.test(path)||
    /^site\/.*\.(?:mjs|cjs|js|css|html)$/.test(path)||/^(?:qa|production|assets)\/.*\.(?:mjs|cjs|js|jsx|ts|tsx|py|sh|bash|ps1|wasm)$/.test(path)||EXECUTED_QA_ROOTS.some(prefix=>path.startsWith(prefix));
}
// Parse executable imports instead of assuming that an authorization filename
// cannot execute during rendering. Package contents are bound by the lockfile;
// local data imports are returned too, so they can enter shared/per-model inputs.
export function modelExecutionDependencies(paths,read){
  const available=new Set(paths),found=new Set();
  function visit(path){
    if(found.has(path))return;
    assert(available.has(path),`Missing render dependency: ${path}`);found.add(path);
    if(!/\.(?:mjs|cjs|js)$/.test(path))return;
    const tree=parseAst(read(path).toString());
    const requireNames=new Set(['require']),factoryNames=new Set(),moduleNames=new Set(['module']);
    // createRequire aliases are valid only when anchored to this exact module.
    // Unknown factories/indirection must not conceal an authorization dependency.
    function nodes(node,fn,parent=null){if(!node||typeof node!=='object')return;fn(node,parent);for(const value of Object.values(node)){if(Array.isArray(value))for(const child of value)nodes(child,fn,node);else if(value&&typeof value==='object')nodes(value,fn,node);}}
    // The card producer loads precisely the independently sealed dist viewer in
    // a browser callback. This is NOT a general computed-import exemption: only
    // this complete audited page.evaluate call AST, on this exact protected
    // source path, qualifies. Any callback/argument change requires review of
    // this protected policy. Every other computed import is still refused.
    const builtImports=new WeakSet(),builtImportIdentifiers=new WeakSet();
    const semantic=node=>Array.isArray(node)?node.map(semantic):node&&typeof node==='object'?Object.fromEntries(Object.entries(node).filter(([key])=>key!=='start'&&key!=='end').map(([key,value])=>[key,semantic(value)])):node;
    if(path==='site/render-web-previews.mjs')nodes(tree,node=>{
      if(node.type==='CallExpression'&&node.callee?.type==='MemberExpression'&&!node.callee.computed&&node.callee.object?.name==='page'&&node.callee.property?.name==='evaluate'&&hashBytes(JSON.stringify(semantic(node)))==='ec38dd26bd2f8ba03d8d1ac4fd6984604829a4f42026f97b6548d0460180eeba'){
        nodes(node.arguments[0],child=>{if(child.type==='ImportExpression')builtImports.add(child);if(child.type==='Identifier'&&child.name==='module')builtImportIdentifiers.add(child);});
      }
    });
    nodes(tree,node=>{
      if(node.type==='ImportDeclaration'&&['node:module','module'].includes(node.source.value))for(const spec of node.specifiers){
        if(spec.type==='ImportSpecifier'&&spec.imported.name==='createRequire')factoryNames.add(spec.local.name);
        else if(['ImportDefaultSpecifier','ImportNamespaceSpecifier'].includes(spec.type))moduleNames.add(spec.local.name);
      }
      if(node.type==='VariableDeclarator'&&node.init?.type==='CallExpression'&&node.init.callee?.name==='require'&&['node:module','module'].includes(node.init.arguments[0]?.value)){
        if(node.id.type==='Identifier')moduleNames.add(node.id.name);
        if(node.id.type==='ObjectPattern')for(const property of node.id.properties)if(property.key?.name==='createRequire'&&property.value?.type==='Identifier')factoryNames.add(property.value.name);
      }
    });
    const isModuleLoad=node=>node?.type==='CallExpression'&&node.callee?.name==='require'&&['node:module','module'].includes(node.arguments[0]?.value);
    const isFactory=callee=>callee?.type==='Identifier'&&factoryNames.has(callee.name)||callee?.type==='MemberExpression'&&!callee.computed&&callee.property?.name==='createRequire'&&(moduleNames.has(callee.object?.name)||isModuleLoad(callee.object));
    const isFactoryCall=node=>node?.type==='CallExpression'&&isFactory(node.callee);
    const moduleURL=node=>node?.type==='Identifier'&&node.name==='__filename'||node?.type==='MemberExpression'&&!node.computed&&node.property?.name==='url'&&node.object?.type==='MetaProperty'&&node.object.meta?.name==='import'&&node.object.property?.name==='meta';
    let changed=true;while(changed){changed=false;nodes(tree,(node,parent)=>{
      const binding=node.type==='VariableDeclarator'?{id:node.id,init:node.init}:node.type==='AssignmentExpression'&&node.operator==='='?{id:node.left,init:node.right}:null;
      if(binding&&binding.init?.type==='Identifier'&&(factoryNames.has(binding.init.name)||moduleNames.has(binding.init.name))){
        assert.equal(binding.id?.type,'Identifier',`Unsupported module loader binding: ${path}`);const names=factoryNames.has(binding.init.name)?factoryNames:moduleNames;if(!names.has(binding.id.name)){names.add(binding.id.name);changed=true;}
      }
      if(binding&&(isFactoryCall(binding.init)||binding.init?.type==='Identifier'&&requireNames.has(binding.init.name))){
        assert.equal(binding.id?.type,'Identifier',`Unsupported require binding: ${path}`);if(!requireNames.has(binding.id.name)){requireNames.add(binding.id.name);changed=true;}
      }
      if(isFactoryCall(node)){
        assert(node.arguments.length===1&&moduleURL(node.arguments[0]),`createRequire must use the current module URL: ${path}`);
        assert(parent&&(parent.type==='VariableDeclarator'&&parent.init===node||parent.type==='AssignmentExpression'&&parent.right===node||parent.type==='CallExpression'&&parent.callee===node),`Unsupported createRequire indirection: ${path}`);
      }
    });}
    // Loader functions may not escape into arrays, objects, callbacks or other
    // opaque dispatch. Recognized direct aliases are resolved above; anything
    // else needs an explicit protected parser change rather than an exemption.
    nodes(tree,(node,parent)=>{
      if(node.type==='Identifier'&&!builtImportIdentifiers.has(node)&&(requireNames.has(node.name)||factoryNames.has(node.name)||moduleNames.has(node.name))){
        const declaration=parent?.type==='ImportSpecifier'||parent?.type==='ImportDefaultSpecifier'||parent?.type==='ImportNamespaceSpecifier'||parent?.type==='VariableDeclarator'&&parent.id===node;
        const alias=parent?.type==='VariableDeclarator'&&parent.init===node&&parent.id?.type==='Identifier'||parent?.type==='AssignmentExpression'&&parent.operator==='='&&(parent.left===node||parent.right===node)&&parent.left?.type==='Identifier';
        const property=parent?.type==='MemberExpression'&&!parent.computed&&parent.property===node||parent?.type==='Property'&&!parent.computed&&parent.key===node&&parent.value!==node;
        const call=parent?.type==='CallExpression'&&parent.callee===node;
        const member=parent?.type==='MemberExpression'&&parent.object===node;
        const typeCheck=parent?.type==='UnaryExpression'&&parent.operator==='typeof';
        assert(declaration||alias||property||call||member||typeCheck,`Unsupported loader escape: ${path}:${node.name}`);
      }
      if(node.type==='MemberExpression'&&requireNames.has(node.object?.name)){
        assert(!node.computed&&(node.property?.name==='main'||node.property?.name==='resolve'&&parent?.type==='CallExpression'&&parent.callee===node),`Unsupported require indirection: ${path}`);
      }
      if(node.type==='MemberExpression'&&moduleNames.has(node.object?.name)&&node.property?.name==='createRequire')assert(!node.computed&&parent?.type==='CallExpression'&&parent.callee===node,`Unsupported createRequire escape: ${path}`);
    });
    function dependency(specifier){
      assert.equal(typeof specifier,'string',`Computed render import needs a protected policy update: ${path}`);
      // The negative scene-input contract uses this one literal browser URL,
      // served only from the pinned Three.js package, never from source bundles.
      if(path==='site/ci-scene-browser-test.mjs'&&specifier==='/modules/examples/jsm/loaders/GLTFLoader.js')return;
      if(specifier.startsWith('.')){
        const local=specifier.replace(/\?(?:raw|url)$/,'');
        const target=relative('/',resolve('/',dirname(path),local)).split(sep).join('/');
        assert(safePath(target)&&!local.includes('?')&&!local.includes('#'),`Unsafe render dependency: ${specifier}`);
        // This exact browser-version metadata comes from the pinned installed
        // Playwright package, not a repository-controlled archival namespace.
        if(path==='site/render-web-previews.mjs'&&target==='node_modules/playwright-core/browsers.json')return;
        visit(target);
      }else assert(/^node:[a-z0-9_/-]+$/i.test(specifier)||/^(?:@[a-z0-9_.-]+\/)?[a-z0-9_.-]+(?:\/[a-z0-9_.-]+)*$/i.test(specifier),`Unresolved or external render import: ${specifier}`);
    }
    function walk(node){
      if(!node||typeof node!=='object')return;
      if(['ImportDeclaration','ExportNamedDeclaration','ExportAllDeclaration'].includes(node.type)&&node.source)dependency(node.source.value);
      if(node.type==='ImportExpression'&&!builtImports.has(node))dependency(node.source.type==='Literal'?node.source.value:undefined);
      if(node.type==='CallExpression'){
        const callee=node.callee;
        if(callee?.type==='MemberExpression'&&moduleNames.has(callee.object?.name))assert(!callee.computed,`Computed module loader requires a policy update: ${path}`);
        const required=callee?.type==='Identifier'&&requireNames.has(callee.name)||isFactoryCall(callee)||callee?.type==='MemberExpression'&&!callee.computed&&callee.property?.name==='require'&&moduleNames.has(callee.object?.name);
        if(required){assert.equal(node.arguments.length,1,`Unsupported require arguments: ${path}`);dependency(node.arguments[0]?.type==='Literal'?node.arguments[0].value:undefined);}
        if(callee?.type==='MemberExpression'&&requireNames.has(callee.object?.name)){assert(!callee.computed&&callee.property?.name==='resolve'&&node.arguments.length===1,`Unsupported require indirection: ${path}`);dependency(node.arguments[0]?.type==='Literal'?node.arguments[0].value:undefined);}
      }
      if(node.type==='NewExpression'&&node.callee?.name==='URL'&&node.arguments[1]?.object?.type==='MetaProperty')dependency(node.arguments[0]?.value);
      for(const [key,value] of Object.entries(node))if(key!=='source'){
        if(Array.isArray(value))for(const child of value)walk(child);
        else if(value&&typeof value==='object')walk(value);
      }
    }
    walk(tree);
  }
  // All application JS is a root, even if an entrypoint currently loads it lazily.
  for(const path of paths.filter(path=>/^site\/.*\.js$/.test(path)))visit(path);
  for(const path of MODEL_PROOF_ENTRYPOINTS)if(available.has(path))visit(path);
  for(const path of EXECUTED_QA_ENTRYPOINTS)if(available.has(path))visit(path);
  return found;
}
function policyInputs(paths,read,mode){
  const closure=modelExecutionDependencies(paths,read);
  const archives=collectArchivalInputs({paths,read,mode,manifest:paths.includes('assets/manifest.json')?JSON.parse(read('assets/manifest.json')):undefined,protectedPaths:closure});
  const excluded=new Set(archives.excludedPaths),archived=new Set(archives.files.map(row=>row.path));
  const selected=paths.filter(path=>!excluded.has(path)&&(protectedModelPath(path)||(publicationOnly.has(path)&&closure.has(path)))).sort();
  for(const path of closure)if((/\.(?:mjs|cjs|js|css|html)$/.test(path)||archived.has(path))&&!selected.includes(path))selected.push(path);
  selected.sort();assert(selected.includes('site/ci-model-proof.mjs'),'Model proof verifier missing from policy');
  const digest=hashObject(selected.map(path=>[path,hashBytes(path===ARCHIVAL_REGISTRY_PATH&&archives.registryMasked?archives.registrySkeleton:read(path))]));
  return {paths:selected,closure,archives,digest};
}
// Python publication checks create ignored bytecode during an otherwise clean
// build. Never use gitignore (or the cache directory name alone) to exempt code:
// only an untracked canonical CPython cache for a tracked source can qualify.
// Recompile the exact source without running it and compare the serialized code
// bytes. No candidate bytecode is imported, executed, or unmarshalled. Unknown,
// malformed, stale, foreign-compiler and tracked bytecode stays policy-bound.
function generatedPythonCaches(root,paths){
  const pattern=/^(scripts(?:\/[A-Za-z0-9_.-]+)*)\/__pycache__\/([A-Za-z_][A-Za-z0-9_]*)\.(cpython-[0-9]+)(?:\.opt-([12]))?\.pyc$/;
  const candidates=paths.map(path=>({path,match:pattern.exec(path)})).filter(row=>row.match);
  if(!candidates.length)return new Set();
  const tracked=new Set(execFileSync('git',['ls-files','--cached','-z','--','scripts'],{cwd:root,timeout:10000,maxBuffer:16*1024*1024}).toString().split('\0').filter(Boolean));
  const available=new Set(paths),checks=[];let sourceBytes=0;
  for(const {path,match} of candidates){
    const source=`${match[1]}/${match[2]}.py`;
    if(tracked.has(path)||!tracked.has(source)||!available.has(source))continue;
    assert(checks.length<64,'Too many generated Python caches');
    assert(lstatSync(resolve(root,path)).size<=16*1024*1024,'Generated Python cache exceeds size limit');
    assert(lstatSync(resolve(root,source)).size<=4*1024*1024,'Python cache source exceeds size limit');
    const data=bytes(root,path),input=bytes(root,source);sourceBytes+=input.length;
    assert(sourceBytes<=16*1024*1024,'Generated Python cache sources exceed size limit');
    if(data.length<16||![0,1,3].includes(data.readUInt32LE(4)))continue;
    checks.push({path,tag:match[3],optimize:Number(match[4]||0),filename:resolve(root,source),source:input.toString('base64'),magic:data.subarray(0,4).toString('hex'),body_sha256:hashBytes(data.subarray(16))});
  }
  if(!checks.length)return new Set();
  const verifier=`import base64, hashlib, importlib.util, json, marshal, resource, sys
resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
valid = []
for row in json.load(sys.stdin):
    if sys.implementation.name != 'cpython' or row['tag'] != sys.implementation.cache_tag or row['magic'] != importlib.util.MAGIC_NUMBER.hex():
        continue
    source = base64.b64decode(row['source'], validate=True)
    code = compile(source, row['filename'], 'exec', dont_inherit=True, optimize=row['optimize'])
    if hashlib.sha256(marshal.dumps(code)).hexdigest() == row['body_sha256']:
        valid.append(row['path'])
print(json.dumps(valid))
`;
  const valid=JSON.parse(execFileSync('python3',['-I','-S','-c',verifier],{cwd:root,input:JSON.stringify(checks),timeout:10000,maxBuffer:1024*1024}).toString());
  assert(Array.isArray(valid)&&valid.every(path=>checks.some(row=>row.path===path))&&new Set(valid).size===valid.length,'Invalid generated Python cache verification');
  return new Set(valid);
}
function currentPolicy(root){
  const paths=POLICY_ROOTS.flatMap(path=>files(root,path));
  // Imported local data can live outside the usual source roots.
  const read=path=>bytes(root,path);
  // A single source scan inventories repository directories, not node_modules or builds.
  const extra=['assets','production'].flatMap(path=>files(root,path));
  const inventory=[...paths,...extra],generated=generatedPythonCaches(root,inventory);
  return policyInputs(inventory.filter(path=>!generated.has(path)),read,path=>lstatSync(resolve(root,path)).mode);
}
export function modelPolicyDigest(root=process.cwd()){return currentPolicy(resolve(root)).digest;}
export function modelArchivalInputs(root=process.cwd()){return currentPolicy(resolve(root)).archives;}
function policyAtCommit(ref,{root=process.cwd()}={}){
  assert(SHA.test(ref),'Exact policy commit required');
  const git=(...args)=>execFileSync('git',args,{cwd:root,maxBuffer:128*1024*1024});
  const entries=git('ls-tree','-r','-z',ref).toString().split('\0').filter(Boolean).map(line=>{const [header,path]=line.split('\t');return {mode:header.split(' ')[0],path};});
  const byPath=new Map(entries.map(row=>[row.path,row])),cache=new Map();
  const read=path=>{assert.equal(byPath.get(path)?.mode,'100644',`Nonregular policy input: ${path}`);if(!cache.has(path))cache.set(path,git('show',`${ref}:${path}`));return cache.get(path);};
  assert(byPath.has('site/ci-model-proof.mjs'),'Base has no v2 model proof policy; full baseline required');
  return policyInputs([...byPath.keys()],read,path=>byPath.get(path)?.mode);
}
export function modelPolicyDigestAtCommit(ref,options){return policyAtCommit(ref,options).digest;}
export function modelArchivalInputsAtCommit(ref,options){return policyAtCommit(ref,options).archives;}
export function assertModelArchivalAppendAtCommit(ref,{root=process.cwd()}={}){
  const before=modelArchivalInputsAtCommit(ref,{root}),after=modelArchivalInputs(root),oldIDs=new Set(before.modelIDs);
  return assertArchivalAppend(before,after,{beforePaths:before.repositoryPaths,oldIDs,newIDs:after.modelIDs.filter(id=>!oldIDs.has(id))});
}
export function catalogIDs(manifest){
  assert(Array.isArray(manifest?.assets)&&manifest.assets.length,'A nonempty catalog is required');
  const ids=manifest.assets.map(asset=>asset.id);assert(ids.every(id=>ID.test(id||'')),'Invalid model ID');
  assert.equal(new Set(ids).size,ids.length,'Duplicate model ID');return ids.sort();
}
function splitMap(root,path,key,shared,perModel){
  if(!existsSync(resolve(root,path)))return;
  const document=json(root,path),mapping=key?document[key]:document;
  assert(mapping&&typeof mapping==='object'&&!Array.isArray(mapping),`Invalid model data map: ${path}`);
  for(const [id,value] of Object.entries(mapping)){
    assert(perModel.has(id),`Unowned model data: ${path}:${id}`);perModel.get(id).data[path]=value;
  }
  if(key){const {[key]:ignored,...rest}=document;shared[path]=rest;}
}
export function gallerySharedData(value,ids){
  const {generated_capture,...rest}=value;if(generated_capture===undefined)return rest;
  assert(generated_capture&&typeof generated_capture==='object'&&!Array.isArray(generated_capture),'Invalid gallery capture diagnostics');
  const {assets,published_total,...recipe}=generated_capture;
  assert(Array.isArray(assets)&&assets.every(id=>ids.has(id))&&new Set(assets).size===assets.length,'Invalid captured model diagnostics');
  assert(Number.isSafeInteger(published_total)&&published_total>=assets.length&&published_total<=ids.size,'Invalid captured catalog count');
  // These two fields report which work ran, not renderer inputs. All remaining
  // fields, including unknown future fields, remain bound as shared recipe data.
  return {...rest,generated_capture:recipe};
}
function splitResources(root,path,shared,perModel){
  if(!existsSync(resolve(root,path)))return;
  const document=json(root,path),{posters,files:seals,...rest}=document;
  assert(posters&&Array.isArray(seals),`Invalid gallery resources: ${path}`);
  shared[path]={...gallerySharedData(rest,new Set(perModel.keys())),files:[]};
  const owner=new Map();
  for(const [id,poster] of Object.entries(posters)){
    assert(perModel.has(id),`Unknown resource model: ${id}`);
    perModel.get(id).data[path]={poster,files:[]};
    for(const kind of ['detail','wheel']){
      const resource=poster[kind];assert.equal(resource,`gallery/posters/${id}${kind==='wheel'?'-wheel':''}.png`,'Noncanonical gallery poster');
      assert(!owner.has(resource),'Duplicate gallery resource owner');owner.set(resource,id);
      perModel.get(id).paths.add(`site/public/${resource}`);
    }
  }
  for(const seal of seals){const id=owner.get(seal.path);if(id)perModel.get(id).data[path].files.push(seal);else shared[path].files.push(seal);}
}
function splitCatalog(root,shared,perModel,manifest){
  const path='site/catalog-data.json';if(!existsSync(resolve(root,path)))return;
  const data=json(root,path);
  // Accepted schema is versioned in the protected curation adapter; unknown fields
  // remain global inputs rather than silently disappearing from the dependency key.
  const {worlds, packs, legacy_memberships,...rest}=data;
  validateCatalogData(data,{manifest});
  assert.equal(data.version,1,'Unknown catalog data schema');
  assert(Array.isArray(worlds)&&Array.isArray(packs)&&Array.isArray(legacy_memberships),'Unknown catalog ownership');
  shared[path]=rest;
  for(const asset of manifest.assets){
    perModel.get(asset.id).data[path]=catalogDataForAsset(asset,data);
  }
}
/** Verify the delivered render surface, not just its source or a candidate seal.
 * The immutable projection is process-local: saved JSON cannot assert that a
 * build was checked. This runs after build/capture and again on each shard.
 */
export async function assertBuiltRenderInputs({root=process.cwd(),outputRoot='dist',templatePath='qa/ci-model-proof/vite-template.html'}={}){
  root=resolve(root);outputRoot=resolve(root,outputRoot);
  assert.equal(realpathSync(outputRoot),outputRoot,'Build root symlink rejected');
  const source=json(root,'assets/manifest.json'),ids=catalogIDs(source),owned=new Map(ids.map(id=>[id,new Set()]));
  const source_sha256=hashObject(source),template=bytes(root,templatePath),actualPaths=files(outputRoot,'.').map(path=>path.slice(2));
  const own=(id,path)=>{assert(safePath(path),`Unsafe delivered model path: ${path}`);owned.get(id).add(path);};
  const checkedOutputHashes=new Map();
  const output=path=>{const data=bytes(outputRoot,path),digest=hashBytes(data);if(checkedOutputHashes.has(path))assert.equal(checkedOutputHashes.get(path),digest,`Build changed during verification: ${path}`);checkedOutputHashes.set(path,digest);return data;},document=path=>JSON.parse(output(path));
  const expected=await enrichManifest(source,root),turntables=await collectTurntables(expected,root);
  for(const asset of expected.assets){
    const id=asset.id;
    if(turntables.posters.has(id))asset.card_preview=turntables.posters.get(id);
    if(turntables.descriptors.has(id))asset.turntable=turntables.descriptors.get(id);
    for(const kind of ['glb','blend','preview']){
      assert.equal(hashBytes(output(asset[kind])),asset.sha256[kind],`Delivered ${kind} bytes differ: ${id}`);own(id,asset[kind]);
    }
    for(const path of [asset.downloads.bundle,asset.downloads.credits])own(id,path);
    asset.file_sizes.bundle=output(asset.downloads.bundle).length;
    assert.equal(output(asset.downloads.credits).toString(),creditText(asset,expected),`Delivered credits differ: ${id}`);
    if(asset.card_preview)own(id,asset.card_preview);
    if(asset.turntable){
      own(id,asset.turntable.manifest);
      const sequence=json(root,asset.turntable.manifest);for(const frame of sequence.frames)own(id,frame.path);
    }
  }
  assert.equal(output('assets/manifest.json').toString(),JSON.stringify(expected,null,2)+'\n','Delivered manifest differs from independently derived source');
  for(const path of turntables.files)assert.equal(hashBytes(output(path)),hashBytes(bytes(root,path)),`Delivered turntable differs: ${path}`);
  const catalogData=json(root,'site/catalog-data.json'),catalog=createCatalog(expected,{approvedOnly:true,catalogData});
  const catalogFiles=new Map([['assets/catalog.json',catalog.index],...catalog.shards,...catalog.details]);
  for(const [path,value] of catalogFiles)assert.equal(output(path).toString(),JSON.stringify(value)+'\n',`Delivered catalog differs: ${path}`);
  for(const id of ids)own(id,`assets/catalog/details/${id}.json`);
  const temporary=mkdtempSync(join(tmpdir(),'render-proof-html-'));
  let htmlPaths;
  try{
    writeFileSync(join(temporary,'index.html'),template);
    await writeStaticRoutes(expected,temporary,{catalogData});
    htmlPaths=files(temporary,'.').map(path=>path.slice(2));
    for(const path of htmlPaths)assert.equal(output(path).toString(),bytes(temporary,path).toString(),`Delivered route differs: ${path}`);
  }finally{rmSync(temporary,{recursive:true,force:true});}
  for(const id of ids)for(const locale of ['','zh-CN/'])own(id,`${locale}models/${id}/index.html`);
  // Gallery descriptors are inert per-model data. Every actual resource byte is
  // sealed, including shared scale companions; no arbitrary path can be owned.
  const resources=document('gallery/resources.json'),{posters,files:resourceSeals,...resourceShared}=resources;
  assert(posters&&Array.isArray(resourceSeals),'Missing delivered gallery resources');
  assert.deepEqual(Object.keys(posters).sort(),ids,'Delivered poster coverage differs');
  const resourceOwners=new Map(),seenSeals=new Set();
  for(const [id,poster] of Object.entries(posters)){
    assert.equal(poster.source_glb_sha256,source.assets.find(asset=>asset.id===id).sha256.glb,`Delivered poster source differs: ${id}`);
    for(const kind of ['detail','wheel']){
      const path=`gallery/posters/${id}${kind==='wheel'?'-wheel':''}.png`;
      assert.equal(poster[kind],path,'Noncanonical delivered poster');own(id,path);resourceOwners.set(path,id);
    }
  }
  const modelResourceData=new Map(ids.map(id=>[id,{poster:posters[id],files:[]}])) ,sharedResourceSeals=[];
  for(const seal of resourceSeals){
    assert(safePath(seal.path)&&seal.path.startsWith('gallery/'),'Unsafe delivered resource seal');assert(!seenSeals.has(seal.path),'Duplicate delivered resource seal');seenSeals.add(seal.path);
    const data=output(seal.path);assert.equal(hashBytes(data),seal.sha256,`Delivered resource bytes differ: ${seal.path}`);assert.equal(data.length,seal.bytes);
    const owner=resourceOwners.get(seal.path);if(owner)modelResourceData.get(owner).files.push(seal);else sharedResourceSeals.push(seal);
  }
  for(const path of resourceOwners.keys())assert(seenSeals.has(path),`Unsealed delivered poster: ${path}`);
  // Generated global data/HTML may grow, but only exact protected regeneration is
  // exempt from shared bytes. Detail documents and model outputs stay per-ID.
  const derived=new Set(['assets/manifest.json','gallery/resources.json',...catalogFiles.keys(),...htmlPaths]);
  const allOwned=new Set([...owned.values()].flatMap(paths=>[...paths]));
  const common=actualPaths.filter(path=>!allOwned.has(path)&&!derived.has(path)&&path!=='ci-review-build.json');
  // Unknown files are shared, including unknown executable additions. The full
  // output audit separately enforces the publication inventory.
  const shared_sha256=hashObject({domain:'verified-built-render-v1',template_sha256:hashBytes(template),
    files:common.sort().map(path=>[path,hashBytes(output(path))]),resources:{...gallerySharedData(resourceShared,new Set(ids)),files:sharedResourceSeals}});
  const models=ids.map(id=>({id,input_sha256:hashObject({files:[...owned.get(id)].sort().map(path=>[path,hashBytes(output(path))]),resources:modelResourceData.get(id),asset:expected.assets.find(asset=>asset.id===id)})}));
  const payloadRows=actualPaths.filter(path=>path!=='ci-review-build.json').map(path=>{if(!checkedOutputHashes.has(path))output(path);return [path,checkedOutputHashes.get(path)];});
  const payload_sha256=hashBytes(JSON.stringify(payloadRows));assert.equal(payload_sha256,payloadDigest(outputRoot),'Build changed during independent render verification');
  const result=Object.freeze({version:1,root,source_sha256,shared_sha256,payload_sha256,models:Object.freeze(models.map(row=>Object.freeze(row)))});
  verifiedBuiltInputs.add(result);return result;
}
export function computeModelInputs({root=process.cwd(),manifest=json(root,'assets/manifest.json'),runtime,built}={}){
  root=resolve(root);
  if(built){assert(verifiedBuiltInputs.has(built),'Built inputs require independent in-process verification');assert.equal(built.root,root,'Built input root differs');assert.equal(built.source_sha256,hashObject(manifest),'Built source manifest changed');}
  const ids=catalogIDs(manifest),perModel=new Map(ids.map(id=>[id,{paths:new Set(),data:{}}])),shared={};
  const lock=json(root,'package-lock.json'),pkg=json(root,'package.json');
  assert.equal(pkg.devDependencies?.playwright,PINNED_BROWSER.playwright,'Browser upgrade requires a new protected proof policy');
  assert.equal(lock.packages?.['node_modules/playwright-core']?.version,PINNED_BROWSER.playwright,'Pinned Chromium package differs');
  if(existsSync(resolve(root,'node_modules/playwright-core/browsers.json'))){
    const installed=JSON.parse(readFileSync(resolve(root,'node_modules/playwright-core/browsers.json'))).browsers.find(item=>item.name==='chromium');
    assert.equal(installed?.browserVersion,PINNED_BROWSER.chromium,'Installed Chromium differs');assert.equal(installed?.revision,PINNED_BROWSER.revision,'Installed Chromium revision differs');
  }
  assert(!process.env.CHROMIUM_PATH,'Unpinned browser executable cannot produce or reuse proof');
  splitMap(root,'site/gallery/wheel-framing.json',null,shared,perModel);
  splitMap(root,'site/gallery/approved-poster-inputs.json','posters',shared,perModel);
  splitResources(root,'site/public/gallery/resources.json',shared,perModel);
  splitCatalog(root,shared,perModel,manifest);
  const card_preview_renderer={render_preset_sha256:hashBytes(JSON.stringify(CARD_RENDER_PRESET)),viewer_source_sha256:hashBytes(bytes(root,'site/viewer.js'))};
  const turntablePath='assets/turntables/index.json',cards=new Map();
  {
    // Source card seals are mandatory even while the separate reproduction job
    // is pending. Neither a manifest preview nor a gallery PNG is this WebP.
    const {assets=[],posters,...rest}=json(root,turntablePath);shared[turntablePath]=rest;
    assert.equal(rest.version,1,'Missing shipped card index');
    assert.equal(rest.render_preset_sha256,card_preview_renderer.render_preset_sha256,'Shipped cards use another renderer preset');
    assert(Array.isArray(assets)&&Array.isArray(posters),'Missing shipped card index entries');
    assert.deepEqual(posters.map(row=>row.id).sort(),ids,'Every model requires exactly one shipped card-preview seal');
    for(const [kind,entries]of Object.entries({assets,posters})){
      const seen=new Set();for(const entry of entries){
        assert(perModel.has(entry.id),`Unknown turntable owner: ${entry.id}`);assert(!seen.has(entry.id),'Duplicate turntable owner');seen.add(entry.id);
        const own=perModel.get(entry.id);own.data[`${turntablePath}:${kind}`]=entry;
        if(entry.path)own.paths.add(entry.path);
      }
    }
    for(const entry of posters){
      const asset=manifest.assets.find(asset=>asset.id===entry.id);
      assert.equal(entry.path,publishedImagePaths(asset,manifest).poster,'Noncanonical shipped card-preview path');
      assert.equal(entry.source_glb_sha256,asset.sha256.glb,'Shipped card source GLB differs');
      assert.equal(entry.render_preset_sha256,card_preview_renderer.render_preset_sha256,'Shipped card renderer preset differs');
      assert.equal(entry.width,CARD_RENDER_PRESET.image.width,'Shipped card width differs');assert.equal(entry.height,CARD_RENDER_PRESET.image.height,'Shipped card height differs');
      const data=bytes(root,entry.path),sha256=hashBytes(data);
      assert.equal(sha256,entry.sha256,`Actual card-preview bytes disagree with index: ${entry.id}`);
      assert(Number.isSafeInteger(entry.bytes)&&entry.bytes>0,'Missing measured shipped card-preview bytes');assert.equal(data.length,entry.bytes,'Shipped card-preview byte count differs');
      if(asset.card_preview!==undefined)assert.equal(asset.card_preview,entry.path,'Manifest card preview differs from shipped card index');
      cards.set(entry.id,{path:entry.path,sha256,bytes:data.length});
    }
  }
  const mapped=new Set(['assets/manifest.json','site/gallery/wheel-framing.json','site/gallery/approved-poster-inputs.json','site/public/gallery/resources.json','site/catalog-data.json']);
  const ownResources=new Set([...perModel.values()].flatMap(row=>[...row.paths]));
  const policy=currentPolicy(root);
  const sharedFiles=[...new Set([...files(root,'site'),...policy.closure])].filter(path=>!mapped.has(path)&&!ownResources.has(path)&&!path.startsWith('site/public/gallery/posters/')&&!path.startsWith('site/gallery/tests/evidence/')&&(!built||!publicationOnly.has(path)||policy.closure.has(path))&&(!built||path!==ARCHIVAL_REGISTRY_PATH||!policy.archives.registryMasked));
  // Unknown files under the public poster namespace are not silently ignored.
  for(const path of files(root,'site/public/gallery/posters'))assert(ownResources.has(path),`Unowned public poster: ${path}`);
  const policy_sha256=policy.digest;
  const runtime_config=runtime||{site_base:process.env.SITE_BASE||'/',site_origin:process.env.SITE_ORIGIN||'',node_major:process.versions.node.split('.')[0],platform:process.platform,arch:process.arch};
  const shared_input_sha256=hashObject({policy_sha256,runtime_config,gpu_policy:GPU_POLICY,card_preview_renderer,built_render:built?{version:built.version,shared_sha256:built.shared_sha256}:null,files:sharedFiles.sort().map(path=>[path,hashBytes(bytes(root,path))]),data:shared});
  const {assets,publication,...manifestShared}=manifest;
  const models=manifest.assets.map(asset=>{
    const own=perModel.get(asset.id);
    if(policy.archives.byModel[asset.id])own.data[ARCHIVAL_REGISTRY_PATH]=policy.archives.byModel[asset.id];
    for(const kind of ['glb','blend','preview']){
      assert(safePath(asset[kind])&&asset[kind].startsWith('assets/'),`Missing safe ${kind}: ${asset.id}`);own.paths.add(asset[kind]);
      const actual=hashBytes(bytes(root,asset[kind]));assert(HASH.test(asset.sha256?.[kind]||''),`Missing ${kind} hash: ${asset.id}`);
      assert.equal(actual,asset.sha256[kind],`Actual ${kind} bytes disagree with manifest: ${asset.id}`);
    }
    for(const path of files(root,`assets/turntables/${asset.id}`))own.paths.add(path);
    if(typeof asset.card_preview==='string')own.paths.add(asset.card_preview);
    // enrichManifest reads this adjacent document into material_count. Its actual
    // bytes and presence must be bound even though it is not a manifest field.
    const adjacentQA=`${dirname(asset.glb)}/qa.json`;if(existsSync(resolve(root,adjacentQA)))own.paths.add(adjacentQA);
    const publication_memberships=Object.entries(publication||{}).filter(([,value])=>Array.isArray(value)&&value.includes(asset.id)).map(([key])=>key).sort();
    const built_model=built?.models.find(row=>row.id===asset.id);if(built)assert(built_model,'Missing verified built model');
    const card_preview=cards.get(asset.id);
    const inputs={asset,manifest:manifestShared,publication_memberships,data:own.data,card_preview,built_render_sha256:built_model?.input_sha256||null,files:[...own.paths].sort().map(path=>[path,hashBytes(bytes(root,path))])};
    const input_sha256=hashObject(inputs),input_key=hashObject({version:2,policy_sha256,shared_input_sha256,input_sha256});
    return {id:asset.id,input_key,input_sha256,glb_sha256:hashBytes(bytes(root,asset.glb)),card_preview};
  }).sort((a,b)=>a.id<b.id?-1:1);
  return {version:2,policy_sha256,shared_input_sha256,runtime_config,gpu_policy:GPU_POLICY,card_preview_renderer,render_inputs:built?'verified-built-render-v1':'source-only',...(built?{built_payload_sha256:built.payload_sha256}:{}),models};
}
function assertCardRendererInputs(renderer){
  for(const key of ['render_preset_sha256','viewer_source_sha256'])assert(HASH.test(renderer?.[key]||''),`Missing card-preview renderer ${key}`);
  return renderer;
}
function assertCompleteModelRecord(row,renderer){
  assertModelRecord(row);assertCardRendererInputs(renderer);
  assert(row.card_preview&&Number.isSafeInteger(row.card_preview.bytes)&&row.card_preview.bytes>0,'Missing measured shipped card-preview input');
  assertCardPreviewRecord(row.card_preview_proof,{input:row,identity:row.origin,payload_sha256:row.origin.payload_sha256,renderer});
  return row;
}
export function assertBaseModelProof(proof,{repository,baseSha,sourceTree,runId,runAttempt,policy_sha256,runtime_config,catalog_ids,card_preview_renderer}={}){
  assert.equal(proof?.version,2,'Missing v2 baseline; full main GPU baseline required');assert.equal(proof.kind,'strict-gpu-model-proof');
  assert.equal(proof.status,'pass');assert.equal(proof.repository,repository);assert.equal(proof.source_commit,baseSha);
  assert(SHA.test(proof.source_tree||''),'Missing source tree');if(sourceTree)assert.equal(proof.source_tree,sourceTree,'Baseline source tree differs');
  assert(HASH.test(proof.shared_input_sha256||''),'Missing shared inputs');assert(HASH.test(proof.payload_sha256||''),'Missing tested payload');
  assert.equal(Number(proof.run_id),Number(runId));assert.equal(Number(proof.run_attempt),Number(runAttempt));
  assert.equal(proof.policy_sha256,policy_sha256,'Baseline validation policy differs');assert.deepEqual(proof.runtime_config,runtime_config,'Baseline runtime differs');
  assert.deepEqual(proof.gpu_policy,GPU_POLICY,'Baseline GPU policy differs');assert.deepEqual(proof.catalog_ids,catalog_ids,'Baseline catalog differs from independently read source');
  assertCardRendererInputs(proof.card_preview_renderer);if(card_preview_renderer)assert.deepEqual(proof.card_preview_renderer,card_preview_renderer,'Baseline card-preview renderer differs');
  assert(Array.isArray(proof.models),'Missing model records');assert.equal(new Set(proof.models.map(row=>row.id)).size,proof.models.length,'Duplicate baseline model');
  for(const row of proof.models){assert(catalog_ids.includes(row.id),'Unknown model in baseline proof');assertCompleteModelRecord(row,proof.card_preview_renderer);}
  return proof;
}
export function assertModelRecord(row){
  for(const key of ['input_key','input_sha256','glb_sha256','report_sha256'])assert(HASH.test(row[key]||''),`Missing model ${key}`);
  assert.equal(row.status,'gpu-pass');assert.equal(row.result?.profile,'strict-gpu');assert.equal(row.result?.browser_status,'pass');assert.equal(row.result?.gpu_status,'pass');
  assert.equal(row.result?.chromium_version,PINNED_BROWSER.chromium);assert.equal(row.result?.review_scope,'models');
  assert.deepEqual(row.result?.page_errors,[]);assert.deepEqual(row.result?.resource_errors,[]);assert.deepEqual(row.result?.fallback_models,[]);
  assert(SHA.test(row.origin?.source_commit||''),'Missing tested source');assert(Number.isSafeInteger(row.origin.run_id)&&row.origin.run_id>0,'Missing origin run');assert(Number.isSafeInteger(row.origin.run_attempt)&&row.origin.run_attempt>0,'Missing origin attempt');
  if(row.origin.source_tree!==undefined)assert(SHA.test(row.origin.source_tree),'Invalid tested source tree');
  assert(HASH.test(row.origin.payload_sha256||''),'Missing original tested build');return row;
}
export function planModelReuse({inputs,baseProof=null,verifiedBaseProof=null,reasons=[]}={}){
  const ids=inputs.models.map(row=>row.id),fresh_ids=[],reused_ids=[],why=[...reasons];
  let usable=Boolean(baseProof&&verifiedBaseProof);
  if(usable){
    try{
      assert.equal(verifiedBaseProof.schema,2);assert.equal(verifiedBaseProof.source_commit,baseProof.source_commit);
      assert.equal(baseProof.version,2);assert.equal(baseProof.kind,'strict-gpu-model-proof');assert.equal(baseProof.status,'pass');
      assert.equal(verifiedBaseProof.repository,baseProof.repository);assert.equal(Number(verifiedBaseProof.run_id),Number(baseProof.run_id));assert.equal(Number(verifiedBaseProof.run_attempt),Number(baseProof.run_attempt));
      assert.equal(verifiedBaseProof.proof_sha256,hashObject(baseProof),'Verified proof was modified');assert.equal(baseProof.policy_sha256,inputs.policy_sha256);
      assert.deepEqual(baseProof.runtime_config,inputs.runtime_config);assert.deepEqual(baseProof.gpu_policy,GPU_POLICY);
      assertCardRendererInputs(inputs.card_preview_renderer);assert.deepEqual(baseProof.card_preview_renderer,inputs.card_preview_renderer,'Baseline card-preview renderer differs');
      assert.equal(new Set(baseProof.models.map(row=>row.id)).size,baseProof.models.length,'Duplicate baseline model');
      for(const record of baseProof.models){assert(baseProof.catalog_ids.includes(record.id),'Unknown baseline model');assertCompleteModelRecord(record,inputs.card_preview_renderer);}
    }catch(error){usable=false;why.push(`Baseline rejected: ${error.message}`);}
  }
  if(!usable)why.push('No independently verified compatible main v2 baseline; run every model');
  for(const current of inputs.models){
    const prior=usable?baseProof.models.find(row=>row.id===current.id):null;
    if(prior&&prior.input_key===current.input_key&&prior.input_sha256===current.input_sha256&&prior.glb_sha256===current.glb_sha256&&hashObject(prior.card_preview)===hashObject(current.card_preview))reused_ids.push(current.id);
    else {fresh_ids.push(current.id);if(usable)why.push(`${current.id}: ${prior?'model or shared inputs changed':'no successful per-model proof'}`);}
  }
  assert.deepEqual([...fresh_ids,...reused_ids].sort(),[...ids].sort());
  return {version:2,fresh_ids,reused_ids,reasons:why,verified_base_proof:usable?verifiedBaseProof:null};
}
export function freshModelRecords({inputs,selectedIDs,browser,identity,payload_sha256}){
  if(inputs.render_inputs==='verified-built-render-v1')assert.equal(inputs.built_payload_sha256,payload_sha256,'Model inputs verified a different built payload');
  assert.equal(browser.status,'pass');assert.equal(browser.browser_status,'pass');assert.equal(browser.profile,'strict-gpu');assert.equal(browser.review_scope,'models');
  assert.equal(browser.commit,identity.source_commit);assert.equal(browser.chromium_version,PINNED_BROWSER.chromium,'Browser is not lockfile-pinned Chromium');
  assert.equal(browser.gpu?.status,'pass');assert.deepEqual(browser.gpu.fallback_models,[]);assert.deepEqual(browser.page_errors,[]);assert.deepEqual(browser.resource_errors,[]);
  const expected=[...selectedIDs].sort();assert.equal(new Set(expected).size,expected.length,'Duplicate selected model');
  assert.deepEqual([...browser.selected_model_ids].sort(),expected,'Report selected wrong models');
  assert.deepEqual(browser.models.map(row=>row.id).sort(),expected,'Report did not execute exact fresh IDs');
  assert.deepEqual([...browser.gpu.rendered_models].sort(),expected,'GPU did not render exact fresh IDs');
  return browser.models.map(row=>{
    const input=inputs.models.find(model=>model.id===row.id);assert(input,'Unpublished model execution');assert.equal(row.status,'gpu-pass','Fallback cannot supply GPU proof');assert.equal(row.glb_sha256,input.glb_sha256);
    return assertModelRecord({...input,status:'gpu-pass',report_sha256:hashObject(browser),checks:row.checks||[],
      result:{profile:browser.profile,browser_status:browser.browser_status,gpu_status:browser.gpu.status,chromium_version:browser.chromium_version,review_scope:browser.review_scope,page_errors:browser.page_errors,resource_errors:browser.resource_errors,fallback_models:browser.gpu.fallback_models},
      origin:{source_commit:identity.source_commit,...(identity.source_tree!==undefined?{source_tree:identity.source_tree}:{}),run_id:Number(identity.run_id),run_attempt:Number(identity.run_attempt),payload_sha256}});
  });
}
export function aggregateModelProof({inputs,scopePlan,freshRecords,freshCardRecords=[],identity,build,baseProof=null,repository=process.env.GITHUB_REPOSITORY}){
  assert.equal(build?.version,1);assert.deepEqual(build.identity,identity,'Current build identity differs');assert(HASH.test(build.payload_sha256||''));
  assertCardRendererInputs(inputs.card_preview_renderer);
  if(inputs.render_inputs==='verified-built-render-v1')assert.equal(inputs.built_payload_sha256,build.payload_sha256,'Aggregate inputs verified a different built payload');
  const ids=inputs.models.map(row=>row.id).sort(),fresh=[...scopePlan.fresh_ids].sort(),reused=[...scopePlan.reused_ids].sort();
  assert.equal(new Set([...fresh,...reused]).size,ids.length,'Duplicate or overlapping model coverage');assert.deepEqual([...fresh,...reused].sort(),ids,'Fresh + reused must exactly equal current catalog');
  assert.deepEqual(freshRecords.map(row=>row.id).sort(),fresh,'Actually executed models differ from planned fresh IDs');
  assert.deepEqual(freshCardRecords.map(row=>row.id).sort(),fresh,'Actually reproduced card previews differ from planned fresh IDs');
  const recomputed=planModelReuse({inputs,baseProof,verifiedBaseProof:scopePlan.verified_base_proof});
  // A caller may choose to rerun additional IDs, but can never invent a reusable ID.
  assert(reused.every(id=>recomputed.reused_ids.includes(id)),'Reuse was not independently verified');
  const models=inputs.models.map(input=>{
    let record;if(fresh.includes(input.id)){
      record=freshRecords.find(row=>row.id===input.id);assertModelRecord(record);
      assert.equal(record.origin.source_commit,identity.source_commit);assert.equal(record.origin.run_id,Number(identity.run_id));assert.equal(record.origin.run_attempt,Number(identity.run_attempt));assert.equal(record.origin.payload_sha256,build.payload_sha256,'Fresh result tested another build');
      if(identity.source_tree!==undefined)assert.equal(record.origin.source_tree,identity.source_tree,'Fresh result tested another source tree');
      const card_preview_proof=freshCardRecords.find(row=>row.id===input.id);
      assertCardPreviewRecord(card_preview_proof,{input,identity,payload_sha256:build.payload_sha256,renderer:inputs.card_preview_renderer});
      record={...record,card_preview_proof};
    }else record=baseProof.models.find(row=>row.id===input.id);
    for(const key of ['input_key','input_sha256','glb_sha256'])assert.equal(record[key],input[key],`Coverage ${key} mismatch: ${input.id}`);
    assert.deepEqual(record.card_preview,input.card_preview,`Coverage shipped card-preview mismatch: ${input.id}`);
    assertCompleteModelRecord(record,inputs.card_preview_renderer);
    return {...record,evidence:reused.includes(input.id)?'reused':'fresh',...(reused.includes(input.id)?{reused_from:{source_commit:baseProof.source_commit,run_id:Number(baseProof.run_id),run_attempt:Number(baseProof.run_attempt),artifact_id:scopePlan.verified_base_proof.artifact_id}}:{})};
  });
  return {version:2,kind:'strict-gpu-model-proof',status:'pass',repository,source_commit:identity.source_commit,source_tree:identity.source_tree,
    run_id:Number(identity.run_id),run_attempt:Number(identity.run_attempt),policy_sha256:inputs.policy_sha256,shared_input_sha256:inputs.shared_input_sha256,runtime_config:inputs.runtime_config,gpu_policy:GPU_POLICY,card_preview_renderer:inputs.card_preview_renderer,
    catalog_ids:ids,fresh_ids:fresh,reused_ids:reused,models,payload_sha256:build.payload_sha256,
    scope:'Strict GPU browser contracts and exact shipped card-WebP reproduction; not visual, factual, hardware or formal asset approval'};
}

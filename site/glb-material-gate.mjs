/** Permanent GLB PBR material and byte-budget gate.
 * Rejects non-whitelisted GLBs that omit pbrMetallicRoughness.metallicFactor
 * (which defaults to 1.0 in glTF 2.0) or set metallicFactor > 0.1 without a
 * metallicRoughnessTexture, and enforces the 5,000,000-byte size budget.
 */
import {execFileSync} from 'node:child_process';
import {readdir,readFile,realpath,stat} from 'node:fs/promises';
import {basename,dirname,extname,join,relative,resolve,sep} from 'node:path';
import {pathToFileURL} from 'node:url';
import {MAX_GLB_BYTES} from './glb-size-gate.mjs';

export {MAX_GLB_BYTES};
export const MAX_NONMETAL_METALLIC_FACTOR=0.1;
export const TRUE_METAL_WHITELIST=Object.freeze([
 'pyrite-cube-cluster',
 'native-copper-dendrite',
]);
export const DEFAULT_MATERIAL_BASELINE_COMMIT='5255c1c99fe9c87864155ae6654fc91ec8e7cf5f';

const GLB_MAGIC=0x46546c67; // 'glTF' little-endian
const CHUNK_JSON=0x4e4f534a; // 'JSON'
const GENERIC_STEM=/^(?:model|candidate|source|mesh|asset|output|rebuilt)(?:-(?:no-index|repaired|fixed|clean|compressed))?(?:-v?[a-f0-9]{6,64})?$/;
const REVISION_SEGMENT=/^(?:r\d+|.*-r\d+|.*-v\d+|.*-\d{8}(?:-\d+)?|batch\d+.*|small-life.*|reviewed-.*|recovered-.*|drive-.*|lean-.*|old-corrective-.*|display-.*)$/;
const SAFE_ID=/^[a-z0-9]+(?:-[a-z0-9]+)*$/;

export function parseGlbJson(bytes){
 const buf=Buffer.isBuffer(bytes)?bytes:Buffer.from(bytes);
 if(buf.length<20)throw new Error(`File too short for GLB (${buf.length} bytes)`);
 if(buf.readUInt32LE(0)!==GLB_MAGIC)throw new Error('Invalid GLB magic header');
 const version=buf.readUInt32LE(4);
 if(version!==2)throw new Error(`Unsupported GLB version ${version} (expected 2)`);
 const declaredLength=buf.readUInt32LE(8);
 if(declaredLength!==buf.length)throw new Error(`Declared GLB length ${declaredLength} !== actual ${buf.length}`);
 const chunkLength=buf.readUInt32LE(12);
 const chunkType=buf.readUInt32LE(16);
 if(chunkType!==CHUNK_JSON)throw new Error('First GLB chunk is not JSON');
 if(chunkLength%4!==0||20+chunkLength>buf.length)throw new Error('Invalid GLB JSON chunk length or alignment');
 const raw=buf.subarray(20,20+chunkLength).toString('utf8');
 const doc=JSON.parse(raw);
 if(!doc||typeof doc!=='object'||Array.isArray(doc))throw new Error('GLB JSON root must be an object');
 return doc;
}

export async function inferAssetId(filePath,{root=null}={}){
 const full=resolve(filePath);
 const folder=dirname(full);
 try{
  const meta=JSON.parse(await readFile(join(folder,'metadata.json'),'utf8'));
  if(typeof meta?.id==='string'&&SAFE_ID.test(meta.id))return meta.id;
 }catch{}
 const stem=basename(full,extname(full));
 if(!GENERIC_STEM.test(stem)&&SAFE_ID.test(stem))return stem;
 const rel=root?relative(resolve(root),folder):folder;
 const segments=rel.split(/[\\/]/).filter(Boolean).reverse();
 for(const seg of segments){
  if(seg==='assets'||seg==='additions'||seg==='successors'||seg==='staging')break;
  if(REVISION_SEGMENT.test(seg))continue;
  if(SAFE_ID.test(seg))return seg;
 }
 return null;
}

export function inspectGlbBuffer(bytes,{
 id=null,
 maxMetallic=MAX_NONMETAL_METALLIC_FACTOR,
 maxBytes=MAX_GLB_BYTES,
 whitelist=TRUE_METAL_WHITELIST,
}={}){
 const buf=Buffer.isBuffer(bytes)?bytes:Buffer.from(bytes);
 const allowed=whitelist instanceof Set?whitelist:new Set(whitelist);
 const exempt=Boolean(id&&allowed.has(id));
 const violations=[];
 const materials=[];
 if(buf.length===0){
  violations.push({code:'empty_file',message:'GLB file is empty (0 bytes)'});
  return {ok:false,id,bytes:0,exempt,materials,violations};
 }
 if(maxBytes!==null&&maxBytes!==undefined&&maxBytes>0&&buf.length>maxBytes){
  violations.push({
   code:'size_exceeded',
   bytes:buf.length,
   limit_bytes:maxBytes,
   message:`${buf.length} bytes exceeds limit ${maxBytes} bytes by ${buf.length-maxBytes} bytes`,
  });
 }
 let doc;
 try{
  doc=parseGlbJson(buf);
 }catch(error){
  violations.push({code:'invalid_glb',message:error.message});
  return {ok:false,id,bytes:buf.length,exempt,materials,violations};
 }
 if(doc.asset?.version!=='2.0'){
  violations.push({code:'invalid_gltf_version',message:`glTF asset.version is ${JSON.stringify(doc.asset?.version)} (expected "2.0")`});
 }
 const rawMaterials=doc.materials;
 if(!Array.isArray(rawMaterials)||rawMaterials.length===0){
  if(!exempt){
   violations.push({code:'missing_materials',message:'GLB defines no materials (glTF 2.0 default material has metallicFactor=1.0)'});
  }
 }else{
  for(let i=0;i<rawMaterials.length;i++){
   const mat=rawMaterials[i];
   const name=typeof mat?.name==='string'&&mat.name?mat.name:`material[${i}]`;
   const pbr=mat?.pbrMetallicRoughness;
   const hasMrTex=Boolean(pbr?.metallicRoughnessTexture&&Number.isInteger(pbr.metallicRoughnessTexture.index)&&pbr.metallicRoughnessTexture.index>=0);
   const hasExplicitMetallic=Boolean(pbr&&typeof pbr==='object'&&Object.hasOwn(pbr,'metallicFactor')&&pbr.metallicFactor!==undefined&&pbr.metallicFactor!==null);
   const metallicFactor=hasExplicitMetallic?pbr.metallicFactor:null;
   const roughnessFactor=pbr&&typeof pbr==='object'&&Object.hasOwn(pbr,'roughnessFactor')?pbr.roughnessFactor:null;
   materials.push({index:i,name,has_metallic_roughness_texture:hasMrTex,metallic_factor:metallicFactor,roughness_factor:roughnessFactor});
   if(hasMrTex||exempt)continue;
   if(!hasExplicitMetallic){
    violations.push({
     code:'omitted_metallic_factor',
     material_index:i,
     material_name:name,
     message:`material[${i}] (${name}) omits pbrMetallicRoughness.metallicFactor without metallicRoughnessTexture (defaults to 1.0 in glTF 2.0)`,
    });
   }else if(typeof metallicFactor!=='number'||!Number.isFinite(metallicFactor)||metallicFactor<0||metallicFactor>1){
    violations.push({
     code:'invalid_metallic_factor',
     material_index:i,
     material_name:name,
     metallic_factor:metallicFactor,
     message:`material[${i}] (${name}) has invalid metallicFactor=${JSON.stringify(metallicFactor)}`,
    });
   }else if(metallicFactor>maxMetallic){
    violations.push({
     code:'high_metallic_factor',
     material_index:i,
     material_name:name,
     metallic_factor:metallicFactor,
     limit:maxMetallic,
     message:`material[${i}] (${name}) metallicFactor=${metallicFactor} exceeds ${maxMetallic} without metallicRoughnessTexture`,
    });
   }
  }
 }
 return {ok:violations.length===0,id,bytes:buf.length,exempt,materials,violations};
}

export async function checkGlbFile(filePath,{
 id=null,
 root=null,
 maxMetallic=MAX_NONMETAL_METALLIC_FACTOR,
 maxBytes=MAX_GLB_BYTES,
 whitelist=TRUE_METAL_WHITELIST,
 rejectSymlinks=false,
}={}){
 const full=resolve(filePath);
 const actual=await realpath(full);
 if(rejectSymlinks&&actual!==full){
  return {ok:false,id,path:filePath,bytes:0,exempt:false,materials:[],violations:[{code:'symlink_rejected',message:`Symlink GLB rejected: ${filePath}`}]};
 }
 if(root){
  const realRoot=await realpath(resolve(root));
  if(!actual.startsWith(realRoot+sep)){
   return {ok:false,id,path:filePath,bytes:0,exempt:false,materials:[],violations:[{code:'path_escape',message:`GLB escapes root: ${filePath}`}]};
  }
 }
 const info=await stat(actual);
 if(!info.isFile()){
  return {ok:false,id,path:filePath,bytes:0,exempt:false,materials:[],violations:[{code:'not_a_file',message:`Not a regular file: ${filePath}`}]};
 }
 const resolvedId=id??await inferAssetId(full,{root});
 const bytes=await readFile(actual);
 const result=inspectGlbBuffer(bytes,{id:resolvedId,maxMetallic,maxBytes,whitelist});
 return {...result,path:filePath};
}

export async function checkGlbPaths(paths,{
 id=null,
 root=null,
 maxMetallic=MAX_NONMETAL_METALLIC_FACTOR,
 maxBytes=MAX_GLB_BYTES,
 whitelist=TRUE_METAL_WHITELIST,
 rejectSymlinks=false,
}={}){
 const allowed=[...(whitelist instanceof Set?whitelist:whitelist)];
 if(id&&paths.length!==1)throw new Error('--id can only be used when checking a single GLB file');
 const results=[];
 for(const p of paths){
  try{
   results.push(await checkGlbFile(p,{id,root,maxMetallic,maxBytes,whitelist:allowed,rejectSymlinks}));
  }catch(error){
   results.push({ok:false,id,path:p,bytes:0,exempt:false,materials:[],violations:[{code:'io_error',message:error.message}]});
  }
 }
 const failures=results.filter(r=>!r.ok);
 return {
  status:failures.length?'FAIL':'PASS',
  checked_count:results.length,
  passed_count:results.length-failures.length,
  failed_count:failures.length,
  limit_bytes:maxBytes,
  max_metallic:maxMetallic,
  whitelist:allowed,
  results,
  failures,
 };
}

async function collectGlbFiles(dir){
 const out=[];
 for(const entry of await readdir(dir,{withFileTypes:true})){
  const full=join(dir,entry.name);
  if(entry.isDirectory())out.push(...await collectGlbFiles(full));
  else if(entry.isFile()&&entry.name.toLowerCase().endsWith('.glb'))out.push(full);
 }
 return out.sort();
}

export async function checkGlbDirectory(dirPath,options={}){
 const dir=resolve(dirPath);
 const files=await collectGlbFiles(dir);
 return checkGlbPaths(files,{...options,root:options.root??dir});
}

export async function checkGitChangedGlbs({
 root=process.cwd(),
 baseRef=null,
 maxMetallic=MAX_NONMETAL_METALLIC_FACTOR,
 maxBytes=MAX_GLB_BYTES,
 whitelist=TRUE_METAL_WHITELIST,
}={}){
 const repoRoot=await realpath(resolve(root));
 const git=(...args)=>execFileSync('git',['-C',repoRoot,...args],{encoding:'utf8',maxBuffer:32*1024*1024});
 const candidates=new Set();
 const addZ=out=>{for(const p of out.split('\0'))if(p&&p.toLowerCase().endsWith('.glb'))candidates.add(p);};
 if(baseRef){
  addZ(git('diff','--name-only','--diff-filter=ACMR','-z',baseRef,'--'));
 }else{
  // Compare working tree + index against HEAD, plus untracked GLBs.
  try{addZ(git('diff','--name-only','--diff-filter=ACMR','-z','HEAD','--'));}catch{}
 }
 addZ(git('ls-files','--others','--exclude-standard','-z'));
 const existing=[];
 for(const rel of [...candidates].sort()){
  const full=resolve(repoRoot,rel);
  try{if((await stat(full)).isFile())existing.push(rel);}catch{}
 }
 const report=await checkGlbPaths(existing.map(rel=>resolve(repoRoot,rel)),{root:repoRoot,maxMetallic,maxBytes,whitelist,rejectSymlinks:true});
 return {
  ...report,
  mode:'git-changed',
  base_ref:baseRef||'HEAD',
  results:report.results.map((r,i)=>({...r,path:existing[i]})),
  failures:report.failures.map(f=>({...f,path:relative(repoRoot,f.path)})),
 };
}

export async function checkReleaseGlbMaterials({
 root=process.cwd(),
 baselineCommit=DEFAULT_MATERIAL_BASELINE_COMMIT,
 manifest,
 maxMetallic=MAX_NONMETAL_METALLIC_FACTOR,
 maxBytes=MAX_GLB_BYTES,
 whitelist=TRUE_METAL_WHITELIST,
}={}){
 root=await realpath(resolve(root));
 if(!/^[a-f0-9]{40}$/.test(baselineCommit||''))throw new Error('Explicit 40-character Git baseline commit required');
 const git=(...args)=>execFileSync('git',['-C',root,...args],{encoding:'utf8',maxBuffer:32*1024*1024});
 if(git('rev-parse',`${baselineCommit}^{commit}`).trim()!==baselineCommit)throw new Error('Invalid baseline commit');
 const baseline=JSON.parse(git('show',`${baselineCommit}:assets/manifest.json`));
 manifest??=JSON.parse(await readFile(resolve(root,'assets/manifest.json'),'utf8'));
 if(!Array.isArray(baseline.assets)||!Array.isArray(manifest.assets)||!manifest.assets.length){
  throw new Error('Nonempty baseline and current manifests required');
 }
 const old=new Map(baseline.assets.map(a=>[a.id,a]));
 const changed=new Set([
  ...git('diff','--name-only','-z',baselineCommit,'--').split('\0'),
  ...git('ls-files','--others','--exclude-standard','-z').split('\0'),
 ]);
 const baselineTracked=new Set(git('ls-tree','-r','--name-only','-z',baselineCommit).split('\0'));
 const required=[],seen=new Set();
 let unchanged=0;
 for(const a of manifest.assets){
  if(!a||typeof a.id!=='string'||!a.id||seen.has(a.id))throw new Error('Missing or duplicate current asset ID');
  seen.add(a.id);
  const p=a.glb,b=old.get(a.id);
  if(typeof p!=='string'||!p.endsWith('.glb')||p.startsWith('/')||/[\\\u0000-\u001f?#%:]/.test(p)||p.split('/').some(x=>!x||x==='.'||x==='..')){
   throw new Error(`Unsafe GLB path: ${a.id}`);
  }
  const replacement=!b||b.glb!==p||b.sha256?.glb!==a.sha256?.glb||changed.has(p)||!baselineTracked.has(p);
  if(replacement)required.push(a);
  else unchanged++;
 }
 const results=[];
 for(const a of required){
  const full=resolve(root,a.glb);
  const res=await checkGlbFile(full,{id:a.id,root,maxMetallic,maxBytes,whitelist,rejectSymlinks:true});
  results.push({...res,path:a.glb});
 }
 const failures=results.filter(r=>!r.ok);
 const report={
  status:failures.length?'BLOCKED_CHANGED_ASSETS':'CHANGED_ASSETS_PASS',
  baseline_commit:baselineCommit,
  limit_bytes:maxBytes,
  max_metallic:maxMetallic,
  whitelist:[...(whitelist instanceof Set?whitelist:whitelist)],
  total:manifest.assets.length,
  changed_count:required.length,
  changed_ids:required.map(a=>a.id),
  unchanged_count:unchanged,
  passed_count:results.length-failures.length,
  failed_count:failures.length,
  failures,
 };
 if(failures.length){
  const summary=failures.map(f=>`${f.id} (${f.path}): ${f.violations.map(v=>v.message).join('; ')}`).join('\n');
  const error=new Error(`GLB material gate failed (${failures.length}/${required.length} changed assets):\n${summary}`);
  error.report=report;
  throw error;
 }
 return report;
}

function parseCliArgs(argv){
 const opts={mode:null,files:[],dir:null,baseRef:null,manifestPath:null,baseline:null,id:null,maxBytes:MAX_GLB_BYTES,maxMetallic:MAX_NONMETAL_METALLIC_FACTOR,json:false};
 for(let i=0;i<argv.length;i++){
  const arg=argv[i];
  if(arg==='--git-changed'){opts.mode='git-changed';}
  else if(arg==='--base'){opts.baseRef=argv[++i];if(!opts.baseRef)throw new Error('--base requires a ref');}
  else if(arg==='--dir'){opts.mode='dir';opts.dir=argv[++i];if(!opts.dir)throw new Error('--dir requires a directory');}
  else if(arg==='--files'){opts.mode='files';}
  else if(arg==='--manifest'){opts.mode='manifest';opts.manifestPath=argv[i+1]&&!argv[i+1].startsWith('--')?argv[++i]:'assets/manifest.json';}
  else if(arg==='--baseline'){opts.baseline=argv[++i];if(!opts.baseline)throw new Error('--baseline requires a commit SHA');}
  else if(arg==='--id'){opts.id=argv[++i];if(!opts.id)throw new Error('--id requires an asset ID');}
  else if(arg==='--max-bytes'){const n=Number(argv[++i]);if(!Number.isInteger(n)||n<0)throw new Error('--max-bytes requires a non-negative integer');opts.maxBytes=n===0?null:n;}
  else if(arg==='--max-metallic'){const n=Number(argv[++i]);if(!Number.isFinite(n)||n<0||n>1)throw new Error('--max-metallic requires a number in [0, 1]');opts.maxMetallic=n;}
  else if(arg==='--json'){opts.json=true;}
  else if(arg==='--help'||arg==='-h'){opts.mode='help';}
  else if(arg.startsWith('--')){throw new Error(`Unknown flag: ${arg}`);}
  else{opts.files.push(arg);if(!opts.mode)opts.mode='files';}
 }
 return opts;
}

async function runCli(argv){
 const opts=parseCliArgs(argv);
 if(opts.mode==='help'||!opts.mode){
  console.log('Usage: node site/glb-material-gate.mjs [--files <a.glb...> | --dir <dir> | --git-changed [--base <ref>] | --manifest [path] [--baseline <sha>]] [--id <id>] [--max-bytes <N>] [--max-metallic <0..1>] [--json]');
  return;
 }
 let report;
 if(opts.mode==='git-changed'){
  report=await checkGitChangedGlbs({baseRef:opts.baseRef,maxBytes:opts.maxBytes,maxMetallic:opts.maxMetallic});
 }else if(opts.mode==='dir'){
  report=await checkGlbDirectory(opts.dir,{maxBytes:opts.maxBytes,maxMetallic:opts.maxMetallic});
 }else if(opts.mode==='manifest'){
  const manifest=JSON.parse(await readFile(resolve(opts.manifestPath),'utf8'));
  if(opts.baseline){
   report=await checkReleaseGlbMaterials({manifest,baselineCommit:opts.baseline,maxBytes:opts.maxBytes,maxMetallic:opts.maxMetallic});
  }else{
   const results=[];
   for(const a of manifest.assets){
    results.push(await checkGlbFile(resolve(a.glb),{id:a.id,root:process.cwd(),maxBytes:opts.maxBytes,maxMetallic:opts.maxMetallic,rejectSymlinks:true}));
   }
   const failures=results.filter(r=>!r.ok);
   report={status:failures.length?'FAIL':'PASS',checked_count:results.length,passed_count:results.length-failures.length,failed_count:failures.length,limit_bytes:opts.maxBytes,max_metallic:opts.maxMetallic,whitelist:[...TRUE_METAL_WHITELIST],results,failures};
  }
 }else{
  if(!opts.files.length)throw new Error('No GLB files provided');
  report=await checkGlbPaths(opts.files,{id:opts.id,maxBytes:opts.maxBytes,maxMetallic:opts.maxMetallic});
 }
 if(opts.json){
  console.log(JSON.stringify(report,null,2));
 }else if(report.failed_count){
  for(const f of report.failures)console.error(`FAIL ${f.id??'<unknown>'} (${f.path}): ${f.violations.map(v=>v.message).join('; ')}`);
  console.error(`GLB material gate FAILED: ${report.failed_count}/${report.checked_count??report.changed_count} file(s) rejected.`);
 }else{
  console.log(`GLB material gate PASSED: ${report.checked_count??report.changed_count} file(s) checked (max metallic ${report.max_metallic}, max bytes ${report.limit_bytes??'unbounded'}).`);
 }
 if(report.status==='FAIL'||report.status==='BLOCKED_CHANGED_ASSETS')process.exitCode=1;
}

if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 try{await runCli(process.argv.slice(2));}
 catch(error){console.error(error.message);process.exitCode=1;}
}

/** Test-only isolated historical manifest. Never relax or alter original rejection suites. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,mkdtempSync,copyFileSync,constants,existsSync,symlinkSync,unlinkSync,rmSync,lstatSync,readdirSync,readlinkSync,realpathSync} from 'node:fs';
import {dirname,resolve,join,relative,sep} from 'node:path';
import {tmpdir} from 'node:os';
import {pathToFileURL} from 'node:url';
import {execFileSync,spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {assertProductionMetadata} from './production-release.mjs';
import {collectManifestProduction} from './production-publication.mjs';
import {historical295Fixture} from './test-historical295-fixture.mjs';
export const HISTORICAL_PUBLICATION_SUITES=Object.freeze(['concept-landair-release','forty-four-release','fifty-two-release','final-five-release']);
const hash=b=>createHash('sha256').update(b).digest('hex');
export function projectHistoricalManifest(manifest,reviewed){
 const result=structuredClone(manifest);
 assert(!(Object.hasOwn(result.publication||{},'production_registry')&&Object.hasOwn(result.publication||{},'production_descriptor')),'Ambiguous production routes');
 if(Object.hasOwn(result.publication||{},'production_registry')||Object.hasOwn(result.publication||{},'production_descriptor')){
  const actual=result.assets.filter(a=>a.production_release);assert.deepEqual(actual.map(a=>a.id).sort(),reviewed.map(a=>a.id).sort(),'Only exact reviewed production assets may be projected');
  for(const asset of actual)assertProductionMetadata(reviewed.find(a=>a.id===asset.id),asset);
  const ids=new Set(reviewed.map(a=>a.id));result.assets=result.assets.filter(a=>!ids.has(a.id));delete result.publication.production_descriptor;delete result.publication.production_registry;
 }else assert.equal(reviewed.length,0,'No unbound production projection');
 historical295Fixture(result);return result;
}
function privateCopy(source,target){
 mkdirSync(dirname(target),{recursive:true});try{copyFileSync(source,target,constants.COPYFILE_FICLONE);}catch(error){if(!['EXDEV','ENOTSUP','EOPNOTSUPP','EINVAL'].includes(error.code))throw error;copyFileSync(source,target);}
 const a=lstatSync(source),b=lstatSync(target);assert(a.dev!==b.dev||a.ino!==b.ino,'Fixture file must not alias source inode');
}
function dependencyInventory(root){
 const records=[];const walk=path=>{for(const name of readdirSync(resolve(root,path)).sort()){const rel=path?path+'/'+name:name,full=resolve(root,rel),stat=lstatSync(full);if(stat.isSymbolicLink()){const target=readlinkSync(full),resolved=resolve(dirname(full),target);assert(resolved.startsWith(root+sep),'Dependency link escapes private tree: '+rel);records.push({path:rel,target});}else if(stat.isDirectory())walk(rel);else{assert(stat.isFile());records.push({path:rel,sha256:hash(readFileSync(full)),mode:stat.mode&0o7777,bytes:stat.size});}}};walk('');return records;
}
export async function runHistoricalSuite(name,{source=process.cwd(),temporary=tmpdir()}={}){
 assert(HISTORICAL_PUBLICATION_SUITES.includes(name),'Unsupported historical suite');
 const original=readFileSync(resolve(source,'assets/manifest.json')),manifest=JSON.parse(original);
 const reviewed=await collectManifestProduction(source,manifest),projected=projectHistoricalManifest(manifest,reviewed);
 const paths=execFileSync('git',['ls-files','-z'],{cwd:source,maxBuffer:64*1024*1024}).toString().split('\0').filter(Boolean);
 assert(paths.includes('assets/manifest.json')&&paths.includes(`site/${name}-test.mjs`),'Real tracked source inventory required');
 const snapshot=paths.map(path=>{const f=resolve(source,path);assert(existsSync(f),'Complete checkout required; missing tracked input: '+path+'; no downloads attempted');assert(lstatSync(f).isFile()&&!lstatSync(f).isSymbolicLink(),'Complete ordinary tracked source required: '+path);return {path,sha256:hash(readFileSync(f)),mode:lstatSync(f).mode&0o7777,bytes:lstatSync(f).size};});
 const dependencyRoot=realpathSync(resolve(source,'node_modules')),dependencies=dependencyInventory(dependencyRoot);
 const limit=Number(process.env.HISTORICAL_FIXTURE_MAX_BYTES||8*1024*1024*1024);assert(Number.isSafeInteger(limit)&&limit>0);assert([...snapshot,...dependencies].reduce((n,f)=>n+(f.bytes||0),0)<=limit,'Historical private fixture exceeds its explicit byte budget');
 const fixture=mkdtempSync(join(temporary,'historical-publication-'));
 try{
  // A distinct index, not the parent's index and not an empty git inventory.
  execFileSync('git',['init','-q',fixture]);
  for(const path of paths){assert(!path.startsWith('/')&&!path.split('/').includes('..'));const full=resolve(source,path);assert(lstatSync(full).isFile()&&!lstatSync(full).isSymbolicLink(),'Ordinary tracked fixture input required: '+path);privateCopy(full,resolve(fixture,path));}
  unlinkSync(resolve(fixture,'assets/manifest.json'));writeFileSync(resolve(fixture,'assets/manifest.json'),JSON.stringify(projected,null,2)+'\n');
  const sourceCommit=execFileSync('git',['rev-parse','HEAD'],{cwd:source,encoding:'utf8'}).trim();
  const objectPath=execFileSync('git',['rev-parse','--git-path','objects'],{cwd:source,encoding:'utf8'}).trim();
  const environment={...process.env,GIT_ALTERNATE_OBJECT_DIRECTORIES:resolve(source,objectPath)};
  // Populate only this fixture's index. No new object copy or source index write.
  execFileSync('git',['read-tree',sourceCommit],{cwd:fixture,env:environment});
  assert.deepEqual(execFileSync('git',['ls-files','-z'],{cwd:fixture,maxBuffer:64*1024*1024}).toString().split('\0').filter(Boolean),paths,'Fixture index must preserve the real source inventory');
  mkdirSync(resolve(fixture,'node_modules'));for(const dep of dependencies){const target=resolve(fixture,'node_modules',dep.path);if(dep.target){mkdirSync(dirname(target),{recursive:true});const inside=relative(dirname(resolve(dependencyRoot,dep.path)),resolve(dirname(resolve(dependencyRoot,dep.path)),dep.target));symlinkSync(inside,target);}else privateCopy(resolve(dependencyRoot,dep.path),target);}
  const result=spawnSync(process.execPath,[`site/${name}-test.mjs`],{cwd:fixture,stdio:'inherit',env:environment});if(result.error)throw result.error;
  assert.equal(hash(readFileSync(resolve(source,'assets/manifest.json'))),hash(original),'Source manifest changed during isolated suite');
  return result.status??1;
 }finally{try{for(const before of snapshot){const full=resolve(source,before.path);assert.equal(hash(readFileSync(full)),before.sha256,'Source bytes changed: '+before.path);assert.equal(lstatSync(full).mode&0o7777,before.mode,'Source mode changed: '+before.path);}assert.deepEqual(dependencyInventory(dependencyRoot),dependencies,'Source installed dependencies changed');assert.deepEqual(execFileSync('git',['ls-files','-z'],{cwd:source,maxBuffer:64*1024*1024}).toString().split('\0').filter(Boolean),paths,'Source tracked inventory changed');}finally{rmSync(fixture,{recursive:true,force:true});}}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 const report={status:'RUNNING',phase:'complete-source-and-production-preflight',suite:process.argv[2]||null,expected_source:process.env.GITHUB_SHA||null,downstream:'NOT_RUN'};
 try{const status=await runHistoricalSuite(process.argv[2]);report.exit_code=status;report.status=status===0?'PASS':'FAIL';if(status!==0)report.failed_phase='historical-suite';process.exitCode=status;}
 catch(error){report.status='FAIL';report.failed_phase=report.phase;report.error=error.stack;process.exitCode=1;console.error(error);}
 finally{mkdirSync('qa/historical-publication',{recursive:true});writeFileSync(resolve('qa/historical-publication',(HISTORICAL_PUBLICATION_SUITES.includes(report.suite)?report.suite:'invalid-suite')+'.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}
}

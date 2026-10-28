import {successorReader,historicalManifestView,historicalGalleryView,historicalTurntableView} from './same-id-successors.mjs';
/** Test-only isolated historical manifest. Never relax or alter original rejection suites. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,mkdtempSync,copyFileSync,constants,existsSync,symlinkSync,unlinkSync,rmSync,lstatSync,readdirSync,readlinkSync,realpathSync,openSync,closeSync,fstatSync} from 'node:fs';
import {dirname,resolve,join,relative,sep} from 'node:path';
import {tmpdir} from 'node:os';
import {pathToFileURL} from 'node:url';
import {execFileSync,spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {assertProductionMetadata} from './production-release.mjs';
import {collectManifestProduction} from './production-publication.mjs';
import {historical295Fixture} from './test-historical295-fixture.mjs';
export const HISTORICAL_PUBLICATION_SUITES=Object.freeze([]);
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
// FD 3 is an unlinked, parent-owned handoff, never an environment bypass flag.
// The child rechecks every tracked input is private before any destructive test.
export function claimHistoricalFixture(suite){
 if(!process.argv.includes('--reuse-private-historical-fixture'))return null;
 assert.equal(suite,'concept-landair-release','Only the nested full-copy suite may reuse its private fixture');
 const fd=fstatSync(3);assert(fd.isFile()&&fd.uid===process.getuid()&&fd.nlink===0,'Handoff must be an unlinked parent-owned regular file');
 const handoff=JSON.parse(readFileSync(3,'utf8'));
 assert.equal(handoff.kind,'private-historical-fixture-v1');assert.equal(handoff.suite,suite);
 assert.equal(handoff.parent_pid,process.ppid,'Private fixture must come from this process parent');
 const root=realpathSync(process.cwd()),source=realpathSync(handoff.source);
 assert.equal(handoff.fixture,root);assert.notEqual(root,source);
 assert(!root.startsWith(source+sep)&&!source.startsWith(root+sep),'Private fixture and checkout must be separate trees');
 const owner=lstatSync(root);assert(owner.isDirectory()&&!owner.isSymbolicLink());
 assert.equal(owner.uid,process.getuid());assert.equal(owner.dev,handoff.device);assert.equal(owner.ino,handoff.inode);
 assert(Array.isArray(handoff.paths)&&handoff.paths.includes('assets/manifest.json')&&handoff.paths.includes(`site/${suite}-test.mjs`));
 const inventory=cwd=>execFileSync('git',['ls-files','-z'],{cwd,maxBuffer:64*1024*1024}).toString().split('\0').filter(Boolean);
 assert.equal(new Set(handoff.paths).size,handoff.paths.length,'Duplicate private fixture paths');
 assert.deepEqual(handoff.paths,inventory(source),'Handoff must cover the complete source inventory');
 assert.deepEqual(handoff.paths,inventory(root),'Private fixture index must match source inventory');
 for(const path of handoff.paths){
  assert(typeof path==='string'&&path&&!path.startsWith('/')&&!path.split('/').some(p=>!p||p==='.'||p==='..'));
  const original=resolve(source,path),copy=resolve(root,path),a=lstatSync(original),b=lstatSync(copy);
  assert(a.isFile()&&b.isFile()&&!a.isSymbolicLink()&&!b.isSymbolicLink());
  assert.equal(realpathSync(copy),copy);assert.equal(realpathSync(original),original);
  assert(a.dev!==b.dev||a.ino!==b.ino,'Private fixture aliases checkout inode: '+path);
 }
 return root;
}
/** Retained import compatibility only; historical batch test execution was removed. */
export async function runHistoricalSuite(){throw new Error('Historical batch tests retired; use npm test for generic integration checks.');}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){console.error('Historical batch tests retired; use npm test.');process.exitCode=1;}

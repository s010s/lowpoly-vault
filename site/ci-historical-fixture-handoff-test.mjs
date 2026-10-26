/** Process-level private-root tests. No model, browser or approval substitute. */
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,copyFileSync,rmSync,openSync,closeSync,unlinkSync,linkSync,statSync,readdirSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {createHash} from 'node:crypto';
import {join} from 'node:path';
import {spawnSync,execFileSync} from 'node:child_process';
import {projectHistoricalManifest,runHistoricalSuite} from './ci-historical-publication.mjs';
import {successorReader,historicalManifestView} from './same-id-successors.mjs';
const root=mkdtempSync(join(tmpdir(),'private-handoff-contract-')),source=join(root,'source'),fixture=join(root,'fixture');
const moduleURL=new URL('./ci-historical-publication.mjs',import.meta.url).href;
const git=(cwd,...args)=>execFileSync('git',args,{cwd,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
const paths=['assets/manifest.json','sentinel.txt','site/concept-landair-release-test.mjs'];
let checks=0;
try{
 for(const dir of [source,fixture]){mkdirSync(dir);git(dir,'init','-q');for(const sub of ['assets','site'])mkdirSync(join(dir,sub));}
 for(const path of paths){writeFileSync(join(source,path),path==='assets/manifest.json'?'{}':'ORIGINAL');copyFileSync(join(source,path),join(fixture,path));}
 for(const dir of [source,fixture])git(dir,'add','.');
 const owner=statSync(fixture),valid={kind:'private-historical-fixture-v1',suite:'concept-landair-release',parent_pid:process.pid,source,fixture,device:owner.dev,inode:owner.ino,paths};
 const probe=`import {claimHistoricalFixture} from ${JSON.stringify(moduleURL)};import {writeFileSync} from 'node:fs';const root=claimHistoricalFixture(process.env.PROBE_SUITE||'concept-landair-release');if(root)writeFileSync(root+'/sentinel.txt','PRIVATE MUTATION');else if(process.env.EXPECT_NULL!=='1')throw Error('missing claim');`;
 function run({handoff=valid,flag=true,fd=true,cwd=fixture,linked=false,suite,expectNull=false}={}){
  const handoffPath=join(root,'handoff.json');let handle;
  if(fd){writeFileSync(handoffPath,JSON.stringify(handoff),{mode:0o600});handle=openSync(handoffPath,'r');if(!linked)unlinkSync(handoffPath);}
  try{return spawnSync(process.execPath,['--input-type=module','-e',probe,...(flag?['--','--reuse-private-historical-fixture']:[])],{cwd,encoding:'utf8',stdio:fd?['ignore','pipe','pipe',handle]:['ignore','pipe','pipe'],env:{...process.env,PROBE_SUITE:suite||'concept-landair-release',EXPECT_NULL:expectNull?'1':'0'}});}
  finally{if(handle!==undefined)closeSync(handle);rmSync(handoffPath,{force:true});}
 }
 const sourceBytes=readFileSync(join(source,'sentinel.txt')),sourceMode=statSync(join(source,'sentinel.txt')).mode;
 assert.equal(run().status,0);assert.equal(readFileSync(join(fixture,'sentinel.txt'),'utf8'),'PRIVATE MUTATION');checks++;
 assert.equal(run({flag:false,fd:false,expectNull:true}).status,0);checks++;
 for(const [label,options] of [
  ['missing FD',{fd:false}],['linked handoff',{linked:true}],['wrong suite',{suite:'final-five-release'}],
  ['wrong parent',{handoff:{...valid,parent_pid:process.pid+1}}],['ordinary checkout',{cwd:source}],
  ['same tree',{handoff:{...valid,source:fixture}}],['wrong inode',{handoff:{...valid,inode:owner.ino+1}}],
  ['omitted tracked input',{handoff:{...valid,paths:paths.filter(p=>p!=='sentinel.txt')}}],
  ['duplicate path',{handoff:{...valid,paths:[...paths,paths[0]]}}],
 ]){assert.notEqual(run(options).status,0,label);checks++;}
 unlinkSync(join(fixture,'sentinel.txt'));linkSync(join(source,'sentinel.txt'),join(fixture,'sentinel.txt'));
 assert.notEqual(run().status,0,'Shared checkout inode rejected');checks++;
 assert.notEqual(run({handoff:{...valid,paths:paths.filter(p=>p!=='sentinel.txt')}}).status,0,'Cannot hide a shared inode by omitting its path');checks++;
 assert.deepEqual(readFileSync(join(source,'sentinel.txt')),sourceBytes);assert.equal(statSync(join(source,'sentinel.txt')).mode,sourceMode);checks++;
 // Real parent/child ownership and cleanup, including failure after destructive writes.
 const current=JSON.parse(readFileSync(join(process.cwd(),'assets/manifest.json')));
 const historical=historicalManifestView({manifest:current,read:successorReader(process.cwd())});
 const projected=projectHistoricalManifest(historical,historical.assets.filter(a=>a.production_release));
 writeFileSync(join(source,'assets/manifest.json'),JSON.stringify(projected));
 writeFileSync(join(source,'assets/fixture-medium.bin'),Buffer.alloc(2*1024*1024,7));
 writeFileSync(join(source,'.gitignore'),'node_modules/\n');mkdirSync(join(source,'node_modules'));
 writeFileSync(join(source,'node_modules/probe.txt'),'ORIGINAL DEPENDENCY');
 git(source,'config','user.name','Historical fixture test');git(source,'config','user.email','fixture@example.invalid');
 const temporary=join(root,'temporary');mkdirSync(temporary);
 for(const exitCode of [0,23]){
  writeFileSync(join(source,'site/concept-landair-release-test.mjs'),`import {claimHistoricalFixture} from ${JSON.stringify(moduleURL)};import {writeFileSync} from 'node:fs';if(claimHistoricalFixture('concept-landair-release')!==process.cwd())throw Error('No private root');writeFileSync('sentinel.txt','PRIVATE MUTATION');writeFileSync('node_modules/probe.txt','PRIVATE DEPENDENCY');process.exit(${exitCode});`);
  git(source,'add','.');git(source,'commit','-qm','Private parent-child ownership probe '+exitCode);
  const inventory=git(source,'ls-files'),beforeFiles=inventory.split('\n').map(path=>({path,sha256:createHash('sha256').update(readFileSync(join(source,path))).digest('hex'),mode:statSync(join(source,path)).mode}));
  assert.equal(await runHistoricalSuite('concept-landair-release',{source,temporary}),exitCode);
  assert.equal(git(source,'ls-files'),inventory,'Original tracked index unchanged');
  for(const before of beforeFiles){assert.equal(createHash('sha256').update(readFileSync(join(source,before.path))).digest('hex'),before.sha256);assert.equal(statSync(join(source,before.path)).mode,before.mode);}
  assert.deepEqual(readdirSync(temporary),[],'Outer finally removes private fixture even after child failure');
  assert.deepEqual(readFileSync(join(source,'sentinel.txt')),sourceBytes);assert.equal(statSync(join(source,'sentinel.txt')).mode,sourceMode);
  assert.equal(readFileSync(join(source,'node_modules/probe.txt'),'utf8'),'ORIGINAL DEPENDENCY');checks++;
 }
 console.log(JSON.stringify({fixture_nested_media_copy_bytes_before:2*1024*1024,fixture_nested_media_copy_bytes_after:0,measurement:'Controlled fixture payload only; full publication quota awaits CI'}));
 console.log(`PASS ${checks} private historical handoff checks; checkout bytes/mode unchanged; child success/failure cleanup verified.`);
}finally{rmSync(root,{recursive:true,force:true});assert(!readdirSync(tmpdir()).includes(root.split('/').at(-1)));}

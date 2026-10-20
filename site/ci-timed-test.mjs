/** A failed or missing mandatory suite must stop CI and preserve its nonzero status. */
import assert from 'node:assert/strict';
import {PUBLICATION_SUITES} from './ci-publication-shards.mjs';
import {mkdtemp,mkdir,writeFile,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
const root=await mkdtemp(join(tmpdir(),'lpv-timing-')),runner=resolve('site/ci-timed.mjs'),names=['initial-release','refined-release','small-life-release','small-fauna-release','small-life-batch-release','small-life-round02-release','small-life-round03-release','small-life-round04-release','small-life-round05-release','small-life-round06-release','small-life-round07-release','small-life-round08-release','small-life-round09-release','small-life-round10-release','small-life-round11-release','small-life-round12-release','small-life-round13-release','concept-seven-release','quartets-capture','concept-quartets-release','landair-capture','concept-landair-release','forty-four-release'];
try{
 assert.deepEqual(PUBLICATION_SUITES,names,'The historical mandatory suite order must remain unchanged before the appended forty-four release');
 await mkdir(join(root,'site'));for(const name of names)await writeFile(join(root,'site',name+'-test.mjs'),`import {appendFileSync} from 'node:fs';appendFileSync('events',${JSON.stringify(name+'\n')});${name==='refined-release'?'process.exit(23);':''}`);
 const run=()=>spawnSync(process.execPath,[runner,'publication'],{cwd:root,encoding:'utf8'}),report=async()=>JSON.parse(await readFile(join(root,'qa/ci-timings/publication.json')));
 assert.equal(run().status,23);assert.equal((await report()).status,'fail');assert.equal((await report()).phases.length,2);assert.equal(await readFile(join(root,'events'),'utf8'),names.slice(0,2).join('\n')+'\n');
 await writeFile(join(root,'events'),'');await writeFile(join(root,'site/refined-release-test.mjs'),"import {appendFileSync} from 'node:fs';appendFileSync('events','refined-release\\n');");assert.equal(run().status,0);assert.equal((await report()).status,'pass');assert.deepEqual((await report()).phases.map(p=>p.name),names);assert.equal(await readFile(join(root,'events'),'utf8'),names.join('\n')+'\n');
 // Both capture contracts and the release contracts are mandatory: failure and absence
 // each stop at that exact suite, including the final newly added release suite.
 for(const name of ['quartets-capture','landair-capture','concept-landair-release','forty-four-release']){
  const file=join(root,'site',name+'-test.mjs'),original=await readFile(file,'utf8'),index=names.indexOf(name);
  await writeFile(join(root,'events'),'');
  await writeFile(file,original+'process.exit(31);');
  assert.equal(run().status,31,`${name}: nonzero status must propagate`);
  assert.equal((await report()).status,'fail');
  assert.deepEqual((await report()).phases.map(p=>p.name),names.slice(0,index+1));
  assert.equal(await readFile(join(root,'events'),'utf8'),names.slice(0,index+1).join('\n')+'\n');
  await rm(file);await writeFile(join(root,'events'),'');
  assert.notEqual(run().status,0,`${name}: absence must not be silently skipped`);
  assert.equal((await report()).status,'fail');
  assert.deepEqual((await report()).phases.map(p=>p.name),names.slice(0,index+1));
  assert.equal(await readFile(join(root,'events'),'utf8'),names.slice(0,index).join('\n')+'\n');
  await writeFile(file,original);
 }
 await rm(join(root,'site/initial-release-test.mjs'));assert.notEqual(run().status,0);assert.equal((await report()).status,'fail');assert.equal((await report()).phases.length,1);
 await writeFile(join(root,'events'),'');await writeFile(join(root,'site/ci-publication.mjs'),"import {appendFileSync} from 'node:fs';appendFileSync('events','publication\\n');process.exit(19);");
 const build=()=>spawnSync(process.execPath,[runner,'build'],{cwd:root,encoding:'utf8'}),buildReport=async()=>JSON.parse(await readFile(join(root,'qa/ci-timings/build.json')));
 assert.equal(build().status,19);assert.equal((await buildReport()).phases.length,1);assert.equal((await buildReport()).status,'fail');
 await mkdir(join(root,'node_modules/vite/bin'),{recursive:true});await writeFile(join(root,'node_modules/vite/package.json'),'{'+'"type":"module"'+'}');
 for(const [file,label]of [['site/ci-publication.mjs','publication'],['site/model-registry-sync.mjs','registry'],['node_modules/vite/bin/vite.js','vite'],['site/ci-render-template.mjs','template'],['site/copy-assets.mjs','copy'],['site/audit-release.mjs','audit']])await writeFile(join(root,file),`import {appendFileSync} from 'node:fs';appendFileSync('events',${JSON.stringify(label+'\n')});`);
 await writeFile(join(root,'events'),'');assert.equal(build().status,0);assert.equal((await buildReport()).status,'pass');assert.equal(await readFile(join(root,'events'),'utf8'),'publication\n'+'registry\n'+'vite\n'+'template\n'+'copy\n'+'audit\n');
 await writeFile(join(root,'site/model-registry-sync.mjs'),'process.exit(29);');assert.equal(build().status,29);assert.equal((await buildReport()).phases.length,2);
 await writeFile(join(root,'site/model-registry-sync.mjs'),'');
 await writeFile(join(root,'site/audit-release.mjs'),'process.exit(27);');assert.equal(build().status,27);assert.equal((await buildReport()).status,'fail');assert.equal((await buildReport()).phases.length,6);
 console.log('CI timing runner: all mandatory suites, first failure status, stop-on-failure and missing-suite refusal (including both capture contracts, land/air release and forty-four release), mandatory pre-build gate and final-audit failure passed.');
}finally{await rm(root,{recursive:true,force:true});}

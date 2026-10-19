/** A failed or missing mandatory suite must stop CI and preserve its nonzero status. */
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
const root=await mkdtemp(join(tmpdir(),'lpv-timing-')),runner=resolve('site/ci-timed.mjs'),names=['initial-release','refined-release','small-life-release','small-fauna-release','small-life-batch-release','small-life-round02-release','small-life-round03-release','small-life-round04-release','small-life-round05-release','small-life-round06-release','small-life-round07-release','small-life-round08-release','small-life-round09-release','small-life-round10-release','small-life-round11-release','small-life-round12-release','small-life-round13-release','small-life-round14-release'];
try{
 await mkdir(join(root,'site'));for(const name of names)await writeFile(join(root,'site',name+'-test.mjs'),`import {appendFileSync} from 'node:fs';appendFileSync('events',${JSON.stringify(name+'\n')});${name==='refined-release'?'process.exit(23);':''}`);
 const run=()=>spawnSync(process.execPath,[runner,'publication'],{cwd:root,encoding:'utf8'}),report=async()=>JSON.parse(await readFile(join(root,'qa/ci-timings/publication.json')));
 assert.equal(run().status,23);assert.equal((await report()).status,'fail');assert.equal((await report()).phases.length,2);assert.equal(await readFile(join(root,'events'),'utf8'),names.slice(0,2).join('\n')+'\n');
 await writeFile(join(root,'events'),'');await writeFile(join(root,'site/refined-release-test.mjs'),"import {appendFileSync} from 'node:fs';appendFileSync('events','refined-release\\n');");assert.equal(run().status,0);assert.equal((await report()).status,'pass');assert.deepEqual((await report()).phases.map(p=>p.name),names);assert.equal(await readFile(join(root,'events'),'utf8'),names.join('\n')+'\n');
 await rm(join(root,'site/initial-release-test.mjs'));assert.notEqual(run().status,0);assert.equal((await report()).status,'fail');assert.equal((await report()).phases.length,1);
 await writeFile(join(root,'events'),'');await writeFile(join(root,'site/initial-release.mjs'),"import {appendFileSync} from 'node:fs';appendFileSync('events','publication\\n');process.exit(19);");
 const build=()=>spawnSync(process.execPath,[runner,'build'],{cwd:root,encoding:'utf8'}),buildReport=async()=>JSON.parse(await readFile(join(root,'qa/ci-timings/build.json')));
 assert.equal(build().status,19);assert.equal((await buildReport()).phases.length,1);assert.equal((await buildReport()).status,'fail');
 await mkdir(join(root,'node_modules/vite/bin'),{recursive:true});await writeFile(join(root,'node_modules/vite/package.json'),'{'+'"type":"module"'+'}');
 for(const [file,label]of [['site/initial-release.mjs','publication'],['node_modules/vite/bin/vite.js','vite'],['site/copy-assets.mjs','copy'],['site/audit-release.mjs','audit']])await writeFile(join(root,file),`import {appendFileSync} from 'node:fs';appendFileSync('events',${JSON.stringify(label+'\n')});`);
 await writeFile(join(root,'events'),'');assert.equal(build().status,0);assert.equal((await buildReport()).status,'pass');assert.equal(await readFile(join(root,'events'),'utf8'),'publication\n'+'vite\n'+'copy\n'+'audit\n');
 await writeFile(join(root,'site/audit-release.mjs'),'process.exit(27);');assert.equal(build().status,27);assert.equal((await buildReport()).status,'fail');assert.equal((await buildReport()).phases.length,4);
 console.log('CI timing runner: all mandatory suites, first failure status, stop-on-failure and missing-suite refusal, mandatory pre-build gate and final-audit failure passed.');
}finally{await rm(root,{recursive:true,force:true});}

/** Deterministic process fixtures only: no browser install or network request. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {installChromium,CHROMIUM_INSTALL} from './ci-install-chromium.mjs';
assert.deepEqual(CHROMIUM_INSTALL,['npx','playwright','install','--with-deps','chromium']);
async function trial(results){
 const calls=[],waits=[],logs=[];
 const status=await installChromium({run:(...args)=>{calls.push(args);const value=results[calls.length-1];if(value instanceof Error)throw value;return value;},sleep:async ms=>waits.push(ms),log:line=>logs.push(line)});
 for(const args of calls)assert.deepEqual(args,['npx',['playwright','install','--with-deps','chromium'],{stdio:'inherit',shell:false}]);
 assert.equal(logs.filter(line=>/^Chromium installation attempt \d\/3:/.test(line)).length,calls.length,'Every attempt is logged');
 return {status,calls,waits,logs};
}
let result=await trial([{status:100},{status:0}]);assert.equal(result.status,0);assert.equal(result.calls.length,2);assert.deepEqual(result.waits,[10000]);assert(result.logs.some(line=>line.includes('exit 100')));
result=await trial([{status:7},{status:8},{status:9}]);assert.equal(result.status,9,'Exhaustion preserves the final nonzero exit');assert.equal(result.calls.length,3);assert.deepEqual(result.waits,[10000,20000]);
result=await trial([{status:0}]);assert.equal(result.status,0);assert.equal(result.calls.length,1);assert.deepEqual(result.waits,[]);
result=await trial([{status:null,signal:'SIGTERM'}]);assert.equal(result.status,143);assert.equal(result.calls.length,1);assert.deepEqual(result.waits,[]);
result=await trial([new Error('spawn failed'),new Error('spawn failed'),new Error('spawn failed')]);assert.equal(result.status,1);assert.equal(result.calls.length,3);assert.equal(result.logs.filter(line=>line.includes('spawn failed')).length,3);
result=await trial([{status:0,error:new Error('not a success')},{status:0}]);assert.equal(result.calls.length,2,'An error cannot be mistaken for exit-zero success');
const cli=spawnSync(process.execPath,['site/ci-install-chromium.mjs','--ignore-failure'],{encoding:'utf8'});assert.notEqual(cli.status,0);assert(cli.stderr.includes('accepts no alternate command'));
for(const path of ['.github/workflows/pages.yml','.github/workflows/full-release-review.yml']){
 const source=readFileSync(path,'utf8');assert.equal((source.match(/run: node site\/ci-install-chromium\.mjs/g)||[]).length,2);
 assert(!source.includes('run: npx playwright install --with-deps chromium'));
 assert(source.includes('node site/ci-install-chromium-test.mjs'),'Installer contract must run before production use');
}
console.log('Chromium installer: unchanged official command, logged first-fail/then-pass, max-three/final-nonzero, bounded delays, launch errors, cancellation and no alternate commands passed.');

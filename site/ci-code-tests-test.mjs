/** Regression for the real cumulative PR diff that revived retired browser suites. */
import assert from 'node:assert/strict';
import {readFile,mkdtemp,mkdir,writeFile,copyFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
import {spawnSync} from 'node:child_process';
import {ACTIVE_CODE_TESTS,testsFor,changedPaths} from './ci-code-tests.mjs';
const expected=['site/capture-model-images-test.mjs','site/ci-code-tests-test.mjs','site/ci-live-smoke-test.mjs','site/ci-simple-build-test.mjs','site/unified-delivery-contract-test.mjs'];
assert.deepEqual(ACTIVE_CODE_TESTS,expected);
const fixture=JSON.parse(await readFile(new URL('../qa/ci-fixtures/pr77-cumulative-paths.json',import.meta.url)));
assert.equal(fixture.head,'9af07afdf4080afc52652e43f6b8face33cd0611');assert.equal(fixture.changed.length,280);assert.equal(fixture.previous_selection.length,16);
assert.deepEqual(testsFor(fixture.changed),expected,'The actual full PR diff must select only current generic fixtures');
const retired=fixture.previous_selection.filter(p=>!expected.includes(p));assert.equal(retired.length,12);
for(const path of retired){assert.deepEqual(testsFor([path]),expected);assert(!testsFor([path]).includes(path),'Retired suite must not reenter via its own changed test file');}
for(const path of ['site/new-unregistered-test.mjs','site/detail-presentation-browser.mjs','site/ci-post-release-browser.mjs','package-lock.json','scripts/qa_glb.py','.github/workflows/pages.yml'])assert.deepEqual(testsFor([path]),expected,'No inferred test execution');
for(const paths of [[],['assets/new/model.glb','assets/new/source.blend'],['site/public/gallery/new.png','qa/review.json']])assert.deepEqual(testsFor(paths),[]);
assert.deepEqual(testsFor(changedPaths({GITHUB_EVENT_PATH:'/missing/fixture'})),expected,'Unknown diff runs current fixtures, never legacy discovery');
// The real CLI must execute each selected test, stop on failure and fail on a missing
// active test, rather than silently filtering a broken allowlist into a green result.
const root=await mkdtemp(join(tmpdir(),'code-test-selection-'));
try{
 await mkdir(join(root,'site'));await copyFile(new URL('./ci-code-tests.mjs',import.meta.url),join(root,'site/ci-code-tests.mjs'));
 for(const file of expected)await writeFile(join(root,file),`import {appendFileSync} from 'node:fs';appendFileSync('calls',${JSON.stringify(file+'\n')});if(process.env.FAIL_TEST===${JSON.stringify(file)})process.exit(7);`);
 const run=fail=>spawnSync(process.execPath,['site/ci-code-tests.mjs'],{cwd:root,env:{...process.env,GITHUB_EVENT_PATH:'/missing/fixture',FAIL_TEST:fail||''},encoding:'utf8'});
 let r=run();assert.equal(r.status,0,r.stderr);assert.deepEqual((await readFile(join(root,'calls'),'utf8')).trim().split('\n'),expected);
 await writeFile(join(root,'calls'),'');r=run(expected[1]);assert.notEqual(r.status,0);assert.deepEqual((await readFile(join(root,'calls'),'utf8')).trim().split('\n'),expected.slice(0,2));
 await rm(join(root,expected[0]));assert.notEqual(run().status,0,'Missing active fixture cannot silently pass');
}finally{await rm(root,{recursive:true,force:true});}
console.log('PASS cumulative 280-path PR regression: exactly 5 active fixtures, 12 retired suites excluded, data-only skip, unknown-diff safe fallback, CLI success/failure/missing-test propagation');

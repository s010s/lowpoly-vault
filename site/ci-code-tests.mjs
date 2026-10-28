/** Code changes get unit tests; a model-data-only commit does not replay model QA. */
import {readFileSync} from 'node:fs';
import {execFileSync,spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
// Only these dependency-free/generic integration fixtures are automatic. Historical
// acceptance and browser suites remain manual/retired, even in a cumulative PR diff.
export const ACTIVE_CODE_TESTS=Object.freeze([
 'site/capture-model-images-test.mjs',
 'site/ci-code-tests-test.mjs',
 'site/ci-live-smoke-test.mjs',
 'site/ci-simple-build-test.mjs',
 'site/unified-delivery-contract-test.mjs',
]);
export function testsFor(paths){
 const code=paths.filter(p=>/^(site\/.*\.(?:mjs|js|css)|scripts\/.*\.py|\.github\/workflows\/|package(?:-lock)?\.json$|vite.config.js$)/.test(p)&&!p.startsWith('site/public/'));
 if(!code.length)return [];
 return [...ACTIVE_CODE_TESTS];
}
export function changedPaths(env=process.env){
 try{const e=JSON.parse(readFileSync(env.GITHUB_EVENT_PATH));const base=e.pull_request?.base.sha||e.before;if(!/^[a-f0-9]{40}$/.test(base)||/^0+$/.test(base))throw Error('No diff');return execFileSync('git',['diff','--name-only',base,'HEAD'],{encoding:'utf8'}).trim().split('\n').filter(Boolean);}
 catch{return ['package.json'];}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 const paths=changedPaths(),tests=testsFor(paths);console.log(JSON.stringify({changed:paths,tests,model_qa:'NOT_REPEATED'}));
 for(const file of tests){const result=spawnSync(process.execPath,[file],{stdio:'inherit'});assert.equal(result.status,0,result.error?.message||file+' failed');}
}

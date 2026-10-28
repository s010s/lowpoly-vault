/** Code changes get unit tests; a model-data-only commit does not replay model QA. */
import {existsSync,readFileSync} from 'node:fs';
import {execFileSync,spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
export function testsFor(paths){
 const code=paths.filter(p=>/^(site\/.*\.(?:mjs|js|css)|scripts\/.*\.py|\.github\/workflows\/|package(?:-lock)?\.json$|vite.config.js$)/.test(p)&&!p.startsWith('site/public/'));
 if(!code.length)return [];
 const tests=new Set(['site/unified-delivery-contract-test.mjs','site/ci-simple-build-test.mjs','site/ci-live-smoke-test.mjs']);
 // Existing generic unit tests remain useful when their implementation changes.
 for(const path of code){if(path.endsWith('-test.mjs'))tests.add(path);else if(/\.(?:mjs|js)$/.test(path))tests.add(path.replace(/\.(?:mjs|js)$/,'-test.mjs'));}
 return [...tests].filter(p=>existsSync(p)).sort();
}
export function changedPaths(env=process.env){
 try{const e=JSON.parse(readFileSync(env.GITHUB_EVENT_PATH));const base=e.pull_request?.base.sha||e.before;if(!/^[a-f0-9]{40}$/.test(base)||/^0+$/.test(base))throw Error('No diff');return execFileSync('git',['diff','--name-only',base,'HEAD'],{encoding:'utf8'}).trim().split('\n').filter(Boolean);}
 catch{return ['package.json'];}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 const paths=changedPaths(),tests=testsFor(paths);console.log(JSON.stringify({changed:paths,tests,model_qa:'NOT_REPEATED'}));
 for(const file of tests){const result=spawnSync(process.execPath,[file],{stdio:'inherit'});assert.equal(result.status,0,result.error?.message||file+' failed');}
 if(paths.some(p=>p.startsWith('scripts/')&&p.endsWith('.py'))){const result=spawnSync('python3',['-m','unittest','discover','-s','scripts','-p','test_*.py'],{stdio:'inherit'});assert.equal(result.status,0,'Pipeline code tests failed');}
}

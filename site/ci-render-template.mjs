/** Preserve the exact Vite template before static routes add catalog-dependent data. */
import {readFileSync,writeFileSync,mkdirSync,lstatSync} from 'node:fs';
import assert from 'node:assert/strict';
const source='dist/index.html',target='qa/ci-model-proof/vite-template.html';
assert(lstatSync(source).isFile()&&!lstatSync(source).isSymbolicLink(),'Vite template must be regular bytes');
const data=readFileSync(source);assert(data.length>0&&data.length<2*1024*1024,'Bounded Vite template required');
mkdirSync('qa/ci-model-proof',{recursive:true});writeFileSync(target,data);

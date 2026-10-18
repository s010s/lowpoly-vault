/** Read-only inputs; measure the actual hash/copy and existing ZIP implementation. */
import {readFile,mkdtemp,mkdir,cp,rm,writeFile} from 'node:fs/promises';
import {resolve,join,dirname} from 'node:path';
import {tmpdir} from 'node:os';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync,execFileSync} from 'node:child_process';
import {parseAst} from 'rollup/parseAst';
import assert from 'node:assert/strict';
const root=resolve(process.argv[2]||'.'),output=resolve(process.argv[3]||'qa/ci-optimization-20261018/delivery.json'),scratch=await mkdtemp(join(tmpdir(),'lpv-delivery-profile-'));
const {enrichManifest,assetFileAllowlist,creditText}=await import(pathToFileURL(resolve(root,'site/asset-delivery.mjs'))),raw=await readFile(resolve(root,'assets/manifest.json')),manifest=JSON.parse(raw),hash=b=>createHash('sha256').update(b).digest('hex'),phases=[];
async function measure(name,action){const start=performance.now(),value=await action();phases.push({name,seconds:Math.round(performance.now()-start)/1000});return value;}
try{
 const enriched=await measure('hash-stat-and-enrich-all-public-payloads',()=>enrichManifest(manifest,root));
 const files=assetFileAllowlist(enriched);await measure('copy-all-public-payloads',async()=>{for(const file of files){await mkdir(dirname(join(scratch,file)),{recursive:true});await cp(resolve(root,file),join(scratch,file));}});
 const source=await readFile(resolve(root,'site/asset-delivery.mjs'),'utf8');let python;function walk(n){if(!n||typeof n!=='object')return;if(n.type==='VariableDeclarator'&&n.id.name==='python'){if(typeof n.init?.value==='string')python=n.init.value;else if(n.init?.type==='TemplateLiteral'&&n.init.expressions.length===0)python=n.init.quasis[0].value.cooked;}for(const v of Object.values(n))if(Array.isArray(v))v.forEach(walk);else if(v&&typeof v==='object')walk(v);}walk(parseAst(source));assert(python,'Use the existing packer, not a reimplementation');
 await mkdir(join(scratch,'zips'));const jobs=enriched.assets.map(a=>({destination:join(scratch,'zips',a.id+'.zip'),files:[a.glb,a.blend].map(p=>({source:resolve(root,p),name:p.split('/').at(-1)})),credits:creditText(a,enriched)}));
 await measure('package-all-zips',()=>{const run=spawnSync('python3',['-c',python],{input:JSON.stringify(jobs),encoding:'utf8'});assert.equal(run.status,0,run.stderr);});
 for(const a of enriched.assets)assert.equal(hash(await readFile(join(scratch,'zips',a.id+'.zip'))),hash(await readFile(resolve(root,a.downloads.bundle.replace('assets/','dist/assets/')))),'ZIP bytes must match the real baseline delivery');
 const report={source_commit:execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),manifest_sha256:hash(raw),delivery_implementation_sha256:hash(source),assets:enriched.assets.length,payload_files:files.length,zip_byte_matches:jobs.length,phases};await mkdir(dirname(output),{recursive:true});await writeFile(output,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
}finally{await rm(scratch,{recursive:true,force:true});}

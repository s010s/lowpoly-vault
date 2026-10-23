/** One source acceptance, one build, one final output audit. No reusable proof or cache. */
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {checkPublishedManifest} from './initial-release.mjs';
import {checkProductionGlbs} from './ci-production-release-check.mjs';
import {readRegistry} from './model-registry-cli.mjs';
import {syncRegistry} from './model-registry-sync.mjs';
import {copyRelease} from './copy-assets.mjs';
import {auditRelease} from './audit-release.mjs';
export const BUILD_PHASES=['publication-check','registry-check','vite','seal-render-template','copy-and-package','full-release-audit'];
export async function buildRelease(){
 const productionResults=new Map();let source;
 const report={version:1,mode:'build',source_commit:process.env.GITHUB_SHA||null,phases:[],status:'running'};
 const commands=[
  async()=>{source=await checkPublishedManifest(process.cwd(),{productionResults});const models=source.assets.filter(a=>a.production_release);const result=await checkProductionGlbs('.',models);await mkdir('qa/production-static',{recursive:true});await writeFile('qa/production-static/report.json',JSON.stringify(result,null,2)+'\n');},
  async()=>syncRegistry({registry:readRegistry(process.cwd()),releaseManifest:source,targetRoot:process.cwd(),check:true}),
  async()=>{const result=spawnSync(process.execPath,['node_modules/vite/bin/vite.js','build'],{stdio:'inherit',env:process.env});assert.equal(result.status,0,result.error?.message||'Vite failed');},
  async()=>{await import('./ci-render-template.mjs');},
  async()=>{await copyRelease({source,productionResults});},
  async()=>{assert.deepEqual(JSON.parse(await readFile('assets/manifest.json')),source,'Source manifest changed during build');await auditRelease({source,productionResults});}
 ];
 try{for(let i=0;i<commands.length;i++){const started=performance.now();try{await commands[i]();report.phases.push({name:BUILD_PHASES[i],seconds:(performance.now()-started)/1000,exit_code:0,signal:null});}catch(error){report.phases.push({name:BUILD_PHASES[i],seconds:(performance.now()-started)/1000,exit_code:1,signal:null});throw error;}console.log('Build phase:',JSON.stringify(report.phases.at(-1)));}report.status='pass';}
 catch(error){report.status='fail';throw error;}
 finally{await mkdir('qa/ci-timings',{recursive:true});await writeFile('qa/ci-timings/build.json',JSON.stringify(report,null,2)+'\n');}
 return report;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)await buildRelease();

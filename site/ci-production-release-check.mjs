/** Production/static acceptance only. No browser, rerender, receipt rewrite or publication permission. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {collectProductionRelease,assertProductionMetadata} from './production-release.mjs';
export async function checkProductionRelease(root='.',onPhase=()=>{}){
 onPhase('manifest');const manifest=JSON.parse(await readFile(resolve(root,'assets/manifest.json'))),descriptor=manifest.publication?.production_descriptor;
 if(!descriptor){assert(!manifest.assets.some(a=>a.production_release),'Unbound production assets');return {status:'PASS',production_ids:[],legacy_path:true};}
 onPhase('production-collection');const assets=await collectProductionRelease(root,descriptor),actual=manifest.assets.filter(a=>a.production_release);
 assert.deepEqual(actual.map(a=>a.id).sort(),assets.map(a=>a.id).sort(),'Production manifest subject differs');
 onPhase('standard-glb-dependency');const {default:validator}=await import('gltf-validator');const results=[];
 for(const asset of assets){onPhase('standard-glb:'+asset.id);assertProductionMetadata(asset,actual.find(a=>a.id===asset.id));const bytes=await readFile(resolve(root,asset.glb));const report=await validator.validateBytes(new Uint8Array(bytes),{uri:asset.glb,maxIssues:1000});assert.equal(report.issues.numErrors,0,asset.id+': standard GLB validator errors');results.push({id:asset.id,glb_sha256:createHash('sha256').update(bytes).digest('hex'),standard_glb_errors:report.issues.numErrors,standard_glb_warnings:report.issues.numWarnings,final_media_route:asset.production_posters.route});}
 return {status:'PASS',production_ids:assets.map(a=>a.id),checks:['science-and-scope','original-independent-acceptance','frozen-budget','source-and-rebuild-pins','native-geometry','standard-glb','preview-and-final-posters','independent-projection'],models:results,browser_status:'NOT_RUN',publication_authorized:false};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 const output=process.argv[2]||'qa/production-static/report.json';
 const report={status:'RUNNING',phase:'initialize',expected_source:process.env.GITHUB_SHA||null,checks:{collection:'NOT_RUN',standard_glb:'NOT_RUN'},downstream:{build:'NOT_RUN',deployment:'NOT_RUN',browser:'NOT_RUN'}};
 try{report.phase='production-collection-and-standard-glb';const result=await checkProductionRelease('.',phase=>{report.phase=phase;});Object.assign(report,result);report.checks={collection:'PASS',standard_glb:'PASS'};report.phase='complete';}
 catch(error){report.status='FAIL';report.failed_phase=report.phase;report.error=error.stack;process.exitCode=1;console.error(error);}
 finally{await mkdir(dirname(output),{recursive:true});await writeFile(output,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}
}

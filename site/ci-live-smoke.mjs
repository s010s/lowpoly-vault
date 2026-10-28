/** Lightweight actual-site readback, not a second model QA run. */
import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
export async function checkLive({baseURL,expectedSha,fetcher=fetch}={}){
 assert(/^[a-f0-9]{40}$/.test(expectedSha||''),'Expected deployed commit required');
 const base=new URL(baseURL);assert(['https:','http:'].includes(base.protocol)&&!base.username&&!base.password,'Invalid site URL');if(!base.pathname.endsWith('/'))base.pathname+='/';
 const get=async(path,method='GET')=>{const url=new URL(path,base);assert(url.origin===base.origin&&url.pathname.startsWith(base.pathname),'Readback path escapes site');url.searchParams.set('deployment',expectedSha);const r=await fetcher(url,{method,signal:AbortSignal.timeout(20000),cache:'no-store'});assert(r.ok,`HTTP ${r.status}: ${path}`);return r;};
 const marker=await (await get('release-build.json')).json();assert.equal(marker.source_commit,expectedSha,'Deployment not yet current');
 const manifest=await(await get('assets/manifest.json')).json();assert(Array.isArray(manifest.assets)&&manifest.assets.length,'Empty deployed manifest');
 await get('models/');
 assert.equal(marker.models,manifest.assets.length,'Deployed model count differs');
 assert(Array.isArray(marker.sample)&&marker.sample.length>0&&marker.sample.length<=2,'Missing deployment sample');
 const sample=marker.sample.map(row=>{const asset=manifest.assets.find(a=>a.id===row.id);assert(asset,'Sample ID missing from live catalog');assert.equal(row.files.glb,asset.glb);assert.equal(row.files.blend,asset.blend);return {...asset,smoke_files:row.files};});
 for(const a of sample)for(const path of [`models/${a.id}/`,...Object.values(a.smoke_files)])await get(path,'HEAD');
 return {status:'PASS',source_commit:expectedSha,models:manifest.assets.length,sampled_ids:sample.map(a=>a.id),model_qa:'NOT_REPEATED'};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 let result;try{for(let attempt=0;;attempt++){try{result=await checkLive({baseURL:process.env.SITE_URL,expectedSha:process.env.DEPLOYED_SHA});break;}catch(error){if(attempt===9)throw error;await new Promise(done=>setTimeout(done,15000));}}}catch(error){result={status:'FAIL',error:error.message};process.exitCode=1;}
 await mkdir('qa/live-smoke',{recursive:true});await writeFile('qa/live-smoke/report.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
}

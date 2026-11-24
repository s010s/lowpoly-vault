/** Local immutable Pages build readback. No network; no writes to dist. */
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {lstat,mkdir,readFile,realpath,writeFile} from 'node:fs/promises';
import {resolve,sep} from 'node:path';
import {pathToFileURL} from 'node:url';
import {checkDelivery} from './ci-release-delivery.mjs';

export const BASE_URL='https://s010s.github.io/lowpoly-vault/';
export const BASELINE_SHA='44a9d6a0c56920658369b374a0aa4b458e7845f0';
const fullSha=s=>{assert(/^[a-f0-9]{40}$/.test(s||''),'Expected full candidate SHA');return s;};
const type=p=>p.endsWith('.json')?'application/json':p.endsWith('.html')?'text/html; charset=utf-8':'application/octet-stream';

const rawMember=path=>{
 assert(typeof path==='string'&&path.length>0&&path.split('/').every(p=>/^[A-Za-z0-9._-]+$/.test(p)&&p!=='.'&&p!=='..'),'Unsafe raw candidate path');
};
export async function createDistFetcher({dist,expectedSha}) {
 fullSha(expectedSha);
 const base=new URL(BASE_URL),root=resolve(dist);
 assert.equal(await realpath(root),root,'Unsafe dist root');
 assert((await lstat(root)).isDirectory(),'No dist directory');
 return async url=>{
  // URL can normalize raw dot segments before pathname is available.
  if(typeof url==='string'){
   assert(url.startsWith(BASE_URL),'Outside candidate site');
   const raw=url.slice(BASE_URL.length).split(/[?#]/,1)[0];
   rawMember(raw.endsWith('/')?raw.slice(0,-1):raw);
  }
  const u=new URL(url);
  assert(u.origin===base.origin&&!u.username&&!u.password&&!u.hash&&u.pathname.startsWith(base.pathname),'Outside candidate site');
  assert.equal(u.search,'?deployment='+expectedSha,'Wrong candidate request version');
  const path=u.pathname.slice(base.pathname.length);
  assert(path&&!/[%\\:]/.test(path),'Unsafe encoded candidate path');
  const parts=(path.endsWith('/')?path+'index.html':path).split('/');
  assert(parts.every(p=>/^[A-Za-z0-9._-]+$/.test(p)&&p!=='.'&&p!=='..'),'Unsafe candidate path');
  const target=resolve(root,...parts);
  assert(target.startsWith(root+sep),'Path outside dist');
  try {
   let current=root;
   for(let i=0;i<parts.length;i++) {
    current=resolve(current,parts[i]);
    const info=await lstat(current);
    assert(!info.isSymbolicLink()&&(i===parts.length-1?info.isFile():info.isDirectory()),'Non-regular candidate member');
   }
   assert.equal(await realpath(target),target,'Candidate alias rejected');
   return new Response(await readFile(target),{status:200,headers:{'content-type':type(target)}});
  } catch(error) {
   if(error.code==='ENOENT') return new Response('Missing candidate file',{status:404,headers:{'content-type':'text/plain'}});
   throw error;
  }
 };
}

export async function inspectCandidate({root=process.cwd(),expectedSha,git=(...args)=>execFileSync('git',['-C',root,...args],{encoding:'utf8',maxBuffer:32*1024*1024})}={}) {
 fullSha(expectedSha);
 assert.equal(git('rev-parse','HEAD').trim(),expectedSha,'Checkout is not exact candidate SHA');
 const pinned=(rev,path)=>JSON.parse(git('show',rev+':'+path));
 const [baseline,source,resources]=[pinned(BASELINE_SHA,'assets/manifest.json'),pinned(expectedSha,'assets/manifest.json'),pinned(expectedSha,'site/public/gallery/resources.json')];
 // The production verifier passes URL objects to fetcher. Scan metadata path
 // inputs before that URL construction can normalize dot-style components.
 for(const asset of source.assets) rawMember(asset.glb);
 for(const poster of Object.values(resources.posters)){
  rawMember(poster.wheel);rawMember(poster.detail);
 }
 // Selected ZIP paths and versioned gallery markers are already exact-string
 // assertions in checkDelivery before a request is built.
 const report=await checkDelivery({baseURL:BASE_URL,expectedSha,baseline,source,resources,fetcher:await createDistFetcher({dist:resolve(root,'dist'),expectedSha})});
 return {...report,evidence:'LOCAL_BUILT_DIST',scope:'Local built release artifact bytes and localized HTML; not public deployment, model acceptance or browser interaction.',baseline_commit:BASELINE_SHA};
}

if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 let report;
 try{report=await inspectCandidate({expectedSha:process.env.GITHUB_SHA});}catch(e){report={status:'FAIL',evidence:'LOCAL_BUILT_DIST',error:e.message};}
 await mkdir('qa/candidate-delivery',{recursive:true});
 await writeFile('qa/candidate-delivery/report.json',JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({status:report.status,evidence:report.evidence,source_commit:report.source_commit,selected:report.selected_count,passed:report.passed,failed:report.failed,error:report.error}));
 if(report.status!=='PASS')process.exitCode=1;
}

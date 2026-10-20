/** Fail closed on missing diff provenance; only published model IDs select GPU work. */
import {execFileSync} from 'node:child_process';
import {readFileSync,appendFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
import {isDeepStrictEqual} from 'node:util';
import {expandModelTasks} from './ci-model-shards.mjs';
export function classify(paths,manifest,full=false,context={}) {
 const previous=context.previousManifest;
 const published=Array.isArray(manifest?.assets)?manifest.assets:[];
 const before=Array.isArray(previous?.assets)?previous.assets:[];
 const changed=new Set();
 const reasons=[];
 const roles=new Set();
 const byId=new Map([...before,...published].map(asset=>[asset.id,asset]));
 const docs=path=>/^(?:README(?:\.zh-CN)?\.md|docs\/[a-zA-Z0-9_./-]+\.md)$/.test(path)&&!path.split('/').includes('..');
 const ownAsset=path=>[...byId.values()].filter(asset=>
  [asset.glb,asset.blend,asset.preview].includes(path)||
  path.startsWith(`assets/additions/${asset.id}/`)||path.startsWith(`assets/revisions/${asset.id}/`)||
  path.startsWith(`assets/card-previews/${asset.id}-`)||path.startsWith(`assets/turntables/${asset.id}/`)||
  path===`site/public/gallery/posters/${asset.id}.png`||path===`site/public/gallery/posters/${asset.id}-wheel.png`);
 let runtime=full, unknown=false;
 if(full)reasons.push('Explicit full review or unavailable diff provenance');
 for(const path of [...new Set(paths)].sort()){
  if(docs(path)){roles.add('docs');continue;}
  if(path==='assets/manifest.json'){
   roles.add('assets');
   if(!previous){unknown=true;reasons.push('Missing previous publication manifest');continue;}
   for(const asset of published)if(!isDeepStrictEqual(asset,before.find(old=>old.id===asset.id)))changed.add(asset.id);
   if(before.some(asset=>!published.some(now=>now.id===asset.id))){runtime=true;reasons.push('Published asset removal');}
   const {assets:previousAssets,...previousShared}=previous,{assets:currentAssets,...currentShared}=manifest;
   if(!isDeepStrictEqual(previousShared,currentShared)){runtime=true;reasons.push('Shared publication metadata changed');}
   continue;
  }
  // Registry data owns a published model, never a new approval or runtime exemption.
  // The stricter append validator below the scope step rejects changed old records,
  // forged refs/batches and unknown registry paths before any proof reuse.
  const record=/^registry\/models\/([a-z0-9]+(?:-[a-z0-9]+)*)\/revisions\/[a-f0-9]{64}\/record\.json$/.exec(path);
  if(record&&byId.has(record[1])){roles.add('assets');changed.add(record[1]);continue;}
  if(/^registry\/batches\/[a-z0-9]+(?:-[a-z0-9]+)*\.json$/.test(path)&&previous){
   const added=published.filter(asset=>!before.some(old=>old.id===asset.id));
   if(added.length){roles.add('assets');for(const asset of added)changed.add(asset.id);continue;}
  }
  const owners=ownAsset(path);
  if(owners.length){roles.add('assets');for(const asset of owners)changed.add(asset.id);continue;}
  if(/^(?:\.github\/|scripts\/|schemas\/|skills\/|\.agents\/)|^(?:package(?:-lock)?\.json|vite\.config\.js)$/.test(path)){
   roles.add('config');runtime=true;reasons.push(`Shared policy, validator or toolchain: ${path}`);continue;
  }
  if(path.startsWith('site/')){roles.add('runtime');runtime=true;reasons.push(`Shared runtime or validation input: ${path}`);continue;}
  roles.add('unknown');unknown=true;reasons.push(`Unclassified path: ${path}`);
 }
 runtime=runtime||unknown;
 const changedAssets=published.filter(asset=>changed.has(asset.id));
 const models=runtime||changedAssets.length>0;
 const ids=runtime?'':changedAssets.map(asset=>asset.id).sort().join(',');
 const previews=runtime||changedAssets.length>0;
 const tasks=runtime?['models','matrix','fallback','small-life','list','shared','handoff','conifer','modal','interaction','scroll','hover']:models?['models']:[];
 const probes={'catalog-scroll-browser-test.mjs':'scroll','shared-model-browser-test.mjs':'shared','image-scrub-browser-test.mjs':'list','handoff-browser-test.mjs':'handoff','hover-reveal-browser-test.mjs':'hover','modal-motion-browser-test.mjs':'modal','interaction-motion-browser-test.mjs':'interaction','browser-test.mjs':'matrix'};
 for(const [file,task]of Object.entries(probes))if(paths.includes('site/'+file))tasks.push(task);
 const changedIDs=new Set(changedAssets.map(a=>a.id)),smallProbe=paths.includes('site/small-life-browser-test.mjs');
 if(smallProbe)tasks.push('small-life');
 if(manifest.publication?.fauna_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_fauna_ids.some(id=>changedIDs.has(id))))tasks.push('fauna');
 if(manifest.publication?.batch_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_batch_ids.some(id=>changedIDs.has(id))))tasks.push('batch');
 if(manifest.publication?.round02_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round02_ids.some(id=>changedIDs.has(id))))tasks.push('round02');
 if(manifest.publication?.round03_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round03_ids.some(id=>changedIDs.has(id))))tasks.push('round03');
 if(manifest.publication?.round04_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round04_ids.some(id=>changedIDs.has(id))))tasks.push('round04');
 if(manifest.publication?.round05_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round05_ids.some(id=>changedIDs.has(id))))tasks.push('round05');
 if(manifest.publication?.round06_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round06_ids.some(id=>changedIDs.has(id))))tasks.push('round06');
 if(manifest.publication?.round07_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round07_ids.some(id=>changedIDs.has(id))))tasks.push('round07');
 if(manifest.publication?.round08_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round08_ids.some(id=>changedIDs.has(id))))tasks.push('round08');
 if(manifest.publication?.round09_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round09_ids.some(id=>changedIDs.has(id))))tasks.push('round09');
 if(manifest.publication?.round10_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round10_ids.some(id=>changedIDs.has(id))))tasks.push('round10');
 if(manifest.publication?.round11_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round11_ids.some(id=>changedIDs.has(id))))tasks.push('round11');
 if(manifest.publication?.round12_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round12_ids.some(id=>changedIDs.has(id))))tasks.push('round12');
 if(manifest.publication?.round13_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round13_ids.some(id=>changedIDs.has(id))))tasks.push('round13');
 if(previews)tasks.push('previews');
 return {category:runtime?(unknown?'unknown':roles.has('config')?'config':'runtime'):roles.has('assets')?'assets':'docs',reasons,affectedIds:changedAssets.map(asset=>asset.id).sort(),runtime,models,previews,ids,tasks:tasks.length?[...new Set(tasks)]:['none']};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 let paths=[],full=process.env.FULL_REVIEW==='true',context={};
 if(!full){try{
  const base=process.env.BASE_SHA;if(!/^[a-f0-9]{40}$/.test(base||'')||/^0+$/.test(base))throw Error('Missing base');
  paths=execFileSync('git',['diff','--name-only','-z',base,'HEAD'],{encoding:'utf8',maxBuffer:16*1024*1024}).split('\0').filter(Boolean);
  // The 217-model source manifest exceeds Node's default 1 MiB pipe buffer.
  // Keep a finite bound; unreadable/oversized provenance still falls back to full.
  const previous=path=>execFileSync('git',['show',`${base}:${path}`],{encoding:'utf8',maxBuffer:16*1024*1024});
  context={previousManifest:JSON.parse(previous('assets/manifest.json')),previousCuration:previous('site/curation.js'),currentCuration:readFileSync('site/curation.js','utf8'),previousPackage:JSON.parse(previous('package.json')),currentPackage:JSON.parse(readFileSync('package.json'))};
 }catch{full=true;console.error('Diff provenance unavailable: requiring full review.');}}
 const manifest=JSON.parse(readFileSync('assets/manifest.json'));
 const scope=classify(paths,manifest,full,context);
 scope.tasks=expandModelTasks(scope,manifest);
 for(const[key,value]of Object.entries(scope)){const line=`${key}=${Array.isArray(value)?JSON.stringify(value):value}\n`;if(process.env.GITHUB_OUTPUT)appendFileSync(process.env.GITHUB_OUTPUT,line);}
 console.log(JSON.stringify({paths,...scope},null,2));
}

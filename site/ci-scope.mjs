/** Fail closed on missing diff provenance; only published model IDs select GPU work. */
import {execFileSync} from 'node:child_process';
import {readFileSync,appendFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
import {isDeepStrictEqual} from 'node:util';
// Only the two literal editorial maps may change without changing frontend behavior.
export function editorialDataOnly(before,after) {
 const mask=source=>source.replace(/export const (PACK_LABELS|PACK_RECORDS) = ([^\n]+);/g,(statement,name,value)=>{
  const tokens=value.replace(/'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"/g,'').replace(/\b(?:PACK_LABELS|starterIds|en|zh|id|name|description|asset_ids)\b/g,'');
  if(!/^[\s{}\[\]:,]*$/.test(tokens))return statement;
  return `export const ${name} = DATA;`;
 });
 return typeof before==='string'&&typeof after==='string'&&mask(before)===mask(after);
}
export function classify(paths,manifest,full=false,context={}) {
 const runtime=full||paths.some(p=>{
  if(p==='site/curation.js'&&editorialDataOnly(context.previousCuration,context.currentCuration))return false;
  if(p==='package.json'&&context.previousPackage&&context.currentPackage){const {scripts:a,...old}=context.previousPackage,{scripts:b,...now}=context.currentPackage;if(isDeepStrictEqual(old,now))return false;}
  if(/^(package(?:-lock)?\.json|vite\.config\.js)$/.test(p))return true;
  return /^site\//.test(p)&&!/^site\/(?:ci-|.*release(?:-test)?\.mjs$|audit-release\.mjs$|accepted-small-life-batch-data\.mjs$|(?:redesign|small-life|live-release|catalog-scroll|shared-model|image-scrub|handoff|hover-reveal|modal-motion|interaction-motion)-browser-test\.mjs$|live-release-contract(?:-test)?\.mjs$)/.test(p);
 });
 const manifestChanged=paths.includes('assets/manifest.json'),previous=context.previousManifest;
 const unknown=manifestChanged&&!previous;
 const changed=manifest.assets.filter(a=>(manifestChanged&&previous&&!isDeepStrictEqual(a,previous.assets.find(b=>a.id===b.id)))||paths.some(p=>[a.glb,a.blend,a.preview].includes(p)||p.startsWith(`assets/card-previews/${a.id}-`)||p.startsWith(`assets/turntables/${a.id}/`)));
 const models=runtime||unknown||changed.length>0||paths.includes('site/redesign-browser-test.mjs');
 const ids=runtime||unknown?'':changed.map(a=>a.id).join(',');
 const previews=full||paths.some(p=>/^(site\/(viewer\.js|render-preset\.js|render-web-previews\.mjs|turntable-delivery\.mjs)|assets\/(card-previews\/|turntables\/))/.test(p))||changed.length>0;
 const tasks=runtime?['models','matrix','fallback','small-life','list','shared','handoff','conifer','modal','interaction','scroll','hover']:models?['models']:[];
 const probes={'catalog-scroll-browser-test.mjs':'scroll','shared-model-browser-test.mjs':'shared','image-scrub-browser-test.mjs':'list','handoff-browser-test.mjs':'handoff','hover-reveal-browser-test.mjs':'hover','modal-motion-browser-test.mjs':'modal','interaction-motion-browser-test.mjs':'interaction','browser-test.mjs':'matrix'};
 for(const [file,task]of Object.entries(probes))if(paths.includes('site/'+file))tasks.push(task);
 const changedIDs=new Set(changed.map(a=>a.id)),smallProbe=paths.includes('site/small-life-browser-test.mjs');
 if(smallProbe)tasks.push('small-life');
 if(manifest.publication?.fauna_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_fauna_ids.some(id=>changedIDs.has(id))))tasks.push('fauna');
 if(manifest.publication?.batch_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_batch_ids.some(id=>changedIDs.has(id))))tasks.push('batch');
 if(manifest.publication?.round02_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round02_ids.some(id=>changedIDs.has(id))))tasks.push('round02');
 if(manifest.publication?.round03_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round03_ids.some(id=>changedIDs.has(id))))tasks.push('round03');
 if(manifest.publication?.round04_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round04_ids.some(id=>changedIDs.has(id))))tasks.push('round04');
 if(manifest.publication?.round05_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round05_ids.some(id=>changedIDs.has(id))))tasks.push('round05');
 if(manifest.publication?.round06_descriptor&&(runtime||unknown||smallProbe||manifest.publication.approved_round06_ids.some(id=>changedIDs.has(id))))tasks.push('round06');
 if(previews)tasks.push('previews');
 return {runtime,models,previews,ids,tasks:tasks.length?[...new Set(tasks)]:['none']};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 let paths=[],full=process.env.FULL_REVIEW==='true',context={};
 if(!full){try{
  const base=process.env.BASE_SHA;if(!/^[a-f0-9]{40}$/.test(base||'')||/^0+$/.test(base))throw Error('Missing base');
  paths=execFileSync('git',['diff','--name-only','-z',base,'HEAD'],{encoding:'utf8'}).split('\0').filter(Boolean);
  const previous=path=>execFileSync('git',['show',`${base}:${path}`],{encoding:'utf8'});
  context={previousManifest:JSON.parse(previous('assets/manifest.json')),previousCuration:previous('site/curation.js'),currentCuration:readFileSync('site/curation.js','utf8'),previousPackage:JSON.parse(previous('package.json')),currentPackage:JSON.parse(readFileSync('package.json'))};
 }catch{full=true;console.error('Diff provenance unavailable: requiring full review.');}}
 const scope=classify(paths,JSON.parse(readFileSync('assets/manifest.json')),full,context);
 for(const[key,value]of Object.entries(scope)){const line=`${key}=${Array.isArray(value)?JSON.stringify(value):value}\n`;if(process.env.GITHUB_OUTPUT)appendFileSync(process.env.GITHUB_OUTPUT,line);}
 console.log(JSON.stringify({paths,...scope},null,2));
}

/** Exact-pose candidate only. Full release build / browser assessment is separate. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {assertOnlyTargetChanged,assertOnlyTargetResourcesChanged,assertCurrentTargetResources} from './model-commit-isolation.mjs';
import {resolveGalleryPoster} from '../../site/gallery/wheel-presentations.js';
import {checkDelivery} from '../../site/unified-delivery-contract.mjs';
import {checkGlbSizes} from '../../site/glb-size-gate.mjs';

const id='odontogriphus',subject='fix(odontogriphus): match exact gallery orientation to anterior-left pose';
const exact='35f5c7816f13d01e66aaaf413022dc1c7d6cc4343f9b4f429fa67bebe59128dc';
const git=(...args)=>execFileSync('git',args,{encoding:'utf8',maxBuffer:16*1024*1024});
const matches=git('log','--format=%H%x09%s','--fixed-strings','--grep='+subject,'--','assets/manifest.json').trim().split('\n').filter(line=>line.slice(41)===subject);
assert.equal(matches.length,1,'Expected exactly one explicitly named integration commit');
const introduced=matches[0].slice(0,40),base=introduced+'^';
const at=(ref,path)=>git('show',`${ref}:${path}`);
const manifestPath='assets/manifest.json', resourcesPath='site/public/gallery/resources.json', rendererPath='site/gallery/renderer.js';
const [manifest,resources]=await Promise.all([manifestPath,resourcesPath].map(async path=>JSON.parse(await readFile(path,'utf8'))));
const renderer=at(introduced,rendererPath),currentRenderer=await readFile(rendererPath,'utf8');
const a=manifest.assets.find(x=>x.id===id),oldManifest=JSON.parse(at(base,manifestPath)),only={...manifest,assets:[a]};
const integratedManifest=JSON.parse(at(introduced,manifestPath)),integratedResources=JSON.parse(at(introduced,resourcesPath));
assertOnlyTargetChanged(oldManifest,integratedManifest,id);
assertOnlyTargetResourcesChanged(JSON.parse(at(base,resourcesPath)),integratedResources,id);
assertCurrentTargetResources(integratedResources,resources,id);
assert.deepEqual(a,integratedManifest.assets.find(x=>x.id===id));
assert.deepEqual(a.sha256,{
 glb:exact,blend:'09c8e5f5764576de9da615b7316837c635281d5c0e00fa6817790fa29f7662fc',preview:'2dd43621a4ea433722c6c475831ad5127d3f67b13a170d7637686674ba83f5fd'
});
const poster=resolveGalleryPoster(a,resources);
assert.equal(poster.source_glb_sha256,exact);
assert.equal(poster.detailPresentation,undefined,'Preserve existing right capture/display policy');
assert.deepEqual(poster.wheelSpec,a.wheelSpec);
assert.equal(resolveGalleryPoster({...a,sha256:{glb:'0'.repeat(64)}},resources),null);
for (const [path,digest] of [[a.preview,a.sha256.preview],['site/public/'+poster.detail,a.sha256.preview],['site/public/'+poster.wheel,'eae25fc1cc4e78eaeda6b32711e6419ea8329cb53d4255bab41b774f9252bb32']]){
 assert.equal(createHash('sha256').update(await readFile(path)).digest('hex'),digest);
}
assert.equal((await checkDelivery({manifest:only,resources,hash:true})).count,1);
assert.equal((await checkGlbSizes(only)).models[0].bytes,1984624);
const additions=[
 ['DISPLAY_ORIENTATION_YAW','4.71238898038469'],
 ['DISPLAY_ORIENTATION_CANDIDATES',JSON.stringify(exact)]
];
let before=renderer;
for(const [key,value] of additions){
 const head=`const ${key}={`,entry=`${head}"${id}": ${value}, `;
 assert.equal(before.split(entry).length,2);
 before=before.replace(entry,head);
 const current=JSON.parse(currentRenderer.match(new RegExp('const '+key+'=(\\{[^\\n]+\\});'))[1]);
 assert.equal(current[id],JSON.parse(value));
}
assert.equal(before,at(base,rendererPath),'Only two exact-source map entries can differ; shared runtime unchanged');
const old=oldManifest.assets.find(x=>x.id===id);
for(const role of ['glb','blend']){
 assert.equal(old[role],a[role]);
 assert.equal(old.sha256[role],a.sha256[role]);
 assert.equal(old.file_sizes[role],a.file_sizes[role]);
}
for(const role of ['dimensions','triangles','axes','revision','revision_provenance'])assert.deepEqual(old[role],a[role]);
console.log('PASS: exact verified download bytes/paths; pose map narrowly bound to fetched source SHA; source-bound posters, unrelated models and resources unchanged');

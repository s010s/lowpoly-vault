/** Recovered candidate only. Full release build / browser assessment is separate. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {assertOnlyTargetChanged,assertOnlyTargetResourcesChanged,assertCurrentTargetResources} from './model-commit-isolation.mjs';
import {resolveGalleryPoster} from '../../site/gallery/wheel-presentations.js';
import {checkDelivery} from '../../site/unified-delivery-contract.mjs';
import {checkGlbSizes} from '../../site/glb-size-gate.mjs';

const id='beelzebufo',subject='fix(beelzebufo): recover reviewed df2 asset and gallery pairing';
const exact='df2a6ffbdca368eaed5f7ac816c69a5eb2411414c716589ef9619cdb5e396c45';
const original='e512ac0585db35aa696c2beadd6000acdc7eb053e4044e19d0a5e998238677f9';
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
 glb:exact,blend:'8e559438fb89a996ada788e9361e0ded784a1bb2f8a2c17224d0b807c7fcb6dd',preview:'04c5909ac7aae4857f3ab081d98fccf727e92350a6d2c47d183242d92ad5fc49'
});
const poster=resolveGalleryPoster(a,resources);
assert.equal(poster.source_glb_sha256,exact);
assert.deepEqual(poster.detailPresentation,{revision:2,minimum_margin:.025,screen_shift:.06,raster_size:1536});
assert.equal(resolveGalleryPoster({...a,sha256:{glb:original}},resources),null);
for (const [path,digest] of [[a.preview,a.sha256.preview],['site/public/'+poster.detail,a.sha256.preview],['site/public/'+poster.wheel,'3166956a6487a228b2888089b75e8fe32dbd4b9c37fd45ce0a815803e6bf011d']]){
 assert.equal(createHash('sha256').update(await readFile(path)).digest('hex'),digest);
}
assert.equal((await checkDelivery({manifest:only,resources,hash:true})).count,1);
assert.equal((await checkGlbSizes(only)).models[0].bytes,4772316);
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
const parse=(buf)=>{
 const n=buf.readUInt32LE(12),j=JSON.parse(buf.subarray(20,20+n)),bin=buf.subarray(28+n);
 const slices=j.bufferViews.map(({byteOffset=0,byteLength})=>bin.subarray(byteOffset,byteOffset+byteLength));
 return [j,slices];
};
const [oj,ob]=parse(await readFile(oldManifest.assets.find(x=>x.id===id).glb)),[nj,nb]=parse(await readFile(a.glb));
for(const k of ['nodes','scenes','accessors','meshes','textures','samplers','images'])assert.deepEqual(nj[k],oj[k],k);
const changed=new Set(nj.images.slice(0,2).map(i=>i.bufferView));
assert.equal(changed.size,2);
for(let i=0;i<ob.length;i++)assert.equal(ob[i].equals(nb[i]),!changed.has(i),'bufferView '+i);
assert.equal(nj.materials[0].pbrMetallicRoughness.metallicFactor,0);
delete nj.materials[0].pbrMetallicRoughness.metallicFactor;
assert.deepEqual(nj.materials,oj.materials);
console.log('PASS: exact recovered bytes; original mesh/transforms and other data views; source-scoped yaw and poster; isolated delivery');

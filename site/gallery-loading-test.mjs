/** Current data contract, without replaying historical model QA. */
import {Vector3} from 'three';
import {metricReferenceSpec} from './viewer.js';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createCatalog} from './catalog-build.mjs';
import {enrichManifest} from './asset-delivery.mjs';
import {DISPLAY_FIELDS,prepareModels,createGalleryCatalog} from './gallery/catalog-build.mjs';
import * as browser from './gallery/catalog-source.js';
const manifest=await enrichManifest(JSON.parse(await readFile('assets/manifest.json')));
const resources=JSON.parse(await readFile('site/public/gallery/resources.json'));
const original=prepareModels(manifest,resources),display=createGalleryCatalog(manifest,resources);
assert.equal(display.assets.length,manifest.assets.length);
for(let i=0;i<original.length;i++){
 for(const key of DISPLAY_FIELDS)assert.deepEqual(display.assets[i][key],original[i][key],`${original[i].id}: ${key}`);
 assert.equal(display.assets[i].sha256.glb,original[i].sha256.glb);
 const size=new Vector3(...original[i].dimensions);assert.deepEqual(metricReferenceSpec(size,display.assets[i]),metricReferenceSpec(size,original[i]),`${original[i].id}: comparison availability`);
}
const index=createCatalog(manifest).index;
assert.deepEqual(display.worlds,index.worlds);assert.deepEqual(display.packs,index.packs);
assert(Buffer.byteLength(JSON.stringify(display))<Buffer.byteLength(JSON.stringify(manifest))+Buffer.byteLength(JSON.stringify(resources)));
const before=JSON.stringify(manifest),resourceBefore=JSON.stringify(resources);createGalleryCatalog(manifest,resources);assert.equal(JSON.stringify(manifest),before);assert.equal(JSON.stringify(resources),resourceBefore);
const previousDocument=globalThis.document,previousLocation=globalThis.location;
globalThis.document={body:{dataset:{}}};globalThis.location=new URL('http://localhost/models/');
try{
 const urls=[];const fetchImpl=async url=>{urls.push(new URL(url).pathname);return {ok:true,json:async()=>structuredClone(display)};};
 await browser.loadGalleryCatalog({fetchImpl});assert.deepEqual(urls,['/assets/gallery.json']);assert.deepEqual(browser.models,display.assets);const accepted=browser.catalog,acceptedModels=browser.models;
 for(const alter of [d=>d.total++,d=>d.assets.push(d.assets[0]),d=>d.assets[0].glb='https://other.test/file.glb',d=>d.assets[0].galleryPosters.detail='gallery/../escape.png',d=>d.worlds[0].count++,d=>d.review_only=true,d=>d.kind='unknown']){
  const bad=structuredClone(display);alter(bad);await assert.rejects(browser.loadGalleryCatalog({fetchImpl:async()=>({ok:true,json:async()=>bad})}));assert.equal(browser.catalog,accepted);assert.equal(browser.models,acceptedModels);
 }
 await assert.rejects(browser.loadGalleryCatalog({fetchImpl:async()=>({ok:false,status:503})}),/503/);
 const controller=new AbortController();controller.abort();await assert.rejects(browser.loadGalleryCatalog({fetchImpl,signal:controller.signal}),{name:'AbortError'});
 let resolve;const old=browser.loadGalleryCatalog({fetchImpl:()=>new Promise(done=>resolve=done)});await browser.loadGalleryCatalog({fetchImpl});const latest=browser.catalog;resolve({ok:true,json:async()=>structuredClone(display)});await assert.rejects(old,{name:'AbortError'});assert.equal(browser.catalog,latest);
}finally{globalThis.document=previousDocument;globalThis.location=previousLocation;}
console.log(`PASS gallery loading: ${display.total} models preserve every display/camera/source field, one payload, exact facets, immutable input, malformed/failed/aborted/stale loads remain atomic`);

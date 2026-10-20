/** Data-only additions cannot approve releases or alter legacy catalog content. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile,writeFile,mkdtemp,readdir,rm} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {CATALOG_DATA,WORLD_LABELS,PACK_LABELS,PACK_RECORDS,catalogMembership,createCuration,validateCatalogData,catalogDataForAsset,inspectCatalogDataAppend} from './curation.js';
import {createCatalog} from './catalog-build.mjs';
import {writeStaticRoutes} from './static-routes.mjs';
import * as gallery from './gallery/catalog-source.js';
const hash=value=>createHash('sha256').update(typeof value==='string'?value:JSON.stringify(value)).digest('hex');
const fixture=JSON.parse(await readFile(new URL('./catalog-data-legacy-fixture.json',import.meta.url)));
const manifest=JSON.parse(await readFile(new URL('../assets/manifest.json',import.meta.url)));
const legacyAssets=fixture.asset_ids.map(id=>manifest.assets.find(asset=>asset.id===id));
assert(legacyAssets.every(Boolean),'All legacy models remain present');
const select=(object,ids)=>Object.fromEntries(ids.map(id=>[id,object[id]]));
assert.equal(hash({WORLD_LABELS:select(WORLD_LABELS,fixture.world_ids),PACK_LABELS:select(PACK_LABELS,fixture.pack_ids),PACK_RECORDS:select(PACK_RECORDS,fixture.pack_ids),memberships:[...legacyAssets,...fixture.membership_cases].map(asset=>[asset.id,catalogMembership(asset)])}),fixture.exports_sha256,'Every exported legacy label/description/owner and all 190 memberships are unchanged');
const built=createCatalog({...manifest,assets:legacyAssets});
assert.equal(hash({index:built.index,shards:[...built.shards],details:[...built.details]}),fixture.catalog_sha256,'All existing generated catalog bytes are unchanged');
assert.equal(PACK_LABELS['prehistoric-concept-landair-20261019'],undefined,'Preserve the historically missing label and fallback');
validateCatalogData(CATALOG_DATA,{manifest});
const out=await mkdtemp(join(tmpdir(),'catalog-data-'));
async function staticFiles(source,data=CATALOG_DATA){
 await writeFile(join(out,'index.html'),fixture.template);
 await writeStaticRoutes(source,out,{base:'/vault/',origin:'https://example.test',catalogData:data});
 const files={};for(const name of (await readdir(out,{recursive:true})).sort()){
  try{files[name]=await readFile(join(out,name),'utf8');}catch(error){if(error.code!=='EISDIR')throw error;}
 }
 return files;
}
try{
 const staticFixture={version:1,assets:fixture.static_asset_ids.map(id=>legacyAssets.find(asset=>asset.id===id))};
 assert.equal(hash(await staticFiles(staticFixture)),fixture.static_sha256,'Known, unknown and starter facets preserve every bilingual static byte');
 const codeFiles=['curation.js','catalog-build.mjs','static-routes.mjs','gallery/main.js','gallery/catalog-source.js'];
 const codeBefore=await Promise.all(codeFiles.map(file=>readFile(new URL(file,import.meta.url),'utf8')));
 const fake={...legacyAssets[0],id:'fixture-new-model',name:{en:'Fixture new model',zh:'夹具新模型'},collection:'fixture-new-world',worlds:['fixture-new-world'],packs:['fixture-new-pack']};
 const next=JSON.parse(JSON.stringify(CATALOG_DATA));
 next.worlds.push({id:'fixture-new-world',name:{en:'Fixture world',zh:'夹具世界'}});
 next.packs.push({id:'fixture-new-pack',name:{en:'Fixture pack',zh:'夹具组合'},description:{en:'Test only. Not approved.',zh:'仅供测试，未经批准。'},asset_ids:[fake.id]});
 const nextManifest={...manifest,assets:[...manifest.assets,fake]};
 const addition=inspectCatalogDataAppend(CATALOG_DATA,next,{addedAssetIds:[fake.id],previousManifest:manifest,currentManifest:nextManifest});
 assert.deepEqual(addition,{addedWorlds:[next.worlds.at(-1)],addedPacks:[next.packs.at(-1)],affectedIds:[fake.id]});
 for(const asset of legacyAssets)assert.deepEqual(catalogDataForAsset(asset,next),catalogDataForAsset(asset),'Pure additions do not change any existing model proof inputs');
 const withBatch=createCatalog(nextManifest,{catalogData:next});
 assert.deepEqual(withBatch.index.packs.find(pack=>pack.id==='fixture-new-pack'),{id:'fixture-new-pack',count:1,...Object.fromEntries(Object.entries(next.packs.at(-1)).filter(([key])=>key!=='id'))});
 assert.deepEqual(withBatch.index.worlds.find(world=>world.id==='fixture-new-world'),{id:'fixture-new-world',count:1,name:next.worlds.at(-1).name});
 const addedStatic=await staticFiles({assets:[fake]},next);
 assert(addedStatic['models/fixture-new-model/index.html'].includes('Fixture pack'));
 assert(addedStatic['models/fixture-new-model/index.html'].includes('?world=fixture-new-world'));
 assert(addedStatic['zh-CN/models/fixture-new-model/index.html'].includes('夹具组合'));
 assert(addedStatic['zh-CN/models/fixture-new-model/index.html'].includes('夹具世界'));
 assert.deepEqual(await Promise.all(codeFiles.map(file=>readFile(new URL(file,import.meta.url),'utf8'))),codeBefore,'Appending inert data never edits executable files');
 assert.equal(createCatalog(manifest,{catalogData:next}).index.total,manifest.assets.length,'Data records do not publish models absent from the manifest');
 assert(!createCatalog(manifest,{catalogData:next}).index.packs.some(pack=>pack.id==='fixture-new-pack'));
 assert.throws(()=>createCatalog({...nextManifest,review_only:true},{catalogData:next,approvedOnly:true}),/review-only/,'Data cannot approve review-only models');
 assert(!codeBefore[3].includes('curation.js')&&!codeBefore[3].includes('catalog-data.json'),'The browser bundle does not embed editable catalog data');
 const packSource=codeBefore[3].match(/^function packLabel\(id\).*$/m)[0];
 const label=Function('catalog','state',`const packLabels=Object.fromEntries(catalog.packs.map(record=>[record.id,record.name]));const packNames={'prehistoric-starter':['Starter collection','初始精选'],'prehistoric-small-life-round12-20261018':['Small life · XII','小生命 · XII']};${packSource};return packLabel;`);
 for(const lang of ['en','zh']){
  const actual=label(withBatch.index,{lang});
  for(const id of [...fixture.pack_ids,'prehistoric-concept-landair-20261019'])assert.equal(actual(id),PACK_LABELS[id]?.[lang]||id.replace('prehistoric-small-life-','Small life · ').replace('-20261018','').replace('round',''));
  assert.equal(actual('fixture-new-pack'),next.packs.at(-1).name[lang]);
 }
 const invalid=mutate=>{const data=structuredClone(CATALOG_DATA);mutate(data);assert.throws(()=>validateCatalogData(data),/Invalid catalog data/);};
 invalid(data=>data.worlds.push(data.worlds[0]));
 invalid(data=>data.packs.push(data.packs[0]));
 invalid(data=>data.packs[0].asset_ids.push(data.packs[0].asset_ids[0]));
 invalid(data=>data.worlds[0].id='constructor');
 invalid(data=>data.worlds[0].id='../escape');
 invalid(data=>data.packs[0].name={en:'No Chinese'});
 invalid(data=>data.packs[0].name.zh='');
 invalid(data=>data.packs[0].description.en='bad\ntext');
 invalid(data=>data.packs[0].approved=true);
 invalid(data=>data.legacy_memberships[0].pack_id='not-declared');
 invalid(data=>data.legacy_memberships[0].asset_ids=['not-an-owner']);
 invalid(data=>Object.defineProperty(data.packs[0],'__proto__',{value:{approved:true},enumerable:true}));
 invalid(data=>data.packs[0]=null);
 invalid(data=>data.version=2);
 const rejectAppend=mutate=>{const data=structuredClone(next);mutate(data);assert.throws(()=>inspectCatalogDataAppend(CATALOG_DATA,data,{addedAssetIds:[fake.id],previousManifest:manifest,currentManifest:nextManifest}),/Invalid catalog data/);};
 rejectAppend(data=>data.packs[0].name.en+=' changed');
 rejectAppend(data=>data.packs[0].asset_ids.reverse());
 rejectAppend(data=>data.packs.reverse());
 rejectAppend(data=>data.worlds[0].name.zh+=' changed');
 rejectAppend(data=>data.legacy_memberships[0].asset_ids.reverse());
 rejectAppend(data=>data.packs.at(-1).asset_ids=[legacyAssets[0].id]);
 rejectAppend(data=>data.packs.at(-1).asset_ids=['not-authorized']);
 assert.throws(()=>inspectCatalogDataAppend(CATALOG_DATA,next,{addedAssetIds:[fake.id,legacyAssets[0].id],previousManifest:manifest}),/existing model/);
 const legacyGap=structuredClone(CATALOG_DATA);legacyGap.packs.push({id:'prehistoric-concept-landair-20261019',name:{en:'New label',zh:'新标签'},description:{en:'Not an append-only change',zh:'不是纯新增'},asset_ids:['sapeornis']});
 assert.throws(()=>inspectCatalogDataAppend(CATALOG_DATA,legacyGap,{addedAssetIds:['sapeornis'],previousManifest:manifest}),/existing model/);
 const orphan=structuredClone(CATALOG_DATA);orphan.packs[0].asset_ids.push('orphan');
 assert.throws(()=>validateCatalogData(orphan,{manifest}),/unknown model/);
 const missingOwner=structuredClone(CATALOG_DATA);missingOwner.packs[0].asset_ids.pop();
 assert.throws(()=>validateCatalogData(missingOwner,{manifest}),/omits owner/);
 // Three asynchronous prerequisites must resolve before any exported state changes.
 globalThis.document={body:{dataset:{}}};globalThis.location=new URL('http://localhost/models/');
 const values={'assets/manifest.json':nextManifest,'gallery/resources.json':{},'assets/catalog.json':withBatch.index};
 const fetchNow=async url=>({ok:true,json:async()=>structuredClone(values[new URL(url).pathname.slice(1)])});
 const initialModels=gallery.models,initialCatalog=gallery.catalog;
 let resolveIndex;const indexReady=new Promise(resolve=>resolveIndex=resolve);
 const delayed=gallery.loadGalleryCatalog({fetchImpl:async url=>new URL(url).pathname.endsWith('/assets/catalog.json')?indexReady:fetchNow(url)});
 await new Promise(resolve=>setImmediate(resolve));assert.equal(gallery.models,initialModels);assert.equal(gallery.catalog,initialCatalog);
 resolveIndex({ok:true,json:async()=>withBatch.index});await delayed;
 assert.deepEqual(gallery.catalog.packs,withBatch.index.packs);assert.deepEqual(gallery.catalog.worlds,withBatch.index.worlds);
 const acceptedModels=gallery.models,acceptedCatalog=gallery.catalog;
 for(const failure of ['http','malformed','count','owners','duplicate','review']){
  await assert.rejects(()=>gallery.loadGalleryCatalog({fetchImpl:async url=>{
   if(!new URL(url).pathname.endsWith('/assets/catalog.json'))return fetchNow(url);
   if(failure==='http')return {ok:false,status:503};
   const index=structuredClone(withBatch.index);
   if(failure==='malformed')index.packs[0].name={en:42,zh:'文字'};
   if(failure==='count')index.total++;
   if(failure==='owners')index.packs.at(-1).asset_ids=['not-present'];
   if(failure==='duplicate')index.packs[1]=index.packs[0];
   if(failure==='review')index.review_only=true;
   return {ok:true,json:async()=>index};
  }}),/Catalog|catalog/);
  assert.equal(gallery.models,acceptedModels);assert.equal(gallery.catalog,acceptedCatalog);
 }
 const controller=new AbortController();controller.abort();
 await assert.rejects(()=>gallery.loadGalleryCatalog({fetchImpl:fetchNow,signal:controller.signal}),{name:'AbortError'});
 let finishOlder;const olderReady=new Promise(resolve=>finishOlder=resolve);
 const older=gallery.loadGalleryCatalog({fetchImpl:async url=>new URL(url).pathname.endsWith('/assets/catalog.json')?olderReady:fetchNow(url)});
 await gallery.loadGalleryCatalog({fetchImpl:fetchNow});const newest=gallery.catalog;
 finishOlder({ok:true,json:async()=>withBatch.index});await assert.rejects(()=>older,{name:'AbortError'});assert.equal(gallery.catalog,newest);
 console.log('Catalog data passed: all 190 legacy exports/memberships/catalog bytes and bilingual static fixtures unchanged; JSON-only additions provide labels/routes without approval or existing model key changes; strict schema/append ownership guards; atomic, delayed, interrupted, superseded and mismatched gallery index loads.');
}finally{await rm(out,{recursive:true,force:true});}

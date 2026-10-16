/** Synthetic scale fixtures stay in memory and never become production records. */
import assert from 'node:assert/strict';
import {createCatalog} from './catalog-build.mjs';
import {CatalogStore} from './catalog.js';
import {filterAndSortCatalog,routeHref,parseRoute,queryFromParams,queryToParams} from './routes.js';
const categories=['plants','geology','wood','traces','animals','fungi','terrain','water','props','structures','rocks','leaves','flowers','vehicles','tools','food','abstract'];
const assets=Array.from({length:10000},(_,i)=>({id:`scale-${i}`,name:{en:`Scale ${String(i).padStart(5,'0')}`,zh:i===9999?'深页测试模型':`模型 ${i}`},category:i<4300?'plants':categories[(i*7)%categories.length],collection:i%2?'prehistoric':'fiction',worlds:i%7===0?['prehistoric','fiction']:[i%2?'prehistoric':'fiction'],packs:[`pack-${i%19}`,...(i%11===0?['overlapping-pack']:[])],preview:`assets/scale/${i}.png`,glb:`assets/scale/${i}.glb`,triangles:i%23===0?null:(i*331)%15000,description:{en:'Fixture only',zh:'仅供测试'}}));
const started=performance.now();
const catalog=createCatalog({assets,review_only:true});
const buildMilliseconds=performance.now()-started;
assert(catalog.index.categories.length>=15,'Exercise genuinely many categories');
assert(Math.max(...catalog.index.categories.map(c=>c.count))>Math.min(...catalog.index.categories.map(c=>c.count))*5,'Exercise uneven category sizes');
const files=new Map([['assets/catalog.json',catalog.index],...catalog.shards,...catalog.details]);
let requests=0;
const store=new CatalogStore({baseURL:'https://example.test/lowpoly-vault/',fetchImpl:async url=>{requests++;const item=files.get(new URL(url).pathname.replace('/lowpoly-vault/',''));return {ok:!!item,status:item?200:404,json:async()=>item};}});
await store.load();
const firstRequests=requests;await store.search();assert.equal(requests-firstRequests,0);const deepRequests=requests;await store.search({page:416});const deepPageRequests=requests-deepRequests;assert.equal(deepPageRequests,1);
const summaries=[...catalog.shards.values()].flatMap(s=>s.items);
for(const options of [{world:'fiction',page:73},{pack:'overlapping-pack',page:15},{category:'plants',world:'prehistoric',pack:'pack-7',sort:'triangles-desc'},{world:'fiction',pack:'pack-13',maxTriangles:1000,sort:'triangles-asc'},{maxTriangles:500,page:99},{query:'深页',world:'prehistoric'},{category:'wood',sort:'name-desc',page:90}]){
 const actual=await store.search(options),expected=filterAndSortCatalog(summaries,options);
 assert.equal(actual.total,expected.length,JSON.stringify(options));
 assert.deepEqual(actual.items.map(x=>x.id),expected.slice(actual.page*24,(actual.page+1)*24).map(x=>x.id));
 assert(store.shardCache.size<=8);
}
for(const root of ['/','/lowpoly-vault/','/custom/deep/'])for(const lang of ['en','zh-CN'])for(const route of [{type:'home'},{type:'about'},{type:'models',page:0},{type:'models',page:33},{type:'detail',id:'natural-arch'}]){
 const actual=parseRoute(routeHref({...route,lang},root),root);assert.equal(actual.type,route.type);assert.equal(actual.lang,lang);if(route.id)assert.equal(actual.id,route.id);if(route.page)assert.equal(actual.page,route.page);
}
const query={query:'fern 树',category:'plants',world:'prehistoric',pack:'prehistoric-starter',sort:'triangles-desc',maxTriangles:5000,page:3,view:'map'};
const parsed=queryFromParams(queryToParams(query));for(const [key,value]of Object.entries(query))assert.equal(parsed[key],value);
assert.equal(parseRoute('/other/models/id/','/lowpoly-vault/').type,'not-found');
assert.throws(()=>routeHref({type:'detail',id:'../x'},'/'),/Invalid/);
console.log(JSON.stringify({result:'Catalog v2 passed',assets:10000,categories:catalog.index.categories.length,unevenCounts:true,multiWorld:true,multiPack:true,maxTriangles:true,requests,cacheBound:8,indexBytes:Buffer.byteLength(JSON.stringify(catalog.index)),summaryShards:catalog.shards.size,summaryBytes:Buffer.byteLength(JSON.stringify([...catalog.shards.values()])),buildMilliseconds:Math.round(buildMilliseconds),deepPageRequests},null,2));

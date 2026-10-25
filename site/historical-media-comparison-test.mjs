/** Complete selected mesh/current-media boundary regression, using real checked-in evidence. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {historicalMediaComparison} from './historical-media-comparison.mjs';
import {successorContext,successorReader,MESH_SUCCESSOR_IDS} from './same-id-successors.mjs';
import {collectBatches5253Additions,collectBatches5657Additions,collectBatches5859Additions,collectBatches6267Additions} from './concept-landair-release.mjs';
import {collectFortyFourAdditions} from './forty-four-release.mjs';
import {collectFiftyTwoAdditions} from './fifty-two-release.mjs';
const root=process.cwd(),read=successorReader(root),manifest=JSON.parse(read('assets/manifest.json'));
const turntables=JSON.parse(read('assets/turntables/index.json')),gallery=JSON.parse(read('site/public/gallery/resources.json'));
const context=successorContext({manifest,read});assert(context,'Actual authorized successor selection required');
const routes={
 'azolla':'small-life-round10:immutable-only','waterfall-ledge':'small-life-round08:immutable-only','onoclea':'small-life:immutable-only','salvinia':'small-life-round07:immutable-only','folded-strata-outcrop':'small-life-round12:immutable-only',
 'welded-ignimbrite-outcrop':'batch53:card','deflation-hollow':'batches56-57:card','barchan-dune':'batches58-59:card','rotational-landslide':'batches62-67:card+gallery','hanging-valley':'fixed44:card+gallery','pertica':'fixed52:card+gallery','oncoid-bed':'fixed52:card+gallery','arroyo-wash':'fixed52:card+gallery','kame-mound':'fixed52:card+gallery'
};assert.deepEqual(Object.keys(routes).sort(),[...MESH_SUCCESSOR_IDS].sort());
const sha=b=>createHash('sha256').update(b).digest('hex'),paths=['assets/manifest.json','assets/turntables/index.json','site/public/gallery/resources.json',manifest.publication.same_id_successors.path],before=paths.map(path=>sha(read(path)));
let checks=0;const results=[];
try{
 const media=historicalMediaComparison({root,turntables,gallery});
 for(const {entry,previous} of context.entries.filter(row=>row.entry.kind==='mesh')){
  const expected=[previous.turntable.poster];assert.deepEqual(media.cardRows(entry.id,expected),expected);assert.deepEqual(media.galleryPoster(entry.id,previous.gallery.poster),previous.gallery.poster);checks+=2;
  const cards=structuredClone(turntables);cards.posters.find(row=>row.id===entry.id).path+='unapproved';assert.throws(()=>assert.deepEqual(historicalMediaComparison({root,turntables:cards}).cardRows(entry.id,expected),expected));checks++;
  const resources=structuredClone(gallery);resources.posters[entry.id].detail+='unapproved';assert.throws(()=>assert.deepEqual(historicalMediaComparison({root,gallery:resources}).galleryPoster(entry.id,previous.gallery.poster),previous.gallery.poster));checks++;
  // Exact old fixtures must not need any manifest, even for a selected ID.
  const legacy=historicalMediaComparison({root:'/nonexistent-historical-fixture',turntables:{posters:expected},gallery:{posters:{[entry.id]:previous.gallery.poster}}});assert.deepEqual(legacy.cardRows(entry.id,expected),expected);assert.deepEqual(legacy.galleryPoster(entry.id,previous.gallery.poster),previous.gallery.poster);checks+=2;
 }
 const first=context.entries.find(row=>row.entry.kind==='mesh'),bad=structuredClone(gallery);bad.files.find(row=>row.path===first.previous.gallery.files[0].path).sha256='0'.repeat(64);assert.throws(()=>historicalMediaComparison({root,gallery:bad}).galleryPoster(first.entry.id,first.previous.gallery.poster));checks++;
 const selected=new Set(context.entries.map(row=>row.entry.id)),unselected=turntables.posters.find(row=>!selected.has(row.id));assert(unselected);
 const unrelatedCards=structuredClone(turntables);unrelatedCards.posters.find(row=>row.id===unselected.id).path+='unapproved';assert.throws(()=>assert.deepEqual(historicalMediaComparison({root,turntables:unrelatedCards}).cardRows(unselected.id,[unselected]),[unselected]));checks++;
 const unrelatedID=Object.keys(gallery.posters).find(id=>!selected.has(id)),unrelatedGallery=structuredClone(gallery);assert(unrelatedID);unrelatedGallery.posters[unrelatedID].detail+='unapproved';assert.throws(()=>assert.deepEqual(historicalMediaComparison({root,gallery:unrelatedGallery}).galleryPoster(unrelatedID,gallery.posters[unrelatedID]),gallery.posters[unrelatedID]));checks++;
 console.log(JSON.stringify({status:'PASS',phase:'all14-authenticated-media-boundaries',checks,routes}));
 const publication=manifest.publication;
 const groups=[
 ['batch53',()=>collectBatches5253Additions(root,publication.batches52_53_descriptors.find(p=>p.path==='assets/releases/batch53-20261020.json'))],
 ['batches56-57',()=>collectBatches5657Additions(root,publication.batches56_57_descriptors)],
 ['batches58-59',()=>collectBatches5859Additions(root,publication.batches58_59_descriptors)],
 ['batches62-67',()=>collectBatches6267Additions(root,publication.batches62_67_descriptors)],
 ['fixed44',()=>collectFortyFourAdditions(root,publication.forty_four_descriptors)],
 ['fixed52',()=>collectFiftyTwoAdditions(root,publication.fifty_two_descriptors)]
 ];
 for(const [group,collect] of groups){const value=await collect(),ids=value.additions.map(a=>a.id);for(const [id,route] of Object.entries(routes))if(route.startsWith(group+':'))assert(ids.includes(id));results.push({group,count:ids.length,status:'PASS'});console.log('PASS historical collector',group,ids.length);checks++;}
 console.log(JSON.stringify({status:'PASS',checks,routes,collectors:results,claim:'All current-media collector boundaries and immutable original checks; no browser/world/physics claim'}));
}finally{for(let i=0;i<paths.length;i++)assert.equal(sha(read(paths[i])),before[i],'Source aggregate mutated: '+paths[i]);}

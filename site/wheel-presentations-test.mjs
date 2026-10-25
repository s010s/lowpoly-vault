import {successorReader,historicalManifestView} from './same-id-successors.mjs';
/** Focused additive correction checks. Does not claim fresh browser/GPU visual approval. */
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import index from './gallery/wheel-presentations-index.js';
import {resolveGalleryPoster,resolveWheelPoster,validPresentationSpec} from './gallery/wheel-presentations.js';
import {prepareModels,loadGalleryCatalog} from './gallery/catalog-source.js';
import {galleryStartupContent} from './gallery/startup.mjs';
import {wheelHistoricalBaseline} from './wheel-historical-baseline.mjs';
import {assertWheelSpec,assertWheelPNG} from './wheel-presentation-contract.mjs';

const read=path=>readFile(new URL('../'+path,import.meta.url));
const json=async path=>JSON.parse(await read(path));
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const manifest=await json('assets/manifest.json');
const resources=await json('site/public/gallery/resources.json');
const historical=await wheelHistoricalBaseline(new URL('..',import.meta.url).pathname,manifest,resources,index);
const affected=historical.manifest.assets.filter(asset=>resources.posters[asset.id]?.render_route==='blender-cycles-cpu-v1'&&!resources.posters[asset.id].wheelSpec);
const first=affected[0],ordinary=manifest.assets[0];
const copy=value=>structuredClone(value);

// These baseline seals protect immutable inputs without re-rendering the library.
test('index membership is exactly the 242 original unframed Blender wheels',async()=>{
  assert.equal(index.version,1);assert.equal(index.kind,'wheel-only-presentations');
  assert.equal(historical.manifest.assets.length,594);assert.equal(index.count,242);
  assert.deepEqual(Object.keys(index.presentations),affected.map(asset=>asset.id));
  assert.deepEqual(affected.map(asset=>asset.id),historical.manifest.assets.slice(352).map(asset=>asset.id));
  // Exact historical global seals are authenticated by wheelHistoricalBaseline above.
  assert.deepEqual(historicalManifestView({manifest,read:successorReader(new URL('..',import.meta.url).pathname)}).assets.slice(0,594),historical.manifest.assets);
  assert.equal(index.review_summary.physical_gpu,'unknown');
  assert.equal(index.review_summary.publication_authority,false);
});

test('every new PNG and same-call framing is bound to preserved capture/report evidence',async()=>{
  for(const pin of Object.values(index.evidence)){
    const bytes=await read(pin.path);assert.equal(bytes.length,pin.bytes,pin.path);assert.equal(hash(bytes),pin.sha256,pin.path);
  }
  const report=await json(index.evidence.batch_report.path);
  const pixelReport=await json(index.evidence.decoded_pixels.path);
  const records=await json(index.evidence.capture_records.path);
  const review=await json(index.evidence.review_summary.path);
  assert.equal(review.status,'pass');assert.equal(review.visual_review.count,242);assert.equal(review.physical_gpu,'unknown');
  assert.equal(records.records.length,242);assert.equal(report.cases.length,242);
  assert.equal(report.source_commit,index.source_commit);assert.equal(report.baseline_commit,index.baseline_commit);
  assert.equal(report.renderer_sha256,index.renderer_sha256);assert.equal(report.browser_version,index.browser_version);
  assert.equal(report.status,'capture-and-geometry-check-pass');assert.deepEqual(report.errors,[]);
  // Source reports remain authentic, rather than changing their original pending labels.
  assert.equal(report.visual_review,'pending');assert.equal(report.publication_authority,false);
  for(const asset of affected){
    const entry=index.presentations[asset.id],saved=records.records.find(row=>row.id===asset.id),capture=saved.record;
    const original=Buffer.from(JSON.stringify(capture,null,2));
    assert.equal(hash(original),saved.sha256,asset.id+' original capture encoding');assert.equal(original.length,saved.bytes);
    assert.equal(saved.sha256,entry.capture_sha256);assert.equal(capture.id,asset.id);
    assert.equal(capture.source_glb_sha256,asset.sha256.glb);assert.equal(entry.source_glb_sha256,asset.sha256.glb);
    assert.equal(capture.previous_wheel_sha256,entry.previous_wheel.sha256);assert.equal(capture.unchanged_detail_sha256,entry.unchanged_detail.sha256);
    assert.equal(capture.renderer_sha256,index.renderer_sha256);assert.equal(capture.browser_version,index.browser_version);
    assert.equal(capture.visual_review,'pending');assert.equal(capture.publication_authority,false);
    assert.deepEqual(capture.png,entry.png);assert.deepEqual(capture.wheelSpec,entry.wheelSpec);assertWheelSpec(entry.wheelSpec);
    assertWheelPNG(await read('site/public/'+entry.wheel),entry.png);
    const result=report.cases.find(row=>row.id===asset.id);
    assert.equal(result.source_glb_sha256,entry.source_glb_sha256);assert.equal(result.wheel_sha256,entry.png.sha256);
    assert.deepEqual(result.spec,entry.wheelSpec);assert.equal(result.first_frame_id,asset.id);
    assert.equal(result.context_lost,false);assert.equal(result.gl_error,0);assert.equal(result.status,'geometry-check-pass');
    assert.deepEqual(entry.capture_binding,{source_glb_sha256:result.source_glb_sha256,wheel_sha256:result.wheel_sha256,first_frame_id:result.first_frame_id});
    assert.deepEqual(entry.checks.decoded_pixels,pixelReport.cases.find(row=>row.id===asset.id));
    assert.deepEqual(entry.checks.lifecycle,result.lifecycle);
    const selected=resolveWheelPoster(asset,resources);assert.equal(selected.wheel,entry.wheel);assert.equal(selected.detail,resources.posters[asset.id].detail);
  }
});

test('ordinary assets cannot be overridden, even by an injected matching entry',()=>{
  const fake=copy(index),poster=resources.posters[ordinary.id];fake.presentations[ordinary.id]={...copy(index.presentations[first.id]),id:ordinary.id,source_glb_sha256:ordinary.sha256.glb};
  assert.equal(resolveWheelPoster(ordinary,resources,fake),poster);
  const specAdded=copy(resources);specAdded.posters[first.id].wheelSpec=copy(poster.wheelSpec);
  assert.equal(resolveWheelPoster(first,specAdded),specAdded.posters[first.id]);
  const nonBlender={...first,production_posters:{route:'browser'}};
  assert.equal(resolveWheelPoster(nonBlender,resources),resources.posters[first.id]);
});

test('unknown IDs, wrong source/new/old hashes, malformed framing and paths fail closed',()=>{
  const unknown={...first,id:'future-unreviewed-wheel'};
  const expanded={...resources,posters:{...resources.posters,[unknown.id]:resources.posters[first.id]}};
  assert.equal(resolveWheelPoster(unknown,expanded),expanded.posters[unknown.id]);
  assert.equal(resolveWheelPoster({...first,sha256:{glb:'f'.repeat(64)}},resources),null);
  for(const mutate of [
    e=>e.id='other',e=>e.source_glb_sha256='f'.repeat(64),e=>e.png.sha256='f'.repeat(64),
    e=>e.capture_binding.first_frame_id='other',e=>e.capture_sha256='not-a-hash',
    e=>e.previous_wheel.sha256='f'.repeat(64),e=>e.unchanged_detail.sha256='f'.repeat(64),
    e=>e.production_descriptor='different-release.json',e=>e.wheel='https://other.invalid/wheel.png',
    e=>e.wheel='wheel-presentations/../other.png',e=>e.wheelSpec.zoom=NaN,e=>e.wheelSpec.offset=[0],
    e=>e.wheelSpec.projectedBounds.right=e.wheelSpec.projectedBounds.left,
  ]){const changed=copy(index);mutate(changed.presentations[first.id]);assert.equal(resolveWheelPoster(first,resources,changed),resources.posters[first.id]);}
  assert.equal(resolveWheelPoster(first,resources,null),resources.posters[first.id]);
  assert.equal(validPresentationSpec({}),false);
});

test('actual native SSR and hydration select identical wheel/detail URLs, preserving first352',()=>{
  const before=JSON.stringify(resources),assetsBefore=JSON.stringify(manifest);
  const models=prepareModels(manifest,resources),base='/lowpoly-vault/';
  const html=galleryStartupContent(manifest.assets,{lang:'en',base},{header:'<header>Wheel parity</header>',resources});
  for(let i=0;i<manifest.assets.length;i++){
    const asset=manifest.assets[i],model=models[i],original=resources.posters[asset.id];
    const row=html.match(new RegExp('<a class="slot"[^>]*data-id="'+asset.id+'"[^>]*>[\\s\\S]*?</a>'))?.[0];assert(row,asset.id);
    assert(row.includes('src="'+base+model.galleryPosters.wheel+'"'),asset.id+' SSR/hydration wheel');
    assert(row.includes('data-poster="'+base+model.galleryPosters.detail+'"'),asset.id+' SSR/hydration detail');
    assert.equal(model.galleryPosters.detail,resolveGalleryPoster(asset,resources).detail);assert.equal(model.glb,asset.glb);assert.equal(model.blend,asset.blend);
    if(i<352){assert.deepEqual(model.galleryPosters,{detail:original.detail,wheel:original.wheel});assert.deepEqual(model.wheelSpec,original.wheelSpec);}
    else if(index.presentations[asset.id]){assert.equal(model.galleryPosters.wheel,index.presentations[asset.id].wheel);assert.deepEqual(model.wheelSpec,index.presentations[asset.id].wheelSpec);}
    else{assert.equal(model.galleryPosters.wheel,original.wheel);assert.deepEqual(model.wheelSpec,original.wheelSpec);}
  }
  assert.equal(JSON.stringify(resources),before);assert.equal(JSON.stringify(manifest),assetsBefore);
});

test('the real asynchronous catalog loader uses the same selector',async()=>{
  const previousDocument=globalThis.document,previousLocation=globalThis.location;
  globalThis.document={body:{dataset:{}}};globalThis.location=new URL('http://localhost/models/');
  try{
    const assets=[ordinary,first].map(asset=>({...asset,collection:undefined,worlds:[],packs:[]}));
    const values={'assets/manifest.json':{...manifest,assets},'gallery/resources.json':resources,'assets/catalog.json':{version:1,total:2,review_only:false,worlds:[],packs:[]}};
    const loaded=await loadGalleryCatalog({fetchImpl:async url=>({ok:true,json:async()=>copy(values[new URL(url).pathname.slice(1)])})});
    assert.equal(loaded.models[0].galleryPosters.wheel,resources.posters[ordinary.id].wheel);
    assert.equal(loaded.models[1].galleryPosters.wheel,index.presentations[first.id].wheel);
    assert.deepEqual(loaded.models[1].wheelSpec,index.presentations[first.id].wheelSpec);
  }finally{globalThis.document=previousDocument;globalThis.location=previousLocation;}
});

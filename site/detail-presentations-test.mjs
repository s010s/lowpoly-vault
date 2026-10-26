import assert from 'node:assert/strict';import {resolveDetailPresentation as resolve} from './gallery/detail-presentations.js';
const hash='a'.repeat(64),oldHash='b'.repeat(64),pngHash='c'.repeat(64),renderer='d'.repeat(64);
const asset={id:'spyroceras',sha256:{glb:hash},production_release:'production/recovery/release.json'};
const poster={source_glb_sha256:hash,detail:'gallery/posters/spyroceras.png',wheel:'wheel-presentations/spyroceras.png',wheelSpec:{zoom:1},render_route:'blender-cycles-cpu-v1',production_descriptor:asset.production_release};
const resources={files:[{path:poster.detail,sha256:oldHash}]};
const entry={id:asset.id,source_glb_sha256:hash,production_descriptor:asset.production_release,previous_detail:{path:poster.detail,sha256:oldHash},detail:'detail-presentations/spyroceras.png',png:{width:512,height:512,bytes:12000,sha256:pngHash},capture:{detail_sha256:pngHash,source_glb_sha256:hash,first_frame_id:asset.id,renderer_input_sha256:renderer,method:'PreviewRenderer.select(detail)/canonical-square-native-clipping-v1'}};
const index={version:1,kind:'detail-only-presentations',renderer_input_sha256:renderer,presentations:{spyroceras:entry}};
const fixed=resolve(asset,resources,poster,index);assert.equal(fixed.detail,entry.detail);assert.equal(fixed.wheel,poster.wheel);assert.equal(fixed.wheelSpec,poster.wheelSpec);assert.equal(poster.detail,'gallery/posters/spyroceras.png');
let count=1;for(const mutate of [e=>e.source_glb_sha256='e'.repeat(64),e=>e.previous_detail.sha256='e'.repeat(64),e=>e.detail='../wrong.png',e=>e.png.width=768,e=>e.capture.first_frame_id='other',e=>e.capture.detail_sha256=oldHash,e=>e.capture.renderer_input_sha256=oldHash,e=>e.production_descriptor='other',e=>e.capture.method='Blender']){const bad=structuredClone(index);mutate(bad.presentations.spyroceras);assert.equal(resolve(asset,resources,poster,bad),poster);count++;}
assert.equal(resolve(asset,resources,poster,undefined),poster);count++;
const ordinary={...poster,render_route:undefined};assert.equal(resolve(asset,resources,ordinary,index),ordinary);count++;
assert.equal(resolve(asset,resources,{...poster,render_route:'blender-detail-preview-wheel-v1'},index).detail,entry.detail);count++;
console.log(`PASS ${count} detail-only binding/guard cases; wheel and source remain untouched. Browser/pixel validation NOT RUN.`);
const {DETAIL_HIRES_METHOD,detailPresentationPolicy}=await import('./gallery/detail-presentation-policy.js');
for(const size of [1536,2048]){const high=structuredClone(index),e=high.presentations.spyroceras;e.png.width=e.png.height=size;e.capture.method=DETAIL_HIRES_METHOD;e.capture.presentation=detailPresentationPolicy(size);const selected=resolve(asset,resources,poster,high);assert.equal(selected.detail,e.detail);assert.deepEqual(selected.detailPresentation,e.capture.presentation);assert.equal(selected.wheel,poster.wheel);assert.equal(selected.wheelSpec,poster.wheelSpec);
 for(const mutate of [e=>e.capture.presentation.minimum_margin=0,e=>e.capture.presentation.screen_shift=0,e=>e.capture.presentation.revision=1,e=>e.capture.presentation.raster_size=512,e=>e.capture.presentation.extra=true,e=>e.png.width=512,e=>e.capture.presentation=null]){const bad=structuredClone(high);mutate(bad.presentations.spyroceras);assert.equal(resolve(asset,resources,poster,bad),poster);}
 assert.equal(resolve(asset,resources,ordinary,high),ordinary);
}
assert(!Object.hasOwn(fixed,'detailPresentation'));
console.log('PASS explicit revision-2 policy/size binding, invalid profile rejection, old/ordinary profile absent');
const {prepareModels}=await import('./gallery/catalog-source.js');
for(const route of [undefined,'blender-cycles-cpu-v1']){
 const raw={...asset,id:'unbound-detail-profile',name:{en:'Unbound'},glb:'assets/unbound.glb',blend:'assets/unbound.blend',preview:'assets/unbound.png',detailPresentation:detailPresentationPolicy(1536)};
 const [prepared]=prepareModels({assets:[raw]},{posters:{[raw.id]:{...poster,render_route:route}}});
 assert(!Object.hasOwn(prepared,'detailPresentation'),'Raw manifest cannot opt into a capture-owned runtime profile');
 assert.deepEqual(raw.detailPresentation,detailPresentationPolicy(1536),'Source asset stays immutable');
}
console.log('PASS ordinary and rejected override cannot inject a raw detail presentation marker');

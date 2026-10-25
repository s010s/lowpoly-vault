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

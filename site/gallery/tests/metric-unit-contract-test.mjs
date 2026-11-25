// Synthetic boxes have explicitly authored meter coordinates. Never relabel catalog assets.
import assert from 'node:assert/strict';
import * as T from 'three';
import {metricReferenceSpec} from '../../viewer.js';
import {PreviewRenderer} from '../renderer.js';
import {hasMetricDimensions,modelHeight,dimensionDetails,dimensionNote,comparisonMeasurement} from '../model-dimensions.js';
import {publishedModels} from './geometry-fixtures.mjs';
const metric={id:'test-meter-box',units:'meters',axes:{glb_up:'+Y'},blender_unit_scale:1,dimensions:[.2,.3,.4]};
const box=new T.Mesh(new T.BoxGeometry(...metric.dimensions),new T.MeshBasicMaterial());
const size=new T.Box3().setFromObject(box).getSize(new T.Vector3());
assert.equal(metricReferenceSpec(size,metric).available,true);
assert.equal(hasMetricDimensions(metric),true);
assert.equal(modelHeight(metric),'30 cm');
assert.match(dimensionDetails(metric),/Height \(Y\): 30 cm/);
assert.match(dimensionDetails(metric,'zh'),/高度 \(Y\)：30 cm/);
for(const units of [undefined,'unknown','centimeters','']){
 const asset={...metric,units};
 assert.equal(metricReferenceSpec(size,asset).available,false);
 assert.equal(hasMetricDimensions(asset),false);assert.equal(modelHeight(asset),'—');
 assert.match(dimensionDetails(asset),/unconfirmed/);assert.match(dimensionDetails(asset,'zh'),/未确认/);
 assert.match(dimensionNote('en',asset),/unavailable/);assert.match(dimensionNote('zh',asset),/暂不提供/);
 const renderer=Object.create(PreviewRenderer.prototype);
 renderer.detail={model:box,metric:metricReferenceSpec(size,asset)};
 renderer.stopHover=()=>{throw Error('Unknown units must not begin comparison');};
 assert.equal(renderer.compare(true),null);assert.equal(renderer.comparison,undefined);
 assert.equal(comparisonMeasurement({...asset,id:'wave-ripple-surface'}),'');
}
for(const asset of [{...metric,dimensions:[NaN,.3,.4]},{...metric,dimensions:[-.2,.3,.4]},{...metric,axes:{glb_up:'+Z'}},{...metric,blender_unit_scale:.01}]){
 assert.equal(hasMetricDimensions(asset),false);assert.equal(metricReferenceSpec(size,asset).available,false);assert.equal(modelHeight(asset),'—');
}
const wave={...metric,id:'wave-ripple-surface',dimensions:[1.5,.081,1.16]};
assert.equal(comparisonMeasurement(wave),'Footprint (W × D) 1.50 × 1.16 m · Thickness 8.1 cm');
const all=await publishedModels();let unknown=0;
for(const asset of all){const before=JSON.stringify(asset);if(!hasMetricDimensions(asset)){unknown++;assert.equal(modelHeight(asset),'—');assert.match(dimensionDetails(asset),/unconfirmed/);assert.equal(comparisonMeasurement(asset),'');}assert.equal(JSON.stringify(asset),before);}
assert(unknown>=0);

const zero={...metric,dimensions:[0,0,0]};
assert.equal(hasMetricDimensions(zero),false);
assert.equal(metricReferenceSpec(new T.Vector3(0,0,0),zero).available,false);
assert.equal(modelHeight(zero),'—');
const flat={...metric,dimensions:[.2,0,.4]};
assert.equal(hasMetricDimensions(flat),true);
assert.equal(metricReferenceSpec(new T.Vector3(...flat.dimensions),flat).available,true);
console.log(JSON.stringify({status:'passed',catalogRows:all.length,unconfirmedRows:unknown,scope:'Metric gate and formatting; synthetic explicitly meter-authored box; no browser/visual approval'}));

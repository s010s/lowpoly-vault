import * as THREE from 'three';
import {PreviewRenderer} from './renderer.js';
import {validDetailPresentation} from './detail-presentation-policy.js';
export {POSTER_IMAGE_SCALE} from './renderer.js';

/** Only explicitly bound revision-2 right deliveries opt in. Never wheel/hover views. */
export class DetailRenderer extends PreviewRenderer{
 attach(view,asset,entry){
  super.attach(view,asset,entry);
  if(view===this.detail&&validDetailPresentation(asset.detailPresentation)){
   if(this.fitDetailMargin(view,asset.detailPresentation))view.fitDistance=view.camera.position.distanceTo(view.target);
  }
  return view;
 }
 fitDetailMargin(view,policy){
  const camera=view.camera,probe=camera.clone(),point=new THREE.Vector3(),limit=1-2*policy.minimum_margin;let changed=false;
  view.model.updateMatrixWorld(true);probe.aspect=1;probe.fov=38; // Exact unchanged canonical preset, not a previous portrait viewport's widened FOV.
  probe.setViewOffset(1,1,policy.screen_shift,0,1,1);probe.updateProjectionMatrix();
  for(let attempt=0;attempt<16;attempt++){
   probe.position.copy(camera.position);probe.quaternion.copy(camera.quaternion);probe.updateMatrixWorld(true);let extent=0;
   view.model.traverse(object=>{if(!object.isMesh)return;const positions=object.geometry.attributes.position;
    for(let i=0;i<positions.count;i++){point.fromBufferAttribute(positions,i).applyMatrix4(object.matrixWorld).project(probe);extent=Math.max(extent,Math.abs(point.x),Math.abs(point.y));}
   });
   if(extent<=limit)return changed;
   changed=true;
   const offset=camera.position.clone().sub(view.target);camera.position.copy(view.target).add(offset.multiplyScalar(extent/limit+0.002));camera.lookAt(view.target);
  }
  throw new Error('Right detail could not satisfy its reviewed safe margin');
 }
}

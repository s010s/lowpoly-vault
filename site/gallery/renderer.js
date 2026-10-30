import * as THREE from 'three';
import {assetURL} from './urls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {previewTurnAngle} from './hover-turntable.js';
import {HoverPresentation} from './hover-presentation.js';
import {metricReferenceSpec} from '../viewer.js';
import {ViewTransition,RESET_DURATION} from './view-transition.js';
import {loadScaleReference,REFERENCE_SPECS} from './scale-reference.js';
import {entryAt,exitAt,DURATION} from './reference-entry.js';
import {measuredSupport,needsSupportDigest} from './model-support.js';

export const POSTER_IMAGE_SCALE=1;
const WHEEL_ASPECT=16/9;
const WHEEL_POSES={'waptia':{azimuth:72,elevation:28},'fern-cluster':{azimuth:42,elevation:38},'conifer-tree':{azimuth:42,elevation:18}};
const preset={azimuth:42,elevation:23.3,fov:38};
const direction=(a,e)=>new THREE.Vector3(Math.sin(a*Math.PI/180)*Math.cos(e*Math.PI/180),Math.sin(e*Math.PI/180),Math.cos(a*Math.PI/180)*Math.cos(e*Math.PI/180));
const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
export class PreviewRenderer {
 constructor(detail,onChange){
  this.host=detail;this.onChange=onChange;this.cache=new Map();this.pending=new Map();this.token=0;this.hoverToken=0;this.raf=0;this.wire=false;this.comparison=false;
  this.stats={rendererCount:1,requests:0,aborted:0,stale:0,cacheEntries:0,estimatedCacheBytes:0,cacheByteLimit:48*1024*1024,frames:0,hoverId:null,detailId:null};
  this.renderer=new THREE.WebGLRenderer({alpha:true,antialias:true,preserveDrawingBuffer:true,powerPreference:'low-power'});
  this.renderer.domElement.className='preview-renderer';this.renderer.domElement.setAttribute('aria-hidden','true');document.body.append(this.renderer.domElement);
  this.renderer.setPixelRatio(Math.min(devicePixelRatio,1.75));this.renderer.outputColorSpace=THREE.SRGBColorSpace;this.renderer.toneMapping=THREE.ACESFilmicToneMapping;this.renderer.toneMappingExposure=1.1;
  this.renderer.shadowMap.enabled=true;this.renderer.shadowMap.type=THREE.PCFShadowMap;this.renderer.autoClear=false;
  // The stage owns its own fixed camera and lighting. Model fitting, zoom and
  // comparison never recolor the whole panel or move its horizon underneath a poster.
  this.backdrop=this.makeView(true);this.backdrop.isBackdrop=true;this.backdrop.contact.visible=false;
  this.backdrop.target.set(0,.9,0);this.backdrop.camera.position.copy(this.backdrop.target).add(direction(preset.azimuth,preset.elevation).multiplyScalar(4.7));this.backdrop.camera.lookAt(this.backdrop.target);
  this.detail=this.makeView(false);this.hover=null;this.firstDetailFrame=null;
  this.controls=this.createControls(detail);
  this.viewMotion=new ViewTransition({read:()=>this.viewState(),write:(state,ownership)=>this.applyState(state,ownership),reduced,onActivity:active=>{this.stats.cameraTransition=active;}});
  this.referenceToken=0;this.referenceFrame=0;this.cameraInputGeneration=0;
  detail.addEventListener('wheel',event=>{event.stopImmediatePropagation();if(event.ctrlKey||event.metaKey||!this.detail.model||!this.controls.enabled)return;if(event.cancelable)event.preventDefault();this.stopHover();this.onInteraction?.();const delta=event.deltaY*(event.deltaMode===1?16:event.deltaMode===2?detail.clientHeight:1);this.zoom(Math.exp(Math.max(-150,Math.min(150,delta))*.001));},{passive:false,capture:true});
  this.observer=new ResizeObserver(()=>this.draw());this.observer.observe(detail);this.visible=true;
  this.intersection=new IntersectionObserver(([entry])=>{this.visible=entry.isIntersecting;if(!this.visible)this.stopHover();this.draw();});this.intersection.observe(detail);
  this.visibility=()=>{if(document.hidden)this.stopHover();else this.draw();};document.addEventListener('visibilitychange',this.visibility);
  this.motion=matchMedia('(prefers-reduced-motion: reduce)');this.motion.addEventListener('change',()=>{this.stopHover();if(reduced()){this.viewMotion.finish();this.finishReference();}this.draw();});
  this.renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();this.lost=true;this.suspend();this.onError?.(new Error('WebGL context lost'),{assetId:this.detail.asset?.id,token:this.token});});
  this.renderer.domElement.addEventListener('webglcontextrestored',()=>{this.lost=false;this.draw();this.onRestore?.();});
  window.__previewGPU=this.stats;
 }
 createControls(host){
  const controls=new OrbitControls(this.detail.camera,host);controls.enableDamping=false;controls.enablePan=false;controls.enableZoom=true;controls.touches.TWO=THREE.TOUCH.DOLLY_ROTATE;controls.enableRotate=true;controls.enabled=false;controls.minPolarAngle=.08;controls.maxPolarAngle=Math.PI/2+.12;
  controls.addEventListener('change',()=>{if(!this.syncingControls)this.consumeMainOrbit();this.draw();this.onChange?.();});
  controls.addEventListener('start',()=>{this.cancelCamera();this.stopHover();this.onInteraction?.();});return controls;
 }
 resetControlSession(){
  // A pointer held through selection must not continue its old gesture on the
  // newly loaded model. A new control instance has no retained pointer/delta state.
  if(this.host&&this.controls?.dispose){const touchAction=this.host.style.touchAction;this.controls.dispose();this.controls=this.createControls(this.host);this.host.style.touchAction=touchAction;}
  this.controls.enabled=false;this.syncControlMode();
 }
 syncControlMode(){
  if(!this.controls)return;const polar=(90-preset.elevation)*Math.PI/180;this.controls.minPolarAngle=this.comparison?polar:.08;this.controls.maxPolarAngle=this.comparison?polar:Math.PI/2+.12;
 }
 clearDetailPixels(){
  if(!this.renderer?.domElement)return;
  // Clear the old model, never the persistent stage. Context loss is the only
  // case where retaining an unavailable framebuffer would expose stale pixels.
  this.renderer.domElement.style.visibility=this.lost?'hidden':'visible';
  if(!this.lost){this.renderer.setScissorTest(false);this.renderer.setClearColor(0,0);this.renderer.clear(true,true,true);}
 }
 cancelDetailFrame(){
  const pending=this.firstDetailFrame;if(!pending)return;
  if(pending.frame)cancelAnimationFrame(pending.frame);this.firstDetailFrame=null;pending.resolve(false);
 }
 detailPresentable(){
  if(this.lost||document.hidden||this.visible===false||!this.detail.model)return false;
  const rect=this.host.getBoundingClientRect();return rect.width>0&&rect.height>0&&rect.right>0&&rect.bottom>0&&rect.left<innerWidth&&rect.top<innerHeight;
 }
 acknowledgeDetailFrame(){
  const pending=this.firstDetailFrame;
  if(!pending||pending.frame||pending.token!==this.token||pending.id!==this.detail.asset?.id||!this.detailPresentable())return;
  // A successful matching render is necessary but not sufficient: retain the
  // selected poster across a presentation boundary, including a cached load.
  const afterFrame=phase=>{
   pending.frame=0;if(this.firstDetailFrame!==pending)return;
   if(pending.token!==this.token||pending.id!==this.detail.asset?.id){this.cancelDetailFrame();return;}
   if(!this.detailPresentable())return;
   if(phase===0){pending.frame=requestAnimationFrame(()=>afterFrame(1));return;}
   this.firstDetailFrame=null;this.stats.detailFirstFrameId=pending.id;this.stats.detailFirstFrameToken=pending.token;pending.resolve(true);
  };
  pending.frame=requestAnimationFrame(()=>afterFrame(0));
 }
 makeView(detail){
  const scene=new THREE.Scene();if(detail){scene.background=new THREE.Color('#c5bdb3');scene.fog=new THREE.Fog('#c5bdb3',6,18);}
  const camera=new THREE.PerspectiveCamera(preset.fov,1,.01,100);
  scene.add(new THREE.HemisphereLight(0xfff9e9,0x738175,1.65));
  const key=new THREE.DirectionalLight(0xfff0db,3.6);key.position.set(-3,9,5);key.castShadow=true;key.shadow.mapSize.set(512,512);Object.assign(key.shadow.camera,{left:-3,right:3,top:4,bottom:-3,near:.1,far:20});key.shadow.bias=-.0003;key.shadow.normalBias=.015;key.shadow.radius=4;scene.add(key);
  const fill=new THREE.DirectionalLight(0xf3f6f0,.75);fill.position.set(5,2,-3);scene.add(fill);
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(200,200),detail?new THREE.MeshStandardMaterial({color:'#ece5da',roughness:1}):new THREE.ShadowMaterial({opacity:.17}));floor.rotation.x=-Math.PI/2;floor.receiveShadow=true;floor.position.y=-.006;scene.add(floor);
  const grid=new THREE.GridHelper(40,100,0xc6c5b8,0xd4d0c4);grid.position.y=-.004;grid.material.transparent=true;grid.material.opacity=.11;grid.material.depthWrite=false;grid.visible=detail;scene.add(grid);
  const textureCanvas=document.createElement('canvas');textureCanvas.width=textureCanvas.height=128;const ctx=textureCanvas.getContext('2d'),gradient=ctx.createRadialGradient(64,64,1,64,64,63);gradient.addColorStop(0,'rgba(62,58,44,.28)');gradient.addColorStop(.3,'rgba(62,58,44,.12)');gradient.addColorStop(1,'rgba(62,58,44,0)');ctx.fillStyle=gradient;ctx.fillRect(0,0,128,128);
  const texture=new THREE.CanvasTexture(textureCanvas);const contact=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:texture,transparent:true,depthWrite:false}));contact.rotation.x=-Math.PI/2;contact.position.y=-.002;scene.add(contact);contact.visible=detail;
  const shadowViewport={value:new THREE.Vector4(0,0,1,1)};
  if(!detail)for(const material of [floor.material,contact.material]){
   // A transparent thumbnail has finite bounds. Feather only ground shadows
   // before they reach those bounds; the model and turntable stay untouched.
   material.onBeforeCompile=shader=>{shader.uniforms.shadowViewport=shadowViewport;shader.fragmentShader='uniform vec4 shadowViewport;\n'+shader.fragmentShader;shader.fragmentShader=shader.fragmentShader.replace('#include <fog_fragment>',`#include <fog_fragment>
    vec2 groundUV=(gl_FragCoord.xy-shadowViewport.xy)/shadowViewport.zw;
    vec2 groundEdge=min(groundUV,1.0-groundUV);
    gl_FragColor.a*=smoothstep(0.0,0.08,min(groundEdge.x,groundEdge.y));`);};
  }
  return {scene,camera,key,floor,grid,contact,shadowViewport,target:new THREE.Vector3(),model:null,asset:null,scale:1};
 }
 async resource(asset,signal,priority='auto'){
  if(this.cache.has(asset.id)){const e=this.cache.get(asset.id);this.cache.delete(asset.id);this.cache.set(asset.id,e);return e;}
  this.stats.requests++;
  const response=await fetch(new URL(assetURL(asset.glb)),{signal,priority});if(!response.ok)throw new Error('GLB '+response.status);
  const bytes=await response.arrayBuffer();if(signal?.aborted)throw new DOMException('Cancelled','AbortError');
  // Only reviewed support overrides need a byte-level identity check. A changed
  // source safely falls back to the existing box origin until reviewed again.
  const sha256=needsSupportDigest(asset)&&globalThis.crypto?.subtle?Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),v=>v.toString(16).padStart(2,'0')).join(''):null;
  const gltf=await new GLTFLoader().parseAsync(bytes,new URL('.',new URL(assetURL(asset.glb))).href);
  if(signal?.aborted){this.disposeRoot(gltf.scene);throw new DOMException('Cancelled','AbortError');}
  const box=new THREE.Box3().setFromObject(gltf.scene),size=box.getSize(new THREE.Vector3());
  const buffers=new Set(),textures=new Set();gltf.scene.traverse(o=>{if(o.geometry){for(const a of [...Object.values(o.geometry.attributes),o.geometry.index])if(a?.array?.buffer)buffers.add(a.array.buffer);}for(const m of Array.isArray(o.material)?o.material:[o.material])if(m)for(const v of Object.values(m))if(v?.isTexture)textures.add(v);});const estimatedBytes=[...buffers].reduce((n,b)=>n+b.byteLength,0)+[...textures].reduce((n,t)=>n+Math.ceil((t.image?.width||0)*(t.image?.height||0)*4*4/3),0);
  const entry={root:gltf.scene,box,size,sha256,bytes:bytes.byteLength,estimatedBytes};this.cache.set(asset.id,entry);this.stats.cacheEntries=this.cache.size;this.trim(asset.id);return entry;
 }
 trim(pendingId){let total=[...this.cache.values()].reduce((n,e)=>n+e.estimatedBytes,0);for(const [id,entry] of this.cache){if(this.cache.size<=3&&total<=this.stats.cacheByteLimit)break;if(id===pendingId||id===this.detail.asset?.id||id===this.hover?.asset?.id)continue;this.cache.delete(id);total-=entry.estimatedBytes;this.disposeRoot(entry.root);}this.stats.cacheEntries=this.cache.size;this.stats.estimatedCacheBytes=total;}
 disposeView(view){this.detach(view);for(const o of [view.floor,view.grid,view.contact]){o.geometry.dispose();o.material.map?.dispose();o.material.dispose();}view.key.shadow.map?.dispose();view.key.shadow.mapPass?.dispose();view.scene.clear();}

 disposeRoot(root){const gs=new Set(),ms=new Set();root.traverse(o=>{if(o.geometry)gs.add(o.geometry);for(const m of Array.isArray(o.material)?o.material:[o.material])if(m)ms.add(m);});gs.forEach(g=>g.dispose());ms.forEach(m=>{for(const v of Object.values(m))if(v?.isTexture)v.dispose();m.dispose();});}
 detach(view){if(!view?.model)return;view.model.removeFromParent();view.model.traverse(o=>{for(const m of Array.isArray(o.material)?o.material:[o.material])m?.dispose();});view.model=null;view.orientation=null;view.comparisonYaw=null;view.authoredRoot=null;view.supportOffset=null;view.supportRule=null;}
 attach(view,asset,entry){
  this.detach(view);view.asset=asset;view.scale=2/Math.max(...entry.size.toArray());const group=new THREE.Group();const root=entry.root.clone(true);
  const center=entry.box.getCenter(new THREE.Vector3());root.position.sub(new THREE.Vector3(center.x,entry.box.min.y,center.z));root.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true; o.material=Array.isArray(o.material)?o.material.map(m=>m.clone()):o.material.clone();}});
  const supportRule=measuredSupport(asset,entry),supportOffset=supportRule?new THREE.Vector3(supportRule.point[0]-center.x,0,supportRule.point[2]-center.z):new THREE.Vector3();
  const orientation=new THREE.Group();orientation.position.x=-supportOffset.x;orientation.position.z=-supportOffset.z;orientation.name='main-model-inspection-pivot';orientation.position.y=entry.size.y*.49;root.position.y-=orientation.position.y;orientation.add(root);const comparisonYaw=new THREE.Group();comparisonYaw.name='main-model-ground-yaw';comparisonYaw.position.copy(supportOffset);comparisonYaw.add(orientation);group.add(comparisonYaw);group.name='main-model-layout-only';group.scale.setScalar(view.scale);view.scene.add(group);view.model=group;view.orientation=orientation;view.comparisonYaw=comparisonYaw;view.authoredRoot=root;view.supportOffset=supportOffset;view.supportRule=supportRule;view.entry=entry;view.target.set(0,entry.size.y*view.scale*.49,0);
  view.contact.visible=true;view.contact.position.x=view.contact.position.z=0;view.contact.scale.set(Math.max(.45,entry.size.x*view.scale*1.35),Math.max(.45,entry.size.z*view.scale*1.6),1);
  view.metric=metricReferenceSpec(entry.size,asset);this.fit(view,preset.azimuth,preset.elevation);return view;
 }
 fit(view,azimuth=preset.azimuth,elevation=preset.elevation,{canonical=true}={}){
  view.camera.zoom=1;view.camera.clearViewOffset();const size=view.entry.size.clone().multiplyScalar(view.scale);const radius=size.length()/2;view.fitDistance=radius/Math.sin(preset.fov*Math.PI/360)*1.08;
  view.camera.position.copy(view.target).add(direction(azimuth,elevation).multiplyScalar(view.fitDistance));view.camera.lookAt(view.target);view.camera.near=.01;view.camera.far=100;view.camera.updateProjectionMatrix();
  if(canonical&&this.fitProjectedGeometry(view,view.target,.06,0))view.fitDistance=view.camera.position.distanceTo(view.target);
 }
 wheelFrame(view,asset,{rebuild=false}={}){
  const authored=asset.wheelSpec;if(authored&&!rebuild){this.fit(view,authored.azimuth,authored.elevation,{canonical:false});this.resizeCamera(view,1600,900);view.camera.zoom=authored.zoom;view.camera.setViewOffset(1600,900,authored.offset[0],authored.offset[1],1600,900);view.camera.updateProjectionMatrix();view.wheelSpec=authored;return authored;}
  const pose=WHEEL_POSES[asset.id]||{azimuth:preset.azimuth,elevation:asset.dimensions?.[1]/Math.max(...(asset.dimensions||[1,1,1]))<.25?40:preset.elevation};this.fit(view,pose.azimuth,pose.elevation,{canonical:false});this.resizeCamera(view,1600,900);view.camera.updateMatrixWorld(true);
  const bounds={left:Infinity,right:-Infinity,top:-Infinity,bottom:Infinity},point=new THREE.Vector3();
  // Use actual projected vertices across a turn, rather than a universal square bbox.
  // This preserves thin appendages without breathing or cropping during auto-rotation.
  for(let turn=0;turn<8;turn++){view.model.rotation.y=turn*Math.PI/4;view.model.updateMatrixWorld(true);view.model.traverse(o=>{if(!o.isMesh)return;const positions=o.geometry.attributes.position;for(let i=0;i<positions.count;i++){point.fromBufferAttribute(positions,i).applyMatrix4(o.matrixWorld).project(view.camera);bounds.left=Math.min(bounds.left,point.x);bounds.right=Math.max(bounds.right,point.x);bounds.top=Math.max(bounds.top,point.y);bounds.bottom=Math.min(bounds.bottom,point.y);}});}
  view.model.rotation.y=0;view.model.updateMatrixWorld(true);const zoom=THREE.MathUtils.clamp(Math.min(1.72/(bounds.right-bounds.left),1.62/(bounds.top-bounds.bottom)),.8,2.4);view.camera.zoom=zoom;
  const offset=[(bounds.left+bounds.right)*zoom*400,-(bounds.top+bounds.bottom)*zoom*225];view.camera.setViewOffset(1600,900,...offset,1600,900);view.camera.updateProjectionMatrix();
  const project=(x,z)=>{point.set(x,.003,z).project(view.camera);return [(point.x+1)/2,(1-point.y)/2];};const floorCenter=project(0,0);let radius=Math.max(view.entry.size.x,view.entry.size.z)*view.scale*.58,floorPoints;
  for(let attempt=0;attempt<9;attempt++){floorPoints=Array.from({length:48},(_,i)=>project(Math.cos(i/48*Math.PI*2)*radius,Math.sin(i/48*Math.PI*2)*radius));if(floorPoints.every(([x,y])=>x>.025&&x<.975&&y>.025&&y<.975))break;radius*=.88;}
  return view.wheelSpec={...pose,zoom,offset,projectedBounds:bounds,aspect:WHEEL_ASPECT,floorCenter,floorPoints};
 }

 // The renderer camera keeps its canonical direction. OrbitControls is used
 // only to collect incremental drag rotation; its temporary orbit is converted
 // immediately into the main model's independent inspection pivot.
 cameraPose(azimuth=preset.azimuth,elevation=preset.elevation){
  const camera=new THREE.PerspectiveCamera();camera.position.copy(direction(azimuth,elevation));camera.lookAt(0,0,0);return camera.quaternion.clone();
 }
 orientationForView(azimuth,elevation){return this.cameraPose().multiply(this.cameraPose(azimuth,elevation).invert()).normalize();}
 recenterInspectedGround(previousY){
  if(this.comparison)return;const delta=this.detail.model.position.y-previousY;this.detail.camera.position.y+=delta;this.controls.target.y+=delta;this.detail.camera.lookAt(this.controls.target);
 }
 groundMainModel(){
  const v=this.detail;if(!v.model)return;
  // Ground-axis yaw cannot change a vertex height. Once inspection tilt has
  // recovered, use the authored base rather than fitting bounds every drag.
  if(this.comparison&&v.orientation&&new THREE.Vector3(0,1,0).applyQuaternion(v.orientation.quaternion).distanceToSquared(new THREE.Vector3(0,1,0))<1e-16){v.model.position.y=0;return;}
  v.model.updateMatrixWorld(true);
  const bounds=new THREE.Box3().setFromObject(v.model,true);if(!bounds.isEmpty())v.model.position.y-=bounds.min.y;
 }
 updateControls(){
  const distance=this.detail.camera.position.distanceTo(this.controls.target),baseline=this.detail.fitDistance||distance;
  // Native pinch is bounded like wheel zoom in ordinary inspection; comparison
  // converts its temporary dolly ratio into separately bounded projection zoom.
  this.controls.minDistance=this.comparison?distance*.001:Math.min(baseline*.15,distance);this.controls.maxDistance=this.comparison?distance*1000:Math.max(baseline*8,distance);
  this.syncingControls=true;try{this.controls.update();}finally{this.syncingControls=false;}this.detail.presentedCameraDistance=this.detail.camera.position.distanceTo(this.controls.target);
 }
 consumeMainOrbit(){
  const v=this.detail;if(!v.orientation)return;
  const camera=v.camera,distance=camera.position.distanceTo(this.controls.target),previousY=v.model.position.y;
  if(this.comparison){
   const expected=v.presentedCameraDistance||distance,orbit=camera.position.clone().sub(this.controls.target);
   const angle=THREE.MathUtils.euclideanModulo(preset.azimuth*Math.PI/180-Math.atan2(orbit.x,orbit.z)+Math.PI,Math.PI*2)-Math.PI;
   if(Math.abs(angle)>1e-9){this.cancelCamera();v.comparisonYaw.rotation.y+=angle;}
   if(Math.abs(distance/expected-1)>1e-9)this.comparisonZoom(distance/expected);
   camera.position.copy(this.controls.target).add(direction(preset.azimuth,preset.elevation).multiplyScalar(expected));camera.lookAt(this.controls.target);
   this.updateControls();return;
  }
  const rotation=this.cameraPose().multiply(camera.quaternion.clone().invert()).normalize();
  if(rotation.angleTo(new THREE.Quaternion())>1e-9){this.cancelCamera();v.orientation.quaternion.premultiply(rotation).normalize();}
  this.groundMainModel();this.recenterInspectedGround(previousY);camera.position.copy(this.controls.target).add(direction(preset.azimuth,preset.elevation).multiplyScalar(distance));camera.lookAt(this.controls.target);
  this.updateControls();
 }
 viewState(){
  const c=this.detail.camera,p=c.position.clone().sub(this.controls.target),orientation=this.detail.orientation?.quaternion||new THREE.Quaternion();
  const effective=new THREE.Vector3(0,0,1).applyQuaternion(orientation.clone().invert().multiply(c.quaternion));
  return {contactPosition:[this.detail.contact.position.x,this.detail.contact.position.z],azimuth:THREE.MathUtils.radToDeg(Math.atan2(effective.x,effective.z)),elevation:THREE.MathUtils.radToDeg(Math.asin(THREE.MathUtils.clamp(effective.y,-1,1))),cameraAzimuth:THREE.MathUtils.radToDeg(Math.atan2(p.x,p.z)),cameraElevation:THREE.MathUtils.radToDeg(Math.asin(p.y/p.length())),position:c.position.toArray(),target:this.controls.target.toArray(),zoom:c.zoom,screenShift:this.detail.screenShift||0,screenShiftY:this.detail.screenShiftY||0,modelYaw:this.detail.comparisonYaw?.rotation.y||0,distance:p.length(),modelPosition:this.detail.model?.position.toArray(),modelQuaternion:this.detail.orientation?.quaternion.toArray()};
 }
 fitProjectedGeometry(view,target,shift=0,shiftY=0){
  // The complete catalog includes very thin surfaces beyond the reviewed sample.
  // Only enlarge a frame when real vertices overflow the limiting square view.
  // The original canonical/wheel poses and all already-fitting frames are intact.
  const camera=view.camera,probe=camera.clone(),point=new THREE.Vector3();let changed=false;
  if(!view.model)return false;view.model.updateMatrixWorld(true);
  probe.aspect=1;probe.fov=preset.fov;probe.setViewOffset(1,1,shift,shiftY,1,1);probe.updateProjectionMatrix();
  for(let attempt=0;attempt<12;attempt++){
   probe.position.copy(camera.position);probe.quaternion.copy(camera.quaternion);probe.updateMatrixWorld(true);let extent=0;
   view.model.traverse(object=>{if(!object.isMesh)return;const position=object.geometry.attributes.position;for(let i=0;i<position.count;i++){point.fromBufferAttribute(position,i).applyMatrix4(object.matrixWorld).project(probe);extent=Math.max(extent,Math.abs(point.x),Math.abs(point.y));}});
   if(extent<=1)return changed;
   changed=true;const offset=camera.position.clone().sub(target);camera.position.copy(target).add(offset.multiplyScalar(extent+0.002));camera.lookAt(target);
  }
  return changed;
 }
 keepResetFramed(){
  const v=this.detail,c=v.camera;
  // Deliberate inspection zoom is never clamped by a reset-only overflow guard.
  if(!v.model||this.comparison||c.zoom>1.000001||!v.orientation||v.orientation.quaternion.angleTo(new THREE.Quaternion())<1e-7)return;
  this.fitProjectedGeometry(v,this.controls.target,v.screenShift||0,v.screenShiftY||0);
 }
 applyState(state,{cameraOwned=true}={}){
  const c=this.detail.camera;c.position.fromArray(state.position);c.zoom=state.zoom;this.detail.screenShift=state.screenShift||0;this.detail.screenShiftY=state.screenShiftY||0;this.controls.target.fromArray(state.target);
  if(this.detail.model&&state.modelPosition)this.detail.model.position.fromArray(state.modelPosition);
  if(this.detail.orientation&&state.modelQuaternion)this.detail.orientation.quaternion.fromArray(state.modelQuaternion);
  if(this.detail.comparisonYaw&&state.modelYaw!==undefined)this.detail.comparisonYaw.rotation.y=state.modelYaw;
  this.groundMainModel();
  // A rotating flat shape can need a much higher ground offset at mid-tween
  // than either endpoint. Follow that offset by translation only, and only
  // while this transition still owns camera framing.
  if(cameraOwned&&!this.comparison&&state.modelPosition){const correction=this.detail.model.position.y-state.modelPosition[1];c.position.y+=correction;this.controls.target.y+=correction;}
  if(state.contactPosition){[this.detail.contact.position.x,this.detail.contact.position.z]=state.contactPosition;}
  else if(state.modelPosition){this.detail.contact.position.x=state.modelPosition[0];this.detail.contact.position.z=state.modelPosition[2];}
  const distance=c.position.distanceTo(this.controls.target);c.near=Math.max(.001,distance/1000);c.far=Math.max(100,distance*12);
  if(this.detail.scene.fog){this.detail.scene.fog.near=Math.max(6,distance*1.5);this.detail.scene.fog.far=Math.max(18,distance*5);}
  c.lookAt(this.controls.target);this.resizeCamera(this.detail,this.detail.viewportWidth||c.aspect,this.detail.viewportHeight||1);if(cameraOwned)this.keepResetFramed();this.updateControls();this.draw();
 }
 async select(asset,{presentationReady=Promise.resolve(true)}={}){
  this.cancelDetailFrame();this.cancelCamera(true);const token=++this.token;this.controller?.abort();this.stopHover();this.comparison=false;this.removeReference();this.resetControlSession();
  const controller=new AbortController();this.controller=controller;this.detach(this.detail);this.detail.contact.visible=false;this.detail.asset=asset;this.stats.detailId=asset.id;this.stats.detailFirstFrameId=null;this.stats.detailFirstFrameToken=null;this.stats.detailStatus='loading';this.clearDetailPixels();this.draw();
  try{
   if(this.lost)throw new Error('WebGL context is unavailable');
   const entry=await this.resource(asset,controller.signal,'high');if(token!==this.token||controller.signal.aborted){this.stats.stale++;return false;}
   // Poster decode can outlive a lost context or an obsolete selection. Abort
   // releases this gate even if the image never settles, so callers can retire
   // their loading UI and no suspended select promise is left hanging.
   await new Promise(resolve=>{
    const done=()=>{controller.signal.removeEventListener('abort',done);resolve();};
    controller.signal.addEventListener('abort',done,{once:true});Promise.resolve(presentationReady).then(done,done);if(controller.signal.aborted)done();
   });
   if(token!==this.token||controller.signal.aborted){this.stats.stale++;return false;}
   if(this.lost)throw new Error('WebGL context is unavailable');
   // Every selection is a new inspection session, including cached assets,
   // retries and a hover-to-detail click. Never inherit pose, zoom or framing.
   const painted=new Promise(resolve=>{this.firstDetailFrame={token,id:asset.id,resolve,frame:0};});
   this.attach(this.detail,asset,entry);this.applyState(this.singleState());this.updateControls();this.wireframe(this.wire);this.stats.detailStatus='rendering';this.draw();this.trim();
   const ready=await painted;if(!ready||token!==this.token||controller.signal.aborted||this.lost)return false;
   this.controls.enabled=true;this.stats.detailStatus='ready';return true;
  }catch(e){
   if(e.name==='AbortError'||token!==this.token){this.stats.aborted++;return false;}
   this.cancelDetailFrame();this.detach(this.detail);this.detail.contact.visible=false;this.clearDetailPixels();this.draw();this.stats.detailStatus='error';this.onError?.(e,{assetId:asset.id,token});throw e;
  }
 }
 suspend(){this.cancelDetailFrame();this.cancelCamera(true);this.comparison=false;this.removeReference();++this.token;this.controller?.abort();this.stopHover();this.resetControlSession();this.detach(this.detail);this.detail.contact.visible=false;this.stats.detailStatus='suspended';this.clearDetailPixels();this.draw();}

 async preview(asset,host){
  this.stopHover();if(reduced()||!this.detail.model||document.hidden)return false;const token=++this.hoverToken;this.hoverController=new AbortController();const hover=this.makeView(false);hover.host=host;this.hover=hover;this.stats.hoverId=asset.id;
  try{const entry=await this.resource(asset,this.hoverController.signal);if(token!==this.hoverToken)return false;await host.querySelector('img').decode().catch(()=>{});if(token!==this.hoverToken)return false;this.attach(hover,asset,entry);this.wheelFrame(hover,asset);hover.presentation=new HoverPresentation(host);hover.surface=hover.presentation.canvas;this.draw();this.stats.hoverFirstFrameId=asset.id;return true;}catch(e){if(e.name!=='AbortError')console.warn('Hover fallback',e.message);if(token===this.hoverToken)this.stopHover();return false;}
 }
 revealHover(){return this.hover?.presentation?.reveal()||Promise.resolve(false);}
 animateHover(){if(!this.hover?.model||reduced())return;const start=performance.now();const tick=now=>{const h=this.hover;if(!h?.model||document.hidden||reduced()){this.raf=0;return;}const angle=previewTurnAngle((now-start)/1000);h.model.rotation.y=angle;h.effect?.rotate(angle);this.stats.hoverAngle=angle;this.draw(true);this.raf=requestAnimationFrame(tick);};this.raf=requestAnimationFrame(tick);}

 hoverView(){if(!this.hover?.model)return null;const p=this.hover.camera.position.clone().sub(this.hover.target);return {azimuth:THREE.MathUtils.radToDeg(Math.atan2(p.x,p.z))-(this.hover.model.rotation.y*180/Math.PI),elevation:THREE.MathUtils.radToDeg(Math.asin(p.y/p.length()))};}
 stopHover(){++this.hoverToken;this.hoverController?.abort();this.hoverController=null;if(this.raf)cancelAnimationFrame(this.raf);this.raf=0;const existed=!!this.hover;if(this.hover){this.hover.effect?.stop();const presentation=this.hover.presentation;if(presentation){if(reduced())presentation.dispose();else void presentation.exit();}this.disposeView(this.hover);this.hover=null;}this.stats.hoverId=null;this.stats.hoverFirstFrameId=null;this.onHoverStop?.();if(existed)this.draw();}

 wireframe(value){this.wire=value;this.detail.model?.traverse(o=>{if(o.isMesh)for(const m of Array.isArray(o.material)?o.material:[o.material])m.wireframe=value;});this.draw();}
 comparisonZoom(factor){
  this.viewMotion?.interruptZoom();const camera=this.detail.camera;camera.zoom=THREE.MathUtils.clamp(camera.zoom/factor,.125,1/.15);camera.updateProjectionMatrix();
 }
 zoom(factor){
  if(!this.detail.model)return;
  if(this.comparison){this.cameraInputGeneration=(this.cameraInputGeneration||0)+1;this.comparisonZoom(factor);this.updateControls();this.draw();return;}
  this.cancelCamera();const camera=this.detail.camera,offset=camera.position.clone().sub(this.controls.target),baseline=this.detail.fitDistance;
  const current=offset.length(),minimum=Math.min((baseline||5)*.15,current),maximum=Math.max((baseline||5)*8,current),distance=Math.max(minimum,Math.min(maximum,current*factor));camera.position.copy(this.controls.target).add(offset.setLength(distance));this.updateControls();this.draw();
 }
 rotate(azimuth,elevation){
  if(!this.detail.orientation)return;this.cancelCamera();
  if(this.comparison){this.detail.comparisonYaw.rotation.y-=azimuth*Math.PI/180;this.updateControls();this.draw();return;}
  const previousY=this.detail.model.position.y;
  // Keyboard rotation follows the same main-only path as pointer rotation.
  const rotation=this.orientationForView(preset.azimuth+azimuth,Math.max(3,Math.min(87,preset.elevation+elevation)));
  this.detail.orientation.quaternion.premultiply(rotation).normalize();this.groundMainModel();this.recenterInspectedGround(previousY);this.updateControls();this.draw();
 }
 get cameraFrame(){return this.viewMotion?.frame||0;}
 singleState(){
  const v=this.detail,target=v.target.clone(),distance=v.fitDistance;
  // Match the canonical transparent poster by translating its projection, not
  // the physical camera: every vertex shifts exactly 6% of the shorter side,
  // regardless of depth. Compare smoothly brings this offset back to center.
  return {contactPosition:[0,0],position:target.clone().add(direction(preset.azimuth,preset.elevation).multiplyScalar(distance)).toArray(),target:target.toArray(),zoom:1,screenShift:.06,screenShiftY:0,modelYaw:0,distance,modelPosition:[0,0,0],modelQuaternion:[0,0,0,1]};
 }
 reset(){
  if(!this.detail.model)return;this.stopHover();this.comparison=false;this.syncControlMode();
  ++this.referenceToken;this.referenceController?.abort();this.referenceController=null;
  this.stats.referenceState=this.companion?'hiding':'idle';if(this.companion)this.animateReference(false);this.animateState(this.singleState());
 }
 removeReference(){
  ++this.referenceToken;this.referenceController?.abort();this.referenceController=null;
  if(this.referenceFrame)cancelAnimationFrame(this.referenceFrame);this.referenceFrame=0;this.referenceAnimation=null;
  this.companion?.dispose();this.companion=null;this.reference=null;this.comparisonState=null;this.stats.referenceState='idle';
 }
 comparisonLayout(companion){
  const v=this.detail,s=v.scale,right=new THREE.Vector3(Math.cos(preset.azimuth*Math.PI/180),0,-Math.sin(preset.azimuth*Math.PI/180));
  const support=(v.supportOffset||new THREE.Vector3()).clone().multiplyScalar(s);
  const a=new THREE.Box3(new THREE.Vector3(-v.entry.size.x*s/2,0,-v.entry.size.z*s/2),new THREE.Vector3(v.entry.size.x*s/2,v.entry.size.y*s,v.entry.size.z*s/2)).translate(support.clone().negate());
  const r=companion.bounds.clone();r.min.multiplyScalar(s);r.max.multiplyScalar(s);
  const span=box=>{let lo=Infinity,hi=-Infinity;for(const x of [box.min.x,box.max.x])for(const z of [box.min.z,box.max.z]){const p=x*right.x+z*right.z;lo=Math.min(lo,p);hi=Math.max(hi,p);}return {width:hi-lo,center:(lo+hi)/2};};
  const aw=span(a),rw=span(r),gap=Math.max(companion.height*s*.09,.04);
  const mainAnchor=right.clone().multiplyScalar(-(rw.width+gap)/2-aw.center),modelPosition=mainAnchor.clone().sub(support);
  const referencePosition=right.clone().multiplyScalar((aw.width+gap)/2-rw.center);
  companion.setDisplayScale(s);companion.root.position.copy(referencePosition);
  a.translate(mainAnchor);r.translate(referencePosition);const union=a.clone().union(r);
  // The camera aims at the common ground midpoint, not changing shape bounds.
  // A fixed projection offset frames the height above it while every zoom keeps
  // wrist/feet and main base on the same screen-space ground line.
  const target=mainAnchor.clone().add(referencePosition).multiplyScalar(.5);target.y=0;
  const radius=union.getSize(new THREE.Vector3()).length()/2;let distance=radius/Math.sin(preset.fov*Math.PI/360)*1.15,screenShiftY=0;
  const fitCamera=new THREE.PerspectiveCamera(preset.fov,1,.001,100000),point=new THREE.Vector3();
  for(let attempt=0;attempt<24;attempt++){
   fitCamera.position.copy(target).add(direction(preset.azimuth,preset.elevation).multiplyScalar(distance));fitCamera.lookAt(target);fitCamera.updateMatrixWorld(true);
   let left=Infinity,right=-Infinity,bottom=Infinity,top=-Infinity;
   for(const x of [union.min.x,union.max.x])for(const y of [union.min.y,union.max.y])for(const z of [union.min.z,union.max.z]){point.set(x,y,z).project(fitCamera);left=Math.min(left,point.x);right=Math.max(right,point.x);bottom=Math.min(bottom,point.y);top=Math.max(top,point.y);}
   screenShiftY=-(top+bottom)/4;
   if(Math.max(Math.abs(left),Math.abs(right))<.88&&top-bottom<1.76)break;
   distance*=1.1;
  }
  // Only a shared scene scalar is used. Framing changes camera distance, never
  // the ratio between the authored asset and the calibrated reference.
  v.camera.near=Math.max(.001,distance/1000);v.camera.far=Math.max(100,distance*12);
  if(v.scene.fog){v.scene.fog.near=Math.max(6,distance*1.5);v.scene.fog.far=Math.max(18,distance*5);}
  this.stats.comparisonScale=s;this.stats.referenceMeters=companion.height;
  return {contactPosition:[mainAnchor.x,mainAnchor.z],position:target.clone().add(direction(preset.azimuth,preset.elevation).multiplyScalar(distance)).toArray(),target:target.toArray(),zoom:1,screenShift:0,screenShiftY,modelYaw:0,distance,modelPosition:modelPosition.toArray(),modelQuaternion:[0,0,0,1]};
 }
 compare(enabled=!this.comparison){
  if(!this.detail.model)return null;
  if(!enabled){this.reset();return false;}
  if(!this.detail.metric?.available)return null;
  this.stopHover();const kind=Math.max(...this.detail.entry.size.toArray())<.6?'hand':'human';
  const result={kind,meters:REFERENCE_SPECS[kind].meters};
  if(this.comparison){this.comparisonCameraIntent=this.cameraInputGeneration||0;if(this.comparisonState)this.animateState(this.comparisonState);return result;}
  this.comparison=true;this.syncControlMode();this.comparisonCameraIntent=this.cameraInputGeneration||0;const token=++this.referenceToken,assetId=this.detail.asset.id;
  const begin=companion=>{
   if(token!==this.referenceToken||!this.comparison||assetId!==this.detail.asset?.id){if(companion!==this.companion)companion.dispose();return;}
   this.companion=companion;this.reference=companion.root;this.detail.scene.add(this.reference);
   this.comparisonState=this.comparisonLayout(companion);const keepManualInput=(this.cameraInputGeneration||0)!==this.comparisonCameraIntent,manual=this.viewState();
   const destination=keepManualInput?{...this.comparisonState,zoom:manual.zoom,modelYaw:manual.modelYaw}:this.comparisonState;
   // Input during a cold load keeps its yaw/zoom, while the required ground
   // framing and old inspection tilt recovery still complete smoothly.
   this.animateState(destination,{camera:true,orientation:true,yaw:!keepManualInput,zoom:!keepManualInput});this.animateReference(true);
   this.stats.referenceState='ready';this.onChange?.();
  };
  if(this.companion){begin(this.companion);return result;}
  this.referenceController?.abort();this.referenceController=new AbortController();this.stats.referenceState='loading';
  this.referenceReady=loadScaleReference(kind,this.referenceController.signal).then(begin).catch(error=>{
   if(error.name==='AbortError'||token!==this.referenceToken)return;
   this.comparison=false;this.syncControlMode();this.stats.referenceState='error';this.onReferenceError?.(error);this.onChange?.();
  });
  return result;
 }
 animateReference(enter){
  if(!this.companion)return;if(this.referenceFrame)cancelAnimationFrame(this.referenceFrame);
  const c=this.companion,from={...c.state},fresh=enter&&from.opacity===0&&from.glow===0,motionReduced=reduced();
  const a={enter,from,fresh,reduced:motionReduced,start:performance.now(),duration:motionReduced?180:enter?(fresh?DURATION*1000:700):1100};this.referenceAnimation=a;
  const tick=time=>{
   // A canceled callback may already have left the RAF queue. It owns only the
   // animation and companion it captured, never a subsequent entry or asset.
   if(this.referenceAnimation!==a||this.companion!==c)return;this.referenceFrame=0;
   const elapsed=Math.max(0,time-a.start),t=Math.min(1,elapsed/a.duration),e=t*t*(3-2*t);let state;
   if(a.reduced){
    const endpoint=a.enter?c.settled():c.absent();state={...endpoint,opacity:a.from.opacity+(endpoint.opacity-a.from.opacity)*e,visible:t<1||a.enter,glow:0,y:0};
   }else if(a.fresh)state=entryAt(elapsed/1000,c.height,false,c.kind);
   else if(!a.enter)state=exitAt(elapsed/1000,c.height,a.from);
   else{
    const end=c.settled();state={...end};for(const key of ['y','glow','opacity','gathered','open','articulation'])state[key]=a.from[key]+(end[key]-a.from[key])*e;
    if(c.kind==='hand'){
     // Resume from the visible frame. Finish the shallow descent before the
     // fingers relax, just as on a fresh arrival; opacity remains continuous.
     const land=Math.min(1,t/.60),relax=Math.max(0,(t-.60)/.40),landEase=land*land*(3-2*land),relaxEase=relax*relax*(3-2*relax);
     state.move=a.from.move+(end.move-a.from.move)*e;state.y=a.from.y+(end.y-a.from.y)*landEase;
     state.open=a.from.open+(end.open-a.from.open)*relaxEase;state.articulation=state.open;
    }
    state.visible=state.opacity>0;
   }
   c.apply(state);this.draw();
   if(this.referenceAnimation!==a||this.companion!==c)return;
   if(t<1)this.referenceFrame=requestAnimationFrame(tick);else{this.referenceAnimation=null;this.referenceFrame=0;this.stats.referenceState=this.comparison?'ready':'hidden';}
  };
  this.referenceFrame=requestAnimationFrame(tick);
 }
 finishReference(){
  if(this.referenceFrame)cancelAnimationFrame(this.referenceFrame);this.referenceFrame=0;this.referenceAnimation=null;
  if(this.companion)this.companion.apply(this.comparison?this.companion.settled():this.companion.absent());
 }
 cancelCamera(all=false){
  if(all){this.viewMotion?.cancelAll();return;}
  this.cameraInputGeneration=(this.cameraInputGeneration||0)+1;
  if(this.comparison)this.viewMotion?.interruptComparisonInput();
  else{
   this.viewMotion?.interruptInspection();
   // On manual takeover during the return, fold residual base yaw into the
   // inspection pivot without moving the model. Both pivots share the Y axis,
   // so subsequent ordinary pitch remains a world-space input, not a tilted axis.
   const v=this.detail;if(v?.comparisonYaw&&v.orientation&&Math.abs(v.comparisonYaw.rotation.y)>1e-12){
    // The reviewed feet pivot need not coincide with the inspection center.
    // Fold its residual translation as well as yaw to preserve every vertex.
    const offset=v.orientation.position.clone();offset.y=0;
    v.model.position.add(offset.clone().applyQuaternion(v.comparisonYaw.quaternion).sub(offset).multiplyScalar(v.scale));
    v.orientation.quaternion.premultiply(v.comparisonYaw.quaternion).normalize();v.comparisonYaw.rotation.y=0;
    const active=this.viewMotion?.active;
    if(active&&offset.lengthSq()>0){const now=performance.now();active.duration=Math.max(0,active.duration-(now-active.start));active.start=now;active.from=this.viewState();}
   }
  }
 }
 animateState(destination,ownership={}){this.viewMotion.start(destination,{duration:RESET_DURATION,...ownership});}
 resizeCamera(view,width,height){
  const aspect=width/height;view.viewportWidth=width;view.viewportHeight=height;view.camera.aspect=aspect;view.camera.fov=THREE.MathUtils.radToDeg(2*Math.atan(Math.tan(preset.fov*Math.PI/360)/Math.min(1,aspect)));
  // Leave authored wheel thumbnail offsets alone. Only detail view states own
  // this normalized screen translation, which also survives a viewport resize.
  if(typeof view.screenShift==='number'){
   if(view.screenShift||view.screenShiftY)view.camera.setViewOffset(width,height,view.screenShift*Math.min(width,height),(view.screenShiftY||0)*Math.min(width,height),width,height);
   else view.camera.clearViewOffset();
  }
  view.camera.updateProjectionMatrix();
 }
 renderScenePasses(view){
  const camera=view.camera,scene=view.scene,mask=camera.layers.mask,background=scene.background,autoClear=this.renderer.autoClear;
  try{
   // Lights in Three.js are selected per camera, not per mesh. Separate passes
   // are required; enabling both layers in one pass would mix both lighting rigs.
   this.renderer.autoClear=false;camera.layers.set(0);this.renderer.render(scene,camera);
   if(view===this.detail&&this.companion){
    camera.layers.set(1);scene.background=null;
    // Keep first-pass depth so floor/main correctly occlude the reference.
    this.renderer.render(scene,camera);
   }
  }finally{camera.layers.mask=mask;scene.background=background;this.renderer.autoClear=autoClear;}
 }
 renderView(view,rect,clip=rect,{overlay=false}={}){
  if(!view||(!view.model&&!view.isBackdrop)||rect.width<1||rect.height<1)return false;
  const clipped={left:Math.max(0,clip.left),right:Math.min(innerWidth,clip.right),top:Math.max(0,clip.top),bottom:Math.min(innerHeight,clip.bottom)};
  clipped.width=clipped.right-clipped.left;clipped.height=clipped.bottom-clipped.top;if(clipped.width<1||clipped.height<1)return false;
  this.resizeCamera(view,rect.width,rect.height);const h=innerHeight;
  const ratio=this.renderer.getPixelRatio();view.shadowViewport.value.set(Math.floor(rect.left*ratio),Math.floor((h-rect.bottom)*ratio),Math.floor(rect.width*ratio),Math.floor(rect.height*ratio));
  this.renderer.setViewport(rect.left,h-rect.bottom,rect.width,rect.height);this.renderer.setScissor(clipped.left,h-clipped.bottom,clipped.width,clipped.height);this.renderer.setScissorTest(true);
  if(overlay)this.renderer.clearDepth();else this.renderer.clear(true,true,true);this.renderScenePasses(view);return true;
 }
 draw(hoverOnly=false){if(!this.renderer||this.lost||document.hidden)return;const width=innerWidth,height=innerHeight,ratio=Math.min(devicePixelRatio||1,1.75);const size=this.renderer.getSize(new THREE.Vector2());if(this.renderer.getPixelRatio()!==ratio){this.renderer.setPixelRatio(ratio);hoverOnly=false;}if(size.x!==width||size.y!==height){this.renderer.setSize(width,height,false);hoverOnly=false;}
  // setSize(..., false) deliberately leaves CSS alone. Intrinsic canvas dimensions
  // are physical pixels at DPR>1, so they must never become its display size.
  Object.assign(this.renderer.domElement.style,{width:'100vw',height:'100dvh'});
  this.renderer.domElement.style.visibility='visible';
  this.stats.logicalWidth=width;this.stats.logicalHeight=height;this.stats.pixelRatio=ratio;this.stats.bufferWidth=this.renderer.domElement.width;this.stats.bufferHeight=this.renderer.domElement.height;
  if(!hoverOnly){this.renderer.setScissorTest(false);this.renderer.setClearColor(0,0);this.renderer.clear(true,true,true);if(this.visible){const rect=this.host.getBoundingClientRect();this.renderView(this.backdrop,rect);if(this.renderView(this.detail,rect,rect,{overlay:true}))this.acknowledgeDetailFrame();}}
  if(this.hover?.host.isConnected&&this.hover.model){const hostRect=this.hover.host.getBoundingClientRect(),rw=Math.min(hostRect.width,hostRect.height*WHEEL_ASPECT),rh=rw/WHEEL_ASPECT,r={left:hostRect.left+(hostRect.width-rw)/2,top:hostRect.top+(hostRect.height-rh)/2,width:rw,height:rh};r.right=r.left+r.width;r.bottom=r.top+r.height;const list=document.querySelector('#wheel').getBoundingClientRect();const clip={left:Math.max(r.left,list.left),right:Math.min(r.right,list.right),top:Math.max(r.top,list.top),bottom:Math.min(r.bottom,list.bottom)};clip.width=clip.right-clip.left;clip.height=clip.bottom-clip.top;if(clip.width>0&&clip.height>0){this.renderer.setClearColor(0,0);this.renderView(this.hover,r,clip);const ratio=this.renderer.getPixelRatio(),w=Math.max(1,Math.floor(r.width*ratio)),h=Math.max(1,Math.floor(r.height*ratio)),sx=Math.floor(r.left*ratio),sy=this.renderer.domElement.height-Math.floor((innerHeight-r.bottom)*ratio)-h;this.hover.presentation.update(this.renderer.domElement,sx,sy,w,h,w,h);this.renderer.setClearColor(0,0);this.renderer.setScissor(clip.left,innerHeight-clip.bottom,clip.width,clip.height);this.renderer.clear(true,true,true);}}
  this.renderer.setScissorTest(false);this.stats.frames++;this.stats.detailId=this.detail.asset?.id||null;
 }
 captureDetail(){this.draw();const rect=this.host.getBoundingClientRect(),ratio=this.renderer.getPixelRatio();const canvas=document.createElement('canvas');canvas.width=Math.round(rect.width*ratio);canvas.height=Math.round(rect.height*ratio);canvas.getContext('2d').drawImage(this.renderer.domElement,rect.left*ratio,rect.top*ratio,rect.width*ratio,rect.height*ratio,0,0,canvas.width,canvas.height);return canvas;}
 async poster(asset,{wheel=false}={}){const controller=new AbortController();const entry=await this.resource(asset,controller.signal);const view=this.makeView(false);this.attach(view,asset,entry);if(wheel)this.wheelFrame(view,asset,{rebuild:true});
  const oldSize=this.renderer.getSize(new THREE.Vector2()),oldRatio=this.renderer.getPixelRatio();this.renderer.setPixelRatio(1);const w=wheel?768:512,h=wheel?432:512;this.renderer.setSize(w,h,false);this.renderer.setScissorTest(false);this.renderer.setViewport(0,0,w,h);this.renderer.setClearColor(0,0);this.resizeCamera(view,w,h);view.shadowViewport.value.set(0,0,w,h);this.renderer.clear(true,true,true);this.renderer.render(view.scene,view.camera);const data=this.renderer.domElement.toDataURL('image/png');this.lastPosterSpec=wheel?view.wheelSpec:null;this.disposeView(view);this.renderer.setPixelRatio(oldRatio);this.renderer.setSize(oldSize.x,oldSize.y,false);this.draw();return data;
 }
}

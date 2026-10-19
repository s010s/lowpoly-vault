import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {metricReferenceSpec} from '../../../site/viewer.js';

const preset={azimuth:42,elevation:23.3,fov:38};
const direction=(a,e)=>new THREE.Vector3(Math.sin(a*Math.PI/180)*Math.cos(e*Math.PI/180),Math.sin(e*Math.PI/180),Math.cos(a*Math.PI/180)*Math.cos(e*Math.PI/180));
const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
export class PreviewRenderer {
 constructor(detail,onChange){
  this.host=detail;this.onChange=onChange;this.cache=new Map();this.pending=new Map();this.token=0;this.hoverToken=0;this.raf=0;this.wire=false;this.comparison=false;
  this.stats={rendererCount:1,requests:0,aborted:0,stale:0,cacheEntries:0,frames:0,hoverId:null,detailId:null};
  this.renderer=new THREE.WebGLRenderer({alpha:true,antialias:true,preserveDrawingBuffer:true,powerPreference:'low-power'});
  this.renderer.domElement.className='preview-renderer';this.renderer.domElement.setAttribute('aria-hidden','true');document.body.append(this.renderer.domElement);
  this.renderer.setPixelRatio(Math.min(devicePixelRatio,1.75));this.renderer.outputColorSpace=THREE.SRGBColorSpace;this.renderer.toneMapping=THREE.ACESFilmicToneMapping;this.renderer.toneMappingExposure=1.1;
  this.renderer.shadowMap.enabled=true;this.renderer.shadowMap.type=THREE.PCFShadowMap;this.renderer.autoClear=false;
  this.detail=this.makeView(true);this.hover=null;
  this.controls=new OrbitControls(this.detail.camera,detail);this.controls.enableDamping=false;this.controls.enablePan=false;this.controls.enableZoom=false;this.controls.enableRotate=true;this.controls.enabled=false;this.controls.minPolarAngle=.08;this.controls.maxPolarAngle=Math.PI/2+.12;
  this.controls.addEventListener('change',()=>{this.draw();this.onChange?.();});
  this.controls.addEventListener('start',()=>{this.cancelCamera();this.stopHover();this.onInteraction?.();});
  detail.addEventListener('wheel',event=>{if(event.ctrlKey||event.metaKey||!this.detail.model||!this.controls.enabled)return;if(event.cancelable)event.preventDefault();this.stopHover();this.onInteraction?.();const delta=event.deltaY*(event.deltaMode===1?16:event.deltaMode===2?detail.clientHeight:1);this.zoom(Math.exp(Math.max(-150,Math.min(150,delta))*.001));},{passive:false});
  this.observer=new ResizeObserver(()=>this.draw());this.observer.observe(detail);this.visible=true;
  this.intersection=new IntersectionObserver(([entry])=>{this.visible=entry.isIntersecting;if(!this.visible)this.stopHover();this.draw();});this.intersection.observe(detail);
  this.visibility=()=>{if(document.hidden)this.stopHover();else this.draw();};document.addEventListener('visibilitychange',this.visibility);
  this.motion=matchMedia('(prefers-reduced-motion: reduce)');this.motion.addEventListener('change',()=>{this.stopHover();this.draw();});
  this.renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();this.lost=true;this.stopHover();this.onError?.(new Error('WebGL context lost'));});
  this.renderer.domElement.addEventListener('webglcontextrestored',()=>{this.lost=false;this.draw();this.onRestore?.();});
  window.__previewGPU=this.stats;
 }
 makeView(detail){
  const scene=new THREE.Scene();if(detail){scene.background=new THREE.Color('#d2ccc2');scene.fog=new THREE.Fog('#d2ccc2',6,18);}
  const camera=new THREE.PerspectiveCamera(preset.fov,1,.01,100);
  scene.add(new THREE.HemisphereLight(0xfff9e9,0x7e8a7d,2.8));
  const key=new THREE.DirectionalLight(0xfff1de,2.4);key.position.set(-3,9,5);key.castShadow=true;key.shadow.mapSize.set(512,512);Object.assign(key.shadow.camera,{left:-3,right:3,top:4,bottom:-3,near:.1,far:20});key.shadow.bias=-.0003;key.shadow.normalBias=.015;key.shadow.radius=4;scene.add(key);
  const fill=new THREE.DirectionalLight(0xf4f5ee,1.1);fill.position.set(5,2,-3);scene.add(fill);
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(200,200),detail?new THREE.MeshStandardMaterial({color:'#e9e3d8',roughness:1}):new THREE.ShadowMaterial({opacity:.17}));floor.rotation.x=-Math.PI/2;floor.receiveShadow=true;floor.position.y=-.006;scene.add(floor);
  const grid=new THREE.GridHelper(40,100,0xc6c5b8,0xd4d0c4);grid.position.y=-.004;grid.material.transparent=true;grid.material.opacity=.11;grid.material.depthWrite=false;grid.visible=detail;scene.add(grid);
  const textureCanvas=document.createElement('canvas');textureCanvas.width=textureCanvas.height=128;const ctx=textureCanvas.getContext('2d'),gradient=ctx.createRadialGradient(64,64,1,64,64,63);gradient.addColorStop(0,'rgba(62,58,44,.28)');gradient.addColorStop(.3,'rgba(62,58,44,.12)');gradient.addColorStop(1,'rgba(62,58,44,0)');ctx.fillStyle=gradient;ctx.fillRect(0,0,128,128);
  const texture=new THREE.CanvasTexture(textureCanvas);const contact=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:texture,transparent:true,depthWrite:false}));contact.rotation.x=-Math.PI/2;contact.position.y=-.002;scene.add(contact);
  return {scene,camera,key,floor,grid,contact,target:new THREE.Vector3(),model:null,asset:null,scale:1};
 }
 async resource(asset,signal){
  if(this.cache.has(asset.id)){const e=this.cache.get(asset.id);this.cache.delete(asset.id);this.cache.set(asset.id,e);return e;}
  this.stats.requests++;
  const response=await fetch(new URL(asset.glb,document.baseURI),{signal});if(!response.ok)throw new Error('GLB '+response.status);
  const bytes=await response.arrayBuffer();if(signal?.aborted)throw new DOMException('Cancelled','AbortError');
  const gltf=await new GLTFLoader().parseAsync(bytes,new URL('.',new URL(asset.glb,document.baseURI)).href);
  if(signal?.aborted){this.disposeRoot(gltf.scene);throw new DOMException('Cancelled','AbortError');}
  const box=new THREE.Box3().setFromObject(gltf.scene),size=box.getSize(new THREE.Vector3());
  const entry={root:gltf.scene,box,size,bytes:bytes.byteLength};this.cache.set(asset.id,entry);this.stats.cacheEntries=this.cache.size;this.trim();return entry;
 }
 trim(){for(const [id,entry] of this.cache){if(this.cache.size<=3)break;if(id===this.detail.asset?.id||id===this.hover?.asset?.id)continue;this.cache.delete(id);this.disposeRoot(entry.root);}this.stats.cacheEntries=this.cache.size;}
 disposeRoot(root){const gs=new Set(),ms=new Set();root.traverse(o=>{if(o.geometry)gs.add(o.geometry);for(const m of Array.isArray(o.material)?o.material:[o.material])if(m)ms.add(m);});gs.forEach(g=>g.dispose());ms.forEach(m=>{for(const v of Object.values(m))if(v?.isTexture)v.dispose();m.dispose();});}
 detach(view){if(!view?.model)return;view.model.removeFromParent();view.model.traverse(o=>{for(const m of Array.isArray(o.material)?o.material:[o.material])m?.dispose();});view.model=null;}
 attach(view,asset,entry){
  this.detach(view);view.asset=asset;view.scale=2/Math.max(...entry.size.toArray());const group=new THREE.Group();const root=entry.root.clone(true);
  const center=entry.box.getCenter(new THREE.Vector3());root.position.sub(new THREE.Vector3(center.x,entry.box.min.y,center.z));root.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true; o.material=Array.isArray(o.material)?o.material.map(m=>m.clone()):o.material.clone();}});
  group.add(root);group.scale.setScalar(view.scale);view.scene.add(group);view.model=group;view.entry=entry;view.target.set(0,entry.size.y*view.scale*.49,0);
  view.contact.scale.set(Math.max(.45,entry.size.x*view.scale*1.35),Math.max(.45,entry.size.z*view.scale*1.6),1);
  view.metric=metricReferenceSpec(entry.size,asset);this.fit(view,preset.azimuth,preset.elevation);return view;
 }
 fit(view,azimuth=preset.azimuth,elevation=preset.elevation){
  const size=view.entry.size.clone().multiplyScalar(view.scale);const radius=size.length()/2;view.fitDistance=radius/Math.sin(preset.fov*Math.PI/360)*1.15;
  view.camera.position.copy(view.target).add(direction(azimuth,elevation).multiplyScalar(view.fitDistance));view.camera.lookAt(view.target);view.camera.near=.01;view.camera.far=100;view.camera.updateProjectionMatrix();
 }
 viewState(){const c=this.detail.camera,p=c.position.clone().sub(this.controls.target);return {azimuth:THREE.MathUtils.radToDeg(Math.atan2(p.x,p.z)),elevation:THREE.MathUtils.radToDeg(Math.asin(p.y/p.length())),position:c.position.toArray(),target:this.controls.target.toArray(),zoom:c.zoom,distance:p.length()};}
 applyState(state){const c=this.detail.camera;c.position.fromArray(state.position);c.zoom=state.zoom;this.controls.target.fromArray(state.target);c.updateProjectionMatrix();this.controls.update();this.draw();}
 async select(asset,{view,preserve=true}={}){
  if(this.lost)throw new Error('WebGL context is unavailable');this.cancelCamera();
  const token=++this.token;this.controller?.abort();this.stopHover();this.comparison=false;this.removeReference();this.stats.detailId=asset.id;
  const before=view|| (this.detail.model&&preserve?this.viewState():null);
  this.controls.enabled=false;this.controller=new AbortController();this.detach(this.detail);this.detail.asset=asset;this.draw();
  try{const entry=await this.resource(asset,this.controller.signal);if(token!==this.token){this.stats.stale++;return false;}
   this.attach(this.detail,asset,entry);if(before)this.fit(this.detail,before.azimuth,before.elevation);this.controls.target.copy(this.detail.target);this.controls.enabled=true;this.controls.update();this.wireframe(this.wire);this.draw();this.trim();return true;
  }catch(e){if(e.name==='AbortError'){this.stats.aborted++;return false;}if(token===this.token)this.onError?.(e);throw e;}
 }
 suspend(){++this.token;this.controller?.abort();this.stopHover();this.controls.enabled=false;this.detach(this.detail);this.draw();}
 async preview(asset,host){
  this.stopHover();if(reduced()||!this.detail.model||document.hidden)return false;const token=++this.hoverToken;this.hoverController=new AbortController();const hover=this.makeView(false);hover.host=host;this.hover=hover;this.stats.hoverId=asset.id;
  try{const entry=await this.resource(asset,this.hoverController.signal);if(token!==this.hoverToken)return false;this.attach(hover,asset,entry);hover.fitDistance/=1.3;hover.camera.position.copy(hover.target).add(direction(preset.azimuth,preset.elevation).multiplyScalar(hover.fitDistance));hover.camera.lookAt(hover.target);this.draw();return true;}catch(e){if(e.name!=='AbortError')console.warn('Hover fallback',e.message);if(token===this.hoverToken)this.stopHover();return false;}
 }
 animateHover(){if(!this.hover?.model||reduced())return;const start=performance.now();const tick=now=>{if(!this.hover?.model||document.hidden||reduced()){this.raf=0;return;}const angle=Math.min(15,(now-start)*.006);const h=this.hover;h.camera.position.copy(h.target).add(direction(preset.azimuth+angle,preset.elevation).multiplyScalar(h.fitDistance));h.camera.lookAt(h.target);this.draw();if(angle<15)this.raf=requestAnimationFrame(tick);else this.raf=0;};this.raf=requestAnimationFrame(tick);}
 hoverView(){if(!this.hover?.model)return null;const p=this.hover.camera.position.clone().sub(this.hover.target);return {azimuth:THREE.MathUtils.radToDeg(Math.atan2(p.x,p.z)),elevation:THREE.MathUtils.radToDeg(Math.asin(p.y/p.length()))};}
 stopHover(){++this.hoverToken;this.hoverController?.abort();if(this.raf)cancelAnimationFrame(this.raf);this.raf=0;if(this.hover){this.detach(this.hover);for(const o of [this.hover.floor,this.hover.grid,this.hover.contact]){o.geometry.dispose();if(o.material.map)o.material.map.dispose();o.material.dispose();}this.hover=null;}this.stats.hoverId=null;this.onHoverStop?.();this.draw();}
 wireframe(value){this.wire=value;this.detail.model?.traverse(o=>{if(o.isMesh)for(const m of Array.isArray(o.material)?o.material:[o.material])m.wireframe=value;});this.draw();}
 zoom(factor){if(!this.detail.model)return;this.cancelCamera();const camera=this.detail.camera,direction=camera.position.clone().sub(this.controls.target);const distance=Math.max(.8,Math.min(25,direction.length()*factor));camera.position.copy(this.controls.target).add(direction.setLength(distance));this.controls.update();this.draw();}
 rotate(azimuth,elevation){this.cancelCamera();const state=this.viewState();const camera=this.detail.camera;camera.position.copy(this.controls.target).add(direction(state.azimuth+azimuth,Math.max(3,Math.min(87,state.elevation+elevation))).multiplyScalar(state.distance));this.controls.update();this.draw();}
 reset(){this.cancelCamera();this.stopHover();this.removeReference();this.comparison=false;this.fit(this.detail);this.controls.target.copy(this.detail.target);this.controls.update();this.draw();}
 removeReference(){if(this.reference){this.reference.removeFromParent();this.disposeRoot(this.reference);this.reference=null;}}
 compare(){
  if(this.comparison){this.removeReference();this.comparison=false;this.animateState(this.comparisonSnapshot);return false;}
  if(!this.detail.metric?.available)return null;
  this.stopHover();this.comparisonSnapshot=this.viewState();this.comparison=true;const v=this.detail,s=v.scale;const span=Math.max(...v.entry.size.toArray());const hand=span<.6;const group=new THREE.Group();const material=new THREE.MeshStandardMaterial({color:'#c9cebf',roughness:1,transparent:true,opacity:.7,flatShading:true});
  const mesh=(geo,x,y,z)=>{const o=new THREE.Mesh(geo,material.clone());o.position.set(x,y,z);o.castShadow=true;group.add(o);return o;};
  if(hand){ // A deliberately schematic 18 cm hand, in the same authored meter units.
   mesh(new THREE.BoxGeometry(.075,.082,.019),0,.064,0);
   const heights=[.065,.092,.098,.078];for(let i=0;i<4;i++)mesh(new THREE.CylinderGeometry(.008,.010,heights[i],5),-.028+i*.019,.102+heights[i]/2,0);
   const thumb=mesh(new THREE.CylinderGeometry(.010,.012,.058,5),.052,.068,.002);thumb.rotation.z=-.65;
   // Normalize the schematic's total measured extent to exactly 0.18 m.
   const box=new THREE.Box3().setFromObject(group);group.scale.setScalar(.18/box.getSize(new THREE.Vector3()).y);const bounds=new THREE.Box3().setFromObject(group);group.position.y=-bounds.min.y;
  }else{
   mesh(new THREE.IcosahedronGeometry(.105,1),0,1.595,0);mesh(new THREE.CylinderGeometry(.15,.10,.48,5),0,1.23,0);
   for(const x of [-.075,.075]){mesh(new THREE.CylinderGeometry(.055,.045,.7,5),x,.44,0);mesh(new THREE.BoxGeometry(.10,.08,.20),x,.04,.045);}
   for(const x of [-.215,.215]){const arm=mesh(new THREE.CylinderGeometry(.038,.033,.58,5),x,1.17,0);arm.rotation.z=x<0?-.17:.17;}
   const box=new THREE.Box3().setFromObject(group);group.scale.setScalar(1.7/box.getSize(new THREE.Vector3()).y);const bounds=new THREE.Box3().setFromObject(group);group.position.y=-bounds.min.y;
  }
  const ref=new THREE.Group();ref.add(group);ref.scale.setScalar(s);ref.position.x=v.entry.size.x*s/2+(hand?.065:.3)*s;v.scene.add(ref);this.reference=ref;
  const bounds=new THREE.Box3().setFromObject(v.model).union(new THREE.Box3().setFromObject(ref));const size=bounds.getSize(new THREE.Vector3()),target=bounds.getCenter(new THREE.Vector3());const distance=size.length()/2/Math.sin(preset.fov*Math.PI/360)*1.2;
  const before=this.comparisonSnapshot;const position=target.clone().add(direction(before.azimuth,before.elevation).multiplyScalar(distance));this.animateState({position:position.toArray(),target:target.toArray(),zoom:before.zoom});return {kind:hand?'hand':'human',meters:hand?.18:1.7};
 }
 cancelCamera(){if(this.cameraFrame)cancelAnimationFrame(this.cameraFrame);this.cameraFrame=0;}
 animateState(destination){this.cancelCamera();if(reduced()){this.applyState(destination);return;}const origin=this.viewState(),start=performance.now();const tick=time=>{const progress=Math.min(1,(time-start)/250),eased=1-(1-progress)**3;this.applyState({position:origin.position.map((v,i)=>v+(destination.position[i]-v)*eased),target:origin.target.map((v,i)=>v+(destination.target[i]-v)*eased),zoom:origin.zoom+(destination.zoom-origin.zoom)*eased});if(progress<1)this.cameraFrame=requestAnimationFrame(tick);else this.cameraFrame=0;};this.cameraFrame=requestAnimationFrame(tick);}
 resizeCamera(view,width,height){const aspect=width/height;view.camera.aspect=aspect;view.camera.fov=THREE.MathUtils.radToDeg(2*Math.atan(Math.tan(preset.fov*Math.PI/360)/Math.min(1,aspect)));view.camera.updateProjectionMatrix();}
 renderView(view,rect,clip=rect){if(!view?.model||rect.width<1||rect.height<1)return;this.resizeCamera(view,rect.width,rect.height);const h=innerHeight;
  this.renderer.setViewport(rect.left,h-rect.bottom,rect.width,rect.height);this.renderer.setScissor(clip.left,h-clip.bottom,clip.width,clip.height);this.renderer.setScissorTest(true);this.renderer.clear(true,true,true);this.renderer.render(view.scene,view.camera);
 }
 draw(){if(!this.renderer||this.lost||document.hidden)return;const width=innerWidth,height=innerHeight;const size=this.renderer.getSize(new THREE.Vector2());if(size.x!==width||size.y!==height)this.renderer.setSize(width,height,false);
  this.renderer.setScissorTest(false);this.renderer.setClearColor(0,0);this.renderer.clear(true,true,true);
  if(this.visible)this.renderView(this.detail,this.host.getBoundingClientRect());
  if(this.hover?.host.isConnected&&this.hover.model){const r=this.hover.host.getBoundingClientRect(),list=document.querySelector('#wheel').getBoundingClientRect();const clip={left:Math.max(r.left,list.left),right:Math.min(r.right,list.right),top:Math.max(r.top,list.top),bottom:Math.min(r.bottom,list.bottom)};clip.width=clip.right-clip.left;clip.height=clip.bottom-clip.top;if(clip.width>0&&clip.height>0)this.renderView(this.hover,r,clip);}
  this.renderer.setScissorTest(false);this.stats.frames++;this.stats.detailId=this.detail.asset?.id||null;
 }
 captureDetail(){this.draw();const rect=this.host.getBoundingClientRect(),ratio=this.renderer.getPixelRatio();const canvas=document.createElement('canvas');canvas.width=Math.round(rect.width*ratio);canvas.height=Math.round(rect.height*ratio);canvas.getContext('2d').drawImage(this.renderer.domElement,rect.left*ratio,rect.top*ratio,rect.width*ratio,rect.height*ratio,0,0,canvas.width,canvas.height);return canvas;}
 async poster(asset){const controller=new AbortController();const entry=await this.resource(asset,controller.signal);const view=this.makeView(false);this.attach(view,asset,entry);
  const oldSize=this.renderer.getSize(new THREE.Vector2()),oldRatio=this.renderer.getPixelRatio();this.renderer.setPixelRatio(1);this.renderer.setSize(512,512,false);this.renderer.setScissorTest(false);this.renderer.setViewport(0,0,512,512);this.renderer.setClearColor(0,0);this.resizeCamera(view,512,512);this.renderer.clear(true,true,true);this.renderer.render(view.scene,view.camera);const data=this.renderer.domElement.toDataURL('image/png');this.detach(view);for(const o of [view.floor,view.grid,view.contact]){o.geometry.dispose();o.material.map?.dispose();o.material.dispose();}this.renderer.setPixelRatio(oldRatio);this.renderer.setSize(oldSize.x,oldSize.y,false);this.draw();return data;
 }
}

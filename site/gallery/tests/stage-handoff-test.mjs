// Real stage/draw/selection methods with Three.js geometry; mocked GPU calls.
// This verifies lifecycle/passes, not a browser raster or physical paint result.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import * as THREE from 'three';
import {PreviewRenderer} from '../renderer.js';
const callbacks=new Map();let frameId=0;
globalThis.requestAnimationFrame=fn=>{callbacks.set(++frameId,fn);return frameId;};
globalThis.cancelAnimationFrame=id=>callbacks.delete(id);
globalThis.innerWidth=1200;globalThis.innerHeight=800;globalThis.devicePixelRatio=1;
globalThis.document={hidden:false,createElement:()=>({getContext:()=>({createRadialGradient:()=>({addColorStop(){}}),fillRect(){}})})};
globalThis.matchMedia=()=>({matches:false});
const tick=()=>{const batch=[...callbacks.values()];callbacks.clear();for(const fn of batch)fn();};
const flush=()=>new Promise(resolve=>setImmediate(resolve));
let rect={left:400,top:60,right:1200,bottom:800,width:800,height:740};
const p=Object.create(PreviewRenderer.prototype),passes=[],clears=[];
p.stats={frames:0,stale:0,aborted:0};p.token=p.referenceToken=0;p.visible=true;p.host={getBoundingClientRect:()=>rect};
p.renderer={domElement:{style:{},width:1200,height:800},autoClear:false,getPixelRatio:()=>1,getSize:v=>v.set(1200,800),setPixelRatio(){},setSize(){},setScissorTest(){},setClearColor(){},setViewport(){},setScissor(){},clear(...args){clears.push(args);},clearDepth(){clears.push('depth');},render(scene,camera){passes.push({scene,camera,position:camera.position.toArray(),fog:scene.fog?.near,background:scene.background,mask:camera.layers.mask});}};
p.backdrop=p.makeView(true);p.backdrop.isBackdrop=true;p.backdrop.contact.visible=false;p.backdrop.target.set(0,.9,0);p.backdrop.camera.position.set(2.888,2.759,3.207);p.backdrop.camera.lookAt(p.backdrop.target);
p.detail=p.makeView(false);p.controls={enabled:false,target:new THREE.Vector3(),update(){}};
p.stopHover=()=>{};p.cancelCamera=()=>{};p.removeReference=()=>{p.companion=null;};p.resetControlSession=()=>{p.controls.enabled=false;};p.trim=()=>{};
const root=new THREE.Group(),mesh=new THREE.Mesh(new THREE.BoxGeometry(1,2,1),new THREE.MeshStandardMaterial());mesh.position.y=1;root.add(mesh);
const box=new THREE.Box3().setFromObject(root),entry={root,box,size:box.getSize(new THREE.Vector3())};
const requests=[];p.resource=asset=>new Promise((resolve,reject)=>requests.push({asset,resolve,reject}));
const asset=id=>({id,dimensions:[1,2,1],units:'meters'});
const checks=[];
p.draw();assert.equal(p.renderer.domElement.style.visibility,'visible');assert.equal(passes.length,1);assert.equal(passes[0].scene,p.backdrop.scene);assert.equal(p.detail.contact.visible,false);
checks.push('Empty and loading stage renders the fixed backdrop without contact/model pixels');
const stable={position:p.backdrop.camera.position.toArray(),quaternion:p.backdrop.camera.quaternion.toArray(),fog:[p.backdrop.scene.fog.near,p.backdrop.scene.fog.far]};
let showPoster;const poster=new Promise(resolve=>showPoster=resolve);let done=false;
const a=p.select(asset('A'),{presentationReady:poster}).then(value=>(done=true,value));requests.at(-1).resolve(entry);await flush();assert.equal(p.detail.model,null);assert.equal(done,false);showPoster(true);await flush();assert(p.detail.model);assert.equal(p.controls.enabled,false);assert.equal(done,false);assert.equal(p.stats.detailStatus,'rendering');assert.equal(p.detail.scene.background,null);assert.equal(p.detail.scene.fog,null);assert(p.detail.floor.material.isShadowMaterial);
tick();await flush();assert.equal(done,false);tick();assert.equal(await a,true);assert.equal(p.controls.enabled,true);assert.equal(p.stats.detailFirstFrameId,'A');assert(clears.includes('depth'));assert.deepEqual(stable,{position:p.backdrop.camera.position.toArray(),quaternion:p.backdrop.camera.quaternion.toArray(),fog:[p.backdrop.scene.fog.near,p.backdrop.scene.fog.far]});
checks.push('Matching poster presentation gates mesh attach; successful render plus two RAF boundaries gates controls/ready');
// No acknowledgment if hidden, offscreen, zero-size, clipped or context-lost.
for(const kind of ['hidden','offscreen','zero','intersection']){
 const good={...rect};let finished=false;const choice=p.select(asset(kind)).then(v=>(finished=true,v));
 if(kind==='hidden')document.hidden=true;if(kind==='offscreen')rect={...good,left:1300,right:2100};if(kind==='zero')rect={...good,width:0,right:good.left};if(kind==='intersection')p.visible=false;
 requests.at(-1).resolve(entry);await flush();tick();tick();await flush();assert.equal(finished,false,kind+' must await a real render');
 document.hidden=false;rect=good;p.visible=true;p.draw();tick();tick();assert.equal(await choice,true);
}
checks.push('Hidden/offscreen/zero-size/intersection-excluded views cannot acknowledge; visible redraw resumes correctly');
// Presentability can be lost after a valid render and before presentation.
let finished=false;const interrupted=p.select(asset('interrupted')).then(v=>(finished=true,v));requests.at(-1).resolve(entry);await flush();tick();document.hidden=true;tick();await flush();assert.equal(finished,false);document.hidden=false;p.draw();tick();tick();assert.equal(await interrupted,true);
checks.push('Hiding between render and acknowledgment preserves pending selection until a new visible frame');
const stale=p.select(asset('stale'));requests.at(-1).resolve(entry);await flush();tick();const current=p.select(asset('current'));assert.equal(await stale,false);assert.equal(p.detail.model,null);assert.equal(p.detail.contact.visible,false);requests.at(-1).resolve(entry);await flush();tick();tick();assert.equal(await current,true);assert.equal(p.stats.detailFirstFrameId,'current');
checks.push('New selection cancels the previous frame promise and never acknowledges its model');
const pendingPoster=p.select(asset('pending-poster'),{presentationReady:new Promise(()=>{})});requests.at(-1).resolve(entry);await flush();assert.equal(p.detail.model,null);p.lost=true;p.suspend();assert.equal(await pendingPoster,false);p.lost=false;
checks.push('Context loss after GLB completion releases an unresolved poster presentation gate');
const lost=p.select(asset('lost'));requests.at(-1).resolve(entry);await flush();p.lost=true;p.suspend();tick();tick();assert.equal(await lost,false);assert.equal(p.renderer.domElement.style.visibility,'hidden');assert.equal(p.controls.enabled,false);assert.equal(p.detail.model,null);p.lost=false;p.draw();assert.equal(p.renderer.domElement.style.visibility,'visible');
checks.push('Context loss cancels pending acknowledgments and clears model; restoration can repaint the same empty backdrop');
const failed=p.select(asset('failed'));requests.at(-1).reject(new Error('network'));await assert.rejects(failed,/network/);assert.equal(p.renderer.domElement.style.visibility,'visible');assert.equal(p.detail.contact.visible,false);assert.equal(p.stats.detailStatus,'error');assert.deepEqual(stable,{position:p.backdrop.camera.position.toArray(),quaternion:p.backdrop.camera.quaternion.toArray(),fog:[p.backdrop.scene.fog.near,p.backdrop.scene.fog.far]});
checks.push('Load failure retains the same fixed floor/background without floating contact shadows');
await mkdir(new URL('./evidence/',import.meta.url),{recursive:true});await writeFile(new URL('./evidence/stage-handoff-report.json',import.meta.url),JSON.stringify({status:'passed',browserVerified:false,scope:'Real PreviewRenderer lifecycle/render methods, actual Three.js geometry, mocked GPU calls',checks},null,2));
console.log(JSON.stringify({status:'passed',checks},null,2));

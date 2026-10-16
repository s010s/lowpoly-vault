import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
export async function createViewer(host,url,isCurrent){
  if(!url)throw new Error('No model URL');
  const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor(0xe8e3d7,1);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.35;host.replaceChildren(renderer.domElement);
  const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(38,1,.01,1000),controls=new OrbitControls(camera,renderer.domElement);
  controls.enableDamping=false;controls.enablePan=false;controls.autoRotate=false;
  scene.add(new THREE.HemisphereLight(0xfff7e5,0x637363,2.5));const sun=new THREE.DirectionalLight(0xfff1db,3);sun.position.set(5,8,6);scene.add(sun);const fill=new THREE.DirectionalLight(0xffffff,1.2);fill.position.set(-5,3,-4);scene.add(fill);
  let model,disposed=false,handlersAttached=false;const render=()=>{if(!disposed){renderer.render(scene,camera);host.dataset.renderTriangles=String(renderer.info.render.triangles);host.dataset.renderLines=String(renderer.info.render.lines);host.dataset.renderCalls=String(renderer.info.render.calls);}};
  const resize=()=>{const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();render();};
  const observer=new ResizeObserver(resize);observer.observe(host);controls.addEventListener('change',render);
  const buttons=['reset','wireframe','zoom-in','zoom-out'].map(id=>document.getElementById(id));
  function disposeObject(object){object?.traverse(o=>{o.geometry?.dispose();for(const m of Array.isArray(o.material)?o.material:[o.material]){if(m){for(const value of Object.values(m))if(value?.isTexture)value.dispose();m.dispose();}}});}
  const dispose=()=>{disposed=true;observer.disconnect();controls.dispose();disposeObject(model);renderer.dispose();renderer.forceContextLoss();renderer.domElement.remove();host.removeEventListener('keydown',onKey);if(handlersAttached)buttons.forEach(b=>b.onclick=null);};
  let distance=5;
  const zoom=factor=>{camera.position.sub(controls.target).multiplyScalar(factor).add(controls.target);controls.update();render();};
  const reset=()=>{camera.position.set(distance*.85,distance*.53,distance);controls.target.set(0,0,0);controls.update();render();};
  function onKey(event){const key=event.key;if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-','Home'].includes(key))return;event.preventDefault();if(key==='Home'){reset();return;}if(['+','=','-'].includes(key)){zoom(key==='-'?1.12:1/1.12);return;}const spherical=new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target));if(key==='ArrowLeft')spherical.theta-=.12;if(key==='ArrowRight')spherical.theta+=.12;if(key==='ArrowUp')spherical.phi-=.12;if(key==='ArrowDown')spherical.phi+=.12;spherical.makeSafe();camera.position.copy(new THREE.Vector3().setFromSpherical(spherical).add(controls.target));controls.update();render();}
  try{const gltf=await new GLTFLoader().loadAsync(url);model=gltf.scene;if(!isCurrent()){dispose();return()=>{};}scene.add(model);const box=new THREE.Box3().setFromObject(model),size=box.getSize(new THREE.Vector3()),center=box.getCenter(new THREE.Vector3());model.position.sub(center);distance=Math.max(size.x,size.y,size.z)*1.25;camera.near=Math.max(distance/1000,.001);camera.far=distance*100;camera.updateProjectionMatrix();controls.minDistance=distance*.25;controls.maxDistance=distance*8;resize();reset();host.addEventListener('keydown',onKey);handlersAttached=true;buttons[0].onclick=reset;buttons[1].onclick=()=>{const on=buttons[1].getAttribute('aria-pressed')!=='true';buttons[1].setAttribute('aria-pressed',String(on));model.traverse(o=>{for(const m of Array.isArray(o.material)?o.material:[o.material])if(m)m.wireframe=on;});render();};buttons[2].onclick=()=>zoom(1/1.2);buttons[3].onclick=()=>zoom(1.2);return dispose;}catch(e){dispose();throw e;}
}

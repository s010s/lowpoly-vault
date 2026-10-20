import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
const items=[
 {id:'didymoceras',file:'didymoceras.glb',size:[.23,.17,.30],x:-.2},
 {id:'spirematospermum',file:'spirematospermum.glb',size:[.018,.062,.016],x:.90,displayRotationY:Math.PI/2},
 {id:'cave-shield',file:'cave-shield.glb',size:[1,.84,.67],x:-1.10},
 {id:'psammichnites-ribbon-trace',file:'psammichnites-ribbon-trace.glb',size:[.28,.38,.045],x:.40},
];
const loader=new GLTFLoader();
function stats(root){
 const materials=new Set(); let tris=0, meshes=0, textures=0;
 root.traverse(o=>{if(o.isMesh){meshes++; const g=o.geometry; const ix=g.index; tris+=ix?ix.count/3:(g.attributes.position?.count||0)/3; for(const m of (Array.isArray(o.material)?o.material:[o.material]))if(m)materials.add(m);}});
 return {meshNodes:meshes,triangles:tris,materials:materials.size,textures};
}
function light(scene){scene.add(new THREE.HemisphereLight(0xffffff,0x8d7661,2.0));const key=new THREE.DirectionalLight(0xffffff,2.8);key.position.set(-2,4,5);scene.add(key);const fill=new THREE.DirectionalLight(0xffffff,1.0);fill.position.set(3,2,-3);scene.add(fill);}
function device(renderer){const gl=renderer.getContext(),ext=gl.getExtension('WEBGL_debug_renderer_info');return {glVendor:gl.getParameter(gl.VENDOR),glRenderer:gl.getParameter(gl.RENDERER),unmaskedVendor:ext?gl.getParameter(ext.UNMASKED_VENDOR_WEBGL):null,unmaskedRenderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):null,webgl2:renderer.capabilities.isWebGL2,contextAttributes:gl.getContextAttributes()};}
function drawScene(root,canvas,{fit=true,sceneMode=false}={}){
 const scene=new THREE.Scene();scene.background=new THREE.Color('#e8e4dc');light(scene);scene.add(root);root.updateMatrixWorld(true);
 let box=new THREE.Box3().setFromObject(root);let size=box.getSize(new THREE.Vector3()),center=box.getCenter(new THREE.Vector3());
 let floor=null;if(sceneMode){floor=new THREE.Mesh(new THREE.PlaneGeometry(4.2,2.2),new THREE.MeshStandardMaterial({color:'#e8e4dc',roughness:.95}));floor.rotation.x=-Math.PI/2;floor.position.set(-.37,-.004,0);scene.add(floor);}
 const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:false,preserveDrawingBuffer:true});renderer.setPixelRatio(1);renderer.setSize(canvas.width,canvas.height,false);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.NoToneMapping;renderer.toneMappingExposure=1;
 const aspect=canvas.width/canvas.height;let halfH;
 if(sceneMode)halfH=1.05;else halfH=Math.max(size.x,size.y,size.z)*.74;
 const camera=new THREE.OrthographicCamera(-halfH*aspect,halfH*aspect,halfH,-halfH,.001,100);camera.position.set(center.x+halfH*1.55,center.y+halfH*1.05,center.z+halfH*2.1);camera.lookAt(center.x,center.y,center.z);camera.updateProjectionMatrix();renderer.info.reset();renderer.render(scene,camera);
 const s=stats(root),info=renderer.info.render;
 return {box:{min:box.min.toArray(),max:box.max.toArray(),size:size.toArray()},boundsCenter:center.toArray(),meshNodes:s.meshNodes,triangles:s.triangles,materials:s.materials,textures:s.textures,drawCalls:info.calls,renderedTriangles:info.triangles,renderer:device(renderer),outputColorSpace:renderer.outputColorSpace,toneMapping:renderer.toneMapping,toneMappingExposure:renderer.toneMappingExposure,glError:renderer.getContext().getError()};
}
window.__qaReady=false;
window.__qaSummary={assets:[],scene:null,errors:[]};
(async()=>{
 try{
  const cards=document.getElementById('cards');const loaded=[];
  for(const item of items){
   const section=document.createElement('section');section.className='card';section.innerHTML=`<h2>${item.id} — ${item.size.join(' × ')} m nominal</h2><canvas width="476" height="420"></canvas><div class="metrics">Loading exact GLB…</div>`;cards.appendChild(section);
   const gltf=await loader.loadAsync('/models/'+item.file);const root=gltf.scene;root.updateMatrixWorld(true);const c=section.querySelector('canvas');
   const result=drawScene(root,c);const itemStats=stats(root);const data={id:item.id,file:item.file,nominalSizeM:item.size,...result,...itemStats};window.__qaSummary.assets.push(data);section.querySelector('.metrics').textContent=JSON.stringify(data,null,2);loaded.push({item,root});
  }
  const combined=new THREE.Group();for(const {item,root} of loaded){root.rotation.y=item.displayRotationY||0;root.position.x=item.x;root.updateMatrixWorld(true);combined.add(root);}combined.updateMatrixWorld(true);
  const sceneRes=drawScene(combined,document.getElementById('sceneCanvas'),{sceneMode:true});sceneRes.assets=loaded.map(({item,root})=>({id:item.id,instances:1,glb:'/models/'+item.file,nominalSizeM:item.size,position:[item.x,0,0],displayRotationYDegrees:(item.displayRotationY||0)*180/Math.PI,bounds:new THREE.Box3().setFromObject(root).getSize(new THREE.Vector3()).toArray()}));window.__qaSummary.scene={...sceneRes,assetCount:4,instances:4,composition:'One exact instance of each GLB at true authored scale on a neutral common floor; presentation offsets only.'};document.getElementById('sceneMetrics').textContent=JSON.stringify(window.__qaSummary.scene,null,2);
 }catch(e){window.__qaSummary.errors.push(String(e?.stack||e));console.error(e);}
 window.__qaReady=true;
})();

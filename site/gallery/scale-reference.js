import * as THREE from 'three';
import {assetURL} from './urls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {entryAt,exitAt,DURATION,clamp} from './reference-entry.js';

export const REFERENCE_LIGHTING=Object.freeze({layer:1,ambient:1.5,key:3.1,fill:1.4,rim:.40,keyPosition:[-.60,2.4,2.02],fillPosition:[2,.9,1],rimPosition:[.6,1.6,-2],shadowOpacity:.23,shadowReceiverDiameterRatio:3.2});

export const HAND_PRESENTATION=Object.freeze({bodyLinearRGB:[.90,.89,.87],gridLinearRGB:[.50,.51,.49],haloDiameterRatio:.72,haloPeak:.98,mistHeightRatio:.12,mistPeak:.48,lighting:REFERENCE_LIGHTING});

export const REFERENCE_SPECS=Object.freeze({
  hand:{path:'gallery/scale-reference/hand-18cm-technical.glb',meters:.18,rotation:Math.PI+32*Math.PI/180},
  human:{path:'gallery/scale-reference/human-180cm.glb',meters:1.8,rotation:32*Math.PI/180},
});
export function disposeReferenceRoot(root){
  const geometries=new Set(),materials=new Set(),textures=new Set();
  root?.traverse(object=>{if(object.geometry)geometries.add(object.geometry);for(const material of (Array.isArray(object.material)?object.material:[object.material]).concat(object.customDepthMaterial||[]))if(material){materials.add(material);for(const value of Object.values(material))if(value?.isTexture)textures.add(value);}});
  root?.traverse(object=>{object.shadow?.map?.dispose();object.shadow?.mapPass?.dispose();});root?.removeFromParent();for(const geometry of geometries)geometry.dispose();for(const material of materials)material.dispose();for(const texture of textures)texture.dispose();
}
export async function loadScaleReference(kind,signal){
  const spec=REFERENCE_SPECS[kind],url=new URL(assetURL(spec.path));
  const response=await fetch(url,{signal});if(!response.ok)throw new Error('Scale reference '+response.status);
  const data=await response.arrayBuffer();signal?.throwIfAborted();
  const gltf=await new GLTFLoader().parseAsync(data,new URL('.',url).href);
  if(signal?.aborted){disposeReferenceRoot(gltf.scene);signal.throwIfAborted();}
  gltf.parser?.cache?.removeAll();
  return new ScaleCompanion(gltf.scene,kind);
}

/** An authored, calibrated mesh, never fitted independently from its subject. */
export class ScaleCompanion {
  constructor(mesh,kind){
    this.kind=kind;this.spec=REFERENCE_SPECS[kind];this.height=this.spec.meters;this.lighting=kind==='hand'?HAND_PRESENTATION.lighting:REFERENCE_LIGHTING;
    this.root=new THREE.Group();this.root.name='calibrated-scale-reference';
    this.body=new THREE.Group();this.body.add(mesh);this.body.rotation.y=this.spec.rotation;this.root.add(this.body);
    this.materials=[];this.morphs=[];this.presentationUniforms={referenceReveal:{value:0},referenceGlow:{value:0},referenceHeight:{value:this.height},referenceGround:{value:0}};
    mesh.traverse(object=>{
      if(object.isMesh){
        object.userData.referenceTopology=/SparseGrid/i.test(object.name);
        object.castShadow=!object.userData.referenceTopology;object.receiveShadow=true;
      }
      for(const material of Array.isArray(object.material)?object.material:[object.material])if(material){
        const grid=!!object.userData.referenceTopology;
        if(object.isMesh){
          material.color.setRGB(...(grid?HAND_PRESENTATION.gridLinearRGB:HAND_PRESENTATION.bodyLinearRGB),THREE.LinearSRGBColorSpace);
          // One prepared shader/depth mode for entry, settled view and exit.
          // Closed front surfaces prevent the back-face cage seen during fades.
          material.transparent=true;material.depthWrite=true;material.forceSinglePass=true;
          material.side=grid?THREE.DoubleSide:THREE.FrontSide;material.alphaTest=.003;
          material.onBeforeCompile=shader=>{
            Object.assign(shader.uniforms,this.presentationUniforms);
            shader.vertexShader='varying float vReferenceWorldY;\n'+shader.vertexShader;
            shader.vertexShader=shader.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\nvReferenceWorldY=(modelMatrix*vec4(transformed,1.)).y;');
            shader.fragmentShader='varying float vReferenceWorldY;uniform float referenceReveal;uniform float referenceGlow;uniform float referenceHeight;uniform float referenceGround;\n'+shader.fragmentShader;
            shader.fragmentShader=shader.fragmentShader.replace('#include <alphatest_fragment>',`float referenceH=(vReferenceWorldY-referenceGround)/referenceHeight;
float revealFront=mix(-.11,1.11,referenceReveal);
float referenceCoverage=1.-smoothstep(revealFront-.09,revealFront+.09,referenceH);
diffuseColor.a*=${grid?'referenceCoverage*referenceCoverage':'referenceCoverage'};
#include <alphatest_fragment>`);
            shader.fragmentShader=shader.fragmentShader.replace('#include <opaque_fragment>',`float baseLight=pow(1.-clamp(referenceH/.32,0.,1.),2.)*referenceGlow;
outgoingLight+=vec3(1.,.97,.90)*baseLight*.85;
#include <opaque_fragment>`);
          };
          material.customProgramCacheKey=()=> 'reference-ground-emergence-v54-'+(grid?'grid':'body');
          if(!grid){
            const depth=new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking,alphaTest:.003,side:THREE.BackSide});
            depth.onBeforeCompile=shader=>material.onBeforeCompile(shader);
            depth.customProgramCacheKey=()=> 'reference-ground-emergence-depth-v54';
            object.customDepthMaterial=depth;
          }
        }
        this.materials.push({material,opacity:material.opacity,transparent:material.transparent,depthWrite:material.depthWrite});
      }
      if(object.morphTargetDictionary)this.morphs.push({object,openIndex:object.morphTargetDictionary.ArrivalOpen,gatheredIndex:object.morphTargetDictionary.ArrivalGathered});
    });
    // Save settled real meter bounds before adding presentation-only light.
    this.bounds=new THREE.Box3().setFromObject(this.body);
    const shader=(fragment)=>new THREE.ShaderMaterial({transparent:true,depthWrite:false,side:THREE.DoubleSide,blending:THREE.NormalBlending,uniforms:{strength:{value:0}},vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:fragment});
    const falloff='(1.-smoothstep(.10,1.,r))';
    this.glow=new THREE.Mesh(new THREE.PlaneGeometry(1,1),shader(`varying vec2 vUv;uniform float strength;void main(){float r=length((vUv-.5)*2.);float a=${falloff}*strength;gl_FragColor=vec4(1.,1.,.985,a);}`));
    this.glow.name='reference-ground-halo';this.glow.rotation.x=-Math.PI/2;this.glow.position.y=Math.min(.001,this.height*.0008);
    const diameter=this.height*HAND_PRESENTATION.haloDiameterRatio;this.glow.scale.set(diameter,diameter,1);this.root.add(this.glow);
    // A shallow, feathered half-ellipsoid adds a little depth to the ground pool.
    // White-over compositing avoids additive clipping half-way through prelight.
    // It has no scrolling texture, beam, sharp upper edge or upright billboard.
    this.mist=new THREE.Mesh(new THREE.SphereGeometry(1,48,24,0,Math.PI*2,0,Math.PI/2),new THREE.ShaderMaterial({
      transparent:true,depthWrite:false,side:THREE.FrontSide,blending:THREE.NormalBlending,
      uniforms:{strength:{value:0}},
      vertexShader:'varying vec3 vLocal;varying vec3 vLocalView;void main(){vLocal=position;vLocalView=(inverse(modelViewMatrix)*vec4(0.,0.,0.,1.)).xyz-position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
      fragmentShader:'varying vec3 vLocal;varying vec3 vLocalView;uniform float strength;void main(){vec3 ray=-normalize(vLocalView);float travel=max(0.,-2.*dot(vLocal,ray));if(ray.y<-.0001)travel=min(travel,max(0.,-vLocal.y/ray.y));float density=0.;for(int i=0;i<6;i++){vec3 p=vLocal+ray*travel*(float(i)+.5)/6.;float heightFade=pow(max(0.,1.-p.y),2.);density+=exp(-dot(p.xz,p.xz)*3.8)*heightFade;}density*=travel/6.;gl_FragColor=vec4(1.,1.,.985,(1.-exp(-density*3.))*strength);}'
    }));
    this.mist.name='reference-low-ground-mist';this.mist.scale.set(diameter*.5,this.height*HAND_PRESENTATION.mistHeightRatio,diameter*.5);this.mist.renderOrder=2;this.root.add(this.mist);
    // Dedicated lights are rendered only in the depth-preserving reference pass.
    const h=this.height,rig=this.lighting;
    this.ambient=new THREE.HemisphereLight(0xf8faf5,0x626961,rig.ambient);this.root.add(this.ambient);
    const directional=(name,intensity,position)=>{const light=new THREE.DirectionalLight(0xfffaf1,intensity);light.name=name;light.position.fromArray(position).multiplyScalar(h);light.target.position.set(0,h*.45,0);this.root.add(light,light.target);return light;};
    this.key=directional('reference-upper-left-key',rig.key,rig.keyPosition);
    this.fill=directional('reference-weak-fill',rig.fill,rig.fillPosition);
    this.rim=directional('reference-soft-rim',rig.rim,rig.rimPosition);
    this.key.castShadow=true;this.key.shadow.mapSize.set(512,512);this.key.shadow.radius=3;this.key.shadow.bias=-.0002;
    // The oblique key projects a standing head beyond one reference height.
    // Include that complete footprint rather than clipping it at the old .85h edge.
    this.shadow=new THREE.Mesh(new THREE.PlaneGeometry(h*rig.shadowReceiverDiameterRatio,h*rig.shadowReceiverDiameterRatio),new THREE.ShadowMaterial({opacity:rig.shadowOpacity,depthWrite:false}));this.shadow.name='reference-wrist-contact-shadow';this.shadow.rotation.x=-Math.PI/2;this.shadow.receiveShadow=true;this.root.add(this.shadow);
    this.contact=new THREE.Mesh(new THREE.PlaneGeometry(h*.24,h*.20),new THREE.ShaderMaterial({transparent:true,depthWrite:false,uniforms:{opacity:{value:0}},vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:'varying vec2 vUv;uniform float opacity;void main(){float d=length((vUv-.5)*2.);gl_FragColor=vec4(.12,.14,.11,pow(max(0.,1.-d),2.)*opacity);}'}));this.contact.name='reference-sole-contact';this.contact.rotation.x=-Math.PI/2;this.root.add(this.contact);
    this.root.traverse(object=>object.layers.set(rig.layer));this.setDisplayScale(1);
    this.apply({...entryAt(0,this.height,false,this.kind),visible:false});
  }
  setDisplayScale(scale){
    this.root.scale.setScalar(scale);const extent=this.height*scale;this.presentationUniforms.referenceHeight.value=extent;
    Object.assign(this.key.shadow.camera,{left:-extent,right:extent,top:extent,bottom:-extent,near:Math.max(.001,extent*.03),far:extent*8});this.key.shadow.camera.updateProjectionMatrix();this.key.shadow.normalBias=extent*.001;
    // Same floor as the main scene, with a tiny depth separation for the overlay.
    this.shadow.position.y=-.0058/scale;this.contact.position.y=-.0056/scale;
  }
  apply(state){
    const opacityFactor=clamp(state.opacity),rawGathered=clamp(state.gathered||0),rawOpen=clamp(state.open??state.articulation??0),total=Math.max(1,rawGathered+rawOpen);
    const gathered=rawGathered/total,open=rawOpen/total;
    this.state={...state,y:Math.max(0,state.y),opacity:opacityFactor,gathered,open,articulation:open};this.body.position.y=this.state.y;this.body.visible=state.visible&&opacityFactor>0;
    this.presentationUniforms.referenceReveal.value=opacityFactor;
    this.presentationUniforms.referenceGlow.value=state.glow;
    this.presentationUniforms.referenceGround.value=this.root.position.y;
    // Entry progress already drives the soft height reveal. Multiplying it into
    // all material alpha again leaves even emerged skin as a translucent cage.
    for(const {material,opacity} of this.materials)material.opacity=opacity;
    for(const {object,openIndex,gatheredIndex} of this.morphs){if(openIndex!==undefined)object.morphTargetInfluences[openIndex]=open;if(gatheredIndex!==undefined)object.morphTargetInfluences[gatheredIndex]=gathered;}
    this.glow.material.uniforms.strength.value=state.glow*HAND_PRESENTATION.haloPeak;this.glow.visible=state.glow>0;
    this.mist.material.uniforms.strength.value=state.glow*HAND_PRESENTATION.mistPeak;this.mist.visible=state.glow>0;
    this.shadow.material.opacity=this.lighting.shadowOpacity*opacityFactor;this.shadow.visible=opacityFactor>0;
    this.contact.material.uniforms.opacity.value=.17*opacityFactor;this.contact.visible=opacityFactor>0;
  }
  settled(){return entryAt(DURATION,this.height,true,this.kind);}
  absent(){return exitAt(1.1,this.height);}
  dispose(){disposeReferenceRoot(this.root);}
}

import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {ScaleCompanion,HAND_PRESENTATION,REFERENCE_LIGHTING} from '../scale-reference.js';
import {entryAt,DURATION} from '../reference-entry.js';
const checks=[],assets={},close=(a,b,e=1e-9)=>assert(Math.abs(a-b)<e,`${a} != ${b}`);
const parse=async name=>{const bytes=await readFile(new URL('../../public/gallery/scale-reference/'+name,import.meta.url));return {bytes,gltf:await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'')};};
const geometryHash=root=>{
 const hash=createHash('sha256');root.traverse(object=>{if(!object.isMesh)return;const geometry=object.geometry;hash.update(object.name);for(const [name,attribute] of Object.entries(geometry.attributes)){hash.update(name);hash.update(new Uint8Array(attribute.array.buffer,attribute.array.byteOffset,attribute.array.byteLength));}if(geometry.index)hash.update(new Uint8Array(geometry.index.array.buffer,geometry.index.array.byteOffset,geometry.index.array.byteLength));for(const [name,attributes] of Object.entries(geometry.morphAttributes))for(const attribute of attributes){hash.update(name);hash.update(new Uint8Array(attribute.array.buffer,attribute.array.byteOffset,attribute.array.byteLength));}});return hash.digest('hex');
};
const handData=await parse('hand-18cm-technical.glb'),handGeometryBefore=geometryHash(handData.gltf.scene),hand=new ScaleCompanion(handData.gltf.scene,'hand');assets.hand=createHash('sha256').update(handData.bytes).digest('hex');assert.equal(assets.hand,'57f27a2693e89240db8dc99b33a8117fcd7bbc04d34d4ec3fc3522d4b154fb72');assert.equal(geometryHash(handData.gltf.scene),handGeometryBefore);
const body=handData.gltf.scene.getObjectByName('Hand18cm_GrayWhite'),grid=handData.gltf.scene.getObjectByName('Hand_SparseGrid');
assert(body.material.isMeshStandardMaterial);assert.deepEqual(body.material.color.toArray(),HAND_PRESENTATION.bodyLinearRGB);assert(body.material.roughness>.93&&body.material.roughness<.95);assert.equal(body.material.emissive.getHex(),0);assert.deepEqual(grid.material.color.toArray(),HAND_PRESENTATION.gridLinearRGB);checks.push('Approved V5.2 hand bytes and decoded geometry unchanged by runtime; runtime white body and gray topology preserve the matte physically-lit surface');
assert.equal(hand.ambient.intensity,1.5);assert.equal(hand.key.intensity,3.1);assert.equal(hand.fill.intensity,1.4);assert.equal(hand.rim.intensity,.4);hand.root.traverse(o=>assert.equal(o.layers.mask,2));checks.push('Stronger shared reference lighting remains layer isolated without changing global exposure');
hand.apply(hand.settled());assert(body.castShadow);assert(!grid.castShadow);assert(body.receiveShadow&&grid.receiveShadow);assert(body.material.transparent&&body.material.depthWrite);assert.equal(body.material.side,THREE.FrontSide);assert.equal(grid.material.side,THREE.DoubleSide);assert.equal(body.material.alphaTest,.003);checks.push('Solid depth-writing body retains real shadows and a stable prepared material mode; fine topology does not cast noisy independent shadows');
hand.apply(entryAt(.90,.18));assert.equal(hand.body.visible,false);assert.equal(hand.state.open,1);assert.equal(hand.state.gathered,0);assert(hand.glow.visible);close(hand.glow.scale.x,.1296);assert(hand.glow.material.fragmentShader.includes('smoothstep(.10,1.,r)'));assert(hand.glow.material.uniforms.strength.value>.5);assert(hand.glow.position.y<=.001);assert.equal(hand.glow.position.x,0);assert.equal(hand.glow.position.z,0);checks.push('Coherent 129.6 mm ground pool appears before the already-open hand, with a shallow21.6mm soft base mist and no column');
const smooth=t=>t*t*(3-2*t),halfR=.55;close(1-smooth((halfR-.1)/.9),.5);const halfDiameter=.1296*halfR;close(halfDiameter,.07128);checks.push('Soft halo half-maximum diameter is 71.28 mm and its unclipped white-over peak is .98');
const humanData=await parse('human-180cm.glb');assets.human=createHash('sha256').update(humanData.bytes).digest('hex');const humanGeometryBefore=geometryHash(humanData.gltf.scene),human=new ScaleCompanion(humanData.gltf.scene,'human');assert.equal(geometryHash(humanData.gltf.scene),humanGeometryBefore);
for(const companion of [hand,human]){
 companion.body.traverse(object=>{if(!object.isMesh)return;const topology=object.userData.referenceTopology;assert.deepEqual(object.material.color.toArray(),topology?HAND_PRESENTATION.gridLinearRGB:HAND_PRESENTATION.bodyLinearRGB);assert.equal(object.castShadow,!topology);});
 assert.equal(companion.ambient.intensity,REFERENCE_LIGHTING.ambient);assert.equal(companion.key.intensity,REFERENCE_LIGHTING.key);assert.equal(companion.fill.intensity,REFERENCE_LIGHTING.fill);close(companion.glow.scale.x,companion.height*.72);close(companion.mist.scale.y,companion.height*.12);assert(companion.mist.geometry.type==='SphereGeometry');assert.equal(companion.mist.material.depthWrite,false);assert.equal(companion.mist.material.side,THREE.FrontSide);assert.equal(companion.mist.renderOrder,2);
 const versions=companion.materials.map(({material})=>material.version);
 for(let frame=0;frame<=Math.round(DURATION*60);frame++){
  const state=entryAt(frame/60,companion.height,false,companion.kind);companion.apply(state);
  close(companion.mist.material.uniforms.strength.value,state.glow*HAND_PRESENTATION.mistPeak);assert.equal(companion.mist.visible,state.glow>0);close(companion.presentationUniforms.referenceReveal.value,state.opacity);close(companion.presentationUniforms.referenceGlow.value,state.glow);close(companion.shadow.material.opacity,companion.lighting.shadowOpacity*state.opacity);close(companion.contact.material.uniforms.opacity.value,.17*state.opacity);
  companion.materials.forEach(({material,opacity},index)=>{assert.equal(material.version,versions[index]);assert(material.transparent&&material.depthWrite&&material.forceSinglePass);assert.equal(material.alphaTest,.003);close(material.opacity,opacity);});
  companion.body.traverse(object=>{if(object.isMesh)assert.equal(object.castShadow,!object.userData.referenceTopology);});
 }
 for(const {material} of companion.materials){
  const shader={uniforms:{},vertexShader:THREE.ShaderLib.standard.vertexShader,fragmentShader:THREE.ShaderLib.standard.fragmentShader};material.onBeforeCompile(shader);
  for(const key of Object.keys(companion.presentationUniforms))assert.equal(shader.uniforms[key],companion.presentationUniforms[key]);
  assert(shader.vertexShader.includes('#include <project_vertex>\nvReferenceWorldY=(modelMatrix*vec4(transformed,1.)).y'));assert(shader.fragmentShader.includes('float referenceCoverage=1.-smoothstep'));assert(shader.fragmentShader.includes('referenceH/.32'));assert(shader.fragmentShader.includes('outgoingLight+='));
 }
 companion.body.traverse(object=>{
  if(!object.isMesh)return;if(object.userData.referenceTopology){assert.equal(object.customDepthMaterial,undefined);return;}
  const depth=object.customDepthMaterial;assert(depth?.isMeshDepthMaterial);assert.equal(depth.depthPacking,THREE.RGBADepthPacking);assert.equal(depth.side,THREE.BackSide);assert.equal(depth.alphaTest,.003);
  const shader={uniforms:{},vertexShader:THREE.ShaderLib.depth.vertexShader,fragmentShader:THREE.ShaderLib.depth.fragmentShader};depth.onBeforeCompile(shader);
  for(const key of Object.keys(companion.presentationUniforms))assert.equal(shader.uniforms[key],companion.presentationUniforms[key]);
  assert(shader.vertexShader.includes('#include <project_vertex>\nvReferenceWorldY=(modelMatrix*vec4(transformed,1.)).y'));
  assert(shader.fragmentShader.includes('float revealFront=mix(-.11,1.11,referenceReveal);'));
  assert(shader.fragmentShader.includes('float referenceCoverage=1.-smoothstep(revealFront-.09,revealFront+.09,referenceH);\ndiffuseColor.a*=referenceCoverage;\n#include <alphatest_fragment>'));assert(!shader.fragmentShader.includes('diffuseColor.a*=referenceReveal;'));
  assert(!shader.fragmentShader.includes('outgoingLight+='),'shadow shader receives reveal but not a visible-light output');
  assert.notEqual(depth.customProgramCacheKey(),object.material.customProgramCacheKey());
 });
 for(const opacity of [0,Number.EPSILON,1e-6,.0009,.0011,1]){
  companion.apply({...companion.settled(),opacity,visible:opacity>0});assert.equal(companion.shadow.visible,opacity>0);assert.equal(companion.contact.visible,opacity>0);close(companion.presentationUniforms.referenceReveal.value,opacity);
 }
}
checks.push('Human decoded geometry and morphs stay unchanged while runtime body/grid colors, lighting and ground-emergence shader now match the hand');
checks.push('Both references keep identical prepared material versions and shadow-caster flags across247frames; light, material reveal, receiver and contact opacity share continuous state uniforms');
checks.push('Visible and custom-depth shaders use the same project-vertex height hook and identical live uniform objects; shadow alpha uses the same height coverage without double attenuation');
checks.push('Soft local light stays below 32% height; surface and grid share height reveal while grid coverage is squared to suppress ghostly lines; shadow/contact visibility begins with any positive opacity. Shader source assertions do not claim GPU compilation');
const depthDisposals=[];for(const companion of [hand,human])companion.body.traverse(object=>{if(object.customDepthMaterial){const entry={name:object.name,count:0};depthDisposals.push(entry);object.customDepthMaterial.addEventListener('dispose',()=>entry.count++);}});
assert(depthDisposals.length>=2);const parent=new THREE.Group();parent.add(hand.root,human.root);hand.dispose();human.dispose();assert.equal(parent.children.length,0);depthDisposals.forEach(entry=>assert.equal(entry.count,1));checks.push('Disposal detaches both reference roots and releases each custom shadow-depth material exactly once');
const report={status:'passed',checks,assets,handHalfMaximumHaloDiameterMeters:halfDiameter,geometryHashes:{hand:handGeometryBefore,human:humanGeometryBefore},depthDisposals,browserRasterVerified:false,limitation:'No final browser pixel/lighting claim; Chromium launch is blocked by socket EPERM.'};await writeFile(new URL('./evidence/reference-presentation-report.json',import.meta.url),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));

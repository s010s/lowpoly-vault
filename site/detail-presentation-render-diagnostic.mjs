/** Probe-only render decomposition. Only the explicit diagnostic browser profile may execute it; never application rendering. */
import assert from 'node:assert/strict';
import {randomUUID} from 'node:crypto';

// These functions are serialized by Playwright. Keep every browser dependency local.
export async function beginNativeLayerDiagnostic(owner){
 if(typeof owner!=='string'||! /^[0-9a-f-]{36}$/.test(owner))throw Error('Missing diagnostic owner');
 const r=window.__preview?.renderer,rr=r?.renderer,v=r?.detail;
 if(!r||!rr||!v?.model||r.companion||r.comparison||r.hover||r.raf||r.lost||r.visible===false||document.hidden||r.firstDetailFrame||r.viewMotion?.active||r.viewMotion?.frame||r.referenceFrame||r.stats?.cameraTransition||window.__detailLayerDiagnostic)throw Error('Unavailable or overlapping diagnostic');
 const canvas=rr.domElement,gl=rr.getContext(),rect=r.host.getBoundingClientRect();
 if(gl.isContextLost())throw Error('Lost diagnostic context');
 const vector=()=>v.shadowViewport.value.clone(),color=()=>v.key.color.clone();
 const snapshot=()=>({
  selected:v.asset.id,token:r.token,lifecycle:{comparison:!!r.comparison,hover:!!r.hover,lost:!!r.lost,motion_active:!!r.viewMotion?.active},backdrop:{camera:{position:r.backdrop.camera.position.toArray(),quaternion:r.backdrop.camera.quaternion.toArray(),projection:r.backdrop.camera.projectionMatrix.toArray(),matrix_world:r.backdrop.camera.matrixWorld.toArray(),near:r.backdrop.camera.near,far:r.backdrop.camera.far,fov:r.backdrop.camera.fov,zoom:r.backdrop.camera.zoom,aspect:r.backdrop.camera.aspect,layers:r.backdrop.camera.layers.mask,view:r.backdrop.camera.view?structuredClone(r.backdrop.camera.view):null},shadow_viewport:r.backdrop.shadowViewport.value.toArray()},render_settings:{output_color_space:rr.outputColorSpace,tone_mapping:rr.toneMapping,exposure:rr.toneMappingExposure,context_attributes:gl.getContextAttributes()},device_pixel_ratio:devicePixelRatio,renderer_pixel_ratio:rr.getPixelRatio(),canvas:{width:canvas.width,height:canvas.height},
  rect:{left:rect.left,top:rect.top,right:rect.right,bottom:rect.bottom,width:rect.width,height:rect.height},
  camera:{layers:v.camera.layers.mask,position:v.camera.position.toArray(),quaternion:v.camera.quaternion.toArray(),projection:v.camera.projectionMatrix.toArray(),matrix_world:v.camera.matrixWorld.toArray(),near:v.camera.near,far:v.camera.far,fov:v.camera.fov,zoom:v.camera.zoom,aspect:v.camera.aspect,view:v.camera.view?structuredClone(v.camera.view):null},
  model_matrix:v.model.matrixWorld.toArray(),viewport:rr.getViewport(vector()).toArray(),scissor:rr.getScissor(vector()).toArray(),scissor_test:rr.getScissorTest(),clear_color:rr.getClearColor(color()).toArray(),clear_alpha:rr.getClearAlpha(),auto_clear:rr.autoClear,
  shadow_viewport:v.shadowViewport.value.toArray(),shadow_map:{auto_update:rr.shadowMap.autoUpdate,needs_update:rr.shadowMap.needsUpdate,type:rr.shadowMap.type,key_map_size:v.key.shadow.mapSize.toArray()},
  visibility:{model:v.model.visible,floor:v.floor.visible,contact:v.contact.visible,grid:v.grid.visible},scene_background:v.scene.background?.getHex?.()??null
 });
 const before=snapshot(),saved={camera:v.camera.clone(),backdropCamera:r.backdrop.camera.clone(),backdropShadowViewport:r.backdrop.shadowViewport.value.clone(),draw:r.draw,ownDraw:Object.hasOwn(r,'draw'),autoUpdate:rr.shadowMap.autoUpdate,needsUpdate:rr.shadowMap.needsUpdate,viewport:rr.getViewport(vector()),scissor:rr.getScissor(vector()),scissorTest:rr.getScissorTest(),clearColor:rr.getClearColor(color()),clearAlpha:rr.getClearAlpha(),autoClear:rr.autoClear,shadowViewport:v.shadowViewport.value.clone(),visibility:[v.model,v.floor,v.contact,v.grid].map(o=>[o,o.visible])};
 const state={owner,r,rr,v,canvas,gl,rect,saved,snapshot,before,overlay:null,suppressed:0,images:{untouched:canvas.toDataURL('image/png')},states:{before}};window.__detailLayerDiagnostic=state;
 // Prevent a late scheduled draw from replacing the isolated diagnostic layer.
 r.draw=()=>{state.suppressed++;};rr.shadowMap.autoUpdate=false;rr.shadowMap.needsUpdate=false;
 const resetVisibility=()=>{for(const[o,visible]of saved.visibility)o.visible=visible;};
 const clear=()=>{rr.setScissorTest(false);rr.setClearColor(0,0);rr.clear(true,true,true);rr.setViewport(rect.left,innerHeight-rect.bottom,rect.width,rect.height);rr.setScissor(rect.left,innerHeight-rect.bottom,rect.width,rect.height);rr.setScissorTest(true);v.shadowViewport.value.copy(saved.shadowViewport);};
 const record=name=>{state.images[name]=canvas.toDataURL('image/png');state.states[name]=snapshot();const e=gl.getError();if(e!==0)throw Error('Diagnostic WebGL error '+name+': '+e);};
 resetVisibility();clear();r.renderScenePasses(v);record('transparent_detail');
 resetVisibility();v.floor.visible=v.contact.visible=v.grid.visible=false;clear();r.renderScenePasses(v);record('model_only');
 resetVisibility();v.model.visible=false;clear();r.renderScenePasses(v);record('shadow_only');
 resetVisibility();clear();r.renderView(r.backdrop,rect);record('backdrop_only');
 const img=new Image();state.overlay=img;img.dataset.nativeLayerDiagnostic='true';img.src=state.images.transparent_detail;
 Object.assign(img.style,{position:'fixed',left:'0',top:'0',width:'100vw',height:'100dvh',maxWidth:'none',maxHeight:'none',margin:'0',padding:'0',border:'0',transform:'none',objectFit:'fill',opacity:'1',mixBlendMode:'normal',pointerEvents:'none',zIndex:'2'});
 await img.decode();document.body.append(img);await new Promise(requestAnimationFrame);
 state.states.composite={...snapshot(),diagnostic_composite:{source:'same-native-viewport-transparent-detail',image_width:img.naturalWidth,image_height:img.naturalHeight,css_rect:JSON.parse(JSON.stringify(img.getBoundingClientRect())),description:'PNG CSS composition over isolated backdrop, NOT the untouched actual native scene'}};
 return {kind:'native-layer-diagnostic-only',images:state.images,states:state.states};
}

export function restoreNativeLayerDiagnostic(owner){
 const state=window.__detailLayerDiagnostic;if(!state)return null;if(state.owner!==owner)throw Error('Diagnostic owner mismatch');
 const{r,rr,v,canvas,gl,saved,snapshot}=state;let result;
 try{
  state.overlay?.remove();for(const[o,visible]of saved.visibility)o.visible=visible;v.camera.copy(saved.camera);r.backdrop.camera.copy(saved.backdropCamera);r.backdrop.shadowViewport.value.copy(saved.backdropShadowViewport);
  rr.shadowMap.autoUpdate=saved.autoUpdate;rr.shadowMap.needsUpdate=saved.needsUpdate;rr.autoClear=saved.autoClear;
  v.shadowViewport.value.copy(saved.shadowViewport);rr.setClearColor(saved.clearColor,saved.clearAlpha);rr.setViewport(saved.viewport);rr.setScissor(saved.scissor);rr.setScissorTest(saved.scissorTest);
  if(saved.ownDraw)r.draw=saved.draw;else delete r.draw;
  saved.draw.call(r);
  const restored=canvas.toDataURL('image/png'),after=snapshot();
  result={images:state.images,states:state.states,image:restored,state:after,restored_exact:restored===state.images.untouched,state_exact:JSON.stringify(after)===JSON.stringify(state.before),suppressed_draw_calls:state.suppressed,gl_error:gl.getError()};
 }catch(error){result={images:state.images,states:state.states,restored_exact:false,state_exact:false,restoration_error:error.message,suppressed_draw_calls:state.suppressed};try{result.image=canvas.toDataURL('image/png');}catch{}try{result.state=snapshot();}catch{}}finally{state.overlay?.remove();if(saved.ownDraw)r.draw=saved.draw;else delete r.draw;delete window.__detailLayerDiagnostic;}
 return result;
}

export async function captureNativeLayerDiagnostic(page){
 const owner=randomUUID();let result,error,restored;
 try{result=await page.evaluate(beginNativeLayerDiagnostic,owner);result.composite=await page.locator('#detail').screenshot();}
 catch(e){error=e;}
 finally{try{restored=await page.evaluate(restoreNativeLayerDiagnostic,owner);}catch(e){error??=e;}}
 if(restored){
  result??={kind:'native-layer-diagnostic-only',images:restored.images,states:restored.states};
  if(restored.image)result.images.restored=restored.image;if(restored.state)result.states.restored=restored.state;result.restoration_error=restored.restoration_error??null;result.restored_exact=restored.restored_exact;result.suppressed_draw_calls=restored.suppressed_draw_calls;
  try{assert(!restored.restoration_error,'Diagnostic restoration failed: '+restored.restoration_error);assert.equal(restored.gl_error,0,'Diagnostic restore WebGL error');assert(restored.restored_exact,'Diagnostic changed the untouched native raster');assert(restored.state_exact,'Diagnostic changed camera/renderer state');}catch(e){error??=e;}
 }
 if(error){error.diagnostic={...result,error:error.message};throw error;}
 assert(restored,'Missing diagnostic restore');return result;
}

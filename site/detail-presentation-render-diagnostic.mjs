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
  actual_gl:{samples:gl.getParameter(gl.SAMPLES),drawing_buffer:[gl.drawingBufferWidth,gl.drawingBufferHeight],viewport:Array.from(gl.getParameter(gl.VIEWPORT)),scissor:Array.from(gl.getParameter(gl.SCISSOR_BOX)),scissor_enabled:gl.isEnabled(gl.SCISSOR_TEST)},model_matrix:v.model.matrixWorld.toArray(),viewport:rr.getViewport(vector()).toArray(),scissor:rr.getScissor(vector()).toArray(),scissor_test:rr.getScissorTest(),clear_color:rr.getClearColor(color()).toArray(),clear_alpha:rr.getClearAlpha(),auto_clear:rr.autoClear,
  shadow_viewport:v.shadowViewport.value.toArray(),shadow_map:{auto_update:rr.shadowMap.autoUpdate,needs_update:rr.shadowMap.needsUpdate,type:rr.shadowMap.type,key_map_size:v.key.shadow.mapSize.toArray()},
  visibility:{model:v.model.visible,floor:v.floor.visible,contact:v.contact.visible,grid:v.grid.visible},scene_background:v.scene.background?.getHex?.()??null
 });
 const poster=document.querySelector('#detail-poster');if(!poster)throw Error('Missing original poster');
 const before=snapshot(),saved={pixelRatio:rr.getPixelRatio(),size:rr.getSize({set(x,y){this.x=x;this.y=y;return this;}}),actualViewport:Array.from(gl.getParameter(gl.VIEWPORT)),actualScissor:Array.from(gl.getParameter(gl.SCISSOR_BOX)),camera:v.camera.clone(),backdropCamera:r.backdrop.camera.clone(),backdropShadowViewport:r.backdrop.shadowViewport.value.clone(),draw:r.draw,ownDraw:Object.hasOwn(r,'draw'),autoUpdate:rr.shadowMap.autoUpdate,needsUpdate:rr.shadowMap.needsUpdate,viewport:rr.getViewport(vector()),scissor:rr.getScissor(vector()),scissorTest:rr.getScissorTest(),clearColor:rr.getClearColor(color()),clearAlpha:rr.getClearAlpha(),autoClear:rr.autoClear,shadowViewport:v.shadowViewport.value.clone(),visibility:[v.model,v.floor,v.contact,v.grid].map(o=>[o,o.visible])};
 const state={owner,r,rr,v,canvas,gl,rect,saved,snapshot,before,overlay:null,suppressed:0,images:{untouched:canvas.toDataURL('image/png')},states:{before}};window.__detailLayerDiagnostic=state;state.poster=poster;state.posterStyle=state.poster.getAttribute('style');state.posterIdentity=JSON.stringify({src:state.poster.currentSrc||state.poster.src,id:state.poster.dataset.modelId,width:state.poster.naturalWidth,height:state.poster.naturalHeight,className:state.poster.className});
 // Prevent a late scheduled draw from replacing the isolated diagnostic layer.
 r.draw=()=>{state.suppressed++;};rr.shadowMap.autoUpdate=false;rr.shadowMap.needsUpdate=false;
 const resetVisibility=()=>{for(const[o,visible]of saved.visibility)o.visible=visible;};
 // Freezing shadow updates removes Three's normal setRenderTarget(null) floor
 // path. Logical setViewport() instead rounds. Reuse the actual integer GL state
 // captured before mutation, through Three's state cache (never raw gl calls).
 const nativeRaster=()=>{rr.state.viewport(vector().set(...saved.actualViewport));rr.state.scissor(vector().set(...saved.actualScissor));};
 const clear=()=>{rr.setScissorTest(false);rr.setClearColor(0,0);rr.clear(true,true,true);nativeRaster();rr.setScissorTest(true);v.shadowViewport.value.copy(saved.shadowViewport);};
 const record=name=>{state.images[name]=canvas.toDataURL('image/png');state.states[name]=snapshot();if(JSON.stringify(state.states[name].actual_gl.viewport)!==JSON.stringify(saved.actualViewport)||JSON.stringify(state.states[name].actual_gl.scissor)!==JSON.stringify(saved.actualScissor))throw Error('Diagnostic physical GL frame changed '+name);const e=gl.getError();if(e!==0)throw Error('Diagnostic WebGL error '+name+': '+e);};
 resetVisibility();clear();r.renderScenePasses(v);record('transparent_detail');
 resetVisibility();v.floor.visible=v.contact.visible=v.grid.visible=false;clear();r.renderScenePasses(v);record('model_only');
 resetVisibility();v.model.visible=false;clear();r.renderScenePasses(v);record('shadow_only');
 resetVisibility();clear();r.backdrop.shadowViewport.value.copy(saved.backdropShadowViewport);r.renderScenePasses(r.backdrop);record('backdrop_only');
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
  state.overlay?.remove();if(state.posterStyle===null)state.poster.removeAttribute('style');else state.poster.setAttribute('style',state.posterStyle);for(const[o,visible]of saved.visibility)o.visible=visible;v.camera.copy(saved.camera);r.backdrop.camera.copy(saved.backdropCamera);r.backdrop.shadowViewport.value.copy(saved.backdropShadowViewport);
  if(state.highResizeStarted){rr.setSize(saved.size.x,saved.size.y,false);rr.setPixelRatio(saved.pixelRatio);}rr.shadowMap.autoUpdate=saved.autoUpdate;rr.shadowMap.needsUpdate=saved.needsUpdate;rr.autoClear=saved.autoClear;
  v.shadowViewport.value.copy(saved.shadowViewport);rr.setClearColor(saved.clearColor,saved.clearAlpha);rr.setViewport(saved.viewport);rr.setScissor(saved.scissor);rr.setScissorTest(saved.scissorTest);rr.state.viewport(v.shadowViewport.value.clone().set(...saved.actualViewport));rr.state.scissor(v.shadowViewport.value.clone().set(...saved.actualScissor));
  if(saved.ownDraw)r.draw=saved.draw;else delete r.draw;
  saved.draw.call(r);
  const restored=canvas.toDataURL('image/png'),after=snapshot(),posterAfter={style:state.poster.getAttribute('style'),identity:JSON.stringify({src:state.poster.currentSrc||state.poster.src,id:state.poster.dataset.modelId,width:state.poster.naturalWidth,height:state.poster.naturalHeight,className:state.poster.className})};
  result={reference:state.highReference,poster_restoration:{before:{style:state.posterStyle,identity:state.posterIdentity},after:posterAfter},poster_exact:state.poster.getAttribute('style')===state.posterStyle&&JSON.stringify({src:state.poster.currentSrc||state.poster.src,id:state.poster.dataset.modelId,width:state.poster.naturalWidth,height:state.poster.naturalHeight,className:state.poster.className})===state.posterIdentity,images:state.images,states:state.states,image:restored,state:after,restored_exact:restored===state.images.untouched,state_exact:JSON.stringify(after)===JSON.stringify(state.before),suppressed_draw_calls:state.suppressed,gl_error:gl.getError()};
 }catch(error){result={reference:state.highReference,images:state.images,states:state.states,restored_exact:false,state_exact:false,restoration_error:error.message,suppressed_draw_calls:state.suppressed};try{result.image=canvas.toDataURL('image/png');}catch{}try{result.state=snapshot();}catch{}}finally{state.overlay?.remove();if(state.posterStyle===null)state.poster.removeAttribute('style');else state.poster.setAttribute('style',state.posterStyle);if(saved.ownDraw)r.draw=saved.draw;else delete r.draw;delete window.__detailLayerDiagnostic;}
 return result;
}

export async function captureNativeLayerDiagnostic(page,{referenceRasterSize}={}){
 const owner=randomUUID();let result,error,restored;
 try{result=await page.evaluate(beginNativeLayerDiagnostic,owner);
  result.composite=await page.locator('#detail').screenshot();
  result.states.background_stage=await page.evaluate(prepareDiagnosticPosterStage,{owner,show:false});
  result.background_stage=await page.locator('#detail').screenshot();
  const before=await page.evaluate(prepareDiagnosticPosterStage,{owner,show:true});
  result.same_ui_poster=await page.locator('#detail').screenshot();
  const after=await page.evaluate(prepareDiagnosticPosterStage,{owner,show:true});
  result.states.same_ui_poster={...before,after,source_kind:'controlled-ready-ui-original-css-image'};
  assert.deepEqual(after,before,'Controlled poster UI/source/CSS changed during screenshot');if(referenceRasterSize!==undefined){const high=await page.evaluate(captureHighDensityReference,{owner,target:referenceRasterSize});Object.assign(result.images,high.images);Object.assign(result.states,high.states);result.reference=high.reference;result.high_density_composite=await page.locator('#detail').screenshot();result.states.high_density_composite_after=await page.evaluate(inspectHighDensityComposite,owner);assert.deepEqual(result.states.high_density_composite_after,result.states.high_density_composite,'High-density CSS/UI/source changed during screenshot');}}

 catch(e){error=e;}
 finally{try{restored=await page.evaluate(restoreNativeLayerDiagnostic,owner);}catch(e){error??=e;}}
 if(restored){
  result??={kind:'native-layer-diagnostic-only',images:restored.images,states:restored.states};
  Object.assign(result.images,restored.images);Object.assign(result.states,restored.states);result.reference??=restored.reference;if(restored.image)result.images.restored=restored.image;if(restored.state)result.states.restored=restored.state;result.restoration_error=restored.restoration_error??null;result.restored_exact=restored.restored_exact;result.poster_restored_exact=restored.poster_exact;result.poster_restoration=restored.poster_restoration;result.suppressed_draw_calls=restored.suppressed_draw_calls;
  try{assert(!restored.restoration_error,'Diagnostic restoration failed: '+restored.restoration_error);assert(restored.poster_exact,'Diagnostic changed original poster identity/style');assert.equal(restored.gl_error,0,'Diagnostic restore WebGL error');assert(restored.restored_exact,'Diagnostic changed the untouched native raster');assert(restored.state_exact,'Diagnostic changed camera/renderer state');}catch(e){error??=e;}
 }
 if(error){error.diagnostic={...result,error:error.message};throw error;}
 assert(restored,'Missing diagnostic restore');return result;
}

// Only original loaded image visibility/transition changes; no reconstructed image.
export function prepareDiagnosticPosterStage({owner,show}){
 const s=window.__detailLayerDiagnostic;if(s?.owner!==owner)throw Error('Diagnostic owner mismatch');s.overlay.style.visibility='hidden';
 const p=s.poster;if(show){p.style.transition='none';p.style.opacity='1';p.style.visibility='visible';}
 const rect=e=>{const b=e.getBoundingClientRect();return{x:b.x,y:b.y,width:b.width,height:b.height};};
 const css=getComputedStyle(p);if(css.opacity!==(show?'1':'0')||show&&css.visibility!=='visible')throw Error('Unexpected actual poster handoff visibility');const image={id:p.dataset.modelId,state:p.dataset.state,src:p.currentSrc||p.src,width:p.naturalWidth,height:p.naturalHeight,rect:rect(p),transform:css.transform,origin:css.transformOrigin,fit:css.objectFit,position:css.objectPosition,opacity:css.opacity};
 if(image.id!==s.v.asset.id||image.state!=='ready'||!image.width)throw Error('Original ready poster binding unavailable');
 return{...s.snapshot(),image,ui:{loading:{text:document.querySelector('#loading').textContent,rect:rect(document.querySelector('#loading'))},compare:{disabled:document.querySelector('#compare').disabled,rect:rect(document.querySelector('#compare'))}}};
}

/** Re-render the current bound scene/camera at an integer physical sampling multiple.
 * Not a canonical-camera generation and not the original interactive native raster. */
export async function captureHighDensityReference({owner,target}){
 const s=window.__detailLayerDiagnostic;if(s?.owner!==owner)throw Error('Diagnostic owner mismatch');
 const{r,rr,v,canvas,gl,saved,snapshot}=s,original=s.before,short=Math.min(...saved.actualViewport.slice(2));
 if(![512,1536].includes(target)||short<=0)throw Error('Unreviewed high-density reference target');
 const k=Math.max(1,Math.ceil(target/short)),width=original.canvas.width*k,height=original.canvas.height*k,vp=saved.actualViewport.map(x=>x*k),sc=saved.actualScissor.map(x=>x*k),limits={texture:gl.getParameter(gl.MAX_TEXTURE_SIZE),renderbuffer:gl.getParameter(gl.MAX_RENDERBUFFER_SIZE),viewport:Array.from(gl.getParameter(gl.MAX_VIEWPORT_DIMS))};
 if(!Number.isSafeInteger(width*height)||width*height>10_000_000||width>Math.min(limits.texture,limits.renderbuffer,limits.viewport[0])||height>Math.min(limits.texture,limits.renderbuffer,limits.viewport[1]))throw Error('High-density reference exceeds reviewed GPU/resource bound');
 s.highReference={kind:'HIGH_DENSITY_NATIVE_REFERENCE',integer_scale:k,target_raster_size:target,buffer:{width,height},actual_gl:{viewport:vp,scissor:sc},effective_short_samples:short*k,limits,rgba_bytes:width*height*4,native_samples:gl.getParameter(gl.SAMPLES),sampling_note:'At least delivery density, NOT exact1536 grid; unchanged scene/camera/material/shadow map; native separately sealed; MSAA/derivative/fixed-pixel kernels are sampling-dependent, not exact native equivalence'};
 s.overlay.style.visibility='hidden';if(s.posterStyle===null)s.poster.removeAttribute('style');else s.poster.setAttribute('style',s.posterStyle);
 s.highResizeStarted=true;rr.setPixelRatio(1);rr.setSize(width,height,false);
 const vector=()=>v.shadowViewport.value.clone(),reset=()=>{for(const[o,visible]of saved.visibility)o.visible=visible;};
 // This is the existing non-companion layer0 pass, with the already-bound
 // native shadow frame scaled explicitly instead of recalculated from CSS/DPR.
 const render=()=>{const mask=v.camera.layers.mask,auto=rr.autoClear;try{rr.autoClear=false;v.camera.layers.set(0);rr.render(v.scene,v.camera);}finally{v.camera.layers.mask=mask;rr.autoClear=auto;}};
 const stage=name=>{rr.setScissorTest(false);rr.setClearColor(0,0);rr.clear(true,true,true);rr.state.viewport(vector().set(...vp));rr.state.scissor(vector().set(...sc));rr.setScissorTest(true);v.shadowViewport.value.set(...saved.shadowViewport.toArray().map(x=>x*k));render();s.images[name]=canvas.toDataURL('image/png');s.states[name]=snapshot();const actual=s.states[name];if(canvas.width!==width||canvas.height!==height||gl.drawingBufferWidth!==width||gl.drawingBufferHeight!==height||actual.actual_gl.samples!==s.highReference.native_samples||JSON.stringify(actual.actual_gl.viewport)!==JSON.stringify(vp)||JSON.stringify(actual.actual_gl.scissor)!==JSON.stringify(sc)||JSON.stringify(actual.camera)!==JSON.stringify(original.camera)||JSON.stringify(actual.model_matrix)!==JSON.stringify(original.model_matrix)||JSON.stringify(actual.shadow_viewport)!==JSON.stringify(saved.shadowViewport.toArray().map(x=>x*k)))throw Error('High-density source/camera/physical frame changed '+name);if(gl.getError()!==0)throw Error('High-density WebGL error '+name);};
 reset();stage('high_density_detail');v.floor.visible=v.contact.visible=v.grid.visible=false;stage('high_density_model');reset();v.model.visible=false;stage('high_density_shadow');reset();
 // Restore the original physical framebuffer BEFORE composing over its original
 // backdrop. The quality reference must not introduce a different background.
 rr.setSize(saved.size.x,saved.size.y,false);rr.setPixelRatio(saved.pixelRatio);rr.setScissorTest(false);rr.setClearColor(0,0);rr.clear(true,true,true);rr.state.viewport(vector().set(...saved.actualViewport));rr.state.scissor(vector().set(...saved.actualScissor));rr.setScissorTest(true);v.shadowViewport.value.copy(saved.shadowViewport);r.backdrop.shadowViewport.value.copy(saved.backdropShadowViewport);r.renderScenePasses(r.backdrop);
 s.overlay.src=s.images.high_density_detail;await s.overlay.decode();if(s.overlay.naturalWidth!==width||s.overlay.naturalHeight!==height||getComputedStyle(s.poster).opacity!=='0')throw Error('High-density CSS source/poster ownership mismatch');s.overlay.style.visibility='visible';await new Promise(requestAnimationFrame);
 s.highCompositeSnapshot=()=>{const uiRect=e=>{const b=e.getBoundingClientRect();return{x:b.x,y:b.y,width:b.width,height:b.height};};const ui={loading:{text:document.querySelector('#loading').textContent,rect:uiRect(document.querySelector('#loading'))},compare:{disabled:document.querySelector('#compare').disabled,rect:uiRect(document.querySelector('#compare'))}};return{...snapshot(),ui,reference:s.highReference,diagnostic_composite:{source:'HIGH_DENSITY_NATIVE_REFERENCE',source_matches_reference:s.overlay.src===s.images.high_density_detail,poster_style:s.poster.getAttribute('style'),image_width:s.overlay.naturalWidth,image_height:s.overlay.naturalHeight,css_rect:JSON.parse(JSON.stringify(s.overlay.getBoundingClientRect())),background:'original native density backdrop and ready UI'}};};
 s.states.high_density_composite=s.highCompositeSnapshot();
 return{images:Object.fromEntries(['high_density_detail','high_density_model','high_density_shadow'].map(k=>[k,s.images[k]])),states:Object.fromEntries(['high_density_detail','high_density_model','high_density_shadow','high_density_composite'].map(k=>[k,s.states[k]])),reference:s.highReference};
}

export function inspectHighDensityComposite(owner){const s=window.__detailLayerDiagnostic;if(s?.owner!==owner||!s.highCompositeSnapshot)throw Error('Missing high-density composite owner');return s.highCompositeSnapshot();}

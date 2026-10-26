/** Right-only revision. The historical wheel/pair renderer and its seals stay unchanged. */
export const DETAIL_HIRES_METHOD='PreviewRenderer.select(detail)/canonical-square-native-clipping-hires-v2';
export const DETAIL_HIRES_SIZES=Object.freeze([1536,2048]);
export function detailPresentationPolicy(rasterSize){
 if(!DETAIL_HIRES_SIZES.includes(rasterSize))throw new Error('Unreviewed detail raster size');
 return {revision:2,minimum_margin:0.025,screen_shift:0.06,raster_size:rasterSize};
}
export function validDetailPresentation(value){
 return !!value&&Object.keys(value).sort().join(',')==='minimum_margin,raster_size,revision,screen_shift'
  &&value.revision===2&&value.minimum_margin===0.025&&value.screen_shift===0.06&&DETAIL_HIRES_SIZES.includes(value.raster_size);
}

export function detailCapturePolicy(base,presentation){return presentation?{...base,detail_revision:presentation}:base;}

/** Exact physical viewport used after the pinned Three shadow pass restores target=null.
 * Keep the legacy renderer untouched; only opted-in posters/ground-shadow frames use this mapping.
 */
export function detailScreenFrame(rect,viewport,ratio,shift=.06){
 const {left,top,width,height}=rect,W=viewport.width,H=viewport.height;
 if(![left,top,width,height,W,H,ratio,shift].every(Number.isFinite)||Math.min(width,height,W,H,ratio)<=0)return null;
 const bufferWidth=Math.floor(W*ratio),bufferHeight=Math.floor(H*ratio);if(!bufferWidth||!bufferHeight)return null;
 const x=Math.floor(left*ratio),y=Math.floor((H-top-height)*ratio),w=Math.floor(width*ratio),h=Math.floor(height*ratio);if(!w||!h)return null;
 const short=Math.min(width,height),cx=W/bufferWidth,cy=H/bufferHeight,sx=w*cx/width,sy=h*cy/height;
 return {physical_viewport:[x,y,w,h],buffer:[bufferWidth,bufferHeight],
  // Transform the existing contain image around its upper-left corner, including its canonical 6% shift.
  css_matrix:[sx,0,0,sy,x*cx-left-shift*short*sx,(bufferHeight-y-h)*cy-top],
  canonical_shadow_frame:[x+w/2-shift*short/width*w-short/width*w/2,y+h/2-short/height*h/2,short/width*w,short/height*h]};
}

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

/** Additive detail override. Must be applied AFTER the existing wheel resolver.
 * Does not change models, production evidence, wheel paths, camera or materials.
 * The publication gate must verify every file seal and current renderer input key.
 */
const HASH=/^[a-f0-9]{64}$/;
const ROUTES=new Set(['blender-cycles-cpu-v1','blender-detail-preview-wheel-v1']);
export function resolveDetailPresentation(asset,resources,poster,index){
 if(!poster||!ROUTES.has(poster.render_route)||poster.source_glb_sha256!==asset?.sha256?.glb)return poster;
 if(index?.version!==1||index.kind!=='detail-only-presentations'||!HASH.test(index.renderer_input_sha256||''))return poster;
 if(!Object.hasOwn(index.presentations||{},asset.id))return poster;
 const entry=index.presentations[asset.id];
 if(entry?.id!==asset.id||entry.source_glb_sha256!==asset.sha256.glb
  ||entry.production_descriptor!==asset.production_release||entry.production_descriptor!==poster.production_descriptor
  ||entry.previous_detail?.path!==poster.detail||!HASH.test(entry.previous_detail?.sha256||'')
  ||!resources.files?.some(file=>file.path===poster.detail&&file.sha256===entry.previous_detail.sha256)
  ||entry.detail!==`detail-presentations/${asset.id}.png`
  ||entry.png?.width!==512||entry.png?.height!==512||!Number.isSafeInteger(entry.png?.bytes)||entry.png.bytes<=0
  ||!HASH.test(entry.png.sha256||'')||entry.capture?.detail_sha256!==entry.png.sha256
  ||entry.capture?.source_glb_sha256!==asset.sha256.glb||entry.capture?.first_frame_id!==asset.id
  ||entry.capture?.renderer_input_sha256!==index.renderer_input_sha256
  ||entry.capture?.method!=='PreviewRenderer.select(detail)/canonical-square-native-clipping-v1')return poster;
 return {...poster,detail:entry.detail};
}

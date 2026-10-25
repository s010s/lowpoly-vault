/** Additive wheel-only presentation selection shared by native HTML and hydration.
 * Original resources, detail posters, source metadata and release provenance stay intact.
 * Pixel/source integrity is checked by wheel-presentations-test.mjs before publication.
 */
import wheelPresentations from './wheel-presentations-index.js';

const HASH=/^[a-f0-9]{64}$/;
const pair=value=>Array.isArray(value)&&value.length===2&&value.every(Number.isFinite);
export function validPresentationSpec(spec){
  return !!spec&&['azimuth','elevation','zoom','aspect'].every(key=>Number.isFinite(spec[key]))
    &&spec.zoom>0&&spec.elevation>-90&&spec.elevation<90&&Math.abs(spec.aspect-16/9)<1e-9
    &&pair(spec.offset)&&pair(spec.floorCenter)&&Array.isArray(spec.floorPoints)
    &&spec.floorPoints.length>=3&&spec.floorPoints.every(pair)
    &&!!spec.projectedBounds&&['left','right','top','bottom'].every(key=>Number.isFinite(spec.projectedBounds[key]))
    &&spec.projectedBounds.right>spec.projectedBounds.left&&spec.projectedBounds.top>spec.projectedBounds.bottom;
}

export function resolveGalleryPoster(asset,resources={},index=wheelPresentations){
  const poster=resources.posters?.[asset?.id];
  if(!poster||poster.source_glb_sha256!==asset?.sha256?.glb)return null;
  // An ordinary WebGL poster, a future asset, or an already framed resource is
  // never eligible, even if an index entry were accidentally added for its ID.
  if(poster.render_route!=='blender-cycles-cpu-v1'||poster.wheelSpec||asset.wheelSpec
    ||asset.production_posters?.route!=='blender-cycles-cpu-v1')return poster;
  if(index?.version!==1||index.kind!=='wheel-only-presentations'
    ||!Object.hasOwn(index.presentations||{},asset.id))return poster;
  const entry=index.presentations[asset.id];
  if(entry?.id!==asset.id||entry.source_glb_sha256!==asset.sha256.glb
    ||!HASH.test(entry.source_glb_sha256)||entry.production_descriptor!==asset.production_release
    ||entry.production_descriptor!==poster.production_descriptor
    ||entry.previous_wheel?.path!==poster.wheel||entry.unchanged_detail?.path!==poster.detail
    ||entry.wheel!==`wheel-presentations/${asset.id}.png`||!HASH.test(entry.png?.sha256||'')
    ||entry.png.sha256!==entry.capture_binding?.wheel_sha256
    ||entry.source_glb_sha256!==entry.capture_binding?.source_glb_sha256
    ||entry.capture_binding?.first_frame_id!==asset.id||!HASH.test(entry.capture_sha256||'')
    ||!Number.isSafeInteger(entry.png.bytes)||entry.png.bytes<=0||!validPresentationSpec(entry.wheelSpec))return poster;
  // A changed old wheel/detail seal must not silently inherit this correction.
  const sealed=pin=>HASH.test(pin?.sha256||'')&&resources.files?.some(file=>file.path===pin.path&&file.sha256===pin.sha256);
  if(!sealed(entry.previous_wheel)||!sealed(entry.unchanged_detail))return poster;
  return {...poster,wheel:entry.wheel,wheelSpec:entry.wheelSpec};
}

/** Shared by the actual detail renderer and offline image capture; theme changes only the surrounding UI. */
export const CARD_RENDER_PRESET = Object.freeze({
  version: 1,
  camera: { type:'perspective', fov:38, azimuth_deg:42, elevation_deg:23.3, fit_padding:1.08 },
  background: '#e8e4dc', color_space:'srgb', tone_mapping:'ACESFilmic', exposure:1.2,
  hemisphere: { sky:0xfff8e9, ground:0x708277, intensity:2.8 },
  lights: [ { color:0xfff5e7, intensity:3, position:[5,8,6] }, { color:0xffffff, intensity:1.25, position:[-5,3,-4] } ],
  image: { width:320, height:320, format:'image/webp', quality:0.75, frames:24 },
});
export function cameraDirection(azimuth=CARD_RENDER_PRESET.camera.azimuth_deg,elevation=CARD_RENDER_PRESET.camera.elevation_deg) {
  const a=azimuth*Math.PI/180,e=elevation*Math.PI/180;
  return [Math.sin(a)*Math.cos(e),Math.sin(e),Math.cos(a)*Math.cos(e)];
}

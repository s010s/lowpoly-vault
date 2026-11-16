// Authored GLB axes are X=width, Y=height, Z=depth. Inspection rotates only
// presentation; these physical dimensions always describe the authored pose.
export function formatModelLength(meters){
  if(!Number.isFinite(meters)||meters<0)return '—';
  // Preserve sub-millimeter dimensions without rounding positive lengths to zero.
  if(meters>0&&meters<.001)return Number((meters*1000).toPrecision(3))+' mm';
  return meters>=1?meters.toFixed(2)+' m':(meters*100).toFixed(1).replace(/\.0$/,'')+' cm';
}
export function hasMetricDimensions(asset){return asset?.units==='meters' && Array.isArray(asset.dimensions) && asset.dimensions.length===3 && asset.dimensions.every(n=>Number.isFinite(n)&&n>=0) && asset.dimensions.some(n=>n>0) && (!asset.axes?.glb_up || asset.axes.glb_up==='+Y') && (asset.blender_unit_scale===undefined || asset.blender_unit_scale===1);}
export function modelHeight(asset){return hasMetricDimensions(asset)?formatModelLength(asset.dimensions[1]):'—';}
export function dimensionDetails(asset,lang='en'){
  if(!hasMetricDimensions(asset))return lang==='zh'?'尺寸单位未确认，暂不显示物理尺寸。':'Dimension units are unconfirmed; physical measurements are unavailable.';
  const [width,height,depth]=asset.dimensions||[];
  return lang==='zh'?`高度 (Y)：${formatModelLength(height)} · 宽度 (X)：${formatModelLength(width)} · 深度 (Z)：${formatModelLength(depth)}`:
    `Height (Y): ${formatModelLength(height)} · Width (X): ${formatModelLength(width)} · Depth (Z): ${formatModelLength(depth)}`;
}
export function dimensionNote(lang='en',asset){
  if(asset && !hasMetricDimensions(asset))return lang==='zh'?'模型坐标不能直接视为米制尺寸，暂不提供实物比例比较。':'Model coordinates are not verified metric measurements; physical-scale comparison is unavailable.';
  return lang==='zh'?'以上为原始造型的美术设定尺寸，单位为米 (m)、厘米 (cm) 或毫米 (mm)；旋转查看时数值保持不变，并非经过验证的标本测量。':
    'These authored-pose dimensions use meters (m), centimeters (cm) or millimeters (mm) and stay fixed when you rotate the view. They are artistic specifications, not verified specimen measurements.';
}
export function comparisonMeasurement(asset,lang='en'){
  // This shallow surface is understood by its X/Z footprint, not its Y height.
  // Keep the ordinary height metric and reference-selection policy independent.
  if(asset?.id!=='wave-ripple-surface'||!hasMetricDimensions(asset))return '';
  const [width,thickness,depth]=asset.dimensions||[];
  if(![width,thickness,depth].every(value=>Number.isFinite(value)&&value>0))return '';
  const footprint=`${width.toFixed(2)} × ${depth.toFixed(2)} m`;
  return lang==='zh'?`占地（宽 × 深）${footprint} · 厚度${formatModelLength(thickness)}`:
    `Footprint (W × D) ${footprint} · Thickness ${formatModelLength(thickness)}`;
}
export function comparisonText(kind,lang='en',asset){
  const reference=lang==='zh'?(kind==='hand'?'手长18 cm':'人物身高1.8m'):
    (kind==='hand'?'Hand length 18 cm':'Human height 1.8 m');
  const measurement=comparisonMeasurement(asset,lang),context=measurement?` · ${measurement}`:'';
  return lang==='zh'?`美术设定尺寸 · 示意比例 · ${reference}${context} · 水平拖动旋转 · 双指/滚轮缩放`:
    `Illustrative authored scale · ${reference}${context} · Horizontal drag · Pinch/scroll to zoom`;
}

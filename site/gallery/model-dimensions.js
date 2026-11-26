// Authored GLB axes are X=width, Y=height, Z=depth. Inspection rotates only
// presentation; these physical dimensions always describe the authored pose.
export function formatModelLength(meters) {
  if (!Number.isFinite(meters) || meters < 0) return '—';
  // Preserve sub-millimeter dimensions without rounding positive lengths to zero.
  if (meters > 0 && meters < 0.001) return Number((meters * 1000).toPrecision(3)) + ' mm';
  return meters >= 1 ? meters.toFixed(2) + ' m' : (meters * 100).toFixed(1).replace(/\.0$/, '') + ' cm';
}

export function hasMetricDimensions(asset) {
  return (
    asset?.units === 'meters' &&
    Array.isArray(asset.dimensions) &&
    asset.dimensions.length === 3 &&
    asset.dimensions.every(n => Number.isFinite(n) && n >= 0) &&
    asset.dimensions.some(n => n > 0) &&
    (!asset.axes?.glb_up || asset.axes.glb_up === '+Y') &&
    (asset.blender_unit_scale === undefined || asset.blender_unit_scale === 1)
  );
}

export function isFlatAsset(asset) {
  if (!hasMetricDimensions(asset)) return false;
  const [width, height, depth] = asset.dimensions;
  const maxHorizontal = Math.max(width, depth);
  return maxHorizontal > 0 && height > 0 && height / maxHorizontal < 0.25;
}

export function formatFootprint(width, depth) {
  if (!Number.isFinite(width) || !Number.isFinite(depth) || width <= 0 || depth <= 0) return '—';
  if (Math.max(width, depth) >= 1) return `${width.toFixed(2)} × ${depth.toFixed(2)} m`;
  return `${formatModelLength(width)} × ${formatModelLength(depth)}`;
}

export function modelHeight(asset) {
  return hasMetricDimensions(asset) ? formatModelLength(asset.dimensions[1]) : '—';
}

/** Smart primary metric: flat landforms/traces show X × Z footprint; upright models show Y height. */
export function primaryDimension(asset, lang = 'en') {
  const zh = lang === 'zh' || lang === 'zh-CN';
  if (!hasMetricDimensions(asset)) {
    return { value: '—', labelEn: 'Model height', labelZh: '模型高度', label: zh ? '模型高度' : 'Model height', isFlat: false };
  }
  const [width, height, depth] = asset.dimensions;
  if (isFlatAsset(asset)) {
    return {
      value: formatFootprint(width, depth),
      labelEn: 'Footprint',
      labelZh: '占地尺寸',
      label: zh ? '占地尺寸' : 'Footprint',
      isFlat: true,
    };
  }
  return {
    value: formatModelLength(height),
    labelEn: 'Model height',
    labelZh: '模型高度',
    label: zh ? '模型高度' : 'Model height',
    isFlat: false,
  };
}

export function formatDimensionsXYZ(asset) {
  if (!hasMetricDimensions(asset)) return '—';
  const [width, height, depth] = asset.dimensions;
  return `${formatModelLength(width)} × ${formatModelLength(height)} × ${formatModelLength(depth)}`;
}

export function dimensionDetails(asset, lang = 'en') {
  const zh = lang === 'zh' || lang === 'zh-CN';
  if (!hasMetricDimensions(asset)) {
    return zh
      ? '尺寸单位未确认，暂未标定物理尺寸。'
      : 'Dimension units are unconfirmed; physical measurements are unavailable.';
  }
  const [width, height, depth] = asset.dimensions || [];
  return zh
    ? `高度 (Y)：${formatModelLength(height)} · 宽度 (X)：${formatModelLength(width)} · 深度 (Z)：${formatModelLength(depth)}`
    : `Height (Y): ${formatModelLength(height)} · Width (X): ${formatModelLength(width)} · Depth (Z): ${formatModelLength(depth)}`;
}

export function dimensionNote(lang = 'en', asset) {
  const zh = lang === 'zh' || lang === 'zh-CN';
  if (asset && !hasMetricDimensions(asset)) {
    return zh
      ? '模型坐标不能直接视为米制尺寸，暂不提供实物比例比较。'
      : 'Model coordinates are not verified metric measurements; physical-scale comparison is unavailable.';
  }
  return zh
    ? '以上为原始造型的美术设定尺寸，单位为米 (m)、厘米 (cm) 或毫米 (mm)；旋转查看时数值保持不变，并非经过验证的标本测量。'
    : 'These authored-pose dimensions use meters (m), centimeters (cm) or millimeters (mm) and stay fixed when you rotate the view. They are artistic specifications, not verified specimen measurements.';
}

export function comparisonMeasurement(asset, lang = 'en') {
  if (!isFlatAsset(asset)) return '';
  const [width, thickness, depth] = asset.dimensions || [];
  if (![width, thickness, depth].every(value => Number.isFinite(value) && value > 0)) return '';
  const footprint = formatFootprint(width, depth);
  const zh = lang === 'zh' || lang === 'zh-CN';
  return zh
    ? `占地（宽 × 深）${footprint} · 厚度 ${formatModelLength(thickness)}`
    : `Footprint (W × D) ${footprint} · Thickness ${formatModelLength(thickness)}`;
}

export function comparisonText(kind, lang = 'en', asset) {
  const zh = lang === 'zh' || lang === 'zh-CN';
  const reference = zh
    ? (kind === 'hand' ? '手长 18 cm' : '人物身高 1.8 m')
    : (kind === 'hand' ? 'Hand length 18 cm' : 'Human height 1.8 m');
  const measurement = comparisonMeasurement(asset, lang);
  const context = measurement ? ` · ${measurement}` : '';
  return zh
    ? `示意比例 · ${reference}${context}`
    : `Illustrative scale · ${reference}${context}`;
}

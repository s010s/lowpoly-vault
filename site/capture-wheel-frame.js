/** One actual PreviewRenderer capture. This does not grant visual or publication approval. */
const capturing = new WeakSet();
export async function captureWheelFrame(renderer, asset) {
  if (!renderer || typeof renderer.poster !== 'function' || !asset?.id || !/^[a-f0-9]{64}$/.test(asset.sha256?.glb || '')) throw new Error('Exact renderer and source asset required');
  if (capturing.has(renderer)) throw new Error('Wheel capture must be serialized per renderer');
  capturing.add(renderer);
  try {
  // Never call detail capture, change authored geometry, or independently infer framing.
  const dataURL = await renderer.poster(asset, {wheel: true});
  const wheelSpec = structuredClone(renderer.lastPosterSpec);
  if (!dataURL.startsWith('data:image/png;base64,') || !wheelSpec) throw new Error('Actual PNG and same-call wheel framing required');
  return {id: asset.id, source_glb_sha256: asset.sha256.glb, dataURL, wheelSpec};
  } finally { capturing.delete(renderer); }
}

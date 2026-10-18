// Blend premultiplied color AND coverage once, rather than stacking two
// translucent source-over layers (which darkens edges and thins the silhouette).
export const HOVER_REVEAL_MS = 140;
export function paintHoverReveal(canvas, poster, model, weight) {
  const context = canvas.getContext('2d');
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.globalCompositeOperation = 'lighter';
  context.globalAlpha = 1 - weight;
  context.drawImage(poster, 0, 0, canvas.width, canvas.height);
  context.globalAlpha = weight;
  context.drawImage(model, 0, 0, canvas.width, canvas.height);
  context.globalAlpha = 1;
  context.globalCompositeOperation = 'source-over';
}

// The caller supplies a snapshot only after the matching model's first draw.
// There is no additional renderer, scene, fetch, or persistent animation loop.
export function startHoverReveal({ host, poster, model, onFinish }) {
  const canvas = document.createElement('canvas');
  canvas.width = model.width; canvas.height = model.height;
  canvas.className = 'model-hover-reveal';
  canvas.setAttribute('aria-hidden', 'true');
  canvas.__presentation = model.__presentation;
  canvas.dataset.assetId = model.dataset.assetId;
  let raf = 0, elapsed = 0, previous = performance.now(), stopped = false;
  const paint = weight => { paintHoverReveal(canvas, poster, model, weight); canvas.dataset.revealWeight = String(weight); };
  function cancel() {
    if (stopped) return;
    stopped = true; cancelAnimationFrame(raf);
    canvas.remove(); canvas.width = canvas.height = 0;
    model.width = model.height = 0;
  }
  function frame(time) {
    if (stopped) return;
    // Slow frames must not turn the dissolve into another one-frame swap.
    elapsed += Math.min(Math.max(0, time - previous), HOVER_REVEAL_MS / 3);
    previous = time;
    const progress = Math.min(1, elapsed / HOVER_REVEAL_MS);
    paint(progress * progress * (3 - 2 * progress));
    if (progress === 1) { cancel(); onFinish(); }
    else raf = requestAnimationFrame(frame);
  }
  paint(0); host.append(canvas); raf = requestAnimationFrame(frame);
  return { canvas, cancel };
}

export const RETURN_TIMING = Object.freeze({ travel: 120, fade: 60, total: 180 });
const clamp = value => Math.max(0, Math.min(1, value));
export const shortestAngleDelta = (from, to) => ((to - from + 540) % 360) - 180;
export const returnEase = progress => 1 - (1 - clamp(progress)) ** 3;
export function interpolateReturnView(from, to, progress) {
  const t = returnEase(progress), mix = (a, b) => a + (b - a) * t;
  return { azimuth_deg: from.azimuth_deg + shortestAngleDelta(from.azimuth_deg, to.azimuth_deg) * t,
    elevation_deg: mix(from.elevation_deg, to.elevation_deg), distance: mix(from.distance, to.distance) };
}

/** Only runs during close. One borrowed live canvas, no second scene or loop. */
export function startModelReturn({ stage, host, from, to, getTarget, initialView, canonicalView, reduced = false, onAligned = () => {} }) {
  let raf = 0, timer, done, aligned = false;
  const started = performance.now();
  const motion = { playState: 'running', finished: new Promise(resolve => { done = resolve; }), cancel, finish };
  const styles = stage.beginCanonicalReturnStyles?.();
  Object.assign(host.style, { position: 'fixed', left: `${from.left}px`, top: `${from.top}px`,
    width: `${from.width}px`, height: `${from.height}px`, transformOrigin: '0 0', pointerEvents: 'none', willChange: 'transform,opacity' });
  const place = t => {
    const target = getTarget?.() || to, dx = target.left - from.left, dy = target.top - from.top, scale = target.width / from.width;
    host.style.transform = `translate(${dx * t}px,${dy * t}px) scale(${1 + (scale - 1) * t})`;
  };
  const align = () => {
    if (aligned) return;
    aligned = true;
    place(1); host.dataset.returnPhase = 'fading'; host.dataset.returnProgress = '1';
    stage.canonicalReturnStyleProgress?.(1, styles);
    stage.setView(canonicalView.azimuth_deg, canonicalView.elevation_deg, canonicalView.distance); onAligned();
  };
  function end(result) {
    if (raf) cancelAnimationFrame(raf); raf = 0; clearTimeout(timer);
    motion.playState = result ? 'finished' : 'idle'; done(result);
    stage.endCanonicalReturnStyles?.(styles);
  }
  function cancel() { if (motion.playState === 'running') end(false); }
  function finish() {
    if (motion.playState !== 'running') return;
    if (stage._host !== host) { cancel(); return; }
    align(); host.style.opacity = '0'; host.dataset.returnProgress = '1'; end(true);
  }
  function frame(time) {
    raf = 0;
    if (motion.playState !== 'running') return;
    if (stage._host !== host) { cancel(); return; }
    const elapsed = Math.max(0, time - started), progress = clamp(elapsed / RETURN_TIMING.travel);
    host.dataset.returnProgress = String(progress);
    if (progress < 1) {
      const view = interpolateReturnView(initialView, canonicalView, progress);
      host.dataset.returnPhase = 'moving';
      place(returnEase(progress)); stage.canonicalReturnStyleProgress?.(returnEase(progress), styles);
      stage.setView(view.azimuth_deg, view.elevation_deg, view.distance);
    } else {
      align(); place(1); host.style.opacity = String(1 - clamp((elapsed - RETURN_TIMING.travel) / RETURN_TIMING.fade));
    }
    if (elapsed >= RETURN_TIMING.total) finish();
    else raf = requestAnimationFrame(frame);
  }
  place(0); host.dataset.returnPhase = 'moving'; host.dataset.returnProgress = '0';
  if (reduced) finish();
  else {
    raf = requestAnimationFrame(frame);
    // A background tab must still finish dismissal when RAF is suspended.
    timer = setTimeout(finish, RETURN_TIMING.total);
  }
  return motion;
}

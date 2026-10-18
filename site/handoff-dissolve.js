export const HANDOFF_DISSOLVE_MS = 160;

/** One finite clock for complementary bitmap/live coverage. No renderer or draw loop. */
export function startHandoffDissolve({ visual, target, reduced, onFinish }) {
  const doc = visual.ownerDocument;
  const original = { visual: visual.style.opacity, target: target.style.opacity };
  const started = performance.now();
  let raf = 0, active = true, partialPresented = false;
  const paint = progress => {
    target.style.opacity = String(progress);
    visual.style.opacity = String(1 - progress);
  };
  function end(complete) {
    if (!active) return;
    active = false;
    cancelAnimationFrame(raf); raf = 0;
    doc.removeEventListener('visibilitychange', visibility);
    reduced.removeEventListener('change', preference);
    try { if (complete) onFinish(); }
    finally {
      target.style.opacity = original.target;
      visual.style.opacity = original.visual;
    }
  }
  function cancel() { end(false); }
  function finish() { if (active) { paint(1); end(true); } }
  function visibility() { if (doc.hidden) finish(); }
  function preference() { if (reduced.matches) finish(); }
  function frame(time) {
    raf = 0;
    if (!active) return;
    if (!visual.isConnected || !target.isConnected) { cancel(); return; }
    // A stalled first frame must still leave one real partial-weight paint.
    // After that render opportunity, catch up to the original wall-clock end;
    // capping every delta would accumulate delay under alternating slow frames.
    const elapsed = Math.min(Math.max(0, time - started), partialPresented ? HANDOFF_DISSOLVE_MS : HANDOFF_DISSOLVE_MS / 2);
    const progress = Math.min(1, elapsed / HANDOFF_DISSOLVE_MS);
    paint(progress);
    if (progress > .025 && progress < .985) partialPresented = true;
    if (progress === 1) end(true);
    else raf = requestAnimationFrame(frame);
  }
  paint(0);
  doc.addEventListener('visibilitychange', visibility);
  reduced.addEventListener('change', preference);
  if (doc.hidden || reduced.matches) finish();
  else raf = requestAnimationFrame(frame);
  return { cancel, finish };
}

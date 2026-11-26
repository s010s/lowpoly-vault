/** Unified Apple-caliber motion language shared by the site and gallery apps. */

export const MOTION = Object.freeze({
  micro: 90,
  fast: 160,
  base: 220,
  gentle: 380,
  returnDuration: 300,
  theme: 440,
  themeReduced: 120,
  themeFallback: 160,
  spatial: 700,
  reducedFade: 100,
  easeStandard: 'cubic-bezier(0.22, 1, 0.36, 1)',
  easeSpatial: 'cubic-bezier(0.32, 0.72, 0, 1)',
  easeTactile: 'cubic-bezier(0.2, 0, 0, 1)',
  easeExit: 'cubic-bezier(0.32, 0, 0.67, 0)',
});

export function prefersReducedMotion(media = globalThis.matchMedia) {
  try {
    return typeof media === 'function' && Boolean(media('(prefers-reduced-motion: reduce)')?.matches);
  } catch {
    return false;
  }
}

const activeAnimations = new WeakMap();
const presenceVersions = new WeakMap();
const resizeGuardInstalled = new WeakSet();

/** Run an interruptible one-shot WAAPI animation keyed by (element, id). */
export function animateOneShot(element, id, frames, options = {}) {
  if (!element || typeof element.animate !== 'function') return null;
  let registry = activeAnimations.get(element);
  if (!registry) {
    registry = new Map();
    activeAnimations.set(element, registry);
  }
  const prior = registry.get(id);
  if (prior) {
    try { prior.cancel(); } catch {}
    registry.delete(id);
  }
  let animation = null;
  try {
    animation = element.animate(frames, {
      duration: MOTION.fast,
      easing: MOTION.easeStandard,
      ...options,
      id: `vault-${id}`,
    });
  } catch {
    return null;
  }
  registry.set(id, animation);
  const cleanup = () => {
    if (registry.get(id) === animation) registry.delete(id);
  };
  Promise.resolve(animation.finished).then(cleanup, cleanup);
  return animation;
}

/** Cancel a named one-shot animation on an element if active. */
export function cancelOneShot(element, id) {
  const registry = element && activeAnimations.get(element);
  const prior = registry?.get(id);
  if (!prior) return false;
  try { prior.cancel(); } catch {}
  registry.delete(id);
  return true;
}

function readLiveOpacity(element) {
  if (typeof globalThis.getComputedStyle !== 'function') return NaN;
  try {
    const value = parseFloat(globalThis.getComputedStyle(element).opacity);
    return Number.isFinite(value) ? Math.max(0, Math.min(1, value)) : NaN;
  } catch {
    return NaN;
  }
}

/**
 * Interruptible show/hide transition for capsules, banners, notices, and empty states.
 * - Uses individual `translate`/`scale` properties so existing CSS `transform` (e.g. centering)
 *   is never clobbered.
 * - Uses `fill: 'forwards'` on exit and clears it after `hidden = true` to prevent end-frame flash.
 * - Reverses smoothly from live computed opacity when interrupted mid-flight.
 * - Falls back synchronously when WAAPI is unavailable (e.g. Node unit tests).
 */
export function animatePresence(element, visible, {
  id = 'presence',
  enterY = 4,
  exitY = 2,
  enterScale = 1,
  enterDuration = MOTION.fast,
  exitDuration = 130,
  immediate = false,
  reduced = prefersReducedMotion(),
  onHidden = null,
} = {}) {
  if (!element) return;
  const version = (presenceVersions.get(element) || 0) + 1;
  presenceVersions.set(element, version);
  const hasActive = Boolean(activeAnimations.get(element)?.has(id));
  const liveOpacity = hasActive ? readLiveOpacity(element) : NaN;
  cancelOneShot(element, id);

  if (visible) {
    const wasHidden = element.hidden || element.dataset?.visible === 'false' || hasActive;
    element.inert = false;
    element.removeAttribute?.('aria-hidden');
    element.hidden = false;
    if (element.dataset) element.dataset.visible = 'true';
    if (immediate || !wasHidden || typeof element.animate !== 'function') return;
    const startOpacity = Number.isFinite(liveOpacity) ? liveOpacity : 0;
    const remaining = Math.max(0.25, 1 - startOpacity);
    if (reduced) {
      animateOneShot(element, id, [{ opacity: startOpacity }, { opacity: 1 }], {
        duration: Math.round(MOTION.reducedFade * remaining),
        easing: MOTION.easeStandard,
      });
      return;
    }
    const from = { opacity: startOpacity };
    const to = { opacity: 1 };
    if (enterY) {
      from.translate = `0 ${(enterY * remaining).toFixed(2)}px`;
      to.translate = '0 0px';
    }
    if (enterScale !== 1) {
      from.scale = String(1 - (1 - enterScale) * remaining);
      to.scale = '1';
    }
    animateOneShot(element, id, [from, to], {
      duration: Math.round(enterDuration * remaining),
      easing: MOTION.easeStandard,
    });
    return;
  }

  if (element.dataset) element.dataset.visible = 'false';
  element.inert = true;
  element.setAttribute?.('aria-hidden', 'true');
  if (element.hidden || immediate || typeof element.animate !== 'function') {
    element.hidden = true;
    onHidden?.();
    return;
  }
  const startOpacity = Number.isFinite(liveOpacity) ? liveOpacity : 1;
  const remaining = Math.max(0.25, startOpacity);
  const frames = reduced
    ? [{ opacity: startOpacity }, { opacity: 0 }]
    : [
        { opacity: startOpacity, ...(exitY ? { translate: '0 0px' } : {}) },
        { opacity: 0, ...(exitY ? { translate: `0 ${exitY}px` } : {}) },
      ];
  const animation = animateOneShot(element, id, frames, {
    duration: Math.round((reduced ? 90 : exitDuration) * remaining),
    easing: MOTION.easeExit,
    fill: 'forwards',
  });
  if (!animation) {
    element.hidden = true;
    onHidden?.();
    return;
  }
  const settle = () => {
    if (presenceVersions.get(element) === version && element.dataset?.visible === 'false') {
      element.hidden = true;
      onHidden?.();
      try { animation.cancel(); } catch {}
    }
  };
  Promise.resolve(animation.finished).then(settle, settle);
}

/** Pause CSS transitions while the window is actively being resized to eliminate rubber-banding. */
export function installResizeMotionGuard({ win = globalThis.window, doc = globalThis.document, delay = 120 } = {}) {
  if (!win || !doc?.documentElement || typeof win.addEventListener !== 'function') return () => {};
  if (resizeGuardInstalled.has(doc)) return () => {};
  resizeGuardInstalled.add(doc);
  let timer = 0;
  const onResize = () => {
    doc.documentElement.dataset.resizing = 'true';
    clearTimeout(timer);
    timer = setTimeout(() => {
      delete doc.documentElement.dataset.resizing;
      timer = 0;
    }, delay);
  };
  win.addEventListener('resize', onResize, { passive: true });
  return () => {
    clearTimeout(timer);
    delete doc.documentElement.dataset.resizing;
    win.removeEventListener?.('resize', onResize);
    resizeGuardInstalled.delete(doc);
  };
}

/** Lock a variable-width button's minWidth before swapping to a shorter confirmation label. */
export function lockButtonWidth(button) {
  if (!button || typeof button.getBoundingClientRect !== 'function' || !button.style) return () => {};
  const width = button.getBoundingClientRect().width;
  if (width > 0) button.style.minWidth = `${Math.ceil(width)}px`;
  return () => {
    button.style?.removeProperty?.('min-width');
  };
}

/** Swap an icon container's SVG markup with a crisp, interruptible confirmation pop-in. */
export function swapIconSmooth(container, markup, { reduced = prefersReducedMotion() } = {}) {
  if (!container) return;
  container.innerHTML = markup;
  if (reduced) {
    animateOneShot(container, 'icon-swap', [{ opacity: 0.35 }, { opacity: 1 }], {
      duration: MOTION.reducedFade,
      easing: MOTION.easeStandard,
    });
    return;
  }
  animateOneShot(container, 'icon-swap', [
    { opacity: 0, transform: 'scale(0.76)' },
    { opacity: 1, transform: 'scale(1)' },
  ], {
    duration: MOTION.fast,
    easing: MOTION.easeStandard,
  });
}

function readZoomMetric(renderer) {
  if (!renderer?.detail?.camera) return NaN;
  if (renderer.comparison) return renderer.detail.camera.zoom;
  const pos = renderer.detail.camera.position;
  const target = renderer.controls?.target;
  if (pos && target && typeof pos.distanceTo === 'function') return pos.distanceTo(target);
  return NaN;
}

/**
 * Interruptible smooth stepper for discrete 3D zoom (+/-) and keyboard rotate triggers.
 * Keeps underlying renderer.zoom() / renderer.rotate() synchronous so wheel/touch stays 1:1
 * and all deterministic 3D unit tests remain unaffected.
 */
export function createDiscreteCameraStepper(getRenderer, { reduced = prefersReducedMotion } = {}) {
  let raf = 0;
  let lastTime = 0;
  let remLog = 0;
  let remAzimuth = 0;
  let remElevation = 0;
  const TAU = 40; // ms exponential time constant (~150-170ms settle, peak response on frame 1)

  function cancel() {
    if (raf && typeof cancelAnimationFrame === 'function') cancelAnimationFrame(raf);
    raf = 0;
    lastTime = 0;
    remLog = 0;
    remAzimuth = 0;
    remElevation = 0;
  }

  function step(now) {
    raf = 0;
    const renderer = getRenderer?.();
    if (!renderer || !renderer.detail?.model) {
      cancel();
      return;
    }
    if (reduced()) {
      const log = remLog, az = remAzimuth, el = renderer.comparison ? 0 : remElevation;
      cancel();
      if (Math.abs(log) > 1e-4) renderer.zoom(Math.exp(log));
      if (Math.abs(az) > 0.01 || Math.abs(el) > 0.01) renderer.rotate(az, el);
      return;
    }
    const dt = lastTime ? Math.min(48, Math.max(4, now - lastTime)) : 16;
    lastTime = now;
    const alpha = 1 - Math.exp(-dt / TAU);

    if (Math.abs(remLog) > 1e-4) {
      const done = Math.abs(remLog) < 0.0025;
      const delta = done ? remLog : remLog * alpha;
      remLog = done ? 0 : remLog - delta;
      const before = readZoomMetric(renderer);
      renderer.zoom(Math.exp(delta));
      const after = readZoomMetric(renderer);
      // Clear remaining backlog immediately when clamped at min/max zoom boundary.
      if (Number.isFinite(before) && Number.isFinite(after) && Math.abs(after - before) < 1e-6) {
        remLog = 0;
      }
    } else {
      remLog = 0;
    }

    if (renderer.comparison) remElevation = 0;
    if (Math.abs(remAzimuth) > 0.01 || Math.abs(remElevation) > 0.01) {
      const doneA = Math.abs(remAzimuth) < 0.12;
      const doneE = Math.abs(remElevation) < 0.12;
      const da = doneA ? remAzimuth : remAzimuth * alpha;
      const de = doneE ? remElevation : remElevation * alpha;
      remAzimuth = doneA ? 0 : remAzimuth - da;
      remElevation = doneE ? 0 : remElevation - de;
      if (da || de) renderer.rotate(da, de);
    } else {
      remAzimuth = 0;
      remElevation = 0;
    }

    if (remLog || remAzimuth || remElevation) {
      raf = requestAnimationFrame(step);
    } else {
      lastTime = 0;
    }
  }

  function schedule() {
    if (raf) return;
    lastTime = 0; // Ensures frame 1 always runs at full 16ms peak impulse.
    raf = requestAnimationFrame(step);
  }

  function zoom(factor) {
    const renderer = getRenderer?.();
    if (!renderer || !renderer.detail?.model) return;
    if (reduced() || typeof requestAnimationFrame !== 'function') {
      cancel();
      renderer.zoom(factor);
      return;
    }
    const delta = Math.log(factor);
    // Reversing direction immediately discards opposing backlog to eliminate dead zones.
    if (remLog && Math.sign(delta) !== Math.sign(remLog)) remLog = 0;
    remLog += delta;
    schedule();
  }

  function rotate(azimuth, elevation) {
    const renderer = getRenderer?.();
    if (!renderer || !renderer.detail?.model) return;
    const effElevation = renderer.comparison ? 0 : elevation;
    if (!azimuth && !effElevation) return;
    if (reduced() || typeof requestAnimationFrame !== 'function') {
      cancel();
      renderer.rotate(azimuth, effElevation);
      return;
    }
    if (azimuth && remAzimuth && Math.sign(azimuth) !== Math.sign(remAzimuth)) remAzimuth = 0;
    if (effElevation && remElevation && Math.sign(effElevation) !== Math.sign(remElevation)) remElevation = 0;
    remAzimuth += azimuth;
    remElevation += effElevation;
    schedule();
  }

  return { zoom, rotate, cancel };
}

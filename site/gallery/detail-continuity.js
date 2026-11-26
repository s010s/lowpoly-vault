import { MOTION } from '../motion-system.js';
const fastSettle = MOTION.easeSpatial;
const enterDuration = MOTION.gentle;
const returnDuration = MOTION.returnDuration;
const reducedDuration = 120;
const animationId = 'gallery-continuity-';

function contain(box, width, height) {
  const scale = Math.min(box.width / width, box.height / height);
  const w = width * scale, h = height * scale;
  return { left: box.left + (box.width - w) / 2, top: box.top + (box.height - h) / 2, width: w, height: h };
}

function raster(bitmap) {
  const width = bitmap.naturalWidth || bitmap.width, height = bitmap.naturalHeight || bitmap.height;
  if (!width || !height) return null;
  if (bitmap instanceof HTMLCanvasElement && !bitmap.isConnected) return bitmap;
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  canvas.getContext('2d').drawImage(bitmap, 0, 0);
  return canvas;
}

function imageFrame(image, { includeHidden = false } = {}) {
  if (!image?.naturalWidth || typeof getComputedStyle !== 'function') return null;
  const style = getComputedStyle(image);
  if (!includeHidden && style.visibility !== 'visible') return null;
  const box = contain(image.getBoundingClientRect(), image.naturalWidth, image.naturalHeight);
  if (!box.width || !box.height) return null;
  const opacity = Number(style.opacity);
  return { bitmap: image, box, opacity: Number.isFinite(opacity) ? opacity : 1 };
}

export function wheelArtwork(row) {
  if (!row || typeof getComputedStyle !== 'function') return null;
  let image = row.querySelector('img[data-thumbnail-state=ready]');
  if (!image) {
    const candidate = row.querySelector('.slot-image img');
    if (candidate?.complete && candidate.naturalWidth > 0) image = candidate;
  }
  const art = image && imageFrame(image);
  if (art) {
    // If HoverPresentation temporarily faded the wheel img to 0 while spinning,
    // still hand off the decoded wheel raster at full stage presence.
    if (art.opacity < .05) art.opacity = 1;
    const parentOp = Number(getComputedStyle(image.parentElement).opacity);
    const motionNode = row.querySelector('.slot-motion');
    const motionOp = motionNode ? Number(getComputedStyle(motionNode).opacity) : 1;
    art.opacity *= (Number.isFinite(parentOp) ? parentOp : 1) * (Number.isFinite(motionOp) ? motionOp : 1);
  }
  return art;
}

export function detailArtwork(image, live, stage) {
  if (live) return { bitmap: live, box: stage.getBoundingClientRect(), opacity: 1 };
  return imageFrame(image);
}

const CANONICAL_AZIMUTH = 42;
const CANONICAL_ELEVATION = 23.3;

function samePoseAsDetail(asset) {
  const spec = asset?.wheelSpec;
  if (!spec) return true;
  return Math.abs((spec.azimuth ?? CANONICAL_AZIMUTH) - CANONICAL_AZIMUTH) < 0.5
    && Math.abs((spec.elevation ?? CANONICAL_ELEVATION) - CANONICAL_ELEVATION) < 0.5;
}

/** Bridge the released wheel raster to the canonical poster without another request. */
export function createStagePoster(stage, reduced, mobile) {
  let current;
  function clear() {
    if (!current) return;
    current.animation?.cancel();
    current.revealAnimation?.cancel();
    current.canvas.remove();
    current = null;
  }
  function prepare(id, art, asset = null) {
    clear();
    if (!art) return null;
    const canvas = raster(art.bitmap);
    if (!canvas) return null;
    const sameSource = asset?.wheelSpec?.aspect === 1;
    canvas.className = sameSource ? 'continuity-poster continuity-same-source' : 'continuity-poster';
    canvas.dataset.modelId = id;
    canvas.setAttribute('aria-hidden', 'true');
    const samePose = sameSource || samePoseAsDetail(asset);
    const spec = asset?.wheelSpec;
    // Pre-align legacy 16:9 wheel rasters to the canonical 1:1 detail projection at 0ms.
    // Same-source 1:1 WebP wheels already match #detail-poster pixel-for-pixel via CSS.
    if (!sameSource && spec && !mobile() && stage?.getBoundingClientRect) {
      const rect = stage.getBoundingClientRect();
      const stageSquare = Math.min(rect.width, rect.height);
      const zoom = Number(spec.zoom) || 1;
      const aspect = Number(spec.aspect) || (16 / 9);
      if (stageSquare > 0 && zoom > 0.2) {
        const rawW = (stageSquare / zoom) * aspect;
        const clampedW = Math.max(stageSquare * 0.58, Math.min(stageSquare * 1.6, rawW));
        const clampedH = clampedW / aspect;
        const ox = Array.isArray(spec.offset) ? Number(spec.offset[0]) || 0 : 0;
        const oy = Array.isArray(spec.offset) ? Number(spec.offset[1]) || 0 : 0;
        const shiftX = samePose ? (ox / 1600) * clampedW : 0;
        const shiftY = samePose ? (oy / 900) * clampedH : 0;
        canvas.style.width = `${clampedW}px`;
        canvas.style.transform = `translate(calc(-50% + ${shiftX.toFixed(2)}px), calc(-50% + ${shiftY.toFixed(2)}px))`;
      }
    }
    stage.prepend(canvas);
    if (!sameSource && !reduced() && typeof canvas.animate === 'function') {
      try {
        canvas.animate([{ opacity: .78 }, { opacity: 1 }], { duration: 110, easing: MOTION.easeStandard, id: animationId + 'poster-enter' });
      } catch {}
    }
    current = { id, canvas, samePose, sameSource };
    return current;
  }
  function frame(id) {
    if (current?.id !== id || !current.canvas.isConnected) return null;
    return {
      bitmap: current.canvas, box: current.canvas.getBoundingClientRect(),
      opacity: Number(getComputedStyle(current.canvas).opacity),
    };
  }
  function restore(poster) {
    if (current !== poster) return;
    poster.canvas.className = poster.sameSource ? 'continuity-poster continuity-same-source' : 'continuity-poster';
    poster.canvas.removeAttribute('style');
    stage.prepend(poster.canvas);
  }
  async function reveal(image) {
    const poster = current;
    if (!poster || poster.id !== image.dataset.modelId) return;
    // A canceled navigation animation is not a failed image load.
    if (poster.travel) await Promise.resolve(poster.travel).catch(() => {});
    if (current !== poster) return;
    if (!image.isConnected) { clear(); return; }
    // Motion is optional: reduced-motion, missing WAAPI, or an unavailable
    // layout must still reveal the decoded image and retire the bridge.
    const canAnimate = !reduced() && typeof poster.canvas.animate === 'function' && typeof image.animate === 'function';
    if (poster.sameSource) {
      // Exact 1:1 pixel match between low-res wheel.webp and high-res detail.webp:
      // never move or scale; purely sharpen in place without alpha dip.
      image.style.visibility = 'visible';
      if (canAnimate) {
        try {
          poster.revealAnimation = image.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 110, easing: MOTION.easeStandard, id: animationId + 'poster-in' });
          await poster.revealAnimation.finished.catch(() => {});
        } catch {}
      }
      if (current === poster) clear();
      return;
    }
    if (canAnimate && poster.samePose) {
      const target = imageFrame(image, { includeHidden: true });
      const source = target ? frame(poster.id) : null;
      if (source?.box?.width > 0 && source.box.height > 0) {
        try {
          const end = artLanding(source, target);
          const dx = end.left - source.box.left, dy = end.top - source.box.top;
          const ratio = end.width / source.box.width;
          // Only run a micro-alignment tween when residual framing differs noticeably.
          if (Math.abs(dx) > 2 || Math.abs(dy) > 2 || Math.abs(ratio - 1) > 0.025) {
            const transform = new DOMMatrix(getComputedStyle(poster.canvas).transform);
            const x = transform.e + dx, y = transform.f + dy;
            poster.animation = poster.canvas.animate([
              { transform: `translate(${transform.e}px,${transform.f}px) scale(1)` },
              { transform: `translate(${x}px,${y}px) scale(${ratio})` },
            ], { duration: mobile() ? reducedDuration : 160, easing: fastSettle, fill: 'both', id: animationId + 'poster' });
            await poster.animation.finished.catch(() => {});
          }
        } catch {
          // A presentation-only animation failure must not block model loading.
        }
      }
    }
    if (current !== poster || !image.isConnected) {
      if (current === poster) clear();
      return;
    }
    if (canAnimate) {
      image.style.visibility = 'visible';
      try {
        if (poster.samePose) {
          // Keep the aligned wheel raster solid underneath while HD detail.png fades in on top
          // so silhouette alpha never dips mid-crossfade.
          poster.revealAnimation = image.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 150, easing: MOTION.easeStandard, id: animationId + 'poster-in' });
          await poster.revealAnimation.finished.catch(() => {});
        } else {
          // Different camera elevation (e.g. 40° flat thumbnail → 23.3° stage): smooth cross-dissolve.
          poster.revealAnimation = image.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 220, easing: MOTION.easeStandard, id: animationId + 'poster-in' });
          const outAnim = poster.canvas.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 220, easing: MOTION.easeStandard, fill: 'forwards', id: animationId + 'poster-out' });
          poster.animation = outAnim;
          await Promise.allSettled([poster.revealAnimation.finished, outAnim.finished]);
        }
      } catch {}
      if (current === poster) clear();
      return;
    }
    // Reduced-motion or non-WAAPI fallback: immediate single-paint swap.
    image.style.visibility = 'visible';
    clear();
  }
  return { prepare, frame, restore, reveal, clear };
}

const typography = ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'lineHeight', 'letterSpacing', 'color', 'direction', 'textAlign', 'overflowWrap', 'whiteSpace', 'display', 'webkitBoxOrient', 'webkitLineClamp', 'overflow'];

function titleFrame(node) {
  if (!node) return null;
  const box = node.getBoundingClientRect(), style = getComputedStyle(node);
  if (!box.width || !box.height || !node.offsetWidth || Number(style.opacity) < .01) return null;
  const textStyle = Object.fromEntries(typography.map(key => [key, style[key]]));
  const scale = box.width / node.offsetWidth;
  return { box, textStyle, text: node.textContent, size: parseFloat(style.fontSize) * scale, opacity: Number(style.opacity) };
}

function place(node, box) {
  Object.assign(node.style, {
    left: `${box.left}px`, top: `${box.top}px`,
    width: `${box.width}px`, height: `${box.height}px`,
  });
}

function inverse(from, to, scaleX, scaleY = scaleX) {
  return `translate(${from.left - to.left}px,${from.top - to.top}px) scale(${scaleX},${scaleY})`;
}

// Match the model within the two rasters. Canonical posters and a live capture
// include more transparent padding than a wheel thumbnail.
function modelBox({ bitmap, box }) {
  const probe = document.createElement('canvas');
  probe.width = probe.height = 96;
  const context = probe.getContext('2d', { willReadFrequently: true });
  context.drawImage(bitmap, 0, 0, 96, 96);
  const pixels = context.getImageData(0, 0, 96, 96).data;
  let left = 96, top = 96, right = 0, bottom = 0;
  for (let y = 0; y < 96; y++) {
    for (let x = 0; x < 96; x++) {
      if (pixels[(y * 96 + x) * 4 + 3] < 90) continue;
      left = Math.min(left, x); right = Math.max(right, x + 1);
      top = Math.min(top, y); bottom = Math.max(bottom, y + 1);
    }
  }
  if (right <= left || bottom <= top) return box;
  return {
    left: box.left + box.width * left / 96, top: box.top + box.height * top / 96,
    width: box.width * (right - left) / 96, height: box.height * (bottom - top) / 96,
  };
}

function artLanding(source, target) {
  try {
    const from = modelBox(source), to = modelBox(target);
    const scale = Math.min(to.width / from.width, to.height / from.height);
    return {
      left: to.left + (to.width - from.width * scale) / 2 - (from.left - source.box.left) * scale,
      top: to.top + (to.height - from.height * scale) / 2 - (from.top - source.box.top) * scale,
      width: source.box.width * scale, height: source.box.height * scale,
    };
  } catch {
    // The motion is optional for an image without readable pixels.
    return contain(target.box, source.box.width, source.box.height);
  }
}

/** One visual surface per shared part. The active pane retains its real DOM and controls. */
export function createPhoneContinuity({ main, collection, workspace, wheel, title, reduced, stagePoster }) {
  let current;
  function stop() {
    if (!current) return;
    const { layer, animations, poster, coveredImage } = current;
    current = null;
    for (const animation of animations) animation.cancel();
    if (poster) stagePoster.restore(poster);
    coveredImage?.classList.remove('continuity-covered');
    layer?.remove();
  }
  function capture(id, art, name) {
    const motion = current?.id === id ? current : null;
    const moving = motion?.art;
    const picture = moving?.isConnected ? {
      bitmap: moving, box: moving.getBoundingClientRect(), opacity: Number(getComputedStyle(moving).opacity),
    } : art?.();
    // A traveling node can be removed during a history update. Keep the pixels
    // needed to start the next action at the position it was actually painted.
    const bitmap = picture && raster(picture.bitmap);
    return { id, art: bitmap ? { ...picture, bitmap } : null, title: titleFrame(motion?.title) || titleFrame(name) };
  }
  function fromWheel(id, row) {
    if (!workspace.animate) return { id, art: wheelArtwork(row) };
    const bounds = row?.getBoundingClientRect(), viewport = wheel.getBoundingClientRect();
    const visible = bounds && bounds.bottom > viewport.top && bounds.top < viewport.bottom;
    return capture(id, () => visible ? wheelArtwork(row) : null, !reduced() && visible ? row.querySelector('strong') : null);
  }
  function fromDetail(id, art) {
    return reduced() || !workspace.animate ? { id } : capture(id, art, title);
  }
  function travel(from, { opening, poster, row, staticTitle = false }) {
    stop();
    if (!workspace.animate) return;
    const motion = { id: from.id, animations: [] };
    current = motion;
    const still = reduced();
    const fixedTitle = opening && staticTitle;
    const duration = still ? reducedDuration : (opening ? enterDuration : returnDuration);
    function animate(element, name, frames, easing = 'linear') {
      const animation = element.animate(frames, { duration, easing, fill: 'both', id: animationId + 'pane-' + name });
      motion.animations.push(animation);
      return animation;
    }
    function layer() {
      if (!motion.layer) {
        motion.layer = document.createElement('div');
        motion.layer.className = 'continuity-pane';
        motion.layer.setAttribute('aria-hidden', 'true');
        motion.layer.inert = true;
        motion.layer.style.setProperty('--continuity-pane-top', `${Math.max(0, main.getBoundingClientRect().top)}px`);
        document.body.append(motion.layer);
      }
      return motion.layer;
    }
    if (still) animate(opening ? workspace : collection, 'fade', [{ opacity: .35 }, { opacity: 1 }], 'ease-out');
    else {
      const targetTitle = opening ? title : row?.querySelector('strong');
      // Measure the settled title when the restored wheel is revealing its centre.
      if (!opening && row?.dataset.nameVisible === 'true') {
        for (const animation of targetTitle.getAnimations()) animation.cancel();
      }
      const endTitle = fixedTitle ? null : titleFrame(targetTitle);
      if (from.title && endTitle && from.title.text === endTitle.text) {
        const name = document.createElement('div');
        name.className = 'continuity-title';
        name.textContent = endTitle.text;
        Object.assign(name.style, endTitle.textStyle);
        place(name, endTitle.box);
        layer().append(name);
        motion.title = name;
        animate(targetTitle, 'cover', [{ opacity: 0 }, { opacity: 0 }]);
        animate(name, 'title', [
          { transform: inverse(from.title.box, endTitle.box, from.title.size / endTitle.size), color: from.title.textStyle.color, opacity: from.title.opacity },
          { transform: 'none', color: endTitle.textStyle.color, opacity: endTitle.opacity },
        ], fastSettle);
      }
      const endArt = opening ? (poster && stagePoster.frame(from.id)) : wheelArtwork(row);
      if (from.art && endArt) {
        const art = opening ? poster.canvas : raster(from.art.bitmap);
        const end = opening ? endArt.box : artLanding(from.art, endArt);
        art.className = 'continuity-art';
        place(art, end);
        layer().append(art);
        motion.art = art;
        animate(art, 'art', [
          { transform: inverse(from.art.box, end, from.art.box.width / end.width, from.art.box.height / end.height) },
          { transform: 'none' },
        ], fastSettle);
        const endOpacity = opening ? 1 : Number(getComputedStyle(row.querySelector('.slot-image')).opacity);
        animate(art, 'alpha', [{ opacity: from.art.opacity }, { opacity: endOpacity }], fastSettle);
        if (opening) {
          motion.poster = poster;
        } else {
          motion.coveredImage = row.querySelector('img');
          motion.coveredImage.classList.add('continuity-covered');
        }
      }
      const pane = opening ? workspace : collection;
      const selectors = opening
        ? ['#subtitle', '#excluded', '.info-region', '.workspace-bottom', '#mobile-back', '#mobile-stepper', '#mobile-interact']
        : ['.searchbar', '.summary', '#empty-state'];
      const entries = selectors.map(selector => pane.querySelector(selector)).filter(node => node && !node.hidden);
      if (opening && !motion.title && !fixedTitle) entries.push(title);
      const lift = opening ? 8 : 5;
      for (const entry of entries) {
        animate(entry, 'arrival', [
          { opacity: 0, transform: `translateY(${lift}px)` },
          { opacity: 0, transform: `translateY(${lift}px)`, offset: .36, easing: MOTION.easeStandard },
          { opacity: 1, transform: 'none' },
        ]);
      }
    }
    const finished = Promise.allSettled(motion.animations.map(animation => animation.finished)).then(() => {
      if (current === motion) stop();
    });
    if (motion.poster) motion.poster.travel = finished;
  }
  return { fromWheel, fromDetail, travel, stop };
}

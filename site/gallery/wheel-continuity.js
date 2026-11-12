function visibleRows(rows, viewport) {
  const visible = new Map();
  for (const row of rows) {
    const surface = row.querySelector('.slot-motion');
    const box = surface.getBoundingClientRect();
    if (box.bottom <= viewport.top || box.top >= viewport.bottom) continue;
    const opacity = Number(getComputedStyle(surface).opacity);
    if (opacity < .01) continue;
    const image = surface.querySelector('.slot-image');
    const imageStyle = getComputedStyle(image);
    visible.set(row.dataset.id, {
      row, surface, box, opacity, image, imageOpacity: imageStyle.opacity, imageTransform: imageStyle.transform,
    });
  }
  return visible;
}

function departingRow(frame, viewport) {
  const row = frame.row.cloneNode(false);
  row.removeAttribute('id');
  row.removeAttribute('role');
  Object.assign(row.style, { top: `${frame.box.top - viewport.top}px`, height: `${frame.box.height}px` });
  const surface = frame.surface.cloneNode(false);
  const image = frame.image.cloneNode(false);
  Object.assign(image.style, { opacity: frame.imageOpacity, transform: frame.imageTransform });
  if (frame.bitmap) {
    const { original, width, height, opacity, transform } = frame.bitmap;
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    canvas.getContext('2d').drawImage(original, 0, 0);
    Object.assign(canvas.style, { opacity, transform });
    image.append(canvas);
  } else if (frame.placeholder) image.append(frame.placeholder);
  row.setAttribute('aria-selected', frame.selected);
  surface.append(frame.marker, image, frame.copy);
  row.append(surface);
  return { row, surface };
}

/** Layout, focus, and hit targets settle immediately. Only the wheel's visual surfaces move. */
export function createWheelContinuity({ wheel, slots, reduced, mobile, onFinish }) {
  const animations = new Set();
  const moving = new Set();
  let exits;
  function stop() {
    for (const animation of animations) animation.cancel();
    animations.clear();
    for (const surface of moving) delete surface.dataset.continuityMoving;
    moving.clear();
    exits?.remove();
    exits = null;
  }
  function animate(element, name, frames, options, done) {
    const animation = element.animate(frames, { ...options, id: 'gallery-continuity-wheel-' + name });
    animations.add(animation);
    if (name === 'move') {
      moving.add(element);
      element.dataset.continuityMoving = 'true';
    }
    animation.addEventListener('finish', () => {
      if (!animations.delete(animation)) return;
      animation.cancel();
      if (moving.delete(element)) delete element.dataset.continuityMoving;
      done?.();
      if (!animations.size) {
        exits?.remove();
        exits = null;
        onFinish();
      }
    }, { once: true });
  }
  function update(change, { keyboard = false } = {}) {
    if (!wheel.clientHeight || !wheel.animate) {
      stop();
      change();
      return;
    }
    const viewport = wheel.getBoundingClientRect();
    const previous = visibleRows([...(exits?.children || []), ...slots.children], viewport);
    // Snapshot the copy before the existing renderer can change its text or state.
    for (const frame of previous.values()) {
      frame.copy = frame.surface.querySelector('.slot-copy').cloneNode(true);
      frame.marker = frame.surface.querySelector('.slot-marker').cloneNode(true);
      frame.selected = frame.row.getAttribute('aria-selected');
      const name = frame.surface.querySelector('strong');
      const style = getComputedStyle(name);
      Object.assign(frame.copy.querySelector('strong').style, {
        transition: 'none', maxHeight: style.maxHeight, marginBottom: style.marginBottom,
        opacity: style.opacity, transform: style.transform,
      });
      const canvas = frame.image.querySelector('canvas');
      const original = canvas && Number(getComputedStyle(canvas).opacity) > .5 ? canvas : frame.image.querySelector('img[data-thumbnail-state=ready]');
      if (original && (original.naturalWidth || original.width)) {
        const style = getComputedStyle(original);
        frame.bitmap = {
          original, width: original.naturalWidth || original.width, height: original.naturalHeight || original.height,
          opacity: style.opacity, transform: style.transform,
        };
      }
      const placeholder = frame.image.querySelector('.thumbnail-placeholder');
      if (!frame.bitmap && placeholder && getComputedStyle(placeholder).visibility === 'visible') {
        frame.placeholder = placeholder.cloneNode(true);
        Object.assign(frame.placeholder.style, { visibility: 'visible', opacity: getComputedStyle(placeholder).opacity });
      }
    }
    stop();
    change();
    const destination = wheel.getBoundingClientRect();
    const next = visibleRows(slots.children, destination);
    const still = reduced();
    const duration = still ? 150 : mobile() ? (keyboard ? 240 : 300) : (keyboard ? 160 : 200);
    const options = { duration, easing: 'ease-in-out', fill: 'both' };
    for (const [id, frame] of next) {
      const old = previous.get(id);
      const y = old ? old.box.top - frame.box.top : 0;
      if (!old) {
        const frames = still ? [{ opacity: 0 }, { opacity: 1 }] : [{ opacity: 0 }, { opacity: 0, offset: .5, easing: 'ease-out' }, { opacity: 1 }];
        animate(frame.surface, 'enter', frames, { ...options, easing: 'linear' });
        continue;
      }
      if (!still && Math.abs(y) > .5) {
        animate(frame.surface, 'move', [{ transform: `translateY(${y}px)`, opacity: old.opacity }, { transform: 'none', opacity: 1 }], options);
      } else if (old.opacity < 1 || (still && Math.abs(y) > .5)) {
        animate(frame.surface, 'enter', [{ opacity: Math.min(old.opacity, still ? .65 : 1) }, { opacity: 1 }], options);
      }
      if (!still && (old.imageTransform !== frame.imageTransform || old.imageOpacity !== frame.imageOpacity)) {
        animate(frame.image, 'image', [
          { transform: old.imageTransform, opacity: old.imageOpacity },
          { transform: frame.imageTransform, opacity: frame.imageOpacity },
        ], options);
      }
    }
    for (const [id, frame] of previous) {
      if (next.has(id)) continue;
      if (!exits) {
        exits = document.createElement('div');
        exits.className = 'wheel-continuity-exits';
        exits.inert = true;
        exits.setAttribute('aria-hidden', 'true');
        wheel.after(exits);
      }
      const ghost = departingRow(frame, destination);
      exits.append(ghost.row);
      animate(ghost.surface, 'exit', [{ opacity: frame.opacity }, { opacity: 0 }], {
        duration: still ? 150 : Math.round(duration * .32), easing: 'ease-out', fill: 'both',
      }, () => ghost.row.remove());
    }
  }
  return { update, stop, get active() { return animations.size > 0; } };
}

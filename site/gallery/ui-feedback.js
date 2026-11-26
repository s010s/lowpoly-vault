// Logical open state is separate from hidden so an exit can reverse in place.
import { formatAttribution, showCopyFallback, clearCopyFallback } from '../shared-ui.js';
import { MOTION, animateOneShot, cancelOneShot, lockButtonWidth, swapIconSmooth } from '../motion-system.js';
import { iconMarkup } from './icons.js';
import { detailHref } from './catalog-source.js';

export function createPopover(panel, trigger, { backdrop = null, enter = 200, exit = 140, reduced = () => false, schedule = setTimeout, cancel = clearTimeout, beforeEnter = () => {} } = {}) {
  let open = false, timer = 0, version = 0;
  panel.classList.add('ui-popover');
  panel.dataset.open = 'false';
  panel.inert = true;
  if (backdrop) {
    backdrop.dataset.open = 'false';
    backdrop.dataset.motion = 'false';
  }
  const clear = () => { cancel(timer); timer = 0; };
  const mode = animate => animate ? (reduced() ? 'reduced' : 'true') : 'false';
  function set(next, { animate = false } = {}) {
    if (open === next) {
      if (!next && !animate) {
        clear();
        panel.hidden = true;
        if (backdrop) { backdrop.dataset.motion = 'false'; backdrop.dataset.open = 'false'; backdrop.hidden = true; }
      }
      return;
    }
    open = next;
    clear();
    const owner = ++version, motion = mode(animate), duration = motion === 'reduced' ? 100 : (motion === 'true' ? (next ? enter : exit) : 0);
    panel.dataset.motion = motion;
    panel.style.setProperty('--ui-duration', duration + 'ms');
    if (backdrop) {
      backdrop.dataset.motion = motion;
      backdrop.style.setProperty('--ui-duration', duration + 'ms');
    }
    trigger?.setAttribute('aria-expanded', String(next));
    panel.inert = !next;
    panel.setAttribute('aria-hidden', String(!next));
    if (next) {
      const wasHidden = panel.hidden;
      panel.hidden = false;
      if (backdrop) {
        backdrop.hidden = false;
        backdrop.dataset.open = 'false';
      }
      beforeEnter();
      if (trigger && (wasHidden || !panel.style.transformOrigin)) {
        const p = panel.getBoundingClientRect(), t = trigger.getBoundingClientRect();
        panel.style.transformOrigin = `${Math.max(0, Math.min(p.width, t.left + t.width / 2 - p.left))}px ${Math.max(0, Math.min(p.height, t.top + t.height / 2 - p.top))}px`;
      }
      if (wasHidden && duration) panel.getBoundingClientRect();
      panel.dataset.open = 'true';
      if (backdrop) backdrop.dataset.open = 'true';
    } else {
      panel.dataset.open = 'false';
      if (backdrop) backdrop.dataset.open = 'false';
      if (duration) timer = schedule(() => {
        if (owner === version && !open) {
          panel.hidden = true;
          if (backdrop) backdrop.hidden = true;
        }
        timer = 0;
      }, duration);
      else {
        panel.hidden = true;
        if (backdrop) backdrop.hidden = true;
      }
    }
  }
  return {
    get open() { return open; },
    show: options => set(true, options),
    hide: options => set(false, options),
    settle() {
      clear();
      panel.dataset.motion = 'false';
      panel.hidden = !open;
      if (backdrop) { backdrop.dataset.motion = 'false'; backdrop.dataset.open = String(open); backdrop.hidden = !open; }
    },
    dispose() { clear(); version++; },
  };
}

export function overflowRemaining(element) { return element.scrollHeight - element.clientHeight - element.scrollTop > 2; }
export function shouldAnimateBoundary(previousCount, nextCount, deliberate) { return !!deliberate && ((previousCount === 0) !== (nextCount === 0)); }

// All dimensions are layout-viewport CSS pixels, including visualViewport offsets.
// The panel may overlap its trigger when the keyboard leaves very little room,
// but it must never put its close control or scrolling viewport off screen.
export function fitInfoPanel({ viewport, anchor, safe = {}, preferredHeight = 360, maxWidth = 340, gutter = 12, gap = 8 }) {
  const leftBound = (viewport.left || 0) + (safe.left || 0) + gutter;
  const topBound = (viewport.top || 0) + (safe.top || 0) + gutter;
  const rightBound = (viewport.left || 0) + viewport.width - (safe.right || 0) - gutter;
  const bottomBound = (viewport.top || 0) + viewport.height - (safe.bottom || 0) - gutter;
  const width = Math.max(1, Math.min(maxWidth, rightBound - leftBound));
  const height = Math.max(1, Math.min(preferredHeight, bottomBound - topBound));
  const left = Math.min(Math.max(anchor.left + anchor.width / 2 - width / 2, leftBound), Math.max(leftBound, rightBound - width));
  const below = bottomBound - anchor.bottom - gap, above = anchor.top - gap - topBound;
  const minimum = Math.min(180, height);
  let top, maxHeight, placement;
  if (below >= minimum) { maxHeight = Math.min(height, below); top = anchor.bottom + gap; placement = 'below'; }
  else if (above >= minimum) { maxHeight = Math.min(height, above); top = anchor.top - gap - maxHeight; placement = 'above'; }
  else { maxHeight = height; top = Math.min(Math.max(anchor.bottom + gap, topBound), Math.max(topBound, bottomBound - maxHeight)); placement = 'clamped'; }
  top = Math.min(Math.max(top, topBound), Math.max(topBound, bottomBound - maxHeight));
  return { left, top, width, maxHeight, placement, availableHeight: Math.max(1, bottomBound - topBound) };
}

export function createUIFeedback({ t, reduced, getSelection }) {
  const root = document.documentElement, abort = new AbortController(), timers = new Set(), reveals = new Map(), chipNodes = new Map();
  let input = 'keyboard', copyVersion = 0, copyTimer = 0, copyState = 'idle', shareVersion = 0, shareTimer = 0, disposed = false;
  const later = (fn, ms) => { const id = setTimeout(() => { timers.delete(id); fn(); }, ms); timers.add(id); return id; };
  const clear = id => { clearTimeout(id); timers.delete(id); };
  const listen = (target, type, fn, options = {}) => target.addEventListener(type, fn, { ...options, signal: abort.signal });
  const pointer = event => !!event && (event.type?.startsWith('pointer') || (event.type === 'click' && event.detail > 0));
  listen(document, 'pointerdown', () => { input = 'pointer'; root.dataset.uiInput = input; }, { capture: true });
  listen(document, 'keydown', () => { input = 'keyboard'; root.dataset.uiInput = input; }, { capture: true });
  root.dataset.uiInput = input;

  const filterPanel = document.querySelector('#filter-panel'), filterForm = document.querySelector('#filter-form');
  function updateFilterOverflow() { filterPanel.dataset.more = String(!filterPanel.hidden && overflowRemaining(filterForm)); }
  function fitFilterPanel() {
    const visual = window.visualViewport, viewportBottom = (visual?.offsetTop || 0) + (visual?.height || window.innerHeight || root.clientHeight || 768);
    const top = (filterPanel.offsetParent?.getBoundingClientRect().top || 0) + (filterPanel.offsetTop || 0);
    filterPanel.style.setProperty('--filter-room', Math.max(0, viewportBottom - top) + 'px');
    updateFilterOverflow();
  }
  const filter = createPopover(filterPanel, document.querySelector('#filters'), { backdrop: document.querySelector('#filter-backdrop'), reduced, schedule: later, cancel: clear, beforeEnter: fitFilterPanel });
  const morePanel = document.querySelector('#download-menu'), moreTrigger = document.querySelector('#more-actions');
  const more = morePanel ? createPopover(morePanel, moreTrigger, { backdrop: document.querySelector('#more-backdrop'), enter: 160, exit: 110, reduced, schedule: later, cancel: clear }) : { open: false, show() {}, hide() {}, settle() {}, dispose() {} };

  const infoPanel = document.querySelector('#info-panel'), infoContent = document.querySelector('#info-content'), infoTrigger = document.querySelector('#info');
  let safeProbe = null;
  function safeInsets() {
    if (typeof window.getComputedStyle !== 'function') return {};
    if (!safeProbe) {
      safeProbe = document.createElement('div');
      safeProbe.className = 'info-safe-area-probe';
      safeProbe.setAttribute('aria-hidden', 'true');
      safeProbe.inert = true;
      document.body.append(safeProbe);
    }
    const style = window.getComputedStyle(safeProbe);
    return { top: parseFloat(style.paddingTop) || 0, right: parseFloat(style.paddingRight) || 0, bottom: parseFloat(style.paddingBottom) || 0, left: parseFloat(style.paddingLeft) || 0 };
  }
  function positionInfo() {
    if (infoPanel.hidden) return;
    const visual = window.visualViewport;
    const viewport = { left: visual?.offsetLeft || 0, top: visual?.offsetTop || 0, width: visual?.width || window.innerWidth || document.documentElement.clientWidth || 1024, height: visual?.height || window.innerHeight || document.documentElement.clientHeight || 768 };
    const anchor = infoTrigger.getBoundingClientRect(), safe = safeInsets();
    const initial = fitInfoPanel({ viewport, anchor, safe });
    infoPanel.style.width = initial.width + 'px';
    infoPanel.style.setProperty('--info-max-height', initial.availableHeight + 'px');
    const measured = Math.min(360, infoPanel.offsetHeight || 360);
    const fitted = fitInfoPanel({ viewport, anchor, safe, preferredHeight: measured });
    infoPanel.style.left = fitted.left + 'px';
    infoPanel.style.top = fitted.top + 'px';
    infoPanel.style.setProperty('--info-max-height', fitted.maxHeight + 'px');
    infoPanel.dataset.placement = fitted.placement;
  }
  const info = createPopover(infoPanel, infoTrigger, { backdrop: document.querySelector('#info-backdrop'), enter: 160, exit: 120, reduced, schedule: later, cancel: clear, beforeEnter: positionInfo });

  function updateOverflow() { infoPanel.dataset.more = String(info.open && overflowRemaining(infoContent)); }
  function refreshInfoViewport() { if (info.open) positionInfo(); updateOverflow(); }
  function refreshPanelsViewport() { if (filter.open) fitFilterPanel(); refreshInfoViewport(); }
  listen(filterForm, 'scroll', updateFilterOverflow, { passive: true });
  listen(infoContent, 'scroll', updateOverflow, { passive: true });
  listen(window, 'resize', refreshPanelsViewport, { passive: true });
  listen(window, 'scroll', refreshPanelsViewport, { passive: true });
  if (window.visualViewport) {
    listen(window.visualViewport, 'resize', refreshPanelsViewport, { passive: true });
    listen(window.visualViewport, 'scroll', refreshPanelsViewport, { passive: true });
  }
  const resize = typeof ResizeObserver === 'function' ? new ResizeObserver(() => { updateFilterOverflow(); updateOverflow(); }) : null;
  resize?.observe(filterForm);
  resize?.observe(infoContent);
  resize?.observe(infoPanel);
  const mutation = typeof MutationObserver === 'function' ? new MutationObserver(refreshInfoViewport) : null;
  mutation?.observe(infoContent, { childList: true, subtree: true, characterData: true });

  function reveal(node, { animate = false, duration = 160, remove = false, onDone = null } = {}) {
    const prior = reveals.get(node);
    if (prior) { clear(prior); reveals.delete(node); }
    const motion = animate ? (reduced() ? 'reduced' : 'true') : 'false';
    node.classList.add('ui-reveal');
    node.dataset.motion = motion;
    node.style.setProperty('--ui-duration', (motion === 'reduced' ? 100 : duration) + 'ms');
    const ms = motion === 'false' ? 0 : motion === 'reduced' ? 100 : duration;
    if (remove) { node.dataset.visible = 'false'; node.inert = true; node.setAttribute('aria-hidden', 'true'); }
    else {
      const wasLeaving = node.dataset.visible === 'false';
      node.inert = false;
      node.removeAttribute('aria-hidden');
      if (!wasLeaving && ms) { node.dataset.visible = 'false'; node.getBoundingClientRect(); }
      node.dataset.visible = 'true';
    }
    if (!ms) { if (remove) node.remove(); onDone?.(); return; }
    reveals.set(node, later(() => {
      reveals.delete(node);
      if (remove) node.remove();
      else { node.classList.remove('ui-reveal'); delete node.dataset.visible; }
      onDone?.();
    }, ms));
  }

  const chips = document.querySelector('#chips');
  let chipsHeightTimer = 0;
  function clearChipFloatStyles(node) {
    node.style.removeProperty('position');
    node.style.removeProperty('left');
    node.style.removeProperty('top');
    node.style.removeProperty('pointer-events');
  }
  function renderChips(items, { animate = false, onRemove, onMore, onClearAll } = {}) {
    const visible = items.slice(0, 3).map(item => ({ ...item, key: item.group + ':' + item.id }));
    if (items.length > 3) visible.push({ key: 'more', label: '+' + (items.length - 3), more: true });
    if (items.length >= 2 && onClearAll) visible.push({ key: 'clear-all', label: t('Clear', '清除'), clearAll: true });
    const keys = new Set(visible.map(item => item.key)), focused = document.activeElement;
    const removedFocus = [...chipNodes].some(([key, node]) => !keys.has(key) && node === focused);
    const shouldFlip = animate && !reduced();
    // Batch-read all resting rects before any DOM mutation (cancel in-flight FLIP first).
    const beforeRects = new Map();
    let containerRect = null;
    if (shouldFlip && chipNodes.size) {
      for (const node of chipNodes.values()) cancelOneShot(node, 'chip-flip');
      if (typeof chips.getBoundingClientRect === 'function') containerRect = chips.getBoundingClientRect();
      for (const [key, node] of chipNodes) {
        if (node.isConnected && !node.inert && typeof node.getBoundingClientRect === 'function') {
          const r = node.getBoundingClientRect();
          if (r.width > 0) beforeRects.set(key, { left: r.left, top: r.top });
        }
      }
    }
    visible.forEach((item, index) => {
      let node = chipNodes.get(item.key);
      const added = !node;
      if (!node) {
        node = document.createElement('button');
        node.type = 'button';
        node.dataset.chipKey = item.key;
        if (item.clearAll) node.className = 'chip-clear-all';
        chipNodes.set(item.key, node);
      } else {
        // Always restore flow positioning when reviving a chip mid-exit.
        clearChipFloatStyles(node);
      }
      node.textContent = item.more || item.clearAll ? item.label : `${item.label} ×`;
      node.title = item.clearAll ? t('Clear all filters', '清除全部筛选') : item.more ? t('More filters', '更多筛选') : t('Remove ', '移除 ') + item.label;
      node.onclick = event => item.clearAll ? onClearAll(event) : item.more ? onMore(event) : onRemove(item, event);
      const at = [...chips.children].filter(child => keys.has(child.dataset.chipKey))[index];
      if (at !== node) chips.insertBefore(node, at || null);
      if (added || node.inert) reveal(node, { animate, duration: 160 });
    });
    let removedAny = false;
    // Float leaving chips only while at least one sibling remains in flow (prevents collapse to 0px).
    const canFloatLeaving = shouldFlip && visible.length > 0 && containerRect && containerRect.width > 0;
    for (const [key, node] of chipNodes) if (!keys.has(key)) {
      removedAny = true;
      if (!animate) {
        const prior = reveals.get(node);
        if (prior) { clear(prior); reveals.delete(node); }
        clearChipFloatStyles(node);
        node.remove();
        chipNodes.delete(key);
      } else if (!node.inert) {
        if (canFloatLeaving) {
          const before = beforeRects.get(key);
          if (before) {
            if (!chips.style.position) chips.style.position = 'relative';
            node.style.position = 'absolute';
            node.style.left = `${before.left - containerRect.left}px`;
            node.style.top = `${before.top - containerRect.top}px`;
            node.style.pointerEvents = 'none';
          }
        }
        reveal(node, {
          animate,
          duration: 120,
          remove: true,
          onDone: () => {
            clearChipFloatStyles(node);
            if (!node.isConnected && chipNodes.get(key) === node) chipNodes.delete(key);
          },
        });
      }
    }
    if (canFloatLeaving && removedAny && beforeRects.size) {
      const afterContainerHeight = typeof chips.getBoundingClientRect === 'function' ? chips.getBoundingClientRect().height : 0;
      if (containerRect.height > afterContainerHeight + 2) {
        chips.style.minHeight = `${Math.ceil(containerRect.height)}px`;
        clear(chipsHeightTimer);
        chipsHeightTimer = later(() => { chips.style.removeProperty('min-height'); chipsHeightTimer = 0; }, 130);
      }
      for (const [key, before] of beforeRects) {
        if (!keys.has(key)) continue;
        const node = chipNodes.get(key);
        if (!node || !node.isConnected || node.inert) continue;
        const after = node.getBoundingClientRect();
        const dx = before.left - after.left, dy = before.top - after.top;
        if (Math.abs(dx) > 0.5 || Math.abs(dy) > 0.5) {
          animateOneShot(node, 'chip-flip', [
            { transform: `translate(${dx}px, ${dy}px)` },
            { transform: 'none' },
          ], { duration: MOTION.fast, easing: MOTION.easeStandard });
        }
      }
    } else if (!visible.length) {
      clear(chipsHeightTimer);
      chipsHeightTimer = 0;
      chips.style.removeProperty('min-height');
    }
    if (removedFocus) ([...chips.children].find(node => !node.inert) || document.querySelector('#filters')).focus({ preventScroll: true });
  }

  const credits = document.querySelector('#credits'), copyText = credits.querySelector('[data-en]'), status = document.querySelector('#copy-status');
  const shareBtn = document.querySelector('#share-link'), shareLabel = shareBtn?.querySelector('[data-en]');
  const creditsAnchor = () => credits.closest?.('.download-menu') || credits.closest?.('.download-card') || credits;
  const shareAnchor = () => shareBtn?.closest?.('.download-menu') || shareBtn?.closest?.('.download-card') || shareBtn;
  let releaseCreditsWidth = null, releaseShareWidth = null;

  function setButtonIcon(button, name, animate = false) {
    const host = button?.querySelector?.('.icon');
    if (!host) return;
    if (animate) swapIconSmooth(host, iconMarkup(name), { reduced: reduced() });
    else host.innerHTML = iconMarkup(name);
  }

  function resetShare() {
    shareVersion++;
    clear(shareTimer);
    shareTimer = 0;
    releaseShareWidth?.();
    releaseShareWidth = null;
    if (!shareBtn || !shareLabel) return;
    const wasSuccess = shareBtn.dataset.copyState === 'success';
    shareBtn.dataset.copyState = 'idle';
    shareBtn.removeAttribute('aria-busy');
    shareLabel.textContent = shareLabel.dataset[root.lang === 'zh-CN' ? 'zh' : 'en'];
    setButtonIcon(shareBtn, 'link', wasSuccess);
    clearCopyFallback(shareAnchor(), 'share-link');
  }

  function resetCopy() {
    copyVersion++;
    clear(copyTimer);
    copyTimer = 0;
    releaseCreditsWidth?.();
    releaseCreditsWidth = null;
    const wasSuccess = copyState === 'success';
    copyState = 'idle';
    credits.dataset.copyState = 'idle';
    credits.removeAttribute('aria-busy');
    copyText.textContent = copyText.dataset[root.lang === 'zh-CN' ? 'zh' : 'en'];
    setButtonIcon(credits, 'copy', wasSuccess);
    status.textContent = '';
    clearCopyFallback(creditsAnchor(), 'credits');
    resetShare();
  }

  async function copyAttribution(asset, event) {
    resetCopy();
    const owner = ++copyVersion, selection = getSelection(), language = root.lang;
    const langCode = language === 'zh-CN' ? 'zh' : 'en';
    copyState = 'pending';
    credits.dataset.copyState = 'pending';
    credits.setAttribute('aria-busy', 'true');
    const canonicalUrl = new URL(detailHref(asset.id, langCode), location.origin).href;
    const text = formatAttribution(asset, langCode, canonicalUrl);
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard is unavailable');
      await navigator.clipboard.writeText(text);
      if (disposed || owner !== copyVersion || selection !== getSelection() || language !== root.lang) return;
      releaseCreditsWidth = lockButtonWidth(credits);
      copyState = 'success';
      credits.dataset.copyState = 'success';
      credits.removeAttribute('aria-busy');
      copyText.textContent = t('Copied', '已复制');
      setButtonIcon(credits, 'check', true);
      status.textContent = t('Attribution copied', '署名已复制');
      copyTimer = later(() => { if (owner === copyVersion) resetCopy(); }, 2000);
    } catch {
      if (disposed || owner !== copyVersion || selection !== getSelection() || language !== root.lang) return;
      copyState = 'error';
      credits.dataset.copyState = 'error';
      credits.removeAttribute('aria-busy');
      copyText.textContent = t('Copy manually', '请手动复制');
      status.textContent = t('Clipboard blocked. Select and copy the attribution below.', '无法自动复制，请从下方输入框手动复制署名。');
      showCopyFallback(creditsAnchor(), text, langCode, { key: 'credits', focusTarget: credits });
      copyTimer = later(() => { if (owner === copyVersion) { copyState = 'idle'; credits.dataset.copyState = 'idle'; copyText.textContent = copyText.dataset[root.lang === 'zh-CN' ? 'zh' : 'en']; } }, 3500);
    }
  }

  async function copyShareLink(asset, event) {
    if (!shareBtn || !shareLabel || !asset) return;
    resetShare();
    const owner = ++shareVersion, selection = getSelection(), language = root.lang;
    const langCode = language === 'zh-CN' ? 'zh' : 'en';
    shareBtn.dataset.copyState = 'pending';
    shareBtn.setAttribute('aria-busy', 'true');
    const url = new URL(detailHref(asset.id, langCode), location.origin).href;
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard is unavailable');
      await navigator.clipboard.writeText(url);
      if (disposed || owner !== shareVersion || selection !== getSelection() || language !== root.lang) return;
      releaseShareWidth = lockButtonWidth(shareBtn);
      shareBtn.dataset.copyState = 'success';
      shareBtn.removeAttribute('aria-busy');
      shareLabel.textContent = t('Copied', '已复制');
      setButtonIcon(shareBtn, 'check', true);
      status.textContent = t('Model link copied', '模型链接已复制');
      shareTimer = later(() => { if (owner === shareVersion) resetShare(); }, 2000);
    } catch {
      if (disposed || owner !== shareVersion || selection !== getSelection() || language !== root.lang) return;
      shareBtn.dataset.copyState = 'error';
      shareBtn.removeAttribute('aria-busy');
      shareLabel.textContent = t('Copy manually', '请手动复制');
      status.textContent = t('Clipboard blocked. Copy the link below.', '无法自动复制，请复制下方链接。');
      showCopyFallback(shareAnchor(), url, langCode, { key: 'share-link', focusTarget: shareBtn });
      shareTimer = later(() => { if (owner === shareVersion) { shareBtn.dataset.copyState = 'idle'; shareLabel.textContent = shareLabel.dataset[root.lang === 'zh-CN' ? 'zh' : 'en']; } }, 3500);
    }
  }

  // Native anchors retain their default navigation/download; feedback never waits.
  const downloads = [...document.querySelectorAll('.download-actions a')];
  downloads.forEach(link => {
    listen(link, 'pointerdown', event => { if (event.isPrimary !== false && event.button === 0) link.dataset.pressed = 'true'; });
    listen(link, 'pointerleave', () => { link.dataset.pressed = 'false'; });
  });
  const release = () => downloads.forEach(link => { link.dataset.pressed = 'false'; });
  listen(window, 'pointerup', release, { passive: true });
  listen(window, 'pointercancel', release, { passive: true });
  listen(window, 'blur', release);

  const media = matchMedia('(prefers-reduced-motion: reduce)');
  listen(media, 'change', () => {
    filter.settle();
    info.settle();
    more.settle();
    release();
    for (const [node, id] of reveals) {
      clear(id);
      if (node.inert) {
        const chipKey = node.dataset?.chipKey;
        if (chipKey && chipNodes.get(chipKey) === node) chipNodes.delete(chipKey);
        clearChipFloatStyles(node);
        node.remove();
      }
      else { node.classList.remove('ui-reveal'); delete node.dataset.visible; }
    }
    chips.style.removeProperty('min-height');
    reveals.clear();
    updateOverflow();
  });

  return {
    filter, info, more, pointer,
    get pointerInput() { return input === 'pointer'; },
    get copyState() { return copyState; },
    renderChips, reveal, resetCopy, resetShare, copyAttribution, copyShareLink, updateOverflow, updateFilterOverflow,
    dispose() {
      if (disposed) return;
      disposed = true;
      abort.abort();
      resize?.disconnect();
      mutation?.disconnect();
      safeProbe?.remove();
      filter.dispose();
      info.dispose();
      more.dispose();
      resetCopy();
      for (const timer of timers) clearTimeout(timer);
      timers.clear();
      reveals.clear();
    },
  };
}

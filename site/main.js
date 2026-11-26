import { releaseCatalogPath } from './release-catalog-path.js';
import { downloadModelZip } from './client-zip.js';
import { CatalogStore } from './catalog.js';
import { initTheme } from './theme.js';
import { words } from './words.js';
import { routeHref, parseRoute } from './routes.js';
import {
  HOME_FEATURED_SPECS, categoryLabel, formatBytes, formatAttribution,
  getStoredLang, setStoredLang, getStoredWireframe, setStoredWireframe,
  showCopyFallback, clearCopyFallback, renderNoticesMarkdown,
} from './shared-ui.js';
import { primaryDimension, dimensionDetails, dimensionNote, comparisonText } from './gallery/model-dimensions.js';
import { modelShortName } from './gallery/presentation-labels.js';
import { iconMarkup } from './gallery/icons.js';
import {
  MOTION, prefersReducedMotion, installResizeMotionGuard, animateOneShot, animatePresence,
  lockButtonWidth, swapIconSmooth, createDiscreteCameraStepper,
} from './motion-system.js';
import './style.css';

const $ = selector => document.querySelector(selector);
const siteRoot = new URL(import.meta.env.BASE_URL, location.origin).pathname;
const initialRoute = parseRoute(location.pathname, siteRoot);

// Honor explicit stored Chinese preference when revisiting bare root with no explicit query.
const redirectingToZh = (
  initialRoute.type === 'home' &&
  initialRoute.lang === 'en' &&
  !location.search &&
  getStoredLang() === 'zh'
);
if (redirectingToZh) {
  location.replace(routeHref({ type: 'home', lang: 'zh-CN' }, siteRoot));
}

let lang = initialRoute.lang === 'zh-CN' ? 'zh' : 'en';
const t = key => words[lang][key] || key;
const loc = value => typeof value === 'object' && value ? (value[lang] || value.en || '') : value || '';
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const href = (type, id, options = {}) => routeHref({ type, id, lang, ...options }, siteRoot);
const plainClick = event => event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey;
const store = new CatalogStore({ baseURL: new URL(siteRoot, location.origin).href });
const path = p => store.resolvePath(p);
initTheme();
installResizeMotionGuard();

let index = null;
let currentView = 'home';
let selected = null;
let requestedDetailId = null;
let detailVersion = 0;
let detailRenderer = null;
let detailReady = false;
let detailIntegrityBlocked = false;
let detailCompareLoading = false;
let detailCompareError = false;
let detailCompareKind = null;
let detailNeighbors = { prev: null, next: null, related: [] };
let detailZipController = null;
let detailZipVersion = 0;
let detailSkeletonTimer = 0;
let detailContentLoaded = false;
let pendingRoute = false;
let queuedRoute = false;
let toastTimer = 0;
let pendingSearchQuery = '';
let pendingCategory = 'all';
const copyTimers = new WeakMap();
const copyWidthReleases = new WeakMap();
const copyVersions = new WeakMap();
const detailStepper = createDiscreteCameraStepper(() => detailRenderer, { reduced: prefersReducedMotion });
const staticContent = $('#static-route-content');
const setStatus = text => { $('#announcement').textContent = text; };

function listURL() {
  const query = {};
  if (pendingSearchQuery.trim()) query.query = pendingSearchQuery.trim();
  if (pendingCategory && pendingCategory !== 'all') query.category = pendingCategory;
  return href('models', undefined, { query });
}

function showToast(message, { actionLabel = null, onAction = null, duration = 2800 } = {}) {
  const host = $('#site-toast'), msg = $('#site-toast-msg'), btn = $('#site-toast-action');
  if (!host || !msg) return;
  const wasVisible = host.classList.contains('visible');
  msg.textContent = message;
  if (wasVisible) {
    animateOneShot(msg, 'toast-swap', [{ opacity: 0.4 }, { opacity: 1 }], { duration: prefersReducedMotion() ? MOTION.reducedFade : 120, easing: MOTION.easeStandard });
  }
  if (actionLabel && onAction && btn) {
    btn.textContent = actionLabel;
    btn.hidden = false;
    btn.onclick = ev => { host.classList.remove('visible'); onAction(ev); };
  } else if (btn) {
    btn.hidden = true;
    btn.onclick = null;
  }
  host.classList.add('visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => host.classList.remove('visible'), actionLabel ? 4500 : duration);
}

function cancelDetailZip() {
  detailZipVersion++;
  detailZipController?.abort();
  detailZipController = null;
  const zipBtn = $('#detail-download-zip');
  if (zipBtn) {
    zipBtn.removeAttribute('aria-busy');
    zipBtn.disabled = detailIntegrityBlocked;
  }
}

function setDetailDownloadsDisabled(disabled) {
  const host = $('#detail-downloads');
  if (!host) return;
  for (const link of host.querySelectorAll('a')) {
    if (disabled) {
      if (link.hasAttribute('href')) {
        link.dataset.disabledHref = link.getAttribute('href');
        link.removeAttribute('href');
      }
      link.setAttribute('aria-disabled', 'true');
    } else {
      if (link.dataset.disabledHref) {
        link.setAttribute('href', link.dataset.disabledHref);
        delete link.dataset.disabledHref;
      }
      link.removeAttribute('aria-disabled');
    }
  }
  for (const btn of host.querySelectorAll('button')) {
    btn.disabled = disabled;
  }
}

function setCopyButtonContent(button, text, iconName, { animateIcon = false } = {}) {
  if (!button) return;
  const label = button.querySelector?.('.btn-label');
  const iconHost = button.querySelector?.('.btn-icon');
  if (label) {
    if (text !== undefined) label.textContent = text;
  } else if (text !== undefined) {
    button.textContent = text;
  }
  if (iconHost && iconName) {
    const markup = iconMarkup(iconName).replace('<svg ', '<svg class="vault-icon" width="15" height="15" ');
    if (animateIcon) swapIconSmooth(iconHost, markup, { reduced: prefersReducedMotion() });
    else iconHost.innerHTML = markup;
  }
}

function resetCopyButton(button, defaultText, { anchor, key } = {}) {
  if (!button) return;
  copyVersions.set(button, (copyVersions.get(button) || 0) + 1);
  const timer = copyTimers.get(button);
  if (timer) { clearTimeout(timer); copyTimers.delete(button); }
  const releaseWidth = copyWidthReleases.get(button);
  if (releaseWidth) { releaseWidth(); copyWidthReleases.delete(button); }
  const wasCopied = button.dataset.copyState === 'copied';
  button.dataset.copyState = 'idle';
  button.removeAttribute('aria-busy');
  const defaultIcon = button.dataset.defaultIcon || '';
  setCopyButtonContent(button, defaultText, defaultIcon, { animateIcon: wasCopied });
  clearCopyFallback(anchor || button.closest('.detail-action-row') || button, key || button.id || '');
}

async function copyText(text, button, { successLabel, statusLabel, defaultLabel, anchor = button, key = button?.id || '' } = {}) {
  if (!button) return;
  resetCopyButton(button, defaultLabel, { anchor, key });
  const version = (copyVersions.get(button) || 0) + 1;
  copyVersions.set(button, version);
  const hasIcon = Boolean(button.querySelector?.('.btn-icon'));
  const doneLabel = successLabel || (hasIcon ? t('copied') : `${t('copied')} ✓`);
  const announceLabel = statusLabel || doneLabel;
  try {
    if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText(text);
    if (!button.isConnected || copyVersions.get(button) !== version) return;
    copyWidthReleases.set(button, lockButtonWidth(button));
    button.dataset.copyState = 'copied';
    setCopyButtonContent(button, doneLabel, hasIcon ? 'check' : '', { animateIcon: hasIcon });
    setStatus(announceLabel);
    const id = setTimeout(() => {
      if (button.isConnected && copyVersions.get(button) === version && button.dataset.copyState === 'copied') {
        resetCopyButton(button, defaultLabel, { anchor, key });
      }
    }, 2000);
    copyTimers.set(button, id);
  } catch {
    if (!button.isConnected || copyVersions.get(button) !== version) return;
    button.dataset.copyState = 'error';
    setStatus(t('copyFail'));
    showCopyFallback(anchor, text, lang, { key, focusTarget: button });
  }
}

function syncHomeSearchClear() {
  const input = $('#home-query'), btn = $('#home-search-clear');
  if (!input || !btn) return;
  animatePresence(btn, Boolean(input.value), {
    id: 'home-search-clear',
    enterY: 0,
    exitY: 0,
    enterScale: 0.82,
    enterDuration: 140,
    exitDuration: 110,
    reduced: prefersReducedMotion(),
  });
  btn.ariaLabel = lang === 'zh' ? '清除搜索词' : 'Clear search';
}

function showView(view) {
  if (!['home', 'about', 'notices', 'detail'].includes(view)) view = 'home';
  const prevView = currentView;
  currentView = view;
  $('#home-page').hidden = view !== 'home';
  $('#about-page').hidden = view !== 'about';
  $('#notices-page').hidden = view !== 'notices';
  $('#detail-page').hidden = view !== 'detail';
  if (staticContent) staticContent.hidden = true;
  if (view !== 'detail') {
    detailRenderer?.suspend();
    detailReady = false;
    if (typeof detailContentLoaded === 'boolean') detailContentLoaded = false;
  }
  document.querySelectorAll('.topbar [data-route]').forEach(anchor => {
    const active = anchor.dataset.route === view;
    if (active) anchor.setAttribute('aria-current', 'page');
    else anchor.removeAttribute('aria-current');
  });
  const docEl = document.documentElement;
  const mounted = docEl?.dataset?.viewMounted === 'true';
  if (docEl?.dataset) docEl.dataset.viewMounted = 'true';
  const targetSection = $(`#${view}-page`);
  if (mounted && prevView !== view && typeof animateOneShot === 'function' && typeof MOTION !== 'undefined') {
    const reduced = typeof prefersReducedMotion === 'function' && prefersReducedMotion();
    animateOneShot(
      targetSection,
      'view-enter',
      reduced ? [{ opacity: 0.45 }, { opacity: 1 }] : [{ opacity: 0, transform: 'translateY(6px)' }, { opacity: 1, transform: 'none' }],
      { duration: reduced ? MOTION.reducedFade : 200, easing: MOTION.easeStandard },
    );
  }
}

function syncDetailTools() {
  $('#detail-wireframe').disabled = !detailReady;
  const showReset = Boolean(detailReady && detailRenderer?.dirty);
  $('#detail-reset').disabled = !showReset;
  animatePresence($('#detail-reset'), showReset, { id: 'detail-reset', enterY: 0, exitY: 0, enterScale: 0.92, enterDuration: 150, exitDuration: 110, reduced: prefersReducedMotion() });
  const metricOk = Boolean(detailReady && detailRenderer?.detail?.metric?.available);
  $('#detail-compare').hidden = !metricOk;
  $('#detail-compare').disabled = !metricOk;
}

let detailOrbitDragging = false, detailOrbitStart = null, detailOrbitTimer = 0;
function setDetailOrbiting(active) {
  const wrap = $('#detail-stage-wrap');
  if (!wrap) return;
  if (active) wrap.dataset.orbiting = 'true';
  else delete wrap.dataset.orbiting;
}
function clearDetailOrbiting() {
  detailOrbitDragging = false;
  detailOrbitStart = null;
  clearTimeout(detailOrbitTimer);
  detailOrbitTimer = 0;
  setDetailOrbiting(false);
}

function updateDetailComparisonLabel() {
  const label = $('#detail-comparison-label');
  if (!label) return;
  const reduced = prefersReducedMotion();
  if (detailCompareError) {
    label.dataset.state = 'error';
    label.textContent = lang === 'zh' ? '参照加载失败，请重试。' : 'Could not load scale reference. Try again.';
    animatePresence(label, true, { id: 'compare-label', enterY: -4, exitY: -3, reduced });
    return;
  }
  if (detailCompareLoading) {
    label.dataset.state = 'loading';
    label.textContent = lang === 'zh' ? '正在载入尺寸参照…' : 'Loading scale reference…';
    animatePresence(label, true, { id: 'compare-label', enterY: -4, exitY: -3, reduced });
    return;
  }
  if (detailRenderer?.comparison && detailCompareKind && selected) {
    label.dataset.state = 'ready';
    label.textContent = comparisonText(detailCompareKind, lang, selected);
    animatePresence(label, true, { id: 'compare-label', enterY: -4, exitY: -3, reduced });
    return;
  }
  delete label.dataset.state;
  animatePresence(label, false, { id: 'compare-label', exitY: -3, reduced });
}

function setDetailLoadingMessage(text) {
  const pill = $('#detail-loading');
  if (!pill) return;
  if (!text) {
    animatePresence(pill, false, {
      id: 'detail-loading',
      exitY: 2,
      reduced: prefersReducedMotion(),
      onHidden: () => { pill.textContent = ''; },
    });
    return;
  }
  pill.textContent = text;
  animatePresence(pill, true, { id: 'detail-loading', enterY: 3, reduced: prefersReducedMotion() });
}

function handleDetailError(version, id, error) {
  if (version !== detailVersion || id !== requestedDetailId) return;
  detailStepper.cancel();
  detailReady = false;
  const posterImg = $('#detail-poster');
  posterImg.classList.remove('ready');
  const integrityFailure = ['MODEL_VERSION_MISMATCH', 'MODEL_IDENTITY_MISSING', 'MODEL_INTEGRITY_UNAVAILABLE'].includes(error?.code);
  if (integrityFailure) {
    detailIntegrityBlocked = true;
    cancelDetailZip();
    posterImg.style.visibility = 'hidden';
    posterImg.removeAttribute('src');
    setDetailDownloadsDisabled(true);
    setDetailLoadingMessage(lang === 'zh'
      ? '文件校验未通过，为避免下到损坏文件已暂停预览与下载，请重试。'
      : 'File check failed. Preview and downloads are paused to avoid corrupted files — please retry.');
  } else {
    setDetailLoadingMessage(selected?.glb ? t('viewError') : t('detailError'));
    if (!selected) {
      $('#detail-title').textContent = id || '';
      $('#detail-description').textContent = t('missing');
    }
  }
  animatePresence($('#detail-retry'), true, { id: 'detail-retry', enterY: 5, reduced: prefersReducedMotion() });
  syncDetailTools();
}

async function ensureDetailRenderer() {
  if (detailRenderer) return detailRenderer;
  const { DetailRenderer } = await import('./gallery/detail-renderer.js');
  detailRenderer = new DetailRenderer($('#detail-stage'), undefined, { inPlace: true });
  detailRenderer.wire = getStoredWireframe();
  detailRenderer.onDirtyChange = () => syncDetailTools();
  detailRenderer.onInteraction = () => {
    detailStepper.cancel();
    if (!prefersReducedMotion() && !detailOrbitDragging && detailReady) {
      setDetailOrbiting(true);
      clearTimeout(detailOrbitTimer);
      detailOrbitTimer = setTimeout(() => { detailOrbitTimer = 0; if (!detailOrbitDragging) setDetailOrbiting(false); }, 420);
    }
  };
  detailRenderer.onError = (error, ctx) => {
    if (!ctx || ctx.assetId === requestedDetailId) {
      handleDetailError(detailVersion, requestedDetailId, error);
    }
  };
  detailRenderer.onRestore = () => {
    if (currentView === 'detail' && requestedDetailId) {
      void openDetail(requestedDetailId);
    }
  };
  detailRenderer.onReferenceStateChange = (status, kind) => {
    if (status === 'loading') {
      detailCompareLoading = true;
      detailCompareError = false;
      detailCompareKind = kind;
      $('#detail-compare').setAttribute('aria-busy', 'true');
    } else if (status === 'ready') {
      detailCompareLoading = false;
      detailCompareError = false;
      detailCompareKind = kind;
      $('#detail-compare').removeAttribute('aria-busy');
    } else if (status === 'idle') {
      detailCompareLoading = false;
      detailCompareError = false;
      detailCompareKind = null;
      $('#detail-compare').removeAttribute('aria-busy');
      $('#detail-compare').setAttribute('aria-pressed', 'false');
    }
    updateDetailComparisonLabel();
    syncDetailTools();
  };
  detailRenderer.onReferenceError = () => {
    detailCompareLoading = false;
    detailCompareError = true;
    $('#detail-compare').removeAttribute('aria-busy');
    $('#detail-compare').setAttribute('aria-pressed', 'false');
    updateDetailComparisonLabel();
    syncDetailTools();
  };
  return detailRenderer;
}

function detailZipLabelHtml(asset) {
  const glbBytes = asset.file_sizes?.glb || asset.glb_bytes || 0;
  const blendBytes = asset.file_sizes?.blend || asset.blend_bytes || 0;
  const bundleBytes = asset.file_sizes?.bundle || (glbBytes + blendBytes);
  return `${esc(t('bundle'))}<small>${esc(t('bundleSub'))}${bundleBytes ? ` · ${esc(formatBytes(bundleBytes, lang))}` : ''}</small>`;
}

function renderDetailInfo(asset) {
  const name = modelShortName(asset, lang);
  $('#detail-crumb-name').textContent = name;
  $('#detail-category').textContent = categoryLabel(asset.category, lang);
  $('#detail-title').textContent = name;
  const desc = loc(asset.reconstruction_notes) || loc(asset.description);
  const scope = loc(asset.scientific_scope);
  const isBoilerplateDesc = !desc || /由本版验收\s*GLB\s*导入|imported from the reviewed GLB/i.test(desc);
  $('#detail-description').textContent = isBoilerplateDesc ? '' : desc;
  const locale = lang === 'zh' ? 'zh-CN' : 'en-US';
  $('#detail-triangles').textContent = Number.isFinite(asset.triangles) ? asset.triangles.toLocaleString(locale) : '—';
  const dim = primaryDimension(asset, lang);
  $('#detail-primary-dim').textContent = dim.value;
  $('#detail-primary-dim-label').textContent = dim.label;
  const glbBytes = asset.file_sizes?.glb || asset.glb_bytes || 0;
  const blendBytes = asset.file_sizes?.blend || asset.blend_bytes || 0;
  $('#detail-glb-bytes').textContent = formatBytes(glbBytes, lang) || '—';
  $('#detail-xyz').textContent = dimensionDetails(asset, lang);
  $('#detail-dim-note').textContent = dimensionNote(lang, asset);

  const glbFile = asset.downloads?.glb || asset.glb;
  const blendFile = asset.downloads?.blend || asset.blend;
  const blendSizeText = formatBytes(blendBytes, lang);
  const zipMarkup = asset.downloads?.bundle
    ? `<a href="${esc(path(asset.downloads.bundle))}" download class="detail-dl-zip"><span>${detailZipLabelHtml(asset)}</span><span class="arrow-down" aria-hidden="true">↓</span></a>`
    : (asset.glb && asset.blend
      ? `<button type="button" id="detail-download-zip" class="detail-dl-zip"><span>${detailZipLabelHtml(asset)}</span><span class="arrow-down" aria-hidden="true">↓</span></button>`
      : '');
  const secondaryMarkup = (blendFile || zipMarkup)
    ? `<div class="detail-dl-secondary-row">${blendFile ? `<a href="${esc(path(blendFile))}" download class="detail-dl-secondary" data-dl-track="blend"><span>${esc(t('blend'))}${blendSizeText ? `<small>${esc(blendSizeText)}</small>` : ''}</span><span class="arrow-down" aria-hidden="true">↓</span></a>` : ''}${zipMarkup}</div>`
    : '';
  $('#detail-downloads').innerHTML =
    (glbFile ? `<a href="${esc(path(glbFile))}" download class="detail-dl-primary" data-dl-track="glb"><span>${esc(t('glb'))}</span><span class="arrow-down" aria-hidden="true">↓</span></a>` : '') +
    secondaryMarkup;

  const zipBtn = $('#detail-download-zip');
  if (zipBtn) {
    if (detailZipController) {
      zipBtn.disabled = true;
      zipBtn.setAttribute('aria-busy', 'true');
      zipBtn.querySelector('span').innerHTML = `${esc(t('preparingZip'))}<small>${esc(t('bundleSub'))}</small>`;
    }
    zipBtn.onclick = async () => {
      if (zipBtn.disabled || detailIntegrityBlocked) return;
      detailZipController?.abort();
      const controller = detailZipController = new AbortController();
      const gen = ++detailZipVersion;
      zipBtn.disabled = true;
      zipBtn.setAttribute('aria-busy', 'true');
      const labelSpan = zipBtn.querySelector('span');
      labelSpan.innerHTML = `${esc(t('preparingZip'))}<small>${esc(t('bundleSub'))}</small>`;
      setStatus(t('preparingZip'));
      try {
        const { filename } = await downloadModelZip(asset, { resolveURL: path, signal: controller.signal });
        if (gen !== detailZipVersion || selected?.id !== asset.id || detailIntegrityBlocked || controller.signal.aborted) return;
        const arrow = zipBtn.querySelector('.arrow-down');
        if (arrow && !prefersReducedMotion()) {
          animateOneShot(arrow, 'dl-nudge', [{ transform: 'translateY(0)' }, { transform: 'translateY(3px)' }, { transform: 'translateY(0)' }], { duration: 220, easing: MOTION.easeStandard });
        }
        showToast(lang === 'zh' ? `已开始下载 ${filename}` : `Downloading ${filename}`, {
          actionLabel: lang === 'zh' ? '复制署名' : 'Copy credit',
          onAction: () => copyAttributionFor(asset),
        });
      } catch (error) {
        if (error?.name === 'AbortError' || gen !== detailZipVersion) return;
        showToast(t('zipFailed'), { duration: 4200 });
        setStatus(t('zipFailed'));
      } finally {
        if (detailZipController === controller) detailZipController = null;
        const activeBtn = $('#detail-download-zip');
        if (gen === detailZipVersion && activeBtn && selected?.id === asset.id) {
          activeBtn.disabled = detailIntegrityBlocked;
          activeBtn.removeAttribute('aria-busy');
          const activeSpan = activeBtn.querySelector('span');
          if (activeSpan) activeSpan.innerHTML = detailZipLabelHtml(asset);
        }
      }
    };
  }

  for (const dlLink of $('#detail-downloads').querySelectorAll('a[data-dl-track]')) {
    dlLink.addEventListener('click', () => {
      if (detailIntegrityBlocked || dlLink.getAttribute('aria-disabled') === 'true') return;
      const arrow = dlLink.querySelector('.arrow-down');
      if (arrow && !prefersReducedMotion()) {
        animateOneShot(arrow, 'dl-nudge', [{ transform: 'translateY(0)' }, { transform: 'translateY(3px)' }, { transform: 'translateY(0)' }], { duration: 220, easing: MOTION.easeStandard });
      }
      showToast(lang === 'zh' ? '已开始下载 · 别忘了附带 CC BY 4.0 署名' : 'Download started · Remember CC BY 4.0 credit', {
        actionLabel: lang === 'zh' ? '复制署名' : 'Copy credit',
        onAction: () => copyAttributionFor(asset),
      });
    });
  }

  if (detailIntegrityBlocked) setDetailDownloadsDisabled(true);

  const actionRow = $('.detail-action-row');
  resetCopyButton($('#detail-copy-credit'), t('copy'), { anchor: actionRow, key: 'detail-copy-credit' });
  resetCopyButton($('#detail-share'), t('share'), { anchor: actionRow, key: 'detail-share' });
  $('#detail-copy-credit').onclick = () => copyAttributionFor(asset);
  $('#detail-share').onclick = () => copyText(new URL(href('detail', asset.id), location.origin).href, $('#detail-share'), {
    successLabel: t('copied'),
    statusLabel: t('linkCopied'),
    defaultLabel: t('share'),
    anchor: actionRow,
    key: 'detail-share',
  });

  const noteText = isBoilerplateDesc ? (desc || scope) : (scope && scope !== desc && !(desc && desc.includes(scope)) ? scope : '');
  const showScope = Boolean(noteText);
  $('#detail-scope-section').hidden = !showScope;
  if (showScope) $('#detail-scope').textContent = noteText;

  const validSources = (asset.sources || []).filter(s => /^https?:\/\//.test(s.url || ''));
  $('#detail-sources-section').hidden = !validSources.length;
  $('#detail-sources').innerHTML = validSources
    .map(s => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title || s.id || s.url)} ↗</a></li>`)
    .join('');
}

function copyAttributionFor(asset) {
  const canonicalUrl = new URL(href('detail', asset.id), location.origin).href;
  return copyText(formatAttribution(asset, lang, canonicalUrl), $('#detail-copy-credit'), {
    successLabel: t('copied'),
    defaultLabel: t('copy'),
    anchor: $('.detail-action-row'),
    key: 'detail-copy-credit',
  });
}

function paintDetailNeighbors() {
  const { prev, next, related } = detailNeighbors;
  const prevEl = $('#previous-model'), nextEl = $('#next-model');
  prevEl.hidden = !prev;
  if (prev) {
    prevEl.href = href('detail', prev.id);
    prevEl.dataset.routeDetail = prev.id;
    prevEl.textContent = `← ${modelShortName(prev, lang)}`;
    prevEl.ariaLabel = `${t('previousModel')}: ${modelShortName(prev, lang)}`;
  }
  nextEl.hidden = !next;
  if (next) {
    nextEl.href = href('detail', next.id);
    nextEl.dataset.routeDetail = next.id;
    nextEl.textContent = `${modelShortName(next, lang)} →`;
    nextEl.ariaLabel = `${t('nextModel')}: ${modelShortName(next, lang)}`;
  }
  const relatedSec = $('#related');
  const hadHidden = relatedSec.hidden;
  relatedSec.hidden = !related.length;
  $('#related-models').innerHTML = related.map(item =>
    `<a href="${esc(href('detail', item.id))}" data-route-detail="${esc(item.id)}"><span class="related-thumb"><img src="${esc(path(item.preview))}" alt="${esc(modelShortName(item, lang))}" loading="lazy" width="160" height="160" data-thumb-loading="true"></span><span>${esc(modelShortName(item, lang))}</span></a>`
  ).join('');
  for (const img of $('#related-models').querySelectorAll('img')) {
    const settle = () => { delete img.dataset.thumbLoading; };
    if (img.complete && img.naturalWidth > 0) settle();
    else {
      img.addEventListener('load', settle, { once: true });
      img.addEventListener('error', settle, { once: true });
    }
  }
  if (hadHidden && related.length) {
    const reduced = prefersReducedMotion();
    animateOneShot(relatedSec, 'related-enter', reduced ? [{ opacity: 0 }, { opacity: 1 }] : [{ opacity: 0, transform: 'translateY(6px)' }, { opacity: 1, transform: 'none' }], { duration: reduced ? MOTION.reducedFade : 180, easing: MOTION.easeStandard });
  }
}

async function renderDetailNeighborsAndRelated(asset, version) {
  try {
    const pageSize = 100;
    let prev = null, next = null, foundPage = null, foundPos = -1, prevPageTail = null;
    for (let page = 0; ; page++) {
      const result = await store.search({ category: asset.category, page, pageSize });
      if (version !== detailVersion) return;
      const list = result.items || [];
      const pos = list.findIndex(item => item.id === asset.id);
      if (pos >= 0) {
        foundPage = list;
        foundPos = pos;
        prev = pos > 0 ? list[pos - 1] : prevPageTail;
        if (pos < list.length - 1) {
          next = list[pos + 1];
        } else if (page + 1 < result.pages) {
          const nextResult = await store.search({ category: asset.category, page: page + 1, pageSize });
          if (version !== detailVersion) return;
          next = nextResult.items?.[0] || null;
        }
        break;
      }
      prevPageTail = list.at(-1) || prevPageTail;
      if (page + 1 >= result.pages || !list.length) break;
    }
    if (version !== detailVersion) return;
    const pool = foundPage || (await store.search({ category: asset.category, page: 0, pageSize: 12 })).items || [];
    if (version !== detailVersion) return;
    const related = [];
    if (foundPos >= 0) {
      for (const offset of [1, -1, 2, -2, 3, -3, 4, -4]) {
        const candidate = pool[foundPos + offset];
        if (candidate && candidate.id !== asset.id && !related.some(x => x.id === candidate.id)) {
          related.push(candidate);
          if (related.length === 4) break;
        }
      }
    }
    if (related.length < 4) {
      for (const candidate of pool) {
        if (candidate.id !== asset.id && !related.some(x => x.id === candidate.id)) {
          related.push(candidate);
          if (related.length === 4) break;
        }
      }
    }
    detailNeighbors = { prev, next, related };
    paintDetailNeighbors();
  } catch {
    if (version !== detailVersion) return;
    detailNeighbors = { prev: null, next: null, related: [] };
    paintDetailNeighbors();
  }
}

function resetDetailSkeleton() {
  $('#detail-crumb-name').textContent = '';
  $('#detail-category').textContent = '';
  $('#detail-title').textContent = '';
  $('#detail-description').textContent = '';
  $('#detail-triangles').textContent = '—';
  $('#detail-primary-dim').textContent = '—';
  $('#detail-glb-bytes').textContent = '—';
  $('#detail-xyz').textContent = '';
  $('#detail-dim-note').textContent = '';
  $('#detail-downloads').replaceChildren();
  $('#detail-scope-section').hidden = true;
  $('#detail-sources-section').hidden = true;
  $('#previous-model').hidden = true;
  $('#next-model').hidden = true;
  $('#related').hidden = true;
  $('#related-models').replaceChildren();
  const posterImg = $('#detail-poster');
  posterImg.classList.remove('ready');
  posterImg.style.visibility = 'hidden';
  posterImg.removeAttribute('src');
  const actionRow = $('.detail-action-row');
  resetCopyButton($('#detail-copy-credit'), t('copy'), { anchor: actionRow, key: 'detail-copy-credit' });
  resetCopyButton($('#detail-share'), t('share'), { anchor: actionRow, key: 'detail-share' });
}

async function openDetail(id) {
  const version = ++detailVersion;
  const previousId = selected?.id || requestedDetailId;
  const wasShowingDetail = currentView === 'detail' && detailContentLoaded;
  const keepStaticWhileLoading = Boolean(
    staticContent &&
    !staticContent.hidden &&
    staticContent.dataset.routeType === 'detail' &&
    staticContent.dataset.assetId === id
  );
  clearTimeout(detailSkeletonTimer);
  detailSkeletonTimer = 0;
  detailStepper.cancel();
  cancelDetailZip();
  requestedDetailId = id;
  selected = null;
  detailReady = false;
  detailIntegrityBlocked = false;
  detailCompareLoading = false;
  detailCompareError = false;
  detailCompareKind = null;
  detailNeighbors = { prev: null, next: null, related: [] };
  detailRenderer?.suspend();
  const infoCol = $('.detail-info-column');
  if (!wasShowingDetail) {
    resetDetailSkeleton();
    setDetailLoadingMessage(t('viewLoading'));
  } else {
    if (previousId !== id && scrollY > 40) {
      scrollTo({ top: 0, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
    }
    detailSkeletonTimer = setTimeout(() => {
      if (version !== detailVersion || selected) return;
      if (infoCol) infoCol.dataset.loading = 'true';
      setDetailLoadingMessage(t('viewLoading'));
    }, 140);
  }
  animatePresence($('#detail-comparison-label'), false, { id: 'compare-label', immediate: true });
  $('#detail-compare').setAttribute('aria-pressed', 'false');
  $('#detail-compare').removeAttribute('aria-busy');
  $('#detail-wireframe').setAttribute('aria-pressed', String(getStoredWireframe()));
  animatePresence($('#detail-retry'), false, { id: 'detail-retry', immediate: true });
  syncDetailTools();
  clearDetailOrbiting();
  if (!keepStaticWhileLoading) showView('detail');

  try {
    const asset = await store.getDetail(id);
    if (version !== detailVersion) return;
    clearTimeout(detailSkeletonTimer);
    detailSkeletonTimer = 0;
    if (infoCol) delete infoCol.dataset.loading;
    selected = asset;
    showView('detail');
    renderDetailInfo(asset);
    detailContentLoaded = true;
    if (wasShowingDetail && previousId !== id && infoCol) {
      animateOneShot(infoCol, 'detail-swap', [{ opacity: 0.6 }, { opacity: 1 }], { duration: prefersReducedMotion() ? MOTION.reducedFade : 160, easing: MOTION.easeStandard });
    }
    document.title = `${modelShortName(asset, lang)} | Lowpoly Vault`;

    const posterImg = $('#detail-poster');
    const previewPath = asset.card_preview || asset.preview;
    posterImg.classList.remove('ready');
    posterImg.style.visibility = previewPath ? 'visible' : 'hidden';
    if (previewPath) {
      const nextSrc = path(previewPath);
      const settlePoster = () => { if (version === detailVersion) delete posterImg.dataset.posterState; };
      posterImg.onload = settlePoster;
      posterImg.onerror = settlePoster;
      posterImg.dataset.posterState = 'loading';
      posterImg.src = nextSrc;
      posterImg.alt = modelShortName(asset, lang);
      if (posterImg.complete && posterImg.naturalWidth > 0) settlePoster();
    } else {
      posterImg.onload = posterImg.onerror = null;
      delete posterImg.dataset.posterState;
      posterImg.removeAttribute('src');
    }
    if (!detailReady) setDetailLoadingMessage(t('viewLoading'));
    void renderDetailNeighborsAndRelated(asset, version);

    const r = await ensureDetailRenderer();
    if (version !== detailVersion) return;
    const ready = await r.select(asset, {
      afterFirstRender: () => {
        if (version === detailVersion) posterImg.classList.add('ready');
      },
    });
    if (version !== detailVersion || !ready) return;
    detailReady = true;
    setDetailLoadingMessage('');
    $('#detail-wireframe').setAttribute('aria-pressed', String(r.wire));
    syncDetailTools();
  } catch (error) {
    clearTimeout(detailSkeletonTimer);
    detailSkeletonTimer = 0;
    if (infoCol) delete infoCol.dataset.loading;
    if (error?.name === 'AbortError' || version !== detailVersion) return;
    if (keepStaticWhileLoading && !selected && staticContent && !staticContent.hidden) {
      showToast(t('detailError'), { duration: 4200 });
      return;
    }
    if (!keepStaticWhileLoading || selected) showView('detail');
    handleDetailError(version, id, error);
  }
}

async function renderNotices() {
  const host = $('#notices-body');
  if (!host || host.dataset.loaded === 'true') return;
  const preRendered = staticContent?.dataset.routeType === 'notices' ? staticContent.querySelector('.notices-rendered') : null;
  if (preRendered && preRendered.innerHTML.trim()) {
    host.innerHTML = preRendered.innerHTML;
    host.dataset.loaded = 'true';
    return;
  }
  let showedLoading = false;
  const loadingTimer = setTimeout(() => {
    if (host.dataset.loaded === 'true') return;
    showedLoading = true;
    host.innerHTML = `<p class="notices-loading" role="status">${esc(lang === 'zh' ? '正在载入许可说明…' : 'Loading notices…')}</p>`;
  }, 90);
  try {
    const response = await fetch(new URL('THIRD_PARTY_NOTICES.md', new URL(siteRoot, location.origin)).href);
    const contentType = response.headers.get('content-type') || '';
    if (!response.ok || /text\/html/i.test(contentType)) throw new Error('Notices unavailable');
    const markdown = await response.text();
    clearTimeout(loadingTimer);
    host.innerHTML = renderNoticesMarkdown(markdown);
    host.dataset.loaded = 'true';
    if (showedLoading) {
      const reduced = prefersReducedMotion();
      animateOneShot(host, 'notices-enter', reduced ? [{ opacity: 0 }, { opacity: 1 }] : [{ opacity: 0, transform: 'translateY(4px)' }, { opacity: 1, transform: 'none' }], { duration: reduced ? MOTION.reducedFade : 180, easing: MOTION.easeStandard });
    }
  } catch {
    clearTimeout(loadingTimer);
    host.innerHTML = `<p><a href="${esc(new URL('THIRD_PARTY_NOTICES.md', new URL(siteRoot, location.origin)).href)}">THIRD_PARTY_NOTICES.md</a></p>`;
  }
}

async function syncRoute(){
  // The wheel owns model-list documents. History/hash navigation must cross
  // the same document boundary as an ordinary link, without mounting both apps.
  const incoming=parseRoute(location.pathname,siteRoot);
  if(incoming.type==='models'){location.reload();return;}
  if(!index&&incoming.type==='detail')return;
  if(pendingRoute){queuedRoute=true;return;}
  pendingRoute=true;
  try{
    const oldHash=location.hash;
    if(oldHash.startsWith('#asset=')){const id=decodeURIComponent(oldHash.slice(7));if(/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(id))history.replaceState(null,'',href('detail',id));}
    else if(['#catalog','#collection','#about'].includes(oldHash))history.replaceState(null,'',href(oldHash==='#about'?'about':'models'));
    const route=parseRoute(location.pathname,siteRoot);
    const nextLang=route.lang==='zh-CN'?'zh':'en';
    if(lang!==nextLang){lang=nextLang;paintLanguage();}
    if(route.type==='models'){location.reload();return;}
    if(route.type==='detail'){
      if(!index)return;
      await openDetail(route.id);
    }else if(route.type==='notices'){
      cancelDetailZip();selected=null;requestedDetailId=null;showView('notices');await renderNotices();
      document.title=`${t('noticesTitle')} | Lowpoly Vault`;
      scrollTo(0,0);
    }else if(route.type==='about'){
      cancelDetailZip();selected=null;requestedDetailId=null;showView('about');
      document.title=`${t('about')} | Lowpoly Vault`;
      scrollTo(0,0);
    }else{
      cancelDetailZip();selected=null;requestedDetailId=null;showView('home');
      document.title=lang==='zh'?'Lowpoly Vault — 原创低多边形 3D 模型库':'Lowpoly Vault — Original low-poly 3D models';
      scrollTo(0,0);
    }
  }finally{pendingRoute=false;if(queuedRoute){queuedRoute=false;syncRoute();}}
}

function navigate(view){if(view==='catalog'){location.assign(listURL());return;}history.pushState({view},'',href(view));syncRoute();}

function paintHome() {
  if (!index) return;
  const locale = lang === 'zh' ? 'zh-CN' : 'en-US';
  const totalFormatted = Number(index.total || 0).toLocaleString(locale);
  document.querySelectorAll('[data-browse] [data-t="exploreAll"]').forEach(el => {
    el.textContent = lang === 'zh' ? `浏览全部 ${totalFormatted} 个模型` : `Explore all ${totalFormatted} models`;
  });
  const countByCat = new Map((index.categories || []).map(c => [c.id, c.count]));
  const featured = Array.isArray(index.featured) && index.featured.length
    ? index.featured
    : HOME_FEATURED_SPECS.map(spec => {
        const pick = index.initial.find(x => x.id === spec.id) || index.initial.find(x => x.category === spec.category);
        return pick ? { category: spec.category, num: spec.num, id: pick.id, name: pick.name, preview: pick.preview } : null;
      }).filter(Boolean);
  const grid = $('#home-categories');
  const existingCards = [...grid.querySelectorAll('.curation-card[data-home-category]')];
  const canReuse = existingCards.length === featured.length &&
    existingCards.every((card, idx) => card.dataset.homeCategory === featured[idx].category);
  if (canReuse) {
    featured.forEach((item, idx) => {
      const card = existingCards[idx];
      const count = (countByCat.get(item.category) || 0).toLocaleString(locale);
      card.href = href('models', undefined, { query: { category: item.category } });
      const img = card.querySelector('img');
      if (img) img.alt = loc(item.name);
      const num = card.querySelector('.curation-number');
      if (num) num.textContent = item.num;
      const titleEl = card.querySelector('.curation-title');
      if (titleEl) {
        const countSpan = titleEl.querySelector('span');
        const label = categoryLabel(item.category, lang);
        if (titleEl.firstChild?.nodeType === 3) titleEl.firstChild.textContent = label;
        else titleEl.prepend(document.createTextNode(label));
        if (countSpan) countSpan.textContent = `${count} ${t('count')} →`;
      }
    });
    return;
  }
  grid.innerHTML = featured.map(item => {
    const count = (countByCat.get(item.category) || 0).toLocaleString(locale);
    return `<a class="curation-card" href="${esc(href('models', undefined, { query: { category: item.category } }))}" data-home-category="${esc(item.category)}"><div><img src="${esc(path(item.preview))}" alt="${esc(loc(item.name))}" loading="lazy" width="640" height="640"><span class="curation-number">${esc(item.num)}</span></div><span class="curation-title">${esc(categoryLabel(item.category, lang))}<span>${esc(count)} ${esc(t('count'))} →</span></span></a>`;
  }).join('');
}

function paintLanguage() {
  const targetDocLang = lang === 'zh' ? 'zh-CN' : 'en';
  const sameInitialDocLang = document.documentElement.lang === targetDocLang;
  document.documentElement.lang = targetDocLang;
  document.querySelectorAll('[data-t]').forEach(el => {
    // Preserve static-baked total count on Home CTA before catalog index loads to avoid width jump.
    if (!index && sameInitialDocLang && el.dataset.t === 'exploreAll' && /\d/.test(el.textContent)) return;
    el.innerHTML = t(el.dataset.t);
  });
  const langEl = $('#language');
  const route = parseRoute(location.pathname, siteRoot);
  const otherLang = lang === 'en' ? 'zh-CN' : 'en';
  langEl.textContent = lang === 'en' ? '中文' : 'EN';
  langEl.ariaLabel = lang === 'en' ? '切换为简体中文' : 'Switch to English';
  langEl.lang = otherLang;
  if (langEl.tagName === 'A') {
    langEl.href = routeHref({ type: route.type === 'not-found' ? 'home' : route.type, id: route.id, page: route.page, lang: otherLang }, siteRoot);
  }
  $('.topbar .github-link').ariaLabel = lang === 'zh' ? 'GitHub 代码仓库（在新标签页打开）' : 'GitHub repository (opens in a new tab)';
  $('#home-query').placeholder = t('homeSearch');
  $('#home-query').ariaLabel = t('homeSearch');
  $('#detail-stage').ariaLabel = t('canvas');
  $('.model-pagination').ariaLabel = lang === 'zh' ? '上一个和下一个模型' : 'Previous and next models';
  document.querySelectorAll('[data-route]').forEach(a => { a.href = href(a.dataset.route); });
  document.querySelectorAll('[data-browse]').forEach(a => { if (a.tagName === 'A') a.href = href('models'); });
  document.querySelectorAll('[data-route-detail]').forEach(a => { a.href = href('detail', a.dataset.routeDetail); });
  $('.hero-art').src = new URL('home/editorial-hero.webp', new URL(siteRoot, location.origin)).href;
  resetCopyButton($('#about-copy-credit'), t('copy'), { anchor: $('#about-copy-credit'), key: 'about-copy-credit' });
  syncHomeSearchClear();
  paintHome();
  if (currentView === 'detail' && selected) {
    renderDetailInfo(selected);
    paintDetailNeighbors();
    updateDetailComparisonLabel();
    document.title = `${modelShortName(selected, lang)} | Lowpoly Vault`;
  } else if (currentView === 'about') {
    document.title = `${t('about')} | Lowpoly Vault`;
  } else if (currentView === 'notices') {
    document.title = `${t('noticesTitle')} | Lowpoly Vault`;
  } else {
    document.title = lang === 'zh' ? 'Lowpoly Vault — 原创低多边形 3D 模型库' : 'Lowpoly Vault — Original low-poly 3D models';
  }
}

document.addEventListener('click', event => {
  const detailLink = event.target.closest('[data-route-detail]');
  if (detailLink && plainClick(event)) {
    event.preventDefault();
    const id = detailLink.dataset.routeDetail;
    history.pushState({ view: 'detail', id }, '', href('detail', id));
    void syncRoute();
    return;
  }
  const nav = event.target.closest('[data-route]');
  if (nav && plainClick(event)) {
    event.preventDefault();
    pendingSearchQuery = '';
    pendingCategory = 'all';
    navigate(nav.dataset.route);
    return;
  }
  const browse = event.target.closest('[data-browse]');
  if (browse && plainClick(event)) {
    event.preventDefault();
    pendingSearchQuery = '';
    pendingCategory = 'all';
    navigate('catalog');
    return;
  }
  const facet = event.target.closest('[data-home-category]');
  if (facet && plainClick(event)) {
    event.preventDefault();
    pendingSearchQuery = '';
    pendingCategory = facet.dataset.homeCategory;
    navigate('catalog');
  }
});

$('#home-search').onsubmit = event => {
  event.preventDefault();
  pendingSearchQuery = $('#home-query').value;
  pendingCategory = 'all';
  navigate('catalog');
};
$('#home-query').addEventListener('input', syncHomeSearchClear);
$('#home-query').addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    e.preventDefault();
    if ($('#home-query').value) { $('#home-query').value = ''; syncHomeSearchClear(); }
    else $('#home-query').blur();
  }
});
$('#home-search-clear').onclick = () => {
  $('#home-query').value = '';
  syncHomeSearchClear();
  $('#home-query').focus();
};

$('#about-copy-credit').onclick = () => {
  const text = $('#about-credit-sample').textContent.trim();
  void copyText(text, $('#about-copy-credit'), {
    successLabel: t('copied'),
    defaultLabel: t('copy'),
    anchor: $('#about-copy-credit'),
    key: 'about-copy-credit',
  });
};

$('#language').onclick = event => {
  if (event && !plainClick(event)) return;
  event?.preventDefault();
  const route = parseRoute(location.pathname, siteRoot);
  lang = lang === 'en' ? 'zh' : 'en';
  setStoredLang(lang);
  const target = href(route.type === 'not-found' ? 'home' : route.type, route.id, { page: route.page });
  history.replaceState(history.state, '', target);
  paintLanguage();
  animateOneShot($('#language'), 'lang-swap', [{ opacity: 0.45 }, { opacity: 1 }], { duration: prefersReducedMotion() ? MOTION.reducedFade : 120, easing: MOTION.easeStandard });
};

$('#detail-wireframe').onclick = () => {
  if (!detailReady || !detailRenderer) return;
  const next = !detailRenderer.wire;
  detailRenderer.wireframe(next);
  setStoredWireframe(next);
  $('#detail-wireframe').setAttribute('aria-pressed', String(detailRenderer.wire));
};
$('#detail-compare').onclick = () => {
  if (!detailReady || !detailRenderer) return;
  detailStepper.cancel();
  detailCompareError = false;
  const result = detailRenderer.compare();
  if (!result) {
    detailCompareLoading = false;
    detailCompareKind = null;
    $('#detail-compare').setAttribute('aria-pressed', 'false');
    $('#detail-compare').removeAttribute('aria-busy');
  } else {
    detailCompareKind = result.kind;
    $('#detail-compare').setAttribute('aria-pressed', 'true');
    if (result.ready) { detailCompareLoading = false; $('#detail-compare').removeAttribute('aria-busy'); }
    else { detailCompareLoading = true; $('#detail-compare').setAttribute('aria-busy', 'true'); }
  }
  updateDetailComparisonLabel();
  syncDetailTools();
};
$('#detail-reset').onclick = () => {
  if (!detailReady || !detailRenderer) return;
  detailStepper.cancel();
  if (!prefersReducedMotion()) {
    const svg = $('#detail-reset svg');
    animateOneShot(svg, 'reset-spin', [{ transform: 'rotate(0deg)' }, { transform: 'rotate(-360deg)' }], { duration: MOTION.gentle, easing: MOTION.easeStandard });
  }
  detailCompareLoading = false;
  detailCompareError = false;
  detailCompareKind = null;
  detailRenderer.reset();
  $('#detail-compare').setAttribute('aria-pressed', 'false');
  $('#detail-compare').removeAttribute('aria-busy');
  updateDetailComparisonLabel();
  syncDetailTools();
};
$('#detail-stage').addEventListener('pointerdown', event => {
  if (!detailReady || event.button > 0) return;
  clearTimeout(detailOrbitTimer);
  detailOrbitStart = { id: event.pointerId, x: event.clientX, y: event.clientY };
});
window.addEventListener('pointermove', event => {
  if (!detailOrbitStart || event.pointerId !== detailOrbitStart.id || detailOrbitDragging || prefersReducedMotion()) return;
  if (Math.hypot(event.clientX - detailOrbitStart.x, event.clientY - detailOrbitStart.y) >= 4) {
    detailOrbitDragging = true;
    setDetailOrbiting(true);
  }
}, { passive: true });
const endDetailOrbit = () => {
  if (!detailOrbitStart && !detailOrbitDragging) return;
  detailOrbitStart = null;
  const was = detailOrbitDragging;
  detailOrbitDragging = false;
  if (was) {
    clearTimeout(detailOrbitTimer);
    detailOrbitTimer = setTimeout(() => { detailOrbitTimer = 0; if (!detailOrbitDragging) setDetailOrbiting(false); }, 180);
  }
};
window.addEventListener('pointerup', endDetailOrbit, { passive: true });
window.addEventListener('pointercancel', endDetailOrbit, { passive: true });
window.addEventListener('blur', clearDetailOrbiting);
$('#detail-retry').onclick = () => { if (requestedDetailId) void openDetail(requestedDetailId); };
$('#detail-stage').addEventListener('keydown', event => {
  if (event.ctrlKey || event.metaKey || event.altKey || !detailReady || !detailRenderer) return;
  const action = {
    '+': () => detailStepper.zoom(0.85), '=': () => detailStepper.zoom(0.85),
    '-': () => detailStepper.zoom(1.18), '_': () => detailStepper.zoom(1.18),
    ArrowLeft: () => detailStepper.rotate(-8, 0), ArrowRight: () => detailStepper.rotate(8, 0),
    ArrowUp: () => detailStepper.rotate(0, 8), ArrowDown: () => detailStepper.rotate(0, -8),
    Home: () => $('#detail-reset').click(), r: () => $('#detail-reset').click(), R: () => $('#detail-reset').click(),
  }[event.key];
  if (action) { event.preventDefault(); action(); }
});

document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && currentView === 'detail' && detailRenderer?.comparison) {
    $('#detail-compare').click();
    return;
  }
  if (event.ctrlKey || event.metaKey || event.altKey) return;
  if (['INPUT', 'TEXTAREA', 'SELECT'].includes(event.target?.tagName)) return;
  if (event.key === '/' && currentView === 'home') {
    event.preventDefault();
    $('#home-query').focus();
    $('#home-query').select();
  }
});

window.addEventListener('popstate', syncRoute);
window.addEventListener('hashchange', syncRoute);
document.addEventListener('visibilitychange', () => { if (document.hidden) detailStepper.cancel(); });
matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', () => { detailStepper.cancel(); });
window.addEventListener('pagehide', event => {
  clearTimeout(detailSkeletonTimer);
  detailStepper.cancel();
  cancelDetailZip();
  if (event.persisted) {
    detailRenderer?.suspend();
    return;
  }
  detailRenderer?.dispose();
  detailRenderer = null;
  store.dispose();
});
window.addEventListener('pageshow', event => {
  if (!event.persisted) return;
  if (currentView === 'detail' && requestedDetailId) {
    void openDetail(requestedDetailId);
  }
});

async function load() {
  try {
    const review = import.meta.env.DEV && new URLSearchParams(location.search).get('review') === '1';
    index = await store.load(new URL(review ? 'assets/catalog-review.json' : releaseCatalogPath('catalog'), new URL(siteRoot, location.origin)).href);
    if (index.review_only && !$('.review-notice')) {
      const notice = document.createElement('p');
      notice.className = 'review-notice';
      notice.textContent = t('review');
      document.body.prepend(notice);
    }
    paintHome();
    await syncRoute();
  } catch {
    const route = parseRoute(location.pathname, siteRoot);
    if (route.type === 'detail') {
      if (staticContent && !staticContent.hidden && staticContent.dataset.routeType === 'detail') {
        showToast(t('detailError'), { duration: 4200 });
      } else {
        showView('detail');
        setDetailLoadingMessage(t('detailError'));
      }
    }
  }
}

if (!redirectingToZh) {
  if (initialRoute.type === 'about') {
    showView('about');
  } else if (initialRoute.type === 'notices') {
    showView('notices');
    void renderNotices();
  } else if (initialRoute.type === 'detail') {
    const hasMatchingStaticDetail = Boolean(
      staticContent &&
      staticContent.dataset.routeType === 'detail' &&
      staticContent.dataset.assetId === initialRoute.id
    );
    if (!hasMatchingStaticDetail) showView('detail');
    else currentView = 'detail';
  } else {
    showView('home');
  }
  paintLanguage();
  load();
}

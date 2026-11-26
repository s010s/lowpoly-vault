/** Single source of truth for bilingual UI terminology, formatting, curation visibility, attribution, and copy feedback. */
import { normalizeText } from './routes.js';

export const CATEGORIES = Object.freeze({
  animals: { en: 'Animals', zh: '动物', aliases: ['animal', 'creature', 'fauna', '生物', '动物形态'] },
  geology: { en: 'Geology', zh: '地质', aliases: ['rock', 'stone', 'mineral', 'landform', '岩石', '石头', '矿物', '地貌'] },
  plants: { en: 'Plants', zh: '植物', aliases: ['flora', 'tree', 'fern', 'leaf', '树', '草', '蕨'] },
  specimen: { en: 'Fossil studies', zh: '化石标本', aliases: ['fossil', 'shell', 'specimen', '化石', '标本', '壳'] },
  traces: { en: 'Traces', zh: '遗迹', aliases: ['trace', 'footprint', 'burrow', 'nest', '痕迹', '足迹', '巢'] },
  terrain: { en: 'Terrain', zh: '地貌', aliases: ['landscape', 'surface', 'ground', '地形', '地表'] },
  wood: { en: 'Wood', zh: '木材', aliases: ['log', 'trunk', 'timber', '木头', '倒木'] },
  mollusk: { en: 'Mollusks', zh: '软体动物', aliases: ['shell', 'nautilus', '螺', '贝'] },
  fungi: { en: 'Fungi', zh: '真菌', aliases: ['fungus', 'mushroom', '菌'] },
});

export const CURATED_PACK_IDS = new Set(['prehistoric-starter']);

export const CURATED_PACK_LABELS = Object.freeze({
  'prehistoric-starter': { en: 'Starter collection', zh: '史前入门精选' },
});

export const HOME_FEATURED_SPECS = Object.freeze([
  { category: 'animals', id: 'stegosaurus', num: '01' },
  { category: 'plants', id: 'cycad', num: '02' },
  { category: 'geology', id: 'natural-arch', num: '03' },
  { category: 'traces', id: 'dinosaur-nest', num: '04' },
  { category: 'specimen', id: 'cooperoceras', num: '05' },
]);

export const LANG_STORAGE_KEY = 'vault-lang';
export const WIREFRAME_STORAGE_KEY = 'vault-wireframe';

export function isZh(lang) {
  return lang === 'zh' || lang === 'zh-CN';
}

export function categoryLabel(category, lang = 'en') {
  const entry = CATEGORIES[category];
  if (!entry) return category || '';
  return isZh(lang) ? entry.zh : entry.en;
}

export function categorySearchTerms(category) {
  const entry = CATEGORIES[category];
  if (!entry) return category ? [category] : [];
  return [category, entry.en, entry.zh, ...entry.aliases];
}

export function isUserFacingPack(packId) {
  return CURATED_PACK_IDS.has(packId);
}

export function curatedPackLabel(packId, lang = 'en', fallbackMap = null) {
  const key = isZh(lang) ? 'zh' : 'en';
  if (CURATED_PACK_LABELS[packId]) return CURATED_PACK_LABELS[packId][key];
  const fromMap = fallbackMap?.[packId];
  if (fromMap) return typeof fromMap === 'string' ? fromMap : (fromMap[key] || fromMap.en || packId);
  return packId;
}

export function formatBytes(bytes, lang = 'en') {
  if (!Number.isFinite(bytes) || bytes <= 0) return '';
  if (bytes < 1024) return '< 1 KB';
  const locale = isZh(lang) ? 'zh-CN' : 'en-US';
  if (bytes < 1024 * 1024) {
    const kb = bytes / 1024;
    return `${kb.toLocaleString(locale, { maximumFractionDigits: kb < 10 ? 1 : 0 })} KB`;
  }
  const mb = bytes / (1024 * 1024);
  return `${mb.toLocaleString(locale, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} MB`;
}

export function formatTrianglesCompact(triangles) {
  if (!Number.isFinite(triangles) || triangles <= 0) return '';
  if (triangles < 1000) return `${triangles.toLocaleString('en-US')} △`;
  return `${(triangles / 1000).toFixed(1).replace(/\.0$/, '')}k △`;
}

export function formatAttribution(asset, lang = 'en', modelUrl = '') {
  const nameEn = (typeof asset?.name === 'string' ? asset.name : asset?.name?.en) || asset?.id || 'Model';
  const nameZh = (typeof asset?.name === 'object' ? asset?.name?.zh : '') || nameEn;
  const author = asset?.author || 'Leon Made This / s010s';
  const link = modelUrl || asset?.source_url || 'https://github.com/s010s/lowpoly-vault';
  if (isZh(lang)) {
    const title = nameZh && nameEn && nameZh !== nameEn && !nameZh.includes(nameEn)
      ? `${nameZh}（${nameEn}）`
      : nameZh;
    return `「${title}」由 ${author} 创作（${link}），采用 CC BY 4.0 许可协议（https://creativecommons.org/licenses/by/4.0/）。如有修改请注明。`;
  }
  return `"${nameEn}" by ${author} (${link}), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Indicate changes if modified.`;
}

export function buildSearchableText(item, extraNames = []) {
  const parts = [
    item?.id || '',
    (item?.id || '').replace(/[-_.]+/g, ' '),
    ...extraNames,
  ];
  if (typeof item?.name === 'string') parts.push(item.name);
  else if (item?.name && typeof item.name === 'object') parts.push(...Object.values(item.name));
  if (item?.category) parts.push(...categorySearchTerms(item.category));
  if (item?.collection) {
    parts.push(item.collection);
    if (item.collection === 'prehistoric') parts.push('史前', '史前世界');
  }
  if (Array.isArray(item?.worlds)) {
    for (const w of item.worlds) {
      parts.push(w);
      if (w === 'prehistoric') parts.push('史前', '史前世界');
    }
  }
  if (Array.isArray(item?.packs)) {
    for (const p of item.packs) {
      parts.push(p);
      if (CURATED_PACK_LABELS[p]) parts.push(CURATED_PACK_LABELS[p].en, CURATED_PACK_LABELS[p].zh);
    }
  }
  if (item?.description) {
    if (typeof item.description === 'string') parts.push(item.description);
    else parts.push(item.description.en || '', item.description.zh || '');
  }
  if (item?.reconstruction_notes) {
    if (typeof item.reconstruction_notes === 'string') parts.push(item.reconstruction_notes);
    else parts.push(item.reconstruction_notes.en || '', item.reconstruction_notes.zh || '');
  }
  return normalizeText(parts.join(' '));
}

export function getStoredLang() {
  try {
    const value = localStorage.getItem(LANG_STORAGE_KEY);
    return value === 'zh' || value === 'en' ? value : null;
  } catch {
    return null;
  }
}

export function setStoredLang(lang) {
  try {
    localStorage.setItem(LANG_STORAGE_KEY, isZh(lang) ? 'zh' : 'en');
  } catch {}
}

export function getStoredWireframe() {
  try {
    return sessionStorage.getItem(WIREFRAME_STORAGE_KEY) === 'true';
  } catch {
    return false;
  }
}

export function setStoredWireframe(enabled) {
  try {
    sessionStorage.setItem(WIREFRAME_STORAGE_KEY, enabled ? 'true' : 'false');
  } catch {}
}

/** Remove any open manual-copy fallback box attached to a container or button. */
export function clearCopyFallback(anchor, key = '') {
  const parent = anchor?.parentElement;
  if (!parent?.querySelectorAll) return;
  const resolvedKey = key || anchor.id || '';
  for (const box of parent.querySelectorAll('.copy-fallback-box')) {
    if ((box.dataset?.for || '') === resolvedKey) box.remove();
  }
}

/** Show a clean selectable read-only input fallback when navigator.clipboard fails. */
export function showCopyFallback(anchor, text, lang = 'en', { key = '', focusTarget = null } = {}) {
  if (!anchor?.parentElement) return null;
  const resolvedKey = key || anchor.id || '';
  clearCopyFallback(anchor, resolvedKey);
  const returnTarget = focusTarget || anchor;
  const box = document.createElement('div');
  box.className = 'copy-fallback-box';
  box.dataset.for = resolvedKey;
  const hint = document.createElement('span');
  hint.className = 'copy-fallback-hint';
  hint.textContent = isZh(lang) ? '无法自动复制，请按 Ctrl/⌘+C 复制：' : 'Clipboard blocked. Press Ctrl/⌘+C to copy:';
  const row = document.createElement('div');
  row.className = 'copy-fallback-row';
  const input = document.createElement('input');
  input.type = 'text';
  input.readOnly = true;
  input.className = 'copy-fallback-input';
  input.value = text;
  input.setAttribute('aria-label', isZh(lang) ? '可手动复制的文本' : 'Text to copy');
  const close = document.createElement('button');
  close.type = 'button';
  close.className = 'copy-fallback-close';
  close.textContent = '×';
  close.setAttribute('aria-label', isZh(lang) ? '关闭复制框' : 'Dismiss copy box');
  const dismiss = () => {
    box.remove();
    returnTarget?.focus?.({ preventScroll: true });
  };
  close.onclick = dismiss;
  input.addEventListener('keydown', e => {
    if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); dismiss(); }
  });
  row.append(input, close);
  box.append(hint, row);
  anchor.after(box);
  input.focus({ preventScroll: true });
  input.select();
  return box;
}

const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function formatInlineNoticeText(text) {
  const escaped = escapeHtml(text);
  // Render inline code spans and bare https:// URLs safely on already-escaped text.
  return escaped
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/https:\/\/[^\s<)]+[^\s<).,;:'"]/g, url => `<a href="${url}" target="_blank" rel="noopener noreferrer">${url} ↗</a>`);
}

function splitTableRow(line) {
  const trimmed = line.trim().replace(/^\|/, '').replace(/\|$/, '');
  return trimmed.split('|').map(cell => cell.trim());
}

/** Shared safe Markdown -> HTML renderer for THIRD_PARTY_NOTICES.md (headings, lists, code fences, GFM tables, paragraphs). */
export function renderNoticesMarkdown(markdown) {
  const lines = String(markdown || '').replace(/\r\n?/g, '\n').split('\n');
  let html = '';
  let inCode = false;
  let codeLines = [];
  let inList = false;
  const closeList = () => { if (inList) { html += '</ul>'; inList = false; } };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('```')) {
      closeList();
      if (inCode) {
        html += `<pre>${escapeHtml(codeLines.join('\n'))}</pre>`;
        codeLines = [];
        inCode = false;
      } else {
        inCode = true;
      }
      continue;
    }
    if (inCode) {
      codeLines.push(line);
      continue;
    }
    if (!line.trim()) {
      closeList();
      continue;
    }
    if (line.startsWith('# ')) continue;
    if (line.startsWith('## ')) {
      closeList();
      html += `<h2>${formatInlineNoticeText(line.slice(3).trim())}</h2>`;
      continue;
    }
    if (line.startsWith('- ')) {
      if (!inList) { html += '<ul>'; inList = true; }
      html += `<li>${formatInlineNoticeText(line.slice(2).trim())}</li>`;
      continue;
    }
    if (
      line.trim().startsWith('|') &&
      i + 1 < lines.length &&
      /^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?\s*$/.test(lines[i + 1])
    ) {
      closeList();
      const headers = splitTableRow(line);
      i += 2; // Skip header and separator row.
      const rows = [];
      while (i < lines.length && lines[i].trim().startsWith('|')) {
        rows.push(splitTableRow(lines[i]));
        i++;
      }
      i--;
      html += `<div class="notices-table-wrap"><table><thead><tr>${headers.map(h => `<th>${formatInlineNoticeText(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr>${r.map(cell => `<td>${formatInlineNoticeText(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
      continue;
    }
    closeList();
    html += `<p>${formatInlineNoticeText(line.trim())}</p>`;
  }
  if (inCode && codeLines.length) html += `<pre>${escapeHtml(codeLines.join('\n'))}</pre>`;
  closeList();
  return html;
}

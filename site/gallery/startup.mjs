/** Native gallery document: real links and downloads, never an unrelated card grid. */
import { readFile } from 'node:fs/promises';
import { routeHref, CATALOG_PAGE_SIZE } from '../routes.js';
import { modelShortName, galleryCategoryLabel, duplicateZhNames, disambiguatedName } from './presentation-labels.js';
import { primaryDimension } from './model-dimensions.js';
import { formatBytes, formatTrianglesCompact } from '../shared-ui.js';
import { iconMarkup } from './icons.js';
import { resolveGalleryPoster } from './wheel-presentations.js';

const icon = name => `<span class="icon" aria-hidden="true">${iconMarkup(name).replace('<svg ', '<svg width="20" height="20" ')}</span>`;
const escape = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
const local = (value, lang) => typeof value === 'string' ? value : value?.[lang === 'zh-CN' ? 'zh' : 'en'] || value?.en || '';

export async function galleryStartupResources() {
  const [brand, style, critical, script, shell, resources] = await Promise.all([
    readFile(new URL('../brand.css', import.meta.url), 'utf8'),
    readFile(new URL('./style.css', import.meta.url), 'utf8'),
    readFile(new URL('./startup.css', import.meta.url), 'utf8'),
    readFile(new URL('./startup.js', import.meta.url), 'utf8'),
    readFile(new URL('./shell.html', import.meta.url), 'utf8'),
    readFile(new URL('../public/gallery/resources.json', import.meta.url), 'utf8'),
  ]);
  return {
    style: `<style id="gallery-startup-style">${brand}\n${style}\n${critical}</style>`,
    script: `<script id="gallery-startup-init">${script.replace(/<\/script/gi, '<\\/script')}</script>`,
    header: shell.match(/<header[\s\S]*?<\/header>/)[0],
    resources: JSON.parse(resources),
  };
}

export function galleryStartupContent(assets, { lang, base, page = 0, review = false }, startup) {
  const zh = lang === 'zh-CN', t = (en, cn) => zh ? cn : en, pages = Math.max(1, Math.ceil(assets.length / CATALOG_PAGE_SIZE));
  const selected = (!page && assets.find(asset => asset.id === 'cooperoceras')) || assets[Math.min(assets.length - 1, page * CATALOG_PAGE_SIZE)];
  const zhDupes = zh ? duplicateZhNames(assets) : null;
  const poster = (asset, wheel = false) => {
    const resource = resolveGalleryPoster(asset, startup.resources);
    return base + (resource && resource.source_glb_sha256 === asset.sha256?.glb ? resource[wheel ? 'wheel' : 'detail'] : asset.card_preview || asset.preview);
  };
  const detail = asset => routeHref({ type: 'detail', id: asset.id, lang }, base);
  const title = asset => disambiguatedName(asset, lang, zhDupes);
  const subtitle = asset => {
    const cat = galleryCategoryLabel(asset.category, lang);
    if (zh) {
      const enName = (typeof asset.name === 'string' ? asset.name : asset.name?.en || '').trim();
      const display = title(asset);
      if (enName && enName.length <= 34 && !display.toLowerCase().includes(enName.toLowerCase()) && !/teaching|specimen|stylized|form|study$/i.test(enName)) {
        return `${cat} · ${enName}`;
      }
    }
    return cat;
  };
  const glbSize = asset => formatBytes(asset.glb_bytes || asset.file_sizes?.glb || 0, lang) || '—';
  const blendSize = asset => formatBytes(asset.blend_bytes || asset.file_sizes?.blend || 0, lang);
  const compactUnit = d => ({ 'Model height': zh ? '高' : 'tall', 'Model length': zh ? '长' : 'long', 'Model width': zh ? '宽' : 'wide', 'Footprint': '', 'Model size': '' }[d.labelEn] ?? d.label);
  const dim = asset => { const d = primaryDimension(asset, lang); return { ...d, label: compactUnit(d) }; };

  let header = startup.header.replace(/<([a-z][\w:-]*)\b([^>]*\bdata-en="([^"]*)"[^>]*\bdata-zh="([^"]*)"[^>]*)>[\s\S]*?<\/\1>/gi, (_, tag, attrs, en, cn) => `<${tag}${attrs}>${zh ? cn : en}</${tag}>`);
  header = header.replace(/<a\b([^>]*data-gallery-route="(home|about)"[^>]*)>/g, (_, attrs, type) => `<a ${attrs.replace(/\bhref="[^"]*"/g, '')} href="${routeHref({ type, lang }, base)}" data-route="${type}">`);
  // Native first paint keeps the same semantic route links as other documents.
  header = header.replace(/<span aria-current="page"([^>]*)>([\s\S]*?)<\/span>/, `<a href="${routeHref({ type: 'models', lang }, base)}" data-route="catalog" aria-current="page"$1>$2</a>`);
  header = header.replace('GitHub repository (opens in a new tab)', t('GitHub repository (opens in a new tab)', 'GitHub 代码仓库（在新标签页打开）'));
  header = header.replace(/<button id="language"[^>]*>[\s\S]*?<\/button>/, `<a id="language" lang="${zh ? 'en' : 'zh-CN'}" href="${routeHref({ type: 'models', lang: zh ? 'en' : 'zh-CN', page }, base)}" aria-label="${zh ? 'Switch to English' : '切换为简体中文'}">${zh ? 'EN' : '中文'}</a>`);

  const rows = assets.map((asset, index) => {
    const d = dim(asset);
    const meta = galleryCategoryLabel(asset.category, lang);
    return `<a class="slot" href="${detail(asset)}" aria-label="${escape(local(asset.name, lang))}" data-id="${escape(asset.id)}" data-category="${escape(asset.category || '')}" data-selected="${asset === selected}" style="--startup-index:${index}" data-poster="${escape(poster(asset))}" data-title="${escape(title(asset))}" data-subtitle="${escape(subtitle(asset))}" data-triangles="${escape(Number(asset.triangles || 0).toLocaleString('en-US'))}" data-dimensions="${escape(d.value)}" data-dimensions-label="${escape(d.label)}" data-file-size="${escape(glbSize(asset))}" data-blend-size="${escape(blendSize(asset))}" data-download="${escape(base + asset.glb)}" data-blend="${escape(base + asset.blend)}" data-info="${detail(asset)}"><span class="slot-marker" aria-hidden="true"></span><span class="slot-image"><img data-src="${escape(poster(asset, true))}" alt="" width="384" height="384"><noscript><img src="${escape(poster(asset, true))}" alt="" loading="lazy" width="384" height="384"></noscript></span><span class="slot-copy"><strong>${escape(title(asset))}</strong><small>${escape(meta)}</small></span></a>`;
  }).join('');

  // No-JS pagination stays real HTML for crawlers and scriptless browsers without flashing during JS startup.
  const pagination = `<noscript><nav class="startup-pagination" aria-label="${t('Collection pages', '模型分页')}">${page ? `<a rel="prev" href="${routeHref({ type: 'models', lang, page: page - 1 }, base)}">← ${t('Previous', '上一页')}</a>` : ''}<span>${t('Page', '页')} ${page + 1}/${pages}</span>${page + 1 < pages ? `<a rel="next" href="${routeHref({ type: 'models', lang, page: page + 1 }, base)}">${t('Next', '下一页')} →</a>` : ''}</nav></noscript>`;

  const selDim = selected ? dim(selected) : null;
  const workspace = selected
    ? `<section class="workspace"><div class="mobile-detail-actions"><a id="mobile-back" hidden href="${routeHref({ type: 'models', lang, page }, base)}">${t('← All models', '← 全部模型')}</a></div><div class="heading"><div class="title-row"><h1 id="title">${escape(title(selected))}</h1><div class="info-region"><a id="info" href="${detail(selected)}" aria-label="${t('Specimen notes', '标本说明')}">${icon('info')}</a></div></div><p id="subtitle">${escape(subtitle(selected))}</p></div><div class="detail-media"><div id="detail" class="stage"><img id="detail-poster" src="${escape(poster(selected))}" alt="${escape(local(selected.name, lang))}" width="512" height="512" fetchpriority="high"></div></div><div class="workspace-bottom"><div class="tools" aria-label="${t('3D tools available after loading', '加载后可使用 3D 工具')}"><button type="button" disabled>${icon('wireframe')}<span>${t('Wireframe', '线框')}</span></button><button type="button" disabled>${icon('compare')}<span>${t('Scale', '尺寸对比')}</span></button></div><section class="download-card"><div class="metrics"><span class="metric-item"><strong id="triangles">${Number(selected.triangles || 0).toLocaleString('en-US')}</strong><span>${t('tris', '面')}</span></span><span class="metric-sep" aria-hidden="true">·</span><span class="metric-item"><strong id="dimensions">${escape(selDim.value)}</strong><span id="dimensions-label">${escape(selDim.label)}</span></span><span class="metric-sep" aria-hidden="true">·</span><span class="metric-item"><strong id="file-size">${escape(glbSize(selected))}</strong></span></div><div class="download-actions"><a id="download" class="primary" download href="${escape(base + selected.glb)}">${icon('download')}<span>${t('Download GLB', '下载 GLB')}</span></a><a id="blend" class="more-btn startup-blend-link" download href="${escape(base + selected.blend)}" aria-label="${t('Blender source', 'Blender 源文件')}">${icon('source')}</a></div></section></div></section>`
    : '<section class="workspace"></section>';

  const countFormatted = assets.length.toLocaleString(zh ? 'zh-CN' : 'en-US');
  const searchPlaceholder = zh ? `搜索 ${countFormatted} 件展品…` : `Search ${countFormatted} models…`;
  return `<a class="gallery-skip" href="#wheel">${t('Skip to models', '跳至模型列表')}</a>${header}<main><aside class="catalog"><div class="searchbar"><div class="search"><svg class="vault-icon search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg><input type="search" disabled placeholder="${escape(searchPlaceholder)}" aria-label="${t('Interactive search is loading', '交互搜索正在加载')}"><span class="searchbar-divider" aria-hidden="true"></span><button id="filters" type="button" disabled><svg class="vault-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" aria-hidden="true"><path d="M4 7h16M4 17h16"/><circle cx="9" cy="7" r="2" fill="var(--vault-panel,#f9f7f1)"/><circle cx="15" cy="17" r="2" fill="var(--vault-panel,#f9f7f1)"/></svg><span>${t('Filters', '筛选')}</span></button></div></div>${review ? `<div class="summary"><span class="gallery-review-notice">${t('Review candidates · Not approved for publication', '候选审阅 · 未获发布批准')}</span></div>` : ''}<div class="wheel-wrap startup-wheel"><div id="wheel" aria-label="${t('Models', '模型列表')}" tabindex="0"><div id="slots" style="--startup-count:${assets.length}">${rows || `<p class="startup-empty">${t('No approved models are available yet.', '目前还没有已获发布批准的模型。')}</p>`}</div></div><div class="focus-guide focus-guide-right startup-guides" aria-hidden="true"></div></div>${pagination}</aside>${workspace}</main>`;
}

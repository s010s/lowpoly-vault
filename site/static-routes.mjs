/** Real HTML documents for every public route; JavaScript enhances rather than supplies content. */
import { mkdir, readFile, writeFile, rm } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { normalizeSiteBase, routeHref, filterAndSortCatalog, CATALOG_PAGE_SIZE } from './routes.js';
import { createCuration, CATALOG_DATA } from './curation.js';
import { words } from './words.js';
import { homepageStartupStyle } from './home-startup.mjs';
import { galleryStartupResources, galleryStartupContent } from './gallery/startup.mjs';
import {
  HOME_FEATURED_SPECS, categoryLabel, isUserFacingPack, curatedPackLabel, formatBytes, renderNoticesMarkdown,
} from './shared-ui.js';
import { formatDimensionsXYZ, hasMetricDimensions } from './gallery/model-dimensions.js';

const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const localized = (value, lang) => typeof value === 'string' ? value : value?.[lang === 'zh-CN' ? 'zh' : 'en'] || value?.en || '';

const labels = {
  en: {
    models: 'All models', home: 'Home', about: 'About', notices: 'Third-party notices',
    download: 'Download', bundle: 'Complete ZIP', glb: 'Download GLB', blend: 'Blender source',
    credits: 'Attribution text', triangles: 'Triangles', dimensions: 'Dimensions (W × H × D)',
    files: 'Files', category: 'Category', packs: 'Collections', license: 'License',
    previous: 'Previous', next: 'Next', page: 'Page',
    review: 'Review candidates. Visual approval is pending; these models are not approved for publication.',
    empty: 'No approved models are available yet.', scope: 'Scientific scope', sources: 'Sources',
    enhance: 'Inspect in 3D', details: 'Model details',
    credit: 'Credit Leon Made This / s010s, link CC BY 4.0, and indicate changes.',
    aboutText: 'An open library of 1,000 original, editable low-poly 3D models by Leon Made This / s010s. Free for personal and commercial projects under CC BY 4.0 — download ready-to-use GLB files or open the Blender sources to remix them.',
    homeTitle: 'Small polygons. Open possibilities.',
    homeDescription: 'Browse original low-poly 3D models by category and curated collection. Ready-to-use GLB models and editable Blender files under CC BY 4.0.',
    pack: 'Starter collection',
  },
  'zh-CN': {
    models: '全部模型', home: '首页', about: '关于', notices: '第三方许可',
    download: '下载', bundle: '完整 ZIP', glb: '下载 GLB', blend: 'Blender 源文件',
    credits: '署名文本', triangles: '三角面', dimensions: '尺寸（宽 × 高 × 深）',
    files: '文件', category: '分类', packs: '精选合集', license: '许可协议',
    previous: '上一页', next: '下一页', page: '页',
    review: '候选模型仅供审阅。视觉审核尚未完成，未获发布批准。',
    empty: '目前还没有已获发布批准的模型。', scope: '科学说明', sources: '参考来源',
    enhance: '进入 3D 查看', details: '模型详情',
    credit: '请署名 Leon Made This / s010s，附上 CC BY 4.0 许可链接，并注明所作修改。',
    aboutText: '由 Leon Made This / s010s 创作的 1,000 个原创低多边形 3D 模型开放库。所有模型均采用 CC BY 4.0 许可，个人与商业项目均可免费使用——可直接下载 GLB 投入项目，也可打开 Blender 源文件自由二次创作。',
    homeTitle: '小小多边形，无限可能。',
    homeDescription: '按分类和精选合集探索原创低多边形 3D 模型。提供开箱即用的 GLB 模型与可编辑 Blender 文件，遵循 CC BY 4.0 署名许可。',
    pack: '史前入门精选',
  },
};

const style = `<style id="static-route-style">.static-route{max-width:1240px;margin:48px auto 84px;padding:0 32px;color:var(--vault-ink,#262a25);font-family:var(--vault-font-ui,Arial,sans-serif)}.static-route a{color:inherit}.static-route h1{font-family:var(--vault-font-display,Georgia,serif);font-weight:400;font-size:clamp(34px,4.5vw,58px);line-height:1.08;letter-spacing:-.035em;margin:16px 0}.static-route h2{font-family:var(--vault-font-display,Georgia,serif);font-weight:400;font-size:22px;margin-top:30px}.static-route p{line-height:1.7;max-width:74ch}.static-breadcrumbs{font-size:13px;display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px;color:var(--vault-muted)}.static-detail{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:44px;align-items:start}.static-preview{width:100%;border-radius:14px;background:#e8ece4;aspect-ratio:1;object-fit:contain}.static-kicker{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--vault-muted)}.static-specs{display:grid;grid-template-columns:minmax(130px,1fr) 2fr;gap:12px;margin:24px 0;font-size:14px}.static-specs dt{color:var(--vault-muted)}.static-specs dd{margin:0}.static-downloads{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}.static-downloads a,.static-button{display:inline-block;padding:12px 18px;border:1px solid var(--vault-line,currentColor);border-radius:9px;text-decoration:none;background:transparent;font:inherit;cursor:pointer}.static-downloads a:first-child{background:var(--vault-accent,#305742);color:var(--vault-on-accent,#fff);border-color:var(--vault-accent,#305742)}.static-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px;margin:26px 0}.static-card{text-decoration:none}.static-card img{width:100%;aspect-ratio:1;object-fit:contain;border-radius:10px;background:#e8ece4}.static-card h2{font-size:17px;margin:10px 0 3px}.static-card p{font-size:12px;margin:0;color:var(--vault-muted)}.static-pagination{display:flex;gap:24px;align-items:center;margin:32px 0}.static-review{padding:12px 16px;border:1px solid #b89045;border-radius:8px;font-size:13px}.static-axes{display:flex;gap:12px;flex-wrap:wrap;margin-top:20px}.static-axes a{padding:9px 15px;border:1px solid var(--vault-line,#a0a69e);border-radius:20px;font-size:13px;text-decoration:none}.static-license{font-size:13px;color:var(--vault-muted)}.static-route pre{padding:16px;border-radius:10px;border:1px solid var(--vault-line);background:var(--vault-panel);overflow-x:auto;font-size:12px;line-height:1.55}.static-route .notices-table-wrap{overflow-x:auto;margin:18px 0}.static-route table{width:100%;border-collapse:collapse;font-size:13px;background:var(--vault-panel)}.static-route th,.static-route td{padding:9px 12px;border:1px solid var(--vault-line,#d9d6cd);text-align:left;vertical-align:top}.static-route th{background:var(--vault-surface,#f6f3ec);font-weight:600}.static-route [hidden]{display:none!important}@media(max-width:800px){.static-route{padding:0 18px;margin-top:28px}.static-detail{grid-template-columns:1fr;gap:24px}.static-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}</style>`;

// Models are emitted in their actual gallery geometry, with inlined production
// styles and real linked content. No application dependency gates the first paint.
// Keep .top-actions (GitHub + real #language link) visible without JS; hide only JS-only controls.
const noScriptStyle = '<noscript><style>body{margin:0;background:var(--vault-surface,#f6f3ec);color:var(--vault-ink,#262a25);font-family:var(--vault-font-ui,Arial,sans-serif)}body>.skip,.theme-toggle,#main-content,#site-toast,#announcement{display:none!important}.static-route{font-family:var(--vault-font-ui,Arial,sans-serif)}.static-route h1,.static-route h2{font-family:var(--vault-font-display,Georgia,serif);font-weight:400}</style></noscript>';

function cards(assets, lang, base) {
  const locale = lang === 'zh-CN' ? 'zh-CN' : 'en-US';
  return `<div class="static-grid">${assets.map(asset => `<a class="static-card" href="${routeHref({ type: 'detail', id: asset.id, lang }, base)}"><img src="${base}${escape(asset.card_preview || asset.preview)}" alt="${escape(localized(asset.name, lang))}" loading="lazy" width="400" height="400"><h2>${escape(localized(asset.name, lang))}</h2><p>${escape(categoryLabel(asset.category, lang))} · ${escape(Number(asset.triangles || 0).toLocaleString(locale))} ${labels[lang].triangles}</p></a>`).join('')}</div>`;
}

function downloadLinks(asset, lang, base) {
  const t = labels[lang];
  const order = ['glb', 'blend', 'bundle'].filter(key => asset.downloads?.[key]);
  return `<div class="static-downloads">${order.map(key => {
    const size = formatBytes(asset.file_sizes?.[key] || (key === 'glb' ? asset.glb_bytes : key === 'blend' ? asset.blend_bytes : 0), lang);
    return `<a download href="${base}${escape(asset.downloads[key])}">${t[key]}${size ? ` · ${escape(size)}` : ''}</a>`;
  }).join('')}</div>${asset.downloads?.credits ? `<a download href="${base}${escape(asset.downloads.credits)}">${t.credits}</a>` : ''}`;
}

function detailContent(asset, lang, base, { catalogMembership, PACK_LABELS }) {
  const t = labels[lang], membership = catalogMembership(asset);
  const locale = lang === 'zh-CN' ? 'zh-CN' : 'en-US';
  const curatedPacks = membership.packs.filter(isUserFacingPack);
  const packLinks = curatedPacks.map(id => `<a href="${escape(routeHref({ type: 'models', lang, query: { pack: id } }, base))}">${escape(curatedPackLabel(id, lang, PACK_LABELS))}</a>`).join(', ');
  const specs = [
    [t.triangles, Number.isFinite(asset.triangles) ? asset.triangles.toLocaleString(locale) : ''],
    [t.dimensions, hasMetricDimensions(asset) ? formatDimensionsXYZ(asset) : null],
  ];
  const filesSummary = ['glb', 'blend']
    .map(key => {
      const bytes = asset.file_sizes?.[key] || (key === 'glb' ? asset.glb_bytes : asset.blend_bytes);
      const formatted = formatBytes(bytes, lang);
      return formatted ? `${key.toUpperCase()}: ${formatted}` : null;
    })
    .filter(Boolean)
    .join(' · ');
  const validSources = (asset.sources || []).filter(source => /^https?:\/\//.test(source.url || ''));
  return `<nav class="static-breadcrumbs" aria-label="Breadcrumb"><a href="${routeHref({ type: 'home', lang }, base)}">${t.home}</a><span>/</span><a href="${routeHref({ type: 'models', lang }, base)}">${t.models}</a><span>/</span><span>${escape(localized(asset.name, lang))}</span></nav><div class="static-detail"><div><img class="static-preview" src="${base}${escape(asset.card_preview || asset.preview)}" alt="${escape(localized(asset.name, lang))}" width="900" height="900"></div><section><span class="static-kicker">${t.details} · CC BY 4.0</span><h1>${escape(localized(asset.name, lang))}</h1><p>${escape(localized(asset.description, lang))}</p><dl class="static-specs"><dt>${t.category}</dt><dd><a href="${escape(routeHref({ type: 'models', lang, query: { category: asset.category } }, base))}">${escape(categoryLabel(asset.category, lang))}</a></dd>${packLinks ? `<dt>${t.packs}</dt><dd>${packLinks}</dd>` : ''}${specs.filter(([, value]) => value).map(([name, value]) => `<dt>${name}</dt><dd>${escape(value)}</dd>`).join('')}${filesSummary ? `<dt>${t.files}</dt><dd>${escape(filesSummary)}</dd>` : ''}<dt>${t.license}</dt><dd><a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0 ↗</a></dd></dl>${downloadLinks(asset, lang, base)}<p class="static-license">${t.credit}</p></section></div>${localized(asset.scientific_scope, lang) ? `<h2>${t.scope}</h2><p>${escape(localized(asset.scientific_scope, lang))}</p>` : ''}${validSources.length ? `<h2>${t.sources}</h2><ul>${validSources.map(source => `<li><a href="${escape(source.url)}" rel="noopener noreferrer">${escape(source.title || source.url)} ↗</a></li>`).join('')}</ul>` : ''}`;
}

function metadata(template, { title, description, url, alternateEN, alternateZH, image, lang, review, asset, base }) {
  let html = template
    .replace(/<html\b[^>]*>/, '<html lang="' + lang + '">')
    .replace(/<title>[\s\S]*?<\/title>/i, '')
    .replace(/<meta\b[^>]*(?:name=["'](?:description|robots)["']|property=["']og:[^"']+["'])[^>]*>/gi, '')
    .replace(/<link\b[^>]*rel=["'](?:canonical|alternate)["'][^>]*>/gi, '');
  const schema = asset ? {
    '@context': 'https://schema.org', '@type': 'CreativeWork',
    name: localized(asset.name, lang), description: localized(asset.description, lang),
    url, image, license: 'https://creativecommons.org/licenses/by/4.0/',
    creator: { '@type': 'Person', name: asset.author || 'Leon Made This / s010s' },
    encoding: ['glb', 'blend'].filter(k => asset.downloads?.[k]).map(k => ({
      '@type': 'MediaObject',
      encodingFormat: k === 'glb' ? 'model/gltf-binary' : 'application/x-blender',
      contentUrl: new URL(asset.downloads[k], new URL(url).origin + base).href,
    })),
  } : null;
  const head = `<title>${escape(title)}</title><meta name="description" content="${escape(description)}"><meta name="robots" content="${review ? 'noindex,nofollow' : 'index,follow'}"><link rel="canonical" href="${escape(url)}"><link rel="alternate" hreflang="en" href="${escape(alternateEN)}"><link rel="alternate" hreflang="zh-CN" href="${escape(alternateZH)}"><link rel="alternate" hreflang="x-default" href="${escape(alternateEN)}"><meta property="og:type" content="${asset ? 'article' : 'website'}"><meta property="og:site_name" content="Lowpoly Vault"><meta property="og:title" content="${escape(title)}"><meta property="og:description" content="${escape(description)}"><meta property="og:url" content="${escape(url)}"><meta property="og:locale" content="${lang === 'zh-CN' ? 'zh_CN' : 'en_US'}">${image ? `<meta property="og:image" content="${escape(image)}">` : ''}${schema ? `<script type="application/ld+json">${JSON.stringify(schema).replace(/</g, '\\u003c')}</script>` : ''}${style}`;
  return html.replace('</head>', head + '</head>');
}

function renderHomeCategoriesStatic(assets, lang, base) {
  const byId = new Map(assets.map(a => [a.id, a]));
  const counts = new Map();
  for (const a of assets) counts.set(a.category, (counts.get(a.category) || 0) + 1);
  const locale = lang === 'zh-CN' ? 'zh-CN' : 'en-US';
  const unit = lang === 'zh-CN' ? '个模型' : 'models';
  return HOME_FEATURED_SPECS.map(spec => {
    const pick = byId.get(spec.id) || assets.find(a => a.category === spec.category);
    if (!pick) return '';
    const count = (counts.get(spec.category) || 0).toLocaleString(locale);
    return `<a class="curation-card" href="${escape(routeHref({ type: 'models', lang, query: { category: spec.category } }, base))}" data-home-category="${escape(spec.category)}"><div><img src="${base}${escape(pick.card_preview || pick.preview)}" alt="${escape(localized(pick.name, lang))}" loading="lazy" width="640" height="640"><span class="curation-number">${escape(spec.num)}</span></div><span class="curation-title">${escape(categoryLabel(spec.category, lang))}<span>${escape(count)} ${unit} →</span></span></a>`;
  }).join('');
}

export async function writeStaticRoutes(manifest, outDir, { base = process.env.SITE_BASE || '/', origin = process.env.SITE_ORIGIN || 'https://s010s.github.io', catalogData = CATALOG_DATA } = {}) {
  const curation = createCuration(catalogData), { catalogMembership } = curation;
  base = normalizeSiteBase(base);
  origin = new URL(origin).origin;
  const template = await readFile(resolve(outDir, 'index.html'), 'utf8');
  const galleryStartup = await galleryStartupResources();
  const homeStartup = await homepageStartupStyle();
  let noticesMarkdown = '';
  try { noticesMarkdown = await readFile(resolve(outDir, 'THIRD_PARTY_NOTICES.md'), 'utf8'); } catch {
    try { noticesMarkdown = await readFile(resolve('THIRD_PARTY_NOTICES.md'), 'utf8'); } catch {}
  }
  const noticesRendered = renderNoticesMarkdown(noticesMarkdown);
  const assets = filterAndSortCatalog(manifest?.assets || []), review = manifest?.review_only === true;
  for (const directory of ['models', 'zh-CN', 'about', 'notices']) await rm(resolve(outDir, directory), { recursive: true, force: true });
  const urls = [];

  async function emit(route, content, title, description, asset) {
    const href = routeHref(route, base), url = origin + href;
    let html = metadata(template, {
      title, description, url,
      alternateEN: origin + routeHref({ ...route, lang: 'en' }, base),
      alternateZH: origin + routeHref({ ...route, lang: 'zh-CN' }, base),
      image: asset ? origin + base + asset.preview : assets[0] ? origin + base + assets[0].preview : undefined,
      lang: route.lang, review, asset, base,
    });
    if (route.type === 'home') html = html.replace('</head>', homeStartup + '</head>');
    if (route.type === 'models') html = html.replace('<html lang="' + route.lang + '">', '<html lang="' + route.lang + '" data-application="gallery">').replace('</head>', galleryStartup.style + '</head>');
    html = html.replace(/<body\b([^>]*)>/, `<body$1 data-static-route="${route.type}"${review ? ' data-review-only="true"' : ''} data-site-base="${escape(base)}">`);
    html = html.replace(/(<a\b[^>]*?)href=["'][^"']*["']([^>]*data-route=["'](home|catalog|models|about|notices)["'][^>]*>)/g, (_, start, rest, type) => `${start}href="${routeHref({ type, lang: route.lang }, base)}"${rest}`);
    html = html.replace(/(<a\b[^>]*?)href=["'][^"']*["']([^>]*data-browse[^>]*>)/g, (_, start, rest) => `${start}href="${routeHref({ type: 'models', lang: route.lang }, base)}"${rest}`);
    html = html.replace(/(<a\b[^>]*?)href=["'][^"']*["']([^>]*data-route-detail=["']([^"']+)["'][^>]*>)/g, (_, start, rest, id) => `${start}href="${routeHref({ type: 'detail', id, lang: route.lang }, base)}"${rest}`);
    html = html.replace(/(?:src|href)="\.\/home\/([^"]+)"/g, match => match.replace('./home/', base + 'home/'));
    const dictionary = words[route.lang === 'zh-CN' ? 'zh' : 'en'];
    html = html.replace(/<([a-z][\w:-]*)\b([^>]*\bdata-t="([^"]+)"[^>]*)>[\s\S]*?<\/\1>/gi, (whole, tag, attributes, key) => dictionary[key] ? `<${tag}${attributes}>${dictionary[key]}</${tag}>` : whole);
    // Bake exact formatted total into home CTA so there is zero hydration width jump.
    if (route.type === 'home' && assets.length) {
      const totalStr = assets.length.toLocaleString(route.lang === 'zh-CN' ? 'zh-CN' : 'en-US');
      const ctaCopy = route.lang === 'zh-CN' ? `浏览全部 ${totalStr} 个模型` : `Explore all ${totalStr} models`;
      html = html.replace(/(<span\b[^>]*data-t="exploreAll"[^>]*>)[\s\S]*?(<\/span>)/g, `$1${ctaCopy}$2`);
      html = html.replace('<div class="curation-grid" id="home-categories"></div>', `<div class="curation-grid" id="home-categories">${renderHomeCategoriesStatic(assets, route.lang, base)}</div>`);
    }
    if (route.lang === 'zh-CN') {
      html = html
        .replace('GitHub repository (opens in a new tab)', 'GitHub 代码仓库（在新标签页打开）')
        .replace(
          /(<input\b[^>]*id="home-query"[^>]*?)placeholder="[^"]*"([^>]*?)aria-label="[^"]*"/,
          `$1placeholder="${escape(dictionary.homeSearch)}"$2aria-label="${escape(dictionary.homeSearch)}"`,
        );
    }
    const otherLang = route.lang === 'zh-CN' ? 'en' : 'zh-CN';
    const langSwitchHtml = `<a id="language" lang="${otherLang}" href="${routeHref({ ...route, lang: otherLang }, base)}" aria-label="${route.lang === 'zh-CN' ? 'Switch to English' : '切换为简体中文'}">${route.lang === 'zh-CN' ? 'EN' : '中文'}</a>`;
    html = html.replace(/<(?:a|button)\b[^>]*id="language"[^>]*>[\s\S]*?<\/(?:a|button)>/, langSwitchHtml);
    if (route.type !== 'home') html = html.replace(/(<(?:section|div|main)[^>]*id="(?:home-page|about-page|notices-page|detail-page)"[^>]*)(>)/g, (all, start, end) => /\bhidden\b/.test(start) ? all : start + ' hidden' + end);
    const article = `<article id="static-route-content" class="static-route" data-route-type="${route.type}" data-asset-id="${asset?.id || ''}" data-lang="${route.lang}">${review ? `<p class="static-review">${labels[route.lang].review}</p>` : ''}${content}</article>`;
    if (route.type === 'models') {
      const body = html.match(/<body\b[^>]*>([\s\S]*?)<\/body>/)?.[1] || '';
      const modules = [...body.matchAll(/<script\b[^>]*type=["']module["'][^>]*>[\s\S]*?<\/script>/gi)].map(match => match[0]).join('');
      const gallery = `<article id="static-route-content" class="gallery-static" data-route-type="models" data-lang="${route.lang}">${galleryStartupContent(manifest?.assets || [], { ...route, base, review }, galleryStartup)}</article>`;
      html = html.replace(/(<body\b[^>]*>)[\s\S]*?<\/body>/, (_, opening) => opening + gallery + noScriptStyle + galleryStartup.script + modules + '</body>');
    } else {
      html = html.replace(/<noscript>[\s\S]*?<\/noscript>/gi, '').replace('</body>', noScriptStyle + article + '</body>');
    }
    const pathname = href.slice(base.length);
    const file = resolve(outDir, pathname, 'index.html');
    await mkdir(dirname(file), { recursive: true });
    await writeFile(file, html);
    urls.push(url);
  }

  for (const lang of ['en', 'zh-CN']) {
    const t = labels[lang];
    const nameCounts = new Map();
    if (lang === 'zh-CN') for (const asset of assets) { const name = localized(asset.name, lang); nameCounts.set(name, (nameCounts.get(name) || 0) + 1); }
    const titleName = asset => { const name = localized(asset.name, lang); return nameCounts.get(name) > 1 ? `${name} (${asset.id})` : name; };
    await emit(
      { type: 'home', lang },
      `<h1>${t.homeTitle}</h1><p>${t.homeDescription}</p><div class="static-axes"><a href="${routeHref({ type: 'models', lang }, base)}">${t.models} (${assets.length.toLocaleString(lang === 'zh-CN' ? 'zh-CN' : 'en-US')})</a>${assets.some(a => catalogMembership(a).packs.includes('prehistoric-starter')) ? `<a href="${escape(routeHref({ type: 'models', lang, query: { pack: 'prehistoric-starter' } }, base))}">${t.pack}</a>` : ''}<a href="${routeHref({ type: 'about', lang }, base)}">${t.about}</a></div>${assets.length ? cards(assets.slice(0, 8), lang, base) : `<p>${t.empty}</p>`}`,
      `Lowpoly Vault · ${t.homeTitle}`,
      t.homeDescription,
    );
    const pages = Math.max(1, Math.ceil(assets.length / CATALOG_PAGE_SIZE));
    for (let page = 0; page < pages; page++) {
      await emit(
        { type: 'models', lang, page },
        `<nav class="static-breadcrumbs"><a href="${routeHref({ type: 'home', lang }, base)}">${t.home}</a></nav><h1>${t.models}</h1><p>${assets.length} ${lang === 'en' ? 'original low-poly models' : '个原创低多边形模型'} · ${t.page} ${page + 1}/${pages}</p>${assets.length ? cards(assets.slice(page * CATALOG_PAGE_SIZE, (page + 1) * CATALOG_PAGE_SIZE), lang, base) : `<p>${t.empty}</p>`}<nav class="static-pagination" aria-label="${t.page}">${page ? `<a rel="prev" href="${routeHref({ type: 'models', lang, page: page - 1 }, base)}">← ${t.previous}</a>` : ''}<span>${t.page} ${page + 1}/${pages}</span>${page + 1 < pages ? `<a rel="next" href="${routeHref({ type: 'models', lang, page: page + 1 }, base)}">${t.next} →</a>` : ''}</nav>`,
        `${t.models}${page ? ` · ${t.page} ${page + 1}` : ''} | Lowpoly Vault`,
        t.homeDescription,
      );
    }
    await emit(
      { type: 'about', lang },
      `<h1>${t.about} Lowpoly Vault</h1><p>${t.aboutText}</p><p>${t.credit}</p><div class="static-axes"><a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0 ↗</a><a href="https://github.com/s010s/lowpoly-vault">GitHub ↗</a><a href="${routeHref({ type: 'notices', lang }, base)}">${t.notices}</a><a href="${routeHref({ type: 'models', lang }, base)}">${t.models}</a></div>`,
      `${t.about} | Lowpoly Vault`,
      t.aboutText,
    );
    await emit(
      { type: 'notices', lang },
      `<nav class="static-breadcrumbs"><a href="${routeHref({ type: 'home', lang }, base)}">${t.home}</a><span>/</span><a href="${routeHref({ type: 'about', lang }, base)}">${t.about}</a><span>/</span><span>${t.notices}</span></nav><h1>${t.notices}</h1><div class="notices-rendered">${noticesRendered}</div>`,
      `${t.notices} | Lowpoly Vault`,
      t.aboutText,
    );
    for (const asset of assets) {
      await emit(
        { type: 'detail', lang, id: asset.id },
        detailContent(asset, lang, base, curation),
        `${titleName(asset)} · ${lang === 'en' ? 'Low-poly 3D model' : '低多边形 3D 模型'} | Lowpoly Vault`,
        localized(asset.description, lang),
        asset,
      );
    }
  }

  const brandHead = (template.match(/<link\b[^>]*rel="(?:icon|stylesheet)"[^>]*>/g) || []).join('');
  const brandLink = (template.match(/<a\b[^>]*class="brand vault-brand"[^>]*>[\s\S]*?<\/a>/) || [''])[0].replace(/href="[^"]*"/, `href="${routeHref({ type: 'home' }, base)}"`);
  const notFoundStyle = `<style>.nf-search{display:flex;gap:10px;max-width:520px;margin:24px 0 28px;padding:6px 8px 6px 14px;border:1px solid var(--vault-line,#d9d6cd);border-radius:9px;background:var(--vault-panel,#f9f7f1)}.nf-search input{flex:1;min-width:0;border:0;background:transparent;color:var(--vault-ink,#262a25);font:16px/1.4 var(--vault-font-ui,Arial,sans-serif);outline:none}.nf-search button{padding:10px 16px;border:0;border-radius:6px;background:var(--vault-accent,#305742);color:var(--vault-on-accent,#fff);font:13px var(--vault-font-ui,Arial,sans-serif);cursor:pointer;white-space:nowrap}.nf-actions{display:flex;gap:12px;flex-wrap:wrap}.nf-actions a{padding:11px 18px;border:1px solid var(--vault-line,#d9d6cd);border-radius:9px;text-decoration:none;font-size:14px}.nf-actions a.primary{background:var(--vault-accent,#305742);border-color:var(--vault-accent,#305742);color:var(--vault-on-accent,#fff)}</style>`;
  const notFound = `<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Lowpoly Vault</title><meta name="robots" content="noindex,follow"><meta name="description" content="This Lowpoly Vault page could not be found. Search the library or browse all models.">${brandHead}${style}${notFoundStyle}<script>try{var t=localStorage.getItem("vault-theme");document.documentElement.dataset.theme=t==="light"||t==="dark"?t:matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";}catch{document.documentElement.dataset.theme=matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";}</script></head><body style="margin:0;background:var(--vault-surface,#f6f3ec);color:var(--vault-ink,#262a25)"><header class="topbar">${brandLink}<nav class="primary-nav" aria-label="Primary"><a id="nf-nav-home" href="${routeHref({ type: 'home' }, base)}">Home</a><a id="nf-nav-models" href="${routeHref({ type: 'models' }, base)}">All models</a><a id="nf-nav-about" href="${routeHref({ type: 'about' }, base)}">About</a></nav></header><main class="static-route"><h1 id="nf-title">Page not found</h1><p id="nf-desc">The link may be outdated, or this model isn’t published yet. Try searching the library below.</p><form id="nf-form" class="nf-search" action="${routeHref({ type: 'models' }, base)}" method="get"><input id="nf-q" name="q" type="search" autocomplete="off" placeholder="Search models…" aria-label="Search models"><button id="nf-submit" type="submit">Search →</button></form><div class="nf-actions"><a id="nf-models" class="primary" href="${routeHref({ type: 'models' }, base)}">Browse all models →</a><a id="nf-home" href="${routeHref({ type: 'home' }, base)}">Back to home</a></div></main><script>(function(){var base=${JSON.stringify(base)},zh=location.pathname.indexOf("/zh-CN/")>=0;if(!zh){try{var saved=localStorage.getItem("vault-lang");zh=saved==="zh"||(!saved&&/^zh/i.test(navigator.language||""));}catch{}}if(!zh)return;document.documentElement.lang="zh-CN";document.title="找不到这个页面 | Lowpoly Vault";var set=function(id,text,href){var el=document.getElementById(id);if(!el)return;if(text)el.textContent=text;if(href)el.href=href;};var brand=document.querySelector(".vault-brand");if(brand)brand.href=base+"zh-CN/";set("nf-nav-home","首页",base+"zh-CN/");set("nf-nav-models","全部模型",base+"zh-CN/models/");set("nf-nav-about","关于",base+"zh-CN/about/");set("nf-title","找不到这个页面");set("nf-desc","链接可能已失效，或该模型尚未发布。你可以直接搜索想找的模型：");set("nf-submit","搜索 →");set("nf-models","浏览全部模型 →",base+"zh-CN/models/");set("nf-home","返回首页",base+"zh-CN/");var f=document.getElementById("nf-form"),q=document.getElementById("nf-q");if(f)f.action=base+"zh-CN/models/";if(q){q.placeholder="搜索模型名称、分类或关键词…";q.setAttribute("aria-label","搜索模型");}})();</script></body></html>`;
  await writeFile(resolve(outDir, '404.html'), notFound);
  await writeFile(resolve(outDir, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls.map(url => `<url><loc>${escape(url)}</loc></url>`).join('')}</urlset>\n`);
  await writeFile(resolve(outDir, 'robots.txt'), `User-agent: *\n${review ? 'Disallow: /' : `Allow: /\nSitemap: ${origin}${base}sitemap.xml`}\n`);
  return { pages: urls.length, models: assets.length, urls };
}

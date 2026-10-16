/** Deployment-aware URLs and catalog query semantics shared by static builds and the browser. */
export const CATALOG_PAGE_SIZE = 24;
export const normalizeText = value => String(value ?? '').normalize('NFKC').toLocaleLowerCase();
export const validAssetId = id => typeof id === 'string' && /^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(id);
export function normalizeSiteBase(base = '/') {
  if (typeof base !== 'string' || /[?#\\\u0000-\u001f]/.test(base) || !base.startsWith('/') || base.startsWith('//') || base.split('/').some(p => p === '.' || p === '..')) throw new Error('SITE_BASE must be an absolute path prefix.');
  return `${base.replace(/\/+$/, '')}/`;
}
export function routeHref({ type = 'home', lang = 'en', id, page = 0, query } = {}, root = '/') {
  root = normalizeSiteBase(root);
  const prefix = lang === 'zh-CN' || lang === 'zh' ? 'zh-CN/' : '';
  let suffix = '';
  if (type === 'detail') { if (!validAssetId(id)) throw new Error('Invalid asset id.'); suffix = `models/${encodeURIComponent(id)}/`; }
  else if (type === 'models' || type === 'catalog') suffix = `models/${page > 0 ? `page/${Math.floor(page) + 1}/` : ''}`;
  else if (type === 'about') suffix = 'about/';
  else if (type !== 'home') throw new Error('Unknown route type.');
  const params = query ? queryToParams(query) : new URLSearchParams();
  // The pathname owns pagination; the query is only search/filter/sort.
  params.delete('page');
  return root + prefix + suffix + (params.size ? `?${params}` : '');
}
export function parseRoute(pathname, root = '/') {
  root = normalizeSiteBase(root);
  let path;
  try { path = new URL(pathname, 'https://route.invalid').pathname; } catch { return { type: 'not-found', lang: 'en' }; }
  if (path === root.slice(0, -1)) path += '/';
  if (!path.startsWith(root)) return { type: 'not-found', lang: 'en' };
  path = path.slice(root.length).replace(/index\.html$/, '').replace(/^\/+|\/+$/g, '');
  let lang = 'en';
  if (path === 'zh-CN' || path.startsWith('zh-CN/')) { lang = 'zh-CN'; path = path.slice(5).replace(/^\//, ''); }
  if (!path) return { type: 'home', lang, page: 0 };
  if (path === 'about') return { type: 'about', lang, page: 0 };
  if (path === 'models') return { type: 'models', lang, page: 0 };
  const page = path.match(/^models\/page\/([1-9]\d*)$/);
  if (page && Number.isSafeInteger(Number(page[1]))) return { type: 'models', lang, page: Number(page[1]) - 1 };
  const detail = path.match(/^models\/([^/]+)$/);
  if (detail && validAssetId(detail[1])) return { type: 'detail', lang, id: detail[1], page: 0 };
  return { type: 'not-found', lang };
}
export function queryFromParams(value = '') {
  const params = value instanceof URLSearchParams ? value : new URLSearchParams(value);
  const sort = params.get('sort');
  return { query: params.get('q') || '', category: params.get('category') || 'all', world: params.get('world') || 'all', pack: params.get('pack') || 'all', collection: params.get('collection') || 'all', sort: ['name', 'name-desc', 'triangles-asc', 'triangles-desc'].includes(sort) ? sort : 'name', view: params.get('view') === 'map' ? 'map' : 'grid', maxTriangles: Math.max(0, Number(params.get('maxTriangles')) || 0), page: Math.max(0, (Number.parseInt(params.get('page'), 10) || 1) - 1) };
}
export function queryToParams(options = {}) {
  const params = new URLSearchParams();
  if (options.query?.trim()) params.set('q', options.query.trim());
  for (const key of ['category', 'world', 'pack', 'collection']) if (options[key] && options[key] !== 'all') params.set(key, options[key]);
  if (options.sort && options.sort !== 'name') params.set('sort', options.sort);
  if (options.view === 'map') params.set('view', 'map');
  if (Number.isFinite(Number(options.maxTriangles)) && Number(options.maxTriangles) > 0) params.set('maxTriangles', String(Number(options.maxTriangles)));
  if (options.page > 0) params.set('page', String(Math.floor(options.page) + 1));
  return params;
}
export const itemWorlds = item => Array.isArray(item.worlds) ? item.worlds : [item.collection].filter(Boolean);
export const itemPacks = item => Array.isArray(item.packs) ? item.packs : [];
export function matchesCatalogItem(item, { query = '', category = 'all', collection = 'all', world = 'all', pack = 'all', maxTriangles = 0 } = {}) {
  if (Number(maxTriangles) > 0 && (!Number.isFinite(item.triangles) || item.triangles > Number(maxTriangles))) return false;
  const terms = normalizeText(query).trim().split(/\s+/).filter(Boolean);
  const has = value => value && value !== 'all';
  if ((has(category) && item.category !== category) || (has(collection) && item.collection !== collection) || (has(world) && !itemWorlds(item).includes(world)) || (has(pack) && !itemPacks(item).includes(pack))) return false;
  const searchable = normalizeText([item.id, ...Object.values(typeof item.name === 'object' ? item.name : { en: item.name }), item.category, item.collection, ...itemWorlds(item), ...itemPacks(item)].join(' '));
  return terms.every(term => searchable.includes(term));
}
const collator = new Intl.Collator('en', { numeric: true, sensitivity: 'base' });
const nameOf = item => typeof item.name === 'string' ? item.name : item.name?.en || item.id;
export const compareCatalogNames = (a, b) => collator.compare(nameOf(a), nameOf(b)) || collator.compare(a.id, b.id);
export function itemComparator(sort = 'name') {
  if (sort === 'name-desc') return (a, b) => compareCatalogNames(b, a);
  if (sort === 'triangles-asc' || sort === 'triangles-desc') return (a, b) => {
    const av = Number.isFinite(a.triangles) ? a.triangles : Infinity, bv = Number.isFinite(b.triangles) ? b.triangles : Infinity;
    if (av === Infinity || bv === Infinity) return (av === bv ? 0 : av === Infinity ? 1 : -1) || compareCatalogNames(a, b);
    return (sort === 'triangles-desc' ? bv - av : av - bv) || compareCatalogNames(a, b);
  };
  return compareCatalogNames;
}
export function filterAndSortCatalog(items, options = {}) { return items.filter(item => matchesCatalogItem(item, options)).sort(itemComparator(options.sort)); }

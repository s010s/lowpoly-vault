/** Lazy, paginated static catalog. Full metadata is fetched only for an opened asset. */
const collator = new Intl.Collator('en', { numeric: true, sensitivity: 'base' });
const normalize = value => String(value ?? '').normalize('NFKC').toLocaleLowerCase();
const abortError = () => new DOMException('Catalog request superseded.', 'AbortError');
const nameOf = item => typeof item.name === 'string' ? item.name : item.name?.en || item.id;
const byName = (a, b) => collator.compare(nameOf(a), nameOf(b)) || collator.compare(a.id, b.id);
const validId = id => typeof id === 'string' && /^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(id);

function cachePut(cache, key, value, limit) {
  cache.delete(key);
  cache.set(key, value);
  while (cache.size > limit) cache.delete(cache.keys().next().value);
}
function cacheGet(cache, key) {
  if (!cache.has(key)) return undefined;
  const value = cache.get(key);
  cache.delete(key);
  cache.set(key, value);
  return value;
}
function safeRelativePath(path) {
  if (typeof path !== 'string' || !path.startsWith('assets/') || /[\\\u0000-\u001f?#%]/.test(path)) return false;
  return !path.split('/').some(part => part === '.' || part === '..');
}
function isItem(item) {
  return item && validId(item.id) && item.name && typeof item.category === 'string' &&
    typeof item.collection === 'string' && safeRelativePath(item.preview) && safeRelativePath(item.glb) && safeRelativePath(item.detail);
}

// A bounded max-heap retains only the best entries needed for the requested sorted page.
function retainBest(heap, item, limit, compare) {
  if (heap.length < limit) {
    heap.push(item);
    let child = heap.length - 1;
    while (child > 0) {
      const parent = Math.floor((child - 1) / 2);
      if (compare(heap[parent], heap[child]) >= 0) break;
      [heap[parent], heap[child]] = [heap[child], heap[parent]];
      child = parent;
    }
    return;
  }
  if (compare(item, heap[0]) >= 0) return;
  heap[0] = item;
  let parent = 0;
  while (true) {
    const left = parent * 2 + 1;
    if (left >= heap.length) break;
    const right = left + 1;
    const child = right < heap.length && compare(heap[right], heap[left]) > 0 ? right : left;
    if (compare(heap[parent], heap[child]) >= 0) break;
    [heap[parent], heap[child]] = [heap[child], heap[parent]];
    parent = child;
  }
}

export class CatalogStore {
  constructor({ fetchImpl = globalThis.fetch?.bind(globalThis), baseURL = globalThis.location?.href || 'http://localhost/' } = {}) {
    this.fetchImpl = fetchImpl;
    this.baseURL = baseURL;
    this.index = null;
    this.shardCache = new Map();
    this.detailCache = new Map();
    this._loadVersion = 0;
    this._searchVersion = 0;
    this._detailVersion = 0;
  }

  /** Load only the small index and its first 24 summaries. */
  async load(indexURL = 'assets/catalog.json') {
    this.cancelSearch();
    this.cancelDetail();
    this._loadController?.abort();
    const version = ++this._loadVersion;
    const controller = this._loadController = new AbortController();
    const url = new URL(indexURL, this.baseURL);
    const origin = new URL(this.baseURL).origin;
    if (url.origin !== origin || !['http:', 'https:'].includes(url.protocol)) throw new Error('Catalog must be same-origin.');
    const index = await this._fetchJSON(url.href, controller.signal);
    if (version !== this._loadVersion) throw abortError();
    if (index.version !== 1 || !Number.isSafeInteger(index.total) || index.total < 0 ||
      index.shardSize !== 256 || !Array.isArray(index.categories) || !Array.isArray(index.collections) ||
      !Array.isArray(index.shards) || !Array.isArray(index.initial) || index.initial.length > 24 ||
      !index.initial.every(isItem) || !safeRelativePath(index.detailBase) ||
      !index.shards.every(shard => safeRelativePath(shard.path) && Number.isInteger(shard.count) && shard.count > 0 &&
        shard.count <= 256 && shard.categories && shard.collections) ||
      index.shards.reduce((sum, shard) => sum + shard.count, 0) !== index.total) {
      throw new Error('Invalid catalog index.');
    }
    this.indexURL = url.href;
    this.siteRoot = new URL('../', url);
    this.index = index;
    this.shardCache.clear();
    this.detailCache.clear();
    return index;
  }

  /** Resolve asset paths under the site's deployment prefix; reject remote/traversal URLs. */
  resolvePath(path) {
    if (!this.siteRoot || !safeRelativePath(path)) return '';
    const url = new URL(path, this.siteRoot);
    return url.origin === this.siteRoot.origin && url.pathname.startsWith(this.siteRoot.pathname) ? url.href : '';
  }

  async _fetchJSON(url, signal) {
    const response = await this.fetchImpl(url, { signal });
    if (!response.ok) throw new Error(`Catalog request failed (${response.status}).`);
    return response.json();
  }

  async _getShard(descriptor, signal, check) {
    check();
    const cached = cacheGet(this.shardCache, descriptor.path);
    if (cached) return cached;
    const data = await this._fetchJSON(this.resolvePath(descriptor.path), signal);
    check();
    if (data.version !== 1 || !Array.isArray(data.items) || data.items.length !== descriptor.count || !data.items.every(isItem)) {
      throw new Error('Invalid catalog shard.');
    }
    cachePut(this.shardCache, descriptor.path, data.items, 8);
    return data.items;
  }

  cancelSearch() {
    ++this._searchVersion;
    this._searchController?.abort();
  }

  /** A newer search aborts the older one. Catch AbortError without rendering an error. */
  async search({ query = '', category = 'all', collection = 'all', sort = 'name', page = 0, pageSize = 24 } = {}) {
    if (!this.index) throw new Error('Load the catalog before searching.');
    this.cancelSearch();
    const version = this._searchVersion;
    const controller = this._searchController = new AbortController();
    const check = () => { if (version !== this._searchVersion || controller.signal.aborted) throw abortError(); };
    const terms = normalize(query).trim().split(/\s+/).filter(Boolean);
    const cat = category && category !== 'all' ? category : '';
    const col = collection && collection !== 'all' ? collection : '';
    pageSize = Math.min(100, Math.max(1, Math.floor(Number(pageSize) || 24)));
    page = Math.max(0, Math.floor(Number(page) || 0));
    if (!Number.isSafeInteger(page)) page = 0;
    const descending = sort === 'name-desc';
    const numeric = sort === 'triangles-asc' || sort === 'triangles-desc';
    const compare = numeric ? (a, b) => {
      const av = Number.isFinite(a.triangles) ? a.triangles : Infinity;
      const bv = Number.isFinite(b.triangles) ? b.triangles : Infinity;
      if (av === Infinity || bv === Infinity) return (av === bv ? 0 : av === Infinity ? 1 : -1) || byName(a, b);
      return (sort === 'triangles-desc' ? bv - av : av - bv) || byName(a, b);
    } : descending ? (a, b) => byName(b, a) : byName;
    const descriptors = this.index.shards.filter(shard => (!cat || shard.categories[cat]) && (!col || shard.collections[col]));
    if (descending) descriptors.reverse();
    const matches = item => (!cat || item.category === cat) && (!col || item.collection === col) &&
      (!terms.length || terms.every(term => normalize([item.id, ...Object.values(typeof item.name === 'object' ? item.name : { en: item.name }), item.category, item.collection].join(' ')).includes(term)));

    // Header counts allow browsing directly to a page without downloading preceding shards.
    const countKnown = !terms.length && !(cat && col);
    if (countKnown && !numeric) {
      const total = cat ? this.index.categories.find(facet => facet.id === cat)?.count || 0 :
        col ? this.index.collections.find(facet => facet.id === col)?.count || 0 : this.index.total;
      const pages = Math.ceil(total / pageSize);
      page = Math.min(page, Math.max(0, pages - 1));
      let skip = page * pageSize;
      const items = [];
      if (!cat && !col && !descending && skip + Math.min(pageSize, total) <= this.index.initial.length) {
        check();
        return { items: this.index.initial.slice(skip, skip + pageSize), total, page, pages };
      }
      for (const descriptor of descriptors) {
        const count = cat ? descriptor.categories[cat] || 0 : col ? descriptor.collections[col] || 0 : descriptor.count;
        if (skip >= count) { skip -= count; continue; }
        const shard = await this._getShard(descriptor, controller.signal, check);
        for (const item of descending ? [...shard].reverse() : shard) {
          if (!matches(item)) continue;
          if (skip) { --skip; continue; }
          items.push(item);
          if (items.length === pageSize) break;
        }
        if (items.length === pageSize) break;
      }
      check();
      return { items, total, page, pages };
    }

    // Search every relevant summary shard, including distant matches. Never fetch details.
    let total = 0;
    const items = [], tail = [], heap = [];
    const offset = page * pageSize;
    const limit = Math.min(this.index.total, offset + pageSize);
    for (const descriptor of descriptors) {
      const shard = await this._getShard(descriptor, controller.signal, check);
      for (const item of descending ? [...shard].reverse() : shard) {
        if (!matches(item)) continue;
        if (numeric) retainBest(heap, item, limit, compare);
        else {
          if (total >= offset && items.length < pageSize) items.push(item);
          tail.push(item);
          if (tail.length > pageSize) tail.shift();
        }
        ++total;
      }
    }
    check();
    const pages = Math.ceil(total / pageSize);
    const resolvedPage = Math.min(page, Math.max(0, pages - 1));
    const result = numeric ? heap.sort(compare).slice(resolvedPage * pageSize, (resolvedPage + 1) * pageSize) :
      resolvedPage !== page ? tail.slice(-(total % pageSize || pageSize)) : items;
    return { items: result, total, page: resolvedPage, pages };
  }

  cancelDetail() {
    ++this._detailVersion;
    this._detailController?.abort();
  }

  /** Fetch a single complete manifest entry, with an independent four-entry LRU. */
  async getDetail(itemOrId) {
    if (!this.index) throw new Error('Load the catalog before opening an asset.');
    this.cancelDetail();
    const version = this._detailVersion;
    const id = typeof itemOrId === 'string' ? itemOrId : itemOrId?.id;
    if (!validId(id)) throw new Error('Invalid asset id.');
    const path = `${this.index.detailBase}${id}.json`;
    const cached = cacheGet(this.detailCache, path);
    if (cached) return cached;
    const controller = this._detailController = new AbortController();
    const detail = await this._fetchJSON(this.resolvePath(path), controller.signal);
    if (version !== this._detailVersion || controller.signal.aborted) throw abortError();
    if (!detail || detail.id !== id) throw new Error('Invalid asset detail.');
    cachePut(this.detailCache, path, detail, 4);
    return detail;
  }

  dispose() {
    this.cancelSearch();
    this.cancelDetail();
    ++this._loadVersion;
    this._loadController?.abort();
    this.shardCache.clear();
    this.detailCache.clear();
    this.index = null;
  }
}

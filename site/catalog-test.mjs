/** Synthetic summary/detail fixtures exist only in memory and never enter a build. */
import assert from 'node:assert/strict';
import { createCatalog } from './catalog-build.mjs';
import { CatalogStore } from './catalog.js';

const assets = Array.from({ length: 10000 }, (_, i) => ({
  id: `fixture-${i}`,
  name: { en: `Fixture ${String(i).padStart(5, '0')}`, zh: i === 9999 ? '远方的测试植物' : `夹具 ${i}` },
  category: i % 3 ? 'plants' : 'geology',
  collection: i % 2 ? 'prehistoric' : 'fiction',
  preview: `assets/test/fixture-${i}.png`,
  glb: `assets/test/fixture-${i}.glb`,
  triangles: (i * 539) % 10000,
  description: { en: 'Full metadata must never enter a summary', zh: '完整资料' },
  sources: [{ title: 'Test-only memory fixture' }],
  scientific_notes: { en: 'Retained unchanged in the detail response.' }
}));
const manifest = { version: 1, review_only: true, license: 'CC-BY-4.0', assets };
const built = createCatalog(manifest);
const files = new Map([['assets/catalog.json', built.index], ...built.shards, ...built.details]);
const calls = [];
const metrics = { summaryActive: 0, detailActive: 0, peakSummary: 0, peakDetail: 0, maxShardCache: 0, maxDetailCache: 0 };
let store;
const fetchImpl = (url, { signal } = {}) => {
  const path = new URL(url).pathname.replace('/prefix/', '');
  calls.push(path);
  const detail = path.includes('/details/');
  const active = detail ? 'detailActive' : 'summaryActive';
  const peak = detail ? 'peakDetail' : 'peakSummary';
  ++metrics[active];
  metrics[peak] = Math.max(metrics[peak], metrics[active]);
  if (store) {
    metrics.maxShardCache = Math.max(metrics.maxShardCache, store.shardCache.size);
    metrics.maxDetailCache = Math.max(metrics.maxDetailCache, store.detailCache.size);
  }
  return new Promise((resolve, reject) => {
    let done = false;
    let timer;
    const finish = (error) => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      signal?.removeEventListener('abort', abort);
      --metrics[active];
      if (error) return reject(error);
      const value = files.get(path);
      resolve({ ok: !!value, status: value ? 200 : 404, json: async () => structuredClone(value) });
    };
    const abort = () => finish(new DOMException('Test request aborted', 'AbortError'));
    if (signal?.aborted) return abort();
    signal?.addEventListener('abort', abort, { once: true });
    timer = setTimeout(() => finish(), 0);
  });
};
store = new CatalogStore({ baseURL: 'https://example.test/prefix/', fetchImpl });
const index = await store.load();
assert.equal(index.shards.length, 40);
assert.equal(index.total, 10000);
assert.equal(index.initial.length, 24);
assert.equal(index.categories.reduce((sum, category) => sum + category.count, 0), 10000);
assert.equal(JSON.stringify(index).includes('Full metadata'), false);
assert.equal(JSON.stringify([...built.shards.values()]).includes('scientific_notes'), false);

let result = await store.search();
assert.equal(result.items.length, 24);
assert.equal(result.pages, 417);
assert.equal(calls.length, 1, 'Initial page must only request the index.');
result = await store.search({ page: 416 });
assert.equal(result.items.length, 16);
assert.equal(result.items.at(-1).id, 'fixture-9999');
assert.equal(calls.length, 2, 'Deep page jump must fetch only its relevant shard.');
result = await store.search({ query: '远方' });
assert.equal(result.total, 1);
assert.equal(result.items[0].id, 'fixture-9999', 'Chinese search must reach the last shard.');
result = await store.search({ query: 'Fixture 09999' });
assert.equal(result.total, 1);
assert.equal(result.items[0].id, 'fixture-9999', 'English search must reach the last shard.');
assert.equal(store.shardCache.size, 8);
assert(calls.every(path => !path.includes('/details/')), 'Search must never request complete metadata.');

const collator = new Intl.Collator('en', { numeric: true, sensitivity: 'base' });
const byName = (a, b) => collator.compare(a.name.en, b.name.en) || collator.compare(a.id, b.id);
const summaries = [...built.shards.values()].flatMap(shard => shard.items);
for (const options of [
  { category: 'plants', page: 12 },
  { collection: 'fiction', page: 47 },
  { category: 'plants', collection: 'prehistoric', page: 4 },
  { query: 'fixture', sort: 'name-desc', page: 3 },
  { sort: 'triangles-asc', page: 0 },
  { sort: 'triangles-desc', page: 31 },
  { sort: 'triangles-asc', page: 10000 },
  { query: 'fixture 000', page: 1000 },
  { category: 'missing' }
]) {
  result = await store.search(options);
  const terms = (options.query || '').toLowerCase().split(/\s+/).filter(Boolean);
  const expected = summaries.filter(item => (!options.category || item.category === options.category) &&
    (!options.collection || item.collection === options.collection) &&
    terms.every(term => [item.id, item.name.en, item.name.zh, item.category, item.collection].join(' ').toLowerCase().includes(term)));
  expected.sort(options.sort === 'name-desc' ? (a, b) => byName(b, a) : options.sort?.startsWith('triangles') ?
    (a, b) => (options.sort === 'triangles-desc' ? b.triangles - a.triangles : a.triangles - b.triangles) || byName(a, b) : byName);
  assert.equal(result.total, expected.length, JSON.stringify(options));
  assert.deepEqual(result.items.map(item => item.id), expected.slice(result.page * 24, (result.page + 1) * 24).map(item => item.id), JSON.stringify(options));
  assert(store.shardCache.size <= 8);
}

assert.equal(store.resolvePath('assets/test/fixture-1.glb'), 'https://example.test/prefix/assets/test/fixture-1.glb');
for (const bad of ['../secrets', 'assets/../secrets', 'https://evil.test/a', '//evil.test/a', 'assets/%2e%2e/secrets', 'assets/a\\b', '/assets/a', 'assets/a?x=1']) {
  assert.equal(store.resolvePath(bad), '');
}
await assert.rejects(() => store.load('https://evil.test/assets/catalog.json'), /same-origin/);
const callsBeforeUnsafeDetails = calls.length;
for (const bad of ['../fixture-0', 'fixture/0', '%2e%2e', '//evil.test/a', '']) {
  await assert.rejects(() => store.getDetail(bad), /Invalid asset id/);
}
assert.equal(calls.length, callsBeforeUnsafeDetails, 'Unsafe detail ids must be rejected before fetch.');
for (let i = 0; i < 5; i++) {
  const detail = await store.getDetail(`fixture-${i}`);
  assert.deepEqual(detail, assets[i]);
  assert(store.detailCache.size <= 4);
}
assert.equal(store.detailCache.size, 4);
const beforeCachedDetail = calls.length;
await store.getDetail({ id: 'fixture-4', detail: 'https://evil.test/ignored' });
assert.equal(calls.length, beforeCachedDetail, 'Cached detail must be reused; arbitrary supplied URLs are ignored.');

const staleSearch = store.search({ query: 'fixture' }).then(
  () => { throw new Error('Stale search resolved.'); },
  error => assert.equal(error.name, 'AbortError')
);
const freshSearch = store.search({ query: '远方' });
await staleSearch;
assert.equal((await freshSearch).total, 1);
const staleDetail = store.getDetail('fixture-9900').then(
  () => { throw new Error('Stale detail resolved.'); },
  error => assert.equal(error.name, 'AbortError')
);
const freshDetail = store.getDetail('fixture-9901');
await staleDetail;
assert.equal((await freshDetail).id, 'fixture-9901');

// Even a transport which ignores AbortSignal cannot return a superseded result.
const ignoredAbortStore = new CatalogStore({ baseURL: 'https://example.test/prefix/', fetchImpl: (url) => fetchImpl(url) });
await ignoredAbortStore.load();
const ignoredStale = ignoredAbortStore.search({ query: 'fixture' }).then(
  () => { throw new Error('Cancellation guard failed.'); },
  error => assert.equal(error.name, 'AbortError')
);
ignoredAbortStore.cancelSearch();
await ignoredStale;

// Production derives exclusively from the supplied release manifest, never directory discovery.
const approvedManifest = { version: 1, assets: [assets[17], assets[43]], license: 'CC-BY-4.0' };
const approvedSnapshot = JSON.stringify(approvedManifest);
const approved = createCatalog(approvedManifest, { approvedOnly: true });
assert.equal(approved.index.total, 2);
assert.equal(approved.index.review_only, false);
assert.equal(approved.details.size, 2);
assert(!approved.details.has('assets/catalog/details/fixture-18.json'));
assert.equal(JSON.stringify(approvedManifest), approvedSnapshot, 'Catalog generation must not alter manifest or QA data.');
assert.throws(() => createCatalog(manifest, { approvedOnly: true }), /review-only/);
assert.throws(() => createCatalog(undefined), /existing manifest/);
assert.throws(() => createCatalog({ assets: [{ ...assets[0], id: '../escape' }] }), /Invalid/);
assert.throws(() => createCatalog({ assets: [assets[0], assets[0]] }), /duplicate/);
assert.throws(() => createCatalog({ assets: [{ ...assets[0], preview: 'https://evil.test/a.png' }] }), /Invalid/);

const emptyBuilt = createCatalog({ assets: [] });
const empty = new CatalogStore({ baseURL: 'https://example.test/', fetchImpl: async () => ({ ok: true, json: async () => emptyBuilt.index }) });
await empty.load();
assert.deepEqual(await empty.search(), { items: [], total: 0, page: 0, pages: 0 });
assert.deepEqual(await empty.search({ query: 'anything', sort: 'triangles-asc' }), { items: [], total: 0, page: 0, pages: 0 });
assert.equal(metrics.peakSummary, 1, 'Summary metadata requests must be serial.');
assert.equal(metrics.peakDetail, 1, 'Detail metadata requests must be serial/cancellable.');
assert.equal(metrics.maxShardCache, 8);
assert.equal(metrics.maxDetailCache, 4);
store.dispose();
ignoredAbortStore.dispose();
empty.dispose();
assert.equal(store.shardCache.size, 0);
assert.equal(store.detailCache.size, 0);
console.log(JSON.stringify({
  result: 'Catalog tests passed',
  assets: 10000,
  shards: index.shards.length,
  indexBytes: new TextEncoder().encode(JSON.stringify(index)).length,
  defaultPageShardRequests: 0,
  deepPageShardRequests: 1,
  maxCachedShards: metrics.maxShardCache,
  maxCachedDetails: metrics.maxDetailCache,
  peakSummaryRequests: metrics.peakSummary,
  peakDetailRequests: metrics.peakDetail,
  verified: ['global bilingual search', 'combined facets', 'sort and pagination', 'cancelled requests', 'abort-ignoring transport guard', 'same-origin deployment prefix', 'safe detail ids', 'complete detail preservation', 'approved-manifest-only production', 'empty catalog']
}, null, 2));

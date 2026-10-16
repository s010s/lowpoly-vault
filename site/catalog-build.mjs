/** Derived browsing data only. This module never discovers assets or approves QA. */
import { mkdir, rm, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';

export const CATALOG_SHARD_SIZE = 256;
const collator = new Intl.Collator('en', { numeric: true, sensitivity: 'base' });
const label = asset => typeof asset.name === 'string' ? asset.name : asset.name?.en || asset.id;
const counts = (assets, key) => Object.fromEntries([...assets.reduce((map, asset) => {
  map.set(asset[key], (map.get(asset[key]) || 0) + 1);
  return map;
}, new Map())].sort(([a], [b]) => collator.compare(a, b)));
const facets = (assets, key) => Object.entries(counts(assets, key)).map(([id, count]) => ({ id, count }));
const relativeAssetPath = value => typeof value === 'string' && value.startsWith('assets/') &&
  !/[\\\u0000-\u001f?#%]/.test(value) && !value.split('/').some(part => part === '..' || part === '.');

/** In-memory equivalent used by Vite. Full detail objects are referenced, never duplicated. */
export function createCatalog(manifest, { name = 'catalog', approvedOnly = false } = {}) {
  if (!manifest || !Array.isArray(manifest.assets)) throw new Error('Catalog requires an existing manifest.');
  if (approvedOnly && manifest.review_only) throw new Error('A review-only manifest cannot produce a release catalog.');
  if (!['catalog', 'catalog-review'].includes(name)) throw new Error('Invalid catalog name.');
  const prefix = `assets/${name}`;
  const ids = new Set();
  for (const asset of manifest.assets) {
    if (!/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(asset.id || '') || ids.has(asset.id)) {
      throw new Error(`Invalid or duplicate catalog asset id: ${asset.id}`);
    }
    ids.add(asset.id);
    if (!asset.name || !asset.category || !asset.collection || !relativeAssetPath(asset.preview) || !relativeAssetPath(asset.glb)) {
      throw new Error(`Invalid catalog browsing fields: ${asset.id}`);
    }
  }
  const ordered = [...manifest.assets].sort((a, b) => collator.compare(label(a), label(b)) || collator.compare(a.id, b.id));
  const items = ordered.map(asset => ({
    id: asset.id,
    name: asset.name,
    category: asset.category,
    collection: asset.collection,
    preview: asset.preview,
    glb: asset.glb,
    triangles: Number.isFinite(asset.triangles) ? asset.triangles : null,
    detail: `${prefix}/details/${asset.id}.json`
  }));
  const shards = new Map();
  const descriptors = [];
  for (let offset = 0; offset < items.length; offset += CATALOG_SHARD_SIZE) {
    const part = items.slice(offset, offset + CATALOG_SHARD_SIZE);
    const path = `${prefix}/shards/${String(descriptors.length).padStart(5, '0')}.json`;
    shards.set(path, { version: 1, items: part });
    descriptors.push({ path, count: part.length, categories: counts(part, 'category'), collections: counts(part, 'collection') });
  }
  const index = {
    version: 1,
    total: items.length,
    review_only: manifest.review_only === true,
    shardSize: CATALOG_SHARD_SIZE,
    categories: facets(items, 'category'),
    collections: facets(items, 'collection'),
    shards: descriptors,
    initial: items.slice(0, 24),
    detailBase: `${prefix}/details/`
  };
  for (const key of ['license', 'code_license', 'author', 'attribution_url']) {
    if (manifest[key] !== undefined) index[key] = manifest[key];
  }
  return { index, shards, details: new Map(ordered.map(asset => [`${prefix}/details/${asset.id}.json`, asset])) };
}

/** Write a catalog beneath a site output root, using only the supplied manifest. */
export async function writeCatalog(manifest, outDir, options = {}) {
  const name = options.name || 'catalog';
  const catalog = createCatalog(manifest, { ...options, name });
  const root = join(outDir, 'assets', name);
  await rm(root, { recursive: true, force: true });
  await mkdir(join(root, 'shards'), { recursive: true });
  await mkdir(join(root, 'details'), { recursive: true });
  for (const [path, value] of [...catalog.shards, ...catalog.details]) {
    await writeFile(join(outDir, path), `${JSON.stringify(value)}\n`);
  }
  const indexPath = join(outDir, 'assets', `${name}.json`);
  await mkdir(dirname(indexPath), { recursive: true });
  await writeFile(indexPath, `${JSON.stringify(catalog.index)}\n`);
  return catalog.index;
}

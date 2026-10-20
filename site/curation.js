/** Editorial data is inert JSON; membership never discovers assets or approves QA. */
import catalogData from './catalog-data.json' with { type: 'json' };

const unsafe = new Set(['__proto__', 'prototype', 'constructor']);
const fail = message => { throw new Error(`Invalid catalog data: ${message}`); };
const identifier = (value, where) => {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(value) || value.includes('..') || unsafe.has(value)) fail(`${where} has an unsafe id`);
};
function record(value, keys, where) {
  if (!value || typeof value !== 'object' || Array.isArray(value) || ![Object.prototype, null].includes(Object.getPrototypeOf(value))) fail(`${where} must be a record`);
  const own = Reflect.ownKeys(value);
  if (own.length !== keys.length || own.some(key => typeof key !== 'string' || unsafe.has(key) || !keys.includes(key))) fail(`${where} has unexpected or missing keys`);
}
function localized(value, where) {
  record(value, ['en', 'zh'], where);
  for (const lang of ['en', 'zh']) if (typeof value[lang] !== 'string' || !value[lang].trim() || /[\u0000-\u001f\u007f]/.test(value[lang])) fail(`${where}.${lang} must be nonempty text`);
}
function ids(value, where, { empty = false } = {}) {
  if (!Array.isArray(value) || (!empty && !value.length)) fail(`${where} must be an id array`);
  const seen = new Set();
  for (const id of value) { identifier(id, where); if (seen.has(id)) fail(`${where} contains duplicate id ${id}`); seen.add(id); }
  return seen;
}
const canonical = value => JSON.stringify(value, function(key, item) {
  return item && typeof item === 'object' && !Array.isArray(item) ? Object.fromEntries(Object.keys(item).sort().map(name => [name, item[name]])) : item;
});

/** Strict shape validation. Optional full-manifest checks verify every declared owner. */
export function validateCatalogData(data, { manifest } = {}) {
  record(data, ['version', 'worlds', 'packs', 'legacy_memberships'], 'root');
  if (data.version !== 1) fail('unsupported version');
  const seen = { worlds: new Set(), packs: new Set(), legacy_memberships: new Set() };
  for (const kind of Object.keys(seen)) {
    if (!Array.isArray(data[kind])) fail(`${kind} must be an array`);
    for (const entry of data[kind]) {
      record(entry, kind === 'worlds' ? ['id', 'name'] : kind === 'packs' ? ['id', 'name', 'description', 'asset_ids'] : ['pack_id', 'asset_ids'], kind);
      const id = kind === 'legacy_memberships' ? entry.pack_id : entry.id;
      identifier(id, kind);
      if (seen[kind].has(id)) fail(`${kind} contains duplicate id ${id}`);
      seen[kind].add(id);
      if (kind !== 'legacy_memberships') localized(entry.name, `${kind}.${id}.name`);
      if (kind === 'packs') localized(entry.description, `packs.${id}.description`);
      if (kind !== 'worlds') ids(entry.asset_ids, `${kind}.${id}.asset_ids`);
    }
  }
  for (const entry of data.legacy_memberships) {
    const pack = data.packs.find(pack => pack.id === entry.pack_id);
    if (!pack || entry.asset_ids.some(id => !pack.asset_ids.includes(id))) fail(`legacy membership ${entry.pack_id} does not reference its pack owners`);
  }
  if (manifest !== undefined) {
    if (!Array.isArray(manifest?.assets)) fail('reference validation requires a manifest');
    ids(manifest.assets.map(asset => asset.id), 'manifest.assets', { empty: true });
    const byId = new Map(manifest.assets.map(asset => [asset.id, asset]));
    for (const pack of data.packs) {
      for (const id of pack.asset_ids) {
        if (!byId.has(id)) fail(`pack ${pack.id} references unknown model ${id}`);
        if (!membership(byId.get(id), data).packs.includes(pack.id)) fail(`pack ${pack.id} does not own model ${id}`);
      }
      for (const asset of manifest.assets) if (membership(asset, data).packs.includes(pack.id) && !pack.asset_ids.includes(asset.id)) fail(`pack ${pack.id} omits owner ${asset.id}`);
    }
  }
  return data;
}
function membership(asset, data) {
  return {
    worlds: [...new Set(Array.isArray(asset.worlds) ? asset.worlds : [asset.collection].filter(Boolean))],
    packs: [...new Set([...(Array.isArray(asset.packs) ? asset.packs : []), ...data.legacy_memberships.filter(entry => entry.asset_ids.includes(asset.id)).map(entry => entry.pack_id)])]
  };
}
export const CATALOG_DATA = validateCatalogData(catalogData);
export function createCuration(data = CATALOG_DATA) {
  validateCatalogData(data);
  return {
    WORLD_LABELS: Object.fromEntries(data.worlds.map(world => [world.id, world.name])),
    PACK_LABELS: Object.fromEntries(data.packs.map(pack => [pack.id, pack.name])),
    PACK_RECORDS: Object.fromEntries(data.packs.map(pack => [pack.id, pack])),
    catalogMembership: asset => membership(asset, data)
  };
}
export const { WORLD_LABELS, PACK_LABELS, PACK_RECORDS, catalogMembership } = createCuration();

/** Per-model proof inputs exclude unrelated records and other models' pack membership. */
export function catalogDataForAsset(asset, data = CATALOG_DATA) {
  const { WORLD_LABELS, PACK_RECORDS, catalogMembership } = createCuration(data);
  const own = catalogMembership(asset);
  return {
    version: data.version,
    membership: own,
    worlds: own.worlds.map(id => ({ id, ...(WORLD_LABELS[id] ? { name: WORLD_LABELS[id] } : {}) })),
    packs: own.packs.map(id => ({ id, ...(PACK_RECORDS[id] ? { name: PACK_RECORDS[id].name, description: PACK_RECORDS[id].description } : {}) }))
  };
}

/** Structural eligibility only, never publication approval. Callers must independently
 * bind each returned record to the authorized descriptors and their exact model IDs. */
export function inspectCatalogDataAppend(previous, current, { addedAssetIds = [], previousManifest, currentManifest } = {}) {
  validateCatalogData(previous);
  validateCatalogData(current);
  const added = ids(addedAssetIds, 'addedAssetIds', { empty: true });
  if (canonical(previous.legacy_memberships) !== canonical(current.legacy_memberships)) fail('existing legacy membership changed');
  for (const kind of ['worlds', 'packs']) {
    if (current[kind].length < previous[kind].length || previous[kind].some((entry, i) => canonical(entry) !== canonical(current[kind][i]))) fail(`existing ${kind} records changed or were reordered`);
  }
  const addedWorlds = current.worlds.slice(previous.worlds.length);
  const addedPacks = current.packs.slice(previous.packs.length);
  const previousOwners = new Set(previous.packs.flatMap(pack => pack.asset_ids));
  for (const pack of addedPacks) for (const id of pack.asset_ids) {
    if (!added.has(id) || previousOwners.has(id)) fail(`new pack ${pack.id} has unauthorized or existing owner ${id}`);
  }
  if (previousManifest !== undefined) {
    if (!Array.isArray(previousManifest?.assets)) fail('previous manifest is malformed');
    for (const asset of previousManifest.assets) {
      if (added.has(asset.id)) fail(`addedAssetIds contains existing model ${asset.id}`);
      if (canonical(catalogDataForAsset(asset, previous)) !== canonical(catalogDataForAsset(asset, current))) fail(`new catalog records change existing model ${asset.id}`);
    }
  }
  if (currentManifest !== undefined) validateCatalogData(current, { manifest: currentManifest });
  return { addedWorlds, addedPacks, affectedIds: [...new Set(addedPacks.flatMap(pack => pack.asset_ids))].sort() };
}

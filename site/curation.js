/** Explicit editorial membership, independent of model category and legacy storage collection. */
export const WORLD_LABELS = { prehistoric: { en: 'Prehistoric', zh: '史前世界' } };
export const PACK_LABELS = { 'prehistoric-starter': { en: 'Prehistoric starter', zh: '史前入门组合' } };
const starterIds = ['natural-arch','stratified-cliff','conifer-tree','cycad','fern-cluster','horsetail-cluster','lepidodendron','dinosaur-nest','three-toed-track','uprooted-log'];
const starter = new Set(starterIds);
export const PACK_RECORDS = { 'prehistoric-starter': { id:'prehistoric-starter', name:PACK_LABELS['prehistoric-starter'], description:{en:'Ten original candidates spanning plants, geology, wood, and traces.',zh:'涵盖植物、地质、木材与痕迹的十个原创候选模型。'}, asset_ids:starterIds } };
export function catalogMembership(asset) {
  return {
    worlds: [...new Set(Array.isArray(asset.worlds) ? asset.worlds : [asset.collection].filter(Boolean))],
    packs: [...new Set([...(Array.isArray(asset.packs) ? asset.packs : []), ...(starter.has(asset.id) ? ['prehistoric-starter'] : [])])]
  };
}

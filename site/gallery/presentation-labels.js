/** One display-name vocabulary for the native preview and enhanced gallery. */
import { categoryLabel, isZh } from '../shared-ui.js';

const names = {
  thamnopora: ['Thamnopora', '枝状珊瑚'],
  'fern-cluster': ['Fern cluster', '地表蕨丛'],
  gryphaea: ['Gryphaea', '弯壳牡蛎'],
  cooperoceras: ['Cooperoceras', '长角盘卷壳'],
  waptia: ['Waptia', '瓦普塔虾'],
  syringopora: ['Syringopora', '笛管珊瑚'],
  'natural-arch': ['Natural Arch', '天然石拱'],
  'conifer-tree': ['Airy conifer', '疏枝针叶树'],
  'quartz-prism-cluster': ['Quartz cluster', '石英晶簇'],
  opabinia: ['Opabinia', '五眼古生动物'],
  halysites: ['Halysites', '链珊瑚'],
  fenestella: ['Fenestella', '窗格扇苔藓动物'],
  cooksonia: ['Cooksonia', '顶囊裸轴'],
  canadaspis: ['Canadaspis', '甲壳底栖动物'],
  metasequoia: ['Metasequoia', '水杉类化石枝'],
  azolla: ['Azolla', '淡水叶瓦浮垫'],
  micrabacia: ['Micrabacia', '放射盘珊瑚'],
  // Preserve the established URL while displaying the adopted taxonomic identity.
  gastornis: ['Diatryma gigantea', 'Diatryma gigantea（始新世巨鸟）'],
};

export function modelShortName(asset, lang = 'en') {
  if (!asset) return '';
  const zh = isZh(lang);
  if (names[asset.id]) return names[asset.id][zh ? 1 : 0];
  if (zh) return asset.name?.zh || asset.name?.en || asset.id;
  return (typeof asset.name === 'string' ? asset.name : asset.name?.en) || asset.id;
}

export function galleryCategoryLabel(category, lang = 'en') {
  return categoryLabel(category, lang);
}

/** Build a set of Chinese display names that collide across distinct taxa so lists can disambiguate them. */
export function duplicateZhNames(assets = []) {
  const counts = new Map();
  for (const asset of assets) {
    const label = modelShortName(asset, 'zh');
    if (label) counts.set(label, (counts.get(label) || 0) + 1);
  }
  const dupes = new Set();
  for (const [label, count] of counts) if (count > 1) dupes.add(label);
  return dupes;
}

/** Disambiguate colliding Chinese names with the model's English/taxonomic name. */
export function disambiguatedName(asset, lang = 'en', zhDupes = null) {
  const primary = modelShortName(asset, lang);
  if (!isZh(lang) || !zhDupes?.has(primary)) return primary;
  const secondary = modelShortName(asset, 'en');
  if (!secondary || secondary === primary || primary.includes(secondary)) return primary;
  return `${primary} · ${secondary}`;
}

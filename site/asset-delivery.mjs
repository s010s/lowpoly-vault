/** Manifest-only delivery: no recursive asset discovery/copying and no QA state changes. */
import { cp, mkdir, readFile, realpath, stat, writeFile, readdir, rm } from 'node:fs/promises';
import { dirname, resolve, sep, extname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { catalogMembership } from './curation.js';
import { validAssetId } from './routes.js';

export function assetFileAllowlist(manifest) {
  if (!manifest || !Array.isArray(manifest.assets)) throw new Error('A supplied manifest is required.');
  const paths = new Set();
  for (const asset of manifest.assets) {
    if (!validAssetId(asset.id)) throw new Error('Invalid asset id.');
    for (const key of ['glb','blend','preview']) {
      const path = asset[key];
      if (typeof path !== 'string' || !path.startsWith('assets/') || /[\\\u0000-\u001f?#%]/.test(path) || path.split('/').some(p => p === '.' || p === '..') ||
        !(key === 'preview' ? ['.png','.jpg','.jpeg','.webp'].includes(extname(path).toLowerCase()) : extname(path) === `.${key}`)) throw new Error(`Unsafe ${key} delivery path: ${asset.id}`);
      if (path.split('/').some(p => /^(qa|experiments?|references?|research)$/i.test(p))) throw new Error(`Non-release directory in asset path: ${path}`);
      paths.add(path);
    }
  }
  return [...paths].sort();
}
export async function enrichManifest(manifest, root = process.cwd()) {
  assetFileAllowlist(manifest);
  const assetRoot = await realpath(resolve(root,'assets'));
  const assets = [];
  for (const asset of manifest.assets) {
    const file_sizes = {};
    for (const key of ['glb','blend','preview']) {
      const source = await realpath(resolve(root, asset[key]));
      if (!source.startsWith(assetRoot + sep)) throw new Error(`Asset symlink escapes asset root: ${asset[key]}`);
      const info = await stat(source);
      if (!info.isFile() || !info.size) throw new Error(`Empty or non-file asset: ${asset[key]}`);
      if (key !== 'preview') file_sizes[key] = info.size;
      if (asset.sha256?.[key] && createHash('sha256').update(await readFile(source)).digest('hex') !== asset.sha256[key]) throw new Error(`Asset differs from approved manifest checksum: ${asset[key]}`);
    }
    let material_count;
    try { const qa = JSON.parse(await readFile(resolve(root,dirname(asset.glb),'qa.json'),'utf8'));
      if (['pass','pass_with_warnings'].includes(qa.glb?.status) && Number.isInteger(qa.glb.materials) && qa.glb.materials >= 0 && qa.glb.sha256 && qa.glb.sha256 === asset.sha256?.glb) material_count = qa.glb.materials;
    } catch(error) { if (error.code !== 'ENOENT') throw error; }
    const {material_count:ignoredMaterialCount,qa:privateQaPath,...sourceAsset}=asset;
    assets.push({...sourceAsset, ...catalogMembership(asset), file_sizes, glb_bytes:file_sizes.glb, blend_bytes:file_sizes.blend,
      ...(material_count === undefined ? {} : { material_count }),
      downloads: {glb:asset.glb, blend:asset.blend, bundle:`assets/downloads/${asset.id}.zip`, credits:`assets/downloads/${asset.id}-CREDITS.txt`}
    });
  }
  return {...manifest, assets};
}
export function creditText(asset, manifest) {
  const title = typeof asset.name === 'string' ? asset.name : asset.name?.en || asset.id;
  if(asset.production_release){return `${title}\n${asset.name?.zh||''}\n\nCreator: ${asset.author||manifest.author}\nProject: ${manifest.attribution_url||'https://github.com/s010s/lowpoly-vault'}\nLicense: CC-BY-4.0\nhttps://creativecommons.org/licenses/by/4.0/\n\n${asset.description.en}\n${asset.description.zh}\n\nOriginal evidence-informed geometry; not a recovered historical model or intact-organism reconstruction.\nConsulted sources (no reference media incorporated):\n${asset.reference_credits.map(s=>s.title+' — '+s.url).join('\n')}\n\nCredit the creator, provide project and license links, and indicate your changes.\n${manifest.review_only?'LOCAL REVIEW CANDIDATE, NOT PUBLISHED.\n':''}`;}
  const revision = asset.revision_provenance;
  const history = revision
    ? `Revision: ${asset.revision}\nRevision creator: ${revision.author}\nRevision source: ${revision.source_url}\nChanges: ${revision.changes}\nOriginal creator: ${revision.original_author}\nOriginal source: ${revision.original_source_url}\nOriginal GLB SHA-256: ${revision.original_glb_sha256}\nThis archive contains the accepted revision's GLB and editable Blender source. Acceptance is for its frozen brief.\n`
    : 'This archive contains the original GLB and editable Blender source; no modifications are claimed.\n';
  return `${title}\n${asset.name?.zh || ''}\n\nCreator: ${asset.author || manifest.author || 'Leon Made This / s010s'}\nSource: ${asset.source_url || manifest.attribution_url || 'https://github.com/s010s/lowpoly-vault'}\nLicense: ${asset.license || manifest.license || 'CC-BY-4.0'}\nLicense URL: https://creativecommons.org/licenses/by/4.0/\n\nYou may share and adapt this asset, including commercially, under CC BY 4.0.\nCredit the creator, provide the source and license links, and indicate your changes.\n${history}${asset.quality_status === 'work_in_progress' || manifest.release_status === 'initial' ? '\nInitial collection: further artistic and scientific refinement is ongoing.\n' : ''}${manifest.review_only ? '\nREVIEW ONLY: This candidate is not approved for publication.\n' : ''}`;
}
export async function clearDeliveredAssets(outDir) {
  const folder = join(outDir,'assets');
  await mkdir(folder,{recursive:true});
  for (const item of await readdir(folder,{withFileTypes:true})) {
    // Vite emits only compiled JS/CSS here. Everything else must come from this delivery pass.
    if (item.isDirectory() || !/\.(?:js|css|map)$/.test(item.name)) await rm(join(folder,item.name),{recursive:true,force:true});
  }
}
export async function deliverManifestAssets(manifest, outDir, { root = process.cwd(), review = false } = {}) {
  if (manifest.review_only && !review) throw new Error('A review-only manifest cannot be released.');
  const enriched = await enrichManifest(manifest,root);
  for (const path of assetFileAllowlist(enriched)) {
    await mkdir(dirname(resolve(outDir,path)),{recursive:true});
    await cp(resolve(root,path),resolve(outDir,path));
  }
  await mkdir(resolve(outDir,'assets/downloads'),{recursive:true});
  const jobs=[];
  for (const asset of enriched.assets) {
    const credits = creditText(asset,enriched);
    await writeFile(resolve(outDir,asset.downloads.credits),credits);
    jobs.push({destination:resolve(outDir,asset.downloads.bundle),files:[asset.glb,asset.blend].map(path=>({source:resolve(root,path),name:path.split('/').at(-1)})),credits});
  }
  const python = `import json,sys,zipfile\nfor job in json.load(sys.stdin):\n with zipfile.ZipFile(job['destination'],'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:\n  for item in job['files']:\n   info=zipfile.ZipInfo(item['name'],date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED\n   with open(item['source'],'rb') as f: archive.writestr(info,f.read())\n  info=zipfile.ZipInfo('CREDITS.txt',date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;archive.writestr(info,job['credits'])\n`;
  if(jobs.length) { const result=spawnSync('python3',['-c',python],{input:JSON.stringify(jobs),encoding:'utf8'}); if(result.status !== 0) throw new Error(`ZIP packaging failed: ${result.stderr || result.error}`); }
  for(const asset of enriched.assets) asset.file_sizes.bundle=(await stat(resolve(outDir,asset.downloads.bundle))).size;
  await writeFile(resolve(outDir,'assets/manifest.json'),`${JSON.stringify(enriched,null,2)}\n`);
  return enriched;
}

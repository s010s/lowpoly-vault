/** Capture-only input. This is never a Pages artifact or a publication gate bypass. */
import { mkdir, cp, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { collectInitialRelease } from './initial-release.mjs';
const manifest=await collectInitialRelease();
await mkdir('dist/assets',{recursive:true});
for(const asset of manifest.assets){await mkdir(dirname(resolve('dist',asset.glb)),{recursive:true});await cp(asset.glb,resolve('dist',asset.glb));}
await writeFile('dist/assets/manifest.json',JSON.stringify(manifest)+'\n');
console.log(`Capture-only inputs: ${manifest.assets.length} hash-checked original GLBs; no deployment artifact is produced.`);

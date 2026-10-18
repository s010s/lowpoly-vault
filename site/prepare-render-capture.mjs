/** Capture-only input. This is never a Pages artifact or a publication gate bypass. */
import { mkdir, cp, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { checkPublishedManifest } from './initial-release.mjs';

export async function prepareRenderCapture({root=process.cwd(),outDir=resolve(root,'dist')}={}) {
  const manifest=await checkPublishedManifest(root);
  await mkdir(resolve(outDir,'assets'),{recursive:true});
  for(const asset of manifest.assets) {
    const destination=resolve(outDir,asset.glb);
    await mkdir(dirname(destination),{recursive:true});
    await cp(resolve(root,asset.glb),destination);
  }
  await writeFile(resolve(outDir,'assets/manifest.json'),JSON.stringify(manifest)+'\n');
  console.log(`Capture-only inputs: ${manifest.assets.length} hash-checked published GLBs; no deployment artifact is produced.`);
  return manifest;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)await prepareRenderCapture();

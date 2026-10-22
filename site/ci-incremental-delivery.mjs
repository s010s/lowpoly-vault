/** Restore trust is the caller's responsibility; this module never authorizes reuse. */
import assert from 'node:assert/strict';
import {readFile,writeFile,cp,mkdir,stat,rm} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {deliverManifestAssets,enrichManifest} from './asset-delivery.mjs';
import {deliverTurntables} from './turntable-delivery.mjs';
import {writeCatalog} from './catalog-build.mjs';
import {writeStaticRoutes} from './static-routes.mjs';
import {auditGalleryAssets} from './gallery-assets.mjs';
export async function incrementalDelivery({root=process.cwd(),outDir=resolve(root,'dist'),addedIds}={}){
 const source=JSON.parse(await readFile(resolve(root,'assets/manifest.json'))),ids=new Set(addedIds);assert(ids.size&&ids.size===addedIds.length);
 const prior=JSON.parse(await readFile(resolve(outDir,'assets/manifest.json'))),oldIds=new Set(prior.assets.map(a=>a.id));
 assert(source.assets.every(a=>oldIds.has(a.id)||ids.has(a.id)));assert.equal(source.assets.length,oldIds.size+ids.size);assert([...ids].every(id=>!oldIds.has(id)));
 const expected=await enrichManifest(source,root),newAssets=source.assets.filter(a=>ids.has(a.id));assert.equal(newAssets.length,ids.size);
 // Derive old public records using current, independently unchanged code. Never
 // blindly splice trusted bytes into a new public manifest on ID alone.
 for(const row of expected.assets.filter(a=>oldIds.has(a.id))){const old=prior.assets.find(a=>a.id===row.id);const {card_preview,turntable,...oldBase}=old;const clone=structuredClone(row);clone.file_sizes.bundle=(await stat(resolve(outDir,row.downloads.bundle))).size;assert.deepEqual(oldBase,clone,'Reused delivered record differs: '+row.id);}
 const fresh=await deliverManifestAssets({...source,assets:newAssets},outDir,{root});
 for(const row of expected.assets){row.file_sizes.bundle=ids.has(row.id)?fresh.assets.find(a=>a.id===row.id).file_sizes.bundle:(await stat(resolve(outDir,row.downloads.bundle))).size;}
 // Complete image-index checks remain; this does not regenerate historical media.
 const manifest=await deliverTurntables({...source,assets:expected.assets},outDir,{root});
 for(const id of ids)for(const suffix of ['','-wheel']){const path=`gallery/posters/${id}${suffix}.png`;await mkdir(dirname(resolve(outDir,path)),{recursive:true});await cp(resolve(root,'site/public',path),resolve(outDir,path));}
 await cp(resolve(root,'site/public/gallery/resources.json'),resolve(outDir,'gallery/resources.json'));
 const gallery=await auditGalleryAssets(manifest,{root,outputRoot:outDir});if(manifest.assets.some(a=>a.production_release))await writeFile(resolve(outDir,'gallery/resources.json'),JSON.stringify({...gallery.resources,production_projection:true},null,2)+'\n');
 await writeCatalog(manifest,outDir,{approvedOnly:true});
 await cp(resolve(root,'qa/ci-model-proof/vite-template.html'),resolve(outDir,'index.html'));
 const routes=await writeStaticRoutes(manifest,outDir);
 return {mode:'additive',packaged_ids:[...ids],reused_package_ids:[...oldIds],routes,full_output_audit:'REQUIRED_NEXT'};
}

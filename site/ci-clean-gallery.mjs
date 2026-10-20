/** Collector-free checks before a clean runner captures or imports gallery PNGs. */
import assert from 'node:assert/strict';
import {readFileSync,lstatSync,realpathSync} from 'node:fs';
import {resolve,sep} from 'node:path';
import {pathToFileURL} from 'node:url';
import {enrichManifest} from './asset-delivery.mjs';
import {collectTurntables} from './turntable-delivery.mjs';
import {hashBytes,modelPolicyDigest,modelPolicyDigestAtCommit} from './ci-model-proof.mjs';
import {auditGalleryAssets} from './gallery-assets.mjs';
import {payloadDigest,currentIdentity} from './ci-model-shards.mjs';

// This does NOT return a verifiedBuiltInputs handle. Missing poster pairs may
// exist before capture; only the final independent full projection grants that.
export async function assertPreCaptureInputs({root=process.cwd(),outputRoot='dist'}={}){
 root=resolve(root);outputRoot=resolve(root,outputRoot);
 assert.equal(realpathSync(outputRoot),outputRoot,'Capture build root symlink rejected');
 const read=(base,path)=>{
  assert(typeof path==='string'&&!/[\\\u0000-\u001f?#%:]/.test(path)&&!path.startsWith('/')&&path.split('/').every(part=>part&&part!=='.'&&part!=='..'),'Unsafe capture input path');
  const full=resolve(base,path);assert(full.startsWith(base+sep));assert.equal(realpathSync(full),full,'Capture input symlink rejected');assert(lstatSync(full).isFile());return readFileSync(full);
 };
 const source=JSON.parse(read(root,'assets/manifest.json')),expected=await enrichManifest(source,root),turntables=await collectTurntables(expected,root);
 for(const asset of expected.assets){
  if(turntables.posters.has(asset.id))asset.card_preview=turntables.posters.get(asset.id);
  if(turntables.descriptors.has(asset.id))asset.turntable=turntables.descriptors.get(asset.id);
  for(const kind of ['glb','blend','preview'])assert.equal(hashBytes(read(outputRoot,asset[kind])),asset.sha256[kind],`Pre-capture delivered ${kind} differs: ${asset.id}`);
  asset.file_sizes.bundle=read(outputRoot,asset.downloads.bundle).length;
 }
 assert.equal(read(outputRoot,'assets/manifest.json').toString(),JSON.stringify(expected,null,2)+'\n','Pre-capture manifest differs from independently derived source');
 // Inventory before serving anything; links/special files cannot enter capture.
 const payload_sha256=payloadDigest(outputRoot);
 return {catalog_ids:expected.assets.map(asset=>asset.id).sort(),payload_sha256};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 const identity=currentIdentity();
 assert.equal(modelPolicyDigest(),modelPolicyDigestAtCommit(identity.source_commit),'Pre-capture policy differs from committed source');
 const checked=await assertPreCaptureInputs({});
 await auditGalleryAssets(JSON.parse(readFileSync('assets/manifest.json')),{outputRoot:'dist',requireComplete:false});
 console.log(`Clean gallery input check passed: ${checked.catalog_ids.length} exact source-bound models; no publication collector executed.`);
}

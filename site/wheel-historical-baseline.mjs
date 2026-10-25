import {successorReader,successorContext,historicalGalleryView} from './same-id-successors.mjs';
/** Authenticate the original capture snapshot, then permit strictly additive catalog growth.
 * The 594-asset capture is not relabelled as a capture of the expanded manifest.
 */
import assert from 'node:assert/strict';
import {isDeepStrictEqual} from 'node:util';
import {productionWheelBytes} from './production-wheel-contract.mjs';
import {wheelHash} from './wheel-presentation-contract.mjs';
const DIRECTORY='qa/wheel-parity-20261024/presentation-evidence';
export function assertWheelHistoricalExtension(manifest,resources,baselineManifest,baselineResources){
 const assets=new Map(manifest.assets.map(asset=>[asset.id,asset]));assert.equal(assets.size,manifest.assets.length,'Duplicate current wheel asset');
 assert(manifest.assets.length>=baselineManifest.assets.length,'Historical wheel catalog shrank');
 for(const [i,asset] of baselineManifest.assets.entries())assert(isDeepStrictEqual(manifest.assets[i],asset),'Historical wheel asset metadata/order changed: '+asset.id);
 const added=new Set(manifest.assets.slice(baselineManifest.assets.length).map(asset=>asset.id));
 for(const [key,value] of Object.entries(baselineResources))if(!['posters','files'].includes(key))assert.deepEqual(resources[key],value,'Historical resource metadata changed: '+key);
 for(const [id,poster] of Object.entries(baselineResources.posters))assert.deepEqual(resources.posters[id],poster,'Historical resource poster changed: '+id);
 for(const id of Object.keys(resources.posters))assert(Object.hasOwn(baselineResources.posters,id)||added.has(id),'Unbound additional resource poster: '+id);
 const files=new Map(resources.files.map(pin=>[pin.path,pin]));assert.equal(files.size,resources.files.length,'Duplicate wheel resource seal');
 for(const pin of baselineResources.files)assert.deepEqual(files.get(pin.path),pin,'Historical resource seal changed: '+pin.path);
 const oldPaths=new Set(baselineResources.files.map(pin=>pin.path)),newPaths=new Set([...added].flatMap(id=>[resources.posters[id]?.detail,resources.posters[id]?.wheel]));
 for(const path of files.keys())assert(oldPaths.has(path)||newPaths.has(path),'Unbound additional wheel resource file: '+path);
 return {manifest:baselineManifest,resources:baselineResources};
}
export async function wheelHistoricalBaseline(root,manifest,resources,index){
 const mb=await productionWheelBytes(root,'assets/manifest.json'),rb=await productionWheelBytes(root,'site/public/gallery/resources.json');
 // Always bind the supplied objects to the repository inputs, not caller-selected subsets.
 assert(isDeepStrictEqual(manifest,JSON.parse(mb)),'Caller manifest differs from repository');assert(isDeepStrictEqual(resources,JSON.parse(rb)),'Caller resources differ from repository');
 if(wheelHash(mb)===index.source_manifest_sha256&&wheelHash(rb)===index.source_resources_sha256)return {manifest,resources};
 const oldManifest=await productionWheelBytes(root,DIRECTORY+'/baseline-manifest.json'),oldResources=await productionWheelBytes(root,DIRECTORY+'/baseline-resources.json');
 assert.equal(wheelHash(oldManifest),index.source_manifest_sha256,'Historical manifest snapshot changed');assert.equal(wheelHash(oldResources),index.source_resources_sha256,'Historical resources snapshot changed');
 const read=successorReader(root),context=successorContext({manifest,read});
 return assertWheelHistoricalExtension(context?context.base:manifest,historicalGalleryView({manifest,resources,read}),JSON.parse(oldManifest),JSON.parse(oldResources));
}

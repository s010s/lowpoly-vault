/** Exact publication selector shared by static tests; it creates no acceptance. */
import assert from 'node:assert/strict';
import {collectProductionRelease,appendProductionReleases,assertProductionMetadata} from './production-release.mjs';
export async function collectManifestProduction(root,manifest){
 const publication=manifest.publication||{};
 const registry=Object.hasOwn(publication,'production_registry'),singular=Object.hasOwn(publication,'production_descriptor');
 assert(!(registry&&singular),'Ambiguous singular and registry production release routes');
 const actual=manifest.assets.filter(asset=>asset.production_release);
 if(!registry&&!singular){assert.equal(actual.length,0,'Unbound production assets');return [];}
 const reviewed=registry?(await appendProductionReleases(root,{publication:{},assets:[]},publication.production_registry)).assets:await collectProductionRelease(root,publication.production_descriptor);
 assert.deepEqual(actual.map(asset=>asset.id).sort(),reviewed.map(asset=>asset.id).sort(),'Production manifest subject differs');
 for(const asset of actual)assertProductionMetadata(reviewed.find(item=>item.id===asset.id),asset);
 return reviewed;
}

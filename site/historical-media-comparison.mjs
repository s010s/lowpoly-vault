/** Lazy, read-only comparison view for immutable historical release collectors.
 * Equality needs no manifest; a changed active pointer requires the complete
 * authenticated same-ID selection. Original capture/QA/media checks stay in the
 * caller, so the inverse never substitutes successor bytes for historical proof.
 */
import {isDeepStrictEqual} from 'node:util';
import {historicalTurntableView,historicalGalleryView,successorReader} from './same-id-successors.mjs';
export function historicalMediaComparison({root,turntables,gallery}){
 let manifest,read,historicalCards,historicalGallery;
 const context=()=>{read??=successorReader(root);manifest??=JSON.parse(read('assets/manifest.json'));return {manifest,read};};
 return {
  cardRows(id,expected){
   const current=turntables.posters.filter(row=>row.id===id);
   if(isDeepStrictEqual(current,expected))return current;
   historicalCards??=historicalTurntableView({...context(),turntables});
   return historicalCards.posters.filter(row=>row.id===id);
  },
  galleryPoster(id,expected){
   const current=gallery.posters[id];
   if(isDeepStrictEqual(current,expected))return current;
   historicalGallery??=historicalGalleryView({...context(),resources:gallery});
   return historicalGallery.posters[id];
  }
 };
}

/** Preserve pinned publication receipts only when every main842 render input is exact.
 * No pixels, receipt, approval, subject key or capture obligation is rewritten. */
import assert from 'node:assert/strict';
import {isDeepStrictEqual} from 'node:util';
import {posterSharedInputs} from './gallery-poster-inputs.mjs';
import {assertMain842PosterRecipe} from './gallery-main842-compat.mjs';

export async function assertRecordedGalleryRecipe(recorded,root=process.cwd()){
 const current=await posterSharedInputs(root);
 if(isDeepStrictEqual(recorded,current))return current;
 const historical=await assertMain842PosterRecipe({root,shared:current});
 assert.deepEqual(recorded,historical,'Pinned gallery receipt must equal the exact proven main842 recipe');
 return historical;
}

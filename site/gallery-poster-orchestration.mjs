/** Supported capture selection API. Never accepts a repository-authored cache receipt. */
import {cp,mkdtemp,writeFile,rename,rm} from 'node:fs/promises';
import {resolve} from 'node:path';
import {auditGalleryAssets} from './gallery-assets.mjs';
import {modelPolicyDigest} from './ci-model-proof.mjs';
import {fetchVerifiedPosterBaseline} from './gallery-poster-cache.mjs';
import {selectPosterCaptures,importVerifiedPosters,writePosterProof,posterRuntime} from './gallery-poster-proof.mjs';

const sessions=new WeakMap();
export async function preparePosterCapture(initial,{root,outputRoot,manifest}){
 const shared=initial.inputState.shared,policy_sha256=modelPolicyDigest(root),runtime=posterRuntime(shared);
 const found=(process.env.CI_GALLERY_FORCE_FULL==='true'||process.env.GITHUB_EVENT_NAME==='workflow_dispatch')?{verified:null,reasons:['Explicit full poster capture requested']}:await fetchVerifiedPosterBaseline({root,shared,policy_sha256,runtime});
 const selection=selectPosterCaptures({manifest,shared,approved:initial.inputState.approved,verified:found.verified,policy_sha256,runtime});
 let next=initial;
 if(selection.reused.some(id=>!initial.inputState.approved.includes(id))){
  const staging=await mkdtemp(resolve(outputRoot,'.gallery-reuse-'));
  try{
   await cp(resolve(outputRoot,'gallery'),resolve(staging,'gallery'),{recursive:true});
   const imported=await importVerifiedPosters({manifest,shared,resources:initial.resources,outputRoot:staging,approved:initial.inputState.approved,verified:found.verified,policy_sha256,runtime});
   await writeFile(resolve(staging,'gallery/resources.json'),JSON.stringify(imported.resources,null,2)+'\n');
   await auditGalleryAssets(manifest,{root,outputRoot:staging});
   const previous=resolve(staging,'previous-gallery');await rename(resolve(outputRoot,'gallery'),previous);
   try{await rename(resolve(staging,'gallery'),resolve(outputRoot,'gallery'));}catch(error){await rename(previous,resolve(outputRoot,'gallery'));throw error;}
   next=await auditGalleryAssets(manifest,{root,outputRoot});
  }finally{await rm(staging,{recursive:true,force:true});}
 }
 Object.assign(initial,next);initial.inputState.capture=selection.capture;
 sessions.set(initial,{root,outputRoot,manifest,shared,policy_sha256,runtime,approved:initial.inputState.approved,verified:found.verified,captured:selection.capture});
 console.log(`Poster selection: ${selection.capture.length} fresh captures, ${selection.reused.length} independently verified artifact pairs, ${initial.inputState.approved.length} unchanged historical golden pairs.`);
 if(!found.verified&&found.reasons.length)console.log(`Poster baseline unavailable: ${found.reasons.join('; ')}`);
 return selection;
}
export async function completePosterCapture(initial,resources){
 const context=sessions.get(initial);if(!context)return null;
 return writePosterProof({...context,resources});
}

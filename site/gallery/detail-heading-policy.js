/** Opt-in bounds for the initial pose of reviewed assets only.
 * Bounds from all original GLB vertices projected by PreviewRenderer at canonical
 * framing, converted to the transparent square poster coordinate system. No GLB
 * wait, pixel scan, runtime fetch, or camera/model mutation. */
const leptomitusBounds=Object.freeze([0.41853058174532254,0.03951666312201862,0.5852153989975197,0.850449296276733]);
const reviewed=new Map([['leptomitus',Object.freeze([{
 glb:'693a8498e9bc4776fd57c33edad7ff38e53216c7b46ea7cfc5b1453765007196',
 detail:'gallery/reviewed-release-20261114-05/leptomitus/detail.png',
 preview:'979deaf0e5d970dddb88b7d34c7e1c09b6d3305dc882ecbed0dfee76c8837c89',
 bounds:leptomitusBounds,
},{
 glb:'47965d4caa9670d1da06f23e295891e4f46054b4649571ec6f5d3e424a612deb',
 detail:'gallery/repairs/leptomitus/material-20261118/detail.png',
 preview:'ffa1c5f2a3b9d733871b336e6a1ae0306d3a96bd476822a1d084e8b4af30b4a6',
 bounds:leptomitusBounds,
}].map(Object.freeze))]]);
// Delivery verifies poster bytes offline. At runtime only the GLB hash and
// the exact versioned detail path are present for this opt-in lookup.
export function reviewedHeadingProfile(asset){
 return reviewed.get(asset?.id)?.find(p=>asset.sha256?.glb===p.glb&&asset.galleryPosters?.detail===p.detail)??null;
}
export function projectedHeadingBounds(rect,bounds){
 const size=Math.min(rect.width,rect.height);
 const x=rect.left+(rect.width-size)/2-.06*size,y=rect.top+(rect.height-size)/2;
 return {left:x+bounds[0]*size,top:y+bounds[1]*size,right:x+bounds[2]*size,bottom:y+bounds[3]*size};
}
const overlaps=(a,b)=>Math.min(a.right,b.right)>Math.max(a.left,b.left)&&Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top);
export function createDetailHeadingLayout({heading,title,stage,footer,button,isMobile}){
 let selected=null;
 const resetHeading=()=>{
  heading.classList.remove('detail-heading-side','detail-heading-compact');
  heading.style.removeProperty('--detail-heading-width');
  heading.style.removeProperty('--detail-heading-left');
 };
 const resetButton=()=>{
  button.classList.remove('detail-interact-side');
  button.style.removeProperty('--detail-interact-left');
 };
 const apply=asset=>{
  selected=asset;
  resetHeading();resetButton();
  const profile=reviewedHeadingProfile(asset);
  if(!profile)return;
  const rect=stage.getBoundingClientRect();
  if(!rect.width||!rect.height)return;
  const model=projectedHeadingBounds(rect,profile.bounds);
  if(isMobile()){
   const control=button.getBoundingClientRect();
   if(!control.width||!overlaps(control,model))return;
   const right=model.right+12,left=model.left-control.width-12;
   const position=right+control.width<=rect.right-16?right:left>=rect.left+16?left:null;
   if(position===null)return;
   button.style.setProperty('--detail-interact-left',position-rect.left+'px');
   button.classList.add('detail-interact-side');
   return;
  }
  if(!overlaps(title.getBoundingClientRect(),model))return;
  const preferred=heading.getBoundingClientRect().left;
  const footerTop=footer.getBoundingClientRect().top-16;
  const rightColumnStart=model.right+16;
  // Try the original reading side first. A right-hand column can fit the
  // same full heading when increased text size would overfill the left.
  for(const [left,right] of [[preferred,model.left-16],[rightColumnStart,rect.right-16]]){
   const available=Math.floor(right-left);
   if(available<180)continue;
   heading.style.setProperty('--detail-heading-width',available+'px');
   heading.style.setProperty('--detail-heading-left',left-rect.left+'px');
   heading.classList.add('detail-heading-side');
   if(available<240||heading.getBoundingClientRect().bottom>footerTop)heading.classList.add('detail-heading-compact');
   if(heading.getBoundingClientRect().bottom<=footerTop)return;
   resetHeading();
  }
  // The original format remains readable if neither side column fits.
 };
 // Never recalculate from the interactive camera; its independent motion is
 // not another layout event.
 return {apply,refresh:()=>{if(selected)apply(selected);}};
}

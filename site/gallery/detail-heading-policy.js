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
}].map(Object.freeze))],['sawdonia',Object.freeze([Object.freeze({
 glb:'6d62e6890268274ed9930a156b574f2e5901bb5ce5051e62b9c821da7e357356',
 detail:'gallery/reviewed-release-20261114-06/sawdonia/detail.png',
 preview:'8f8fc3397860873be9f4a1f7756560cc73acef9cbca6258e62e360dfbdb96dc2',
 bounds:Object.freeze([0.303429945259016,0.15390621080320468,0.7102649641251585,0.8605725078342307]),
 mobileOnly:true,
 mobileTools:true,
})])],['spyroceras',Object.freeze([Object.freeze({
 glb:'2a08b6e6d97ef9b5c7fe36cbdb49c335afbd772d2e503b3bd56d54cfe73b2a54',
 detail:'gallery/reviewed-release-20261114-06/spyroceras/detail.png',
 preview:'8cdceb2ed2544054308026bd9a7d047b37d42b7b16204a2f344da0a72d62a01d',
 bounds:Object.freeze([0.4020327018770514, 0.056135696539828084, 0.580190431235307, 0.8556603907833367]),
})])],['diplomoceras',Object.freeze([Object.freeze({
 glb:'6dad0da9076f6b7afbfc22c578f8886801c17639c5cb138aeb99074bdaca9a67',
 detail:'gallery/posters/diplomoceras.png',
 preview:'dbb5971ef2590f7941d27be91dd65dc94a81afd57f8e9d1310af3cf549f98e3e',
 // Full alpha + exact initial 3D projection in the legacy square, padded 1px.
 bounds:Object.freeze([162/512,45/512,508/512,478/512]),
 desktopOnly:true,
})])]]);
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
export function createDetailHeadingLayout({heading,title,stage,footer,button,tools,download,isMobile}){
 let selected=null;
 const resetHeading=()=>{
  heading.classList.remove('detail-heading-side','detail-heading-compact');
  heading.style.removeProperty('--detail-heading-width');
  heading.style.removeProperty('--detail-heading-left');
 };
 const resetButton=()=>{
  button.classList.remove('detail-interact-side','detail-interact-above');
  button.style.removeProperty('--detail-interact-left');
  button.style.removeProperty('--detail-interact-top');
 };
 const resetTools=()=>{
  footer.classList.remove('detail-tools-side');
  for(const field of ['left','width','bottom','flow-height'])footer.style.removeProperty('--detail-tools-'+field);
 };
 const moveTools=(rect,model)=>{
  if(!tools||!download)return;
  const normal=tools.getBoundingClientRect();
  if(!normal.width||!overlaps(normal,model))return;
  const box=footer.getBoundingClientRect(),card=download.getBoundingClientRect();
  const topControl=button.getBoundingClientRect();
  for(const [left,right,side] of [[model.right+12,rect.right-16,'right'],[rect.left+16,model.left-12,'left']]){
   const width=Math.floor(Math.min(104,right-left));
   if(width<88)continue;
   const x=side==='right'?right-width:left;
   footer.style.setProperty('--detail-tools-left',x-box.left+'px');
   footer.style.setProperty('--detail-tools-width',width+'px');
   footer.style.setProperty('--detail-tools-bottom',box.bottom-normal.bottom+'px');
   footer.style.setProperty('--detail-tools-flow-height',normal.height+'px');
   footer.classList.add('detail-tools-side');
   const placed=tools.getBoundingClientRect();
   if(placed.top>=Math.max(rect.top+16,heading.getBoundingClientRect().bottom+8)
     &&!overlaps(placed,model)&&!overlaps(placed,card)&&!overlaps(placed,topControl))return;
   resetTools();
  }
 };
 const apply=asset=>{
  selected=asset;
  resetHeading();resetButton();resetTools();
  const profile=reviewedHeadingProfile(asset);
  if(!profile||(profile.desktopOnly&&isMobile()))return;
  const rect=stage.getBoundingClientRect();
  if(!rect.width||!rect.height)return;
  const model=projectedHeadingBounds(rect,profile.bounds);
  if(isMobile()){
   const control=button.getBoundingClientRect();
   if(control.width&&overlaps(control,model)){
    const right=model.right+12,left=model.left-control.width-12;
    const position=right+control.width<=rect.right-16?right:left>=rect.left+16?left:null;
    if(position!==null){
     button.style.setProperty('--detail-interact-left',position-rect.left+'px');
     button.classList.add('detail-interact-side');
    }else if(profile.mobileTools){
     // The full English label may be wider than either side. Only use
     // the free band above the specimen when it clears the whole heading.
     const top=model.top-12-control.height;
     if(top>=Math.max(rect.top+16,heading.getBoundingClientRect().bottom+8)){
      button.style.setProperty('--detail-interact-top',top-rect.top+'px');
      button.classList.add('detail-interact-above');
     }
    }
   }
   if(profile.mobileTools)moveTools(rect,model);
   return;
  }
  if(profile.mobileOnly)return;
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

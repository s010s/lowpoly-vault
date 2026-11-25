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
 glb:'ef144a99db868bf0e9c9786f4f396d5a4915dac1e22f913ba0c8fd341df0b21e',
 detail:'gallery/repairs/leptomitus/material-20261118/detail.png',
 preview:'ffa1c5f2a3b9d733871b336e6a1ae0306d3a96bd476822a1d084e8b4af30b4a6',
 bounds:leptomitusBounds,
}].map(Object.freeze))],['sawdonia',Object.freeze([Object.freeze({
 glb:'3f6e42b9ea26b9acadf2691f0d853b882cd43439247e0579fe78ae384c8daa35',
 detail:'gallery/ws1a-repair-20261125-07/sawdonia/detail.png',
 preview:'974716b4e472fa69f8be90bd3499da192027ba6f1baf8fd5d068e44ee81df3eb',
 bounds:Object.freeze([0.303429945259016,0.15390621080320468,0.7102649641251585,0.8605725078342307]),
 mobileOnly:true,
 mobileTools:true,
})])],['spyroceras',Object.freeze([Object.freeze({
 glb:'09f51c0e0ac3cf13c171fe0fef81e2a3ea01e2f4393928cdd4045f5e2757ae71',
 detail:'gallery/ws1a-repair-20261125-08/spyroceras/detail.png',
 preview:'5c5353edda5aa74cdc26317dc6a3aaba78f8bf01bad26b70d38f55c8528d64a6',
 bounds:Object.freeze([0.4020327018770514, 0.056135696539828084, 0.580190431235307, 0.8556603907833367]),
})])],['chaloneria',Object.freeze([Object.freeze({
 glb:'bb73e1de4010944f1ee455deb69530241bded201b91271d85ef52f7e180733d7',
 detail:'gallery/ws1a-repair-20261125-02/chaloneria/detail.png',
 preview:'fdafcf6171013290f2e8b8acacd2edfb6d0c1553a145a7060770cce6f29dcf28',
 // Canonical projected mesh and matching poster subject; padded by two poster pixels.
 bounds:Object.freeze([0.45075812716623764,0.04283366259586899,0.5669514764562911,0.8756414949704007]),
 desktopOnly:true,
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
const HASH=/^[a-f0-9]{64}$/;
const validDesktopBounds=(entry,glb,detail)=>entry?.version===1&&entry.kind==='legacy-square-subject'
 &&typeof glb==='string'&&HASH.test(glb)&&entry.glb===glb&&typeof detail==='string'
 &&/^gallery\/posters\/[a-z0-9-]+\.png$/.test(detail)&&entry.detail===detail
 &&typeof entry.detail_sha256==='string'&&HASH.test(entry.detail_sha256)
 &&Number.isSafeInteger(entry.detail_bytes)&&entry.detail_bytes>0
 &&Array.isArray(entry.bounds)&&entry.bounds.length===4&&entry.bounds.every(x=>Number.isFinite(x)&&x>=0&&x<=1)
 &&entry.bounds[0]<entry.bounds[2]&&entry.bounds[1]<entry.bounds[3];

// Called only with the final resolved poster; wheel/preview bytes are not substitutes.
export function resolveDesktopHeadingBounds(asset,poster,resources){
 const entry=poster?.desktopHeadingBounds,glb=asset?.sha256?.glb,detail=poster?.detail;
 if(!entry||poster.detailPresentation||poster.source_glb_sha256!==glb||!validDesktopBounds(entry,glb,detail)||!Array.isArray(resources?.files))return null;
 const pins=resources.files.filter(file=>file?.path===detail);
 if(pins.length!==1||pins[0].sha256!==entry.detail_sha256||pins[0].bytes!==entry.detail_bytes)return null;
 return {version:1,kind:'legacy-square-subject',glb,detail,detail_sha256:entry.detail_sha256,detail_bytes:entry.detail_bytes,bounds:[...entry.bounds]};
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
  const phone=isMobile(), reviewedProfile=reviewedHeadingProfile(asset);
  const candidate=asset?.desktopHeadingBounds;
  const desktop= !phone&&!asset?.detailPresentation
   &&validDesktopBounds(candidate,asset?.sha256?.glb,asset?.galleryPosters?.detail)?candidate:null;
  // Preserve all previous reviewed policies; no new mobile/3D path.
  const profile=reviewedProfile||desktop;
  if(!profile||(profile.desktopOnly&&phone))return;
  const rect=stage.getBoundingClientRect();
  if(!rect.width||!rect.height)return;
  const model=projectedHeadingBounds(rect,profile.bounds);
  if(phone){
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
   const placed=heading.getBoundingClientRect();
   const card=download?.getBoundingClientRect();
   if(placed.bottom<=footerTop&&(!desktop||reviewedProfile||(!overlaps(placed,model)&&(!card||!overlaps(placed,card)))))return;
   resetHeading();
  }
  // The original format remains readable if neither side column fits.
 };
 // Never recalculate from the interactive camera; its independent motion is
 // not another layout event.
 return {apply,refresh:()=>{if(selected)apply(selected);}};
}

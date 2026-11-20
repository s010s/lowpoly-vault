/** A release-catalog canonical detail role is selected by GLB identity at build
 * time. Like the existing image loader, runtime does not independently hash PNGs. */
const SHA=/^[a-f0-9]{64}$/;
function hasCanonicalDetail(asset) {
 const path=asset?.galleryPosters?.detail;
 return SHA.test(asset?.sha256?.glb||'')&&typeof path==='string'&&
  (path.startsWith('gallery/')||path.startsWith('detail-presentations/'))&&
  !/[\\\u0000-\u001f?#%]/.test(path)&&path.split('/').every(p=>p&&p!=='.'&&p!=='..');
}
export function canonicalEntrancePlan({asset,isPhone,openMobile,activateMobile,opening,reviewOnly=false}){
 const canonicalFirst=Boolean(!reviewOnly&&isPhone&&openMobile&&!activateMobile&&opening?.id&&opening.id===asset?.id&&hasCanonicalDetail(asset));
 return {canonicalFirst,opening:canonicalFirst?{...opening,art:null}:opening};
}

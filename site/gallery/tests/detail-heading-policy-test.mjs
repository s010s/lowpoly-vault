import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {createDetailHeadingLayout,projectedHeadingBounds,reviewedHeadingProfile} from '../detail-heading-policy.js';

const root=new URL('../../../',import.meta.url);
const file=p=>readFileSync(fileURLToPath(new URL(p,root)));
const asset=JSON.parse(file('assets/manifest.json')).assets.find(a=>a.id==='leptomitus');
const profile=reviewedHeadingProfile(asset);
assert.ok(profile,'reviewed GLB and exact gallery-detail path must match');
const digest=bytes=>createHash('sha256').update(bytes).digest('hex');
assert.equal(digest(file(asset.glb)),profile.glb);
assert.equal(digest(file('site/public/'+profile.detail)),profile.preview);
const pins=JSON.parse(file('site/public/gallery/resources.json')).files;
assert.equal(pins.find(pin=>pin.path===profile.detail)?.sha256,profile.preview);
assert.equal(asset.sha256.preview,profile.preview);
assert.equal(digest(file(asset.preview)),profile.preview);
for(const id of ['toString','constructor','__proto__','confuciusornis',null,undefined]){
 assert.equal(reviewedHeadingProfile({...asset,id}),null);
}
assert.equal(reviewedHeadingProfile({...asset,sha256:{glb:'bad'}}),null);
assert.equal(reviewedHeadingProfile({...asset,galleryPosters:{detail:'wrong.png'}}),null);
assert.equal(reviewedHeadingProfile(null),null);
const box=projectedHeadingBounds({left:407.515625,top:62,width:1032.484375,height:938},profile.bounds);
assert.ok(Math.abs(box.left-791.0594981771126)<.001);
assert.ok(Math.abs(box.top-99.06663000845347)<.001);
console.log('Exact Leptomitus GLB, canonical detail PNG and pin bytes match:',profile.glb,profile.preview);

const saw=JSON.parse(file('assets/manifest.json')).assets.find(a=>a.id==='sawdonia');
const sawProfile=reviewedHeadingProfile(saw);
assert.ok(sawProfile?.mobileOnly&&sawProfile.mobileTools);
for(const role of ['glb','blend','preview'])assert.equal(digest(file(saw[role])),saw.sha256[role]);
for(const path of Object.values(saw.galleryPosters)){
 const pin=pins.find(pin=>pin.path===path),bytes=file('site/public/'+path);
 assert.equal(bytes.length,pin?.bytes);
 assert.equal(digest(bytes),pin?.sha256);
}
assert.equal(sawProfile.preview,saw.sha256.preview);
assert.equal(reviewedHeadingProfile({...saw,sha256:{glb:'bad'}}),null);
assert.equal(reviewedHeadingProfile({...saw,galleryPosters:{...saw.galleryPosters,detail:'wrong.png'}}),null);

// At a layout where neither side nor the band above the specimen is safe,
// leave the original controls and all unrelated styles alone.
const rect=(left,top,width,height)=>({left,top,width,height,right:left+width,bottom:top+height});
function element(bounds){
 const classes=new Set(),style=new Map([['--unrelated','keep']]);
 return {getBoundingClientRect:()=>bounds,classes,styles:style,
  classList:{remove:(...keys)=>keys.forEach(key=>classes.delete(key)),add:key=>classes.add(key)},
  style:{removeProperty:key=>style.delete(key),setProperty:(key,value)=>style.set(key,value)}};
}
const stage=element(rect(0,55,280,515));
const heading=element(rect(16,85,248,200));
const footer=element(rect(12,365,256,186));
const button=element(rect(55,198,170,44));
const tools=element(rect(14,371,252,44));
const download=element(rect(12,429,256,122));
const layout=createDetailHeadingLayout({heading,title:heading,stage,footer,button,tools,download,isMobile:()=>true});
layout.apply(saw);
assert.deepEqual([...button.classes],[]);
assert.deepEqual([...footer.classes],[]);
assert.deepEqual([...button.styles],[['--unrelated','keep']]);
assert.deepEqual([...footer.styles],[['--unrelated','keep']]);
assert.deepEqual(button.getBoundingClientRect(),rect(55,198,170,44));
assert.deepEqual(tools.getBoundingClientRect(),rect(14,371,252,44));
console.log('Sawdonia five exact files, reviewed-path gate and cramped control fallback pass');

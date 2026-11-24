import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {createDetailHeadingLayout,projectedHeadingBounds,reviewedHeadingProfile} from '../detail-heading-policy.js';

const root=new URL('../../../',import.meta.url);
const read=p=>readFileSync(new URL(p,root));
const hash=b=>createHash('sha256').update(b).digest('hex');
const asset=JSON.parse(read('assets/manifest.json')).assets.find(a=>a.id==='chaloneria');
const resources=JSON.parse(read('site/public/gallery/resources.json'));
const profile=reviewedHeadingProfile(asset);
assert.ok(profile?.desktopOnly);
assert.equal(profile.glb,resources.posters.chaloneria.source_glb_sha256);
assert.equal(profile.detail,resources.posters.chaloneria.detail);
assert.equal(profile.preview,asset.sha256.preview);
const [poster]=resources.files.filter(x=>x.path===profile.detail);
assert.equal(poster.sha256,profile.preview);
const detailBytes=read('site/public/'+profile.detail);
assert.equal(detailBytes.length,poster.bytes);
assert.equal(hash(detailBytes),profile.preview);
assert.equal(hash(read(asset.glb)),profile.glb);
assert.equal(reviewedHeadingProfile({...asset,id:'other'}),null);
assert.equal(reviewedHeadingProfile({...asset,sha256:{...asset.sha256,glb:'f'.repeat(64)}}),null);
assert.equal(reviewedHeadingProfile({...asset,galleryPosters:{...asset.galleryPosters,detail:'changed.png'}}),null);

const rect=(left,top,width,height)=>({left,top,width,height,right:left+width,bottom:top+height});
const stage=rect(407.515625,62,1032.484375,938);
const box=projectedHeadingBounds(stage,profile.bounds);
// Each all-vertex bound from the exact recorded 1440x1000 default is inside
// the padded canonical box, not inferred from a single pixel of the title.
assert.ok(box.left<822.51029&&box.right>929.05694&&box.top<103.39933&&box.bottom>882.13036);
assert.ok(box.left>820&&box.right<931&&box.top>101&&box.bottom<884);
const fixed=bounds=>({getBoundingClientRect:()=>bounds});
let mobile=false;
const classes=new Set(),styles=new Map();
const heading={
 getBoundingClientRect:()=>rect(446,100,Number.parseFloat(styles.get('--detail-heading-width'))||731,classes.has('detail-heading-side')?110:65),
 classList:{remove:(...keys)=>keys.forEach(key=>classes.delete(key)),add:key=>classes.add(key)},
 style:{removeProperty:key=>styles.delete(key),setProperty:(k,v)=>styles.set(k,v)},
};
const fake=()=>({classList:{remove:()=>{}},style:{removeProperty:()=>{}}});
const layout=createDetailHeadingLayout({heading,title:heading,stage:fixed(stage),footer:{...fake(),getBoundingClientRect:()=>rect(444,700,950,280)},button:fake(),isMobile:()=>mobile});
layout.apply(asset);
assert.ok(classes.has('detail-heading-side'));
assert.ok(heading.getBoundingClientRect().right<=box.left-16);
layout.apply({...asset,id:'unrelated'});
assert.equal(classes.size,0);
assert.equal(styles.size,0);
mobile=true;
layout.apply(asset);
assert.equal(classes.size,0);
assert.equal(styles.size,0);
console.log('A868 exact GLB and PNG, padded canonical bounds, desktop-only side placement and scope guard pass');

import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {projectedHeadingBounds,reviewedHeadingProfile} from '../detail-heading-policy.js';

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

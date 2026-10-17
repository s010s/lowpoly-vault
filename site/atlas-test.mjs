import assert from 'node:assert/strict';
import {layoutRegions,slotPosition,visibleSlots,ATLAS_LIMIT} from './atlas.js';
import {CatalogStore} from './catalog.js';
import {createCatalog} from './catalog-build.mjs';
import {readFile} from 'node:fs/promises';
const real=JSON.parse(await readFile('assets/manifest.review.json','utf8')).assets;
for(const count of [10,10000]){
 const items=Array.from({length:count},(_,i)=>({...real[i%real.length],id:`asset-${String(i).padStart(5,'0')}`,name:{en:`Asset ${String(i).padStart(5,'0')}`},category:['geology','plants','wood','traces'][i%4]}));
 const categories=['geology','plants','wood','traces'].map(id=>({id,count:items.filter(a=>a.category===id).length}));
 const regions=layoutRegions(categories);assert.equal(regions.reduce((n,r)=>n+r.count,0),count);
 let maximum=0;for(let x=-300;x<13000;x+=317)for(let y=-300;y<13000;y+=491){let visible=[];for(const r of regions){visible.push(...visibleSlots(r,{x,y,width:1600,height:1100},ATLAS_LIMIT-visible.length));if(visible.length>=ATLAS_LIMIT)break;}maximum=Math.max(maximum,visible.length);assert(visible.length<=80);}
 for(const r of regions){const p=slotPosition(r,0);assert.equal(p.x,r.x+45);assert.equal(p.y,r.y+90);assert.deepEqual(visibleSlots(r,{x:r.x,y:r.y,width:400,height:400}),visibleSlots(r,{x:r.x,y:r.y,width:400,height:400}));}
 console.log(`${count} layouts: deterministic category slots, bounded visible candidates (${maximum} max, cap ${ATLAS_LIMIT})`);
}
console.log('Atlas geometry checks passed. DOM and interaction checks run separately in the cloud browser.');

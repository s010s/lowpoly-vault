/** Historical isolation is checked at the exact model commit; live bytes are checked separately. */
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
export function assertOnlyTargetChanged(before,after,id){
 assert(before.assets.some(a=>a.id===id)&&after.assets.some(a=>a.id===id),'Target missing');
 assert.deepEqual(after.assets.filter(a=>a.id!==id),before.assets.filter(a=>a.id!==id),'Integration changed unrelated assets');
 const {assets:oldAssets,...oldMeta}=before,{assets:newAssets,...newMeta}=after;
 assert.deepEqual(newMeta,oldMeta,'Integration changed manifest-level metadata');
 assert.notDeepEqual(after.assets.find(a=>a.id===id),before.assets.find(a=>a.id===id),'No target change');
}
const ownedBy=(path,id)=>path.split('/').some(part=>part===id||part===id+'.png'||part===id+'-wheel.png');
export function assertCurrentTargetResources(introduced,current,id){
 assert.deepEqual(current.posters[id],introduced.posters[id],'Current target poster differs from integrated version');
 const target=resources=>resources.files.filter(row=>ownedBy(row.path,id));
 assert.deepEqual(target(current),target(introduced),'Current target resource files differ from integrated version');
}
export function assertOnlyTargetResourcesChanged(before,after,id){
 const {posters:oldPosters,files:oldFiles,...oldMeta}=before,{posters:newPosters,files:newFiles,...newMeta}=after;
 assert.deepEqual(newMeta,oldMeta,'Unrelated resource metadata changed');
 const without=rows=>Object.fromEntries(Object.entries(rows).filter(([key])=>key!==id));
 assert.deepEqual(without(newPosters),without(oldPosters),'Unrelated poster changed');
 const unrelated=rows=>rows.filter(row=>!ownedBy(row.path,id));
 assert.deepEqual(unrelated(newFiles),unrelated(oldFiles),'Unrelated resource file changed');
}
export function assertModelIntegrationIsolation({id,subject,currentManifest,currentResources}){
 const hashes=execFileSync('git',['log','--format=%H%x09%s','--fixed-strings','--grep='+subject,'--','assets/manifest.json'],{encoding:'utf8'}).trim().split('\n').filter(line=>line.slice(41)===subject).map(line=>line.slice(0,40));
 assert.equal(hashes.length,1,'Expected one explicitly named model integration commit');
 const integration=hashes[0];assert.match(integration,/^[a-f0-9]{40}$/);
 const at=(ref,path)=>JSON.parse(execFileSync('git',['show',`${ref}:${path}`],{encoding:'utf8',maxBuffer:16*1024*1024}));
 const before=at(integration+'^','assets/manifest.json'),introduced=at(integration,'assets/manifest.json');
 assertOnlyTargetChanged(before,introduced,id);
 assertOnlyTargetResourcesChanged(at(integration+'^','site/public/gallery/resources.json'),at(integration,'site/public/gallery/resources.json'),id);
 assertCurrentTargetResources(at(integration,'site/public/gallery/resources.json'),currentResources,id);
 assert.deepEqual(currentManifest.assets.find(a=>a.id===id),introduced.assets.find(a=>a.id===id),'Current target differs from integrated version; update its verification');
 return integration;
}

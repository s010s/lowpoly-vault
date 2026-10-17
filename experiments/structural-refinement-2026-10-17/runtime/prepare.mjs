/** Review-only exact-GLB input preparation. Never changes published metadata. */
import {readFile,writeFile,mkdir,cp} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const hash=b=>createHash('sha256').update(b).digest('hex');
const root=process.cwd(),plan=JSON.parse(await readFile(process.argv[2]));
const original=JSON.parse(await readFile('assets/manifest.json'));
const assets=[];
for(const item of plan.assets){
  const previous=original.assets.find(a=>a.id===item.id);assert(previous);
  assert(!item.glb.startsWith('/')&&!item.glb.split('/').includes('..'));
  const bytes=await readFile(item.glb);assert.equal(hash(bytes),item.glb_sha256);
  assert(Array.isArray(item.dimensions)&&item.dimensions.length===3);
  const path=`review-candidates/${item.id}.glb`;
  await mkdir(dirname(resolve('dist',path)),{recursive:true});await cp(item.glb,resolve('dist',path));
  assets.push({...previous,glb:path,dimensions:item.dimensions,triangles:item.triangles,
    sha256:{...previous.sha256,glb:item.glb_sha256},quality_status:'review_pending'});
}
assert(assets.length>0);
await mkdir('dist/assets',{recursive:true});
await writeFile('dist/assets/manifest.json',JSON.stringify({...original,review_only:true,assets},null,2)+'\n');
await writeFile('dist/review-plan.json',JSON.stringify(plan,null,2)+'\n');
console.log(`Prepared ${assets.length} review-only candidate inputs; original publication is unchanged.`);

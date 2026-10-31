/** HTTP readback of this batch after GitHub Pages reports deployment success.
 * No credentials, mutations or alternate network route. Future revisions of an
 * ID are reported as superseded and checked by their own release coordinator.
 */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const folder='production/creature36-20261031',ledger=JSON.parse(await readFile(folder+'/integration-ledger.json')),source=JSON.parse(await readFile('assets/manifest.json')),resources=JSON.parse(await readFile('site/public/gallery/resources.json'));
const expected=process.env.DEPLOYED_SHA;assert(/^[a-f0-9]{40}$/.test(expected||''));
const base=new URL(process.env.SITE_URL);assert.equal(base.origin,'https://s010s.github.io');assert.equal(base.pathname,'/lowpoly-vault/');
const report={status:'RUNNING',source_commit:expected,scope:'Actual public GitHub Pages HTTP bytes from GitHub Actions, not a browser or physical-device test.',models:[],superseded:[]};
const get=async(path,method='GET')=>{assert(!path.startsWith('/')&&!path.includes('..'));const u=new URL(path,base);u.searchParams.set('deployment',expected);const r=await fetch(u,{method,signal:AbortSignal.timeout(60000),cache:'no-store'});assert(r.ok,`${path}: HTTP ${r.status}`);return r;};
const sha=b=>createHash('sha256').update(b).digest('hex');
const escapeHTML=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
try{
 const marker=await(await get('release-build.json')).json();assert.equal(marker.source_commit,expected);
 const manifest=await(await get('assets/manifest.json')).json(),gallery=await(await get('assets/gallery.json')).json();
 assert.deepEqual(manifest.assets.map(a=>a.id),source.assets.map(a=>a.id));assert.equal(gallery.assets.length,source.assets.length);report.total_catalog_ids=manifest.assets.length;
 for(const row of ledger.models){
  const current=source.assets.find(a=>a.id===row.id);assert(current);
  if(current.sha256.glb!==row.glb_sha256){report.superseded.push(row.id);continue;}
  const live=manifest.assets.find(a=>a.id===row.id),display=gallery.assets.find(a=>a.id===row.id);assert(live&&display);assert.equal(live.sha256.glb,row.glb_sha256);assert.equal(display.sha256.glb,row.glb_sha256);assert.equal(live.glb,row.glb);assert.deepEqual(live.dimensions,current.dimensions);
  const glb=Buffer.from(await(await get(live.glb)).arrayBuffer());assert.equal(sha(glb),row.glb_sha256);assert.equal(glb.length,row.glb_bytes);
  const poster=resources.posters[row.id],images=[];
  for(const role of ['wheel','detail']){const path=poster[role],pin=resources.files.find(f=>f.path===path);assert(pin);const b=Buffer.from(await(await get(path)).arrayBuffer());assert.equal(sha(b),pin.sha256);images.push({role,path,sha256:sha(b),bytes:b.length});assert.equal(display.galleryPosters[role],path);}
  for(const [path,lang] of [[`models/${row.id}/`,'en'],[`zh-CN/models/${row.id}/`,'zh']]){const html=await(await get(path)).text();assert(html.includes(escapeHTML(current.name[lang])),`Localized model name missing: ${path}`);}
  const blend=await get(live.blend,'HEAD');assert.equal(Number(blend.headers.get('content-length')),current.file_sizes.blend);
  report.models.push({id:row.id,status:'PASS',glb_sha256:sha(glb),glb_bytes:glb.length,posters:images,bilingual_pages:true,blend_head_bytes:current.file_sizes.blend});
  console.log('LIVE_BYTES_PASS',row.id,glb.length,row.glb_sha256);
 }
 report.status='PASS';assert.equal(report.models.length+report.superseded.length,36);
}catch(error){report.status='FAIL';report.error=error.message;process.exitCode=1;}
await mkdir('qa/live-smoke',{recursive:true});await writeFile('qa/live-smoke/creature36-readback.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({status:report.status,source_commit:expected,verified:report.models.length,superseded:report.superseded,error:report.error}));

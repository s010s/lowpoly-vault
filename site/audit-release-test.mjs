/** Exercise the real final inventory audit at catalog shard boundaries. */
import assert from 'node:assert/strict';
import {mkdtemp, mkdir, readFile, writeFile, copyFile, rm, symlink} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {writeCatalog} from './catalog-build.mjs';
import {CATALOG_PAGE_SIZE} from './routes.js';

const root=await mkdtemp(join(tmpdir(),'lpv-inventory-'));
const site=dirname(fileURLToPath(import.meta.url));
const put=async(path,bytes='fixture')=>{const target=join(root,path);await mkdir(dirname(target),{recursive:true});await writeFile(target,bytes);};
const json=(path,value)=>put(path,JSON.stringify(value)+'\n');
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const modelBytes={glb:'tiny GLB fixture',blend:'tiny Blend fixture',preview:'tiny preview fixture'};
const staticFiles=['index.html','models/index.html','about/index.html','zh-CN/index.html','zh-CN/models/index.html','zh-CN/about/index.html','404.html','sitemap.xml','robots.txt','THIRD_PARTY_NOTICES.md','LICENSE','LICENSES/CC-BY-4.0.txt','LICENSES/MIT.txt','home/editorial-hero.webp','brand/favicon.svg','gallery/resources.json'];
const run=()=>spawnSync(process.execPath,['site/audit-release.mjs'],{cwd:root,encoding:'utf8'});
const passes=()=>{const result=run();assert.equal(result.status,0,result.stdout+result.stderr);};
const refuses=pattern=>{const result=run();assert.notEqual(result.status,0,'The real audit must refuse this mutation');assert.match(result.stderr,pattern);};
try{
 await put('package.json','{"type":"module"}');
 await mkdir(join(root,'site'));
 // These production bytes are executed unchanged, including the full walk,
 // allowlist, exact model hashes, private-QA and Python ZIP member/hash guards.
 for(const path of ['audit-release.mjs','catalog-build.mjs','routes.js','curation.js','catalog-data.json','asset-delivery.mjs'])await copyFile(join(site,path),join(root,'site',path));
 // Source acquisition and unrelated gallery/registry/turntable contracts have
 // their own mandatory suites. This fixture supplies already checked inputs.
 await put('site/ci-publication.mjs',"import {readFileSync} from 'node:fs';export async function checkedPublication(){return JSON.parse(readFileSync('source.json'));}");
 await put('site/model-registry-cli.mjs','export function readRegistry(){return {};}');
 await put('site/model-registry-sync.mjs','export function syncRegistry(){}');
 await put('site/turntable-delivery.mjs','export async function collectTurntables(){return {files:[]};}');
 await put('site/gallery-assets.mjs','export async function auditGalleryAssets(){return {resources:{files:[]}};}');
 async function build(count){
  await rm(join(root,'dist'),{recursive:true,force:true});
  for(const path of staticFiles)await put('dist/'+path);
  for(const [key,bytes]of Object.entries(modelBytes))await put('dist/assets/test/shared.'+(key==='preview'?'png':key),bytes);
  const assets=Array.from({length:count},(_,i)=>({id:`fixture-${i}`,name:`Fixture ${i}`,category:'geology',collection:'earth',glb:'assets/test/shared.glb',blend:'assets/test/shared.blend',preview:'assets/test/shared.png',sha256:Object.fromEntries(Object.entries(modelBytes).map(([key,bytes])=>[key,hash(bytes)])),downloads:{bundle:'assets/downloads/shared.zip',credits:'assets/downloads/shared-CREDITS.txt'}}));
  const manifest={assets};await json('source.json',manifest);await json('dist/assets/manifest.json',manifest);
  await writeCatalog(manifest,join(root,'dist'));
  for(const asset of assets)for(const locale of ['','zh-CN/'])await put(`dist/${locale}models/${asset.id}/index.html`);
  for(let page=2;page<=Math.ceil(count/CATALOG_PAGE_SIZE);page++)for(const locale of ['','zh-CN/'])await put(`dist/${locale}models/page/${page}/index.html`);
  await put('dist/assets/downloads/shared-CREDITS.txt','fixture credits');
  const zip=spawnSync('python3',['-c',"import zipfile,pathlib\np=pathlib.Path('dist')\nwith zipfile.ZipFile(p/'assets/downloads/shared.zip','w') as z:\n for name in ['shared.glb','shared.blend']: z.writestr(name,(p/'assets/test'/name).read_bytes())\n z.writestr('CREDITS.txt',(p/'assets/downloads/shared-CREDITS.txt').read_bytes())"],{cwd:root,encoding:'utf8'});assert.equal(zip.status,0,zip.stderr);
  return manifest;
 }
 for(const count of [251,256,257,295,1000]){await build(count);passes();}
 const manifest=await build(295);passes();
 const shard='dist/assets/catalog/shards/00001.json',originalShard=await readFile(join(root,shard));
 await rm(join(root,shard));refuses(/Missing deployment file: assets\/catalog\/shards\/00001\.json/);await put(shard,originalShard);
 for(const extra of ['00002.json','99999.json','00001-copy.json','nested/00001.json']){
  const path='dist/assets/catalog/shards/'+extra;await put(path);refuses(/Unexpected deployment file: assets\/catalog\/shards\//);await rm(join(root,path));
 }
 // A forged deployed catalog index must not authorize an additional shard.
 const indexPath='dist/assets/catalog.json',originalIndex=await readFile(join(root,indexPath));
 const index=JSON.parse(originalIndex);index.shards.push({path:'assets/catalog/shards/00002.json',count:1});index.total++;
 await json(indexPath,index);await put('dist/assets/catalog/shards/00002.json');refuses(/Unexpected deployment file: assets\/catalog\/shards\/00002\.json/);
 await put(indexPath,originalIndex);await rm(join(root,'dist/assets/catalog/shards/00002.json'));
 const manifestPath='dist/assets/manifest.json';await json(manifestPath,{assets:[...manifest.assets,{...manifest.assets[0],id:'unapproved-extra'}]});refuses(/Delivered scope must equal the exact checked release/);await json(manifestPath,manifest);
 await json(manifestPath,{assets:manifest.assets.map((a,i)=>i?a:{...a,qa:'private.json'})});refuses(/Private QA bookkeeping/);await json(manifestPath,manifest);
 await put('dist/assets/test/shared.glb','changed');refuses(/Delivered bytes differ/);await put('dist/assets/test/shared.glb',modelBytes.glb);
 await rm(join(root,shard));await symlink(join(root,'dist/assets/catalog/shards/00000.json'),join(root,shard));refuses(/No symlinks may enter deployment/);await rm(join(root,shard));await put(shard,originalShard);
 const zipPath='dist/assets/downloads/shared.zip',originalZip=await readFile(join(root,zipPath));await put(zipPath,'not a ZIP');refuses(/BadZipFile/);await put(zipPath,originalZip);
 passes();
 console.log('Release inventory: real audit passes 251/256/257/295/1000; missing/extra/out-of-range shards, forged index/scope, private QA, changed bytes, symlink and invalid ZIP refused.');
}finally{await rm(root,{recursive:true,force:true});}

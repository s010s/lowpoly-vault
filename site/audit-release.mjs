/** Fail-closed inventory of every deployed file, including Vite's public directory. */
import { readFile, readdir, lstat } from 'node:fs/promises';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { collectTurntables } from './turntable-delivery.mjs';
import { checkedPublication } from './ci-publication.mjs';
import { CATALOG_PAGE_SIZE } from './routes.js';
import { assetFileAllowlist } from './asset-delivery.mjs';
import { auditGalleryAssets } from './gallery-assets.mjs';
const root=resolve('dist');
const manifest=JSON.parse(await readFile(resolve(root,'assets/manifest.json'),'utf8'));
assert(!manifest.review_only);
const source=await checkedPublication();
assert.deepEqual(manifest.assets.map(a=>a.id),source.assets.map(a=>a.id),'Delivered scope must equal the exact checked release');
const expected=new Set(['index.html','models/index.html','about/index.html','zh-CN/index.html','zh-CN/models/index.html','zh-CN/about/index.html','404.html','sitemap.xml','robots.txt','THIRD_PARTY_NOTICES.md','LICENSE','LICENSES/CC-BY-4.0.txt','LICENSES/MIT.txt','home/editorial-hero.webp','brand/favicon.svg','assets/manifest.json','assets/catalog.json','assets/catalog/shards/00000.json',...assetFileAllowlist(manifest)]);
for(let page=2;page<=Math.ceil(manifest.assets.length/CATALOG_PAGE_SIZE);page++) for(const locale of ['','zh-CN/'])expected.add(`${locale}models/page/${page}/index.html`);
const turntables=await collectTurntables(manifest);
for(const file of turntables.files) {
  expected.add(file);
  assert.equal(createHash('sha256').update(await readFile(resolve(root,file))).digest('hex'),
    createHash('sha256').update(await readFile(resolve(file))).digest('hex'),`Delivered image or sequence metadata differs: ${file}`);
}
for(const asset of manifest.assets) {
  for(const path of [`models/${asset.id}/index.html`,`zh-CN/models/${asset.id}/index.html`,`assets/catalog/details/${asset.id}.json`,asset.downloads.bundle,asset.downloads.credits]) expected.add(path);
  assert.equal(asset.qa,undefined,'Private QA bookkeeping must not enter public metadata');
  for(const key of ['glb','blend','preview']) {
    assert.equal(createHash('sha256').update(await readFile(resolve(root,asset[key]))).digest('hex'),asset.sha256[key],`Delivered bytes differ: ${asset[key]}`);
  }
}
async function walk(directory='') {
  const result=[];
  for(const name of await readdir(resolve(root,directory))) {
    const path=directory?`${directory}/${name}`:name,info=await lstat(resolve(root,path));
    assert(!info.isSymbolicLink(),'No symlinks may enter deployment');
    if(info.isDirectory())result.push(...await walk(path));else result.push(path);
  }
  return result;
}
const gallery=await auditGalleryAssets(source,{outputRoot:root,requireComplete:process.env.REQUIRE_COMPLETE_GALLERY==='1'});
expected.add('gallery/resources.json');for(const file of gallery.resources.files)expected.add(file.path);
const files=await walk();
for(const file of files) assert(expected.has(file)||/^assets\/(?:index|viewer|presentation|main|preload-helper|catalog-source|routes|bootstrap)-[A-Za-z0-9_-]+\.(?:js|css)$/.test(file),`Unexpected deployment file: ${file}`);
for(const file of expected)assert(files.includes(file),`Missing deployment file: ${file}`);
const jobs=manifest.assets.map(a=>({path:resolve(root,a.downloads.bundle),files:Object.fromEntries(['glb','blend'].map(k=>[a[k].split('/').at(-1),a.sha256[k]])),credits:resolve(root,a.downloads.credits)}));
const script=`import json,sys,zipfile,hashlib\nfor job in json.load(sys.stdin):\n with zipfile.ZipFile(job['path']) as z:\n  assert sorted(z.namelist())==sorted([*job['files'],'CREDITS.txt'])\n  for name,digest in job['files'].items(): assert hashlib.sha256(z.read(name)).hexdigest()==digest\n  assert z.read('CREDITS.txt')==open(job['credits'],'rb').read()\n`;
const result=spawnSync('python3',['-c',script],{input:JSON.stringify(jobs),encoding:'utf8'});
assert.equal(result.status,0,result.stderr);
console.log(`Release inventory passed: ${files.length} allowlisted files; ${manifest.assets.length} byte-identical GLB/Blend pairs and ZIPs; no QA, research or experiments.`);

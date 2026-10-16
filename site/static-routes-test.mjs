import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,readFile,readdir,stat,rm,symlink} from 'node:fs/promises';
import {join,dirname} from 'node:path';
import {tmpdir} from 'node:os';
import {spawnSync} from 'node:child_process';
import {assetFileAllowlist,deliverManifestAssets,clearDeliveredAssets} from './asset-delivery.mjs';
import {writeCatalog} from './catalog-build.mjs';
import {writeStaticRoutes} from './static-routes.mjs';
const root=await mkdtemp(join(tmpdir(),'vault-delivery-'));
const out=join(root,'out');
const template='<!doctype html><html lang="en"><head><title>Template</title><meta name="description" content="Template"></head><body><section id="home-page">Home shell</section><main id="catalog-page" hidden></main><script type="module" src="/lowpoly-vault/assets/app.js"></script></body></html>';
try {
 const assets=[];
 for(let i=0;i<25;i++){
  const path=`assets/legacy/plants/asset-${i}`;await mkdir(join(root,path),{recursive:true});
  for(const [name,bytes]of [[`asset-${i}.glb`,Buffer.alloc(73+i)],[`asset-${i}.blend`,Buffer.alloc(119+i)],['preview.png',Buffer.alloc(33)]])await writeFile(join(root,path,name),bytes);
  await writeFile(join(root,path,'qa.json'),'{"secret":"Must not be copied"}');
  await writeFile(join(root,path,'reference.png'),'Not approved');
  assets.push({id:`asset-${i}`,name:{en:`Model ${i}`,zh:`模型 ${i}`},description:{en:`Original model ${i}`,zh:`原创模型 ${i}`},category:'plants',collection:'legacy',worlds:['world-a','world-b'],packs:['pack-a','pack-b'],triangles:100+i,glb:`${path}/asset-${i}.glb`,blend:`${path}/asset-${i}.blend`,preview:`${path}/preview.png`,material_count:999});
 }
 await mkdir(join(root,'assets/unapproved'),{recursive:true});await writeFile(join(root,'assets/unapproved/secret.glb'),'Unapproved');
 await mkdir(join(out,'assets'),{recursive:true});await writeFile(join(out,'assets/app.js'),'compiled');await writeFile(join(out,'assets/stale.glb'),'old');await mkdir(join(out,'assets/old'),{recursive:true});await writeFile(join(out,'assets/old/raw.blend'),'old');
 await clearDeliveredAssets(out);assert.deepEqual(await readdir(join(out,'assets')),['app.js']);
 const source={version:1,author:'Test author',license:'CC-BY-4.0',assets};const before=JSON.stringify(source);
 const manifest=await deliverManifestAssets(source,out,{root});
 assert.equal(JSON.stringify(source),before,'Delivery must not mutate the manifest or approval state');
 assert.equal(manifest.assets[0].file_sizes.glb,73);assert.equal(manifest.assets[0].file_sizes.blend,119);assert.equal(manifest.assets[0].material_count,undefined,'Do not claim unverified material counts');
 assert(manifest.assets[0].file_sizes.bundle>0);assert.equal(assetFileAllowlist(manifest).length,75);
 for(const path of ['assets/unapproved/secret.glb','assets/legacy/plants/asset-0/qa.json','assets/legacy/plants/asset-0/reference.png'])await assert.rejects(()=>stat(join(out,path)),/ENOENT/);
 const inspect=spawnSync('python3',['-c',"import zipfile,sys,json;z=zipfile.ZipFile(sys.argv[1]);print(json.dumps(z.namelist()));print(z.read('CREDITS.txt').decode())",join(out,manifest.assets[0].downloads.bundle)],{encoding:'utf8'});
 assert.equal(inspect.status,0);assert.deepEqual(JSON.parse(inspect.stdout.split('\n')[0]),['asset-0.glb','asset-0.blend','CREDITS.txt']);assert(inspect.stdout.includes('https://creativecommons.org/licenses/by/4.0/'));
 await assert.rejects(()=>deliverManifestAssets({...source,review_only:true},out,{root}),/review-only/);
 await writeCatalog(manifest,out);
 for(const base of ['/lowpoly-vault/','/','/custom/deep/']){
  await writeFile(join(out,'index.html'),template);
  const result=await writeStaticRoutes(manifest,out,{base,origin:'https://example.test'});assert.equal(result.pages,58);
  for(const locale of ['','zh-CN/']){
   const html=await readFile(join(out,locale,'models/asset-0/index.html'),'utf8');
   assert(html.includes('<article id="static-route-content"'));assert(html.includes('<section id="home-page" hidden>'));assert(html.includes(locale?'模型 0':'Model 0'));
   assert(html.includes(`rel="canonical" href="https://example.test${base}${locale}models/asset-0/"`));assert(html.includes('hreflang="zh-CN"'));assert(html.includes('class="static-locale"'));assert(html.includes(locale?'English':'简体中文'));assert(html.includes('application/ld+json'));assert(html.includes(`href="${base}assets/downloads/asset-0.zip"`));
   assert.equal((html.match(/<title>/g)||[]).length,1);assert.equal((html.match(/name="description"/g)||[]).length,1);
   const page=await readFile(join(out,locale,'models/page/2/index.html'),'utf8');assert(page.includes(`href="${base}${locale}models/asset-24/"`));assert(page.includes(`rel="prev" href="${base}${locale}models/"`));
  }
  const missing=await readFile(join(out,'404.html'),'utf8');assert(missing.includes('We couldn’t find that page.'));assert(!missing.includes('type="module"'));
  const sitemap=await readFile(join(out,'sitemap.xml'),'utf8');assert(sitemap.includes(`https://example.test${base}zh-CN/models/asset-24/`));
 }
 await symlink('/etc/hosts',join(root,'assets/escape.glb'));
 await assert.rejects(()=>deliverManifestAssets({...source,assets:[{...assets[0],glb:'assets/escape.glb'}]},out,{root}),/symlink escapes/);
 for(const glb of ['assets/../outside.glb','assets/qa/secret.glb','assets/experiments/raw.glb'])assert.throws(()=>assetFileAllowlist({assets:[{...assets[0],glb}]}),/Unsafe|Non-release/);
 console.log('Static route and release tests passed: bilingual real documents, pagination, metadata, custom/project/root deployment, exact sizes, ZIP credits, approved allowlist, no QA/reference files, symlink/traversal refusal.');
}finally{await rm(root,{recursive:true,force:true});}

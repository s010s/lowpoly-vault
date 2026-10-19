/** Identity is shared by enhanced routes, native documents and every base path. */
import assert from 'node:assert/strict';
import {readFile,mkdtemp,writeFile,rm} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {writeStaticRoutes} from './static-routes.mjs';
const read=path=>readFile(new URL(path,import.meta.url),'utf8');
const [template,shell,shared,home,gallery,favicon]=await Promise.all(['./index.html','./gallery/shell.html','./brand.css','./style.css','./gallery/style.css','./public/brand/favicon.svg'].map(read));
const mark=source=>source.match(/<svg class="vault-mark"[\s\S]*?<\/svg>/)?.[0];
assert(mark(template));assert.equal(mark(template),mark(shell),'One exact existing cube across both applications');
assert.match(mark(template),/width="32" height="32"/);assert.match(mark(template),/fill="none" stroke="currentColor"/);
for(const source of [template,shell])assert.match(source,/class="vault-wordmark">LOWPOLY <span>VAULT<\/span>/);
assert(!/[◭⌕☷×]/.test(shell),'Brand and utility icons do not depend on platform glyphs');
for(const svg of shell.match(/<svg\b[^>]+>/g)||[])assert(/width="\d+" height="\d+"/.test(svg),'Shell icons have intrinsic bounds');
for(const path of [...mark(template).matchAll(/<path d="([^"]+)"/g)].map(match=>match[1]))assert(favicon.includes(`d="${path}"`),'Favicon uses the exact header cube geometry');
assert.match(favicon,/viewBox="0 0 32 32"/);assert.match(favicon,/fill="#305742"/);
assert(!/@font-face|https?:\/\/.*fonts/.test(shared),'No network-dependent typography');
for(const source of [home,gallery])for(const variable of ['--vault-font-ui','--vault-font-display','--vault-accent','--vault-line'])assert(source.includes(variable),variable+' is shared');
const asset={id:'test-model',name:{en:'Test model',zh:'测试模型'},description:{en:'Test',zh:'测试'},category:'plants',worlds:['prehistoric'],preview:'assets/test.png',glb:'assets/test.glb',blend:'assets/test.blend',triangles:120,downloads:{glb:'assets/test.glb',blend:'assets/test.blend'}};
const root=await mkdtemp(join(tmpdir(),'vault-brand-'));
try{
 for(const base of ['/','/lowpoly-vault/','/custom/deep/']){
  await writeFile(join(root,'index.html'),template.replaceAll('%BASE_URL%',base));
  await writeStaticRoutes({assets:[asset]},root,{base,origin:'https://example.test'});
  for(const locale of ['','zh-CN/'])for(const route of ['', 'models/', 'models/test-model/', 'about/']){
   const html=await readFile(join(root,locale,route,'index.html'),'utf8');
   assert(html.includes(`href="${base}brand/favicon.svg"`));
   assert(html.includes(`href="${base}${locale}" data-route="home"`));
   assert(html.includes(`href="${base}${locale}models/" data-route="catalog"`));
   assert.equal(mark(html),mark(template));
   assert.match(html,/var\(--vault-font-display,Georgia,serif\)/);
  }
  const missing=await readFile(join(root,'404.html'),'utf8');
  assert.equal(mark(missing),mark(template));assert(missing.includes(`href="${base}brand/favicon.svg"`));assert(missing.includes(`href="${base}" data-route="home"`));
 }
}finally{await rm(root,{recursive:true,force:true});}
console.log('Brand contracts passed: identical bounded SVG lockup/favicon, shared local font and color tokens, semantic utility icons, bilingual home/list/detail/about/404 and root/project/nested base paths.');

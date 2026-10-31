/** Startup contract: useful homepage geometry must not await the app CSS/JS. */
import assert from 'node:assert/strict';
import {readFile,mkdtemp,mkdir,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import postcss from 'postcss';
import {homepageCriticalCSS,homepageStartupStyle,isHomepageSelector} from './home-startup.mjs';
import {writeStaticRoutes} from './static-routes.mjs';

const source=await readFile(new URL('./style.css',import.meta.url),'utf8');
const css=homepageCriticalCSS(source),tree=postcss.parse(css);
const rules=[];tree.walkRules(rule=>rules.push(rule));
const has=(selector,property,value)=>rules.some(rule=>rule.selectors.includes(selector)&&rule.nodes.some(node=>node.prop===property&&node.value===value));
assert(has('.hero-art','position','absolute'),'The hero cannot use its 1600×1000 natural flow size before app CSS');
assert(has('.hero-art','width','100%'));assert(has('.hero-art','height','100%'));
assert(has('.theme-toggle .moon','display','none'));assert(has('[data-theme=light] .theme-toggle .sun','display','none'));assert(has('[data-theme=light] .theme-toggle .moon','display','block'));
assert(has('.home-hero','position','relative'));assert(has('.home-hero','min-height','560px'));
assert(has('.skip','position','fixed'));assert(has('.skip','top','-80px'));assert(has('.skip:focus','top','12px'));
assert(has('body','margin','0'));assert(has('html .home-copy h1','font-family','var(--vault-font-display)'));
assert(has('html .home-copy h1','font-weight','400'));assert(has('.theme-toggle','width','42px'));
assert(css.includes('@media(min-width:1500px)')&&css.includes('min-height:650px'));
assert(css.includes('@media(max-width:700px)')&&css.includes('min-height:690px'));
assert(css.includes('prefers-reduced-motion:reduce'));assert(css.includes('[data-theme=light]')&&css.includes('[data-theme=dark]'));
for(const selector of ['.asset-card','#grid','#viewer-dialog','.slot-image'])assert(!css.includes(selector),'No unused gallery/3D/modal rules in homepage startup CSS: '+selector);
assert(!css.includes('url(')&&!css.includes('@font-face')&&!css.includes('@import'),'No new asset/font requests');
assert(Buffer.byteLength(css)<18000,'Keep the first-paint budget bounded');
assert.equal(isHomepageSelector('html .home-copy h1'),true);assert.equal(isHomepageSelector('#viewer-dialog .home-copy'),false);
assert.equal(isHomepageSelector('.asset-card button'),false);
const synthetic=homepageCriticalCSS('@media(max-width:700px){.home-hero,.asset-card{height:4px}}@supports(display:grid){.home-page{display:grid}.slot{height:9px}}@keyframes obsolete{to{opacity:1}}');
assert(synthetic.includes('@supports')&&synthetic.includes('.home-page')&&synthetic.includes('.home-hero'));
assert(!synthetic.includes('.asset-card')&&!synthetic.includes('.slot')&&!synthetic.includes('@keyframes'));
const style=await homepageStartupStyle();assert.equal(style,`<style id="home-startup-style">${css}</style>`);
const root=await mkdtemp(join(tmpdir(),'home-first-paint-'));
try{
 const html=await readFile(new URL('./index.html',import.meta.url),'utf8');await writeFile(join(root,'index.html'),html);
 const a={id:'test-shape',name:{en:'Test shape',zh:'测试形态'},description:{en:'Test',zh:'测试'},category:'geology',collection:'prehistoric',dimensions:[1,1,1],triangles:100,preview:'assets/test/preview.png',glb:'assets/test/model.glb',blend:'assets/test/source.blend'};
 await writeStaticRoutes({assets:[a]},root,{base:'/lowpoly-vault/'});
 for(const locale of ['', 'zh-CN/']){
  const home=await readFile(join(root,locale,'index.html'),'utf8');assert.equal((home.match(/id="home-startup-style"/g)||[]).length,1);
  assert(home.indexOf('id="home-startup-style"')<home.indexOf('</head>'));assert(home.includes('class="hero-art"')&&home.includes('width="1600" height="1000"'));
  assert(home.includes('<noscript><style>')&&home.includes('id="static-route-content"'),'Meaningful native/no-JS content stays in the document');
  for(const suffix of ['models/index.html','about/index.html','models/test-shape/index.html']){
   const other=await readFile(join(root,locale,suffix),'utf8');assert(!other.includes('id="home-startup-style"'),'Home rules must not alter other route budgets: '+locale+suffix);
  }
 }
}finally{await rm(root,{recursive:true,force:true});}
console.log('PASS homepage first paint: intrinsic-image regression guarded, typography/skip/focus/theme/responsive/reduced-motion preserved, no asset preloads, bounded build-only CSS, bilingual head injection and isolated non-home routes');

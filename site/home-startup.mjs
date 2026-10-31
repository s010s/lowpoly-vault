/** First-paint rules derived from the same stylesheet as the enhanced homepage.
 * Keep source order, responsive/theme conditions and existing motion preferences.
 * This is build-time only; the browser receives no parser or second JS startup. */
import {readFile} from 'node:fs/promises';
import postcss from 'postcss';

const shellClasses=new Set(['topbar','top-actions','primary-nav','brand','brand-light','skip','sr-only','edition','text-link','inline-icon','theme-toggle','nav-active','sun','moon']);
const homeIds=new Set(['home-page','home-title','home-search','home-query','theme-toggle','language']);
export function isHomepageSelector(selector){
 const classes=[...selector.matchAll(/\.([a-zA-Z_][\w-]*)/g)].map(match=>match[1]);
 const ids=[...selector.matchAll(/#([a-zA-Z_][\w-]*)/g)].map(match=>match[1]);
 if(classes.some(name=>!shellClasses.has(name)&&!/^(home-|hero-|curation-|vault-)/.test(name))||ids.some(id=>!homeIds.has(id)))return false;
 return !!(classes.length||ids.length)||/^(?::root\b|html\b|body\b|\*|\[hidden\]|\[data-theme(?:=|\])|(?:button|a|input|select|h1|main)(?=[\s:.#[>+~]|$))/.test(selector);
}
export function homepageCriticalCSS(source){
 const root=postcss.parse(source);
 const prune=node=>{
  for(const child of [...(node.nodes||[])]){
   if(child.type==='rule'){
    const selectors=child.selectors.filter(isHomepageSelector);
    if(selectors.length)child.selector=selectors.join(',');else child.remove();
   }else if(child.type==='atrule'&&['media','supports'].includes(child.name)){
    prune(child);if(!child.nodes?.length)child.remove();
   }else child.remove();
  }
 };
 prune(root);return root.toString();
}
export async function homepageStartupStyle(){
 const css=homepageCriticalCSS(await readFile(new URL('./style.css',import.meta.url),'utf8'));
 return `<style id="home-startup-style">${css.replace(/<\/style/gi,'<\\/style')}</style>`;
}

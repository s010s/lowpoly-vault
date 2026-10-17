import assert from 'node:assert/strict';
import {initTheme} from './theme.js';
globalThis.MutationObserver=class{observe(){}};
function fixture({dark=false,reduced=false,failStorage=false,saved=null,vt=false}={}){
 const events={},animations=[],data={},attrs={};let savedValue=saved;
 const button={setAttribute:(k,v)=>attrs[k]=v,getAttribute:k=>attrs[k],addEventListener:(k,f)=>events.click=f,getBoundingClientRect:()=>({left:950,top:20,width:40,height:40})};
 const root={lang:'en',dataset:data,style:{},animate:(frames,opts)=>{animations.push({frames,opts});return {finished:Promise.resolve(),cancel(){}};}};
 const sys={matches:dark,addEventListener:(k,f)=>events.system=f},reduce={matches:reduced};
 const doc={documentElement:root,querySelectorAll:()=>[button],querySelector:()=>null};
 if(vt)doc.startViewTransition=f=>{f();return{ready:Promise.resolve(),finished:Promise.resolve(),skipTransition(){}}};
 const c=initTheme({doc,media:q=>q.includes('color-scheme')?sys:reduce,storage:()=>{if(failStorage)throw Error('blocked');return{getItem:()=>savedValue,setItem:(k,v)=>{savedValue=v}}},viewport:()=>({width:1000,height:800})});
 return{c,events,animations,sys,data,get saved(){return savedValue}};
}
const settle=()=>new Promise(r=>setTimeout(r,5));
for(const dark of [false,true]){const f=fixture({dark});assert.equal(f.c.theme,dark?'dark':'light');f.sys.matches=!dark;f.events.system();await settle();assert.equal(f.c.theme,dark?'light':'dark');}
const saved=fixture({saved:'dark'});assert.equal(saved.c.theme,'dark');saved.events.click();await settle();assert.equal(saved.saved,'light');saved.sys.matches=true;saved.events.system();await settle();assert.equal(saved.c.theme,'light');
const failed=fixture({failStorage:true});failed.events.click();await settle();assert.equal(failed.c.theme,'dark');
const rapid=fixture({vt:true});for(let i=0;i<7;i++)rapid.events.click();await settle();assert.equal(rapid.c.theme,'dark');assert.equal(rapid.saved,'dark');const clip=rapid.animations.find(a=>a.frames[1].clipPath);assert(clip);assert(clip.frames[1].clipPath.includes(String(Math.hypot(970,760))));
const reduced=fixture({reduced:true,vt:true});reduced.events.click();await settle();assert(reduced.animations.every(a=>!a.frames[1].clipPath));assert.equal(reduced.animations[0].opts.duration,120);
const fallback=fixture();fallback.events.click();await settle();assert.equal(fallback.animations[0].opts.duration,160);
console.log('Theme tests passed: OS initial/change, explicit preference, persistence failure, seven rapid clicks, farthest-corner radius, reduced motion, no-ViewTransition fallback.');

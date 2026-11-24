// Exercises the actual selectPoster body with controlled image/animation timing.
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFile} from 'node:fs/promises';
const source=await readFile(new URL('../main.js',import.meta.url),'utf8');
const start=source.indexOf('function selectPoster(asset,version,source){');
const body=source.slice(start,source.indexOf('async function choose(',start));
function fixture(){
 let serial=0;const frames=new Map();const nodes=new Map();
 const image=()=>({dataset:{},complete:false,naturalWidth:0,currentSrc:'',src:'',onload:null,onerror:null,decoding:'',style:{removeProperty(key){delete this[key];}},classList:{toggle(){}},removeAttribute(key){delete this[key];if(key==='src')this.cancelled=true;},replaceWith(next){nodes.set('#detail-poster',next);},decode:()=>Promise.resolve()});
 const cache=new Map();let bridge={cancelled:false},clears=0;
 const stagePoster={clear(){clears++;if(bridge)bridge.cancelled=true;bridge=null;},prepare(){this.clear();return null;},reveal:()=>Promise.resolve()};
 const context={URL,Promise,queueMicrotask,document:{createElement:image},location:{href:'https://example.test/'},mobile:()=>false,
  detailPosterCache:cache,stagePoster,stage:{dataset:{},prepend(img){nodes.set('#detail-poster',img);}},state:{selected:'bird',lang:'en'},selectionVersion:1,currentReady:false,cancelSelectedPoster:null,
  $:sel=>nodes.get(sel),poster:a=>a.galleryPosters.detail,cacheDetailPoster:(id,entry)=>cache.set(id,entry),updateSelectedPosterFrame(){},t:x=>x,
  requestAnimationFrame:fn=>{frames.set(++serial,fn);return serial;},cancelAnimationFrame:id=>frames.delete(id)};
 vm.createContext(context);vm.runInContext(body,context);
 const asset={id:'bird',name:{en:'Bird'},sha256:{glb:'a'.repeat(64)},galleryPosters:{detail:'gallery/bird.png'}};
 const readyImage=()=>{const i=image();Object.assign(i,{complete:true,naturalWidth:512,currentSrc:'https://example.test/gallery/bird.png',src:'gallery/bird.png'});Object.assign(i.dataset,{modelId:'bird',glbSha:asset.sha256.glb,source:'canonical',state:'ready'});return i;};
 const tick=()=>{const pending=[...frames.values()];frames.clear();pending.forEach(fn=>fn());};
 return {context,cache,nodes,asset,image,readyImage,tick,choose:()=>context.selectPoster(asset,context.selectionVersion,null),get clears(){return clears;},get bridge(){return bridge;}};
}
{
 const f=fixture(),previous=f.readyImage(),oldBridge=f.bridge;f.nodes.set('#detail-poster',previous);
 const first=f.choose();assert.equal(first.image,previous);assert.equal(oldBridge.cancelled,true);assert.equal(f.bridge,null);assert.equal(previous.style.visibility,'visible');
 f.context.selectionVersion++;const second=f.choose();assert.equal(await first.ready,false);f.tick();f.tick();assert.equal(await second.ready,true);assert.equal(second.image,previous);
}
for(const kind of ['pending','sha-mismatch','url-mismatch']){
 const f=fixture(),cached=f.readyImage();cached.onload=()=>{};cached.onerror=()=>{};
 if(kind==='sha-mismatch')cached.dataset.glbSha='b'.repeat(64);if(kind==='url-mismatch')cached.currentSrc='https://example.test/old.png';
 f.cache.set('bird',{image:cached,ready:kind!=='pending'});const result=f.choose();
 assert.notEqual(result.image,cached,kind);assert.equal(cached.onload,null);assert.equal(cached.onerror,null);assert.equal(cached.cancelled,true);assert.equal(f.cache.has('bird'),false);
 f.context.cancelSelectedPoster();assert.equal(await result.ready,false);
}
{
 const f=fixture(),cached=f.readyImage();f.cache.set('bird',{image:cached,ready:true});const result=f.choose();
 assert.equal(result.image,cached);assert.notEqual(cached.cancelled,true);f.tick();f.tick();assert.equal(await result.ready,true);
}
{
 const f=fixture(),previous=f.readyImage(),extra=f.readyImage();extra.onload=()=>{};f.nodes.set('#detail-poster',previous);f.cache.set('bird',{image:extra,ready:true});
 const result=f.choose();assert.equal(result.image,previous);assert.equal(extra.onload,null);assert.equal(extra.cancelled,true);f.tick();f.tick();assert.equal(await result.ready,true);
}
console.log('PASS actual selectPoster: same-model rapid reselect clears bridge; pending/stale/duplicate cache canceled; exact decoded cache reused. No browser visual claim.');

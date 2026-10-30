import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFile} from 'node:fs/promises';
import {heldNativeThumbnail} from './gallery-thumbnail-reveal-browser-test.mjs';

// Run the exact serialized browser predicate. The DOM-first lazy row may never
// enter decode, while offscreen eager rows may decode before the visible one.
const rect=(left,top,right,bottom)=>({left,top,right,bottom});
const clip=rect(0,150,370,760);
const heldImage=(box,{slot=true,state='decoding'}={})=>({dataset:{thumbnailState:state},matches:selector=>slot&&selector==='.slot-image img',getBoundingClientRect:()=>box,closest:selector=>{assert.equal(selector,'#wheel');return{getBoundingClientRect:()=>clip};}});
const lazyFirst=heldImage(rect(50,-120,250,-20),{state:'pending'}),offscreen=heldImage(rect(50,40,250,140)),center=heldImage(rect(50,400,250,500)),lower=heldImage(rect(50,580,250,680)),detail=heldImage(rect(400,200,800,600),{slot:false});
const nativeDecodes=[],predicateContext=vm.createContext({window:{nativeDecodes},innerWidth:1280,innerHeight:844,document:{querySelector(){throw Error('Never select the DOM-first lazy image');}}});
const selectHeld=vm.runInContext('('+heldNativeThumbnail.toString()+')',predicateContext);
nativeDecodes.push({image:detail},{image:offscreen},{image:center});
assert.equal(selectHeld(),null,'Require three held wheel images, not unrelated detail images');
nativeDecodes.push({image:lower});
const captured=selectHeld();assert.equal(captured,center);assert.notEqual(captured,lazyFirst);
nativeDecodes.reverse();assert.equal(selectHeld(),lower,'The decode list can arrive in any order');
center.dataset.thumbnailState='ready';assert.equal(captured,center,'The retained handle still refers to the same completed image');
assert.equal(captured.dataset.thumbnailState,'ready');
nativeDecodes.splice(0,nativeDecodes.length,...[rect(50,40,250,140),rect(50,770,250,820),rect(380,400,500,500)].map(box=>({image:heldImage(box)})));
assert.equal(selectHeld(),null,'Do not choose images clipped outside the wheel even when inside the viewport');
predicateContext.innerHeight=100;nativeDecodes.push({image:center});
assert.equal(selectHeld(),null,'A held image must also intersect the viewport');
predicateContext.innerHeight=844;assert.equal(selectHeld(),center,'Do not filter on readiness and hide a premature-ready regression');
console.log('Native browser fixture identity passed: real held-decode predicate, three wheel images, arbitrary arrival order, wheel/viewport clipping and retained image identity.');

const main=await readFile(new URL('./gallery/main.js',import.meta.url),'utf8');
const inertMain=main.replace(/^import .*;$/gm,'').replace(/^if\(import\.meta\.hot\).*$/gm,'').replace('export async function mountGallery(){','async function mountGallery(){');
const trap=new Proxy({}, {get(){throw Error('Import must not inspect or mutate the DOM');}});
const imported=vm.createContext({document:trap,window:trap});
vm.runInContext(inertMain,imported);
assert.equal(vm.runInContext('typeof mountGallery',imported),'function');
const icons=await readFile(new URL('./gallery/icons.js',import.meta.url),'utf8');
vm.runInContext(icons.replace(/^export /gm,''),vm.createContext({document:trap}));

const bootstrap=(await readFile(new URL('./gallery/bootstrap.js',import.meta.url),'utf8')).replace(/^import .*;$/gm,'').replace("import('./main.js')",'importApp()');
const deferred=()=>{let resolve,reject;const promise=new Promise((yes,no)=>{resolve=yes;reject=no;});return {promise,resolve,reject};};
const tick=async()=>{for(let i=0;i<8;i++)await Promise.resolve();};
function fixture(){
 const app=deferred(),catalog=deferred(),firstFrame=deferred(),original=[{id:'legacy'},{id:'static-route-content'}],events=[];
 const classes=new Set(),body={childNodes:[...original],dataset:{staticRoute:'models'},classList:{add:v=>classes.add(v),remove:v=>classes.delete(v)},replaceChildren(...nodes){this.childNodes=nodes;events.push(nodes[0]?.id==='legacy'?'restore':'swap');}};
 const article={removeAttribute(){},append(node){events.push('status');this.status=node.textContent;}};
 const document={body,documentElement:{dataset:{theme:'dark'},lang:'zh-CN'},head:{append(){}},querySelector:()=>article,createElement:tag=>({content:{cloneNode:()=>({id:'gallery-shell'})},remove(){},setAttribute(){},textContent:''})};
 const context=vm.createContext({document,shell:'<main>approved shell</main>',loadGalleryCatalog:()=>catalog.promise,importApp:()=>app.promise,console:{error(){events.push('expected-error');}}});
 const run=vm.runInContext('(async()=>{'+bootstrap+'})()',context);
 const mountGallery=()=>{events.push('mount');assert.equal(body.dataset.gallery,'approved-v55');assert(!classes.has('gallery-loading'),'Mount measures visible geometry');return firstFrame.promise;};
 return {app,catalog,firstFrame,original,body,events,document,article,run,mountGallery};
}
for(const first of ['app','catalog']){
 const f=fixture();await tick();assert.deepEqual(f.events,[]);assert.deepEqual(f.body.childNodes,f.original);
 f[first].resolve(first==='app'?{mountGallery:f.mountGallery}:{});await tick();assert.deepEqual(f.events,[],'One ready dependency cannot remove useful SSG');
 f[first==='app'?'catalog':'app'].resolve(first==='app'?{}:{mountGallery:f.mountGallery});await tick();
 assert.deepEqual(f.events,['swap','mount'],'All prerequisites are ready before synchronous body swap/mount');
 assert.equal(f.document.documentElement.dataset.theme,'light');
 f.firstFrame.resolve();await f.run;
}
for(const failure of ['app','catalog','mount']){
 const f=fixture();
 if(failure==='app')f.app.reject(Error('stylesheet or module failed'));
 else f.app.resolve({mountGallery:failure==='mount'?()=>{throw Error('mount failed');}:f.mountGallery});
 if(failure==='catalog')f.catalog.reject(Error('catalog failed'));else f.catalog.resolve();
 await f.run;assert.deepEqual(f.body.childNodes,f.original);assert.equal(f.body.dataset.gallery,undefined);assert.equal(f.document.documentElement.dataset.theme,'dark');assert(f.article.status.includes('仍可打开模型详情'));
}
console.log('Gallery startup passed: imports are DOM-inert; code/CSS and catalog gate the swap; mount has visible geometry; all rejected prerequisites restore linked SSG and theme.');

// The tiny parser-time initializer is independent of app imports and catalog
// fetches. Verify query selection and real fallback navigation without a browser.
const initializer=await readFile(new URL('./gallery/startup.js',import.meta.url),'utf8');
function nativeFixture({query='',mobile=false,reduced=false,ids=['first','cooperoceras','last'],selected='cooperoceras',thumbnail={}}={}){
 const nodes=Object.fromEntries(['title','subtitle','triangles','dimensions','file-size','download','blend','info','detail-poster','mobile-back'].map(id=>[id,{hidden:id==='mobile-back',style:{}}]));
 const rows=ids.map(id=>({dataset:{id,selected:String(id===selected),title:id,subtitle:'Plants / Stylized specimen',poster:`/gallery/posters/${id}.png`,triangles:'100',dimensions:'1 m',fileSize:'10 KB',download:`/assets/${id}.glb`,blend:`/assets/${id}.blend`,info:`/models/${id}/`},image:{style:{}},thumbnail:{dataset:{},hasAttribute:()=>true,addEventListener(type,handler){this[type]=handler;},removeEventListener(type,handler){if(this[type]===handler)delete this[type];},getAnimations:()=>[],...thumbnail},getAttribute:()=>id,setAttribute(key,value){this[key]=value;},querySelector(selector){return selector==='.slot-image img'?this.thumbnail:this.image;}}));
 const wheel={scrollTop:0,addEventListener(type,handler){this[type]=handler;}},root={dataset:{},classList:{contains:()=>true},querySelectorAll:()=>rows,querySelector:selector=>selector==='#wheel'?wheel:nodes[selector.slice(1)]};
 const timers=new Map();let timerID=0;
 const classes=new Set(),document={addEventListener(){},getElementById:()=>root,body:{classList:{toggle(key,on){if(on)classes.add(key);else classes.delete(key);}}}};
 vm.runInContext(initializer,vm.createContext({IntersectionObserver:class{observe(){}disconnect(){}},document,location:{href:'https://example.test/lowpoly-vault/models/'+query},URL,matchMedia:media=>({matches:media.includes('max-width')?mobile:reduced}),setTimeout:(fn,delay)=>{timers.set(++timerID,{fn,delay});return timerID;},clearTimeout:id=>timers.delete(id),cancelAnimationFrame:()=>{},requestAnimationFrame:fn=>{fn();return 1;}}));
 return {nodes,rows,wheel,root,classes,timers};
}
for(const mobile of [false,true]){
 const selected=nativeFixture({mobile,query:'?model=last&q=fern&category=plants'});
 assert.equal(selected.nodes.title.textContent,'last');assert.equal(selected.nodes['detail-poster'].src,'/gallery/posters/last.png');
 assert.equal(selected.nodes.download.href,'/assets/last.glb');assert.equal(selected.nodes.info.href,'/models/last/');
 assert.equal(selected.nodes['mobile-back'].href,'/lowpoly-vault/models/?q=fern&category=plants');assert.equal(selected.nodes['mobile-back'].hidden,!mobile);
 assert.equal(selected.classes.has('mobile-detail'),mobile);assert.equal(selected.wheel.scrollTop,mobile?0:256);
 assert.equal(selected.rows.filter(row=>row.dataset.selected==='true').length,1);
 const collection=nativeFixture({mobile});assert.equal(collection.classes.has('mobile-detail'),false);assert.equal(collection.wheel.scrollTop,128);assert.equal(collection.rows[1].dataset.nameVisible,'true');
 const invalid=nativeFixture({mobile,query:'?model=missing'});assert.equal(invalid.nodes.title.textContent,'cooperoceras');assert.equal(invalid.classes.has('mobile-detail'),false);
}
assert.doesNotThrow(()=>nativeFixture({ids:[]}));
console.log('Native startup passed: parser-time centering, canonical selected poster, direct mobile detail, preserved filter return link, invalid-query fallback and empty catalog.');

// Execute the production paint expressions, not a duplicate geometry helper.
const enhancedPaint=main.split('\n').find(line=>line.includes('const d=(i*SLOT-position)/SLOT'));
assert(enhancedPaint,'Enhanced wheel paint remains covered');
const galleryCSS=await readFile(new URL('./gallery/style.css',import.meta.url),'utf8');
assert.match(galleryCSS,/@media\(max-width:760px\)\{\.slot-image\{left:-12px\}\}/,'A shared mobile-only host offset moves thumbnails and loading cubes together, including reduced motion');
const numericTransform=value=>value==='none'?{x:0,scale:1}:(()=>{const match=value.match(/^translateX\(([-+\d.e]+)px\) scale\(([-+\d.e]+)\)$/);assert(match,value);return{x:Number(match[1]),scale:Number(match[2])};})();
for(const width of [320,390,440,760,761,1024,1180,1280,1440])for(const reduced of [false,true])for(const offset of [0,37]){
 const mobile=width<=760,ids=['top','above','center','below','bottom'],native=nativeFixture({mobile,reduced,ids,selected:'center'}),position=256+offset;
 if(offset){native.wheel.scrollTop=position;native.wheel.scroll();}
 const transforms=[];
 for(let i=0;i<ids.length;i++){
  const host={style:{}},context=vm.createContext({i,SLOT:128,position,reduced:()=>reduced,mobile:()=>mobile,row:{querySelector:()=>host}});
  vm.runInContext(enhancedPaint,context);
  const actual=numericTransform(host.style.transform),initial=numericTransform(native.rows[i].image.style.transform),distance=(i*128-position)/128;
  assert.deepEqual(actual,initial,`Startup and enhanced paint agree at ${width}px, row ${i}, reduced=${reduced}`);
  assert.equal(host.style.opacity,native.rows[i].image.style.opacity);
  assert.equal(actual.scale,reduced?1:.58+.42*Math.exp(-.65*distance*distance),'The established scale curve is unchanged');
  assert.equal(actual.x,0,'Every desktop and mobile row stays on its shared thumbnail-column axis');
  transforms.push(actual);
 }
 assert(transforms.every(value=>value.x===0),'All scaled rows share the existing image-column X axis');
}
console.log('Thumbnail axis passed: native/enhanced agreement, 320/390/440/760/761/1024/1180/1280/1440 widths, shared 12px mobile host offset, centered/fractional scroll, scale/opacity preservation and reduced motion.');

const nativePending=nativeFixture();const pendingImage=nativePending.rows[0].thumbnail;let nativeDecoded;pendingImage.decode=()=>new Promise(done=>nativeDecoded=done);pendingImage.load();assert.equal(pendingImage.dataset.thumbnailState,'decoding');nativeDecoded();await tick();assert.equal(pendingImage.dataset.thumbnailState,'ready');
let nativeCachedDecodes=0;const nativeCached=nativeFixture({thumbnail:{complete:true,naturalWidth:32,decode:()=>{nativeCachedDecodes++;return Promise.resolve();}}});await tick();assert(nativeCached.rows.every(row=>row.thumbnail.dataset.thumbnailState==='ready'));nativeCached.rows[0].thumbnail.load();assert.equal(nativeCachedDecodes,3,'Cached readiness and a later load event do not restart native decode');
for(const decode of [()=>Promise.reject(Error('bad decode')),()=>{throw Error('bad decode');}]){const broken=nativeFixture({thumbnail:{complete:true,naturalWidth:32,decode}});await tick();assert(broken.rows.every(row=>row.thumbnail.dataset.thumbnailState==='error'));}
const nativeFailed=nativeFixture({thumbnail:{complete:true,naturalWidth:0}});assert(nativeFailed.rows.every(row=>row.thumbnail.dataset.thumbnailState==='error'));
console.log('Native thumbnail readiness: pending decode, cached completion, duplicate load, decode rejection/throw and failed image passed.');

for(const completion of ['timeout','event']){
 const noAPI=nativeFixture({thumbnail:{getAnimations:undefined,complete:true,naturalWidth:32,decode:()=>Promise.resolve()}});await tick();
 assert(noAPI.rows.every(({thumbnail})=>thumbnail.dataset.thumbnailState==='ready'&&thumbnail.dataset.thumbnailReveal==='entering'),'Native images without animation inspection stay decoded while the reveal runs');
 assert.equal(noAPI.timers.size,3);assert([...noAPI.timers.values()].every(timer=>timer.delay===250),'Native fallback keeps the existing 250 ms bound');
 if(completion==='event')for(const {thumbnail}of noAPI.rows)thumbnail.transitionend({target:thumbnail,propertyName:'opacity'});
 else for(const {fn}of [...noAPI.timers.values()])fn();
 assert(noAPI.rows.every(({thumbnail})=>thumbnail.dataset.thumbnailState==='ready'&&thumbnail.dataset.thumbnailReveal==='settled'));assert.equal(noAPI.timers.size,0);
 assert(noAPI.rows.every(({thumbnail})=>!thumbnail.transitionend&&!thumbnail.transitioncancel),'Native fallback and events clean both listeners');
}
console.log('Native missing animation API: real transition is not cut short, opacity end or 250 ms fallback settles ready and cleans listeners.');

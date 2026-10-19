import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFile} from 'node:fs/promises';

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
 const article={removeAttribute(){},prepend(node){events.push('status');this.status=node.textContent;}};
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
 await f.run;assert.deepEqual(f.body.childNodes,f.original);assert.equal(f.body.dataset.gallery,undefined);assert.equal(f.document.documentElement.dataset.theme,'dark');assert(f.article.status.includes('仍可浏览'));
}
console.log('Gallery startup passed: imports are DOM-inert; code/CSS and catalog gate the swap; mount has visible geometry; all rejected prerequisites restore linked SSG and theme.');

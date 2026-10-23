import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import vm from 'node:vm';
import {formatModelLength,modelHeight,dimensionDetails,dimensionNote,comparisonMeasurement,comparisonText} from '../model-dimensions.js';
import {publishedModels} from './geometry-fixtures.mjs';
const root=new URL('./',import.meta.url),models=await publishedModels(),source=await readFile(new URL('../main.js',root),'utf8'),html=await readFile(new URL('../shell.html',root),'utf8');
const checks=[];assert(models.length>0);
const cycad=models.find(a=>a.id==='cycad');assert.equal(modelHeight(cycad),'1.37 m');assert.equal(dimensionDetails(cycad),'Height (Y): 1.37 m · Width (X): 2.11 m · Depth (Z): 2.17 m');assert.equal(dimensionDetails(cycad,'zh'),'高度 (Y)：1.37 m · 宽度 (X)：2.11 m · 深度 (Z)：2.17 m');checks.push('Exact cycad identity: 1.37 m height, 2.11 m width, 2.17 m depth in both languages');
const wave=models.find(a=>a.id==='wave-ripple-surface');
assert.equal(comparisonMeasurement(wave),'Footprint (W × D) 1.50 × 1.16 m · Thickness 8.1 cm');
assert.equal(comparisonMeasurement(wave,'zh'),'占地（宽 × 深）1.50 × 1.16 m · 厚度8.1 cm');
assert.equal(modelHeight(wave),'8.1 cm');
for(const asset of models.filter(a=>a!==wave))for(const lang of ['en','zh'])for(const kind of ['hand','human'])assert.equal(comparisonText(kind,lang,asset),comparisonText(kind,lang));
for(const asset of [undefined,{id:wave.id},{id:wave.id,dimensions:[1.5,NaN,1.16]},{id:wave.id,dimensions:[1.5,-.081,1.16]}])assert.equal(comparisonMeasurement(asset),'');
checks.push('Flat-wave caption separates X/Z footprint 1.50 × 1.16 m from Y thickness 8.1 cm in both languages; all other published model captions stay unchanged');
for(const asset of models){
 const original=JSON.stringify(asset.dimensions),[width,height,depth]=asset.dimensions;
 assert.equal(modelHeight(asset),formatModelLength(height));
 for(const lang of ['en','zh']){
  const text=dimensionDetails(asset,lang);for(const size of [width,height,depth])assert(text.includes(formatModelLength(size)));
  assert.match(text,lang==='en'?/^Height \(Y\): .* · Width \(X\): .* · Depth \(Z\): /:/^高度 \(Y\)：.* · 宽度 \(X\)：.* · 深度 \(Z\)：/);
 }
 assert.equal(JSON.stringify(asset.dimensions),original,'Dimension presentation must not mutate metadata');assert(!/^0(?:\.0)? cm$/.test(modelHeight(asset)),'Small dimensions must not round down to zero');
}
checks.push('All published primary metrics use Y; X/Y/Z details stay explicit in both languages without mutating metadata or rounding tiny heights to zero');
assert.equal(formatModelLength(NaN),'—');assert.equal(formatModelLength(-1),'—');assert.equal(formatModelLength(undefined),'—');assert.equal(formatModelLength(.18),'18 cm');assert.equal(formatModelLength(.009243897),'0.9 cm');
// Sub-millimeter formatting is independent of which models are published.
for(const [meters,expected] of [
 [0,'0 cm'],[-0,'0 cm'],[Number.MIN_VALUE,'4.94e-321 mm'],
 [1e-12,'1e-9 mm'],[.0000001,'0.0001 mm'],[.0000499,'0.0499 mm'],
 [.00040237721987068653,'0.402 mm'], // Actual Palaeotarbus height.
 [.000499999999,'0.5 mm'],[.0005,'0.5 mm'],[.000999,'0.999 mm'],
 [.001,'0.1 cm'],[.001001,'0.1 cm'],[.009243897,'0.9 cm'],
 [.18,'18 cm'],[.999,'99.9 cm'],[1,'1.00 m'],[1.37,'1.37 m'],
 [Infinity,'—'],[-Infinity,'—'],['0.0004','—'],[null,'—'],
])assert.equal(formatModelLength(meters),expected,`Length ${meters}`);
for(let exponent=-323;exponent<=-4;exponent++){
 const meters=10**exponent,formatted=formatModelLength(meters);
 assert(Number.parseFloat(formatted)>0,`Positive ${meters} must stay positive: ${formatted}`);
 assert.match(formatted,/ mm$/);
}
const tinyAsset={dimensions:[.000499,.00040237721987068653,.000001]},tinySnapshot=JSON.stringify(tinyAsset);
assert.equal(modelHeight(tinyAsset),'0.402 mm');
assert.equal(dimensionDetails(tinyAsset),'Height (Y): 0.402 mm · Width (X): 0.499 mm · Depth (Z): 0.001 mm');
assert.equal(dimensionDetails(tinyAsset,'zh'),'高度 (Y)：0.402 mm · 宽度 (X)：0.499 mm · 深度 (Z)：0.001 mm');
assert.equal(JSON.stringify(tinyAsset),tinySnapshot);
assert.match(dimensionNote('en'),/millimeters \(mm\)/);assert.match(dimensionNote('zh'),/毫米 \(mm\)/);
checks.push('Sub-millimeter actual Palaeotarbus height, unit boundaries, zero, invalid input and positive values down to Number.MIN_VALUE retain nonzero measurements; ordinary cm/m outputs remain unchanged');
assert.match(html,/id="dimensions"><\/strong><span data-en="Model height" data-zh="模型高度"/);
assert.doesNotMatch(source,/Math\.max\(\.\.\.asset\.dimensions\)/);assert.match(source,/\$\('#dimensions'\)\.textContent=modelHeight\(asset\);/);
checks.push('Production main.js uses modelHeight, and index.html labels it Model height / 模型高度');
class Node{
 constructor(){this.children=[];this.dataset={};this.attributes={};this.textContent='';this.hidden=false;this.style={};this.classList={add(){},remove(){}};}
 append(...nodes){this.children.push(...nodes);}
 replaceChildren(...nodes){this.children=[...nodes];}
 setAttribute(name,value){this.attributes[name]=value;}
 contains(node){return this===node||this.children.some(child=>child.contains?.(node));}
}
const nodes=new Map(),get=s=>{if(!nodes.has(s))nodes.set(s,new Node());return nodes.get(s);},label=new Node();label.dataset={en:'Model height',zh:'模型高度'};
const state={lang:'en',selected:'cycad'},document={documentElement:{lang:'en'},createElement:()=>new Node()},renderer={comparison:false,kind:'human',compare(){this.comparison=true;return {kind:this.kind};}};
const ui={resetCopy(){},updateOverflow(){}},storage=new Map();
const context=vm.createContext({state,document,$:get,all:selector=>selector==='[data-gallery-route]'?[]:[label],wheel:new Node(),renderer,URL,siteRoot:new URL('https://example.test/'),detailHref:id=>'/models/'+id+'/',saveCurrentHistory(){},t:(en,zh)=>state.lang==='zh'?zh:en,modelHeight,dimensionDetails,dimensionNote,comparisonText,ui,sample:models,localStorage:{setItem:(k,v)=>storage.set(k,v)},renderSummary(){},renderWheel(){},short:a=>a.id,categories:{plants:['Plants','植物']},draft:null,renderFilters(){},currentReady:true});
for(const name of ['updateComparisonLabel','translate','infoContent']){const line=source.split('\n').find(s=>s.startsWith('function '+name+'('));assert(line);vm.runInContext(line,context);}
const languageLine=source.split('\n').find(s=>s.startsWith("$('#language').onclick="));vm.runInContext(languageLine,context);
const comparisonStart=source.indexOf("$('#compare').onclick="),comparisonEnd=source.indexOf(";$('#reset').onclick=",comparisonStart);assert(comparisonEnd>comparisonStart);vm.runInContext(source.slice(comparisonStart,comparisonEnd)+';',context);
const actualMetricAssignment=source.match(/\$\('#dimensions'\)\.textContent=[^;]+;/)[0];
for(const asset of models){context.asset=asset;vm.runInContext(actualMetricAssignment,context);assert.equal(get('#dimensions').textContent,formatModelLength(asset.dimensions[1]));for(const lang of ['en','zh']){state.lang=lang;vm.runInContext('infoContent(asset);',context);assert.equal(get('#info-content').children[1].textContent,dimensionDetails(asset,lang));assert.equal(get('#info-content').children[2].textContent,dimensionNote(lang));}}
checks.push('Actual production metric assignment and infoContent execute correctly in a bounded fake DOM for all published models × 2 languages');
state.lang='en';renderer.kind='hand';get('#compare').onclick();assert.match(get('#comparison-label').textContent,/Hand length 18 cm/);assert.equal(get('#compare').ariaPressed,'true');assert.equal(get('#comparison-label').hidden,false);
get('#compare').onclick();assert.equal((get('#comparison-label').textContent.match(/Horizontal drag/g)||[]).length,1);
get('#language').onclick();assert.equal(state.lang,'zh');assert.equal(label.textContent,'模型高度');assert.equal(document.documentElement.lang,'zh-CN');assert.match(get('#comparison-label').textContent,/手长18 cm/);assert.equal(get('#info-content').children[1].textContent,dimensionDetails(cycad,'zh'));assert.equal(storage.get('wheel-language'),'zh');
get('#language').onclick();assert.equal(label.textContent,'Model height');assert.match(get('#comparison-label').textContent,/Hand length 18 cm/);assert.equal(get('#info-content').children[1].textContent,dimensionDetails(cycad,'en'));
renderer.kind='human';get('#compare').onclick();assert.match(get('#comparison-label').textContent,/Human height 1.8 m/);get('#language').onclick();assert.match(get('#comparison-label').textContent,/人物身高1.8m/);
checks.push('Actual Compare and language-click handlers update both metric/info labels and live reference wording in both directions; repeated Compare keeps one gesture hint');
// Reuse production handlers with a bounded renderer/DOM stub to test label ownership.
renderer.compare=function(){this.comparison=!this.comparison;return this.comparison?{kind:this.kind}:false;};
renderer.reset=function(){this.comparison=false;};
renderer.select=async function(){this.comparison=false;return true;};
renderer.detail={metric:{available:true}};
Object.assign(context,{syncMobileView(){},selectionVersion:0,selectionLoadingTimer:0,closeInfo(){},stopHover(){},hover:{pause(){},refresh(){}},settler:{stop(){}},saveCurrentHistory(){},pushHistory(){},urlAsset:path=>path,selectPoster:()=>({ready:Promise.resolve(true)}),mobile:()=>false,setTimeout:()=>1,clearTimeout(){},showError(){throw Error('Unexpected selection error');},console:{warn(){}}});
document.body=new Node();ui.filter={open:false};
vm.runInContext(source.slice(source.indexOf('async function choose('),source.indexOf('function showError(')),context);
const resetStart=source.indexOf("$('#reset').onclick="),resetEnd=source.indexOf(";$('#retry').onclick=",resetStart);vm.runInContext(source.slice(resetStart,resetEnd)+';',context);
const errorStart=source.indexOf('renderer.onReferenceError='),errorEnd=source.indexOf(';renderer.onInteraction=',errorStart);assert(errorEnd>errorStart);vm.runInContext(source.slice(errorStart,errorEnd)+';',context);
const pointerHandlers=[];document.addEventListener=(name,handler)=>{if(name==='pointerdown')pointerHandlers.push(handler);};
vm.runInContext(source.split('\n').find(line=>line.startsWith("document.addEventListener('pointerdown'")&&line.includes('ui.filter.open')),context);
for(const lang of ['en','zh']){
 state.lang=lang;await vm.runInContext("choose('wave-ripple-surface',{push:false,openMobile:false});",context);
 assert.equal(get('#comparison-label').hidden,true);assert.equal(get('#compare').attributes['aria-pressed'],'false');assert.equal(get('#dimensions').textContent,'8.1 cm');
 renderer.kind='human';get('#compare').onclick();assert.equal(get('#comparison-label').textContent,comparisonText('human',lang,wave));
 get('#language').onclick();assert.equal(get('#comparison-label').textContent,comparisonText('human',state.lang,wave));
 pointerHandlers[0]({target:get('#detail')});assert.equal(renderer.comparison,true);
 pointerHandlers[0]({target:get('#compare')});assert.equal(renderer.comparison,true);
 pointerHandlers[0]({target:new Node()});assert.equal(renderer.comparison,false);assert.equal(get('#comparison-label').hidden,true);
 get('#compare').onclick();get('#reset').onclick();assert.equal(renderer.comparison,false);assert.equal(get('#comparison-label').hidden,true);
 get('#compare').onclick();renderer.comparison=false;renderer.onReferenceError(new Error('reference load failed'));
 const failure=state.lang==='en'?'Reference could not load. Try again.':'参照加载失败，请重试。';assert.equal(get('#comparison-label').textContent,failure);assert.equal(get('#compare').ariaPressed,'false');
 vm.runInContext('translate();',context);assert.equal(get('#comparison-label').textContent,failure,'An error must not restore a stale measurement caption');
 await vm.runInContext("choose('cooperoceras',{push:false,openMobile:false});",context);assert.equal(get('#comparison-label').hidden,true);
 renderer.kind='hand';get('#compare').onclick();assert.equal(get('#comparison-label').textContent,comparisonText('hand',state.lang));assert.doesNotMatch(get('#comparison-label').textContent,/1\.50|8\.1|Footprint|占地/);
}
checks.push('Actual label, Compare, language, outside-click, Reset, selection and load-error handlers keep wave measurements tied to the current asset; hand text stays compact');
const css=await readFile(new URL('../style.css',root),'utf8');
assert.match(css,/@media\(max-width:760px\)\{[^\n]*#comparison-label\{[^}]*max-width:80%;[^}]*font-size:9px/);
assert.doesNotMatch(css,/#comparison-label\{[^}]*white-space:nowrap/);
checks.push('Existing phone caption width and wrapping are retained; static CSS contract only, not browser layout verification');
assert.match(dimensionNote('en'),/authored-pose.*meters \(m\).*centimeters \(cm\).*stay fixed when you rotate/);assert.match(dimensionNote('zh'),/原始造型.*米 \(m\).*厘米 \(cm\).*旋转查看时数值保持不变/);
checks.push('Info disclosure explicitly defines authored pose and units and states dimensions stay fixed while rotating');
const report={status:'passed',scope:'Pure formatting plus actual production DOM-writing functions and click handlers in bounded fake DOM; no browser layout or raster verification',models:models.length,checks,cycad:{height:modelHeight(cycad),en:dimensionDetails(cycad),zh:dimensionDetails(cycad,'zh')}};await mkdir(new URL('./evidence/meter-scale/',root),{recursive:true});await writeFile(new URL('./evidence/meter-scale/ui-regression.json',root),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));

import assert from 'node:assert/strict';
import {mkdtempSync,readFileSync,writeFileSync,mkdirSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';import {dirname,join} from 'node:path';import {execFileSync} from 'node:child_process';
import {collectFinalFiveRelease,appendFinalFiveRelease,FINAL_FIVE_PRESENTATION,FINAL_FIVE_IDS} from './final-five-release.mjs';
import {digest} from './model-registry.mjs';
const root=process.cwd(),manifest=JSON.parse(readFileSync('assets/manifest.json'));
const out=await collectFinalFiveRelease(root);assert.deepEqual(out.additions.map(x=>x.id).sort(),FINAL_FIVE_IDS);
const base={...manifest,assets:manifest.assets.filter(x=>!FINAL_FIVE_IDS.includes(x.id)),publication:{...manifest.publication}};delete base.publication.final_five_presentation;
assert.deepEqual(await appendFinalFiveRelease(root,base,FINAL_FIVE_PRESENTATION),manifest);
const before=digest(base);await assert.rejects(appendFinalFiveRelease(root,{...base,assets:base.assets.slice(1)},FINAL_FIVE_PRESENTATION));assert.equal(digest(base),before);
await assert.rejects(collectFinalFiveRelease(root,{...FINAL_FIVE_PRESENTATION,sha256:'0'.repeat(64)}));
const pins=JSON.parse(execFileSync('python3',['-c',"import sys,json;sys.path.insert(0,'scripts');from final_delivery_fixed import DELIVERY_PATHS,DELIVERY_SUPPORT_PINS,RESTORATION_INDICES;print(json.dumps(sorted(set([p for x in DELIVERY_PATHS.values() for p in x.values()]+[x['path'] for x in DELIVERY_SUPPORT_PINS]+[x['path'] for x in RESTORATION_INDICES.values()]+['qa/final-delivery-20261021/'+b+'-summary.candidate.json' for b in ['batch109','batch108-en']]))))"],{encoding:'utf8'}));
const index=out.index;const paths=new Set([...pins,FINAL_FIVE_PRESENTATION.path,index.card_presentation_index.path,'site/public/gallery/resources.json','assets/turntables/index.json',...index.capture.shared.files.map(x=>x[0])]);
for(const row of index.rows){for(const pin of [row.metadata,row.canonical_preview,row.card])paths.add(pin.path);for(const f of row.gallery.files)paths.add('site/public/'+f.path);}
const fixture=mkdtempSync(join(tmpdir(),'final-five-contract-test-'));let rejects=2;
try{
 for(const p of paths){mkdirSync(dirname(join(fixture,p)),{recursive:true});writeFileSync(join(fixture,p),readFileSync(p));}
 // Browser version is a recipe input, not an executable fixture dependency.
 const browser='node_modules/playwright-core/browsers.json';mkdirSync(dirname(join(fixture,browser)),{recursive:true});writeFileSync(join(fixture,browser),readFileSync(browser));
 // posterRendererFiles parses static imports and needs no module execution.
 await collectFinalFiveRelease(fixture);
 const mutate=async(p,fn)=>{const f=join(fixture,p),b=readFileSync(f);try{writeFileSync(f,fn(b));await assert.rejects(collectFinalFiveRelease(fixture),undefined,`Must reject ${p}`);rejects++;}finally{writeFileSync(f,b);}};
 for(const p of [FINAL_FIVE_PRESENTATION.path,index.card_presentation_index.path,...index.rows.flatMap(x=>[x.metadata.path,x.glb.path,x.canonical_preview.path,x.card.path,'site/public/'+x.gallery.files[0].path,'site/public/'+x.gallery.files[1].path]),...pins.filter(x=>x.endsWith('.blend')||x.endsWith('summary.candidate.json'))])await mutate(p,b=>Buffer.concat([b,Buffer.from('tampered')]));
 await mutate('site/public/gallery/resources.json',b=>{const x=JSON.parse(b);delete x.posters.caryocrinites;return JSON.stringify(x);});
 await mutate('assets/turntables/index.json',b=>{const x=JSON.parse(b);x.posters=x.posters.filter(x=>x.id!=='caryocrinites');return JSON.stringify(x);});
 await mutate(FINAL_FIVE_PRESENTATION.path,b=>{const x=JSON.parse(b);x.rows[0].id='cupressocrinites';x.independent_gallery_review.status='PASS';return JSON.stringify(x);});
 await mutate(FINAL_FIVE_PRESENTATION.path,b=>{const x=JSON.parse(b);x.hardware_gpu_verified=true;return JSON.stringify(x);});
 console.log(`PASS final-five release: seven-role actual native collector, fixed presentation, exact347 append, ${rejects} rejection cases; no GPU/scene/live acceptance.`);
}finally{rmSync(fixture,{recursive:true,force:true});}

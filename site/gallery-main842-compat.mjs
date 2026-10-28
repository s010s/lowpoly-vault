/** Exact main842 v3 consistency boundary. No approval or capture-policy upgrade. */
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
export const MAIN842_POSTER_RECIPE={
  "version": 3,
  "sha256": "20565eab93aa3e8d17f47665c1a2221f0cff805d7a49ab8e373d74adae07549b",
  "files": [
    [
      "package-lock.json",
      "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
    ],
    [
      "package.json",
      "1bddf73367b09c1c72034cca826c1dfcebc1ae35e1480d9da99b8fd202a34b1b"
    ],
    [
      "site/capture-gallery-posters.mjs",
      "9eb0127253d66ad4bf81f3356071190f9a5c103c6dd1dfab002dc19dbddb8e15"
    ],
    [
      "site/gallery-poster-inputs.mjs",
      "c85d3ceef3cf03c5130a03d1f466d7db3a1893f88622579e31aa997eeb5c48f0"
    ],
    [
      "site/gallery/hover-presentation.js",
      "cd9c3f06412f451bf8cffb65dcbdc5bfe59692551f7b3d52cf8cf5edea9275e8"
    ],
    [
      "site/gallery/hover-turntable.js",
      "7e8ab8eaa60ad8ac6522f3327e19e7c31e0031329cce98d54a73210a81d66930"
    ],
    [
      "site/gallery/liquid-core.js",
      "e350d68360308cfa111ce7426aea54799da705f27054d5e4f12d52a34ed1c17a"
    ],
    [
      "site/gallery/model-support.js",
      "a1bf09e4997527448965dc1aadbb8e4241f69a9d33db25458ef25b0614e4fa74"
    ],
    [
      "site/gallery/reference-entry.js",
      "5104d47241d775da123f746bcb9ffd33ee8ab8ae86c4b14912f10ff9d8fb9943"
    ],
    [
      "site/gallery/renderer.js",
      "f31d66d68c5c63c448bb039b9059ef57937e58a9aa65d46d02e1ecd67fd08a6b"
    ],
    [
      "site/gallery/scale-reference.js",
      "da31270abaff87862147b0379edb3b4217cb4dfc2db466fcfc4dc15f26dc8b86"
    ],
    [
      "site/gallery/urls.js",
      "3b0fd929466739a8aca78141cd60500f15167fadde5b9bc3a501479926699113"
    ],
    [
      "site/gallery/view-transition.js",
      "8d18dc9f7f9f6c13d627fe3c4e6b8115504208900d4ed0883e5057ed9ad4caf0"
    ],
    [
      "site/render-preset.js",
      "8b0bb498d6127e4cd6f858d0811a796966cbc49ea7438e11904b5d9a28bc9044"
    ],
    [
      "site/viewer.js",
      "3d3e6dd1335c21b0836ebcf32689a4bfc558a8803ac2cc666e407f79ced509d0"
    ],
    [
      "vite.config.js",
      "e731be1d9c87e5297b9ab3ce3d11291fd3f81444fcc6277f783f6b53bb491c0a"
    ]
  ],
  "policy": {
    "version": 2,
    "site_base": "/",
    "node_major": "22",
    "viewport": {
      "width": 1440,
      "height": 900
    },
    "deviceScaleFactor": 1,
    "reducedMotion": "reduce",
    "detail": [
      512,
      512
    ],
    "wheel": [
      768,
      432
    ],
    "engine": "playwright-pinned-chromium",
    "args": [
      "--no-sandbox",
      "--use-gl=angle",
      "--use-angle=swiftshader",
      "--enable-unsafe-swiftshader"
    ],
    "fonts": "Not applicable: poster() draws transparent WebGL geometry directly to PNG, with no text or DOM rasterization."
  },
  "browser": "141.0.7390.37"
};
const INSERTIONS=[
  "import {restoreHistoricalPosterSerialization} from './gallery-poster-compat.mjs';\n",
  "import {successorReader,successorContext,historicalGalleryView,verifySuccessorPresentation} from './same-id-successors.mjs';\n",
  " if(manifest.publication?.same_id_successors){\n  const read=successorReader(root),context=successorContext({manifest,read});\n  await verifySuccessorPresentation(root,context);\n  const historicalResources=historicalGalleryView({manifest,resources,read});\n  await assertHistoricalPosterApprovals({root,baseline});\n  const orderedHistorical=restoreHistoricalPosterSerialization(historicalResources,baseline);\n  const legacy=await posterInputState(context.base,orderedHistorical,{root});\n  const ids=context.entries.map(row=>row.entry.id);\n  // Unchanged historical metadata/pixels are checked above, fresh mesh presentation\n  // is checked separately. Do not relabel successor receipts as old golden approval.\n  return {...legacy,valid:[...new Set([...legacy.valid,...ids])],stale:legacy.stale.filter(id=>!ids.includes(id)),approved:legacy.approved.filter(id=>!ids.includes(id)),capture:legacy.capture.filter(id=>!ids.includes(id)),successors:ids};\n }\n",
  "import {appendProductionPosterInputState} from './production-release.mjs';\n",
  "import {assertMain842PosterRecipe} from './gallery-main842-compat.mjs';\n",
  " const production=manifest.assets.filter(asset=>asset.production_release);\n if(production.length){\n  for(const asset of production)assert(!baseline?.posters?.[asset.id],'Production route cannot replace a historical golden approval');\n  const legacy=await posterInputState({...manifest,assets:manifest.assets.filter(asset=>!asset.production_release)},resources,{root});\n  return appendProductionPosterInputState(root,production,resources,legacy);\n }\n",
  "  // Existing non-golden consistency is retained only for the exact main842 v3\n  // recipe. These captures remain unapproved and stay in the fresh-capture list.\n  if(!approved&&baseline?.shared){\n   const main842=await assertMain842PosterRecipe({root,shared});\n   if(poster.input_sha256===posterInputKey(asset,main842)&&poster.browser_version===main842.browser){valid.push(asset.id);continue;}\n  }\n"
];
export function main842PosterSource(source){
 // Exact new dispatch removed only for old recipe comparison; its own source/presentation gate remains mandatory.
 for(const insertion of ["import {correctiveContext,correctiveOutputView,verifyCorrectivePresentation} from './old-corrective-ten-selection.mjs';\n", " if(manifest.publication?.old_corrective_ten){\n  const read=successorReader(root),context=correctiveContext({manifest,read});\n  await verifyCorrectivePresentation(root,context);\n  const historicalResources=correctiveOutputView({manifest,kind:'gallery',value:resources,read});\n  const legacy=await posterInputState(context.baseline.manifest,historicalResources,{root});\n  const ids=context.entries.map(e=>e.next.id);\n  return {...legacy,valid:[...new Set([...legacy.valid,...ids])],stale:legacy.stale.filter(id=>!ids.includes(id)),approved:legacy.approved.filter(id=>!ids.includes(id)),capture:legacy.capture.filter(id=>!ids.includes(id)),corrective:ids};\n }\n"]){if(source.includes(insertion)){assert.equal(source.split(insertion).length,2);source=source.replace(insertion,'');}}
 for(const insertion of INSERTIONS){assert.equal(source.split(insertion).length,2,'Main842 compatibility insertion changed');source=source.replace(insertion,'');}
 return source;
}
// Only this reviewed, explicit opt-in dispatch may be absent from the older pair recipe.
// Its dynamic imports execute only in --detail-presentations mode; that mode's
// outputs require their separate mandatory detail-capture authority and closure proof.
// This does NOT authenticate the new mode or rewrite any historical receipt.
export const MAIN842_DETAIL_DISPATCH = "// Single supported entry: this narrow migration uses the same runtime recipe.\nif(process.argv.includes('--detail-presentations')){\n const delta=process.argv.find(arg=>arg.startsWith('--detail-ids='));\n if(delta){const {captureDetailDelta}=await import('./detail-capture-delta.mjs');await captureDetailDelta(delta.slice('--detail-ids='.length).split(',').filter(Boolean));}\n else {const {default:detailIndex}=await import('./gallery/detail-presentations-index.js');if(Object.keys(detailIndex.presentations||{}).length)throw new Error('Existing right deliveries require explicit --detail-ids for incremental capture; a full renderer migration needs separate review');await import('./capture-detail-presentations.mjs');}\n process.exit(0);\n}\n";
export function main842CaptureSource(source){
 const expected=MAIN842_POSTER_RECIPE.files.find(([path])=>path==='site/capture-gallery-posters.mjs')[1];
 if(hash(source)===expected)return source;
 const prefix='// BEGIN GALLERY POSTER V3 ORCHESTRATION\n';
 const next="import {preparePosterCapture,completePosterCapture} from './gallery-poster-orchestration.mjs';\n";
 assert(source.startsWith(prefix+MAIN842_DETAIL_DISPATCH+next),'Main842 detail dispatch position or bytes changed');
 assert.equal(source.split(MAIN842_DETAIL_DISPATCH).length,2,'Main842 detail dispatch must occur exactly once');
 const historical=prefix+source.slice(prefix.length+MAIN842_DETAIL_DISPATCH.length);
 assert.equal(hash(historical),expected,'Main842 historical pair capture body changed');
 return historical;
}
export async function assertMain842PosterRecipe({root,shared}){
 const expected=MAIN842_POSTER_RECIPE;
 assert.equal(expected.sha256,hash(JSON.stringify({domain:'gallery-poster-capture-v3',policy:expected.policy,files:expected.files,browser:expected.browser})),'Main842 recipe seal differs');
 assert.deepEqual(shared.policy,expected.policy,'Main842 capture policy changed');assert.equal(shared.browser,expected.browser,'Main842 browser changed');
 assert.deepEqual(shared.files.map(row=>row[0]),expected.files.map(row=>row[0]),'Main842 renderer dependency closure changed');
 for(const [path,digest]of expected.files){
  let actual=shared.files.find(row=>row[0]===path)?.[1];
  if(path==='site/gallery-poster-inputs.mjs')actual=hash(main842PosterSource(await readFile(resolve(root,path),'utf8')));
  if(path==='site/capture-gallery-posters.mjs'){
   const source=await readFile(resolve(root,path),'utf8');assert.equal(hash(source),actual,'Main842 supplied capture input differs from actual bytes');
   actual=hash(main842CaptureSource(source));
  }
  assert.equal(actual,digest,`Main842 actual renderer/harness input changed: ${path}`);
 }
 return expected;
}

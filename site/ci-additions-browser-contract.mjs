/** Pure, fail-closed acceptance contract. No filesystem, browser, or publication imports. */
import assert from 'node:assert/strict';

export const ADDITIONS_BROWSER_VERSION = 1;
export const ADDITIONS_BROWSER_KIND = 'added-model-browser-acceptance';
export const ADDITIONS_DESKTOP_KIND = 'added-model-desktop-acceptance';
export const ADDITIONS_BROWSER_PIN = Object.freeze({playwright:'1.56.1',chromium:'141.0.7390.37',revision:'1194'});
export const ADDITIONS_VIEWPORTS = Object.freeze([
  Object.freeze({name:'1440x1000',width:1440,height:1000,touch:false,lang:'en'}),
  Object.freeze({name:'390x844-touch',width:390,height:844,touch:true,lang:'zh'}),
]);
const ID=/^[a-z0-9]+(?:-[a-z0-9]+)*$/, HASH=/^[a-f0-9]{64}$/, SHA=/^[a-f0-9]{40}$/;
const safePath=value=>typeof value==='string'&&value.startsWith('assets/')&&!/[\\\u0000-\u001f?#%:]/.test(value)&&value.split('/').every(part=>part&&part!=='.'&&part!=='..');
const positive=value=>Number.isSafeInteger(value)&&value>0;
function exactIDs(ids,label){
  assert(Array.isArray(ids)&&ids.length>0,`${label} must be a nonempty ID array`);
  assert(ids.every(id=>typeof id==='string'&&ID.test(id)),`${label} contains an unsafe ID`);
  assert.equal(new Set(ids).size,ids.length,`${label} contains duplicate IDs`);
  return [...ids].sort();
}
export function parseAddedModelIDs(raw){
  assert(typeof raw==='string'&&raw.trim(),'QA_ADDED_MODEL_IDS is required; no full-catalog default is allowed');
  return exactIDs(raw.split(',').map(id=>id.trim()),'QA_ADDED_MODEL_IDS');
}
export function selectAddedModels(manifest,selectedIDs){
  const selected=exactIDs(selectedIDs,'Selected additions');
  assert(manifest&&manifest.review_only!==true&&Array.isArray(manifest.assets),'A published manifest is required');
  const published=exactIDs(manifest.assets.map(asset=>asset.id),'Published manifest');
  assert(selected.every(id=>published.includes(id)),'Selected additions contain an unpublished model');
  return selected.map(id=>{
    const asset=manifest.assets.find(asset=>asset.id===id);
    for(const key of ['glb','blend']){
      assert(safePath(asset[key])&&asset[key].endsWith(`.${key}`),`${id}: unsafe ${key} path`);
      assert(HASH.test(asset.sha256?.[key]||''),`${id}: missing ${key} hash`);
    }
    assert(['en','zh'].every(lang=>typeof asset.name?.[lang]==='string'&&asset.name[lang].trim()),`${id}: missing localized title`);
    return asset;
  });
}
function assertIdentity(report,identity){
  assert(identity&&SHA.test(identity.source_commit||''),'Expected source commit is required');
  assert.equal(report.source_commit,identity.source_commit,'Additions source commit differs');
  for(const key of ['run_id','run_attempt']){
    assert(positive(Number(identity[key])),`Expected ${key} is required`);
    assert(positive(report[key]),`Report ${key} is required`);
    assert.equal(report[key],Number(identity[key]),`Additions ${key} differs`);
  }
  if(identity.source_tree!==undefined){assert(SHA.test(identity.source_tree),'Invalid expected source tree');assert.equal(report.source_tree,identity.source_tree,'Additions source tree differs');}
}
function assertFile(file,path,hash,label){
  assert(file&&file.path===path,`${label}: wrong file path`);
  assert.equal(file.sha256,hash,`${label}: actual file hash differs`);
  assert(positive(file.bytes),`${label}: missing actual file bytes`);
}
/** The caller supplies independently derived new IDs and current run identity.
 * Success establishes functional browser coverage, not visual/formal approval.
 */
function assertAcceptanceReport(report,{manifest,selectedIDs,identity},viewports,kind){
  const assets=selectAddedModels(manifest,selectedIDs),expected=assets.map(asset=>asset.id);
  assert.equal(report?.version,ADDITIONS_BROWSER_VERSION,'Unsupported additions browser report');
  assert.equal(report.kind,kind,'Wrong additions browser report kind');
  assert.equal(report.status,'pass','Additions browser did not pass');
  assertIdentity(report,identity);
  assert.equal(report.chromium_version,ADDITIONS_BROWSER_PIN.chromium,'Additions browser is not pinned Chromium');
  assert.deepEqual(report.browser_pin,ADDITIONS_BROWSER_PIN,'Additions browser package/revision differs');
  assert.equal(report.served_output_only,true,'Only the built output may be served');
  assert.equal(report.visual_approval,false,'Browser acceptance is not visual approval');
  assert.equal(report.formal_approval,false,'Browser acceptance is not formal publication approval');
  assert.deepEqual(exactIDs(report.selected_ids,'Reported additions'),expected,'Browser selection differs from exact additions');
  assert.deepEqual(exactIDs(report.actual_glb_ids,'Actually loaded additions'),expected,'Actual GLB coverage differs');
  for(const key of ['page_errors','resource_errors','fallback_events'])assert.deepEqual(report[key],[],`Additions reported ${key}`);
  assert.equal(report.sequence_requests,0,'Additions must not request historical turntable sequences');
  assert(Array.isArray(report.cases)&&report.cases.length===expected.length*viewports.length,'Exact required viewport cases are required per addition');
  const seen=new Set();
  for(const row of report.cases){
    const asset=assets.find(asset=>asset.id===row.id),viewport=viewports.find(viewport=>viewport.name===row.viewport);
    assert(asset,'Unexpected browser case model');assert(viewport,'Unexpected browser viewport');
    const key=`${row.id}:${row.viewport}`;assert(!seen.has(key),'Duplicate additions browser case');seen.add(key);
    assert.equal(row.status,'pass',`${key}: did not pass`);
    assert.deepEqual(row.viewport_config,{width:viewport.width,height:viewport.height,hasTouch:viewport.touch,isMobile:viewport.touch},`${key}: wrong viewport configuration`);
    assert.equal(row.lang,viewport.lang,`${key}: wrong locale`);
    assert.equal(row.discovery?.id,row.id,`${key}: wrong wheel row`);
    assert.equal(row.discovery?.poster_decoded,true,`${key}: poster was not decoded`);
    assert(positive(row.discovery?.poster_width)&&positive(row.discovery?.poster_height),`${key}: empty poster`);
    assert.equal(row.horizontal_overflow,false,`${key}: horizontal overflow`);
    assert.equal(row.fallback,false,`${key}: fallback is not accepted`);
    const detail=row.detail;
    for(const field of ['id','selected_id','first_frame_id','renderer_id'])assert.equal(detail?.[field],row.id,`${key}: wrong ${field}`);
    assert.equal(detail.title,asset.name[viewport.lang],`${key}: wrong localized title`);
    assert.equal(detail.state,'ready',`${key}: detail not ready`);
    assert.equal(detail.renderer_status,'ready',`${key}: renderer not ready`);
    assert.equal(detail.model_present,true,`${key}: no live GLB model`);
    assert.equal(detail.context_lost,false,`${key}: lost WebGL context`);
    assert.equal(detail.renderer_count,1,`${key}: expected one renderer`);
    assert.equal(detail.gl_error,0,`${key}: WebGL error`);
    assert.equal(detail.poster_source,'canonical',`${key}: fallback poster`);
    assert(positive(detail.live_bytes),`${key}: missing live GLB bytes`);
    assert(Array.isArray(row.observed_glbs)&&row.observed_glbs.length>0,`${key}: no browser GLB response`);
    for(const file of row.observed_glbs){assertFile(file,asset.glb,asset.sha256.glb,`${key} browser GLB`);assert.equal(file.bytes,detail.live_bytes,`${key}: live GLB byte count differs`);}
    for(const format of ['glb','blend'])assertFile(row.downloads?.[format],asset[format],asset.sha256[format],`${key} ${format} download`);
    assert.equal(row.downloads.glb.bytes,detail.live_bytes,`${key}: downloaded/live GLB bytes differ`);
    assert.equal(row.navigation?.detail_model,row.id,`${key}: detail URL differs`);
    if(viewport.touch){
      assert.equal(row.navigation.back_to_collection,true,`${key}: mobile Back failed`);
      assert.equal(row.navigation.collection_model,null,`${key}: collection URL retains a model`);
      assert.equal(row.navigation.collection_url_restored,true,`${key}: collection URL was not restored`);
      assert.equal(row.navigation.wheel_visible,true,`${key}: wheel missing after Back`);
      assert.equal(row.navigation.scroll_restored,true,`${key}: wheel scroll was not restored`);
      assert.equal(row.navigation.results_restored,true,`${key}: collection membership changed`);
    }
  }
  return report;
}

export function assertAdditionsReport(report,options={}){
  return assertAcceptanceReport(report,options,ADDITIONS_VIEWPORTS,ADDITIONS_BROWSER_KIND);
}
export function assertAdditionsDesktopReport(report,options={}){
  return assertAcceptanceReport(report,options,ADDITIONS_VIEWPORTS.slice(0,1),ADDITIONS_DESKTOP_KIND);
}
/** Reuse only successful strict-GPU output from this exact shard/run/source. */
export function assertAdditionsDesktopSource(browser,options={}){
  const selected=exactIDs(options.selectedIDs,'Selected desktop additions');
  for(const key of ['status','browser_status'])assert.equal(browser?.[key],'pass',`Desktop source ${key} did not pass`);
  assert.equal(browser.profile,'strict-gpu','Desktop source permits fallback');
  assert.equal(browser.review_scope,'models','Desktop source is not model-scoped');
  assert.equal(browser.commit,options.identity?.source_commit,'Desktop source commit differs');
  assert.equal(browser.chromium_version,ADDITIONS_BROWSER_PIN.chromium,'Desktop source browser differs');
  assert.equal(browser.gpu?.status,'pass','Desktop source GPU did not pass');
  for(const key of ['page_errors','resource_errors'])assert.deepEqual(browser[key],[],`Desktop source ${key}`);
  assert.deepEqual(browser.gpu.fallback_models,[],'Desktop source used fallback');
  assert.deepEqual(exactIDs(browser.selected_model_ids,'Desktop source selection'),selected,'Desktop source selection differs');
  assert.deepEqual(exactIDs(browser.gpu.rendered_models,'Desktop source rendered models'),selected,'Desktop source rendered IDs differ');
  assert(Array.isArray(browser.models),'Missing desktop source model cases');
  assert.deepEqual(exactIDs(browser.models.map(row=>row.id),'Desktop source cases'),selected,'Desktop source cases differ');
  const assets=selectAddedModels(options.manifest,selected);
  for(const row of browser.models){assert.equal(row.status,'gpu-pass','Desktop source model did not pass GPU');assert.equal(row.glb_sha256,assets.find(asset=>asset.id===row.id).sha256.glb,'Desktop source GLB differs');}
  return assertAdditionsDesktopReport(browser.additions_desktop,options);
}

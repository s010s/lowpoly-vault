import { existsSync } from 'node:fs';
import { runGalleryBrowserTests } from './gallery-browser-test.mjs';
/** Review-only acceptance. Never publishes, approves assets, or mutates the release manifest. */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import assert from 'node:assert/strict';
import { createCatalog } from './catalog-build.mjs';
import { catalogMembership } from './curation.js';
import { normalizeSiteBase, routeHref, CATALOG_PAGE_SIZE } from './routes.js';

const root = resolve(process.env.GALLERY_DIR || 'qa/redesign-v2-site');
const prefix = normalizeSiteBase(process.env.SITE_BASE || '/lowpoly-vault/');
const output = resolve(process.env.QA_OUTPUT_DIR || 'qa/redesign-browser');
const allowFallback = process.env.QA_ALLOW_WEBGL_FALLBACK === '1';
const forceFallback = process.env.QA_FORCE_WEBGL_FALLBACK === '1';
const reviewScope = process.env.QA_REVIEW_SCOPE || 'full';
assert(['full','models','matrix'].includes(reviewScope), 'Known review scope required');
const selectedIDs = process.env.QA_MODEL_IDS ? new Set(process.env.QA_MODEL_IDS.split(',')) : null;
const staticOnly = process.env.QA_STATIC_ONLY === '1';
const wheelBuild = existsSync(resolve(root,'gallery/resources.json'));
assert(!forceFallback || allowFallback, 'Forced fallback requires QA_ALLOW_WEBGL_FALLBACK=1');
const report = {
  status: 'running', commit: process.env.GITHUB_SHA || null, build_directory: root,
  review_scope: reviewScope, selected_model_ids: selectedIDs ? [...selectedIDs] : null, site_base: prefix, review_only: null, visual_approval: 'pending_human_inspection',
  profile: staticOnly ? 'static-only' : forceFallback ? 'forced-webgl-fallback' : allowFallback ? 'allow-webgl-fallback' : 'strict-gpu',
  static_routes: [], checks: [], models: [], screenshots: [], page_errors: [], resource_errors: [],
  gpu: { status: 'not-run', fallback_models: [], rendered_models: [] },
};
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.glb': 'model/gltf-binary', '.zip': 'application/zip', '.txt': 'text/plain; charset=utf-8' };
// Real static hosting semantics: directories resolve to their own index.html.
// Unknown paths get a 404, never an SPA fallback that could hide broken deep links.
const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url, 'http://localhost');
    if (!url.pathname.startsWith(prefix)) { response.writeHead(404).end(); return; }
    const relative = decodeURIComponent(url.pathname.slice(prefix.length));
    let path = resolve(root, relative || 'index.html');
    if (path !== root && !path.startsWith(root + sep)) { response.writeHead(403).end(); return; }
    if ((await stat(path)).isDirectory()) path = resolve(path, 'index.html');
    const bytes = await readFile(path);
    response.writeHead(200, { 'Content-Type': mime[extname(path)] || 'application/octet-stream', 'Content-Length': bytes.length });
    response.end(request.method === 'HEAD' ? undefined : bytes);
  } catch { response.writeHead(404).end(); }
});
let browser, currentPage, baseURL, manifest;
const urlFor = (route = {}) => new URL(routeHref(route, prefix), baseURL).href;
const assetURL = path => new URL(prefix + path, baseURL).href;
const nameOf = (asset, lang = 'en') => typeof asset.name === 'string' ? asset.name : asset.name[lang === 'zh-CN' ? 'zh' : 'en'] || asset.name.en;
const cards = page => page.locator('#grid .asset-card[data-id]');
const cardIDs = page => cards(page).evaluateAll(elements => elements.map(element => element.dataset.id));
const gpu = page => page.evaluate(() => ({ ...window.__vaultGPU }));
const check = description => report.checks.push(description);
const attr = (tag, name) => tag.match(new RegExp(`\\b${name}\\s*=\\s*(["'])(.*?)\\1`, 'i'))?.[2];
const tags = (html, tag) => [...html.matchAll(new RegExp(`<${tag}\\b[^>]*>`, 'gi'))].map(match => match[0]);
const meta = (html, name) => tags(html, 'meta').find(tag => attr(tag, 'name') === name || attr(tag, 'property') === name);
const link = (html, rel, language) => tags(html, 'link').find(tag => attr(tag, 'rel') === rel && (!language || attr(tag, 'hreflang') === language));

async function screenshot(page, name) {
  // Full-page screenshots do not automatically scroll lazy thumbnails into view.
  // Exercise their real scroll loading before recording an all-card catalog image.
  if(name.startsWith('catalog-')) {
    const position=await page.evaluate(()=>({x:scrollX,y:scrollY}));
    for(const image of await page.locator('#grid .asset-card .asset-image img').all()) {
      await image.scrollIntoViewIfNeeded();
      await image.evaluate(img=>img.decode());
      assert(await image.evaluate(img=>img.complete&&img.naturalWidth>0),'Every scrolled catalog poster must decode');
    }
    await page.evaluate(p=>scrollTo(p.x,p.y),position);
  }
  await page.screenshot({ path: resolve(output, `${name}.png`), fullPage: !await page.locator('#viewer-dialog').isVisible(), animations: 'disabled' });
  report.screenshots.push(`${name}.png`);
}
function observe(page, label) {
  currentPage = page;
  page.on('pageerror', error => report.page_errors.push(`${label}: ${error.message}`));
  page.on('response', response => {
    if (response.status() >= 400 && !page.__intentionalFailure) report.resource_errors.push(`${label}: ${response.status()} ${response.url()}`);
  });
}
async function newContext(options = {}) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce', ...options });
  if (forceFallback && options.javaScriptEnabled !== false) {
    await context.addInitScript(() => {
      const original = HTMLCanvasElement.prototype.getContext;
      HTMLCanvasElement.prototype.getContext = function (type, ...args) {
        return /^webgl2?$|^experimental-webgl$/.test(type) ? null : original.call(this, type, ...args);
      };
    });
  }
  return context;
}
async function waitCatalog(page, expected) {
  await page.locator('#collection').waitFor({ state: 'visible' });
  await page.waitForFunction(() => document.querySelector('#grid')?.getAttribute('aria-busy') === 'false');
  if (expected) await page.waitForFunction(ids => JSON.stringify([...document.querySelectorAll('#grid .asset-card')].map(card => card.dataset.id)) === JSON.stringify(ids), expected);
}
async function selectFacet(page, selector, value) {
  if (!await page.locator(selector).isVisible()) await page.locator('.catalog-refine summary').click();
  await page.locator(selector).selectOption(value);
}
async function search(page, value) {
  if (!await page.locator('#search').isVisible()) await page.locator('#search-trigger').click();
  await page.locator('#search').fill(value);
  await page.waitForURL(url => (url.searchParams.get('q') || '') === value.trim());
  await waitCatalog(page);
}
async function waitModel(page, id) {
  await page.locator('#viewer-dialog').waitFor({ state: 'visible' });
  await page.waitForURL(url => url.pathname.endsWith(`/models/${id}/`));
  await page.waitForFunction(() => ['ready', 'error'].includes(document.querySelector('#canvas-host')?.dataset.modelState), null, { timeout: 30000 });
  const state = await page.locator('#canvas-host').getAttribute('data-model-state');
  if (state === 'ready') {
    assert.equal(forceFallback, false, 'The forced fallback profile must not report a successful WebGL renderer');
    assert.equal(await page.locator('#canvas-host .model-canvas').count(), 1);
    assert(Number(await page.locator('#canvas-host').getAttribute('data-render-triangles')) > 0, 'A ready model must draw real triangles');
    if (!report.gpu.rendered_models.includes(id)) report.gpu.rendered_models.push(id);
  } else {
    assert(allowFallback, `${id}: WebGL failed; strict GPU QA does not accept preview-only coverage`);
    const preview = page.locator('#canvas-host img');
    assert(await preview.isVisible(), 'Unsupported WebGL must retain a visible actual model preview');
    await preview.evaluate(image => image.decode());
    assert(await preview.evaluate(image => image.naturalWidth > 0));
    assert((await page.locator('#viewer-status').textContent()).trim(), 'Fallback must explain the unavailable 3D view');
    assert.equal((await gpu(page)).liveScenes, 0, 'Failed WebGL must release its parsed scene');
    if (!report.gpu.fallback_models.includes(id)) report.gpu.fallback_models.push(id);
  }
  return state;
}
async function waitClosed(page) {
  await page.locator('#viewer-dialog').waitFor({ state: 'hidden' });
  await page.waitForFunction(() => !document.querySelector('.stage-flight') && (!window.__vaultGPU || (window.__vaultGPU.liveScenes === 0 && window.__vaultGPU.activeRequests === 0 && window.__vaultGPU.rafPending === 0)));
  assert.equal(await page.locator('.model-canvas').count(), 0, 'Close must detach the shared WebGL canvas');
  assert.equal(await page.locator('.model-preview-snapshot,.stage-flight,.return-composite').count(),0,'Completed close leaves only the canonical poster, with no retained snapshot or live return flight');
  assert.equal(await page.evaluate(()=>window.__vaultPreview?.activeId??null),null,'Completed close releases active card inspection');
}
async function closeModel(page) { await page.locator('#close').click(); if(wheelBuild){await page.waitForFunction(()=>window.__gallery?.models.length>0,null,{timeout:45000});assert.equal(await page.locator('#viewer-dialog,.model-canvas,.stage-flight,.return-composite').count(),0);}else await waitClosed(page); }

async function staticChecks() {
  const uniqueTitles = new Set();
  for (const lang of ['en', 'zh-CN']) {
    const routes = [{ type: 'home', lang }, { type: 'models', lang }, { type: 'about', lang }, ...manifest.assets.map(asset => ({ type: 'detail', lang, id: asset.id }))];
    for (const route of routes) {
      const response = await fetch(urlFor(route));
      assert.equal(response.status, 200, `Static route missing: ${response.url}`);
      assert(response.headers.get('content-type').includes('text/html'));
      const html = await response.text();
      assert.match(html, new RegExp(`<html\\b[^>]*lang=["']${lang}["']`), `Wrong HTML language: ${response.url}`);
      const title = html.match(/<title>([\s\S]*?)<\/title>/i)?.[1];
      assert(title?.trim() && !uniqueTitles.has(title), `Missing/duplicate route title: ${response.url}`);
      uniqueTitles.add(title);
      assert(attr(meta(html, 'description') || '', 'content')?.trim(), `Missing description: ${response.url}`);
      const canonical = attr(link(html, 'canonical') || '', 'href');
      assert(canonical && new URL(canonical, baseURL).pathname === new URL(response.url).pathname, `Canonical must identify its real route: ${response.url}`);
      for (const language of ['en', 'zh-CN']) {
        const alternate = attr(link(html, 'alternate', language) || '', 'href');
        assert(alternate && new URL(alternate, baseURL).pathname === new URL(urlFor({ ...route, lang: language })).pathname, `Missing language alternate: ${response.url}`);
      }
      assert(attr(meta(html, 'og:title') || '', 'content'), `Missing Open Graph title: ${response.url}`);
      assert(attr(meta(html, 'og:image') || '', 'content'), `Missing Open Graph image: ${response.url}`);
      const structured = [...html.matchAll(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)].map(match => JSON.parse(match[1]));
      if (route.type === 'detail') assert(structured.length > 0, `Missing detail JSON-LD: ${response.url}`);
      assert.match(html, /id=["']static-route-content["']/, `No-JS route content missing: ${response.url}`);
      if (route.type === 'detail') {
        const asset = manifest.assets.find(item => item.id === route.id);
        for (const key of ['glb', 'blend', 'bundle', 'credits']) assert(html.includes(prefix + asset.downloads[key]), `No-JS ${key} link missing: ${asset.id}`);
        assert.match(html, /data-enhance-model/, 'A static detail needs an optional 3D enhancement');
      }
      report.static_routes.push({ path: new URL(response.url).pathname, status: 'pass', language: lang });
    }
  }
  for (const asset of manifest.assets) {
    for (const kind of ['glb', 'blend', 'bundle', 'credits']) {
      const path = asset.downloads[kind], response = await fetch(assetURL(path));
      assert.equal(response.status, 200, `${asset.id} ${kind} missing`);
      const bytes = new Uint8Array(await response.arrayBuffer());
      assert(bytes.length > 0, `${asset.id} ${kind} empty`);
      if (asset.file_sizes[kind] !== undefined) assert.equal(bytes.length, asset.file_sizes[kind], `${asset.id} ${kind} size must match delivered bytes`);
      if (kind === 'glb') assert.equal(new TextDecoder().decode(bytes.slice(0, 4)), 'glTF');
      if (kind === 'bundle') assert.deepEqual([...bytes.slice(0, 2)], [0x50, 0x4b], 'Bundle must be a real ZIP');
      if (kind === 'credits') {
        const text = new TextDecoder().decode(bytes);
        assert.match(text, /https:\/\/creativecommons\.org\/licenses\/by\/4\.0\//);
        assert.match(text, /Leon Made This|s010s/);
      }
    }
  }
  assert.equal((await fetch(new URL(prefix + 'models/no-such-model/', baseURL))).status, 404, 'The test server must not silently serve the home page for missing model routes');
  assert.equal((await fetch(new URL('/outside-site-prefix/', baseURL))).status, 404);
  check('Real static home, catalog, about and every detail route: bilingual metadata, canonical, hreflang, Open Graph and detail JSON-LD');
  check('Every GLB, Blender source, ZIP and CREDITS file exists; stated byte sizes match actual download bytes');
}

async function noJavaScriptChecks() {
  const context = await newContext({ javaScriptEnabled: false });
  const page = await context.newPage(); observe(page, 'No-JS');
  try {
    for (const lang of ['en', 'zh-CN']) {
      const content = page.locator('#static-route-content'), detailLinks = [];
      const pages = Math.max(1, Math.ceil(manifest.assets.length / CATALOG_PAGE_SIZE));
      for (let index = 0; index < pages; index++) {
        await page.goto(urlFor({ type: 'models', lang, page: index }));
        assert(await (wheelBuild?content.locator('.vault-header'):content).isVisible(), 'No-JS catalog must remain readable');
        const links = await content.locator(wheelBuild?'a.slot[href]':'a.static-card').evaluateAll(nodes => nodes.map(node => node.href));
        assert.equal(links.length, wheelBuild?manifest.assets.length:manifest.assets.slice(index * CATALOG_PAGE_SIZE, (index + 1) * CATALOG_PAGE_SIZE).length);
        assert.equal(new Set(links).size,links.length,'Each native document links every model exactly once');
        if(wheelBuild){
          const selected=(!index&&manifest.assets.find(asset=>asset.id==='cooperoceras'))||manifest.assets[index*CATALOG_PAGE_SIZE];
          assert.equal(await content.locator('.slot[data-selected=true]').getAttribute('data-id'),selected.id,'Page routes retain their initial wheel selection');
        }
        if(!wheelBuild||index===0)detailLinks.push(...links);
        for (const [rel, target] of [['prev', index - 1], ['next', index + 1]]) {
          const navigation = content.locator(`${wheelBuild?'.startup-pagination':'.static-pagination'} a[rel="${rel}"]`);
          if (target >= 0 && target < pages) {
            assert.equal(await navigation.count(), 1, 'No-JS pagination must expose adjacent pages');
            assert.equal(await navigation.evaluate(node => node.href), urlFor({type:'models',lang,page:target}));
          } else assert.equal(await navigation.count(), 0);
        }
        assert.equal(await page.locator('canvas').count(), 0);
      }
      assert.equal(new Set(detailLinks).size, detailLinks.length, 'No duplicated No-JS catalog entries');
      assert.deepEqual(detailLinks.sort(), manifest.assets.map(asset => urlFor({type:'detail',lang,id:asset.id})).sort(), 'No-JS catalog must expose every actual review asset across all reachable pages');
      await page.goto(urlFor({ type: 'detail', lang, id: manifest.assets[0].id }));
      assert(await content.isVisible());
      assert((await content.locator('h1').textContent()).includes(nameOf(manifest.assets[0], lang)));
      assert(await content.locator('a[href$=".glb"]').isVisible());
      assert(await content.locator('a[href$=".blend"]').isVisible());
      for (const colorScheme of ['light', 'dark']) {
        await page.emulateMedia({ colorScheme });
        const contrast = await content.locator('.static-specs dt').first().evaluate(node => {
          const rgb = color => (color.match(/[\d.]+/g) || []).map(Number);
          const foreground = rgb(getComputedStyle(node).color);
          let background = [255, 255, 255], ancestor = node;
          while (ancestor) {
            const color = rgb(getComputedStyle(ancestor).backgroundColor);
            if (color.length >= 3 && (color[3] === undefined || color[3] === 1)) { background = color; break; }
            ancestor = ancestor.parentElement;
          }
          const opacity = Number(getComputedStyle(node).opacity);
          const blended = foreground.slice(0, 3).map((value, i) => value * opacity + background[i] * (1 - opacity));
          const luminance = values => values.slice(0, 3).map(value => value / 255).map(value => value <= .04045 ? value / 12.92 : ((value + .055) / 1.055) ** 2.4).reduce((sum, value, i) => sum + value * [.2126, .7152, .0722][i], 0);
          const a = luminance(blended), b = luminance(background);
          return (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
        });
        assert(contrast >= 4.5, `${lang} no-JS ${colorScheme} specification labels need at least 4.5:1 text contrast; got ${contrast}`);
      }
      await screenshot(page, `no-js-detail-${lang}`);
    }
    check('JavaScript-disabled catalog and detail remain visible with working file links in English and Chinese; static specification labels retain at least 4.5:1 contrast');
  } catch(error) { report.failure_diagnostics={gpu:await gpu(page).catch(()=>null),canvas:await page.locator('canvas').count(),url:page.url()}; await screenshot(page, 'failure').catch(()=>{}); throw error; } finally { await context.close(); }
}

async function navigationChecks() {
  const context = await newContext();
  const page = await context.newPage(); observe(page, 'Navigation');
  try {
    await page.goto(urlFor());
    await page.locator('#home-page').waitFor({ state: 'visible' });
    assert.equal(await page.locator('canvas').count(), 0, 'Homepage must not eagerly create a WebGL renderer');
    assert.equal(await page.locator('#replay-entrance').count(), 0, 'Replay control must not reappear in the redesigned UI');
    await page.locator('.primary-nav [data-route="catalog"]').click();
    await page.waitForURL(url => url.pathname === routeHref({ type: 'models' }, prefix));
    await waitCatalog(page);
    assert.equal(await cards(page).count(), Math.min(CATALOG_PAGE_SIZE, manifest.assets.length));
    assert(await page.locator('#grid').isVisible(), 'Grid is the global default');
    assert.equal(await page.locator('.catalog-modes').isVisible(), false, 'Global catalog must not offer a map without a small selected pack');
    for (const element of await cards(page).all()) {
      assert.equal(await element.evaluate(node => node.tagName), 'A');
      const id = await element.getAttribute('data-id');
      assert.equal(new URL(await element.getAttribute('href'), baseURL).pathname, routeHref({ type: 'detail', id }, prefix));
    }
    const trigger = page.locator('#search-trigger');
    assert.equal(await trigger.getAttribute('aria-expanded'), 'false');
    await trigger.focus(); await page.keyboard.press('Enter');
    assert.equal(await trigger.getAttribute('aria-expanded'), 'true');
    assert.equal(await page.locator('#search').evaluate(node => node === document.activeElement), true);
    await page.keyboard.press('Escape');
    assert.equal(await trigger.getAttribute('aria-expanded'), 'false');
    await page.keyboard.press('/');
    assert.equal(await page.locator('#search').evaluate(node => node === document.activeElement), true);
    await search(page, 'THIS_DOES_NOT_EXIST');
    await page.waitForFunction(() => document.querySelectorAll('#grid .asset-card').length === 0);
    assert((await page.locator('#grid').textContent()).trim(), 'Empty results need useful text');
    await search(page, '');
    const category = manifest.assets.reduce((map, asset) => map.set(asset.category, (map.get(asset.category) || 0) + 1), new Map());
    const chosen = [...category].sort((a, b) => b[1] - a[1])[0][0];
    await page.locator(`[data-category="${chosen}"]`).click();
    await page.waitForURL(url => url.searchParams.get('category') === chosen);
    await waitCatalog(page);
    assert.equal(await page.locator(`[data-category="${chosen}"]`).getAttribute('aria-pressed'), 'true');
    const firstAsset = manifest.assets.find(asset => asset.category === chosen);
    const membership = catalogMembership(firstAsset);
    await selectFacet(page, '#world-filter', membership.worlds[0]);
    await selectFacet(page, '#pack-filter', membership.packs[0]);
    await page.locator('#sort').selectOption('triangles-desc');
    await search(page, chosen);
    await page.waitForURL(url => url.searchParams.get('world') === membership.worlds[0] && url.searchParams.get('pack') === membership.packs[0] && url.searchParams.get('sort') === 'triangles-desc');
    await waitCatalog(page);
    const expected = manifest.assets.filter(asset => asset.category === chosen && catalogMembership(asset).worlds.includes(membership.worlds[0]) && catalogMembership(asset).packs.includes(membership.packs[0])).sort((a, b) => b.triangles - a.triangles || nameOf(a).localeCompare(nameOf(b), 'en', { numeric: true })).map(asset => asset.id);
    await waitCatalog(page, expected);
    assert(await page.locator('.catalog-modes').isVisible(), 'A selected pack of at most 30 models may offer its map');
    const sourceURL = page.url();
    const sourceCard = cards(page).first();
    const id = await sourceCard.getAttribute('data-id');
    await sourceCard.scrollIntoViewIfNeeded(); await sourceCard.focus();
    const sourceScroll = await page.evaluate(() => scrollY);
    await page.keyboard.press('Enter');
    await waitModel(page, id);
    const dialog = page.locator('#viewer-dialog');
    assert.equal(await dialog.getAttribute('aria-labelledby'), 'asset-title');
    for (let i = 0; i < 24; i++) {
      await page.keyboard.press('Tab');
      assert(await dialog.evaluate(node => node.contains(document.activeElement)), 'Tab focus must stay in the modal');
    }
    await page.goBack(); await waitClosed(page); await waitCatalog(page, expected);
    assert.equal(page.url(), sourceURL, 'Back restores the exact query/filter/sort route');
    assert(Math.abs(await page.evaluate(() => scrollY) - sourceScroll) <= 4, 'Back restores catalog scroll');
    assert.equal(await page.evaluate(() => document.activeElement?.dataset.id), id, 'Back restores focus to the originating model card');
    await page.goForward(); await waitModel(page, id);
    await page.locator('#close').focus();
    if (expected.length > 1) {
      const next = page.locator('#next-model');
      assert.equal(await next.evaluate(node => node.tagName), 'A');
      const nextURL = new URL(await next.getAttribute('href'), page.url());
      await page.keyboard.press('ArrowRight');
      const nextID = nextURL.pathname.split('/').filter(Boolean).at(-1);
      await waitModel(page, nextID);
      assert.equal(new URL(page.url()).pathname, nextURL.pathname, 'ArrowRight outside canvas changes models in the active result set');
      await page.locator('#close').focus(); await page.keyboard.press('ArrowLeft'); await waitModel(page, id);
    }
    const state = await page.locator('#canvas-host').getAttribute('data-model-state');
    if (state === 'ready') {
      const currentURL = page.url(), before = (await gpu(page)).renderedFrames;
      await page.locator('#canvas-host').focus(); await page.keyboard.press('ArrowRight');
      await page.waitForFunction(frames => window.__vaultGPU.renderedFrames > frames, before);
      assert.equal(page.url(), currentURL, 'Canvas arrow keys orbit without selecting another asset');
    }
    await page.locator('#related-models a').first().waitFor({ state: 'visible' });
    const related = await page.locator('#related-models a').evaluateAll(links => links.map(anchor => ({ href: anchor.href, id: anchor.dataset.id })));
    assert(related.length > 0, 'Detail must link to actual same-pack models');
    for (const item of related) {
      const relatedID = item.id || new URL(item.href).pathname.split('/').filter(Boolean).at(-1);
      const asset = manifest.assets.find(asset => asset.id === relatedID);
      assert(asset && relatedID !== id && catalogMembership(asset).packs.some(pack => membership.packs.includes(pack)), 'Related cards must be real same-pack assets');
    }
    await page.keyboard.press('Escape'); await waitClosed(page);
    assert.equal(page.url(), sourceURL);
    await page.reload(); await waitCatalog(page, expected);
    assert.equal(await page.locator('#search').inputValue(), chosen);
    assert.equal(await page.locator('#world-filter').inputValue(), membership.worlds[0]);
    assert.equal(await page.locator('#pack-filter').inputValue(), membership.packs[0]);
    assert.equal(await page.locator('#sort').inputValue(), 'triangles-desc');
    await page.locator('.primary-nav [data-route="about"]').click();
    await page.locator('#about-page').waitFor({ state: 'visible' }); await page.reload();
    assert(await page.locator('#about-page').isVisible());
    await page.goto(urlFor({ type: 'detail', id }));
    const directURL = page.url();
    await waitModel(page, id);
    assert.equal(page.url(), directURL, 'A direct detail route automatically starts real 3D');
    await closeModel(page); await waitCatalog(page);
    assert(new URL(page.url()).pathname.endsWith('/models/'), 'Closing a direct detail returns to the catalog');
    check('Semantic links, compact search keyboard control, query/category/world/pack/sort URL persistence and real About route');
    check('Back/Forward/Close/Escape preserve catalog results, scroll and focus; direct detail automatically loads real 3D');
    check('Modal focus trap, adjacent-model arrows outside canvas, canvas orbit arrows and actual same-pack related links');
  } catch(error) { report.failure_diagnostics={gpu:await gpu(page).catch(()=>null),canvas:await page.locator('canvas').count(),url:page.url()}; await screenshot(page, 'failure').catch(()=>{}); throw error; } finally { await context.close(); }
}

async function actualModelChecks() {
  const context = await newContext();
  const page = await context.newPage(); observe(page, 'Actual models');
  try {
    if(!wheelBuild){await page.goto(urlFor({ type: 'models' })); await waitCatalog(page);}
    const selected = manifest.assets.filter(asset => !selectedIDs || selectedIDs.has(asset.id));
    assert(selected.length > 0 && (!selectedIDs || selected.length === selectedIDs.size), 'All selected models must exist');
    for (const asset of selected) {
      // Each real model must remain discoverable when the catalog spans pages.
      await page.goto(urlFor({ type: 'models' }) + '?q=' + encodeURIComponent(asset.id));
      if(wheelBuild){
        await page.waitForFunction(()=>window.__gallery?.models.length>0,null,{timeout:45000});
        assert((await page.evaluate(()=>window.__gallery.state.results.map(a=>a.id))).includes(asset.id),'Every model remains discoverable in the full wheel catalog');
        await page.locator(`#slots [data-id="${asset.id}"]`).click();
        await page.waitForFunction(id=>document.querySelector('#detail')?.dataset.modelId===id&&['ready','fallback'].includes(document.querySelector('#detail').dataset.state),asset.id,{timeout:45000});
        const inline=await page.locator('#detail').getAttribute('data-state');
        if(forceFallback)assert.equal(inline,'fallback');else if(!allowFallback)assert.equal(inline,'ready',asset.id+': inline gallery must render actual GLB');
        if(inline==='ready')assert.equal(await page.evaluate(()=>window.__gallery.renderer.stats.detailFirstFrameId),asset.id);
        assert.equal(await page.locator('#download').getAttribute('href'),assetURL(asset.glb));
        // The independent canonical route retains its original detailed viewer,
        // wireframe, metric grid, theme continuity and download acceptance below.
        await page.goto(urlFor({type:'detail',id:asset.id}));
      }else{await waitCatalog(page);await page.locator(`#grid .asset-card[data-id="${asset.id}"]`).click();}
      const state = await waitModel(page, asset.id);
      const downloads = page.locator('#downloads');
      for (const kind of ['glb', 'blend', 'bundle']) {
        const download = downloads.locator(`a[href$="${asset.downloads[kind]}"]`);
        assert.equal(await download.count(), 1, `${asset.id} needs its ${kind} download`);
        assert(await download.isVisible());
        assert(await download.getAttribute('download') !== null, `${kind} should initiate a file download`);
        if (kind !== 'credits') assert.match(await download.textContent(), /\d.*(?:B|KB|MB|GB|bytes|字节)/i, `${kind} must display a real file size`);
      }
      assert(await page.locator('#copy-attribution').isVisible(), 'Attribution must remain readily copyable');
      const [download] = await Promise.all([
        page.waitForEvent('download'),
        downloads.locator('a[href$=".glb"]').click(),
      ]);
      assert(download.suggestedFilename().endsWith('.glb'));
      const announcement = (await page.locator('#announcement').textContent()).trim();
      assert.match(announcement, /request|start|initiated|请求|开始/i, 'Download feedback reports initiation');
      assert.doesNotMatch(announcement, /download(?: is| has)? (?:complete|finished)|successfully saved|下载(?:已)?完成|已保存/i, 'Click cannot prove the browser completed or saved a download');
      const modelChecks = ['Actual preview', 'GLB, Blender, ZIP and attribution download links', 'Download initiated, not falsely reported complete'];
      if (state === 'ready') {
        const before = await gpu(page);
        assert.equal(before.rendererCreations, 1, 'The document must reuse one renderer');
        assert.equal(before.liveScenes, 1); assert.equal(before.peakRequests, 1);
        assert(before.cacheEntries <= 3 && before.cacheBytes <= 24 * 1024 * 1024);
        await page.locator('#wireframe').click();
        assert.equal(await page.locator('#wireframe').getAttribute('aria-pressed'), 'true');
        await page.waitForFunction(() => Number(document.querySelector('#canvas-host').dataset.renderLines) > 0);
        await page.locator('#wireframe').click();
        const scale = page.locator('#scale-reference');
        assert(await scale.isEnabled(), `${asset.id} has verified metric metadata and must offer a scale reference`);
        await scale.click();
        assert.equal(await scale.getAttribute('aria-pressed'), 'true');
        const reference = await gpu(page);
        assert.equal(reference.referenceObjects, 1); assert.equal(reference.referenceGeometries, 1); assert.equal(reference.referenceMaterials, 1);
        assert.match(await page.locator('#scale-status').textContent(), /\d.*(?:m|米)/, 'Scale reference must state authored metric spacing');
        await page.locator('#canvas-host').focus(); await page.keyboard.press('+'); await page.keyboard.press('ArrowLeft');
        await page.locator('#reset').click();
        assert.equal(await scale.getAttribute('aria-pressed'), 'true', 'Reset changes the camera, not the user’s scale-reference choice');
        await scale.click();
        assert.equal((await gpu(page)).referenceObjects, 0); assert((await gpu(page)).disposedReferences > 0);
        const canvas = await page.locator('#canvas-host .model-canvas').elementHandle();
        const diagnostics = await page.evaluateHandle(() => window.__vaultGPU);
        const originalTheme = await page.locator('html').getAttribute('data-theme');
        await page.locator('#viewer-dialog [data-theme-toggle]').click();
        await page.waitForFunction(theme => document.documentElement.dataset.theme !== theme, originalTheme);
        assert(await canvas.evaluate(node => node === document.querySelector('#canvas-host .model-canvas')), 'Theme toggle must retain the same canvas');
        assert(await diagnostics.evaluate(object => object === window.__vaultGPU), 'Theme toggle must retain the same renderer');
        assert.equal((await gpu(page)).liveScenes, 1);
        assert.equal((await gpu(page)).rendererCreations, 1);
        modelChecks.push('Real GLTFLoader/WebGL triangles', 'Wireframe lines', 'Metric reference resources and disposal', 'Orbit, zoom, reset', 'Theme preserves live model and renderer');
      }
      await screenshot(page, `model-${asset.id}-${state}`);
      await closeModel(page);
      if(wheelBuild){
        await page.waitForFunction(()=>window.__gallery?.models.length>0,null,{timeout:45000});
        assert.equal(await page.locator('#viewer-dialog,.model-canvas,.stage-flight,.return-composite').count(),0,'Closing the independent detail disposes its entire document and legacy stage');
        assert((await page.locator('canvas.preview-renderer').count())<=1,'The new gallery owns at most one renderer');
        modelChecks.push('Independent detail closes into the new isolated gallery document');
      }else{
        const stats = await gpu(page);
        assert.equal(stats.liveScenes, 0); assert.equal(stats.activeRequests, 0); assert.equal(stats.rafPending, 0);
        assert.equal(stats.referenceObjects, 0); assert.equal(stats.referenceGeometries, 0); assert.equal(stats.referenceMaterials, 0);
      }
      report.models.push({ id: asset.id, glb_sha256: asset.sha256?.glb || null, status: state === 'ready' ? 'gpu-pass' : 'fallback-only', checks: modelChecks });
    }
    check('All actual review assets: downloads, accessible fallback or strict GPU, bounded one-renderer cache and scene cleanup');
  } catch(error) { report.failure_diagnostics={gpu:await gpu(page).catch(()=>null),canvas:await page.locator('canvas').count(),url:page.url()}; await screenshot(page, 'failure').catch(()=>{}); throw error; } finally { await context.close(); }
}

async function visualMatrixChecks() {
  for (const lang of ['en', 'zh-CN']) for (const theme of ['light', 'dark']) for (const touch of [false, true]) {
    const key = `${lang}-${theme}-${touch ? '390-touch' : 'desktop'}`;
    const context = await newContext({ colorScheme: theme, viewport: touch ? { width: 390, height: 844 } : { width: 1440, height: 1000 }, hasTouch: touch, isMobile: touch });
    const page = await context.newPage(); observe(page, key);
    try {
      await page.goto(urlFor({ lang }));
      await page.locator('#home-page').waitFor({ state: 'visible' });
      await page.locator('#home-page img').evaluateAll(images => Promise.all(images.filter(image => image.loading !== 'lazy').map(image => image.decode())));
      await page.waitForFunction(value => document.documentElement.dataset.theme === value, theme);
      assert.equal(await page.locator('html').getAttribute('lang'), lang);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${key} home horizontal overflow`);
      await screenshot(page, `home-${key}`);
      await page.locator('.primary-nav [data-route="catalog"]').click(); await waitCatalog(page);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${key} catalog horizontal overflow`);
      await screenshot(page, `catalog-${key}`);
      const card = cards(page).first(), id = await card.getAttribute('data-id');
      if (touch) await card.tap(); else await card.click();
      await waitModel(page, id);
      assert(await page.locator('#viewer-dialog').evaluate(element => element.scrollWidth <= element.clientWidth + 1), `${key} dialog horizontal overflow`);
      await screenshot(page, `detail-${key}`);
      if (touch) await page.locator('#close').tap(); else await page.locator('#close').click();
      await waitClosed(page);
      await page.locator('#language').click();
      const nextLang = lang === 'en' ? 'zh-CN' : 'en';
      await page.waitForFunction(value => document.documentElement.lang === value, nextLang);
      assert.equal(new URL(page.url()).pathname, routeHref({ type: 'models', lang: nextLang }, prefix), 'Language selection must update the shareable route');
      await page.reload(); await waitCatalog(page);
      assert.equal(await page.locator('html').getAttribute('lang'), nextLang);
      const original = await page.locator('html').getAttribute('data-theme');
      await page.locator('.topbar [data-theme-toggle]').click();
      await page.waitForFunction(value => document.documentElement.dataset.theme !== value, original);
      const chosen = await page.locator('html').getAttribute('data-theme');
      await page.reload(); await waitCatalog(page);
      assert.equal(await page.locator('html').getAttribute('data-theme'), chosen, 'Explicit theme survives reload');
    } catch(error) { report.failure_diagnostics={gpu:await gpu(page).catch(()=>null),canvas:await page.locator('canvas').count(),url:page.url()}; await screenshot(page, 'failure').catch(()=>{}); throw error; } finally { await context.close(); }
  }
  check('Screenshot matrix: English/Chinese × light/dark × desktop/390px touch-emulated Chromium; home/catalog/detail and no horizontal overflow');
  check('Language updates real routes and survives reload; theme follows initial scheme and explicit choice persists');
}

function buildSyntheticCatalog() {
  // Deliberately uneven facets and distant-shard names, using existing real files.
  // This data exists only in interception memory and is never written to production.
  const assets = Array.from({ length: 10000 }, (_, i) => ({
    ...manifest.assets[i % manifest.assets.length],
    id: `fixture-${String(i).padStart(5, '0')}`,
    name: { en: `Fixture ${String(i).padStart(5, '0')}`, zh: `测试资产 ${String(i).padStart(5, '0')}` },
    category: i < 6400 ? 'geology' : i < 8500 ? 'plants' : `uneven-${i % 37}`,
    collection: 'prehistoric', worlds: [`world-${i % 7}`], packs: [`pack-${Math.floor(i / 25)}`],
    triangles: i % 503 + 100,
  }));
  return { assets, catalog: createCatalog({ ...manifest, assets }) };
}
async function scaleChecks() {
  const { assets, catalog } = buildSyntheticCatalog();
  const context = await newContext();
  const page = await context.newPage(); observe(page, '10000 fixture');
  await page.route('**/assets/catalog.json', route => route.fulfill({ contentType: 'application/json', body: JSON.stringify(catalog.index) }));
  await page.route('**/assets/catalog/shards/*.json', route => {
    const key = 'assets/' + new URL(route.request().url()).pathname.split('/assets/')[1];
    assert(catalog.shards.has(key));
    return route.fulfill({ contentType: 'application/json', body: JSON.stringify(catalog.shards.get(key)) });
  });
  await page.route('**/assets/catalog/details/*.json', route => {
    const id = new URL(route.request().url()).pathname.split('/').pop().replace('.json', '');
    const asset = assets.find(asset => asset.id === id); assert(asset);
    return route.fulfill({ contentType: 'application/json', body: JSON.stringify(asset) });
  });
  try {
    await page.goto(urlFor({ type: 'models' }));
    await waitCatalog(page, assets.slice(0, 24).map(asset => asset.id));
    const nodes = await page.locator('*').count();
    assert(nodes < 1400, `10000-item DOM is not bounded: ${nodes}`);
    assert.equal(await cards(page).count(), 24);
    assert((await page.locator('#count').textContent()).replace(/[,\s]/g, '').includes('10000'));
    assert.equal(await page.locator('.catalog-modes').isVisible(), false);
    await cards(page).last().click(); await waitModel(page, 'fixture-00023');
    await page.locator('#next-model').waitFor({ state: 'visible' });
    await page.locator('#close').focus(); await page.keyboard.press('ArrowRight');
    await waitModel(page, 'fixture-00024');
    await closeModel(page); await waitCatalog(page, assets.slice(0, 24).map(asset => asset.id));
    assert.equal(await page.evaluate(() => document.activeElement?.dataset.id), 'fixture-00023', 'Cross-page adjacent navigation still restores the original card');
    await selectFacet(page, '#poly-filter', '500');
    await page.waitForURL(url => url.searchParams.get('maxTriangles') === '500');
    await waitCatalog(page, assets.filter(asset => asset.triangles <= 500).slice(0, 24).map(asset => asset.id));
    await selectFacet(page, '#poly-filter', '0'); await waitCatalog(page, assets.slice(0, 24).map(asset => asset.id));
    await page.locator('#next-page').click();
    await page.waitForURL(url => url.pathname.endsWith('/models/page/2/'));
    await waitCatalog(page, assets.slice(24, 48).map(asset => asset.id));
    assert.match(await page.locator('#page-number').textContent(), /417/);
    await page.locator('#prev-page').click();
    await waitCatalog(page, assets.slice(0, 24).map(asset => asset.id));
    await search(page, 'Fixture 09999');
    await waitCatalog(page, ['fixture-09999']);
    await search(page, '');
    await page.locator('[data-category="uneven-13"]').click();
    await page.waitForURL(url => url.searchParams.get('category') === 'uneven-13');
    await selectFacet(page, '#world-filter', 'world-2');
    await page.locator('#sort').selectOption('triangles-desc');
    await page.waitForURL(url => url.searchParams.get('sort') === 'triangles-desc' && url.searchParams.get('world') === 'world-2');
    const expected = assets.filter(asset => asset.category === 'uneven-13' && asset.worlds.includes('world-2')).sort((a, b) => b.triangles - a.triangles || a.id.localeCompare(b.id));
    await waitCatalog(page, expected.slice(0, 24).map(asset => asset.id));
    assert(expected.length > 1);
    await page.locator('[data-category="all"]').click();
    await selectFacet(page, '#world-filter', 'all');
    await selectFacet(page, '#pack-filter', 'pack-399');
    await page.locator('#sort').selectOption('name');
    const packIDs = assets.slice(9975, 9999).map(asset => asset.id);
    await waitCatalog(page, packIDs);
    assert(await page.locator('.catalog-modes').isVisible(), 'A bounded 25-item pack can offer its map');
    await screenshot(page, 'scale-10000-filtered-pack');
    await page.locator('[data-mode="atlas"]').click();
    await page.waitForURL(url => url.searchParams.get('view') === 'map');
    await page.locator('.model-atlas .asset-card').first().waitFor({ state: 'visible' });
    const mapped = await page.locator('.model-atlas .asset-card').evaluateAll(nodes => nodes.map(node => node.dataset.id));
    assert(mapped.length > 0 && mapped.length <= 25 && mapped.every(id => assets.slice(9975).some(asset => asset.id === id)), 'Map must contain only the selected small pack');
    await screenshot(page, 'scale-10000-scoped-map');
    await page.locator('[data-mode="grid"]').click(); await waitCatalog(page, packIDs);
    await selectFacet(page, '#pack-filter', 'all');
    await waitCatalog(page, assets.slice(0, 24).map(asset => asset.id));
    assert.equal(await page.locator('.catalog-modes').isVisible(), false);
    if(await page.locator('.catalog-refine').getAttribute('open') !== null) await page.locator('.catalog-refine summary').click();
    await page.emulateMedia({ reducedMotion: 'no-preference' });
    for (let i = 0; i < 8; i++) { await cards(page).nth(i).hover(); await page.waitForTimeout(195); }
    await cards(page).nth(8).click(); await waitModel(page, 'fixture-00008');
    const stats = await gpu(page);
    assert.equal(stats.peakRequests, 1, 'Rapid hover must serialize/abort network requests');
    assert(stats.cacheEntries <= 3 && stats.cacheBytes <= 24 * 1024 * 1024);
    assert(stats.liveScenes <= 1); assert(stats.rendererCreations <= 1);
    if (!report.gpu.fallback_models.includes('fixture-00008')) assert.equal(stats.rendererCreations, 1);
    await closeModel(page);
    assert.equal((await gpu(page)).liveScenes, 0);
    report.scale = { metadata: assets.length, categories: catalog.index.categories.length, worlds: catalog.index.worlds.length, packs: catalog.index.packs.length, card_nodes: 24, dom_nodes: nodes, pages: 417, peak_glb_requests: stats.peakRequests, cache_entries: stats.cacheEntries, cache_bytes: stats.cacheBytes, renderer_creations: stats.rendererCreations };
    check('In-memory 10000-item fixture: uneven 39-category/7-world/400-pack facets, distant search, 417 pages and bounded DOM');
    check('Cross-page adjacent navigation restores its originating card; measured triangle filter and scoped pack map work');
    check('Intentional list hover and detail switching share one GLB request lane and renderer; completed close restores canonical posters with bounded bytes and zero live scenes');
  } catch(error) { report.failure_diagnostics={gpu:await gpu(page).catch(()=>null),canvas:await page.locator('canvas').count(),url:page.url()}; await screenshot(page, 'failure').catch(()=>{}); throw error; } finally { await context.close(); }
}

async function failureRecoveryChecks() {
  const context = await newContext();
  const page = await context.newPage(); observe(page, 'Failure recovery');
  try {
    page.__intentionalFailure = true;
    await page.route('**/assets/catalog.json', route => route.fulfill({ status: 503, contentType: 'text/plain', body: 'Intentional QA outage' }));
    await page.goto(urlFor({ type: 'models', lang: 'zh-CN' }));
    await page.locator('#retry').waitFor({ state: 'visible' });
    assert(await page.locator('#collection').isVisible());
    assert.equal(await cards(page).count(), 0);
    assert.match(await page.locator('#grid').textContent(), /不可用|失败|重试/);
    await page.unroute('**/assets/catalog.json');
    page.__intentionalFailure = false;
    await page.locator('#retry').click(); await waitCatalog(page);
    assert.equal(await cards(page).count(), Math.min(24, manifest.assets.length));
    check('Catalog failure remains visible and its retry recovers without a page refresh');
  } catch(error) { report.failure_diagnostics={gpu:await gpu(page).catch(()=>null),canvas:await page.locator('canvas').count(),url:page.url()}; await screenshot(page, 'failure').catch(()=>{}); throw error; } finally { await context.close(); }
}

await mkdir(output, { recursive: true });
try {
  manifest = JSON.parse(await readFile(resolve(root, 'assets/manifest.json'), 'utf8'));
  report.review_only = manifest.review_only === true;
  if (process.env.QA_REVIEW_ONLY === '1') assert(manifest.review_only, 'Review CI must only use a review-only manifest');
  assert(manifest.assets.length > 0, 'Acceptance requires real review assets');
  if (process.env.QA_REQUIRE_COUNT) assert.equal(manifest.assets.length, Number(process.env.QA_REQUIRE_COUNT));
  await new Promise((accept, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', accept); });
  baseURL = `http://127.0.0.1:${server.address().port}/`;
  await staticChecks();
  if (staticOnly) {
    report.status = 'static-only-pass';
    report.browser_status = 'not-run';
    console.log(`Static route and download checks passed (${report.static_routes.length} documents). Browser, accessibility, screenshots and GPU were NOT run.`);
  } else {
    try {
      browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
    } catch (error) {
      report.browser_status = 'blocked';
      throw error;
    }
    report.chromium_version = browser.version();
    if (reviewScope !== 'models') {
      await noJavaScriptChecks();
      if(wheelBuild){
        const groups=forceFallback?['fallback']:['routes','interaction','scroll','scale','modal','fallback'];
        const result=await runGalleryBrowserTests({groups,root,output:resolve(output,'approved-wheel'),baseURL:urlFor({type:'home'})});
        report.approved_wheel=result;
        check('Approved wheel route/search/filter/mobile/native-scroll matrix, real 10,000-record fixture and explicit fallback; retired grid/pack-map assumptions are not reported as measured');
      }else{
        await navigationChecks();await visualMatrixChecks();await scaleChecks();await failureRecoveryChecks();
      }
    }
    if (reviewScope !== 'matrix') await actualModelChecks();
    assert.deepEqual(report.page_errors, [], 'Unexpected browser exceptions');
    assert.deepEqual(report.resource_errors, [], 'Unexpected failed resource requests');
    report.browser_status = 'pass';
    report.gpu.status = forceFallback ? 'forced-fallback-not-gpu-accepted' : report.gpu.fallback_models.length ? 'fallback-only-or-partial' : 'pass';
    report.status = forceFallback || report.gpu.fallback_models.length ? 'pass-with-webgl-fallback' : 'pass';
    console.log(`${report.status}: scope=${reviewScope}; ${report.models.length} actual models; ${reviewScope === 'models' ? 'fixture not selected' : '10000 metadata fixture'}; ${report.static_routes.length} static routes. ${forceFallback || report.gpu.fallback_models.length ? 'GPU acceptance remains incomplete.' : 'Strict GPU acceptance passed.'} Screenshots still require human visual review.`);
  }
} catch (error) {
  report.status = report.browser_status === 'blocked' ? 'blocked-browser' : 'fail';
  report.error = error.stack || error.message;
  try { if (currentPage && !currentPage.isClosed()) await screenshot(currentPage, 'failure'); } catch {}
  console.error(error);
  process.exitCode = 1;
} finally {
  await writeFile(resolve(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  await browser?.close();
  if (server.listening) await new Promise(accept => server.close(accept));
}

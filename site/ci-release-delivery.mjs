/** Actual HTTP delivery checks of changed GLBs, posters and localized pages.
 * This checks deployed bytes; it does not repeat artistic or model acceptance.
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {mkdir, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';

const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const commit = value => { assert(/^[a-f0-9]{40}$/.test(value || ''), 'Full commit SHA required'); return value; };
function anchorTargets(html, pageURL) {
  // Ignore JSON-LD, script strings and comments: they are not download anchors.
  const markup = html.replace(/<!--[\s\S]*?-->|<(script|style)\b[^>]*>[\s\S]*?<\/\1\s*>/gi, '');
  const targets = [];
  for (const tag of markup.matchAll(/<a\b([^>]*)>/gi)) {
    const attribute = /(?:^|\s)href\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))/i.exec(tag[1]);
    if (!attribute) continue;
    const href = (attribute[1] ?? attribute[2] ?? attribute[3]).replace(/&amp;/gi, '&');
    try { targets.push(new URL(href, pageURL).href); } catch { /* Invalid href is not a delivery link. */ }
  }
  return targets;
}
function hasLocalizedHeading(html, name) {
  const markup = html.replace(/<!--[\s\S]*?-->|<(script|style)\b[^>]*>[\s\S]*?<\/\1\s*>/gi, '');
  return [...markup.matchAll(/<h1\b[^>]*>([\s\S]*?)<\/h1\s*>/gi)].some(match => match[1].replace(/<[^>]*>/g, '').trim() === escapeHTML(name));
}

export async function checkDelivery({baseURL, expectedSha, baseline, source, resources, fetcher = fetch, concurrency = 4}) {
  commit(expectedSha);
  assert(Number.isInteger(concurrency) && concurrency > 0 && concurrency <= 8);
  const base = new URL(baseURL);
  assert(['https:', 'http:'].includes(base.protocol) && !base.username && !base.password, 'Invalid site URL');
  if (!base.pathname.endsWith('/')) base.pathname += '/';
  const get = async path => {
    assert(typeof path === 'string' && !path.startsWith('/') && !path.includes('..') && !path.includes('\\'), 'Unsafe delivery path');
    const url = new URL(path, base);
    assert(url.origin === base.origin && url.pathname.startsWith(base.pathname), 'Delivery path escapes site');
    url.searchParams.set('deployment', expectedSha);
    const response = await fetcher(url, {signal: AbortSignal.timeout(60000), cache: 'no-store'});
    assert(response.ok, `${path}: HTTP ${response.status}`);
    return response;
  };
  const marker = await (await get('release-build.json')).json();
  assert.equal(marker.source_commit, expectedSha, 'Deployment not yet current');
  const live = await (await get('assets/manifest.json')).json();
  const gallery = await (await get('assets/gallery.json')).json();
  assert.deepEqual(live.assets.map(a => [a.id, a.glb, a.sha256.glb]), source.assets.map(a => [a.id, a.glb, a.sha256.glb]), 'Live catalog differs from pinned commit');
  assert.equal(marker.models, source.assets.length);
  assert.equal(gallery.assets.length, source.assets.length);
  const old = new Map(baseline.assets.map(a => [a.id, a.sha256.glb]));
  const selected = source.assets.filter(a => old.get(a.id) !== a.sha256.glb);
  assert(selected.length > 0, 'No changed models selected');
  const pins = new Map(resources.files.map(f => [f.path, f]));
  const display = new Map(gallery.assets.map(a => [a.id, a]));
  const report = {status: 'RUNNING', source_commit: expectedSha, started_at: new Date().toISOString(),
    scope: 'Actual HTTP GET bytes and localized HTML; no repeated model acceptance or browser/device interaction test.',
    total_catalog_ids: source.assets.length, selected_count: selected.length, models: []};
  const binary = async (path, expectedHash, expectedBytes) => {
    assert(/^[a-f0-9]{64}$/.test(expectedHash || ''), `Missing SHA: ${path}`);
    assert(Number.isInteger(expectedBytes) && expectedBytes > 0, `Missing size: ${path}`);
    const response = await get(path), bytes = Buffer.from(await response.arrayBuffer());
    const actual = {path, http_status: response.status, bytes: bytes.length, sha256: sha(bytes)};
    assert.equal(actual.sha256, expectedHash, `SHA mismatch: ${path}`);
    assert.equal(bytes.length, expectedBytes, `Size mismatch: ${path}`);
    return actual;
  };
  let next = 0;
  await Promise.all(Array.from({length: Math.min(concurrency, selected.length)}, async () => {
    while (next < selected.length) {
      const asset = selected[next++];
      const row = {id: asset.id, change: old.has(asset.id) ? 'replacement' : 'new', status: 'RUNNING', posters: [], pages: []};
      try {
        row.glb = await binary(asset.glb, asset.sha256.glb, asset.file_sizes.glb);
        const shown = display.get(asset.id);
        assert.equal(shown?.sha256.glb, asset.sha256.glb, 'Gallery GLB differs');
        for (const role of ['wheel', 'detail']) {
          const path = resources.posters[asset.id]?.[role], pin = pins.get(path);
          assert(pin, `Missing poster pin: ${asset.id}/${role}`);
          assert.equal(shown.galleryPosters[role], path, 'Gallery poster differs');
          row.posters.push({role, ...await binary(path, pin.sha256, pin.bytes)});
        }
        for (const [path, language] of [[`models/${asset.id}/`, 'en'], [`zh-CN/models/${asset.id}/`, 'zh']]) {
          const response = await get(path), html = await response.text();
          assert(hasLocalizedHeading(html, asset.name[language]), `Localized name missing: ${path}`);
          const targets = anchorTargets(html, new URL(path, base));
          assert(targets.includes(new URL(asset.glb, base).href), `GLB link missing: ${path}`);
          assert(targets.includes('https://creativecommons.org/licenses/by/4.0/'), `License link missing: ${path}`);
          row.pages.push({path, language, http_status: response.status, bytes: Buffer.byteLength(html), sha256: sha(html), checks: ['localized-name', 'selected-glb-link', 'CC-BY-4.0-link']});
        }
        row.status = 'PASS';
      } catch (error) { row.status = 'FAIL'; row.error = error.message; }
      report.models.push(row);
      console.log('DELIVERY_' + row.status, row.id, row.error || row.glb.sha256);
    }
  }));
  report.models.sort((a,b) => a.id.localeCompare(b.id));
  report.passed = report.models.filter(a => a.status === 'PASS').length;
  report.failed = report.models.length - report.passed;
  report.status = report.failed ? 'FAIL' : 'PASS';
  report.finished_at = new Date().toISOString();
  return report;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  let report;
  try {
    const expectedSha = commit(process.env.DEPLOYED_SHA), baselineSha = commit(process.env.DELIVERY_BASELINE_SHA);
    const pinned = async (revision, path) => {
      const response = await fetch(`https://raw.githubusercontent.com/s010s/lowpoly-vault/${revision}/${path}`, {signal: AbortSignal.timeout(60000)});
      assert(response.ok, `Pinned source HTTP ${response.status}: ${path}`);
      return response.json();
    };
    const [baseline, source, resources] = await Promise.all([pinned(baselineSha, 'assets/manifest.json'), pinned(expectedSha, 'assets/manifest.json'), pinned(expectedSha, 'site/public/gallery/resources.json')]);
    report = await checkDelivery({baseURL: process.env.SITE_URL, expectedSha, baseline, source, resources});
    report.baseline_commit = baselineSha;
  } catch (error) { report = {status: 'FAIL', error: error.message}; }
  await mkdir('qa/live-smoke', {recursive: true});
  await writeFile('qa/live-smoke/release-delivery.json', JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({status: report.status, selected: report.selected_count, passed: report.passed, failed: report.failed, error: report.error}));
  if (report.status !== 'PASS') process.exitCode = 1;
}

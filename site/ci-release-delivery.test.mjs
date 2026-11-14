import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {checkDelivery} from './ci-release-delivery.mjs';

const sha = value => createHash('sha256').update(value).digest('hex');
const expectedSha = 'a'.repeat(40);
function fixture({fault, stale = false, badPath = false} = {}) {
  const files = new Map(), rows = ['new-model', 'replacement'].map(id => {
    const glb = `assets/${id}.glb`, bytes = Buffer.from(id);
    files.set(glb, bytes);
    return {id, glb, name: {en: 'A & B', zh: '中文'}, sha256: {glb: sha(bytes)}, file_sizes: {glb: bytes.length}, galleryPosters: {wheel: `gallery/${id}-wheel.png`, detail: `gallery/${id}-detail.png`}};
  });
  const resources = {files: [], posters: {}};
  for (const asset of rows) {
    resources.posters[asset.id] = asset.galleryPosters;
    for (const path of Object.values(asset.galleryPosters)) {
      const bytes = Buffer.from(path); files.set(path, bytes);
      resources.files.push({path, bytes: bytes.length, sha256: sha(bytes)});
    }
    for (const [path, name] of [[`models/${asset.id}/`, 'A &amp; B'], [`zh-CN/models/${asset.id}/`, '中文']]) files.set(path, `<h1>${name}</h1><a href="/vault/${asset.glb}">model</a><a href="https://creativecommons.org/licenses/by/4.0/">License</a>`);
  }
  const unchanged = {id: 'unchanged', glb: 'same.glb', sha256: {glb: 'b'.repeat(64)}};
  const source = {assets: [...rows, unchanged]};
  const baseline = {assets: [{id: 'replacement', sha256: {glb: 'c'.repeat(64)}}, unchanged]};
  files.set('release-build.json', JSON.stringify({source_commit: stale ? 'd'.repeat(40) : expectedSha, models: 3}));
  files.set('assets/manifest.json', JSON.stringify(source));
  files.set('assets/gallery.json', JSON.stringify(source));
  if (badPath) rows[0].glb = 'https://elsewhere.invalid/model.glb';
  const requests = [];
  const fetcher = async url => {
    requests.push(String(url));
    assert.equal(url.origin, 'https://example.test');
    const path = url.pathname.replace('/vault/', '');
    const body = fault?.path === path ? fault.body : files.get(path);
    return new Response(body || 'missing', {status: body ? 200 : 404});
  };
  return {options: {baseURL: 'https://example.test/vault/', expectedSha, baseline, source, resources, fetcher}, requests};
}

test('reads changed model bytes, both posters and localized pages; skips identical versions', async () => {
  const {options, requests} = fixture();
  const report = await checkDelivery(options);
  assert.equal(report.status, 'PASS'); assert.equal(report.passed, 2);
  assert.deepEqual(report.models.map(r => r.change), ['new', 'replacement']);
  assert.equal(requests.length, 13); assert(!requests.some(path => path.includes('same.glb')));
  assert(report.models.every(r => r.glb.http_status === 200 && r.posters.length === 2 && r.pages.length === 2));
});

for (const [label, path, body] of [
  ['corrupt GLB', 'assets/new-model.glb', 'wrong'],
  ['corrupt poster', 'gallery/new-model-wheel.png', 'wrong'],
  ['wrong localized page', 'zh-CN/models/new-model/', '<h1>wrong</h1>'],
  ['missing download', 'models/new-model/', '<h1>A &amp; B</h1>'],
  ['JSON-LD without anchors', 'models/new-model/', '<h1>A &amp; B</h1><script type="application/ld+json">{"contentUrl":"assets/new-model.glb","license":"https://creativecommons.org/licenses/by/4.0/"}</script>'],
  ['incorrect href with correct visible text', 'models/new-model/', '<h1>A &amp; B</h1><a href="/vault/other.glb">assets/new-model.glb</a><a href="https://creativecommons.org/licenses/by/4.0/">License</a>'],
  ['license text without license anchor', 'models/new-model/', '<h1>A &amp; B</h1><a href="/vault/assets/new-model.glb">model</a>https://creativecommons.org/licenses/by/4.0/'],
  ['data-href instead of href', 'models/new-model/', '<h1>A &amp; B</h1><a data-href="/vault/assets/new-model.glb">model</a><a href="https://creativecommons.org/licenses/by/4.0/">License</a>'],
  ['correct metadata with wrong heading', 'models/new-model/', '<h1>Other model</h1><script type="application/ld+json">{"name":"A &amp; B"}</script><a href="/vault/assets/new-model.glb">model</a><a href="https://creativecommons.org/licenses/by/4.0/">License</a>'],
]) test(`detects ${label} and still checks the other asset`, async () => {
  const {options} = fixture({fault: {path, body}});
  const report = await checkDelivery(options);
  assert.equal(report.status, 'FAIL'); assert.equal(report.failed, 1); assert.equal(report.passed, 1);
  assert.equal(report.models.find(r => r.id === 'replacement').status, 'PASS');
});

test('rejects a stale deployment before accepting model downloads', async () => {
  const {options, requests} = fixture({stale: true});
  await assert.rejects(checkDelivery(options), /Deployment not yet current/);
  assert.equal(requests.length, 1);
});

test('blocks asset paths outside the site', async () => {
  const {options, requests} = fixture({badPath: true});
  // Keep the live catalog consistent so the path guard is exercised.
  options.fetcher = ((original) => async url => url.pathname.endsWith('assets/manifest.json') || url.pathname.endsWith('assets/gallery.json') ? new Response(JSON.stringify(options.source)) : original(url))(options.fetcher);
  const report = await checkDelivery(options);
  assert.equal(report.failed, 1);
  assert.match(report.models[0].error, /escapes site/);
  assert(!requests.some(url => url.includes('elsewhere.invalid')));
});

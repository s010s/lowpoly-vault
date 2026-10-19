import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { routeApplication } from './entry.js';
import { parseRoute, routeHref } from './routes.js';
import { writeStaticRoutes } from './static-routes.mjs';

for (const base of ['/', '/lowpoly-vault/', '/custom/deep/']) {
  for (const lang of ['en', 'zh-CN']) {
    for (const route of [
      { type: 'home' }, { type: 'about' },
      { type: 'models' }, { type: 'models', page: 7 },
      { type: 'detail', id: 'cooperoceras' },
    ]) {
      const pathname = routeHref({ ...route, lang }, base);
      const expected = route.type === 'models' ? 'gallery' : 'site';
      assert.equal(routeApplication(pathname, base), expected, pathname);
      assert.equal(routeApplication(pathname + 'index.html', base), expected, pathname);
      assert.equal(parseRoute(pathname, base).lang, lang);
    }
  }
}
assert.equal(routeApplication('/other/models/', '/lowpoly-vault/'), 'site');
assert.equal(routeApplication('/models/no-such-model/'), 'site');

// An existing home/about/detail document must never activate its legacy list.
const main = await readFile(new URL('./main.js', import.meta.url), 'utf8');
const navigation = main.match(/^function navigate\(view\).*$/m)?.[0];
assert(navigation, 'Legacy navigation entry point is present');
const calls = [];
const navigate = new Function('location', 'history', 'listURL', 'href', 'syncRoute',
  `${navigation};return navigate;`)(
  { assign: url => calls.push(['assign', url]) },
  { pushState: (...args) => calls.push(['pushState', ...args]) },
  () => '/lowpoly-vault/zh-CN/models/?q=fern&category=plants',
  type => `/lowpoly-vault/zh-CN/${type}/`,
  () => calls.push(['syncRoute']),
);
navigate('catalog');
assert.deepEqual(calls, [['assign', '/lowpoly-vault/zh-CN/models/?q=fern&category=plants']]);
calls.length = 0;
navigate('about');
assert.equal(calls[0][0], 'pushState');
assert.equal(calls[0][3], '/lowpoly-vault/zh-CN/about/');
assert.equal(calls[1][0], 'syncRoute');

const guard = main.slice(main.indexOf('async function syncRoute(){'), main.indexOf('  if(pendingRoute)'));
let reloads = 0;
const synchronize = new Function('parseRoute', 'location', 'siteRoot',
  `let index=null;${guard}};return syncRoute;`)(
  parseRoute, { pathname: '/lowpoly-vault/models/', reload: () => reloads++ }, '/lowpoly-vault/',
);
await synchronize();
assert.equal(reloads, 1, 'History crossing to the wheel reloads before the legacy app loads');

const sourceHTML = await readFile(new URL('./index.html', import.meta.url), 'utf8');
assert(sourceHTML.includes('src="/entry.js"'));
for(const svg of sourceHTML.matchAll(/<svg\b[^>]*>/g)){assert(/width="\d+"/.test(svg[0])&&/height="\d+"/.test(svg[0]),'Template SVGs have bounded intrinsic dimensions before CSS');assert(svg[0].includes('fill="none"'),'Template stroke icons do not become black polygons without CSS');}
assert(!sourceHTML.includes('src="/main.js"'));
const out = await mkdtemp(join(tmpdir(), 'vault-entry-routes-'));
try {
  const assets = Array.from({ length: 25 }, (_, i) => ({
    id: `model-${i}`, name: { en: `Model ${i}`, zh: `模型 ${i}` },
    description: { en: 'Original model', zh: '原创模型' }, category: 'plants',
    collection: 'prehistoric', preview: `assets/model-${i}/preview.webp`,
    glb: `assets/model-${i}/model.glb`, blend: `assets/model-${i}/model.blend`,
    downloads: { glb: `assets/model-${i}/model.glb`, blend: `assets/model-${i}/model.blend` },
  }));
  for (const base of ['/', '/lowpoly-vault/', '/custom/deep/']) {
    await mkdir(out, { recursive: true });
    await writeFile(join(out, 'index.html'), sourceHTML);
    const result = await writeStaticRoutes({ assets }, out, { base, origin: 'https://example.test' });
    assert.equal(result.pages, 58);
    for (const locale of ['', 'zh-CN/']) {
      for (const path of ['', 'models/', 'models/page/2/', 'about/', 'models/model-0/']) {
        const html = await readFile(join(out, locale, path, 'index.html'), 'utf8');
        assert(html.includes('id="static-route-content"'), `${locale}${path} has real HTML`);
        assert(html.includes('src="/entry.js"'), `${locale}${path} shares the route dispatcher`);
        assert(html.includes('<noscript><style>'), `${locale}${path} remains readable without app CSS`);
        assert(html.includes(`rel="canonical" href="https://example.test${base}${locale}${path}"`));
      }
      const listing = await readFile(join(out, locale, 'models/index.html'), 'utf8');
      const critical=listing.match(/<style id="gallery-startup-style">([\s\S]*?)<\/style>/)?.[1];
      assert(critical,'List first-paint guard is rendered into HTML');
      assert(listing.indexOf('id="gallery-startup-style"')<listing.indexOf('</head>'),'Guard is in the head, outside noscript');
      assert(critical.includes('>:not(#static-route-content){display:none!important}'),'Only the useful SSG catalog is visible before mount');
      assert(critical.includes('prefers-color-scheme:dark')&&critical.includes('data-theme="dark"'),'Saved and system dark preference keep a matching background');
      assert(listing.includes(`href="${base}${locale}models/model-0/"`));
      assert(listing.includes(`rel="next" href="${base}${locale}models/page/2/"`));
      const detail = await readFile(join(out, locale, 'models/model-0/index.html'), 'utf8');
      assert(detail.includes('application/ld+json'));
      assert(detail.includes(`href="${base}assets/model-0/model.glb"`));
      assert(detail.includes('https://creativecommons.org/licenses/by/4.0/'));
    }
  }
} finally {
  await rm(out, { recursive: true, force: true });
}
console.log('Route entry tests passed: isolated wheel lists, original home/about/detail, locale/base prefixes, cross-app navigation, real HTML pagination, metadata, downloads and no-JS fallback.');

// Route entry also owns the first-paint startup contract. Keep this in the
// existing aggregate entry point without changing the sealed toolchain manifest.
await import('./gallery-startup-test.mjs');

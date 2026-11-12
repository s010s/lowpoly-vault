/** Run against the local gallery preview with headed Chrome. */
import assert from 'node:assert/strict';
import { mkdir, mkdtemp, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { chromium } from 'playwright';

const base = new URL(process.env.QA_BASE_URL || 'http://127.0.0.1:5201/lowpoly-vault/');
const output = process.env.QA_OUTPUT_DIR ? resolve(process.env.QA_OUTPUT_DIR) : await mkdtemp(join(tmpdir(), 'vault-continuity-'));
const report = { base: base.href, cases: [] };
const requested = new Set(process.argv.slice(2));
const gallery = new URL('zh-CN/models/', base).href;
const phone = { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 };
const rowSelector = id => `#slots [data-id="${id}"]`;
const thumbSelector = id => rowSelector(id) + ' img[data-thumbnail-state=ready]';

await mkdir(output, { recursive: true });
const browser = await chromium.launch({ channel: 'chrome', headless: false });
report.browser = browser.version();

async function boot(page) {
  await page.goto(gallery, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.__gallery?.models.length > 30);
}

async function search(page, text) {
  await page.locator('#search').fill(text);
  await page.locator('#search').press('Enter');
  await page.waitForFunction(value => window.__gallery.state.query === value, text);
}

async function center(page, index) {
  await page.locator('#wheel').evaluate((wheel, index) => {
    wheel.scrollTop = index * wheel.querySelector('.slot').offsetHeight;
  }, index);
  await page.waitForFunction(index => {
    const { state, settler } = window.__gallery;
    return state.center === state.results[index]?.id && settler.state === 'idle';
  }, index);
  return page.evaluate(index => window.__gallery.state.results[index].id, index);
}

async function playing(page, id, minTime = 0) {
  await page.waitForFunction(({ id, minTime }) => document.getAnimations().some(animation => animation.id === id && animation.currentTime >= minTime), { id, minTime }, { timeout: 3000 });
}

async function settled(page) {
  await page.waitForFunction(() => document.getAnimations().every(animation => !animation.id.startsWith('gallery-continuity-')));
}

async function snapshot(page, name) {
  await page.screenshot({ path: join(output, name + '.png') });
}

async function recordPhoneArtwork(page, id) {
  await page.evaluate(id => {
    const frames = [];
    const stage = document.querySelector('#detail');
    const samplePixel = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
    let backdropSamples = 0;
    const trace = window.phoneArtworkTrace = { frames, running: true };
    const visibleOpacity = node => {
      if (!node?.getBoundingClientRect().width) return 0;
      const style = getComputedStyle(node);
      return style.visibility === 'visible' ? Number(style.opacity) : 0;
    };
    function sample() {
      if (!trace.running) return;
      const detail = document.body.classList.contains('mobile-detail');
      let backdrop;
      if (detail && backdropSamples++ < 4) {
        const renderer = window.__gallery.renderer.renderer;
        const box = stage.getBoundingClientRect(), ratio = renderer.getPixelRatio();
        samplePixel.clearRect(0, 0, 1, 1);
        samplePixel.drawImage(renderer.domElement, (box.left + 4) * ratio, (box.top + 4) * ratio, 1, 1, 0, 0, 1, 1);
        backdrop = samplePixel.getImageData(0, 0, 1, 1).data[3];
      }
      frames.push({
        detail, backdrop,
        moving: visibleOpacity(document.querySelector('.continuity-art')),
        bridge: visibleOpacity(stage.querySelector(`.continuity-poster[data-model-id="${id}"]`)),
        poster: visibleOpacity(stage.querySelector(`#detail-poster[data-model-id="${id}"][data-state=ready]`)),
        wheel: visibleOpacity(document.querySelector(`#option-${id} img[data-thumbnail-state=ready]`)),
      });
      requestAnimationFrame(sample);
    }
    sample();
  }, id);
}

async function finishPhoneArtwork(page) {
  return page.evaluate(async () => {
    await new Promise(requestAnimationFrame);
    const trace = window.phoneArtworkTrace;
    trace.running = false;
    return trace.frames;
  });
}

async function checkFilterScroll(page, glbs, entry) {
  const requests = glbs.length;
  const panel = page.locator('#filter-panel');
  const form = page.locator('#filter-form');
  const frame = () => panel.evaluate(panel => {
    const form = panel.querySelector('form');
    const bounds = element => {
      const { top, bottom } = element.getBoundingClientRect();
      return [top, bottom];
    };
    return {
      header: bounds(panel.querySelector('.panel-heading')),
      footer: bounds(panel.querySelector('.filter-actions')),
      close: bounds(panel.querySelector('#filter-close')),
      viewportHeight: innerHeight,
      panelScroll: panel.scrollTop,
      panelHeight: panel.clientHeight,
      panelContent: panel.scrollHeight,
      formScroll: form.scrollTop,
      formRange: form.scrollHeight - form.clientHeight,
      scrollbar: getComputedStyle(form).scrollbarWidth,
    };
  });
  await page.locator('#filters').focus();
  await page.keyboard.press('Enter');
  assert.equal(await page.evaluate(() => document.activeElement.id), 'filter-close');
  const top = await frame();
  assert(top.formRange > 0 && top.panelContent <= top.panelHeight + 1, 'Only the filter choices are scrollable');
  assert.equal(top.scrollbar, 'none');
  assert.equal(await panel.getAttribute('data-more'), 'true');
  const cue = page.locator('.filter-scroll-cue');
  assert.equal(await cue.getAttribute('aria-hidden'), 'true');
  await page.waitForFunction(() => Number(getComputedStyle(document.querySelector('.filter-scroll-cue')).opacity) === 1);
  assert(top.header[0] >= 0 && top.footer[1] <= top.viewportHeight);
  await snapshot(page, entry.name + '-top');
  await form.focus();
  await page.keyboard.press('End');
  await page.waitForFunction(() => document.querySelector('#filter-panel').dataset.more === 'false');
  const bottom = await frame();
  assert(Math.abs(bottom.formRange - bottom.formScroll) <= 2);
  assert.deepEqual(bottom.header, top.header);
  assert.deepEqual(bottom.close, top.close);
  assert.deepEqual(bottom.footer, top.footer);
  assert.equal(bottom.panelScroll, 0);
  await page.waitForFunction(() => Number(getComputedStyle(document.querySelector('.filter-scroll-cue')).opacity) === 0);
  await snapshot(page, entry.name + '-bottom');
  await page.keyboard.press('Home');
  await page.waitForFunction(() => document.querySelector('#filter-panel').dataset.more === 'true');
  await page.locator('#filter-close').click();
  assert.equal(await page.evaluate(() => document.activeElement.id), 'filters');
  await page.locator('#filters').click();
  await page.locator('#filter-form input[data-group=category][value=plants]').check();
  await page.locator('#filter-apply').click();
  assert(await page.evaluate(() => window.__gallery.state.results.every(asset => asset.category === 'plants')));
  assert.equal(glbs.length, requests);
  entry.scrollRange = bottom.formRange;
}

async function check(name, options, test) {
  if (requested.size && !requested.has(name)) return;
  const context = await browser.newContext(options);
  const page = await context.newPage();
  page.setDefaultTimeout(15000);
  const entry = { name, errors: [] };
  report.cases.push(entry);
  const glbs = [];
  page.on('pageerror', error => entry.errors.push(error.message));
  page.on('request', request => {
    if (new URL(request.url()).pathname.endsWith('.glb')) glbs.push(request.url());
  });
  try {
    await boot(page);
    await test(page, glbs, entry);
    assert.deepEqual(entry.errors, []);
    entry.status = 'pass';
    console.log('PASS', name);
  } catch (error) {
    entry.status = 'fail';
    entry.error = error.stack;
    console.error('FAIL', name, error.message);
    await snapshot(page, name + '-failure').catch(() => {});
  } finally {
    entry.glbRequests = glbs.length;
    await context.close();
  }
}

try {
  await check('filter-scroll-desktop', { viewport: { width: 919, height: 570 } }, checkFilterScroll);
  await check('filter-scroll-phone', { ...phone, viewport: { width: 390, height: 540 } }, checkFilterScroll);

  await check('wheel', { viewport: { width: 1440, height: 1000 } }, async (page, glbs, entry) => {
    await page.waitForFunction(() => document.querySelector('#detail').dataset.state === 'ready');
    const plan = await page.evaluate(() => {
      const { results } = window.__gallery.state;
      const index = results.findIndex(asset => asset.category !== results[0].category);
      return { index, category: results[index].category, id: results[index].id };
    });
    await center(page, plan.index - 1);
    await page.locator(thumbSelector(plan.id)).waitFor({ state: 'visible' });
    const before = await page.locator(rowSelector(plan.id)).evaluate(row => {
      window.testWheelRow = row;
      return { y: row.getBoundingClientRect().top, selected: window.__gallery.state.selected };
    });
    const requests = glbs.length;
    await page.locator('#filters').click();
    await page.locator(`#filter-form input[data-group=category][value="${plan.category}"]`).check();
    await page.locator('#filter-apply').click();
    await playing(page, 'gallery-continuity-wheel-move', 24);
    const during = await page.locator(rowSelector(plan.id)).evaluate(row => {
      const visual = row.querySelector('.slot-motion').getBoundingClientRect();
      const box = row.getBoundingClientRect();
      const hit = document.elementFromPoint(box.left + 30, box.top + box.height / 2)?.closest('.slot');
      return { same: row === window.testWheelRow, y: visual.top, hit: hit === row, end: box.top };
    });
    assert(during.same && during.hit, 'The same option moves visually with its target at the result position');
    assert(during.y < before.y && during.y > during.end, 'The matching model is between its previous and final positions');
    await snapshot(page, 'wheel-filter');
    await settled(page);
    assert.equal(await page.locator(rowSelector(plan.id)).evaluate(row => row.querySelector('.slot-motion').getBoundingClientRect().top), during.end);
    assert.equal(await page.evaluate(() => window.__gallery.state.selected), before.selected);
    assert.equal(glbs.length, requests, 'Changing results must not load a model');
    assert(await page.evaluate(() => window.__gallery.state.results.every(asset => asset.category === window.__gallery.state.facets.category[0])));
    await page.locator('#filters').click();
    await page.locator('#filter-form select').selectOption('triangles-desc');
    await page.locator('#filter-apply').click();
    assert(await page.evaluate(() => window.__gallery.state.results.every((asset, i, list) => !i || asset.triangles <= list[i - 1].triangles)));
    await search(page, plan.id);
    await search(page, 'zzzz-no-real-model-987654');
    await page.locator('#empty-state').waitFor({ state: 'visible' });
    await page.locator('#empty-clear').click();
    await settled(page);
    assert(await page.evaluate(() => window.__gallery.state.results.length === window.__gallery.models.length && document.querySelector('#slots').children.length < 30));
    assert.equal(glbs.length, requests);
    entry.model = plan.id;
  });

  await check('phone', phone, async (page, glbs, entry) => {
    const id = await center(page, 7);
    await page.locator(thumbSelector(id)).waitFor({ state: 'visible' });
    const position = await page.locator('#wheel').evaluate(wheel => wheel.scrollTop);
    await snapshot(page, 'phone-collection');
    await page.locator(rowSelector(id)).tap();
    await playing(page, 'gallery-continuity-pane-art');
    await playing(page, 'gallery-continuity-pane-title');
    assert.equal(await page.locator('#detail').getAttribute('data-model-id'), id);
    assert.equal(await page.evaluate(() => document.activeElement.id), 'title');
    assert.match(await page.locator('#title').ariaSnapshot(), /heading ".+" \[level=1\]/);
    await snapshot(page, 'phone-opening');
    await settled(page);
    await page.locator('#detail-poster[data-state=ready]').waitFor({ state: 'visible' });
    await snapshot(page, 'phone-detail');
    assert.equal(glbs.length, 0, 'Opening a phone poster must preserve its existing 3D load policy');
    await page.locator('#mobile-back').tap();
    await playing(page, 'gallery-continuity-pane-art');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'wheel');
    assert.equal(await page.locator('#wheel').getAttribute('aria-activedescendant'), 'option-' + id);
    assert.match(await page.locator('#wheel').ariaSnapshot(), /listbox/);
    assert.equal(await page.locator('#wheel').evaluate(wheel => wheel.scrollTop), position);
    await page.goForward({ waitUntil: 'commit' });
    await page.waitForFunction(() => document.body.classList.contains('mobile-detail'));
    await page.goBack({ waitUntil: 'commit' });
    await page.waitForFunction(() => !document.body.classList.contains('mobile-detail'));
    await settled(page);
    assert.equal(await page.locator('#wheel').evaluate(wheel => wheel.scrollTop), position);
    assert.equal(glbs.length, 0);
    const detailScroll = await page.evaluate(() => history.state.scroll);
    await center(page, 10);
    const otherScroll = await page.locator('#wheel').evaluate(wheel => wheel.scrollTop);
    await page.goForward({ waitUntil: 'commit' });
    await page.waitForFunction(() => document.body.classList.contains('mobile-detail'));
    assert.equal(await page.evaluate(() => history.state.scroll), detailScroll);
    await settled(page);
    await page.locator('#mobile-interact').tap();
    await page.waitForFunction(() => document.querySelector('#detail').dataset.state === 'ready');
    await page.goBack({ waitUntil: 'commit' });
    await page.waitForFunction(() => !document.body.classList.contains('mobile-detail'));
    await settled(page);
    assert.equal(await page.locator('#wheel').evaluate(wheel => wheel.scrollTop), otherScroll);
    assert.equal(glbs.length, 1, 'Only the explicit 3D action loads the model on a phone');
    await page.locator('#language').tap();
    const long = await page.evaluate(() => window.__gallery.models.reduce((a, b) => a.name.en.length >= b.name.en.length ? a : b));
    await search(page, long.id);
    await settled(page);
    await page.locator(thumbSelector(long.id)).waitFor({ state: 'visible' });
    await page.locator('#wheel').focus();
    await page.keyboard.press('Enter');
    await playing(page, 'gallery-continuity-pane-title');
    await settled(page);
    assert.equal(await page.locator('#detail').getAttribute('data-model-id'), long.id);
    assert(await page.locator('#title').evaluate(title => title.getBoundingClientRect().right <= innerWidth));
    assert.equal(glbs.length, 1);
    entry.model = id;
    entry.longNameModel = long.id;
  });

  await check('phone-artwork-handoff', phone, async (page, glbs, entry) => {
    const id = 'eocladus';
    const asset = await page.evaluate(id => window.__gallery.models.find(asset => asset.id === id), id);
    await search(page, id);
    await settled(page);
    await page.locator(thumbSelector(id)).waitFor({ state: 'visible' });
    assert.equal(new URL(await page.locator(thumbSelector(id)).evaluate(image => image.currentSrc)).pathname,
      new URL('gallery/posters/eocladus-wheel.png', base).pathname);
    await page.waitForFunction(id => Number(getComputedStyle(document.querySelector(`#option-${id} img`)).opacity) === 1, id);
    let release;
    const posterHeld = new Promise(resolve => { release = resolve; });
    await page.route(new URL(asset.galleryPosters.detail, base).href, async route => {
      await posterHeld;
      await route.continue().catch(() => {});
    });
    await recordPhoneArtwork(page, id);
    try {
      await page.locator(rowSelector(id)).tap();
      await playing(page, 'gallery-continuity-pane-art');
    } finally {
      release();
    }
    await settled(page);
    await page.locator('#detail-poster[data-state=ready]').waitFor({ state: 'visible' });
    await page.locator('#detail .continuity-poster').waitFor({ state: 'detached' });
    entry.opening = await finishPhoneArtwork(page);
    await snapshot(page, 'phone-artwork-detail');

    await recordPhoneArtwork(page, id);
    await page.locator('#mobile-back').tap();
    await playing(page, 'gallery-continuity-pane-art');
    await settled(page);
    await page.locator(thumbSelector(id)).waitFor({ state: 'visible' });
    entry.returning = await finishPhoneArtwork(page);
    await snapshot(page, 'phone-artwork-wheel');
    assert.equal(glbs.length, 0);

    await page.locator(rowSelector(id)).tap();
    await settled(page);
    await page.locator('#mobile-interact').tap();
    await page.waitForFunction(() => document.querySelector('#detail').dataset.state === 'ready');
    await page.evaluate(() => {
      const go = history.go;
      history.go = function (delta) {
        window.resumePhoneBack = () => {
          history.go = go;
          go.call(history, delta);
        };
      };
    });
    await page.locator('#mobile-back').tap();
    await page.waitForFunction(() => window.resumePhoneBack);
    entry.waitingForHistory = await page.evaluate(() => ({
      detail: document.body.classList.contains('mobile-detail'),
      state: document.querySelector('#detail').dataset.state,
      mesh: window.__gallery.renderer.detail.model !== null,
    }));
    await page.evaluate(() => window.resumePhoneBack());
    await page.waitForFunction(() => !document.body.classList.contains('mobile-detail'));
    await settled(page);
    assert.equal(glbs.length, 1);
    assert.deepEqual(entry.waitingForHistory, { detail: true, state: 'ready', mesh: true },
      'The live detail stays visible until the return starts');

    for (const [name, frames] of [['opening', entry.opening], ['returning', entry.returning]]) {
      assert(frames.some(frame => frame.moving > .9), `Record the moving artwork while ${name}`);
      assert(frames.every(frame => [frame.moving, frame.bridge, frame.poster, frame.wheel].some(opacity => opacity > .9)),
        `Keep visible artwork on every frame while ${name}`);
      assert(frames.every(frame => [frame.moving, frame.bridge, frame.poster, frame.wheel].filter(opacity => opacity > .015).length === 1),
        `Keep one view of the model while ${name}`);
    }
    assert.deepEqual(entry.opening.flatMap(frame => frame.backdrop ?? []), [255, 255, 255, 255],
      'The stage backdrop is painted on the first visible detail frame');
  });

  await check('reduced', { ...phone, reducedMotion: 'reduce', colorScheme: 'dark' }, async (page, glbs, entry) => {
    const asset = await page.evaluate(() => window.__gallery.models.at(-1));
    for (const path of new Set([asset.galleryPosters?.wheel, asset.galleryPosters?.detail, asset.preview].filter(Boolean))) {
      await page.route(new URL(path, base).href, route => route.abort());
    }
    await search(page, asset.id);
    const row = page.locator(rowSelector(asset.id));
    await row.locator('img[data-thumbnail-state=error]').waitFor({ state: 'attached' });
    await row.tap();
    await playing(page, 'gallery-continuity-pane-fade');
    const moving = await page.evaluate(() => document.getAnimations().filter(a => a.id.startsWith('gallery-continuity-')).flatMap(a => a.effect.getKeyframes()).some(frame => frame.transform || frame.translate || frame.scale));
    assert.equal(moving, false, 'Reduced motion changes opacity only');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'title');
    await settled(page);
    await page.locator('#mobile-back').tap();
    await page.waitForFunction(() => !document.body.classList.contains('mobile-detail'));
    await settled(page);
    assert.equal(await row.count(), 1);
    assert.equal(glbs.length, 0);
    entry.model = asset.id;
  });

  await check('desktop', { viewport: { width: 1440, height: 1000 } }, async (page, glbs, entry) => {
    await page.waitForFunction(() => document.querySelector('#detail').dataset.state === 'ready');
    await center(page, 0);
    const assets = await page.evaluate(() => window.__gallery.state.results.filter(asset => asset.id !== window.__gallery.state.selected).slice(0, 2));
    let release;
    const held = new Promise(resolve => { release = resolve; });
    for (const asset of assets) {
      await page.route(new URL(asset.galleryPosters?.detail || asset.preview, base).href, async route => {
        await held;
        await route.continue().catch(() => {});
      });
    }
    const [first, second] = assets;
    try {
      for (const asset of assets) await page.locator(thumbSelector(asset.id)).waitFor({ state: 'visible' });
      await page.locator(rowSelector(first.id)).click();
      await page.locator(rowSelector(second.id)).click();
      const art = page.locator(`#detail canvas.continuity-poster[data-model-id="${second.id}"]`);
      await art.waitFor({ state: 'visible' });
      assert.equal(await page.locator('#detail canvas.continuity-poster').count(), 1);
      assert.equal(await page.locator('canvas.preview-renderer').count(), 1);
      assert.equal(await page.locator('#detail').getAttribute('data-model-id'), second.id);
      assert.equal(await page.locator('#detail-poster').getAttribute('data-state'), 'loading');
      assert(await art.evaluate(canvas => canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data.some((value, index) => index % 4 === 3 && value > 128)));
      await snapshot(page, 'desktop-stalled-poster');
    } finally {
      release();
    }
    await page.waitForFunction(id => document.querySelector('#detail').dataset.state === 'ready' && window.__gallery.renderer.stats.detailFirstFrameId === id, second.id);
    await settled(page);
    assert.equal(await page.locator('#detail canvas.continuity-poster').count(), 0);
    assert.equal(await page.locator('#detail-poster').getAttribute('data-model-id'), second.id);
    assert(glbs.filter(url => url === new URL(second.glb, base).href).length <= 1);
    await snapshot(page, 'desktop-live');
    entry.models = assets.map(asset => asset.id);
  });

  await check('poster-failure', { viewport: { width: 1440, height: 1000 } }, async (page, glbs, entry) => {
    await page.waitForFunction(() => document.querySelector('#detail').dataset.state === 'ready');
    const id = await center(page, 0);
    const asset = await page.evaluate(id => window.__gallery.models.find(asset => asset.id === id), id);
    await page.locator(thumbSelector(id)).waitFor({ state: 'visible' });
    for (const path of new Set([asset.galleryPosters?.detail, asset.preview].filter(Boolean))) {
      await page.route(new URL(path, base).href, route => route.abort());
    }
    await page.locator(rowSelector(id)).click();
    await page.waitForFunction(id => window.__gallery.renderer.stats.detailFirstFrameId === id, id);
    assert.equal(await page.locator('#detail-poster').getAttribute('data-state'), 'error');
    await settled(page);
    assert.equal(await page.locator('#detail .continuity-poster').count(), 0, 'The first live frame takes over when both detail posters fail');
    assert.equal(await page.locator('#detail').getAttribute('data-state'), 'ready');
    assert(glbs.filter(url => url === new URL(asset.glb, base).href).length <= 1);
    entry.model = id;
  });

  await check('different-views', { viewport: { width: 919, height: 987 }, deviceScaleFactor: 2 }, async (page, glbs, entry) => {
    const id = 'eocladus';
    const asset = await page.evaluate(id => window.__gallery.models.find(asset => asset.id === id), id);
    const posterURL = new URL(asset.galleryPosters.detail, base).href;
    let release;
    const held = new Promise(resolve => { release = resolve; });
    await page.route(posterURL, async route => {
      await held;
      await route.continue().catch(() => {});
    });
    try {
      await search(page, id);
      await settled(page);
      await page.locator(thumbSelector(id)).waitFor({ state: 'visible' });
      await page.locator(rowSelector(id)).click();
      await page.locator(`#detail .continuity-poster[data-model-id="${id}"]`).waitFor({ state: 'visible' });
      await snapshot(page, 'eocladus-wheel-while-loading');
      await page.evaluate(id => {
        const stage = document.querySelector('#detail'), frames = [];
        window.eocladusHandoff = frames;
        const opacity = node => {
          if (!node) return 0;
          const style = getComputedStyle(node);
          return style.visibility === 'visible' ? Number(style.opacity) : 0;
        };
        function sample() {
          // Once the first live frame is presented, the matching poster fades over it.
          if (window.__gallery.renderer.stats.detailFirstFrameId === id) return;
          frames.push({
            wheel: opacity(stage.querySelector('.continuity-poster')),
            detail: opacity(document.querySelector('#detail-poster')),
          });
          requestAnimationFrame(sample);
        }
        sample();
      }, id);
    } finally {
      release();
    }
    await page.waitForFunction(id => window.__gallery.renderer.stats.detailFirstFrameId === id, id);
    const frames = await page.evaluate(() => window.eocladusHandoff);
    entry.frames = frames;
    assert(frames.some(frame => frame.wheel > .95 && frame.detail === 0));
    assert(frames.some(frame => frame.wheel === 0 && frame.detail > .95));
    assert(frames.every(frame => frame.wheel <= .015 || frame.detail <= .015), 'Two camera views must not appear at once');
    assert(frames.every(frame => Math.max(frame.wheel, frame.detail) > .95), 'Keep the current model visible while the desktop poster changes');
    assert(glbs.filter(url => url === new URL(asset.glb, base).href).length <= 1);
    await snapshot(page, 'eocladus-live');
  });

  await check('desktop-history-handoff', { viewport: { width: 1100, height: 900 } }, async (page, glbs, entry) => {
    await page.waitForFunction(() => document.querySelector('#detail').dataset.state === 'ready');
    const original = await page.locator('#detail').getAttribute('data-model-id');
    await search(page, 'eocladus');
    await settled(page);
    await page.locator(thumbSelector('eocladus')).waitFor({ state: 'visible' });
    assert.equal(await page.locator(rowSelector(original)).count(), 0);
    await page.locator(rowSelector('eocladus')).click();
    await page.waitForFunction(() => window.__gallery.renderer.stats.detailFirstFrameId === 'eocladus');

    await page.evaluate(id => {
      const { decode } = HTMLImageElement.prototype;
      let release;
      const held = new Promise(resolve => { release = resolve; });
      HTMLImageElement.prototype.decode = function () {
        const decoded = decode.call(this);
        return this.id === 'detail-poster' && this.dataset.modelId === id ? decoded.then(() => held) : decoded;
      };
      window.releaseHistoryDecode = () => {
        HTMLImageElement.prototype.decode = decode;
        release();
      };
    }, original);
    try {
      await page.goBack({ waitUntil: 'commit' });
      await page.waitForFunction(id => document.querySelector('#detail').dataset.modelId === id, original);
      entry.frames = await page.evaluate(async id => {
        const frames = [];
        for (let index = 0; index < 3; index++) {
          await new Promise(requestAnimationFrame);
          const image = document.querySelector('#detail-poster');
          const style = getComputedStyle(image);
          const live = window.__gallery.renderer.stats.detailFirstFrameId === id;
          frames.push({
            poster: image.dataset.modelId === id && image.naturalWidth && style.visibility === 'visible' ? Number(style.opacity) : 0,
            live,
          });
        }
        return frames;
      }, original);
    } finally {
      await page.evaluate(() => window.releaseHistoryDecode());
    }
    await page.waitForFunction(id => window.__gallery.renderer.stats.detailFirstFrameId === id, original);
    assert.equal(await page.locator('#search').inputValue(), 'eocladus');
    assert.equal(new URL(page.url()).searchParams.has('model'), false);
    assert(entry.frames.every(frame => frame.live || frame.poster > .95),
      'Back restores the decoded detail image even when its row is filtered out');
    await snapshot(page, 'desktop-history-restored');
  });
} finally {
  await browser.close();
  await writeFile(join(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log('Evidence', output);
  if (!report.cases.length || report.cases.some(entry => entry.status !== 'pass')) process.exitCode = 1;
}

import {createHash} from 'node:crypto';
import {mkdir, writeFile} from 'node:fs/promises';
import {chromium} from 'playwright';

const base = new URL('.', import.meta.url);
const output = new URL('./runtime/', base);
await mkdir(output, {recursive: true});
const browser = await chromium.launch({
  headless: true,
  executablePath: '/usr/bin/chromium',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--enable-webgl', '--ignore-gpu-blocklist', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
});
const page = await browser.newPage({viewport: {width: 1280, height: 760}, deviceScaleFactor: 1});
const consoleMessages = [];
const pageErrors = [];
page.on('console', message => consoleMessages.push({type: message.type(), text: message.text()}));
page.on('pageerror', error => pageErrors.push(String(error)));
try {
  await page.goto('http://127.0.0.1:4173/qa/independent/small-land-air-quartet-20261019/webgl-scene-check.html', {waitUntil: 'networkidle'});
  await page.waitForFunction(() => typeof window.qaRun === 'function', null, {timeout: 30000});
  const result = await page.evaluate(() => window.qaRun());
  const imageFiles = [];
  for (const scenario of result.scenarios) {
    const name = scenario.id + '.png';
    const png = Buffer.from(scenario.canvas_png_data_url.split(',')[1], 'base64');
    await writeFile(new URL(name, output), png);
    imageFiles.push({path: 'runtime/' + name, bytes: png.byteLength, sha256: createHash('sha256').update(png).digest('hex')});
    delete scenario.canvas_png_data_url;
  }
  result.screenshots = imageFiles;
  result.runtime.launch_arguments = ['--enable-webgl', '--ignore-gpu-blocklist', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'];
  result.console_messages = consoleMessages;
  result.page_errors = pageErrors;
  result.status = pageErrors.length === 0 && result.runtime.context_created && result.runtime.rendered && !result.runtime.context_lost ? 'pass_limited_software_webgl' : 'fail';
  await writeFile(new URL('software-webgl-scene.report.json', output), JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({status: result.status, three: result.runtime.three_version, renderer: result.runtime.gl_renderer, scenarios: result.scenarios.map(({id, instances_total, render_calls, rendered_triangles, frame_ms_median, frame_ms_max}) => ({id, instances_total, render_calls, rendered_triangles, frame_ms_median, frame_ms_max})), page_errors: pageErrors}));
} finally {
  await browser.close();
}

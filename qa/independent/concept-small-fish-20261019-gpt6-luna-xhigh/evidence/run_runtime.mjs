import fs from 'node:fs/promises';
import path from 'node:path';
import { chromium } from 'playwright';

const [baseUrl = 'http://127.0.0.1:8765', outputJson, screenshotPath] = process.argv.slice(2);
if (!outputJson || !screenshotPath) throw new Error('Usage: node run_runtime.mjs BASE_URL OUTPUT.json SCREENSHOT.png');

const browser = await chromium.launch({
  headless: true,
  executablePath: '/usr/bin/chromium',
  args: ['--no-sandbox', '--enable-webgl', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
});
const page = await browser.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1 });
const consoleErrors = [];
const pageErrors = [];
page.on('console', message => { if (message.type() === 'error') consoleErrors.push(message.text()); });
page.on('pageerror', error => pageErrors.push(String(error)));
try {
  const harness = 'qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/runtime-harness.html';
  await page.goto(`${baseUrl}/${harness}`, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.__qa?.status === 'done' || window.__qa?.status === 'error', { timeout: 30000 });
  const runtime = await page.evaluate(() => window.__qa);
  const result = {
    tested_at_utc: new Date().toISOString(),
    browser: await page.evaluate(() => navigator.userAgent),
    renderer_backend: 'Chromium ANGLE SwiftShader software WebGL; hardware GPU not used',
    harness: 'evidence/runtime-harness.html',
    runtime,
    console_errors: consoleErrors,
    page_errors: pageErrors
  };
  await fs.mkdir(path.dirname(outputJson), { recursive: true });
  await fs.mkdir(path.dirname(screenshotPath), { recursive: true });
  await fs.writeFile(outputJson, JSON.stringify(result, null, 2) + '\n');
  if (runtime.status === 'done') await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(JSON.stringify(result, null, 2));
  if (runtime.status !== 'done' || consoleErrors.length || pageErrors.length) process.exitCode = 1;
} finally {
  await browser.close();
}

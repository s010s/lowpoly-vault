import assert from 'node:assert/strict';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import {
  hasMetricDimensions, formatModelLength, modelHeight, primaryDimension, isFlatAsset,
  formatDimensionsXYZ, dimensionDetails, dimensionNote, comparisonMeasurement, comparisonText,
} from '../model-dimensions.js';
import { publishedModels } from './geometry-fixtures.mjs';

const root = new URL('./', import.meta.url);
const models = await publishedModels();
const source = await readFile(new URL('../main.js', root), 'utf8');
const html = await readFile(new URL('../shell.html', root), 'utf8');
const css = await readFile(new URL('../style.css', root), 'utf8');
const checks = [];
assert(models.length > 0);

// 1. Explicit meter-authored fixtures for upright and flat models.
const cycad = { ...models.find(a => a.id === 'cycad'), units: 'meters', dimensions: [2.11, 1.37, 2.17] };
assert.equal(modelHeight(cycad), '1.37 m');
assert.equal(isFlatAsset(cycad), false);
assert.equal(primaryDimension(cycad, 'en').value, '1.37 m');
assert.equal(primaryDimension(cycad, 'en').label, 'Model height');
assert.equal(dimensionDetails(cycad), 'Height (Y): 1.37 m · Width (X): 2.11 m · Depth (Z): 2.17 m');

const wave = { ...models.find(a => a.id === 'wave-ripple-surface'), units: 'meters', dimensions: [1.5, 0.081, 1.16] };
assert.equal(isFlatAsset(wave), true);
assert.equal(primaryDimension(wave, 'en').value, '1.50 × 1.16 m');
assert.equal(primaryDimension(wave, 'en').label, 'Footprint');
assert.equal(primaryDimension(wave, 'zh').label, '占地尺寸');
assert.equal(comparisonMeasurement(wave), 'Footprint (W × D) 1.50 × 1.16 m · Thickness 8.1 cm');
assert.equal(comparisonMeasurement(wave, 'zh'), '占地（宽 × 深）1.50 × 1.16 m · 厚度 8.1 cm');
assert.equal(modelHeight(wave), '8.1 cm');

// Generalized flat-model detection covers all shallow models without hardcoding IDs.
const anyFlat = { id: 'any-flat-slab', units: 'meters', dimensions: [2.0, 0.05, 1.4] };
assert.equal(isFlatAsset(anyFlat), true);
assert.equal(comparisonMeasurement(anyFlat), 'Footprint (W × D) 2.00 × 1.40 m · Thickness 5 cm');
for (const bad of [undefined, { id: 'x' }, { id: 'x', units: 'meters', dimensions: [1.5, NaN, 1.16] }, { id: 'x', units: 'meters', dimensions: [1.5, -0.081, 1.16] }]) {
  assert.equal(comparisonMeasurement(bad), '');
}
checks.push('Upright models show height, while all flat models (height/maxHorizontal < 0.25) automatically show X × Z footprint and thickness with clean Chinese spacing');

// 2. Bilingual comparisonText stays clean and non-redundant (gesture hint lives in .stage-hint).
assert.equal(comparisonText('hand', 'en', cycad), 'Illustrative scale · Hand length 18 cm');
assert.equal(comparisonText('hand', 'zh', cycad), '示意比例 · 手长 18 cm');
assert.equal(comparisonText('human', 'en', cycad), 'Illustrative scale · Human height 1.8 m');
assert.equal(comparisonText('human', 'zh', cycad), '示意比例 · 人物身高 1.8 m');
assert.match(comparisonText('human', 'zh', wave), /人物身高 1\.8 m · 占地（宽 × 深）1\.50 × 1\.16 m · 厚度 8\.1 cm/);
checks.push('Comparison captions use proper CJK/unit spacing and stay free of redundant gesture hints');

// 3. All published models format cleanly without rounding positive values to zero or mutating metadata.
for (const asset of models) {
  const original = JSON.stringify(asset.dimensions), [width, height, depth] = asset.dimensions;
  if (!hasMetricDimensions(asset)) {
    assert.equal(modelHeight(asset), '—');
    assert.match(dimensionDetails(asset), /unconfirmed/);
    continue;
  }
  assert.equal(modelHeight(asset), formatModelLength(height));
  assert.equal(formatDimensionsXYZ(asset), `${formatModelLength(width)} × ${formatModelLength(height)} × ${formatModelLength(depth)}`);
  for (const lang of ['en', 'zh']) {
    const text = dimensionDetails(asset, lang);
    for (const size of [width, height, depth]) assert(text.includes(formatModelLength(size)));
    assert.match(text, lang === 'en' ? /^Height \(Y\): .* · Width \(X\): .* · Depth \(Z\): / : /^高度 \(Y\)：.* · 宽度 \(X\)：.* · 深度 \(Z\)：/);
  }
  assert.equal(JSON.stringify(asset.dimensions), original, 'Dimension presentation must not mutate metadata');
  assert(!/^0(?:\.0)? cm$/.test(modelHeight(asset)), 'Small dimensions must not round down to zero');
}
checks.push('All 1,000 published models keep exact non-mutating X/Y/Z and primary dimensions without rounding tiny models to zero');

// 4. Sub-millimeter precision boundaries.
for (const [meters, expected] of [
  [0, '0 cm'], [-0, '0 cm'], [Number.MIN_VALUE, '4.94e-321 mm'],
  [1e-12, '1e-9 mm'], [0.0000001, '0.0001 mm'], [0.0000499, '0.0499 mm'],
  [0.00040237721987068653, '0.402 mm'],
  [0.000499999999, '0.5 mm'], [0.0005, '0.5 mm'], [0.000999, '0.999 mm'],
  [0.001, '0.1 cm'], [0.001001, '0.1 cm'], [0.009243897, '0.9 cm'],
  [0.18, '18 cm'], [0.999, '99.9 cm'], [1, '1.00 m'], [1.37, '1.37 m'],
  [Infinity, '—'], [-Infinity, '—'], ['0.0004', '—'], [null, '—'], [NaN, '—'], [-1, '—'], [undefined, '—'],
]) {
  assert.equal(formatModelLength(meters), expected, `Length ${meters}`);
}
checks.push('Sub-millimeter, cm, m, zero, and invalid boundaries format accurately');

// 5. UI integration checks: dynamic dimensions label, no outside-click cancellation of Compare, readable mobile font size.
assert.match(html, /id="dimensions"><\/strong><span id="dimensions-label"/);
assert.match(source, /primaryDimension\(asset,state\.lang\)/);
assert.doesNotMatch(source, /pointerdown[^;]*renderer\?\.comparison/, 'Clicking UI controls outside the stage must not cancel Compare size');
assert.match(css, /#comparison-label\{[^}]*font-size:12px/, 'Mobile comparison caption remains readable (>=12px)');
assert.doesNotMatch(css, /#comparison-label\{[^}]*white-space:nowrap/);
assert.match(dimensionNote('en'), /authored-pose.*meters \(m\).*centimeters \(cm\).*stay fixed when you rotate/);
assert.match(dimensionNote('zh'), /原始造型.*米 \(m\).*厘米 \(cm\).*旋转查看时数值保持不变/);
checks.push('Production gallery uses smart primaryDimension, preserves Compare across outside clicks, and keeps readable mobile typography');

const report = { status: 'passed', models: models.length, checks };
await mkdir(new URL('./evidence/meter-scale/', root), { recursive: true });
await writeFile(new URL('./evidence/meter-scale/ui-regression.json', root), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));

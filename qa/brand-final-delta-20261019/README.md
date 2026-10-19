# Final brand delta — bounded real-browser verification

Tested source: `35030430c363db2ab975c9438ddef11c1ff22db2` on
`feat/unified-gallery-brand-20261019`.
Baseline already inspected: `2efdd2ef36e87f17ed0fb1da0aec82d9ead29110`.

The source diff has only four mobile-detail toolbar CSS lines plus brand test
launcher/coverage and startup screenshot-guard updates. Renderer, model assets,
posters and artwork did not change. No art review or full-model screenshot sweep
was repeated. This branch adds QA evidence only; no application/test changes,
merge to main, or deployment were performed.

## Results

- Complete production build and release audit: pass.
- Unmodified `site/brand-browser-test.mjs`: **17/17 pass**, zero runtime errors.
  The script's real-browser assertions confirm all five 390px independent-detail
  buttons have top coordinates within 2px, and that no-query mobile routes show
  the actual visible wheel list. Both English and Chinese cases passed.
- Updated `startup` group: **14/14 pass**, zero runtime errors. The previously
  blocked held-entry screenshot now succeeds with the repository's scoped guard.
  The caller explicitly unset `PW_TEST_SCREENSHOT_NO_FONTS_READY`; it was still
  unset after the suite, recorded by `font_wait_guard_restored=true`.
- Both commands exited 0 and used `/usr/bin/chromium` directly. No custom Chromium
  wrapper or caller-level screenshot/font adaptation was used this time.

## Actual visual checks

Opened `brand/en-mobile-detail.png` and its first-viewport/toolbar crops. Reset
view, Wireframe, Scale reference, plus and minus are all on **one row** at 390px;
the minus no longer wraps. Labels/icons and the rightmost control remain inside
the panel without clipping. Original full-page output also contains below-viewport
document content; `*-first-viewport.png` isolates the actual 390 × 844 view.

Opened the actual `brand/en-mobile-catalog.png` and `zh-mobile-catalog.png` at full
size: both are no-query catalog views, not the selected mobile-detail state. The
shared cube/wordmark, search, filters, row labels and guide rail fit the viewport.
There is no horizontal clipping. The favicon capture was also opened; its identity
is unchanged.

Opened the held-entry fallback first paint from the updated startup group. Real
linked content stays visible; there is no giant black unstyled SVG, visible legacy
Skip link, or blank initial page. The 14 delay/failure/no-JS/no-CSS cases retain the
existing DOM/layout/color checks and now capture without leaking the font flag.

## Execution

Saved Linux cloud environment; Chromium `154.0.8037.57`, Playwright `1.56.1`, Node
`v24.19.0`; software WebGL via ANGLE/SwiftShader. The user's computer was not used.
Each browser command had a 600-second bound. This is responsive UI/startup evidence,
not physical-device performance or a new broad functional/model acceptance claim.

```sh
GITHUB_SHA=35030430c363db2ab975c9438ddef11c1ff22db2 \
  REQUIRE_COMPLETE_GALLERY=1 SITE_BASE=/lowpoly-vault/ npm run build
env -u PW_TEST_SCREENSHOT_NO_FONTS_READY \
  GITHUB_SHA=35030430c363db2ab975c9438ddef11c1ff22db2 \
  CHROMIUM_PATH=/usr/bin/chromium SITE_BASE=/lowpoly-vault/ \
  BRAND_QA_OUTPUT_DIR=/workspace/scratch/brand-final-delta-35030430/brand \
  timeout 600 node site/brand-browser-test.mjs
env -u PW_TEST_SCREENSHOT_NO_FONTS_READY \
  GITHUB_SHA=35030430c363db2ab975c9438ddef11c1ff22db2 \
  CHROMIUM_PATH=/usr/bin/chromium SITE_BASE=/lowpoly-vault/ \
  QA_OUTPUT_DIR=/workspace/scratch/brand-final-delta-35030430/startup \
  timeout 600 node --input-type=module -e "import {runGalleryBrowserTests} from './site/gallery-browser-test.mjs'; if (process.env.PW_TEST_SCREENSHOT_NO_FONTS_READY !== undefined) throw new Error('unexpected caller font flag'); await runGalleryBrowserTests({groups:['startup']}); if (process.env.PW_TEST_SCREENSHOT_NO_FONTS_READY !== undefined) throw new Error('font guard leaked'); console.log('font_wait_guard_restored=true');"
```

`summary.json`, both original reports/logs and exit-code files, build timings, and
actual browser screenshots are retained alongside this report.

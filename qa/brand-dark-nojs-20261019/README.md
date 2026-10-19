# Dark OS / no-JavaScript document contrast verification

Exact source: `435aaffe18e78ac23227a767add0d92a99432268` on
`feat/unified-gallery-brand-20261019`.

The latest commit's narrow patch adds native OS-dark brand tokens for documents
without an explicit theme/application marker, plus regression assertions. This QA
does not assess unrelated release/history changes or perform a model/artwork sweep.
No application, test, model or style files were modified by this QA branch. No merge
to main or deployment was performed; all execution used the saved cloud environment.

## Results

| Check | Result |
| --- | --- |
| Complete production build and release audit | Pass; current published manifest has 182 entries |
| Existing brand browser script | **20/20 pass**, zero runtime errors |
| English OS-dark, no-JS detail specification label | **8.555584820908084:1** |
| Chinese OS-dark, no-JS detail specification label | **8.555584820908084:1** |
| Chinese light, no-JS detail specification label | **7.131626841699527:1** |
| Existing redesign matrix | Pass; 370 static routes, 15 wheel cases, no runtime/resource errors |
| Existing forced-fallback matrix | Expected `pass-with-webgl-fallback`; 2 wheel fallback cases, no runtime/resource errors |

Both existing redesign profiles execute `noJavaScriptChecks`: English/Chinese linked
catalog pagination and detail/file links remain usable, and the specification-label
contrast is asserted at **at least 4.5:1 in both light and dark** modes. The assertions
use computed foreground, the opaque ancestor background, label opacity and sRGB
relative luminance. Raw ratios are retained in `brand/report.json` and `summary.json`.

Both redesign runs explicitly use `QA_REVIEW_SCOPE=matrix`, so they do not rerun the
all-model GLB scene loop. The underlying script's generic GPU-summary wording must
not be interpreted as full-model or physical/hardware GPU acceptance. Forced WebGL
fallback is intentionally reported separately from rendering acceptance.

## Actual screenshot inspection

Opened both full-resolution dark no-JS specification text crops from the brand
script, the dark 404 screenshot, and English/Chinese dark no-JS detail screenshots
from both redesign profiles. Labels, values, description text, links and downloads
are readable on dark surfaces. No remaining low-contrast specification-label issue
or clipped text was observed in those inspected regions. The dark 404's wordmark,
heading, explanatory text and recovery links are also clearly visible.

Key evidence:

- `brand/en-mobile-detail-nojs-dark-text-crop.png`
- `brand/zh-mobile-detail-nojs-dark-text-crop.png`
- `brand/en-desktop-404-dark.png`
- `matrix/no-js-detail-en-first-viewport.png`
- `matrix/no-js-detail-zh-CN-first-viewport.png`
- Corresponding `fallback/no-js-detail-*-first-viewport.png`

The crops preserve actual browser pixels; original full-page screenshots are also
retained. No model-artwork review was repeated and no rendered proxy was substituted.

## Commands and environment

Chromium `/usr/bin/chromium` `154.0.8037.57`, Playwright `1.56.1`, Node `v24.19.0`,
Linux cloud with ANGLE/SwiftShader. Browser commands each had a 600-second bound.
The scripts used their existing repository launchers without custom wrappers or
test-source changes. Font fallback and responsive behavior are environment-specific;
this does not establish physical-device or Safari performance.

Common environment:

```sh
export GITHUB_SHA=435aaffe18e78ac23227a767add0d92a99432268
export CHROMIUM_PATH=/usr/bin/chromium
export SITE_BASE=/lowpoly-vault/
export GALLERY_DIR=dist
```

Executed commands/scopes:

```sh
REQUIRE_COMPLETE_GALLERY=1 npm run build
BRAND_QA_OUTPUT_DIR=/workspace/scratch/brand-dark-nojs-435aaffe/brand \
  timeout 600 node site/brand-browser-test.mjs
QA_OUTPUT_DIR=/workspace/scratch/brand-dark-nojs-435aaffe/matrix \
  QA_REVIEW_SCOPE=matrix QA_ALLOW_WEBGL_FALLBACK=0 QA_FORCE_WEBGL_FALLBACK=0 \
  timeout 600 node site/redesign-browser-test.mjs
QA_OUTPUT_DIR=/workspace/scratch/brand-dark-nojs-435aaffe/fallback \
  QA_REVIEW_SCOPE=matrix QA_ALLOW_WEBGL_FALLBACK=1 QA_FORCE_WEBGL_FALLBACK=1 \
  timeout 600 node site/redesign-browser-test.mjs
```

All three browser commands exited 0. `build-timings.json`, each `report.json`, logs,
exit-code files and screenshots provide the exact scope and underlying evidence.

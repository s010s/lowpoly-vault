# Refresh first paint and shared brand — bounded cloud browser evidence

This branch contains QA evidence only. Application, renderer, model, poster, style
and test source files are unchanged. No merge to main or site deployment occurred.
The saved cloud environment stayed available; the user's computer was not used.

## Exact sources and results

| Scope | Exact application source | Result |
| --- | --- | --- |
| Refresh first paint | `cac612ed06656ff475a7f80833f5461eb62be82d` | Complete build passed. Original run 18/19; one screenshot helper timed out waiting for fonts while the entry script was intentionally held. Same unmodified test suite passes 19/19 with screenshot font waiting disabled. |
| Shared brand, including final independent-detail SVG controls | `2efdd2ef36e87f17ed0fb1da0aec82d9ead29110` | Complete build passed. Original launch blocked by the cloud Chromium SUID sandbox helper. Same unmodified script passes 15/15 via a cloud-only executable wrapper adding `--no-sandbox`; favicon capture also completed. |

The originally supplied brand prefix `f0d78af1` resolved to
`f0d78af1e898c9b99a1108941081e83d7e412309`, but no brand build or screenshot was
performed from that superseded source. All final brand pictures are from `2efdd2ef`.

Environment: Chromium `/usr/bin/chromium` version `154.0.8037.57`, real WebGL via
ANGLE/SwiftShader, Playwright `1.56.1`, Node `v24.19.0`, Linux cloud. Viewports are
1440 × 1000 and 390 × 844. Mobile/responsive layout and OS font fallback are not
physical-device or Safari acceptance. Both browser commands had a 600-second bound.

## Refresh first-paint inspection

The requested `startup`, `routes`, and `fallback` groups completed. The 14 startup
cases delay/fail entry, bootstrap, main module, CSS, manifest and resource manifest,
plus light/dark no-JavaScript and no-external-CSS cases. They cover actual built HTML.

All 14 fallback first-paint captures and six mounted captures were opened in the
contact sheets. The held-entry desktop fallback and dark no-JS/no-CSS mobile
fallback were also opened at full size. They retain linked model cards and readable
light/dark text. There is no giant black unstyled SVG or visible legacy blue Skip
link. Delays resolve into the styled application; failures retain useful static
content rather than a permanent white/blank page. Existing routes/fallback cases pass.

One immediate mobile mounted screenshot catches row posters still downloading.
A bounded follow-up delayed resources again, decoded all 13 current row images,
and opened `mobile-resources-settled.png`: one styled header, visible model rows,
no giant SVG and no permanent blank listing.

The original `startup-delay-entry-desktop` fallback assertions already passed:
24 linked cards, both legacy shell elements hidden, correct light colors, no giant
SVG and no overflow. Playwright then waited for `document.fonts.ready` while that
test intentionally kept the module request unresolved. The original failed report
is preserved, not relabeled as a pass. Local Playwright source at
`node_modules/playwright-core/lib/server/screenshotter.js:218` supports
`PW_TEST_SCREENSHOT_NO_FONTS_READY=1`; it changes only capture waiting and no page
or test assertions. The complete repeat is in `refresh-cac612ed/no-font-wait/`.

```sh
GITHUB_SHA=cac612ed06656ff475a7f80833f5461eb62be82d \
  REQUIRE_COMPLETE_GALLERY=1 SITE_BASE=/lowpoly-vault/ npm run build
PW_TEST_SCREENSHOT_NO_FONTS_READY=1 \
  GITHUB_SHA=cac612ed06656ff475a7f80833f5461eb62be82d \
  CHROMIUM_PATH=/usr/bin/chromium SITE_BASE=/lowpoly-vault/ \
  QA_OUTPUT_DIR=/workspace/scratch/gallery-refresh-first-paint-cac612ed/no-font-wait \
  timeout 600 node --input-type=module -e "import {runGalleryBrowserTests} from './site/gallery-browser-test.mjs'; await runGalleryBrowserTests({groups:['startup','routes','fallback']});"
```

## Shared-brand visual inspection

All 15 actual first-viewport pictures were opened in desktop/mobile contact sheets:
English/Chinese home, list URL and independent detail at both widths; dark English
home; no-JS Chinese detail; and the 404 document. The independent-detail toolbar was
also opened at full size to inspect the final reset/wireframe/scale SVG controls.

The list URL in the existing script contains `?model=cooperoceras`, which opens
mobile details at 390px. Two additional no-query English/Chinese list screenshots
therefore show the actual catalog state. Both were opened at original size and
measured at 390px without overflow, with the common 25px mark and same wordmark font.

The same outlined cube, spaced `LOWPOLY VAULT` wordmark, serif display hierarchy,
system UI type, forest/ivory palette and stroke icons are visible across the
inspected routes. Independent detail controls match the common stroke style.
Long text wraps, controls remain inside the viewport, and no horizontal clipping
or cut utility control was observed. The no-JS detail remains scrollable/readable.
The dark home uses the corresponding light accent without changing the identity.

`favicon-16-32.png` was opened: the shared cube remains distinct at 16px and 32px
CSS sizes. The existing script uses DPR 2 and also includes a 64px enlargement.
Computed checks independently record the one font-family stack and weight 400,
25/29px square marks, bounded utility icons, shared favicon URL, and correct links.

The existing script requests `chromiumSandbox:true`. Its first launch aborts on
this cloud image's unconfigured SUID helper before any cases run. The original
report/log are preserved under `brand-2efdd2ef/`. The supported `CHROMIUM_PATH`
override points to `chromium-cloud-wrapper.sh`, which execs the installed browser
with `--no-sandbox` and all original Playwright arguments. No application or test
code was changed. The complete successful capture is under `cloud-launch/`.

```sh
GITHUB_SHA=2efdd2ef36e87f17ed0fb1da0aec82d9ead29110 \
  REQUIRE_COMPLETE_GALLERY=1 SITE_BASE=/lowpoly-vault/ npm run build
GITHUB_SHA=2efdd2ef36e87f17ed0fb1da0aec82d9ead29110 \
  SITE_BASE=/lowpoly-vault/ \
  CHROMIUM_PATH=/workspace/scratch/unified-gallery-brand-2efdd2ef/chromium-cloud-wrapper.sh \
  BRAND_QA_OUTPUT_DIR=/workspace/scratch/unified-gallery-brand-2efdd2ef/cloud-launch \
  timeout 600 node site/brand-browser-test.mjs
```

Each source folder has a summary, original and adapted reports/logs, build timings,
and the actual screenshots. Original-size full-page files and explicit
`*-first-viewport.png` crops are both retained. Contact sheets contain only those
actual browser pixels. This is the requested startup/brand visual verification;
it does not claim a new full functional, model-artwork, or hardware-performance pass.

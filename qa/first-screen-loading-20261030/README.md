The gallery now downloads one display catalog instead of the complete manifest, resource proofs and presentation-index code. Native wheel images load only inside the clipped viewport; neighbor detail posters warm after deliberate browsing and selected-model readiness. Selected posters/GLBs have high fetch priority. Artwork and catalog membership remain unchanged.

Source baseline: `0993add1a454200e83e88bd599180e38d62385e5` (current main read at task start, PR #86). All runtime file hashes and unchanged input hashes are in `source-receipt.json`.

| Route / network | Encoding | Transferred MB before → after | Model usable seconds before → after |
| --- | --- | ---: | ---: |
| gallery-default / 5 Mbps | identity | 13.221 → 6.587 | 22.07 (21.83–22.32) → 11.59 (11.43–11.76) |
| gallery-deep / 5 Mbps | identity | 16.859 → 8.167 | 27.81 (27.76–27.86) → 14.02 (13.72–14.32) |
| mobile-deep / 5 Mbps | identity | 14.565 → 7.173 | 24.27 (24.23–24.31) → 12.23 (12.19–12.26) |
| mobile-collection / 5 Mbps | identity | 12.865 → 6.454 | — → — |
| home / 5 Mbps | identity | 1.815 → 1.815 | — → — |
| detail-page / 5 Mbps | identity | 4.588 → 4.588 | 7.67 → 7.65 |
| gallery-default / 20 Mbps | identity | 13.221 → 6.587 | 6.92 → 3.83 |
| gallery-deep / 20 Mbps | identity | 16.859 → 8.167 | 7.34 → 4.23 |
| mobile-deep / 20 Mbps | identity | 14.565 → 7.173 | 6.61 → 3.68 |
| mobile-collection / 20 Mbps | identity | 12.865 → 6.454 | — → — |
| home / 20 Mbps | identity | 1.815 → 1.815 | — → — |
| detail-page / 20 Mbps | identity | 4.588 → 4.588 | 2.10 → 2.13 |
| gallery-default / 5 Mbps | gzip | 4.285 → 2.667 | 7.73 → 5.50 |
| gallery-deep / 5 Mbps | gzip | 7.923 → 4.248 | 13.23 → 7.52 |
| mobile-deep / 5 Mbps | gzip | 5.393 → 3.253 | 9.90 → 6.06 |

MB are decimal, CDP encoded transfer bytes including HTTP headers. Shell visibility and every request URL/type/priority/encoding/byte count are in the reports. The default gallery selects Cooperoceras; gallery deep links select Gomphotherium. `detail-page` is `/models/gomphotherium/`; `home` is `/`. Mobile is 390×844, desktop 1440×1000, DPR 1.

Measurements used Chromium 154.0.8037.57 with SwiftShader, fresh contexts, cache disabled and service workers blocked. CDP throttling was 5 Mbps/80 ms or 20 Mbps/40 ms. Identity and gzip are measured separately on the same built-site loopback server. Slow identity cases repeat twice; gzip and 20 Mbps cases have one sample. Timings are synthetic, not a real CDN or physical-device prediction. Baseline and final optimized runs were sequential.

Readiness requires the selected renderer to acknowledge its first presentation frame and expose the interactive ready state. Network idle is not used as readiness. Recording continues until all requests finish and no new request starts for 2 seconds; an additional browser regression confirms no new requests start during 10 idle seconds after readiness. Deferred posters load on user browsing, not a timer beyond the cutoff.

On mobile, 3D remains opt-in: the harness clicks “Interact in 3D” immediately after the enhanced selected poster is decoded. Table timings are navigation-to-usable including that automatic click, excluding human dwell time. The report also records poster and click timestamps. Mobile collection loads zero GLBs. A static native poster can appear before enhancement.

**Validation:** six active CI fixtures passed; route/startup, catalog/thumbnail, 13 detail-binding cases and 752 selection/state cases passed; final full build passed for 752 models. Full logs are in `checks/`. Actual browser tests cover scroll-to-visible images, keyboard activation, Back/Forward, deep-link refresh, orbit/reset, scale comparison entry/reset, fast selections (two stale GLBs aborted), 3D failure/retry, catalog failure/native scrolling, missing enhancement code, JavaScript disabled, and mobile reduced/normal motion. All eight browser scenarios passed.

The default desktop, deep-link desktop and deep-link mobile final screenshots are pixel-identical to baseline. Screenshot inspection caught and corrected two intermediate defects (missing units disabled scale comparison, and a noscript display override exposed raw markup/offset fallback images). Corrected screenshots and explicit regression assertions are included. The failed experiments remain in the task workspace outside this delivery directory.

Two retired historical suites (`wheel-presentations-test.mjs`, `catalog-data-test.mjs`) still fail before their relevant assertions: “Manifest differs from exact corrective selection”. The same failure was reproduced with original source from the exact baseline and unchanged data; no historical seals or expected results were relaxed. Current presentation/metric-field parity is covered for every model by the new active `gallery-loading-test.mjs`.

**Trade-offs:** the full public provenance files remain downloadable but are no longer startup dependencies. The display catalog is still about 3.72 MB raw / 1.11 MB gzip because exact wheel footprints and model descriptions are preserved. Noscript fallback adds about 94 KB raw HTML / 4.7 KB gzip. A deep link still briefly requests the small default detail poster before parser-time selection; this patch removes the larger offscreen wheel/default-neighbor burst. First selection of an unwarmed neighbor may need its detail poster. The home and standalone detail app remain unchanged, including their bytes.

Live CDN/browser validation is unperformed because `s010s.github.io` is denied by the enforced policy. No domain permissions, credentials or enforced network policy were changed; no alternate network route was used. No Mac, Meshy, ImageGen or paid generation calls were used.

**Reproduce:** install the existing lockfile with `npm ci --ignore-scripts --cache /tmp/lowpoly-npm-cache`, then `SITE_BASE=/lowpoly-vault/ npm run build`. Use a fresh output directory; an existing report resumes completed runs. Run `node qa/first-screen-loading-20261030/measure.mjs after dist /tmp/loading-after identity` (or `gzip`). Chromium must already exist at `/usr/bin/chromium`; no browser download/install is performed. For interactions, start `REVIEW_OUT=dist SITE_BASE=/lowpoly-vault/ PORT=5190 node site/serve-review.mjs`, then run `node qa/first-screen-loading-20261030/regressions.mjs`.

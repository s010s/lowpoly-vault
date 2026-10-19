# Approved gallery integration — cloud browser QA

Final tested application source: `1e8b5cb48f5211fa12a2108861591bc71150fce3`.
The earlier `59895824` run is explicitly superseded; see `SUPERSEDED-RUN.md`.
All work ran in the saved Linux cloud environment, without the user's computer.
No runtime, model, poster, UI design, or deployment changes are made by this QA branch.

## Acceptance status

The original gallery browser suite has a reproducible test-wait failure, so the
unmodified full acceptance command must **not** be described as passed. Final
entrypoint statuses and durations are recorded in `final-1e8b5cb4/entrypoints.json`.

The main suite completed 24/25 cases with no runtime exceptions. The sole failure
is `native-wheel-stationary-layout-resize-history` in
`site/gallery-browser-test.mjs:227–228`. The same case blocks wrappers that select
the scroll group, including the new full `npm run test:browser` command. That
command fails in its initial wheel matrix before reaching all-model acceptance;
the existing strict `models` scope is run separately so model coverage is not hidden.

## Reproducible blocking test issue

1. Open `/lowpoly-vault/models/?model=cooperoceras` at 1440 × 1000.
2. Initial wheel `scrollTop` is 19968, and the settler is idle.
3. Dispatch a native `mouse.wheel(0, 900)` over the wheel.
4. The existing wait requires only `idle && scrollTop > 0`, which was already true
   before the input. It can return before the browser processes the wheel event.
5. The immediately sampled value stays 19968, failing `after.scroll > before.scroll`.
   After approximately 250 ms, it is around 20865 and ultimately settles at 20864.

`scroll-wait-diagnostic/timing.json` records this in five out of five independent
preliminary-source runs. Both final-source main commands reproduce the same failure.
The test source did not change between those application SHAs. No test assertion
or application code was altered to turn the original commands green.

`final-1e8b5cb4/edge-cases/report.json` independently waits for an observed change
relative to the previous position before checking idle, then verifies the remainder
of the native scroll case: selected identity, stationary surrounding layout and
document scroll, Back restoration of the browsing offset, and resize. These checks
pass. The integration author should repair the original wait condition and rerun
the unmodified full entrypoints before acceptance is marked green.

## Additional final-source browser checks

- Full 175-item membership, deep/full-width multilingual search, filters and sort
  drafts, empty-state recovery, keyboard activation, Back/Forward, downloads,
  attribution clipboard success/denial, mobile poster-first opt-in inspection.
- Poster/live identity during superseded and failed loads, held-pointer rejection,
  retry, WebGL context loss/recovery, no-JS linked documents, failed-catalog HTML
  fallback, forced-WebGL fallback distinguished from GPU acceptance.
- Real 10,000-record fixture, deep search and virtualized DOM; one matched row after
  deep search. Real-model cache reuse, one renderer, at most three cache entries and
  a 48 MiB limit; idle inspection stops drawing.
- Independent final-sort checks cover `name` and `name-desc` locale round trips,
  retained browsing anchor and keyboard identity, unchanged selected mesh/request
  token/GLB count, and the `triangles-asc` filter-select alias.
- Preserved home, modal/history, bilingual static documents, canonical independent
  detail routes, downloads, wireframe, theme, authored metric reference and reset
  remain covered by their existing entrypoints.

See each report for the exact executed scope. The original deployment script has
a hard-coded public Pages origin. `live-entrypoint-local-adapter.mjs` preserves its
assertions while substituting only local transport and provenance labels; its
provenance report describes those substitutions. This is not post-deployment or
public-site acceptance. No site was published to run the checks.

## Actual visual inspection

Final-source screenshots in `final-1e8b5cb4/gallery/` and `visual/` were opened,
including desktop listing/filter/info, mobile listing/static/live details/filter,
selected poster under a delayed GLB, preserved home/modal and independent detail.
Actual Chromium compositor frames (not reconstructed/interpolated frames) record
hand and human reference entry/reset; frame timestamps are in `visual/sequence.json`.
The contact sheets show those real frames. Additional `visual/warm-settled-probe/`
captures wait for both reference and camera animation owners to finish and show
the settled reference entry and complete reset withdrawal.

Observed model/reference silhouettes, light/ground treatment, and selected-poster
identity remain coherent in the inspected images. Both hand and human disappear
after reset, and the main model regains its normal view. Mobile controls/downloads
fit the viewport, and mobile comparison/reset retains the selected authored height.
A separate settled mobile-header probe records zero document scroll and zero
visual viewport offset. No persistent layout clipping or blank selected model was
observed in these inspected states.

Software-rendered Chromium captures relatively few compositor frames during some
transitions. This evidence checks actual appearance and settled behavior; it does
not establish smooth physical-device animation, hardware GPU, Safari, or native
mobile performance. Single screenshots can miss an entire cold shader-compile
transition, which is why actual compositor sequences and settled checks are separate.

## Reproduction and evidence layout

Chromium: `/usr/bin/chromium`, version `154.0.8037.57`, ANGLE / SwiftShader WebGL 2.
Node `v24.19.0`, npm `11.9.0`, Playwright `1.56.1`, Three.js `0.180.0`.

```sh
GITHUB_SHA=1e8b5cb48f5211fa12a2108861591bc71150fce3 \
  REQUIRE_COMPLETE_GALLERY=1 SITE_BASE=/lowpoly-vault/ npm run build
QA_RUN_ROOT=qa/approved-gallery-integration-20261019/final-1e8b5cb4 \
  python3 qa/approved-gallery-integration-20261019/run-entrypoints.py
```

The runner records every command, environment override, source SHA, duration and
exit code; each entrypoint has a 20-minute bound. `edge-cases.mjs` uses `QA_OUTPUT_DIR`
and `GITHUB_SHA`. `visual-check.mjs` uses `QA_VISUAL_ROOT`, `GITHUB_SHA`, and optional
`QA_WARM_MOTION_ONLY=1`. Both are independently bounded by their caller. Application
tests are unmodified. Repeated wrapper PNGs are retained locally; committed evidence
keeps the main matrix, independent visual captures, reports, and selected model
contact sheets rather than duplicating the same screenshot across every wrapper.

The source branch remains unmerged and unpublished. No PR #20 or #22 was modified.

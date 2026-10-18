# Follow-up: real CI opening-dissolve regression

The first local result did not establish that GitHub CI was green. Exact old head `50e7621023174f19e2c1b4fa70acc6e8c03ff485` [gallery run 39142907751](https://github.com/s010s/lowpoly-vault/actions/runs/39142907751) failed `desktop-chinese` at the actual partial complementary-layer assertion (old modal test line 541): `samples:0`. Its shared-model suite passed 17/17 under Chromium 141.0.7390.37. The unmodified main `7772085` [gallery run 39119316297](https://github.com/s010s/lowpoly-vault/actions/runs/39119316297) passed. We do not classify this modal failure as a known baseline failure or dismiss it as flaky.

The two independent 160ms WAAPI opacity timelines could elapse and retire the bitmap while a main-thread frame stalled, with no partial blend sampled at a render opportunity. A deterministic 220ms stalled Chinese opening reproduces the identical `samples:0` failure against the old runtime. The fix starts one finite shared-weight controller only after the actual matching draw. If its first frame is late, it retains a 0.5/0.5 frame until the next rendering opportunity, then catches up to the original wall-clock deadline. Healthy scheduling remains 160ms. No second renderer, model redraw loop, new animation library or layout animation was added. Cancellation, detached ownership, reduced-motion changes and page visibility cancel or finish immediately and restore inline opacity.

Original partial-RAF, additive isolation, exact complementary coverage, geometry, pixel and resource assertions remain enforced. The old conditional WAAPI test now also checks the new explicit inline/computed weight pair and absence of independent opacity animations. The reduced-motion cached reopen now releases in the same task; the handoff probe samples the actual Element.remove operation on both sides, retains its mandatory release-boundary assertion and unchanged 3px / 3% geometry thresholds, and labels these samples synchronous. It does not defer the user's reduced-motion result or pretend those samples are RAF paints.

Final local validation on cloud Chromium 154.0.8037.57 / SwiftShader:

- Build, npm test, test:redesign, test:publication and the new deterministic handoff controller tests pass.
- Modal 9/9, including the added 220ms stalled Chinese opening; measured partial samples are 0 before and 1 after. See selected/ci-fix-before-summary.json, ci-fix-modal-summary.json and ci-fix-measured-opening-weights.json.
- Actual pixel/handoff 10/10 after measuring the exact synchronous release boundary; interaction 8/8.
- Shared-model remains 16/17 locally, with only the already reproduced Chromium154 rapid touch-zoom failure. This is separate from the 17/17 old-head CI141 result. The original test is unchanged.
- Existing modal timing-only advisories remain; functional passes do not claim the original nominal close timing targets all passed.

Independent review: [independent-review.md](independent-review.md), Approve for the scoped diff with explicit browser/CI limits. The new interaction browser suite is now also wired into gallery CI with its screenshots/report retained as a CI artifact.

The separate [Chromium review run on main 39119316282](https://github.com/s010s/lowpoly-vault/actions/runs/39119316282) already fails in `site/turntable-delivery.mjs:61` during review-site generation. This unrelated descriptor-path assertion and its workflow are unchanged. Release gallery validation and isolated review generation must not be conflated.

The CI ZIP materialization and download of matching Chromium141 were denied by the environment network proxy (403); no bypass was used. Exact CI logs were read successfully through the authorized GitHub connector. New head CI results must be checked after the follow-up push; no preemptive all-green claim is made in this document.

## User-facing visual acceptance

`selected/animation-walkthrough.mp4` is a short real-browser recording: cold hover loading → same-model detail opening → successful attribution copy → continuous return → immediate filtering → reversible Refine. Caption overlays are recording-only; the real cold GLB request is delayed 450ms so its loading state can be read. Product animation durations are unchanged by the recorder. Playback and screenshots have been inspected, including copying and Refine overlays.

This environment exposes only loopback preview servers. No user-accessible preview URL or port-forwarding capability is provided by the selected tools; no preview link is invented and no site is deployed. The user need only watch the supplied recording; technical regression and pixel checks are completed here.

Google Drive uploads remain cancelled at the user's request. Earlier local recovery archive ending `50e7621` describes the earlier head; it is not a backup of this follow-up fix. Main is not merged or deployed by this work.

## Exact 7a627e6 CI and mirrored conifer probe

[Gallery run 39144775710](https://github.com/s010s/lowpoly-vault/actions/runs/39144775710), exact head `7a627e6f2e17a39b7b213ed8f97f6ddf7971998a`, confirms modal **9/9**, including normal Chinese and 220ms stalled Chinese; shared-model **17/17**, main pixel/handoff **10/10**, and new interaction **8/8** on Chromium **141.0.7390.37**. Pipeline run 39144775685 passed. Gallery was still **failed**, specifically its independent mirrored conifer probe: reduced-motion cached reopen must sample the actual overlay-release boundary (`:632`, `:909`, reduced-motion call `:1199`). The earlier modal regression is fixed; this subsequent failed gate was investigated separately.

The follow-up changes only that conifer probe to sample the same actual removal boundary as the main probe, then restores the prototype. All original release-boundary, alpha/source-over, resource and 3px / 3% geometry assertions remain intact. It changes no product runtime. Selecting only the original reduced-motion round trip reproduces boundaries **0/fail before → 1/pass after**; diagnostic scope patches and compact original measurements are retained under diagnostics/ and selected/conifer-reduced-*-summary.json. This is synchronous sampling, not an assertion that an intermediate RAF occurred in reduced motion.

The full local conifer run still fails the **camera return actual intermediate draw** assertion under Chromium154 / software WebGL. A separate run against the actual unmodified main `77720858` dist reproduces the identical assertion on desktop-motion. See selected/conifer-local-154-baseline-comparison.json. The assertion was not weakened or retried until green, and neither run is described as a local conifer pass. This local baseline reproduction does not dismiss the different CI141 reduced-motion probe failure. The next exact head must complete CI before gallery success is claimed.

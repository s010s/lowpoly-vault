# Asset browser redesign: implementation checklist

Status: **implementation and automated verification complete; owner review only**. Branch checkpoints preserve code and original model sources; they do not approve asset QA, merge to main, or deploy GitHub Pages.

## Scope

- [x] Preserve original candidate IDs, source geometry, authored scale and file paths.
- [x] Separate worlds, multi-membership curated packs, cross-world categories and reliable technical specifications.
- [x] Make global assets a searchable grid; reserve the map for an explicitly selected small real pack.
- [x] Generate genuine English and Simplified Chinese static detail/listing HTML with useful no-JS content, metadata, canonical/hreflang, sitemap and ordinary links under GitHub Pages base paths.
- [x] Enhance list clicks with the existing modal and FLIP; retain filter/query/sort/page/scroll through Back/Forward; direct links remain useful.
- [x] Reduce visual noise, remove permanent format badges and replay entrance, show measured file sizes, previous/next model links, same-pack related models and honest download initiation feedback.
- [x] Package source/model with CREDITS.txt; copy release files through an approved-manifest allowlist only.
- [x] Preserve the singleton renderer, bounded cache/cancellation, on-demand drawing, disposal and reduced-motion behavior; add a truthful optional metric reference.
- [x] Experiment on dinosaur-nest, lepidodendron and natural-arch: matched rendering rules, 12–16 frame scrub, encoded/decode size and alpha/shadow comparison. Integrate only if evidence supports it.
- [x] Test 10 real assets and a 10,000-item uneven many-category fixture, static routes, URL state, accessibility, keyboard and actual download paths.
- [x] Capture actual UI screenshots; distinguish cloud fallback tests from GPU/mobile/continuous-animation acceptance.
- [x] Keep English-first Skills and bilingual README current; maintain this checklist and checkpoint work periodically.

## Preservation and acceptance boundaries

The original working directory and port-5188 review build remain intact. Implementation runs in an independent worktree populated from the complete current candidate snapshot. Existing previews and experiments remain available for comparison. No candidate becomes release-approved through this UI work. The interactive cloud browser has no WebGL; separate CI checks exercise real Chromium WebGL through software SwiftShader. This is not hardware-GPU performance certification. Bounded Node/DOM checks do not prove network, GPU or frame-rate performance. No external reference artwork is included in release output.

## Checkpoints

- Initial checkpoint: candidate snapshot plus this scope, before implementation.

## Current verification (2026-10-16)

- Local catalog, manifest, route/release, theme and metric-reference tests pass. The 10,000-record fixture uses 17 uneven categories and overlapping worlds/packs; it measures catalog metadata and cache behavior, not end-to-end GPU/network performance.
- All 26 real bilingual route documents and all 40 original/download/credit endpoints pass static HTTP checks. Unknown model routes return 404.
- Actual cloud Chromium: grid, geology filtering, real detail URL, keyboard next model and Back restore query/scroll/original-card focus. Direct Chinese detail retains visible static content and download links. WebGL is disabled and is explicitly reported as fallback.
- Actual 390px iframe browser rendering captured in `qa/redesign-v2-mobile-grid-zh.png` and `qa/redesign-v2-mobile-detail-zh.png`; document content width is 375px with desktop scrollbar, no horizontal overflow. This checks narrow layout, not Android device/touch/GPU behavior.
- Both complete CI profiles passed at 818f6b7 in run 38952193828. Final screenshot inspection then caught low-contrast labels on the JavaScript-disabled dark detail; 7bd2ced corrects the inherited color and adds a 4.5:1 contrast regression. The final rerun 38953140279 passed both profiles.
- Preview experiment: clean static images total 12,228 bytes; three 16-frame sheets total 171,688 bytes. Each sheet has a 4 MiB RGBA8 pixel budget, versus 0.25 MiB static. Shadow RGBA introduces grain/clipped edges and poor dark compositing. Decision: keep sprites experimental and retain lazy GLB. See experiment report for exact CPU proxy conditions.

## Checkpoint history

- 8285d53: complete original candidate snapshot and initial scope.
- 3f895b8: shared schema v2 contract.
- 4dec685: real static routes, curated grid, bundles, metric reference and review CI. Uploaded to the WIP branch only.

- 6d75ce2: preview experiment, mobile screenshots and layout polish. Uploaded to WIP branch and backed up privately in two verified ZIPs (original assets 80,542,918 bytes; code/renders 57,188,345 bytes).
- Follow-up CI found keyboard focus could leave the modal at a tab-order boundary. Explicit visible/eligible focus wrapping was added and subsequently passed both full CI profiles.
- Real cloud Chromium image decode probe now recorded in the experiment: static median 1.00–1.20 ms versus sheet 9.90–13.20 ms. This measures fresh image decoding from preloaded bytes, not network/GPU/device frame rate.

- c988773: keyboard containment and queued history navigation; actual cloud Tab cycling passes. CI reached all ten models and the complete locale/theme/viewport screenshot matrix, then its rapid-hover test was obstructed by the intentionally still-open filter disclosure. The test now closes that panel before hover; Escape/outside-click dismissal was also added.
- Manifest validation now accepts world-only metadata independently of legacy folder names, with regression coverage for stable ID/path compatibility and multi-world/multi-pack records. `npm test` performs explicit review-only structural checks without creating an approved manifest.

- The additional scoped-map stress test exposed 25 sparse categories collapsing into unreadable region labels. Small packs with more than six categories now use one compact pack arrangement; the global 10,000-item catalog still has no map.

## Remaining acceptance boundaries

- Final code 7bd2ced passed both complete profiles in CI run 38953140279, including the static-label contrast correction. SwiftShader verifies real browser rendering paths but is not hardware GPU performance certification.
- Selected final CI viewport screenshots have been inspected, including true GLB detail, bilingual homepage, dark catalog and no-JavaScript detail. 390px touch emulation and the cloud narrow iframe do not replace a physical Android device review.
- No universal animation frame-rate or latency claim is made. Sprite integration is intentionally rejected on the measured trade-off.
- Original 20 GLB/Blender source hashes match both authored metadata and the untouched original work directory (`qa/redesign-source-preservation.json`).
- Owner-private phone review hosting requires a separate authorized deployment; the current localhost preview is not a phone-accessible URL. Public Pages release and asset artistic/scientific approval remain outside this review checkpoint.

- Final stress-test fix: closing a 3D dialog could reactivate a different card under the stationary pointer after scroll restoration. Hover now waits for a genuine pointer movement after dismissal, preserving zero live scenes/RAF at rest. Both forced-fallback and strict WebGL CI now pass this lifecycle edge.

## Verified handoff

The concise implementation, measurements, remaining owner review and deployment boundary are in [redesign-v2-acceptance.md](redesign-v2-acceptance.md). Selected CI evidence is retained in `qa/redesign-v2-evidence/`; exact build files/hashes are in `qa/redesign-v2-build-verification.json`.

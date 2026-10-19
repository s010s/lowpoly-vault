# Dual-wheel browser — isolated interaction preview

This experiment is based on production commit `de413ef720463a2999516faf92c606bcdf9ab1b7` (175 catalog entries). It is independent of paused draft PR #20. No model acceptance, asset revision, production manifest change, merge or deployment is authorized by this experiment.

## Preflight, 2026-10-19

- Branch: `preview/dual-wheel-browser-20261019`.
- Inspected every existing file in `.github/workflows/`: asset-pipeline, full-release-review, gallery-review, hover-reveal-review, modal-motion-review, modal-raster-review, pages, publication-poster-capture, render-card-previews and scrollbar-modal-comparison.
- Only `pages.yml` deploys a website. Its deploy job requires a non-PR event and `refs/heads/main`. Other workflows test, build or upload downloadable evidence; none provides an isolated PR website URL.
- Existing Pages source/settings were not changed. The authenticated CLI Pages settings query returned Forbidden; the workflow audit does not claim to inspect undisclosed external integrations.
- Safest small deployment option: an explicitly authorized separate preview repository with its own Pages site and a small self-contained build. This requires repository creation or access to a designated preview repository, plus permission to configure Pages and deployment. No such changes have been made. A production subdirectory would require changing the production build/deployment and is outside this preview's scope.
- Library direct transfer and the single explicit-destination retry failed. The owner subsequently requested private Google Drive transfer; no public design-input branch is expected. The current session's Drive profile read succeeded, and authenticated metadata/fetch tools are available. Exact target IDs and actual local byte accessibility are still pending. No reference has been overwritten and no visual fidelity is claimed before inspection.
- The parent task is independently checking a Cloudflare Pages GitHub App used by another project. That is separate from GitHub Pages and is not yet configured or verified for this repository. No external service has been enabled by this experiment.

## Implementation boundary

Use the existing pinned Vite 7.3.7, Three.js 0.180.0 and Playwright 1.56.1 stack. Keep the preview entry/build independent from production. Start with a small explicit selection of existing manifest assets; do not discover or publish new assets. Existing `ModelStage` provides a single reusable renderer, cancellable fetch, stale-parse disposal, bounded resource caches, canonical camera data and snapshots. Its metric floor reference is not a hand/human comparison and must not be described as one.

Core interaction acceptance:

- Native left-only scrolling follows input continuously. Snap only after scrolling settles; new wheel/touch/key input cancels the snap. Centered and clicked selection are separate state. Only explicit activation changes detail.
- Search and one Filters entry; theme/type/specification values use OR within each group and AND across groups. Applied chips form one collapsible line. Results summary contains the count once.
- Hover loads real GLB on demand, retains the poster until a matching rendered frame, then dissolves. Superseded loading cannot replace the current item. Preserve right-side direction during switching and reuse one renderer when possible.
- Right-side wheel zooms; direct dragging rotates. Pause automatic rotation after interaction, while not visible and for reduced motion.
- Supplemental information supports hover travel into its popover, click pinning, keyboard, touch and Escape. Name, dimensions, polygon count and download remain visible.
- Scale comparisons use validated authored meters with a clearly labeled illustrative human/hand reference. Unverified scale is unavailable or explicitly illustrative. Exit restores the previous camera.
- English and Simplified Chinese; light appearance only for the initial preview.

## Verification plan

Run focused state tests and real Chromium interaction checks: uninterrupted wheel motion, interrupted settling, clicked-vs-centered selection, same-group OR/cross-group AND, chip removal, no results, quick repeated switches, delayed GLB cancellation, return/Back, keyboard and touch controls, Escape, runtime reduced-motion change, visibility pause, first-frame handoff, scale enter/exit camera restoration and responsive layout. Capture actual screenshots and a short interaction recording. Confirm production assets, manifest, entry and workflows have no diff.

Environment: Linux, Node 24.19.0, installed Chromium 154.0.8037.57. Dependency installation succeeded using a writable workspace npm cache. Browser tests will record the actual renderer; software GPU results cannot establish hardware performance.

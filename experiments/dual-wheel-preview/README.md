# Dual-wheel browser — isolated interaction preview

A light-only, bilingual interaction study with **9 existing real models**, based on production `de413ef720463a2999516faf92c606bcdf9ab1b7` (175 entries). Draft PR #21 is preview-only. Do not merge, deploy over production, resume PR #20, publish assets or change hosting permissions.

## Run and rebuild

From repository root:

```sh
npm ci --cache /workspace/.npm-cache
npx vite --config experiments/dual-wheel-preview/vite.config.js
```

Development entry: `http://127.0.0.1:5197/`. Build an independent static directory:

```sh
node experiments/dual-wheel-preview/build.mjs
REVIEW_OUT=experiments/dual-wheel-preview/build SITE_BASE=/ PORT=5198 node site/serve-review.mjs
```

Static entry: `http://127.0.0.1:5198/`. Output is `experiments/dual-wheel-preview/build/index.html`, with bundled same-origin JS/CSS/Three.js, the nine exact existing GLBs, their original Blender downloads/fallback images, and nine preview-only matched posters. GLBs contain their own materials; there are no remote runtime script/font dependencies. The existing Blender files are included to keep the Blender-source download functional. The entire production catalog is not copied. No `.git`, private references, PRD, credentials or signed download URLs enter the build.

Source does not modify the production app entry, assets, manifest, package files, Vite configuration or workflows. The experimental Vite configuration is separate. Deploy the generated directory only to an independently authorized preview environment; no deployment has been performed by this work.

## Implemented

- Fixed 128px hit slots with continuous position-driven model scaling, readable unscaled text, thin track and selected dot. Bounded mounted range with overscan and retained keyboard option. Native scrolling does not select a model. A quiet 150ms interval precedes one interruptible 220ms settling animation. New input interrupts immediately; pointer holds defer settling; click/keyboard/history positioning does not trigger a follow-up snap. Reduced motion keeps the natural stopping position.
- English / Simplified Chinese, one search and one Filters entry, draft/apply/cancel, OR within a dimension and AND across dimensions, chips limited to one line with overflow entry, triangle bands from actual metadata. Selected detail survives excluded/empty results. The one result summary reports nine preview models, not the production count. IME composition is respected.
- Keyboard list navigation and explicit Enter/Space selection, real GLB detail, direct orbit dragging, local wheel zoom and keyboard rotation/zoom. Ctrl/Meta browser shortcuts are left available. Detail is stationary by default.
- One GPU renderer/context with separate scenes/cameras for detail and one hover. The renderer composites a small 2D hover presentation surface inside the masked list, so the poster/first-frame dissolve and row opacity/clip share the same DOM geometry. A 300ms deliberate hover loads real GLB; after the first drawn frame, a 160ms dissolve precedes 6°/s rotation capped at 15°. Leaving fades back to the poster; scrolling, interaction, blur, invisibility and reduced motion stop hover. Click inherits the observed hover angle. The right view preserves direction when switching models.
- Abortable fetches, generation checks after parsing, stale-result disposal, at most three cached entries and a 48MiB estimated decoded-byte budget. Active scenes are protected from eviction; GPU estimates are not driver memory measurements. Temporary hover floor, contact texture and shadow-map resources are disposed.
- Continuous lit floor, soft directional shadow and grounded contact shadow, restrained grid, warm background, serif titles and light download panel. Matched canonical 512px posters use the same 42° azimuth, 23.3° elevation, 38° FOV and exposure as the real renderer. Existing model geometry/materials are preserved: the actual Cooperoceras asset is an open coiled shell, not the fuller shell depicted in the visual concept.
- Info hover intent, travel grace, scrollable sources, click pinning, keyboard focus, outside click and Escape. Names/dimensions/triangles/download/credit remain visible.
- Metric bounds validated before comparison. A schematic hand is exactly 18cm tall or a schematic person exactly 1.7m tall in the authored meter coordinate system. Both are explicitly illustrative, not specimen measurements. Camera enter/exit eases over 250ms, is interruptible, and restores position/target/zoom. Reduced motion skips camera animation.
- Mobile starts in the collection without a GLB request. Item opens a static detail; 3D is opt-in with an explicit exit control. Return restores the list. The 3D controller does not swallow the exit button's pointer event.

## Real reference inspection

Both original PNGs were **actually viewed**, not inferred from metadata. The authorized private Drive connector's raw inline-content route returned the original PNG bytes, which were displayed as image content and then materialized outside the repository. Library and signed-transfer network routes had failed; neither sharing permissions nor public access was changed.

- Original English UI: Drive `1TjI2pI8or_hJrnAXzJ1OxGTntVfA8Ph1`, 1,721,737 bytes, SHA-256 `e4a7809d1540b7c5f779a9ce3ae1bceab324897c716e1e226793c726af6a38ea`.
- Size-comparison reference: Drive `1ltdmlBiW26Cdo4yNqfyWdiDU6u11H0xE`, 1,622,995 bytes, SHA-256 `82d0c65d29cdb0ae32b7a9304111bfeb338bc8bea018709ab36ff86a26ae8472`.
- Private local PNGs: `/workspace/private-drive-references/Lowpoly-Vault-Original-English-UI-Reference-20261019.png` and `/workspace/private-drive-references/Lowpoly-Vault-Scale-Comparison-Reference-20261019.png`.
- PRD 0.5 was read through Drive readable text and retained privately as `/workspace/private-drive-references/PRD-v0.5.md`.

The English image defines the visual language. The auxiliary image only informs the single filter entry and hand comparison; its rectangular selected cards are not adopted. No private reference pixels are committed or packaged.

## Verification and evidence

```sh
node experiments/dual-wheel-preview/state-test.mjs
npm run test:preview
npm run test:redesign
CHROMIUM_PATH=/usr/bin/chromium node experiments/dual-wheel-preview/browser-test.mjs
```

Browser checks expect the built site at port 5198 and Playwright's ffmpeg for recording. In the selected environment, system ffmpeg is exposed at `/workspace/pw-browsers/ffmpeg-1011/ffmpeg-linux`; run with `PLAYWRIGHT_BROWSERS_PATH=/workspace/pw-browsers`. A normal Playwright installation can instead install its bundled Chromium and ffmpeg and set `CHROMIUM_PATH` appropriately.

Evidence is in `qa/dual-wheel-preview/`: report, real desktop/Chinese/comparison/tablet/phone screenshots and a recorded interaction walkthrough. The report names actual checks and renderer. The 200% equivalent CSS viewport is an emulation of available layout space; native browser zoom/pinch remain manual checks. The static build provenance lists exact original download hashes.

Poster regeneration is preview-only: start the development server, then run `node experiments/dual-wheel-preview/capture-posters.mjs`. It does not alter any production poster.

## Hosting audit and remaining scope

All ten existing workflows were inspected at the production base: asset-pipeline, full-release-review, gallery-review, hover-reveal-review, modal-motion-review, modal-raster-review, pages, publication-poster-capture, render-card-previews and scrollbar-modal-comparison. Only `pages.yml` deploys a site, and its deploy job requires a non-PR event on main. The others upload builds/evidence rather than isolated websites. The CLI Pages settings query was Forbidden; this audit does not claim to inspect undisclosed integrations. The parent task is separately handling authorized owner-private Sites preview delivery. No preview URL has been invented.

This is a nine-model study, not implementation or performance acceptance of the full PRD. It uses query-state URLs within its independent entry; existing production SSG model routes and SEO are unchanged. Search is synchronous for this small sample, not a 10,000-item Worker index. The sample uses curated ordering and real triangle bands, not a full taxonomy editor. Physical-device GPU performance, Safari, native zoom/pinch, accessibility assistive-technology testing and 1k/10k workload budgets remain unverified. Linux Node 24.19.0 / Chromium 154 / SwiftShader evidence establishes only the recorded functional and visual scope. User artistic/interaction acceptance is still pending.

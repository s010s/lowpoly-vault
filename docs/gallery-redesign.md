# Gallery redesign: implementation and verification

## Brief and audit

The previous interface devoted the first screen to a large serif headline and a single image, followed by an unbounded gallery and long introductory material. This was a poor fit for finding usable assets, and it created one WebGL context on every detail visit. The current motion prototype uses a compact charcoal shelf with regular geometric asset cards, unchanged light-stage model previews, a strong sans wordmark, an always-available search field and horizontal collection/type facets. This follows a pale mint prototype that the user rejected as too conventional. Visual approval remains pending; the current version is a first-screen and open/close interaction sample, not a declared final design. It retains the existing Vite / vanilla CSS / Three.js stack, original files, bilingual UI, attribution, and GitHub Pages subpath support.

This is a browsing application, not a cinematic marketing landing page. The first-screen claim is proved directly by the usable asset collection. There are no fabricated models, testimonials, counters, speculative categories, or generated substitute previews.

## Taste sources actually read

Retrieved 2026-10-16 from the links on https://www.tasteskill.dev/:

- https://github.com/Leonxlnx/taste-skill/blob/main/skills/redesign-skill/SKILL.md
- https://github.com/Leonxlnx/taste-skill/blob/main/skills/gpt-tasteskill/SKILL.md
- https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md

Applied: audit the existing product before changing it; preserve the working stack; make real subject imagery do the visual work; short headlines; deliberate typography and numeric alignment; coherent surface tokens; clear focus, pressed, loading, empty, and failure states; responsive composition; screenshot-led correction; transform/opacity animation; reduced-motion alternatives.

The current default skill explicitly excludes app screens. Its marketing-page draw and inspector were therefore not run or claimed. Likewise, GPT variant requirements for enormous section gaps, AIDA landing sections, stock photography, and scroll pinning conflict with this user's dense asset browser. Those were deliberately not imported. The grid is a real product catalog, not a row of decorative feature cards. A local system sans stack avoids runtime font CDN dependencies and unverified font redistribution.

## Motion references actually inspected

Catalog: https://github.com/showheyohtaki/motion-prompt/blob/main/api/v1/catalog.json (version 1.3ecb2619b4).

Reference source implementations were read in the four pack.js files below. Their Canvas 2D demo code is not shipped in this project. The production behavior is an original adaptation of the described motion. Motion Prompt is MIT, copyright 2026 Shohei Ohtaki: https://github.com/showheyohtaki/motion-prompt/blob/main/LICENSE.

| Reference | Source | Adaptation |
| --- | --- | --- |
| #002 Stagger | packs/motion/pack.js, element 02 | Newly rendered page cards rise 12px over 400ms; 30ms offsets capped at seven steps. Content remains present without animation. |
| #030 Orbit (Arc shot) | packs/camera/pack.js, element 06 | Pointer coordinates rotate the real loaded GLB pivot, bounded to slight X/Y rotation. One finite smoothing loop settles, instead of a perpetual demonstration loop or a CSS card tilt. |
| #049 Modal dialog | packs/ui/pack.js, element 01 | Native modal focus containment and backdrop; opening maps only the selected image bounds to the centered image stage using FLIP. Detail text is not scaled; it follows with a 180ms opacity/8px entrance. Image travel is 420ms cubic-bezier(.18,.8,.2,1), return 280ms. |
| #061 Filter chips | packs/ui/pack.js, element 13 | 150ms control feedback, explicit selected state and removable active filters. Results are actually filtered, not merely dimmed. |
| #092 Page transition | packs/lp/pack.js, element 20 | Preserve URL and return-navigation continuity; replace the reference's full-screen curtain with the requested card-to-detail FLIP. Missing/offscreen origin returns with a 140ms fade. |

Source URLs share the base https://github.com/showheyohtaki/motion-prompt/blob/main/ . No external runtime animation library or CDN is required.

## Scale and resource architecture

- Build-time catalog is derived exclusively from the manifest supplied to the build. It does not discover or approve assets.
- Small index contains counts, 256-entry shard descriptors and at most 24 initial lightweight summaries. Scientific, provenance and QA metadata lives in per-asset details fetched only when opened.
- Pagination mounts at most 24 card buttons. A 10,000-entry fixture remains test-only; it never enters the deployed catalog.
- Header counts let ordinary pagination jump directly to the relevant shard. Global bilingual search scans lightweight shards sequentially; query cancellation discards stale results. Eight shard and four detail LRU limits.
- Exactly one movable, lazy WebGL renderer and one live GLB scene. 140ms hover intent prevents incidental traversal downloads. Fetch and parse are serialized, aborted/superseded work cannot attach, and bytes are cached at three models / 24MiB maximum.
- Geometry, materials and textures are disposed on scene switch/hide. The renderer is reused until page teardown. Hidden/offscreen stages pause. There is no permanent animation loop.
- Original previews stay visible until an actual GPU draw succeeds. GPU or load failure retains the preview and provides a readable state, without treating a preview as 3D verification.
- Touch opens the detail with one tap; keyboard users can focus/open cards and use arrow keys, zoom buttons and reset. Native dialog handles focus containment. Reduced motion removes FLIP, stagger and pointer rotation while preserving inspection controls.
- #asset=ID links survive refresh on static Pages. Back closes an in-session detail. Filters and scroll stay in the mounted browsing page. If the originating card is absent or offscreen, close uses a short fade rather than flying to an invalid position.

## Verification boundary

`npm run test:catalog` executes the 10,000-entry metadata fixture and cache/paging/search checks in Node. `npm run test:browser` is the real Chromium/GPU acceptance suite: all actual GLBs, downloads, mobile/bilingual states, real hover triangles, pointer redraw, 10,000-entry DOM bounds, maximum GLB concurrency, cache bounds, and resource release. It must run in CI with a working Chromium/WebGL installation.

The available cloud Chrome has WebGL disabled. Local Playwright launch is blocked by the execution sandbox. Neither condition is a runtime pass. Existing failed browser evidence is retained; no asset QA state is promoted by this redesign. Screenshot/UI checks and build checks are separately reportable, and do not replace GPU acceptance or human artistic approval.

## Observed cloud UI checks

On 2026-10-16, the isolated review server on port 5188 was opened in a separate cloud Chrome tab. Actual screenshots are `qa/redesign-motion-shelf.jpg` and `qa/redesign-motion-detail.jpg`. The first-screen catalog shows the ten original approved-candidate previews; the detail displays the real source preview and an explicit WebGL-unavailable message. Earlier cloud checks verified Chinese/category filtering, detail hash refresh, and Back returning to the filtered catalog. These are UI/fallback observations only. The 10k browser DOM/resource assertions and actual pointer-driven GLB draw remain pending a GPU-enabled CI run.

The final isolated tab-14 check clicked the review-only Replay entrance control, opened the cycad, observed the temporary image-flight layer and hash route, then closed it and observed the restored ten-card catalog. This confirms execution and endpoints, not a continuous frame-rate assessment. Replay only restarts the existing card entrance classes; it retains filters/page and makes no catalog or model requests. Tab 13 was left untouched after possible concurrent human interaction. Visual direction is intentionally paused for user feedback.


## Theme reveal and expanded motion system (2026-10-16)

The user's next request added theme switching and broader usable motion. The current Motion Prompt catalog has no dedicated dark-mode example: the implementation adapts #085 Ripple (packs/lp/pack.js, element 13; 600ms cubic ease-out, farthest-corner radius) and #059 Toggle (packs/ui/pack.js, element 11; 200ms switch feedback). Both source implementations and catalog specifications were read. No demo source was copied.

`theme.js` changes only the root UI theme attribute and control labels. Header and modal each contain an accessible sun/moon button. Preview images, renderer, scene, camera and material state are untouched. View Transitions reveal the new UI from the invoking button centre to the farthest viewport corner over 600ms. Reduced motion uses 120ms opacity, and unavailable View Transitions use a 160ms opacity fallback. Explicit preference survives refresh; otherwise the OS preference is followed, including later changes. Storage failure is nonfatal. Fast requests are serialized and coalesced to the latest selection, with obsolete transitions skipped. A pre-paint theme initializer avoids a wrong-theme startup flash.

`motion.js` owns interruptible WAAPI animations per element. Initial header stages take 240ms with 45ms offsets. Cards enter from 24px/.96 scale over 460ms with 40ms offsets capped at 240ms. Offscreen cards are revealed once when observed; DOM content stays available, and focus cancels the focused card animation. Filtering/search/sort use a 100ms outgoing phase, stable-ID 280ms position FLIP for retained visible items, and entrance for new items. This does not use View Transitions, so it cannot deadlock the theme lane. Detail text follows image travel in 220ms sub-stages with 22ms offsets capped at 132ms. Disclosure content uses 220ms; buttons use 180ms press feedback. Loading feedback is tied only to actual pending work. Download feedback says that the file is being requested, never that it completed. All spatial effects are removed with reduced motion; finite UI animations pause while the document is hidden. The separate renderer continues its existing offscreen/visibility suspension.

Actual cloud tab 15 screenshots: `qa/redesign-theme-light.jpg`, `qa/redesign-theme-dark.jpg`, `qa/redesign-theme-detail-light.jpg`, `qa/redesign-theme-detail-dark.jpg`. Both complete UI themes were visually inspected; photos retain the same colours and framing. Modal theme toggles remained available with the cycad detail/hash unchanged. A single explicit dark selection survived reload. Filtered two-item geology results survived replay. The tool confirms start/end states, not continuous frame smoothness. OS change, seven rapid requests, storage failure, radius geometry, reduced-motion and unsupported-API behavior pass the isolated controller tests (`npm run test:theme`); corresponding real-browser CI tests remain unrun locally. A rapid browser click sequence did not establish an exact per-click count, so it is not reported as a rapid-input browser pass.

The CI browser suite now also asserts clean OS-theme defaults, saved preference, modal canvas identity/GPU counters, unchanged rotated/zoomed/wireframe canvas pixels, seven-click interruption cleanup, and reduced-motion opacity. This coverage was syntax-checked only; it has not executed in this restricted environment.


## Independent editorial homepage (2026-10-16, latest)

The user had continued to view the old port-5174 version during earlier feedback. That evidence does not establish rejection of the current motion sample. The new explicit homepage brief nevertheless called for a distinct front door rather than equating the homepage with the scalable catalog.

Following actual reference-site review coordinated by the parent (Kenney: composed model cover; Sketchfab: subject-led presentation and clear search; image-library examples: editorial title and cover-edge discovery), the root page now presents an original Blender-rendered model composition, a short bilingual headline and a real all-models CTA. The cover uses the repository's arch, conifer, cycad and fern on display platforms, not a claimed coexisting ecosystem. It remains a light display surface in both UI themes. No reference-site imagery is published. The original cover and attribution metadata are in `site/public/home/`.

Routes: no hash is Home; `#catalog` is the preserved bounded browser; `#about` contains library/license information; `#asset=ID` is the existing shareable detail. Old `#collection` is normalized to `#catalog`. In-session detail history records its source view; Back restores that view and the retained catalog filters/scroll. A fresh detail link closes to the catalog. Homepage search transfers to the real catalog query, and the three curated category entries use actual metadata counts. The source catalog remains ten candidates; no speculative stock or experimental models were added.

Cloud tab 26 observed: Home → arch detail → Back to Home; CTA → ten-model catalog; Home/About navigation; homepage search `arch` → one catalog match; geology curation → two models; and both homepage themes. Screenshots: `qa/homepage-desktop-dark.jpg`, `qa/homepage-desktop-light.jpg`. Narrow-screen browser verification was not completed; 390px responsive assertions were added to CI but not executed locally. The supported CUA API exposed no viewport setter, and a DevTools shortcut did not produce a usable responsive testing surface; no workaround bypassed browser restrictions.

Focused `test:catalog`, `test:theme`, JavaScript syntax and isolated review build pass. Aggregate `npm test` is not a pass: release validation stops because `assets/manifest.json` does not exist while the project remains review-only. No fake release manifest was created. GPU, full browser pressure and continuous-frame smoothness remain pending. Port 5188 and its source build directory are preserved. The parent is responsible for refreshing and marking the single user-facing tab 10 as the current deliverable.

Final CUA limitation: the tab-26 native AX observation and the same binding's Playwright DOM snapshot disagreed (native showed the homepage; DOM showed an older cycad detail). Therefore the last catalog-detail Back check is not counted as a reliable bound-tab pass. The parent must make the final navigation check through the real cloud desktop on the single user-facing tab 10. Screenshots of the new composition and earlier AX endpoint observations are retained, with this limitation disclosed.

## Model Atlas prototype (2026-10-16)

The default All models route now mounts a spatial 2D atlas in `site/atlas.js`, with a separate `site/atlas.css`; Grid remains an explicit alternative. The homepage, asset manifests, original previews, theme controller, download URLs and shared ModelStage are unchanged. The map transforms only spatial UI coordinates; it does not pretend to rotate a preview photograph. Actual GLB rotation continues through the one existing renderer. Cloud Chrome still reports the explicit unavailable-3D fallback, so this is not GPU acceptance.

Category counts create region geometry without downloading every summary. Each region uses stable category-local sorted ordinal slots and the asset's stable ID for card identity. The viewport computes intersecting rows/columns and mounts at most 80 asset buttons. Below 38% scale it shows region navigation rather than thousands of tiny assets. Visible ranges fetch 100-summary pages through the existing sharded CatalogStore (256-item shards, eight-shard LRU); detail metadata remains on-demand. Search scans the existing summary shards and remaps matching ranges into a search region. This prototype's layout remains stable during navigation; adding/renaming assets can shift ordinal slots in a subsequent catalog edition.

Interactions: drag threshold distinguishes pan from click; two-pointer pinch, focused-map/modified-wheel zoom with cursor anchor, explicit zoom/reset controls, keyboard arrows/+/-/Home, category camera flight, reduced-motion immediate flights, real-model hover, existing FLIP dialog and history Back with unchanged map camera. Plain unfocused wheel remains page scrolling. Regions and assets are actual labeled buttons, with Grid available for linear searching. Search/collection/sort rebuild geometry; category navigation focuses a region. At 10 assets the starting frame is intentionally zoomed for exploration, and Reset reveals the full atlas.

Observed cloud checks (isolated tab 30; original user tab 10 untouched): ten actual assets render; category navigation focuses plants; natural arch opens the correct detail and source download links; history Back closes the modal and preserves map transform `translate(130.395px, 55px) scale(0.656292)`; grid fallback shows the five filtered plants. The original screenshot is `qa/atlas-desktop-light.jpg`; focused-category screenshot is `qa/atlas-plants-focus.jpg`. Screenshots are real browser captures, not simulated animation or video.

Scale check: a test-only 10,000-summary browser harness starts with four region buttons and zero model cards; focusing plants mounted 36 card buttons (214 total DOM elements), rather than 10,000. Distant search found Synthetic 9999; changing the query twice ended with only Synthetic 8888. The synthetic fixture was isolated in the review directory and removed on the next review rebuild. `node site/atlas-test.mjs` separately checked 10/10,000 layout intersection bounds (80 maximum across sampled views). Existing catalog tests passed global bilingual search, cancellation and abort-ignoring transport, cache bounds and release gates; theme tests passed. Existing GPU browser regression uses explicit `?browse=grid` to preserve its historical grid-specific assertions. Full GPU, touch-device, and automated end-to-end atlas CI acceptance are still pending; these are not claimed by the cloud DOM checks.

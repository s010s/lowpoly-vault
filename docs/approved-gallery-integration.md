# Approved gallery integration

## Source and scope

The production list routes use the approved V55 dual-wheel application, derived from source commit `86dd9476078097cd0099fe42b2f79f896e5e11ea`. The runtime is in `site/gallery/`. Existing home, About and model-detail documents retain their original application; `site/entry.js` routes each full document to exactly one application. No renderer, stylesheet or global handler is mounted twice.

The release manifest owns catalog membership. The gallery requests `assets/manifest.json`, retaining every published asset's dimensions, units, checksum, scientific/source notes, downloads and curation membership. It never bundles the prototype's 30-model fixture or truncates at the catalog store's 100-item page limit. Virtualized rows and intentional hover/selection keep GLB fetching bounded.

Real English and Chinese HTML routes, static pagination, canonical/hreflang metadata, structured data, ZIP/GLB/Blend/credits downloads and no-JavaScript browsing remain in `site/static-routes.mjs`. Gallery filter/search/sort/selection state is URL-addressable. Links in model information open the original real detail pages.

## Rendering preservation

The approved layout, native-wheel settling, title hysteresis, click centering, compact icons, selected-poster presentation gate, first-frame crossfade, bounded single renderer, stale-response guards, mobile opt-in inspection and reduced-motion paths remain in the copied renderer/controllers.

The hand stays calibrated to 18 cm and human to 1.8 m with the shared asset scalar. The V55 reveal/ground-light treatment and footprint geometry are retained. Only the reviewed source-hash-matching Confuciusornis receives its measured support origin.

Full-catalog vertex tests found thin surfaces absent from the 30-model sample could clip in canonical or interrupted Reset views. A projection guard expands camera distance only when actual vertices exceed the limiting square viewport. It leaves all original 30 canonical camera positions and fit distances bit-for-bit unchanged, and never changes their reviewed wheel camera specs or poster bytes. Deliberate inspection zoom is not clamped by this reset guard.

## Reproducible posters and release gate

`site/public/gallery/approved-resources.json` is the immutable, checksum-pinned baseline for the original 30 poster pairs and calibrated scale files. `resources.json` can grow to cover the current published catalog. Every poster is paired with its source GLB hash, camera spec, PNG dimensions and file hash. Unknown paths and modified approved resources fail the audit.

For a new model, build the current site, then render only missing poster pairs with the real application in Chromium:

    SITE_BASE=/lowpoly-vault/ npm run build
    SITE_BASE=/lowpoly-vault/ npm run gallery:posters
    REQUIRE_COMPLETE_GALLERY=1 node site/audit-release.mjs

Set `CHROMIUM_PATH` only when using a known installed Chromium. `node site/capture-gallery-posters.mjs --source-output` additionally saves the sealed output under `site/public/gallery/` so subsequent builds reuse it. Capture is staged, validates exact full catalog identity and requires complete coverage before replacing output. Browser/context/shader errors fail the operation. No CPU raster proxy substitutes for this step.

Pages and the full-release workflow run capture plus the complete audit before deployment or acceptance. A partial ordinary build is usable to generate the remaining images, but it is not release-ready. The capture path automatically supports future catalog additions.

## Verification

`npm run test:gallery` covers production route selection, dynamic full membership, search and URL state, current real GLB geometry, original camera preservation, handoff/first-frame guards, wheel/title/guides, main-only reset and scale-reference entry/lighting/footprints. Geometry-only Node tests explicitly substitute textures; the existing browser parser remains responsible for actual embedded-image decoding.

`npm run test:gallery:browser` exercises actual browser routes and interactions, including interruptions and repeated actions. Legacy grid-specific browser acceptance entrypoints detect the new build and run the corresponding wheel/detail scenarios. Static documents, downloads, publication rejection tests and all-asset parsing remain mandatory.

Browser screenshots and raster/interaction results must be reported separately from deterministic geometry checks. Software-rendered Chromium and emulated touch do not establish physical-device or Safari performance.

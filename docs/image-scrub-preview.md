# Image-only catalog previews and continuous 3D details

This release adds a 24-frame pilot for the original natural arch, conifer tree and fern cluster. The remaining seven models keep static previews. No new model or artistic/scientific acceptance is implied.

## One renderer preset, two delivery modes

`site/render-preset.js` is the shared presentation contract. `site/render-web-previews.mjs` captures the actual `ModelStage` offline using the pinned Playwright Chromium and exact published GLBs. It records the preset and GLB hashes, browser version and actual encoded byte counts. The public catalog only receives WebP images. It does not import Three.js or fetch GLBs while browsing or scrubbing.

The preset fixes the camera, target/normalization, neutral background, color management, exposure and lights. Detail renders keep that presentation in light and dark UI themes. Perspective fitting preserves the same centered-square composition across different modal aspect ratios. GPU and browser differences can still affect individual pixels; this is a controlled matching preset, not a cross-device pixel-identity claim.

Blender diagnostic views remain independent QA evidence. They are not substituted for appearance-matched website frames.

## Interaction and resource bounds

- Desktop: after a brief hover intent delay, only the current card loads its sequence manifest, current image and up to two neighboring images. Horizontal motion rotates relative to the entry point, so a small first movement does not jump to the opposite angle; there is no autoplay.
- Keyboard: focus a pilot card, use arrow keys, Home/End or Escape. Enter opens the real detail renderer.
- Touch: horizontal drag starts scrubbing; a normal tap opens detail and vertical movement remains native scrolling.
- Three decoded frame bitmaps are retained, plus one active canvas. At the shipped 320 px resolution this is 1,228,800 bytes of retained RGBA frames plus a 409,600-byte canvas. This is a controlled-object budget, not a measurement of total browser memory.
- Encoded LRU: at most 12 frames / 2 MiB; manifest LRU: three. One network request runs at a time. Intermediate pointer positions coalesce. Superseded requests abort and stale decoded bitmaps close.
- Leaving the card, hiding the document, scrolling it out of view or opening detail releases decoded frames. A failed sequence keeps its static poster and usable detail link.

Clicking a rotated card copies the current bitmap and its azimuth/elevation. The same image expands without nonuniform stretching, while the real GLB loads automatically at that camera angle. The image remains until the real renderer's first successful paint. Next/previous navigation similarly retains a copy of the last actual draw until the replacement is painted; it never requires two live GLB scenes. Closing can retain the last detail snapshot on the originating pilot card until inspection resumes, including free-orbit elevations that are not present in the fixed-elevation sequence.

## Measured delivery size

All frames are 320 × 320 WebP, quality 0.75, with 24 angles per sequence:

| Original asset | All 24 frames | Static poster |
| --- | ---: | ---: |
| Natural arch | 47,868 bytes | 2,070 bytes |
| Conifer tree | 85,854 bytes | 3,514 bytes |
| Fern cluster | 111,402 bytes | 4,684 bytes |

The ten static posters total 30,248 bytes. A complete sequence is not eagerly downloaded on hover: initial activation is its manifest plus at most three frame files. Sequence metadata is approximately 5 KiB each. The original GLB/Blend/preview downloads remain byte-identical. The previous catalog used original 1–2 MiB PNG previews; derived card posters now avoid that cost.

`npm run test:scrub` verifies the sealed paths, hashes, dimensions and source identities plus cancellation, bounded caches and failure behavior. `npm run test:scrub:browser` records browser interaction, camera-angle continuity, zero GLB/Three.js list requests, rapid/slow replacement, touch, screenshots and video. Full release checks independently exercise all ten actual GLBs, bilingual routes, downloads and forced WebGL fallback.

## Release verification

The release workflow rerenders all 82 shipped WebPs with the pinned browser and actual built viewer, then checks their bytes against the shipped frames. The presentation preset is an isolated small shared chunk so the offline capture does not import the application UI. Browser handoff tests separately compare the current image with the real renderer at desktop/mobile aspect ratios and in both UI themes. Test evidence is uploaded as a CI artifact and excluded from Pages.

The first candidate browser run measured 16–42 ms pointer-to-frame latency on its local CI server, one active image request, three decoded frame bitmaps and zero empty frames across 92 sampled delayed/rapid detail-switch frames. These are software-rendered CI measurements, not mobile-network or physical-device performance promises.

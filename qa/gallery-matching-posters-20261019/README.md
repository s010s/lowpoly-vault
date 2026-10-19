# Matching gallery posters — cloud capture and independent QA

Source commit: `ac4668e434cbf3eed9a535f41cdb255093be6a59` on
`feat/approved-gallery-integration-20261019`. Capture ran entirely in the saved
Linux cloud environment on 2026-10-19. No user computer was used. No applicable
`AGENTS.md` existed in the repository or its workspace ancestors.

## Result

- Generated exactly 145 previously missing detail/wheel pairs (290 PNG files,
  40,659,936 bytes). Coverage is now 175/175 published models.
- Detail images are transparent 512 × 512 PNGs; wheel images are transparent
  768 × 432 PNGs. All decode, contain nonblank model content, and have opaque
  model bounds inside the image, with a minimum edge margin of 22 pixels.
- The 60 original PNGs for 30 reviewed models, hand/human GLBs, reference notices,
  and approved baseline retain their exact bytes. Of the 72 existing gallery
  files, only `resources.json` changed. Its reviewed poster specifications,
  reference mappings, and sealed file records still equal the approved baseline.
- Independent browser QA projects actual mesh vertices for all 175 detail views
  and all 175 wheel views at eight 45-degree turns. No model geometry crosses a
  clip boundary; largest absolute horizontal/vertical NDC coordinate is
  0.9162980392542515. Browser error list is empty.
- Six pairs were rendered again and matched the saved PNG bytes exactly:
  `cruziana-crawling-furrow`, `stratified-cliff`, `leptomitus`, `leclercqia`,
  `sand-spit`, and `nereites-lobed-meander`.
- All ten contact sheets were opened and visually reviewed. Actual original-size
  detail/wheel PNGs for `cruziana-crawling-furrow`, `leclercqia`, and `sand-spit`
  were also opened. No blank model or model clipping was observed.

## Environment and provenance

- Node `v24.19.0`, npm `11.9.0`, Playwright `1.56.1`, Three.js `0.180.0`.
- Chromium executable `/usr/bin/chromium`, browser `154.0.8037.57`.
- WebGL 2.0; ANGLE / Vulkan 1.3.0 / SwiftShader Device (Subzero), SwiftShader driver.
- Actual source `site/gallery/renderer.js` SHA-256:
  `f31d66d68c5c63c448bb039b9059ef57937e58a9aa65d46d02e1ecd67fd08a6b`.
- Capture script SHA-256:
  `5661ae27a28d405f11dc6267432bb318ced7d2a1e597d89d8614aa1fe17b7ce9`.
- Approved resource baseline SHA-256:
  `3a8a3d69f8c4069dbe1aa3e7a338f314638a1d142c10daf93207dde5c2c997a7`.
- The resource metadata's preserved `source_renderer_sha256` is the original
  approved reference provenance. The actual repaired renderer used for this
  capture is identified separately above and in `browser-verification.json`.

## Commands and evidence

Dependency install succeeded with `npm ci --cache /tmp/lowpoly-npm-cache` after
the default home cache proved unwritable. The lockfile was unchanged.

```sh
SITE_BASE=/lowpoly-vault/ npm run build
timeout 1200 env CHROMIUM_PATH=/usr/bin/chromium SITE_BASE=/lowpoly-vault/ \
  node site/capture-gallery-posters.mjs --source-output
timeout 900 env CHROMIUM_PATH=/usr/bin/chromium \
  node qa/gallery-matching-posters-20261019/verify.mjs
python3 qa/gallery-matching-posters-20261019/verify-images.py
REQUIRE_COMPLETE_GALLERY=1 SITE_BASE=/lowpoly-vault/ npm run build
```

`capture.txt` records all 145 captured IDs and completion. `source-audit.json`
and `dist-audit.json` seal the complete gallery. `browser-verification.json`
records all projected bounds, browser/renderer provenance, and sample byte
comparisons. `image-verification.json` records every generated image's hash,
dimensions, opaque-content measurements, and preserved baseline file hashes.
`build-complete.txt` and `build-complete-timings.json` record the final complete
resource build and release audit.

Only generated gallery files, the extended resource manifest, and this independent
QA evidence are included in the deliverable commit. Integration code, model art,
camera/light implementation, and reviewed resources were not edited by this task.
This is thumbnail generation and validation only; final page functionality
regression belongs to the integration task. No main merge, publication, or changes
to candidate PR #22 or old PR #20 were performed.

# Shared real-model preview

The catalog keeps one static transparent poster per card. A fine-pointer hover must dwell for 180 ms before acquiring the real GLB; keyboard arrows/Home/End and a deliberate horizontal touch drag acquire it explicitly. Vertical touch scrolling and ordinary focus do not load 3D. No turntable manifest or sequence frame is fetched by the running catalog. Historical frame assets and their immutable publication checks remain available.

`SharedModelPreview` is a presentation controller. It borrows `ModelStage`, the same singleton used by model details, and owns no WebGL renderer or decoded model cache. Only one real canvas/model can be attached. Pointer updates coalesce to one requested frame; there is no idle, auto-rotation or reduced-motion render loop. Visibility, card intersection, dismissal and stale generations release ownership.

Card opening captures the actual transparent draw for the existing flight animation. The real canvas then moves into details and acquires the same decoded scene, with actual azimuth, elevation and normalized orbit distance preserved. Lighting, exposure, alpha and square-based framing use the same preset. Closing transfers a bounded square snapshot back to the original card. That snapshot stays static until another intentional inspection; reacquisition preserves the inspected pose and zoom. The retained snapshot and canvas are separate visual surfaces, but there is only one renderer/context and one attached scene.

Encoded GLBs have a 3-entry / 24 MiB LRU. Decoded resources have a separate 3-entry / estimated 48 MiB LRU with explicit cache ownership and one active lease. In-flight fetch/parse work is serialized. An oversized resource may exist as one uncached active scene and is disposed when released. Cache pressure never disposes the active lease. Geometry, material, texture, skeleton and ImageBitmap disposal are deduplicated. Decoded byte diagnostics estimate unique buffers and image texture storage; they do not measure driver allocations or JavaScript heap.

Default cards remain visible until the matching model has successfully drawn. A superseded fetch/import/parse cannot attach to a newer host. Failed or lost WebGL restores the static poster; context restoration redraws the current owner. No old GPU draw is shown while a different asset loads.

## Verification

- `npm test` includes deterministic controller and real Three.js resource-object lifecycle tests.
- `npm run test:preview:browser` exercises real WebGL, cold/warm request/timing evidence, stale native image decoding, ten-model LRU pressure, interruption, input, theme, resize and context restoration, recording screenshots and videos.
- `npm run test:scrub:browser` retains its legacy command name but now tests intentional real-model catalog inspection.
- Existing strict detail, modal motion, natural-arch/conifer pixel parity, immutable source/publication and fallback tests remain gates.

Linux browser results must identify the tested commit, Chromium renderer and execution environment. Loopback/SwiftShader and emulated touch results are not production-network or physical-device performance certification. The current selected conifer has separately documented software-rendering frame-budget limits; switching transport does not remove that rendering cost.

The 10,000-item fixtures exercise catalog metadata pagination/search and bounded shards, not 10,000 loaded GLBs. Exact current ten-asset transport comparisons are recorded in `qa/shared-model-preview/payload-audit.md`. Full-sequence savings do not establish a cold-hover win: every current GLB is larger than the first three historical image frames.

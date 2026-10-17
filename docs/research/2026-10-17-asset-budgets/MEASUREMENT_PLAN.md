# Device and scene verification plan

Status: proposed protocol. No actual-device FPS, GPU timer, decode-time or total-memory benchmark was completed by this research task. Blender renders, static validation and software WebGL do not establish real-device performance.

## 1. Nominate devices and criteria

Select an actual minimum Android/Chrome, iPhone/Safari and integrated-GPU laptop/browser. Record model, OS/browser, renderer, available extensions, power/battery, thermal state, flags, viewport/FOV and physical drawing buffer. Discrete GPU is an enhancement cohort, not a substitute. Declare 30/60 FPS policy, percentile/stall criteria, cold-load target and visual conditions before testing. Proposed profile caps are starting allocations, not hardware facts.

## 2. Representative fixtures

Use visually reviewed small opaque prop, alpha-heavy plant, repeated tree, architecture module, static creature, skinned creature and inspection hero. Keep source/export hashes and licenses. Compare portable, controlled quantization+EXT_meshopt, matched-quality Draco where appropriate, KTX2 ETC1S/UASTC and planned LOD/material tiers. Do not transform the whole library first. Do not call changes to topology/UV/map count/precision a codec-only comparison.

## 3. Static inventory

Run pinned Khronos Validator and preserve reports. The supplied inventory script supports a narrow read-only subset and reads declarations; it does not validate/decode compressed geometry. Add positive/negative fixtures and missing-decoder/fallback tests before extending the existing release checker to compression, skinning or morphs.

Count all distribution dependencies; exported vertices, unique and scene-instance triangles; mesh/primitive/material/alpha states; image encoding, dimensions, assumed/actual formats and mips; joints/clips/morphs; extensions; semantic nodes, units and bounds. Retain exact tool versions/arguments and SHA-256.

## 4. Visual checks

Render exact delivery bytes in the intended consumer with matched camera/FOV, framing, lighting/environment, tone mapping/exposure and color management. Include multiple sides, intended near and normal scene distances, silhouette, seams, quantization, mip bleed and LOD transitions. Judge proportions/factual landmarks separately from surface palette/detail. Automated image difference is diagnostic, not an aesthetic/scientific verdict.

## 5. Loading

Use the actual deployment or controlled server with recorded headers/network conditions. Measure cold asset+cold decoder/transcoder, cold asset+warm shared decoder, and warm revisits separately. Record transferred/encoded-body bytes where browser timing permits; unavailable cross-origin timing is unknown, not zero. Include every dependency and HTTP content encoding.

Instrument download, parse, decode/transcode, image upload/compile scheduling and first useful view. Worker overlap needs a timeline, not a misleading sum. Initial repeatable protocol: five cold and five warm loads per fixture, raw samples plus median/p95; expand if variance changes the decision. These repeat counts are proposed experiment settings, not standards. [model-viewer loading](https://modelviewer.dev/examples/loading/)

## 6. Frame costs

Use a deterministic room route with fixed near/mid/wide views and realistic counts, animation, shadows, alpha overlap and UI. Suggested initial windows: 30 s warm-up, 120 s route capture, 10-minute mobile thermal observation. These are project protocol choices. Preserve raw intervals and median/p95/p99, long stalls, missed-frame rate, context loss. Median alone is not smoothness; 60/30 FPS correspond to roughly 16.67/33.33 ms frame budgets.

In Three r180 set renderer.info.autoReset=false. Reset once before the complete application frame; run all main/shadow/composer/probe/secondary-view work, then copy calls/triangles/lines/points and geometry/texture counts. Tag passes if main/all-pass values are both required. Verify instrumentation with a known mesh with/without shadows. Default r180 reset follows shadow rendering and can omit that work in naive readings. Counts are not bytes. [Renderer](https://github.com/mrdoob/three.js/blob/r180/src/renderers/WebGLRenderer.js), [counters](https://github.com/mrdoob/three.js/blob/r180/src/renderers/webgl/WebGLInfo.js)

CPU render-call duration is not GPU completion time. Use disjoint timer queries only when supported, with the corresponding WebGL API, and reject unavailable/disjoint results. Do not block awaiting GPU completion. Unsupported GPU timing remains unknown. [MDN timer query](https://developer.mozilla.org/en-US/docs/Web/API/EXT_disjoint_timer_query)

## 7. Memory and lifecycle

Record each unique geometry/texture allocation, sharing, actual format and mip levels; compute conservative estimates with compressed-block rounding. Include RGBA fallback and separate render targets, depth/MSAA, shadows, PMREM and postprocessing. CPU images/worker buffers/JS heap and GPU estimates are different ledgers. Browser/driver overhead remains uncertain.

Do not assume a portable free-VRAM query or allocate until failure. Set conservative caps/headroom, then validate on the nominated device. [MDN WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices)

Repeat room-enter/leave and inspection-open/close cycles until counts/observable memory plateau or a leak is found. Test reference-counted shared atlases/geometry, disposal, ImageBitmap closure and worker cleanup. Record load overlap peaks: old room+next room+temporary decode, not only steady state. [Three disposal](https://threejs.org/manual/pages/how-to-dispose-of-objects.html)

## 8. Decision and stop conditions

Approve a profile only after its minimum-device scene meets predeclared visual/frame/cold-load criteria and bounded cache/memory policy. Save raw results, failed cases, environment manifest, images, exact asset/decoder hashes and rationale.

If a codec saves bytes but harms first view or quality, retain portable or conditional use. Test resolution/alpha/shadow when fill-rate bound, batching when submission bound, LOD when vertex bound; never diagnose from file size alone. Keep five gates independent, required unknown=hold. Re-run after changes that invalidate evidence.

Research deliverables can be complete while this explicitly documented real-device calibration remains outstanding. No hardware approval is implied.

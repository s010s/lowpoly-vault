# Conifer r20 independent runtime evidence

Frozen candidate: `265b47eed899307228d609355cc46c6d6992f61d`, revision `structure-r20-A-normal16`.
GLB SHA-256: `c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40` (715,500 bytes, 19,052 triangles, 3 opaque primitives).

No maker file, frozen candidate record, published arch/fern asset, website image, release descriptor or main ref was modified. This local render branch contains runtime evidence for independent QA; it grants no publication approval.

## Measured runtime and scene scope

Actual built website `ModelStage` from website commit `e6af7a7` and the unchanged v2 render preset, Three.js 0.180.0, Chromium 141.0.7390.37. The GLB bytes consumed in-browser were SHA-256 checked. All three NORMAL attributes load as normalized Int16Array, with KHR_mesh_quantization and no external decoder.

Metal reports `ANGLE (Apple, ANGLE Metal Renderer: Apple M5 Pro, Unspecified Version)`. The separate SwiftShader context is software. One isolated browser at a time; scene viewport 1200×900/DPR1, 20 warmup renders, 60 timed render submissions and 30 rAF intervals per case. Valid completed GPU query results are separate: Metal has60 per case; SwiftShader has60 for1-copy cases and only10 for each16/32-copy case. The other query results were unavailable within the original bounded wait and are not counted or reconstructed. Clone and instanced modes use identical underlying mesh/material data and world transforms; camera fits the full authored-meter grove. Shadows are disabled; floor/grid are included.

| Copies | Mode | Measured calls | Measured triangles | M5 GPU timer p95 ms | M5 rAF p95 ms | SwiftShader rAF p95 ms |
|---:|---|---:|---:|---:|---:|---:|
| 1 | clones | 5 | 19054 | 2.392 | 8.9 | 16.8 |
| 1 | instanced | 5 | 19054 | 2.375 | 9.1 | 16.9 |
| 16 | clones | 50 | 304834 | 0.624 | 9.6 | 133.4 |
| 16 | instanced | 5 | 304834 | 1.413 | 9.6 | 133.4 |
| 32 | clones | 98 | 609666 | 0.433 | 9.5 | 259.7 |
| 32 | instanced | 5 | 609666 | 0.901 | 9.7 | 266.5 |

Calls/triangles are actual `renderer.info` observations, including two reference drawables and the floor’s two triangles. The single website ModelStage alone measures **3 calls / 19,052 triangles**. Actual visible clone counts equal 1/16/32. Instancing lowers calls but is not automatically faster in GPU execution.

M5 Pro meets the 16.7 ms target in these sampled headless scenes. All SwiftShader cases miss the strict16.7ms rAF p95 target:1-copy clones/instancing are16.8/16.9ms,16-copy cases about133ms,32-copy cases about260–267ms. None is labeled a performance pass; original arrays remain unchanged. Software elapsed timers are not physical GPU performance. CPU `render + gl.finish` return timings are near clock granularity and can remain asynchronous across the browser GPU process; they are retained but never used as GPU time or a budget pass. Thermal state/unrelated host workloads were not controlled. This is no universal hardware/gameplay certification.

## Pixels, normals, backfaces and thin leaves

The material check finds opacity 1 / transparent false. Green foliage is DoubleSide; openness comes from geometric gaps rather than alpha-blended leaves. Background/canvas alpha is separately retained for previews. Selected full-tree, 32-copy grove, under-view and branch-detail pixels were opened. No shader/context/console errors or missing back surfaces were observed. Small-angle original sequences at native128 and512 preserve ordinary subpixel edge changes; the foliage remains intentionally airy. This is not a whole-art-direction verdict.

Fixed-view repeats at128 and512 are byte-stable in both profiles. Matched r19 FLOAT-normal versus r20 SHORT-normal comparisons at42/132/222 degrees preserve small **nonzero** differences; raw metrics and paired PNGs are in `runtime-report.json` and `normal16/`. Do not relabel normal quantization mathematically lossless. No stochastic static flicker was detected; fine needle sampling/edge aliasing during motion remains visible for independent assessment.

The harness warns about two same-version Three.js imports: built website renderer and separate grove module after disposing the first stage. SwiftShader also logs screenshot/readPixels stalls. Both warning classes are retained with explicit scope/reason; they are not hidden or called shader failures.

## Previews and exact evidence entry points

- `attempt-01/summary.json`: distributions, device classification and scoped conclusions.
- `attempt-01/metal/runtime-report.json` and `swiftshader/runtime-report.json`: raw arrays, calls, geometry, camera/light/renderer configuration, warnings and source hashes.
- `attempt-01/{metal,swiftshader}/scene/`: six actual population screenshots per profile.
- `attempt-01/{metal,swiftshader}/diagnostics/`: under/high views and branch attachment closeups.
- `attempt-01/{metal,swiftshader}/preview/turntable.json`: exact24-frame sequence,768×768 WebP quality0.9, transparent alpha, each frame bound to current GLB/brief/references/preset. `poster.webp` equals frame0. All24 encoded frames in each profile passed dimensions, decoded alpha and SHA checks. Neutral composites/contact sheets are navigation aids only; original alpha frames remain intact.
- `attempt-01/{metal,swiftshader}/motion/`:12 original small-angle PNGs per128/512 size; strips are navigation aids.
- `attempt-01/gpu.report.json`, `scene.report.json`, `evidence-handoff.json`: subject-bound producer reports plus72 hashed image/report evidence entries, for fresh independent QA to inspect/bind.
- `attempt-01/run-inputs.json`, `probe.source.mjs`, `execution.json` per profile, process stdout/stderr and supplemental diagnostics execution: reproducible bounded-run identities and logs.

Prefer the separately identified SwiftShader sequence for a future CI-pixel-reproducible draft; Metal is a distinct physical-GPU measurement/profile. Neither preview set is approved for release by this task. All48 original frames were decoded/alpha checked, both24-frame navigation sheets inspected, and selected full-resolution actual images opened; this task does not claim a fresh full-angle artistic/factual approval.

Gate conclusion: exact-loader/GPU correctness **pass** in both contexts; measured **M5 scene scope passes**, SwiftShader frame budget **fails in all six cases**. Independent final seven-stage candidate acceptance and publication remain pending. Existing publication routes require safe lowercase revisions; this frozen revision contains capital `A`. This task preserves its exact identity and draft namespace; future integration must explicitly resolve that existing gate constraint without silently rewriting the frozen record.

Both main probe profiles completed with exit0; supplemental diagnostic contexts/browsers and local HTTP servers were closed in finally blocks. No user Chrome profile, Safari, new software or external service was used.

## Continuous-motion supplement

The discrete42–44.2° images are retained as the original narrow diagnostic, not evidence of a complete dynamic orbit. `motion-continuous-01/` adds one new7-second continuous360° orbit with near/far zoom, actual encoded video, frame-by-frame camera/timestamp trace, selected original PNGs and source/device/config identity. It is not a rerun of the population performance matrix. It reuses the exact original r20 GLB hash; doc1 may reference this run only after independently confirming unchanged bytes and renderer configuration, with the original candidate identity retained.

`SHA256SUMS.json` remains the original c92f415 inventory; its README entry identifies the pre-correction documentation in that fixed commit. The supplement inventory identifies this corrected README and new files. Original runtime arrays, queries, images and producer reports were not rewritten.

Doc1 identity now exists at `062be906210f34f206748a313e288934a52a2c4f`, `candidate-r20-a-normal16-doc1`, revision `structure-r20-a-normal16-doc1`. Exact GLB/Blend hashes were independently rechecked unchanged. `motion-continuous-01/supplement-report.json` records the new candidate and reuse-document hashes. Original runtime/video identities remain r20; doc1 documentation and reuse scope still require independent review.

# Pipeline pilot, 17 October 2026

## What is reproducible from this repository

`legacy-natural-arch/candidate.json` references the actual unchanged 40,656-byte, 672-triangle repository GLB and editable source. Its new study brief, references and all current stages are explicitly pending. It does **not** alter the historical asset metadata or approve its art, geology, GPU rendering or publication.

```sh
python3 scripts/validate_candidate.py qa/pipeline-pilot/legacy-natural-arch/candidate.json --json
# exit 0, valid=true, approved_for_brief=false
python3 scripts/validate_candidate.py qa/pipeline-pilot/legacy-natural-arch/candidate.json --require-approved --json
# exit 1: current unknown stages and pending decision block approval
python3 scripts/test_pipeline_pilot.py -v
```

This real-file integration test is included in `npm run test:pipeline`. Synthetic passing fixtures in the unit tests only exercise gate behavior; they never approve catalog assets. The narrow initial-ten WIP release remains a separate sealed exception.

## Actual headless Blender runs

The following cloud pilot measurements are observations, not production throughput promises. Full generated study bundles were retained separately from the release repository; this report does not pretend that their large binary artifacts are committed here.

- Effective process affinity: 9 CPUs. Container quota was not visible, so quota-limited capacity remains unknown. Other workers shared the machine.
- Two real assets, sequential queue, one process at a time and two Blender threads: 8.68 seconds total, sampled process-tree peak RSS 272,039,936 bytes. This smoke used two quick views per asset and did not establish full visual coverage or parallel-Blender speed.
- Textured Triceratops full quick pack: 24 evenly spaced azimuth views plus front/rear/left/right/top/bottom/clay/alternate light/wire/head detail. 34 images at 256×256, four Cycles CPU samples, fixed lighting/color management/framing. Queue wall time 31.15 seconds; renderer time 26.42 seconds; sampled peak RSS 348,184,576 bytes. Encoded frame bytes 1,870,928; all-frame RGBA estimate 8,912,896 bytes (no mip/decoder overhead).
- Frozen source GLB: `e24b10555eab61d0a3001f1dba9713477a80a3099c77a33ec6a8196a7ec70930`, 14,432 triangles, 9,552,372 bytes. Three embedded 2048×2048 PNG images total 8,976,805 encoded bytes; conservative RGBA full-mip estimate about 64 MiB.
- Frozen brief: `c92f4465651538aff4e52289a447ffff1e4c67771fb0470d3e4bc3bc2c10b475`; references: `5b8fa297301ec85874eb767191d39a7afc9a26ab07b5bc19bccc3ef1ba77f0d1`.
- Actual manifest passed checks for all frame bytes/hashes/dimensions, frozen subject/config binding, distinct orbit coverage and required diagnostics. The real study record remained `valid=true`, `approved_for_brief=false`; its visual decision was fail, with other obligations unknown. Rendering completion never changed that decision.
- PNG and WebP encoder paths were exercised. No browser GPU pass or HD surface-quality approval was inferred.

## Independent visual findings and repair loop

The first Triceratops near-8.3k-triangle revision was rejected after actual exact-GLB hero/profile/front and diagnostic inspection: abrupt horn collars, button-like eyes, repetitive frill beads, pinched lower legs, enlarged feet and jagged belly colors. The maker supplied a separately hashed 14,432-triangle revision addressing several of these issues, then a same-geometry texture A/B. Texture-rich low-poly was accepted as a valid direction, not rejected for departing from flat colors.

On the 2K texture study above, the reviewer opened hero/detail/side/front, the complete quick montage and original top/bottom/rear/alternate-clay/detail frames. Not every orbit original was individually opened, so no complete inspected-frame pass is asserted. Skin detail is visible, but its uniform regional pattern and soft torso/limb masses remain; the quick pack is too small/noisy for final fine-surface judgment. The 2K cost is not justified as the default without a lower-cost comparison. A later regional-material revision is a new hash and does not inherit this decision.

The real natural-arch surface pilot used GLB `9427a1b0e38790c562bb30f04559c825ecb0b59600d4dce221ee805ccc01cc81`: 672 triangles, 1,669,400 bytes, unchanged triangle-position multiset relative to the palette baseline. Exact-GLB hero/reverse/clay/alternate-light, close and albedo comparisons showed surface cues but a regular molded arch silhouette. The 1K PBR tier offered no convincing benefit over 512px in those tested views; the 69,912-byte color-only study retained most visible pigment cues. The full-PBR replacement was rejected on visible value. Its valid record did not become approved.

These are scoped craft/cost decisions, not botanical, paleontological, geological or runtime certificates. Feature-specific factual review, complete production deliverables, actual target GPU and populated-scene tests remain required for production acceptance. The scheduler's bounded overlap is tested with fixtures; safe production concurrency still needs a representative benchmark.

## Later bounded material study

A subsequent Triceratops regional-material revision (`c20a5ee7cf8058b79854d334a7f74e19da6a9637d74a0ed5a8f781837bfc8de0`, 7,695,292 bytes) quieted face/frill detail and broadened body scales. Independent inspection of its four exact-GLB images found an improved material hierarchy, while cheeks/mouth/eye rims and torso/limb transitions still held the full asset from the refined museum-style target. The 1K derivative (`62a19b7808a01591c3d13ab7ecfcdd543be8c4d323289f42caa2517a5f65c520`, 2,689,404 bytes) retained the medium-distance material read but visibly softened body-scale relief in the matched close crop. Retain the lighter study tier and an optional close-inspection tier; do not claim equal pixels or full asset acceptance. This bounded experiment ended with concrete unresolved form/factual/runtime scopes, not another automatic polishing cycle.

## Engineering checkpoint

See [independent review](independent-engineering-review.md), [test results](test-results.json), and the saved test log. All 125 pipeline tests, 46 initial-release checks, redesign integration and production build passed. The existing large viewer-chunk build warning remains nonfatal; this pipeline change does not claim to optimize the viewer bundle. Four Skill packages also passed skill-format validation.

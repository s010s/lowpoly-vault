# r15 maker handoff — independent review pending

Exact model: `conifer-tree.glb`, SHA-256 `2ad0baa9c4b54be1a3a5ebd2298eb612ca9d9cb4b4b3a09a2eddd16ae38eca8d`.

This is a candidate, not an accepted replacement. Original asset and r12 are unchanged. The maker does not approve visual, factual or specification gates. Parent task assigns independent Sol Medium QA before release.

## Change and measurements

Inherited all r12 woody geometry and 141 spray attachment positions. Replaced the four thick green fingers per spray with five paired shallow lanceolate needle groups, one short terminal and a slim connecting keel. Spray blades have width 30% of length and physical depth 13% of width; 11–40 degree whole-fan roll adds noncoplanar layers without adding geometry. Modern Metasequoia foliage is a shape analogue, not an ancient-species reconstruction.

- 16,450 exported triangles, 479,320 GLB bytes, 3 opaque materials / 3 primitives, zero textures.
- 11,677 authored/evaluated source vertices; 15,718 exported POSITION-stream vertices.
- Relative to r12: 2,256 fewer triangles (12.1%), 13,536 more bytes (2.9%). Original: 2,382 triangles / 145,732 bytes.
- Woody mesh: 1,525 vertices / 2,914 triangles. Vertex coordinates, face indices and world matrix exactly equal r12, proved in `wood-preservation.report.json`.

## Evidence entry points

`comparisons/r12-vs-r15-hero.png`, `r12-vs-r15-detail.png`, `r12-vs-r15-detailclay.png` are matched 512px render pairs (16 samples each, same framing/lights/color management). `original-r12-r15-hero128.png` and `original-r12-r15-silhouette128.png` preserve native 128px cells without enlargement. Three-column original/r12/r15 color/clay pairs are also present.

`evidence/full-angle256/` contains exact-GLB 24 azimuths plus 11 diagnostic images, including front/rear/both sides/top/bottom, clay/alternate key and wire. `comparisons/full-angle256-contact-sheet.png` is navigation only; all raw PNGs and hash-bound manifests remain. Current close detail is under `evidence/detail512/`; 6 native128 views are under `evidence/native128/`. Baseline raw images are retained under sibling `candidate-r14/evidence/original512`, `original128`, `r12-reference512` and `r12-reference128`.

## Technical results

Blender 5.2.0 LTS local macOS, one worker, two threads, per-process 180-second timeout. Official Khronos validator: 0 errors / 0 warnings. Static audit: pass. Source/export comparison: pass with the explicitly documented intentional smooth-foliage warning. Independent process rebuild: byte-identical and semantic-identical, with hash-bound request/result. Three.js 0.180.0 Node parser: pass. Dependencies were read from an existing install; nothing installed. No browser used or user browser touched.

Repository cloud queue is Linux-specific and refused macOS. That failed invocation remains recorded in r14. The separate `run_local_build.py` runs and records bounded local rebuilds without making Linux affinity, cgroup or memory-limit claims. Its request/result are checked by the repository reproducibility checker.

`candidate-validation.report.json` must say valid=true, approved_for_brief=false. `--require-approved` deliberately fails because independent art/factual/specification and actual GPU/composed-scene gates remain open.

## Known issues for independent QA

- Canopy remains airy at native128; full tree outline is visible but fine leaf groups may read as texture/noise rather than a solid crown.
- Fans remain directional. r15 fixes much of r14's cardinal edge-on thinning, yet hero left/right density differs and several shallow blades still present as lines from selected angles. Inspect every azimuth and opposite hero.
- Enlarged lanceolate groups can look like pointed diamond leaves at 512px, rather than fine needles. Decide whether this abstraction meets the requested spray/leaf reading; technical counts do not resolve that judgment.
- Buried organic intersections are intentional; fans can overlap neighbors. Check detail and underside for distracting crossings.
- No actual browser/GPU or populated-grove performance evidence. No LOD or dense-forest performance claim.

Retained preflights: r13 sparse isolated leaf tips; r14 overly edge-on planar fans. Their source, configs, outputs, pixels and execution histories remain unchanged. Do not promote them or reuse old r12 style acceptance.

## Reference scope and license

NC State Extension's Metasequoia page, Leaves/identification sections, supports linear, paired, soft feathery needle foliage: https://plants.ces.ncsu.edu/plants/metasequoia-glyptostroboides/ . C.J. Earle's Gymnosperm Database description supports flattened linear leaves: https://www.conifers.org/cu/Metasequoia.php . References were consulted only; no external pixels, model, palette or geometry were incorporated. Exact dimensions, simplified grouping and canopy arrangement are artistic choices. Source ledger is `references.json`.

Original code: MIT. Geometry, blend, renders and documentation: CC-BY-4.0, Leon Made This / s010s.

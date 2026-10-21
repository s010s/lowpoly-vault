# Archaeopteris r002 independent difference review

**Static core: PASS.** Technical, visual, factual, specification and runtime_parse pass; GPU and scene remain unknown/unrun. This is not formal/user/website/release/live approval. No global count changed.

## Fixed identity
- Commit: 08c1f20150c8a511aae6465074f49542f5e9884e
- GLB: de929572015716dd525e713fdaf6f94da20e2674112768369de49410b4e9e87a
- Brief: bafbe6e295670f1236ce1fc999a5f021b54c628484bb4cd2cc495a44f33fa078
- References: 9cf9ee7961498fe5dc53cc8b17cea994212aa012ff0736ab48b388890a1ab34e

## Leaf repair
All 576 final GLB blades independently measured. Base-tip and longest chord both range **0.149999952481–0.230000045802 m**. The original 96 genuinely oversized leaves (up to0.238413414m in this double-precision remeasurement) are repaired. All blade-local dimensions and directions remain intact instead of being scaled with the tree.

There are64 literal endpoint excursions in the stored floats. They are not hidden or treated as zero. Per-coordinate float32 rounding cells cover575 nominal lengths. One0.23m leaf misses that final-storage-only interval by0.603nanometers; a separately executed isolated mathutils trace reproduces its normalized-vector and multiplication rounding. All576 actual pre-normalization deltas lie componentwise inside final storage rounding cells. No new global tolerance or frozen-range change is used. Width ratio0.62 and thickness0.009m lie in every blade's coordinate-derived interval. Total measured height3.799999952316m correctly represents3.8m.

## Preserved geometry and evidence
- One trunk,6 roots,12 structural limbs,48 sprays,576 blades,3 scars;5856 authored/evaluated vertices,7918 polygons,9128 triangles.
- Skeleton scale differs by0.055912%; maximum nonleaf displacement2.196374mm. Edge/polygon/material assignments unchanged.
-645 actual attachment checks pass after checking real overlap, not imposing a new requirement that every interface center be inside its host.
- True independent source reopen and byte-identical reexport. No source saved. No external libraries/images.
- Project/schema, Khronos0 errors/0 warnings and actual Three180 GLTFLoader parse pass.
-367 binding hash checks and126 committed-blob checks; two separate rebuild PID34/57 with matching semantic digest and all input/output bytes.
- Final triplet predates actual final-render request. Eight512px PNGs inspected individually; lossless sheet tiles identical.
- Original failed r001, all original frozen inputs and other three batch91 candidates remain unchanged.

## Scientific and visual scope
Primary text, Fig9 and the planning concept were personally inspected. The result remains an artistic selection of the published low-tree macrophyllous hypothesis, not a complete fossil, unique proven crown or additional Callixylon asset. Broad paired paddles, ascending woody framework, scars and modest roots remain readable. No new static visual defect was found. Copyrighted primary pixels are consult-only and not copied into this QA package.

See independent-report.json and its bound detailed reports for per-leaf measurements, numerical derivation, per-view observations and raw execution provenance.

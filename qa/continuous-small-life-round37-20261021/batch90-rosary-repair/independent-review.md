# Independent differential review: Rosary r002

PASS for independent static-stylized-v1 candidate acceptance only. GPU and scene are unknown/not run. No formal, user, website, release or live approval.

Fixed source commit: afa7e3514b5c346794c1a5e6dae59ebb6645d1a6

## Corrected original defect

The original r001 failure and immutable2.7–3.2mm freeze are preserved. Actual exported r002 geometry contains2249 positive chamber-contribution triangles in13 connected patches. Every complete triangle is inside one unchanged original chamber disk. All78 outside normal probes have exactly zero chamber contribution. The original3.2/3.5/3.8mm failure points are exactly on the exported host plane. Actual normal support semiradii are2.706882743–3.193794516mm. This is not a contour-height pass or a widened tolerance.

The independent check freshly reopened the source and recomputed the unchanged neck-only field, decoded actual indexed GLB triangles using a separately written decoder, and mapped every exported vertex to the reopened source. Convex-disk vertex containment proves whole-triangle containment. The new20nm inward guard is constructed inside the original bounds, not an acceptance epsilon.

## Independent checks

- Source:2023 authored/evaluated vertices,4042 triangles, one closed volume, no boundary/nonmanifold edges. Independently exported GLB is byte-identical.
- Khronos:0 errors/0 warnings. Own Three r180 parse:4042 triangles,3materials/meshes, matching bounds.
- Exact actual size:100.00000149 ×74.00000095 ×12.29999959mm.13chamber peaks; connected centerline minimum relief1.19228712mm. Chamber/neck breadth ratio3.25258 at an explicitly reported80µm readability contour, not used for radius acceptance.
- Original path, chamber formula, centers/heights, seed, palette, freeze and references unchanged.124common neck-only vertex heights and all28bottom vertices identical. Original slab footprint, bounds, renderer and render config identical. Retriangulated neck interpolation is not falsely claimed byte-identical.
- Original queued builds PID46 and71 verified against exact input/output hashes, request/results, raw logs and byte-identical GLBs. No redundant rebuilds.
-109committed payload blobs and215pins checked. Final proof binding precedes genuine8-frame render. Each512frame personally inspected; all sheet crops pixel-exact.
- Primary source text and actual PRI76855 pixels rechecked. Original concept panels inspected. Factual uncertainty and consult-only rights retained.

## Precision and scope

The old3.5mm defect is1.251848310µm above nominal host9mm. The same hit is1.252235741µm above exported float32 host because nominal9mm rounds down0.000387430µm. That offset does not excuse the original real tail. New constant host triangles evaluate exactly to exported host; no global epsilon masks a positive chamber increment.

Unrelated three batch90 assets were not rebuilt. The r001 failure remains historical truth. This closes only the fixed r002 static differential review, not GPU, composed scene or publication gates. No candidate/queue/source mutation, push, PR, upload, merge, release or authority-count change occurred.

See independent-review.json and own-exact-geometry.json for exact evidence identities and all13component dimensions. A preliminary checker call failed only on an outside-root report-path formatting restriction; its script/log/report are preserved and the corrected invocation used byte-identical committed request/result snapshots.

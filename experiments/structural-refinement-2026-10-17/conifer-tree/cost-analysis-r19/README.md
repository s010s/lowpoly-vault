# Read-only cost audit: r12 /r15 /frozen r19

All original candidate GLBs, source files and frozen r19 pilot evidence remain unchanged. This audit parses actual accessors and buffer views, not triangle-based estimates. Scripts and raw results: `analyze_costs.py`, `byte-accounting.json`, `transport-compression.json`.

## Actual byte composition

| Storage | r12 | r15 | r19 | r19 share |
| --- | ---: | ---: | ---: | ---: |
| FLOAT32 POSITION |175,080 |188,616 |358,584 |42.95% |
| FLOAT32 NORMAL |175,080 |188,616 |358,584 |42.95% |
| UINT16 indices |112,236 |98,700 |114,312 |13.69% |
| JSON chunk +container headers |3,388 |3,388 |3,360 |0.40% |
| **Total bytes** |**465,784** |**479,320** |**834,840** |100% |

All3 files contain exactly POSITION and NORMAL attributes,9 accessors,9 buffer views,3 materials/primitives and0 textures. No UV, tangent, color, skin or animation attribute bloat. BIN padding/unreferenced bytes: **0**. Unused vertices: **0**. Exact duplicate (position,normal) vertices, including across the3 primitives: **0**. All index streams already use16-bit, not wasteful32-bit.

## Why almost the same triangle count can cost much more

The primary change is boundary/endpoint count, not excessive export splitting. r12 has10,549 source vertices and14,590 export vertices; r15 has11,677 /15,718; r19 has25,325 /29,882. Separate thin strips have many independent ends and little closed-surface vertex reuse.

r12 foliage alone:9,024 vertices /15,792 triangles. r19 foliage alone:23,542 vertices /15,794 triangles. Thus foliage triangles are effectively unchanged (+2), while foliage position+normal storage grows348,432 bytes. With the12-byte leaf-index delta, foliage explains348,444 of r19's369,056-byte increase (94.4%). Added upper wood supports explain20,640 bytes; JSON is28 bytes smaller.

Exact decomposition of the r19 −r12 increase:

- Additional authored-vertex attribute storage: **354,624 B** (96.1% of increase).
- Additional export split vertices: **12,384 B** (3.4%).
- Additional indices: **2,076 B** (0.56%).
- JSON/container difference: **−28 B**.

The export split increment goes from4,041 to4,557 (+516); this is mostly the344-triangle fine support addition with flat normals, not a mysterious duplicate foliage layer. r19 main-wood positions1,783 become6,340 position/normal vertices because flat faces need distinct normals. Foliage has23,542 unique positions and23,542 unique position/normal tuples, so there is no extra foliage normal seam split to weld away.

Compared with r15, the exact355,520-byte delta is327,552 B authored-vertex attributes +12,384 B split-vertex attributes +15,612 B indices −28 B JSON.

## What exact lossless cleanup can and cannot do

There is no significant zero-error vertex/buffer garbage to remove. Removing **all** names and extras would save at most752 B (0.09%) and discard useful identity/license metadata, so it is not recommended. Reordering indices alone preserves the raw byte count; it can only influence compressed transport or GPU cache behavior, which needs separate measurement. Welding all equal positions would destroy required wood normal discontinuities. Removing NORMAL would change default GLTFLoader shading toward flat shading and is not a lossless A appearance preservation. Splitting every spray into8-bit-index primitives could reduce index bytes but substantially increase draw submissions; it violates the current3-primitive baseline and is not recommended.

Measured lossless HTTP/archive encoding, with byte-identical decompression:

| File | raw GLB | gzip9 | Brotli11 |
| --- | ---: | ---: | ---: |
| r12 |465,784 |287,822 |243,078 |
| r15 |479,320 |313,994 |277,214 |
| r19 |834,840 |521,340 |429,349 |

These are encoded transfer sizes, not standalone GLB sizes or GPU allocations. Serving Brotli/gzip would preserve every original GLB byte and needs ordinary browser HTTP decoding, but whether hosting currently enables it must be checked by integration; already compressed responses cannot be counted again. No hosting configuration was changed.

## Storage precision options, no A silhouette redesign

The first proposed delivery option leaves every FLOAT32 position, triangle/index order, material and node transform exact, changing only normal storage:

- **16-bit normalized normals**, required KHR_mesh_quantization,8-byte aligned stride: payload reduction119,528 B. The actual separate r20 probe is **715,500 B**, saving119,340 B /14.29% after188 B schema overhead. Measured normal error: max0.001443°, mean0.000661°, p990.001227°. This is bounded normal precision loss, not mathematical losslessness.
- **8-bit normalized normals**,4-byte stride: theoretical raw size about595,784 B plus small schema overhead. Measured max angular error0.372° and max unit-length error0.006335; this exceeds the current static normal-length tolerance before renormalization and has greater shading risk. Not selected or written as a candidate.
- **16-bit positions** could save another119,528 B but changes coordinates, up to0.0537 mm per component /0.0931 mm3D in the full7.04m range. Not used. We are not forcing a472KB target by moving geometry or accepting extra errors.

KHR_mesh_quantization is a declared required format extension, not Draco/Meshopt compression. The pinned Three.js0.180.0 GLTFLoader includes its extension handler and existing normalized buffer-attribute path; no external decoder/WASM dependency is added. Primary format/alignment source: https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_mesh_quantization . Local pinned loader evidence is the existing `modal-fix/node_modules/three/examples/jsm/loaders/GLTFLoader.js` extension handler and normalized accessor path. Real target renderer support and scene behavior still require actual GPU tests.

## Actual normal16 probe evidence and limits

r20 is separate; r19 is not overwritten. `candidate-r20/geometry-equivalence.report.json` proves exact positions, indices/order, material dictionaries and node/scene transforms. Official Khronos validation of the new file:0 errors /0 warnings.

Four identical-camera512px CPU Cycles GLB reimports were measured against frozen r19: hero/color detail/clay detail/whole clay. They are **not pixel-identical**. Changed pixel fractions are0.0744%,0.4292%,0.4490%,0.0744%; mean absolute8-bit channel differences0.000538,0.003512,0.005535,0.000849. Maximum isolated channel difference is9/255 in clay detail; RMSE there is0.0951/255. These small measured differences are explicitly retained for independent visual comparison; arithmetic and maker inspection do not certify perceptual equivalence.

Proceed only as a new storage-precision candidate, preserving original r19 and requiring independent confirmation of the normal16 appearance, full-angle technical/rebuild evidence and exact Three.js1/16/32-clone scene tests. None of these byte or CPU-image figures is a GPU performance measurement.

Code MIT; report CC-BY-4.0, Leon Made This /s010s.

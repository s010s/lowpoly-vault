# Primary-source ledger

Retrieved 2026-10-17. Living pages can change; repository sources are pinned where practical. Normative constraints, vendor recommendations and project observations must not be conflated. No universal numeric performance budget is attributed to glTF.

## S01 — glTF 2.0.1

[Original source](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)

- Evidence: normative
- Version/date: 2021-10-11
- Supports: Format semantics; no universal MB or triangle performance limit.

## S02 — Khronos Asset Creation Guidelines 2.0

[Original source](https://github.com/KhronosGroup/3DC-Asset-Creation/blob/3ba6cf7045f0b3bc7d845bc518ccdbd1356a3b93/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md)

- Evidence: recommendation
- Version/date: 2.0.0 August 2025; snapshot 2026-07-11
- Supports: Source/delivery, instancing, seams, textures, animation; several full chapters remain WIP.

## S03 — Khronos 2020 creation guidelines

[Original source](https://www.khronos.org/assets/uploads/apis/3DCommerce-Realtime-sset-Creation-Guidelines_Jul20.pdf)

- Evidence: historical recommendation
- Version/date: July 2020
- Supports: The <5 MB / 100k triangle advice is commerce publishing guidance, not a modern populated-scene limit.

## S04 — KHR_texture_basisu

[Original source](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_texture_basisu/README.md)

- Evidence: normative plus encoding advice
- Version/date: Complete, Ratified; snapshot 2026-10-13
- Supports: KTX2 ETC1S/UASTC, color spaces, mips, device-dependent transcode and non-color fallback.

## S05 — EXT_meshopt_compression

[Original source](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Vendor/EXT_meshopt_compression/README.md)

- Evidence: normative
- Version/date: Complete, Ratified; snapshot 2026-10-13
- Supports: Buffer-view compression includes geometry, morphs, animation and instance transforms.

## S06 — KHR_draco_mesh_compression

[Original source](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_draco_mesh_compression/README.md)

- Evidence: normative
- Version/date: Complete, Ratified; snapshot 2026-10-13
- Supports: Mesh-primitive geometry codec, not arbitrary animation/texture/LOD optimization.

## S07 — KHR_mesh_quantization

[Original source](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_mesh_quantization/README.md)

- Evidence: normative
- Version/date: Complete, Ratified; snapshot 2026-10-13
- Supports: Smaller vertex storage; illustrative PBR layout 48 to 20 B/vertex; precision and consumer support.

## S08 — EXT_mesh_gpu_instancing

[Original source](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Vendor/EXT_mesh_gpu_instancing/README.md)

- Evidence: normative
- Version/date: Complete, Ratified; snapshot 2026-10-13
- Supports: Repeated geometry with fewer calls; node reuse and GPU instancing differ.

## S09 — KHR_meshopt_compression

[Original source](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_meshopt_compression/README.md)

- Evidence: draft status
- Version/date: Release Candidate at retrieval
- Supports: Do not silently replace EXT in pinned r180.

## S10 — meshoptimizer

[Original source](https://github.com/zeux/meshoptimizer/tree/f0a684f11ead064e176775c9b796f82a55910e92)

- Evidence: implementation guidance
- Version/date: snapshot 2026-10-14
- Supports: Cache/fetch/quantization ordering, attribute discontinuities and hardware-dependent overdraw gains.

## S11 — gltfpack

[Original source](https://meshoptimizer.org/gltf/)

- Evidence: tool guidance
- Version/date: living documentation
- Supports: Optimization can change hierarchy, material, animation and quantization; test emitted asset.

## S12 — Basis Universal

[Original source](https://github.com/BinomialLLC/basis_universal/tree/1706f948a2f0992d7a6dc2a909f35690b508571c)

- Evidence: implementation guidance
- Version/date: snapshot 2026-10-16
- Supports: Universal GPU transcoding differs from JPEG/WebP; quality, target format and overhead matter.

## S13 — glTF Transform CLI

[Original source](https://gltf-transform.dev/cli)

- Evidence: tool guidance
- Version/date: living documentation
- Supports: Inspect and use controlled individual transforms, not only broad optimize presets.

## S14 — glTF Transform textureCompress

[Original source](https://gltf-transform.dev/modules/functions/functions/textureCompress)

- Evidence: tool API
- Version/date: living documentation
- Supports: Resize/transcode by texture use with explicit size and quality.

## S15 — Three.js textures

[Original source](https://threejs.org/manual/pages/textures.html)

- Evidence: engine guidance
- Version/date: living documentation
- Supports: Compressed image file size differs from GPU allocation; RGBA with mips approx w*h*4*4/3.

## S16 — Three.js many objects

[Original source](https://threejs.org/manual/pages/optimize-lots-of-objects.html)

- Evidence: engine guidance
- Version/date: living documentation
- Supports: Submission and scene graph overhead; combining objects has trade-offs.

## S17 — Three.js Material

[Original source](https://threejs.org/docs/pages/Material.html)

- Evidence: engine API
- Version/date: living documentation; r180 checked locally
- Supports: Double-sided transparent two-pass behavior; forceSinglePass is not universally visually safe.

## S18 — Three.js InstancedMesh

[Original source](https://threejs.org/docs/pages/InstancedMesh.html)

- Evidence: engine API
- Version/date: living documentation
- Supports: Shared geometry/material and bounds.

## S19 — Three.js LOD

[Original source](https://threejs.org/docs/pages/LOD.html)

- Evidence: engine API
- Version/date: living documentation
- Supports: Distance switching/hysteresis; thresholds are application-specific.

## S20 — Three.js disposal

[Original source](https://threejs.org/manual/pages/how-to-dispose-of-objects.html)

- Evidence: engine guidance
- Version/date: living documentation
- Supports: GPU and ImageBitmap lifetime; shared resource ownership/ref counting.

## S21 — Three.js shadows

[Original source](https://threejs.org/manual/pages/shadows.html)

- Evidence: engine guidance
- Version/date: living documentation
- Supports: Extra scene passes; point-light shadow uses six views.

## S22 — Three.js on-demand rendering

[Original source](https://threejs.org/manual/pages/rendering-on-demand.html)

- Evidence: engine guidance
- Version/date: living documentation
- Supports: Avoid continuously rendering unchanged inspection views.

## S23 — Three.js renderer source

[Original source](https://github.com/mrdoob/three.js/blob/r180/src/renderers/WebGLRenderer.js)

- Evidence: pinned source code
- Version/date: r180 / 0.180.0
- Supports: Default info reset follows shadows; autoReset=false/reset once for all-pass accounting.

## S24 — Three.js counter source

[Original source](https://github.com/mrdoob/three.js/blob/r180/src/renderers/webgl/WebGLInfo.js)

- Evidence: pinned source code
- Version/date: r180 / 0.180.0
- Supports: Memory values are counts; triangles multiply instanceCount.

## S25 — Three.js GLTFLoader

[Original source](https://github.com/mrdoob/three.js/blob/r180/examples/jsm/loaders/GLTFLoader.js)

- Evidence: pinned source code
- Version/date: r180 / 0.180.0
- Supports: Explicit Draco/Meshopt/KTX2 setup; supports EXT_meshopt.

## S26 — Three.js KTX2Loader

[Original source](https://threejs.org/docs/pages/KTX2Loader.html)

- Evidence: engine API
- Version/date: living documentation
- Supports: detectSupport and target-format selection; transcoder deployment.

## S27 — MDN WebGL best practices

[Original source](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices)

- Evidence: browser guidance
- Version/date: living documentation
- Supports: No portable max-VRAM query; physical pixels, memory/caches, mips/compression.

## S28 — MDN disjoint timer query

[Original source](https://developer.mozilla.org/en-US/docs/Web/API/EXT_disjoint_timer_query)

- Evidence: browser API
- Version/date: living documentation
- Supports: Optional GPU timing; reject disjoint results; use corresponding WebGL2 API when applicable.

## S29 — Unity mobile art optimization

[Original source](https://unity.com/how-to/mobile-game-optimization-tips-part-1)

- Evidence: vendor recommendation
- Version/date: publication date unstated
- Supports: Silhouette first, material LOD, tiny/static assets may not need LOD; independent map sizes.

## S30 — Unreal mobile performance

[Original source](https://dev.epicgames.com/documentation/en-us/unreal-engine/performance-guidelines-for-mobile-devices-in-unreal-engine?application_version=5.6)

- Evidence: vendor/historical hardware guidance
- Version/date: UE 5.6 documentation view
- Supports: 500k triangles/700 calls text tied to old iPad4/Air ~30fps, not WebGL baseline.

## S31 — PlayCanvas optimization

[Original source](https://developer.playcanvas.com/user-manual/optimization/guidelines/)

- Evidence: Web3D vendor recommendation
- Version/date: living documentation
- Supports: Rough low-end mobile 100–200 calls; shaders, DPR, alpha, shadows, on-demand rendering.

## S32 — model-viewer loading

[Original source](https://modelviewer.dev/examples/loading/)

- Evidence: viewer guidance/demo
- Version/date: living documentation
- Supports: Poster/lazy loading, decoder cold cost and dynamic resolution.

## S33 — model-viewer API

[Original source](https://modelviewer.dev/docs/index.html)

- Evidence: viewer API
- Version/date: living documentation
- Supports: Model-count cache is not a byte limit.

## S34 — Khronos Asset Auditor

[Original source](https://www.khronos.org/blog/khronos-gltf-asset-auditor)

- Evidence: official tool rationale
- Version/date: 2023 release-era article
- Supports: Use-case profiles distinct from format validation.

## S35 — glTF Validator

[Original source](https://github.com/KhronosGroup/glTF-Validator)

- Evidence: official tool
- Version/date: project pins 2.0.0-dev.3.10
- Supports: Conformance does not establish beauty, scientific correctness or frame rate.

## S36 — Blender glTF exporter

[Original source](https://github.com/KhronosGroup/glTF-Blender-IO/blob/main/docs/blender_docs/scene_gltf2.rst)

- Evidence: exporter guidance
- Version/date: living documentation; project Blender 4.3 baseline
- Supports: UV/hard-normal seams split runtime vertices; exportable material graph.

## S37 — Khronos official sample assets

[Original source](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/edc7c9e67c639d230715049ee31f9a96a6babbbe)

- Evidence: reproducible metadata
- Version/date: snapshot 2026-10-02
- Supports: Fox, DamagedHelmet, FlightHelmet exact file/mesh metadata; not FPS or quality rankings.

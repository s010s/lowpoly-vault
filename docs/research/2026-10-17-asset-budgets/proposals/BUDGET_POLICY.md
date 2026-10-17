# Proposed Skill addition: budget by use, verify the scene

Status: review proposal, not an adopted production default. Baseline: lowpoly-vault e4019e2, Three.js 0.180.0. Date: 2026-10-17.

## Purpose and contract

Produce editable, proportionally convincing low-poly assets suitable for a mobile/desktop Web3D museum. A budget belongs to a visual role, projected size, visible instance count and target consumer. Neither glTF nor this proposal supplies a universal good-asset MB/triangle limit.

Use [the profile table](budget-profiles.proposed.json) as planning allocations only. Nominate and calibrate devices and a representative scene before approving a profile. The accepted 471,784-byte Triceratops is a bounded style/size decision, not a 500 KB cap or a scientific/runtime pass.

Freeze the brief before production:
- Identity, factual references, dimensions, required silhouette landmarks and purpose.
- Role, nearest inspection, projected pixel range, FOV, physical drawing buffer and maximum visible instances.
- Target scene/device, lighting/shadows/alpha, animation and fallback.
- Explicit byte, exported triangle/vertex, primitive/material and resident-resource limits.
- Which values are planning goals versus approved hard gates. Do not invent a hard gate after viewing a candidate.

Lower complexity is welcome when the brief is met; ranges are not minimum geometry quotas. Important thin structures may justify exceptions.

## Five independent cost ledgers

1. Distribution: stored_glb_bytes, all external dependencies, actual cold_transfer_bytes including required decoder/transcoder fetches, warm transfer and first useful view. Record HTTP content encoding/cache state; do not assume server Brotli.
2. CPU/load: parse/decode/transcode, image upload scheduling, transient buffers, main-thread stalls and animation update.
3. Resident resources: unique decoded geometry/animation and texture allocations, actual runtime format/mips and sharing. Render targets, depth/MSAA, shadows and PMREM belong in a separate scene ledger. Estimates are not measured VRAM.
4. Per-frame: actual all-pass calls/submitted triangles, CPU and optional valid GPU timing, physical pixels, alpha overdraw, shadows and shader features.
5. Source: .blend, original maps, generators, license/provenance, tool versions/parameters and derived hashes. Source archive size is not the initial web payload.

Unknown is not zero. Three r180 memory.textures/geometries are counts. Its default info reset occurs after shadow rendering: use autoReset=false, reset once before the complete application frame and sample after every pass. [Renderer](https://github.com/mrdoob/three.js/blob/r180/src/renderers/WebGLRenderer.js), [counters](https://github.com/mrdoob/three.js/blob/r180/src/renderers/webgl/WebGLInfo.js)

## Material tiers

- Palette: flat/vertex colors or a small shared palette, scalar roughness/metalness.
- Color-lite: one appropriately sized base-color map; start 256–512 for small assets, test 1K when occupancy justifies it.
- Selective-detail: independently justified normal/nonconstant packed ORM; maps need not share dimensions.
- Inspection-enhanced: larger maps/advanced material features only as on-demand options with a lightweight fallback and device/scene evidence.

Compare exact exported GLBs under matched framing, camera, lighting, exposure and color management, at intended near and ordinary distances. Reject cost without visible benefit. Color enrichment does not repair silhouette or anatomy. User style acceptance does not replace factual/runtime review.

For RGBA8 estimate exact mip sums and disclose dimensions, format and allocation count. JPEG/PNG/WebP file bytes are not GPU allocation. KTX2 needs actual transcode target or named conservative fallback. [Three textures](https://threejs.org/manual/pages/textures.html), [KHR_texture_basisu](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_texture_basisu/README.md)

## Optimization order

1. Pass silhouette/proportion/factual review and capture baseline inventory.
2. Remove proven-unused attributes/maps/materials/nodes/clips. Remove tangents only if not needed by the material/runtime.
3. Deduplicate resources; preserve interaction names, meaningful hierarchy and useful culling granularity.
4. Remove/resize maps with controlled A/B; avoid automatic full PBR stacks and constant-value textures.
5. Reduce geometry by screen-space effect and repetition; record exported vertices because UV/hard-normal seams split them.
6. Evaluate quantization/cache ordering and transport compression separately from LOD/draw calls.
7. Test a populated scene, all passes, load peaks and resource release on actual target devices; fix the measured bottleneck.

Pin optimizer/exporter versions and commands. Broad presets can change hierarchy/materials/animation/quantization. Validate and render emitted bytes, not only source viewport images. [glTF Transform](https://gltf-transform.dev/cli), [gltfpack](https://meshoptimizer.org/gltf/), [exporter](https://github.com/KhronosGroup/glTF-Blender-IO/blob/main/docs/blender_docs/scene_gltf2.rst)

## Delivery variants and codecs

Preserve editable source and high-quality original maps. Keep a portable GLB where interoperability matters. Optimized web variants explicitly declare required extensions, decoder versions, hashes and fallback.

Compare Meshopt/Draco at matched geometry/precision/quality. Neither automatically removes texture or render-call costs. Meshopt buffer-view compression can include animations; Draco's glTF extension concerns mesh-primitive geometry. Count cold decoder/transcoder downloads and warm amortization.

KTX2/BasisU needs real-format and transcode tests, especially for normal/ORM data and RGBA fallback. Do not assume identical formats on all devices. The pinned Three r180 consumer supports EXT_meshopt; do not silently substitute KHR_meshopt, a Release Candidate in this research snapshot. Separate negotiated variants can avoid embedding both compressed and fallback images in every required download.

[Meshopt](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Vendor/EXT_meshopt_compression/README.md), [Draco](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_draco_mesh_compression/README.md), [r180 loader](https://github.com/mrdoob/three.js/blob/r180/examples/jsm/loaders/GLTFLoader.js), [model-viewer loading](https://modelviewer.dev/examples/loading/)

## Repetition, LOD, atlases and streaming

Budget visible instances and all passes, not only unique geometry. Instancing saves submissions/shared storage, not per-instance triangle or shading work. Use spatially bounded batches with correct bounds/culling.

Choose LOD by projected size/error, test multiple views/transitions, add hysteresis and simplify material/shadow cost too. Tiny meshes or fixed inspection views may not need extra LOD. Put LODs in separately loaded files if initial transfer savings are intended.

Share biome/trim/palette resources with mip-safe gutters and versioned membership. Atlases do not inherently reduce texels; a huge atlas forces unrelated resources resident. Self-contained GLB versus external shared texture delivery must be an explicit contract.

Alpha-heavy foliage, double-sided transparency, animated crowds and repeated shadow casters are scene stress cases. [InstancedMesh](https://threejs.org/docs/pages/InstancedMesh.html), [LOD](https://threejs.org/docs/pages/LOD.html), [Material](https://threejs.org/docs/pages/Material.html), [Unity](https://unity.com/how-to/mobile-game-optimization-tips-part-1)

A 10,000-item library is not a 10,000-item resident scene. Use paginated metadata, viewport-local posters, bounded image decode/concurrency, current-room loading and on-demand enhancement/source downloads. Enforce byte caches and shared-resource reference counts. Dispose GPU objects and CPU ImageBitmaps safely; render static views on demand. [Disposal](https://threejs.org/manual/pages/how-to-dispose-of-objects.html), [on demand](https://threejs.org/manual/pages/rendering-on-demand.html), [MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices)

## Gates and exceptions

Keep technical, visual/form, factual, runtime and scene evidence independent and bound to exact artifact hashes. Record user acceptance scope separately. Unknown required evidence is a hold. Unsupported codecs/skins/animations stay unsupported until positive/negative fixtures and consumer tests exist.

An exception specifies asset hash, exceeded field/new upper limit, semantic/visual reason, device/scene evidence, lightweight fallback, approver and validity/review conditions. A hero exception does not authorize unlimited replication or a library-wide default.

The proposed schema/example/checker illustrate evidence structure; they do not replace the existing pipeline, glTF Validator or human/device QA. Reconcile with the repository's frozen-brief format before adoption. No proposed numeric profile is automatically production-approved.

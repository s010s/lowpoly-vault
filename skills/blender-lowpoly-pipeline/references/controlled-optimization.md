# Controlled form, surface and delivery optimization

Use this checklist for a size/material revision after the asset's intended viewing role is known. Read the [measured case](../../../docs/case-studies/lightweight-triceratops.md) for the evidence behind these decisions. Numerical limits still come from the current brief and [role-based budgeting](../../lowpoly-art-direction/references/asset-budgeting.md), not from that one example.

## Before spending on detail

- Name the required improvement and its viewing distance/projected size. Inspect silhouette, neutral clay, attachments and identifying internal relief first. A higher count or detailed normal map does not establish better structure.
- Freeze the baseline GLB, brief and reference ledger. Keep the authoring source and failed attempts recoverable. Distinguish a geometry experiment from a surface-only comparison.
- For a surface A/B, verify exported positions, normals, indices, pose and relevant UVs; hold camera, framing, lights, exposure, color management and render settings fixed. A count match alone does not prove geometry identity. If an atlas necessarily changes UVs/splits, report that change and compare triangle positions/normals separately.
- Do not change flat/smooth normals between variants and attribute the result to texture. Include an unlit base-color view and neutral/alternate-key views when they help identify which surface channel contributes.

## Compare fair delivery costs

- First remove demonstrably unused attributes or resources from the control without changing required appearance, animation or export behavior. Revalidate retained arrays/materials and render when equivalence is uncertain. Tangents are not universally removable; normal mapping and the consuming renderer determine whether they are required or generated.
- Report original and optimized controls by their own filenames/hashes. Do not relabel an original-control render as a fresh optimized-GLB render. An identity check supports a bounded equivalence claim, not an invented render run.
- Compare the smallest useful alternatives: palette factors, color-only atlas, and extra PBR channels only where they visibly help. Keep high-detail editable source/maps even when delivery uses a smaller tier.
- Record exported triangle and POSITION-stream counts, primitives/materials, geometry bytes, embedded image bytes/dimensions, total GLB bytes and relevant extensions. Consolidating materials may reduce primitives and duplicate streams; verify the export rather than assuming one material means one draw call.
- Keep four costs separate: editable source/archive storage; network-delivered model/textures; decoded CPU/GPU memory estimates; measured rendering/parse/decode performance. Preview sequences and first-load decoder JS/WASM are additional delivery costs, not hidden inside the GLB count. Useful separate fields are `stored_glb_bytes`, `cold_transfer_bytes`, `decoded_geometry_bytes` and `texture_resident_estimate_bytes`, with stated format/mip/instance assumptions; keep these distinct even before a final budget schema is adopted.
- Choose texture and geometry compression from measured visual benefit, channel/alpha needs, required extensions and target-runtime support. Account for cold decoder fetch/startup and warm-cache reuse separately. A smaller image/GLB is not proof of lower GPU memory or a faster first view. Do not present JPEG, WebP, KTX2, Draco or meshopt as automatically best.
- State memory assumptions. An RGBA8 full mip-chain estimate is approximately width × height × 4 × 4/3 per image; actual allocation/transcoding/sharing can differ. Measure actual target devices before asserting a GPU saving.

## Fresh-import image guard

A Blender 4.3.2 study exposed a review-script failure: redundantly calling `Image.pack()` on an already-packed imported JPEG with an empty filepath removed its packed payload and produced magenta. The frozen GLB remained valid and unchanged. This is a demonstrated failure of that recipe, not proof that every Blender version or packed image behaves the same way.

For the static embedded-image profile:

1. Extract the expected embedded image bytes/hashes from the frozen GLB before importing.
2. Fresh-import the GLB and identify its required images/material links. If reusing a studio, distinguish its images from the imported asset's images; do not assert one image hash across unrelated textures.
3. Preserve already-packed images. Only pack an unpacked file image when a valid readable source is available and packing is actually needed. A safe guard in the tested recipe was `if image.packed_file is None: image.pack()`; that guard alone is not a complete multi-image or tiled-image implementation.
4. Assert each required packed payload exists and matches its expected encoded hash for this unchanged embedded-image workflow. If a deliberate image conversion occurred, bind the new bytes and revalidate rather than insisting the old hash survives. Check again after save/reopen when the saved source is a deliverable.
5. Inspect a cheap exact-GLB preview before expensive renders. Missing colors or magenta blocks are a failed preflight even if Khronos validation passed. Investigate import/script/image state before altering a valid GLB to compensate.
6. Preserve the failing recipe, state log and image under a failed-attempt label. Bind corrected images to the unchanged GLB plus corrected recipe/config; never silently replace failed evidence and claim it passed all along.

The repository's `render_candidate_views.py` does not call `Image.pack()`; do not add a redundant repack stage to it. The corrected study recipe and its failed predecessor are preserved in the case's recovery archive.

## Decide and stop

- Have an independent reviewer inspect the exact-GLB evidence before receiving the maker's verdict. Record concrete retained features, losses and defects by view; keep unseen angles and factual/runtime obligations unknown.
- A smaller tier can be acceptable for a stated use while visibly inferior at close range. Describe the tradeoff; do not call it equal quality or an artistic upgrade unless the comparison supports that claim.
- Keep style/size acceptance separate from anatomy, structure, runtime and production approval. A user accepting a 472 KB example does not approve every similarly sized model or establish a global cap.
- After a finite comparison reaches a decision, stop. Further modeling, full QA, batch replacement and publication each require the applicable brief and authorization. Preserve rejected variants and the reason for rejection.

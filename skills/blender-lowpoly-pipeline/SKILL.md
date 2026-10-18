---
name: blender-lowpoly-pipeline
description: Create reproducible original low-poly Blender assets, GLB exports, previews, and QA reports for a Three.js prehistoric museum and its environment library. Use for new asset production or revisions, not for copying or relicensing third-party models.
---

# Build low-poly museum assets


## Practical children’s-world prop tier

For the approved small-fauna batch, follow [pragmatic-props.md](references/pragmatic-props.md). Its explicit environment-prop tier permits artistic colors, textures, pose, proportions and harmless detail while retaining recognizable basic structure and reliable exports. Use representative references without exhaustive fossil closure; use a descriptive inspired-by label when identity is loose. Fine uncertainty is advisory. Cross-period curation is allowed in the labeled imagined world, without a scientific coexistence claim. Default QA is six to eight useful images and one shared poster, zero orbit; one consolidated fresh independent review and at most one planned cosmetic repair. The user need not review every model. Hero/scientific-reconstruction work keeps its separately requested stronger brief. Existing accepted artifacts, hashes, licenses and publication records remain unchanged.

## Scope and runtime

Honor the requested environment, model, and repository permissions. For lowpoly-vault the current instruction is cloud-only, no user Mac, with Blender modeling performed using GPT-6 Astra at xhigh reasoning. This skill grants no publishing or Git authority.

The researched baseline is Blender 4.3.2, verified at `/usr/bin/blender` on 2026-10-16. Probe the actual runtime and exporter RNA before using version-sensitive options. Pin Blender, the generator seed, Python source, parameters, exporter settings, and the consuming Three.js version in build metadata. Do not silently replace the requested model or Blender environment.

Read [standardized-pipeline.md](references/standardized-pipeline.md) for the required brief-to-review lifecycle and parallel batch boundaries. For surface or delivery-size revisions, use the [controlled optimization checklist](references/controlled-optimization.md) and the [measured lightweight case study](../../docs/case-studies/lightweight-triceratops.md). Use [production-contract.md](references/production-contract.md) for asset decisions and [qa-design.md](references/qa-design.md) for existing executable checks. Official references and observed runtime facts are in [sources.md](references/sources.md).

## Asset contract

Deliver one editable `.blend`, a standalone `.glb`, the deterministic Blender Python generator and parameters, transparent/neutral previews, and machine-readable metadata plus QA. Write to `assets/<collection_id>/<category>/<slug>/`; default collection is `prehistoric`. Keep the source and presentation scene separate from the exported asset. A generated asset is original geometry; reference photos, diagrams, and scientific facts still need provenance. State artistic reconstruction choices without claiming uncertain anatomy is settled.

Use a dedicated `EXPORT` collection with a single identity-transform root named for the asset. Place the root at the floor contact center (or the explicitly recorded mounting point for a swimming/flying specimen). Author in meters: Blender Z-up and -Y forward, exported glTF Y-up and +Z forward. Retain real-world size across the collection; never independently normalize each asset to a unit cube. Make any display scaling a museum-layout concern.

Prefer deliberate profile/loft topology and visible silhouette features over assembling an organic shape entirely from untouched primitives. Spend geometry on head profile, pose, limb separation, tail taper, and defining anatomy. Choose smooth, faceted or mixed normals deliberately, with a consistent palette and a PBR-compatible material graph. Avoid unnecessary microgeometry, hidden internal surfaces, and transparent overlap.

Choose a palette-only or textured-PBR profile in the brief. The current refined-low-poly direction permits original baked base-color, roughness and normal detail: low-poly does not mean flat color or low surface detail. Keep geometry and texture budgets separate. Export portable Principled/glTF materials, normals and required UV/tangent data, with no source-only shader dependency. The first pack's texture-free static baseline remains a valid historical profile, not a library-wide restriction. Rigs, animation, instances and required extensions need explicit profile tests.

## Reproducible production

1. Start from factory state and build deterministically. Prefer the data API (`bpy.data.meshes.new`, `Mesh.from_pydata`, `bmesh`) over context-sensitive operators; set active object and mode explicitly when an operator is unavoidable. Check invalid mesh input rather than relying on automatic repair.
2. Store editable semantic parts, material names, palette values, seed, measurements, and source references. Apply or evaluate modifiers deliberately. For mirrored geometry avoid exporting negative determinant transforms; fix winding when baking a reflection. Do not destructively join a rig or destroy useful editable parts merely to reduce object count.
3. Run source QA on evaluated geometry. Save the `.blend` before temporary preview scene changes. Export only the intended root and descendants with explicit flags; see the tested exporter configuration in the production contract.
4. Inspect the emitted GLB, run Khronos glTF Validator, and load that exact GLB in the pinned Three.js viewer. Source renders do not establish export correctness. Compare bounds, front direction, colors, silhouette, normals, and ground contact after export.
5. Produce hero 3/4 plus front/side/rear views with a consistent camera and lighting preset; inspect the actual images. Use a wireframe or clay view when topology/shading needs review. Record performance on the combined museum scene as well as individual assets.
6. Rebuild twice. Compare semantic metrics and a normalized geometry/material digest; byte-identical `.blend` files are not required. Record checksums of the delivered files for integrity. Deliver only after errors are zero, warnings are reviewed, and visual review is complete.

Freeze each candidate by asset ID, revision, brief/reference hashes and exact GLB hash. Run a fresh independent review task against the brief, reference ledger and actual export evidence, before sharing the maker's verdict. Keep visual craft, factual obligations, specification, parsing, GPU rendering and populated-scene performance separate. Use `scripts/validate_candidate.py` to check record/evidence integrity; it cannot certify beauty or truth. A failed or unknown required gate remains unapproved.

Use bounded headless processes for parallel production, not one serial GUI and not one process per planned asset. Read the queue contract linked from the standardized pipeline, coordinate shared CPU/memory capacity, and isolate every attempt's outputs. Quick full-angle evidence comes before expensive final renders; independent image reviewers can work while other assets build. A screenshot does not prove internal geometry or scientific correctness.

## Shared helper

The executable interface and verified runtime lessons are in [qa-design.md](references/qa-design.md). Use `scripts/asset_common.py` instead of rewriting export, color conversion, preview lighting, or output paths per asset. Run `scripts/validate_gltf.cjs` for official format validation and `scripts/test_qa_glb.py` for checker regression tests. Code is MIT; assets, rendered previews, documentation and Skill prose are CC-BY-4.0, attributed to Leon Made This / s010s.

## Acceptance boundaries

Do not label a local checker as a complete glTF validator. The bundled GLB audit intentionally covers only the static, uncompressed, embedded-buffer baseline and stops on unsupported content rather than passing it silently. Surface limitations and any skipped browser/GPU or validator stage. Numeric QA cannot certify species identity, beauty, scientific accuracy, or clean visual intersections.

Triangle, material, and file-size limits are configurable project budgets, not universal truths. The first environment pack's bands (T1 250–700, T2 700–1,400, T3 1,400–2,600) and the helper’s 12,000 ceiling are historical settings, not limits for every revision. Choose current limits with the [role-based budgeting framework](../lowpoly-art-direction/references/asset-budgeting.md) and measured performance. A successful 472 KB example does not establish a universal 500 KB cap. Never make an asset meet a budget by damaging its identifying silhouette.

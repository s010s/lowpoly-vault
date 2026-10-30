---
name: blender-lowpoly-pipeline
description: Build original concept-guided low-poly Blender assets, editable sources, GLB exports, exact-export previews and QA records. Use for bounded design studies or formal production revisions across the library; keep their acceptance and publication scopes distinct.
---

# Build original low-poly assets

## Scope and runtime

Honor the current task’s authorized execution environment, tool choices and repository permissions. Probe the actual runtime rather than treating a requested tool or model as verified. This skill grants no publishing or Git authority.

The researched baseline is Blender 4.3.2, verified at `/usr/bin/blender` on 2026-10-16. Probe the actual runtime and exporter RNA before using version-sensitive options. Pin Blender, the generator seed, Python source, parameters, exporter settings, and the consuming Three.js version in build metadata. Do not silently replace the requested model or Blender environment.

Read [standardized-pipeline.md](references/standardized-pipeline.md) for the required brief-to-review lifecycle and parallel batch boundaries. For surface or delivery-size revisions, use the [controlled optimization checklist](references/controlled-optimization.md) and the [measured lightweight case study](../../docs/case-studies/lightweight-triceratops.md). Use [production-contract.md](references/production-contract.md) for asset decisions and [qa-design.md](references/qa-design.md) for existing executable checks. Official references and observed runtime facts are in [sources.md](references/sources.md).

For externally generated creature bases, route through [Meshy → Blender](../meshy-blender-creatures/SKILL.md) before selecting a candidate profile. Reuse applicable export and QA checks here, but do not claim deterministic reconstruction of an external base. Preserve its source bytes and provenance; any incompatible formal profile needs an explicit scoped adjustment, not a relabeled pass.

## Choose the review scope, then establish the concept

For new concept-led geometry, generate genuine ImageGen concepts, inspect them, then freeze the modeling brief before construction. Use [concept-guided-lowpoly](../concept-guided-lowpoly/SKILL.md) for prompts, compatible multiview interpretation, retained provenance and the evidence sidecar. Existing export repairs or revisions may reuse a retained concept; do not invent a new pre-model concept after the model exists. Images guide silhouette, palette and material regions, not unique geometry or factual truth.

A **bounded design study** can deliver editable sources, exact-GLB views, measured checks and explicit unknowns for comparison. Keep it in an isolated study/revision folder; it does not enter production asset paths or release counts. A **formal production candidate** must additionally satisfy the frozen candidate profile, source/export/rebuild, factual/specification and target-runtime gates below. The study checker reports integrity/completeness, never production acceptance. The [standardized lifecycle](references/standardized-pipeline.md) owns both routes and their transition.

## Asset contract

Deliver one editable `.blend`, a standalone `.glb`, the deterministic Blender Python generator and parameters, exact-export transparent/neutral previews, and machine-readable metadata plus QA. For production assets, write to `assets/<collection_id>/<category>/<slug>/`; default collection is `prehistoric`. Keep the source and presentation scene separate from the exported asset. A generated asset is original geometry; reference photos, diagrams, and scientific facts still need provenance. State artistic reconstruction choices without claiming uncertain anatomy is settled.

Use a dedicated `EXPORT` collection with a single identity-transform root named for the asset. Place the root at the floor contact center (or the explicitly recorded mounting point for a swimming/flying specimen). Author in meters: Blender Z-up and -Y forward, exported glTF Y-up and +Z forward. Retain real-world size across the collection; never independently normalize each asset to a unit cube. Make any display scaling a museum-layout concern.

Prefer deliberate profile/loft topology and visible silhouette features over assembling an organic shape entirely from untouched primitives. Spend geometry on head profile, pose, limb separation, tail taper, and defining anatomy. Choose smooth, faceted or mixed normals deliberately, with a consistent palette and a PBR-compatible material graph. Avoid unnecessary microgeometry, hidden internal surfaces, and transparent overlap.

Choose a palette-only or textured-PBR profile in the brief. The current refined-low-poly direction permits original baked base-color, roughness and normal detail: low-poly does not mean flat color or low surface detail. Keep geometry and texture budgets separate. Export portable Principled/glTF materials, normals and required UV/tangent data, with no source-only shader dependency. The first pack's texture-free static baseline remains a valid historical profile, not a library-wide restriction. Rigs, animation, instances and required extensions need explicit profile tests.

## Reproducible production

The following is the formal-candidate route. For a bounded study, execute the checks in its frozen scope and mark remaining stages unrun; do not call that production acceptance. Share quick full-angle evidence before expensive polish.

1. Start from factory state and build deterministically. Prefer the data API (`bpy.data.meshes.new`, `Mesh.from_pydata`, `bmesh`) over context-sensitive operators; set active object and mode explicitly when an operator is unavoidable. Check invalid mesh input rather than relying on automatic repair.
2. Store editable semantic parts, material names, palette values, seed, measurements, and source references. Apply or evaluate modifiers deliberately. For mirrored geometry avoid exporting negative determinant transforms; fix winding when baking a reflection. Do not destructively join a rig or destroy useful editable parts merely to reduce object count.
3. Run source QA on evaluated geometry. Save the `.blend` before temporary preview scene changes. Export only the intended root and descendants with explicit flags; see the tested exporter configuration in the production contract.
4. Inspect the emitted GLB, run Khronos glTF Validator, and load that exact GLB in the pinned Three.js viewer. Source renders do not establish export correctness. Compare bounds, front direction, colors, silhouette, normals, and ground contact after export.
5. Produce final hero/thumbnail and diagnostic views from a clean import of the delivered GLB, with a consistent camera and lighting preset; inspect the actual images. Source-scene previews are authoring diagnostics only. Map front/side/top to the declared asset axes and label oblique poses honestly. Use a wireframe or clay view when topology/shading needs review. Record performance on the combined museum scene as well as individual assets.
6. Rebuild twice. Compare semantic metrics and a normalized geometry/material digest; byte-identical `.blend` files are not required. Record checksums of the delivered files for integrity. Deliver only after errors are zero, warnings are reviewed, and visual review is complete.

Freeze each candidate by asset ID, revision, brief/reference hashes and exact GLB hash. Run a fresh independent review task against the brief, reference ledger and actual export evidence, before sharing the maker's verdict. Keep visual craft, factual obligations, specification, parsing, GPU rendering and populated-scene performance separate. Use `scripts/validate_candidate.py` to check record/evidence integrity; it cannot certify beauty or truth. A failed or unknown required gate remains unapproved.

Use bounded headless processes for parallel production, not one serial GUI and not one process per planned asset. Read the queue contract linked from the standardized pipeline, coordinate shared CPU/memory capacity, and isolate every attempt's outputs. Quick full-angle evidence comes before expensive final renders; independent image reviewers can work while other assets build. A screenshot does not prove internal geometry or scientific correctness.

## Shared helper

The executable interface and verified runtime lessons are in [qa-design.md](references/qa-design.md). Use `scripts/asset_common.py` instead of rewriting export, color conversion, preview lighting, or output paths per asset. Run `scripts/validate_gltf.cjs` for official format validation and `scripts/test_qa_glb.py` for checker regression tests. Code is MIT; assets, rendered previews, documentation and Skill prose are CC-BY-4.0, attributed to Leon Made This / s010s.

## Acceptance boundaries

Do not label a local checker as a complete glTF validator. The bundled GLB audit intentionally covers only the static, uncompressed, embedded-buffer baseline and stops on unsupported content rather than passing it silently. Surface limitations and any skipped browser/GPU or validator stage. Numeric QA cannot certify species identity, beauty, scientific accuracy, or clean visual intersections.

Triangle, material, and file-size limits are configurable project budgets, not universal truths. The first environment pack's bands (T1 250–700, T2 700–1,400, T3 1,400–2,600) and the helper’s 12,000 ceiling are historical settings, not limits for every revision. Choose current limits with the [role-based budgeting framework](../lowpoly-art-direction/references/asset-budgeting.md) and measured performance. A successful 472 KB example does not establish a universal 500 KB cap. Never make an asset meet a budget by damaging its identifying silhouette.

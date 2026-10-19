# QA design and executable entry points

For new work, the [standardized pipeline](standardized-pipeline.md) adds frozen candidate records and fail-closed evidence validation to the existing checks below. Use [parallel-queue.md](parallel-queue.md) for isolated bounded headless jobs and quick exact-GLB multi-angle evidence. Historical `threejs_runtime.status=pass` records must be read with their scope: parsing alone is not GPU rendering. Never promote old or unrelated evidence to a new artifact's pass.

## Repository interfaces

`scripts/asset_common.py` (relative to the repository root) is imported by Blender generators. Its current signatures are:

```python
collection = setup_scene(slug, seed=0)
mat = make_material(name, '#RRGGBB', roughness=0.85, metallic=0.0, double_sided=False)
obj = mesh_object(name, vertices, faces, mat, collection, recalculate_normals=True)
link_object(obj, collection, parent=True)  # for geometry made with other Blender tools
shift = ground_asset(collection, center_xy=False)  # optional, preserves the root
record = export_asset(
    slug, {'en': 'Name', 'zh': '名称'}, category, collection,
    metadata={'description': {'en': 'Description', 'zh': '描述'},
              'generator': 'scripts/models/build_example.py', 'sources': []},
    output_root=None, render=True,
    views=('hero', 'reversehero', 'front', 'side', 'rear', 'top'),
    max_triangles=12000, max_materials=8, max_primitives=24,
    resolution=1024, samples=32, collection_id='prehistoric', diagnostics=True,
)
```

`setup_scene` resets the Blender scene, so call it once for each independent asset. Vertex coordinates and positions are meters. `mesh_object` recalculates consistent face normals and uses flat shading. For open sheets, normal direction still needs visual review. A list of materials may be passed, then polygon material indices assigned explicitly by the author.

By default output is `assets/<collection_id>/<category>/<slug>/`. First-batch categories are geology, plants, wood, traces. `output_root`, if supplied, replaces the parent of the slug directory. Metadata uses actual repository-relative file paths, or absolute paths only for deliberately outside-repository test outputs. All assets retain editable `.blend` plus standalone `.glb`.

`title` and description are bilingual dictionaries. The helper supplies dimensions in glTF axes (X width, Y height, Z depth), original Blender dimensions, license `CC-BY-4.0`, author `Leon Made This / s010s`, palette, build options, seed, triangle counts, and file SHA-256s. Code/scripts are MIT; models/renders/docs/Skill prose are CC-BY-4.0. The helper does not publish files or edit the aggregate manifest.

## What the helper automatically verifies

Source stage: export collection/root existence, meter scale, root identity, supported object types, resolved object instances, positive mesh transform determinants, finite vertices, evaluated triangle count, degenerate faces, missing materials, manifold/boundary warnings, intentional smooth-shading warnings, ground-height warning, and world bounds.

GLB stage (`qa_glb.py`): container header/chunks, standalone embedded resources, core static baseline, bounded accessor reads, finite geometry, normals, indices, degeneracy, node hierarchy/cycle checks, exact transformed bounds, unique mesh and scene-expanded triangle/primitive counts, configurable budgets. A shared mesh referenced by two nodes is counted twice for scene work but once as unique mesh geometry. It stops on compressed, sparse, skinned, morph or GPU-instanced data instead of pretending those paths were verified.

Source-to-export stage: compare triangle counts and the explicitly axis-converted bounds. A source bbox `[x,y,z]` maps into GLB `[x,z,-y]`. A mismatch larger than 0.0001 m fails this baseline.

These checks do not prove a complete glTF schema implementation, camera framing, model identity, visual beauty, or paleontological accuracy.

## Independent official format validation

Run after the asset build, from the repository root:

```sh
node scripts/validate_gltf.cjs assets/prehistoric
```

The script uses the pinned official `gltf-validator` devDependency, processes GLBs sequentially, rejects external-resource fetches, writes each `gltf-validator.report.json`, and updates only `qa.json.khronos_validator`. It records the GLB checksum to bind the report to the inspected artifact. Zero errors is required; warnings still require review. A missing dependency or inability to validate is a failure, never a fabricated pass.

Regression checks:

```sh
python scripts/test_qa_glb.py -v
```

The self-contained suite covers valid geometry, shared mesh instances, node transforms, missing/bad normals, invalid indices, NaN vertices, degenerate triangles, rejected sparse/compressed profiles, cycles, and budget enforcement. It creates only temporary test geometry, not deliverable models.

## Actual browser gate

The pinned Three.js viewer must load the shipped GLB through GLTFLoader. Inspect console/network errors, shader failures, missing dependencies, all views, and material/normal behavior. Compare world bounds against metadata after updating world matrices. Check the model with backface culling rather than hiding defects using forced DoubleSide.

Record renderer version, output color space, tone mapping, exposure, scene lights, measured draw calls/triangles, screenshot path, GLB checksum, and actual outcome in `qa.json.threejs_runtime`. App-level screenshots and import are separate from Blender PNGs. Rendering all ten assets together tests a different performance load from a single-asset gallery card.

## Actual visual gate

`export_asset` ensures hero and reversehero images, plus requested front/side/rear/top. With diagnostics enabled it adds `preview-silhouette.png` (128 square, black-on-white, no floor/shadow), gray `preview-clay.png`, reverse-key `preview-clay-alt.png`, and `preview-wireframe.png`. Wireframe uses a temporary copy of evaluated `loop_triangles`; it does not change triangulation with a guessed modifier setting. Source `.blend` is saved before any preview stage exists.

The initial scene's editable source has no preview camera/light/ground. Repeated rendering does not resave it. All outputs must be opened and reviewed. Use the separate lowpoly-art-direction skill's rubric; record reasoning and fixes. Do not set visual status to pass just because an image file exists. Record any intentional open edges, double-sided foliage, smooth regions, or budget exceptions in reviewed warnings, with the actual reason.

## Reproducibility and known runtime findings

Observed on 2026-10-16: Blender 4.3.2, glTF exporter 4.3.47. An 8-vertex asymmetric wedge exported as 12 triangles and 24 GLB vertices because flat normals split corners. Bounds transformed exactly, and repeated exports produced the same GLB SHA-256 while `.blend` hashes differed. Semantic reproducibility and deliverable integrity hashes are separate concerns.

The cloud Blender build has Cycles CPU but lacks OpenImageDenoise. Enabling denoising caused a real render error. The helper disables denoising, then rendered all diagnostic modes successfully. At low samples the image is visibly noisy; raise samples for final quality if needed, keeping the same settings across comparable assets. Do not silently switch color management or add a different per-asset lighting rig.

The standard is Standard view transform, None Look, exposure 0, gamma 1, neutral light rig, and warm studio floor #E8E4DC. Earlier research used AgX before the first-batch art standard was defined; all production helper outputs now follow the unified Standard preset.

The test `.blend` was reopened and verified to contain no `_PREVIEW_ONLY`, camera, or light. Its official Khronos validation returned 0 errors, 0 warnings, and no info/hint messages. This evidence applies to the fixture, not to future generated assets. Production QA begins with explicit `not_run`/`pending` browser, official-validator, and visual statuses until those stages actually happen.

## Real multi-mesh failure and its regression test

The first one-object fixture did not expose a multi-mesh wireframe failure. A real cycad export crashed Blender 4.3.2 while constructing diagnostic meshes from depsgraph-owned evaluated data. Creating new datablocks can invalidate that evaluated RNA. The fix is a strict two-phase operation: first freeze `list(collection.all_objects)`, copy every evaluated vertex, loop triangle and world matrix into ordinary Python/Matrix values, and clear every temporary mesh; only then create preview mesh datablocks. Do not hold evaluated mesh/RNA references across scene edits.

This fix was tested against the saved multi-mesh cycad source, then added to `scripts/test_asset_common.py`. Run that test inside Blender with `--python-exit-code 1`. Its temporary three-part fixture checks 36 exported triangles, all ten preview modes, exact axis-aware bounds, deterministic GLB output on a rebuild, and a reopened source `.blend` free of preview cameras/lights/ground. It does not produce or publish a library asset.

## Semantic rebuild digest and actual GLB roundtrip

`qa_glb.audit_glb(...)["semantic_sha256"]` hashes decoded geometry attributes/indices, materials, and scene structure, ignoring the generator string, custom extras, JSON formatting, and binary offsets. Node/mesh/topology ordering still matters; this is a deterministic-rebuild test, not geometric-isomorphism or perceptual equivalence. The pure-Python suite now includes tests proving metadata independence and material-color sensitivity (14 tests total).

To inspect what was really shipped:

```sh
blender --background --factory-startup --python-exit-code 1 --python scripts/check_glb_roundtrip.py -- assets/prehistoric/plants/cycad/cycad.glb
```

The script imports the actual GLB into a clean scene, checks count/bounds, and writes isolated GLB-origin hero/wireframe PNGs and `glb-roundtrip.report.json`. It never modifies the source blend, GLB, original QA stages, or metadata. By default the check images are 512 pixels at 32 samples. Exported flat normals split vertices; after re-import this can produce topological boundary-edge counts without a visible hole. Review these as representation warnings rather than automatically rejecting an intact rendered surface. This Blender import is still separate from the Three.js browser gate.

## Concept-study evidence and final exported previews

The [standardized lifecycle](standardized-pipeline.md#scope-design-study-or-formal-candidate) distinguishes a reviewable study from a production-approved candidate. Use `scripts/validate_concept_evidence.py` for supplemental file/hash/chronology records and [the workflow recipe](../../concept-guided-lowpoly/references/workflow.md) for exact-GLB rendering. Its `valid` and `evidence_complete` outputs are distinct, and neither is visual, factual or runtime approval. Missing historical ImageGen receipts/timestamps or render-time manifests stay null/incomplete; a present-day hash cannot recreate an old tool event.

For new final thumbnails use `scripts/render_candidate_views.py` on the actual delivered GLB, retain its hash-bound manifest and inspect the pixels. An ImageGen concept is never a final asset thumbnail. Existing source-preview helpers remain useful for authoring and historical reproducibility, but are not interchangeable with exact-export proof. Keep static advisories such as double-sided materials separate from zero Khronos warnings. Nonzero absolute signed-volume magnitude does not establish outward normals or a printable union; declare the inspection method and limits.

## Historical source-preview hero refinement

The following records the first batch's source-.blend preview route, not the final exact-GLB route for new deliverables. The first production heroes at 32 samples showed visible CPU path-tracing noise. Final hero images for the first batch are therefore re-rendered at 256 samples after all authors finish writing their models; diagnostics may remain at 32 samples. Do not race a generator that may overwrite the same PNG.

For one existing editable source:

```sh
blender --background assets/prehistoric/plants/cycad/cycad.blend --python-exit-code 1 --python scripts/render_hero.py -- --samples 256 --resolution 1024
```

For the finished ten-item batch:

```sh
python scripts/render_heroes.py --assets-root assets/prehistoric --expected-count 10 --samples 256 --resolution 1024
```

The hero tool renders to a temporary directory before replacing only `preview-hero.png`, confirms the source blend checksum stayed unchanged, and updates only `qa.previews.per_view.hero`. It does not save the blend, re-export GLB, overwrite metadata, or fabricate validator/browser/visual-review status. The refreshed hero gets its own PNG checksum and `rendered_not_visually_reviewed` status; inspect it before declaring the final visual result complete.

A later consistency check also separated the world shader's camera-visible background from its illumination branch. Horizontal orthographic views now see the same intended warm studio background instead of darkening that background to the environment-light strength. This preserves illumination/exposure and leaves geometry/material exports unchanged. Final hero refinement writes `hero-render.report.json` as an independent record as well as its per-view QA entry, so its provenance is recoverable if an author separately rewrites a QA file.

## Pause expensive polish when art direction changes

More render samples improve noise, not silhouette design, proportions, botanical structure, or the overall visual language. If the user rejects the direction while a batch is rendering, stop launching subsequent renders, preserve completed images and editable sources, and label unfinished refinement pending. Finish an already-running render only when allowed. Rework a representative model against the new direction before spending another full batch on polish.

The batch and per-item hero tools honor `qa/hero-refinement.pause.json`. A requested pause is a workflow stop, not an asset-format failure. Do not remove the pause marker or resume because time elapsed; resume only when the revised task authorizes it. Frame/noise checks on a hero image are limited evidence and do not establish user acceptance of the art direction.

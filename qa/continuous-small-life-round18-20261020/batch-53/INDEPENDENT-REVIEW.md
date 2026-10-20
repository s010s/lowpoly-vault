# Batch 53 — Independent QA

**Result:** Asset-level technical, specification, visual, and factual review passed for all four frozen r001 assets. This is an independent review record, not formal publication approval. Formal GPU and composed-scene acceptance remain unproven; concept evidence completeness is blocked only by the intentionally unknown exact provider generation time.

## Frozen inputs and method

- Repository: `s010s/lowpoly-vault`
- Frozen concept/model baseline: `b204a43a5c816f9c0c76683b5ee8a4451e9050a8`
- Metadata-only maker identity update: `0d4d6153955b2ca8809d343d63628f55b493b074` (descends from the frozen baseline)
- Final `production/continuous-small-life-round18-20261020/work/batch-53/HANDOFF.json` SHA-256: `022ccc702db84d01e2f1005cfecad760310ff5931c299f834d57a565c6cbea48` (the earlier handoff had SHA-256 `0923e6fb13da7b2d8428ebdc8543f494e4286034752c8d6f3abce63a4f2c224a`)
- Verified maker task/thread: `01a156a2-8680-7691-b35e-25e9eecee03b`; turn: `01a156a2-9163-72a1-ac93-9a657d275a35`.
- Parent comparison confirmed the update is limited to identity/profile binding: all 269 protected model, freeze, concept, and view files are byte-identical to the baseline.
- Reopened the four `.blend` files in Blender 4.3.2; independently ran `validate_candidate.py` against `static-stylized-v1` and its profile contract, ran `check_glb_roundtrip.py`, checked the Khronos validator report/hash bindings, and ran the concept evidence record validator. Pixel-inspected each concept image, every required static view, the additional Halopoa clay-top view, and all six bound WebGL frames for each asset. No candidate artifacts were modified.

## Per-asset results

Dimensions below are Blender XYZ in metres. “Nominal” is the frozen brief value; “measured” is the re-opened `.blend` bounding-box extent. These are modeling dimensions, not biological specimen measurements. GLB Y-up bounds are axis-reordered from Blender and agree within float precision.

| Asset | `.blend` SHA-256 | GLB SHA-256 | GLB bytes / triangles / materials / primitives / textures | Nominal XYZ → measured XYZ | Review |
|---|---|---|---|---|---|
| `hypoturrilites` | `3aaba1ae3140edd3730a3800fb271a131b3891aa8919d95a0efaff11dfb139cc` | `23d62a058ebc966e287d6a70feec6c041e30a4c2314418e7504ca59258d56bc1` | 755,148 / 13,744 / 3 / 4 / 0 | `[0.100, 0.100, 0.180]` → `[0.1000000015, 0.0999999940, 0.1800000072]` | **Pass.** Continuous tapered helicoid with descending whorls, node rows, aperture and closed reverse; top and reverse views show the intended coiled form. Within all static profile budgets. |
| `iodes-brownii` | `85b7c6596cdd0c3c21ccd6ac25863569961c5686929243393a7753af46fdb55c` | `f3604fbfab6eb74df9dfc6924994e642dc9722681a3329a91f21c0d42c997dff` | 508,768 / 9,512 / 3 / 4 / 0 | `[0.007, 0.0045, 0.009]` → `[0.0070000002, 0.0044999998, 0.0089999996]` | **Pass.** Flattened reticulate form; inspection of opposing faces confirms one near-apical horn on each face, not two on one face. The requested inventory label is retained as an inspired-by label, not a claim that the historical paper used that genus combination. |
| `welded-ignimbrite-outcrop` | `1e1cdcb3bfd64ed630455fb6b6bcda8f66b83704823a17fb7a0914a0bb3f5357` | `83b7d4170c8cb51870e2ea643294306e4cc6a62a2386712457cfb887ff0c2704` | 119,408 / 2,218 / 3 / 3 / 0 | `[1.400, 0.850, 0.900]` → `[1.399999976, 0.850000024, 0.899999976]` | **Pass.** Lens forms have visible geometric relief and side walls in neutral clay and WebGL views; they are not only painted spots. The block is deliberately faceted and somewhat regular, a non-blocking art-direction limitation. |
| `halopoa-furrowed-burrow` | `6c538d87b579f9a32fe28d2a21c19f6937927108773f0c1774bb63ebd7699714` | `42e7fd3105d689c27d3bdf7de6ea0fbfc95094d0645e840b1b66062ca8fd54f6` | 162,400 / 9,902 / 3 / 5 / 0 | `[0.240, 0.170, 0.035]` → `[0.239999995, 0.170000002, 0.0350000001]` | **Pass.** The slab carries overlapping, raised probes with longitudinal furrows. Front, side, rear, top, clay-top and WebGL views confirm positive relief rather than a negative impression. |

All four candidate validations returned `valid: true`, no errors, and `profile_contract_status: pass` for `static-stylized-v1` rule `2026-10-18.1`. The corresponding geometry budgets are ≤14,000 triangles, ≤1,000,000 GLB bytes, ≤6 materials, ≤30 primitives, and zero textures; all four fit. Source mesh audits found zero boundary and non-manifold edges. The official Khronos reports are bound to the exact GLB hashes above and each records zero errors, warnings, infos, or hints.

Each `.blend` reopened successfully. Independent Blender GLB re-imports preserved each GLB SHA and decoded semantic digest; triangle counts agreed and measured bound deltas were 0 for three files and `1.862645149e-9 m` for `hypoturrilites`.

## Halopoa smooth-normal warning disposition

The source audit reports three intentional smooth-normal warnings: `long-low-probe` (1,920 smooth faces), `oblique-overlapping-probe` (1,920), and `short-offcenter-probe` (1,280). All three source meshes are closed, with zero boundary and non-manifold edges. Neutral clay and shaded color images retain coherent probe shading and readable furrows; I saw no holes, discontinuities, or groove loss. **Reviewed and non-blocking; no model repair is warranted.**

The Blender GLB re-import diagnostic also labels split-normal/vertex-boundary patterns for review. Those are importer representation warnings: original source topology is closed and the exact-GLB renders show no visible defect. On Halopoa, the importer’s “smooth slab” observation is contradicted by the direct `.blend` audit (the slab has zero smooth faces), further indicating an import-side classification artifact.

## Runtime and scene evidence

The included runtime records are hash-bound to the exact GLBs above. Each reports Three.js 180, Chromium WebGL 2.0, and `ANGLE … SwiftShader` software rendering, with zero runtime errors. The six reported image-file hashes per asset match the included files; the images were pixel-inspected. These records support software-WebGL parse/render smoke testing. They do **not** establish a physical GPU, target-device performance, or formal GPU-stage acceptance.

Each `scene-9` image is a synthetic nine-copy scale/graphics smoke test. It is not a populated production composition and does **not** establish the brief’s formal parent-scene acceptance. The frozen brief lists separate `gpu` and `scene` required stages; both remain unknown/pending in the candidate status. The machine-recorded `qa.json` also retains `threejs_runtime: not_run` and `visual_review: pending`; the external runtime bundle is supplementary evidence, not a replacement for those approval fields.

The Blender GLB round-trip checker returned `pass_with_warnings` because glTF vertex splitting/split normals trigger generic importer topology/smooth-face notices. Geometry hashes/digests, triangle counts, bounds, source topology, and viewed renders show no functional mismatch. No change is required for those notices.

## Concept, references, and provenance

All four concept evidence records validate structurally with no errors. Each correctly preserves `concept_generated_at: null`; evidence completeness is therefore false with the validator blocker “concept_generated_at: unknown; do not reconstruct times from file mtimes.” Keep that timestamp unknown unless the provider supplies a verifiable exact time. This is a provenance-completeness limitation, not evidence of a model defect.

The concept images and frozen model views were visually compared. Source text supports the reviewed diagnostic features: the [Digital Atlas of Ancient Life ammonoid guide](https://www.digitalatlasofancientlife.org/learn/mollusca/cephalopoda/ammonoidea/) describes *Hypoturrilites gravesianus* as torticone; the [American Journal of Botany paper](https://bsapubs.onlinelibrary.wiley.com/doi/10.3732/ajb.1400550) describes reticulate surfaces and two apical horns, one per valve, for *Biceratocarpum brownii*; the [National Park Service ignimbrite overview](https://www.nps.gov/articles/000/pyroclastic-flows-and-ignimbrites-and-pyroclastic-surges.htm) describes massive ignimbrite and flattened pumice fiamme; and the [Kansas Geological Survey ichnology reference](https://www.kgs.ku.edu/Publications/Bulletins/245/04_ichno.html) describes *Halopoa* traces with longitudinal striae/wrinkles and overlapping cylindrical probes. This supports a stylized inspired-by interpretation; it does not assert exact specimen reconstruction or taxonomy beyond the frozen asset labels.

## Disposition

- **Model repairs required:** none.
- **Non-blocking visual note:** the ignimbrite’s terraced block silhouette and lens spacing are regular; refine only if the art direction later asks for more natural irregularity.
- **Evidence/status still pending:** exact provider generation time (unknown by instruction), physical-device/target-GPU evidence, and formal populated parent-scene acceptance. No invented values should be added. The existing pending approval fields were not changed by this independent review.
- **Publication:** this report does not change candidate assets, `main`, website, or approval metadata; no pull request was created.

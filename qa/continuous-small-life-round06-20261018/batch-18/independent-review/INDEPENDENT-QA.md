# Batch 18 independent asset review

**Decision: PASS — all four candidates** under `static-stylized-v1` / rule `2026-10-18.1`.

This review is bound to handoff commit `0a44bac24c493bd4eafdd782dc3fbf05af49d0bb` and to each source branch tip and asset hash below. The earlier batch01 QA was not consulted or reused. The review accepts natural, refined, stylized low-poly teaching art; it does not demand a strict specimen reconstruction or exact fossil measurements.

| Asset | Exact source branch / commit | Blend SHA-256 | GLB SHA-256 | Bytes / triangles | Result |
|---|---|---|---|---:|---|
| spinolestes | `candidate/batch18-spinolestes-20261018` / `10448e2d3e12670d09e9a438dd5ee3cd609ca541` | `62f391ccc87d16e1c3e8d9ff936259229b239cf613c649ab64337aa70f1c6674` | `23d03175317951de71b33b37bdc9333eb7fde1f035b51beeaec312c4668c0775` | 140,440 / 7,256 | PASS |
| odontogriphus | `candidate/batch18-odontogriphus-20261018` / `2b897228411ee19af3fe9ee830e7bfc45735af46` | `b4af74a22c1d3464b3cd5d7121a938fef17441d2d073d534a74cdf1ec13ccb2d` | `234865d367f33960eae9fe3cdc7b48f439eb2a10efc8e013ab0a5726ebd844e7` | 56,396 / 2,796 | PASS |
| trapa | `candidate/batch18-trapa-20261018` / `a3af799b00353308fbe65852f4ac15cd8caa4843` | `2789444794805baf07a972f105e5eabb848aeb531970b540b4ca2dc7f8dfba30` | `707022336cce0a0d817511f710a7c68128846747c36ad62df7db5a51131b4644` | 46,740 / 1,932 | PASS |
| flint-nodule | `candidate/batch18-flint-nodule-20261018` / `87583c3f88e276972d190d379e2c01b50c0cde32` | `38de72c82a00c17271aa37727be4012faa02a2088b4d9ddb417dbcb20e6648af` | `224dcf06d4d5ef58fc9066a981c0cead5a894fa32ba93651d875f2ae04993fff` | 52,264 / 2,684 | PASS |

## Checks performed

- Read the exact `final-handoff.jsonl`, confirmed all four source refs still point to their handoff commits, and recomputed **all 86 handoff artifact pins**. Blend, GLB, generator, brief, reference, candidate, profile-contract, view/runtime evidence and report pins all match.
- Re-ran `scripts/validate_candidate.py` with the explicit `static-stylized-v1` profile and each frozen contract. All four records are structurally valid, profile contract status is `pass`, and there are no validation errors.
- Reopened each exact `.blend` read-only in Blender 4.3.2, inspected the `EXPORT` meshes, then imported the exact GLB. Every source part has closed manifold edges, finite vertex normals, positive signed volume and positive face area. Source and imported GLB triangle totals match exactly; reimported bounds match within `1e-4 m`.
- Independently ran Khronos glTF Validator 2.0.0-dev.3.10 on the four exact GLBs: **0 errors and 0 warnings for each**.
- Verified source fixed-view manifests and image hashes, then rendered each exact GLB again in Blender 4.3.2 / Cycles CPU / 2 threads / 24 samples. Each has the exact eight required views (`hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`) and zero turntable frames. The source and independent render manifests both bind the exact GLB SHA.
- Independently loaded and rendered each GLB with Three.js 180 `GLTFLoader` in Chromium 154 / ANGLE SwiftShader WebGL. Per-asset and nine-copy renders have no browser-console or GL errors and have positive foreground pixels and render triangles. A second composition loaded all four batch18 GLBs together at source scale: 4 instances, 19 meshes, 14,668 asset triangles, 23 draw calls, no GL errors, with a 100 mm ruler. This proves functional software-WebGL rendering and scale continuity; it is not a hardware-GPU or performance claim.

## Visual review

- **spinolestes — PASS.** The low, compact body, short connected limbs and paws, blunt muzzle, small ears and localized short dorsal protospine patch read together in color, clay, silhouette and front/side/rear/top views. Body length is 139.4 mm against its nominal 140 mm (tail excluded); the full model extends to 186.8 mm with the tapered tail. The head, paws and tail have no visible floating seams or gaps.
- **odontogriphus — PASS.** The exact model reads as a shell-free, dorsoventrally compressed oval with a smooth dorsal surface. The underside is a continuous broad foot; short marginal gill folds are present and were checked in a targeted bottom render. The proportions and gill count are stylized; no exact specimen ratio is claimed. This preserves the brief's basic form and matches the broad morphology described by the [Royal Ontario Museum](https://burgess-shale.rom.on.ca/fossils/odontogriphus-omalus/).
- **trapa — PASS.** The compact fruit body and four spreading horns are clear in the top view; the short recurved barbs remain subordinate and rounded. Dark seams near some barb contacts are visible in top lighting, but they are closed, attached geometry; source topology is manifold and there are no missing faces or detached horns.
- **flint-nodule — PASS.** The asset reads as one irregular rounded nodule with pale cortex and one coherent concave curved fracture scar. It stays within the explicitly artistic geological teaching scope and does not imply a specific site, specimen or tool. The exact GLB shows no open faces or discontinuities.

## Gate results and scope

The original frozen `candidate.json` records still say `approved_for_brief: false` because their independent stages were deliberately pending. This report completes those review gates for the exact source and GLB hashes; the candidate branches and their files remain unchanged. No blocking findings remain for this independent review.

GPU/runtime acceptance here is functional software-WebGL only. No hardware GPU, production performance, strict scientific reconstruction, or physical-specimen measurement is claimed. Nominal scale choices are retained without resizing the models to normalize the gallery preview.

This branch contains review documentation and evidence only. No model geometry, budget or validation threshold, CI, permission, merge, release, or Drive changes were made.

## Evidence index

- [`review.json`](review.json) — per-asset SHA-bound decisions and criterion results.
- [`source-evidence-checks.json`](source-evidence-checks.json) — exact source refs, hashes, manifests and rerun summaries.
- [`relative-scale-scene.json`](relative-scale-scene.json) — four-asset scene metrics and source hash bindings.
- `evidence/fixed-views/<asset>/` — independent eight-view PNGs, manifest and contact sheet.
- `evidence/runtime/<asset>/` — actual browser screenshots and runtime report.
- `evidence/targeted/odontogriphus/` — underside check.
- `evidence/targeted/trapa/` — high-resolution top view and barb-contact check.
- [`evidence/relative-scale/batch18-relative-scale-scene.png`](evidence/relative-scale/batch18-relative-scale-scene.png) — actual four-asset composition at source scale.
- `scripts/` — read-only Blender geometry audit, exact-GLB scene renderer and targeted-view render scripts.

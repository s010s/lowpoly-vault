Batch-22 independent QA | IDs: florissantia, stanleycaris, pahoehoe-lava-surface, staurolite-cross-twin | model source commit SHA: `1bfc3c7e33bbbd2131f86799f5fff5e9971ba0a5`

# Independent QA: batch-22

**Result: PASS for all four selected artifacts at the exact hashes below. No required rebuilds.** This report records a scoped independent review of these exact Blend/GLB pairs. It does not change candidate stage fields, `approved_for_brief`, or publication authority; those remain as recorded in the handoff.

The checkout is based on handoff tip `42d05757288c22b3e458414bfaa9747b3d53b301` on `candidate/small-life-batch22-20261018`. The scope file pins the model source commit above and these four GLBs. Direct SHA-256 checks of each selected Blend and GLB matched both `candidate.json` and the frozen scope.

| Asset | Verdict | Blend SHA-256 | GLB SHA-256 | GLB bounds (X × Y × Z, meters) | Triangles |
|---|---|---|---|---:|---:|
| `florissantia` | **PASS** | `7c94635bc4b1a1e765af3e790f1fcdc96fa47fcacbaab727de43bda4c081c503` | `d64badf1fc1c3c2a1dde99502dbf1dba7c284496877c55fce75beedf2392190f` | `0.059742 × 0.007892 × 0.062176` | 8,588 |
| `stanleycaris` | **PASS** | `86c58fd9dea7f6c3bde2882d821e44e37661132f384cc120e5c72f73e3535493` | `cb1d0a833dc425fce32333d2bdcba34bea234e150d2b456aac155ba50c17c18d` | `0.036400 × 0.015100 × 0.130343` | 9,340 |
| `pahoehoe-lava-surface` | **PASS** | `029a2ad7c634e3c7040028edea9e5e40ddd09e51eb569a8fcfce799174d557a2` | `22d72f2ab8b64a419427df6334ac5d7ca50277d4132cbdca99ca4003c768a7e5` | `0.933450 × 0.084360 × 0.668655` | 10,032 |
| `staurolite-cross-twin` | **PASS** | `f19bec44334092e619d71098d1825fd452fc8fdf141942a3bce333fe85d48b4e` | `0c36f1a2ed7d63406d8ea636ac82fb907da0e25ab1a244efd12a66510c4e5511` | `0.106458 × 0.120996 × 0.019578` | 146 |

## Visual review

I inspected the eight fixed source views (`hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`) and the GLB runtime contact sheets for each selected asset. The source `view-manifest.json` has exactly those eight source frames, zero turntable frames, and 12 GLB runtime frames; all listed source/runtime image hashes and byte sizes match the files. I also inspected close runtime views for the pahoehoe top and small-size presentation and the staurolite hero/top.

- **florissantia — PASS.** The low-relief five-lobed preserved calyx reads as one coherent organ from both faces, with the shallow central cup and quiet primary veins visible. Side/rear thinness is consistent with the intended sheet-like specimen; I saw no exposed break or disconnected vein.
- **stanleycaris — PASS.** The small head plate, three eyes, paired rake appendages, segmented trunk/swimming flaps, and four caudal blades remain legible across the fixed views and runtime. Their contacts read as embedded or naturally attached; no conspicuous gap or detached part appears at hero, reverse, front, side, rear, top, or bottom.
- **pahoehoe-lava-surface — PASS.** The selected attempt-02 reads as one continuous crust with rounded folds following a shared flow direction and modest lobe/height variation. The fold fronts wander and the crop is irregular compared with preserved attempt-01; common-direction ridging remains intentional and does not read as the earlier perfectly regular corrugation. It is an illustrative patch, not a site reconstruction.
- **staurolite-cross-twin — PASS.** The two-prism intergrowth reads as a continuous, faceted cruciform mineral form. The center intersection is visible in hero and top views and has no exposed split. The sparse logical facets suit the accepted stylized bar and do not need geometry padding.

The reviewed scene captures show six instances of each asset. Their rendered dimensions are consistent with art-scale props: florissantia about 62 mm across, stanleycaris about 130 mm long, the lava crust about 0.93 m wide (the configured nominal art scale is 0.9 m), and staurolite about 121 mm tall. These are model extents, not scientific measurements. The scene evidence is per-asset six-instance rendering, not a claim about mixed-taxon co-occurrence or physical habitat scale.

## Source/export and runtime checks

I independently ran `scripts/check_source_export.py` in Blender 4.3.2 against each pinned `.blend` and exact `.glb`, writing the audit outputs under `/tmp/batch22-independent-qa/` without saving or exporting over candidate files. All four passed triangle parity and axis-converted bounds matching. Maximum bounds errors were `2.33e-10 m` (florissantia), `0 m` (stanleycaris), `2.33e-9 m` (pahoehoe), and `6.40e-10 m` (staurolite). Audited source parts have zero boundary and non-manifold edges. Three soft-surface assets emit intentional smooth-face review warnings; those faces were visually reviewed and show no unintended shading defect. Staurolite has no such warning.

The pinned browser reports load the exact GLB hashes using Three.js 0.180.0 `GLTFLoader` and Chromium WebGL2 on ANGLE/SwiftShader software rendering. Single-asset and six-instance scene runs report `pass`, with no errors or failed views. Single-view draw calls are 3 / 9 / 2 / 3 and six-instance scene calls are 18 / 54 / 12 / 18 for florissantia / stanleycaris / pahoehoe / staurolite respectively. This is software WebGL evidence only; it does not establish physical GPU or device performance.

Visual evidence and manifests are retained alongside the candidates under `assets/candidates/continuous-small-life-round08-20261018/batch-22/<asset>/r001/<attempt>/<asset>/` (`source-contact-sheet.jpg`, `runtime-contact-sheet.jpg`, `view-manifest.json`, and `runtime/`). The handoff and scope pins are in `production/continuous-small-life-round08-20261018/work/batch-22/HANDOFF.md` and `QA-HANDOFF-SCOPE.json`.

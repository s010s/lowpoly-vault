# Independent QA — undersea invertebrates concept batch

**Review date:** 2026-10-19 UTC

**Frozen production commit:** `fc2f6db4133b62e48b9764e4a33b0fd518e806df`

**Production branch:** `batch/undersea-invertebrates-concept-20261019`

**QA branch base:** the frozen production commit above.

**Reference skills reviewed:** `main` commit `bac6621fc39144b3759c53b1b27231ac1b6e21c6`, including `asset-factual-review`, `concept-guided-lowpoly`, `blender-lowpoly-pipeline`, and `lowpoly-art-direction`. No `AGENTS.md` is present in the frozen tree or that `main` commit.

## Verdict

The four exact Blend/GLB pairs are internally consistent and load correctly in a fresh Blender import and a real Chromium/Three.js software-WebGL scene. The three candidates below pass the visual and broad, genus-informed checks in their frozen briefs. Ctenoimbricata passes the concept-led visual check, while its factual review remains **unknown** until the original paper's Figure 4/5 pixels can be inspected. No model changes are requested by this review.

This is not production or publication approval. Full-resolution review of every proof frame is incomplete; the target populated scene and physical-device performance have not been measured; and the GitHub checks remain pending. Ctenoimbricata's figure-image review is an additional factual gate.

## Per-candidate findings

| Candidate | Independent visual/specification finding | Factual finding | Action |
|---|---|---|---|
| `mackenzia r001` | **Pass.** Exact GLB reads as an upright ribbed sac with eight longitudinal folds, a short stalk, and holdfast. The model is slimmer and more faceted than the concept image, but the silhouette and all explicit brief features remain clear. | **Pass for the declared genus-informed scope.** The Royal Ontario Museum description supports an upright sac up to 16 cm, a short stalk and holdfast, 8–10 longitudinal ridges, and no tentacles. The brief does not claim a specimen-accurate reconstruction or settled cnidarian affinity. | No model revision requested. |
| `prasopora r003` | **Pass.** A low hemispherical colony, cream epitheca, recessed pores, and concentric underside folds are legible in the exact-GLB views. The pore pattern is more regular and ringed than the AI concept, but it still forms pore groups separated by quiet bands, consistent with the frozen stylized brief. | **Pass for the declared genus-informed scope.** The reviewed Atlas entry supports discoidal-to-hemispherical colonies, prismatic zooecia/angular mesopores, and a wrinkled lower epitheca. No species claim is made. | No model revision requested. A more irregular pore layout is optional only if the concept's patch arrangement is a required style choice. |
| `strophomena r003` | **Pass.** The exact GLB preserves the semicircular fan, straight hinge, fine ribs, shallow paired-shell profile, and subdued continuous lavender growth band. Side and top views support the intended thin shell rather than a thick slab. | **Pass for the declared genus-informed scope.** The reviewed Atlas entry supports a semicircular outline, radiating fine ribs, and a profile that changes convexity. The asset depicts only the external shell and makes no species-specific claim. | No model revision requested. |
| `ctenoimbricata r001` | **Pass for concept-led visual/specification.** The exact GLB is bilaterally symmetric and flattened, with a single marginal ring, four lateral spine pairs, a front comb, and sparse dorsal studs. Its color blocking and scale match the frozen interpretation. | **Unknown pending Figure 4/5 pixel review.** The PLOS article text supports a roughly 20 mm bilateral disc, a single marginal ring, an anterior imbricate roof, and 14 ventral spinose elements. I verified the model contains the corresponding named parts and comb, but could not inspect the original figure pixels to assess their detailed arrangement. | No correction is justified from the accessible evidence. Complete the primary-figure visual check before factual acceptance; revise only if it exposes a material anatomical mismatch. |

The figure image links on the PLOS article page were available, and its text/captions opened. The web fetcher failed on the redirected Figure 4/5 image targets; direct fetches returned HTTP 403, and the alternate PMC page presented a CAPTCHA. The original Figure 4/5 pixels were therefore **not** reviewed. See the [primary article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0038296).

Other factual references reviewed: [Royal Ontario Museum — Mackenzia costalis](https://burgess-shale.rom.on.ca/fossils/mackenzia-costalis/), [Atlas of Ordovician Life — Prasopora](https://www.ordovicianatlas.org/atlas/bryozoa/stenolaemata/trepostomatida/monticuliporidae/prasopora/), and [Atlas of Ordovician Life — Strophomena](https://www.ordovicianatlas.org/atlas/brachiopoda/strophomenata/strophomenida/strophomenidae/strophomena/). These support the broad stylized claims only; none makes these models specimen-accurate reconstructions.

## Frozen file pins and independent import results

All SHA-256 values below match the pins in `production/undersea-invertebrates-concept-20261019/handoff.json`.

| Candidate | Blend SHA-256 | GLB SHA-256 | GLB bounds (X × Y × Z, mm) | Triangles | Materials / primitives | GLB bytes |
|---|---|---|---:|---:|---:|---:|
| `mackenzia r001` | `68cc73013eae89fb96fdb9b9feeec7d2743fc5d32943498c64145921858fbdbe` | `6558b3cce6b208ff5e27d0fe56b4ff703ba205f187a51d9d3d178b318ac6bd5d` | 49.720 × 140.000 × 49.720 | 1,896 | 5 / 5 | 103,344 |
| `prasopora r003` | `3aaf9fbec27c1be0d7c02a41a21c1fb9baa1fc3b6b821c87870928e4b65cff25` | `851e07d6c7b66e4e60a14cec6e153d46fbdc11a6f4f4da4480d733dddd075840` | 61.000 × 26.890 × 61.000 | 8,392 | 3 / 4 | 451,588 |
| `strophomena r003` | `cc40230a5c9d4f5d36846212815ec0cb334d04168307d2928a00e578b5b5a171` | `2880d555e1ff87e7b191a62f4b27557ab10ca5ee5c0f059701dce4e4430813ca` | 55.600 × 5.076 × 41.300 | 4,656 | 3 / 3 | 258,128 |
| `ctenoimbricata r001` | `6c85858c168f4839c441ae3e72d4e4f1ce03daf76555fb08eb6a879d7f46b522` | `f23b40c062dd139c58607f3ade6f22f358c6197eddf451849726511581fb0dc5` | 22.833 × 2.940 × 21.322 | 2,732 | 5 / 26 | 174,736 |

I reopened each frozen `.blend` in Blender 4.3.2, removed the source objects, and imported that candidate's exact pinned GLB into the resulting clean scene. Source and imported GLB had matching mesh-object counts and triangle totals. The imported world-space bounds matched the source bounds to **0 m** for all four. Principled base-color values matched source-to-import within **0.000001 linear**, with measured maximum absolute delta **0.0** for every material. The per-asset measurements and color comparisons are in [`evidence/blender-import-audit.json`](evidence/blender-import-audit.json); the audit script is [`evidence/audit_blender_import.py`](evidence/audit_blender_import.py).

Khronos validator, static GLB, source-export, and two rebuild checks are recorded as passing in the frozen handoff. I checked the exact hashes and loaded files but did not rerun those production checks. The candidate records remain `approved_for_brief=false`, and the concept sidecars' `--require-complete` check remains incomplete; those are honest pending review states, not file-integrity failures.

## Real browser and small-scene check

Using the repository's existing `batch-runtime.mjs` against the four frozen GLBs, I independently loaded each exact file with Three.js `GLTFLoader` in Chromium 154.0.8037.57 / Three.js 180 / ANGLE SwiftShader WebGL, then rendered a four-asset scene at authored scales and seven camera views. Result: **pass**, 987,796 GLB bytes, 17,676 triangles, 38 meshes, 16 materials, 38 draw calls, 44.3 ms aggregate asset load, visible foreground in every tested view, and zero WebGL errors. The scene screenshot is [`evidence/scene-4-assets.png`](evidence/scene-4-assets.png), and the raw report is [`evidence/browser-runtime-report.json`](evidence/browser-runtime-report.json).

This establishes real parsing and functional software rendering for the four-file sample scene only. SwiftShader timings do **not** establish physical GPU performance, browser performance on target devices, or performance in the intended populated environment. The small Ctenoimbricata appears much smaller in this shared-scale scene because its authored dimensions are much smaller; the screenshot is not a per-item catalog framing test.

## Coverage and remaining gates

- I inspected the original concept sheet, the concept-versus-exact-GLB comparison, all four full-contact sheets, and selected individual exact-GLB views including hero/top/bottom, top/bottom/detail, top/side, and top/front/side views. I did **not** open all 37 images per asset individually at original 512 px resolution. Full-frame visual completeness remains pending.
- Ctenoimbricata primary Figure 4/5 pixel review remains pending as detailed above.
- Physical-device GPU behavior and the intended populated target-scene performance remain unknown. The local four-asset sample scene is not a substitute.
- CI/Pages jobs were recorded as queued during the service backlog. They were not rerun in this QA task.
- No model, production record, candidate gate, permissions, or main branch was changed. Only this independent QA report and its evidence were added.

## Evidence files

- `evidence/blender-import-audit.json` — exact source/GLB geometry and material-color comparison.
- `evidence/browser-runtime-report.json` — local Chromium/Three.js runtime metrics and tested views.
- `evidence/scene-4-assets.png` — rendered four-asset scene at authored scale.
- `evidence/audit_blender_import.py` — headless Blender reopen/import audit used above.

# Batch 15 independent QA

**Reviewed:** 2026-10-18 UTC · **Reviewer:** Leon Made This · **Candidate handoff commit:** `ee22aea0066e62ee13d4902f6bcecf367d0e7296` · **Handoff JSONL SHA-256:** `789fe89411872df64a7670bc17afed9537e5c43e914e1639518f4ab3b2a5031b`

## Scope and method

Reviewed only the four batch-15 candidate tips recorded in `production/continuous-small-life-round05-20261018/work/batch-15/final-handoff.jsonl`: Beelzebufo, Pluricarpellatia, Paratingia and Stromatolite mound. Applied the main `static-stylized-v1` contract, rules `2026-10-18.1`: eight fixed views (`hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`) and zero turntable frames. The old nine-view expectation does not apply.

For each item I matched the pushed candidate tip and handoff artifact hashes, reopened the exact Blend read-only in Blender 4.3.2, independently compared its evaluated export collection with the delivered GLB, checked units/root transforms/normals/closed edges, reran both candidate checker profiles, and inspected the eight-view sheet plus exact-GLB Three.js/Chromium runtime views (including near and nine-copy scene evidence). Runtime uses ANGLE SwiftShader software WebGL; local timing is functional evidence only, not a physical-device performance claim.

## Per-item verdicts

| Asset | Frozen Blend source SHA-256 | Exact GLB SHA-256 | Verdict | Required fix |
|---|---|---|---|---|
| beelzebufo | `5f337837c9c916a4c75efe572e9f84eb884faf18f9cf07ce6d110cad74ae5509` | `67f3b628dd5bd33df681ced41ce74446cf4fc196decb58949ed0c8db5a6e7d67` | **PASS** | None |
| pluricarpellatia | `5a99a2148566f525bbeec8ba3d711b31b122fbceb7a6c95eb3d560a60ef3522c` | `1db1a4cca9d936f87fbb15213126744dd0b7a51b0a4156114558da1539210c5b` | **PASS** | None |
| paratingia | `20a5bc033271f96cea87bc40cf06da6e25a840b3f02e4dcb106b42ea99025e01` | `6d6da83a11bb7bdc59790dde6d22b07b66984041808e9926359d5705e4666f5e` | **PASS** | None |
| stromatolite-mound | `6207a8cd1e458e5a2ae129415dca975c3e076537aa26bf64b5d2abde955fdc00` | `90d7583a58345dd9e673c815a4d53b2df18be70bc8a05c1c9c8a74165ff06a2b` | **PASS** | None |

### Visual findings

- **Beelzebufo:** The broad head, low stout body and folded grounded limbs remain legible across views. Hip seams read as articulation/occlusion; no open hole, detached limb or broken silhouette was visible.
- **Pluricarpellatia:** Horizontal rhizome, visible petiole starts, broad simple peltate/cordate-style blades and rootlets read as a small rooted herb. No modern flower or unrelated reproductive organ appears.
- **Paratingia:** The narrow trunk and compound crown read clearly; differing leaflet sizes and the four-rank crown show at near/top angles. No broken or floating parts were visible.
- **Stromatolite mound:** The low mound and curved laminae read clearly. The exposed flat side is the declared teaching section. It does not read as coral or plant.

All four fit the requested naturally refined stylized low-poly direction. No microscopic reconstruction or strict paleontological measurement was a required criterion. Nominal sizes are labeled as artistic choices (0.22 m body length; 0.18 m rooted patch span; 0.90 m tree height; 0.65 m mound width). Measured extents in meters are recorded in [`results.json`](results.json).

## Technical evidence

Fresh Blender opens reported unit scale 1.0, identity root transform, finite vertex normals and no nonpositive face areas. Every export part had zero boundary and non-manifold edges. Fresh source-to-GLB audits had matching triangle counts and 0 m axis-converted bounds delta for all four. The retained Khronos reports are pinned to the exact GLBs and report zero errors/warnings; two recorded semantic rebuilds per item match the deliverables. Exact-GLB runtime reports pass with zero GL errors, and the nine-copy scenes rendered. Raw fresh outputs and hash-identified image evidence are under [`evidence/`](evidence/).

## Candidate checker outcomes

The explicitly selected `static-stylized-v1 / 2026-10-18.1` check passes for all four: profile compatibility passes and candidate-record `valid=true`. Each remains `approved_for_brief=false`, with independent stages still `unknown/pending`. This report changes none of those records and grants no publication authority.

The direct legacy-v1 checker result is **not PASS** for any item. All four invocations exit 1 with the genuine schema failure for a missing nonempty `<reference-id>.license` field: `VT-G-AMPHIBIANS.license`, `FL-pluricarpellatia.license`, `FL-paratingia.license`, and `EN-MB1.license`. The frozen reference ledgers say consulted-only and no third-party media/mesh is incorporated; reference copies are byte-identical. I did not invent a source-media license to silence the old checker. If legacy-v1 is required, the precise remaining blocker is that missing field. Under the selected static contract it remains a legacy compatibility failure, separate from this model/export PASS.

Eleven source smooth-face warnings were preserved (5 Beelzebufo, 4 Pluricarpellatia, 2 Paratingia). The reviewed style is coherent; no correction is required. Stromatolite has no smooth-face warning.

## Evidence index

[`results.json`](results.json) binds each verdict to source and GLB hashes, source commits, handoff pins, fresh Blender/source-export outputs, both checker outcomes, and original evidence hashes. The inspected images are included byte-for-byte under [`evidence/images/`](evidence/images/). Candidate assets and their original QA/runtime records remain on the recorded source commits.

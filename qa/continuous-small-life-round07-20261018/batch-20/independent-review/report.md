# Batch 20 independent QA

**Reviewed:** 2026-10-18 UTC · **Reviewer:** Leon Made This · **Candidate handoff commit:** `f4090f8bc7130347cabc73dfbcd44f81b5cd5a9f` · **Handoff JSONL SHA-256:** `365c149c01bb494be06761184c044ca0b95b001eb3d333aecf5f0eced41fd418`

## Scope and method

Reviewed only `leclercqia`, `canadia`, `salvinia` and `load-cast-bedding` from the exact batch-20 handoff. Applied `static-stylized-v1 / 2026-10-18.1`: eight fixed views (`hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`) and zero turntable frames. The legacy nine-view expectation does not apply.

For each asset, I matched the remote candidate tip and every artifact hash in `final-handoff.jsonl`, reopened the exact Blend read-only in Blender 4.3.2, and freshly compared its evaluated export collection to the exact delivered GLB. I checked meter units, identity root transforms, finite normals, positive face areas and closed/manifold parts. I reran both candidate checker profiles, inspected all eight source views, and viewed exact-GLB Three.js/Chromium runtime evidence including near and nine-copy scene frames. Runtime is ANGLE SwiftShader software WebGL; its local timings are functional evidence only, not a physical-device performance claim.

## Per-item verdicts

| Asset | Candidate tip | Blend source SHA-256 | GLB SHA-256 | Verdict | Required fix |
|---|---|---|---|---|---|
| leclercqia | `5194c8cbcacbeb496f79ec6e7cf086adf9cc03b7` | `5506fbc67c7e63f177df132909c613797607d0d68f9c1da561af008c58388cac` | `83790eda41c579b89f5abde777f7d6b6a30099df551425b21d0096a5cfc59e2c` | **PASS** | None |
| canadia | `05f4e45f5f65a33ec7ab1738b41275b5dab71bc3` | `48d72418b220c1ee4f43d4d61110ee25d333234b539ac890ea946dc0b490f529` | `8fbcd32a40b1a79c02df0e5cc4e91224606cef3482cee88990d73ab26bc02273` | **PASS** | None |
| salvinia | `a379c60eb5ace3ffbd7226fab7939e1d2dbd45ce` | `337b2a57188825adbce1c0cd37a0514009334d032ae910233c4620e5e4d992ce` | `266e49ba2eecf604aeb27cf0f7c31edfb061d34e21da7bda6657ed04d2cdf321` | **PASS** | None |
| load-cast-bedding | `1d7fdb2e890ff1c79ce341a82c4b8571462716b9` | `855edf00ff5e7893a84b513775357a177d05c9929f75b2c86733ce981075d499` | `c9c1eb75ec0d81448eb935f38bc86916ae1110617cf315972508cd4c82467e07` | **PASS** | None |

### Visual findings

- **Leclercqia:** Slender shoot and spirally placed divided leaves read coherently. The recurved central segments are visible at hero/top/near views, and the leaf bases connect naturally to the shoot.
- **Canadia:** The flattened segmented body, overlapping broad dorsal chaetal fans and two anterior tentacles are legible at close/hero angles. The very narrow front silhouette follows the intended dorsoventral flattening.
- **Salvinia:** Two broad floating leaves remain distinct from the single hanging divided submerged leaf. Connections are readable, and the submerged structure is not mistaken for true roots.
- **Load-cast bedding:** The upper and lower beds stay continuous around the rounded downward lobes. The exposed interface is the declared teaching section, not a missing face or gap.

All four fit the requested naturally refined stylized low-poly style. No strict paleontological or microscopic reconstruction was required. Nominal scales are labeled as artistic choices: 0.18 m shoot height; 0.06 m Canadia body length; 0.06 m paired Salvinia float span; 0.80 m bedding width. Full model bounds are in meters in [`results.json`](results.json); Canadia’s 0.06 m nominal scale is its body, while the full model extent includes the paired tentacles/appendages.

## Technical evidence

Fresh Blender opens reported unit scale 1.0, identity root transform, finite vertex normals, no nonpositive face areas, and zero boundary/non-manifold edges for every source part. Fresh source-to-GLB audits matched triangle counts and reported a 0 m axis-converted bounds delta for all four. The exact-GLB Khronos reports show zero errors and warnings. Two retained semantic rebuilds per item match the delivered GLB. Exact-GLB runtime reports pass with zero GL errors and the nine-copy scenes rendered. Raw fresh outputs and hash-identified image evidence are in [`evidence/`](evidence/).

## Candidate checker outcomes

The explicit `static-stylized-v1 / 2026-10-18.1` checks pass for all four: contract compatibility passes and candidate records are `valid=true`. They remain `approved_for_brief=false`; the independent stages are still `unknown/pending`. This report does not update those records or grant publication authority.

The direct legacy-v1 result is **not PASS** for any item. All four invocations exited 1 with the real missing-license-field error: `FL-leclercqia.license`, `IV-ROM-CANADIA.license`, `FL-lygodium.license` (the reference ID carried by the Salvinia source ledger), and `EN-SE2.license`. The ledgers mark the references consulted-only; no third-party media or mesh is incorporated and the frozen references are byte-identical to their contract copies. I did not invent a source-media license to suppress the old checker. If legacy-v1 is required, those exact missing fields remain its blocker; under the selected static profile these failures remain visible and separate from the model/export PASS.

Ten smooth-face prompts were retained from source QA (2 Leclercqia, 3 Canadia, 3 Salvinia, 2 load-cast bedding). Visual inspection found the smoothing appropriate to the approved style, so no corrective action is required.

## Evidence index

[`results.json`](results.json) binds each conclusion to the exact source commit, Blend and GLB hashes, handoff artifact pins, fresh Blender/source-export outputs, candidate checks, validator/runtime reports, and original image hashes. Inspected image sheets are copied byte-for-byte under [`evidence/images/`](evidence/images/). Candidate assets and their maker reports remain on the recorded source commits.

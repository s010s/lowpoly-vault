# Batch 44 independent QA — one round

**Review date:** 2026-10-19 UTC
**Scope:** `yochelcionella`, `joffrea`, `oxbow-lake-basin`, `stylolite-seam-section`, at the exact candidate tips below.
**Decision:** Three current-hash visual/form passes; `joffrea` needs one bounded visual correction. Batch is held for that repair. This is not publication authority.

## Source and review method

- Reviewed handoff source commit: `0103a2b33cc544719e16bbd9810d625e4b59c8a5`.
- `production/continuous-small-life-round15-20261018/work/batch-44/HANDOFF.md` SHA-256: `8e92751caeb662b9dc948834e4a545982ccf22faf138e0e537634d8c01912be4`.
- `production/continuous-small-life-round15-20261018/work/batch-44/final-handoff.jsonl` SHA-256: `d5c1240e719a2ca0a9b276dfad07a8baf4e773ba793767f952b6d6621f70cd78`.
- `production/continuous-small-life-round15-20261018/work/batch-44/scope.json` SHA-256: `a2d97b031caebf44c0c4008ae3ecfa5108691d77bc6d83ad0e1c3252827e0a44`; its JSONL pin matches the file above.
- Candidate base: `081606c10836f95e6d708ea02f1ed1e321595af5`; planning commit: `60c430b3b929838ce807305251dba8f3364657b3`. The four fetched remote branch tips match the handoff's full commit pins.
- Applied `static-stylized-v1` / `2026-10-18.1`, plus the repository `asset-factual-review`, `lowpoly-art-direction`, and `blender-lowpoly-pipeline` guidance. I reviewed actual eight-view pixels, runtime images, and the gray diagnostics. This is a children’s teaching-model review, not a strict scientific reconstruction.
- Recomputed SHA-256 for all 35 handoff-pinned artifacts per item: 140/140 matched. Independently matched the fixed-view manifest to all eight image files and the runtime evidence manifest to all seven runtime image files per item, including each file's byte count and PNG dimensions. All fixed views are 512×512 except the 128×128 silhouette. The rendered hero/gray views and the exact-GLB runtime hero/near images were also inspected directly.
- Read the existing source-export, mesh-measurement, Khronos, runtime, and rebuild reports and verified their pinned inputs/outputs against the archived files. Each stored rebuild output GLB is byte-identical to its candidate. I did not rerun the maker's validators, Blender exports, or rebuild queue because the pinned reports and payloads matched; serial execution, CI, thresholds, profiles, and candidate files were left unchanged.
- Reviewer/model identity is **not independently verified from execution metadata**. The requested GPT-6 Luna xhigh identity is therefore not asserted as an observed fact.

## Per-item decision

| Item | Decision | Independent visual finding |
| --- | --- | --- |
| `yochelcionella` | **PASS** at the stated stylized teaching scope | The cap is tall and laterally compressed; the subapical tube rises obliquely and has a real open mouth. The actual underside diagnostic shows the shell aperture. The shell-only boundary is clear, the calm material treatment is coherent, and the growth relief is restrained. Smooth-face source warning is intentional here and did not obscure the form. |
| `joffrea` | **MUST FIX** — one bounded form-readability repair | The long/short shoot junction and attached stalks read. In `views/preview-clay.png`, `views/preview-silhouette.png`, `runtime/hero.png`, and `runtime/near.png`, however, the terminal organs read first as narrow pointed leaf blades. Their shallow suture is not legible at normal review size, so the defining follicle-bearing fruiting state is not clear without relying on its label. This is a core brief/readability issue, not a demand for fine scientific detail. Make the existing attached organs modestly more capsule-like and make one restrained longitudinal suture readable from an ordinary view; keep the current organ count and single maturity state. Do not add unrelated leaves, seeds, a whole tree, or surface micro-noise. After correction, use only a targeted difference review against this finding. The cited primary-paper page provides text support for attached reproductive organs; its Fig. 28 caption identifies mature follicles, a twisted infructescence, follicle stalks, and suture orientation. No source figure pixels were used or treated as a proportion template. [Crane & Stockey (1985), paper page and Fig. 28 caption](https://www.researchgate.net/publication/237162379_Growth_and_reproductive_biology_of_Joffrea_speirsii_gen_et_sp_nov_a_Cercidiphyllum-like_plant_from_the_Late_Paleocene_of_Alberta_Canada). |
| `oxbow-lake-basin` | **PASS** as a generic landform teaching concept | The top/oblique views show a depressed C-shaped abandoned channel distinct from the straight through-river, with closed land/sediment necks. It reads as a simplified floodplain cutout; the rectangular outer edges read as crop boundaries. No water, named site, event, or measured hydrodynamics are claimed. |
| `stylolite-seam-section` | **PASS** as an interpretive geology section | The gray front view shows opposing irregular teeth continuing into two solid rock halves, with a narrow but readable seam gap. It reads as a teaching cut-section without a painted black zigzag or added display plinth. The clean block faces and nominal scale are appropriately bounded as presentation choices. |

**Repair criterion:** `joffrea` — fail `basic-form-and-scope` and `normal-view-craft` at this exact hash; other three reviewed models pass those visual/form criteria. For all four, factual review remains limited to the stated generic/teaching scope and the text available in the frozen reference ledgers; no exact-site or complete scientific-restoration claim is made.

## Exact candidate tips and principal pins

| Item | Remote branch tip | GLB SHA-256 | Blend SHA-256 | GLB bytes / triangles / materials / primitives |
| --- | --- | --- | --- | --- |
| `yochelcionella` | `be6b514a9180a87581b54e9ae9f7c4f1324c3786` | `b99ab145664ecff2ee669278eb6e13a7808ab0d67722030fd1430ff7b1dde498` | `7b3d1660dd59fcbdf1afab4f635aa04a992d6fc378c3ec6edcfcf25a9a2335c2` | 85,124 / 4,512 / 2 / 2 |
| `joffrea` | `b0e2c0e5fd229cecacee666c6f7ed2bb8cc5b208` | `169b06763a494c8ac7e99ba382306604ed925e0cfd0a6b5df7e39b678025447e` | `893323ef3805ce25706fce7a657627a4de30cb0c3b38cf4a1e42619d160fa264` | 91,396 / 4,904 / 2 / 2 |
| `oxbow-lake-basin` | `f3d549acfce729574fbe4b26908fe100210bab1a` | `ceb95df56c195042c87459ae720a549498fa631a5141989dbcb3b3e11c79a756` | `b9a67ef06f42b74bf8719ffe9c2d947f8fc54a62cdae8436b63c74f5b887ddeb` | 197,476 / 10,884 / 1 / 1 |
| `stylolite-seam-section` | `943d87a913b4cf306286b40caabe92f409bade68` | `f9732c4c5cfd2584316e3aa756ed25eb11c4f2af344fb11f0a20b2608835c456` | `cf6ed7581d3ca77f4bc5b1d31bd577afa308f954d69c2bf4317efe6a8a496a70` | 93,464 / 2,512 / 2 / 2 |

The full image hashes are listed in each pinned manifest. Manifest SHA-256 values independently checked here:

| Item | Fixed-view manifest (`views/render-manifest.json`) | Runtime manifest (`runtime/evidence-manifest.json`) |
| --- | --- | --- |
| `yochelcionella` | `fa8d298fb89ded805aac68d27f9821834324502f1ce94b035b625205baf38e70` | `cd9ee59cb303e6ca2e3354cf67cd1f122faf1b26b240a84781906f2cfdd9ec68` |
| `joffrea` | `0da2bde72142f618a3c8df5d86958903acbf3d467185622ae99d8d224b99294e` | `3868f63cfe5f39a45ba2457a702ff7e168f725872926e63a900967d3b850e0e2` |
| `oxbow-lake-basin` | `f015c0b52078b557b46fa92db78734577cf8e770d670404d2f2ded957be40c1b` | `0bcac3870659aaffc2dec9b980c43777431af3653fac66d0d2675b6443f208bb` |
| `stylolite-seam-section` | `0a27ec59f1c21faf3d88e9115091af84ab0218d87a53292a6e3370c002b06dd5` | `edd7bf42b15dcc91d67e0bb028943eb0df46cbfdbed2d370555e346841d704ed` |

## Source, GLB, rebuild, and runtime evidence

For every item, `source-export.report.json` pins the delivered Blend and GLB hashes, reports Blender 4.3.2, matching source/export triangle counts, matching bounds, and zero bounds error. The first three exports carry only the maker's intentional smooth-style review prompt; `stylolite-seam-section` has no source warning. The corresponding `source-mesh-measurements.json` pins the Blend SHA, meter unit scale 1.0, identity root transform, finite normals, positive face areas, and closed/manifold exported source parts. The report files also say `source_saved: false`.

For each of the four items, both `reproducibility-1.report.json` and `reproducibility-2.report.json` are `pass`, byte-identical, and semantic matches. The semantic digests are respectively:

- `yochelcionella`: `e24afd04076fd20700d0ff4d98abff8ec9368cf733b830ba6b8b09b3341a5107`
- `joffrea`: `5c96da709ebf22157a49e097afb350942b17fd15f45ded32c7ce0f5234771bb8`
- `oxbow-lake-basin`: `c91f6c1ffa239dd01720eed8ec63d7569d65df548012acd9d929101ba96a413c`
- `stylolite-seam-section`: `db5c2e4994836234ccffbf7c1653e467891ae1ea68b2df023d9795c94cbfa7d1`

I independently hashed each archived rebuild GLB output: both outputs for each item equal its candidate GLB byte-for-byte. The rebuild reports themselves correctly describe the queue records as attestations and do not claim the checker independently executed the generator.

All four pinned `gltf-validator.report.json` records show zero errors and zero warnings. Each `runtime/runtime-report.json` records seven successful views, positive render triangles and foreground pixels, and zero GL errors; each image matched `runtime/evidence-manifest.json`. The graphics string is Chromium ANGLE SwiftShader software WebGL. These results establish parse/load/render functionality only; they are not hardware-GPU or production-performance evidence.

## Record and release boundary

All four source handoffs record profile-contract pass and candidate-record validity, while `approved_for_brief` remains `false` pending independent visual stages. This review does not mutate those records or promote the other three items to publication status. The retained legacy checker result is `valid=false` for each candidate because its historic reference-license text requirement is incompatible with the consulted-only reference record; that preserved legacy result is separate from the explicit static profile and from model QA. No license was guessed or added.

The maker's frozen source paths are:

- `assets/candidates/continuous-small-life-round15-20261018/batch-44/<item>/r001/`
- `production/continuous-small-life-round15-20261018/work/batch-44/<item>/r001/`

This report is the only change in this QA branch. No models, thresholds, CI, profiles, permissions, or publication state were changed.


## Targeted difference review — Joffrea r002

**Review date:** 2026-10-19 UTC
**Scope:** Only the prior `joffrea` MUST FIX finding at r001 (`169b06763a494c8ac7e99ba382306604ed925e0cfd0a6b5df7e39b678025447e`). No other asset and no full-batch criteria were reviewed in this follow-up.

- Updated handoff source: `49b1d6cddd807c89884935974ee2de1bc27bd0fb`. Its `HANDOFF.md` SHA-256 is `0c9739ebf73ea08c6d68935dd3ba806e95ec7f0df2743a4aab68a7604bde9aef`; `final-handoff.jsonl` SHA-256 is `6e88777c4181c654596231d0a03c087266dc1fb7befedae2f72e5f5175b3adaa`. Only the Joffrea JSONL line changed from the original four-row handoff.
- The fetched remote tip for `candidate/batch44-joffrea-r002-20261019` matches the full r002 candidate commit `ed8e178b94fcbbec0a151f44f77113c4f9699c28`.
- Exact r002 GLB SHA-256: `1337fd3e1e239bb02d3b1ed0d8f6eaf1857c4f42e88add65bc71ce2c2a3e809f` (178,160 bytes / 9,724 triangles). Exact Blend SHA-256: `768bcb86d2e5b8c517ec2d5b7deaf801abc574c3241f9316e1159e78bfb79849`.

**Verdict: PASS for the two targeted visual criteria, `basic-form-and-scope` and `normal-view-craft`, at the exact r002 hash.** In the actual fixed `views/preview-hero.png` and exact-GLB `runtime/hero.png` / `runtime/near.png`, the five attached organs now read as plump elongated capsules with blunt-curved ends rather than narrow pointed leaf blades. In `diagnostics/gray-top/preview-top.png` and `views/preview-clay.png`, a restrained longitudinal groove/valve shoulder is visible along the pod bodies; the runtime hero also carries this suture relief. The gray views show relief rather than a color-only mark. The long/short shoot junction and stalk attachments remain legible. The correction adds no leaf, seed, open fruit, mixed maturity state, whole plant, or surface micro-noise. It resolves the specific teaching-form defect without expanding the scientific claim.

Actual image files opened and their individual hashes checked against manifests:

| Evidence path relative to r002 candidate directory | SHA-256 | Finding |
| --- | --- | --- |
| `views/preview-hero.png` | `c4eb708cec67d3f2dc9bb2ce7ec97f1462748423c19ec1e8bce87d060690522e` | Capsule form and longitudinal relief visible in ordinary hero view |
| `views/preview-clay.png` | `7bd2e71242d7bad66a8687a4950e0181392437ff0978f87a66301d4584b1b14a` | Gray-shaded relief remains visible |
| `views/preview-top.png` | `22d97c7dd2e3206d35d42f9ddb645f03ca4d2af525863dcdb71ad880ccc2b6a6` | Longitudinal suture visible along the attached capsules |
| `runtime/hero.png` | `43c832fc0de1f41ba53523a5b40a62cfd827094eaf4d6277c62144eacd0e8ad9` | Same form and suture on the exact GLB |
| `runtime/near.png` | `6742cd9b62591f418255ec2b9386cb6b6e724a5554ebefc23175839a038abf03` | Near view retains pod fullness and seam relief |

The fixed manifest `views/render-manifest.json` SHA-256 is `3b9d2886314a518cfbf52530e053abeaecdc76cf69997ef053d36cfb9b5f67b3`; all eight fixed image hashes, byte counts, and dimensions match. The runtime manifest `runtime/evidence-manifest.json` SHA-256 is `3594a2e143c14517f15f37f8ae75de7fa5a50664042cb15b10d5a7b7d7e3232a`; all seven runtime image hashes/byte counts match. The pinned runtime report is `pass` with zero errors and zero GL errors, using ANGLE SwiftShader software WebGL; this says nothing about hardware performance.

The pinned source-export report binds the exact Blend SHA to the exact GLB and reports matching triangle counts/bounds. Two archived rebuild reports are `pass`, byte-identical and semantic matches; their stored outputs have the candidate GLB SHA. These checks were read at the r002 pins; no new export, validator run, rebuild, or broad QA was performed.

The candidate record still has `approved_for_brief: false`; this targeted PASS only resolves the original visual repair finding. It does not update profile, publication, or any candidate-stage record. Reviewer/model identity remains unverified from execution metadata and is not claimed here.

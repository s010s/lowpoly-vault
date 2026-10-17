# Lightweight Triceratops: measured lessons and first-ten triage

**Study date:** 2026-10-17. **Scope:** an original, evidence-informed illustrative Triceratops and three environment surface comparisons. This is a case study, not a universal polygon/byte standard, scientific certification or release approval.

The user accepted the approximately 472 KB version's size and aesthetic direction. The independent finite review accepted it as a viable lightweight color tier. Earlier structure/style issues, anatomy uncertainty and missing browser-GPU evidence were not cleared. Wider budget research remains pending; **500 KB is not a library-wide cap**.

## What the controlled comparison established

All Triceratops variants below retain **14,432 exported triangles**. The lightweight derivative's POSITION, NORMAL, TEXCOORD_0 and index arrays match the final regional 2K reference exactly. The optimized plain control retains the original plain control's render-relevant arrays and materials; its unused tangents were removed. The original plain and textured controls were already matched for geometry, normals and UVs. Their accessor layouts are not identical: plain has 10,392 exported POSITION-stream vertices versus 10,141 in the consolidated textured representation. The shared oriented triangle/normal/UV digest supports shape equivalence, not identical stream organization.

| Variant | GLB bytes | Materials / primitives | Surface |
|---|---:|---:|---|
| Original plain control | 596,068 | 9 / 9 | Palette factors; unused tangents retained |
| Optimized plain control | 428,496 | 9 / 9 | Same materials and retained arrays; unused tangents removed |
| Lightweight color tier | 471,784 | 1 / 1 | One embedded 512 × 512 JPEG base-color atlas; no normal/ORM map |
| Regional 1K PBR reference | 2,689,404 | 1 / 1 | Base color, normal and roughness maps |
| Regional 2K PBR reference | 7,695,292 | 1 / 1 | Base color, normal and roughness maps |

The fair incremental comparison is **+43,288 bytes, or +10.10%**, for the lightweight color tier versus optimized plain. Comparing only with the unoptimized 596,068-byte control would overstate texture's byte advantage. Both fit this particular user's requested lightweight direction; that does not establish a default budget for other subjects or scenes.

The JPEG itself is **58,887 bytes**. Its full-mip RGBA8 estimate is **1,398,100 bytes (about 1.33 MiB)**. The 1K and 2K three-map estimates are approximately **16 MiB** and **64 MiB** respectively. These are allocation estimates, not measured browser GPU memory. Editable `.blend` files, original maps and the complete recovery archive have a separate storage/backup budget. Preview frames and any additional format decoders also have separate delivery costs.

Nine-to-one primitive consolidation is a useful structural result. It does not prove nine-to-one draw calls, faster loading or a frame-rate improvement. Actual runtime submissions depend on passes, instances and the renderer. This study used no mesh-compression extension; it did not benchmark decoder startup or compressed alternatives.

## What the images did and did not establish

The final bounded review opened the corrected exact-GLB hero/detail, original plain hero/detail, and matched plain/2K detail sheets. The saved control studio kept camera, framing and lighting stable. The optimized plain file was verified through retained arrays/materials; the old plain renders were explicitly labeled as the original control, not falsely described as new optimized-file renders.

- **Retained:** olive frill, green body, ivory horns, dark beak and modest pigment variation. Corrected views show normal colors and no large missing-texture region in those two views.
- **Lost:** much of the 2K body-scale relief and directional keratin detail. Cheeks and shoulders read as soft mottling rather than crisp scales. The lightweight result is not equal close-view quality.
- **Unproven:** a general craft improvement over optimized plain. Regional color is the strongest change; a color choice alone does not prove that a texture is necessary or superior.
- **Still open:** prior torso/joint and facial-form concerns, precise anatomy and browser GPU behavior. The final lightweight pass was not a new full-angle or production acceptance run. Earlier full-angle evidence for another hash cannot automatically approve this derivative.

Prefer the lightweight color tier when those regional color cues are useful; prefer optimized plain when minimum payload is more important. Retain richer source and reference tiers for editing and justified close-inspection uses. Do not continue adding detail after a finite study has answered its question.

## Geometry first, then useful surface detail

The dinosaur work and environment A/B tests support a practical order: primary form and proportion, secondary structure and attachment, then material-specific detail. Low-poly permits rich textures and smooth/faceted mixtures. It does not require flat colors, and adding triangles or maps does not automatically improve craft.

For the environment tests, the full-PBR B variants were rejected as default replacements. Smaller color-only D variants remained exploratory. Texture did not resolve the regular arch outline, arrow-like fern pinnae or crude conifer branch joins. A same-geometry test was useful precisely because those defects stayed visible.

This does not establish that normal/roughness maps never help. The conclusions are limited to the reviewed assets, lighting, distances and evidence. Choose additional channels when their visible contribution justifies download, decoding and runtime cost.

## Import failure worth retaining

An early lightweight render was magenta although the GLB validated and its embedded JPEG decoded. In the Blender 4.3.2 review recipe, the imported image's 58,887 bytes survived orphan cleanup. A redundant `image.pack()` call on the already-packed image with an empty filepath removed its packed payload. The GLB hash did not change.

The corrected recipe skipped images that were already packed, asserted the expected JPEG payload hash, and rendered a cheap preflight before the final views. The failed recipe, image and state log were preserved separately. This was a review-script state bug in the tested setup, not a demonstrated GLB corruption or browser-GPU problem. The shared queue renderer does not perform that repack call.

See the [controlled optimization checklist](../../skills/blender-lowpoly-pipeline/references/controlled-optimization.md#fresh-import-image-guard) for safe reuse of this lesson, including multi-image and saved-source limits.

## First-ten triage

**Recommendation: do not remake all ten.** Keep existing originals and their history. Prioritize three structural revision candidates after a new brief and explicit production authorization:

| Priority candidate | Evidence-supported issue | Next evaluation target |
|---|---|---|
| Conifer tree | Original broad smooth foliage envelopes read more like broad leaves. The separate 14,118-triangle v2 surface baseline still had plank-like joins and starburst needle clumps. | Crown silhouette, bough/branchlet hierarchy, believable joins and gaps before bark detail |
| Fern cluster | Broad arrow-shaped pinnae, abrupt folded planes and overlapping tips dominate; faint veins added little useful structure. | Curved frond/rachis hierarchy, pinna taper/attachment and negative space |
| Natural arch | Regular molded outline, repeated thick bands and generic crest dominate; 1K PBR added little value over lighter variants at the tested distance. | Unequal supports, thickness, erosion/undercuts and coherent bedding before fine grain |

The conifer v2 was a separately labeled geometry baseline, **14,118 triangles versus the original's 2,382**. Its surface comparison was not evidence that texture alone improved the original tree.

Retain and reassess the other seven: **stratified cliff, uprooted log, cycad, horsetail cluster, Lepidodendron, dinosaur nest and three-toed track**. Their earlier audit noted potential close-view improvements, such as differential erosion, breakage hierarchy, leaf cushions or internal track relief. They have not received equivalent new all-angle independent acceptance. Retaining them is neither a finding that they are flawless nor a request to start seven remakes.

Before any replacement, compare old and proposed geometry at matched scale/framing, inspect clay and relevant detail views, complete the current candidate gates, and obtain the required release decision. The sealed initial-ten WIP publication exception is not retroactive artistic approval and does not authorize swapping new assets into that release.

## Reproducible evidence anchors

Full editable files, corrected/failed renders, logs and authored reviews are preserved in the owner's private recovery archives. They are not bundled into this public documentation commit. The hashes below identify the measured artifacts; this document is not a substitute for the actual files, reviewed pixels or a complete candidate record.

| Artifact | SHA-256 |
|---|---|
| Original plain GLB | `ea03f692466b690e7292ff729d9a5834d58fa538e79366b35136182ac31a71cc` |
| Optimized plain GLB | `542d20bd8cd2b534e993858c5dcd4f0bd49bcc4a9a3dcca1c9f7484683e6202e` |
| Lightweight color GLB | `d9396f37f1d8453fa68916de8e4d6671f20b89cc96bf4687b60652006d9c2b9c` |
| Regional 1K GLB | `62a19b7808a01591c3d13ab7ecfcdd543be8c4d323289f42caa2517a5f65c520` |
| Regional 2K GLB | `c20a5ee7cf8058b79854d334a7f74e19da6a9637d74a0ed5a8f781837bfc8de0` |
| Authored lightweight cost/material review | `997bff4d6b04c74d80c5c53f9afdacf5644d2a0e644ee27c2b476aaadbaec24d` |
| Lightweight render manifest | `49582732177ff9dd7667059b33cb5a09b491ca126caf20b0a504f1c33fbba4a0` |
| Complete lightweight recovery ZIP, 27,498,749 bytes / 51 files | `3fc96b9b2ba4467baf9a45eacd1c42f477a22d763e9db0464248109ce8245122` |

The lightweight GLB's official format/project checks passed. That status is separate from the scoped visual findings and unresolved factual/GPU gates. The reusable [production and acceptance lifecycle](../../skills/blender-lowpoly-pipeline/references/standardized-pipeline.md) remains authoritative; current [role-based budget research](../../skills/lowpoly-art-direction/references/asset-budgeting.md) must not be replaced by this sample's numbers.

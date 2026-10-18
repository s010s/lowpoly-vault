# Batch 14 independent QA

**Verdict: PASS for all four frozen briefs.** I found no blocking geometry, delivery, runtime, or basic-form defect in the selected candidates. Notes that may help clarify claims or presentation are listed separately below. This report records independent compatibility and acceptance evidence; the candidate records remain pending, and publication authority is separate.

## Exact review scope

- Candidate branch: `candidate/small-life-batch14-20261018`
- Exact source commit reviewed: `5d33dccfb439c44d5342e2a1047b81891b850435` (`Document batch14 exact artifact handoff and pending independent acceptance`)
- Selected checkpoints are ancestors of that exact source commit: Montlivaltia `d76e674eabbe601a785384c2555003367b65c0b6`; Cobbania `02e88054aab7c7ca01437b7a4b3f332eebc77b1c`; Aysheaia `c74b8465056aca81a513777de212f86c0034e271`; Tafoni `2dd3f8f1a17a536ae4974dd95b6443ff4dae4e17`.
- Review tools and policy came from current `main` at `6482ec9c04a9ec2d1ac84f9e1dc3ec20dbdccbea`, static profile rule `2026-10-18.1`.
- Candidate handoff: [`HANDOFF.md`](evidence/candidate-HANDOFF.md), [`HANDOFF.json`](evidence/candidate-HANDOFF.json). Every handoff-pinned path hash/byte count matched the archived source tree. The four candidate checkpoints, exact GLBs, Blend files, metadata inputs, fixed-view sheets, manifests, and contact sheet are recorded in [`hash-audit.json`](hash-audit.json).

## Per-asset results

[Four-candidate overview contact sheet](evidence/batch14-contact-sheet.jpg).

| Asset / selected attempt | Verdict | Exact GLB SHA-256 | Bytes / triangles | Materials / primitives / textures | Six-copy runtime scene |
|---|---|---|---:|---:|---:|
| Montlivaltia · attempt-01 | **PASS** | `535626995156365c82bf6d31e7f219055a568573de07b938ccf2d2525971996f` | 199,664 / 10,800 | 2 / 2 / 0 | 12 calls, 64,800 tris |
| Cobbania · attempt-02 | **PASS** | `ee0ab0c680c3c39c97bf1dc604dd2018efecd1964f4c9e9f4b298931b44cbca9` | 193,940 / 9,896 | 4 / 5 / 0 | 30 calls, 59,376 tris |
| Aysheaia · attempt-03 | **PASS** | `315180f543e8d31d0b413116f85532be0e95cacfdffe149db263dd953562c572` | 233,320 / 12,554 | 3 / 4 / 0 | 24 calls, 75,324 tris |
| Tafoni outcrop · attempt-02 | **PASS** | `631af6bacfaa351adcffe89f453f3fd576acb1bd34bf344d6aab42f2d4bd7611` | 102,688 / 4,750 | 3 / 3 / 0 | 18 calls, 28,500 tris |

The matching exact Blend SHA-256 values are Montlivaltia `454b6d06990d177c1b926648130b5616f0a4e0d6361eaa9acaa3f58731bfed3c`, Cobbania `f9334e1c8428a4d424aa3d4a12ec2658f95a19599b0cda6448058466f09f69c6`, Aysheaia `11bc0784cd50e784eae50cc3d6d3fa62e2aaaa961384d8b10472e88f0092573c`, and Tafoni `42423442d3baab4b27ccb0afa25c93062cf32492553f2fd4ade84b29533a57d1`.

### Montlivaltia — PASS

The eight fixed views show a continuous narrow pedicel, flaring solitary cup, and legible radial ribs; the exact-GLB WebGL views preserve that shape at 80, 160, 240, and 480 px. The six-copy scene remains legible. I saw no detached cup, open edge, missing face, or visible intersection. Group-level Scleractinia material supports solitary cups and septa, but it does not verify this genus-specific stalked silhouette. The task brief bounds this as inspired teaching art, rather than a strict genus/specimen restoration, so this does not block acceptance.

- [Source eight-view sheet](evidence/montlivaltia-source_contact_sheet.jpg) · [exact-GLB runtime sheet](evidence/montlivaltia-runtime_contact_sheet.jpg)
- [80 px](evidence/runtime/montlivaltia/single-80px.png) · [160 px](evidence/runtime/montlivaltia/single-160px.png) · [240 px](evidence/runtime/montlivaltia/single-240px.png) · [six-copy scene](evidence/runtime/montlivaltia/scene-hero.png)
- Blend SHA-256: `454b6d06990d177c1b926648130b5616f0a4e0d6361eaa9acaa3f58731bfed3c`.

### Cobbania — PASS

The views read as three cupped trumpet leaves with basal pouches, joined along a short floating axis, with roots below the waterline. Connections look intentional, and the source and runtime views agree. No broken leaf surfaces or visible intersections were found. The independent source/export audit reports zero boundary and non-manifold edges for each of the three closed source components. The below-zero mounting warning is consistent with the frozen freshwater waterline origin and hanging-root contract.

- [Source eight-view sheet](evidence/cobbania-source_contact_sheet.jpg) · [exact-GLB runtime sheet](evidence/cobbania-runtime_contact_sheet.jpg)
- [80 px](evidence/runtime/cobbania/single-80px.png) · [160 px](evidence/runtime/cobbania/single-160px.png) · [240 px](evidence/runtime/cobbania/single-240px.png) · [six-copy scene](evidence/runtime/cobbania/scene-hero.png)
- Blend SHA-256: `f9334e1c8428a4d424aa3d4a12ec2658f95a19599b0cda6448058466f09f69c6`.

### Aysheaia — PASS

The fixed views show the intended corrugated, unarmored soft trunk, ten pairs of stout stub legs, and terminal claw clusters; these remain readable in actual-GLB runtime images. Fused foot roots and the front appendage/mouth shapes are continuous. No detached duplicate shell, missing faces, or visible leg/body intersections were found. The selected attempt also has zero boundary and non-manifold edges for all three source components. The Royal Ontario Museum description supports the basic body, clawed limbs, anterior mouth, appendages, and papillae; it says there was no separate head.

- [Source eight-view sheet](evidence/aysheaia-source_contact_sheet.jpg) · [exact-GLB runtime sheet](evidence/aysheaia-runtime_contact_sheet.jpg)
- [80 px](evidence/runtime/aysheaia/single-80px.png) · [160 px](evidence/runtime/aysheaia/single-160px.png) · [240 px](evidence/runtime/aysheaia/single-240px.png) · [front view](evidence/runtime/aysheaia/single-front.png) · [six-copy scene](evidence/runtime/aysheaia/scene-hero.png)
- Blend SHA-256: `11bc0784cd50e784eae50cc3d6d3fa62e2aaaa961384d8b10472e88f0092573c`.

### Tafoni outcrop — PASS

The views show a continuous slab with clustered rounded recesses and ribs. The cavities read at normal and near viewing scales, and the rear face remains solid; no missing surface or unintended through-hole is visible. The exact runtime scene preserves the shape without crowding. The NPS description supports rounded, smooth-edged clustered openings as a general tafoni form; the asset does not assert an exact site or weathering mechanism.

- [Source eight-view sheet](evidence/tafoni-outcrop-source_contact_sheet.jpg) · [exact-GLB runtime sheet](evidence/tafoni-outcrop-runtime_contact_sheet.jpg)
- [80 px](evidence/runtime/tafoni-outcrop/single-80px.png) · [160 px](evidence/runtime/tafoni-outcrop/single-160px.png) · [240 px](evidence/runtime/tafoni-outcrop/single-240px.png) · [six-copy scene](evidence/runtime/tafoni-outcrop/scene-hero.png)
- Blend SHA-256: `42423442d3baab4b27ccb0afa25c93062cf32492553f2fd4ade84b29533a57d1`.

## Verification evidence

I ran current-main `qa_glb.py` using each frozen brief's existing limits (14,000 triangles, 6 materials, 30 primitives, 1,000,000 GLB bytes), official Khronos `gltf-validator`, Blender 4.3.2 `check_source_export.py` with scripts disabled, and current-main `validate_candidate.py --profile static-stylized-v1 --profile-contract …`. No limit was changed. The independent results and actual command logs are under [`evidence/checks/`](evidence/checks/); the concise machine summary is [`independent-check-summary.json`](evidence/independent-check-summary.json).

- Per-asset raw results: [Montlivaltia](evidence/checks/montlivaltia/), [Cobbania](evidence/checks/cobbania/), [Aysheaia](evidence/checks/aysheaia/), [Tafoni](evidence/checks/tafoni-outcrop/). Each folder includes the exact GLB input copy, `qa_glb.py` JSON and command transcript, Blender source/export JSON and transcript, Khronos report and transcript, and current-main candidate-validator JSON and transcript.
- All exact GLB byte hashes match the handoff. The frozen Blend and exact GLB were independently reopened/audited; source triangles match GLB triangles for all four. Converted bounds match within the script’s fixed 0.0001 m tolerance (maximum observed delta: 0.000000014 m). All source components have 0 boundary edges and 0 non-manifold edges.
- All four official Khronos runs report 0 errors and 0 warnings. Current-main candidate validation reports `valid: true` and profile-contract `pass` for all four, while `approved_for_brief` remains false because the candidate records still have pending independent stages. That compatibility result is not the verdict in this report.
- The runtime manifests bind both single-asset and six-instance software-WebGL2 screenshots to the exact GLB SHA. Every listed source/runtime image hash was recomputed; see [`runtime-evidence-audit.json`](evidence/runtime-evidence-audit.json). The declared renderer is Three.js 0.180.0 with ANGLE/SwiftShader; this is software-render evidence, not a physical-GPU performance claim.
- Reviewed the accepted small-fauna trio v2 previews as the style reference: muted natural palettes, soft connections, and simplified readable forms. Batch14 fits that direction at intended scale; the face-on Aysheaia view is the one presentation nuance below.

## Non-blocking notes

1. **Montlivaltia claim boundary:** the WoRMS tax-details URL was attempted directly but returned 403; only a search excerpt was available, describing a solitary discoid-to-cylindroid corallum. The accessible [PRI Scleractinia overview](https://www.digitalatlasofancientlife.org/learn/cnidaria/anthozoa/scleractinia/) is group-level. Neither verifies a narrow pedicel with a flared cup as a Montlivaltia diagnostic. Current wording marks the design as inspired-by teaching art and disclaims strict restoration; keep that boundary if the name or description is reused. [WoRMS record](https://www.marinespecies.org/scleractinia/aphia.php?id=504165&p=taxdetails)
2. **Cobbania citation label:** the linked [2016 primary paper](https://apirs.plants.ifas.ufl.edu/site/assets/files/371429/371429.pdf) is relevant to a floating aquatic Cobbania, but the frozen ledger title differs from the title shown in the PDF (“Evaluating Relationships among Floating Aquatic Monocots: A New Species of Cobbania (Araceae) from the Upper Maastrichtian of South Dakota”). Consider normalizing that bibliographic label when convenient; it does not undermine the linked source or current inspired-by scope.
3. **Aysheaia front impression:** the mouth and four small papillae read as a face or eye-like pattern in the front view. The mesh uses the documented mouth/appendage/papilla arrangement and has no separate eye objects; this is an interpretation risk, not a blocking anatomy error. If displayed with factual captions, describing the dots as papillae and noting “no separate head” would prevent an eye/head claim. [ROM Aysheaia description](https://burgess-shale.rom.on.ca/fossils/aysheaia-pedunculata/)
4. **Tafoni source scope:** [NPS tafoni guidance](https://www.nps.gov/articles/tafoni.htm) supports the general shape, but not a specific site or formation mechanism. The candidate’s label stays generic, which is appropriate.

No required repair is identified. No candidate model, brief threshold, CI, or permission setting was changed in this QA branch. Publication remains a separate parent decision.

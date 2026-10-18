metasequoia b47cd91c5cd88146d9c3bf9e854e2425e3dfd220 | ovatiovermis 3487c3ce65e904130a3836e80c1c56d218bb2078 | nordenskioldia 00710386584b58bdb844e9ea8db5b2c2b0de0920 | waterfall-ledge 8a73f884021695ddbf1932ef7c1c6b2333ab8ed6
# Batch 23 independent review

**Overall disposition: FIX REQUIRED — label-only, for metasequoia.** The model geometry, Blend/GLB integrity, fixed views and runtime all pass. Ovatiovermis, Nordenskioldia and waterfall-ledge PASS. No source model was changed or rebuilt.

This review is bound to handoff `cbc6b33756fa1eb02ff9ac1b95fd84545698efda`, the four source branch tips listed above, and the exact Blend/GLB SHA-256 values in [`review.json`](review.json). It uses `static-stylized-v1`, rule `2026-10-18.1`. The expected style is natural, refined stylized low-poly teaching art; no exact fossil measurement or strict reconstruction is claimed.

## Metasequoia: model PASS; label correction required

The actual Blender source and exported GLB depict a preserved leafy branch with opposite lateral attachments and paired/decussate small leaves. They do **not** contain a cone, flower, or other reproductive structure. The geometry is attached and closed in source; exact source/export triangle counts match at 3,204, bounds match with 0.0 m delta, the Khronos report has 0 errors/warnings, and runtime renders without GL errors. This model needs no geometry edit, rebuilding, or re-export.

The one required change is the display label:

- **Primary path:** `assets/candidates/continuous-small-life-round08-20261018/batch-23/metasequoia/r001/metadata.json`, JSON pointer `/name/en`
- **Current value:** `Metasequoia opposite-leaf fertile branch`
- **Recommended value:** `Metasequoia-inspired preserved leafy branch`

The same display text is duplicated in these source records, so align the user-facing names in the same text-only correction if each is consumed by the product:

- `assets/candidates/continuous-small-life-round08-20261018/batch-23/metasequoia/r001/brief.json` `/display_name`: `Stylized preserved botanical organ: Metasequoia opposite-leaf fertile branch` → `Stylized preserved botanical organ: Metasequoia-inspired leafy branch`.
- The same `brief.json` `/subject/inventory_name/en`: `Metasequoia opposite-leaf fertile branch` → `Metasequoia-inspired preserved leafy branch`.
- `assets/candidates/continuous-small-life-round08-20261018/batch-23/metasequoia/r001/inventory-record.json` `/name/en`: `Metasequoia opposite-leaf fertile branch` → `Metasequoia-inspired preserved leafy branch`. The mismatch is specifically that “fertile” suggests the depicted organ includes reproductive structures while the delivered mesh is leafy only. A primary Metasequoia fossil study treats vegetative shoots separately from pollen and ovulate cones and cautions that isolated organs are not generally diagnostic: [Stockey, Rothwell & Falder (2001)](https://www.journals.uchicago.edu/doi/10.1086/317914).

**Do not edit the Blend or GLB to resolve this finding.** Their baseline SHA-256 values are Blend `b0543479cd9c277dc065cdeac770e0c6796c2a102da28d5c2069000d6e4d125a` and GLB `1f8c69eefb337b06b37ae03b2b28a0de1c736025180b71b28642fbc23f98c046`. No post-fix producer commit/diff is present in the inspected remote yet, so preservation of those hashes after the label edit remains to be verified when that text-only commit is pushed.

## Other assets

- **Ovatiovermis — PASS.** Soft naked body; two long anterior limb pairs, four shorter middle pairs, and three robust posterior pairs with single curved claws are connected and readable. Setae are an economical stylization. No exact locomotion claim. The broad form is consistent with the original description by [Caron & Aria (2017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5282736/).
- **Nordenskioldia — PASS.** Slender axis supports four separate radial segmented fruits on short receptacles; attachments and wedges remain legible in top/front/side/clay views. Ten wedges per teaching fruit are an art choice, not a diagnostic count. See [Crane et al. (1991)](https://bsapubs.onlinelibrary.wiley.com/doi/10.1002/j.1537-2197.1991.tb12599.x).
- **Waterfall ledge — PASS.** One continuous closed rock form reads as a resistant projecting lip above a recessed softer bed. No specific site, flow simulation, or dated landscape is claimed. The natural process is consistent with the [USGS Yellowstone Volcano Observatory explanation](https://www.usgs.gov/observatories/yvo/news/spectacular-waterfalls-are-often-hidden-gem-yellowstone-national-park).

## Verification record

- Confirmed the exact remote handoff ref and all four candidate refs against the commits in the frozen handoff; recomputed **88/88 artifact pins** directly from Git objects.
- Re-ran `scripts/validate_candidate.py` with the declared `static-stylized-v1` profile and contract: all four records are structurally valid and profile-contract status is `pass`; this checker does not approve visual quality by itself.
- Independently reopened each exact `.blend` read-only in Blender 4.3.2, compared the `EXPORT` collection against the exact GLB, and imported the GLB back. Triangle totals agree and bounds deltas are 0.0 m. Smooth-face warnings were reviewed as intentional stylized curved forms. Round-trip boundary warnings on split leaf/fruit faces are representation artifacts; the exact fixed and runtime views show no missing faces.
- Verified all eight frozen fixed-view image hashes per asset (`hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`), zero turntable frames, each view manifest's binding to its exact GLB, all runtime image hashes, and source Khronos validator reports (0 errors, 0 warnings per GLB).
- Opened the exact runtime captures in Chromium 154 / Three.js 180 / ANGLE SwiftShader software WebGL. Per-asset and nine-copy scenes show positive draw calls/triangles, visible foreground, and zero GL errors. This is functional software-WebGL evidence only, not hardware-GPU or production-performance evidence. Candidate nominal dimensions remain artistic scale choices; no resizing was applied.

## Evidence

- [`review.json`](review.json): source commits, exact hashes and per-asset results.
- [`source-evidence-checks.json`](source-evidence-checks.json): handoff, pin, view-manifest, runtime and validator checks.
- [`evidence/source-artifacts/`](evidence/source-artifacts/): byte-identical read-only copies of the handed-off Blend/GLB files.
- [`evidence/assets/`](evidence/assets/): fixed-view images and manifests, actual runtime captures, candidate records and independent Blender audit/reimport reports.
- [`evidence/source/profile-rechecks.json`](evidence/source/profile-rechecks.json): fresh static-profile checker output.

No model, budget, threshold, CI, permission, merge, publication, or Drive change was made. Publication authority remains separate.

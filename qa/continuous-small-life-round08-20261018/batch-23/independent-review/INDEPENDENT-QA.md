metasequoia 6cffc7a4eaf403e1339c9ddc022aa9ef82f661cd | ovatiovermis 3487c3ce65e904130a3836e80c1c56d218bb2078 | nordenskioldia 00710386584b58bdb844e9ea8db5b2c2b0de0920 | waterfall-ledge 8a73f884021695ddbf1932ef7c1c6b2333ab8ed6
# Batch 23 independent review — label-v002 recheck

**Final QA result: PASS — all findings from the prior independent review are resolved.** Metasequoia’s former label-only blocker is closed. No Blender/GLB rebuild or geometric change occurred. The three other assets retain their prior PASS results.

This update is bound to handoff commit `f1b0572a6642f66c2d7c716b848e3828899b6c6e`. Metasequoia’s source branch now points to `6cffc7a4eaf403e1339c9ddc022aa9ef82f661cd`; the other three source branch commits remain those in [`review.json`](review.json). The prior review is preserved as [`INDEPENDENT-QA-v001.md`](INDEPENDENT-QA-v001.md) and was explicitly named by the v002 amendment as label authority.

## Label-v002 verification

The four fields now resolve to the recommended wording:

- `assets/candidates/continuous-small-life-round08-20261018/batch-23/metasequoia/r001/metadata.json` `/name/en`: `Metasequoia-inspired preserved leafy branch`.
- `assets/candidates/continuous-small-life-round08-20261018/batch-23/metasequoia/r001/label-v002/brief.json` `/display_name`: `Stylized preserved botanical organ: Metasequoia-inspired leafy branch`.
- The same `label-v002/brief.json` `/subject/inventory_name/en`: `Metasequoia-inspired preserved leafy branch`.
- `assets/candidates/continuous-small-life-round08-20261018/batch-23/metasequoia/r001/label-v002/inventory-record.json` `/name/en`: `Metasequoia-inspired preserved leafy branch`.

The current `candidate.json` binds its brief artifact to `label-v002/brief.json`; `metadata.json` declares `label_revision: label-v002` and points to the v002 brief, inventory and amendment. The original top-level frozen `brief.json`, `inventory-record.json` and `freeze.json` remain byte-identical to the prior source commit. The producer’s preservation manifest lists 101 v001 files; all 101 match the original commit and their recorded SHA-256 values.

## Model and evidence integrity

All 95 handoff artifact pins were recomputed from the exact candidate commit Git objects: **95 pass, 0 fail**. Each remote candidate ref matches its handoff commit. The label amendment does not change model geometry or render pixels:

| Asset | Previous → current source commit | Blend SHA-256 | GLB SHA-256 | Result |
|---|---|---|---|---|
| metasequoia | `b47cd91c5cd88146d9c3bf9e854e2425e3dfd220` → `6cffc7a4eaf403e1339c9ddc022aa9ef82f661cd` | `b0543479cd9c277dc065cdeac770e0c6796c2a102da28d5c2069000d6e4d125a` | `1f8c69eefb337b06b37ae03b2b28a0de1c736025180b71b28642fbc23f98c046` | PASS |
| ovatiovermis | `3487c3ce65e904130a3836e80c1c56d218bb2078` → `3487c3ce65e904130a3836e80c1c56d218bb2078` | `1caf6f3f354a246e2c968649e680b0d51b500788e792997e29209ddbc23d26e8` | `a21f595f92b1733ddd9ff1ae5c2c7d60d62fbe50fe432f98513e807e44f68dbc` | PASS |
| nordenskioldia | `00710386584b58bdb844e9ea8db5b2c2b0de0920` → `00710386584b58bdb844e9ea8db5b2c2b0de0920` | `130862f7ab85ccd51cf367f1294e45e5fa017baa974b8a59b742986409f0f2ce` | `983079c22610d6bf826cc642ce909429f95bab99683c658ad3a21453d98e2b0e` | PASS |
| waterfall-ledge | `8a73f884021695ddbf1932ef7c1c6b2333ab8ed6` → `8a73f884021695ddbf1932ef7c1c6b2333ab8ed6` | `ff777a51aa83a6a2273d261a9d1cfbb33eb48ad2481c6e6ddc001fbf7c589af2` | `815b86ec82deb66a25b2c6588625111a7fa35bbe64f9c4f3af32e92354a92667` | PASS |

Metasequoia’s Blend remains `b0543479cd9c277dc065cdeac770e0c6796c2a102da28d5c2069000d6e4d125a` (593,908 bytes); its GLB remains `1f8c69eefb337b06b37ae03b2b28a0de1c736025180b71b28642fbc23f98c046` (118,168 bytes). Both hashes equal the previous review and the original source commit. The other three assets’ Blend and GLB hashes also equal their previous PASS records.

All eight Metasequoia fixed-view image files and seven runtime screenshots are byte-identical to the previously reviewed images, and their updated manifests still bind them to the unchanged GLB. The manifests were updated to bind the v002 brief; no pixels were re-rendered. The existing Blender source/export and GLB round-trip evidence still applies because geometry hashes are unchanged.

## Disposition and limits

**All required findings raised by this review are cleared.** No new mandatory finding remains. The source candidate’s own checker and handoff still report `approved_for_brief: false` with independent stage placeholders pending. This QA report does not alter those approval fields or grant publication authority; the handoff continues to mark publication authority as separate.

No candidate source was edited during this recheck. Only this existing QA branch report and its verification evidence were updated. No model, budget, validation threshold, CI, permissions, merge, publication or Drive changes were made.

## Evidence

- [`review.json`](review.json): final per-asset decision, source commits and hashes.
- [`source-evidence-checks.json`](source-evidence-checks.json): initial and v002 recheck index.
- [`evidence/source/label-v002-verification.json`](evidence/source/label-v002-verification.json): full 95-pin direct Git-object verification, four field values, frozen-record and 101-file preservation checks.
- [`evidence/source/label-v002-image-geometry-verification.json`](evidence/source/label-v002-image-geometry-verification.json): previous/current Blend/GLB and image-pixel comparison.
- [`evidence/assets/metasequoia/source-records-v002/`](evidence/assets/metasequoia/source-records-v002/): exact new consumer records and amendment.
- [`evidence/source/final-handoff-label-v002.jsonl`](evidence/source/final-handoff-label-v002.jsonl): exact updated handoff.

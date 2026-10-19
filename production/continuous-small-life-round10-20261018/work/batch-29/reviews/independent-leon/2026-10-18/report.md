# Batch 29 independent QA

Date: 2026-10-18
Reviewer context: GPT-6 Luna xhigh.
QA branch: `qa/independent-batch29-20261018`.

## Subject pin

This review is for exactly `batch-29`: candidate branch `candidate/small-life-batch29-20261018` at `ad5f8d9a17a0e1c1afa36ceb92dc2d349e6ee9e4`, whose parent and declared `model_source_commit` is `6cf8031f4b79d9add2f8f4dd55983bc9a3a40821`. The candidate remote tip matched the pinned candidate commit at review start.

The four reviewed IDs are exactly `azolla`, `odaraia`, `pachypteris`, and `sand-spit`. `HANDOFF.json` SHA-256 is `9f48853db2a3f87b34cdd9144f59b511554eceabcfe926b3d9855a7309137559`; `QA-HANDOFF-SCOPE.json` SHA-256 is `0d457c63576aea4e71b7bd1088ba3c054eaa47ff357723449a7ca3604c1dcd45`. Both pin source commit `6cf8031f4b79d9add2f8f4dd55983bc9a3a40821` and the exact four GLB hashes below.

| Asset / selected attempt | Exact GLB SHA-256 | Exact Blender source SHA-256 | GLB bounds (m; XYZ) | Triangles |
|---|---|---|---:|---:|
| `azolla` / `attempt-03` | `3861f85cba1eae4cfa3ac134c0dbd624f0976e9251236b582592ec5512e70710` | `e8a07997f3818cc2b691dc61be6be4d2bf9eef869878dedcc6319ead2f455711` | `0.0718 × 0.0179 × 0.1010` | 7,674 |
| `odaraia` / `attempt-01` | `f2f6d3ff078b8d4c053ff8ea723aba1474082c02bd221525cbcae648d9818de4` | `4ab1f5d6689335d9aebb0f3a48f3732d25bfb6228e36a98578fceba79bb23db0` | `0.0440 × 0.0288 × 0.1382` | 12,452 |
| `pachypteris` / `attempt-02` | `e8f84e8681fbe2a23578f093a7eb268f79edfa1c60b28fe7f26e8dd175f8faf6` | `94a63c04d6adb6877b4188837b5191fea763424947cea0204c16d46ab94941b2` | `0.1222 × 0.0033 × 0.2181` | 6,532 |
| `sand-spit` / `attempt-02` | `0bf2e41c64cc39ae46df4dd4e8cdef53d6d2e7bf1a00641c6975c9e07cd9cbd5` | `5586aba1cf19ac6c384d0b85dfd1a230b56e4fb2434e89c47bd7f676bd3ca719` | `12.0000 × 0.7355 × 5.8212` | 6,514 |

The complete file pins, artifact byte counts, mesh audit results, per-frame hashes, and independent runtime JSON are in [evidence.json](evidence.json). Exact source contact sheets and manifests are included under `evidence/<asset>/`; the original 8-view source set is linked below per object.

## What I checked

- Read the frozen handoff, QA scope, four briefs, and `static-stylized-v1 2026-10-18.1` profile rules. The profile calls for eight distinct static source views and does not turn profile compatibility into brief approval.
- Verified each exact `.blend` and `.glb` SHA against the scope, handoff, and `candidate.json`.
- Reopened every pinned `.blend` read-only in Blender 4.3.2 and ran `scripts/check_source_export.py` against the exact pinned GLB. All four reports are `pass_with_warnings`, have no errors, identical source/GLB triangle counts, and matching bounds to sub-micrometre tolerance. Each exported source part has zero boundary edges and zero nonmanifold edges. Warnings are the checker’s named-part “smooth faces require intentional-style review” notices; I reviewed the smooth forms and joins in the fixed views. I did not save or export replacement assets.
- Opened and reviewed all eight fixed views for every item: hero, reverse hero, front, side, rear, top, clay, silhouette. Each manifest has exactly 8 `source` frames, 12 `exact-glb-runtime` frames, and no turntable frames; all 20 image file hashes and dimensions match the manifest. The source views are 512 × 512 except the silhouette thumbnails (128 × 128).
- Reran the checked-in browser QA scripts from a detached scratch worktree at the pinned candidate tip. Each exact GLB loaded through Three.js `GLTFLoader` in Chromium WebGL2. Single-object checks rendered seven directions plus 80 px, 160 px, and 240 px hero extents; scene checks rendered six same-asset instances from hero and top. All eight runs passed with zero page/console errors and zero failed requests. The independent screenshots, JSON logs, and contact sheets are under `evidence/<asset>/runtime/`.
- Renderer was Chromium ANGLE SwiftShader software WebGL2, Three.js 0.180.0. This is an actual GLB loader/render check, but it is not a physical GPU or device-performance test.

## Findings

### `azolla` — visual/form pass with a note; factual reference gate stays open

The leafy axis and alternating, overlapping ranks remain legible in hero and top views; the hanging root hints are visible and their attachments do not show open seams or missing faces. At small extents the object reads more as one small fern branch than as a broad floating mat. That is a presentation limitation to keep in mind for the intended “single creeping floating branch mat” scope, but it does not break the approved stylized single-branch simplification.

PlantNET’s modern genus description supports free-floating aquatic habit, a short creeping rhizome, roots, and fronds in two alternate rows. It does not validate extinct species detail. Keep `needs-specific-reference` **OPEN** as the handoff requires; do not imply a strict fossil-species reconstruction. [PlantNET Azolla genus description](https://plantnet.rbgsyd.nsw.gov.au/cgi-bin/NSWfl.pl?page=nswfl&lvl=gn&name=Azolla)

[Azolla fixed source views](evidence/azolla/source-contact-sheet.jpg) · [Azolla independent exact-GLB runtime views](evidence/azolla/independent-runtime-contact-sheet.jpg)

### `odaraia` — visual/form pass

The open-ended tube, projecting head, paired spherical eyes, and three-bladed tail read as one connected stylized animal. The shell is intentionally very tubular and can read as a little submersible; the ROM description itself calls out the open front/back tube, large paired spherical eyes, and three tail blades. Fine segments and limbs are subdued inside the shell, but those are explicitly simplified in the frozen brief. No Dollocaris/Isoxys borrowing or unrequested anatomical claim was found. [Royal Ontario Museum: Odaraia alata](https://burgess-shale.rom.on.ca/fossils/odaraia-alata/)

[Odaraia fixed source views](evidence/odaraia/source-contact-sheet.jpg) · [Odaraia independent exact-GLB runtime views](evidence/odaraia/independent-runtime-contact-sheet.jpg)

### `pachypteris` — visual/form pass

The main and secondary rachis branches read cleanly, the pinnules have whole margins and blunt oval tips, and their curved attachments remain visible without obvious gaps. The thin edge-on silhouette is consistent with a single preserved foliage organ; the nominal bounds are about 12.2 cm × 0.33 cm × 21.8 cm. The model stays at foliage scale and does not imply a parent shrub, tree, roots, or habitat. [Museo Val Sanagra Pachypteris record](https://valsanagra.it/inventario/pachypteris/)

[Pachypteris fixed source views](evidence/pachypteris/source-contact-sheet.jpg) · [Pachypteris independent exact-GLB runtime views](evidence/pachypteris/independent-runtime-contact-sheet.jpg)

### `sand-spit` — visual/form pass

The 12 m teaching patch has a broad landward root, one attached shore side, and a free tongue that narrows and bends gently. The silhouette does not close into an island or tombolo, and no water plane is present. At the smallest 80 px extent the landform is simple, while the larger extents retain the hook clearly. The NPS description supports the key distinction: a spit is a depositional ridge extending from a coast; a connection to an offshore island describes a tombolo. This is not a mapped real coast or a sediment/wave simulation. [U.S. National Park Service: Sandy Coast Landforms](https://www.nps.gov/articles/sandy-coast-landforms.htm)

[Sand-spit fixed source views](evidence/sand-spit/source-contact-sheet.jpg) · [Sand-spit independent exact-GLB runtime views](evidence/sand-spit/independent-runtime-contact-sheet.jpg)

## Disposition and limits

Requested visual, basic-form, exact-hash, Blender-to-GLB consistency, fixed-view, and static-browser-render checks passed for all four pinned subjects. `Azolla` retains its explicitly open `needs-specific-reference` factual gate. The recorded candidate profile gates still show `approved_for_brief=false` and independent approval pending; this review does not certify the full seven-stage production path, a physical GPU, or target-device performance. The model, thresholds, CI, permissions, and Drive were not changed; nothing was merged or published.

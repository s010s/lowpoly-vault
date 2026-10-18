# Batch 11 QA evidence index

All copied contact sheets are byte-identical to files named in the candidate's frozen `view-manifest.json`. `image-hashes.json` records both their candidate-side source paths and recomputed SHA-256 values.

## Reviewed source and exact-GLB runtime sheets

| Asset | Eight fixed source views | Exact GLB runtime views |
|---|---|---|
| micrabacia | [source sheet](images/micrabacia-source-contact-sheet.jpg) | [runtime sheet](images/micrabacia-runtime-contact-sheet.jpg) |
| sengelia | [source sheet](images/sengelia-source-contact-sheet.jpg) | [runtime sheet](images/sengelia-runtime-contact-sheet.jpg) |
| coquina-outcrop | [source sheet](images/coquina-outcrop-source-contact-sheet.jpg) | [runtime sheet](images/coquina-outcrop-runtime-contact-sheet.jpg) |
| naraoia | [source sheet](images/naraoia-source-contact-sheet.jpg) | [runtime sheet](images/naraoia-runtime-contact-sheet.jpg) |

Runtime contact sheets show GLTFLoader views at 480 px projected extent, the 80/160/240 px checks, and two six-copy scene views. The separate frozen-input audit verifies all source/runtime frame hashes, exact GLB pins, zero turntable frames, and runtime JSON status.

The [accepted trio v002 before/after image](images/trio-v002-style-reference-before-after.jpg) is copied from the main-branch style reference for the requested visual comparison.

## Machine-readable evidence

- [Frozen handoff / freeze / frame hash audit](frozen-input-audit.json)
- [Source/base and checkpoint pins](source-pins.txt)
- [Reproducible commands](commands.md)
- [Image hash ledger](image-hashes.json)
- Per asset: `*-blend-glb.json` and `*-blender.log` (fresh Blender reopen + exact GLB import); `*-glb-audit.json` (project baseline); `*-khronos-summary.json` and `*-khronos-report.json` (official validator); `*-profile-validation.json` (explicit current profile result, including retained approval-pending and legacy fields).

The archived GLB input copies and all executable output reports remained under `/tmp`; only the review outputs, logs, and copied contact sheets are committed on the independent QA branch.

# Batch36 independent QA

## Scope and source pins

This is an independent review of exactly four frozen candidates: `gryphaea`, `folded-strata-outcrop`, `volcanic-bomb`, and `teredolites-wood-boring-cast`. The source candidate branch is `candidate/small-life-batch36-20261018` at handoff commit `d1974c6e84e4a52f77329419f669ee45dac2c3b9`; the model source commit is `b0e0b4e7cee3e58d68ba968f91fcb826a4f929bf`. `QA-HANDOFF-SCOPE.json` was checked for the exact four IDs, source commit, and GLB pins before review. The upstream branch tip was confirmed against `origin`.

The reviewed rule is `static-stylized-v1` / `2026-10-18.1`. Work was done in an isolated worktree and on the independent branch `qa/s010s/batch36-independent-qa-20261019`, based on the frozen handoff commit. The maker’s verdict and expected answer were not used as the visual review result. This report keeps the candidate’s existing pending approval state intact.

## Decision

**Content QA: PASS for all four candidates within their frozen, intentionally stylized teaching-art scopes. No model or geometry must-fix items.** The actual images, source Blend files, exact shipped GLBs, source/export geometry, GLB roundtrip, exact checksums, independent rebuilds, and browser renders were inspected.

**Formal profile acceptance: BLOCKED.** The available browser is Chromium 154 / Three.js r180 / WebGL2 on ANGLE SwiftShader software rendering. It loads and renders each exact GLB without browser, request, or WebGL errors, and confirms six-instance workload counts. This is functional software-render evidence; it does not satisfy the hardware-GPU gate and does not establish physical-device performance. To close that gate, record an actual WebGL2 hardware-GPU run for each exact pinned GLB, including device/renderer and screenshot hashes. No model change is indicated.

The explicit static profile checker reports each record valid with `profile_contract_status: pass`. `approved_for_brief` remains false. The legacy checker’s consulted-only reference license-field incompatibility is preserved; no license was inferred and no checker or gate was altered.

## Pinned assets and exact artifacts

| Asset | Attempt / checkpoint | Triangles · GLB bytes | Blend SHA-256 | GLB SHA-256 | Result |
|---|---|---:|---|---|---|
| `gryphaea` | `attempt-03` / `c04539436d56a2b1bd9bf7b789f7da4898c4a369` | 8,412 · 159,436 | `df78b68ab5438e6c2849e39e3aea30017ac1e007bbe8db7729f2b1702ff90b5b` | `fa7f25433044c572d589ee356625b2767f76f655226d78eff718598e3f750c7e` | Content PASS · GPU gate open |
| `folded-strata-outcrop` | `attempt-01` / `fface49adf91aebe4bc3992102e176d9f3bf455a` | 9,912 · 538,828 | `c70a65b36102fd11c9e9e5ffa2e1f800c433e7e505ab32ccfdbadb3c6dc6675d` | `dbd2512c5163b8ae8ea2f688ae94a62d62da5aea0d9ec8967e6c7f93e3086dac` | Content PASS · GPU gate open |
| `volcanic-bomb` | `attempt-02` / `7de7f002f8f3c0fd85e0655c53de871237bf5bb1` | 6,768 · 123,440 | `7d54573e0d66b25b9c9e028fa513371ffd21da2a2a64aef5ab0e9bfe97e0d82a` | `bb37a65482755f81a6d13ee4f52ff08504d3f2fe1c0212dd2059302701ea7092` | Content PASS · GPU gate open |
| `teredolites-wood-boring-cast` | `attempt-04` / `b0e0b4e7cee3e58d68ba968f91fcb826a4f929bf` | 6,912 · 230,688 | `c2cce630b43fe990a481a6888a70317a661b58dd925a6ea7e789d55dd8548211` | `f68a1e3d779205b206d4c968644974797c09fe8946039d135698c37e8e6ba2bb` | Content PASS · GPU gate open |

For each ID, the exact source files are under:

- `assets/candidates/continuous-small-life-round12-20261018/batch-36/<asset>/r001/<attempt>/<asset>/<asset>.blend`
- `assets/candidates/continuous-small-life-round12-20261018/batch-36/<asset>/r001/<attempt>/<asset>/<asset>.glb`

Maker source and runtime contact sheets plus the eight-view manifest are in the same directory. Their hashes and bytes are pinned in `production/continuous-small-life-round12-20261018/work/batch-36/HANDOFF.json`. Independent runtime captures are under `evidence/runtime/<asset>/`; the original source/export reports and GLB roundtrip reports are under `evidence/blender/<asset>/`.

## Per-asset findings

- **Gryphaea — PASS.** The silhouette reads as a deep, recurved principal valve with a smaller, flatter lid aligned to its mouth. Growth relief is visible, and the model has no soft tissue. The [Cambridge TF0105 page](https://p1acollections.esc.cam.ac.uk/p1acollections/exhibits/show/bivalves/tf0105.html) describes two articulated unequal valves, flat upper right and curved lower left, with umbo and growth lines. The candidate stays within a stylized shell-only concept and makes no exact-specimen claim. No required fix.
- **Folded strata — PASS.** Six substantial continuous beds bend through an anticline and syncline; exposed thickness and the fold survive neutral clay and actual-GLB views. The [NPS tectonic landforms page](https://www.nps.gov/subjects/geology/tectonic-landforms.htm) supports the broad fold vocabulary. Bed count, section, dimensions and colors are labeled teaching-art choices, without a named site or strain claim. The GLB is 538,828 bytes: above the usual 500 KB soft range but below the 1 MB hard cap. The solid beds are readable structure, so no reduction is required.
- **Volcanic bomb — PASS.** The single slightly irregular spindle clast remains clearly readable from the fixed and runtime views, with shallow integral relief and no weapon or eruption-scene framing. The [NPS Little Springs account](https://home.nps.gov/para/learn/nature/the-little-springs-eruption-at-mt-trumbull.htm) describes a rounded spindle bomb with a stretched end and degassing cracks. This candidate is an original stylized teaching concept; its shallow grooves are not presented as an exact copy of that specimen. No required fix.
- **Teredolites — PASS.** The cut host reveals five club-ended cavity forms, two matching visible infill casts and three open cavities; the grain lines stay subordinate. The section view makes the internal relationship clear, and top/bottom views are consistent with the sectional display. The [PRI Digital Atlas](https://www.digitalatlasofancientlife.org/vc/trace-fossils/dwelling-traces/) supports Teredolites as borings in fossil wood; [KU Ichnology](https://ichnology.ku.edu/invertebrate_traces/tfimages/teredolites.html) describes clavate/club-shaped to flask-shaped tubes in woodgrounds. The candidate claims no exact excavated specimen, producer or tree species. No required fix.

## Checks and evidence

- `evidence/handoff-integrity.txt` records 157 exact handoff path/hash/byte checks, matching source-commit GLBs, and the exact scope echo.
- `evidence/source-snapshot.json` pins the source branch, handoff commit, model source commit, QA scope and their hashes.
- `evidence/profile/<asset>.json` records fresh `static-stylized-v1` validation. All four are `valid: true`, `profile_contract_status: pass`, and remain `approved_for_brief: false`.
- `evidence/glb/<asset>.json` records independent static GLB audits. All four exact GLBs have no errors or warnings. `evidence/gltf/<asset>/gltf-validator.report.json` is a fresh official Khronos validation: 0 errors / 0 warnings for each exact checksum.
- `evidence/blender/<asset>/source-export.json` reads the exact Blend without saving it, audits the exact GLB and compares triangle count and axis-converted bounds. Triangle counts match at 8,412 / 9,912 / 6,768 / 6,912; maximum bounds discrepancy is under `0.000000008 m`. `source-scene.json` confirms the source roots and evaluated parts reopen; `glb-roundtrip/glb-roundtrip.report.json` records fresh Blender imports of the exact shipped GLBs.
- Each candidate was independently rebuilt twice in an isolated output root with one worker and two Blender threads. All eight runs succeeded and every rebuilt GLB was byte-identical to its frozen candidate, as well as semantically identical. Results are in `evidence/rebuild/rebuild-comparison.json`; the queue and its run records are retained alongside it.
- Independent Chromium reports capture 10 single-item views plus hero/top six-copy scenes for each GLB. They record exact GLB SHA, Three revision, renderer, API, calls, triangles, per-view GL errors and screenshot SHA-256 values. There are no page/console errors, failed requests or WebGL errors. Renderer: ANGLE SwiftShader software.
- Intentional smooth-normal warnings were inspected in actual pixels. Source parts remain closed; GLB roundtrip boundary-edge warnings are consistent with normal/vertex splitting on import and show no visible missing surface. No required warning remains undispositioned.
- References are consulted only. No image, scan, mesh, texture or external code is incorporated; consulted source pages are not treated as asset licenses.

No candidate model or maker file, threshold, gate, CI, permission, release record or external Drive content was changed. The only deliverable is this independent QA report and its hash-bound evidence on the separate review branch.

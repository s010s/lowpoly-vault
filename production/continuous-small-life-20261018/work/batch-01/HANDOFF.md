# Batch 01 — four built candidates, independent QA pending

Branch: `candidate/small-life-batch-01-20261018`. Based on main `643534830397824dfd46990485bd16ad66ecf9ce`. Planning copied from `ac44f7de4082fde7fada3adc0324882b80fb2bb1`. No merge, publication, Drive use, CI edit, global site logic change, or other-batch production.

Each bundle is `assets/candidates/continuous-small-life-20261018/batch-01/<ID>/r001/`. Use `candidate.json`, `brief.json`, `references.json`, `reference-access.json`, `execution-brief.json`, `source-metadata.json`, `view-manifest.json`, `contact-sheet.jpg` and `checksums.sha256`. Model source and GLB have the asset ID as filename. Eight real Cycles views include a transparent hero. `evidence/runtime` contains the exact GLB at normal/near scale and seven directions, plus a neutral three-copy benchmark. `evidence/technical` retains executed command logs, separate rebuilt GLB, semantic comparison, source reopen and clean-import reports. Geometry remains in meters; tiny-specimen source previews use temporary presentation scaling only.

| ID | GLB bytes | Triangles | Source/evaluated vertices | Export POSITION vertices | Materials/primitives |
|---|---:|---:|---:|---:|---:|
| archaeopteryx | 141564 | 3776 | 2040 / 2040 | 4518 | 5 / 14 |
| canadaspis | 112708 | 4276 | 2276 / 2276 | 3220 | 5 / 14 |
| ceratomyrmex | 43596 | 1856 | 976 / 976 | 976 | 5 / 11 |
| hydropteris | 234596 | 5332 | 2904 / 2904 | 8214 | 4 / 6 |

All are original palette-only geometry: zero textures, zero texture encoded/decoded bytes. The small ant is intentionally below the usual byte range; no filler geometry. Full exact hashes for source, GLB, generator, config, brief, reference ledger and contact sheet are in `handoff-hashes.json` and each candidate record. Every bundle file has an integrity digest in `checksums.sha256`.

Completed commands and outcomes:

- `python3 production/continuous-small-life-20261018/verify_plan.py`: PASS, frozen planning inputs unchanged.
- `node scripts/validate_gltf.cjs assets/candidates/continuous-small-life-20261018/batch-01`: all four 0 errors / 0 warnings.
- `python3 production/continuous-small-life-20261018/work/batch-01/verify_builds.py <ID>`: actual separate Blender build, source reopen and clean import all returned 0; semantic digests matched. Retained per-bundle reports and logs.
- `node production/continuous-small-life-20261018/work/batch-01/browser_qa.mjs <ID>` with the local review server: pinned Three.js r180 loaded exact files, matched bounds, no page/console/request errors; three-copy work counts measured. Renderer is ANGLE Vulkan SwiftShader: functional software evidence, not physical GPU/device performance.
- `python3 production/continuous-small-life-20261018/work/batch-01/validate_bundle.py`: all four PASS for current practical fixed-view evidence integrity and configured budgets. This does not approve art/science.
- `python3 scripts/test_qa_glb.py -v`: 14 tests OK. `npm test`: exit 0. `npm run build`: exit 0; existing 16 published assets remain allowlisted, candidate assets excluded. Logs in `checks/`.

For a fresh rebuild without overwriting frozen evidence:

```sh
blender -b -t 2 --python-exit-code 1 --python production/continuous-small-life-20261018/work/batch-01/build_batch01.py -- --asset archaeopteryx --output /tmp/batch01-review-rebuild
# Canadaspis uses build_canadaspis.py; the other three use build_batch01.py.
# Add --render for the eight source views, or --config <frozen config path>.
```

The checker reports smooth organic normals as a review warning; intentional feather/leaf facets and split exported normal vertices are documented separately. The closed authored source parts have zero boundary/nonmanifold edges. Missing optional Draco and read-only Blender extension-cache startup notices do not prevent uncompressed exports. A packaging-only p002 renamed metadata to `source-metadata.json` to avoid the existing recursive publication scanner; source/GLB/PNG hashes were verified unchanged. No global scanner or release descriptor was modified. The initial failed build log is preserved beside the succeeding build log.

Parent should dispatch the requested fresh GPT-6 Luna xhigh independent visual/factual/specification review, bound to exact hashes in `handoff-hashes.json`. All acceptance statuses remain pending. Historical `validate_candidate.py` has turntable requirements that conflict with this frozen zero-sequence practical brief, so no historical-schema approval PASS is claimed. Some primary PDF/image endpoints returned 403; the access ledger distinguishes opened museum/paper abstracts, indexed original-paper support and inaccessible full texts. Exact colors, fine feather/segment counts, missing soft tissue and dimensions are explicitly artistic, not verified scientific restoration.

Per-model normal pushed checkpoints:

- Archaeopteryx: `fd0f5a4c68b318262944a6528daead3327c8c987`
- Canadaspis: `0486bdd343690971f38d5742fc6075202f1ec781`
- Ceratomyrmex: `3267e1e46d3d439987d2d62fc2bc5ab57a7f8a0e`
- Hydropteris: `d2d04d752a80f3bd207439f1816bcb997b5725e8`

The final evidence-packaging commit follows these checkpoints. Merge/release stays with the parent coordinator.

# Conifer published and verified

Published main commit: `01c60dd85322932a967c4f2aa50045f2da1a25bd`.

- [Exact candidate complete Linux CI](https://github.com/s010s/lowpoly-vault/actions/runs/39040133125): success;250 preview bytes compared with zero mismatches; full repository/queue/pipeline, production build, real GLBs, image scrub, original and new conifer handoff, modal motion and explicit fallback all passed.
- [Main complete build and GitHub Pages deployment](https://github.com/s010s/lowpoly-vault/actions/runs/39040688596): success at the same commit. No force push, permission change or history deletion.
- Live [English conifer](https://s010s.github.io/lowpoly-vault/models/conifer-tree/) / [中文针叶树](https://s010s.github.io/lowpoly-vault/zh-CN/models/conifer-tree/).

`publication-summary.json` binds the approval and delivered artifacts. Independent Linux candidate record SHA256 is4ecdcbc679099789ab917f72e0cc6ffbb959a9b870e16698f325a2283c41ef27. GLB remains715500 bytes/19052 triangles; original source Blend/model are unchanged. Poster/frame0 fb46be69…dab975 is the independently approved Linux canonical image. All24 original Mac and Linux evidence sets, their separate approvals, failed CI logs and original model/failure histories remain preserved.

## Actual live acceptance

`live-files.json`:361 deployed files/routes return200 and equal the exact local production build hashes, including all26 bilingual documents, actual GLB/Blend, all240 frames and10 card posters, scripts, fonts, and10 download ZIPs. Every fetched ZIP passes CRC and its entries are individually hashed. The new conifer ZIP SHA256 remains55f96771afe827fff62971f396d4caead2274be76384ca8ff6762daf532c4d56. `live-other-nine-check.json` compares45 live delivery files for the other9 assets to the independently checked pre-conifer baseline; all match.

`live-cycle/report.json`:fresh isolated Chromium against ordinary public URLs confirms the bare live manifest equals the production build, all10 actual models load during consecutive previous/next navigation, one live scene at a time, and zero after close; no page errors. The retained conifer screenshot was visually inspected.

`live-handoff/report.json`:the full current conifer suite ran against the actual public origin, not the local dist server. Ten checks and7 recorded cases pass, including desktop/retina/mobile/reduced-motion/dark frame7→actual GLB, retained image ownership, close/reopen, context-loss recovery, immediate GLB failure fallback, rapid Back and delayed-import history. No page errors. Actual desktop/mobile GLB pixel captures retained. `live-handoff-harness-provenance.json` records the only harness transport changes:public origin and per-browser local proxy. Assertions and the corrected common-square sampler are unchanged. This is software-rendered functional verification, not physical-device performance acceptance.

`candidate-ci/` preserves selected original Linux reports/captures. `candidate-ci-artifact-inventory.json` hashes every downloaded QA artifact file; full original artifact remains in the linked run and locally under ignored qa/release-conifer-doc1-live/. Test videos are not placed in the Pages artifact.

## Environment investigation and preserved failures

`environment-comparison.json` records evidence-supported differences:macOS27 arm64 with explicitly selected full Chromium.app versus Ubuntu24.04.5 with default Playwright Headless Shell. Both identify Chromium141.0.7390.37/build1194 and use the same viewer, preset, DPR and requested SwiftShader backend. OS and browser package are not isolated; no proven single root cause or cross-platform byte equality is claimed. Use the exact independently approved canonical Linux images; the zero-mismatch gate remains unchanged.

Prior image mismatch39038352273 and the new conifer mobile sampling failure39039596864 remain preserved in the earlier QA folders. The latter sampled square preview at384px versus actual model at192px. The QA-only correction uses equal visible-square sampling and explicitly asserts equal sampling resolution; all original3% scale/3px displacement, alpha, camera, parity and navigation thresholds remain. Successful candidate Linux mobile max scale step is1.3333%; no production renderer/model/image change was needed for that measurement correction.

KHR_mesh_quantization and tested Three.js0.180.0 requirement, scoped M5 Pro/Metal measurements, SwiftShader frame-budget failure including single tree, unverified other devices/loaders and fine-needle aliasing remain disclosed. No universal performance claim. All owned local browsers, test servers and foreground probes exited; no unrelated process was touched.

This receipt is stored on the integration branch after deployment; main remains the exact verified release commit above. Receipt-only files are excluded from the361-file production allowlist.

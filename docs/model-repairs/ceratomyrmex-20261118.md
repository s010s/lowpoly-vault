# Ceratomyrmex material repair candidate

- Revision: material-20261118. Work in progress, not deployed.
- Only body Material_0 metallicFactor default 1 → 0. Two previous side repair materials stay unchanged. GLB BIN byte-identical; all geometry, textures and anatomical structures preserved. Validator: 0 errors / 0 warnings.
- Original imported editable Blend updated to the same material and reopened in Blender 4.3.2. Geometry, UV, matrices and packed-image hashes unchanged. This is not a newly reconstructed model or original modeling project.
- Eleven disconnected components / 202 faces were highlighted in five views. They lie on the posterior abdomen, not legs/antennae, but their intent cannot reliably be distinguished from adjacent attached surface projections. Deletion test was rejected. No topology removal in delivered model.
- Material control in two identical-camera pairs improves eyes, thorax and abdominal shading while retaining brown/orange body and yellow-brown legs. Existing surface projections remain a stylistic/anatomical limitation, not claimed repaired.
- Paired new wheel/detail images captured from source 7f20f92544c2708b1c11187e086a7dc128bb27ba (production renderer identical to c49ae7ba); fresh wheelSpec from the actual capture. Old assets/posters remain available at original revision paths.
- Selected two-model catalog test uses actual c49 compiled JS with actual original/candidate assets served locally, without JS injection. This is not yet final unified-branch integration or 939-model QA.
- Original baseline: desktop 30 / phone 57 sampled frames. Candidate: desktop 24 / phone 50. Both desktop sequences contain timestamp inversions; mobile sequences monotonic. These are finite samples, not continuous all-frame proof.
- Candidate held→live full-page mean RGB difference: desktop 0.632435, phone 0.505235; differences remain in shadow/fine edges/UI. Actual viewed position, orientation, size and brown material remain consistent, no substantive abrupt model change observed in these views.
- Six bounded retry/cancel/history regressions passed; failed request is ERR_FAILED, not simulated HTTP 503. Cancellation is not proof of completed stale response handling.
- Independent review, unified branch integration visual verification and exact-commit CI still required before completion. Original lineage/source scope retained; no claim of scientific anatomical reconstruction.

Independent bounded review: accepted the material benefit and conservative geometry retention. Actual original/new material views and both held/stable endpoints inspected; no substantive position/scale/orientation/main-colour jump observed. Independently checked model JSON/BIN, four delivered asset hashes, 938 non-target manifest entries and resource isolation. Candidate desktop has one timestamp inversion, phone zero. Reviewer did not independently reopen Blender or rerun browser. Unified integration and exact-commit CI remain pending.

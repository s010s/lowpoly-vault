# Canadaspis: retain current model; verify shared handoff fix

Review baseline: `4bc5dcc7cf6a57cb6feec83d5fe319ef78a92123`.
Model: `a0bbc63b3d0ef37121bc50187952f7b2b6c2791b552bfbf2c24e555d9b0b8929` (2,107,076 bytes; 33,000 triangles).

No model, texture, poster, orientation, or Blender source is replaced by this commit. The existing brown material and recognizable paired carapace, antennae, segmented abdomen, and tail projections are retained. A temporary metallic=0 comparison lightened the entire model to sandy tan; that style change was not adopted. Small appendage simplifications and ventral occlusion are existing accepted limitations, not a new reason to regenerate this asset.

Nine local rendered views were inspected. Exact-position topology analysis found 23 boundary edges in five groups and one non-manifold edge. Screen projections place four groups at fine antenna/tail endpoints and one at the shell/abdomen transition; projection alone does not prove a visible defect or authorize capping. No geometry was patched. The published editable source was reopened with packed texture present; it is an existing GLB-derived source, not proof of the original generation session.

## Actual source regression

The unmodified shared fix at the baseline commit was compiled locally with Vite. Current full catalog metadata and the exact Canadaspis assets were served; this was target-limited delivery, **not** the all-asset release build or a deployment.

- Desktop 1440×1000 and emulated touch mobile 390×844 loaded the exact expected GLB SHA with HTTP 200 and reached ready, with no JavaScript page errors.
- First source run: 39 desktop and 58 mobile CDP samples, no timestamp inversions. In the 24/14 samples whose CDP timestamps were at or after the settled-poster interaction event, the prior empty-model flash did not recur. Finite sampling is not a continuous-frame guarantee.
- The old production snapshot had two mobile samples without the model; its next image was the poster, not proof of 3D readiness. Those old observations are not attributed to the new source build.
- Portable-script rerun: 34 desktop / 58 mobile samples; one timestamp inversion on each device. The 23/14 samples whose CDP timestamps were at or after the settled-poster interaction event retained dark model features; this is limited sampling, not an ordering or duration guarantee. The first attempted external-server run failed with connection refused before capture; starting the server in the same execution session resolved the fixture issue.
- Existing source unit tests for poster-cache identity and stage handoff passed. This change does not copy the earlier diagnostic pre-navigation delay or add a new waiting/navigation contract.
- Counts above use event-time comparison, not marker.nextFrame: the latter gives 25/14 and 24/14 respectively and includes an earlier desktop sample. CDP ordering remains limited by the documented inversions. A non-target Cooperoceras request returned 404 in the target-only fixture; it is not a Canadaspis success or a whole-site pass.
- Original poster-to-3D dark-feature bounds differ by at most one pixel in the checked endpoints. Pixel colors are not identical (sampled original PC/mobile dark-intersection mean absolute channel error approximately 3.04/7.28). Stable-render ROI equality must not be used to claim exact poster/3D color equality.

## Re-run

Serve a built gallery containing this exact model and its original matching posters. Then:

```sh
QA_BASE_URL=http://127.0.0.1:PORT/lowpoly-vault \
QA_OUTPUT_DIR=/path/outside/repository/canadaspis \
node site/gallery/tests/canadaspis-handoff-browser.mjs
```

The test uses sandboxed headless Chromium, rejects other origins, delays the exact model response, performs the actual selection/mobile interaction, saves finite frame samples, and asserts the target response SHA and final model identity. Captures are kept outside Git. A viewer must inspect the captured transition; ready and hash assertions alone are not a visual pass.

No new scientific/original-input-source certification, physical-device performance guarantee, complete shared matrix, or production deployment is asserted. No evidence currently justifies regenerating the model; remaining batch integration and deployed-device checks belong to the shared release process.

## Integrated follow-up at c49ae7ba

The exact current model was then checked in the five-model integrated build of `c49ae7ba2216f6fbff5bc5b1177d12e8d6eb5d23`. Its desktop/phone handoff captures contain 7/4 finite, monotonic CDP samples, matching successful response-byte hashes and no page or HTTP errors. The four held/ready stage images retain the same brown model, framing and orientation; sampling and fine shadow/raster differences remain limitations.

The three other models' 24 regressions were **not** counted for Canadaspis. The unchanged regression script committed at `7f20f92544c2708b1c11187e086a7dc128bb27ba` was separately run with `QA_MODEL_IDS=canadaspis`: all eight desktop/phone cases passed (rapid reselection, cancellation after switching to Confuciusornis, visible retry after controlled failure, drag then Reset). Retry required at least two requests. Reset waited for the real animation endpoint and retained the camera/target `1e-4` and quaternion `1e-7` tolerances. Mouse drag in a touch-emulated viewport is not native multitouch, and the late-response case tests cancellation rather than successful stale data delivery.

This completes this model's scoped repair review and integrated regression without replacing its assets or requiring regeneration. Batch deployment and its post-deployment checks remain separate; this is not full-inventory, all-device, or production-release acceptance.

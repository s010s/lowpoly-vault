# Integrated review: Confuciusornis, Diplomystus, Archaeopteryx

Tested production source and assets: `c49ae7ba2216f6fbff5bc5b1177d12e8d6eb5d23` on `repair/live-models-review`. No production rendering code was changed for these checks. This records scoped acceptance evidence, not deployment or completion of the entire model inventory.

## Scope and outcome

The unmodified Vite source was compiled once. The project's normal delivery, gallery/catalog and static-route functions generated a five-model local review site. Missing public resources were served from the same clean Git worktree. No alternative rendering implementation, substituted catalog response or replacement model response was injected. Test instrumentation records runtime state and exercises the existing selection API. GLB delay/failure was controlled in the browser; successful responses remained the real built assets.

For each of the three models, desktop (1440 px) and touch-emulated phone (390 px) poster-to-3D views were checked against the current asset SHA. The twelve before/after stage images received independent review. Position, scale, orientation and main colour/material appearance remained consistent. Fine feather/scale edge sampling and shadows are not pixel-identical; no wholesale style/material replacement or projected-position jump was observed.

Finite captured frames: Confuciusornis 7 desktop + 6 phone; Diplomystus 36 + 6; Archaeopteryx 34 + 6. One Archaeopteryx phone timestamp reversal is retained. These are 95 finite samples, not a guarantee about every frame. Sampled states contained no wrong model ID or hidden poster without a model. JavaScript and HTTP error lists were empty for these handoffs.

Twenty-four browser regressions passed: three models × two viewports × rapid same-model reselection, late-response cancellation after switching models, visible failed-load retry, and drag followed by Reset. Rapid reselection means three calls after the model is ready, not exhaustive clicks during loading or bridge animation. Phone rotation uses mouse-drag simulation in a touch-emulated viewport, not native multitouch. The regression script's SHA check validates runtime asset metadata; actual response-byte hashing was separately performed in the handoff capture. Retry cases issued at least two GLB requests, now enforced explicitly.

Reset's final camera and target match the original within `1e-4`, and model quaternion within `1e-7`.

## Test corrections, not production fixes

An early mobile harness call made before initial UI readiness timed out. The reusable test waits for the actual initial selected poster to become ready rather than merely the renderer export.

A fixed-900-ms Diplomystus desktop Reset assertion failed. That old sample did not record animation activity, so its exact state cannot be reconstructed. Checking the actual animation endpoint passed without relaxing tolerances. All six Reset cases were rerun with endpoint waiting and the additional target/quaternion assertions. The test waits for both `cameraTransition === false` and no active view transition, after the transition's final write.

## Reproduction

Run `qa/repair-integration/integrated-browser-regression.mjs` with `QA_BASE_URL` set to a running local build and `QA_OUTPUT_DIR` set to an evidence directory. It requires Playwright and sandbox-capable Chromium. The catalog must include the target models plus Confuciusornis and Diplomystus as switching anchors. `QA_MODEL_IDS` can select a comma-separated subset. The script writes success records or a failure record and never edits production assets.

Headless/touch emulation is not physical-device certification. The five-model review does not replace full-inventory visual review, whole-model scientific/artistic assessment, or full release validation. Later changes to shared rendering or these assets require affected checks to be rerun. No PR, merge or production release is implied by this report.

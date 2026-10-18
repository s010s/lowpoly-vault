# Touch zoom diagnostics

Original `site/shared-model-browser-test.mjs` remains unchanged. Full current run: 16/17 pass; `trusted-touch-swipe-and-tap` fails because the zoom tap after a CDP canvas gesture has pointer/touch events but no compatibility click within the original test window. The same failure reproduces at base `77720858d73fcb8f6b8845576851762dcba078ef` with the same cloud Chromium 154.0.8037.57.

The patches create disposable scripts under site/ so all original relative imports remain correct. They select only this test and log capture-phase trusted input events. Apply one from the repository root, run with the same Playwright/Chromium environment, then remove the resulting disposable script.

- `touch-zoom-diagnostic.patch`: original gesture schedule + event logging; fails on current and base. See `touch-diagnostic/` and `touch-baseline/`.
- `touch-zoom-no-press.patch`: disables the new CSS pointer press for the zoom tap; still fails. See `touch-no-press/`.
- `touch-zoom-settled.patch`: permits 400ms after the canvas gesture before the next tap. Trusted zoom click, camera distance, return, renderer reuse and subsequent swipes all pass. See `touch-settled/`.

Example:

```sh
git apply qa/animation-refinements/diagnostics/touch-zoom-settled.patch
CHROMIUM_PATH=/usr/bin/chromium PLAYWRIGHT_BROWSERS_PATH=/workspace/playwright-browsers QA_OUTPUT_DIR=qa/touch-repro node site/.touch-zoom-settled.mjs
rm site/.touch-zoom-settled.mjs
```

The 400ms diagnostic is additional evidence, not a replacement of the original failure. It narrows the symptom to native touch/click gesture sequencing in this environment; it does not certify the root cause or physical touch-device behavior.

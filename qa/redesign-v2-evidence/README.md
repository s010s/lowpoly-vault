# Review evidence, 2026-10-16

Code commit: `7bd2ced4948a36dfb28dbb0367de0da61786f529`. Both profiles passed in [run 38953140279](https://github.com/s010s/lowpoly-vault/actions/runs/38953140279). Reports are copied verbatim from the CI artifacts. The selected screenshots are actual browser captures, not mockups.

- `strict-gpu-report.json`: all 10 real models rendered through Chromium 141 software WebGL/SwiftShader. This is not a physical GPU benchmark.
- `fallback-only-report.json`: WebGL creation deliberately fails; previews and downloads remain usable.
- `*-390-touch.png`: 390×844 touch-emulated Chromium, not an Android device. Detail screenshots show the viewport; homepage captures show the entire page.
- `no-js-detail-zh-CN.png`: real directory-index HTML with JavaScript disabled. Specification-label contrast was fixed after the previous screenshot review.

Visually inspected English desktop home/detail, Chinese narrow home/detail in light and dark, dark desktop catalog and Chinese no-JavaScript detail. No layout clipping or horizontal overflow was found in these selected captures. Artistic/scientific model approval and physical phone testing remain pending. Full CI artifact sets are included in the prepared incremental backup; the remote receipt is verified separately.

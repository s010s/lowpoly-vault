# Calceola: retain accepted original

Review baseline: `d0d38f94b920a1972cbe09bb5f4d9abcf7bffd51`.
This review changes no production asset, manifest, material, poster, camera recipe or renderer.

- GLB: `df84e3b770382473d6f23d42c38e25fc592d6ff7fb7308995c0a53d59f08ac13` (2,046,000 bytes).
- Imported editable Blend: `4e8a813458c0e4fd2d323bc8c9f6f69f3a1f4d43a667f49ba83c9d01fc180da6` (2,456,923 bytes). This is not the original authoring session.
- Existing artistic educational scope and unknown physical/biological scale remain unchanged. The lid opening, ribs and dark recessed regions are preserved, not blindly filled.

## Actual checks

The official Vite/source delivery pipeline built a scoped site from the baseline above. Desktop 1440 and simulated phone 390 screenshots compare the real held detail poster against the actual original GLB after release. Main position, scale, angle and brown material appear consistent. There were 28 desktop and 6 phone screencast frames, with monotonic timestamps, exact GLB response SHA and no recorded HTTP/JS errors. This is finite sampling, not every-frame or real-phone certification; page/title motion is not an all-pixel stability claim.

Four actual runtime angles per viewport were captured with original material and a metal0 diagnostic control, explicitly redrawing after each change. Metal0 makes the surface substantially paler without establishing a needed repair. The original material and posters are retained. This is not a new material candidate or a geometry reconstruction.

The shared browser regression passed 8/8 cases: two viewport sizes, ready-then-reselection, late response, retry (at least two attempts), and rotation/reset. Reset waits for the true motion endpoint and retains camera/target 1e-4 and quaternion 1e-7 thresholds. Mobile rotation uses simulated mouse input, not all-touch hardware certification.

`node qa/repair-integration/calceola-test.mjs` passes actual original GLB/Blend/preview hashes, original manifest preservation, source-bound gallery poster resolution, official generated download bundle member bytes/CRC and source/license credits. Its initial credits assertion incorrectly expected the full description in CREDITS; it was corrected to the actual import-provenance text, while independently asserting the description's original-session disclaimer. No production change was used to make the test pass.

Independent review and exact integrated-head CI are still pending. No deployment is claimed.

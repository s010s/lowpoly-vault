# Bird pair r2: actual Chromium runtime review

**PASS for both corrected static bird props.** The original r1 missing-surface defect is fixed. All five actual browser screenshots and all twelve r2 Blender preview images were inspected. No remaining blocking visual defect was found for the child-friendly environment-prop scope.

- Exact asset checkpoint: `d5cc3d2f3ff34d032dbd740470e3c454e2909405`.
- Tested QA commit: `61ca734a388d38194ae9d0d57b101b80790c588a`.
- [GitHub Actions run 39090931667](https://github.com/s010s/lowpoly-vault/actions/runs/39090931667): success.
- Ichthyornis SHA-256: `016fa98ae3c7b430a5756ffd0a683fb51f48d0a9e168b9f9c295222c6db98be9`.
- Confuciusornis SHA-256: `264383f0cca9b772479d93037f83c4084a6feabefd26d0285278e6a539f16bdb`.

## Verified outcome

Three.js 0.180.0 GLTFLoader parsed the exact inputs. Chromium 141.0.7390.37 / ANGLE Vulkan SwiftShader / WebGL 2.0 rendered intact head, torso and wing surfaces. Before/after-orbit screenshots show coherent silhouettes; the twelve-prop image is also intact. This is an actual raster inspection, in addition to the automated checks.

Fourteen loads and fourteen 45-degree orbit actions completed, including six two-asset switching cycles. Both screenshot pairs changed. One canvas remained throughout. There were zero page, console or GL errors. Fifteen clear/dispose observations returned geometry and texture counters to zero. Twelve duplicated props rendered 27,240 triangles in 48 draw calls.

The independent exact-coordinate orientation audit now reports zero inconsistent shared edges for both GLBs, with zero open boundary or >2-face edges. Materials remain single-sided; no double-sided rendering workaround masks the defect. Counts and bounds remain consistent with the reviewed shapes.

## Optional polish and limits

Ichthyornis's far wing can align behind its head from the initial hero angle. Fine feathers and streamers may alias at small screen sizes. These are optional presentation/LOD points, not blockers for these static props.

Software-WebGL results are functional evidence only, not hardware/mobile performance. Disposal observations are bounded renderer counters, not long-duration memory-leak proof. Mixed sizes are normalized for display, not biological scale. Rigging, animation, collision, scientific certification, main publication and deployment are outside this review.

## Preserved evidence

Original artifact ID 12122797217, ZIP SHA-256 `d54f3621c8ce636ad8361a70f1fa3ab1e73408c7e984e1f8e6a3792f782568e5`; downloaded and hash-verified. Original archive expires 2026-11-17. Extracted raw JSON and all five unchanged PNGs are stored here with the independent review and orientation audit.

The original r1 failure, screenshots and diagnosis remain unchanged in [actions-evidence](../actions-evidence/README.md). This PASS applies only to the exact r2 hashes above.

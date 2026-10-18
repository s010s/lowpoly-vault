# Four small-life props: actual Chromium runtime result

PASS for this narrow functional scope on 2026-10-18. No asset changes or deployment.

- Tested harness commit: `4f4b524e3efbeaf9082b7ebb1696b891fb46555f`.
- GitHub Actions run: https://github.com/s010s/lowpoly-vault/actions/runs/39085495885 (success).
- Inputs: insect/plant from `bdc4e791c0628f92a29a105927c3880b41dba5a3`; aquatic from `d0735b414baae2edd4a35d0f911bc3afdbe9c624`. Four exact GLB SHA-256 hashes in `expected.json` and `results/browser-report.json`; checked before testing.
- Three.js 0.180.0 Node GLTFLoader parsed all four and reproduced geometry counts/bounds.
- Actual Chromium 141.0.7390.37, WebGL 2.0 through ANGLE Vulkan SwiftShader. This is real browser/software-WebGL functional evidence, not physical-device or hardware-GPU performance evidence.
- All four rendered nonempty images. Four before/after-orbit screenshot pairs differ and were inspected independently; no new visual blocker. Original artistic/basic-form advisories still apply.
- Sixteen successful asset loads and sixteen 45-degree orbit actions, including three four-asset switching cycles. One canvas throughout. Zero reported page, console or GL errors.
- Seventeen clear/dispose observations returned renderer geometry and texture counters to zero. This is a bounded renderer-resource check, not a long-duration heap/leak proof.
- Twelve mixed duplicated props (three of each) rendered with 30,180 triangles and 75 draw calls, zero GL error. Display sizes were normalized for inspection; this is neither a biological-scale ecosystem nor an integrated museum scene/performance benchmark.

Screenshots and raw machine reports are preserved here rather than relying on an expiring Actions download. Original archive artifact ID 12120751685, SHA-256 `364f80833da45d27855c30198ad08d11a69884c4ee64f8473eec61eb8a9843e7`, expires 2026-11-17. Archive downloaded and inspected.

This resolves the earlier cloud-local browser blocker through the established same-host Actions workflow. The historical `runtime-addendum.md` records the earlier failed local attempts; its browser-untested status is superseded only for the narrow functional scope above. No full release approval, hardware/mobile performance, animation readiness, scientific reconstruction certification or main merge is implied.

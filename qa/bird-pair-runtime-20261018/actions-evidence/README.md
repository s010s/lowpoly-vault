# Bird pair: actual Chromium runtime review

**FAIL runtime visual acceptance for both exact bird GLBs.** The automated functional checks passed, but inspection of the actual browser screenshots found major missing body/wing surfaces. No models or original previews were edited.

## Evidence

- Asset checkpoint: `00c88aaca6a8a97b1a8843000958125749a95104`.
- Tested QA commit: `5a134c03464fa7b000077e9b3baeb7388f21d3f8`.
- [GitHub Actions run 39090283618](https://github.com/s010s/lowpoly-vault/actions/runs/39090283618): workflow success is **mechanical test success**, not visual acceptance.
- Exact GLB SHA-256 values were checked before Node/browser tests and are recorded in `expected.json` and `review.json`.
- Original artifact ID 12122940405, ZIP SHA-256 `1a4d34df85313df5733b6e35db0dfda68dd45bcbcab9f4c87de086bca369a7d3`; downloaded and verified. Its archive expires 2026-11-17. The extracted evidence is preserved here.

## Passed mechanical checks

Three.js 0.180.0 GLTFLoader parsed both GLBs. Chromium 141.0.7390.37 rendered via ANGLE Vulkan SwiftShader / WebGL 2.0. Fourteen successful loads and fourteen orbit actions completed, including six two-asset switching cycles. Both before/after-orbit screenshot pairs changed. One canvas remained throughout. Zero page, console or GL errors. Fifteen clear/dispose observations returned geometry and texture counters to zero. Twelve duplicated props rendered 27,240 triangles in 48 draw calls.

## Blocking visual defect and read-only diagnosis

All five screenshots were inspected. Both birds lose substantial torso, head and wing surfaces in normal single-sided browser rendering. This creates conspicuous open striped silhouettes and is a blocker for practical scene use.

The exact-coordinate geometric-edge audit finds zero boundary edges, but 755 shared edges in Ichthyornis and 891 in Confuciusornis have the same traversal direction in both adjacent triangles. Correctly oriented closed surfaces require opposite traversal. All four materials in each GLB are single-sided. Thus the earlier boundary warnings really were material seams, but edge closure alone did not establish consistent triangle orientation. See `orientation-audit.json`.

Likely source: `scripts/build_bird_pair.py` function `preserve_and_batch` duplicates each polygon's vertices and passes the disconnected faces into `asset_common.mesh_object`, whose default normal recalculation runs before the later weld. The weld does not restore consistent face orientation. A bounded follow-up should preserve the already-oriented source face winding during batching (for example, disable that intermediate recalculation), re-export the same geometry/palette and rerun these exact runtime checks. No such model fix was performed in this review.

## Limits

The earlier six-view Blender visual PASS covered those preview pixels. This runtime visual FAIL prevents treating it as end-to-end readiness. Software-WebGL results are functional evidence only, not hardware/mobile performance. Disposal observations are bounded renderer counters, not a long-duration heap/leak proof. Duplicates use normalized display sizes, not biological scale. No main merge, deployment, release approval or scientific reconstruction claim is implied.

# Batches 37–39 publication closeout

This release adds exactly twelve independently reviewed models to the unchanged 163-model production catalog. It stops at 175 models; no next batch is claimed.

- Profile: `static-stylized-v1`, rule `2026-10-18.1`; separate owner-authorized QA-passed website publication policy.
- Source/QA bindings are retained in `production/continuous-release-round13-20261018/source-bundle.json` and `site/accepted-round13-release.mjs`.
- Batch 39 uses only aa-lava-front **r002**, candidate `1a65d88bd1fe81d0df3211b61235a150d71caa8d`, GLB SHA-256 `7960936e5ee17c46db8cd3d5658705ef04643a665ebfe5305e16a2bdefeb243c`. The final differential QA closes B39-AA-01 while preserving the other three original decisions.
- Independent model QA is reused. Publication integrity/profile checks and browser delivery regressions do not grant candidate approval, strict scientific reconstruction claims, or hardware GPU acceptance.
- All new candidate approvals remain false. Formal profile acceptance remains `BLOCKED`, hardware GPU verification remains false, and ANGLE SwiftShader evidence supports functional software WebGL only. Earlier batch 27 and 36 hardware limits are preserved.
- `preservation.json` records unchanged old model metadata and all 652 old GLB/Blend/preview/poster files.
- Canonical posters use pinned Playwright Chromium 141. The existing capture workflow is capture-only; normal publication, exact poster reproduction, CI, Pages, and actual public-origin checks remain required.
- No frontend behavior/UI files, repository permissions, protected-branch settings, or remote history are changed. Git operations use ordinary pushes and merge, attributed to Leon Made This.

Local validation: round13 publication rejection suite 57 checks; 438 source handoff pin occurrences; 1752 frozen source/QA files. CI records complete publication regressions and necessary browser checks. Final live reports and workflow timing evidence are available as GitHub Actions artifacts on the exact merged main SHA.

Capture transport note: the initial capture attempt correctly refused a missing frozen log excluded by `.gitignore`. The following ordinary commit retains all 192 referenced ignored evidence files. No refusal assertion was removed or weakened.

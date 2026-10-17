# Arch / fern release integration checkpoint

Based on published website commit `bf1c06703a502a86ff3fb97ef60ce22d2f3a4745`, with public strict gate `9503327115a80dd74ac7af5c0033812b45b2bcad` merged normally. Website viewer, motion, scrub and CI source remain unchanged from that website commit.

Only natural-arch structural-r002 and fern-cluster r006 replace catalogue entries. The other eight entries and all original model files remain unchanged. Exact accepted source, GLB and approved preview are copied into immutable `assets/revisions/<id>/<revision>/` paths. Frozen generators/configs (and fern packer) are beside them. The 24 revision WebP frames retain their accepted bytes and alpha; manifests alone use revision namespaces. Preview equals frame 0. Frozen acceptance closures under `experiments/structural-refinement-2026-10-17/accepted/` are source-side gate inputs, never delivered in Pages.

`integration-audit.json` records checks and descriptor. Both strict candidate gates, mixed gate, build/delivery audit, pinned Three.js parsing, publication/manifest/scrub/redesign regressions pass. The mixed CLI circular-load deadlock found during integration is fixed; a subprocess regression exercises the actual entrypoint.

## New reproducibility runs

`runs/macos-blender52-20261017/` contains two NEW executions per asset, stdout/stderr, request/result and summary. These are not historical log replacements. Both runs per asset are byte-identical. Relative to accepted Blender 4.3.2 exports, BIN chunks are byte-identical and semantic hashes match; only `/asset/generator` changes from Khronos Blender I/O v4.3.47 to v5.2.39. See `blender-version-differences.json`. Published files retain accepted bytes.

Blender 5.2 Boolean evaluation adds an unused empty material slot to the arch. `scripts/rebuild_frozen_blender.py` removes only unreferenced empty slots before the existing audit; referenced empty slots fail. Frozen source is not edited. Reproduce with installed Blender: `python3 scripts/rebuild_refinements.py --run-id <fresh-name>`. Diagnostic outputs stay ignored and separate.

`historical-closure-coverage.json` records four missing historical logs: stdout plus empty stderr per rebuild. No historical file was fabricated. All present closure bytes match original SHA-256; strict gates pass despite the additional history-log omission.

## Remaining visual blocker

The integrated local website requires a fresh actual-browser render check. Codex in-app browser is unavailable, browser inventory is empty, and Safari is blocked by a locked Mac. No headless browser or user Chrome was launched. Preview: `http://127.0.0.1:4176/lowpoly-vault/` while the preview process runs. Static checks and archived software-renderer pixels do not establish a new integrated-site visual pass.

This is a branch checkpoint, not a main update or deployment. Obtain independent review after actual browser regression. Conifer stays the original WIP entry; r12 tube-like foliage remains rejected. Separate clean maker worktree: `products/lowpoly-vault-worktrees/conifer-refinement`, branch `conifer-refinement`, HEAD `0eab01f04c26b174acfa4c8a96c9a7443bd0e469`. Entry: `experiments/structural-refinement-2026-10-17/conifer-tree/candidate-r12/`. Create a new immutable candidate with flat, shallow-thickness, gradually tapered foliage sprays, preserving branch joins/crown gaps, then use a separate exact-file QA task.

No new software installed. Existing dependencies are reused locally from the same project's modal-fix worktree; that local symlink is ignored. Tests use `TMPDIR=/private/tmp` so macOS `/var` versus `/private/var` aliases are not mistaken for prohibited file symlinks.

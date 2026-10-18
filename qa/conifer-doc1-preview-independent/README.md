# Independent conifer A publication-preview review

Reviewed fixed branch `integrate/conifer-doc1-20261017`, commit `35de59d2ad4dbce7e88eae9d8df237c480098c02`. Fresh independent publication review, performed on the owner's explicitly authorized Mac task. Author: Leon Made This <8357465+s010s@users.noreply.github.com>.

**Publication-preview verdict: PASS for these exact bytes. Strict candidate and proposed mixed-release gates: PASS. Production build/inventory and scoped integration tests: PASS. Full npm test: FAIL on this Mac because the unchanged cloud queue requires Linux process groups, /proc and flock.** No all-tests-green claim, main activation, push or publication.

## Actual pixel inspection

Opened all 24 individual 768×768 decoded selected images, not just a montage. Frame 0 was additionally composited on both light and dark; the remaining frames were viewed individually with alternating light/dark composition. Opened the selected poster separately. Correct alpha composition retains fine separated feathery needles and the intentionally airy A crown; RGB blocks in fully transparent pixels are not visible backing. All tips, side sprays and roots remain inside the image. Minimum alpha-bounds margins across all frames: left196/top141/right196/bottom155 px. Height varies456–467 px as perspective rotates; this is consistent with the fixed camera, not framewise zoom.

Sequence: azimuth42+15*i, elevation23.3; all24 hashes equal source commit `b3107dc7a5e04c2fd1cb0031ebb1bdb4f8cdfc17`. Poster, frame0 and revision preview share SHA256 `6296286130490b04dba1f1b4b1a7c00149cfecbc43bfeab82dd0c7b18eb0cfd4`. Selected manifest SHA256 `fac3664fec9f0177debf18b57b91d6175838cd749ae4008b6d394aa689e34bde`. Exact frame hashes, decoded bounds, alpha and inspected observations are in `artifact-audit.json` and the new candidate evidence.

Independently inspected the retained actual desktop/mobile GLB captures and initial ready frame0 screenshot in `../conifer-doc1-integration/browser-evidence/`. Site and validator code is unchanged from the recorded browser execution checkpoint9c19765 through the fixed review commit. Existing five frame7 handoff cases have normalized320px RGB mean absolute error0.00287–0.00396, bbox delta1–2px and centroid delta<0.2px; preview-flight RGBA hashes match. Camera preset, rotation order and frame0 agree with ModelStage v2. Visual structure, woody tan and foliage greens match real GLB captures. Retained reverse/reopen/context-recovery/interrupted navigation assertions passed. Original failed first harness attempt is preserved. These are independently inspected existing browser execution artifacts, **not a new browser run**. No browser was launched or controlled.

## Acceptance and immutable records

GLB:715500 bytes;19052 triangles;3 materials;0 textures; SHA256 `c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40`. Source Blend SHA256 `04c20d19354455e57bbc70a8cced6308d9020e02ff057996bfde7c585a7acbef`. No model/source/brief/reference/render bytes changed.

New schema-compliant record:
`experiments/structural-refinement-2026-10-17/accepted/conifer-tree/qa/doc1-publication-preview-independent/candidate.reviewed.json`.
Its visual report explicitly attributes and inherits the prior complete model visual review; this task adds the exact24 selected image hashes and poster, with new independent identity, report and approval seal. Other six model-stage decisions remain unchanged. The original final independent candidate/report are untouched. Strict validation includes `--previous qa/r20-doc1-final-independent/candidate.independent.json --require-approved`.

New proposal descriptor:
`assets/releases/conifer-doc1-preview-reviewed-20261017.json`, pinned by `reviewed-release-pin.json`. The old proposal, active source manifest and active turntable index remain unchanged. Only the isolated build copy selects the new descriptor/index.

## Integration verification

`integration-check.json` contains exact command results and45 independent byte comparisons for all other9 assets. The isolated copy is `qa/review-site/conifer-doc1-independent-attempt02/`, based on a Git archive of35de59d2 plus only the new approval/descriptor. Its unchanged production workflow passed strict release collection, production build,361-file deployment allowlist,10 GLB/Blend pairs,240 frames,10 posters,26 bilingual documents and exact ZIP contents. Private evidence is excluded by the deployment inventory. Comparison baseline was freshly delivered from the unchanged current source manifest. No publication occurred.

Final isolated conifer ZIP SHA256 `55f96771afe827fff62971f396d4caead2274be76384ca8ff6762daf532c4d56`; CRC and all3 entries pass. This is the production-format package checked locally, distinct from the maker's earlier review-only ZIP. The bilingual credits and both static language details retain required compatibility/performance wording.

Passed: publication tests46+78 checks, image scrub/delivery/mixed-source tests, redesign/static route/scale/motion tests, manifest/catalog/theme tests,14 GLB checker tests and75 candidate gate tests. Full `npm test` then fails at14 Linux-only queue tests (16 assertion failures); downstream pipeline-pilot/technical-report suite commands are consequently not reached. No gate or source test was modified. `repository-tests.txt` retains failure details. Run the remaining full pipeline in its supported Linux environment before claiming complete repository CI green.

The first publication-test attempt also encountered macOS `/var` versus `/private/var` temporary-path normalization. Its log is `publication-tests-attempt01.txt`; retry used canonical `TMPDIR=/private/tmp`, preserving all assertions, and passed. Integration script supports `--resume` to finish byte/ZIP verification after that full-suite platform failure; it does not change or waive the failed result.

## Compatibility and remaining limits

**KHR_mesh_quantization is required** for normalized SHORT normals; pinned tested loader is Three.js0.180.0. Existing performance acceptance is limited to recorded Apple M5 Pro/ANGLE Metal, Chromium141, DPR1,1200×900,no-shadow measured profile. SwiftShader misses16.7ms including the single-tree tests. Other hardware/loaders remain unverified. Fine-needle subpixel aliasing remains disclosed; no zero-shimmer guarantee. The user's light/open A style is respected rather than treated as missing foliage.

No publication-preview defect remains. Remaining verification blocker: full Linux queue/pipeline CI cannot pass on this Mac. Main activation/publication is separate. No background process was started; owned foreground checks exited. No other task's process or branch was touched.

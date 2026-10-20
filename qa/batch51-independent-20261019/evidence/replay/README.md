# Batch 51 evidence replay

Run from the repository root. All commands read the pinned candidate assets; generated reports and temporary renders should go under `/tmp`.

## Check exact inputs and frozen asset bundles

```sh
python3 qa/batch51-independent-20261019/evidence/verify_inputs.py
```

This checks the pinned source and handoff commits, all handoff role hashes, each `bundle-files.sha256`, the four selected GLBs, all eight candidate-proof frames, concept/prompt/inspection hashes and order receipts, runtime screenshots, and Conichnus diagnostic image/ray artifacts. It also confirms that the model and production trees have not changed since the handoff commit.

## Candidate and concept evidence gates

The exact checker outputs and exit codes are preserved under `candidate-checks/exit-codes.json`. To rerun the candidate integrity and formal-approval checks, use each selected bundle's `candidate.json` and `profile-contract.json`:

```sh
python3 scripts/validate_candidate.py assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate.json --root . --profile static-stylized-v1 --profile-contract assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/profile-contract.json --json
python3 scripts/validate_candidate.py assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate.json --root . --profile static-stylized-v1 --profile-contract assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/profile-contract.json --require-approved --json
python3 scripts/validate_concept_evidence.py concept-evidence.json --root assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001 --require-complete
```

Use `calcite-raft-deposit/r002`, `accretionary-lapilli-bed/r002`, and `conichnus-conical-burrow/r001` for the other three items. Expected outcomes on the pinned records are candidate integrity exit 0, `--require-approved` exit 1, and `--require-complete` exit 1 with the single unknown exact-generation-time blocker.

## Blender source/export comparison

The independent reports in `blender-source-export/` were generated with Blender 4.3.2 and `scripts/check_source_export.py`. For each item, select its `.blend` and `.glb` and write a new report path, for example:

```sh
blender -b --factory-startup --disable-autoexec --python-exit-code 1 \
  --python scripts/check_source_export.py -- \
  --source assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/conichnus-conical-burrow.blend \
  --glb assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/conichnus-conical-burrow.glb \
  --collection EXPORT --output /tmp/conichnus-independent-source-export.json
```

The script reopens the saved Blend with auto-execution disabled and does not save or export over either source. It compares evaluated triangle counts and axis-converted bounds; it does not claim material equivalence or scientific fidelity.

## Conichnus negative-cavity check

```sh
blender -b --factory-startup --disable-autoexec --python-exit-code 1 \
  --python qa/batch51-independent-20261019/evidence/replay/probe_negative_cavity.py -- \
  assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/conichnus-conical-burrow.glb
```

The script accepts only the pinned GLB hash, imports it into a disposable scene, and prints six downward-ray results. It does not save or edit any model.

## Official Khronos validation

The raw Khronos reports in `khronos/<asset>/` came from repository script `scripts/validate_gltf.cjs` and `gltf-validator 2.0.0-dev.3.10`. That script writes next to its input, so replay against a temporary GLB copy rather than a candidate source path. Preserve the original candidate hash and compare it with `QA-HANDOFF.json` before reporting a result.

## Runtime replay

`runtime/runtime-replay-summary.json` records an independent run of the exact batch `runtime.mjs` using Chromium 154.0.8037.57, Three.js 0.180, Playwright 1.56.1, and ANGLE SwiftShader. It confirms the exact imported GLB hash, parser metrics, zero browser/WebGL errors, nine clone instances, and pixel-identical hashes for all 7 screenshots per item. This proves the declared software rendering path only. It does not test a physical GPU or the parent/museum scene.

`verify_inputs.py`, candidate checker outputs, Blender reports, the Khronos results, runtime results, and the independent Conichnus ray output are all committed alongside the decision report. The visual pixels themselves remain in the pinned handoff source commit; every frame hash is stored in the evidence index.

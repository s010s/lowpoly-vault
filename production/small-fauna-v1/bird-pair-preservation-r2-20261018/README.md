# Bird pair r2 preservation checkpoint

The repaired r2 GLBs, editable Blender sources and generator were already durable at `d5cc3d2f3ff34d032dbd740470e3c454e2909405`. This checkpoint preserves the twelve existing regenerated 512px views, their source-bound manifests, producer records and approved independent-review reference records. No Blender modeling or geometry/material edits were performed during preservation.

## Current evidence

- `paired-source-preview-manifest.json` is the current exact r2 model, preview and metadata hash index. Every local frame, config, brief and execution-record source hash was checked.
- Both `assets/prehistoric/birds/<asset>/independent-review.json` files are the reviewer's approved exact-r2 PASS references.
- Full independent six-view and actual five-image browser review: [QA evidence](https://github.com/s010s/lowpoly-vault/tree/cd443a934b0e6440f05276f0faa4183813a545f8/qa/bird-pair-runtime-20261018/actions-evidence-r2).
- [Functional run 39090931667](https://github.com/s010s/lowpoly-vault/actions/runs/39090931667) tested these exact r2 GLB hashes. Software-WebGL evidence is not hardware/mobile performance certification.

## Historical versus later records

Producer `qa.json`, execution records, render manifests and metadata retain their generation-time pending/not-run fields. The independent review happened later; read `independent-review.json` and `preservation-status.json` for its exact scope. The original r1 reports are archived as `independent-review-r1.json`; they do not approve r2. The older `bird-pair-preservation-20261018` directory remains a historical snapshot. The QA branch retains the original r1 runtime failure and the successful r2 evidence.

Two static unrigged candidate props, six meaningful views each, zero turntable frames. No main merge, gallery/museum update, animation acceptance or scientific certification is implied.

# Existing pipeline audit

Audited the published initial-pack tree based on `eeab789f7ee6791cf6bb36fe9218167faeec460c`, including the inherited redesign work. The new contract builds on existing work rather than claiming a pipeline or review never existed.

- Existing Skills already describe authoring, source audits, GLB export, Khronos validation, clean reimport, multi-angle images, rebuild checks and target-runtime checks.
- `qa/art-direction-review.md` records actual independent image inspection, including a rejected/repaired fern and concerns that the conifer crown read like broad leaves. Independent art review existed; it was not consistently enforced as a frozen per-candidate acceptance obligation.
- All ten stored asset `qa.json` records retain `threejs_runtime.status = not_run`. Separately, `qa/redesign-v2-evidence/strict-gpu-report.json` contains GPU-pass entries whose ten GLB SHA-256 values match the current original files. Those two facts should be reconciled by scope and provenance, not collapsed into either “never tested” or “fully approved.” The saved visual-approval status remains pending human inspection.
- Previous formal manifest generation relied heavily on status strings and optional artifact hashes. It did not require every new report/image/brief/reference and independent criterion to be current and bound together.
- `prehistoric-environment-art` explicitly excludes animal anatomy. A dinosaur requires a separate taxon-specific factual review rather than inheriting environment-art acceptance.

The implementation adds explicit candidate records, scoped independent review, image/report/approval bindings, fail-closed formal release checks and a bounded headless worker contract. It keeps the exact initial-ten WIP publication exception separate. Evidence integrity cannot prove the honesty of a reviewer or guarantee scientific truth.

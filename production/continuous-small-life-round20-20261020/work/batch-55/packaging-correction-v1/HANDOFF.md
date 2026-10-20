# Batch 55 additive packaging correction v1

Local review artifact only. No commit, push, PR, merge, publication, or deployment
was performed for this correction.

## Result and exact boundary

The existing validator does **not** allow an explicitly empty
`required_deliverables` list to be overridden by a profile sidecar. Its supported
immutable-revision/supersedes mechanism does allow a later, separately versioned
brief. This correction uses that mechanism, not a new validation exception.

Four new packaging-only candidates are under
`assets/candidates/continuous-small-life-round20-20261020/batch-55/`:

- `vermicularia/r001-packaging-v1/candidate.json`
- `weichselia/r001-packaging-v1/candidate.json`
- `ventifact/r001-packaging-v1/candidate.json`
- `pentichnus-deep-dwelling-trace/r002-packaging-v1/candidate.json`

Each new candidate has a new brief hash, a hash-bound `supersedes` link to its
original candidate, and unchanged GLB/source/generator/config/reference pins. Its
new brief changes only `brief_version`, the current packaging `frozen_at`, and
`required_deliverables` (explicit source/generator/config roles, paths, hashes).
It does not duplicate, regenerate, or edit any model, source, config, image,
reference, historical evidence, or original frozen brief.

`packaging-contract.json` beside each new candidate explicitly records this as a
post-modeling declaration. The declaration time is `2026-10-20T02:26:04+00:00`, not
a pre-generation freeze. Original concept-first evidence still binds its original
brief and revision; it is neither rewritten nor assigned to the new subject.

All four new candidates pass the **unchanged** `static-stylized-v1` structural
candidate gate: `valid=true`, `approved_for_brief=false`. All seven stages remain
byte-for-byte equivalent unknown entries; approval remains pending. Existing
blockers remain unchanged, and two explicit open blockers are added for the
historical missing logs and the new packaging subject's pending review.
No old model/QA verdict is promoted or rebound to the new brief hash.

## Preservation

- Baseline: `89f6086b5d6411b70a7d42c8f5d7aff69b68f7d5`.
- Model source remains `1e43f9e2c79b6d2465d8eadf2169355cba3690c7`.
- `preserved-files.json` covers every baseline round20 file plus the validators,
  schemas, pinned publication policy, and profile-contract documentation: 520
  original files, including 20 GLBs, 20 Blends, and 79 PNGs.
- The audit compares current SHA-256 and Git blob identity against that exact
  baseline commit. All 520 are unchanged. Existing HANDOFF and identity-validation
  reports are deliberately untouched.
- Original candidate records still fail the empty-deliverables requirement.
  Both original and corrected records retain the legacy zero-turntable rejection.
- Official candidate/profile validators, thresholds, approval rules, and policy
  bytes are unchanged. The batch-local audit is not a release validator and
  grants no publication authority.

## Historical gaps remain open

The original four hash manifests list 20 absent log files, five per asset:
`khronos.log`, `reproducibility-1.log`, `reproducibility-2.log`,
`source-export.log`, and `source-metrics.log`, all in `evidence/`.
All 205 present entries still match their original hashes. Each packaging
contract lists the missing paths and original expected hashes. No placeholder,
copy of a corresponding JSON report, or newly generated run is passed off as a
historical log. The original manifest and missing paths remain unchanged.

Original concept evidence remains integrity-valid but incomplete: provider
generation time and modeling-authoring start time are unknown. Current-time
validation does not fill them. No new model generation, rebuild, rendering,
visual/factual acceptance, browser GPU, or populated-scene run occurred here.
The corrected candidates are structurally valid **pending records**, not complete
packages, approvals, or release-ready assets.

## Verification and reproduction

`validation-current.json` is a newly timestamped read-only verification result.
It records original failures, new candidate diagnostics, current GLB measurement,
concept integrity rechecks, unchanged original bytes, and missing-log inventories.
It is separate from all historical evidence.

From the repository root, substitute the actual current UTC time:

```sh
python3 production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/verify.py --checked-at <current-ISO-UTC-time>
python3 production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/test_verify.py -v
```

The audit runs the unchanged official validator with `--previous` semantics and
the exact official profile sidecar. `--require-approved` remains nonzero. The
18 new tests cover original Git-byte preservation, additive derivation, hash
tampering, forbidden budget/stage/blocker changes, empty deliverables, no
backdating, no manufactured historical logs, no sidecar fallback, legacy
zero-turntable rejection, pending approval, and creator no-clobber behavior.

`regression-results.json` retains the initial nine-suite run: 191 tests passed,
and the one natural-arch integration test could not find its fixture in this
sparse checkout. `pipeline-pilot-baseline-retry.json` records a successful retry
with unchanged scripts and fixture bytes materialized from the baseline commit
into a temporary directory on the same native computer. No sparse-checkout
settings or original tracked files were changed. In total, all 192 distinct
tests passed across those runs; the initial environmental failure is preserved,
not replaced with a green result. These are integrity/regression tests, not new
model QA or visual acceptance.

Parent review is still required before any repository publication. A later
acceptance flow must explicitly review the changed brief subject and honestly
resolve or disclose the historical packaging gaps; it must not copy old review
subjects, fabricate old logs, or silently treat these pending records as approved.

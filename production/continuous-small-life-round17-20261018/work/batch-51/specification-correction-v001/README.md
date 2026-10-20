# Batch 51 supplemental specification correction v001

This is a metadata-only correction for the existing exact Calcite r002 and lapilli r002 geometry. It does not claim independent acceptance or formal candidate approval.

- Calcite nominal concept/design span: 0.32 m. Exact exported GLB XYZ bounds: 0.33593830466270447 × 0.02606956660747528 × 0.25428861379623413 m.
- Lapilli nominal concept/design width: 0.28 m. Exact exported GLB XYZ bounds: 0.28449925780296326 × 0.11559999734163284 × 0.20509090274572372 m.

The original ImageGen prompts and frozen construction plans agree on those nominal values. Inherited descriptive scale fields (0.42 and 0.60 m) are retained as historical contradictions, explicitly superseded only for supplemental specification review. Original candidate/configuration/freeze/report/image/model bytes are unchanged. No fresh geometry or render was required. Nominal design scale is not an exact bounding box, specimen measurement, or a newly invented acceptance tolerance.

Each new brief changes only its version label and descriptive scale, and adds an explicit correction note. Every original criterion, required stage, source, deliverable, view and budget remains unchanged. New metadata records distinguish nominal design scale from actual measured bounds. The new derived freezes are explicitly post-model records, not backdated modeling inputs.

## Candidate and review boundary

`index.json` binds the original handoff and independent review commits. This directory's supplemental briefs are not silently registered as the original r002 candidate briefs. That would alter an immutable artifact and invalidate historical subject hashes. The registered candidate records and their evidence remain untouched; no old PASS is attributed to a new brief.

The existing independent reviewer should check only these corrected descriptive values, the new exact brief/metadata hashes, and preservation of the original model/evidence. A formal candidate transition, if needed, remains separate and must honor immutable-revision and evidence-subject rules. No alternative release policy or waived obligation is introduced here.

## Verified

Run from the repository root:

    python3 production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/verify_correction.py

The read-only checker verifies 772 protected original files, all handoff pins and bundle checksums, fresh exact-GLB bounds, unchanged criteria and valid supplemental brief structure. It also repeats all four original candidate and concept gates:

- Candidate integrity: exit 0, valid, unapproved.
- Candidate `--require-approved`: exit 1, unchanged pending/unknown stages and blockers.
- Concept integrity: exit 0, valid but incomplete.
- Concept `--require-complete`: exit 1, solely because the exact provider generation timestamp remains unknown.

`verification.json` preserves those fresh results. `baseline-original-verification.json` is the exact original independent verification run BEFORE the handoff pointers were updated, not a claim that the complete production tree is now unchanged. The original handoff bytes are in `historical-handoff/`. `regression-tests.log` records 75 candidate, 20 static-profile, and 20 concept-evidence regression tests passing without validator modifications.

No exact ImageGen time was synthesized, no model/source/image was changed, no formal stage was promoted, and no publication was performed. Independent difference acceptance remains pending.

# Intake format checks retained

The initial read-only intake script rejected two assumptions about report formatting before the repository import began. These were intake-format issues, not failed model verdicts:

- A literal `tafoni-outcrop`/PASS-line check rejected the unchanged batch14 report, which labels that exact hashed asset `Tafoni outcrop`. The final new gate accepts the visible hyphen/space spelling while still requiring the exact independent report, source commit and both payload hashes.
- A literal per-asset source-commit-in-report check rejected batch15. Its report actually pins the full handoff commit and JSONL SHA, with both exact payload hashes; the per-asset commit and Blend pin are in the JSONL's `commit` and nested `artifacts.blend.sha256`, not a top-level `blend_sha256`. Final validation explicitly checks report→exact handoff SHA→matching asset row→source commit and GLB/Blend hashes. The handoff-tamper regression must reject modified bytes.

No source report was edited to insert missing strings, no failed model was reclassified and no pre-existing production assertion was removed. Original legacy checker failures, approval blockers, QA observations and source warnings remain in the frozen imported records. The bootstrap copy-assets attempt before poster capture also correctly rejects 67 posters for a 79-model manifest; its actual log is retained. The completed build must then satisfy every poster and deployment assertion.

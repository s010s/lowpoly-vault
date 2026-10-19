# Land/air delivery-record repair

This isolated supplement starts at source commit `68483aa3b8eed2d86f9e59a930128d99579b0838` and follows the record-only completion pattern from marine commit `1c1b5fd0f466feb95457a8c96ed58ed8f219201f`. It retains Sapeornis, Longirostravis, Dunbaria and Chimerarachne r001. Sapeornis r002 is preserved and is not adopted.

Only the four delivery metadata files, handoff prose/index and current bundle hash manifest may change. The original versions are saved under `original-records/`; all original file hashes are pinned in `baseline-files.json`. No geometry, editable source, original generator, design/config/reference, original technical evidence or image changes are permitted. No catalog, release, site or marine files are edited.

- `inspect_delivered_sources.py`: fresh read-only Blender source audit; autoexec disabled; never saves or exports.
- `validate_exact_glbs.cjs`: fresh official Khronos checks written here, preserving original QA files.
- `complete_delivery_records.py`: measured metadata, real existing diagnostic preview paths, correct generator path and current-time unapproved candidate registration. Original briefs/references are immutable and separately pinned; the added formal-contract supplements do not claim a pre-production freeze.
- `verify_delivery_completion.py`: verifies actual measurements, all original bytes outside the explicit record allowlist, referenced file hashes, unchanged limited independent QA copies, concept completeness and valid-but-unapproved candidate behavior. It explicitly checks that `--require-approved` fails.
- `exact-diff.json`: exact baseline and current hashes for changed records and added files, excluding its own bytes and the final snapshot manifest to avoid circular hashing. `freeze-manifest.json` hashes it and every other bundle file except itself.

Existing independent review at `3d024e53c36863d1887abd726998fa0f0d7b3831` is copied without changes. Its visual/technical and software WebGL 1/8/32 scenes are supporting evidence, not formal acceptance of these newly registered hashes, physical-device GPU certification or deployed-gallery approval. Official gallery posters remain a separate task. Every formal candidate stage remains unknown and approval pending.

Run from repository root:

    blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 --python production/concept-small-land-air-20261019/delivery-completion/inspect_delivered_sources.py
    node production/concept-small-land-air-20261019/delivery-completion/validate_exact_glbs.cjs
    python3 production/concept-small-land-air-20261019/delivery-completion/complete_delivery_records.py
    python3 production/concept-small-land-air-20261019/delivery-completion/finalize_delivery_snapshot.py

Measurement/registration reruns intentionally produce new timestamps and hashes. Regenerate the final exact-diff and bundle snapshot after any rerun; do not silently reuse stale evidence.

Original assets, images and prose: CC BY 4.0, Leon Made This / s010s. Executable code: MIT. Third-party references were consulted only.

Regression checks: initial full `npm test` encountered a pre-existing timing-sensitive queue-fixture assertion (observed overlap 1 versus expected 2). The unchanged focused fixture passed on retry; the entire unchanged `npm test` suite subsequently passed. Both original failure and retry output are retained. No test or runtime code was changed. This does not establish physical GPU or deployment acceptance.

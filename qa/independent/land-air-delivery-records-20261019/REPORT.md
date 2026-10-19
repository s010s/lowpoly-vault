# Independent land/air delivery-record repair audit

Outcome: PASS for delivery-record repair integrity only. No blockers found in repair `e874e99d20b3b98c73cddb8496bcd7e89be4e28c`. This does not grant formal candidate, hardware, production-scene, integration, release or publication approval.

## Exact inputs and isolation

- Frozen original source: `68483aa3b8eed2d86f9e59a930128d99579b0838`
- Audited repair: `e874e99d20b3b98c73cddb8496bcd7e89be4e28c`, with the frozen source as its immediate parent
- Prior independent QA: `3d024e53c36863d1887abd726998fa0f0d7b3831`
- Selected Sapeornis, Longirostravis, Dunbaria and Chimerarachne revisions: all r001
- Separate audit branch: `qa/independent-land-air-delivery-records-20261019`
- This audit adds evidence only under `qa/independent/land-air-delivery-records-20261019/`. No source bundle, existing QA, candidate, marine, catalog or release content is edited.

## Verified result

1. Exact Git-tree and byte comparison: the frozen bundle has 336 files. Exactly seven existing delivery records change: four metadata files, `HANDOFF.md`, `handoff.json`, and `freeze-manifest.json`. All other 329 original files are byte-identical; 61 new record/evidence files are added; no deletions or changes outside the bundle exist in the repair. Each original record is retained verbatim. All 397 current bundle files match the audited repair commit. Sapeornis r002, the generators, GLBs, Blender sources, original briefs/references/reports and every image remain immutable.
2. The current snapshot has 396 valid file/size/SHA-256 bindings, covering every bundle file except itself. Independent verification of the baseline and exact-diff records matches Git, including the disclosed self-reference exclusions. 263 further current descriptors resolve and hash-match across handoff, candidate, brief, references, metadata and selected diagnostic preview manifests. Historical paths in immutable original reports remain historical provenance rather than current delivery links.
3. Blender 4.3.2 loaded all four current sources with autoexec disabled. Direct evaluated world bounds, triangle counts, authored vertex/polygon counts and actual used material names/PBR values agree with the GLBs, metadata, original source-export reports and repair measurements. Read-only before/after hashes are unchanged. Source-to-GLB bound errors are at most 7.450580596923828e-09 m, exactly matching the original reports and comfortably below 1e-08 m. Authored palette inventories may include unused colors; actual GLB material counts are explicitly separate.
4. Fresh official Khronos glTF Validator 2.0.0-dev.3.10 results: zero errors and warnings for all four exact GLBs. Fresh static analysis agrees with the recorded geometry and sizes. Sapeornis retains its understood negative-floor warning because its origin is the flight-body center; the other three pass without that warning.
5. All four normal candidate validator invocations return `valid: true`, `approved_for_brief: false`, no schema errors, and the exact stored validation result. All four `--require-approved` invocations correctly exit 1. All seven stages and criteria remain unknown, reviewers/subjects/review times remain null, formal evidence arrays remain empty, and approval remains pending. No evidence was re-signed or promoted.
6. Original concept-evidence validation remains complete for all four. Preview targets exist and are bound through their original manifest to the exact current GLB and original brief/references. Sapeornis, Longirostravis and Dunbaria use `proof/hero.png`; Chimerarachne uses the already-frozen `proof-macro-attempt02/hero.png`. Its actual pixels were inspected to verify the chosen existing macro preview is readable; no new render was created. All previews are explicitly diagnostic, not official gallery posters. Sapeornis now correctly identifies `generator-r001.py`.
7. Both copied independent QA reports are byte-identical to their originals. All 129 prior QA files remain accessible in the exact prior commit and are cataloged by blob ID and SHA-256. The prior source tree equals the frozen original tree. The hash-bound prior visual images and software scenarios of 1/8/32 copies are verified as preserved evidence. The reported renderer is ANGLE SwiftShader; this is not hardware or deployed-scene acceptance. No full visual or browser rerun was needed for immutable model/image bytes.
8. A fresh complete `npm test` passed on the first independent run, exit 0; full output is retained. The repair's original timing-sensitive queue-fixture failure and focused/full retries remain preserved unchanged. No runtime or test code changed.

## Measured exact artifacts

| Asset | Triangles | Materials | Primitives | GLB bytes | Blender bytes | GLB dimensions X,Y,Z in meters |
|---|---:|---:|---:|---:|---:|---|
| sapeornis | 5744 | 6 | 78 | 340260 | 1127248 | 0.943240940571, 0.210977971554, 0.449886322021 |
| longirostravis | 2428 | 7 | 35 | 160264 | 828516 | 0.0913477018476, 0.136473651393, 0.318628832698 |
| dunbaria | 1582 | 7 | 31 | 113700 | 768512 | 0.0595000013709, 0.00824796166853, 0.0543434116989 |
| chimerarachne | 1418 | 5 | 26 | 98176 | 688336 | 0.00383354001679, 0.00123318996702, 0.00715652341023 |

## SHA-256 identities

### sapeornis r001

- GLB: `7b0aef80ee8327ebc06a8372fc63fce63c393a62451820b4bd183ff868b2755b`
- Blender source: `fe598c50f50823d38e50a15aa1ce903dd1264f17d05cda20194c7b3396d7a734`
- Candidate record: `38fb0b38d4b2ef9f22d68c670e305cf9aca7ebe44bf394b7b3cf8c2d46b2c009`
- Metadata: `50d58e2a7c7c2a6ff0c04525fe9827176134fd98e26fda22d69aed33bb55662d`

### longirostravis r001

- GLB: `10668416201cf7ec57e48285019fcd0738e6bb69665fd8fb519559aabaa6bd83`
- Blender source: `b9ccf3e817136a22c848afcb4a6f48b7791c31acb32ef86b0c7eb841d140ebe3`
- Candidate record: `660678f4d4a160dcfcd7d97dfac342666f1b5115b32c7a5e616643e85280148c`
- Metadata: `c7026d6f169f95f8273bb910096580b781b60eb732b453a1501e238ce0a18d89`

### dunbaria r001

- GLB: `2f584412b3318fa3969e6b008271df107f73fe9f00c8f304c04bfa47e134311e`
- Blender source: `27a429059cbacb2f93563cf7a132a09ebe04eb6b7961e8234c85528d85ea4730`
- Candidate record: `f319c784d3ac8398877696092791fcb41fb27020549c6cf251ee366a38646952`
- Metadata: `3058c26b470e87accf70f96bab5cd85835c1da64d887bb30dbc6c39981b027e4`

### chimerarachne r001

- GLB: `848328130f8874bc6c81b0636d8bfc78f76d04b46cfa0786fe7d978f28e3ad6c`
- Blender source: `02db9598d09e548f42e72cd443a87b8028dd6d76dd40a4676ef79b4070609259`
- Candidate record: `9f1425803ab60620628f2f079be5de5f872e9af276b70ea4fc047870eb3b955e`
- Metadata: `48925de79977c53889cf5ac04ed49e30bf07f44d3c3dfd5fbac8a7bfcd167528`

## Remaining gates and audit limits

- Formal technical, visual, factual, specification, runtime-parse, GPU and scene stages are unknown and approval remains pending. Prior limited QA remains supporting evidence for unchanged original artifacts, not formal acceptance of new candidate/brief hashes.
- The newly registered production profile requires detail coverage and 24 turntable frames. Original proof contains eleven fixed views and zero turntable frames; formal coverage has not been waived or passed.
- Physical target-device GPU/performance and deployed populated production-gallery acceptance remain unverified. Native-scale Chimerarachne still needs intentional parent-scene presentation.
- Official unified-gallery posters remain separate from the repaired diagnostic preview links.
- Sapeornis r001 stays selected with its outer-wing limitation and flight-body-center warning; r002 stays rejected.
- No scientific/factual recertification, source rebuild, full visual review, browser rerun, merge, publication or formal approval was performed here. Later integration remains parent-owned.

## Evidence and repeatability

- `tree-integrity.json`: exact baseline/current Git and SHA-256 comparisons
- `original-qa-integrity.json`: original QA object/hash catalog and retained visual/software bindings
- `current-path-hash-bindings.json`: every explicitly audited current descriptor
- `*-fresh-blender-source.json`, `*-fresh-glb-audit.json`, `*-fresh-khronos.json`: new measurements
- `*-candidate-validation.json`, `*-approval-guard.json`, `*-concept-integrity.json`: fresh fail-closed checks
- `npm-test.txt`: complete independent regression output
- `report.json`: machine-readable audit outcome and exact artifact identities
- `read_source.py`, `validate_glbs.cjs`, `audit_records.py`: independent audit scripts

Run from repository root in an isolated worktree at the audited repair, using a fresh adjacent audit-output directory. Blender and Khronos scripts refuse to overwrite evidence. The integrity script permits only byte-identical prior deterministic evidence and otherwise refuses overwrites. Commands used:

    blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 --python qa/independent/land-air-delivery-records-20261019/read_source.py
    node qa/independent/land-air-delivery-records-20261019/validate_glbs.cjs
    npm test
    python3 -B qa/independent/land-air-delivery-records-20261019/audit_records.py

Two audit-harness assumptions were corrected before the final pass, with each script and failure output retained in `audit-attempts/`: exact-zero bounds was too strict for the already-documented floating-point deltas, and the audit initially assumed every preview lived in `proof/` instead of following Chimerarachne's valid existing macro manifest. These were auditor assumptions, not candidate defects. Final checks use a tighter-than-original 1e-08 m bound tolerance, require the exact historical delta, and verify the actual chosen preview manifest. No candidate/source file changed during those corrections.

License: new audit code MIT; audit prose CC BY 4.0, Leon Made This / s010s.

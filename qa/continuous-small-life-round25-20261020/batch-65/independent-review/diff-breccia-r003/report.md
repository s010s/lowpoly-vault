# Independent differential QA: breccia-outcrop r003

Date: 2026-10-20 UTC  
Scope: targeted read-only assessment of the newly found coplanar-clast website-stage defect and its r003 geometry repair. This does not reopen the full batch review. The previous static review remains unchanged. No accepted model was rebuilt or rerendered, and no source, candidate approval state, site or CI file was changed.

## Result and boundary

**breccia-outcrop r003: ACCEPT BOUNDED for this source/model-level differential only.** An independent exact-GLB geometry detector confirms the r002 coplanar positive-area overlaps are removed in r003. The repaired model retains its host, materials, placements and design brief, and the eight exact r003 CPU proof views show no comparable opaque crosshatching. Angular embedded clasts remain legible.

**The new website ModelStage/gallery outcome is still PENDING.** These CPU views, a glTF parser and source geometry cannot establish the result in the website renderer. The parent website worker must recapture the exact r003 GLB there and record the platform-stage result before the defect can be considered closed or the candidate release-ready. GPU/scene stages were not run. This is not formal/user approval or publication authority.

## Original observation and count scopes

The retained actual website screenshot (`website-original-defect.png`) visibly shows fine opaque crosshatching on a clast face. The saved website diagnostic binds that finding to the original r002 GLB `bfe0389608e76cd908e46e1b3cbbab91cb4ce282dcc5aa070a098da85d1169af` and reports seven coplanar-overlap pairs in its narrower website-focused scope. The diagnosis is consistent with closely separated, overlapping coplanar clast faces, not an alpha/material transparency change.

My independently written raw-GLB parser and geometric checker applies full scene transforms, triangle bounding-box broadphase, plane-parallel/separation tests (`1e-5 m`) and exact projected convex-triangle clipping; a positive intersection area must exceed `1e-8 m²`. With this broad all-material exact-GLB scope, it finds **33** triangle-pair overlaps in r002 and **0** in r003; the original maximum intersection area is `0.048913152030289786 m²`. The 33 pairs comprise 21 same-material dark-clast pairs and 12 same-material ochre-clast pairs, with no cross-material pair. The r003 check is zero across all materials.

The seven pairs listed as examples in the website diagnostic are all present among the broad detector’s 33 original pairs and absent in its r003 results. The broad detector’s additional simple filter for mesh 6 / primitive 0 / `darkclast` finds 21 pairs, not 7. The retained website diagnostic does not fully specify its narrower selection filter, so I do not equate its seven-count with either broad count. Both findings are compatible, distinct-scope observations.

Independently reopening and component-hashing the r002/r003 Blender source finds 120 fragment components in each, with exactly six component geometry hashes changed and 114 unchanged. The six changes are localized to two aggregate surface-fragment mesh objects. The host matrix mesh hash is exactly equal; all five source material definitions and their parameters are exactly equal. This is consistent with the three documented actual component-pair conflicts touching six clasts, while my acceptance of defect removal rests on the independent 33-to-0 exact-GLB test, not on the maker report.

## No concealment or target drift found

- Original r002 and final r003 `brief.json` are byte-identical, SHA-256 `67f033d70cbf57fb087cffa9d345758d50bef29e4d2a61111677545702358f97`; the modeling freeze records the original target unchanged. The intended generic angular breccia-outcrop teaching prop and its bounded scientific claims remain unchanged.
- The original full-batch static review remains historical as written: r002 was accepted bounded as a static generic teaching asset. The newer website screenshot/diagnostic adds a later platform-specific defect finding; I did not rewrite or relabel the previous review as a past failure.
- Original and final GLB material definitions match exactly; material alpha is opaque/default in both. Source material definitions also match exactly. No alpha/material workaround was found.
- Original and final proof-render configs are byte-identical (SHA-256 `94400a61547ac850cd053257c64456c745e67e6ff2243d94ed5c00981748b2d2`), including camera, framing, renderer, lighting and samples. No camera, renderer or depth-bias concealment was found.
- The original r002 file, website screenshot/diagnostic, original report and prior build/freeze history remain retained.

## Final r003 artifact and checks

Pinned final GLB SHA-256: `72584669cf0926313c81fc88f34f8c76ed8706c4d26272856dcdf0cf3eac2147` (115,472 bytes). Saved Blender source SHA-256: `4ce3a73e4f32a45d036c5555cd19266772ca08c65399bb99c17224028c4e3154` (623,332 bytes).

- Project static GLB audit: PASS, 2,120 triangles, 8 primitives, 5 materials, 3,960 POSITION entries, 0 textures. Budget limits checked: 14,000 triangles, 1,000,000 bytes, 6 materials, 30 primitives. Actual values are 2,120 / 115,472 / 5 / 8.
- Independent Khronos validator: PASS, 0 errors and 0 warnings.
- Fresh Three.js 0.180.0 `GLTFLoader.parseAsync`: PASS on the exact final GLB, 8 primitives and 2,120 triangles. This is not a browser or GPU render.
- Blender 4.3.2 source comparison: both saved r002 and r003 sources reopened read-only under the blocking production Blender lock with two threads. r003 has 1,302 authored/evaluated vertices, 2,120 triangles, measured Blender bounds `3.679635 × 2.648611 × 1.905729 m`, and exported Y-up GLB bounds `3.679634 × 1.905729 × 2.648611 m`. All seven source mesh parts are closed with positive volume and zero boundary/non-manifold edges. r003 total enclosed source volume is `10.3872152707 m³`; the source/export report’s triangles and bounds agree within tolerance.

## Actual r003 proof frames and queued rebuilds

The r003 render manifest SHA-256 is `d113f5296e702398d21800619c48a9d91808fe12247f917b69200947ed2c06af`, created at `2026-10-20T14:56:32.213174+00:00`. Both its `source_glb_sha256` and `subject.glb_sha256` bind to the exact final GLB above, revision r003. I independently checked PNG bytes, manifest hashes, dimensions and decoded RGBA digests; all eight frames match at 512×512. I inspected every individual final view: hero, reversehero, front, side, rear, top, clay and silhouette. No copied or relabeled old pixels were used. The frames show the same generic rock mass with angular embedded fragments, with no visible thin crosshatching in the clay view. They are Blender Cycles CPU proof views, not website-stage evidence.

Two actual queued Blender jobs are preserved as distinct successful jobs in the same sequential queue invocation. They have separate job IDs, request fingerprints, output directories, PIDs, start/end times, output source hashes and stdout `BUILT` lines. Both result records match every declared output; each rebuilt GLB equals the pinned final SHA-256, and both semantic comparisons are byte-identical with digest `6347913e8ad68e6d93640c2458a75870f4c4fb072ef9f3e9b71b7314241c2f5e`.

| Job | PID | Start → finish (UTC) | Fingerprint | Request SHA-256 | Result SHA-256 | Rebuilt GLB SHA-256 | Rebuilt source SHA-256 |
|---|---:|---|---|---|---|---|---|
| semantic-rebuild-1 | 123 | 14:56:32.660673 → 14:56:36.897252 | `fde7f2e1d2f4ba9535978592fcb035c178e0d5b7833dd224c0d89e3f49be16e0` | `a334925211ed9fcfc764ccf2fd15fbd49a042fa60385137b269d4b2b18595067` | `373d3f6036b4473f93959ec1595ee7130c8a9d291b9d869a30142f3d791bec40` | `72584669cf0926313c81fc88f34f8c76ed8706c4d26272856dcdf0cf3eac2147` | `cfdfc965e9cd4985723b295ff25a5b77c8c6e4d75dab7a633b06f86ee94dceb9` |
| semantic-rebuild-2 | 146 | 14:56:36.904413 → 14:56:41.201151 | `090344d2d279e001557c741727ed7d41c4956b5f597365c8e4e759b1a5268a04` | `af4bf77515888d7f68aa70484d85f0c0c9bd3dc3ce26c05be7dc00bf7da6a68a` | `968561b65610277ddfd133a60bda582982c504238b10ce81a34b5abae5a50142` | `72584669cf0926313c81fc88f34f8c76ed8706c4d26272856dcdf0cf3eac2147` | `88ae09c280f5acacd6c99e115b25e5a33da1bb04ee096c509a3e6610c55cdfaa` |

The semantic comparison reports `generator_executed:false` because that checker compares saved files rather than executing a generator itself. The actual executions are separately evidenced by the queued request/result records, distinct PIDs/times/output directories, successful output hashes and both stdout build records; no generator was rerun during this independent QA.

## Preserved assets, status and limits

I independently checked current bytes against all saved after-hashes for the three other accepted candidate trees: Burgessochaeta r002, rotational landslide r001 and stalagmite-group r003. All 64 files in each tree match; no build or render was invoked for them.

The producer checkout remains clean at `d32ad6eeb619216f3b4868a66a5020c3cd74c388`. The r003 candidate ledger remains `approved_for_brief:false`; formal stages remain unknown/pending. Concept evidence is valid but incomplete because the internal provider timestamp remains unavailable; no time was inferred. The historical r002 report at `/workspace/shared/lowpoly-round25-qa65/report.md` is unmodified (SHA-256 `f6866f3c37b3fdf8cd0024c72756c4508fce1cdc4ef6879f1b71eb51a4da447a`). No push, upload, publication, GPU render, populated-scene test or final website retest was performed in this QA.

## Evidence files

- `machine-summary.json`: concise decision and blockers.
- `differential-evidence.json`: final pins, full render-frame binding, queue records, no-concealment checks, preservation hashes and candidate limits.
- `independent-overlap-check.py` / `independent-overlap.json`: independent exact-GLB geometric test and full pair set.
- `independent-source-reopen-compare.py` / `source-compare.json` / `.log`: locked read-only source reopen and host/material comparison.
- `independent-component-compare.py` / `component-compare.json` / `.log`: source fragment component hash comparison.
- `project-static.json` / `.log`, `khronos.json`, `three-parse.json`: independent final-GLB checks.

The original website screenshot is referenced by path/hash in the evidence only; it is not copied into this report folder.

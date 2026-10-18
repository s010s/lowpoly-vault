# Batch 24 independent QA — williamsonia, halkieria, ctenorhabdotus, conglomerate-outcrop — source SHA 15ebe8c0420bcb128f5c9496c7c77f96787ab736

**Source pin:** `candidate/small-life-batch24-20261018` @ `15ebe8c0420bcb128f5c9496c7c77f96787ab736`<br>
**Frozen model source commit in handoff:** `b1460146163ad4421f05c6cef51d8e59ff063b97`<br>
**Scope echo:** `williamsonia`, `halkieria`, `ctenorhabdotus`, `conglomerate-outcrop` only. All four IDs, the exact source pin, and the four expected GLB hashes match `QA-HANDOFF-SCOPE.json`.
**Profile:** `static-stylized-v1` / `2026-10-18.1`<br>
**Verdict:** all four PASS within their frozen natural, refined low-poly teaching-art briefs. These are not strict scientific reconstructions.

## Independent checks

- Recomputed SHA-256 and byte counts for each candidate JSON, editable Blend, selected GLB, profile contract, brief, metadata, freeze record, view manifest, and source/runtime contact sheet. All match the frozen handoff. The supplied `HANDOFF.md` and `QA-HANDOFF-SCOPE.json` hashes are recorded in `review.json`.
- Re-ran `scripts/validate_candidate.py` under the pinned profile for all four candidates. Each is `valid=true`, `profile_contract_status=pass`, with no errors. `approved_for_brief=false` remains unchanged because the original formal stages and approval are pending.
- Reopened every exact Blend in Blender 4.3.2. Confirmed unit scale 1, identity asset root, no saved camera/light objects, positive mesh transforms, source triangle counts, closed export meshes, and no degenerate triangles. Independently audited each exact GLB and found matching source/export counts and bounds.
- Khronos glTF Validator 2.0.0-dev.3.10 returned 0 errors and 0 warnings for every pinned GLB.
- Reproduced each GLB in the supplied pinned Three.js 0.180.0 viewer using Chromium ANGLE SwiftShader WebGL2. Captured seven directions, 80/160/240 px views, and two six-copy scene views per asset. All 12 PNG hashes per asset exactly match the frozen runtime manifest. No browser errors or failed requests. This is software-rendering evidence only, not hardware-GPU performance evidence.
- Inspected actual pixels in all four source and runtime contact sheets, including silhouette, clay, top, reverse, side and bottom views. The small-size captures reduce fine detail as expected; the main asset forms remain distinguishable at the normal/near views.

## Measurements and verdicts

| Asset | Revision / selected attempt | Nominal scale | Measured GLB bounds X×Y×Z (m) | Triangles / GLB | Six-copy scene calls / triangles | Verdict |
|---|---|---:|---:|---:|---:|---|
| williamsonia | r001 / attempt-02 | 0.10 m structure height | 0.0480 × 0.0960 × 0.0450 | 4,314 / 88,364 B | 18 / 25,884 | PASS |
| halkieria | r001 / attempt-01 | 0.07 m body length | 0.0255 × 0.0169 × 0.0700 | 8,040 / 154,268 B | 30 / 48,240 | PASS |
| ctenorhabdotus | r001 / attempt-02 | 0.055 m body height | 0.0458 × 0.0523 × 0.0412 | 11,614 / 223,948 B | 24 / 69,684 | PASS |
| conglomerate-outcrop | r001 / attempt-02 | 0.80 m outcrop width | 0.8034 × 0.4476 × 0.4143 | 7,840 / 174,328 B | 24 / 47,040 | PASS |

### williamsonia — PASS

Checkpoint `5560604ebb0ec37af38821b873b909ade8b1763a`; Blend SHA-256 `6270ec94bdcf3d4b58911a598c5ddc4e213012a74b04e5fae5e4a76398e5d932`; GLB SHA-256 `be8508e48b7bdd40eaff065d9e26bcc753ba9794df9bf34485dc36686380e2a7`.

The compact ovulate cone reads as a distinct oval reproductive organ with a restrained tessellated surface and continuous short stalk. The selected attempt-02 resolves the earlier pinched stalk profile. The 96 mm measured height is close to the nominal 100 mm art-direction size. No petals, whole parent plant, or unsupported associated organs are implied.

### halkieria — PASS

Checkpoint `2ae0cfa84f639ddc5f344b608c4cb2def397b22e`; Blend SHA-256 `3602d86d20eeea3ff52686aa26999ea09a280c90db7568a8d6ce2b60bfc8b22a`; GLB SHA-256 `b68978490fededa8e37ef6a3b8e131ce5f4047d7385bdc90a3f4442ac18ed76b`.

The flattened crawler has distinct anterior and posterior cap shells, an orderly overlapping dorsal armour rhythm, and short marginal sclerites. Side, top, front, rear, clay and bottom runtime views show a coherent connected body. The review accepts simplified plate counts and makes no exact species, phylogeny, or locomotion claim.

### ctenorhabdotus — PASS

Checkpoint `dfaf6ce25fa9a97ff7f43d258e8b5d7151f7aee7`; Blend SHA-256 `b676aea99bf5db6365495ab918da19738f65fd693ab34b8d0d878ad5bee1f17c`; GLB SHA-256 `bdf4ce2db481b2e54947ade282ba13e0a4dd762adc1e33e288886012f6cc271b`.

The short oval barrel, flatter poles and repeated triple comb-band groups remain legible in source and exact-GLB views. Attempt-02 separates the bands enough to avoid a merged stitch-like appearance. Fine band detail falls away at 80 px, while the overall body remains readable; the 160/240 px and larger views recover the diagnostic rhythm. No bell, tentacle curtain, or microciliary detail is claimed.

### conglomerate-outcrop — PASS

Checkpoint `b1460146163ad4421f05c6cef51d8e59ff063b97`; Blend SHA-256 `9c3d477b58d81e71b95c0c70e8e48530de0dfe67451160308bcb0e626d66cec3`; GLB SHA-256 `26b2433a5fbc8f2742b6f37a90af274e2409b29c850568ec1127a5d95d607be4`.

The irregular matrix reads as one continuous finer-grained mass containing varied rounded clasts, with a clear bounded cut face and curved relief. Attempt-02 removes the negligible cut-edge degeneracies recorded for attempt-01. The clasts remain visually embedded rather than reading as a loose sphere pile. No exact site, age, or clast chemistry is inferred.

## Limitations and handoff state

- No must-fix visual or mesh defect was found within the four frozen briefs.
- Browser/runtime checks used SwiftShader software WebGL2. Hardware GPU rendering and physical-device performance remain unknown.
- The full planning verifier still lacks `production/continuous-small-life-20261018/queue.json`; the handoff reports direct frozen checksums for its 72 planning entries. This does not invalidate the exact asset/hash review above.
- The static profile record is structurally valid, but candidate approval remains pending and the original formal stages remain unknown. This review does not change candidate stage fields, publish, or authorize merge.
- Legacy license-check errors for consulted-only references are preserved; no license claims were fabricated and no reference media or geometry were incorporated.

Exact per-file pins, per-view digests/dimensions, Blender reopen results, GLB bounds, Khronos findings, runtime screenshots and renderer metrics are in [`review.json`](./review.json).

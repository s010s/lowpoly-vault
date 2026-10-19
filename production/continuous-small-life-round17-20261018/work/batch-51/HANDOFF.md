# Batch 51 candidate handoff

Artifact source commit: `ee4e37b3c1cc49ab5e41c807c6ca8e1a155bbc6b`.

The handoff-only commit adds this file and QA-HANDOFF.json. All selected artifact pins refer to the artifact source commit above. This is a candidate delivery, not approval or publication.

| Asset | Revision | Derived plan | Triangles | GLB bytes | Bundle |
|---|---|---|---:|---:|---|
| dicranurus | r001 | batch51-concept-plan-v001 | 9016 | 481424 | `assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001` |
| calcite-raft-deposit | r002 | batch51-concept-plan-v002 | 1400 | 79228 | `assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002` |
| accretionary-lapilli-bed | r002 | batch51-concept-plan-v002 | 5496 | 291392 | `assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002` |
| conichnus-conical-burrow | r001 | batch51-concept-plan-v001 | 1790 | 86088 | `assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001` |

Every bundle contains actual editable Blender source, standalone GLB, frozen generator/config, original ImageGen concept/prompt/result receipt, concept inspection, both construction and final artifact freezes, measured source/export metrics, source reopen, two separate queue rebuilds, full Khronos report, exact final eight-frame manifest and transparent cover, plus Chromium/Three.js and nine-copy SwiftShader evidence. Final fixed views were actually opened individually. Original round17-plan-v001 inputs and r001 attempts are preserved; selected r002 files do not overwrite them.

Conichnus: actual clean-GLB raycasts measure center cavity depth 0.1124999672 m below outside top, with 0.0275000334 m substrate below the narrow basal termination. Gray top, oblique and explicit half-section are under diagnostics/. KGS genus description supports rounded base; the asset uses a strongly tapering narrow rounded termination rather than inheriting Lockeia almond relief or claiming a mathematically sharp apex. Section operates on a diagnostic copy, while delivered GLB remains intact.

Known blockers remain explicit: all four concept completeness checks are valid but incomplete solely because exact ImageGen generation time was not disclosed. Real invocation/result/original and premodel inspection exist; no mtime, capture-time substitution or fabricated clock PASS was used. Technical and runtime_parse automated stages pass; visual, factual, specification, GPU-image acceptance and representative-scene acceptance remain unknown for independent QA. ANGLE SwiftShader evidence establishes software functionality only; hardware GPU and actual parent/museum scene are unverified.

Use QA-HANDOFF.json for exact four-ID guard, source commit, selected revisions, all artifact and evidence hashes, dimensions, bytes and remaining blockers. Parent coordinates exactly one new-context GPT-6 Luna xhigh model QA. Begin from exact GLBs, brief/reference ledger and raw views, without treating maker notes as an acceptance verdict. No independent or integration task was created here.

Integrity commands, repeated for each bundle:

```sh
python3 scripts/validate_candidate.py <bundle>/candidate.json --root . --profile static-stylized-v1 --profile-contract <bundle>/profile-contract.json --json
python3 scripts/validate_concept_evidence.py <bundle>/concept-evidence.json --root <bundle> --require-complete
```

The first exits 0 for a structurally valid pending candidate. The second currently exits 1 for the honest exact-generation-clock gap. Adding --require-approved to the first must fail until all required independent decisions and blockers are resolved. No standard was lowered.

Git boundary: only this batch candidate/work/necessary planning files were added. No main branch, formal asset directories, release descriptor, website, CI, deployment, PR merge, Google Drive or permission changes. Git author is the verified Leon Made This <8357465+s010s@users.noreply.github.com>.

Original art/renders/prose: CC BY 4.0, Leon Made This / s010s. Executable code: MIT. References are consulted only, with no copied media, meshes or textures.

## Supplemental specification correction v001

The original handoff and every original candidate/model/concept/freeze/evidence file are preserved. See `specification-correction-v001/index.json` and the original handoff copies in `specification-correction-v001/historical-handoff/`. The original source artifact commit remains `ee4e37b3c1cc49ab5e41c807c6ca8e1a155bbc6b`.

Independent QA `925ff855ad0fcc3635cfc44a457101344ffddbde` found two inherited nominal-scale contradictions, not visual defects. New supplemental specification briefs select the existing prompt/construction-design nominal values: Calcite 0.32 m and lapilli 0.28 m. Their exact measured GLB XYZ bounds remain separately recorded; these nominal values are not exact bounding boxes or fossil measurements. All geometry, originals, references and evidence are unchanged.

The new supplemental briefs are for a targeted specification difference review. They are NOT silently substituted for the immutable registered r002 candidate briefs; historical candidate reports remain bound to their original subjects. `QA-HANDOFF.json` distinguishes `candidate_brief` from `corrected_specification_brief` and retains both pins. No formal stage, source receipt, generator configuration, render manifest or approval is relabeled. The current candidate validators remain valid/unapproved; concept completeness remains incomplete because exact provider generation time is unknown. No clock substitution, gate change or new full model QA is authorized by this correction.

Replay the additive metadata/identity checks with `python3 production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/verify_correction.py`. This mechanical result is not independent model or specification acceptance.

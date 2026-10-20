# Batch 55 candidate handoff

Branch: candidate/small-life-batch55-concept-20261020
Main baseline: 0cbef7c9826ddd1d83e7d0c941b7864dbaa6865c
Planning source: 0044cdab4ba0fd18ab35b5158ae977b3083cc776 (only required round20 inputs; no merge).
Execution thread: 01a156e7-da1f-74f2-8e73-50637c8ea004; separate task ID unavailable, parent confirms. Parent thread: 01a15646-8945-7703-be3c-da5870e32021.

Final subjects:

| Asset | Revision | Triangles | GLB bytes | GLB SHA-256 |
|---|---|---:|---:|---|
| vermicularia | r001 | 9264 | 503156 | 5bb8a455b222496fbe8568184eb2aff11b717aab29bbf42d3138707781b27f7f |
| weichselia | r001 | 2492 | 135004 | 4ece730443de73b6c2dca2fe2bc7a50517628e344b5e6edd37486901c997676a |
| ventifact | r001 | 28 | 3644 | 291ad1bbff024594c61ad218ea4fc33add08425d2998fbec20051de8abad64fa |
| pentichnus-deep-dwelling-trace | r002 | 90 | 7840 | aefb89b47511df9534a02af61e0d96c77bafc34c2646eb295891bc2104cc59f9 |

Every final bundle is under `assets/candidates/continuous-small-life-round20-20261020/batch-55/<asset>/<revision>/`. It contains editable Blend, standalone GLB, original generator/config and frozen brief/references, original ImageGen sheet/prompt/receipt, exact eight-view proof and navigation sheet, candidate JSON, metrics, hashes, raw format/source/rebuild/Node parse reports. Work and all attempt logs: `production/continuous-small-life-round20-20261020/work/batch-55/`.

Checks: final Khronos 0 errors/0 warnings; static budgets within 14k triangles / 1MB / 6 materials / 30 primitives; source reopen/axis bounds pass; all final source meshes have zero boundary/non-manifold edges; two separately executed semantic rebuild comparisons pass; Three.js 0.180.0 GLTFLoader Node parse pass. All 32 separate 512px proof frames inspected by maker. No independent acceptance signature. GPU/browser/populated scene not run and not claimed. One Blender process, two threads.

Pentichnus r001 has source topology warnings and is superseded by r002; both are retained. Shared renderer rejected silhouette, so failed attempts remain, and a local derived renderer adds black emission silhouette and preserves side semantics without editing repository helpers. Original dependencies pinned.

Chronology: ImageGen provider time/model/seed undisclosed and remain null. Receipt observed at 2026-10-20T01:25:32Z; pixel inspection separately recorded. Exact generator authoring start unrecorded/null; derived freeze precedes generator writing and first Blender construction. Real queue started/finished timestamps retained. Concept checker valid=true, evidence_complete=false due unknown provider and authoring start times; completeness gate intentionally remains nonzero. Candidate/profile checks stop at null maker.task_id; parent must resolve actual identity without guessing. All seven candidate acceptance stages remain unknown/pending; passing raw reports are not self-approval.

Reference limits: Shell Museum old/new page full fetch 403, indexed museum excerpts support generic coiled-to-uncoiled pattern and V. recta fossil context; MolluscaBase supports named fossil taxon. Weichselia repository abstract opened, PDF unavailable. NPS and KGS sections opened. Factual morphology remains for independent review. No third-party media/mesh incorporated. Original code MIT; art/prose CC BY 4.0, Leon Made This / s010s.

Dimensions: measurements.json separates nominal artistic Blender XYZ intent, measured Blender XYZ, and measured glTF XYZ. glTF Y-up is not Blender Z-up. No exact specimen-scale claim.

Parent next action: pin the actual model-source commit plus four GLB hashes; launch exactly one fresh-context GPT-6 Luna xhigh batch QA, no maker verdict used as independent outcome. No main/catalog/site/PR20 changes, no merge PR or deployment.

Frozen model-source commit: `1e43f9e2c79b6d2465d8eadf2169355cba3690c7`. QA scope pins this exact source commit and four GLB hashes. Later handoff-only commit does not change model bundles.

## Identity correction after original handoff

The original missing-ID statements and stored candidate check failures above are historical. `maker-identity-provenance.json` records the coordinator-verified original task creation identities: task/thread `01a156e7-da1f-74f2-8e73-50637c8ea004`, original turn `01a156e7-e4c5-70b8-9dd7-9cf381271201`. The stable task thread ID now fills maker.task_id; no distinct task identifier or new production turn is invented. Only the maker identity blocker is resolved. Candidate/profile hashes are rebound; original candidate evidence reports remain untouched as historical observations.

All four final model subjects remain pinned to model-source `1e43f9e2c79b6d2465d8eadf2169355cba3690c7`. Candidate artifact/texture descriptors, every GLB, Blend, concept image, proof frame, freeze, brief, reference, generator, config and historical evidence remain byte-identical. The separate independent QA branch `qa/batch55-independent-20261020` at `1cdfab1b0351c61854b5480c8eac012440232fa1` is not rewritten or re-run. New identity-only validation is in `maker-identity-validation.json`; it does not promote any acceptance stage, manufacture missing timestamps, merge, publish or deploy.

Identity-only validation outcome: all four profile-contract compatibility checks pass, but full candidates remain invalid at the next pre-existing obligation: `production: frozen source/generator/config required_deliverables missing`. Each frozen brief explicitly contains an empty required_deliverables list; the static compatibility fallback only applies when that field is absent. No frozen brief or validator was edited to bypass it. Legacy retains the zero-turntable incompatibility. Concept integrity stays valid/incomplete. The 75 candidate and 20 profile regression tests pass.

Checksum audit: all 205 present per-bundle manifest entries match. The original commit omitted five .log entries per final asset (`khronos.log`, `reproducibility-1.log`, `reproducibility-2.log`, `source-export.log`, `source-metrics.log`, all under evidence/), while listing their hashes. These 20 historical missing files are disclosed, not recreated. All 460 protected tracked round20 files remain identical to the prior candidate head, including 20 GLBs, 20 Blends, 79 PNGs and 15 Python files.

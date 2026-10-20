# Batch 55 independent QA

**Outcome:** Independent technical, visual, factual, specification and runtime-parse checks pass for the four pinned model revisions. The physical-GPU and target-production-scene stages remain **unknown / unrun**. The candidate records remain **pending**; this report is not an approval or publication authorization.

## Pinned subjects

Candidate branch `candidate/small-life-batch55-concept-20261020` at `b2341debdb31f73e0719d4aadbe832321db6008a`; frozen model source `1e43f9e2c79b6d2465d8eadf2169355cba3690c7` (verified ancestor). QA scope and handoff were read from the candidate commit. The detailed GLB, Blend, concept, prompt and all 32 proof-frame SHA-256 values are bound in [`evidence/asset-binding.json`](evidence/asset-binding.json).

| Asset | Revision | GLB SHA-256 | Blender source bounds (XYZ m) | Tris | GLB bytes | Mats / primitives |
|---|---|---|---|---:|---:|---:|
| vermicularia | r001 | `5bb8a455b222496fbe8568184eb2aff11b717aab29bbf42d3138707781b27f7f` | 0.17785 × 0.08915 × 0.07701 | 9,264 | 503,156 | 4 / 4 |
| weichselia | r001 | `4ece730443de73b6c2dca2fe2bc7a50517628e344b5e6edd37486901c997676a` | 0.16354 × 0.15532 × 0.30000 | 2,492 | 135,004 | 5 / 5 |
| ventifact | r001 | `291ad1bbff024594c61ad218ea4fc33add08425d2998fbec20051de8abad64fa` | 0.81334 × 0.91816 × 0.60000 | 28 | 3,644 | 2 / 2 |
| pentichnus-deep-dwelling-trace | r002 | `aefb89b47511df9534a02af61e0d96c77bafc34c2646eb295891bc2104cc59f9` | 0.13315 × 0.12663 × 0.13000 | 90 | 7,840 | 4 / 4 |

Dimensions above are measured in Blender Z-up XYZ; candidate `measurements.json` separately reports GLB Y-up XYZ. These are artistic design bounds, not measured specimen scale. The nominal Blender XYZ differs by about +19% on vermicularia's Y extent and +22% on ventifact's Y extent; the briefs do not specify strict dimension tolerances, so these are recorded as nonblocking scale advisories.

## Independent stage results

Each cell is the independent outcome recorded in this review. Source `candidate.json` stage fields are still `unknown` and approval remains `pending`.

| Asset | Technical | Visual | Factual | Specification | Runtime parse | GPU | Scene |
|---|---|---|---|---|---|---|---|
| vermicularia r001 | Pass | Pass | Pass | Pass | Pass | Unknown | Unknown |
| weichselia r001 | Pass | Pass | Pass | Pass | Pass | Unknown | Unknown |
| ventifact r001 | Pass | Pass | Pass | Pass | Pass | Unknown | Unknown |
| pentichnus-deep-dwelling-trace r002 | Pass | Pass | Pass | Pass | Pass | Unknown | Unknown |

### Technical and specification

All four pinned GLBs match QA-scope hashes. Khronos glTF Validator `2.0.0-dev.3.10` reports zero errors and zero warnings for each. The static profile is satisfied: at most 14,000 triangles, 1,000,000 bytes, 6 materials and 30 primitives; all four have zero textures, zero external images, zero cameras and no required extensions. Source Blender audits found no boundary or non-manifold edges on the four final source meshes. Dimensions and bounds are finite and recorded with the Blender Z-up / GLB Y-up distinction.

I independently reopened each `.blend` with Blender 4.3.2 and compared its export collection to the exact GLB. Triangle counts match and the largest axis-converted bound error is below `1e-7 m` for each. I also imported each pinned GLB into a clean Blender 4.3.2 process; triangles, materials and bounds matched the static GLB data. Reports and logs are in [`evidence/source/`](evidence/source/) and [`evidence/glb-reopen/`](evidence/glb-reopen/).

### Visual and factual

I inspected each original concept sheet, each 8-view contact sheet, and the hero/top source images against its frozen brief. The independent browser renders are also preserved under [`evidence/webgl/`](evidence/webgl/).

- **vermicularia:** the continuous juvenile coil, irregular adult tube, thick aperture and open lumen read clearly. The concept's bead-like apex was corrected to a continuous coil. The linked Shell Museum article could not be fetched directly (403); indexed museum excerpts support the generic coiled-to-uncoiled analogy, while [MolluscaBase's *Vermicularia recta* record](https://molluscabase.org/aphia.php?id=1355272&p=taxdetails) supports the fossil taxon context. The asset remains explicitly an inspired study, not an exact specimen.
- **weichselia:** the short single stem, thick cortex, raised attachment relief and restrained cut face are clear. The [linked 2021 repository abstract](https://orbi.uliege.be/handle/2268/295478) supports the cortex and external scale-insertion context. The reference URL is sound, though the title string in `references.json` should be corrected to the publication's full title when metadata is next edited.
- **ventifact:** three broad planes and their sharp ridges remain legible in the clay and silhouette views; there are no paint-only erosion cues. The [National Park Service Aeolian Landforms page](https://www.nps.gov/subjects/geology/aeolian-landforms.htm) supports the wind-abrasion premise; the exact facet arrangement is the explicitly original design.
- **pentichnus-deep-dwelling-trace:** r002 reads as a deep, narrowing, five-sided negative cavity with an illustrative section cut. [Kansas Geological Survey systematic ichnology](https://www.kgs.ku.edu/Publications/Bulletins/245/04_ichno2.html) supports the five-sided subconical/depth distinction. The brief correctly labels the negative cavity as illustrative and avoids an unsupported tracemaker or behavior claim.

### Pentichnus r002 repair check

I checked the defect that r002 claims to fix, not just the older r001 conclusion. Fresh Blender metrics show r001 had **2 boundary edges and 6 edges classified non-manifold including those boundaries** (4 additional non-boundary non-manifold edges) around the cavity-floor/cap topology. r002 has **0 boundary and 0 non-manifold edges**, with the cavity-floor correction described in [`repair-note.md`](evidence/pentichnus-r002-repair-note.md). The [r001→r002 generator diff](evidence/pentichnus-generator-r001-r002.diff) shows that the floor/cap geometry was reworked. Its source and GLB both have 90 triangles and matching bounds. The reported repair is present in the pinned r002 geometry; no remaining mesh repair is required.

### Runtime and scene limits

Three.js `GLTFLoader` `0.180.0` parsed each exact GLB in Node and loaded/rendered all four in headless Chromium `154.0.8037.57` using WebGL 2 and ANGLE/SwiftShader. The independent software renderer string identifies SwiftShader; page errors and console errors were zero. A synthetic four-asset smoke composition rendered at 11,876 triangles including its ground plane. Its image and exact GLB pins are recorded in [`evidence/webgl/software-webgl-report.json`](evidence/webgl/software-webgl-report.json).

This confirms software WebGL loading/rendering only. It does **not** test physical GPU performance, a target browser/device, or the target production scene. No target scene path or configuration was specified in the inspected batch material, so the `gpu` and `scene` gates remain unknown rather than being marked passed.

## Record status and minimum follow-up

The independent results above do not change any candidate record. The formal candidate validator reports `valid: false` solely because all four `candidate.json` files have `maker.task_id: null`; it stops before completing the profile-contract check. The separate independent static audit did run and passed the pinned profile for all four GLBs. The task ID must be filled from the actual confirmed task identity, never inferred. Each concept-evidence result is `valid: true` but `evidence_complete: false`, with the exact blockers `concept_generated_at: unknown` and `modeling_started_at: unknown`. Provider generation timestamp/model/seed and generator-authoring start remain null. Only actual receipt/pixel-inspection and first Blender geometry timestamps are retained; no mtime was used to invent chronology.

Minimum outstanding items before the formal record can validate or all seven gates can be complete:

1. Resolve the real maker task ID from its owner and update the candidate record through its authorized owner.
2. Run the intended physical-GPU/browser check and the actual target production scene when that environment/scene is identified.

No geometry repair is required for the four pinned versions. The Weichselia reference-title correction is a metadata advisory, not a mesh blocker; scale deviations are documented, not treated as hard failures because the briefs identify the dimensions as artistic intent without a strict tolerance.

## Reproduction

See [`evidence/README.md`](evidence/README.md) for exact commands and requirements. Machine-readable results are in [`independent-qa.json`](independent-qa.json). The package contains source/export reports, fresh Blender GLB-import reports, Khronos validator results, candidate/concept checker output, browser WebGL results, images, and the exact-input hash binding. No candidate model, main branch, catalog, website or publication record was changed.

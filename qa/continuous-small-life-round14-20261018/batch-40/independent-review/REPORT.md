# Batch 40 independent QA

## Decision

**Content QA: PASS for all four exact, hash-pinned assets within their frozen, intentionally stylized scopes. No model repair is required.** The drawings read naturally at the intended child-friendly environment-prop scale; the fixed views and actual-GLB runtime pixels show no broken silhouette, missing surfaces, detached critical parts, or wrong-subject substitution.

**Formal profile acceptance remains BLOCKED.** The saved Chromium/Three.js evidence uses WebGL2 on ANGLE SwiftShader software rendering. It establishes that the exact GLBs parse and render in that software runtime; it does not establish hardware-GPU behavior or performance. The candidate records remain `approved_for_brief=false`. If formal acceptance is required, capture the required WebGL2 evidence on supported hardware and bind it to each unchanged GLB SHA below.

## Identity and review scope

- Candidate branch: `candidate/small-life-batch40-20261018`
- Candidate/handoff commit: `af92e43e0b191f024c72232a40f0fe0f42996fa1` (the remote branch ref was verified at this full SHA)
- Model-source commit: `cf7565ed2c4ca70c4ffed567aa32ec0aafd40a0b`
- Batch: `batch-40`; exact IDs, in handoff order: `sidneyia`, `botrychium`, `barrier-island`, `diplocraterion-spreite-burrow`
- Parent task: `01a1187a-1f8d-746a-8448-61f8cb38d0fc`
- Profile: `static-stylized-v1`, rule `2026-10-18.1`; one independent review round
- Reviewer identity: the parent requested GPT-6 Luna xhigh. This execution environment did not expose model-identity metadata, so the backend identity is **not independently verified**.

The frozen handoff and QA scope files were read. Their exact hashes are recorded in `evidence/artifact-audit.json`. That audit checked all 110 distinct path/SHA references found in the handoff against the files on this commit; all matched. It also parsed each actual GLB v2 header/JSON chunk and checked primitive, triangle, vertex, material, texture, and position-bound data against the pins. Each frozen Blend was independently reopened read-only in Blender 4.3.2; its evaluated `EXPORT` geometry, units, and bounds match the source-scene and source-export evidence. Stored two-run rebuild records bind both byte-identical GLBs to each delivered hash; the builds were not rerun.

The eight Blender fixed views and the actual Chromium/Three.js single-item and six-instance runtime screenshots were inspected as pixels. Their individual file hashes, dimensions, and view bindings are in `evidence/artifact-audit.json`; Blender reopen results are in `evidence/blend-open-audit.json`. Khronos validator reports are hash-pinned in the handoff and record zero errors and warnings for all four GLBs. Three source-export records carry only the existing “smooth faces require intentional-style review” warnings; I reviewed those surfaces in the actual images and found no actionable defect. Barrier-island's two additional exact-GLB context captures were inspected separately; the blue plane is a labeled display datum, not GLB water geometry or a simulation.

## Hash-bound results

Dimensions below are the exact GLB X/Y/Z bounds in meters. Blender dimensions use Blender's Z-up axis order in the evidence JSON; they are axis-converted in the GLB as expected.

| Asset | Attempt / checkpoint | GLB triangles / materials / primitives | Dimensions (m) | Blend SHA-256 | GLB SHA-256 | Result |
| --- | --- | ---: | --- | --- | --- | --- |
| `sidneyia` | `attempt-01` / `b5d6a4d5dc9fa51672e2b4b1435892b706873f49` | 9,360 / 4 / 10 | `0.091629 × 0.024121 × 0.157563` | `5efab6f9aa667332a32099cbb10f7b51e3fce3139ec61efaae04ee1c6fe31f94` | `aee5615e6cf4c94c81f8038dd6f8549609e89d2cd30fd51a9109f2ad7bd17aa5` | Content PASS; no model fix |
| `botrychium` | `attempt-01` / `4d1b50010311495c8e3f2ded4066f582150ab656` | 9,496 / 2 / 2 | `0.072272 × 0.004250 × 0.160000` | `17bb228c277f0e4842f0cd9362e1800240fc0293df93055c04c0474a34eae8e2` | `cf068307745f6167560877d44359d188939dfa43928b4b87e8da2eee038ebb77` | Content PASS; no model fix |
| `barrier-island` | `attempt-01` / `628aaeb3336cc8d7170dc9310754a20cba9e4539` | 2,920 / 3 / 4 | `20.000000 × 2.119825 × 11.800218` | `4dfdb4f507f039f26fa52eca7f1a94816f94bab695ff356361732055875ddb2f` | `5876bedea2434d7f9f8e01b1ac6dcafacf06edc18f27e010b95a05e76989d156` | Content PASS; no model fix |
| `diplocraterion-spreite-burrow` | `attempt-01` / `cf7565ed2c4ca70c4ffed567aa32ec0aafd40a0b` | 9,076 / 4 / 10 | `0.250000 × 0.246000 × 0.056786` | `56017e4101708b2751172edda9521fb2d16417cec1c1b8743d64db55a60c8311` | `1bb03ea5e48dfb4a09b95657d89a134f4226f2d3d2ce40ecc86183756b250fde` | Content PASS; no model fix |

## Per-asset review

- **Sidneyia — PASS.** The broad, overlapping trunk plates taper into a narrower ringed abdomen and paired tail paddles; the domed head, antennae, eyes, and economical limbs remain connected and readable across the fixed and runtime angles. This meets the brief's named-taxon-inspired teaching-art scope. It is not a strict specimen reconstruction, and exact limb/segment counts, locomotion, and color are not claimed. The ROM description supports the broad head/thorax, narrower abdominal rings, telson/flaps, antennae, and eyes ([ROM Sidneyia description](https://burgess-shale.rom.on.ca/fossils/sidneyia-inexpectans/)).
- **Botrychium — PASS.** The single shallow-relief fertile branch system has acute branchlets and visibly attached rounded sporangia. It reads as a preserved fertile fragment, without implying a complete plant, roots, or unattached vegetative organs. That scope is consistent with the Rothwell and Stockey paper's fossil-fragment description ([author-uploaded paper text](https://www.researchgate.net/publication/250269889_Fossil_Ophioglossales_in_the_Paleocene_of_Western_North_America)). The simple, repeated forms are appropriate here; no microscopic spore detail is needed.
- **Barrier island — PASS.** The exact GLB shows a separate mainland crop and elongated detached sand barrier with an open corridor between them. The two separately pinned context images place a flat blue display datum at `0.3 m`, making the lagoon/ocean relationship legible while clearly labeling the plane as display-only. The form communicates a general barrier/lagoon teaching concept, not a site, full measured island, or water simulation. This stays within the NPS coastal-landform scope ([NPS Sandy Coast Landforms](https://www.nps.gov/articles/sandy-coast-landforms.htm)).
- **Diplocraterion spreite burrow — PASS.** The actual mesh and close neutral/runtime views show the U-shaped wall, two open mouths, and eight successive intervening sheets. These are modeled geometry rather than painted stripes. It is a sectional teaching concept; it does not claim an exact specimen or trace-maker. The KGS discussion identifies the spreiten connecting U-burrow arms as the distinguishing form ([Kansas Geological Survey, Diplocraterion discussion](https://www.kgs.ku.edu/Publications/Bulletins/245/04_ichno.html)).

## Evidence paths

- Handoff: `production/continuous-small-life-round14-20261018/work/batch-40/HANDOFF.json`
- QA identity/scope: `production/continuous-small-life-round14-20261018/work/batch-40/QA-HANDOFF-SCOPE.json`
- Source branch pin: `evidence/source-ref.txt`; other batch-40 remote refs: `evidence/batch40-remote-refs.txt`
- Actual file hashes, parsed GLB data, all eight fixed images, runtime PNGs, contact sheets, runtime reports, and barrier context PNGs: `evidence/artifact-audit.json`
- Independent read-only Blend reopen metrics and per-object results: `evidence/blend-open-audit.json`, `evidence/blender/`, and `evidence/logs/`
- Stored maker evidence, checked against the exact hashes above:
  - Each asset's `production/continuous-small-life-round14-20261018/work/batch-40/<asset>/r001/source-scene.json`
  - Each asset's `production/continuous-small-life-round14-20261018/work/batch-40/<asset>/r001/source-export.json`
  - Each asset's `production/continuous-small-life-round14-20261018/work/batch-40/<asset>/r001/reproducibility.json` and `two-rebuilds.txt`
  - Each asset's `assets/candidates/continuous-small-life-round14-20261018/batch-40/<asset>/r001/attempt-01/<asset>/view-manifest.json`, `source-contact-sheet.jpg`, and `runtime-contact-sheet.jpg`
  - Each asset's `assets/candidates/continuous-small-life-round14-20261018/batch-40/<asset>/r001/attempt-01/<asset>/runtime/single.json` and `runtime/scene.json`
  - Barrier context: `production/continuous-small-life-round14-20261018/work/batch-40/barrier-island/r001/barrier-context.json` and `assets/candidates/continuous-small-life-round14-20261018/batch-40/barrier-island/r001/attempt-01/barrier-island/context/{hero,top}.png`

## Limits and remaining gate

- The static-profile reports are valid for their explicitly pinned sidecar contract, but the existing candidate records remain unapproved. The old legacy report errors about a missing source `license` field are preserved; all cited references here are marked consulted-only, and the ledgers report no third-party model, texture, or source image incorporated. That legacy warning does not require a model change.
- The handoff notes that the frozen planning verifier cannot complete against main because its historical queue file is absent; direct frozen checksum checks are recorded as passed. This review independently checked the handoff artifact pins present at the candidate commit and did not run the planning verifier.
- Hardware-GPU evidence remains unknown. The software-WebGL captures do not claim a hardware renderer, a physical-device result, or performance.
- No model, candidate, threshold, CI, permission, publication, Drive, or main-branch file was changed. This branch contains only this independent QA report and its supporting audit evidence. No merge was performed.

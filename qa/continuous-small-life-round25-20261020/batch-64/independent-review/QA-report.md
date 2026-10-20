# Independent QA report: lowpoly-vault batch64

**Reviewer:** GPT-6 Luna xhigh (fresh-context independent review)  
**Pinned source:** `e2fc0ab54ba3f99228dd27964a63be56f10ed2b8`  
**Branch:** `candidate/small-life-batch64-concept-20261020` (clean before and after QA)  
**Review date:** 2026-10-20 UTC

## Decision

All four exact r001 static GLBs receive a bounded **ACCEPT** for the five stages independently tested: technical, visual, factual, specification, and runtime parse. **The full seven-stage gate is BLOCKED** for each asset because target GPU rendering and a populated composed-scene test were not performed. These findings are independent QA evidence, not formal candidate approval, user approval, or publication authority. The repository candidate records remain `approved_for_brief: false`; no model, candidate, approval, or publication files were changed, and nothing was uploaded or published.

## Per-asset results

- **Chancelloria** — `3e1e643beb551fe16db51f72be43f3ec9ff5c9c5d66ea1dad8dd19581822591c`; 11,148 triangles, 4 materials, 6 primitives, 0 textures, 577,132 bytes. Five tested stages ACCEPT; GPU and scene BLOCKED. The model reads as an attached tapered hollow sac with open crown/pore, dense crown ring and five-ray projecting sclerites. Scope correctly retains unknown affinity and treats the restored body/sclerite layout as evidence-informed, not a measured fossil replica. ROM distinguishes the Chancelloria lectotype USNM 66524 from Allonnia USNM 66528 and describes the hollow cylindrical body, pore, outward central ray, tangential rays and 4–7 rays per spicule. [ROM source](https://burgess-shale.rom.on.ca/fossils/chancelloria-eros/)
- **Parabolic dune** — `203a4940714165708aed83799fa132eae02c633d7581806fef47f4540ff4bcf9`; 4,994 triangles, 4 materials, 4 primitives, 0 textures, 333,152 bytes. Five tested stages ACCEPT; GPU and scene BLOCKED. The low arms trail toward −Y, with a rounded higher nose at +Y, continuous low interior and sparse anchoring vegetation; no barchan reversal or star ridges. NPS describes vegetation holding long parabolic arms while the nose migrates forward, and contrasts this with barchan arms pointing forward. [NPS dune reference](https://www.nps.gov/grsa/learn/nature/dune-types.htm)
- **Terminal moraine** — `31c3eda6721127b5bb04e5d9fa797a6c51164eb991fd43a28cc58741c20b2470`; 8,358 triangles, 4 materials, 4 primitives, 0 textures, 519,636 bytes. Five tested stages ACCEPT; GPU and scene BLOCKED. The visible broad irregular transverse debris arc, low valley floor and varied angular stones distinguish it from a sinuous esker; no site-specific lake/glacier claim. NPS supports terminal-position debris at the glacier toe; the consulted NPS photo provides the arcuate landform reference. [NPS moraine reference](https://www.nps.gov/articles/terminalandrecessionalmoraines.htm)
- **Geyser sinter cone** — `7401c44118c072bb31c4b7b5347d263a66f0c7c3b6429281fe3e22373203cf84`; 2,404 triangles, 4 materials, 5 primitives, 0 textures, 129,780 bytes. Five tested stages ACCEPT; GPU and scene BLOCKED. The generic squat, irregular tiered cone has a genuinely open narrow vent/recessed throat and lobe-like crust; no eruption, exact geyser, assay, or plumbing simulation claim. NPS supports silica/sinter cone formation around narrow vents and geyserite-like bulbous deposits. [NPS hydrothermal reference](https://www.nps.gov/yell/learn/nature/hydrothermal-features.htm)

## Seven separate stages

For **each** of the four exact GLBs: `technical ACCEPT`; `visual ACCEPT`; `factual ACCEPT`; `specification ACCEPT`; `runtime_parse ACCEPT`; `gpu BLOCKED / not run`; `scene BLOCKED / not run`. No CPU proof render was treated as GPU or composed-scene acceptance. Details and bindings are in `findings.json`.

## Independent verification performed

- Rechecked all four SHA-256 values against the pinned branch; opened each source `.blend` read-only with Blender 4.3.2 under the required blocking shared flock and `--threads 2`. Authored and evaluated vertex counts matched for every source; no modifiers were present; each source object had zero boundary and nonmanifold edges; source/export triangle counts and axis-converted bounds matched.
- Independently parsed each exact GLB using Three.js r180 `GLTFLoader` and `gltf-validator` 2.0.0-dev.3.10: zero parse errors, zero Khronos errors/warnings, exact expected triangle/material/mesh counts, zero textures. All four are within the frozen limits of 14,000 triangles, 6 materials, 30 primitives, 1,000,000 bytes, and zero textures.
- Inspected all **32 individual original-resolution final frames** (8 views × 4 assets), plus the four lossless contact sheets. Each final manifest binds the exact GLB, the packaging-derived candidate brief, the delivery-v001 rights ledger and frame hashes. The candidate brief differs from the frozen brief only by post-build source/generator/config path-and-hash closure; its frozen design criteria remain unchanged. The original frozen brief itself was not modified. The original eight-view sets remain preserved, are hash-checked, and bind the original frozen reference ledger. The separately rendered delivery sets bind the new ledger; original frames were not relabeled.
- Verified per asset that two distinct semantic rebuild requests each have separate request/result records, unique run fingerprints and PIDs, successful return codes and output hashes matching the candidate GLB. These are runner attestations plus the exact output comparisons, not cryptographic proof of artistic quality.
- Recomputed all seven freeze-file hashes for every asset. The original frozen brief/config/reference/concept files match. The candidate-brief packaging adapter adds only post-build artifact path/hash closure and source/generator/config deliverables; the original design content is unchanged. Each delivery ledger adds explicit non-incorporation/rights declarations; no consulted third-party fossil/photo pixels are included in the candidate bundle or redistributed.

## Evidence limitations and release status

The concept image and pixel-inspection evidence are present. However, exact provider-generation/tool-invocation and modeling-start timestamps are unavailable. The preserved clarification labels the start time as approximate/inferred, and `concept-validation.json` honestly keeps `evidence_complete: false`; no unknown timestamp was promoted into a fact. This limits completeness but is not evidence of fabrication. Separately, required GPU and scene stages remain unrun, formal approval remains pending, and publication authority is separate.

Actual nominal/artistic bounds are recorded in `findings.json`. For example, the parabolic dune’s relief measures 7.355748 m against the 8.0 m nominal brief dimension; the frozen brief expressly calls dimensions nominal/artistic and supplies no numeric pass tolerance, so this was not treated as a measured-scope failure.

## Durable evidence

- `findings.json` — per-asset identity, all seven stage outcomes, measurements, source/bindings, chronology, rights and rendering evidence.
- `source-reopen.py` and `source-reopen.log` — independent locked Blender reopen procedure and output.
- `runtime-parse-independent.json` — independent Three.js r180 parse plus Khronos-validator measurements for each exact GLB.
- `artifact-binding.json` — digest binding for this report and its evidence to the pinned candidate revision.

Primary scientific references: [ROM Chancelloria eros](https://burgess-shale.rom.on.ca/fossils/chancelloria-eros/), [NPS dune types](https://www.nps.gov/grsa/learn/nature/dune-types.htm), [NPS terminal/recessional moraines](https://www.nps.gov/articles/terminalandrecessionalmoraines.htm), and [NPS Yellowstone hydrothermal features](https://www.nps.gov/yell/learn/nature/hydrothermal-features.htm).

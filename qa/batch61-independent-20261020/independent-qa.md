# Independent batch 61 QA

Date: 2026-10-20 UTC  
Outcome: one candidate `ACCEPT_BOUNDED`; three candidates `BLOCKED` on a narrow specification-metadata defect. This is not release approval.

## Exact source and scope

Read-only verification used checkout `/tmp/lowpoly-batch61-20261020`, branch `candidate/small-life-batch61-concept-20261020`, final HEAD `f1737e4f00dfc5c1817084ecb31763320ec2a163` (clean), and payload commit `b2ff8314140e2539c825d573fef2152584120059`. The only files added between payload commit and final HEAD are batch `HANDOFF.md` and `handoff.json`. Final HEAD and all four selected GLB/Blend hashes were pinned before review. Applicable `static-stylized-v1` contract is rule `2026-10-18.1`: fixed eight-view output and zero turntable frames; publication authority remains separate.

## Findings by candidate

| Candidate | Independent bounded outcome | Pinned GLB SHA-256 | Pinned editable Blend SHA-256 | Geometry / technical result |
|---|---|---|---|---|
| pseudopulex r003 | `ACCEPT_BOUNDED` | `75f6799431a7bf6037881c78d12e7cf731670fcb2fdea82b66576dadc8cdf99c` | `e572b15e3efffc4331f3b865c4fe74fb37d29632893b459904cc87fc233b8415` | 5,112 triangles; 14 primitives; 5 materials; no textures; 310,212-byte GLB |
| daemonelix-helical-burrow r002 | `BLOCKED` | `c415fbe405e75ac182bb39512ea33b43f81d574723263f04378422fb0221aa82` | `802c13dc3117cadd7748201ca2dc5fce4b3a50cc60ab5791e0042ba463ea6248` | 3,858 triangles; 2 primitives; 2 materials; no textures; 210,896-byte GLB |
| mesa r002 | `BLOCKED` | `399e9fb78b225cd808563598485888ea343b568e8bc2cac8b427939fc94f1cad` | `716288207373eb8d1b4ff123bc9bebda485d1b015d3e85f09b5c5b94f053f57d` | 1,022 triangles; 5 primitives; 5 materials; no textures; 79,124-byte GLB |
| drumlin r002 | `BLOCKED` | `317dee38ec731d1939985a61fd431238a188b5be34dfcc717dafe23dc4bd7534` | `ee0abc1e2a6860fb6624c0bf150f4c29f0287ab306539c5a2ad75e6d241a8fea` | 1,638 triangles; 1 primitive; 1 material; no textures; 126,080-byte GLB |

`BLOCKED` is limited to the copied, animal-specific scale-note clause described below. The other visual, factual, geometry and parsing findings for those three are positive within this bounded review; their exact GLBs need not be altered to address the metadata issue. All four current candidate integrity records are valid but explicitly remain pending/not approved. The project gate is not a maker or release approval.

## Material blocker and minimal correction

The specification issue is the exact JSON field `scale_note` in each current delivery brief:

- `assets/candidates/continuous-small-life-round23-20261020/batch-61/daemonelix-helical-burrow/r002/candidate-brief.json#/scale_note`, current brief SHA-256 `2fcfd328842918ca9e1bc75bbb542692960c9a1f0644eb678bd8cca5a5056896`
- `assets/candidates/continuous-small-life-round23-20261020/batch-61/mesa/r002/candidate-brief.json#/scale_note`, current brief SHA-256 `4bf4e45bce74a19ba20ef2d8f658d08358c702ad0bb449055732434489f346cf`
- `assets/candidates/continuous-small-life-round23-20261020/batch-61/drumlin/r002/candidate-brief.json#/scale_note`, current brief SHA-256 `12ddf48322e3b644df06d7df62a15a4272ed1a7bd5df680fe6e8ed2ed169ad6a`

All three fields currently say: `Illustrative nominal envelope; actual measured bounds reported separately. Animal body nominal17mm excludes antenna; pose appendages extend bounds.` The animal-body/antenna clause is false and irrelevant for a fossil burrow cast and two geological-form assets, and makes their frozen specification internally inconsistent. The same text is suitable for pseudopulex, whose delivery brief is `candidate-brief.json` SHA-256 `3ee0ecc2d4a18b634c4d94eddea7fa985ce458c91538749388d230695f8fbe67`.

Minimal acceptable repair: leave each original `brief.json`, its original modeling-freeze record/hash, geometry, source Blend, generator, config, reference ledger and exact GLB immutable. Publish a documented new delivery-adapter / metadata revision that retains the old record and hashes for audit, explicitly identifies the superseded copied `scale_note`, and carries only a suitable asset-specific correction. For example: “Illustrative teaching-asset envelope only; actual mesh bounds are reported separately. Not a measured specimen or named-site dimension.” For Daemonelix, “not a measured fossil-burrow specimen dimension” is also appropriate. Update downstream candidate/handoff metadata bindings to the new metadata revision/hash, but do not retroactively rewrite the frozen original or change geometry. Then run focused validation of the new metadata binding, candidate record, and specification field. No rerender or geometry regeneration is indicated by this defect. A targeted differential QA of the three changed metadata records is sufficient after correction.

## Visual, concept, and factual review

All four concepts and all 32 exact final 512×512 proof frames were inspected; every frame's hash matched its render manifest and pinned GLB. The final head macro for pseudopulex was also inspected and hash-bound to its r003 GLB. The four actual consulted-only reference images matched the ledger hashes and were viewed as pixels, not accepted from summary text: Gao et al. 2012 original Pseudopulex Figure 1 (DOI `10.1016/j.cub.2012.03.012`), the NPS Daemonelix exhibit photo, the NPS Wild Horse Mesa photo, and the NASA Landsat drumlin image. These consulted references remain outside the candidate repository; a full hash scan found no copied reference pixels in the candidate tree.

- **Pseudopulex:** The final is a whole-organism reconstruction with a broad dorsoventrally flattened dominant abdomen, not modern flea lateral compression; six long similar legs without enlarged jumping thighs; a short wingless thorax; serrated stylet/claws and tibial combs. Original whole-organism obligation remains intact. The head macro shows palp shafts connected into head and bead segments, not floating beads. Fine setae, palp count/detail, colors and soft morphology remain explicit artistic simplifications; no species blending, host or blood meal claim. Proud collar repair is resolved in r002 and head/palp connections in r003.
- **Daemonelix:** Final silhouette reads as an exposed, solid helical burrow-cast/infill with open spaces between turns and a terminal chamber/neck; it does not read as a hollow pipe or modeled animal. Read-only source reopen verifies a single connected closed solid. The r002 join seam is resolved. Exact coil count, chamber profile and scale remain illustrative, not measured-site reconstruction.
- **Mesa:** Broad flat cap, coherent layers, integrated scarps/embayments and lower talus read clearly; no detached rectangular strap geometry remained in r002. It is presented as a generic geological form with no named-site, age or habitat claim.
- **Drumlin:** Smooth, low, elongated, rounded asymmetric mound with blunt end and taper; the r002 cusp is gone. No ice-flow direction is claimed because directional conventions conflict, and NASA's overhead image cannot establish vertical profile.

Original brief/config/reference/concept freezes precede generator authoring and modeling; the documented geometry repairs preserve the original frozen brief/reference hashes and do not narrow scope. The four concept images are valid evidence, but exact provider-internal generation times and precise modeling start were not returned. The source correctly flags chronology as incomplete; no times were inferred from filesystem mtimes.

## Independent technical checks

- Four exact source Blends reopened read-only in Blender 4.3.2. Authored components were closed/watertight; no boundary or non-manifold edges or loose vertices were reported. Reopened source vertex counts match source claims, and exported POSITION accessor counts match handoff values. Measured bounds match independent Y-up GLB/Three.js bounds after axis conversion.
- Source vertex counts / exported accessor counts: pseudopulex 3,002 / 11,096; Daemonelix 1,933 / 7,688; mesa 513 / 2,817; drumlin 821 / 4,756.
- Each exact GLB passed the project static GLB check, official Khronos validation (zero errors and zero warnings), and an independent Three.js `GLTFLoader.parseAsync` v0.180.0 parse.
- Two distinct queue-bound Blender processes per asset (eight unique process PIDs total) succeeded with return code 0. Each rebuilt file was byte-identical and semantically matching to its pinned final GLB; source/generator/config closure hashes and seeds verified. The evidence contains two queue run IDs overall, not eight separate queue runs.
- Exact native images, candidate records, generator/config/dependency closure, and all final pins are independently recorded in `verification.json`; support reports and commands are retained in this QA directory.

## Limits and files

The requested bounded technical/visual/factual/specification/runtime-parse checks were performed. Target GPU hardware rendering and composed-scene checks were not run; they remain separate candidate stages and no GPU, scene, live, formal user-approval or release claim is made. No source, candidate flags, old models, CI, site, remote branch, Git state or approval state was changed by this review. All new reports and evidence are under `/tmp/lowpoly-round23-qa61` only.

Machine-readable details: `results.json`; underlying exact pins and checks: `verification.json`, `audit-details.json`; validation output files are named per candidate (`*-candidate-gate.json`, `*-glb-gate.json`, `*-khronos.json`, `*-three-parse.json`, `*-source-reopen.json`). Visual inspection sheets are `*-exact-full.jpg` in this directory.

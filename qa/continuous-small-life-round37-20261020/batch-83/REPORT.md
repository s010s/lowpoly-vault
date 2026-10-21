# Batch83 independent fixed-candidate QA

Commit: `1e0664988dfd77ec163bee527f11fc482668fddd`

Result: **3 local PASS, 1 REVISE. Zero formal approvals.** GPU and composed-scene stages remain NOT RUN for all four.

## Blocking correction

wave-dominated-delta r002, SHA-256 `03ee5b98b897a979e2204ffaede9cdcf152ac0ff966c6e5ef5e4ecf2a66dfcea`: the secondary distributary is isolated blue triangles, and the main river also has continuity breaks. Exact original top view plus two fresh focused diagnostic renders and water-region adjacency establish the defect.

Retain the smooth arcuate shore and shallow plain. Rebuild/resample actual channel bed and bank topology along both river centerlines, with sufficient nonzero cross-sectional width and connected water/bed faces from upstream through the branch and two open mouths into the sea. Avoid reliance on vertex-only corner contacts, per-triangle paint thresholds or renderer/depth-bias tricks. Do not simply recolor intervening high bank faces.

New immutable revision with original frozen scope intact; actual selected final GLB two queued semantic rebuilds, source/export checks and exact eight512px views. Fresh targeted difference review of main/secondary bed continuity, bank silhouette, mouth shore regression and all previously passing invariants. Preserve this failed original evidence.

Evidence: `wave-dominated-delta/channel-diagnostic/detail.png`, `clay.png`, their hash-bound render manifest and `wave-dominated-delta/water-connectivity.json`.

## Per-asset local decisions

### cloudina r002 — PASS

GLB: `eae46d63f9c74f3a53bd2862ad94a57d7302e5806c06432be9d996107dd7c805`

Stages: technical=pass, visual=pass, factual=pass, specification=pass, runtime_parse=pass, gpu=not_run, scene=not_run.

Measurements: 10944 triangles; 594200 GLB bytes; 5472 authored/evaluated vertices; 21884 exported POSITION vertices.

- PASS: WOOD2017 Fig.2b actual photograph plus article nested-cone paragraph; hero/front/clay show a narrow single wall with flaring eccentric units.
- PASS: Top through-lumen and broken end contours, plus saved-source watertight wall topology. Closed wall manifold does not mean closed tube lumen.
- PASS: Genus-level fragment only; no species/locality, soft tissue, natural basal apex or life orientation claim. 12 mm length and palette explicitly illustrative; microlaminae unresolved.

No local geometry correction required by this review. Separately test actual target GPU and populated scene; this is not formal or release approval.

### wave-dominated-delta r002 — REVISE

GLB: `03ee5b98b897a979e2204ffaede9cdcf152ac0ff966c6e5ef5e4ecf2a66dfcea`

Stages: technical=pass, visual=fail, factual=fail, specification=fail, runtime_parse=pass, gpu=not_run, scene=not_run.

Measurements: 11104 triangles; 331868 GLB bytes; 5554 authored/evaluated vertices; 10895 exported POSITION vertices.

- PASS: NPS Delta Landforms paragraph on longshore redistribution and slight seaward bulges; NASA Nile analog pixels and final top show broad low plain and smooth modest bowed coast.
- FAIL: Frozen brief expressly selects one main incised river and one subdued secondary mouth. Exact top/detail shows disconnected blue pieces; independent edge adjacency identifies 11 water regions, including three isolated one-triangle secondary patches.
- PASS: No actual Nile DEM, agriculture, exact place, period or ecosystem claim; channel-count failure is against this original design, not a universal rule that every wave-dominated delta must have exactly two mouths.

Repair B83-DELTA-01 before targeted difference review; then independently test actual target GPU and populated scene.

### lava-tube-entrance r003 — PASS

GLB: `b7022acdc470a85c3ff76fa13025e3a95e75ac6fe7a5b9b6a3ee2d98c3789f00`

Stages: technical=pass, visual=pass, factual=pass, specification=pass, runtime_parse=pass, gpu=not_run, scene=not_run.

Measurements: 4120 triangles; 229524 GLB bytes; 2064 authored/evaluated vertices; 8327 exported POSITION vertices.

- PASS: NPS Lava Caves/Tubes formation text and actual El Malpais entrance photo support thick low roof over a cavity. Front/hero/clay and saved source show hollow roof/walls.
- PASS: Modeled recessed interior and solidified floor; original source interior geometry and rear wall bound a finite segment. No black plane substitutes for volume.
- PASS: Generic entrance module, not exact El Malpais, cave scan, age or ecosystem. No molten lava, vegetation or engineered access copied from a photo.

No local geometry correction required by this review. Separately test actual target GPU and populated scene; this is not formal or release approval.

### impact-crater r002 — PASS

GLB: `cfd50732977a30859163cfee30ce7190324830c07500a26ce63aeaa47a67cd43`

Stages: technical=pass, visual=pass, factual=pass, specification=pass, runtime_parse=pass, gpu=not_run, scene=not_run.

Measurements: 4608 triangles; 304108 GLB bytes; 2306 authored/evaluated vertices; 11352 exported POSITION vertices.

- PASS: NASA/USGS Barringer photograph and final top/clay show excavated bowl. Source profile floor 35 m, plain about260 m and rim about403 m before local variation confirm the depression is below the plain.
- PASS: Nonperfect ring with mild rim variation, inner radial relief and outward slope merging into quiet broad plain. No central uplift, volcano or eruption.
- PASS: Generic simple crater only; shape is explicitly not impact-origin proof, exact Barringer reconstruction or measured site scale. Primary caption/image were inspected before freeze; supplemental process text chronology is corrected transparently.

No local geometry correction required by this review. Separately test actual target GPU and populated scene; this is not formal or release approval.

## Provenance and exactness

All651present tracked input files matched immutable Git blobs. Original selected inventory matches canonical source entries/hash. Each original r001 freeze, final subject hashes, final frame hashes, camera/render bindings and lossless contact-sheet cells were verified. Delivery brief changes are only the separately declared packaging adapter and hashed deliverables.

All four fresh saved-source exports are byte-identical to delivered GLBs. Project audits and evaluated-source topology passed; Khronos reports0errors/0warnings; Three.js0.180.0 Node parses passed. Each asset has two genuinely distinct queued successful execution chains with checked requests/results/logs/output hashes and fresh semantic comparisons. See `provenance-audit.json`, `fresh-processes.json` and each asset folder.

All32original final frames, four original concepts and four consult-only source images were personally inspected. Full per-view findings, source URLs and seven-stage states are in `independent-qa.report.json`. No reference pixels were copied into this QA package.

Concept checker is valid but `evidence_complete=false`: provider internal generation time and exact authoring start remain unknown. Observer invocation/return/inspection and actual process intervals are retained, not reconstructed from mtimes. Impact process text was read just after freeze; the transparently retained supplement corrects the original ledger claim, while the required NASA/USGS caption/photo preceded freeze.

## Boundaries

Maker tree and all prior evidence unchanged. Four read-only saved-source reopen/export jobs and one two-frame focused diagnostic process used the global blocking flock and2threads each. No push, PR, merge, release, site, CI, security, access or credential changes. The three local passes require actual GPU/scene work before formal acceptance.

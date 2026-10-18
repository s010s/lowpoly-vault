# Batch 11 independent QA

**Verdicts: PASS for all four frozen candidates**, within the supplied static, stylized brief and its non-scientific-reconstruction claim. I found no must-fix defect in the reviewed exports, connections, proportions, scale, or supported display range.

I compared the surfaces and palette against the accepted trio v002 reference: the four candidates keep the same calm colors and soft, continuous forms without adding unnecessary microdetail. The [style reference image](evidence/images/trio-v002-style-reference-before-after.jpg) is included in the evidence bundle.

This report reviews source candidate commit `7394fef092feb21ab9c084f331cfdf35a86979aa` (`candidate/small-life-batch11-20261018`) against main `0bd62cda92814af5ac781e1a706bba6310cecc35` and the explicit `static-stylized-v1` rule `2026-10-18.1`. The selected per-asset checkpoints are ancestors of that exact source commit. No model, gate threshold, CI, permission, or publication state was changed.

## Frozen candidates and review

| Asset | Verdict and visual review | GLB bytes / triangles | GLB SHA-256 | Blend SHA-256 |
|---|---|---:|---|---|
| `micrabacia` | **PASS.** A clear low radial disc; broad ribs and shallow central cup remain coherent from top, side, clay, silhouette, and exact-GLB views. No obvious broken rim or detached geometry. | 162,836 / 8,960 | `89bc867f362236919fe72faec8dbdf789ce4f5b61d745cb83eefc9226b34c40e` | `e35fc9f6f67f75fa0d4fd2d0b241113d28daf18456583911dbe6c22b7a99dde3` |
| `sengelia` | **PASS.** The low, branching ground plant has legible K-junctions and attached root-bearing axes; it reads as terrestrial shore/wetland vegetation, not algae. Small leaf cues are secondary at card scale, as expected for this simplification. | 77,400 / 3,940 | `4c8ad676418f7918f401c3dbd8e2280c3c4f548db56ba4b234f530be7a934f61` | `7dbd2d9d24d0e74bdb29e62a0e8901ea0818226c1d84ab2f169c86a97bec80e2` |
| `coquina-outcrop` | **PASS.** The continuous, compact rock mass and partially exposed shell fragments read as lithified coquina, not a pile of loose shells. The selected `attempt-02` keeps the shell details attached and the silhouette quiet. | 213,368 / 11,480 | `d540bc55b753bd32cf253878f5adcba085623bbb68588f249b1d7a15e40926cc` | `19b497fbd8c4f87c5c1b4eb522d722a486baf971aa185152847bc30762da5eb7` |
| `naraoia` | **PASS.** Two dorsal shields, the narrow joint, paired limb rows, and forward appendages remain distinct in top, side, and near views. The simplified smooth shields do not turn it into a modern crab or a left/right bivalve. | 133,596 / 7,400 | `36ca01ff1daba56e4b9e4abc36833503e7bafba0819668f02d4d9c98aafa6fe1` | `422e388b11c0cfce4d1be0c8ace053c04d26bd9428f85502996a67394f76e68c` |

## Technical, scale, and runtime checks

- Recomputed the handoff, freeze, candidate, source, generator, config, reference, profile-sidecar, practical-integrity, and named evidence hashes and byte counts. Each asset's 20 view-manifest frames also match their file hashes and byte counts: exactly eight fixed source views, 12 exact-GLB runtime frames, and zero turntable frames.
- Reopened each frozen `.blend` in Blender 4.3.2 and imported its exact frozen GLB. Source/import triangle counts, materials, and world bounds agree; bound differences are at most `1e-5` m. Source meshes have no boundary edges, non-manifold edges, or degenerate triangles. All object determinants are positive. The source scenes contain no cameras or lights.
- Ran the project static GLB audit at the brief's unchanged ceilings: 14,000 triangles, 6 materials, and 30 primitives. All four pass with no audit warnings. Re-ran the Khronos glTF Validator `2.0.0-dev.3.10`: **0 errors / 0 warnings** for each.
- Explicit `static-stylized-v1` candidate validation reports `valid: true` and `profile_contract_status: pass` for all four. The retained legacy checker still records its historical missing-license-field error; the current sidecar identifies those sources as consulted-only, with no media incorporated, and does not invent a license.
- Inspected all eight fixed source views and the exact-GLB runtime contact sheets, including the 80, 160, and 240 px views plus 480 px near views. Runtime manifests pin the exact GLB hash and show nonzero rendered triangles. Six-instance scene evidence reports 6/18/18/24 draw calls and 53,760/23,640/68,880/44,400 triangles respectively.

Measured dimensions are consistent with the nominal art-direction scales: Micrabacia disc span 0.060 m; Sengelia ground-axis span 0.258 m vs 0.25 m nominal; Coquina width 0.823 m vs 0.8 m nominal; Naraoia two-shield body length 0.0535 m vs 0.05 m nominal. Naraoia's full appendage envelope is 0.0727 m; the extra length comes from the appendages, not oversized shields.

## Bounded factual review

The briefs limit these to stylized, named-taxon-inspired teaching props rather than strict specimen reconstructions. I reviewed claims only at that scope:

- The Scleractinia reference supports solitary and colonial coral forms, not a genus-specific Micrabacia silhouette. The candidate stays within the brief's broad radial-disc inspiration and makes no specimen-level claim. [Digital Atlas of Ancient Life: Scleractinia](https://www.digitalatlasofancientlife.org/learn/cnidaria/anthozoa/scleractinia/)
- The primary Sengelia paper describes an Early Devonian lycophyte with prostrate shoots, K-branching, leafy stems, and root-bearing axes in flood-prone settings. The model's land-plant / shore-wetland label and branching-root form fit that bounded use; it is not presented as algae or a strict reconstruction. [Matsunaga & Tomescu, 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5604611/)
- The NPS overview describes coquina as shell fragments cemented into porous limestone. The model follows that general shell-rock concept without claiming an exact locality or specimen. [National Park Service: Coquina](https://www.nps.gov/casa/learn/historyculture/coquina-the-rock-that-saved-st-augustine.htm)
- The ROM fossil entry describes Naraoia's two dorsal shields and paired cephalic/trunk appendages. The candidate retains the two-shield body plan with deliberately simplified limbs. [Royal Ontario Museum: Naraoia compacta](https://burgess-shale.rom.on.ca/fossils/naraoia-compacta/)

## Nonblocking note

At 80 px, Sengelia's individual leaflets are hard to distinguish, although the branching plant silhouette remains visible and the brief's terrestrial wetland label resolves its category. Keep that habitat caption with the smallest gallery card; no geometry change is needed for this pass.

## Evidence and reproducible commands

The [evidence index](evidence/README.md) links the copied source/runtime sheets, image hash ledger, frozen-input audit, Blender reopen/import reports, static GLB audits, Khronos reports, and profile-validation outputs. The [commands and pins record](evidence/commands.md) lists the executed commands and exact source/base refs. `frozen-input-audit.json` records the exact hashes for every checked file and frame.

This QA verdict does not mutate or promote the candidate record. The maker's profile output still has the formal production-stage fields `unknown` and `approved_for_brief: false`; the legacy failure remains preserved. Parent-owned acceptance/integration/publication must use its own release process.

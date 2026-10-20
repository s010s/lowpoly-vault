# Targeted differential QA: batch 66 repair r002

- Fixed source: `ed8c2e7994ce1463c487e3ace18105888ef3211e`, clean branch `candidate/small-life-batch66-concept-20261020`.
- This is only the differential review of repaired Louisella and Hoodoo. Original r001 history and original QA were preserved; that report's SHA-256 remains `5a05852395f37ee76a66f73ffe49b430b469fd9ea63c32313c7b2903f0451c14`.
- All 16 final 512×512 frames and both r002 contact sheets were opened and visually reviewed. Camera/material concealment checks included clay/silhouette/top/rear/reverse angles. Original concept and primary-source pixels were used only for comparison; no reference pixels were copied into this QA evidence.
- All four r001 directory trees were independently rehashed; unchanged. Accepted Graben and river tree digests remain `707f3cd43570b200c537bf1d6f3aa98b4328913b7fff93fbdc89d36dc8e04929` and `c545609ea01e365d71ab92ed1d6b30d1ceaa1cce010065da6fec50111cc2db90`; neither asset was rebuilt or rerendered. Original inventory digest remains pinned.

| Asset | Exact GLB | Measured | Bounded disposition |
|---|---|---:|---|
| louisella r002 | `63a540aaf41598f0921b10083020af9763789a41395ef6e46641b9ed7a4fc50c` | 10860 tris; 576116 B; 6 materials; 9 primitives; 0 textures | **ACCEPT BOUNDED** |
| hoodoo r002 | `dbe8dfda24834a86b2a7609aee52d7bcf9d90c416a5c9ee321c63d5359a5fc9c` | 2516 tris; 138580 B; 4 materials; 4 primitives; 0 textures | **ACCEPT BOUNDED** |

## Differential findings

- **Louisella: ACCEPT BOUNDED.** The previously pointed posterior is now blunt, smoothly rounded and unspined in side/rear/silhouette. Two separated blunt papilla ridges are visible in top, hero and clay views. Annulated middle, short-spined anterior, papillate region and smooth rear read as differentiated texture zones at full output resolution; the proboscis retains its long-spine ring and fine scalids. No unsupported gill-function claim. It remains an illustrative whole-organism reconstruction, not a specimen-scale replica.
- **Hoodoo: ACCEPT BOUNDED.** The previous four regular full-rim tiers are replaced by three asymmetric interrupted local projections and unequal shoulders on a single irregular tapered pillar. Color, clay, rear, reverse, top and silhouette views confirm real geometry, not just banding or camera concealment; cap is coherent/modest and foot broad. This is a generic teaching prop, not a named locality or measured section.

## Stage disposition, kept separate

| Asset | technical | visual | factual | specification | runtime_parse | GPU | scene |
|---|---|---|---|---|---|---|---|
| Louisella r002 | ACCEPT | ACCEPT | ACCEPT bounded | ACCEPT | ACCEPT (Node Three parse only) | BLOCKED / unknown, not run | BLOCKED / unknown, not run |
| Hoodoo r002 | ACCEPT | ACCEPT | ACCEPT bounded | ACCEPT | ACCEPT (Node Three parse only) | BLOCKED / unknown, not run | BLOCKED / unknown, not run |

Independent project static audits pass; source reopen has exact triangle/bounds agreement and no boundary/nonmanifold edges; Khronos validator 2.0.0-dev.3.10 reports zero errors/warnings; Three.js r180 parses the exact GLB hash. Both models meet the 14,000 triangle / 1 MB / 6 material / 30 primitive budgets.

For each repaired asset, two distinct semantic-rebuild jobs were independently matched to successful request/result records, PIDs, request/result SHA-256, start/end times, output hashes and semantic digests; each rebuilt GLB is byte-identical to r002. These queue records remain attestations, not cryptographic proof of execution. Exact original concept provider-generation and generator-authoring start timestamps remain unknown; no filesystem mtime was used to infer them.

No actual browser GPU execution, composed scene, formal/user approval or publication was performed. Candidate validation remains `approved_for_brief:false`; bounded acceptance is not release authorization. Full quantitative/evidence closure is in `machine-summary.json` and `independent/`.

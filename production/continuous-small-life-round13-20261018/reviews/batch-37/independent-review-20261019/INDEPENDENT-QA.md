# Batch 37 — independent QA (2026-10-19)

**Review base:** `handoff/batch37-20261018` at `4642f57de8be861e2e9ecc44f05167424e7e7973`  
**Scope:** exact pinned candidates `pentremites`, `schizoneura`, `tombolo`, and `entobia-sponge-boring-network`.  
**Reviewer model identity:** not independently verified. The parent requested GPT-6 Luna xhigh, but this environment exposed no verifiable model/version/reasoning-effort metadata.  
**Profile reviewed:** `static-stylized-v1`, rule `2026-10-18.1`.

## Decision

**Bounded static-stylized content QA: PASS for all four. No model repair is required.** Each asset reads in its supplied fixed views and exact-GLB runtime evidence, fits the requested natural, refined low-poly teaching-art direction, and has an editable Blend that opens. The delivered GLB has the same triangle count and bounds as its source export; both pinned semantic rebuild reports match the exact delivered GLB digest. Candidate commits and 134 handoff-pinned artifacts were checked with zero missing or mismatched pins.

This content QA does **not** turn the candidates’ `approved_for_brief` field to true. The explicit static profile validator returned `valid: true` and `profile_contract_status: pass` for each, while all four records remain `approved_for_brief: false` with required stages/blockers still unknown or pending. The legacy checker also remains invalid because each consulted-only reference has no nonempty `license` value. The pinned reference ledgers say no source media, mesh, or texture was incorporated; I did not invent a reuse license or alter any record.

All bundled runtime evidence uses Chromium 154 / Three.js r180 on ANGLE SwiftShader **software** WebGL. It verifies GLB loading and functional rendering only. Hardware-GPU behavior and performance remain **unverified**; no physical-device claim is made.

## Per-asset results

| Asset | Result and precise visual evidence | Required repair | Nonblocking scope note | Candidate tip |
|---|---|---|---|---|
| **Pentremites** | **PASS.** The five-rayed petaloid bud, longitudinal grooves, stalk, and open brachioles read across `qa-contact-sheet.png` and `runtime-contact-sheet.png`; top, clay, silhouette, and runtime views show clear radial structure and connected parts. | None. | The nominal scale, color, exact brachiole count, and simplified pod are teaching-art choices. Two smooth-face prompts (stalk, brachioles) were inspected and accepted as deliberate soft secondary surfaces around a faceted body. | `79db273e561ff145e1c3e092f2153f9f957ad973` |
| **Schizoneura** | **PASS.** Paired sheaths and a jointed axis are legible in the neutral top and oblique views. Front/side views confirm the intended shallow specimen relief; the slab stays secondary. | None. | The paired fans simplify a more varied fused-leaf sheath arrangement. Keep the existing inspiration/generalization label; this is not a species-exact whorl or specimen reconstruction. One smooth-face prompt was reviewed and accepted. | `9fc2fec2717ae798be984c3e1115d546004f239c` |
| **Tombolo** | **PASS.** The mainland, low sediment neck, offshore island, and lower shore margins read in hero/reverse/top and exact-GLB runtime views. The broad relief works as a small coastal-process teaching tile. | None. | Nominal scale and layout are illustrative, not a mapped or measured site. One smooth-face prompt was reviewed and accepted as continuous landform shading. | `227259bd9e9579192936f75ade88cb021de6ebf0` |
| **Entobia sponge-boring network** | **PASS.** The cut carbonate block shows a connected chamber-and-gallery network rather than unrelated surface pits. Top, hero/reverse, gray, and runtime views preserve the openings and connections. | None. | The section is interpretive and makes no producer, locality, or specimen claim. Editable source-only cutters remain in the Blend and are excluded from the single exported host mesh, as intended. | `c59f4813bbdd6ecdfbd6ca2085a867577aaa59ac` |

## Exact files and technical evidence

| Asset | Editable Blend SHA-256 | Exact GLB SHA-256 | GLB bytes / triangles |
|---|---|---|---:|
| Pentremites | `fe767ff636ed67c2fada0d3de94ba2acbed7dbe580bb43ac4941a68dbbf486cf` | `59a5ffb6a3329f099826f138848ed7b85e296b88fcb50a9d304335b7a865a28f` | 264,756 / 6,850 |
| Schizoneura | `8dbde9b5f52887101afc700d7c0265d2f01cb5717c77baacf6880acfee420170` | `26db0627566dbc6743b35e7591c15bf2766346bd036f950e462ccae32272f3da` | 65,572 / 3,200 |
| Tombolo | `ce67704b8537918e73703cdebf9198d04343403cc244f2ae125278f3040d8778` | `defec50fe617220529ed6fca54e08956585debc35acbc48555c3d4e0fb3bc0cb` | 160,500 / 8,832 |
| Entobia sponge-boring network | `d71a7ff5752534d55cbf839f7e658da43a3531cb0c65510185a589c3315a02e8` | `9565569dae4d8e591408e9e19babd9505f2a04b4bb0d7d499ca0c639f4a727bf` | 117,952 / 2,042 |

Read-only Blender 4.3.2 opens succeeded for all four Blend files. Source-export reports bind the exact Blend and GLB hashes, show matching triangle totals and `0.0 m` maximum bound error. Khronos validator reports are pinned to the exact GLBs with zero errors and warnings. The eight fixed stills and their file hashes match each `view-manifest.json`; each manifest has zero turntable frames. Runtime manifests and all image hashes also match; the runtime reports reference the same GLB SHA as each handoff.

The two existing serial semantic rebuild reports for each asset both return `pass`, with the same semantic digest as the delivered GLB. These are the handoff’s pinned runner outputs; this review checked their evidence and did not launch another build or repeat the browser render.

## Bounded factual scope

- **Pentremites:** the University of Kentucky Geological Survey describes the five ambulacra/food grooves, brachioles, theca, and stem that inform this broad teaching form. Species-level shape and anatomy require more specific evidence, so no exact species claim is accepted here. [Source](https://www.uky.edu/KGS/fossils/fossil-of-the-month_2023-07_pentremites.php)
- **Schizoneura:** the peer-reviewed reappraisal discusses leaf-base morphology and fusion as genus-diagnostic features. The candidate’s paired-fan layout is therefore treated as an explicit simplification, not a specimen-faithful diagnostic. [Source](https://doi.org/10.1080/03115518.2013.764693)
- **Tombolo:** the National Park Service describes a tombolo as sediment connecting an offshore island or sea stack to the mainland; the model’s connecting neck expresses that broad relationship without claiming a real location. [Source](https://www.nps.gov/articles/sandy-coast-landforms.htm)
- **Entobia:** Tapanila’s paleontological article describes interconnected chambers and galleries. The model communicates that trace structure but names no maker. [Source](https://pubs.geoscienceworld.org/paleosoc/jpaleontol/article/80/4/760/139588/DEVONIAN-ENTOBIA-BORINGS-FROM-NEVADA-WITH-A)

## Evidence and boundaries

- Source handoff: `HANDOFF.md` SHA-256 `5abe0aa574ba1e6a53e54a9ea01159bf481a589d224beadd18cb282c46c39306`.
- `final-handoff.jsonl` SHA-256 `adf6520711b56b4df2695f3a67eebbf6b9c98a7b44b4dbde6a309813facb1081`; it matches `scope.json`.
- Machine-readable per-asset findings, complete candidate artifact pins, validator summaries, exact GLB/runtime identities, and rebuild digests: [`evidence/independent-qa.json`](evidence/independent-qa.json) (SHA-256 `654351e6a44165cfd470233e0ae8f06905e3c976718c2264b2429718c9e2c7e2`).
- The `.agents/skills` inventory contains animation-only guidance; this review used the repository’s prehistoric-art, low-poly art-direction, Blender pipeline, factual-review skills, and the explicit `static-stylized-v1 2026-10-18.1` contract.

No candidate model, brief, threshold, CI, permission, formal acceptance, or publication record was changed. This is a report-only branch based on the exact source handoff commit; it has not been merged.

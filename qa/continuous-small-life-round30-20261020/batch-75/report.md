# Batch 75 independent QA

Created: 2026-10-20T16:48:44.740009+00:00

Decision: ACCEPT static QA only for Parvancorina r001, glacial horn r002, and eruptive fissure r003. REVISE banded gneiss r003. All four remain evidence-incomplete and not approved for brief/publication because GPU and composed-scene evidence are not run; approval remains separate.

## Identity and integrity

- Producer commit: `64a896d4a62893f7d0f6c8276438fb95e424e518` on `candidate/small-life-batch75-concept-20261020`; worktree clean.
- Original inventory Git blob verified at base `54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c`; SHA256 `b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c`.
- All 747 source-evidence-manifest files matched current bytes and Git blobs; the same snapshot remained unchanged after QA.
- All 32 exact final 512px images, four lossless contact sheets, source/concept pixels, rights ledgers and final-GLB/brief/reference bindings were checked. All source pixels remained outside the repository.
- Each final `.blend` reopened in Blender 4.3.2; exporting the full `EXPORT` collection recreated the exact final GLB byte-for-byte. Fresh Three.js 0.180.0 parse and Khronos validation had 0 errors and 0 warnings for every final GLB.
- Two actual separate semantic rebuild executions per final revision were verified from independent run summaries, PIDs, requests/results and output hashes; cached re-use records were not counted.
- Fresh saved-source BVH review found zero nonadjacent self-intersection pairs and zero boundary/nonmanifold edges for the four final surfaces. This was corroborative evidence, not a universal static rejection rule.

## Per-asset results

### parvancorina r001: ACCEPT_STATIC_QA_ONLY
- GLB SHA256: `6d121aa830daae492b81ff6a4fd99dd491f74105c0273ecb034a907de2b4fd35`
- Counts: 10,054 triangles; 5,029 source vertices; 3 materials; 3 primitives; 758,812 GLB bytes; 0 textures.
- Visual: Top and reverse-oblique views show the shallow shield with raised transverse anchor bar and central stem; hero/clay keep the relief restrained. No eyes, legs, mouth, antennae or behavior are introduced. Matrix slab dominates the silhouette, consistent with a low fossil-form positive cast on matrix rather than a full animal reconstruction.
- Factual limits: The inspected 2017 mould reference supports a shield and raised anchor-like relief, but not settled affinity, anterior-posterior orientation, function, external minor ridges, or mobility. The asset correctly remains a fossil-form study, not an exact specimen or living organism.
- Stages: technical PASS; factual PASS; specification PASS; runtime_parse PASS; gpu NOT RUN; scene NOT RUN.

### glacial-horn r002: ACCEPT_STATIC_QA_ONLY
- GLB SHA256: `dc476400091e3a9375de913d3684cceb8a8400ea9a4af18228516899bb5ed92b`
- Counts: 1,278 triangles; 641 source vertices; 3 materials; 3 primitives; 96,748 GLB bytes; 0 textures.
- Visual: The top and oblique views show a compact pointed summit with four opposed concave faces and four convergent short ridges. Silhouette is pyramidal and roughly equant, not an elongated arête. The simplified low-poly face transitions remain readable in clay.
- Factual limits: Generic glacial-horn teaching form only. It does not assert an exact named mountain, site, date, rock type, or active glacier; no snow, trees, or water imply site identity.
- Stages: technical PASS; factual PASS; specification PASS; runtime_parse PASS; gpu NOT RUN; scene NOT RUN.

### eruptive-fissure r003: ACCEPT_STATIC_QA_ONLY
- GLB SHA256: `5c01f576cfdb26179b4002bebc0c27997f41e805cf2fb9d9075b022291f83caf`
- Counts: 3,482 triangles; 1,743 source vertices; 4 materials; 4 primitives; 238,388 GLB bytes; 0 textures.
- Visual: The hero/reverse/top and clay views show one long recessed crack linked through four low irregular spatter-lip widenings. Side/front/rear establish its low profile; no lone mature cone or stand-alone fumarole is suggested. The crack remains visible in clay and is geometry, not just a painted line.
- Factual limits: Generic static morphology informed by HVO Fissure 17 imagery, not a contemporaneous site reconstruction, temperature/height/time record, flow simulation, or dynamic lava claim. Short orthogonal views naturally occlude parts of the cavity.
- Stages: technical PASS; factual PASS; specification PASS; runtime_parse PASS; gpu NOT RUN; scene NOT RUN.

### banded-gneiss-outcrop r003: REVISE
- GLB SHA256: `ead8a0740aae860dce43f982ebb9a0ba72800b976a322c37ea18cef17630e638`
- Counts: 3,406 triangles; 1,705 source vertices; 4 materials; 4 primitives; 267,592 GLB bytes; 0 textures.
- Visual: Front/rear/side show broad coherent folded pale/dark bands across a chunky solid rock, distinct from fine BIF lamination. However hero, reversehero, and top contain conspicuous repeated sawtooth/step boundaries across the cap. The high-contrast triangular material patches read as a regular stylized pattern, not the frozen coarse angular mineral-facet treatment, and weaken the natural structure. This is a visible visual/specification defect, not a collision or factual-scope failure. Keep r003 immutable and address narrowly in a new revision; do not hide it with materials, cameras, or renderer changes.
- Factual limits: Generic coarse folded foliation only; no named locality, exact specimen, mineral percentages, protolith, pressure-temperature history, age, or geological coexistence is asserted. The top-boundary issue is visual; no specific geological false claim was observed.
- Stages: technical PASS; factual PASS; specification PASS; runtime_parse PASS; gpu NOT RUN; scene NOT RUN.

## Artifact paths

- Machine report: `/workspace/shared/lowpoly-round30-qa75/report.json`
- Raw manifest: `/workspace/shared/lowpoly-round30-qa75/raw-manifest.json`
- Integrity pre/post snapshots: `/workspace/shared/lowpoly-round30-qa75/integrity-pre.json` and `/workspace/shared/lowpoly-round30-qa75/integrity-post.json`
- Fresh GLB checks: `/workspace/shared/lowpoly-round30-qa75/fresh-parse.json`
- Blender reopen/export evidence: `/workspace/shared/lowpoly-round30-qa75/blend-reopen`
- Raw rebuild evidence: `/workspace/shared/lowpoly-round30-qa75/rebuild-evidence.json`

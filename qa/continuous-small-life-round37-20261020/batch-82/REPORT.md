# Batch82 independent local QA

Reviewed 2026-10-20T20:50:12.356969+00:00. Immutable source commit `13556c314fbf5ee1a4469fb92fc4a3fa84f1771d`.

## Outcome

- PASS: Kimberella r002, badlands-ridge-network r002, playa-basin r003.
- REVISE: stratovolcano r006, one major visual/specification defect B82-STRATO-01.
- This is local first-five-stage QA only. GPU and populated-scene stages are NOT RUN. None is formally accepted, user-approved, website-approved or publication-approved.

## Independent checks

All 797 present tracked files matched immutable Git blobs and SHA-256s; the four exact GLBs, original inventory and r001 freezes, unchanged original briefs/configs/ledgers, final delivery closures and all32 final512px frame hashes verified. Delivery briefs add artifact hash/path closure only. All32 individual final images and all four actual retained primary-reference images were personally opened. Each lossless contact-sheet cell matches its original512px frame exactly.

All four saved Blender sources were freshly reopened read-only and exported in new processes. All four reexports are byte-identical and semantically identical to their delivered GLBs. Fresh project checks, Khronos default-severity validation and Three0.180.0 parsing pass. Each source has zero detected boundary/nonmanifold edges, duplicate triangles or nonadjacent BVH intersection pairs. These audits do not prove exhaustive surface correctness.

Both existing real semantic-rebuild jobs per asset were independently traced through different request/result directories, distinct PIDs, actual intervals, complete output hashes and Blender stdout; fresh semantic comparisons pass. These are independently rechecked maker runs, not eight new generator executions.

## Seven stages

| Asset | Technical | Visual | Factual | Specification | Runtime parse | GPU | Scene |
|---|---|---|---|---|---|---|---|
| kimberella r002 | pass | pass | pass | pass | pass | not_run | not_run |
| badlands-ridge-network r002 | pass | pass | pass | pass | pass | not_run | not_run |
| playa-basin r003 | pass | pass | pass | pass | pass | not_run | not_run |
| stratovolcano r006 | pass | fail | pass | fail | pass | not_run | not_run |

## Measurements

| Asset | Triangles | GLB bytes | Authored/evaluated vertices | Exported POSITION vertices | Materials/primitives |
|---|---:|---:|---:|---:|---:|
| kimberella | 12712 | 963148 | 6358/6358 | 36818 | 3/3 |
| badlands-ridge-network | 12464 | 945048 | 6234/6234 | 36126 | 3/3 |
| playa-basin | 2560 | 137436 | 1282/1282 | 4952 | 3/3 |
| stratovolcano | 2496 | 187952 | 1250/1250 | 7105 | 2/2 |

All are texture-free and below the frozen14,000-triangle /1,000,000-byte /6-material /30-primitive ceilings. Measured Blender XYZ extents and Y-up GLB extents are recorded separately in JSON. Badlands height99.589775m versus nominal75m is disclosed, not treated as measured site error: dimensions were explicitly illustrative and no numeric tolerance was frozen.

## Per-asset reasoning

### Kimberella: PASS within fossil-specimen scope
The elongate shallow negative mould, broader rounded end, narrower truncated region, smooth central area and narrow marginal transverse frill survive top, both obliques and independent top clay. No eyes, shell, limbs or settled muscular-foot claim is introduced. The slab silhouette is not the taxon test. Planning inventory was provisional and suggested a domed cover; the original premodel freeze explicitly made the supported negative-impression choice before modeling. Do not relabel this as a living mollusc or a replica of P49391. Primary paper Fig2 pixels were not inspected; it supplies contextual text/caption only.

### Badlands ridge network: PASS
Top, hero and gray show a coherent erosional mass with joined collector, unequal primary branches, smaller tributaries and intervening narrow divides. It is not isolated spires, a regular waffle or merely painted channels. Some fine sampling serration is visible along sharp channel margins, but no material depth conflict or disconnected geometry is observed and the required network remains readable. No new universal irregularity rule is imposed.

### Playa basin: PASS
A broad nearly planar quiet floor, gentle inward margin and continuous low irregular rim remain visible in color, gray and independent top clay. Its shallow side profiles match a basin rather than a deep crater. The fixed underside is closed and does not visibly cross the floor. The dry-state depiction does not assert that playas never contain ephemeral water.

### Stratovolcano: REVISE, B82-STRATO-01
The steep concave primary cone, broad skirt and small summit vent are correct. But the original inventory and r001 design require integrated nested flank architecture and uneven branching/merging gullies. Exact hero/clay/front are dominated by smooth sectors; top/rear remain broad radial wedge faces. The independent alternate-key512px clay makes shallow buttresses easier to see but does not recover a readable branching hierarchy. The problem is middle-scale readability against the original frozen brief, not an invented ban on repetition and not a demand for an exact Iliamna replica. Generic factual category/uncertainty remains acceptable; visual and specification stages fail.

**Repair:** Preserve the primary profile, vent, scale and original scope. Build visible differently sized nested ridges/gullies with branch junctions and terminations, keeping quiet faces where useful. Do not conceal the deficiency with random noise, palette patches, renderer/camera changes or depth tricks. First run focused matched hero/reversehero/top/alternate-key clay. A selected new revision needs complete exact-bound final lifecycle and targeted difference/regression review. Preserve r006 and all earlier evidence.

## Provenance and remaining limits

Observed ImageGen invocation16:54:16.696970UTC and return16:56:02.922694UTC, actual retained concept pixels and per-asset inspections precede immutable freezes16:56:37–16:56:43UTC and recorded builds. Original freeze documents are unchanged. Provider internal generation ID/time and exact authoring-start instant are not exposed; no filesystem mtime inference was used. Supplemental concept validators are valid but evidence_complete=false for those unknown instants. This report does not silently turn incomplete receipt history into formal acceptance.

Source and generated geometry/GLBs were never modified. New evidence is compact and isolated. No publication action taken.

## Source links

- [KIM-P49391](https://www.ediacaran.org/kimberella.html): Actual retained301x406 P49391 pixels opened; central elongate smooth region and narrow grooved margins, unequal ends and preservation damage observed. Not a replica and no scan copied.
- [EVANS2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7934905/): Primary representative-taxa text read through indexed article; Fig2 caption verified through https://pubmed.ncbi.nlm.nih.gov/33622124/. PMC direct page showed browser check, not bypassed. Contextual figured fossils differ from P49391; Fig2 pixels not claimed inspected. Anatomy/affinity uncertainty preserved.
- [NPS-BADL](https://npgallery.nps.gov/AssetDetail/57d69301-f084-40ee-a254-80c7a3e74bd6): Actual retained1399x787 field photograph inspected; incised slopes, unequal divides, foreland channel junctions observed. Background mesas/vegetation not required for generic network.
- [NPS-PLAYA](https://www.nps.gov/media/photo/gallery-item.htm?gid=0BFD7C36-A61A-4405-95DA-F95E85F133EA&id=6ecde70c-94fb-4fb0-97da-3edcc230648f&pg=0): Actual retained640x480 dry-playa photo inspected. Broad pale flat floor and subtly rising margins, not a high crater wall. Gallery tool body sparse, retained pixels checked by hash.
- [NPS-ARID](https://www.nps.gov/subjects/geology/arid-landforms.htm): Primary text directly read: water erosion in arid terrain and shallow short-lived lakes in outletless, very flat basins. Supports process form, not specific dimensions.
- [NPS-COMPOSITE](https://www.nps.gov/articles/000/composite-volcanoes.htm): Primary Introduction, Overall Description and Craters/Vents read plus actual retained1300x864 Iliamna photo. Concave steeper-top cone, common summit vent and erosional flanks supported. Photo snow obscures rock; no precise site, snow-free geology or orderly layered construction claimed.

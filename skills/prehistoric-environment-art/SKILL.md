---
name: prehistoric-environment-art
description: Create evidence-informed prehistoric environment assets and review their temporal, botanical, geological, and educational claims. Use for prehistoric lowpoly props or habitats, not modern landscaping or animal anatomy.
---

# Prehistoric Environment Art

Make original, recognizable environment assets while keeping the distinction between scientific evidence and artistic choices visible. A convincing prehistoric mood does not prove a particular species, place, or time.

## Read only what the task needs

- For this repository's first ten assets, read [asset-briefs.json](references/asset-briefs.json). Its target dimensions and simplified forms are art-direction starting points, not fossil measurements.
- For museum context and the scientific boundaries, read [museum-research.md](references/museum-research.md). A [Simplified Chinese supplement](references/museum-research.zh-CN.md) is available.
- Resolve the source IDs in those briefs through [sources.json](references/sources.json). Check current primary museum, university, specimen, or research sources before expanding a claim.

The first pack is a specific ten-category assignment, not a requirement for every future project. Later work should follow its own requested subjects, period, and location. For whether to revise those originals, consult the [evidence-based first-ten triage](../../docs/case-studies/lightweight-triceratops.md#first-ten-triage): prioritize conifer, fern and arch structure; retain and reassess the other seven. This is a recommendation, not authorization to remake or replace a batch.

Use [asset-factual-review](../asset-factual-review/SKILL.md) for feature-by-feature evidence decisions, especially animal anatomy outside this Skill's scope. Follow the [standardized pipeline](../blender-lowpoly-pipeline/references/standardized-pipeline.md) for immutable candidates and fresh independent review. Historical first-pack approvals do not automatically apply to later revisions or a new surface style.

## Establish the claim before the mesh

For each asset record:
1. A distinct object category and identifying structure.
2. Intended period, region or biome, including whether these are merely broad design contexts.
3. Source-supported features, artistic decisions, and unknowns separately.
4. Whether it is a broad concept, teaching model, or a reconstruction of an identified specimen/site.

Do not upgrade a concept to a scientific reconstruction without a supported taxon or landform, locality/stratum, scale, and evidence for the restored parts. A modern botanical analogue helps explain shape; it does not establish that a modern species existed unchanged in deep time.

## Morphology that must survive simplification

- Conifer: main axis and lateral branch structure, with readable crown gaps. Do not reduce every tree to stacked cones.
- Cycad-inspired plant: stout stem and stiff pinnate crown. Do not turn it into a palm, or combine cycad and bennettitalean reproductive structures without evidence.
- Ground fern: curved frond axes, pinnae, and limited unfurling growth. Ferns are not seed ferns; flowers/seeds are not fern ornaments.
- Horsetail: segmented stems and whorled side branches. Do not scale a modern small horsetail into a Carboniferous Calamites reconstruction.
- Arborescent lycopsid: leaf-cushion pattern and appropriate branching, distinct from conifer branches. A mature branching crown does not describe every life stage.
- Uprooted log: natural breakage and roots appropriate to its plant group. The first pack's root plate belongs to a seed-plant concept, not a lycopsid.
- Sedimentary outcrop: coherent bedding and meaningful variation in layer resistance.
- Natural arch: through-opening, plausible solid supports, and thickness. The rock's deposition age is not the age of its present eroded shape.
- Egg nest: identify the limited fossil inspiration. Do not assign the nest to an animal merely because it is nearby.
- Track patch: distinguish a fresh depression, an undertrack, and a fossil cast. Three toes alone do not identify a named dinosaur.

## Keep the package scientifically honest

The first pack contains a Carboniferous tree, Mesozoic-inspired plants, teaching traces, and time-neutral geology concepts. Show them together only as a clearly labeled cross-period asset catalogue. A habitat reconstruction requires compatibility at the period, place, substrate, and climate levels.

For the current museum:
- The legacy gobi ID means an Iren Dabasu vegetated fluvial plain, not today's dune desert.
- Kayenta-inspired scenes are seasonal river/floodplain environments; today's exposed canyon is not a snapshot of their Jurassic topography.
- Keep Carboniferous lycopsids in their own theme.
- Do not use the pack's plants to fill the mammoth steppe by default.
- The existing museum uses panoramas, PBR ground and world-space ecology. A lowpoly pack is not automatically a style-matched production replacement.

Use the model card wording “evidence-informed stylized concept” or “teaching model” unless stronger reconstruction evidence exists. List colors, exact layout, simplified leaf counts, weathering, and unmeasured dimensions as artistic choices.

## Build and review

For a new concept-led subject, follow the [integrated concept-first route](../concept-guided-lowpoly/SKILL.md) before authoring: generate and inspect the concept, resolve ambiguous views, then freeze the structural brief. Keep its artistic silhouette/palette choices separate from the evidence claims above. Reuse the retained brief for export repairs; no retrospective concept is proof of earlier design intent.

Author original geometry from the structural brief. Viewing a reference is not a reason to download, copy, or lightly alter a third-party model. Do not bundle reference images, institutional text, or source code as if they were original assets.

Review:
- For silhouette-led categories, a monochrome silhouette communicates identity without relying on color. For nests and footprint slabs, inspect neutral-gray top views and identifying internal relief instead; their outer silhouette is not an identification gate.
- Geometry, branching, negative spaces and surface structure express the subject.
- Names, previews, gallery grouping and metadata make no stronger scientific claim than the brief.
- Coordinate system, units, origin, intended dimensions and license are explicit.
- Independently loaded assets render correctly from front, rear, top and three-quarter views.
- Counts and performance are measured after export; preserve recognizability when deriving LOD.
- Any museum integration is separately tested for scale, visibility, style and selected-theme loading.

Keep the palette calm and the subject readable for the museum's young audience. Nest and deadwood props need no danger narrative.

Use this repository's declared asset license and attribution files. Scientific reference links are citations, not imported asset licenses or institutional endorsements.


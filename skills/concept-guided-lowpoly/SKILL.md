---
name: concept-guided-lowpoly
description: Translate genuine ImageGen design concepts into editable volumetric low-poly Blender assets, exact exported-GLB proof renders, and an auditable study bundle. Use when concept-first production or refinement is requested; this supplements existing asset QA and grants no batch or publication approval.
---

# Concept-guided low-poly studies

Use ImageGen to establish the intended shape and visual language **before constructing the model**. Then author real geometry, inspect the exact exported GLB, and report the visible differences. This is a provisional method learned from three examples, not an automatic image-to-mesh reconstruction system.

For an external creature-base workflow, use [Meshy → Blender](../meshy-blender-creatures/SKILL.md). Reuse suitable retained research and design views; this concept-first module does not require generating a new concept for every external-base refinement.

## Work from a frozen design

1. Confirm subject, use/viewing role, dimensions, intended factual claims and the current experiment boundary. Use [the brief/prompt template](assets/concept-brief.template.md); keep English primary and optional bilingual asset labels. Apply [lowpoly-art-direction](../lowpoly-art-direction/SKILL.md) and [blender-lowpoly-pipeline](../blender-lowpoly-pipeline/SKILL.md) rather than replacing their contracts.
2. Generate and retain the real ImageGen output, exact prompt and generation record. Inspect its pixels before writing the modeling brief. Save original output separately from model renders; never label a source-scene render or a later illustration as a prior concept.
3. When depth, branching or anatomy is ambiguous, request compatible front/side/top concept views with the same dimensions, landmarks and palette. Check cross-view proportions and landmark counts. AI views can disagree; resolve contradictions in the brief instead of treating them as measured ground truth. Record the design decisions for hidden surfaces.
4. Translate visible structure into primary masses, secondary landmarks, negative spaces, thickness and material regions. Model a full volume; do not optimize only for one camera. Keep `.blend`, generator, configuration/seed and export settings. A concept image is not a texture/billboard substitute for volumetric work.

## Prove the exported result

Use the [production and evidence recipe](references/workflow.md) for runnable commands and the supplemental evidence format. Reuse repository export, static QA, Khronos validation and exact-GLB rendering helpers. Inspect hero and alternate-angle images from clean imports of the delivered GLB, plus structural/clay views as needed. Final thumbnails must come from that GLB, never from ImageGen. Keep original concepts visibly labeled in any comparison sheet.

Compare revisions with the same camera, framing, lighting and color management. Define a named visible improvement before adding geometry: branch curvature, cheek transition or band irregularity, for example. More triangles or render samples alone do not establish refinement. Preserve each prior revision and its evidence. Adopt a revision only when the review finds a meaningful visible benefit; retain the prior version when extra complexity does not help.

Record actual stage timings, or explicitly say unrecorded/not run. Choose budgets by deployment role; approximately 1,000,000 bytes per GLB was a soft target for this study only, excluding `.blend` and renders. Preserve identifying form before optimizing. Texture-free construction is an experiment choice, not a requirement for unrelated assets.

## Review boundary

The [three-case lesson](references/pilot-lessons.md) records what worked, remaining weaknesses and missing browser evidence. The supplemental checker verifies files, hashes, chronology attestations, exact-GLB view coverage and preview identity; it cannot judge craft, volume, scientific truth, tool authenticity or user approval. Continue using the existing candidate gate for formal approval, source/export/rebuild checks, factual review, target runtime, GPU and populated-scene evidence. Unknown or unrun stages stay unknown.

Ask the user to review the small representative set before expanding a batch or changing a style rule. Study acceptance does not authorize release or deployment. Original art, renders and prose: CC BY 4.0, Leon Made This / s010s. Executable code: MIT. Record third-party provenance and reuse rights separately; generated concepts do not establish factual accuracy or license the source material that inspired them.

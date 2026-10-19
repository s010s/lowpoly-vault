---
name: lowpoly-art-direction
description: Design and independently review original low-poly assets for animals, natural, geological, modern, futuristic, fantasy, and alien subjects. Use for shape hierarchy, proportions, portable surface detail, topology, role-based budgets, and visual acceptance; factual claims and publication need separate gates.
---

# Original Low-Poly Asset Art

Use deliberately designed planes to communicate identity, weight, material, and rhythm. Prioritize silhouette, component proportions, convincing secondary structure, and detail concentrated where it explains the object. Neither more polygons nor fewer polygons alone establishes quality. Derive budgets from viewing and deployment roles using [asset budgeting](references/asset-budgeting.md); the old first-pack triangle bands are historical starting points, not library-wide caps or industry standards.

The target is refined, coherent low-poly with a surface profile chosen for the brief. Palette-only, color-textured and textured-PBR treatments are all valid; the reviewed three-case concept study used a polished, child-friendly palette-only style. Rich original surface maps and mixed smooth/faceted shading remain compatible with other briefs. Separate geometry complexity from texture resolution, memory and material cost. Texture cannot repair a wrong outline, missing anatomy or implausible joint. The [Triceratops and environment surface study](../../docs/case-studies/lightweight-triceratops.md) records where inexpensive regional color helped, where fine relief was lost, and why three surface-heavy environment prototypes were rejected. Use its [controlled comparison checklist](../blender-lowpoly-pipeline/references/controlled-optimization.md) for new variants; its accepted byte count is an example, not a preset. Follow the [standardized pipeline](../blender-lowpoly-pipeline/references/standardized-pipeline.md) for frozen briefs, independent review and acceptance records.

For new concept-led assets, begin with [concept-guided-lowpoly](../concept-guided-lowpoly/SKILL.md): generate and inspect the actual ImageGen concept, translate it into the structural brief below, then build real geometry. Check compatible concept views when depth or anatomy is ambiguous, resolve contradictions explicitly and design unseen surfaces. A concept is aesthetic direction rather than measured geometry. Existing repairs can reuse the retained concept and brief. Its three-case lesson informs this workflow without setting universal texture, size or scientific-accuracy rules.

## Establish the brief

- Record the category, viewing distance, real or explicitly stylized scale, three identifying features, and dominant silhouette. For trace-based assets such as nests and footprint slabs, also name the identifying internal geometry.
- Write a component-and-cause brief: primary mass, secondary structure, one tertiary identifying feature, quiet region, and the reason for each important connection or interruption. State the representation scale: individual leaves, shoots, branchlet sprays, crown masses, structural panels, or assemblies. Do not accidentally mix these scales.
- Label the asset as scientific reconstruction, evidence-informed generalization, stylized environment prop, or fantasy. A child-friendly decorative fish or coral need not assert a species or specimen claim; review it against the explicitly stylized brief. Unverified species, periods, footprints, and nests must not be presented as scientific reconstructions.
- Separate the reusable asset from its presentation scene. Do not include preview lights, platforms, or cameras in asset exports.
- This first pack is an independent, consistently stylized environment library. The existing museum uses realistic distant scenery, PBR terrain, and vegetation placed at real-world coordinates. Do not claim direct replacement or visual compatibility, and do not modify the museum. Use the shared gallery to demonstrate this pack's own consistency.
- Respect the task's environment and originality boundaries. This project is cloud-only in an authorized environment. Separately authorized temporary reference inspection does not authorize reuse: isolate research files outside the original-asset tree, record license status, and do not incorporate unlicensed models, code, materials, palettes, textures, or images. See [reference lessons and reuse limits](references/reference-quality-lessons.md).

## Design the structure first

1. Block out a few dominant masses before materials. For silhouette-led objects, approve the black silhouette first. For nests and footprint slabs, approve neutral-gray top views, depressions, rims, egg placement, and other identifying internal geometry instead; a pure outer silhouette is not an identification gate for these assets. Give every object a clear direction and center of gravity, with secondary masses supporting the main form.
2. Build large, medium, and small shape rhythms rather than repeating equally sized masses. A roughly 60/30/10 visual-area relationship can be a starting point, but judge the image rather than enforcing the ratio mechanically.
3. Place edges and vertices at meaningful turns, forks, notches, leaf ridges, fractures, and bends. Each edge should improve silhouette, plane orientation, structure, or deformation behavior.
4. Keep most areas quiet; concentrate smaller facets on identifying features. Do not apply uniform vertex noise or random face colors across the entire asset.
5. Use organized asymmetry tied to weight, growth toward light, erosion, bedding, breakage, or growth direction. Each variant should change at least one major structural decision. Rotation, uniform scaling, or a new random seed alone is not a new design.
6. Resolve the middle scale before adding microdetail: branch-to-spray relationships, complete frond taper, erosion steps, functional joints, or an invented assembly system. At least one secondary identifying structure must remain apparent in neutral gray. Add geometry only for a named visible improvement; random noise and uniform subdivision do not repair missing structure.

## Organize planes by material

- **Rock:** Choose a layered, blocky, or eroded structural logic before adding a few fractures. Do not derive every rock from the same distorted icosphere.
- **Wood:** Taper trunks progressively; give branches a thickness hierarchy and growth direction. Use distinct broad planes for cuts, breaks, and bark. Avoid stacks of equal-width cylinders.
- **Plants:** Design the whole crown and the negative spaces between leaves before detailing individual leaves. Give leaves a base, axis, bend, taper, and thickness logic. Avoid identical leaves in evenly spaced gear-like arrangements.
- **Terrain:** Preserve quiet, low-frequency areas for characters and other assets. Concentrate height changes near shorelines, ridges, and slope breaks. Give seams and lower boundaries a clear purpose.
- **Water:** Establish readable shorelines, depth zones, and contact relationships before reflections. Transparency, ripples, and emission must not conceal poor shore geometry or floating objects.
- **Manufactured and futuristic objects:** Establish functional proportions, openings, assembly joints, and motion or service access. Concentrate smaller details where operation or construction warrants them, rather than covering every panel with trim.
- **Fantasy and alien forms:** Establish a coherent invented growth, support, segmentation, or assembly logic. Preserve deliberate exceptions and focal silhouettes without importing terrestrial anatomy or city-prop scale rules as defaults.

## Color and lighting

- Share one original palette within a style family or batch, using a base color and a few nearby values per material. The prehistoric pack's vegetation, wood, earth/stone, and water families are documented in [first-batch standards](references/first-batch.md); that palette is not mandatory for every future theme.
- Assign colors by structure or material region, not randomly by polygon index. Let lighting provide most shadows; avoid permanently painting a face black to fake shadow.
- Review color, grayscale, and silhouette views. Reserve the brightest or most saturated colors for intentional focal points; supporting props should not compete with the intended subject. For trace assets, judge identity from neutral-gray top views and internal relief, not the outer silhouette.
- Use the current pack's agreed palette and fixed diagnostic preview setup; [first-batch standards](references/first-batch.md) records the prehistoric pack's setup. Choose explicit per-profile geometry ceilings through [asset budgeting](references/asset-budgeting.md), not its historical tier table. Record the actual Blender version and view transform. Do not change exposure for one asset merely to make it pass review.
- Inspect volume with a neutral soft key and sufficient fill, then change the key direction to inspect plane orientation. Mood lighting is valid for presentation, but structural checks must not rely on fog, strongly colored lights, depth of field, rim lighting, or ambient occlusion to hide flaws.

## Topology and shading

- Prefer flat shading where facets are intentional. Deliberately combine smooth and flat regions where appropriate; low-poly does not require identical shading everywhere.
- Let facet direction follow form. Broad coplanar regions do not need decorative triangulation. Choose the split direction of nonplanar quads and n-gons deliberately to avoid unexpected creases after export.
- Use Decimate for cleanup or LOD, not as an art-style generator. After sculpting and decimation, recheck silhouette, facet-size hierarchy, and thin triangles. Do not deliver a one-click decimation without review.
- Inspect the actual triangulation in an export copy and retain editable source geometry. Check normals, colors, backfaces, and transparent materials in the target viewer, not only in Blender.
- Distinguish intentional open leaf surfaces from accidental holes. Double-sided materials do not repair incorrect normals, overlapping surfaces, or unusable collision geometry.
- If using palette textures, create the palette and materials yourself, and verify filtering, UV placement, and exported colors. Fewer material slots simplify consistency, but one material does not guarantee one draw call.
- For textured-PBR work, preserve editable source and bake original portable maps. Inspect UV seams/stretching, texel density, mip bleed, tangent/normal orientation, roughness response and small-scale shimmer in the exact GLB. Compare surface variants with identical geometry, normals, camera, lighting and exposure; label geometry changes as a separate experiment. See the [surface profile](../blender-lowpoly-pipeline/references/production-contract.md#textured-pbr-profile).
- Report authored and evaluated source vertices, exported POSITION-stream vertices, triangles, material/primitive counts, and visible instance counts separately. Never infer one through a fixed ratio or describe them ambiguously as "polys." Verify optional LOD switching in the actual runtime, not merely the existence of several files.

## Review and iterate

Render and inspect using the [visual acceptance checklist](references/visual-acceptance.md). Fix recognition-bearing structure and proportions first, then planes, color groups, and small details. For most assets this begins with silhouette; for nests and footprints it begins with neutral-gray top views and readable internal geometry. A polished hero image cannot compensate for a failed hard gate.

Use a fresh independent reviewer for each quality candidate. Supply the frozen brief, source ledger, exact model and full-angle evidence, not the maker's self-score or expected verdict. Record criterion-level pass/fail/unknown with locations and evidence. For factual obligations use [asset-factual-review](../asset-factual-review/SKILL.md); attractive styling does not establish species identity or regional compliance. Re-exported changes invalidate affected verdicts and require recheck.

Before extending a new style or revised workflow across a batch, freeze two or three representative quality samples with their version/hash, gray and color views, target-viewer evidence, and explicit visual decision. Technical validity and category recognition are minimum gates, not benchmark quality. Compare revisions under matching framing and lighting; record the observed weakness, structural change, and visible outcome. A score must not override a weak criterion or the user's visible objection. Adopt a revision only for a meaningful visible benefit. In the three-case comparison the user preferred R1 coral and found the other R2 differences small, so none of R2 was promoted; more detailed geometry was not an improvement verdict. Apply the original lessons in [reference-quality lessons](references/reference-quality-lessons.md), not the reference's models or recipes.

Distinguish visually verified findings, automated checks, and unverified runtime or scientific information in delivery notes. Read [primary sources and evidence limits](references/sources.md) when the reasoning behind the workflow is needed.

## Catalog preview experiments

Choose a preview method from measured visual and resource tradeoffs. Fit each object's projected bounds using a shared angle, light, color-management and occupancy rule; do not rescale source geometry to force identical framing. Compare static images, 12–16-view sheets and the actual GLB on representative tall, wide and arched shapes. Report exact encoded bytes, decoded pixel budgets and the conditions of any timing. CPU decode/parse proxies are not browser/GPU performance. Inspect alpha and shadows on both light and dark surfaces; an apparently transparent shadow is not automatically theme-correct. Keep experiments outside release assets until reviewed. The original cloud-only 2026-10-16 experiment is documented in `experiments/preview-turntable-v3/README.md`; it recommended static cards plus on-demand GLB, not production sprite integration.

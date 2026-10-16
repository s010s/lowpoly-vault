---
name: lowpoly-art-direction
description: Design and visually review original low-poly environment assets in Blender, including silhouettes, shape rhythm, palettes, facet topology, and consistent asset families. Use for prehistoric museum environments and adaptable fantasy scenery; this skill does not establish paleontological accuracy or authorize publication.
---

# Original Low-Poly Environment Art

Use a small number of deliberately designed planes to communicate identity, weight, material, and rhythm. Reducing polygon count alone is not the goal. Set budgets for the project's runtime, viewing distance, and style. Numerical targets here are starting conventions for this project, not industry standards.

## Establish the brief

- Record the category, viewing distance, real or explicitly stylized scale, three identifying features, and dominant silhouette. For trace-based assets such as nests and footprint slabs, also name the identifying internal geometry.
- Label the asset as scientific reconstruction, evidence-informed generalization, stylized environment prop, or fantasy. Unverified species, periods, footprints, and nests must not be presented as scientific reconstructions.
- Separate the reusable asset from its presentation scene. Do not include preview lights, platforms, or cameras in asset exports.
- This first pack is an independent, consistently stylized environment library. The existing museum uses realistic distant scenery, PBR terrain, and vegetation placed at real-world coordinates. Do not claim direct replacement or visual compatibility, and do not modify the museum. Use the shared gallery to demonstrate this pack's own consistency.
- Respect the task's environment and originality boundaries. This project is cloud-only in an authorized environment. Study methods from public tutorials; do not download, copy, or repackage third-party models, textures, palettes, or scenes.

## Design the structure first

1. Block out a few dominant masses before materials. For silhouette-led objects, approve the black silhouette first. For nests and footprint slabs, approve neutral-gray top views, depressions, rims, egg placement, and other identifying internal geometry instead; a pure outer silhouette is not an identification gate for these assets. Give every object a clear direction and center of gravity, with secondary masses supporting the main form.
2. Build large, medium, and small shape rhythms rather than repeating equally sized masses. A roughly 60/30/10 visual-area relationship can be a starting point, but judge the image rather than enforcing the ratio mechanically.
3. Place edges and vertices at meaningful turns, forks, notches, leaf ridges, fractures, and bends. Each edge should improve silhouette, plane orientation, structure, or deformation behavior.
4. Keep most areas quiet; concentrate smaller facets on identifying features. Do not apply uniform vertex noise or random face colors across the entire asset.
5. Use organized asymmetry tied to weight, growth toward light, erosion, bedding, breakage, or growth direction. Each variant should change at least one major structural decision. Rotation, uniform scaling, or a new random seed alone is not a new design.

## Organize planes by material

- **Rock:** Choose a layered, blocky, or eroded structural logic before adding a few fractures. Do not derive every rock from the same distorted icosphere.
- **Wood:** Taper trunks progressively; give branches a thickness hierarchy and growth direction. Use distinct broad planes for cuts, breaks, and bark. Avoid stacks of equal-width cylinders.
- **Plants:** Design the whole crown and the negative spaces between leaves before detailing individual leaves. Give leaves a base, axis, bend, taper, and thickness logic. Avoid identical leaves in evenly spaced gear-like arrangements.
- **Terrain:** Preserve quiet, low-frequency areas for characters and other assets. Concentrate height changes near shorelines, ridges, and slope breaks. Give seams and lower boundaries a clear purpose.
- **Water:** Establish readable shorelines, depth zones, and contact relationships before reflections. Transparency, ripples, and emission must not conceal poor shore geometry or floating objects.

## Color and lighting

- Share one original palette across the batch. Group colors into vegetation, wood, earth/stone, and water families, using a base color and a few nearby values per material. See [first-batch standards](references/first-batch.md).
- Assign colors by structure or material region, not randomly by polygon index. Let lighting provide most shadows; avoid permanently painting a face black to fake shadow.
- Review color, grayscale, and silhouette views. Reserve the brightest or most saturated colors for intentional focal points; environment props should usually support the animal exhibits. For trace assets, judge identity from neutral-gray top views and internal relief, not the outer silhouette.
- Follow the fixed palette, triangle tiers, and preview setup in the [first-batch standards](references/first-batch.md). Record the actual Blender version and view transform. Do not change exposure for one asset merely to make it pass review.
- Inspect volume with a neutral soft key and sufficient fill, then change the key direction to inspect plane orientation. Mood lighting is valid for presentation, but structural checks must not rely on fog, strongly colored lights, depth of field, rim lighting, or ambient occlusion to hide flaws.

## Topology and shading

- Prefer flat shading where facets are intentional. Deliberately combine smooth and flat regions where appropriate; low-poly does not require identical shading everywhere.
- Let facet direction follow form. Broad coplanar regions do not need decorative triangulation. Choose the split direction of nonplanar quads and n-gons deliberately to avoid unexpected creases after export.
- Use Decimate for cleanup or LOD, not as an art-style generator. After sculpting and decimation, recheck silhouette, facet-size hierarchy, and thin triangles. Do not deliver a one-click decimation without review.
- Inspect the actual triangulation in an export copy and retain editable source geometry. Check normals, colors, backfaces, and transparent materials in the target viewer, not only in Blender.
- Distinguish intentional open leaf surfaces from accidental holes. Double-sided materials do not repair incorrect normals, overlapping surfaces, or unusable collision geometry.
- If using palette textures, create the palette and materials yourself, and verify filtering, UV placement, and exported colors. Fewer material slots simplify consistency, but one material does not guarantee one draw call.

## Review and iterate

Render and inspect using the [visual acceptance checklist](references/visual-acceptance.md). Fix recognition-bearing structure and proportions first, then planes, color groups, and small details. For most assets this begins with silhouette; for nests and footprints it begins with neutral-gray top views and readable internal geometry. A polished hero image cannot compensate for a failed hard gate.

Distinguish visually verified findings, automated checks, and unverified runtime or scientific information in delivery notes. Read [primary sources and evidence limits](references/sources.md) when the reasoning behind the workflow is needed.

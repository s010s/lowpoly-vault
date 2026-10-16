# Visual Acceptance Checklist

These are working gates for this project, not universal objective measures of artistic quality. Automated checks establish only what they test. Visual conclusions require opening the actual images.

## Minimum evidence per asset

1. A front three-quarter view and an opposite-side three-quarter view under the shared lighting setup.
2. Relevant front, side, and top orthographic views, with scale. Foliage clusters, nests, footprint slabs, and shorelines require top views.
3. A 128×128 black silhouette with the asset occupying about 80% of the frame, without a platform, fog, cast shadow, or outline. For nests and footprint slabs, use this only to inspect outer mass and proportions, not to identify the subject.
4. A neutral-gray material view with textures and face colors removed, plus at least one alternate key-light direction. For nests and footprint slabs, a neutral-gray top view must reveal the identifying internal geometry: depression, rim, egg placement, or footprint relief.
5. The export copy's actual triangulated wireframe and close-ups of its most complex forks, folds, and thin surfaces.
6. A screenshot after reimporting the target format or opening it in the target viewer. Mark this unverified when it cannot be done.
7. For a quality sample, matched before/after views and at least one secondary identifying structure that survives removal of color. Record the actual asset version/hash; do not use an older contact-sheet cell to assess a newer revision.

Add two contact sheets per batch: one with consistent individual framing for style comparisons, and one arranged at true relative scale. Automatically normalized thumbnails cannot prove scale consistency.

## Five hard gates

- **Recognition:** For silhouette-led objects, the silhouette must communicate the category and at least one distinctive feature without depending primarily on color, text, or a decorative platform. Review hidden structural features, flattened crowns, and unreadable shorelines. For trace-based assets such as nests and footprint slabs, recognition comes from neutral-gray top views and internal geometric details instead. A nest may need its bowl, rim, and eggs; a footprint slab needs readable depressions and toe relief. Their outer silhouette alone is not an identification requirement, and failure of that test alone must not trigger rework.
- **Structural completeness:** Every intended viewing angle is free of accidental spikes, dark cracks, floating joints, obvious intersections, collapses, or paper-thin shortcuts that work only from the hero camera.
- **Stable planes and lighting:** Moving the light does not reveal unexplained fragmentation, star-shaped dents, or abrupt shading changes. Triangulation and reimport introduce no significant unintended shading creases.
- **Family consistency:** Neighboring assets have compatible exaggeration, facet size, saturation, and detail density. Variants of one category must differ structurally.
- **Honest context:** Unverified species, periods, tracks, nests, and behavior must not be labeled scientific reconstructions. Keep fantasy variants separate from realistic museum reconstructions.

## Suggested art score: five criteria, 0–4 each

0 = unfinished; 1 = obvious problems; 2 = usable but generic; 3 = intentional and consistent; 4 = strong identity, rhythm, and finish.

| Criterion | Inspect | Typical rework signal |
|---|---|---|
| Silhouette, proportions, and structural readability | Identity, dominant direction, weight, and negative space. For nests and footprints, assess neutral-gray top-view structure rather than outer-silhouette identity. | All rocks resemble one sphere; all trees resemble lollipops; footprint relief or nest cavities disappear in gray |
| Planes and rhythm | Large/medium/small hierarchy, broad quiet areas, meaningful local turns | Uniform all-over noise; equally sized triangular fragments without structural purpose |
| Color groups and material | Clear material families, grayscale separation, controlled emphasis | Random face colors, competing candy saturation, permanent painted black shadows |
| Detail and craft | Growth/fracture/erosion logic, correct contact, clean export | Equal spacing, equal-width branching, floating parts, sliver triangles, normal errors |
| Family reuse | Structural variant differences, consistent scale and design language, viewing-angle coverage | Recolors treated as new assets; single-angle construction; inseparable display platforms |

Current recommendation: at least 3 in every criterion and at least 16/20 overall, with all five hard gates passed. Give a one-sentence reason for each score. Technical validity and recognizable category are minimum usability gates; benchmark quality additionally requires convincing secondary structure, component proportions, and concentrated, purposeful detail. Neither the total score nor an automated pass overrides a weak criterion or the user's visible objection. Freeze accepted samples before using them as a quality reference, without copying their silhouettes.

## Budget and viewing-profile acceptance

Follow [asset budgeting](asset-budgeting.md) for separate source/export vertex counts, triangles, materials/primitives, repetition, and viewing assumptions. Review at intended small, medium, and close projected sizes and in the intended population; a normalized thumbnail or an isolated GLB below a cap is insufficient. Optional LODs must actually switch in the target runtime, with transition and identity checks. Mark unavailable device or scene tests unverified rather than inferring performance from counts.

For every structural revision, record the observed weakness, the change, and the expected visible outcome, then compare under matching framing and lighting. "More triangles," "higher resolution," and "more realistic" are not sufficient explanations. Inspect topology spending at bends, joints, terminations, and negative spaces before adding detail elsewhere. Preserve the neutral-gray top-view/internal-relief exception for nests and footprints.

## Diagnosing generic procedural forms

| Symptom | Common cause | Correction |
|---|---|---|
| Rounded potato rock | A sphere with uniform random displacement substitutes for construction | Establish the supporting base, long axis, two main fracture planes, and one notch first |
| Shattered-glass rock | Excessive decimation or too many small triangles | Enlarge key planes manually; remove fragments that do not improve silhouette |
| Fan-like palm or cycad | Identical leaf lengths, angles, and pitch | Establish crown layers, then let a few leaves extend, droop, or be absent |
| Green-comb fern | Coplanar, equally spaced leaves with identical curves | Give the frond a clear curve, depth layers, and gradually changing leaflets |
| Stacked-cone tree | Similar tier widths/heights and a rigid centerline | Vary crown overlap and spacing; introduce a deliberate offset or opening |
| Pipe-like fallen log | Constant-width cylinder, regular break, no root structure | Taper cross-sections, add a main bend, and use a few hierarchical broken branches and ends |
| Noise-filter terrain | High-frequency displacement covers all usable areas | Preserve quiet platforms and concentrate detail at landform boundaries |
| Incoherent asset family | Each asset independently chooses colors, density, cameras, and lighting | Compare under the same palette, test lighting, and visual facet density |

## Useful automated checks, not substitutes for inspection

- Record authored source vertices, evaluated source vertices, exported POSITION-stream vertices, exported triangles, used materials, primitives, bounding box, asset and mesh instance counts, visible/hidden objects, texture references, and file size. State counting scopes using [asset budgeting](asset-budgeting.md).
- Check NaN/Inf coordinates, zero-area faces, loose vertices, duplicate faces, negative scale, unintended nonmanifold edges, and missing external textures.
- Flag unusual triangle aspect ratios for visual review. Long narrow leaf faces may be intentional; do not repair them indiscriminately.
- Compare bounds, counts, colors, and normals before and after export/reimport. A file opening successfully does not establish artistic acceptance.

## Review record template

Asset ID:
Source file / export file:
Review date / Blender version / target viewer:
Dimensions / authored and evaluated vertices / exported POSITION vertices / triangles:
Used materials / primitives / asset and mesh instances:
Viewing profile / projected size / population / runtime measurements:
Previews actually inspected:
Frozen asset version/hash:
Recognition method: silhouette-led / neutral-gray top-view internal geometry
Observed weakness / structural change / expected and observed visible outcome:
Five hard gates:
Five scores and reasons:
Highest-priority 1–3 corrections:
Scientific context and unverified items:
Decision: pass / rework / conditional pass (state limitations)

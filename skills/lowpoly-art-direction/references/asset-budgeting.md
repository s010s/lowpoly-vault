# Role-Based Asset Budgeting

Choose a budget for an asset's viewing and deployment role, not its theme or a size noun. The same framework applies to natural, geological, modern, futuristic, fantasy, and alien environments. A close-inspected small object may need more resolved form than a distant mountain; repeated groundcover may dominate a scene more than one focal object.

## Correct units and historical context

At the inspected [reference commit](https://github.com/RHS059/low_poly_items/tree/2c3cf681cce1cdbcb8f0c7297120422ab178ab90), **999 / 5,000 / 10,000 are ceilings on both source and exported vertices**, not triangle targets or quotas. The reference applies them to handheld, person-sized-or-smaller, and car-sized-or-larger classes: see its [budget table](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/README.md#L35-L43), [export accounting](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/tools/build.py#L138-L141), and [validation](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/tools/validate.py#L43-L56). These are that collection's rules, not a universal low-poly standard. Do not import its city-oriented scale classes into this library.

Our old 250–2,600 **exported-triangle** bands describe the first prehistoric modeling pass only. They are historical starting points, not library-wide ceilings. Never compare a triangle count directly with a vertex cap: the study's frozen fern had 2,418 triangles and 6,784 exported POSITION-stream vertices. Those snapshot counts illustrate different units, not a failure under a cap we have not adopted.

## Define one usage profile before freezing limits

1. **Runtime:** renderer/version, representative device, framebuffer size, target frame time, lighting/shadow passes, and isolated gallery versus populated environment. A gallery pass does not prove scene performance.
2. **View envelope:** world bounds, closest supported and typical camera distances, field of view or orthographic span, projected pixel extent, and whether close inspection is supported. Orthographic coverage depends on span, not distance alone.
3. **Repetition:** normal and stress-case visible asset copies, clustering, culling, and occlusion assumptions. Count submitted copies, not just distinct files in the catalog.
4. **Visual obligations:** name the silhouette breaks, negative spaces, secondary structures, proportions, and interaction/recognition details that must survive. For nests and footprint slabs, preserve identifying internal relief.
5. **Representation:** decide whether one representation is sufficient, or whether environmental, close-inspection, far, or LOD variants solve a real need. Do not demand a fixed number of LODs.
6. **Independent limits and proof:** propose separate vertex, triangle, material/primitive, texture-memory, file-size, and shader/overdraw limits. Freeze numerical ceilings only after representative samples pass visual and populated-runtime tests; record measurements and unresolved tests.

## Soft study targets are not production caps

The three-case concept-first study used roughly 1,000,000 bytes per GLB as a soft delivery target, excluding editable `.blend` sources, renders and archives. It retained identifying structure rather than degrading geometry to meet that number. Its R1 files were 18,816, 240,024 and 142,420 bytes; this is observed evidence, not a budget for unrelated assets. Palette-only construction was a study choice, not a prohibition on textures.

R2 coral increased from 3,000 to 4,200 triangles but the user preferred R1. R2 fish gained triangles while its GLB shrank. Neither count direction establishes quality or runtime performance; use matched visual review and measured deployment costs. The 41-primitive fish and double-sided materials remain runtime advisories despite small files and zero Khronos warnings. See [the case record](../../concept-guided-lowpoly/references/pilot-lessons.md).

## Report explicit counts

Use these field meanings consistently, or declare a different convention before comparing reports. Stored geometry and scene-instance workload are different measurements. Record per-representation/LOD counts as well as any whole-file total; do not charge every stored LOD as simultaneously active in a scene estimate.

| Metric | Counting convention |
|---|---|
| Authored source vertices | Sum vertices in distinct included authoring mesh datablocks before modifiers. State exclusions. Count reused mesh instances separately; do not merge vertices merely because coordinates match. |
| Evaluated source vertices | Sum vertices in distinct included evaluated geometry variants after modifiers, at the exported state. Object-specific modifiers can create separate variants of a shared source mesh. Declare realization/deformation settings and report any per-instance-expanded total separately. |
| Exported POSITION-stream vertices | For each exported mesh definition, sum the POSITION accessor count of every primitive. Count each primitive occurrence even when it references a shared accessor; do not multiply by scene nodes or instances here. This is a per-primitive stream sum, not a count of unique geometric positions. |
| Unique POSITION accessor elements | Optional separate sum over distinct POSITION accessor IDs. This is not the same as the stream sum, geometric welding, or necessarily unique storage bytes when accessors share buffers. Report actual buffer/file bytes separately. |
| Exported triangles | Sum by primitive mode in each mesh definition. For TRIANGLES, validated index count divided by three, or POSITION count divided by three if unindexed. For TRIANGLE_STRIP/FAN, use max(element count minus two, zero), identifying any separate nondegenerate count. Points/lines are not triangles. Reject malformed data instead of silently rounding. |
| Materials and primitives | Report distinct material indices actually referenced, any default/unassigned material, and the number of primitives in mesh definitions. A material count is not a draw-call measurement; report runtime submissions separately. |
| Instances and workload | Report visible asset copies plus submitted mesh-node/GPU-instance multiplicities by active representation or LOD. Stored mesh definitions are counted once above; multiply by actual visible instances when estimating scene work. |

The [glTF geometry specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#geometry) defines primitives, attribute accessors, indices, and modes. Normal, UV, and material boundaries can expand exported streams. Shared accessors and reused meshes can change accounting. Never infer source vertices, export vertices, triangles, or memory from one another using a fixed ratio.

## Spend geometry where it is visible

- Resolve primary silhouette, proportions, and **middle-scale structure** before tertiary detail. Spend on meaningful bends, attachments, cavities, fractures, and terminations. Remove redundant interior subdivision first; uniform noise and a larger count are not quality improvements.
- Inspect the actual exported asset at its intended projected size. A useful diagnostic sweep is about 32, 128, and 512 pixels on the longest projected dimension, with extra views for thin/high-contrast features. These are proposed review sizes, not hardware standards or automatic LOD thresholds.
- Record the before/after structural change and visible benefit under identical framing and light. Permit a justified increase; do not fill a ceiling or reduce to an arbitrary percentage.
- Estimate each relevant pass as the sum of visible instance count × triangles at the active level, with analogous vertex-stream and submission totals. For example, 200 copies of the study's 2,418-triangle fern imply 483,600 submitted triangles in one pass before extra shadow work. This arithmetic is not a measured performance failure. Instancing reduces some submission overhead; rendered copies still cost work.

## Optional LOD must be demonstrated

Use LOD only where view range or population benefits. Remove invisible tertiary detail first, simplify secondary groups coherently, and preserve identity-bearing openings, silhouette, contact, orientation, anchors, bounds, and major color groups. Do not impose universal 50% reductions.

Implement and observe actual switching in the target viewer. Test near/far camera travel, zoom/FOV changes, transition thresholds, hysteresis, popping, flicker, thin surfaces, and all relevant views. Distance-based switching requires calibration to the camera; screen-size intent is not implemented by naming files LOD0/LOD1/LOD2. Record which level activates and where. Multiple files alone are not proof of LOD readiness. The inspected reference explicitly [has no LODs](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/README.md#L33); this optional workflow is ours.

## Apply the framework across themes

| Family | Preserve first | Validate in context |
|---|---|---|
| Natural vegetation | Growth hierarchy, crown/frond envelope, meaningful gaps, curvature, attachment | Grove or groundcover population; low and high views; thin-surface visibility |
| Geology and terrain | Ridgelines, major fractures, cavities, bedding relief, ground contact | Near walkable areas and distant skyline; useful chunks, seams, and total visible terrain |
| Modern objects | Functional proportions, joints, handles/openings, mechanisms | Interaction distance, repeated interiors/streets, material submissions |
| Futuristic objects | Coherent assembly, power/motion paths, service interfaces, clear unfamiliar components | Close inspection versus repeated infrastructure; geometry and effects costs separately |
| Fantasy structures/props | Internally coherent support/growth logic, focal silhouette, selective motifs | Landmark and background roles separately; readability without effects |
| Alien organisms/technology | Consistent invented branching, segmentation, growth, or assembly | Colony/field density, unfamiliar-form recognition, overlap and effects |

Do not automatically cap a terrain chunk or distant mountain as a car-sized object. Do not apply industrial bevel conventions to geology or terrestrial botanical anatomy to alien forms without a design reason. Keep scientific evidence labels separate from invented-world logic.

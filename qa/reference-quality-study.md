# Reference quality study: RHS059/low_poly_items

Date: 2026-10-16 UTC. Research only; no model, generator, or skill was changed by this study. No commit or push was made.

## Decision

The useful lesson is **more specific shape decisions per asset**, rather than more polygons everywhere. The reference's strongest manufactured objects have a clear main body, recognizable component proportions, a few meaningful recesses or openings, and small details concentrated where the object operates. Our current pack is coherent and technically organized, but some assets still read as diagrams of their category rather than resolved objects.

Keep the original palette and modeling ownership. First revise **two or three quality samples: conifer, fern, and natural arch**, then obtain a visual decision before extending the approach to the remaining assets. This is a proposed modeling pass, not work performed by this study. The broader library should support natural, geological, modern, fantasy and alien scenes; Section 7 separates reusable budget principles from this city reference and our current prehistoric sample pack.

## 1. What was actually inspected

Reference: [RHS059/low_poly_items](https://github.com/RHS059/low_poly_items), checked out separately at commit [2c3cf681cce1cdbcb8f0c7297120422ab178ab90](https://github.com/RHS059/low_poly_items/tree/2c3cf681cce1cdbcb8f0c7297120422ab178ab90). Local research checkout: `/tmp/lowpoly-reference`, outside this project. The scope below is the primary 1,050 assets in `exports/`, not the separate `argon/` collection.

This was not a README-only review:

- Opened the actual pixels of `previews/overview.jpg`; individual eastern white pine, daylily, and stone tunnel portal thumbnails; and six stored viewer screenshots listed below.
- Read selected builders in `batches/batch03.py`, `batch08.py`, `batch10.py`, and `batch17.py`; the preview and build implementations; the current viewer lighting; materials; manifest; and selected revision records.
- Independently parsed the JSON chunks of all **1,050 exported GLBs**. None contains image textures, image resources, or `TEXCOORD_0`. Selected triangle and exported POSITION-stream counts agree with the manifest. These are measurements, not an artistic score.
- Imported six actual GLBs into Blender 4.3.2 and rendered them under one neutral-gray setup: reference pine, daylily, shoe; our conifer, fern, arch. Original materials were replaced only in temporary research scenes. No reference builder was executed, no `.blend` was saved, and no derived model was exported.
- Opened all six generated gray renders. This controls color and much of the presentation difference; it is a limited-angle structural comparison, not a fresh browser acceptance test or an exhaustive audit of the reference.
- Inspected our ten-asset contact sheet and selected hero, side, top, reverse, and alternate-key gray views for the three comparison assets. The fern contact-sheet cell is older than the later fern images and must not be used as evidence of the final revision.

### Screenshot and model evidence

All reference links are pinned to the inspected commit. Reference images are linked, **not copied into this repository**.

| Reference asset | Actual screenshot/preview inspected | Actual model and relevant evidence |
|---|---|---|
| Classic muscle coupe | [review/b03_classic_muscle_coupe.png](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/review/b03_classic_muscle_coupe.png) | `exports/b03_classic_muscle_coupe.glb`; `batches/batch03.py`: shaped longitudinal body sections, wheel openings, bowed/framed glass, fascia, wheels |
| Bottled-drink vending machine | [review/b10_bottled_drink_vending_machine.png](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/review/b10_bottled_drink_vending_machine.png) | `exports/b10_bottled_drink_vending_machine.glb`; `batches/batch10.py`: cabinet, framed display, controls, tray and grille |
| Running shoe | [review/b17_running_shoe.png](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/review/b17_running_shoe.png) | `exports/b17_running_shoe.glb`; reopened and rendered in neutral gray |
| American elm | [review/b08_american_elm.png](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/review/b08_american_elm.png) | `exports/b08_american_elm.glb`; `batches/batch08.py`: spreading scaffold branches and terminal crown groups |
| Eastern white pine | [previews/items/b08_eastern_white_pine.png](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/previews/items/b08_eastern_white_pine.png) | `exports/b08_eastern_white_pine.glb`; reopened and rendered in neutral gray |
| Daylily clump | [previews/items/b08_daylily_clump.png](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/previews/items/b08_daylily_clump.png) | `exports/b08_daylily_clump.glb`; reopened and rendered in neutral gray |
| Open debris skip | [review/b04_compact_open_debris_skip.png](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/review/b04_compact_open_debris_skip.png) | `exports/b04_compact_open_debris_skip.glb`; tapered open body, top rail, stiffeners and lifting points |
| Window opening wall | [review/b21_wall_window_opening_4m.png](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/review/b21_wall_window_opening_4m.png) | `exports/b21_wall_window_opening_4m.glb`; opening, thickness, restrained perimeter treatment |
| Cut-stone tunnel portal | [previews/items/b13_streetcar_cut_stone_tunnel_portal.png](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/previews/items/b13_streetcar_cut_stone_tunnel_portal.png) | `exports/b13_streetcar_cut_stone_tunnel_portal.glb`; useful **counterexample** to natural-arch construction, not a geological reference |

### Research-render record

Temporary evidence is in `/tmp/lowpoly-study-renders/`: `reference-pine-clay.png`, `reference-daylily-clay.png`, `reference-shoe-clay.png`, `our-conifer-clay.png`, `our-fern-clay.png`, `our-arch-clay.png`, and `render-provenance.json`. Research script: `/tmp/lowpoly-study-render.py`. Independent GLB audit: `/tmp/lowpoly-reference-study-glb-audit.json`.

Settings: Cycles CPU, 64 samples, 512×512, Standard transform, exposure 0, gray nonmetallic material, fixed soft key/fill, orthographic camera, longest object extent normalized to 2 units. Images are individually normalized, **not a relative-scale comparison**. Denoising was unavailable in this Blender build; the failed first attempt produced no images and was rerun with denoising off. Fine sampling noise is not a geometry defect.

Our research inputs were frozen under `/tmp/lowpoly-study-inputs/` because other work was revising the fern concurrently:

| Input | Actual triangles | Export POSITION vertices | SHA-256 |
|---|---:|---:|---|
| `plants/conifer-tree/conifer-tree.glb` | 2,382 | 4,938 | `f7331e9602faea1e2d29bc9b185baa2fbd3ee16bd36bb2d6641eabc4aa019fea` |
| `plants/fern-cluster/fern-cluster.glb` | 2,418 | 6,784 | `ef8b028ba1189bafedc33d93e25abc84f384cfebab678d6a777c313dccccdd19` |
| `geology/natural-arch/natural-arch.glb` | 672 | 1,312 | `393dbf9e01187f6f417650cb56c56240053671367d4069d1f9d05c257f735013` |

Paths in this table are relative to `assets/prehistoric/`. The comparisons describe these snapshots; later changed files need another review.

## 2. Why selected reference objects feel more resolved

### A. Specific proportions and construction carry the identity

The coupe is not just a rectangular body plus four wheels: the cabin-to-hood relationship, shoulder, wheel openings, glazing boundary and fascia give several scales of recognition. The shoe has a heel, foot opening, shaped upper, toe transition and layered sole. It remains recognizable in our gray render at only **330 triangles**. The skip's sloping walls, rim, lifting points and underside supports explain its construction with **1,168 triangles**.

Transferable principle: design the relationships between recognizable parts before adding surface detail. For a plant, those relationships are trunk–bough–branchlet–foliage, or crown–petiole–rachis–pinna, rather than handles and panels.

### B. Detail has a location and a purpose

The vending machine reserves a large quiet side panel. Most small forms are placed on the front where a person chooses, pays, and collects. The 572-triangle window wall is mostly plain, because the opening and wall thickness do the important work. A single chamfer or inset can describe how parts meet more effectively than many arbitrary facets.

Transferable principle: give each asset one or two high-information regions, supported by quiet masses. For an arch this could be an eroded shoulder and undercut; for a fern, the frond's midsection and unfurling tip. Do not add equally dense detail everywhere.

### C. Mid-scale form is doing more work than microdetail

The reference's primary silhouette, secondary construction and tertiary trim are distinct. Our conifer has a clear trunk and many similarly sized pointed foliage pieces, but the intermediate branchlet-to-spray organization is less convincing. Our arch has an opening and surface bands, but little middle-scale erosion or differential bedding relief. Increasing tiny facets would miss that gap.

### D. Color groups reinforce actual components

The reference uses solid PBR colors. Car paint, glass, rubber and metal have different visual roles; the shoe's sole is visibly separated from its upper. These contrasts explain construction. Our green and earth families are already coherent. We need better placement of value and form changes more than a replacement palette.

Do not import the reference's palette. Use our own named colors to distinguish growth stage, exposed wood, sedimentary units or genuine material transitions. A hue change should not substitute for a missing fold, cavity or joint.

### E. Polygons are a means, not an explanation

| Reference asset | Triangles | Export vertices | Materials |
|---|---:|---:|---:|
| Running shoe | 330 | 618 | 6 |
| Window opening wall | 572 | 1,248 | 2 |
| Open debris skip | 1,168 | 2,464 | 3 |
| Daylily | 1,692 | 3,990 | 3 |
| Vending machine | 1,856 | 3,760 | 9 |
| American elm | 3,552 | 7,776 | 3 |
| Eastern white pine | 3,616 | 7,382 | 3 |
| Muscle coupe | 5,158 | 9,620 | 11 |

Counts were checked against actual GLB accessors. Export vertices include normal/material splits and are not the same as authored mesh vertices. These unrelated subjects do not establish a universal quality-per-triangle ranking. They do disprove a simple rule that more triangles automatically produce a more finished object. More materials also mean more primitives in these files; copying their material count is not a performance strategy.

## 3. Geometry, texture, material and presentation contributions

**Geometry: substantial and directly observed.** The shoe remains descriptive after all materials are replaced with gray. The reference pine retains a crown envelope and foliage thickness; our gray tests also expose its repeated domed clusters. Our own conifer remains sparse and spear-like in gray, and our arch remains unusually regular. These differences are not caused solely by color grading.

**Textures: no contribution in the audited primary GLBs.** All 1,050 contain zero images, textures and UV0 sets. Claims that the reference looks better because of texture resolution would be incorrect.

**Materials: useful secondary contribution.** The reference differentiates painted surfaces, glass, rubber and metal through solid color and metallic/roughness parameters. Our natural subjects should remain mostly nonmetallic. Do not copy material definitions merely because their swatch looks appropriate: the inspected daylily uses the shared metallic `gold` material for flower parts, an example where palette reuse is not a botanical material model.

**Presentation: meaningful, but not a substitute for modeling.** The catalog's `tools/preview.py` shades actual exported triangles with a fixed light and a substantial ambient term; it is not a photoreal render. The stored viewer screenshots add a grid, framing and cast shadows. Current `index.html` uses three camera-relative directional lights, ACES tone mapping at exposure 1.15, and floor shadows while meshes do not receive shadow maps. This differs from the README's one-directional-light description. Inspect implementation rather than repeating that description.

Consequently, the reference looks crisp partly because its presentation keeps parts visible. Our soft, grainy draft renders can obscure small boundaries, so final presentation needs cleaning up too. However, a render-only polish would leave the central structural weaknesses intact. Do not imitate moving lights or suppressed self-shadows as an acceptance test: keep a fixed-light and alternate-key diagnostic, and inspect the exported model in the actual target viewer.

The reference's `review/viewer-check.json` is the author's stored test report, not a browser test repeated during this research. This study does not certify its current live viewer.

## 4. Three actionable comparisons

### Sample 1: Conifer — fix the scale of the foliage representation

Evidence: `assets/prehistoric/plants/conifer-tree/preview-hero.png`, `preview-side.png`, `preview-clay-alt.png`, the frozen GLB and new gray render. Reference: eastern white pine and elm above.

**Current reading.** The tapering trunk and branch tiers are clear. However, large, diamond-section pointed pieces read as individual oversized broad leaves or spears. The side view exposes a strong ladder of shelves with similar open intervals. The description calls these needle-bearing sprays, but the visible proportions do not consistently communicate that scale.

**Make these changes first:**

1. Preserve the conifer's dominant axis and the intended open crown. Replace the broad single-tip units with thinner, elongated, locally forked spray envelopes. Each spray should contain a main direction and two unequal lateral branchlet groups; do not model every needle.
2. Establish three scales: structural bough, secondary branchlet fan, small terminal shoot. Taper and angle them differently. A spray should appear attached along a branchlet, not like one enormous leaf mounted on a stick.
3. Change overlap and spacing of selected tiers so one side forms a continuous crown mass while another retains a deliberate opening. Avoid simply filling all gaps or adding identical extra tiers.
4. Reassign light/dark groups by crown depth or growth group only after the gray form works. Avoid a row-by-row color pattern.

**Acceptance.** At 128 px, recognize an open conifer crown rather than a pole bearing broad leaves. At 512 px, read branchlet-to-spray attachment in three-quarter and side views. Keep one intentional crown gap without exposing a repetitive shelf pattern. Document whether any added geometry improves a visible silhouette or joint.

**Do not copy:** the reference white pine's conical top or repeated cushion-like foliage. Its thick crown groups help read mass, but their repeated domes are also a simplification. This is a construction lesson, not a species reconstruction target.

### Sample 2: Fern — design the frond as a continuous tapered unit

Evidence: `assets/prehistoric/plants/fern-cluster/preview-hero.png`, `preview-side.png`, `preview-top.png`, frozen 2,418-triangle GLB and new gray render. Reference: daylily only for hierarchy and leaf thickness, not fern anatomy.

**Current reading.** The new version is more legible than the old contact-sheet cell. The bowed axes and separate pinnae are present. Still, large triangular pinnae dominate as a sequence of flags; the eye follows isolated sharp pieces more readily than a soft tapered frond. Stem-heavy gaps and abrupt leaflet silhouettes contribute to a mechanical appearance. This is a remaining art-direction issue, not a claim that the recent revision failed its technical repair.

**Make these changes first:**

1. Approve each frond's overall tapered envelope before constructing individual pinnae: narrower basal region, fuller middle, diminishing tip. Vary the outline along the curve rather than repeating one triangle scaled up and down.
2. Adjust pinna attachment angle, width profile and local fold together. Keep enough face area visible from common low viewpoints, while retaining believable thin foliage. A strongly horizontal or uniformly vertical leaf plane should not be the only solution.
3. Prefer a few clean shape bends over isolated serrations. Allocate extra vertices where they soften an angular pinna shoulder or follow rachis curvature, not to decorative facets inside a flat leaf.
4. Group seven fronds into a legible dominant fan, a lower supporting fan and the young crozier. Allow overlap near the crown, then open selected outer gaps. Reduce exposed stem length where the clump currently reads as an umbrella frame.

**Acceptance.** At 128 px, see a fern clump with coherent arching fronds. At 512 px and from the side, the middle and distal parts retain readable leaf surface and taper. Check top, side and reverse views after export; improvement in the hero camera alone is insufficient.

**Do not copy:** flowers, straight strap-leaf grouping, radial planting geometry, or the daylily's exact blade recipe. Ferns need their own pinna rhythm and curved local coordinate frames. No flowers should be added to this prehistoric fern concept.

### Sample 3: Natural arch — move structure out of the color bands

Evidence: `assets/prehistoric/geology/natural-arch/preview-hero.png`, `preview-reversehero.png`, `preview-clay-alt.png`, frozen GLB and new gray render. Reference: the cut-stone tunnel portal is a deliberate contrast, while skip/shoe examples illustrate meaningful edge transitions.

**Current reading.** The opening has real depth, support widths differ, and the broad planes are clean. Yet the arch's cross-section and curve remain regular enough to resemble a fabricated portal. In gray, much of the geological layering disappears because several divisions are primarily material bands. The three small base stones do not change that reading.

**Make these changes first:**

1. Choose one dominant erosion or jointing story. Introduce a broad shoulder fracture on one side and a local undercut or recessed weaker bed on the other, while keeping a believable load-bearing crown.
2. Change thickness through depth in a few intentional regions. Offset or recess one rear shoulder and reshape part of the soffit; do not apply uniform noise to every ring.
3. Let two or three bedding changes affect plane position as well as color: a resistant ledge, a shallow recess, or a broken termination. Keep the bulk of the surface quiet.
4. Make the base transition purposeful: one attached foot mass and a localized fragment group associated with the chosen break. Avoid evenly decorating both feet with pebbles.

**Acceptance.** In a neutral-gray front, reverse and side view, at least two broad geological form changes survive without color. The opening remains unmistakably full-depth, and the object no longer relies on stripes to read as weathered stone. Preserve the natural arch identity; do not turn it into stacked masonry or a noisy pile.

**Do not copy:** the tunnel portal's regular voussoirs, symmetrical arch rhythm, constant reveal or architectural plinths. Applying those details would make our existing weakness worse.

## 5. Proposed skill changes and quality-sample workflow

The current skills already mention silhouette, hierarchy, asymmetry, quiet planes, and benchmark assets. The missing step is making those directions enforceable before a batch is declared visually successful. These are proposed edits for a separate authorized pass; the study did not modify the skills.

1. **`skills/lowpoly-art-direction/SKILL.md`: add a component-and-cause brief.** Before modeling, record primary mass, secondary structure, one tertiary identifying feature, quiet region, and why each connection or interruption exists. For plants, state explicitly whether geometry represents individual leaves, shoots, branchlet sprays, or crown masses. Reject ambiguous mixing of those scales.
2. **`references/first-batch.md`: add a real sample freeze.** Produce only two or three representative samples first. Review gray and target-viewer evidence, make structural revisions, and record the accepted versions before propagating their approach. The earlier suggested benchmark sequence should be a production dependency, not just a paragraph.
3. **`references/visual-acceptance.md`: separate usable from benchmark quality.** Technical validity and category recognition are minimum gates. A sample also needs convincing secondary structure, component proportions and intentional detail concentration. Do not use a high aggregate score to mask a weak criterion or to override visible user feedback.
4. **Add a visible-change record.** For each revision, state the observed weakness, the structural change, and the expected visible outcome. Compare before/after at the same framing and lighting. “More triangles,” “higher resolution,” and “more realistic” are not sufficient reasons.
5. **Add a gray persistence test.** At least one secondary identifying structure must remain apparent with colors removed. This is a useful check for growth architecture, folded leaves, bark breaks and erosion. Preserve the existing internal-relief exception for nests and footprints.
6. **Add a geometry-spending check.** Review topology around major bends, terminations, joints and negative spaces. Allow a justified budget increase, but first remove geometry that does not improve those regions. Triangles and material slots remain measured costs, not quality targets.
7. **Keep diagnostic and promotional lighting separate.** A crisp catalog is desirable, but the sample must also pass fixed neutral lighting, alternate key direction and exported-model review. Do not adjust exposure or light tracking per asset to obtain a pass.
8. **Clarify reference handling.** This task explicitly authorized temporary research downloads. Keep third-party research outside the original-asset tree, record license status, and distinguish permission to inspect from permission to redistribute. Existing originality restrictions must still prohibit unlicensed asset, source-code, texture, palette and screenshot reuse.

Recommended sequence: conifer and arch first to test canopy construction and broad geological form; add fern as the third sample to test fine organic rhythm. Show the same three views for each: original, revised gray, revised color, with a side/reverse check available. Continue the other seven only after the chosen visual standard is actually met. This is an art-direction gate, not a request to imitate a city-prop aesthetic.

## 6. License and reuse boundary

No license file, copyright/permission grant, SPDX declaration, or README license section was found in the inspected tracked snapshot. Filename search covered LICENSE/LICENCE/COPYING/NOTICE patterns; text search found workflow permission declarations, which are unrelated to asset licensing. This establishes **no reusable license found**, not proof that the author has never issued permission elsewhere.

Public GitHub access should not be treated as permission to incorporate the models, generators, materials or screenshots into our public library. GitHub explains the difference between public visibility and a license in its [official licensing documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

For this task: retain only our original analysis and links in this repository. Keep the research checkout and derived inspection images in temporary storage. Do not copy reference files into `assets/`, `scripts/`, `site/`, distribution packages or public QA images. If direct reuse is ever desired, establish the relevant rights first. General lessons about proportion, hierarchy and inspection can be applied through independently authored geometry.

## 7. Verified budget units and a scene-independent framework

Addendum following the user's request for a multi-scenario library. The reference's city subject matter must not become the scope of our asset library or the sole basis of its budgets.

### Exact source check: these are vertex ceilings

At the inspected commit:

| Evidence | What it establishes |
|---|---|
| [README.md, lines 35–43](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/README.md#L35-L43) | The section is titled Vertex budgets. The table covers maximum source and exported vertices: handheld **999**; person-sized and smaller **5,000**; car-sized and larger **10,000**. These are ceilings, not amounts to fill. |
| [tools/assetlib.py, line 30](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/tools/assetlib.py#L30) and [lines 139–144](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/tools/assetlib.py#L139-L144) | The executable class limits are 999, 5,000 and 10,000, and construction validates vertex count against the selected class. |
| [tools/build.py, lines 138–141](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/tools/build.py#L138-L141) | Exported vertices are summed from each primitive's POSITION accessor. The manifest separately records authored vertices, evaluated source vertices, polygons and triangles. Exported counts are checked against the vertex ceiling. |
| [tools/validate.py, lines 43–56](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/tools/validate.py#L43-L56) | Validation independently counts POSITION elements and triangle indices, then applies the vertex cap to both evaluated source geometry and exported geometry. |
| [QUALITY_REVIEW.md, line 18](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/QUALITY_REVIEW.md#L18) | The revision policy repeats the vertex ceilings and rejects subdivision merely to consume a budget. |

Thus “1,000 / 5,000 / 10,000” is a useful approximate recollection, but the implemented first ceiling is **999 vertices**, and none of these figures is a triangle or polygon target. This is an enforced policy for that collection, not a universal low-poly standard. Its [README, line 33](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/README.md#L33) also says the delivered models have no LODs; a proposed LOD workflow below is our extension, not an observed reference feature.

Our current first-batch ranges are **exported triangles**. They cannot be compared numerically to the reference's vertex caps without measuring both. For example, our sampled fern has 2,418 triangles but 6,784 exported POSITION vertices; the conifer has 2,382 triangles but 4,938 exported POSITION vertices. The fern would exceed a hypothetical 5,000-exported-vertex cap despite being below 2,600 triangles. That does not make it defective under a policy we have not adopted; it shows why units must be explicit.

Use separate fields for authored vertices, evaluated vertices, exported POSITION-stream vertices, exported triangles, primitives/materials and bytes. Count triangles according to primitive mode, rather than treating every polygon as a triangle. In glTF, geometry consists of primitives with attribute accessors and optional indices; primitive splitting can also reflect different materials. See the [Khronos glTF geometry specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#geometry). For a generalized exporter, distinguish the sum of per-primitive vertex counts from unique accessor/storage counts if buffers are shared. Never infer one from the other through a fixed ratio.

### The general rule

**Choose a budget for an asset in a viewing and deployment role, rather than for a theme or a world-size noun.** Real dimensions are one input. A hand-sized object filling an inspection view can justify more form detail than a huge distant mountain. A fantasy crystal repeated 1,000 times has a different budget from one crystal used as a focal landmark.

For every asset or intended usage profile, record six decisions before final modeling:

1. **Runtime envelope.** Renderer/version, representative device class, framebuffer size, target frame time, lighting and shadow passes. Record whether the result is an isolated gallery object, a populated environment, or both. A single-object gallery does not establish a scene budget.
2. **World scale and view envelope.** Bounding dimensions, minimum allowed camera distance, typical distance, field of view or orthographic span, and measured object pixel extent at those views. State whether close inspection is supported. Normalized thumbnails do not supply this evidence.
3. **Simultaneous use.** Typical and stressful visible instance counts, clustering, occlusion and culling assumptions. Count the copies actually submitted, not the number of distinct files in the library.
4. **Semantic importance.** Name the silhouette, negative spaces and secondary parts that must survive. A landmark, interaction target and background filler can have different priorities even at equal size and screen coverage.
5. **Representation and LOD.** Define which features exist at close, medium and distant views, whether a far variant or impostor is useful, and whether a single LOD is already sufficient. Do not demand exactly three levels from every object.
6. **Independent limits and evidence.** Set explicit ceilings for exported triangles and vertices per level, plus materials/primitives, texture memory when applicable, file size and shader/overdraw risks. Then record actual counts, target-viewer images and populated-scene timing. An increase must identify the visible benefit and pass the same test conditions.

This produces concrete per-profile limits without inventing one universal triangle table. The current first-pack bands can remain documented historical starting points; they should not silently become limits for all future environments. Freeze numeric ceilings for each new profile only after the representative samples have been viewed and tested.

### Screen coverage and viewing distance

Judge the exported model at its actual projected size. A useful diagnostic sweep is approximately **32, 128 and 512 pixels on the longest projected dimension**. These are proposed review sizes, not hardware standards, automatic LOD thresholds, or a guarantee of adequate detail. Small/high-contrast features and long thin objects may need additional views.

- At small coverage, spend geometry on stable silhouette, major holes and contact.
- At medium coverage, preserve component relationships and dominant folds or breaks.
- At close coverage, resolve the few junctions, cavities and plane transitions that a person can actually inspect.

For perspective planning, projected height is approximately proportional to world height divided by distance and the tangent of half the vertical field of view. For orthographic views, it depends on world height relative to the camera's vertical span rather than camera distance. Measure the projected bounds in the viewer before deciding a distant LOD is safe; size alone cannot answer this.

The installed Three.js 0.180.0 implementation, `node_modules/three/src/objects/LOD.js`, selects levels by camera distance adjusted by zoom, with hysteresis support. The [official LOD documentation](https://threejs.org/docs/pages/LOD.html) describes distance-based transitions. Our proposed screen-coverage policy therefore needs either per-asset calibrated distances for a known camera or explicit projected-size selection; it is not obtained automatically by naming files LOD0/LOD1/LOD2.

### Repetition and scene cost

Estimate submitted geometry per relevant pass as the sum, over visible asset/LOD groups, of **instance count × triangles at that level**. Track the analogous vertex-stream total and draw submissions, but do not mistake these estimates for measured GPU time. Culling, material grouping, vertex reuse, shadows, transparency and shader work all matter.

For illustration, **200 visible copies × our sampled 2,418-triangle fern = 483,600 submitted triangles** for one pass before considering additional shadow work. A single larger focal object can contribute less geometry than that repeated groundcover. This arithmetic is a planning example, not a performance failure measured on a device.

Instancing can reduce draw-call overhead for repeated geometry and materials; it does not make all rendered copies cost the same as one copy. This distinction is consistent with the [official InstancedMesh documentation](https://threejs.org/docs/pages/InstancedMesh.html), and with the installed `node_modules/three/src/objects/InstancedMesh.js`. Evaluate material count and dense foliage overlap alongside geometric counts.

### Variable LOD: preserve meaning before percentage reduction

Do not prescribe a universal 50% reduction per level. Choose the coarsest representation that passes at the intended projected size:

- Remove invisible tertiary details first.
- Simplify secondary parts while preserving their relation to the main mass.
- Retain identity-bearing negative spaces, dominant silhouette breaks, contact and useful orientation cues.
- Preserve a stable anchor, bounds and major color groups across levels; inspect transitions for popping and flicker.
- Tune transition distances or projected-size thresholds and hysteresis in the target runtime. Distance-based LODs require reconsideration when field of view or inspection zoom changes.
- Use a separate close-inspection variant when a dense environmental version would be wasteful, rather than forcing every scene instance to carry it.
- Cull only when the intended scene use allows disappearance. A distant navigation landmark may remain important at very small screen coverage.

### Applying the same framework across subjects

| Subject family | Geometry that earns its budget | What usually simplifies first | Important deployment test |
|---|---|---|---|
| Natural trees and shrubs | Trunk taper, growth hierarchy, crown envelope and large canopy gaps | Minor shoots and internal foliage subdivisions; regroup into larger crown masses at distance | A populated grove, low and elevated views, crown silhouette through LOD transitions |
| Ferns, grasses and small plants | Coherent leaf/frond envelope, local curvature, base attachment and a few distinguishing tips | Small pinnae/serrations and redundant interior blades, while preserving fan direction | Many simultaneous clumps; thin-surface visibility and overlap at actual screen sizes |
| Rock, cliffs and landforms | Major fracture planes, arches/cavities, ridgelines, bedding steps and contact | Small chips, shallow surface breaks and unseen subdivision | Near walkable region plus distant skyline; chunk boundaries if the landform is split |
| Modern objects and machines | Functional proportions, handles/openings, joints, mechanisms and wheel/body relationships | Tiny fasteners, grille repetitions and hidden trim | Interaction/inspection distance, repeated street or interior placement, material submissions |
| Fantasy structures and props | Designed load/growth logic, focal silhouette, repeated design motifs and deliberate exceptions | Ornament that does not support recognition or interaction | Focal-object and background uses separately; the form must work without effects masking it |
| Alien organisms, crystals and technology | A consistent invented structural system: branching, segmentation, growth, support or assembly rules | Repeated tiny spines, grooves or nodules once the invented system reads | Colony or field density, unfamiliar-object recognition, and effects/overdraw separately from mesh detail |

These are transferable priorities, not permission to copy terrestrial botanical anatomy onto alien forms or industrial bevels onto rocks. Fantasy and alien work need internal visual logic rather than scientific labels. For scientific or evidence-informed natural assets, retain the existing reconstruction boundaries. Large terrain should be budgeted per useful chunk/view region and total scene, not automatically classified as a “car-sized” object with a 10,000-vertex cap.

### Additional skill proposals

9. **Separate topic from budget profile.** Make the top-level art-direction skill usable for natural, geological, modern, fantasy and alien assets. Put prehistoric scientific constraints in the dedicated domain skill and current pack conventions in pack-specific references.
10. **Add a budget brief with explicit units.** Require the six decisions above, measured source/export counts, expected projected sizes, repetition assumptions and a reason for each selected ceiling. Store triangle and vertex fields separately; remove ambiguous uses of “poly count.”
11. **Add per-profile visual/runtime acceptance.** Review the approved sample at small, medium and close projected sizes and in its intended population. A single attractive thumbnail and an individual GLB under its cap are insufficient.
12. **Make LOD optional and purpose-driven.** Require levels only where the view envelope or population benefits, describe the structures each level retains, and verify the selection behavior in the chosen renderer. Do not claim LOD readiness from multiple files alone.
13. **Use the reference numbers as evidence, not inherited law.** Cite its 999/5,000/10,000 **vertex ceilings** accurately when discussing that collection. Derive our own numeric limits from use cases and sample tests; neither impose those ceilings universally nor spend up to them automatically.

## Bottom line

Improve the **middle layer of form**: branchlet-to-crown relationships, whole-frond taper, and meaningful erosion planes. Keep the surfaces calm, spend detail on identity and construction, and use material and presentation polish to reveal those choices. Two or three genuinely convincing samples will teach us more than another full batch that merely satisfies the existing checklist.

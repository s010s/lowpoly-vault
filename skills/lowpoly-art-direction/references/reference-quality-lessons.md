# Reference Quality Lessons and Reuse Limits

This is an original summary of the project's [2026-10-16 recorded study](../../../qa/reference-quality-study.md), not a copy of reference models, source code, palettes, or images. The inspected source is [RHS059/low_poly_items at commit 2c3cf681cce1cdbcb8f0c7297120422ab178ab90](https://github.com/RHS059/low_poly_items/tree/2c3cf681cce1cdbcb8f0c7297120422ab178ab90). Use that fixed snapshot when discussing findings; do not silently substitute the current branch.

## What the recorded study establishes

The study inspected previews, stored viewer images, selected builders and rendering implementations, and the actual JSON chunks of 1,050 primary exported GLBs, excluding the separate argon collection. It also rendered six actual exported models in neutral gray: reference pine, daylily, and shoe; our conifer, fern, and arch. No reference builder was executed or derived model exported. These actions are the study's recorded work, not a new audit performed by this skill revision.

The matched gray setup used Blender 4.3.2, Cycles CPU, 64 samples, 512×512, Standard, exposure 0, a fixed soft key/fill, and orthographic framing. Each object's longest extent was normalized to two units. This controls color and much of presentation, but is neither a relative-scale comparison nor exhaustive multiview or live-browser acceptance. Sampling noise is not geometry. Findings apply to frozen study inputs; later revisions require fresh inspection.

- The audited primary GLBs contained no image textures, image resources, or UV0 sets. Their finish cannot be explained by texture resolution.
- A 330-triangle reference shoe remained descriptive in gray through its opening, upper, heel/toe transition, and layered sole. Other subjects used much larger counts. This supports purposeful structure, not a universal quality-per-triangle ranking.
- Solid material colors helped explain real components, but did not replace them. Keep our original palettes and use color to reinforce structure.
- The inspected viewer implementation differed from its README lighting description. Treat implementation and observed output as evidence; the author's stored test report is not a browser test we repeated.

## Transfer the decisions, not the recipes

1. **Primary, secondary, tertiary:** Define a dominant body, convincing intermediate construction, and a few small identifying features. A missing middle layer cannot be repaired by many tiny facets.
2. **Proportion relationships:** Resolve trunk–bough–branchlet–spray, crown–rachis–pinna, body–opening–joint, or an invented equivalent before decoration. State what scale each geometric unit represents.
3. **Concentrated detail:** Give an asset one or two informative regions supported by quiet masses. Concentrate detail at operation, attachment, fracture, or growth transitions rather than spreading it uniformly.
4. **Gray persistence:** At least one secondary identifying structure should survive color removal. A material stripe cannot stand in for a needed recess or erosion step. Nests and footprints retain their neutral-gray top-view/internal-relief recognition test.
5. **Matched revisions:** Compare the same framing, lights, and exported state. Record observed weakness → structural change → visible result. More triangles, random noise, or a new render grade is not a sufficient change rationale.

## Current sample directions

These are proposed improvements derived from the frozen comparison, not claims that revised assets have passed.

| Sample | Structural priority | Evidence required |
|---|---|---|
| Conifer (针叶树) | Distinguish bough, branchlet fan, and terminal spray; replace ambiguous giant-leaf units; preserve one deliberate crown gap without regular shelves | Open-conifer reading at small size; branchlet-to-spray connection in gray three-quarter and side views |
| Fern (蕨丛) | Establish a complete tapered frond envelope; coordinate pinna angle, width, and fold; reduce exposed umbrella-like stem gaps | Coherent arching fronds; leaf surface and taper visible from side, top, and reverse after export |
| Natural arch (石拱) | Add a few meaningful shoulder fractures, undercuts, depth changes, or bedding steps; retain a plausible crown and quiet mass | At least two broad geological changes visible in gray from front, reverse, and side; a full-depth opening |

Do not copy the reference pine's repeated foliage cushions, the daylily's flowers or strap-leaf recipe, or the [cut-stone portal's architectural construction](https://github.com/RHS059/low_poly_items/blob/2c3cf681cce1cdbcb8f0c7297120422ab178ab90/previews/items/b13_streetcar_cut_stone_tunnel_portal.png). The portal is a counterexample for a natural arch, not geological evidence. Keep any scientific reconstruction claims subject to independent evidence.

Freeze two or three approved sample versions with gray/color and target-viewer evidence before extending their approach to a whole batch. Recognition and technical validity are minimum usability; benchmark quality requires convincing secondary structure, proportions, and detail placement. Scores cannot override a visibly weak criterion or user feedback. The broader library is not restricted to prehistoric or city props; [asset budgeting](asset-budgeting.md) applies these principles across all supported themes.

## License and publication boundary

The study found **no reuse license in the inspected tracked snapshot**: no license/permission file, SPDX declaration, or README license section. This does not prove that the author has never granted permission elsewhere. Workflow permission declarations are not asset licenses. Public repository visibility is not treated as permission to incorporate its contents.

Keep only original analysis and fixed-commit links in this repository. Separately authorized inspection copies and derived inspection renders stay in temporary research storage outside the original-asset tree. Do not copy or repackage reference models, generator code, materials, palettes, textures, screenshots, or derived comparison images into assets, scripts, the site, distribution packages, or public QA imagery. Establish the relevant rights before any direct reuse. General lessons about proportion, hierarchy, and review may inform independently authored work.

All reference-repository links above are pinned to the inspected commit. Do not embed or vendor its images merely to make this summary more visual.

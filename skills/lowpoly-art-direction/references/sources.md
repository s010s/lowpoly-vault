# Primary Sources and Evidence Limits

Research date: 2026-10-16. Sources are Blender's official documentation and artists' own websites or tutorials. No third-party models, textures, palettes, or .blend files were downloaded. The recommendations are an original synthesis for this project, not a verbatim account of any artist's process or a claim that the videos were watched in full.

## Blender documentation

1. [Decimate Modifier](https://docs.blender.org/manual/en/3.3/modeling/modifiers/generate/decimate.html)
   - The searchable official text describes reducing vertices and faces while minimizing shape changes. Economically modeled meshes usually do not need this step; complex modeling, sculpting, or subdivision results are more typical simplification candidates.
   - Project application: reduction does not replace low-poly art direction. Sculpting followed by decimation is valid, but requires another visual review.
   - Evidence limit: the official search index exposed version 3.3 text; direct fetching returned 402. This supports the concept, not assumptions about the installed version's UI or Python API.

2. [Triangulate Modifier](https://docs.blender.org/manual/en/5.3/modeling/modifiers/generate/triangulate.html)
   - The searchable official text describes conversion of quads and n-gons to triangles, with different diagonal and n-gon splitting methods.
   - Project application: inspect the final split directions, especially for nonplanar quads. Triangulation is not a reason to create visible facet noise everywhere.
   - Evidence limit: search returned version 5.3 documentation. This does not establish the production environment's version or that version's release status. Direct fetching returned 402. Use help matching the actual installed version when executing.

3. [Mesh Structure / Shading](https://docs.staging.blender.org/manual/en/latest/modeling/meshes/structure.html)
   - The official indexed text explains normal interpolation in flat versus smooth shading and object-level or face-level control.
   - Project application: geometry and normals jointly communicate facets. Allow intentional mixed shading rather than enforcing one treatment across every low-poly asset.
   - Evidence limit: only the official indexed text was available. Direct fetching returned 403; no attempt was made to bypass it. No account action or download was performed through this page.

4. [Mesh Clean Up](https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html)
   - The official index lists Delete Loose, Degenerate Dissolve, Make Planar Faces, Split Non-Planar Faces, Split Concave Faces, and Merge by Distance.
   - Project application: explicitly inspect large nonplanar faces and degenerate geometry. Running all cleanup tools is not automated art acceptance.
   - Evidence limit: indexed text was available; direct fetching returned 402. Tool names and concepts do not replace operational verification in the installed version.

5. [Blender 4.0 Color Management Release Notes](https://developer.blender.org/docs/release_notes/4.0/color_management/)
   - This primary document confirms that AgX replaced Filmic as the default view transform for new Blender 4.0 files, changing highlight color handling.
   - Project application: lock and record the view transform and exposure; do not compare palette results under different version defaults.

## Artists' own resources

6. [Polygon Runway: Become a 3D Illustrator](https://polygonrunway.com/p/become-a-3d-illustrator)
   - Roman Klčo's own course outline combines modeling, lighting, texture painting, composition, and ambient lighting into a creative workflow, with forest and ancient-ruin examples.
   - Project application: review assets both in isolation and in a scene grouping. Image quality depends on more than polygon count.
   - Evidence limit: only the public course outline was read. No paid lessons or downloadable example scenes were accessed.

7. [Polygon Runway: Enchanted Forest](https://www.youtube.com/watch?v=stdVW3kmMbw)
   - The artist's public tutorial description lists a ground tile, stump, mushrooms, grass, and rocks, with possible use in isometric illustration or game assets.
   - Project application: a category-combination example and a later learning reference, not a source of models or a scene to copy.
   - Evidence limit: the public description was read; full frame-by-frame video content was not obtained. No specific modeling steps are attributed to unseen footage.

8. [Polygon Runway: Better Blender Low Poly with a Simple Trick](https://www.blendernation.com/2024/12/11/better-blender-low-poly-with-a-simple-trick/)
   - The article is credited to polygonrunway and describes a tutorial addressing planar faces and unexpected rendering in low-poly models.
   - Corresponding artist video: [YouTube](https://www.youtube.com/watch?v=ahhLRwTxtPk).
   - Project application: treat nonplanar faces as a common visual failure to inspect.
   - Evidence limit: only the credited article's description was read. Video retrieval failed; no claim is made to have watched the specific technique.

9. [Grant Abbitt Course Library](https://www.gabbitt.co.uk/courses)
   - The artist's site describes a simple sculpting workflow for low-poly rocks and directly links [Realistic Low Poly Game Assets — Rocks](https://www.youtube.com/watch?v=WQHBSgRQ50o).
   - Project application: several modeling routes can produce low-poly work. Original craftsmanship does not prohibit sculpting or procedural assistance; the final form still needs design.
   - Evidence limit: the course listing and video title were verified, not the full tutorial content. Its rocks were not copied.

10. [Imphenzia: PixPal Palette Texture](https://imphenzia.com/imphenzia-pixpal)
    - The creator explains scene-wide coloring through a small shared palette texture and material, with UV placement selecting colors and material parameters.
    - Project application: learn the shared-palette workflow concept while designing all colors, textures, and materials independently. The asset pack was not downloaded. One material does not guarantee a fixed draw-call count independent of the target engine.

11. [Andrew Price: Lighting Mastery Series](https://www.blenderguru.com/posts/2019/lighting-mastery)
    - The artist's public page organizes lighting into direction, source size, color, readability, and emphasis, discussing shadow softness, exposure, fill, and subject separation.
    - Project application: test lighting first reveals volume, contact, and readability. Presentation lighting can then establish mood without concealing structural defects.

12. [Andrew Price: Understanding Composition](https://www.blenderguru.com/posts/understanding-composition)
    - The artist's article explains that composition goes beyond the rule of thirds, providing a learning entry point for structure, focus, and balance.
    - Project application: environments provide space and visual guidance for animal exhibits. Making every asset the brightest or most saturated focal point destroys hierarchy.

## Original synthesis, not source quotations

The following are project-specific decisions: the 128-pixel silhouette test with a neutral-gray internal-geometry exception for trace assets, five scoring criteria and a 16/20 threshold, three initial benchmarks, triangle tiers, the 60/30/10 starting shape relationship, the fourteen-color palette, and the specific failure-pattern corrections. These are adjustable working conventions, not universal standards stated by any document or tutorial. The project selected the final ten asset categories; this research supplied their construction guidance.

## Questions requiring dedicated research

- The museum's actual period, region, target animals, and evidence for vegetation coexistence.
- Plant leaf arrangement, branching, proportions, and whether modern genus/species names are appropriate.
- Nest, egg, and footprint shapes, dimensions, numbers, arrangements, and supporting evidence.
- Target runtime, minimum visible size, device constraints, collision, and LOD requirements.

Until these are established, assets may be made as clearly labeled stylized environment props, but not advertised as an accurate reconstruction of a particular period's ecosystem.

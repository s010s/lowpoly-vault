# Future-only technical profile: lowpoly-lighttexture-v1

## Practical defaults, not pass/fail budgets

Start with base color around **512 px**; for opaque color, JPEG around quality 80–85 with no chroma subsampling is a useful starting point. Keep alpha when needed (PNG; use MASK for cutouts where appropriate); never silently discard transparency. A **256 px normal** and **128 px roughness** are optional starting points, not three compulsory maps. Adjust dimensions, compression and channel choice to the actual object and intended viewing distance within the existing frozen budget. A near-view hero may need more; a plain material may need only constants. Record the decision, do not run mandatory quality ladders.

Use original, object-aligned UV/material-region detail. Spend geometry on silhouette and structural connections; use maps for surface-scale detail. Align patterns with growth, layering, anatomy and curvature. Avoid doubled detail when geometry already expresses scales, cracks or ribs. Place seams discreetly, give islands sufficient padding for filtering/mips, and inspect the actual export at useful overall and close views. Do not prescribe one padding value or unique UVs everywhere; mirrored/reused UVs are acceptable when the intended appearance permits them.

Base-color images are sRGB; normal/roughness/metallic/occlusion are Non-Color linear data. Use tangent-space glTF normals (+Y); wire through a Normal Map node. glTF metallic-roughness uses roughness in G, metallic in B, occlusion in R when packed; use Separate Color channels, not an arbitrary grayscale-to-color connection. Keep constant metallic zero for ordinary nonmetals. Blender procedural shaders must be baked into supported image textures for portable GLB. Do not bake directional lighting into albedo. Resize color in linear light then encode sRGB; filter normal maps as vectors and renormalize. Avoid lossy normal-map encoding as an untested default.

## Export contract and evidence

Use a future producer with UV export enabled; do **not** inherit `export_texcoords=False` from purecolor producers or alter old producers. `scripts/lighttexture_profile.py:export_options(has_normal_map=...)` supplies future-only static Blender flags and rejects missing runtime support through `export_glb`; prefer explicit tangents when normal-mapped; a verified target-runtime MikkTSpace derivation is also valid, not a universal hard gate. Triangulate deliberately before normal-map baking/export if needed to keep the tangent basis consistent. Pin actual Blender/exporter settings and all texture bytes; do not claim the experiment's Blender 5.2 runtime is this environment's 4.3.2.

Run `python scripts/lighttexture_profile.py candidate.glb` on the actual exported file. It reports hash, embedded image dimensions/bytes, referenced texture slots, required UV attributes and declared glTF color-space semantics. It is a narrow uncompressed static-profile check, **not** Khronos validation, source color-space verification, visual acceptance or publication approval. Retain the official glTF validator and existing geometry/source checks. Image decoding uses Pillow; absence is a blocker, not PASS.

For a texture-bearing candidate require its intended maps to be embedded, decode successfully and be referenced by used materials with matching UVs. If constant-only surfaces are justified, use `--allow-untextured` and record that exception in the frozen brief; never use it to hide a dropped intended texture. Unsupported compression/extensions need a separately reviewed profile, not a fabricated PASS. The actual GLB must load in the target runtime; inspect its colors, seams and highlights rather than a source-only render. A format report cannot establish visual correctness or scientific truth.

Measure GLB and embedded compressed image bytes separately from decoded GPU-memory estimates. JPEG reduces transfer size, not texture dimensions or decoded GPU memory. Report any RGBA8+mips estimate as an estimate, not measured VRAM. KTX2/compression is optional future work, not a prerequisite or automatic profile extension.

## Experiment evidence boundary

The later user feedback explicitly accepted the improvement and supersedes older report statements awaiting owner choice. This supports adopting the default now without another full experiment; it does not grant publishing authority.

User-supplied report `internal/asset-pipeline-20261029/experiment-record.md` records 512/256/128 as the lightweight trial, with visible near-view losses. Local inspection received reports, not underlying GLBs/images; numbers are reported history, not independently reproduced here. The user's visual approval supports the direction, not automatic acceptance of future assets or every old experimental variant. Historical ~472 KB example is not a library-wide cap. Do not copy old experiment retry counts into current budgets.


## Official references reviewed for this update

- [Khronos realtime asset guidelines](https://www.khronos.org/assets/uploads/apis/3DCommerce-Realtime-sset-Creation-Guidelines_Jul20.pdf): silhouette, UV allocation and material craft; its commerce-specific resolution/photorealism budgets are not this project's hard gates.
- [Khronos advanced materials tutorial](https://github.com/KhronosGroup/glTF-Tutorials/blob/main/gltfTutorial/gltfTutorial_014_AdvancedMaterial.md): material response and normal detail versus actual geometry.
- [glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html): texture color/data semantics, channel packing, alpha modes and tangent basis. Explicit tangents are not mandatory for all glTF assets.
- [Blender 4.2 Normal Map manual](https://docs.blender.org/manual/id/4.2/render/shader_nodes/vector/normal_map.html): matching UVs and Non-Color input. This is documentation context, not a claim that every installed-version export option was verified.
- [Three.js color management](https://threejs.org/manual/pages/color-management.html): input/working/output spaces; do not apply duplicate conversions to GLTFLoader-managed textures.
- [Three.js textures](https://threejs.org/manual/pages/textures.html): encoding, dimensions and estimated memory are different budgets.
- [KHR_texture_basisu](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_texture_basisu) and [Three.js KTX2Loader](https://threejs.org/docs/pages/KTX2Loader.html): optional compressed GPU delivery requires target support detection and transcoder setup, not an automatic quality/memory guarantee.

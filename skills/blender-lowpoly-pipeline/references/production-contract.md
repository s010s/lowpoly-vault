# Production contract draft

## Proposed output structure

For asset `<slug>`, use `assets/<collection_id>/<category>/<slug>/` containing `<slug>.blend`, `<slug>.glb`, `preview-hero.png`, `preview-reversehero.png`, requested orthographic/diagnostic PNGs, `metadata.json`, `qa.json` and the official validator report. Reproducible generators live in `scripts/models/`. The first collection is `prehistoric`; categories are geology, plants, wood, traces. Preserve this structure for the first pack and keep the collection parameter extensible.

Metadata should include schema version, slug, display name/taxon, style variant, model dimensions in meters, Blender and exporter versions, generator/seed/config hash, axis and origin conventions, material palette, source and reconstruction notes, license/provenance for each included component, counts from both source and exported geometry, GLB bytes, extension list, checksums, QA statuses and reviewed warnings. Record real-world-scale estimates and their uncertainty independently of artistic pose bounds.

## Geometry and topology

- Profile-based lofts for torso/neck/tail and low-sided tapered sections for limbs usually give better deliberate shape than default UV spheres. Change cross-section density where the silhouette turns, not uniformly everywhere.
- Keep thin features thick enough to survive the actual museum viewing distance. Inspect negative space between legs, horns, fins, jaws, and the torso at thumbnail size.
- Baseline static exports contain only meshes and organizational empties. Convert curves and realize Geometry Nodes instances deliberately when the required output is ordinary meshes. Preserve the editable source where helpful.
- Closed solid body parts should be manifold and outward-facing. A disconnected assembly is not automatically an error. Intentional openings, mouth cavities, open fins, and overlapping anatomical parts need explicit visual review; do not use watertightness as an unconditional pass/fail for every model.
- Set flat shading explicitly, export normals, and verify the final GLB. glTF triangulates polygons; flat edges can split vertices. A Blender face count is not a shipping triangle or vertex count. Intentional smooth eye or joint surfaces can be documented exceptions.
- Bake/apply object scale for ordinary unique static meshes. Avoid negative scale at export and confirm face winding. Keep a stable asset root and named semantic parts. Object origins may remain meaningful for editing, while the asset root defines museum placement.

## Coordinate and scale conventions

Blender authoring coordinates are X lateral, -Y animal forward, Z up. The Blender 4.3.2 glTF exporter maps `(x, y, z)` to `(x, z, -y)` with `export_yup=True`. Thus animal front becomes glTF +Z. Set `scene.unit_settings.system='METRIC'` and `scale_length=1.0`; build geometry numerically in meters rather than expecting a unit label to repair arbitrary geometry.

Grounded animals have lowest intended contact point at Z=0 in Blender and Y=0 in GLB, within an explicit tolerance. Root (0,0,0) is the center of the intended footprint, not the center of the entire bounding box or the tail tip. Flying/swimming assets need a declared alternate mounting origin. Use a neutral orientation fixture when changing exporter versions.

## Materials and color

Use one Principled BSDF connected to Material Output for baseline parts. Prefer 4–8 palette colors per animal, metallic 0, roughness around 0.7–1.0, alpha 1, and no emission unless required by the brief. These values are artistic defaults. Keep Principled extension-triggering inputs at defaults unless a supported extension is intended. Inspect `extensionsUsed` after export instead of assuming no extensions were written.

Palette hex colors are sRGB; Blender node color sockets and glTF baseColorFactor are linear. Convert each sRGB channel `c`: `c/12.92` when `c <= 0.04045`, otherwise `((c+0.055)/1.055)**2.4`. Do not assign hex/255 directly to linear node sockets. GLTFLoader already handles glTF color roles; do not re-convert loaded material colors or mark normal/roughness textures sRGB.

For closed meshes enable Blender material backface culling to export single-sided material. Do not hide reversed normals by making every material double-sided. Intentional thin sheets can be double-sided if measured and documented. Avoid procedural-only shaders; bake the result to supported textures if genuinely needed. Normal maps, when used, are tangent-space +Y with non-color data. Color/emission textures are sRGB; metallic/roughness/occlusion/normal textures are data.

## Instances and runtime cost

Linked Blender mesh data can reduce unique geometry storage but ordinary glTF nodes still cost separate rendering unless the runtime batches/instances them. Do not equate linked copies with automatic GPU instancing. `EXT_mesh_gpu_instancing` is supported by current GLTFLoader, but pin the actual Three.js version and test it. Blender exporter restrictions and material variations need their own fixture before enabling it.

For the simplest static baseline, keep `export_gpu_instances=False` and realize procedural instances. Share reusable props at the application level where useful. Primitive count is a useful baseline draw-call estimate, not the total frame cost: shadows, multipass rendering, transparency, culling, and instancing change the actual count. Measure `renderer.info.render.calls` and triangles after rendering the complete scene.

## Starting budgets to validate

First-pack art-direction bands are T1 250–700, T2 700–1,400, T3 1,400–2,600 exported triangles. These are design targets; fewer triangles may be better and justified exceptions can be accepted. Use 2–5 structurally meaningful palette groups when possible. The helper’s default 12,000-triangle error ceiling is a broad safety limit, not the target.

Primitive and byte budgets remain configurable. A texture-free ordinary GLB should usually be comfortably under 1 MB, but visual correctness comes first. Measure the real combined scene and renderer draw calls instead of predicting frame rate from triangle count alone.

## Explicit Blender 4.3.2 static exporter baseline

Call after selecting only EXPORT root and descendants:

```python
bpy.ops.export_scene.gltf(
    filepath=out_glb,
    export_format='GLB',
    use_selection=True,
    export_yup=True,
    export_apply=True,
    export_normals=True,
    export_texcoords=False,       # set True for a texture-bearing profile
    export_tangents=False,        # reconsider for normal-mapped profile
    export_materials='EXPORT',
    export_vertex_color='NONE',   # set MATERIAL when deliberately used
    export_animations=False,
    export_skins=False,
    export_morph=False,
    export_cameras=False,
    export_lights=False,
    export_extras=True,
    export_gpu_instances=False,
    export_gn_mesh=False,
    export_draco_mesh_compression_enable=False,
    export_use_gltfpack=False,
)
```

These option names were read from the actual Blender 4.3.2 RNA. Fail clearly on a missing required option rather than silently filtering all unknown keys. `export_apply` evaluates modifiers; it is not permission to destructively alter the editable source. Do not use this static profile for rigged/morph assets without changing it.

## Preview preset and visual acceptance

Prefer Cycles CPU for a headless-safe reference render; Eevee requires working graphics support and should first be smoke-tested. Use orthographic camera for front, side, rear; a 35-degree azimuth / 25-degree elevation 3/4 hero and its reverse; fixed soft key/fill/rim areas; transparent PNG and/or neutral background. Keep stage, camera, lights, and labels outside EXPORT. Preserve the `.blend` source before creating temporary preview helpers.

A high-quality Blender image cannot certify Three.js appearance. Render the shipped GLB in a fixed Three.js scene with a documented renderer version, tone mapping, exposure, output color space, light/environment settings, and camera. For color diagnosis use known palette swatches and an unlit diagnostic pass; do not try to correct a transfer-function error by arbitrarily changing lights. Use Standard/None Look, exposure 0 and gamma 1 for this pack. Browser tone mapping still need not match pixel-for-pixel.

Review: silhouette, species-defining proportions, head/limb readability, clean joins, no accidental holes or intersections, tail/feet not cropped, grounded contact, deliberate faceting, no unwanted bright/specular faces, no flipped faces, front orientation, real-world scale, and no preview stage accidentally exported.

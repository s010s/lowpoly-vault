# Sources and observed facts

Research date: 2026-10-16. Official documentation describes the format/API; project-specific aesthetic and budget choices are recommendations, not requirements from these sources.

- Blender glTF manual: https://docs.blender.org/manual/en/5.1/addons/import_export/scene_gltf2.html . Material/export capabilities, Y-up setting, evaluated modifier export, and instancing options. Version 5.1 documentation is not proof that a flag exists in 4.3; local RNA was checked separately.
- Blender 4.3 manual, indexed official localized copy: https://docs.blender.org/manual/sl/4.3/addons/import_export/scene_gltf2.html . Backface culling controls the inverse of glTF doubleSided. Direct fetch failed during this research; official search indexing provided the relevant passage.
- Blender mesh API: https://docs.blender.org/api/current/bpy.types.Mesh.html . `from_pydata` is efficient direct construction; mesh input validation remains the caller's responsibility. Flat shading uses face normals. The installed 4.3.2 signature was independently probed.
- Blender glTF mesh notes: https://docs.blender.org/manual/en/3.2/addons/import_export/scene_gltf2.html . Export triangulates quads/ngons, and flat shading/UV seams can increase exported vertex count. These stable concepts were checked against the installed exporter and fixture rather than treating older docs as current API signatures.
- glTF specification and registry: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html and https://registry.khronos.org/glTF/ . glTF uses right-handed coordinates, Y up, asset front +Z, and meters. Core material factors and attribute semantics govern runtime interchange.
- Khronos validator: https://github.com/KhronosGroup/glTF-Validator . Official validator checks container/schema/references/buffer values and reports JSON issues/statistics. It does not certify aesthetic quality or species anatomy.
- Three.js GLTFLoader: https://threejs.org/docs/pages/GLTFLoader . Supported extensions include `EXT_mesh_gpu_instancing`; Draco/Meshopt/texture compression can need decoder setup. Test the pinned app version rather than relying on today's support list.
- Three.js color management: https://threejs.org/manual/pages/color-management.html . Rendering works in linear-sRGB; color textures and display outputs use sRGB conventions, while data textures do not. GLTFLoader should interpret glTF materials rather than applying blanket color corrections.
- Three.js Box3: https://threejs.org/docs/pages/Box3.html . World-matrix-aware bounds enable imported size/origin tests. Update ancestor/world matrices before computing bounds.
- Three.js WebGLRenderer: https://threejs.org/docs/pages/WebGLRenderer.html . Renderer statistics expose runtime cost. Output color space, tone mapping, exposure, and rendering passes need explicit viewer settings.

## Actual local runtime evidence

`/usr/bin/blender --version` returned `Blender 4.3.2`. `bpy.app.build_options.cycles` was True. Exporter module path: `/usr/share/blender/scripts/addons_core/io_scene_gltf2/__init__.py`. `Mesh.from_pydata` signature: `(self, vertices, edges, faces, shade_flat=True)`.

Installed exporter source `blender/exp/nodes.py` lines 529–530 and `blender/com/gltf2_blender_math.py` lines 82–84 map location `(x,y,z)` to `(x,z,-y)` when Y-up is enabled. These are installed official implementation observations, not claims derived from an unofficial tutorial.

The smoke-test fixture and its report record what this exact runtime actually exported. The fixture is a plain asymmetric wedge for QA, not a museum asset. The research does not assert that Khronos validation or a browser preview ran unless a corresponding result is present.

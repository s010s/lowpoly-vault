"""Read-only Blender inspection for one frozen Blend; writes JSON evidence only."""
import bpy
import json
import math
import sys
from mathutils import Vector


args = sys.argv[sys.argv.index("--") + 1 :]
if len(args) != 3:
    raise SystemExit("usage: blender -b asset.blend --python read_blend_readonly.py -- ASSET_ID EXPECTED_GLB_SHA OUTPUT_JSON")
asset_id, expected_glb_sha, output_path = args
collection = bpy.data.collections.get("EXPORT")
if collection is None:
    raise SystemExit("EXPORT collection missing")
depsgraph = bpy.context.evaluated_depsgraph_get()
rows = []
triangles = 0
vertices = 0
mins = [math.inf, math.inf, math.inf]
maxs = [-math.inf, -math.inf, -math.inf]
used_materials = set()
positive_determinants = True
for obj in sorted(collection.all_objects, key=lambda x: x.name):
    if obj.type != "MESH":
        continue
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    mesh.calc_loop_triangles()
    ntri = len(mesh.loop_triangles)
    triangles += ntri
    vertices += len(mesh.vertices)
    determinant = eval_obj.matrix_world.to_3x3().determinant()
    positive_determinants &= determinant > 0
    for mat in mesh.materials:
        if mat:
            used_materials.add(mat.name)
    obj_min = [math.inf, math.inf, math.inf]
    obj_max = [-math.inf, -math.inf, -math.inf]
    for vertex in mesh.vertices:
        co = eval_obj.matrix_world @ vertex.co
        for i in range(3):
            obj_min[i] = min(obj_min[i], co[i])
            obj_max[i] = max(obj_max[i], co[i])
            mins[i] = min(mins[i], co[i])
            maxs[i] = max(maxs[i], co[i])
    rows.append({
        "object": obj.name,
        "vertices": len(mesh.vertices),
        "triangles": ntri,
        "world_bounds_m": {"min": obj_min, "max": obj_max},
        "world_matrix_determinant": determinant,
    })
    eval_obj.to_mesh_clear()

payload = {
    "asset_id": asset_id,
    "expected_glb_sha256": expected_glb_sha,
    "blender_version": bpy.app.version_string,
    "unit_scale_length": bpy.context.scene.unit_settings.scale_length,
    "export_collection_found": True,
    "source_scene_cameras_lights": [o.name for o in bpy.data.objects if o.type in {"CAMERA", "LIGHT"}],
    "mesh_objects": len(rows),
    "evaluated_authored_vertices": vertices,
    "evaluated_triangles": triangles,
    "used_material_names": sorted(used_materials),
    "positive_world_determinants": positive_determinants,
    "bounds_blender_m": {"min": mins, "max": maxs, "size": [maxs[i] - mins[i] for i in range(3)]},
    "objects": rows,
    "read_only": True,
    "saved": False,
}
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("READ_ONLY_BLEND_AUDIT", json.dumps(payload, ensure_ascii=False))

import bpy, hashlib, json, os, sys
from mathutils import Vector

args = sys.argv[sys.argv.index('--') + 1:]
source, report_path = args
bpy.ops.wm.open_mainfile(filepath=source)
depsgraph = bpy.context.evaluated_depsgraph_get()
meshes = []
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    points = [obj.matrix_world @ v.co for v in obj.data.vertices]
    if points:
        lo = [min(p[i] for p in points) for i in range(3)]
        hi = [max(p[i] for p in points) for i in range(3)]
    else:
        lo, hi = [None] * 3, [None] * 3
    eval_obj = obj.evaluated_get(depsgraph)
    eval_mesh = eval_obj.to_mesh()
    eval_points = [eval_obj.matrix_world @ v.co for v in eval_mesh.vertices]
    if eval_points:
        eval_lo = [min(p[i] for p in eval_points) for i in range(3)]
        eval_hi = [max(p[i] for p in eval_points) for i in range(3)]
    else:
        eval_lo, eval_hi = [None] * 3, [None] * 3
    meshes.append({
        'name': obj.name,
        'authored_vertices': len(obj.data.vertices),
        'authored_edges': len(obj.data.edges),
        'authored_faces': len(obj.data.polygons),
        'evaluated_vertices': len(eval_mesh.vertices),
        'evaluated_edges': len(eval_mesh.edges),
        'evaluated_faces': len(eval_mesh.polygons),
        'materials': len(obj.data.materials),
        'bounds_min': lo,
        'bounds_max': hi,
        'evaluated_bounds_min': eval_lo,
        'evaluated_bounds_max': eval_hi,
        'modifier_count': len(obj.modifiers),
    })
    eval_obj.to_mesh_clear()
with open(source, 'rb') as f:
    digest = hashlib.sha256(f.read()).hexdigest()
report = {
    'source_path': os.path.realpath(source),
    'source_sha256': digest,
    'blender_version': bpy.app.version_string,
    'library_count': len(bpy.data.libraries),
    'external_image_count': len([x for x in bpy.data.images if x.source == 'FILE']),
    'scene_count': len(bpy.data.scenes),
    'object_count': len(bpy.data.objects),
    'mesh_objects': meshes,
}
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2, sort_keys=True)
print('QA_SOURCE_REOPEN=' + json.dumps(report, sort_keys=True))

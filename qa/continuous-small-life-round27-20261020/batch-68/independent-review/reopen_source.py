import bpy, hashlib, json, os, sys
from mathutils import Vector

args = sys.argv[sys.argv.index('--') + 1:]
source, report_path = args
bpy.ops.wm.open_mainfile(filepath=source)
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
    meshes.append({
        'name': obj.name,
        'vertices': len(obj.data.vertices),
        'edges': len(obj.data.edges),
        'faces': len(obj.data.polygons),
        'materials': len(obj.data.materials),
        'bounds_min': lo,
        'bounds_max': hi,
    })
with open(source, 'rb') as f:
    digest = hashlib.sha256(f.read()).hexdigest()
report = {
    'source_path': os.path.realpath(source),
    'source_sha256': digest,
    'blender_version': bpy.app.version_string,
    'scene_count': len(bpy.data.scenes),
    'object_count': len(bpy.data.objects),
    'mesh_objects': meshes,
}
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2, sort_keys=True)
print('QA_SOURCE_REOPEN=' + json.dumps(report, sort_keys=True))

"""Non-mutating source .blend mesh audit for batch-07 exact candidates.

Run with Blender, pointing it at the frozen .blend and passing a JSON output path
after `--`. It only reads the file; it never saves or edits it.
"""
import bpy
import bmesh
import hashlib
import json
import math
import sys
from pathlib import Path
from mathutils import Vector

args = sys.argv[sys.argv.index('--') + 1:]
if len(args) != 1:
    raise SystemExit('expected one JSON output path after --')
out = Path(args[0])
source = Path(bpy.data.filepath).resolve()
collection = bpy.data.collections.get('EXPORT')
if collection is None:
    raise RuntimeError('missing EXPORT collection')
root_name = collection.get('asset_root')
root = bpy.data.objects.get(root_name) if root_name else None
if root is None:
    raise RuntimeError('missing EXPORT.asset_root')
depsgraph = bpy.context.evaluated_depsgraph_get()
parts = []
lo = [math.inf] * 3
hi = [-math.inf] * 3
for obj in collection.all_objects:
    if obj.type != 'MESH':
        continue
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    mesh.calc_loop_triangles()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    local_areas = [poly.area for poly in mesh.polygons]
    for vert in mesh.vertices:
        p = evaluated.matrix_world @ vert.co
        for axis in range(3):
            lo[axis] = min(lo[axis], p[axis])
            hi[axis] = max(hi[axis], p[axis])
    parts.append({
        'name': obj.name,
        'authored_vertices': len(obj.data.vertices),
        'evaluated_vertices': len(mesh.vertices),
        'evaluated_triangles': len(mesh.loop_triangles),
        'nonfinite_positions': sum(not all(math.isfinite(c) for c in vert.co) for vert in mesh.vertices),
        'nonfinite_normals': sum(not all(math.isfinite(c) for c in vert.normal) for vert in mesh.vertices),
        'nonpositive_polygon_areas': sum(area <= 0 for area in local_areas),
        'boundary_edges': sum(edge.is_boundary for edge in bm.edges),
        'nonmanifold_edges': sum(not edge.is_manifold for edge in bm.edges),
        'world_matrix': [list(row) for row in evaluated.matrix_world],
    })
    bm.free()
    evaluated.to_mesh_clear()
if not parts:
    raise RuntimeError('EXPORT collection contains no mesh objects')
scene_objects = list(bpy.context.scene.objects)
report = {
    'source_path': str(source),
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'blender_version': bpy.app.version_string,
    'export_collection': 'EXPORT',
    'root_world_matrix': [list(row) for row in root.matrix_world],
    'world_bounds_blender_m': {'min': lo, 'max': hi, 'size': [hi[i] - lo[i] for i in range(3)]},
    'parts': parts,
    'totals': {
        'authored_vertices': sum(p['authored_vertices'] for p in parts),
        'evaluated_vertices': sum(p['evaluated_vertices'] for p in parts),
        'evaluated_triangles': sum(p['evaluated_triangles'] for p in parts),
        'boundary_edges': sum(p['boundary_edges'] for p in parts),
        'nonmanifold_edges': sum(p['nonmanifold_edges'] for p in parts),
        'nonfinite_positions': sum(p['nonfinite_positions'] for p in parts),
        'nonfinite_normals': sum(p['nonfinite_normals'] for p in parts),
        'nonpositive_polygon_areas': sum(p['nonpositive_polygon_areas'] for p in parts),
    },
    'scene_camera_count': sum(obj.type == 'CAMERA' for obj in scene_objects),
    'scene_light_count': sum(obj.type == 'LIGHT' for obj in scene_objects),
    'source_saved': False,
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
if any(report['totals'][key] for key in ('nonfinite_positions', 'nonfinite_normals', 'nonpositive_polygon_areas')):
    raise RuntimeError('invalid source geometry detected')

import argparse
import hashlib
import json
import sys
from pathlib import Path
import bpy
from mathutils import Vector

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def mesh_summary(objects):
    meshes = [obj for obj in objects if obj.type == 'MESH']
    depsgraph = bpy.context.evaluated_depsgraph_get()
    triangles = 0
    materials = set()
    bounds = []
    for obj in meshes:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        mesh.calc_loop_triangles()
        triangles += len(mesh.loop_triangles)
        for material in mesh.materials:
            if material:
                materials.add(material.name)
        for corner in obj.bound_box:
            bounds.append(obj.matrix_world @ Vector(corner))
        evaluated.to_mesh_clear()
    if bounds:
        mins = [min(v[k] for v in bounds) for k in range(3)]
        maxs = [max(v[k] for v in bounds) for k in range(3)]
    else:
        mins = maxs = []
    return {
        'object_count': len(objects),
        'mesh_count': len(meshes),
        'triangles': triangles,
        'materials': sorted(materials),
        'bounds_blender_xyz_m': {
            'min': mins,
            'max': maxs,
            'size': [maxs[k] - mins[k] for k in range(3)] if mins else [],
        },
    }

args = sys.argv[sys.argv.index('--') + 1:]
p = argparse.ArgumentParser()
p.add_argument('--source', required=True, type=Path)
p.add_argument('--glb', required=True, type=Path)
p.add_argument('--output', required=True, type=Path)
a = p.parse_args(args)
source = a.source.resolve()
glb = a.glb.resolve()
output = a.output.resolve()

bpy.ops.wm.open_mainfile(filepath=str(source))
source_objects = list(bpy.context.scene.objects)
source_summary = mesh_summary(source_objects)
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(glb))
imported_objects = [obj for obj in bpy.data.objects if obj not in before]
import_summary = mesh_summary(imported_objects)
result = {
    'schema_version': 1,
    'kind': 'blender_source_reopen_and_glb_import_audit',
    'blender_version': bpy.app.version_string,
    'source': {
        'path': str(source),
        'sha256': digest(source),
        'summary': source_summary,
    },
    'glb': {
        'path': str(glb),
        'sha256': digest(glb),
        'bytes': glb.stat().st_size,
        'imported_objects': [obj.name for obj in imported_objects],
        'summary': import_summary,
    },
    'status': 'pass' if import_summary['mesh_count'] > 0 and import_summary['triangles'] > 0 else 'fail',
    'limitation': 'Blender source reopen and clean-import structural audit; visual inspection is recorded separately.',
}
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'glb_sha256': result['glb']['sha256'], 'mesh_count': import_summary['mesh_count'], 'triangles': import_summary['triangles'], 'materials': import_summary['materials'], 'bounds': import_summary['bounds_blender_xyz_m']}))

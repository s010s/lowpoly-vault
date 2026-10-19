#!/usr/bin/env python3
"""Open frozen Blend sources, then clean-import each exact GLB for comparison."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def bounds(points):
    if not points:
        raise ValueError('No mesh vertices found')
    return {
        'min': [min(p[i] for p in points) for i in range(3)],
        'max': [max(p[i] for p in points) for i in range(3)],
    }


def material_color(material):
    if material and material.use_nodes:
        node = next((node for node in material.node_tree.nodes if node.type == 'BSDF_PRINCIPLED'), None)
        if node and 'Base Color' in node.inputs:
            return [round(float(v), 9) for v in node.inputs['Base Color'].default_value]
    return [round(float(v), 9) for v in material.diffuse_color] if material else None


def inspect_objects(objects):
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    points, triangles, polygons, vertices = [], 0, 0, 0
    mesh_objects, used_materials, per_material = [], {}, {}
    for obj in objects:
        if obj.type != 'MESH':
            continue
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        try:
            mesh.calc_loop_triangles()
            triangles += len(mesh.loop_triangles)
            polygons += len(mesh.polygons)
            vertices += len(mesh.vertices)
            points.extend(evaluated.matrix_world @ v.co for v in mesh.vertices)
            names = []
            for material in mesh.materials:
                if material:
                    key = material.name.removesuffix('.001')
                    used_materials[key] = material_color(material)
                    per_material[key] = per_material.get(key, 0) + 1
                    names.append(key)
            mesh_objects.append({'name': obj.name, 'materials': names})
        finally:
            evaluated.to_mesh_clear()
    return {
        'mesh_objects': len(mesh_objects),
        'vertices': vertices,
        'polygon_faces': polygons,
        'triangles': triangles,
        'bounds': bounds(points),
        'materials_linear_rgba': dict(sorted(used_materials.items())),
        'material_slot_assignments': dict(sorted(per_material.items())),
        'mesh_object_names': [row['name'] for row in mesh_objects],
    }


def size(b):
    return [b['max'][i] - b['min'][i] for i in range(3)]


def main():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('--pairs', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    raw_pairs = json.loads(args.pairs.read_text())
    pairs = raw_pairs.get('assets', raw_pairs) if isinstance(raw_pairs, dict) else raw_pairs
    report = {
        'schema_version': 1,
        'kind': 'independent_blender_source_glb_import_audit',
        'started_at_utc': datetime.now(timezone.utc).isoformat(),
        'blender_version': bpy.app.version_string,
        'limitations': [
            'Geometry, world-space bounds, mesh counts and Principled base colors are compared; this does not prove anatomy or artistic quality.',
            'Blender maps imported glTF Y-up/+Z-forward back to Blender Z-up/-Y-forward; bounds are compared in Blender coordinates.',
            'Separate closed mesh parts can overlap intentionally; no fused-solid or printability claim is made.'
        ],
        'assets': [],
    }
    bpy.context.preferences.filepaths.use_scripts_auto_execute = False
    for pair in pairs:
        blend, glb = Path(pair['blend']).resolve(), Path(pair['glb']).resolve()
        blend_hash, glb_hash = digest(blend), digest(glb)
        bpy.ops.wm.open_mainfile(filepath=str(blend), load_ui=False, use_scripts=False)
        marked = [collection for collection in bpy.data.collections if collection.get('asset_root')]
        if len(marked) != 1:
            raise RuntimeError(f"{pair['asset_id']}: expected one asset_root collection, got {len(marked)}")
        source = inspect_objects(list(marked[0].all_objects))
        expected_blender_bounds = source['bounds']
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.context.view_layer.update()
        bpy.ops.import_scene.gltf(filepath=str(glb))
        imported = inspect_objects(list(bpy.context.scene.objects))
        actual_bounds = imported['bounds']
        bound_delta = max(abs(actual_bounds[side][axis] - expected_blender_bounds[side][axis])
                          for side in ('min', 'max') for axis in range(3))
        source_colors, imported_colors = source['materials_linear_rgba'], imported['materials_linear_rgba']
        shared = sorted(set(source_colors) & set(imported_colors))
        color_delta = {name: max(abs(a - b) for a, b in zip(source_colors[name], imported_colors[name]))
                       for name in shared}
        color_keys_match = set(source_colors) == set(imported_colors)
        color_pass = color_keys_match and len(color_delta) == len(source_colors) and all(v <= 1e-6 for v in color_delta.values())
        if digest(blend) != blend_hash or digest(glb) != glb_hash:
            raise RuntimeError(f"{pair['asset_id']}: an input changed during inspection")
        report['assets'].append({
            'asset_id': pair['asset_id'],
            'revision': pair['revision'],
            'blend': {'path': str(blend), 'bytes': blend.stat().st_size, 'sha256': blend_hash},
            'glb': {'path': str(glb), 'bytes': glb.stat().st_size, 'sha256': glb_hash},
            'source_export_collection': marked[0].name,
            'source_mesh_audit': source,
            'clean_imported_glb_audit': imported,
            'source_expected_blender_bounds_m': expected_blender_bounds,
            'imported_glb_bounds_max_abs_delta_m': bound_delta,
            'triangle_count_matches': source['triangles'] == imported['triangles'],
            'bounds_match_within_0_1mm': bound_delta <= 0.0001,
            'source_imported_material_names_match': color_keys_match,
            'source_imported_base_color_max_abs_delta_linear': color_delta,
            'base_colors_match_within_1e-6_linear': color_pass,
            'pass': (source['triangles'] == imported['triangles'] and bound_delta <= 0.0001 and color_pass),
        })
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    report['status'] = 'pass' if all(a['pass'] for a in report['assets']) else 'fail'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise FileExistsError(args.output)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + '\n')
    print(json.dumps({'status': report['status'], 'output': str(args.output), 'assets': len(report['assets'])}, indent=2))
    if report['status'] != 'pass':
        raise RuntimeError('Independent Blend/GLB comparison failed')


if __name__ == '__main__':
    main()

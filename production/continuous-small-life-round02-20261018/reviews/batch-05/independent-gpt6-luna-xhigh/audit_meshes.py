"""Read-only Blender comparison of frozen source blends and exact GLBs."""
import bpy
import bmesh
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HANDOFF = ROOT / "production/continuous-small-life-round02-20261018/work/batch-05/HANDOFF.json"
AREA_LIMIT_M2 = 1e-14
WELD_EPSILON_M = 1e-8

def inspect(objects=None):
    deps = bpy.context.evaluated_depsgraph_get()
    triangle_count = 0
    unique_positions = set()
    areas = []
    sizes = [[], [], []]
    raw_boundary = 0
    raw_nonmanifold = 0
    welded_boundary = 0
    welded_nonmanifold = 0
    mesh_count = 0
    for obj in objects if objects is not None else bpy.context.scene.objects:
        if obj.type != "MESH":
            continue
        mesh_count += 1
        evaluated = obj.evaluated_get(deps).to_mesh()
        bm = bmesh.new()
        bm.from_mesh(evaluated)
        bm.transform(obj.matrix_world)
        bmesh.ops.triangulate(bm, faces=list(bm.faces), quad_method="BEAUTY", ngon_method="BEAUTY")
        triangle_count += len(bm.faces)
        for vert in bm.verts:
            for i in range(3):
                sizes[i].append(float(vert.co[i]))
            unique_positions.add(tuple(round(float(c), 7) for c in vert.co))
        for edge in bm.edges:
            if len(edge.link_faces) == 1:
                raw_boundary += 1
            elif len(edge.link_faces) != 2:
                raw_nonmanifold += 1
        areas.extend(face.calc_area() for face in bm.faces)
        welded = bm.copy()
        bmesh.ops.remove_doubles(welded, verts=list(welded.verts), dist=WELD_EPSILON_M)
        bmesh.ops.recalc_face_normals(welded, faces=list(welded.faces))
        welded_boundary += sum(len(edge.link_faces) == 1 for edge in welded.edges)
        welded_nonmanifold += sum(len(edge.link_faces) != 2 for edge in welded.edges)
        welded.free()
        bm.free()
        obj.to_mesh_clear()
    if not areas:
        raise RuntimeError("No mesh geometry found")
    return {
        "meshes": mesh_count,
        "triangles": triangle_count,
        "positions": unique_positions,
        "bounds_m": [max(axis)-min(axis) for axis in sizes],
        "min_area_m2": min(areas),
        "below_area_limit": sum(area < AREA_LIMIT_M2 for area in areas),
        "zero_area": sum(area == 0 for area in areas),
        "raw_boundary": raw_boundary,
        "raw_nonmanifold": raw_nonmanifold,
        "welded_boundary": welded_boundary,
        "welded_nonmanifold": welded_nonmanifold,
    }

handoff = json.loads(HANDOFF.read_text())
all_ok = True
for entry in handoff["assets"]:
    name = entry["asset_id"]
    blend_path = ROOT / entry["blend"]["path"]
    glb_path = ROOT / entry["glb"]["path"]
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    export_collection = bpy.data.collections.get("EXPORT")
    if export_collection is None:
        raise RuntimeError(f"{name}: source blend has no EXPORT collection")
    source = inspect(export_collection.all_objects)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb_path))
    glb = inspect()
    same_positions = source["positions"] == glb["positions"]
    ok = (
        source["triangles"] == entry["triangles"] == glb["triangles"]
        and len(source["positions"]) == entry["source_authored_vertices"]
        and same_positions
        and source["below_area_limit"] == glb["below_area_limit"] == 0
        and source["zero_area"] == glb["zero_area"] == 0
        and source["welded_boundary"] == glb["welded_boundary"] == 0
        and source["welded_nonmanifold"] == glb["welded_nonmanifold"] == 0
    )
    print(
        f"{name}: meshes={source['meshes']}/{glb['meshes']} "
        f"triangles={source['triangles']}/{glb['triangles']} "
        f"unique positions equal@1e-7m={same_positions} ({len(source['positions'])}/{len(glb['positions'])}) "
        f"bounds_m={[round(v, 9) for v in source['bounds_m']]} "
        f"min_triangle_area_m2={source['min_area_m2']:.6g}/{glb['min_area_m2']:.6g} "
        f"area<{AREA_LIMIT_M2:g}={source['below_area_limit']}/{glb['below_area_limit']} "
        f"zero_area={source['zero_area']}/{glb['zero_area']} "
        f"raw_boundary={source['raw_boundary']}/{glb['raw_boundary']} "
        f"welded_boundary={source['welded_boundary']}/{glb['welded_boundary']} "
        f"result={'PASS' if ok else 'FAIL'}"
    )
    all_ok = all_ok and ok
if not all_ok:
    raise SystemExit(1)

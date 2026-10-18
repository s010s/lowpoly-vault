#!/usr/bin/env python3
"""Independently reopen a frozen Blend and import its exact frozen GLB."""
import bpy
import bmesh
import hashlib
import json
import math
import sys
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def objects():
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


def inspect_meshes():
    depsgraph = bpy.context.evaluated_depsgraph_get()
    meshes = objects()
    all_objects = list(bpy.context.scene.objects)
    out = {
        "scene_object_type_counts": {kind: sum(o.type == kind for o in all_objects)
                                     for kind in sorted({o.type for o in all_objects})},
        "mesh_objects": len(meshes),
        "authored_vertices": 0,
        "evaluated_vertices": 0,
        "triangles": 0,
        "materials": set(),
        "world_bounds": None,
        "boundary_edges": 0,
        "nonmanifold_edges": 0,
        "degenerate_triangles": 0,
        "positive_determinants": True,
        "negative_or_zero_determinant_objects": [],
        "object_details": [],
    }
    low = [math.inf, math.inf, math.inf]
    high = [-math.inf, -math.inf, -math.inf]
    for obj in meshes:
        out["authored_vertices"] += len(obj.data.vertices)
        out["materials"].update(m.name for m in obj.data.materials if m)
        det = obj.matrix_world.to_3x3().determinant()
        if det <= 0:
            out["positive_determinants"] = False
            out["negative_or_zero_determinant_objects"].append({"object": obj.name, "determinant": det})
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        try:
            mesh.calc_loop_triangles()
            out["evaluated_vertices"] += len(mesh.vertices)
            out["triangles"] += len(mesh.loop_triangles)
            bm = bmesh.new()
            try:
                bm.from_mesh(mesh)
                for edge in bm.edges:
                    linked = len(edge.link_faces)
                    if linked == 1:
                        out["boundary_edges"] += 1
                    elif linked != 2:
                        out["nonmanifold_edges"] += 1
            finally:
                bm.free()
            for tri in mesh.loop_triangles:
                area = tri.area
                if not math.isfinite(area) or area <= 1e-14:
                    out["degenerate_triangles"] += 1
            obj_low = [math.inf, math.inf, math.inf]
            obj_high = [-math.inf, -math.inf, -math.inf]
            for vertex in mesh.vertices:
                p = eval_obj.matrix_world @ vertex.co
                for axis in range(3):
                    low[axis] = min(low[axis], p[axis])
                    high[axis] = max(high[axis], p[axis])
                    obj_low[axis] = min(obj_low[axis], p[axis])
                    obj_high[axis] = max(obj_high[axis], p[axis])
            out["object_details"].append({
                "name": obj.name,
                "vertices": len(mesh.vertices),
                "triangles": len(mesh.loop_triangles),
                "materials": sorted(m.name for m in mesh.materials if m),
                "world_bounds": {
                    "min": obj_low,
                    "max": obj_high,
                    "size": [obj_high[i] - obj_low[i] for i in range(3)],
                },
            })
        finally:
            eval_obj.to_mesh_clear()
    if meshes:
        out["world_bounds"] = {"min": low, "max": high, "size": [high[i] - low[i] for i in range(3)]}
    out["materials"] = sorted(out["materials"])
    out["material_count"] = len(out["materials"])
    return out


def clear_mesh_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for coll in list(bpy.data.collections):
        if coll.name != "Collection" and coll.users == 0:
            bpy.data.collections.remove(coll)


def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 4:
        raise SystemExit("usage: blender -b --python reopen_compare_blend_glb.py -- ASSET_ID BLEND GLB OUTPUT_JSON")
    asset_id, blend_path, glb_path, out_path = args
    blend_path, glb_path, out_path = map(lambda x: str(Path(x).resolve()), (blend_path, glb_path, out_path))
    report = {
        "asset_id": asset_id,
        "blender_version": bpy.app.version_string,
        "blend": {"path": blend_path, "sha256": sha256(blend_path)},
        "glb": {"path": glb_path, "sha256": sha256(glb_path)},
    }
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    report["source"] = inspect_meshes()
    clear_mesh_scene()
    bpy.ops.import_scene.gltf(filepath=glb_path)
    report["imported_glb"] = inspect_meshes()
    a, b = report["source"], report["imported_glb"]
    report["checks"] = {
        "triangle_count_matches": a["triangles"] == b["triangles"],
        "material_count_matches": a["material_count"] == b["material_count"],
        "world_bounds_match_1e-5": all(
            abs(a["world_bounds"]["min"][i] - b["world_bounds"]["min"][i]) <= 1e-5
            and abs(a["world_bounds"]["max"][i] - b["world_bounds"]["max"][i]) <= 1e-5
            for i in range(3)
        ),
        "source_has_no_degenerate_triangles": a["degenerate_triangles"] == 0,
    }
    report["status"] = "pass" if all(report["checks"].values()) else "fail"
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

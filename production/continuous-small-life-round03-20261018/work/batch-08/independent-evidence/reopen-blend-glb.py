"""Read-only independent reopen/import audit for frozen Batch 08 artifacts.

Run inside Blender with --disable-autoexec and a JSON manifest containing
asset_id, blend, glb and expected triangle count for each item.
"""
import bpy
import bmesh
import hashlib
import json
import math
import sys
from pathlib import Path
from mathutils import Vector


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def mesh_stats(objects):
    meshes = [obj for obj in objects if obj.type == "MESH"]
    tris = verts = faces = 0
    materials = set()
    lows = [math.inf, math.inf, math.inf]
    highs = [-math.inf, -math.inf, -math.inf]
    bad_normals = nonmanifold_edges = 0
    boundary_edges = overlinked_edges = 0
    boundary_keys = []
    for obj in meshes:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        mesh.calc_loop_triangles()
        tris += len(mesh.loop_triangles)
        verts += len(mesh.vertices)
        faces += len(mesh.polygons)
        materials.update(m.name for m in mesh.materials if m)
        for v in mesh.vertices:
            p = evaluated.matrix_world @ v.co
            for i, value in enumerate(p):
                lows[i] = min(lows[i], value)
                highs[i] = max(highs[i], value)
            if not all(math.isfinite(float(n)) for n in v.normal):
                bad_normals += 1
        bm = bmesh.new()
        bm.from_mesh(mesh)
        nonmanifold_edges += sum(not edge.is_manifold for edge in bm.edges)
        for edge in bm.edges:
            linked = len(edge.link_faces)
            if linked == 1:
                boundary_edges += 1
                points = []
                for vert in edge.verts:
                    point = evaluated.matrix_world @ vert.co
                    points.append(tuple(round(float(value), 6) for value in point))
                boundary_keys.append(tuple(sorted(points)))
            elif linked > 2:
                overlinked_edges += 1
        bm.free()
        evaluated.to_mesh_clear()
    if not meshes:
        bounds = None
    else:
        bounds = {"min": lows, "max": highs, "size": [highs[i] - lows[i] for i in range(3)]}
    paired_keys = sum(1 for count in __import__("collections").Counter(boundary_keys).values() if count == 2)
    unpaired_keys = sum(1 for count in __import__("collections").Counter(boundary_keys).values() if count == 1)
    overpaired_keys = sum(1 for count in __import__("collections").Counter(boundary_keys).values() if count > 2)
    return {
        "mesh_objects": len(meshes), "vertices": verts, "faces": faces,
        "triangles": tris, "materials": sorted(materials), "bounds_m": bounds,
        "nonfinite_vertex_normals": bad_normals,
        "nonmanifold_edges": nonmanifold_edges,
        "boundary_edges": boundary_edges,
        "coincident_boundary_edge_pairs": paired_keys,
        "unpaired_boundary_edge_keys": unpaired_keys,
        "overpaired_boundary_edge_keys": overpaired_keys,
        "edges_with_more_than_two_faces": overlinked_edges,
    }


def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 2:
        raise RuntimeError("expected: -- MANIFEST.json OUTPUT.json")
    manifest_path, output_path = map(Path, args)
    items = json.loads(manifest_path.read_text())
    results = []
    for item in items:
        blend = Path(item["blend"]).resolve()
        glb = Path(item["glb"]).resolve()
        bpy.ops.wm.open_mainfile(filepath=str(blend), load_ui=False)
        export_collection = bpy.data.collections.get("EXPORT")
        if export_collection is None:
            raise RuntimeError(f"{item['asset_id']}: missing EXPORT collection")
        source = mesh_stats(export_collection.all_objects)
        source_digest = sha256(blend)

        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(glb))
        imported = mesh_stats(bpy.context.scene.objects)
        glb_digest = sha256(glb)
        differences = []
        if source["triangles"] != imported["triangles"]:
            differences.append("source and GLB triangle counts differ")
        if source["bounds_m"] is None or imported["bounds_m"] is None:
            differences.append("source or GLB contains no mesh geometry")
        else:
            for axis in range(3):
                for side in ("min", "max"):
                    if abs(source["bounds_m"][side][axis] - imported["bounds_m"][side][axis]) > 1e-5:
                        differences.append(f"source and GLB bounds differ on {side}[{axis}]")
        if source["triangles"] != item["expected_triangles"]:
            differences.append("source triangle count differs from handoff")
        if imported["triangles"] != item["expected_triangles"]:
            differences.append("GLB triangle count differs from handoff")
        if source["nonfinite_vertex_normals"] or source["nonmanifold_edges"]:
            differences.append("source geometry has nonfinite normals or nonmanifold edges")
        if imported["nonfinite_vertex_normals"]:
            differences.append("imported GLB has nonfinite vertex normals")
        results.append({
            "asset_id": item["asset_id"],
            "blend_sha256": source_digest, "glb_sha256": glb_digest,
            "source": source, "glb_import": imported,
            "differences": differences, "status": "pass" if not differences else "fail",
        })
    output = {
        "check": "fresh Blender 4.3.2 source reopen and exact GLB clean import",
        "blender_version": bpy.app.version_string,
        "autoexec_disabled_by_command": True,
        "inputs": str(manifest_path),
        "assets": results,
        "status": "pass" if all(x["status"] == "pass" for x in results) else "fail",
    }
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


main()

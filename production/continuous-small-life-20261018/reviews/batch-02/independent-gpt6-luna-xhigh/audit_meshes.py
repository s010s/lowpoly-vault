"""Read-only Blender audit of source blend files and the exact frozen GLBs."""
import bpy
import bmesh
import os
import sys

NAMES = ("longipteryx", "urasterella", "alienopterus", "aglaophyton")
AREA_LIMIT = 1e-14
WELD_EPSILON_M = 1e-8

def inspect_scene():
    deps = bpy.context.evaluated_depsgraph_get()
    tris = 0
    areas = []
    unique_positions = set()
    bounds = [[], [], []]
    boundary = 0
    nonmanifold = 0
    welded_boundary = 0
    welded_nonmanifold = 0
    mesh_count = 0
    for obj in bpy.context.scene.objects:
        if obj.type != "MESH":
            continue
        mesh_count += 1
        ev = obj.evaluated_get(deps).to_mesh()
        bm = bmesh.new()
        bm.from_mesh(ev)
        bm.transform(obj.matrix_world)
        bmesh.ops.triangulate(bm, faces=list(bm.faces), quad_method="BEAUTY", ngon_method="BEAUTY")
        tris += len(bm.faces)
        for vert in bm.verts:
            for axis in range(3):
                bounds[axis].append(float(vert.co[axis]))
            unique_positions.add(tuple(round(float(c), 7) for c in vert.co))
        for edge in bm.edges:
            if len(edge.link_faces) == 1:
                boundary += 1
            elif len(edge.link_faces) != 2:
                nonmanifold += 1
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
    size = [max(axis) - min(axis) for axis in bounds]
    return {
        "meshes": mesh_count,
        "triangles": tris,
        "vertices": len(unique_positions),
        "positions": unique_positions,
        "bounds": size,
        "min_area": min(areas),
        "below_limit": sum(area < AREA_LIMIT for area in areas),
        "zero_area": sum(area == 0 for area in areas),
        "boundary": boundary,
        "nonmanifold": nonmanifold,
        "welded_boundary": welded_boundary,
        "welded_nonmanifold": welded_nonmanifold,
    }

root = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "assets/candidates/continuous-small-life-20261018/batch-02/r001"
all_ok = True
for name in NAMES:
    bpy.ops.wm.open_mainfile(filepath=os.path.join(root, name, name + ".blend"))
    source = inspect_scene()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.join(root, name, name + ".glb"))
    glb = inspect_scene()
    same_positions = source["positions"] == glb["positions"]
    ok = (
        source["triangles"] == glb["triangles"]
        and source["vertices"] == glb["vertices"]
        and same_positions
        and source["below_limit"] == 0
        and glb["below_limit"] == 0
        and source["zero_area"] == 0
        and glb["zero_area"] == 0
        and source["welded_boundary"] == 0
        and glb["welded_boundary"] == 0
        and source["welded_nonmanifold"] == 0
        and glb["welded_nonmanifold"] == 0
    )
    print(
        f"{name}: blend/glb meshes={source['meshes']}/{glb['meshes']} "
        f"triangles={source['triangles']}/{glb['triangles']} "
        f"unique-position sets equal={same_positions} ({source['vertices']}/{glb['vertices']}) "
        f"bounds_m={[round(v, 9) for v in source['bounds']]} "
        f"min_triangle_area_m2={source['min_area']:.6g}/{glb['min_area']:.6g} "
        f"area<{AREA_LIMIT:g}={source['below_limit']}/{glb['below_limit']} "
        f"zero_area={source['zero_area']}/{glb['zero_area']} "
        f"raw_boundary_edges={source['boundary']}/{glb['boundary']} "
        f"welded_boundary_edges={source['welded_boundary']}/{glb['welded_boundary']} "
        f"result={'PASS' if ok else 'FAIL'}"
    )
    all_ok = all_ok and ok
if not all_ok:
    raise SystemExit(1)

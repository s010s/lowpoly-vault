"""Render the four frozen GLBs together at their authored meter scale.

This is review evidence only. It imports the exact frozen exports; it does not
change their mesh, material, transforms, metadata, budgets, or release state.
"""
from pathlib import Path
import hashlib
import json
import math
import sys

import bpy
from mathutils import Vector


ROOT = next(p for p in Path(__file__).resolve().parents if (p / "scripts/asset_common.py").exists())
OUT = ROOT / "qa/continuous-small-life-20261018/batch-03/independent-review"
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if argv:
    OUT = Path(argv[0]).resolve()
OUT.mkdir(parents=True, exist_ok=True)

ASSET_ROOT = ROOT / "assets/candidates/continuous-small-life-20261018/batch-03"
IDS = ["cephalaspis", "saccocoma", "archaeocidaris", "onoclea"]

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)


def object_bounds(objects):
    corners = [obj.matrix_world @ Vector(corner) for obj in objects if obj.type == "MESH" for corner in obj.bound_box]
    return Vector((min(p.x for p in corners), min(p.y for p in corners), min(p.z for p in corners))), Vector((max(p.x for p in corners), max(p.y for p in corners), max(p.z for p in corners)))


records = []
staged = []
for asset_id in IDS:
    revision = "r002" if asset_id == "onoclea" else "r001"
    glb = ASSET_ROOT / asset_id / revision / asset_id / f"{asset_id}.glb"
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(glb))
    imported = list(set(bpy.data.objects) - before)
    lo, hi = object_bounds(imported)
    dims = hi - lo
    glb_hash = hashlib.sha256(glb.read_bytes()).hexdigest()
    # The fish's 22 cm body axis points along Blender Y. Turn it in the review
    # layout so its true length can be compared horizontally with the patch.
    turn_z = math.pi / 2 if asset_id == "cephalaspis" else 0.0
    display_dims = Vector((dims.y, dims.x, dims.z)) if turn_z else dims.copy()
    staged.append((asset_id, revision, glb, imported, lo, hi, dims, display_dims, turn_z, glb_hash))

gap_m = 0.10
label_column_min_m = 0.24
total_width = sum(max(row[7].x, label_column_min_m) for row in staged) + gap_m * (len(staged) - 1)
cursor = -total_width / 2
for asset_id, revision, glb, imported, lo, hi, dims, display_dims, turn_z, glb_hash in staged:
    center_x = (lo.x + hi.x) / 2
    column_width = max(display_dims.x, label_column_min_m)
    target_center_x = cursor + column_width / 2
    root = bpy.data.objects.new(f"Review placement {asset_id}", None)
    bpy.context.collection.objects.link(root)
    for obj in imported:
        old_world = obj.matrix_world.copy()
        obj.parent = root
        obj.matrix_world = old_world
    root.rotation_euler.z = turn_z
    root.location.x = target_center_x
    records.append({
        "id": asset_id,
        "revision": revision,
        "glb": str(glb.relative_to(ROOT)),
        "glb_sha256": glb_hash,
        "dimensions_m": [round(dims.x, 6), round(dims.y, 6), round(dims.z, 6)],
        "review_layout_center_x_m": round(target_center_x, 6),
        "geometry_transform": "meter scale preserved; translation only, with cephalaspis rotated 90 degrees around Z for presentation",
    })
    cursor += column_width + gap_m

# Neutral ground and a 10 cm bar make the shared physical scale visible.
ground_mat = bpy.data.materials.new("Review neutral ground")
ground_mat.diffuse_color = (0.78, 0.80, 0.73, 1)
ground_mat.use_nodes = True
ground_mat.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.78, 0.80, 0.73, 1)
ground_mat.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = 1.0
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, -0.001))
ground = bpy.context.object
ground.name = "Review ground"
ground.scale = (max(total_width + .2, 1.0), .72, 1)
ground.data.materials.append(ground_mat)

# Scale bar: 0.10 m long, with 0.05 m end ticks.
bar_y = -0.29
bar_z = 0.002
scale_center_x = -total_width / 2 + .07
bar_start = scale_center_x - 0.05
bar_end = scale_center_x + 0.05
def add_bar_line(name, p1, p2, radius=.0014):
    mid = (Vector(p1) + Vector(p2)) / 2
    direction = Vector(p2) - Vector(p1)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=radius, depth=direction.length, location=mid)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = direction.to_track_quat("Z", "Y")
    obj.data.materials.append(ground_mat)
    return obj

add_bar_line("10 cm scale bar", (bar_start, bar_y, bar_z), (bar_end, bar_y, bar_z))
for ix, x in enumerate((bar_start, 0, bar_end)):
    add_bar_line(f"5 cm tick {ix}", (x, bar_y - .009, bar_z), (x, bar_y + .009, bar_z))

text_mat = bpy.data.materials.new("Review label ink")
text_mat.diffuse_color = (.13, .17, .14, 1)
text_mat.use_nodes = True
text_nodes = text_mat.node_tree.nodes
text_nodes.get("Principled BSDF").inputs["Base Color"].default_value = (.13, .17, .14, 1)
text_nodes.get("Principled BSDF").inputs["Roughness"].default_value = 1.0

def add_label(name, body, x, y, z, size):
    font = bpy.data.curves.new(name, "FONT")
    font.body = body
    font.size = size
    font.align_x = "CENTER"
    label = bpy.data.objects.new(name, font)
    bpy.context.collection.objects.link(label)
    label.location = (x, y, z)
    label.rotation_euler.x = math.pi / 2
    label.data.materials.append(text_mat)
    return label

add_label("Review scale label", "10 cm", scale_center_x, bar_y, .13, .026)

for row in records:
    add_label(f"Label {row['id']}", row["id"], row["review_layout_center_x_m"], -.315, .035, .026)

world = bpy.data.worlds.new("Review world")
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (.82, .84, .80, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = .28

def area(name, loc, energy, size):
    light_data = bpy.data.lights.new(name, "AREA")
    light_data.energy = energy
    light_data.shape = "DISK"
    light_data.size = size
    light = bpy.data.objects.new(name, light_data)
    bpy.context.collection.objects.link(light)
    light.location = loc
    light.rotation_euler = (Vector((0, 0, .15)) - light.location).to_track_quat("-Z", "Y").to_euler()

area("Large soft key", (-.7, -1.1, 1.8), 40, 1.3)
area("Soft fill", (1.5, -.1, 1.0), 20, 1.5)

camera_data = bpy.data.cameras.new("Review camera")
camera = bpy.data.objects.new("Review camera", camera_data)
bpy.context.collection.objects.link(camera)
camera.location = (0, -2.4, .72)
target = Vector((0, -.02, .22))
camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
camera_data.type = "ORTHO"
camera_data.ortho_scale = max(total_width + .3, 1.65)
camera_data.lens = 45
scene = bpy.context.scene
scene.camera = camera
scene.render.engine = "CYCLES"
scene.cycles.samples = 32
scene.cycles.use_denoising = False
scene.render.resolution_x = 1920
scene.render.resolution_y = 960
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
scene.view_settings.exposure = -0.6
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.render.filepath = str(OUT / "true-relative-scale.png")
scene.render.image_settings.color_mode = "RGBA"
scene.camera.data.dof.use_dof = False
bpy.ops.render.render(write_still=True)

(OUT / "true-relative-scale.json").write_text(json.dumps({
    "scope": "Exact GLB import in Blender 4.3.2 at preserved authored meter scale; side-by-side translation only, no mesh scaling.",
    "camera": "orthographic, shared frame for all four assets",
    "scale_bar_m": 0.10,
    "assets": records,
}, indent=2) + "\n")
print(json.dumps(records, indent=2))

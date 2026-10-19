#!/usr/bin/env python3
"""Measure the exported Pteraspis caudal lobe endpoints after clean Blender GLB import."""
import bpy
import hashlib
import json
import sys

glb = sys.argv[sys.argv.index("--") + 1]
digest = hashlib.sha256(open(glb, "rb").read()).hexdigest()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
matches = [obj for obj in bpy.context.scene.objects if "hypocercal-caudal" in obj.name.lower()]
if len(matches) != 1:
    raise RuntimeError(f"Expected one caudal mesh; got {[obj.name for obj in matches]}")
mesh = matches[0]
points = [mesh.matrix_world @ vertex.co for vertex in mesh.data.vertices]
root_y = min(point.y for point in points)  # Blender +Y is the rearward direction for this fish.
upper = max(points, key=lambda point: point.z)
lower = min(points, key=lambda point: point.z)
result = {
    "asset_id": "pteraspis",
    "glb_sha256": digest,
    "clean_import_object": mesh.name,
    "coordinate_note": "Blender import convention: fish forward is -Y, so +Y is tailward; +Z is dorsal.",
    "caudal_root_y_m": root_y,
    "upper_lobe_apex": {"y_m": upper.y, "z_m": upper.z, "tailward_extent_from_root_m": upper.y - root_y},
    "lower_lobe_apex": {"y_m": lower.y, "z_m": lower.z, "tailward_extent_from_root_m": lower.y - root_y},
    "lower_lobe_extends_farther_rearward_by_m": lower.y - upper.y,
    "scope": "Verifies the model's stated lower-lobe-larger design cue in this export; it does not validate the scientific ratio for a specimen reconstruction.",
}
print(json.dumps(result, indent=2))

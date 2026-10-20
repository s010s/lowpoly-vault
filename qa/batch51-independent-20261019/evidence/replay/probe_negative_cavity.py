"""Independent Blender ray probe of the hash-pinned Conichnus GLB.

Run only through Blender 4.3.2, with the GLB path after ``--``:
  blender -b --factory-startup --disable-autoexec --python-exit-code 1 \
    --python qa/batch51-independent-20261019/evidence/replay/probe_negative_cavity.py \
    -- assets/candidates/continuous-small-life-round17-20261018/batch-51/\
conichnus-conical-burrow/r001/conichnus-conical-burrow.glb

The script imports the GLB into a disposable scene and prints JSON only. It
does not save or edit the GLB or Blend source.
"""
import hashlib
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


args = sys.argv[sys.argv.index("--") + 1 :]
if len(args) != 1:
    raise SystemExit("Expected one GLB path after --")
glb = Path(args[0]).resolve()
digest = hashlib.sha256(glb.read_bytes()).hexdigest()
expected = "34948b0738264195544dd24ff377a1b0f3b92a93a1e34ab07d66647235388042"
if digest != expected:
    raise SystemExit(f"Unexpected GLB hash: {digest}")

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(glb))
bpy.context.view_layer.update()
depsgraph = bpy.context.evaluated_depsgraph_get()
hits = []
for x in (0.0, 0.01, 0.02, 0.03, 0.04, 0.05):
    hit, point, normal, face_index, obj, matrix = bpy.context.scene.ray_cast(
        depsgraph, Vector((x, 0.0, 0.30)), Vector((0.0, 0.0, -1.0)), distance=1.0
    )
    hits.append(
        {
            "x_m": x,
            "hit": bool(hit),
            "hit_position_blender_xyz_m": [float(v) for v in point] if hit else None,
            "normal": [float(v) for v in normal] if hit else None,
        }
    )

z = [entry["hit_position_blender_xyz_m"][2] for entry in hits if entry["hit"]]
if len(z) != len(hits) or any(b <= a for a, b in zip(z, z[1:])):
    raise SystemExit("Expected six ray hits and a monotonically rising cavity wall")
result = {
    "status": "pass",
    "glb_sha256": digest,
    "blender_version": bpy.app.version_string,
    "method": "Independent downward raycasts against freshly imported exact GLB in temporary Blender scene.",
    "hits": hits,
    "center_depth_below_outer_top_m": z[-1] - z[0],
    "below_base_substrate_m": z[0],
    "wall_rises_monotonically_toward_opening": True,
    "negative_cavity_confirmed": z[0] < 0.04 and z[-1] > 0.13,
}
if not result["negative_cavity_confirmed"]:
    raise SystemExit("Cavity depth did not meet the independent threshold")
print("BATCH51_RAY_PROBE_JSON=" + json.dumps(result, separators=(",", ":")))

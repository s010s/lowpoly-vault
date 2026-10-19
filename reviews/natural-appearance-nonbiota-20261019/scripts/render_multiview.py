#!/usr/bin/env python3
"""Render six fixed color views from the exact pinned review GLBs.

Run with Blender from the repository root:
  blender -b --factory-startup --python-exit-code 1 \
    --python reviews/natural-appearance-nonbiota-20261019/scripts/render_multiview.py -- \
    /tmp/lowpoly-natural-review/render-inputs.json \
    /tmp/lowpoly-natural-review/renders
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from asset_common import link_object, render_previews, setup_scene  # noqa: E402


def main() -> None:
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 2:
        raise SystemExit("expected INPUTS_JSON OUTPUT_DIR")
    input_path, output_root = Path(args[0]), Path(args[1])
    inputs = json.loads(input_path.read_text())
    output_root.mkdir(parents=True, exist_ok=True)
    rows = []
    views = ("hero", "reversehero", "front", "side", "rear", "top")
    for index, item in enumerate(inputs, 1):
        asset = item["asset_id"]
        out = output_root / asset
        out.mkdir(parents=True, exist_ok=True)
        collection = setup_scene("review-" + asset)
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=item["input_path"])
        imported = [obj for obj in bpy.data.objects if obj not in before]
        for obj in imported:
            link_object(obj, collection, parent=False)
        files = render_previews(collection, out, views=views, resolution=512, samples=8, transparent=False)
        rows.append({
            **item,
            "renderer": "Blender Cycles CPU",
            "blender_version": bpy.app.version_string,
            "resolution_per_view_px": [512, 512],
            "samples": 8,
            "views": list(views),
            "rendered_files": [Path(f).name for f in files],
        })
        print(json.dumps({"progress": f"{index}/{len(inputs)}", "asset_id": asset, "views": len(files)}, ensure_ascii=False), flush=True)
    (output_root / "render-manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"assets_rendered": len(rows), "views_per_asset": len(views), "total_views": len(rows) * len(views), "blender": bpy.app.version_string}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()

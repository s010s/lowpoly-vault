#!/usr/bin/env python3
"""Compose one 512px-per-view six-angle sheet for each pinned GLB."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews/natural-appearance-nonbiota-20261019"
LABELS = ["Hero 3/4", "Opposite 3/4", "Front", "Side", "Rear", "Top"]
SIZE = 512
GUTTER = 16
HEADER = 46
LABEL_H = 32
BG = (236, 233, 225)
INK = (38, 43, 40)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    args = __import__("sys").argv[1:]
    if len(args) != 2:
        raise SystemExit("expected BLENDER_RENDER_MANIFEST OUTPUT_DIR")
    manifest_path, output_dir = Path(args[0]), Path(args[1])
    rows = json.loads(manifest_path.read_text())
    render_root = manifest_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    out_rows = []
    sheet_w = GUTTER * 4 + SIZE * 3
    sheet_h = HEADER + LABEL_H * 2 + SIZE * 2 + GUTTER * 3
    for row in rows:
        asset = row["asset_id"]
        image = Image.new("RGB", (sheet_w, sheet_h), BG)
        draw = ImageDraw.Draw(image)
        title = f"{asset}  |  {row['batch']} {row['revision']}  |  GLB {row['sha256'][:12]}"
        draw.text((GUTTER, 10), title, fill=INK, font=title_font)
        for i, (filename, label) in enumerate(zip(row["rendered_files"], LABELS)):
            col, r = i % 3, i // 3
            x = GUTTER + col * (SIZE + GUTTER)
            y = HEADER + GUTTER + r * (SIZE + LABEL_H + GUTTER)
            with Image.open(render_root / asset / filename) as src:
                frame = src.convert("RGB")
                if frame.size != (SIZE, SIZE):
                    frame = frame.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
                image.paste(frame, (x, y))
            draw.text((x + 8, y + SIZE + 5), label, fill=INK, font=font)
        path = output_dir / f"{asset}.jpg"
        image.save(path, format="JPEG", quality=90, optimize=True, subsampling=0)
        out_rows.append({
            "asset_id": asset,
            "batch": row["batch"],
            "revision": row["revision"],
            "source_commit": row["source_commit"],
            "source_ref": row["source_ref"],
            "source_model_path": row["model_path"],
            "source_glb_sha256": row["sha256"],
            "image_path": path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix(),
            "image_sha256": sha(path),
            "image_bytes": path.stat().st_size,
            "image_dimensions_px": list(image.size),
            "render": {
                "renderer": row["renderer"],
                "blender_version": row["blender_version"],
                "projection": "orthographic",
                "view_size_px": [SIZE, SIZE],
                "samples": row["samples"],
                "views": row["views"],
            },
        })
    (OUT / "evidence/visual-manifest.json").write_text(json.dumps(out_rows, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"contact_sheets": len(out_rows), "output_dir": str(output_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

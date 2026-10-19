#!/usr/bin/env python3
"""Create lossless 4x4 navigation sheets without resizing any candidate proof frame."""
from hashlib import sha256
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

REPO = Path(__file__).resolve().parents[3]
ASSET_ROOT = REPO / "assets/candidates/undersea-invertebrates-concept-20261019"
OUT = Path(__file__).resolve().parent / "full-res-review-sheets"
ASSETS = [("mackenzia", "r001"), ("prasopora", "r003"), ("strophomena", "r003"), ("ctenoimbricata", "r001")]
VIEW_NAMES = ["hero", "reversehero", "front", "rear", "left", "right", "top", "bottom", "clay", "clayalt", "wire", "detail", "silhouette"] + [f"turntable-{i:03d}" for i in range(24)]
CELL_W, CELL_H, LABEL_H, COLS, ROWS = 512, 540, 28, 4, 4

def file_sha(path):
    h = sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

OUT.mkdir(parents=True, exist_ok=True)
manifest = {"schema_version": 1, "method": "Lossless 4x4 contact sheets. Each proof PNG is pasted at its native 512x512 pixels without scaling; sheets are navigation aids, and canonical frames remain unchanged.", "assets": []}
for asset, revision in ASSETS:
    proof = ASSET_ROOT / asset / revision / "proof"
    frame_rows = []
    for name in VIEW_NAMES:
        path = proof / f"{name}.png"
        if not path.is_file():
            raise FileNotFoundError(path)
        with Image.open(path) as im:
            if im.size != (512, 512):
                raise ValueError(f"Expected 512x512 frame, got {im.size}: {path}")
            im.verify()
        frame_rows.append({"name": name, "path": path.relative_to(REPO).as_posix(), "sha256": file_sha(path), "size_px": [512, 512]})
    sheet_records = []
    for page in range(3):
        subset = frame_rows[page * COLS * ROWS:(page + 1) * COLS * ROWS]
        canvas = Image.new("RGB", (COLS * CELL_W, ROWS * CELL_H), "white")
        draw = ImageDraw.Draw(canvas)
        for i, record in enumerate(subset):
            col, row = i % COLS, i // COLS
            x, y = col * CELL_W, row * CELL_H
            draw.text((x + 8, y + 5), f"{record['name']}  |  {record['sha256'][:12]}", fill=(25, 25, 25))
            with Image.open(REPO / record["path"]) as im:
                canvas.paste(im.convert("RGB"), (x, y + LABEL_H))
        out = OUT / f"{asset}-{page + 1:02d}.png"
        canvas.save(out, format="PNG", optimize=True)
        sheet_records.append({"path": out.relative_to(REPO).as_posix(), "sha256": file_sha(out), "size_px": list(canvas.size), "frames": [x["name"] for x in subset]})
    manifest["assets"].append({"asset_id": asset, "revision": revision, "frames": frame_rows, "sheets": sheet_records})
manifest_path = Path(__file__).resolve().parent / "full-res-review-sheets.json"
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"assets": len(manifest["assets"]), "frames": sum(len(x["frames"]) for x in manifest["assets"]), "sheets": sum(len(x["sheets"]) for x in manifest["assets"]), "manifest": manifest_path.relative_to(REPO).as_posix()}, indent=2))

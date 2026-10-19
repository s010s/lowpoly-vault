#!/usr/bin/env python3
"""Summarize pixels and create compact contact sheets from independent renders."""
import hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[5]
QA = Path(__file__).resolve().parents[1]
OUT = QA / "evidence/contact-sheets"
OUT.mkdir(parents=True, exist_ok=True)
IDS = ["diplomoceras", "nelumbo", "marine-terrace", "angular-unconformity-outcrop"]
BG = (232, 228, 220)
FONT = ImageFont.load_default()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stats(path, source=False, silhouette=False):
    image = Image.open(path).convert("RGBA")
    width, height = image.size
    px = list(image.getdata())
    if source and not silhouette and any(a < 255 for _, _, _, a in px):
        foreground = sum(a > 8 for _, _, _, a in px)
        rule = "alpha>8"
    else:
        if silhouette:
            foreground = sum(max(r, g, b) < 245 for r, g, b, a in px)
            rule = "silhouette RGB max<245"
        else:
            foreground = sum(max(abs(r-BG[0]), abs(g-BG[1]), abs(b-BG[2])) > 18 for r, g, b, a in px)
            rule = "distance from #E8E4DC >18"
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path), "bytes": path.stat().st_size,
            "width": width, "height": height, "foreground_pixels": foreground,
            "total_pixels": width*height, "foreground_fraction": round(foreground/(width*height), 6),
            "coverage_rule": rule}

def contact_sheet(items, path, title):
    tile_w, tile_h, image_w = 288, 302, 256
    cols = 4
    rows = (len(items) + cols - 1)//cols
    sheet = Image.new("RGB", (cols*tile_w, 42 + rows*tile_h), "#F2EFE8")
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 12), title, fill="#26353A", font=FONT)
    for i, (label, file, silhouette) in enumerate(items):
        x, y = (i%cols)*tile_w+16, 42+(i//cols)*tile_h
        image = Image.open(file).convert("RGBA")
        matte = Image.new("RGBA", image.size, (255,255,255,255) if silhouette else (*BG,255))
        matte.alpha_composite(image)
        image = matte.convert("RGB")
        image.thumbnail((image_w,image_w), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (tile_w-24, image_w), (255,255,255))
        canvas.paste(image, ((canvas.width-image.width)//2, (canvas.height-image.height)//2))
        sheet.paste(canvas, (x,y))
        draw.text((x, y+image_w+5), label, fill="#26353A", font=FONT)
    sheet.save(path, quality=90, optimize=True)

report = {"schema_version": 1, "check": "independent_render_pixel_review_evidence", "coverage_is_diagnostic_only": True, "assets": []}
for asset in IDS:
    source_dir = QA / "evidence/fixed-views" / asset
    runtime_dir = QA / "evidence/runtime" / asset
    source_names = ["hero", "reversehero", "front", "side", "rear", "top", "clay", "silhouette"]
    runtime_names = ["single-hero", "single-reversehero", "single-front", "single-side", "single-rear", "single-top", "single-bottom",
                     "single-80px", "single-160px", "single-240px", "scene-hero", "scene-top"]
    source_items, runtime_items = [], []
    source_pixels, runtime_pixels = [], []
    for name in source_names:
        file = source_dir / f"preview-{name}.png"
        source_items.append((name, file, name == "silhouette"))
        source_pixels.append(stats(file, source=True, silhouette=name == "silhouette"))
    for name in runtime_names:
        file = runtime_dir / f"{name}.png"
        runtime_items.append((name, file, False))
        runtime_pixels.append(stats(file))
    source_sheet, runtime_sheet = OUT / f"{asset}-source.jpg", OUT / f"{asset}-runtime.jpg"
    contact_sheet(source_items, source_sheet, f"{asset} · fresh Blend source views · 512px / silhouette 128px")
    contact_sheet(runtime_items, runtime_sheet, f"{asset} · fresh GLTFLoader pixels · Chromium / WebGL2 SwiftShader")
    report["assets"].append({"asset_id": asset, "source_fixed_views": source_pixels, "runtime_views": runtime_pixels,
        "source_contact_sheet": {"path": source_sheet.relative_to(ROOT).as_posix(), "sha256": sha(source_sheet), "bytes": source_sheet.stat().st_size},
        "runtime_contact_sheet": {"path": runtime_sheet.relative_to(ROOT).as_posix(), "sha256": sha(runtime_sheet), "bytes": runtime_sheet.stat().st_size}})
out = QA / "evidence/visual-inspection.json"
out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"status": "ready_for_manual_visual_review", "assets": [
    {"asset_id": a["asset_id"], "source_pixels": [v["foreground_fraction"] for v in a["source_fixed_views"]],
     "runtime_pixels": [v["foreground_fraction"] for v in a["runtime_views"]],
     "source_contact_sheet": a["source_contact_sheet"], "runtime_contact_sheet": a["runtime_contact_sheet"]} for a in report["assets"]]}, indent=2))

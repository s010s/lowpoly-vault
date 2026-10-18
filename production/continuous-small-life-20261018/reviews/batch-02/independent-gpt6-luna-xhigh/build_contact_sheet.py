"""Build the independent review contact sheet from frozen source/runtime pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ASSET_ROOT = ROOT / "assets/candidates/continuous-small-life-20261018/batch-02/r001"
OUT = HERE / "contact-sheet.jpg"
NAMES = ("longipteryx", "urasterella", "alienopterus", "aglaophyton")
HEADERS = ("Source hero", "Exact GLB 80px", "Exact GLB 240px", "Exact GLB 360px", "Exact GLB top", "Exact GLB scene · 9 copies")
CELL, ROW_LABEL, HEADER, CAPTION = 192, 116, 32, 22
FONT = ImageFont.load_default()
width = ROW_LABEL + CELL * len(HEADERS)
height = HEADER + len(NAMES) * (CELL + CAPTION)
sheet = Image.new("RGB", (width, height), "#f2f1ed")
draw = ImageDraw.Draw(sheet)
for col, label in enumerate(HEADERS):
    draw.text((ROW_LABEL + col*CELL + 6, 9), label, font=FONT, fill="#263139")

for row, name in enumerate(NAMES):
    source = ASSET_ROOT / name
    runtime = source / "runtime"
    images = [
        source / "preview-hero.png",
        HERE / "runtime80" / name / "runtime" / "small80.png",
        runtime / "normal.png",
        runtime / "near.png",
        runtime / "top.png",
        runtime / "scene.png",
    ]
    labels = ("source", "80 projected px", "240 projected px", "360 projected px", "top at 360 px", "9 copies")
    y = HEADER + row * (CELL + CAPTION)
    draw.rectangle((0, y, ROW_LABEL-1, y+CELL+CAPTION-1), fill="#e3e4e2")
    draw.text((8, y+10), name, font=FONT, fill="#263139")
    for col, (path, caption) in enumerate(zip(images, labels)):
        if not path.is_file():
            raise FileNotFoundError(path)
        im = Image.open(path).convert("RGBA")
        im.thumbnail((CELL-10, CELL-10), Image.Resampling.LANCZOS)
        tile = Image.new("RGBA", (CELL, CELL), "#e8e4dc")
        if path.name == "preview-hero.png":
            tile = Image.new("RGBA", (CELL, CELL), "white")
        tile.alpha_composite(im, ((CELL-im.width)//2, (CELL-im.height)//2))
        x = ROW_LABEL + col * CELL
        sheet.paste(tile.convert("RGB"), (x, y))
        draw.text((x+5, y+CELL+4), caption, font=FONT, fill="#263139")

sheet.save(OUT, quality=93, optimize=True)
print(f"{OUT.relative_to(ROOT)} {OUT.stat().st_size} bytes")

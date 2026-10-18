"""Build a review sheet from frozen source and exact-GLB runtime frames."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[5]
HANDOFF = ROOT / "production/continuous-small-life-round02-20261018/work/batch-05/HANDOFF.json"
OUT = Path(__file__).with_name("batch05-independent-qa-contact-sheet.jpg")
HANDOFF_DATA = json.loads(HANDOFF.read_text())
WIDTH, HEIGHT = 176, 176
LABEL_HEIGHT, ROW_LABEL = 23, 26
HEADERS = ["Source hero", "Source front", "Source side", "Source top",
           "GLB runtime hero", "GLB 80px", "GLB 160px", "GLB 240px",
           "GLB runtime top", "GLB six-copy scene"]
font = ImageFont.load_default()
sheet = Image.new("RGB", (ROW_LABEL + len(HEADERS)*WIDTH, 26 + len(HANDOFF_DATA["assets"])*(HEIGHT+LABEL_HEIGHT)), "#e8e7e3")
draw = ImageDraw.Draw(sheet)
for col, title in enumerate(HEADERS):
    x = ROW_LABEL + col*WIDTH
    draw.text((x+5, 6), title, fill="#273038", font=font)

for row, entry in enumerate(HANDOFF_DATA["assets"]):
    manifest = json.loads((ROOT / entry["view_manifest"]["path"]).read_text())
    frame_by_name = {Path(frame["path"]).name: ROOT / frame["path"] for frame in manifest["frames"]}
    names = ["preview-hero.png", "preview-front.png", "preview-side.png", "preview-top.png",
             "single-hero.png", "single-80px.png", "single-160px.png", "single-240px.png",
             "single-top.png", "scene-hero.png"]
    y = 26 + row*(HEIGHT+LABEL_HEIGHT)
    draw.rectangle((0, y, ROW_LABEL-1, y+HEIGHT+LABEL_HEIGHT-1), fill="#d5d7d7")
    draw.text((3, y+8), entry["asset_id"], fill="#273038", font=font)
    for col, filename in enumerate(names):
        path = frame_by_name[filename]
        image = Image.open(path).convert("RGBA")
        image.thumbnail((WIDTH-8, HEIGHT-8), Image.Resampling.LANCZOS)
        cell = Image.new("RGBA", (WIDTH, HEIGHT), "white")
        cell.alpha_composite(image, ((WIDTH-image.width)//2, (HEIGHT-image.height)//2))
        x = ROW_LABEL + col*WIDTH
        sheet.paste(cell.convert("RGB"), (x, y))
        draw.text((x+4, y+HEIGHT+3), filename.replace(".png", ""), fill="#273038", font=font)

sheet.save(OUT, quality=92, optimize=True)
print(f"{OUT.relative_to(ROOT)} {OUT.stat().st_size} bytes")

"""Preserve compact views of actual independent-viewer browser screenshots."""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw

root = Path('qa/approved-gallery-integration-20261019/final-1e8b5cb4')
source = root / 'redesign-models'
out = root / 'model-contacts'
out.mkdir(exist_ok=True)
manifest = json.load(open('assets/manifest.json'))
found = [(a['id'], source / f"model-{a['id']}-ready.png") for a in manifest['assets']]
found = [(i, p) for i, p in found if p.exists()]
sheets = []
for start in range(0, len(found), 15):
    batch = found[start:start + 15]
    sheet = Image.new('RGB', (1200, math.ceil(len(batch) / 5) * 355), '#e7e3d8')
    draw = ImageDraw.Draw(sheet)
    for n, (model_id, path) in enumerate(batch):
        with Image.open(path) as src:
            # The independent viewer's actual model stage, without downscaling
            # the lengthy metadata column into illegible text.
            im = src.convert('RGB').crop((113, 32, 759, 944))
        im.thumbnail((236, 329))
        x, y = (n % 5) * 240, (n // 5) * 355
        draw.text((x + 3, y + 4), model_id, fill='#202020')
        sheet.paste(im, (x, y + 23))
    name = f'model-contact-{start // 15 + 1:02d}.jpg'
    sheet.save(out / name, quality=90)
    sheets.append({'file': name, 'model_ids': [i for i, _ in batch]})
(out / 'index.json').write_text(json.dumps({'source_sha': '1e8b5cb48f5211fa12a2108861591bc71150fce3',
    'models_captured': len(found), 'published': len(manifest['assets']),
    'description': 'Crops of actual saved browser screenshots, preserving each model stage; no rendered proxies.',
    'sheets': sheets}, indent=2) + '\n')
print(f'{len(found)} model screenshots in {len(sheets)} contact sheets')

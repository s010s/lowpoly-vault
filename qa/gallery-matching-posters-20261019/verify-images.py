"""Decode every new PNG, measure opaque model content, and make review sheets."""
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageStat

ROOT = Path('site/public')
QA = Path('qa/gallery-matching-posters-20261019')
resources = json.loads((ROOT / 'gallery/resources.json').read_text())
baseline = json.loads((ROOT / 'gallery/approved-resources.json').read_text())
ids = [i for i in resources['posters'] if i not in baseline['posters']]
assert len(ids) == 145
old_files = []
for f in baseline['files']:
    data = (ROOT / f['path']).read_bytes()
    assert len(data) == f['bytes']
    assert hashlib.sha256(data).hexdigest() == f['sha256']
    old_files.append({'path': f['path'], 'sha256': f['sha256']})

rows = []
for i in ids:
    for kind, size in [('detail', (512, 512)), ('wheel', (768, 432))]:
        path = ROOT / resources['posters'][i][kind]
        with Image.open(path) as source:
            source.load()
            assert source.format == 'PNG' and source.size == size
            im = source.convert('RGBA')
        alpha = im.getchannel('A')
        # Model surfaces are opaque; soft floor shadows have low alpha.
        mask = alpha.point(lambda a: 255 if a >= 200 else 0)
        box = mask.getbbox()
        count = mask.histogram()[255]
        assert box and count > 100, f'Blank or negligible model: {i} {kind}'
        margin = [box[0], box[1], size[0] - box[2], size[1] - box[3]]
        assert min(margin) > 0, f'Opaque model meets image edge: {i} {kind} {box}'
        stats = ImageStat.Stat(im.convert('RGB'), mask)
        assert max(stats.stddev) > 1, f'Flat content: {i} {kind}'
        rows.append({'id': i, 'kind': kind, 'size': size, 'bytes': path.stat().st_size,
                     'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'opaque_pixels': count, 'opaque_bbox': box, 'edge_margin_px': margin,
                     'rgb_stddev': stats.stddev})

# Each cell shows the actual detail and wheel files on the same neutral ground.
sheets = []
for start in range(0, len(ids), 15):
    subset = ids[start:start + 15]
    sheet = Image.new('RGB', (1140, math.ceil(len(subset) / 3) * 160), '#e5dfd4')
    draw = ImageDraw.Draw(sheet)
    for n, i in enumerate(subset):
        x, y = (n % 3) * 380, (n // 3) * 160
        draw.text((x + 5, y + 3), i, fill='#222222')
        for kind, dx, size in [('detail', 4, (128, 128)), ('wheel', 140, (228, 128))]:
            with Image.open(ROOT / resources['posters'][i][kind]) as src:
                im = src.convert('RGBA').resize(size, Image.Resampling.LANCZOS)
            sheet.paste(im, (x + dx, y + 24), im)
    name = f'contact-{start // 15 + 1:02d}.jpg'
    sheet.save(QA / name, quality=90)
    sheets.append(name)

report = {'decoded_generated_images': len(rows), 'generated_pairs': len(ids),
          'all_nonblank': True, 'all_opaque_bounds_inside_image': True,
          'minimum_opaque_edge_margin_px': min(min(r['edge_margin_px']) for r in rows),
          'baseline_files_byte_identical': old_files, 'images': rows, 'contact_sheets': sheets,
          'limits': 'Opaque alpha bounds exclude soft shadows. Independent actual-vertex projection checks cover geometric clipping, including transparent materials.'}
(QA / 'image-verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k not in ('images', 'baseline_files_byte_identical')}))

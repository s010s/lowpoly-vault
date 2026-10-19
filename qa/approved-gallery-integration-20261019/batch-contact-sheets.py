"""Contact sheets of actual desktop/mobile screenshots from batch regressions."""
import math
from pathlib import Path
from PIL import Image, ImageDraw

root = Path('qa/approved-gallery-integration-20261019/final-1e8b5cb4')
out = root / 'batch-contacts'
out.mkdir(exist_ok=True)
for folder in ['small-life', 'round13', 'live-local-adapter']:
    for prefix in ['desktop', 'mobile', 'touch']:
        images = sorted((root / folder).glob(prefix + '-*.png'))
        if not images:
            continue
        mobile = prefix != 'desktop'
        width, height, columns = (195, 422, 5) if mobile else (400, 278, 3)
        sheet = Image.new('RGB', (columns * width, math.ceil(len(images) / columns) * (height + 24)), '#e6e2d8')
        draw = ImageDraw.Draw(sheet)
        for i, path in enumerate(images):
            with Image.open(path) as original:
                image = original.convert('RGB')
            image.thumbnail((width, height))
            x, y = (i % columns) * width, (i // columns) * (height + 24)
            draw.text((x + 2, y + 4), path.stem.removeprefix(prefix + '-'), fill='#202020')
            sheet.paste(image, (x, y + 24))
        name = f'{folder}-{prefix}.jpg'
        sheet.save(out / name, quality=92)
        print(name, len(images))

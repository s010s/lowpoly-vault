# SPDX-License-Identifier: MIT
"""Encode the original Blender render for the web, without retouching it."""
from pathlib import Path
import hashlib,json
from PIL import Image
root=Path(__file__).resolve().parents[2]
out=root/'site/public/home'
with Image.open(out/'editorial-hero.png') as image:
    image.convert('RGB').save(out/'editorial-hero.webp',format='WEBP',quality=90,method=6)
report_path=out/'editorial-hero.json'
report=json.loads(report_path.read_text())
report['web_encoding']={'format':'WebP','quality':90,'method':6,'retouching':'None',
                        'bytes':(out/'editorial-hero.webp').stat().st_size,
                        'sha256':hashlib.sha256((out/'editorial-hero.webp').read_bytes()).hexdigest()}
report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(report['web_encoding']))

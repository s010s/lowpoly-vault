# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
R=Path.cwd();W=R/'production/continuous-small-life-round24-20261020/work/batch-62'
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path'];man=json.loads((b/'proof-final/render-manifest.json').read_text());im=Image.new('RGB',(2048,1060),'#e8e4dc');d=ImageDraw.Draw(im)
 for i,f in enumerate(man['frames']):
  pic=Image.open(b/'proof-final'/f['path']).convert('RGB');assert pic.size==(512,512);im.paste(pic,((i%4)*512,(i//4)*530+18));d.text(((i%4)*512+8,(i//4)*530+2),f['id'],fill='black')
 im.save(b/'contact-sheet.png')

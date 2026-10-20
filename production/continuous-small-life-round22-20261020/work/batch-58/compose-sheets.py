# SPDX-License-Identifier: MIT
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
R=Path.cwd();W=R/'production/continuous-small-life-round22-20261020/work/batch-58'
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path'];p=b/('proof-final' if (b/'proof-final/render-manifest.json').exists() else 'proof')
 if not (p/'render-manifest.json').exists():continue
 sheet=Image.new('RGB',(2048,1060),'#E8E4DC');d=ImageDraw.Draw(sheet)
 for j,n in enumerate(['hero','reversehero','front','side','rear','top','clay','silhouette']):
  sheet.paste(Image.open(p/(n+'.png')).convert('RGB'),((j%4)*512,(j//4)*530));d.text(((j%4)*512+8,(j//4)*530+512),x['asset_id']+' / '+n,fill='#222222')
 sheet.save(b/'contact-sheet.png');print(x['asset_id'])

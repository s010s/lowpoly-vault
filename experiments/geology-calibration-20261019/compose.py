# SPDX-License-Identifier: MIT
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
H=Path(__file__).resolve().parent
M=json.loads((H/'comparison-metrics.json').read_text())
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def F(n):return ImageFont.truetype(font,n)
for slug,metrics in M.items():
 # Two columns preserve matching physical size, camera, exposure and lighting.
 for mode,views,width,tile in [('comparison',['hero'],1280,640),('all-views',['hero','front','back','clay','top','side','reversehero','thumbnail-scene-240'],960,480)]:
  top=150;row=tile+42;im=Image.new('RGB',(width,top+row*len(views)+54),'#F0EFEB');d=ImageDraw.Draw(im)
  d.text((24,16),slug,font=F(27),fill='#252824')
  for col,version in enumerate(['before','after']):
   q=metrics[version];x=col*(width//2)+24
   d.text((x,58),version.title(),font=F(27),fill='#252824')
   d.text((x,99),f"{q['scene_triangles']:,} triangles | {q['bytes']:,} B GLB",font=F(21),fill='#44483F')
  for r,view in enumerate(views):
   y=top+r*row
   for col,version in enumerate(['before','after']):
    src=Image.open(H/slug/'views'/(version+'-'+view+'.png')).convert('RGB')
    if view.startswith('thumbnail'):
     # 240px remains exact native resolution, never upscaled.
     x=col*(width//2)+(width//2-240)//2;im.paste(src,(x,y+(tile-240)//2))
    else:im.paste(src.resize((tile,tile),Image.Resampling.LANCZOS),(col*tile,y))
   d.text((24,y+tile+6),view,font=F(21),fill='#44483F')
  d.text((24,im.height-36),'Exact GLB renders | fixed pair camera / scale / studio | candidate only',font=F(18),fill='#44483F')
  im.save(H/slug/(mode+'.jpg'),quality=94)

# SPDX-License-Identifier: MIT
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
H=Path(__file__).resolve().parent
old=json.loads((H.parent/'comparison-metrics.json').read_text())['cross-bedded-sandstone'];new=json.loads((H/'cross-bedded-sandstone/qa.json').read_text())['glb']
metrics={'production':old['before'],'previous':old['after'],'new':new}
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def F(n):return ImageFont.truetype(font,n)
for name,views in [('comparison-side',['bedding-side','right-side']),('comparison-hero',['hero']),('comparison-clay',['clay']),('comparison-scene-240',['scene-240'])]:
 small=views==['scene-240'];tile=320 if small else 640;top=150 if not small else 128;row=tile+36
 im=Image.new('RGB',(tile*3,top+len(views)*row+48),'#F0EFEB');d=ImageDraw.Draw(im)
 d.text((22,12),'Sandstone / three frozen GLBs / '+name.replace('comparison-',''),font=F(22 if small else 30),fill='#262B25')
 for col,(version,label) in enumerate([('production','Production / Before'),('previous','Previous candidate'),('new','New textured / R002')]):
  q=metrics[version];x=col*tile+20
  d.text((x,58),label,font=F(18 if small else 28),fill='#262B25')
  d.text((x,92),f"{q['scene_triangles']:,} tri | {q['bytes']:,} B",font=F(16 if small else 23),fill='#44493E')
  if not small:d.text((x,122),f"{q['materials']} material(s) | {q['scene_primitives_estimated_base_draw_calls']} primitive(s)",font=F(20),fill='#44493E')
 for r,view in enumerate(views):
  y=top+r*row
  for col,version in enumerate(metrics):
   src=Image.open(H/'views'/(version+'-'+view+'.png')).convert('RGB')
   x=col*tile+(tile-src.width)//2;im.paste(src,(x,y+(tile-src.height)//2))
  d.text((22,y+tile+6),view,font=F(20),fill='#44493E')
 d.text((22,im.height-32),'Same camera, lights, meter scale; no burial. Original atlas; no photo texture.',font=F(15 if small else 20),fill='#44493E')
 im.save(H/(name+'.jpg'),quality=94)
(H/'three-version-metrics.json').write_text(json.dumps(metrics,indent=2))

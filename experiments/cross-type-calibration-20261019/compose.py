# SPDX-License-Identifier: MIT
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
H=Path(__file__).resolve().parent
B=json.loads((H/'preflight.json').read_text())['before'];font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def F(n):return ImageFont.truetype(font,n)
metrics={}
for slug in ['conglomerate-outcrop','horsetail-cluster']:
 q=json.loads((H/'candidates'/slug/'qa.json').read_text())['glb'];metrics[slug]={'before':B[slug]['actual_glb_metrics'],'candidate':q}
 hero='reversehero' if slug.startswith('conglomerate') else 'hero'
 foot='Six clasts only; original matrix and teaching fracture retained.' if slug.startswith('conglomerate') else 'Three branch tips only; retained control, no defect established.'
 for mode,views,tile in [('comparison',[hero],640),('all-views',['hero','reversehero','front','side','top','clay','scene-240'],480)]:
  top=154;row=tile+36;im=Image.new('RGB',(tile*2,top+row*len(views)+56),'#F0EFEB');d=ImageDraw.Draw(im)
  d.text((22,14),slug,font=F(30),fill='#272D26')
  for col,version,label in [(0,'before','Original'),(1,'candidate','Candidate')]:
   x=col*tile+22;m=metrics[slug][version];d.text((x,56),label,font=F(28),fill='#272D26');d.text((x,95),f"{m['scene_triangles']:,} tri | {m['bytes']:,} B GLB",font=F(22),fill='#454B42');d.text((x,126),f"{m['materials']} materials | {m['unique_mesh_primitives']} primitives | 0 textures",font=F(18),fill='#454B42')
  for r,view in enumerate(views):
   y=top+r*row
   for col,version in enumerate(['before','candidate']):
    src=Image.open(H/'evidence'/slug/(version+'-'+view+'.png')).convert('RGB')
    if view=='scene-240':im.paste(src,(col*tile+(tile-240)//2,y+(tile-240)//2))
    else:im.paste(src.resize((tile,tile),Image.Resampling.LANCZOS),(col*tile,y))
   d.text((22,y+tile+6),view,font=F(21),fill='#454B42')
  d.text((22,im.height-44),foot,font=F(18),fill='#454B42');d.text((22,im.height-22),'Exact GLBs; matched cameras, lights and meter scale. Candidate only.',font=F(16),fill='#454B42')
  im.save(H/(slug+'-'+mode+'.jpg'),quality=94)
(H/'comparison-metrics.json').write_text(json.dumps(metrics,indent=2))

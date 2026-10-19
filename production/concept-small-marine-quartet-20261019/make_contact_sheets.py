# SPDX-License-Identifier: MIT
"""Labeled evidence derivatives only; never gallery posters."""
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
NAMES=['concept-match','hero','reversehero','front','rear','left','right','top','bottom','clay','clayalt','wire']
for s in ['emeraldella','burgessia','tuzoia','sanctacaris']:
 for rev in ['r001','r002']:
  d=HERE/s/rev;proof=d/'proof'
  if not (proof/'render-manifest.json').exists():continue
  out=Image.new('RGB',(1280,1032),'#e8e4dc');draw=ImageDraw.Draw(out)
  for i,n in enumerate(NAMES):
   image=Image.open(proof/(n+'.png')).convert('RGB').resize((320,320));x=i%4*320;y=i//4*344;out.paste(image,(x,y+24));draw.text((x+8,y+5),s+' '+rev+' / '+n,fill='#223340')
  out.save(d/'proof-contact.png')
 if not (HERE/s/'r002/proof/render-manifest.json').exists():continue
 out=Image.new('RGB',(1024,1060),'#e8e4dc');draw=ImageDraw.Draw(out)
 for row,view in enumerate(['concept-match','top']):
  for col,rev in enumerate(['r001','r002']):
   f=HERE/s/rev/'proof'/(view+'.png');out.paste(Image.open(f).convert('RGB'),(col*512,row*530+18));draw.text((col*512+8,row*530+4),s+' '+rev+' '+view,fill='#223340')
 out.save(HERE/s/'r002/revision-comparison.png')

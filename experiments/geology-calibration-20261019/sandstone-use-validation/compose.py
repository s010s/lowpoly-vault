# SPDX-License-Identifier: MIT
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
H=Path(__file__).resolve().parent
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def F(n):return ImageFont.truetype(font,n)
for name,title,placement,caution in [
 ('half-buried-slope','Ground placement: partially buried rock','Bottom buried about 0.15 m; top and side exposure remain visible.','Visible limit: ordered bands and broad cut planes remain; burial is not a shape repair.'),
 ('embedded-bank','Bank placement: rear embedded, bedding face exposed','Rear inserted +0.06 m; curved soil meets lower and side edges.','Visible limit: the insert boundary / cut-fragment character is still assessable.')]:
 im=Image.new('RGB',(1800,990),'#F0EFEB');d=ImageDraw.Draw(im)
 d.text((28,16),title,font=F(32),fill='#282C26')
 for col,version,stats in [(0,'before','588 triangles | 34,128 B'),(1,'after','2,276 triangles | 133,172 B')]:
  x=col*900
  d.text((x+28,66),version.title(),font=F(30),fill='#282C26')
  d.text((x+210,72),stats,font=F(23),fill='#4A4D45')
  im.paste(Image.open(H/(name+'-'+version+'.png')).convert('RGB'),(x,120))
 d.text((28,890),placement,font=F(25),fill='#282C26')
 d.text((28,929),caution,font=F(23),fill='#4A4D45')
 d.text((28,963),'Real frozen GLB renders | same pair terrain / camera / lights | candidate only, no asset edit',font=F(18),fill='#4A4D45')
 im.save(H/(name+'-comparison.jpg'),quality=94)

#!/usr/bin/env python3
"""Collect the unchanged native 128px identification renders into review sheets."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
QA=Path('qa/independent/small-marine-quartet-20261019-gpt6-luna-xhigh/evidence');VIEWS=['hero','front','right','top']
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
assets=[]
for asset,rev in [('emeraldella','r002'),('burgessia','r002'),('tuzoia','r003'),('sanctacaris','r002')]:
 d=QA/'renders-128'/asset;manifest=json.loads((d/'render-manifest.json').read_text());by={x['view']:x for x in manifest['frames']};sheet=Image.new('RGB',(288,288),'#e8e4dc');draw=ImageDraw.Draw(sheet);frames=[]
 for i,view in enumerate(VIEWS):
  p=d/f'{view}.png';f=by[view]
  if sha(p)!=f['sha256']:raise SystemExit(f'{asset}/{view}: hash mismatch')
  with Image.open(p) as image:
   if image.size!=(128,128):raise SystemExit(f'{asset}/{view}: unexpected image size')
   x=(i%2)*144;y=(i//2)*144;sheet.paste(image.convert('RGB'),(x,y+16));draw.text((x+3,y+2),view,fill='#16232b')
  frames.append({'view':view,'path':p.as_posix(),'sha256':f['sha256'],'dimensions':[128,128]})
 out=QA/'renders-128'/f'{asset}-review-sheet.png';sheet.save(out,optimize=True)
 assets.append({'asset_id':asset,'revision':rev,'glb_sha256':manifest['subject']['glb_sha256'],'frames':frames,'sheet':out.as_posix(),'sheet_sha256':sha(out),'sheet_dimensions':[288,288],'frame_pixels_preserved':True})
result={'schema_version':1,'kind':'128px-review-sheets','method':'The original 128×128 renders are shown at native size; labels occupy separate 16px rows.','assets':assets};p=QA/'128px-review-sheet-manifest.json';p.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'pass','assets':len(assets),'output':p.as_posix()},indent=2))

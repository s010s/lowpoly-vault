from pathlib import Path
import json,subprocess,datetime,hashlib
R=Path.cwd();W=R/'production/continuous-small-life-round21-20261020/work/batch-56';final=json.loads((W/'final-selection.json').read_text());bl=['blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
# First runner must finish before this starts to preserve one Blender process.
for a in final:
 b=R/a['path'];args=bl+[str(W/'render-batch56.py'),'--',str(b/'model.glb'),'--revision',a['revision'],'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof-final'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','24']
 with (b/'proof-final.log').open('w') as f:subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=180)
 (b/'preview.png').write_bytes((b/'proof-final/hero.png').read_bytes())
 from PIL import Image,ImageDraw
 sheet=Image.new('RGB',(2048,1064),'#f5f1e9');draw=ImageDraw.Draw(sheet)
 for i,v in enumerate(['hero','reversehero','front','side','rear','top','clay','silhouette']):
  x=(i%4)*512;y=(i//4)*532;sheet.paste(Image.open(b/'proof-final'/f'{v}.png').convert('RGB'),(x,y+20));draw.text((x+8,y+4),a['asset_id']+' '+v,fill='black')
 sheet.save(b/'eight-view-sheet.png');print(a['asset_id'],'canonical8 complete',flush=True)
subprocess.run(['node',str(W/'runtime-parse.mjs')]+[str(R/a['path']) for a in final],check=True)

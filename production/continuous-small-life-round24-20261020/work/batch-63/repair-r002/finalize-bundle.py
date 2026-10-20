# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,subprocess,time,shutil
from PIL import Image,ImageDraw
R=Path.cwd();W=R/'production/continuous-small-life-round24-20261020/work/batch-63/repair-r002';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();F=json.loads((W/'final-selection.json').read_text());bl=['blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
for x in F:
 b=R/x['path'];brief=json.loads((b/'brief.json').read_text());brief['required_deliverables']=[dict(role=k,path=str((b/n).relative_to(R)),sha256=H(b/n)) for k,n in [('generator','generator.py'),('config','build-config.json'),('source','source.blend')]];brief['packaging_adapter']=dict(created_at=now(),frozen_design_brief_sha256=H(b/'brief.json'),note='Post-build deliverable path/hash binding only; frozen geometry design, source claims, view contract and scale unchanged. Fresh proof-bound renders use this exact delivery brief.');(b/'candidate-brief.json').write_text(json.dumps(brief,indent=2)+'\n')
 deps=[b/'generator.py',b/'build-config.json',R/'scripts/asset_common.py',R/'scripts/qa_glb.py',W/'render-fixed8.py'];(b/'build-dependencies.json').write_text(json.dumps(dict(schema_version=1,files={str(p.relative_to(R)):H(p) for p in deps},blender='4.3.2',three='0.180.0',required_external_assets=[],note='Texture-free deterministic generator imports only Blender bpy/mathutils, Python standard library, and pinned asset_common/qa_glb helpers; no unpinned external data.'),indent=2)+'\n')
 #Preserve initial proof under its original prebinding brief identity.
 p=b/'proof-final';p.rename(b/'proof-initial')
 args=bl+[str(W/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision',x['revision'],'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.json'),'--output-dir',str(p),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16'];t=time.monotonic();start=now()
 with (b/'proof-bound.log').open('x') as f:rc=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=600).returncode
 with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps(dict(stage='proof-bound',started_at=start,ended_at=now(),wall_seconds=time.monotonic()-t,exit_code=rc,command=args))+'\n')
 assert rc==0;shutil.copyfile(p/'hero.png',b/'preview.png');sheet=Image.new('RGB',(2048,1060),'#ece8e0');draw=ImageDraw.Draw(sheet)
 for i,name in enumerate(['hero','reversehero','front','side','rear','top','clay','silhouette']):
  im=Image.open(p/(name+'.png')).convert('RGB');assert im.size==(512,512);xx=(i%4)*512;yy=(i//4)*530;sheet.paste(im,(xx,yy+18));draw.text((xx+8,yy+3),name,fill='#25231f')
 sheet.save(b/'contact-sheet.png',compress_level=9);print('BOUND',x['asset_id'],flush=True)
args=bl+[str(W/'count-source-vertices.py')]
with (W/'source-counts.log').open('x') as f:rc=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=180).returncode
assert rc==0

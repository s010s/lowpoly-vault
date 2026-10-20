# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,subprocess,shutil,time
R=Path.cwd();W=R/'production/continuous-small-life-round25-20261020/work/batch-64';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path'];d=json.loads((b/'references.json').read_text());d['no_incorporated_third_party_assets']=True;d['packaging_rights_adapter']={'created_at':now(),'premodel_references_sha256':H(b/'references.json'),'note':'Explicit machine-readable rights fields only. Original references and modeling freeze unchanged; same primary sources, facts and scope. New exact-GLB renders bind this derived ledger; no old pixel relabeling.'}
 for s in d['sources']:
  if s.get('use')=='consulted-only':s.update(incorporated=False,rights_note='Consultation only. No third-party source photo, fossil scan, mesh, texture or other asset incorporated or redistributed.')
 (b/'references.delivery-v001.json').write_text(json.dumps(d,indent=2)+'\n')
 (b/'proof-final').rename(b/'proof-original-ledger');shutil.copyfile(b/'contact-sheet.png',b/'contact-sheet-original-ledger.png');shutil.copyfile(b/'preview.png',b/'preview-original-ledger.png')
 args=['flock','/tmp/lowpoly-production-blender.lock','blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(W/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision',x['revision'],'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.delivery-v001.json'),'--output-dir',str(b/'proof-final'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16'];start=now();t=time.monotonic()
 with (b/'proof-final-delivery-ledger.log').open('x') as f:
  p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT);pid=p.pid;code=p.wait(timeout=600)
 with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps({'stage':'proof-final-delivery-ledger','runner_pid':pid,'command':args,'started_at':start,'ended_at':now(),'wall_seconds':time.monotonic()-t,'exit_code':code})+'\n')
 print(x['asset_id'],code,flush=True);assert code==0;shutil.copyfile(b/'proof-final/hero.png',b/'preview.png')

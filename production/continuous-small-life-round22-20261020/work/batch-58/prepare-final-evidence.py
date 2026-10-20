# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,subprocess,time
R=Path.cwd();W=R/'production/continuous-small-life-round22-20261020/work/batch-58';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path'];d=json.loads((b/'brief.json').read_text());d['packaging_adapter']={'created_at':now(),'frozen_design_brief_sha256':H(b/'brief.json'),'note':'Post-build artifact-path/hash declaration only. Original premodel frozen brief retained unchanged; no concept, design, source, geometry, budget, view or stage-scope change. Not claimed to precede geometry.'};d['required_deliverables']=[{'role':k,'path':str((b/n).relative_to(R)),'sha256':H(b/n)} for k,n in [('source','source.blend'),('generator','generator.py'),('config','build-config.json')]];(b/'candidate-brief.json').write_text(json.dumps(d,indent=2)+'\n')
 args=['blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(W/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision',x['revision'],'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof-final'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16']
 started=now();t=time.monotonic()
 with (b/'proof-final.log').open('w') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=400)
 with (b/'lifecycle.jsonl').open('a') as f:f.write(json.dumps({'stage':'proof-final','started_at':started,'ended_at':now(),'wall_seconds':time.monotonic()-t,'exit_code':p.returncode,'command':args})+'\n')
 print(x['asset_id'],'final-proof',p.returncode,flush=True)
 if p.returncode:raise RuntimeError(x)
 (b/'preview.png').write_bytes((b/'proof-final/hero.png').read_bytes())

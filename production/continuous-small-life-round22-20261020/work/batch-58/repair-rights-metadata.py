# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,subprocess,shutil,time
R=Path.cwd();W=R/'production/continuous-small-life-round22-20261020/work/batch-58';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path'];shutil.copy(b/'references.json',b/'references-premodel.json');d=json.loads((b/'references.json').read_text());d['no_incorporated_third_party_assets']=True;d['packaging_rights_adapter']={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'premodel_references_sha256':H(b/'references-premodel.json'),'note':'Explicit machine-readable rights declaration only. Same consulted sources, feature claims, URLs, scope and geometry; original frozen source ledger retained separately unchanged.'}
 for s in d['sources']:
  if s.get('use')=='consulted-only':s.update(incorporated=False,rights_note='Consulted factual source only. No source media, mesh, texture, palette or other third-party asset incorporated or redistributed.')
 (b/'references.json').write_text(json.dumps(d,indent=2)+'\n');shutil.move(b/'proof-final',b/'proof-prerights');shutil.copy(b/'candidate-validation.json',b/'candidate-validation-prerights-failed.json')
 args=['blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(W/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision',x['revision'],'--brief',str(b/'candidate-brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'proof-final'),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16']
 with (b/'proof-final-rights.log').open('w') as f:subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=400)
 shutil.copy(b/'proof-final/hero.png',b/'preview.png');print(x['asset_id'],'rights+fresh-proof',flush=True)

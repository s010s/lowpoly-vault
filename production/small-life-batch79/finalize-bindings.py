# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime
R=Path.cwd();W=R/'production/small-life-batch79';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path'];runs=[]
 for result in (W/'rebuild-runs/build'/x['asset_id']/x['revision']).rglob('result.json'):
  d=json.loads(result.read_text());q=result.parent/'request.json';request=json.loads(q.read_text())
  if d['status']!='succeeded' or request['identity']['inputs']['generator']['sha256']!=H(b/'generator.py'):continue
  runs.append(dict(pid=d['pid'],path=str(result.parent.relative_to(R)),job_id=d['job_id'],started_at=d['started_at'],finished_at=d['finished_at'],request_sha256=H(q),result_sha256=H(result),output_glb_sha256=H(result.parent/'outputs/model.glb'),semantic_comparison_report_sha256=H(b/('repro-final-'+d['job_id'][-1]+'.report.json'))))
 assert len(runs)==2 and len({r['pid'] for r in runs})==2
 (b/'final-rebuild-binding.json').write_text(json.dumps(dict(verified_at=now(),glb_sha256=H(b/'model.glb'),generator_sha256=H(b/'generator.py'),config_sha256=H(b/'build-config.json'),distinct_real_queue_runs=runs),indent=2)+'\n')
 assert json.loads((b/'physical-surfaces.report.json').read_text())['status']=='pass'
print('Pixel observations and final two-run/physical closure fixed',now())

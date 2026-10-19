#!/usr/bin/env python3
"""Render exact imported GLBs at the frozen brief's 128px identification size."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT=Path.cwd();QA=Path('qa/independent/small-marine-quartet-20261019-gpt6-luna-xhigh/evidence')
INPUTS=json.loads((QA/'inputs.json').read_text());VIEWS='hero,front,right,top';records=[]

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

for item in INPUTS['assets']:
    asset,revision=item['asset_id'],item['revision'];glb=ROOT/item['glb']
    blend=ROOT/item['blend'];out=QA/'renders-128'/asset
    cmd=['/usr/bin/blender','--background','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python','scripts/render_candidate_views.py','--',item['glb'],'--revision',revision,'--brief',str((blend.parent/'brief.json').relative_to(ROOT)),'--references',str((blend.parent/'references.json').relative_to(ROOT)),'--output-dir',out.as_posix(),'--views',VIEWS,'--turntable-frames','0','--resolution','128','--samples','8']
    before=sha(glb);start=datetime.now(timezone.utc).isoformat();t0=time.monotonic();p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);elapsed=round(time.monotonic()-t0,6);finish=datetime.now(timezone.utc).isoformat()
    (QA/'renders-128'/f'{asset}.stdout.txt').write_text(p.stdout);(QA/'renders-128'/f'{asset}.stderr.txt').write_text(p.stderr)
    if p.returncode:raise SystemExit(f'{asset} 128px render failed: {p.stderr[-2000:]}')
    manifest=json.loads((out/'render-manifest.json').read_text())
    if manifest.get('subject',{}).get('glb_sha256')!=before:raise SystemExit(f'{asset} 128px evidence is bound to another GLB')
    records.append({'asset_id':asset,'revision':revision,'glb_path':item['glb'],'glb_sha256_before':before,'glb_sha256_after':sha(glb),'started_at_utc':start,'finished_at_utc':finish,'elapsed_wall_seconds_monotonic':elapsed,'command':cmd,'returncode':p.returncode,'renderer_version':manifest.get('render_config',{}).get('version'),'resolution':[128,128],'views':VIEWS.split(','),'manifest':(out/'render-manifest.json').as_posix(),'manifest_sha256':sha(out/'render-manifest.json')})
    if records[-1]['glb_sha256_after']!=before:raise SystemExit(f'{asset} frozen GLB changed during 128px rendering')
report={'schema_version':1,'kind':'128px_identification_render','method':'Four exact GLBs were independently imported by the repository renderer and rendered in hero/front/right/top at 128×128; no per-frame model resizing or mesh normalization.','assets':records,'status':'pass'}
output=QA/'128px-render-log.json';output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'pass','assets':len(records),'output':output.as_posix()},indent=2))

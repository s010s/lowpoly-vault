#!/usr/bin/env python3
"""Run the project's read-only concept evidence checker for the four frozen bundles."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import time

ROOT = Path.cwd()
QA = Path('qa/independent/small-marine-quartet-20261019-gpt6-luna-xhigh/evidence')
ASSETS = [('emeraldella','r002'),('burgessia','r002'),('tuzoia','r003'),('sanctacaris','r002')]
report={'schema_version':1,'kind':'concept_evidence_integrity_checks','created_at_utc':datetime.now(timezone.utc).isoformat(),'results':[]}
for asset,revision in ASSETS:
    rel=f'{asset}/{revision}/concept-evidence.json'
    cmd=['python3','scripts/validate_concept_evidence.py',rel,'--root','production/concept-small-marine-quartet-20261019','--require-complete']
    started=datetime.now(timezone.utc).isoformat(); t0=time.monotonic()
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    elapsed=round(time.monotonic()-t0,6); finished=datetime.now(timezone.utc).isoformat()
    raw=json.loads(p.stdout)
    report['results'].append({'asset_id':asset,'revision':revision,'command':cmd,'started_at_utc':started,'finished_at_utc':finished,'elapsed_wall_seconds_monotonic':elapsed,'returncode':p.returncode,'checker_result':raw,'stderr':p.stderr})
    if p.returncode or not raw.get('valid') or not raw.get('evidence_complete'):
        raise SystemExit(f'{asset} concept evidence checker failed')
report['status']='pass'
out=QA/'concept-evidence-checks.json';out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
print(json.dumps({'status':report['status'],'assets':len(report['results']),'output':str(out)},indent=2))

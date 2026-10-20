#!/usr/bin/env python3
"""Read-only integrity check of the final batch52 candidates; no acceptance grant."""
import pathlib, json, subprocess, hashlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[4]
# parents: batch-52/work/round18/production/repository
BASE='assets/candidates/continuous-small-life-round18-20261020/batch-52'
REVISIONS={'aturia':'r002','phoenicopsis':'r001','cave-popcorn':'r003','curvolithus-trilobed-trail':'r001'}
def ref(p):
 b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
results=[]
for slug,revision in REVISIONS.items():
 d=ROOT/BASE/slug/revision
 c=d/'candidate.json'; contract=d/'profile-contract.json'
 command=[sys.executable,'scripts/validate_candidate.py',str(c.relative_to(ROOT)),'--root','.', '--profile','static-stylized-v1','--profile-contract',str(contract.relative_to(ROOT)),'--json']
 p=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
 try:r=json.loads(p.stdout)
 except Exception:r={'valid':False,'stdout':p.stdout,'stderr':p.stderr}
 results.append({'asset_id':slug,'revision':revision,'exit_code':p.returncode,'candidate':ref(c),'result':r})
print(json.dumps({'kind':'maker-handoff-integrity-only','independent_qa':False,'publication':False,'results':results},indent=2))
sys.exit(0 if all(x['exit_code']==0 and x['result'].get('valid') for x in results) else 1)

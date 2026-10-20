# SPDX-License-Identifier: MIT
"""Read-only integrity and candidate/evidence verification of the completed r003 handoff."""
from pathlib import Path
import hashlib,json,subprocess
W=Path(__file__).resolve().parent;R=next(p for p in W.parents if (p/'scripts/asset_common.py').exists());h=json.loads((W/'handoff.json').read_text());O=R/h['selected_directory']
for n,d in h['selected_files'].items():
 p=R/d['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256'],n
for argv in [['python3','scripts/validate_candidate.py',str(O/'candidate.json'),'--root',str(R),'--profile','static-stylized-v1','--profile-contract',str(O/'profile-contract.json'),'--json'],['python3','scripts/validate_concept_evidence.py','concept-evidence.json','--root',str(O)]]:
 subprocess.run(argv,cwd=R,check=True)
print(json.dumps({'status':'pass','pinned_files':len(h['selected_files']),'glb_sha256':h['glb_sha256'],'approval':'pending','provider_timestamp':'unknown'}))

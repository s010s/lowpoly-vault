# SPDX-License-Identifier: MIT
"""Two deterministic semantic/byte rebuild checks; run using ordinary Python."""
from pathlib import Path
import subprocess,json,hashlib
here=Path(__file__).resolve().parent
records=[]
for attempt in range(2):
 before={p.parent.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in here.glob('*/*.glb')}
 subprocess.run(['blender','-b','-t','2','--python',str(here/'build.py')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
 after={p.parent.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in here.glob('*/*.glb')}
 records.append({'attempt':attempt+1,'before':before,'after':after,'byte_identical_glb':before==after})
(here/'rebuild-report.json').write_text(json.dumps(records,indent=2))
assert all(r['byte_identical_glb'] for r in records)

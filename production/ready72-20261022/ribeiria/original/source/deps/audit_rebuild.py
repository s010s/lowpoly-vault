# SPDX-License-Identifier: MIT
"""Rebuild with Python audit-event observation. This is not OS-level sandboxing.
Use from an isolated copied source tree. All events are recorded without contents.
"""
import json,runpy,sys
from pathlib import Path
source=Path(__file__).resolve().parents[1]
events=[]
def audit(event,args):
    if event=='open' and args and isinstance(args[0],str):events.append({'path':args[0],'mode':str(args[1]) if len(args)>1 else None})
sys.addaudithook(audit)
try:runpy.run_path(str(source/'generate.py'),run_name='__main__')
finally:
    p=source.parent/'python-open-events.json'
    p.write_text(json.dumps(events,indent=2)+'\n')

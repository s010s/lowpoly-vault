# SPDX-License-Identifier: MIT
"""Check shared capacity and run one bounded Blender subprocess, never other jobs."""
import argparse,os,sys,subprocess,shutil,time,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--timeout',type=int,default=180);ap.add_argument('--log',type=Path,required=True);ap.add_argument('args',nargs=argparse.REMAINDER);a=ap.parse_args()
args=a.args[1:] if a.args[:1]==['--'] else a.args
mem={r.split(':')[0]:int(r.split()[1])*1024 for r in Path('/proc/meminfo').read_text().splitlines()}
free=shutil.disk_usage(Path.cwd()).free;active=[]
for p in Path('/proc').glob('[0-9]*'):
    try:
        if (p/'comm').read_text().strip()=='blender':active.append(int(p.name))
    except (FileNotFoundError,PermissionError,ProcessLookupError):pass
if mem['MemAvailable']<2*1024**3 or free<1.5*1024**3 or len(active)>=4:raise RuntimeError('Bounded resource gate unavailable; do not launch')
env=dict(os.environ,OMP_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2',MKL_NUM_THREADS='2',PYTHONDONTWRITEBYTECODE='1')
before=time.monotonic();a.log.parent.mkdir(parents=True,exist_ok=True)
with a.log.open('w') as log:
    r=subprocess.run(['/usr/bin/blender','-b','-t','2','--python-exit-code','1']+args,stdout=log,stderr=subprocess.STDOUT,env=env,timeout=a.timeout)
record={'returncode':r.returncode,'elapsed_seconds':round(time.monotonic()-before,3),'available_ram_bytes_at_launch':mem['MemAvailable'],'free_disk_bytes_at_launch':free,'other_blender_pids_at_launch':active,'threads':2,'max_global_blender_processes':4,'timeout_seconds':a.timeout}
a.log.with_suffix('.run.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record));sys.exit(r.returncode)

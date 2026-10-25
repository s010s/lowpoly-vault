# SPDX-License-Identifier: MIT
"""Resource probe and single-process launch, never kills another task's process."""
import os,sys,json,subprocess,shutil,datetime
from pathlib import Path
if '--' not in sys.argv:raise SystemExit('run_bounded.py PROBE.json -- COMMAND...')
i=sys.argv.index('--');path=Path(sys.argv[1]);cmd=sys.argv[i+1:]
mem=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
active=subprocess.run(['pgrep','-a','blender'],capture_output=True,text=True).stdout.splitlines();disk=shutil.disk_usage(path.parent).free
r={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mem_available_bytes':mem,'disk_free_bytes':disk,'blender_processes':active,'cpu_affinity_count':len(os.sched_getaffinity(0)),'threads':2,'minimum_ram_bytes':2*1024**3,'minimum_disk_bytes':int(1.5*1024**3),'global_heavy_limit':4,'status':'PASS' if mem>=2*1024**3 and disk>=1.5*1024**3 and len(active)<4 else 'BLOCK'}
path.write_text(json.dumps(r,indent=2)+'\n');assert r['status']=='PASS',r
os.environ.update({'OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'2'})
sys.exit(subprocess.call(cmd))

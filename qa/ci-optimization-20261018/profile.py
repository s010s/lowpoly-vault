import subprocess,time,json,os,sys,shlex
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
commands=[('publication-check','node site/initial-release.mjs --check')]+[(name,'node site/'+name+'-test.mjs')for name in ['initial-release','refined-release','small-life-release','small-fauna-release','small-life-batch-release','small-life-round02-release','small-life-round03-release','small-life-round04-release','small-life-round05-release']]+[('vite','node_modules/.bin/vite build'),('copy-assets','node site/copy-assets.mjs'),('audit-release','node site/audit-release.mjs')]
bin_dir=out/'instrumentation-bin';bin_dir.mkdir(exist_ok=True)
wrapper=bin_dir/'python3';wrapper.write_text('#!/bin/bash\nprintf \'%s\\n\' "$1" >> "$LPV_PROFILE_PYTHON_LOG"\nexec {python} "$@"\n'.format(python=shlex.quote(sys.executable)));wrapper.chmod(0o755)
rows=[]
for name,command in commands:
 counter=out/(name+'-python.log');counter.write_text('');env={**os.environ,'SITE_BASE':'/lowpoly-vault/','SITE_ORIGIN':'https://s010s.github.io','LPV_PROFILE_PYTHON_LOG':str(counter),'PATH':str(bin_dir)+':'+os.environ['PATH']};start=time.perf_counter()
 with (out/(name+'.log')).open('w')as log:r=subprocess.run(command.split(),cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
 calls=counter.read_text().splitlines();row={'phase':name,'command':command,'seconds':round(time.perf_counter()-start,3),'returncode':r.returncode,'python_calls':len(calls),'python_scripts':{s:calls.count(s)for s in sorted(set(calls))}};rows.append(row);(out/'timings.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(row),flush=True)
 if r.returncode:sys.exit(r.returncode)

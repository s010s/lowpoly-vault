#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bounded local macOS rebuild with hash-bound input/output records.
One worker, two Blender threads. Own process-group cleanup on cancellation.
No Linux /proc, affinity, cgroup, or memory-limit claims.
"""
import hashlib,json,os,signal,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(path,value):
 with path.open('x') as f:json.dump(value,f,indent=2);f.write('\n')
def main():
 spec=json.loads((P/'rebuild-jobs.json').read_text())['jobs'][0]
 dest=P/'rebuild-runs/local-rebuild-01';dest.mkdir(parents=True,exist_ok=False)
 output=dest/'outputs';output.mkdir()
 inputs={key:{'path':str(Path(value).resolve()),'sha256':H(Path(value)),'bytes':Path(value).stat().st_size} for key,value in spec['inputs'].items()}
 identity={'runner_schema':1,'lane':'build','environment':'macOS local bounded runner','job':{key:spec[key] for key in ['asset_id','revision','job_id']},'inputs':inputs,'threads':2,'workers':1,'timeout_seconds':180,'memory_limit':'not_enforced; sequential bounded job'}
 fingerprint=hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
 argv=['/Applications/Blender.app/Contents/MacOS/Blender','-b','-t','2','--factory-startup','--python-exit-code','1','--python',inputs['generator']['path'],'--','--output-dir',str(output),'--config',inputs['config']['path']]
 write(dest/'request.json',{'identity':identity,'fingerprint':fingerprint,'argv':argv})
 started=time.monotonic();code=None;error=None
 with (dest/'stdout.log').open('w') as log:
  proc=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,'OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'2'})
  try:code=proc.wait(timeout=180)
  except BaseException as exc:
   error=type(exc).__name__;os.killpg(proc.pid,signal.SIGTERM)
   try:proc.wait(timeout=3)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
  finally:
   results={name:{'sha256':H(output/name),'bytes':(output/name).stat().st_size} for name in spec['outputs'] if (output/name).is_file()}
   changed=[key for key,item in inputs.items() if H(Path(item['path']))!=item['sha256']]
   if changed:error='Inputs changed: '+str(changed)
   result={'schema_version':1,'fingerprint':fingerprint,**identity['job'],'status':'succeeded' if code==0 and error is None and len(results)==len(spec['outputs']) else 'failed','returncode':code,'error':error,'outputs':results,'wall_seconds':time.monotonic()-started,'environment':'macOS local bounded runner'}
   write(dest/'result.json',result)
 if result['status']!='succeeded':raise RuntimeError(result)
 print(json.dumps(result))
if __name__=='__main__':main()

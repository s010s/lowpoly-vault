# SPDX-License-Identifier: MIT
import pathlib,json,hashlib,datetime,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[2];P=R/'production/batch94';E=pathlib.Path('/workspace/shared/lowpoly-batch94-evidence');now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=pathlib.Path(sys.argv[1]).resolve();name=sys.argv[2];cmd=sys.argv[3:];e=E/'stages'/b.parent.name/b.name/name;e.mkdir(parents=True,exist_ok=True)
assert not(e/'request.json').exists(),'Check uncertain execution before rerun'
(e/'request.json').write_text(json.dumps({'requested_at':now(),'command':cmd},indent=2)+'\n')
with(e/'stdout.log').open('x')as f:proc=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT);code=proc.wait()
(e/'result.json').write_text(json.dumps({'finished_at':now(),'runner_pid':proc.pid,'exit_code':code,'log_sha256':H(e/'stdout.log'),'request_sha256':H(e/'request.json')},indent=2)+'\n')
d=json.load(open(P/'recovery-progress.json'));d['events'].append(dict(recorded_at=now(),stage=f'{b.parent.name}/{b.name}/{name}',artifacts=[dict(path=str(e/'result.json'),sha256=H(e/'result.json'))],exit_code=code));(P/'recovery-progress.json').write_text(json.dumps(d,indent=2)+'\n');print(b.parent.name,b.name,name,code,flush=True);sys.exit(code)

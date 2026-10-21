from pathlib import Path
import subprocess,json,datetime,time,hashlib,sys
R=Path('/workspace/shared/lowpoly-batch96-20261020');P=R/'production/batch96';E=Path('/workspace/shared/lowpoly-batch96-evidence');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
bl=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python']
def run(b,name,args):
 log=E/'diagnostic-logs'/b.parent.name/(b.name+'-'+name+'.log');log.parent.mkdir(parents=True,exist_ok=True)
 if log.exists():log=log.with_name(log.stem+'-retry-'+str(time.time_ns())+log.suffix)
 start=now()
 request=log.with_suffix('.request.json');request.write_text(json.dumps(dict(requested_at=start,command=args),indent=2)+'\n')
 with log.open('x')as f:
  proc=subprocess.Popen(args,cwd=R,stdout=f,stderr=subprocess.STDOUT);code=proc.wait(timeout=3600)
 with (b/'diagnostic-lifecycle.jsonl').open('a')as f:f.write(json.dumps(dict(stage=name,runner_pid=proc.pid,started_at=start,finished_at=now(),exit_code=code,command=args,log=str(log),log_sha256=H(log)))+'\n')
 d=json.load(open(P/'recovery-progress.json'));d['events'].append(dict(recorded_at=now(),stage=b.parent.name+' '+name,artifacts=[dict(path=str(b/'diagnostic-lifecycle.jsonl'),sha256=H(b/'diagnostic-lifecycle.jsonl'))],exit_code=code));(P/'recovery-progress.json').write_text(json.dumps(d,indent=2)+'\n')
 print(b.parent.name,name,code,flush=True)
 if code:raise RuntimeError(str(log))
for aid in sys.argv[1:]or['paralycopodites','lyginopteris','medullosa','cordaites']:
 b=P/'assets'/aid/'r002'
 if not(b/'model.glb').exists():run(b,'build',bl+[str(b/'generator.py'),'--','--config',str(b/'build-config.json'),'--output',str(b)])
 if not(b/'source-vertex-counts-v002.json').exists():run(b,'measure',bl+[str(P/'measure-both.py'),'--',str(b)])
 if not(b/'hierarchy-measurements.json').exists():run(b,'hierarchy',bl+[str(P/'measure-hierarchy.py'),'--',str(b)])
 if not(b/'diagnostic8/render-manifest.json').exists():run(b,'diagnostic8',bl+[str(P/'render-fixed8.py'),'--',str(b/'model.glb'),'--revision','r002','--brief',str(b/'brief.json'),'--references',str(b/'references.json'),'--output-dir',str(b/'diagnostic8'),'--views','hero,front,side,top','--turntable-frames','0','--resolution','256','--samples','8'])

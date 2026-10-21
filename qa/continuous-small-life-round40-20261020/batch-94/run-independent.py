import pathlib,subprocess,json,datetime,time
O=pathlib.Path('/workspace/shared/lowpoly-batch94-independent-qa-20261020')
for a,r in [('rhacophyton','r002'),('sigillaria','r001'),('pseudobornia','r001'),('calamites','r001')]:
 argv=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(O/'independent-geometry.py'),'--',a,r];st=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 with (O/(a+'-independent.log')).open('x')as f:p=subprocess.Popen(argv,stdout=f,stderr=subprocess.STDOUT);code=p.wait()
 (O/(a+'-execution.json')).write_text(json.dumps({'started_at':st,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runner_pid':p.pid,'returncode':code,'wall_seconds':time.monotonic()-t,'argv':argv},indent=2)+'\n');print(a,code,flush=True)
 if code:raise SystemExit(code)

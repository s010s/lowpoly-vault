from pathlib import Path
import subprocess,json,datetime,time,hashlib,os
O=Path(__file__).parent;R=Path('/workspace/shared/lowpoly-batch84-20261020');W=R/'production/batch84';os.environ['PYTHONDONTWRITEBYTECODE']='1'
s=(W/'render-comparison-fixed.py').read_text().replace("sys.path.insert(0,str(next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())/'scripts'))", "sys.path.insert(0,'/workspace/shared/lowpoly-batch84-20261020/scripts')\nsys.dont_write_bytecode=True")
s=s.replace("'clayalt':(35,20)","'clayalt':(35,38)")
# Explicit diagnostic ONLY: same-size same-camera neutral A/B alternate light, and neutral top delta. No geometry or base-color edits.
s=s.replace("if args.glb.parent.parent.name=='solution-cave-passage':", "if args.glb.parent.parent.name=='tide-dominated-delta':\n        DIRECTIONS['clay']=(0,90)\n    if args.glb.parent.parent.name=='solution-cave-passage':")
(O/'render_focused_diagnostics.py').write_text(s)
scope={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'Check actual delta topographic readability without material labels and neutral leaf comparison under opposite key. Diagnostic does not replace final8 or change model/control geometry.','samples':32,'resolution':512,'views':{'delta':'clay at0,90 same light as canonical','leaf_pair':'clayalt at35,38 both same-size, same neutral material, opposite key direction3,4,6'},'source_renderer_sha256':hashlib.sha256((W/'render-comparison-fixed.py').read_bytes()).hexdigest(),'diagnostic_renderer_sha256':hashlib.sha256((O/'render_focused_diagnostics.py').read_bytes()).hexdigest()};(O/'focused-diagnostic-scope.json').write_text(json.dumps(scope,indent=2)+'\n')
runs=[]
for name,p,view in [('glossopteris',W/'assets/glossopteris/r001','clayalt'),('bjuvia-control',W/'comparison-control/bjuvia-simplex','clayalt'),('tide-dominated-delta',W/'assets/tide-dominated-delta/r002','clay')]:
 out=O/name/'diagnostic';out.parent.mkdir(exist_ok=True)
 c=['flock','/tmp/lowpoly-production-blender.lock','blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(O/'render_focused_diagnostics.py'),'--',str(p/'model.glb'),'--output-dir',str(out),'--revision','independent-focused-diagnostic','--views',view,'--turntable-frames','0','--resolution','512','--samples','32']
 if (p/'candidate-brief.json').exists():c+=['--brief',str(p/'candidate-brief.json'),'--references',str(p/'references.json')]
 t=time.monotonic();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (out.parent/'diagnostic.log').open('x') as log:proc=subprocess.Popen(c,stdout=log,stderr=subprocess.STDOUT);code=proc.wait()
 runs.append({'name':name,'command':c,'pid':proc.pid,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':code});(O/'diagnostic-processes.json').write_text(json.dumps(runs,indent=2)+'\n');print(name,code,flush=True)
 assert code==0

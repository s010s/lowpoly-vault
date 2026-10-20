# SPDX-License-Identifier: MIT
"""Real fixed8 rendering only; no generator or source construction is invoked."""
from pathlib import Path
import json,hashlib,subprocess,datetime,time,os
R=Path.cwd();W=R/'production/continuous-small-life-round23-20261020/work/batch-61';D=W/'render-proof-v003';BASE='896563bfcbc70f160edf29b84dacfc824536be6a';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(R));now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
def pin(p):return {'path':rel(p),'sha256':H(p)}
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==BASE
assert not subprocess.check_output(['git','diff','--name-only'],text=True).strip()
selected=[x for x in json.loads((W/'final-selection.json').read_text()) if x['asset_id']!='pseudopulex'];originals={}
for x in selected:
 b=R/x['path']
 for path in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',x['path']],text=True).splitlines():originals[path]=H(R/path)
put(D/'pre-render-original-pins.json',{'baseline_commit':BASE,'files':originals,'includes':'All original committed files in three selected final asset trees, including original frozen/adapter/candidate/proofs and rejected v002 manifests.'})
rows=[]
for x in selected:
 b=R/x['path'];o=b/'proof-scale-v003';assert not o.exists();g=b/'model.glb';brief=b/'candidate-brief-scale-v002.json';refs=b/'references.json';renderer=W/'render-fixed8.py';inputs={k:pin(p) for k,p in [('glb',g),('corrected_brief',brief),('references',refs),('renderer_script',renderer),('helper',R/'scripts/asset_common.py'),('audit_helper',R/'scripts/qa_glb.py')]};binary={'path':'/usr/bin/blender','sha256':H(Path('/usr/bin/blender'))};argv=['/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(renderer),'--',str(g),'--revision',x['revision'],'--brief',str(brief),'--references',str(refs),'--output-dir',str(o),'--views','hero,reversehero,front,side,rear,top,clay,silhouette','--turntable-frames','0','--resolution','512','--samples','16'];start=now();t=time.monotonic();log=D/(x['asset_id']+'-actual-render.log')
 with log.open('x') as f:
  p=subprocess.Popen(argv,stdout=f,stderr=subprocess.STDOUT,cwd=R);pid=p.pid
  try:code=p.wait(timeout=300)
  except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=10);raise
 run={'schema_version':1,'kind':'actual-fresh-glb-render-run','asset_id':x['asset_id'],'geometry_revision':x['revision'],'metadata_proof_revision':'v003','started_at':start,'ended_at':now(),'wall_seconds':time.monotonic()-t,'runner_pid':os.getpid(),'blender_process_pid':pid,'command':argv,'working_directory':str(R),'threads':2,'max_concurrent_blender_processes':1,'binary':binary,'inputs':inputs,'returncode':code,'stdout':pin(log),'operation':'Exact GLB clean import and fresh fixed8 rendering; no generator/source rebuild invoked','new_manifest':pin(o/'render-manifest.json') if code==0 else None,'approval':'not granted'};assert code==0,run
 for v in inputs.values():assert H(R/v['path'])==v['sha256']
 man=json.loads((o/'render-manifest.json').read_text());assert man['subject']['brief_sha256']==H(brief);assert man['source_glb_sha256']==H(g);assert len(man['frames'])==8;assert man['created_at']>=start;assert not (o/'render-manifest-scale-v002.json').exists()
 rp=D/(x['asset_id']+'-actual-run.json');put(rp,run);rows.append({**x,'proof_directory':rel(o),'runner_record':pin(rp),'manifest':pin(o/'render-manifest.json')});print(x['asset_id'],'REAL RENDER',pid,code,round(run['wall_seconds'],3),flush=True)
for path,h in originals.items():assert H(R/path)==h,path
put(D/'actual-render-index.json',{'baseline_commit':BASE,'assets':rows,'all_preexisting_selected_asset_bytes_unchanged':True,'new_rendered_view_count':24,'no_geometry_or_source_rebuild':True,'no_push':True})

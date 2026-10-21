import pathlib,json,hashlib,datetime,re,sys
from PIL import Image,ImageChops
R=pathlib.Path('/workspace/shared/lowpoly-batch107-20261021');B=R/'production/small-life-batch107';E=pathlib.Path('/workspace/shared/lowpoly-batch107-evidence');O=pathlib.Path('/workspace/shared/lowpoly-batch107-independent-qa-20261021');sys.path.insert(0,str(R/'scripts'));from qa_glb import audit_glb
j=lambda p:json.loads(p.read_text());h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();ids=['dendrocystites','trochocystites','helicoplacus','stromatocystites'];bad=[];bindings=[];old=j(O/'identity-freeze-report.json')
# Historical archive resolution, preserving first broad-check diagnostics rather than changing source.
for f in B.rglob('*.json'):
 def walk(x):
  if isinstance(x,dict):
   if 'path' in x and 'sha256' in x and isinstance(x['path'],str):
    p=pathlib.Path(x['path']); ps=[p] if p.is_absolute() else [R/p,f.parent/p]
    if 'retired-pre-final-binding2-relocation' in f.name:
     ps=[E/'retired-pre-final-binding2'/p.relative_to(B)] if str(p).startswith(str(B)) else [E/'retired-pre-final-binding2'/'queue-manifests'/p.name]
    elif 'retired-pre-final-binding-relocation' in f.name:ps=[E/'retired-pre-final-binding'/p]
    elif p.name=='generate-r001.py':ps=[E/'original-generators/generate-r001.py']
    good=[a for a in ps if a.exists() and a.is_file() and h(a)==x['sha256']];bindings.append({'origin':str(f.relative_to(R)),'declared_path':str(p),'resolved_path':str(good[0]) if good else None,'sha256':x['sha256'],'pass':bool(good)})
    if not good:bad.append(bindings[-1])
   for y in x.values():walk(y)
  elif isinstance(x,list):
   for y in x:walk(y)
 walk(j(f))
assets=[]
for id in ids:
 A=B/id/'r001';g=A/'artifacts'/f'{id}.glb';trip={'revision':'r001','glb_sha256':h(g),'brief_sha256':h(A/'delivery-brief.json'),'references_sha256':h(A/'references.json')};checks=[];renders=[]
 for label in ['views','details']:
  M=j(A/label/'render-manifest.json');assert M['subject']==trip
  for frame in M['frames']:
   p=A/label/frame['path'];im=Image.open(p);assert h(p)==frame['sha256'];assert im.size==(512,512)
  if label=='views':
   sheet=Image.open(A/label/'contact-sheet.png').convert('RGBA');match=[]
   for n,frame in enumerate(M['frames']):
    raw=Image.open(A/label/frame['path']).convert('RGBA');crop=sheet.crop(((n%4)*512,(n//4)*544,(n%4+1)*512,(n//4)*544+512));match.append(ImageChops.difference(raw,crop).getbbox() is None)
   assert all(match)
  renders.append({'label':label,'manifest_sha256':h(A/label/'render-manifest.json'),'frames_bound':len(M['frames']),'created_at':M['created_at'],'lossless_sheet_verified':label=='views'})
 rebuilds=[]
 for kind in ['original-build','rebuild-a','rebuild-b','final-render','detail-render']:
  D=A/'qa'/kind;req=j(D/'request.json');res=j(D/'result.json');assert res['status']=='succeeded' and res['returncode']==0;argv=req['argv'];assert argv[0]=='/usr/bin/flock' and argv[1]=='/tmp/lowpoly-production-blender.lock';assert argv[argv.index('--threads')+1]=='2';out=pathlib.Path(argv[argv.index('--output')+1]) if '--output' in argv else pathlib.Path(argv[argv.index('--output-dir')+1]).parent
  results=[]
  for name,info in res['outputs'].items():
   p=out/name;ok=p.exists() and h(p)==info['sha256'];results.append({'path':str(p),'sha256':info['sha256'],'pass':ok});assert ok,(kind,p)
  if kind in ['original-build','rebuild-a','rebuild-b']:
   exe=j(D/'execution.json');assert exe['parent_pid']==res['pid'];raw=out/id/f'{id}.glb';q=audit_glb(raw,14000,6,30);assert q['semantic_sha256']==audit_glb(g,14000,6,30)['semantic_sha256'];assert exe['generator_sha256']==h(B/'tools/generate-r007.py');assert exe['config_sha256']==h(A/'config.json')
   rebuilds.append({'job':kind,'queue_pid':res['pid'],'blender_pid':exe['pid'],'request_at':req['created_at'],'start':res['started_at'],'finish':res['finished_at'],'output_root':str(out),'semantic_sha256':q['semantic_sha256'],'glb_sha256':h(raw),'outputs':results})
  checks.append({'job':kind,'request_sha256':h(D/'request.json'),'result_sha256':h(D/'result.json'),'outputs_verified':results,'status':'pass'})
 assert len({x['blender_pid'] for x in rebuilds})==3
 for a,b in zip(rebuilds,rebuilds[1:]):assert a['finish']<b['start']
 assets.append({'id':id,'triplet':trip,'renders':renders,'jobs':checks,'retained_rebuilds':rebuilds})
report={'status':'pass' if not bad else 'fail','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'context_resolved_bindings':bindings,'unresolved':bad,'assets':assets,'diagnostic_correction':'First broad path scan treated retired old-path entries as current subjects and treated manifest-local filenames as repo-relative. Those are reviewer resolution assumptions, not candidate defects. First report retained. This report resolves each according to archive or manifest context.'};(O/'context-binding-report.json').write_text(json.dumps(report,indent=2)+'\n');print('context bindings',len(bindings),'unresolved',bad,'assets verified',len(assets))

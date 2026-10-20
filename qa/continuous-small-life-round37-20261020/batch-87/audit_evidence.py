import pathlib,json,hashlib,datetime,sys,subprocess
from PIL import Image
R=pathlib.Path('/workspace/shared/lowpoly-batch87-20261020');P=R/'production/small-life-batch87';O=pathlib.Path('/workspace/shared/lowpoly-batch87-independent-qa-20261020');L=pathlib.Path('/workspace/shared/lowpoly-batch87-local');h=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();j=lambda p:json.loads(pathlib.Path(p).read_text());errors=[];checks=[]
def ck(ok,label):
 checks.append({'check':label,'pass':bool(ok)})
 if not ok:errors.append(label)
def walk(x):
 if isinstance(x,dict):
  if 'path' in x and 'sha256' in x:
   p=pathlib.Path(x['path']);p=p if p.is_absolute() else R/p;ck(p.is_file() and h(p)==x['sha256'],'bound '+str(p))
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
H=j(P/'maker-handoff.json');ck(h(P/'maker-handoff.json')=='97366cb9232d71750203b8b3e62ef07f07b32225d507a9ae74ad03bc3281ece2','handoff pinned');walk(H)
raw=j(L/'raw-evidence-manifest.json');ck(len(raw['files'])==448,'448 raw files')
for f,rec in raw['files'].items():p=L/f;ck(p.is_file() and h(p)==rec['sha256'] and p.stat().st_size==rec['bytes'],'raw '+f)
freeze=j(P/'original-freeze-manifest.json')
for f,digest in freeze['files'].items():ck(h(R/f)==digest,'freeze '+f)
walk(j(P/'dependencies.json'))
items=[]
for item in H['items']:
 aid=item['asset_id'];rev=item['revision'];p=P/aid/rev;refs=j(R/item['artifacts']['references']['path']);walk(refs)
 orig=j(P/aid/'r001/original-brief.json');brief=j(p/'delivery-brief.json');cfg=j(p/'config.json');ck(orig['parameters']==cfg['parameters']==brief['parameters'],aid+' frozen numeric values not rewritten')
 for key in orig:
  if key=='brief_version':continue
  ck(orig[key]==brief[key],aid+' derived preserves '+key)
 receipt=j(P/'concepts'/f'{aid}-receipt.json');ck(receipt['observed_call_returned_at']<freeze['freeze_observed_at'],aid+' concept before freeze');ck(h(receipt['source_path'])==h(P/'concepts'/f'{aid}-concept.png'),aid+' original concept bytes')
 man=j(p/'views/render-manifest.json');rc=j(p/'views/render-config.json');rp=pathlib.Path(man['derivation']['raw_nine_view_manifest']);rm=j(rp);run=rp.parents[2];request=j(run/'request.json');result=j(run/'result.json');subject={k+'_sha256':item['artifacts'][k]['sha256'] for k in ['glb','brief','references']};subject['revision']=rev
 ck(rm['subject']==subject==man['subject'],aid+' raw/shipped/final triplet');ck(h(rp)==man['derivation']['raw_manifest_sha256'],aid+' raw manifest hash');ck(h(pathlib.Path(rc['derivation']['raw_config_path']))==rc['derivation']['raw_config_sha256'],aid+' raw config hash')
 ck(result['status']=='succeeded' and result['returncode']==0,aid+' actual final render succeeded');ck(brief['delivery_bound_at']<request['created_at']<=result['started_at']<result['finished_at'],aid+' triplet fixed before render')
 ck(len(rm['frames'])==9 and len(man['frames'])==8,aid+' real nine and shipped eight')
 rawframes={f['id']:f for f in rm['frames']};frame_summary=[]
 for view in orig['required_views']+['bottom']:
  f=rawframes[view];path=p/'views'/f['path'];ck(h(path)==f['sha256']==h(rp.parent/f['path']),aid+' same pixels '+view);ck(Image.open(path).size==(512,512),aid+' 512 '+view);ck(result['outputs']['views/'+f['path']]['sha256']==h(path),aid+' process output '+view)
  if view!='bottom':ck(next(v for v in man['frames'] if v['id']==view)==f,aid+' subset entry '+view)
  frame_summary.append({'view':view,'path':str(path),'sha256':h(path),'dimensions':[512,512]})
 for role in ['brief','references','glb']:ck(request['identity']['inputs'][role]['sha256']==item['artifacts'][role]['sha256'],aid+' renderer input '+role)
 rawc=j(rc['derivation']['raw_config_path']);subc={k:v for k,v in rc.items() if k!='derivation'};rawc['frames']=[f for f in rawc['frames'] if f['id']!='bottom'];ck(subc==rawc,aid+' render config subset only')
 prov=j(p/'qa/execution-provenance.json');walk(prov);rebuilds=[]
 for rep in prov['two_distinct_real_rebuilds']:
  rawdir=pathlib.Path(rep['raw_directory']);req=j(rawdir/'request.json');res=j(rawdir/'result.json');ex=j(rawdir/'outputs/execution.json')
  ck(res['status']=='succeeded' and res['returncode']==0,aid+' rebuild '+rep['label']+' succeeded')
  ck(res['started_at']<=ex['started_at']<=ex['finished_at']<=res['finished_at'],aid+' rebuild '+rep['label']+' process timing')
  for k,v in req['identity']['inputs'].items():ck(h(v['path'])==v['sha256'],aid+' rebuild '+rep['label']+' input '+k)
  for f,rec in res['outputs'].items():ck(h(rawdir/'outputs'/f)==rec['sha256'],aid+' rebuild '+rep['label']+' output '+f)
  ck(h(rawdir/'outputs'/aid/(aid+'.glb'))==item['artifacts']['glb']['sha256'],aid+' rebuild '+rep['label']+' GLB byte equal')
  ck(ex['generator_sha256']==item['artifacts']['generator']['sha256'] and ex['config_sha256']==item['artifacts']['config']['sha256'],aid+' rebuild '+rep['label']+' execution closure')
  rebuilds.append({'label':rep['label'],'request_path':str(rawdir/'request.json'),'request_sha256':h(rawdir/'request.json'),'result_sha256':h(rawdir/'result.json'),'pid':ex['pid'],'queue_pid':res['pid'],'started_at':ex['started_at'],'finished_at':ex['finished_at'],'byte_equal':True,'semantic_sha256':rep['semantic_sha256']})
 ck(rebuilds[0]['pid']!=rebuilds[1]['pid'] and rebuilds[0]['request_path']!=rebuilds[1]['request_path'],aid+' distinct rebuild processes')
 items.append({'asset_id':aid,'revision':rev,'subject':subject,'frames':frame_summary,'render_process':{'request':str(run/'request.json'),'pid':result['pid'],'started_at':result['started_at'],'finished_at':result['finished_at'],'fixed_at':brief['delivery_bound_at'],'raw_manifest_sha256':h(rp)},'rebuilds':rebuilds,'concept_receipt':receipt})
r={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'check_count':len(checks),'errors':errors,'checks':checks,'items':items,'limitations':'Process records are execution provenance, not trusted external timestamps. All hashes are independently recomputed.'};(O/'evidence-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'checks':len(checks),'errors':errors},indent=2))

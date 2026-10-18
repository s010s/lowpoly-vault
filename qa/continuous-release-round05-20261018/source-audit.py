import subprocess,json,hashlib,posixpath,re,sys
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()))
from validate_candidate import STATIC_VIEWS
spec=json.loads(Path('qa/continuous-release-round05-20261018/source-spec.json').read_text())
qspec={'13':('8d11b8c933496110888f058cbe11e3927092115c','production/continuous-small-life-round05-20261018/reviews/batch-13/independent-gpt6-luna-xhigh/INDEPENDENT-QA.md','c173fe4666939005f1617e7be46cdbba6b4cef89'),'14':('5ccb29d763025e033f7f91ad7e65c88cf91b4266','production/continuous-small-life-round05-20261018/work/batch-14/qa-independent/independent-qa-report.md','5d33dccfb439c44d5342e2a1047b81891b850435'),'15':('051bec9b31e17b9d270fb4520da46d93e5070b35','qa/continuous-small-life-round05-20261018/batch-15/independent-review/report.md','ee22aea0066e62ee13d4902f6bcecf367d0e7296')}
cache={}
def read(ref,p):
 k=(ref,p)
 if k not in cache:cache[k]=subprocess.check_output(['git','show',ref+':'+p],stderr=subprocess.PIPE)
 return cache[k]
def js(ref,p):return json.loads(read(ref,p))
def sha(b):return hashlib.sha256(b).hexdigest()
def zero(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['errors','failed','page_errors','consoleErrors','resource_errors']:assert not v,(k,v)
   if k=='gl_error':assert v==0
   zero(v)
 elif isinstance(x,list):
  for v in x:zero(v)
rows=[];batches=[];declared=0
for batch in ['13','14','15']:
 qa,review,handoff=qspec[batch];rb=read(qa,review);text=rb.decode();assert handoff in text
 sources={id:ref for n,id,ref,cp in spec if n==batch};b={'batch':batch,'sources':sources,'handoff_commit':handoff,'review_commit':qa,'review':{'path':review,'sha256':sha(rb)},'ids':list(sources)}
 if True:
  hp=f'production/continuous-small-life-round05-20261018/work/batch-{batch}/'+('final-handoff.jsonl'if batch in ['13','15']else'HANDOFF.json');b['handoff']={'path':hp,'sha256':sha(read(handoff,hp))}
 batches.append(b)
 for n,id,source,cp in [r for r in spec if r[0]==batch]:
  files=set(subprocess.check_output(['git','ls-tree','-r','--name-only',source],text=True).splitlines());c=js(source,cp);folder=posixpath.dirname(c['artifacts']['glb']['path']);work=f'production/continuous-small-life-round05-20261018/work/batch-{batch}/{id}/r001';mp=folder+'/metadata.json';m=js(source,mp);pins={}
  def pin(p):
   data=read(source,p);pins[p]={'path':p,'sha256':sha(data),'bytes':len(data),'git_commit':source};return pins[p]
  def resolve(path,doc,expected=None):
   opts=[path,posixpath.normpath(posixpath.join(posixpath.dirname(doc),path)),posixpath.normpath(posixpath.join(posixpath.dirname(posixpath.dirname(doc)),path)),posixpath.join(folder,path),posixpath.join(work,path)]
   for token in ['assets/','production/','scripts/','site/']:
    if token in path:opts.append(path[path.index(token):])
   opts+=[p for p in files if p.endswith('/'+path)]
   return next((p for p in opts if p in files and(expected is None or sha(read(source,p))==expected)),None)
  def walk(v,doc):
   global declared
   if isinstance(v,dict):
    if isinstance(v.get('path'),str)and re.fullmatch('[a-f0-9]{64}',str(v.get('sha256',''))):
     p=resolve(v['path'],doc,v['sha256']);assert p,(id,'unresolved or stale pin',doc,v['path']);a=pin(p);assert a['sha256']==v['sha256'];
     if 'bytes'in v:assert a['bytes']==v['bytes']
     if 'byte_length'in v:assert a['bytes']==v['byte_length']
     declared+=1
    for child in v.values():walk(child,doc)
   elif isinstance(v,list):
    for child in v:walk(child,doc)
  pin(cp);walk(c,cp);pin(mp);walk(m,mp);glb=pin(m['glb']);blend=pin(m['blend']);assert glb['sha256']==m['sha256']['glb']==c['artifacts']['glb']['sha256'];assert blend['sha256']==m['sha256']['blend']==c['artifacts']['source']['sha256'];assert m['glb_bytes']==glb['bytes']
  assert glb['sha256']in text and blend['sha256']in text,(id,'QA payload bindings')
  if batch=='15':
   hp=b['handoff'];hb=read(handoff,hp['path']);assert hp['sha256']in text;hr=next(json.loads(l)for l in hb.splitlines()if json.loads(l)['asset_id']==id);assert hr['commit']==source and hr['glb_sha256']==glb['sha256']and hr['artifacts']['blend']['sha256']==blend['sha256']
  else:assert source in text,(id,'QA source binding')
  assert any(({'tafoni-outcrop':'tafoni outcrop'}.get(id,id)).casefold() in l.casefold()and'PASS'in l for l in text.splitlines()),(id,'visual PASS')
  brief=js(source,c['artifacts']['brief']['path']);refs=js(source,c['artifacts']['references']['path']);assert brief['turntable_frames']==0 and set(brief['required_views'])==STATIC_VIEWS;assert refs['no_incorporated_third_party_assets']is True
  for ref in refs['sources']:assert ref['url']and ref['rights_note']and ref['use']in ['consulted-only','consulted-only; no source media/mesh/texture incorporated','consulted-only; no source media, mesh or texture incorporated']
  vp=folder+('/views/render-manifest.json'if batch in ['13','15']else'/view-manifest.json');v=js(source,vp);pin(vp);walk(v,vp);assert v['turntable_frames']==0;assert v.get('glb_sha256',v.get('subject',{}).get('glb_sha256'))==glb['sha256']
  if batch in ['13','15']:assert len(v['frames'])==8 and {f['view']for f in v['frames']}==STATIC_VIEWS
  rp=folder+('/runtime/runtime-report.json'if batch in ['13','15']else'/runtime/single.json');runtime=js(source,rp);pin(rp);walk(runtime,rp);zero(runtime);assert runtime['status']=='pass'and runtime.get('glb_sha256',runtime.get('source_glb_sha256'))==glb['sha256'];assert runtime['views']and all(f.get('triangles',f.get('render_triangles',0))>0 for f in runtime['views'])
  scene=rp if batch in ['13','15']else folder+'/runtime/scene.json';sc=js(source,scene);pin(scene);walk(sc,scene);zero(sc);assert sc['status']=='pass';assert any(f.get('instances',sc.get('instances',0))>=2 for f in sc['views'])
  if batch in ['13','15']:
   for extra in ['runtime/evidence-manifest.json','views/view-manifest.json','reproducibility-1.report.json','reproducibility-2.report.json','maker-self-check.json','source-mesh-measurements.json','project-checker.report.json','reference-access.json']:
    p=folder+'/'+extra;pin(p);walk(js(source,p),p)
   checks=folder+'/checksums.sha256';pin(checks)
   for l in read(source,checks).decode().splitlines():
    if not l.strip():continue
    expected,p=l.split(None,1);p=p.lstrip('*');target=resolve(p,checks,expected);assert target,(id,'checksum',p);pin(target);declared+=1
  else:
   for f in runtime['views']:
    if f.get('path'):target=resolve(f['path'],rp);assert target;pin(target)
  se=folder+'/source-export.report.json'if batch in ['13','15']else work+('/source-export-final.json'if False else'/source-export.json');s=js(source,se);pin(se);assert s['status']in ['pass','pass_with_warnings']and s['errors']==[]and s['triangles_match']is True and s['bounds_match']is True and s['glb_sha256']==glb['sha256']and s['source_sha256']==blend['sha256']
  kp=folder+'/gltf-validator.report.json';k=js(source,kp);pin(kp);assert k['issues']['numErrors']==0 and k['issues']['numWarnings']==0 and k['issues']['truncated']is False
  rows.append({'id':id,'batch':batch,'source_commit':source,'review_commit':qa,'handoff_commit':handoff,'review':b['review'],'candidate':pin(cp),'source_metadata':pin(mp),'metadata':m,'glb':glb,'blend':blend,'views':pin(vp),'runtime':pin(rp),'scene':pin(scene),'source_export':pin(se),'validator':pin(kp),'evidence':list(pins.values())});print(batch,id,glb['bytes'],glb['sha256'],flush=True)
assert len(rows)==12 and len({a['id']for a in rows})==12
Path('/tmp/lpv-round05-audit.json').write_text(json.dumps({'status':'pass','verified_declared_pins':declared,'batches':batches,'assets':rows},ensure_ascii=False,indent=2)+'\n');print('Verified declared pins',declared)

import subprocess,json,hashlib,posixpath,re,sys
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()))
from validate_candidate import STATIC_VIEWS
specs=[('04','abc24f3289df8ccce4ef6fd29c1edb1eeec8253a','2404d63bf812e113c4688d14e2f456ab43b8f87c',['calceola','favosites','opabinia','choia'],'production/continuous-small-life-round02-20261018/work/batch-04/INDEPENDENT-REVIEW.md'),('05','e968fab0544ce2dc41814c057b1f9dca43a2b22d','831253010e3a177a0ab561a16328520546645fb4',['goniophyllum','halysites','marrella','proteroctopus'],'production/continuous-small-life-round02-20261018/reviews/batch-05/independent-gpt6-luna-xhigh/INDEPENDENT-QA.md'),('06','e82f82ea41221afecc140d2fc7056e87cf6c1bc6','614977406575b05e18f3558e2ce3a20f21eb9c25',['aulopora','thamnopora','hallucigenia','fenestella'],'production/continuous-small-life-round02-20261018/work/batch-06/independent-review/qa-s010s-20261018/report.md')]
cache={}
def read(ref,p):
 k=(ref,p)
 if k not in cache:cache[k]=subprocess.check_output(['git','show',ref+':'+p],stderr=subprocess.PIPE)
 return cache[k]
def js(ref,p):return json.loads(read(ref,p))
def sha(b):return hashlib.sha256(b).hexdigest()
def zero_errors(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['errors','failed','page_errors','pageErrors','consoleErrors','resource_errors']:assert not v,(k,v)
   if k=='gl_error':assert v==0
   zero_errors(v)
 elif isinstance(x,list):
  for v in x:zero_errors(v)
rows=[];batches=[];declared=0
for batch,source,qa,ids,review in specs:
 files=set(subprocess.check_output(['git','ls-tree','-r','--name-only',source],text=True).splitlines());qfiles=set(subprocess.check_output(['git','ls-tree','-r','--name-only',qa],text=True).splitlines())
 review_bytes=read(qa,review);text=review_bytes.decode();assert source in text
 batches.append({'batch':batch,'source_commit':source,'review_commit':qa,'ids':ids,'review':{'path':review,'sha256':sha(review_bytes)}})
 for id in ids:
  cp=f'production/continuous-small-life-round02-20261018/work/batch-{batch}/{id}/r001/candidate.json';c=js(source,cp);folder=posixpath.dirname(c['artifacts']['glb']['path']);work=posixpath.dirname(cp);mp=folder+'/metadata.json';m=js(source,mp);assert m['id']==id
  pins={};declared_pins=[]
  def pin(path,ref=source):
   b=read(ref,path);pins[path]={'path':path,'sha256':sha(b),'bytes':len(b),'git_commit':ref};return pins[path]
  def resolve(path,doc,ref=source):
   fs=files if ref==source else qfiles
   if path.startswith('/workspace/lowpoly-vault/'):path=path[len('/workspace/lowpoly-vault/'):]
   opts=[path,posixpath.normpath(posixpath.join(posixpath.dirname(doc),path)),posixpath.normpath(posixpath.join(posixpath.dirname(posixpath.dirname(doc)),path)),posixpath.join(folder,path),posixpath.join(work,path)]
   return next((p for p in opts if p in fs),None)
  def walk(x,doc,ref=source):
   global declared
   if isinstance(x,dict):
    if isinstance(x.get('path'),str)and re.fullmatch('[a-f0-9]{64}',str(x.get('sha256',''))):
     p=resolve(x['path'],doc,ref);assert p,(id,'unresolved pin',doc,x['path']);pinned=pin(p,ref);assert pinned['sha256']==x['sha256'],(id,p,'hash mismatch')
     if 'bytes'in x:assert pinned['bytes']==x['bytes']
     if 'byte_length'in x:assert pinned['bytes']==x['byte_length']
     declared+=1;declared_pins.append(pinned)
    for v in x.values():walk(v,doc,ref)
   elif isinstance(x,list):
    for v in x:walk(v,doc,ref)
  pin(cp);walk(c,cp);pin(mp);walk(m,mp)
  glb=pin(m['glb']);blend=pin(m['blend']);assert glb['sha256']==m['sha256']['glb']==c['artifacts']['glb']['sha256'];assert blend['sha256']==m['sha256']['blend']==c['artifacts']['source']['sha256'];assert glb['bytes']==m['glb_bytes']
  assert glb['sha256']in text and blend['sha256']in text,(id,'QA exact payload binding');assert any(id.lower() in line.lower()and 'PASS'in line for line in text.splitlines()),(id,'perasset QA PASS')
  vp=folder+'/views/manifest.json'if batch=='04'else folder+'/view-manifest.json'if batch=='05'else work+'/source-view-manifest.json';v=js(source,vp);pin(vp);walk(v,vp)
  if batch!='06':assert v['glb_sha256']==glb['sha256']and v['turntable_frames']==0
  rp=c['artifacts'].get('runtime',{}).get('path')or(folder+'/runtime/single.json'if batch=='05'else work+f'/runtime-attempt-01/{id}.json');r=js(source,rp);pin(rp);walk(r,rp);zero_errors(r);assert r['status']=='pass'and r['glb_sha256']==glb['sha256'];assert r['webgl2']is True and r['views']and all(x['triangles']>0 for x in r['views'])
  # Bind every existing runtime screenshot even when its original report omitted per-image hashes.
  for view in r['views']:
   p=resolve(view['path'],rp);assert p,(id,'runtime screenshot',view['path']);pin(p)
  source_export=folder+'/technical/source-export.json'if batch=='04'else work+'/source-export.json';s=js(source,source_export);pin(source_export);assert s['status']in ['pass','pass_with_warnings']and s['errors']==[]and s['triangles_match']is True and s['bounds_match']is True and s['source_sha256']==blend['sha256']and s['glb_sha256']==glb['sha256']
  validator=folder+'/gltf-validator.report.json';k=js(source,validator);pin(validator);assert k['issues']['numErrors']==0 and k['issues']['numWarnings']==0 and k['issues']['truncated']is False
  brief=js(source,c['artifacts']['brief']['path']);assert brief['turntable_frames']==0 and set(brief['required_views'])==STATIC_VIEWS
  scene='production/continuous-small-life-round02-20261018/work/batch-04/runtime-scene-attempt-02/scene.json'if batch=='04'else folder+'/runtime/scene.json'if batch=='05'else'production/continuous-small-life-round02-20261018/work/batch-06/runtime-scene-attempt-01/scene.json'
  if scene not in files:
   options=[p for p in files if '/batch-'+batch+'/'in p and p.endswith('/scene.json')];print('scene options',batch,options,flush=True);scene=options[-1]
  sc=js(source,scene);pin(scene);walk(sc,scene);zero_errors(sc);assert sc['status']=='pass'and sc['views']and all(x['triangles']>0 for x in sc['views']);assert sc.get('instances',0)>=2
  # Immutable helper snapshots are evidence, never replacements for current shared scripts.
  dependencies=[]
  for p in ['scripts/asset_common.py','scripts/render_exact_glb_views.py','package-lock.json']:
   if p in files:dependencies.append({'original_path':p,'sha256':sha(read(source,p))})
  row={'id':id,'batch':batch,'source_commit':source,'review_commit':qa,'review':batches[-1]['review'],'candidate':pin(cp),'source_metadata':pin(mp),'metadata':m,'glb':glb,'blend':blend,'views':pin(vp),'runtime':pin(rp),'source_export':pin(source_export),'validator':pin(validator),'scene':pin(scene),'evidence':list(pins.values()),'dependencies':dependencies,'declared_pins_verified':len(declared_pins)}
  rows.append(row);print(id,glb['bytes'],glb['sha256'],'source/validator/runtime/scene/PASS bound',flush=True)
assert len(rows)==12 and len(set(r['id']for r in rows))==12
out={'status':'pass','rule_version':'2026-10-18.1','scope':'Read-only frozen Git-object hashes and existing independent source/export/validator/runtime/scene evidence. No modeling or rerendering; full candidate validity remains separately reported.','verified_declared_pins':declared,'batches':batches,'assets':rows}
Path('/tmp/lowpoly-round02-source-audit-recheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')

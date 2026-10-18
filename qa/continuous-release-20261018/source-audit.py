import subprocess,json,hashlib,re,posixpath
from pathlib import Path
specs=[('01','e7798a7064ef513cab6dc78b54d70f25cbd38c59','e156005f24970ab7a0a60ab2ffdaa639d04e16f5',['archaeopteryx','canadaspis','ceratomyrmex','hydropteris'],'production/continuous-small-life-20261018/work/batch-01/independent-qa-report.md'),('02','29b0ceb97ae74d77846f7576cf9552fe178accb9','30ceb9ee050824d7d825df84d49bda4abc9f875a',['longipteryx','urasterella','alienopterus','aglaophyton'],'production/continuous-small-life-20261018/reviews/batch-02/independent-gpt6-luna-xhigh/INDEPENDENT-QA.md'),('03','da240359dabe69c775c9d251d6530cf30db25dad','12e1024ac57b7d09a92cfbf08bb7881ace5fff54',['cephalaspis','saccocoma','archaeocidaris','onoclea'],'qa/continuous-small-life-20261018/batch-03/independent-review/review.md')]
def read(ref,p):return subprocess.check_output(['git','show',ref+':'+p],stderr=subprocess.PIPE)
def js(ref,p):return json.loads(read(ref,p))
def sha(b):return hashlib.sha256(b).hexdigest()
rows=[];reports=[];pin_count=0
for batch,source,qa,ids,review in specs:
 files=set(subprocess.check_output(['git','ls-tree','-r','--name-only',source],text=True).splitlines())
 review_bytes=read(qa,review);text=review_bytes.decode();assert source in text,(batch,'review source binding')
 assert all(id in text and re.search(r'(?:###\s+'+re.escape(id)+r'\b[^\n]*PASS|`'+re.escape(id)+r'`[^\n]*PASS)',text,re.I) for id in ids),(batch,'per-asset PASS headings')
 reports.append({'batch':batch,'source_commit':source,'review_commit':qa,'review':{'path':review,'sha256':sha(review_bytes)},'ids':ids,'qa_verdict_preserved':'all-four-pass'})
 for id in ids:
  if batch=='01':candidate=f'assets/candidates/continuous-small-life-20261018/batch-01/{id}/r001/candidate.json'
  elif batch=='02':candidate=f'assets/candidates/continuous-small-life-20261018/batch-02/r001/{id}/candidate.json'
  else:
   rev='r002'if id=='onoclea'else'r001';candidate=f'production/continuous-small-life-20261018/work/batch-03/{id}/{rev}/candidate.json'
  c=js(source,candidate)
  metadata=(posixpath.dirname(candidate)+'/source-metadata.json')if batch=='01'else(posixpath.dirname(candidate)+'/metadata.json')if batch=='02'else c['artifacts']['metadata']['path']
  m=js(source,metadata);assert m['id']==id
  glb=read(source,m['glb']);blend=read(source,m['blend']);assert sha(glb)==m['sha256']['glb'] and sha(blend)==m['sha256']['blend'];assert len(glb)==m['glb_bytes']
  if batch=='02':assert c['files'][id+'.glb']['sha256']==sha(glb) and c['files'][id+'.blend']['sha256']==sha(blend)
  else:assert c['artifacts']['glb']['sha256']==sha(glb) and c['artifacts']['source']['sha256']==sha(blend)
  pins=[]
  def walk(x,doc):
   global pin_count
   if isinstance(x,dict):
    if isinstance(x.get('path'),str) and re.fullmatch('[0-9a-f]{64}',str(x.get('sha256',''))):
     p=x['path'];p=p if p in files else posixpath.normpath(posixpath.join(posixpath.dirname(doc),p))
     assert p in files,(batch,id,'unresolved declared pin',x['path'],doc)
     b=read(source,p);assert sha(b)==x['sha256'],(batch,id,'pin mismatch',p)
     if 'bytes'in x:assert len(b)==x['bytes'],p
     pins.append({'path':p,'sha256':x['sha256']});pin_count+=1
    for v in x.values():walk(v,doc)
   elif isinstance(x,list):
    for v in x:walk(v,doc)
  walk(c,candidate)
  if batch=='02':
   for p,v in c['files'].items():
    b=read(source,posixpath.dirname(candidate)+'/'+p);assert sha(b)==v['sha256'] and len(b)==v['bytes'],(id,p);pin_count+=1
  validator=posixpath.dirname(m['glb'])+'/gltf-validator.report.json';v=js(source,validator);assert v['issues']['numErrors']==v['issues']['numWarnings']==0
  row={'id':id,'batch':batch,'source_commit':source,'qa_commit':qa,'candidate':{'path':candidate,'sha256':sha(read(source,candidate))},'source_metadata':{'path':metadata,'sha256':sha(read(source,metadata))},'glb':{'path':m['glb'],'sha256':sha(glb),'bytes':len(glb)},'blend':{'path':m['blend'],'sha256':sha(blend),'bytes':len(blend)},'validator':{'path':validator,'sha256':sha(read(source,validator))},'review':{'path':review,'sha256':sha(review_bytes)},'source_pins_verified':len(pins),'metadata':m}
  if batch=='01':row['runtime']=c['technical_evidence']['runtime'];row['views']=c['technical_evidence']['views']
  elif batch=='02':
   root=posixpath.dirname(candidate);row['runtime']={'path':root+'/runtime/report.json','sha256':sha(read(source,root+'/runtime/report.json'))};row['views']={'path':root+'/evidence-manifest.json','sha256':sha(read(source,root+'/evidence-manifest.json'))}
  else:row['runtime']=c['artifacts']['browser'];row['views']=c['artifacts']['views']
  runtime=js(source,row['runtime']['path']);assert runtime.get('status')=='pass' and runtime.get('glb_sha256')==sha(glb);
  def zero_errors(x):
   if isinstance(x,dict):
    for k,v in x.items():
     if k in ['errors','failed','page_errors','pageErrors','consoleErrors','resource_errors']:assert not v,(id,k,v)
     if k=='gl_error':assert v==0,(id,k,v)
     zero_errors(v)
   elif isinstance(x,list):
    for v in x:zero_errors(v)
  zero_errors(runtime);walk(js(source,row['views']['path']),row['views']['path']);row['runtime_status']=runtime.get('status');row['runtime_keys']=list(runtime);rows.append(row)
  print(id,len(glb),sha(glb),row['runtime_status'],flush=True)
assert len(rows)==12 and len({r['id']for r in rows})==12
out={'status':'pass','scope':'Read-only Git object hashes and independent review/source bindings; no geometry re-export, image regeneration or QA verdict changes','verified_declared_pins':pin_count,'reviews':reports,'assets':rows}
Path(__file__).with_name('source-audit-recheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('Verified declared pins',pin_count)

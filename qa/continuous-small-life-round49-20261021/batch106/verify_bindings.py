import json,hashlib,pathlib,datetime,subprocess,os
from PIL import Image
R=pathlib.Path('/workspace/shared/lowpoly-batch106-20261021');B=R/'production/small-life-batch106'; O=pathlib.Path(__file__).parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest(); errors=[]; checks=[]
def pin(p,s,scope):
 p=pathlib.Path(p);p=p if p.is_absolute() else R/p
 ok=p.exists() and h(p)==s; checks.append({'path':str(p),'sha256':h(p) if p.exists() else None,'expected':s,'scope':scope,'pass':ok})
 if not ok:errors.append(str(p))
for f,s in [('handoff.json','07fea59f653f2b5ac2df46e2287ee066088262389f5f141556759053577703c5'),('delivery-manifest.json','6d838da974adcd0081d1af45b615182cfa3a969d4785d153294753ba2f25141a'),('original-freeze-manifest.json','2c2492abded0b815a3d6c0a3e9850769157b829bc96553ae6e24b1a116794675')]:pin(B/f,s,'intake')
for file,scope in [('original-freeze-manifest.json','original freeze'),('build-dependencies.json','dependency closure')]:
 for f in json.loads((B/file).read_text())['files']:pin(f['path'],f['sha256'],scope)
for aid,rev in [('didymograptus','r004'),('monograptus','r004'),('diplograptus','r009'),('dictyonema','r005')]:
 d=B/aid/rev;c=json.loads((d/'candidate.json').read_text());sub={'revision':rev,'glb_sha256':c['artifacts']['glb']['sha256'],'brief_sha256':c['artifacts']['brief']['sha256'],'references_sha256':c['artifacts']['references']['sha256']}
 for k,v in c['artifacts'].items():pin(v['path'],v['sha256'],aid+' candidate '+k)
 for e in c['evidence']:
  pin(e['path'],e['sha256'],aid+' evidence');assert e['subject']==sub
 refs=json.loads((B/aid/'r001/references.json').read_text())
 for ref in refs['sources']:
  assert ref['rights_note'] and ref['incorporated']==False
  for f in ref.get('consult_only_files',[]):pin(f['path'],f['sha256'],'reference')
 for mf in d.glob('*/render-manifest.json'):
  m=json.loads(mf.read_text());
  for f in m['frames']:
   fp=mf.parent/f['path'];pin(fp,f['sha256'],'actual image');assert Image.open(fp).size==(f['width'],f['height'])
  # full subject keys may be direct fields or nested; preserve for exact inspection
 for nm in ['rebuild-a-execution.json','rebuild-b-execution.json','rebuild-a-request.json','rebuild-b-request.json','rebuild-a-result.json','rebuild-b-result.json']:
  x=json.loads((d/'qa'/nm).read_text());(O/(aid+'-'+nm)).write_text(json.dumps(x,indent=2))
result={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'errors':errors,'checks':checks,'status':'PASS' if not errors else 'FAIL'};(O/'bindings.json').write_text(json.dumps(result,indent=2));print(result['status'],len(checks),errors)

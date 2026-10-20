import subprocess,json,re,hashlib,datetime
from pathlib import Path
w='/workspace/shared/lowpoly-deterministic-ci';base=Path('/workspace/shared/lowpoly-round31-coordination');ids=['rangea','natural-levee','serac','boudinaged-rock-layer','ernietta','oxbow-lake-basin','moulin-shaft','solifluction-lobe'];patterns={i:re.compile(r'(?:^|/)'+re.escape(i)+r'(?:/|\.glb$|\.blend$|\.json$)') for i in ids};refs=[];conflicts={};errors=[]
for line in (base/'remote-refs.txt').read_text().splitlines():
 sha,ref=line.split()
 if not (ref=='refs/heads/main' or any(ref.startswith('refs/heads/'+x) for x in ['candidate/','production/','release/'])):continue
 r=subprocess.run(['git','-C',w,'ls-tree','-r','--name-only',sha],capture_output=True,text=True)
 if r.returncode:errors.append({'sha':sha,'ref':ref,'error':r.stderr[:200]});continue
 lines=r.stdout.splitlines();refs.append({'ref':ref,'sha':sha,'paths':len(lines)})
 for i,p in patterns.items():
  hits=[s for s in lines if p.search(s)]
  if hits:conflicts.setdefault(i,[]).append({'ref':ref,'paths':hits[:5]})
obj=subprocess.check_output(['git','-C',w,'rev-list','--objects','--all'],text=True);hist={}
for i,p in patterns.items():
 hits=[s.partition(' ')[2] for s in obj.splitlines() if p.search(s.partition(' ')[2])]
 if hits:hist[i]=hits[:10]
active=[]
for root in [Path('/workspace/shared'),Path('/tmp')]:
 for f in root.glob('lowpoly-round*-coordination/batch-*-claim.json'):
  try:d=json.loads(f.read_text())
  except Exception:continue
  hits=set(d.get('ids',[]))&set(ids)
  if hits:active.append({'claim':str(f),'matches':sorted(hits)})
for n in [76,77]:
 if subprocess.run(['git','-C',w,'show-ref','--verify','--quiet',f'refs/heads/candidate/small-life-batch{n}-concept-20261020']).returncode==0:errors.append({'existing_branch':n})
now=datetime.datetime.now(datetime.timezone.utc).isoformat();report={'checked_at':now,'selected':ids,'scope':'Fresh all current main/candidate/production/release remote heads, all locally reachable historical Git object paths, and active shared/tmp batch claims; UI-only heads excluded; prospective local branches absent','refs':refs,'conflicts':conflicts,'historical_conflicts':hist,'active_conflicts':active,'errors':errors,'status':'PASS' if not(conflicts or hist or active or errors) else 'BLOCKED'};(base/'preclaim-dedup.json').write_text(json.dumps(report,indent=2)+'\n');print('dedup',report['status'],'refs',len(refs),'errors',errors,'conflicts',conflicts,'historic',hist,'active',active)
assert report['status']=='PASS'
blob=subprocess.check_output(['git','-C',w,'show','54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c:research/prehistoric-1000-v1/inventory.json']);sha=hashlib.sha256(blob).hexdigest();assert sha=='b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c';inv=json.loads(blob);selected=[x for x in inv['assets'] if x['id'] in ids];assert len(selected)==8
(base/'selected-inventory.json').write_text(json.dumps({'source_inventory_commit':'54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c','source_inventory_path':'research/prehistoric-1000-v1/inventory.json','source_inventory_sha256':sha,'assets':selected},indent=2,ensure_ascii=False)+'\n')
for n,sel in [(76,ids[:4]),(77,ids[4:])]:
 (base/f'batch-{n}-claim.json').write_text(json.dumps({'round':31,'batch':n,'ids':sel,'base_main':'54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c','claimed_at':now,'status':'exclusive reserved scope; no actual maker task, frozen brief or model yet. Actual primary pixels/concepts/complete freeze and free maker lane still required.'},indent=2)+'\n')
(base/'status.json').write_text(json.dumps({'round':31,'updated_at':now,'status':'two next scopes reserved after fresh dedup; no maker dispatched or geometry created','batch76':{'ids':ids[:4],'status':'reserved, awaiting actual freed maker lane'},'batch77':{'ids':ids[4:],'status':'reserved, awaiting actual freed maker lane'},'dedup_refs':len(refs)},indent=2)+'\n')

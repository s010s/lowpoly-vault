import json,subprocess,concurrent.futures,datetime
from pathlib import Path
w='/workspace/shared/lowpoly-deterministic-ci';b=Path('/workspace/shared/lowpoly-round31-coordination');inv=json.loads(subprocess.check_output(['git','-C',w,'show','54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c:research/prehistoric-1000-v1/inventory.json']))['assets'];allids={x['id'] for x in inv};refs=json.loads((b/'preclaim-dedup.json').read_text())['refs']
def get(r):
 s=subprocess.check_output(['git','-C',w,'ls-tree','-r','--name-only',r['sha']],text=True);found=set()
 for p in s.splitlines():
  parts=p.split('/');found.update(allids.intersection(parts));found.update(allids.intersection([parts[-1].removesuffix('.glb').removesuffix('.blend')]))
 return r['ref'],sorted(found)
res=dict(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(get,refs));used=set().union(*[set(x) for x in res.values()]);active=set()
for root in [Path('/workspace/shared'),Path('/tmp')]:
 for f in root.glob('lowpoly-round*-coordination/batch-*-claim.json'):
  try:active.update(json.loads(f.read_text()).get('ids',[]))
  except:pass
out={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'snapshot':'remote-refs.txt','relevant_ref_count':len(refs),'used_ids':sorted(used),'active_claim_ids':sorted(active),'per_ref_ids':res};(b/'current-path-id-cache.json').write_text(json.dumps(out,indent=2)+'\n')
print('unused geological IDs:');print([x['id'] for x in inv if x['representation']=='geological-form' and x['id'] not in used|active]);print('unused trace IDs:');print([x['id'] for x in inv if x['representation']=='trace-concept' and x['id'] not in used|active])

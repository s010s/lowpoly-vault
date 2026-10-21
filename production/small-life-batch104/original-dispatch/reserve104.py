from pathlib import Path
import json,subprocess,hashlib,datetime,re,os
os.environ.update(GIT_NO_LAZY_FETCH="1",GIT_TERMINAL_PROMPT="0")
b=Path('/workspace/shared/lowpoly-round47-coordination');old=Path('/workspace/shared/lowpoly-round31-coordination');w='/workspace/shared/lowpoly-deterministic-ci'
cache=json.loads((old/'current-path-id-cache.json').read_text())
ids=['kerygmachela','pambdelurion','aegirocassis','arthropleura']
pat={i:re.compile(r'(?:^|/)'+re.escape(i)+r'(?:/|\.glb$|\.blend$|\.json$)') for i in ids}
oldrefs={line.split()[1]:line.split()[0] for line in (old/'remote-refs.txt').read_text().splitlines()};newrefs={line.split()[1]:line.split()[0] for line in (b/'remote-refs-preclaim.txt').read_text().splitlines()};conf=[];checked=[]
for ref,sha in newrefs.items():
 if not(ref=='refs/heads/main' or any(ref.startswith('refs/heads/'+x) for x in ['candidate/','production/','release/'])):continue
 if oldrefs.get(ref)==sha and ref in cache['per_ref_ids']:
  hits=sorted(set(ids)&set(cache['per_ref_ids'][ref]));method='immutable unchanged-head tree-ID cache'
 else:
  names=subprocess.check_output(['git','-c','protocol.allow=never','-C',w,'ls-tree','-r','--name-only',sha],text=True).splitlines();hits=[i for i,p in pat.items() if any(p.search(n) for n in names)];method='fresh exact-head tree scan'
 checked.append({'ref':ref,'sha':sha,'method':method})
 if hits:conf.append({'ref':ref,'ids':hits})
obj=subprocess.check_output(['git','-c','protocol.allow=never','-C',w,'rev-list','--objects','--all'],text=True).splitlines()
for i,p in pat.items():
 hits=[s.partition(' ')[2] for s in obj if p.search(s.partition(' ')[2])]
 if hits:conf.append({'historic_id':i,'paths':hits[:5]})
for root in [Path('/workspace/shared'),Path('/tmp')]:
 for f in root.glob('lowpoly-round*-coordination/batch-*-claim.json'):
  try:d=json.loads(f.read_text())
  except Exception:continue
  hits=set(ids)&set(d.get('ids',[]))
  if hits:conf.append({'claim':str(f),'ids':sorted(hits)})
for n in [104]:
 if subprocess.run(['git','-c','protocol.allow=never','-C',w,'show-ref','--verify','--quiet',f'refs/heads/candidate/small-life-batch{n}-concept-20261021']).returncode==0:conf.append({'existing_branch':n})
assert len(newrefs)>=150 and 'refs/heads/main' in newrefs
now=datetime.datetime.now(datetime.timezone.utc).isoformat();report={'checked_at':now,'ids':ids,'status':'PASS' if not conf else 'BLOCKED','scope':'fresh all relevant current remoteheads with immutable sameSHA cache plus changed-head scan, all locally reachable historical paths, fresh active claims and prospective branch absence','refs':checked,'ref_count':len(checked),'cache':str(old/'current-path-id-cache.json'),'cache_sha256':hashlib.sha256((old/'current-path-id-cache.json').read_bytes()).hexdigest(),'conflicts':conf};(b/'preclaim-dedup.json').write_text(json.dumps(report,indent=2)+'\n');print('result',report['status'],'refs',len(checked),'conflicts',conf);assert not conf
invcommit='54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c';base='43e40fc89f2b369a5f1858e72fa58a0d10418124'
blob=subprocess.check_output(['git','-c','protocol.allow=never','-C',w,'show',invcommit+':research/prehistoric-1000-v1/inventory.json']);sha=hashlib.sha256(blob).hexdigest();assert sha=='b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c';inv=json.loads(blob)
for n,sel in [(104,ids)]:
 assert not (b/f'batch-{n}-claim.json').exists()
 a=[x for x in inv['assets'] if x['id'] in sel];assert len(a)==4
 (b/f'batch-{n}-selected-inventory.json').write_text(json.dumps({'source_inventory_commit':invcommit,'source_inventory_path':'research/prehistoric-1000-v1/inventory.json','source_inventory_sha256':sha,'assets':a},indent=2,ensure_ascii=False)+'\n')
 (b/f'batch-{n}-claim.json').write_text(json.dumps({'round':47,'batch':n,'ids':sel,'base_main':base,'claimed_at':now,'status':'exclusive future reservation only, no maker/geometry yet; complete concept/source/freeze gates mandatory'},indent=2)+'\n')
 r=json.loads((Path('/workspace/shared/lowpoly-round36-coordination')/'batch-86-concept-plan-requirements.json').read_text());r.update(created_at=now,base_main=base,asset_ids=sel,reference_preflight='No inspected reference preflight yet; maker must research primary text and actual pixels',maker='Current compliant inherited model; do not interrupt production to restore historical model selection',independent_qa='One fresh-context full independent review per exact four-ID batch pinned to immutable commit and GLB hashes; actual repairs receive targeted difference review',addendum='/workspace/shared/lowpoly-round36-coordination/PRODUCTION-ADDENDUM.md',lean_git='Only necessary final deliverables and compact required proof indexed in Git. Keep full original process evidence local. Source URL must point to actual uploaded lean commit after verified push. No uploading historical process ancestors merely to preserve old source URL.');r['future_numeric_preflight']='Distinguish evidence/user hard limits from nominal artistic targets before freeze; do not invent microscopic hard gates. Actual final transformed component geometry and all relevant contact directions must verify original genuine bounds. Existing earlier freezes unchanged.';(b/f'batch-{n}-concept-plan-requirements.json').write_text(json.dumps(r,indent=2)+'\n')
(b/'future-reservations.json').write_text(json.dumps({'round':47,'updated_at':now,'status':'one future scope reserved after actual fresh dedup; not maker dispatched','batches':[104],'slot_priority':'102/103 remain actual makers;104 reserved for next actual maker completion.100 independent QA active,101 queued.','no_reference_or_concept_or_geometry_claim':True},indent=2)+'\n')

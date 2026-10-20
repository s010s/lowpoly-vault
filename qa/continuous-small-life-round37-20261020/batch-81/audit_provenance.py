import sys,json,pathlib,hashlib,datetime,subprocess
r=pathlib.Path('/workspace/shared/lowpoly-batch81-20261020');o=pathlib.Path(__file__).parent;sys.path.insert(0,str(r/'scripts'));sys.dont_write_bytecode=True
from check_reproducibility import compare_rebuild
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();summary=[]
for a in json.load(open(r/'production/small-life-batch81/handoff.json'))['assets']:
 p=r/a['path'];d=o/a['asset_id'];orig=p.parent/'r001';f=json.load(open(p/'modeling-freeze.json'));g=json.load(open(p/'concept-generation.json'));life=[json.loads(t) for t in (p/'lifecycle.jsonl').read_text().splitlines()];pre=json.load(open(p/'preproof-binding.json'));ren=next(e for e in life if e['stage']=='proof-final');build=next(e for e in life if e['stage']=='build');repair=json.load(open(p/'repair-freeze.json'));br=json.load(open(p/'brief.json'));deliv=json.load(open(p/'candidate-brief.json'))
 changes={k for k in set(br)|set(deliv) if br.get(k)!=deliv.get(k)};assert changes=={'required_deliverables','packaging_adapter'},changes
 assert g['invoked_at']<g['returned_at']<g['inspected_at']<f['frozen_at']<build['started_at']
 assert repair['created_at']<build['started_at'];assert repair['generator_sha256']==a['hashes']['generator'];assert pre['checked_at']<ren['started_at']<ren['ended_at'];assert ren['exit_code']==0
 refs=[]
 for e in json.load(open(p/'references.json'))['sources']:assert e.get('rights_note') and e.get('incorporated') is False
 runs=[]
 for rb in json.load(open(p/'final-rebuild-binding.json'))['distinct_real_queue_runs']:
  q=r/rb['path'];req=json.load(open(q/'request.json'));res=json.load(open(q/'result.json'));assert sha(q/'request.json')==rb['request_sha256'];assert sha(q/'result.json')==rb['result_sha256'];assert res['pid']==rb['pid'];assert res['returncode']==0 and res['status']=='succeeded';assert res['started_at']<res['finished_at'];assert req['identity']['threads']==2;assert res['job_id'] in ['semantic-rebuild-1','semantic-rebuild-2']
  for role,fi in req['identity']['inputs'].items():assert sha(pathlib.Path(fi['path']))==fi['sha256'],(a['asset_id'],role)
  for file,fi in res['outputs'].items():assert sha(q/'outputs'/file)==fi['sha256'];assert (q/'outputs'/file).stat().st_size==fi['bytes']
  log=(q/'stdout.log').read_text();assert 'BUILT '+a['asset_id']+' '+a['hashes']['glb'] in log and 'Blender quit' in log
  rep=compare_rebuild(p/'model.glb',q/'outputs/model.glb',p/'generator.py',p/'build-config.json',q/'request.json',q/'result.json','model.glb',r);assert rep['status']=='pass';(d/(res['job_id']+'-fresh-comparison.json')).write_text(json.dumps(rep,indent=2)+'\n')
  runs.append({'path':rb['path'],'pid':res['pid'],'job_id':res['job_id'],'started_at':res['started_at'],'finished_at':res['finished_at'],'request_sha256':sha(q/'request.json'),'result_sha256':sha(q/'result.json'),'stdout_sha256':sha(q/'stdout.log'),'output_glb_sha256':sha(q/'outputs/model.glb'),'semantic_sha256':rep['semantic_sha256'],'semantic_match':True,'byte_identical':rep['byte_identical']})
 assert len(runs)==2 and len({x['pid'] for x in runs})==2 and len({x['path'] for x in runs})==2
 for kind,args in [('candidate-profile',['validate_candidate.py',str(p/'candidate.json'),'--root',str(r),'--profile','static-stylized-v1','--profile-contract',str(p/'profile-contract.json'),'--json']),('concept-corrected-cli',['validate_concept_evidence.py',str(p/'concept-evidence.json'),'--root',str(p)])]:
  command=[sys.executable,str(r/'scripts'/args[0])]+args[1:];run=subprocess.run(command,capture_output=True,text=True);(d/(kind+'-fresh.json')).write_text(run.stdout);assert run.returncode==0,(kind,run.stdout,run.stderr)
 summary.append({'asset_id':a['asset_id'],'revision':a['revision'],'concept_observed':g,'frozen_at':f['frozen_at'],'build_started_at':build['started_at'],'repair_freeze_at':repair['created_at'],'delivery_brief_changes_only':sorted(changes),'preproof_at':pre['checked_at'],'proof_started_at':ren['started_at'],'proof_finished_at':ren['ended_at'],'runs':runs,'limitation':'Retained process records and stdout provide observed execution provenance, not cryptographic proof. Provider internal generation time/ID and precise generator-authoring start unknown; exact observer times and original concepts retained. No filesystem mtime inference.'})
(o/'provenance-audit.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assets':summary},indent=2)+'\n');print('All four chronology, schema/profile, retained process rebuild outputs and fresh semantic comparison checks pass.')

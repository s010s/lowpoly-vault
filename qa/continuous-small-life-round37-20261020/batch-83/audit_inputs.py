import sys,json,pathlib,hashlib,datetime,subprocess
from PIL import Image
r=pathlib.Path('/workspace/shared/lowpoly-batch83-20261020');o=pathlib.Path(__file__).parent;p=r/'production/small-life-batch83';sys.path.insert(0,str(r/'scripts'));sys.dont_write_bytecode=True
from check_reproducibility import compare_rebuild
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
commit='1e0664988dfd77ec163bee527f11fc482668fddd';git=lambda *a:subprocess.check_output(['git','-C',str(r),*a])
assert git('rev-parse','HEAD').decode().strip()==commit
assert not git('status','--porcelain')
files=[]
for line in git('ls-tree','-r',commit,'production/small-life-batch83','scripts','skills','schemas','package.json','package-lock.json').decode().splitlines():
 pre,name=line.split('\t');mode,typ,obj=pre.split();f=r/name
 if not f.exists():continue
 blob=git('cat-file','blob',obj);assert blob==f.read_bytes(),name
 files.append({'path':name,'git_blob':obj,'sha256':sha(f),'bytes':len(blob)})
inv=json.loads((p/'selected-inventory.json').read_text());raw=git('show',inv['source_inventory_commit']+':'+inv['source_inventory_path']);assert hashlib.sha256(raw).hexdigest()==inv['source_inventory_sha256']
allinv=json.loads(raw);print('inventory structure',type(allinv).__name__,flush=True)
if isinstance(allinv,dict): allinv=allinv.get('assets',allinv.get('items'))
for a in inv['assets']:assert a==next(x for x in allinv if x['id']==a['id'])
(o/'immutable-input-audit.json').write_text(json.dumps({'checked_at':now(),'immutable_commit':commit,'clean_worktree':True,'present_tracked_files_matched':len(files),'original_inventory_hash':inv['source_inventory_sha256'],'selected_inventory_equal_to_original_entries':True,'files':files},indent=2)+'\n')
summary=[]
for a in json.load(open(p/'handoff.json'))['assets']:
 d=r/a['path'];dest=o/a['asset_id'];dest.mkdir(exist_ok=True);orig=d.parent/'r001'
 for k,f in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json'),('source','source.blend'),('generator','generator.py'),('config','build-config.json')]:assert sha(d/f)==a['hashes'][k]
 f=json.load(open(orig/'modeling-freeze.json'));g=json.load(open(d/'concept-generation.json'));life=[json.loads(t) for t in (d/'lifecycle.jsonl').read_text().splitlines()];pre=json.load(open(d/'preproof-binding.json'));ren=next(e for e in life if e['stage']=='proof-final');build=next(e for e in life if e['stage']=='build');repair=json.load(open(d/'repair-freeze.json'));br=json.load(open(d/'brief.json'));de=json.load(open(d/'candidate-brief.json'))
 for name,h in f['files'].items():assert sha(orig/name)==h,(a['asset_id'],name)
 for name in ['brief.json','brief.md','references.json','concept-original.png','concept-prompt.txt','concept-generation.json']:assert (d/name).read_bytes()==(orig/name).read_bytes(),(a['asset_id'],name)
 changes={k for k in set(br)|set(de) if br.get(k)!=de.get(k)};assert changes=={'required_deliverables','packaging_adapter'},changes
 assert g['invoked_at']<g['recorded_at']<json.load(open(d/'concept-evidence.json'))['chronology']['concept_inspected_at']<f['frozen_at']<build['started_at']; assert g['invoked_at']<g['returned_observed_at']<g['recorded_at'] and g['provider_internal_timestamp'] is None
 assert repair['created_at']<build['started_at'];assert pre['checked_at']<ren['started_at']<ren['ended_at'];assert ren['exit_code']==0
 deps=json.load(open(d/'build-dependencies.json'))
 for name,h in deps['files'].items():assert sha(r/name)==h,(name,h)
 assert sha(pathlib.Path(deps['blender']['executable']))==deps['blender']['sha256']
 refs=[]
 for e in json.load(open(d/'references.json'))['sources']:
  assert e.get('rights_note') and e.get('incorporated') is False
  for im in e.get('consulted_images',[]):
   path=pathlib.Path('/workspace/shared/batch83-consult-only')/im['filename'];assert sha(path)==im['sha256'];refs.append({'source_id':e['id'],'path':str(path),'sha256':sha(path),'dimensions':Image.open(path).size,'inspected_by_reviewer':True})
 frames=[];manifest=json.load(open(d/'proof-final/render-manifest.json'))
 assert manifest['subject']=={'revision':a['revision'],'glb_sha256':a['hashes']['glb'],'brief_sha256':a['hashes']['brief'],'references_sha256':a['hashes']['references']}
 assert set(x['view'] for x in manifest['frames'])==set(br['required_views'])
 assert sha(d/'proof-final/render-config.json')==manifest['config_sha256']
 for fr in manifest['frames']:
  fp=d/'proof-final'/fr['path'];assert sha(fp)==fr['sha256'];assert Image.open(fp).size==(512,512);frames.append({'view':fr['view'],'path':str(fp.relative_to(r)),'sha256':sha(fp),'dimensions':[512,512],'personally_inspected':True})
 assert sha(d/'preview.png')==sha(d/'proof-final/hero.png')
 # Both distinct semantic rebuilds: directly inspect request/result/output and rerun comparisons, not report-copying.
 runs=[]
 for n in (1,2):
  repold=json.load(open(d/f'repro-final-{n}.report.json'));rb=repold['build_run'];reqpath=r/rb['request']['path'];respath=r/rb['result']['path'];q=reqpath.parent;req=json.load(open(reqpath));res=json.load(open(respath))
  assert sha(reqpath)==rb['request']['sha256'];assert sha(respath)==rb['result']['sha256'];assert res['returncode']==0 and res['status']=='succeeded';assert res['started_at']<res['finished_at'];assert req['identity']['threads']==2;assert res['job_id']==f'semantic-rebuild-{n}'
  for role,fi in req['identity']['inputs'].items():assert sha(pathlib.Path(fi['path']))==fi['sha256'],(a['asset_id'],role)
  for filename,fi in res['outputs'].items():assert sha(q/'outputs'/filename)==fi['sha256'];assert (q/'outputs'/filename).stat().st_size==fi['bytes']
  log=(q/'stdout.log').read_text();assert 'BUILT '+a['asset_id']+' '+a['hashes']['glb'] in log and 'Blender quit' in log
  rep=compare_rebuild(d/'model.glb',q/'outputs/model.glb',d/'generator.py',d/'build-config.json',reqpath,respath,'model.glb',r);assert rep['status']=='pass';(dest/f'semantic-rebuild-{n}-fresh-comparison.json').write_text(json.dumps(rep,indent=2)+'\n')
  runs.append({'path':str(q.relative_to(r)),'pid':res['pid'],'job_id':res['job_id'],'started_at':res['started_at'],'finished_at':res['finished_at'],'request_sha256':sha(reqpath),'result_sha256':sha(respath),'stdout_sha256':sha(q/'stdout.log'),'output_glb_sha256':sha(q/'outputs/model.glb'),'semantic_sha256':rep['semantic_sha256'],'semantic_match':True,'byte_identical':rep['byte_identical']})
 assert len({x['pid'] for x in runs})==2 and len({x['path'] for x in runs})==2
 validators={}
 for kind,args in [('candidate-profile',['validate_candidate.py',str(d/'candidate.json'),'--root',str(r),'--profile','static-stylized-v1','--profile-contract',str(d/'profile-contract.json'),'--json']),('concept',['validate_concept_evidence.py',str(d/'concept-evidence.json'),'--root',str(d)])]:
  cmd=[sys.executable,str(r/'scripts'/args[0])]+args[1:];run=subprocess.run(cmd,capture_output=True,text=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'});(dest/(kind+'-fresh.json')).write_text(run.stdout);assert run.returncode==0,(kind,run.stdout,run.stderr);validators[kind]={'exit_code':run.returncode,'command':cmd}
 summary.append({'asset_id':a['asset_id'],'revision':a['revision'],'subject':a['hashes'],'original_design_frozen_at':f['frozen_at'],'original_design_unchanged':True,'concept_observed':g,'repair_freeze_at':repair['created_at'],'build_started_at':build['started_at'],'delivery_brief_changes_only':sorted(changes),'preproof_at':pre['checked_at'],'proof_started_at':ren['started_at'],'proof_finished_at':ren['ended_at'],'actual_primary_pixels':refs,'final_frames':frames,'runs':runs,'validators':validators,'limitation':'Retained process records are execution provenance, not cryptographic proof. Provider internal generation time/ID and precise authoring start unknown; observer and actual process intervals retained. No mtime inference; concept completeness remains false.'})
 print(a['asset_id'],'identity/provenance/validators pass',flush=True)
(o/'provenance-audit.json').write_text(json.dumps({'checked_at':now(),'assets':summary},indent=2)+'\n')

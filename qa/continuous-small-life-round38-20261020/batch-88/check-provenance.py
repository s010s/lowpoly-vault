import json,hashlib,subprocess,datetime
from pathlib import Path
from PIL import Image
R=Path('/workspace/shared/lowpoly-batch88-20261020');W=R/'production/batch88';Q=Path('/workspace/shared/lowpoly-batch88-independent-qa-20261020')
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads(p.read_text());checks={};seen=[]
def ck(name,condition,detail=None):checks[name]={'pass':bool(condition),'detail':detail}
ck('pinned_commit',subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip()=='b7c7f1c9ec495ad528568770a789b5d15a2de3a4')
ck('clean_source',not subprocess.check_output(['git','-C',str(R),'status','--porcelain'],text=True).strip())
ck('handoff_hash',H(W/'handoff-assets.json')=='2c3f73e4f0fa69e8387bd26ba0563b579bc27f9746821c1b4971bacc9d71551f')
index=J(W/'local-evidence-index.json');local=[]
for group in ['omitted_local_files','consulted_only_files']:
 for e in index[group]:
  p=Path(e['path']);ok=p.exists() and p.stat().st_size==e['bytes'] and H(p)==e['sha256'];local.append({'path':str(p),'pass':ok,'bytes':p.stat().st_size if p.exists() else None})
ck('retained_local_hashes',all(x['pass'] for x in local),{'files':len(local),'unique_bytes':sum({x['path']:x['bytes'] for x in local}.values()),'failures':[x for x in local if not x['pass']]})
inv=J(W/'batch-88-selected-inventory.json');raw=subprocess.check_output(['git','-C',str(R),'show',inv['source_inventory_commit']+':'+inv['source_inventory_path']]);ck('source_inventory_blob',hashlib.sha256(raw).hexdigest()==inv['source_inventory_sha256']);obj=json.loads(raw);orig=obj if isinstance(obj,list) else obj.get('assets',obj.get('items',[]));lookup={x.get('id'):x for x in orig};ck('selected_inventory_unchanged',all(lookup.get(x['id'])==x for x in inv['assets']))
for a in J(W/'handoff-assets.json'):
 d=R/a['path'];key=a['asset_id'];o=d.parent/'r001';freeze=J(o/'modeling-freeze.json');ck(key+'/original_freeze',all(H(o/n)==h for n,h in freeze['files'].items()))
 ck(key+'/original_scope_unchanged',H(d/'brief.json')==H(o/'brief.json') and H(d/'references.json')==H(o/'references.json'))
 ck(key+'/handoff_file_hashes',all(H(d/n)==a['hashes'][k] for k,n in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json'),('source','source.blend'),('generator','generator.py'),('config','build-config.json')]))
 dep=J(d/'build-dependencies.json');ck(key+'/dependency_closure',all(H(R/p)==h for p,h in dep['inputs'].items()) and H(R/'package-lock.json')==dep['node_lockfile_sha256'])
 c=J(d/'candidate-brief.json');ck(key+'/derived_closure',all(H(R/v['path'])==v['sha256'] for v in c['required_deliverables']) and c['packaging_adapter']['frozen_design_brief_sha256']==H(d/'brief.json'))
 bind=J(d/'preproof-binding.json');man=J(d/'proof-final/render-manifest.json');life=[json.loads(s) for s in (d/'lifecycle.jsonl').read_text().splitlines()];render=next(v for v in life if v['stage']=='proof-final');expected={k:a['hashes'][k] for k in ['glb','brief','references']}
 ck(key+'/exact_subject',all(man['subject'][k+'_sha256']==h==bind[k+'_sha256'] for k,h in expected.items()))
 ck(key+'/fixed_before_real_render',bind['checked_at']<render['started_at']<render['ended_at'] and render['exit_code']==0 and render['wall_seconds']>0,render)
 frames=[]
 for v in man['frames']:
  f=d/'proof-final'/v['path'];im=Image.open(f);frames.append({'view':v['view'],'sha256':H(f),'size':list(im.size),'pass':H(f)==v['sha256'] and list(im.size)==[512,512] and f.stat().st_size==v['bytes']})
 ck(key+'/eight_exact_frames',len(frames)==8 and len({f['view'] for f in frames})==8 and all(f['pass'] for f in frames),frames)
 ck(key+'/render_config_hash',H(d/'proof-final/render-config.json')==man['config_sha256'])
 q=[]
 for i in [1,2]:
  rep=J(d/('repro-final-'+str(i)+'.report.json'));rq=R/rep['build_run']['request']['path'];rs=R/rep['build_run']['result']['path'];req,res=J(rq),J(rs);outs=rs.parent/'outputs'
  ok=all(H(R/rep['build_run'][k]['path'])==rep['build_run'][k]['sha256'] for k in ['request','result']) and all(H(Path(v['path']))==v['sha256'] for v in req['identity']['inputs'].values()) and all(H(outs/n)==v['sha256'] and (outs/n).stat().st_size==v['bytes'] for n,v in res['outputs'].items()) and res['status']=='succeeded' and res['returncode']==0 and req['created_at']<=res['started_at']<res['finished_at'] and res['wall_seconds']>0 and H(outs/'model.glb')==a['hashes']['glb']
  log=rs.parent/'stdout.log';logs=list(rs.parent.glob('*.log'));q.append({'pass':ok,'pid':res['pid'],'started_at':res['started_at'],'finished_at':res['finished_at'],'wall_seconds':res['wall_seconds'],'request':str(rq),'request_sha256':H(rq),'result':str(rs),'result_sha256':H(rs),'output_sha256':H(outs/'model.glb'),'log_paths':[str(p) for p in logs],'log_nonempty':all(p.stat().st_size>0 for p in logs)})
 ck(key+'/two_real_queued_rebuild_records',all(v['pass'] for v in q) and q[0]['pid']!=q[1]['pid'] and q[0]['request']!=q[1]['request'],q)
 refs=J(d/'references.json');ck(key+'/reference_rights',refs['no_incorporated_third_party_assets'] and all(s.get('rights_note') and not s.get('incorporated') for s in refs['sources']))
 ce=J(d/'concept-evidence.json');ck(key+'/honest_unknown_concept_timestamps',ce['chronology']['concept_generated_at'] is None and ce['chronology']['modeling_started_at'] is None)
 origconcept=J(W/'concepts'/key/'invocation.json');ck(key+'/concept_receipt',origconcept['start']<origconcept['end']<freeze['frozen_at'] and bool(origconcept['result'].get('output_hint')))
(Q/'provenance-check.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'all_pass':all(x['pass'] for x in checks.values())},indent=2)+'\n')
print('CHECKS',len(checks),'FAILURES',{k:v for k,v in checks.items() if not v['pass']})

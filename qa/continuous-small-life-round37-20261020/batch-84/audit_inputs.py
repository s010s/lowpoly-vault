import json,hashlib,subprocess,sys,datetime
from pathlib import Path
from PIL import Image,ImageChops
sys.dont_write_bytecode=True
R=Path('/workspace/shared/lowpoly-batch84-20261020');W=R/'production/batch84';O=Path(__file__).parent;C=Path('/workspace/shared/lowpoly-batch84-consult-only');sys.path.insert(0,str(R/'scripts'))
from qa_glb import audit_glb
from check_reproducibility import compare_rebuild
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
J=lambda p:json.loads(Path(p).read_text())
cmd=lambda *x:subprocess.check_output(x,cwd=R)
expected='d7e1fed195c2c9fcb9690cdd52353b06b9edb261';assert cmd('git','rev-parse','HEAD').decode().strip()==expected
rows=J(W/'content-manifest.json')['files'];errs=[]
for x in rows:
 p=R/x['path']
 if not p.is_file() or H(p)!=x['sha256'] or p.stat().st_size!=x['bytes']:errs.append(x['path'])
 tracked=cmd('git','show',expected+':'+x['path'])
 if hashlib.sha256(tracked).hexdigest()!=x['sha256']:errs.append('git:'+x['path'])
inv=J(W/'selected-inventory.json');raw=cmd('git','show',inv['source_inventory_commit']+':'+inv['source_inventory_path']);assert hashlib.sha256(raw).hexdigest()==inv['source_inventory_sha256'];whole=json.loads(raw);inventory=whole['assets'] if isinstance(whole,dict) and 'assets' in whole else whole
if isinstance(inventory,dict): print('inventory keys',inventory.keys());raise ValueError('inspect inventory schema')
for x in inv['assets']:assert x==next(y for y in inventory if y['id']==x['id'])
assets=[]
for a in J(W/'handoff.json')['complete_maker_candidates']:
 p=R/a['path'];slug=a['asset_id'];original=p.parent/'r001';f=J(original/'modeling-freeze.json');assert all(H(original/n)==v for n,v in f['files'].items());assert H(p/'brief.json')==H(original/'brief.json');assert H(p/'references.json')==H(original/'references.json')
 hm={k:H(p/n) for k,n in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json'),('source','source.blend'),('generator','generator.py'),('config','build-config.json')]};assert hm==a['hashes']
 b=J(p/'candidate-brief.json');ob=J(p/'brief.json');assert b['packaging_adapter']['frozen_design_brief_sha256']==H(p/'brief.json');assert {k:v for k,v in b.items() if k not in ['packaging_adapter','required_deliverables']}=={k:v for k,v in ob.items() if k!='required_deliverables'}
 assert all(H(R/x['path'])==x['sha256'] for x in b['required_deliverables'])
 refs=J(p/'references.json');cr=[]
 for src in refs['sources']:
  assert src.get('rights_note');assert not src['incorporated']
  for x in src.get('consulted_images',[]):assert H(C/x['filename'])==x['sha256'];cr.append(x)
 proof=J(p/'proof-final3/render-manifest.json');assert proof['subject']['glb_sha256']==hm['glb'] and proof['subject']['brief_sha256']==hm['brief'] and proof['subject']['references_sha256']==hm['references'];assert H(p/'proof-final3/render-config.json')==proof['config_sha256'];sheet=Image.open(p/'contact-sheet.png').convert('RGB');frames=[]
 for n,x in enumerate(proof['frames']):
  pp=p/'proof-final3'/x['path'];im=Image.open(pp).convert('RGB');assert im.size==(512,512);assert H(pp)==x['sha256'];assert ImageChops.difference(im,sheet.crop(((n%4)*512,(n//4)*530,(n%4+1)*512,(n//4)*530+512))).getbbox() is None
  frames.append({'view':x['view'],'path':str(pp.relative_to(R)),'sha256':H(pp),'size':list(im.size)})
 assert len(frames)==8
 # Preserved old proofs remain separate; fresh corrected final3 manifest is never rebound to an old GLB.
 oldp=p/'proof-final';oldframes=J(oldp/'render-manifest.json')['frames'] if (oldp/'render-manifest.json').exists() else []
 pixel_changes={x['view']:H(oldp/x['path'])!=H(p/'proof-final3'/x['path']) for x in oldframes}
 deps=J(p/'build-dependencies.json');assert all(H(R/n)==v for n,v in deps['inputs'].items())
 runs=[]
 for rp in sorted((W/'rebuild-runs/build'/slug/a['revision']).rglob('result.json')):
  request=rp.parent/'request.json';res=J(rp);rq=J(request);assert res['status']=='succeeded' and res['returncode']==0
  assert all(H(Path(x['path']))==x['sha256'] for x in rq['identity']['inputs'].values());assert all(H(rp.parent/'outputs'/n)==x['sha256'] for n,x in res['outputs'].items())
  report=compare_rebuild(p/'model.glb',rp.parent/'outputs/model.glb',p/'generator.py',p/'build-config.json',request,rp,'model.glb',R);assert report['status']=='pass';(O/slug/('rebuild-'+res['job_id']+'.json')).write_text(json.dumps(report,indent=2)+'\n')
  runs.append({'request':str(request.relative_to(R)),'request_sha256':H(request),'result':str(rp.relative_to(R)),'result_sha256':H(rp),'pid':res['pid'],'started_at':res['started_at'],'finished_at':res['finished_at'],'fingerprint':res['fingerprint'],'run_id':rq['run_id'],'output_sha256':H(rp.parent/'outputs/model.glb'),'semantic_match':report['semantic_match']})
 assert len(runs)==2 and len({x['pid'] for x in runs})==2 and len({x['run_id'] for x in runs})==2 and len({x['fingerprint'] for x in runs})==2
 audit=audit_glb(p/'model.glb',14000,6,30);assert not audit['errors'];(O/slug/'project-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
 proc=subprocess.run([sys.executable,str(R/'scripts/validate_candidate.py'),str(p/'candidate.json'),'--root',str(R),'--profile','static-stylized-v1','--profile-contract',str(p/'profile-contract-v2.json'),'--json'],capture_output=True,text=True,cwd=R);(O/slug/'candidate-schema-fresh.json').write_text(proc.stdout);assert proc.returncode==0,proc.stdout+proc.stderr
 assets.append({'asset_id':slug,'revision':a['revision'],'hashes':hm,'original_freeze_sha256':H(original/'modeling-freeze.json'),'original_brief_sha256':H(original/'brief.json'),'consulted_media_verified':cr,'eight_frames':frames,'lossless_contact_sheet_match':True,'old_final_vs_final3_pixel_changed':pixel_changes,'queued_rebuilds':runs,'fresh_project_audit':'pass','schema_record_valid':True,'formal_approval':False})
report={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':expected,'git_status':cmd('git','status','--short').decode(),'manifest_sha256':H(W/'content-manifest.json'),'manifested_files_verified':len(rows),'errors':errs,'manifest_actual_and_commit_blobs_match':not errs,'original_inventory_sha256':inv['source_inventory_sha256'],'original_inventory_records_match':True,'assets':assets,'excluded':'solution-cave-passage r005 remains maker BLOCKED, no independent fourth candidate'}
(O/'immutable-input-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'manifest_files':len(rows),'errors':errs,'assets':[a['asset_id'] for a in assets]}))

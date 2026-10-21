import pathlib,json,hashlib,subprocess,datetime,os
from PIL import Image
R=pathlib.Path('/workspace/shared/lowpoly-batch77-ernietta-repair-20261020');P=R/'production/batch77-ernietta-repair';A=P/'assets/ernietta/r012';Q=pathlib.Path('/workspace/shared/lowpoly-ernietta-r012-independent-qa-20261020')
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();J=lambda p:json.loads(pathlib.Path(p).read_text());S=lambda *a:subprocess.check_output(a,cwd=R,text=True).strip()
expected={'handoff':'370ecc2aa196ae9a7f8be3e7a9d0d8d1ddf71731c3b81af3e1466cae8f093a07','glb':'72b30dfed8b7786a357e63102bd36ff26007cfb45af28923c6393b7314018e6b','source':'41851d81db91af4808dad70bd26bc21dedf88fe4378df69f038ca4c91d8225e3'}
assert S('git','rev-parse','HEAD')=='d1a3aa6a277908cd3aee66aa38e4d6dca818879b';assert S('git','status','--porcelain')=='';assert S('git','branch','--show-current')=='candidate/batch77-ernietta-repair-20261020';assert H(P/'handoff.json')==expected['handoff'];assert H(A/'model.glb')==expected['glb'];assert H(A/'source.blend')==expected['source']
snapshot={}
def check(p,h,size=None):
 p=pathlib.Path(p);assert H(p)==h,str(p);assert size is None or p.stat().st_size==size,str(p);snapshot[str(p)]=h
mf=J(P/'source-evidence-manifest.json');assert H(P/'source-evidence-manifest.json')==J(P/'handoff.json')['source_evidence_manifest_sha256']
blobchecks=[]
for e in mf['files']:
 p=R/e['path'];check(p,e['sha256'],e['bytes']);b=subprocess.check_output(['git','show','HEAD:'+e['path']],cwd=R);assert hashlib.sha256(b).hexdigest()==e['sha256'];blobchecks.append({'path':e['path'],'sha256':e['sha256'],'bytes':len(b),'matches_git':True})
assert len(blobchecks)==mf['file_count'];assert sum(e['bytes'] for e in blobchecks)==mf['total_bytes']
orig=J(P/'byte-identity-map.json')
for e in orig['files']:check(e['original'],e['sha256'],e['bytes']);check(P/e['copy'],e['sha256'],e['bytes'])
for e in orig['external_read_only']:check(e['path'],e['sha256'])
raw=J(P/'local-raw-manifest.json')
for e in raw['files']:check(e['path'],e['sha256'],e['bytes'])
assert sum(e['bytes'] for e in raw['files'])==raw['total_bytes']
freeze=J(P/'original-freeze/modeling-freeze.json')
for f,h in freeze['files'].items():check(P/'original-freeze'/f,h)
brief=J(A/'candidate-brief.json');old=J(P/'original-freeze/brief.json');diff=[k for k in set(brief)|set(old) if brief.get(k)!=old.get(k)];assert set(diff)=={'packaging_adapter','required_deliverables'}
for e in brief['required_deliverables']:check(R/e['path'],e['sha256'])
for f,h in J(A/'build-dependencies.json')['files'].items():check(R/f,h)
hand=J(P/'handoff.json');names={'glb':'model.glb','brief':'candidate-brief.json','references':'references.json','source':'source.blend','generator':'generator.py','config':'build-config.json'}
for k,f in names.items():check(A/f,hand['asset']['hashes'][k])
subject={'revision':'r012','glb_sha256':H(A/'model.glb'),'brief_sha256':H(A/'candidate-brief.json'),'references_sha256':H(A/'references.json')}
rend=J(A/'proof-final/render-manifest.json');assert rend['subject']==subject;assert rend['source_glb_sha256']==subject['glb_sha256'];check(A/'proof-final/render-config.json',rend['config_sha256'])
frames=[]
for f in rend['frames']:
 p=A/'proof-final'/f['path'];check(p,f['sha256'],f['bytes']);im=Image.open(p);assert im.size==(512,512);assert im.format=='PNG';frames.append({'view':f['id'],'sha256':H(p),'size':im.size,'angle':f['angle_degrees'],'metadata':{k:({'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()} if isinstance(v,bytes) else v) for k,v in im.info.items()}})
assert [f['view'] for f in frames]==brief['required_views'];assert H(A/'preview.png')==H(A/'proof-final/hero.png')
sheet=Image.open(A/'contact-sheet.png');assert sheet.format=='PNG'
prooflog=(A/'proof-final.log').read_text();assert all('/proof-final/'+f['view']+'.png' in prooflog for f in frames)
life=[json.loads(s) for s in (A/'lifecycle.jsonl').read_text().splitlines()];proof=next(e for e in life if e['stage']=='proof-final');pre=J(A/'preproof-binding.json');schema=J(A/'fresh-schema-check.json');D=datetime.datetime.fromisoformat
assert D(pre['created_at'])<D(proof['started_at']);assert D(schema['checked_at'])<D(proof['started_at']);assert D(rend['created_at'])>D(proof['started_at']);assert proof['returncode']==0
for k in ['glb_sha256','brief_sha256','references_sha256']:assert pre[k]==subject[k]
jobs=[];bind=J(A/'final-rebuild-binding.json')
for b in bind['jobs']:
 req=R/b['request'];res=R/b['result'];check(req,b['request_sha256']);check(res,b['result_sha256']);rq=J(req);rs=J(res);assert rs==b['result_record'];assert rs['status']=='succeeded' and rs['returncode']==0 and not rs['error'];assert D(rq['created_at'])<=D(rs['started_at'])<D(rs['finished_at'])<D(pre['created_at']);assert rq['fingerprint']==rs['fingerprint'];assert rq['identity']['threads']==2
 for key,e in rq['identity']['inputs'].items():check(e['path'],e['sha256'],e['bytes'])
 for f,e in rs['outputs'].items():check(res.parent/'outputs'/f,e['sha256'],e['bytes'])
 assert H(res.parent/'outputs/model.glb')==expected['glb'];stdout=(res.parent/'stdout.log').read_text();assert 'BUILT ernietta '+expected['glb']+' 5216 401724' in stdout;assert 'Blender quit' in stdout;assert not (res.parent/'stderr.log').read_text().strip()
 jobs.append({'pid':rs['pid'],'job_id':rs['job_id'],'fingerprint':rs['fingerprint'],'request_sha256':H(req),'result_sha256':H(res),'started_at':rs['started_at'],'finished_at':rs['finished_at'],'output_sha256':H(res.parent/'outputs/model.glb'),'stdout_sha256':H(res.parent/'stdout.log'),'distinct_output_path':str(res.parent/'outputs/model.glb')})
assert len(set(j['pid'] for j in jobs))==2;assert len(set(j['job_id'] for j in jobs))==2;assert len(set(j['fingerprint'] for j in jobs))==2
oldcfg=J(pathlib.Path(orig['external_read_only'][0]['path']).parent/'proof-final/render-config.json');newcfg=J(A/'proof-final/render-config.json');configdiff={k:{'old':oldcfg.get(k),'new':newcfg.get(k)} for k in set(oldcfg)|set(newcfg) if oldcfg.get(k)!=newcfg.get(k)}
for key in ['frames','renderer_sha256','helper_sha256','audit_helper_sha256','blender_version','engine','resolution','samples','denoising','view_transform','look','exposure','gamma','base_pose_deg','fixed_orbit_framing']:assert oldcfg[key]==newcfg[key],key
for p in [P/'handoff.json',P/'source-evidence-manifest.json',P/'local-raw-manifest.json',P/'byte-identity-map.json']:snapshot[str(p)]=H(p)
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':S('git','rev-parse','HEAD'),'parents':S('git','log','-3','--format=%H %P').splitlines(),'status':'pass','subject':subject,'source_sha256':expected['source'],'handoff_sha256':expected['handoff'],'committed_manifest_files':len(blobchecks),'committed_manifest_bytes':sum(e['bytes'] for e in blobchecks),'git_blob_checks':blobchecks,'original_identity_copies_verified':len(orig['files']),'original_source_model_generator_verified':len(orig['external_read_only']),'original_freeze_entries_verified':len(freeze['files']),'retained_failed_raw_files':len(raw['files']),'retained_failed_raw_bytes':raw['total_bytes'],'derived_brief_changed_keys_only':diff,'required_frame_checks':frames,'contact_sheet_size':sheet.size,'contact_sheet_sha256':H(A/'contact-sheet.png'),'preproof_binding_at':pre['created_at'],'schema_before_render_at':schema['checked_at'],'final_render_start':proof['started_at'],'final_render_end':proof['finished_at'],'rebuild_jobs':jobs,'render_config_differences':configdiff,'limitations':'Rebuild execution is corroborated by raw request/result/stdout/output provenance, not cryptographic proof of the historical process. No filesystem mtimes used for chronology.'}
(Q/'integrity-check.json').write_text(json.dumps(report,indent=2)+'\n');(Q/'input-hashes-before.json').write_text(json.dumps(snapshot,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['git_blob_checks','required_frame_checks','render_config_differences']},indent=2))

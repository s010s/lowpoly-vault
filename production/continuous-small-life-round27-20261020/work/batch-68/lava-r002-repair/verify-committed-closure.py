# SPDX-License-Identifier: MIT
"""Read-only active artifact/manifest closure and protected history check against Git bytes."""
from pathlib import Path
import json,hashlib,subprocess,sys
R=Path.cwd();W=Path(__file__).resolve().parent;b=R/'assets/candidates/continuous-small-life-round27-20261020/batch-68/lava-dome/r002';ref=sys.argv[1] if len(sys.argv)>1 else 'HEAD';seen={}
H=lambda raw:hashlib.sha256(raw).hexdigest()
def gitdata(p):
 rel=str(p.resolve().relative_to(R));spec=(':'+rel) if ref=='INDEX' else ref+':'+rel
 raw=subprocess.check_output(['git','show',spec]);assert raw==p.read_bytes(),('Git/worktree differ',rel);return raw

def pin(p,sha,why):
 assert p.is_file(),('missing',p,why);raw=gitdata(p);assert H(raw)==sha,('hash mismatch',p,why);seen[str(p.relative_to(R))]={'sha256':sha,'git_verified':True,'reason':why}
# Protected trees include ignored original logs; committed source continuity additionally checked.
base=json.loads((W/'unchanged-baseline.json').read_text());protected=0
for e in base['files']:
 p=R/e['path'];assert p.is_file() and H(p.read_bytes())==e['sha256'],('protected modified',e['path'])
 if e['git_blob'] is not None:
  raw=gitdata(p);assert H(raw)==e['sha256'];blob=subprocess.check_output(['git','hash-object','--stdin'],input=raw).decode().strip();assert blob==e['git_blob']
 protected+=1
c=json.loads((b/'candidate.json').read_text());assert c['asset_id']=='lava-dome' and c['revision']=='r002'
for group in ['artifacts','raw_checks']:
 for name,e in c[group].items():pin(R/e['path'],e['sha256'],group+':'+name)
for e in c['evidence']:pin(R/e['path'],e['sha256'],'candidate evidence')
pin(R/c['supersedes']['path'],c['supersedes']['sha256'],'immutable r001 superseded candidate')
for n in ['profile-contract.json','candidate-validation.json','pixel-inspection.json','metadata.json','concept-evidence.json','concept-validation.json']:gitdata(b/n)
contract=json.loads((b/'profile-contract.json').read_text());pin(R/contract['candidate']['path'],contract['candidate']['sha256'],'profile candidate');pin(R/contract['publication_policy']['path'],contract['publication_policy']['sha256'],'unchanged policy')
brief=json.loads((R/c['artifacts']['brief']['path']).read_text())
for e in brief['required_deliverables']:pin(R/e['path'],e['sha256'],'delivery brief')
freeze=json.loads((b/'modeling-freeze.json').read_text())
for n,h in freeze['files'].items():pin(b/n,h,'immutable repair freeze')
deps=json.loads((b/'build-dependencies.json').read_text());pin(R/c['artifacts']['generator']['path'],deps['generator_sha256'],'generator dependency');pin(R/c['artifacts']['config']['path'],deps['config_sha256'],'config dependency')
for n,h in deps['files'].items():pin(R/n,h,'unchanged dependency')
manifest=json.loads((b/'proof-final/render-manifest.json').read_text());assert len(manifest['frames'])==8
for frame in manifest['frames']:assert frame['width']==512 and frame['height']==512;pin(b/'proof-final'/frame['path'],frame['sha256'],'exact final512px frame')
pin(b/'proof-final/render-config.json',manifest['config_sha256'],'unchanged renderer config file')
bind=json.loads((b/'preproof-binding-check.json').read_text());assert bind['checked_at']<manifest['created_at'];assert bind['glb_sha256']==c['artifacts']['glb']['sha256'];assert bind['brief_sha256']==c['artifacts']['brief']['sha256'];assert bind['references_sha256']==c['artifacts']['references']['sha256']
# Two distinct actual final queue executions, not pre-contact-skirt receipts.
receipts=[]
for i in [1,2]:
 report=json.loads((b/f'repro-final-{i}.report.json').read_text());assert report['status']=='pass'
 result_path=R/report['build_run']['result']['path'];request_path=R/report['build_run']['request']['path'];pin(result_path,report['build_run']['result']['sha256'],'bound queue result');pin(request_path,report['build_run']['request']['sha256'],'bound queue request')
 result=json.loads(result_path.read_text());request=json.loads(request_path.read_text());assert result['status']=='succeeded' and result['returncode']==0
 for n,e in result['outputs'].items():pin(result_path.parent/'outputs'/n,e['sha256'],'final rebuild output')
 for name,e in request['identity']['inputs'].items():pin(Path(e['path']),e['sha256'],'final rebuild input:'+name)
 exe=request['identity']['executable'];pin(Path(exe['path']),exe['sha256'],'per-job blocking flock wrapper')
 assert result['outputs']['model.glb']['sha256']==c['artifacts']['glb']['sha256'];receipts.append({'job_id':result['job_id'],'pid':result['pid'],'started_at':result['started_at'],'finished_at':result['finished_at'],'request_sha256':H(request_path.read_bytes()),'result_sha256':H(result_path.read_bytes()),'result_path':str(result_path.relative_to(R))})
assert receipts[0]['pid']!=receipts[1]['pid'];assert receipts[0]['request_sha256']!=receipts[1]['request_sha256'];assert receipts[0]['result_sha256']!=receipts[1]['result_sha256']
# Every new tracked byte, including raw logs and retained attempt snapshots, is present in Git.
newroots=[str(b.relative_to(R)),str(W.relative_to(R)),'production/continuous-small-life-round27-20261020/work/batch-68/prepare-lava-r002.py']
files=subprocess.check_output(['git','ls-files',*newroots],text=True).splitlines();logs=0
for n in files:gitdata(R/n);logs+=n.endswith('.log')
assert logs>=12,('required raw logs not tracked',logs)
print(json.dumps({'status':'pass','git_ref':ref,'active_pin_count':len(seen),'protected_full_tree_files':protected,'new_tracked_files_verified':len(files),'tracked_raw_logs':logs,'active_artifacts':c['artifacts'],'rebuild_receipts':receipts,'note':'All active candidate artifacts/raw/evidence, final frames, delivery/freeze/dependency and final queue input/output entries checked against Git bytes. Historical superseded snapshots retained, never reinterpreted as active pins. Original ignored logs protected by full-tree SHA256; original tracked Git blobs identical.'},indent=2))

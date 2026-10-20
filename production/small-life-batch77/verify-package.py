# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime
R=Path.cwd();W=R/'production/small-life-batch77';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();results=[]
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path'];f=json.loads((b/'modeling-freeze.json').read_text());assert all(H(b/n)==v for n,v in f['files'].items());c=json.loads((b/'candidate.json').read_text());cv=json.loads((b/'candidate-validation.json').read_text());assert cv['valid'] and not cv['approved_for_brief'];assert all(H(R/v['path'])==v['sha256'] for v in c['artifacts'].values());p=json.loads((b/'proof-final/render-manifest.json').read_text());assert len(p['frames'])==8
 for frame in p['frames']:assert H(b/'proof-final'/frame['path'])==frame['sha256']
 for i in [1,2]:
  d=json.loads((b/f'repro-final-{i}.report.json').read_text());assert d['status']=='pass'
 k=json.loads((b/'gltf-validator.report.json').read_text());assert k['issues']['numErrors']==0 and k['issues']['numWarnings']==0
 results.append({'asset_id':x['asset_id'],'original_freeze_unchanged':True,'candidate_integrity_valid':True,'approved':False,'final_fixed8_hashes_valid':True,'glb_sha256':H(b/'model.glb')})
(W/'verification-final.json').write_text(json.dumps({'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results,'note':'Integrity and automated evidence only. No independent acceptance or unrun GPU/scene inferred.'},indent=2)+'\n');print('VERIFIED',len(results))

"""Append a new independently sealed record; original approval remains immutable."""
from pathlib import Path
import json,hashlib,shutil,sys
from datetime import datetime,timezone
sys.path.insert(0,str(Path('scripts').resolve()))
from validate_candidate import approval_snapshot_sha256
root=Path('experiments/structural-refinement-2026-10-17/accepted/conifer-tree')
prior=root/'qa/r20-doc1-final-independent/candidate.independent.json'
out=root/'qa/doc1-publication-preview-independent';out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,r:p.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
r=json.loads(prior.read_text());request=json.loads(Path('qa/conifer-doc1-integration/preview-review-request.json').read_text());audit=json.loads(Path('qa/conifer-doc1-preview-independent/artifact-audit.json').read_text());assert audit['status']=='pass'
subject=r['approval']['subject'];reviewer={'id':'independent-conifer-publication-preview-sol61','task_id':'conifer-doc1-publication-preview-independent-20261017'};now=datetime.now(timezone.utc).isoformat()
shutil.copyfile('qa/conifer-doc1-preview-independent/artifact-audit.json',out/'artifact-audit.json')
shutil.copyfile(request['preview_manifest'],out/'selected-turntable.json')
shutil.copyfile('qa/conifer-doc1-integration/preview-review-request.json',out/'preview-review-request.json')
new=[]
for i,f in enumerate(request['frames']+ [{'path':request['poster'],'sha256':request['poster_sha256']}]):
 name=f'frame-{i:03}.webp' if i<24 else 'poster.webp';p=out/name;shutil.copyfile(f['path'],p);assert sha(p)==f['sha256']
 new.append({'id':f'publication-frame-{i:03}' if i<24 else 'publication-poster','kind':'rendered_image','stage':'visual','path':p.relative_to(root).as_posix(),'sha256':sha(p),'subject':subject})
r['evidence'] += new
oldreport=next(e for e in r['evidence'] if e['id']=='independent-visual');inherited=json.loads((root/oldreport['path']).read_text())
report={'schema_version':1,'kind':'visual_report','stage':'visual','subject':subject,'status':'pass','reviewer':reviewer,'reviewed_at':now,'method':'Independent publication-only review of all24 exact selected WebPs at full decoded768px on alternating light/dark backgrounds, frame0 on both, separate poster, existing actual desktop/mobile GLB pixel captures and five handoff metrics. No browser operation. Existing complete model visual verdict is inherited with original reviewer attribution; no model-stage re-review is claimed.','observations':[audit['visual_observation'],audit['camera'],'Poster/release preview/frame0 have identical SHA256 '+request['poster_sha256']+'. Full360-degree order42+15*i at23.3 elevation; alpha borders empty and all tip/root bounds inside frame.','Selected preview source bytes equal b3107dc; site/scripts code unchanged from recorded handoff browser commit through reviewed35de59d2. Five parity cases have1–2px bbox and<0.2px centroid deviation at normalized320px.','Inherited independent model visual findings: '+ '; '.join(inherited['observations'])],'errors':[],'warnings':[],'warning_review':[],'reviewed_evidence':sorted([{'id':e['id'],'sha256':e['sha256']} for e in r['evidence'] if e['stage']=='visual' and e['kind']!='visual_report'],key=lambda e:e['id']),'inherited_model_review':{'candidate':{'path':prior.relative_to(root).as_posix(),'sha256':sha(prior)},'report':{'path':oldreport['path'],'sha256':oldreport['sha256']},'reviewer':inherited['reviewer'],'scope':'Retains prior53-image model craft/reference review and criterion decisions, exact unchanged model/brief/reference identity. Current reviewer inspected selected publication sequence and integration evidence only.'},'publication_preview':{'request':{'path':(out/'preview-review-request.json').relative_to(root).as_posix(),'sha256':sha(out/'preview-review-request.json')},'manifest':{'path':(out/'selected-turntable.json').relative_to(root).as_posix(),'sha256':sha(out/'selected-turntable.json')},'audit':{'path':(out/'artifact-audit.json').relative_to(root).as_posix(),'sha256':sha(out/'artifact-audit.json')},'inspected_frames':[f'publication-frame-{i:03}' for i in range(24)],'poster':'publication-poster'},'limits':[x for x in inherited['limits'] if not x.startswith('Publication authorization')]+['Publication preview approval is limited to the exact selected hashes; main activation/publication remains separate. No new GPU execution or performance acceptance by this reviewer.']}
write(out/'visual.report.json',report)
oldreport.update(path=(out/'visual.report.json').relative_to(root).as_posix(),sha256=sha(out/'visual.report.json'))
r['stages']['visual']['evidence'] += [e['id'] for e in new]
r['stages']['visual'].update(reviewer=reviewer,reviewed_at=now,note='Publication supplement: independent inspection of selected24alpha/poster and saved actual GLB handoff pixels; prior model visual criteria/reference inspection inherited from original independently approved record, with full attribution in report.')
r['approval'].update(reviewer=reviewer,reviewed_at=now,note='Preserves exact seven-stage model acceptance from immutable prior independent record; adds independent approval of all24 selected publication images and poster under same subject. Requires KHR_mesh_quantization; performance acceptance remains only recorded M5 Pro/Metal, SwiftShader failures retained. No main publication performed.')
r['acceptance_scope']['limitations']=[x for x in r['acceptance_scope']['limitations'] if not x.startswith('Publication authorization')]
r['acceptance_scope']['limitations']+=['Exact selected24alpha/poster publication preview approved by independent supplement; website activation/publication remains separate.']
r['publication_preview_approval']={'status':'pass','reviewer':reviewer,'reviewed_at':now,'poster_sha256':request['poster_sha256'],'manifest_sha256':request['preview_manifest_sha256'],'frames':request['frames'],'prior_candidate_sha256':sha(prior),'reviewed_commit':audit['reviewed_commit']}
r['approval']['review_snapshot_sha256']=approval_snapshot_sha256(r)
write(out/'candidate.reviewed.json',r)
# New proposal descriptor only: active manifest, active index, prior proposal stay unchanged.
p=Path('assets/releases/conifer-doc1-preview-reviewed-20261017.json');d=json.loads(Path('assets/releases/conifer-doc1-20261017.json').read_text());d['release_id']='conifer-doc1-preview-reviewed-20261017';entry=next(e for e in d['revisions'] if e['id']=='conifer-tree');entry['candidate']={'path':(out/'candidate.reviewed.json').relative_to(root).as_posix(),'sha256':sha(out/'candidate.reviewed.json')};write(p,d)
write(Path('qa/conifer-doc1-preview-independent/reviewed-release-pin.json'),{'path':str(p),'sha256':sha(p)})
print('New candidate',sha(out/'candidate.reviewed.json'));print('New proposal descriptor',sha(p))

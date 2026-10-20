# SPDX-License-Identifier: MIT
"""Read-only bounded evidence check; no candidate approval or guessed identity."""
from pathlib import Path
import json,sys,hashlib,subprocess
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'scripts'));from validate_candidate import check_brief,check_render_manifest,STATIC_PROFILE
O=R/'assets/candidates/continuous-small-life-round18-20261020/batch-53';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for s in ['hypoturrilites','iodes-brownii','welded-ignimbrite-outcrop','halopoa-furrowed-burrow']:
 o=O/s/'r001';c=json.loads((o/'candidate.json').read_text());brief=json.loads((o/'delivery-brief.json').read_text());refs=json.loads((o/'references-profile.json').read_text());fz=json.loads((o/'modeling-freeze.json').read_text());assert all(sha(o/f)==h for f,h in fz['files'].items());assert refs['no_incorporated_third_party_assets'];assert all(x['rights_note'] and not x['incorporated'] for x in refs['sources'])
 check_brief(brief,c,{x['id'] for x in refs['sources']},STATIC_PROFILE);ev=c['evidence'][0];coverage=check_render_manifest(json.loads((R/ev['path']).read_text()),ev,ev['subject'],brief,R,STATIC_PROFILE);assert not coverage['problems'],coverage
 for d in brief['required_deliverables']:assert c['artifacts'][d['role']]=={k:d[k] for k in ['path','sha256']}
 ce=json.loads((o/'concept-checker.report.json').read_text());assert ce['valid'] and ce['blockers']==['concept_generated_at: unknown; do not reconstruct times from file mtimes']
 assert json.loads((o/'delivery-binding.json').read_text())['decoded_RGBA_pixels_identical_to_inspected_prior_views']
 md=json.loads((o/'metadata.json').read_text());assert all((R/md[k]).is_file() for k in ['glb','blend','preview']);assert sha(R/md['glb'])==c['artifacts']['glb']['sha256']
 assert json.loads((o/'profile-checker.report.json').read_text())['errors']==['maker.task_id: nonempty text required']
 m=json.loads((o/'metrics.json').read_text());assert m['khronos_errors']==m['khronos_warnings']==m['textures']==0;assert m['triangles']<=14000 and m['glb_bytes']<=1000000 and m['materials']<=6 and m['primitives']<=30
 for name in ['rebuild-1.report.json','rebuild-2.report.json']:
  q=json.loads((o/name).read_text());assert q['semantic_match'] and q['status']=='pass' and q['provenance_status']=='bound_successful_build_run'
 assert c['maker']['task_id'] is None;assert all(stage['status']=='unknown' for stage in c['stages'].values());assert c['approval']['status']=='pending'
 print(s,'bounded evidence PASS; full candidate task identity remains blocked; no approval')
# Retained planning input bytes are identical to the reserved commit; no broad merge.
P=R/'production/continuous-small-life-round18-20261020'
for rel in ['batch-53-TASK.md','batch-53-QA-SCOPE.json','concept-plan-requirements.json','profile-policy.json','reference-policy.json','review-policy.json','source-freeze.json','preclaim-dedup.json','work/batch-53/claim.json']+[f'items/{s}/{f}.json' for s in ['hypoturrilites','iodes-brownii','welded-ignimbrite-outcrop','halopoa-furrowed-burrow'] for f in ['dispatch-boundary','inventory-record']]:
 p=P/rel;assert p.read_bytes()==subprocess.check_output(['git','show','37fd2c0ebc795b9d89289f20544587e0266be4c8:'+str(p.relative_to(R))],cwd=R)
print('All 17 imported planning inputs unchanged; previous inventories and freezes untouched')

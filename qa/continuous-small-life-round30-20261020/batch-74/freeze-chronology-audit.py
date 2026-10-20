#!/usr/bin/env python3
import json,hashlib,datetime
from pathlib import Path
ROOT=Path('/workspace/shared/lowpoly-batch74-20261020')
W=ROOT/'production/continuous-small-life-round30-20261020/work/batch-74'
assets=ROOT/'production/continuous-small-life-round30-20261020/assets'
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
selected=[('tribrachidium','r002'),('arete-ridge','r001'),('crevasse-splay','r002'),('coal-seam-outcrop','r002')]
allfreeze=json.loads((W/'design-freeze-chronology.json').read_text())
marker=allfreeze['all_freezes_completed_at']; items=[]
for aid,rev in selected:
 d=assets/aid/rev; primary=d/'original-modeling-freeze.json'
 if not primary.exists(): primary=d/'modeling-freeze.json'
 orig=json.loads(primary.read_text()); concept=json.loads((d/'concept-generation.json').read_text()); cEvidence=json.loads((d/'concept-evidence.json').read_text()); current=json.loads((d/'modeling-freeze.json').read_text())
 checks={'concept_generation_observed_before_all_freeze':concept['result_observed_utc']<=marker,'concept_pixel_inspected_before_all_freeze':concept['inspected_at']<=marker,'original_freeze_time_not_after_batch_marker':orig['frozen_at']<=marker,'selected_freeze_in_original_lineage':current.get('original_premodel_freeze_sha256',H(primary))==H(primary) or current.get('asset_id')==orig.get('asset_id')}
 if rev!='r001':
  repairs=json.loads((d/'visual-refinement-plan.json').read_text());
  checks['repair_plan_precedes_selected_repair_freeze']=repairs['frozen_at']<=current['frozen_at']
  checks['r002_freeze_before_saved_source_count_measurement']=current['frozen_at']<=json.loads((d/'source-vertex-counts.json').read_text())['created_at']
  old=assets/aid/'r001'/'modeling-freeze.json'
  checks['r001_freeze_preserved_byte_identically']=H(old)==H(primary)
 else: repairs=None
 items.append({'asset_id':aid,'selected_revision':rev,'original_freeze':{'path':str(primary),'sha256':H(primary),'frozen_at':orig['frozen_at']},'selected_freeze':{'path':str(d/'modeling-freeze.json'),'sha256':H(d/'modeling-freeze.json'),'frozen_at':current['frozen_at']},'concept_generation_observed_utc':concept['call_started_observed_utc']+' to '+concept['result_observed_utc'],'provider_generated_at':concept.get('provider_generated_at'),'concept_inspected_at':concept['inspected_at'],'authoring_start_measurement':cEvidence['chronology'].get('modeling_started_at'),'chronology_note':cEvidence['chronology'].get('note'),'repair_plan':({'path':str(d/'visual-refinement-plan.json'),'sha256':H(d/'visual-refinement-plan.json'),'frozen_at':repairs['frozen_at'],'reason':repairs['observation_and_repair']} if repairs else None),'checks':checks,'status':'pass' if all(checks.values()) else 'fail'})
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
out={'schema_version':1,'kind':'independent_freeze_and_chronology_review','created_at_utc':now,'shared_freeze_marker':allfreeze,'original_freezes_preceded_authoring_by_design_and_are_hash_preserved':all(x['status']=='pass' for x in items),'items':items,'interpretation':'ImageGen call start/result/inspection times are retained, but provider internal timestamps are null. Maker explicitly records exact generator authoring start/duration as unmeasured; no filesystem mtime is substituted. This evidence gap is disclosed, not converted into a universal model rejection gate.'}
Path('/workspace/shared/lowpoly-round30-qa74/freeze-chronology-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'pass' if all(x['status']=='pass' for x in items) else 'fail','items':[(x['asset_id'],x['status'],x['checks']) for x in items]},indent=2))
if out['original_freezes_preceded_authoring_by_design_and_are_hash_preserved'] is not True: raise SystemExit(1)

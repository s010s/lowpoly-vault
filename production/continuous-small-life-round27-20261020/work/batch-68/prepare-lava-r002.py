from pathlib import Path
import json,hashlib,datetime,shutil,subprocess
R=Path.cwd();W=R/'production/continuous-small-life-round27-20261020/work/batch-68/lava-r002-repair';W.mkdir(exist_ok=True);A=R/'assets/candidates/continuous-small-life-round27-20261020/batch-68';old=A/'lava-dome/r001';b=A/'lava-dome/r002';b.mkdir(exist_ok=True);H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();paths=[];tracked=set(subprocess.check_output(['git','ls-files'],text=True).splitlines())
for slug in ['thaumaptilon','sandstone-fin','ice-wedge-polygon-ground','lava-dome']:
 root=A/slug/('r001' if slug=='lava-dome' else '')
 for p in sorted(root.rglob('*')):
  if p.is_file():
   rel=str(p.relative_to(R));blob=None
   if rel in tracked:
    blob=subprocess.check_output(['git','rev-parse',base+':'+rel],text=True).strip();assert hashlib.sha256(subprocess.check_output(['git','show',base+':'+rel])).hexdigest()==H(p)
   paths.append({'path':rel,'sha256':H(p),'git_blob':blob,'original_untracked_ignored_file':rel not in tracked})
put(W/'unchanged-baseline.json',{'commit':base,'files':paths,'note':'Complete protected three accepted asset trees and original lava-dome r001, checked against Git bytes before repair.'})
for n in ['references.json','concept-original.png','concept-prompt.txt','concept-generation.json','LICENSES.md']:shutil.copyfile(old/n,b/n)
repair='Replace circumferential block placement with one welded coarse fractured surface across entire dome footprint, including summit and flanks. Unequal irregular planar rock plate regions join at shallow discontinuous fracture grooves; variable local inclination and relief tied to overall dome curvature, no separate repeated cylinders, no ring, no bare summit disc. Preserve bulbous steep-sided broad craterless dome proportions, original palette/materials/renderer/budgets, static generic nominal scale and subordinate contact skirt. Not a cinder cone or loose rock pile.'
d=json.loads((old/'brief.json').read_text());d.update(brief_version='r002',created_at=now(),repair_scope=repair,concept_decisions=d['concept_decisions']+' Explicit r002 geometry repair: '+repair);put(b/'brief.json',d)
(b/'brief.md').write_text((old/'brief.md').read_text()+'\n## Explicit r002 repair\n\n'+repair+'\nOriginal r001 brief and QA retained unchanged; targeted independent review pending.\n')
c=json.loads((old/'build-config.json').read_text());c['revision']='r002';c['modeling_decisions']+=' Explicit r002 repair: '+repair;put(b/'build-config.json',c)
refs=json.loads((b/'references.json').read_text());assert refs['no_incorporated_third_party_assets'] is True and all(e['rights_note'] and e['incorporated'] is False for e in refs['sources']);put(b/'prefreeze-ledger-check.json',{'checked_at':now(),'status':'pass','references_sha256':H(b/'references.json'),'all_entries_have_rights_note':True,'no_incorporated_third_party_assets':True})
qa=Path('/workspace/shared/lowpoly-round27-qa68/QA.md');assert H(qa)=='825a9bfc1fa14145a3b198be5db1c4538cedb12e1516bc28e4e6971217033e18'
put(b/'modeling-freeze.json',{'asset_id':'lava-dome','revision':'r002','frozen_at':now(),'kind':'explicit-immutable-geometry-repair-freeze-before-geometry','original_source_commit':'5dee4300e53732cd137d87f9dfa1d761bf5b66b0','qa_commit':base,'original_brief_sha256':H(old/'brief.json'),'original_glb_sha256':H(old/'model.glb'),'original_qa_sha256':H(qa),'source_pixels_reinspected':[{'filename':n,'sha256':H(Path('/workspace/shared/batch68-consulted-only')/n)} for n in ['dome.jpg','dome-rubble.jpg']],'repair_scope':repair,'material_camera_renderer_validator_changes':False,'files':{n:H(b/n) for n in ['brief.json','brief.md','build-config.json','references.json','concept-original.png','concept-prompt.txt','concept-generation.json']},'approval':'pending-targeted-independent-differential'})
put(W/'final-selection.json',[{'asset_id':'lava-dome','revision':'r002','path':str(b.relative_to(R))}]);put(W/'chronology-start.json',{'repair_freeze_completed_at':now(),'next_action':'Author geometry only after this record','provider_internal_timestamp':None})
print('Frozen r002',now())

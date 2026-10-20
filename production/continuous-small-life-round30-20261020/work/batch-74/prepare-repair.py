import pathlib,json,shutil,hashlib,datetime
R=pathlib.Path.cwd();W=R/'production/continuous-small-life-round30-20261020/work/batch-74';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plans={'tribrachidium':'r001 exact8 inspected: three primary curves read, but apical pits/bullae too faint at supporting size. Adjust integrated surface to clearer three shallow EMPTY pits and modest ridge/bulla relief, maintain ~2mm relief and no living appendages; reduce blank outer annulus by extending primary curves toward margin. No material/camera changes.', 'crevasse-splay':'r001 exact8 inspected: connected trunk/breach/fan visible, but distal channels narrower than mesh sampling create isolated puddles. Increase diagnostic terminal channel widths enough to resolve continuous geometry, weld coincident internal water vertices and verify branch connectivity. Preserve one generic fan with low relief and no site replication. No camera/depth bias.', 'coal-seam-outcrop':'r001 exact8 inspected: coal blocks leave see-through gaps at host contacts and are too regular pillar-like. Extend actual coal into host beds, add solid inset core behind cleats so no through-sky slots, and create chipped uneven column fronts with irregular shorter terminating butt cleats. Increase actual host surface faceting, no paint-only fixes or camera/depth changes.'}
sel=json.loads((W/'final-selection.json').read_text())
for x in sel:
 slug=x['asset_id']
 if slug not in plans:continue
 old=R/x['path'];b=old.parent/'r002';b.mkdir()
 for n in ['brief.json','brief.md','references.json','concept-original.png','concept-prompt.txt','concept-generation.json','prefreeze-ledger-check.json','chronology-clarification.json']:
  shutil.copy(old/n,b/n)
 shutil.copy(old/'modeling-freeze.json',b/'original-modeling-freeze.json')
 cfg=json.loads((old/'build-config.json').read_text());cfg['revision']='r002';cfg['repair_decisions']=plans[slug];(b/'build-config.json').write_text(json.dumps(cfg,indent=2)+'\n')
 (b/'visual-refinement-plan.json').write_text(json.dumps({'frozen_at':now(),'original_revision':'r001','original_glb_sha256':H(old/'model.glb'),'original_render_manifest_sha256':H(old/'proof-final/render-manifest.json'),'observation_and_repair':plans[slug],'scope_unchanged':True,'prohibited':'No camera/material/depth-bias concealment. Repair actual geometry, retain failures.'},indent=2)+'\n')
 fs=['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','visual-refinement-plan.json','original-modeling-freeze.json']
 (b/'modeling-freeze.json').write_text(json.dumps({'asset_id':slug,'revision':'r002','frozen_at':now(),'status':'Geometry repair freeze after original unchanged scope and original r001 evidence; new generator authorship follows this marker','original_premodel_freeze_sha256':H(old/'modeling-freeze.json'),'files':{n:H(b/n) for n in fs}},indent=2)+'\n')
 x['revision']='r002';x['path']=str(b.relative_to(R))
(W/'r001-selection.json').write_text((W/'final-selection.json').read_text());(W/'final-selection.json').write_text(json.dumps(sel,indent=2)+'\n');print('repair frozen',now())

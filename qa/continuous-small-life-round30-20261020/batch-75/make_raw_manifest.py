import json, hashlib, pathlib, os, datetime, subprocess
O=pathlib.Path('/workspace/shared/lowpoly-round30-qa75')
W=pathlib.Path('/workspace/shared/lowpoly-batch75-20261020'); P=W/'production/continuous-small-life-round30-20261020/work/batch-75'
def rec(p, role=None):
 p=pathlib.Path(p); r={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if role:r['role']=role
 return r
# Source inputs that define the batch, frozen scope, final identity, and exact final images.
source=[]
for p,role in [
 (P/'handoff.json','maker handoff'),(P/'source-evidence-manifest.json','747-entry immutable source manifest'),(P/'tracked-manifest-check.json','tracked source-manifest verification'),(P/'design-freeze-chronology.json','freeze chronology'),(P/'source-inventory-closure.json','original inventory closure'),(P/'concept-plan-requirements.json','batch requirements'),(P/'PRODUCTION-ADDENDUM.md','production protocol'),(P/'REFERENCE-PREFLIGHT-DRAFT.md','reference preflight'),(P/'final-selection.json','exact final revisions'),(P/'verification-final.json','maker final integrity verification')]: source.append(rec(p,role))
assets=json.load(open(P/'handoff.json'))['assets']
for a in assets:
 d=W/a['path']; id=a['asset_id']; rev=a['revision']
 for name,role in [('model.glb','exact final GLB'),('source.blend','editable source'),('generator.py','deterministic generator'),('build-config.json','active config'),('build-dependencies.json','dependency closure'),('brief.json','immutable pregeometry brief'),('candidate-brief.json','active candidate brief'),('references.json','reference rights/source ledger'),('modeling-freeze.json','immutable freeze record'),('preproof-binding.json','pre-render binding record'),('source-metrics.json','saved source authored/evaluated counts'),('metrics.json','producer technical metrics'),('physical-surfaces.report.json','producer physical overlap check'),('concept-original.png','original concept pixels'),('concept-prompt.txt','concept prompt'),('concept-generation.json','concept receipt/observed timestamps'),('proof-final/render-config.json','proof camera/render settings'),('proof-final/render-manifest.json','hash-bound final render manifest')]:
  if (d/name).is_file(): source.append(rec(d/name,f'{id} {rev}: {role}'))
 for view in ['hero','reversehero','front','side','rear','top','clay','silhouette']:
  source.append(rec(d/'proof-final'/f'{view}.png',f'{id} {rev}: exact final {view} 512px frame'))
 source.append(rec(d/'contact-sheet.png',f'{id} {rev}: lossless final contact sheet'))
# Actual consulted pixels, deliberately outside Git.
consult=[]
for name in ['parvancorina-fig4.jpg','horn.jpg','fissure17.jpg','gneiss.jpg','gneiss-folded.jpg','gneiss-usgs.jpg']:
 p=pathlib.Path('/workspace/shared/batch75-consult-only')/name; consult.append(rec(p,'consult-only actual reference pixels; outside Git worktree'))
# Exact separate, successful, executed semantic rebuild raw records and outputs.
rebuild_files=[]; re=json.load(open(O/'rebuild-evidence.json'))
for asset in re['assets']:
 for run in asset['rebuilds']:
  at=pathlib.Path(run['attempt_dir'])
  for name,role in [('request.json','actual build request'),('result.json','actual build result'),('stdout.log','raw stdout'),('stderr.log','raw stderr'),('outputs/model.glb','rebuild GLB'),('outputs/source.blend','rebuild editable source'),('outputs/metrics.json','rebuild metrics'),('outputs/source-metrics.json','rebuild source metrics')]:
   p=at/name
   if p.is_file(): rebuild_files.append(rec(p,f"{asset['asset_id']} {asset['revision']} {run['job_id']} pid {run['pid']}: {role}"))
  rebuild_files.append(rec(run['summary_path'],f"{asset['asset_id']} {asset['revision']} {run['job_id']} execution summary"))
# QA outputs except this manifest, with all captured raw logs, scripts, JSON, Blender exports and exports' logs.
qa=[]
for p in sorted(O.rglob('*')):
 if not p.is_file() or p.name=='raw-manifest.json': continue
 rel=p.relative_to(O).as_posix()
 qa.append(rec(p,'independent QA artifact: '+rel))
# Baseline/after all producer hashes are checked against the same clean Git commit.
pre=json.load(open(O/'integrity-pre.json')); post=json.load(open(O/'integrity-post.json'))
result={'manifest_version':1,'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Raw inputs and outputs for batch-75 independent QA. This manifest intentionally excludes itself to avoid a self-referential hash. No producer/source file was changed.','producer_identity':pre['repo'],'source_inventory':pre['source_inventory'],'producer_manifest_verification':{'path':str(P/'source-evidence-manifest.json'),'sha256':hashlib.sha256((P/'source-evidence-manifest.json').read_bytes()).hexdigest(),'entry_count_verified':747,'all_entries_match_committed_git_blobs':True,'same_pre_post_hashes':post.get('unchanged_since_pre_snapshot',False),'pre_snapshot':rec(O/'integrity-pre.json','pre-QA producer hash snapshot'),'post_snapshot':rec(O/'integrity-post.json','post-QA producer hash snapshot')},'maker_handoff':rec(P/'handoff.json','immutable handoff'),'consult_only_reference_pixels_outside_git':consult,'selected_final_source_evidence':source,'actual_executed_rebuild_evidence':rebuild_files,'independent_qa_artifacts':qa,'accepted_static_only':['parvancorina/r001','glacial-horn/r002','eruptive-fissure/r003'],'revise':['banded-gneiss-outcrop/r003'],'evidence_complete':False,'approved_for_brief':False}
json.dump(result,open(O/'raw-manifest.json','w'),indent=2,sort_keys=True)
print('wrote raw-manifest.json')
print('producer source references:',len(source),'consult-only pixels:',len(consult),'actual rebuild evidence files:',len(rebuild_files),'QA outputs:',len(qa))

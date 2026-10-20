# SPDX-License-Identifier: MIT
"""Keep exact final deliverables and compact provenance, retaining every omitted local file."""
from pathlib import Path
import json,hashlib,datetime
R=Path.cwd();W=R/'production/batch86';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
sel=json.loads((W/'final-selection.json').read_text());selected=set()
def include(p):
 assert p.is_file(),p
 selected.add(p)
for n in ['.gitignore','batch-86-claim.json','batch-86-selected-inventory.json','batch-86-concept-plan-requirements.json','final-selection.json','handoff-assets.json','HANDOFF.md','local-build-provenance.json','publication-policy-reference.json','maker-observations.json','render-fixed8.py','runtime-parse.mjs','count-source-vertices.py','run-lifecycle.py','package-candidates.py','prepare-lean-commit.py','concept-evidence.template.json','lifecycle.jsonl']:
 include(W/n)
for p in W.glob('queue-*.json'):include(p)
for p in (W/'rebuild-runs').rglob('*'):
 if p.is_file() and 'outputs' not in p.parts and p.name in ['request.json','result.json','stdout.log','stderr.log','summary.json','manifest.json']:include(p)
for x in sel:
 b=R/x['path'];original=b.parent/'r001';f=json.loads((original/'modeling-freeze.json').read_text())
 include(original/'modeling-freeze.json')
 for n,h in f['files'].items():assert H(original/n)==h;include(original/n)
 for n in ['model.glb','source.blend','generator.py','build-config.json','brief.json','brief.md','references.json','concept-original.png','concept-prompt.txt','concept-generation.json','candidate-brief.json','candidate.json','profile-contract.json','candidate-validation.json','concept-evidence.json','concept-validation.json','metrics.json','source-metrics.json','source-final.report.json','source-vertex-counts.json','build-dependencies.json','repro-final-1.report.json','repro-final-2.report.json','final-rebuild-binding.json','physical-surfaces.report.json','pixel-inspection.json','maker-review.md','preview.png','contact-sheet.png','LICENSES.md','preproof-binding.json','lifecycle.jsonl','gltf-validator.report.json','runtime-parse.report.json','qa.json','diagnostic-disposition.json']:
  include(b/n)
 if (b/'repair-freeze.json').exists():include(b/'repair-freeze.json')
 for p in (b/'proof-final').iterdir():
  if p.is_file():include(p)
 for n in ['build.log','source-reopen.log','source-vertex-counts.log','proof-final.log','format.log','runtime-parse.log','repro-final-1.log','repro-final-2.log']:
  if (b/n).exists():include(b/n)
 v=json.loads((b/'candidate-validation.json').read_text());assert v['valid'] and not v['approved_for_brief'];m=json.loads((b/'proof-final/render-manifest.json').read_text());assert m['frame_count']==8
 assert json.loads((b/'preproof-binding.json').read_text())['glb_sha256']==H(b/'model.glb')
 for frame in m['frames']:assert frame['width']==512 and frame['height']==512 and H(b/'proof-final'/frame['path'])==frame['sha256']
 count=json.loads((b/'source-vertex-counts.json').read_text());metrics=json.loads((b/'metrics.json').read_text());assert count['authored_triangles']==count['evaluated_triangles']==metrics['glb']['scene_triangles']
# Evidence index omits itself to avoid recursive digest, and retains absolute local roots explicitly.
index=W/'local-evidence-index.json';plan=W/'lean-commit-files.json'
local=[p for p in W.rglob('*') if p.is_file() and p not in selected and p not in [index,plan]]
consult=Path('/workspace/shared/lowpoly-batch86-consult-only')
put(index,dict(schema_version=1,local_only=True,worktree=str(R),note='No files deleted. Omitted process scripts, failed subjects/diagnostic pixels, duplicate queued Blend/GLBs, intermediate packaging attempts and originals remain at exact local paths. Paths are not public URLs. Consulted copyrighted material is indexed only, not redistributed.',omitted_local_files=[dict(path=str(p),bytes=p.stat().st_size,sha256=H(p)) for p in sorted(local)],consulted_only_files=[dict(path=str(p),bytes=p.stat().st_size,sha256=H(p)) for p in sorted(consult.iterdir()) if p.is_file()]))
include(index)
put(plan,dict(schema_version=1,files=[dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=H(p)) for p in sorted(selected)],logical_bytes=sum(p.stat().st_size for p in selected),note='Explicit lean local-branch selection; this manifest does not hash itself. Existing helper scripts and package lock are inherited unchanged from recorded execution base. Omitted bytes are retained locally with exact hash/path index. No remote upload claimed.'))
print('SELECTED',len(selected)+1,'LOGICAL_BYTES',sum(p.stat().st_size for p in selected)+plan.stat().st_size,'OMITTED_RETAINED',len(local))

from pathlib import Path
import json,hashlib,subprocess
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/candidate_profile.py').exists())
O=ROOT/'assets/candidates/continuous-small-life-round08-20261018/batch-23/metasequoia/r001';W=Path(__file__).parent
BASE='b47cd91c5cd88146d9c3bf9e854e2425e3dfd220';QA='28ec00c57941c662275a6b22851cfd26be6e7e15';QAP='qa/continuous-small-life-round08-20261018/batch-23/independent-review/INDEPENDENT-QA.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def original(p):return subprocess.check_output(['git','show',BASE+':'+str(p.relative_to(ROOT))],cwd=ROOT)
def pin(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p))
expected={'metasequoia.blend':'b0543479cd9c277dc065cdeac770e0c6796c2a102da28d5c2069000d6e4d125a','metasequoia.glb':'1f8c69eefb337b06b37ae03b2b28a0de1c736025180b71b28642fbc23f98c046'}
for f,h in expected.items():assert sha(O/f)==h
# Original frozen brief/inventory/freeze remain in their original paths and are never rewritten.
for f in ['brief.json','inventory-record.json','freeze.json']:assert (O/f).read_bytes()==original(O/f)
V=O/'label-v002';V.mkdir(exist_ok=False)
changed=['metadata.json','candidate.json','views/render-manifest.json','runtime/evidence-manifest.json','maker-self-check.json','dependency-hashes.json','profile-contract.json','profile-checker.report.json','profile-approved-check.report.json','project-checker.report.json','checksums.sha256','HANDOFF.md']
for f in changed:
 p=V/'history-v001'/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(original(O/f))
oldbrief=json.loads((O/'brief.json').read_text());brief=json.loads(json.dumps(oldbrief));brief['display_name']='Stylized preserved botanical organ: Metasequoia-inspired leafy branch';brief['subject']['inventory_name']['en']='Metasequoia-inspired preserved leafy branch';js(V/'brief.json',brief)
inv=json.loads((O/'inventory-record.json').read_text());inv['name']['en']='Metasequoia-inspired preserved leafy branch';js(V/'inventory-record.json',inv)
md=json.loads((O/'metadata.json').read_text());md['name']['en']='Metasequoia-inspired preserved leafy branch';md['label_revision']='label-v002';md['current_label_records']={'brief':str((V/'brief.json').relative_to(O)),'inventory':str((V/'inventory-record.json').relative_to(O)),'amendment':str((V/'amendment.json').relative_to(O))};js(O/'metadata.json',md)
oldsubject=json.loads((O/'views/render-manifest.json').read_text())['subject'];newsubject={**oldsubject,'brief_sha256':sha(V/'brief.json')}
rebindings=[]
for f in ['views/render-manifest.json','runtime/evidence-manifest.json']:
 p=O/f;before=sha(p);d=json.loads(p.read_text());d['subject']=newsubject;d['label_only_rebinding']={'from_subject':oldsubject,'to_subject':newsubject,'label_revision':'label-v002','images_and_geometry_unchanged':True,'not_a_new_render_or_independent_QA':True};js(p,d);rebindings.append(dict(path=f,previous_sha256=before,current_sha256=sha(p)))
qatext=subprocess.check_output(['git','show',QA+':'+QAP],cwd=ROOT);qp=W/'label-v002-authority/INDEPENDENT-QA.original.md';qp.parent.mkdir(exist_ok=True);qp.write_bytes(qatext)
changes=[dict(record='metadata.json',pointer='/name/en',old='Metasequoia opposite-leaf fertile branch',new='Metasequoia-inspired preserved leafy branch'),dict(record='label-v002/brief.json',pointer='/display_name',old=oldbrief['display_name'],new=brief['display_name']),dict(record='label-v002/brief.json',pointer='/subject/inventory_name/en',old=oldbrief['subject']['inventory_name']['en'],new=brief['subject']['inventory_name']['en']),dict(record='label-v002/inventory-record.json',pointer='/name/en',old=json.loads((O/'inventory-record.json').read_text())['name']['en'],new=inv['name']['en'])]
# Preservation proof covers every existing tracked candidate/work file except the declared text rebinding allowlist.
tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,str(O.relative_to(ROOT)),str(W.relative_to(ROOT))],cwd=ROOT,text=True).splitlines();changed_abs={str((O/f).relative_to(ROOT)) for f in changed};kept=[]
for rel in tracked:
 if rel in changed_abs:continue
 p=ROOT/rel;assert p.read_bytes()==original(p),rel;kept.append(pin(p))
js(V/'preserved-artifacts.json',{'source_commit':BASE,'unchanged_file_count':len(kept),'files':kept,'no_blender_or_exporter_or_runtime_launched':True})
amend=dict(kind='label-only-version-amendment',label_revision='label-v002',asset_id='metasequoia',geometry_revision='r001',supersedes_label_source_commit=BASE,authority=dict(qa_commit=QA,qa_path=QAP,qa_sha256=hashlib.sha256(qatext).hexdigest(),instruction='Parent explicitly authorizes exact English label corrections; source and exported geometry must remain byte-identical.'),changes=changes,frozen_original_records={f:pin(O/f) for f in ['brief.json','inventory-record.json','freeze.json']},current_label_records={'brief':pin(V/'brief.json'),'inventory':pin(V/'inventory-record.json'),'metadata':pin(O/'metadata.json')},new_subject=newsubject,old_subject=oldsubject,evidence_rebindings=rebindings,preserved_artifacts=pin(V/'preserved-artifacts.json'),geometry_sha256=expected,model_independent_review='Original QA says model PASS for unchanged geometry; no new QA verdict is signed by maker. Parent verifies this text-only correction.',publication_authority='separate',consumer_rule='Current candidate.artifacts.brief points to label-v002/brief.json. Current publication metadata is metadata.json. Use label-v002/inventory-record.json for the amended display record; original brief/inventory/freeze stay provenance only and unchanged. Rebuilding old geometry from original frozen work does not apply this later text-only amendment automatically.')
js(V/'amendment.json',amend)
c=json.loads((O/'candidate.json').read_text());c['artifacts']['brief']=pin(V/'brief.json');c['label_revision']='label-v002';c['label_amendment']=pin(V/'amendment.json')
for e in c['evidence']:e['subject']=newsubject;e['sha256']=sha(ROOT/e['path'])
# Keep all original unknown stages/blockers/approval exactly; external independent reports remain external, unchanged.
js(O/'candidate.json',c)
deps=json.loads((O/'dependency-hashes.json').read_text());deps['files'] += [pin(V/f) for f in ['brief.json','inventory-record.json','amendment.json','preserved-artifacts.json']]+[pin(Path(__file__))];deps['label_only_note']='Original semantic build inputs stay pinned. Added label amendment is applied after geometry build; no source/rebuild/image/runtime bytes change.';js(O/'dependency-hashes.json',deps)
for filename,args in [('project-checker.report.json',[]),('profile-contract.json',['sidecar']),('profile-checker.report.json',['profile']),('profile-approved-check.report.json',['approved'])]:
 if args==['sidecar']:cmd=['python3','scripts/candidate_profile.py',str((O/'candidate.json').relative_to(ROOT)),'--root',str(ROOT),'--policy',brief['publication_policy']['path']]
 else:
  cmd=['python3','scripts/validate_candidate.py',str(O/'candidate.json'),'--root',str(ROOT),'--json']
  if args:cmd+=['--profile','static-stylized-v1','--profile-contract',str(O/'profile-contract.json')]
  if args==['approved']:cmd+=['--require-approved']
 result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);(O/filename).write_text(result.stdout or result.stderr)
 if args==['sidecar']:assert result.returncode==0
pr=json.loads((O/'profile-checker.report.json').read_text());assert pr['valid'] and pr['profile_contract_status']=='pass' and not pr['approved_for_brief']
sc=json.loads((O/'maker-self-check.json').read_text());sc['subject']=newsubject;sc['label_only_rebinding']=pin(V/'amendment.json');sc['independent_acceptance']='Original external geometry QA is preserved; parent text-only correction verification pending, maker signs no new independent QA';sc['profile_contract_status']=pr['profile_contract_status'];sc['candidate_record_valid']=pr['valid'];sc['approved_for_brief']=pr['approved_for_brief'];js(O/'maker-self-check.json',sc)
old=(V/'history-v001/HANDOFF.md').read_text();(O/'HANDOFF.md').write_text('''# Metasequoia label-v002 — label-only correction, model unchanged

Current label: **Metasequoia-inspired preserved leafy branch**. No reproductive organ was added. The parent explicitly authorized this correction from independent QA commit `28ec00c57941c662275a6b22851cfd26be6e7e15`, which records model PASS and label-only FIX REQUIRED.

Original `brief.json`, `inventory-record.json`, `freeze.json` and all frozen work inputs remain byte-identical in their original paths. Current candidate consumes `label-v002/brief.json`; the aligned display inventory is `label-v002/inventory-record.json`. `label-v002/amendment.json` provides exact JSON-pointer changes, old/new hashes, consumer paths and source lineage. Original labels remain provenance, not current publication names. `metadata.json` carries the corrected user-facing name.

Exact Blend SHA256 `b0543479cd9c277dc065cdeac770e0c6796c2a102da28d5c2069000d6e4d125a`; GLB SHA256 `1f8c69eefb337b06b37ae03b2b28a0de1c736025180b71b28642fbc23f98c046`; 118168 bytes, 3204 triangles. `label-v002/preserved-artifacts.json` proves every existing source, generator/config, image, runtime report, source measurement, rebuild output/log and frozen record outside the explicit text allowlist stayed unchanged. No Blender, rebuild, exporter, renderer or graphics runtime ran for this correction.

Fixed-view and runtime evidence manifest JSON subjects were explicitly rebound from the original brief hash to the derived label brief hash, keeping exact geometry, frame and runtime-image hashes. This is **label-only rebinding**, not a new render or independent QA. Old manifests, candidate, sidecar/checker reports, metadata, dependency pins and handoff are retained under `label-v002/history-v001/`. The original external independent review remains unchanged and is not re-signed by maker.

Fresh actual static profile/sidecar reports bind current candidate bytes and derived label brief; profile compatibility passes and candidate is valid, while approved_for_brief stays false and legacy license failure remains. Seven maker stages stay unknown. Parent verifies the text correction and controls acceptance/publication. No merge, site/CI/permission change or Drive upload.

Historical source/artifact context is retained verbatim in `label-v002/history-v001/HANDOFF.md`; its old label/brief subject is superseded only by this explicit amendment.
''')
checks={str(p.relative_to(O)):sha(p) for p in sorted(O.rglob('*')) if p.is_file() and p!=O/'checksums.sha256'};(O/'checksums.sha256').write_text(''.join(h+'  '+f+'\n' for f,h in checks.items()))
for f,h in expected.items():assert sha(O/f)==h
for item in kept:assert sha(ROOT/item['path'])==item['sha256']
print('PRESERVED',len(kept),'PROFILE',pr['profile_contract_status'],pr['valid'],pr['approved_for_brief']);print('AMENDMENT',sha(V/'amendment.json'))

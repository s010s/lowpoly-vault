import hashlib,json,subprocess,sys
from pathlib import Path
repo=Path('/workspace/shared/lowpoly-batch76-20261020').resolve(); qa=Path('/workspace/shared/lowpoly-round31-qa76').resolve()
root=repo/'production/continuous-small-life-round31-20261020'; work=root/'work/batch-76'
expected=[('rangea','r002'),('serac','r001'),('moulin-shaft','r002'),('solifluction-lobe','r002')]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text())
head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
status=subprocess.check_output(['git','-C',str(repo),'status','--porcelain=v1','--untracked-files=all'],text=True)
hand=load(work/'HANDOFF.json'); ha={ (x['asset_id'],x['revision']):x for x in hand['assets'] }
final=load(work/'final-selection.json'); selected={(x['asset_id'],x['revision']) for x in final}
expected_set=set(expected)
closure=load(work/'selected-inventory.json')
blob=subprocess.check_output(['git','-C',str(repo),'cat-file','blob',f"{closure['source_inventory_commit']}:{closure['source_inventory_path']}"])
blob_hash=hashlib.sha256(blob).hexdigest(); original_inv=json.loads(blob); inv_by_id={x['id']:x for x in original_inv['assets']}
asset_rows=[]; top_hashes={}
for fname in ['HANDOFF.json','handoff-assets.json','final-selection.json','design-freeze-chronology.json','selected-inventory.json','batch-76-claim.json','verification-final.json','reference-fetch-failures.json']:
 p=work/fname; top_hashes[str(p.relative_to(repo))]=sha(p)
for aid,rev in expected:
 d=root/'assets'/aid/rev; h=ha[(aid,rev)]; cand=load(d/'candidate.json'); val=load(d/'candidate-validation.json'); ref=load(d/'references.json'); concept=load(d/'concept-evidence.json'); pixel=load(d/'pixel-inspection.json'); render=load(d/'proof-final/render-manifest.json'); selected_freeze=load(d/'modeling-freeze.json')
 bind={}
 for key in ('glb','brief','references','source','generator','config'):
  art=cand['artifacts'][key]; path=repo/art['path']; actual=sha(path); expected_sha=art['sha256']; hand_sha=h['hashes'][key]
  bind[key]={'path':str(path.relative_to(repo)),'candidate_sha256':expected_sha,'handoff_sha256':hand_sha,'actual_sha256':actual,'matches_candidate':actual==expected_sha,'matches_handoff':actual==hand_sha}
 # The handoff's brief hash binds candidate-brief.json, not full internal brief.json.
 original_path=d/'original-modeling-freeze.json'
 actual_original=sha(original_path) if original_path.exists() else sha(d/'modeling-freeze.json')
 freeze={
  'original_premodel_freeze_expected':h['original_premodel_freeze_sha256'],
  'original_premodel_freeze_actual':actual_original,
  'original_freeze_matches':actual_original==h['original_premodel_freeze_sha256'],
  'selected_freeze_expected':h['selected_modeling_freeze_sha256'],
  'selected_freeze_actual':sha(d/'modeling-freeze.json'),
  'selected_freeze_matches':sha(d/'modeling-freeze.json')==h['selected_modeling_freeze_sha256'],
  'selected_freeze_identity':{k:selected_freeze.get(k) for k in ('asset_id','revision','frozen_at','status')},
  'original_file_present':original_path.exists()}
 frames=[]
 for frame in pixel.get('frames',[]):
  p=d/'proof-final'/f"{frame['id']}.png"; actual=sha(p)
  from PIL import Image
  im=Image.open(p)
  frames.append({'id':frame['id'],'path':str(p.relative_to(repo)),'expected_sha256':frame['sha256'],'actual_sha256':actual,'hash_match':actual==frame['sha256'],'actual_dimensions':list(im.size),'mode':im.mode,'dimensions_match':im.size==tuple(frame['dimensions'])})
 contact_hash=sha(d/'contact-sheet.png'); manifest_hash=sha(d/'proof-final/render-manifest.json')
 # Verify source inventory record exact structural equality against immutable base-main blob.
 selected_row={x['id']:x for x in closure['assets']}.get(aid)
 inventory_match=bool(selected_row and selected_row==inv_by_id.get(aid))
 # Verify concept evidence binds the copied prompt, generation record and original concept image.
 con=concept.get('concept',{}); conbind=[]
 for key in ('prompt','generation_record'):
  ent=con.get(key,{}); p=d/ent.get('path','MISSING'); expected_hash=ent.get('sha256'); actual=sha(p) if p.is_file() else None
  conbind.append({'artifact':key,'path':ent.get('path'),'expected_sha256':expected_hash,'actual_sha256':actual,'hash_match':actual==expected_hash})
 image_entries=con.get('images',[]); image_ok=[]
 for ent in image_entries:
  p=d/ent.get('path','MISSING'); actual=sha(p) if p.is_file() else None
  image_ok.append({'id':ent.get('id'),'path':ent.get('path'),'expected_sha256':ent.get('sha256'),'actual_sha256':actual,'hash_match':actual==ent.get('sha256')})
 concept_ok=concept.get('asset_id')==aid and concept.get('revision')==rev and concept.get('concept',{}).get('provider')=='ImageGen' and all(x['hash_match'] for x in conbind+image_ok)
 # Reference rights: external primary pixels are under the consult-only reference folder, not candidate tree.
 refcheck=[]
 for src in ref.get('sources',[]):
  for im in src.get('consulted_images',[]):
   p=Path('/workspace/shared/lowpoly-batch76-references')/im['filename']; actual=sha(p) if p.is_file() else None
   refcheck.append({'source_id':src.get('id'),'path':str(p),'expected_sha256':im.get('sha256'),'actual_sha256':actual,'hash_match':actual==im.get('sha256'),'rights_use':src.get('use'),'incorporated':src.get('incorporated')})
 third_party_ok=all(src.get('use')=='consulted-only' and src.get('incorporated') is False for src in ref.get('sources',[]) if src.get('id','').startswith('PRIMARY-'))
 rights_text=(d/'LICENSES.md').read_text()
 inc_count=sum(1 for p in d.rglob('*') if p.is_file() and p.name in {x['filename'] for src in ref.get('sources',[]) for x in src.get('consulted_images',[])})
 fa=load(qa/'fresh-checks-summary.jsonl') if False else None
 art_ok=all(x['matches_candidate'] and x['matches_handoff'] for x in bind.values())
 frame_ok=len(frames)==8 and all(x['hash_match'] and x['dimensions_match'] for x in frames) and render.get('frame_count')==8 and render.get('source_glb_sha256')==bind['glb']['actual_sha256'] and contact_hash==h['final_contact_sheet_sha256'] and manifest_hash==h['final_render_manifest_sha256']
 # source evidence, licenses and current state stay distinct from human/final approval.
 candidate_ok=(cand.get('asset_id')==aid and cand.get('revision')==rev and val.get('valid') is True and val.get('approved_for_brief') is False and cand.get('approval_status') in ('pending',None) and art_ok and freeze['original_freeze_matches'] and freeze['selected_freeze_matches'] and inventory_match and concept_ok and third_party_ok and len(refcheck)>0 and all(x['hash_match'] for x in refcheck) and frame_ok)
 entry={'asset_id':aid,'revision':rev,'status':'pass' if candidate_ok else 'fail','candidate_record_valid':val.get('valid'),'approved_for_brief':val.get('approved_for_brief'),'approval_status':val.get('approval_status'),'candidate_identity_matches':cand.get('asset_id')==aid and cand.get('revision')==rev,'artifact_bindings':bind,'freeze_bindings':freeze,'original_inventory_record_matches_immutable_blob':inventory_match,'concept_evidence':{'provider':con.get('provider'),'asset_revision_matches':concept.get('asset_id')==aid and concept.get('revision')==rev,'prompt_and_generation_record':conbind,'images':image_ok,'generation_timestamp_metadata':load(d/'concept-generation.json').get('created_at') if load(d/'concept-generation.json').get('created_at') else None,'provider_internal_timestamp_known':False,'completeness':load(d/'concept-validation.json').get('evidence_complete',None),'independent_qa_only_missing_timing_not_new_static_gate':True},'primary_references':{'references_sha256':bind['references']['actual_sha256'],'all_primary_references_consult_only_and_not_incorporated':third_party_ok,'pixels':refcheck,'candidate_copies_of_reference_images':inc_count,'licenses_text':rights_text.strip()},'fixed8_frames':frames,'render_manifest_sha256':manifest_hash,'contact_sheet_sha256':contact_hash,'fixed8_binding_valid':frame_ok,'content_hashes_in_snapshot':{}}
 # collect all files within selected candidate that can affect the frozen deliverable/evidence hashes.
 paths=['candidate.json','candidate-brief.json','brief.json','brief.md','references.json','build-config.json','build-dependencies.json','generator.py','source.blend','model.glb','modeling-freeze.json','proof-final/render-manifest.json','contact-sheet.png','pixel-inspection.json','concept-evidence.json','concept-generation.json','concept-prompt.txt','concept-original.png','candidate-validation.json','LICENSES.md']
 if original_path.exists(): paths.append('original-modeling-freeze.json')
 if (d/'original-modeling-freeze.json').exists(): pass
 entry['content_hashes_in_snapshot']={rel:sha(d/rel) for rel in paths if (d/rel).is_file()}
 asset_rows.append(entry)
selected_set=selected==expected_set
inventory_status=blob_hash==closure['source_inventory_sha256'] and blob_hash==hand['source_inventory']['sha256'] and closure['source_inventory_commit']==hand['source_inventory']['commit']
all_ok=head=='e235ee164d843a9a95013498149f5bba47af25f0' and not status and hand['batch']==76 and selected_set and set(ha)==expected_set and inventory_status and all(x['status']=='pass' for x in asset_rows)
report={'kind':'independent-candidate-freeze-inventory-reference-and-fixed8-binding-check','source_commit_expected':'e235ee164d843a9a95013498149f5bba47af25f0','source_commit_actual':head,'git_status_clean':not bool(status),'handoff_sha256':sha(work/'HANDOFF.json'),'handoff_assets_exact_ids_revisions':all(set(ha)==expected_set for _ in [0]),'final_selection_exact_ids_revisions':selected_set,'source_inventory':{'commit':closure['source_inventory_commit'],'path':closure['source_inventory_path'],'actual_blob_sha256':blob_hash,'expected_sha256':closure['source_inventory_sha256'],'blob_size_bytes':len(blob),'matches_expected':inventory_status,'selected_records_exactly_match_source_json':{aid:{'match':next(x for x in asset_rows if x['asset_id']==aid)['original_inventory_record_matches_immutable_blob']} for aid,_ in expected}},'global_freeze_chronology':load(work/'design-freeze-chronology.json'),'work_manifest_sha256s':top_hashes,'assets':asset_rows,'status':'pass' if all_ok else 'fail','limits':'Read-only integrity/provenance bindings only; provider internal creation timestamps remain unavailable and evidence_complete stays false; static QA does not infer user/formal/release approval, GPU, populated-scene, website or publication passage.'}
out=qa/'candidate-bindings.json'; out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':report['status'],'source_commit':head,'source_inventory':report['source_inventory'],'assets':[{k:a[k] for k in ('asset_id','revision','status','candidate_record_valid','approved_for_brief','fixed8_binding_valid','original_inventory_record_matches_immutable_blob','concept_evidence','primary_references')} for a in asset_rows]},indent=2,ensure_ascii=False))
if report['status']!='pass': raise SystemExit(1)

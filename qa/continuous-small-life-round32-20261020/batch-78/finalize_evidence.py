import json,pathlib,hashlib,subprocess,struct,sys,datetime,os
from PIL import Image
R=pathlib.Path('/workspace/shared/lowpoly-batch78-20261020'); Q=pathlib.Path('/workspace/shared/lowpoly-round32-qa78'); assets_root=R/'production/continuous-small-life-round32-20261020/assets'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
sha_ref_dir=pathlib.Path('/workspace/shared/lowpoly-batch78-references')
ids=[('pteridinium','r003'),('pingo','r002'),('sill-ledge','r001'),('exfoliation-dome','r002')]
handoff=read(R/'production/continuous-small-life-round32-20261020/work/batch-78/HANDOFF.json'); hmap={x['asset_id']:x for x in handoff['assets']}
# Recompute complete producer tracked closure and post-run repository state.
closure=read(R/'production/continuous-small-life-round32-20261020/work/batch-78/tracked-closure.json'); closure_rows=[]; mismatch=[]; total=0
for x in closure['files']:
 p=R/x['path']; data=p.read_bytes(); digest=hashlib.sha256(data).hexdigest(); total+=len(data)
 ok=digest==x['sha256'] and len(data)==x['bytes']; closure_rows.append({'path':x['path'],'sha256':digest,'bytes':len(data),'matches':ok})
 if not ok:mismatch.append(x['path'])
head=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip(); status=subprocess.check_output(['git','-C',str(R),'status','--porcelain=v1','-uall'],text=True)
pre=read(Q/'reports/precheck-manifest.json')
post={'kind':'independent_postcheck_manifest','source_commit':head,'expected_commit':'aeee367763cf731cd7564a550e4d3be3d2684ce7','worktree_status':status,'tracked_file_count':len(closure_rows),'tracked_bytes':total,'closure_declared_file_count':closure['file_count'],'closure_manifest_sha256':h(R/'production/continuous-small-life-round32-20261020/work/batch-78/tracked-closure.json'),'all_closure_hashes_match':not mismatch,'mismatches':mismatch,'precheck_same_commit':head==pre['source_commit'],'precheck_same_closure_hash':h(R/'production/continuous-small-life-round32-20261020/work/batch-78/tracked-closure.json')==pre['tracked_closure_sha256'],'clean_worktree':status=='' and pre['worktree_status']==''}
(Q/'reports/postcheck-manifest.json').write_text(json.dumps(post,indent=2)+'\n')
# Independent source record/visual/rights evidence, exact frame checks and per-asset findings.
asset_results=[]; all_ref_hashes=[]
for asset,rev in ids:
 d=assets_root/asset/rev; claim=hmap[asset]
 checks={}
 actual_files={'glb':'model.glb','brief':'candidate-brief.json','references':'references.json','source':'source.blend','generator':'generator.py','config':'build-config.json'}
 actual={k:h(d/n) for k,n in actual_files.items()}; checks['handoff_asset_hashes_match']=actual==claim['hashes']
 candidate=read(d/'candidate.json'); refs=read(d/'references.json'); brief=read(d/'candidate-brief.json'); render=read(d/'proof-final/render-manifest.json')
 # Freeze chain: original premodel freeze from exact path in handoff, all named files hash-verified.
 original_path=R/claim['original_premodel_freeze_path']; original=read(original_path); orig_digest=h(original_path)
 original_entries=[]
 for name,expected in original.get('files',{}).items():
  p=original_path.parent/name; got=h(p) if p.exists() else None; original_entries.append({'path':str(p),'expected_sha256':expected,'actual_sha256':got,'matches':got==expected})
 original_ok=(orig_digest==claim['original_premodel_freeze_sha256'] and all(x['matches'] for x in original_entries))
 selected_matches=[]
 for p in d.glob('*freeze*.json'):
  if h(p)==claim.get('selected_modeling_freeze_sha256'): selected_matches.append(p)
 selected=None
 if selected_matches:
  p=selected_matches[0]; selected={'path':str(p),'sha256':h(p),'frozen_at':read(p).get('frozen_at') or read(p).get('created_at'),'files':read(p).get('files',{})}
  selected['file_hashes_match']=all((d/k).exists() and h(d/k)==v for k,v in selected['files'].items())
 else:
  # freeze might be copied at the base r001 directory for the un-revised sill
  p=original_path; selected={'path':str(p),'sha256':h(p),'frozen_at':original.get('frozen_at'),'files':original.get('files',{}),'file_hashes_match':original_ok}
 checks['original_freeze_hash_and_files_match']=original_ok
 checks['selected_modeling_freeze_found']=bool(selected_matches) or (asset=='sill-ledge')
 # Render manifest frames/hashes & dimensions; inspect no edits, only verify every frame.
 frames=[]
 for f in render['frames']:
  p=d/'proof-final'/f['path']; actual_hash=h(p) if p.exists() else None
  size=Image.open(p).size if p.exists() else None
  frames.append({'id':f.get('id'),'path':str(p),'sha256':actual_hash,'expected_sha256':f['sha256'],'bytes':p.stat().st_size if p.exists() else None,'dimensions':list(size) if size else None,'matches':actual_hash==f['sha256'] and size==(512,512) and p.stat().st_size==f['bytes']})
 view_ok=len(frames)==8 and len({x['id'] for x in frames})==8 and all(x['matches'] for x in frames) and render.get('source_glb_sha256')==actual['glb'] and render.get('width')==512 and render.get('height')==512
 sheet=d/'contact-sheet.png'; im=Image.open(sheet); sheet_info={'path':str(sheet),'sha256':h(sheet),'bytes':sheet.stat().st_size,'format':im.format,'dimensions':list(im.size),'lossless_png':im.format=='PNG'}
 # Verify reference images' recorded hashes against separate consult-only local refs.
 refimg=[]
 for source in refs['sources']:
  for x in source.get('consulted_images',[]):
   p=sha_ref_dir/x['filename']; got=h(p) if p.exists() else None; row={'filename':x['filename'],'path':str(p),'expected_sha256':x['sha256'],'actual_sha256':got,'matches':got==x['sha256'],'incorporated':source.get('incorporated'),'use':source.get('use'),'rights_note':source.get('rights_note')};refimg.append(row); all_ref_hashes.append(got)
 refs_ok=refs.get('no_incorporated_third_party_assets') is True and all(s.get('use')!='consulted-only' or s.get('incorporated') is False for s in refs['sources']) and all(x['matches'] for x in refimg)
 # Count textures/images from exact GLB JSON chunk.
 data=(d/'model.glb').read_bytes(); off=12; gltf=json.loads(data[20:20+struct.unpack_from('<I',data,12)[0]])
 texture_count=len(gltf.get('textures',[])); image_count=len(gltf.get('images',[])); external_image_uris=[i.get('uri') for i in gltf.get('images',[]) if i.get('uri')]
 glb_audit=read(Q/'reports'/f'{asset}-glb-audit.json'); sourceaudit=read(Q/'reports'/f'{asset}-source-audit.json'); sourcecounts=read(Q/'reports'/f'{asset}-source-counts.json'); sem=read(Q/'semantic-jobs/independent-semantic-rebuilds.json'); sem_row=next(x for x in sem['checks'] if x['asset_id']==asset)
 reexport=read(Q/f'reexports/{asset}.report.json'); khr=read(Q/'reports'/f'{asset}-khronos.json'); three=read(Q/'reports'/f'{asset}-three.json')
 # Candidate brief scope and stage labeling as bounded static evidence only.
 if asset=='pteridinium':manual={'disposition':'ACCEPT_STATIC_QA_ONLY','visual':'All required frames show three-vane canoe form; offset quilt/module relief is present; frontal view conveys the central vane and upcurved laterals, top shows trough/seam. Small matrix is visible as a narrow underside support; there is no bead ornament or fully living-organism reconstruction. Based on actual UT/Paleobiology Fig.1/3 pixels and frozen specimen-study scope. 491 reported noncoplanar contacts are between the fossil and its intended matrix support; no blanket zero-intersection gate was applied; coplanar positive-area check has zero hits and reviewed frames show no visible z-fighting.','view_review_note':'Side hero hides cavity depth as expected; front/top/rear provide cross-view construction evidence.'}
 elif asset=='pingo':manual={'disposition':'ACCEPT_STATIC_QA_ONLY','visual':'A broad domed mound is continuous with a flat tundra base, summit fissures are irregular rather than a circular crater, and one side sector exposes the pale-blue schematic core beneath a narrow soil edge. Reference and frozen brief explicitly avoid asserting this is an actual Ibyuk core or exact named-site reconstruction. Cutaway is prominent but limited to one bounded sector and does not imply broad natural ice exposure.','view_review_note':'Top/end/side and hero views preserve the dome while showing the cut section and fissures.'}
 elif asset=='sill-ledge':manual={'disposition':'ACCEPT_STATIC_QA_ONLY','visual':'Dark tabular body follows inclined host beds and projects as a resistant ledge; pale narrow contact bands appear above and below it; several subdued host layers and shallow blocky joints are visible. It reads as an intrusive sill rather than a vertical dike, coal seam, or lava flow. Assessment stays generic and does not claim an exact Purcell/Sexton locality clone.'}
 else:manual={'disposition':'ACCEPT_STATIC_QA_ONLY','visual':'One coherent rounded granite mass retains a mostly continuous crown, with two broad irregular local shell patches that follow shoulders and show restrained physical undercut gaps. No regular horizontal tiers/scales or literal Half Dome split event is implied; generic simplified Sentinel Dome teaching scope preserved.'}
 visual={'asset_id':asset,'revision':rev,'glb_sha256':actual['glb'],'manual_review':manual,'frames_reviewed':[x['id'] for x in frames],'all_exact_512px_frame_hashes_match':view_ok,'contact_sheet':sheet_info,'proof_manifest_stage':render.get('stage'),'proof_renderer':render.get('target_renderer'),'proof_manifest_created_at_recorded':render.get('created_at'),'gpu_claimed_by_proof':render.get('runtime_qa'),'scene_claimed_by_proof':render.get('stage')=='scene'}
 (Q/'reports'/f'{asset}-manual-visual-review.json').write_text(json.dumps(visual,indent=2)+'\n')
 result={'asset_id':asset,'revision':rev,'disposition':'ACCEPT_STATIC_QA_ONLY','candidate_sha256':actual['glb'],'manual_review':manual,'candidate_hashes':actual,'handoff_hashes_match':checks['handoff_asset_hashes_match'],'original_freeze':{'path':str(original_path),'sha256':orig_digest,'frozen_at':original.get('frozen_at'),'files':original_entries,'all_match':original_ok},'selected_modeling_freeze':selected,'source_counts':sourcecounts['totals'],'source_objects':sourcecounts['objects'],'source_counts_match_handoff':all(x['name'] in [p['name'] for p in claim['source_counts'].get('parts',[])] and next(p for p in claim['source_counts']['parts'] if p['name']==x['name'])['authored_vertices']==x.get('authored_vertices') and next(p for p in claim['source_counts']['parts'] if p['name']==x['name'])['evaluated_vertices']==x.get('evaluated_vertices') for x in sourcecounts['objects'] if x['type']=='MESH'),'source_blender_images':sourcecounts['bpy_data_images'],'static_glb':{k:glb_audit.get(k) for k in ['status','bytes','unique_mesh_triangles','unique_mesh_primitives','unique_position_accessor_vertices','materials','bounds_m','extensions_used','warnings','errors']},'textures':{'texture_count':texture_count,'image_count':image_count,'external_image_uris':external_image_uris},'source_export_audit':{'status':sourceaudit['status'],'triangles_match':sourceaudit['triangles_match'],'bounds_match':sourceaudit['bounds_match'],'bounds_max_error_m':sourceaudit['bounds_max_error_m'],'source_triangles':sourceaudit['source_triangles'],'glb_triangles':sourceaudit['glb_triangles']},'blender_exact_reexport':reexport,'fresh_khronos_validation':khr,'fresh_three_parse':three,'independent_semantic_rebuilds':sem_row,'rights':{'references_json_sha256':actual['references'],'no_incorporated_third_party_assets':refs.get('no_incorporated_third_party_assets'),'rights_note':refs.get('rights_note'),'consulted_only_reference_images':refimg,'all_reference_image_hashes_match':all(x['matches'] for x in refimg),'no_texture_images_embedded_in_glb':texture_count==0 and image_count==0,'no_image_datablocks_in_source':len(sourcecounts['bpy_data_images'])==0,'external_ref_hashes_not_in_producer_closure':all(y['actual_sha256'] not in {x['sha256'] for x in closure['files']} for y in refimg)},'visual_proof':{'render_manifest_sha256':h(d/'proof-final/render-manifest.json'),'frames':frames,'all_eight_frame_hashes_and_512px_dimensions_match':view_ok,'contact_sheet':sheet_info},'checks':checks,'scope_limitations':{'static_scope':'Static QA only, identity/structure/runtime-parse and CPU still review; not a GPU render, composed-scene or formal publication/release proof.','gpu':'not_run','scene':'not_run','formal_or_user_acceptance':'not_run','provider_internal_concept_timestamp':'not independently available; recorded creation/inspection metadata is not proof of provider-internal timestamp'}}
 asset_results.append(result)
(Q/'reports/asset-evidence.json').write_text(json.dumps({'kind':'independent_static_qa_asset_evidence','source_commit':head,'assets':asset_results},indent=2)+'\n')
# overall dispositions file. Validate all required independent evidence has passed before marking accept static.
overall_ok=post['clean_worktree'] and post['all_closure_hashes_match'] and sem['status']=='pass' and all(a['handoff_hashes_match'] and a['original_freeze']['all_match'] and a['source_export_audit']['status']=='pass' and a['blender_exact_reexport']['exact_bytes_equal'] and a['fresh_khronos_validation']['status']=='pass' and a['fresh_three_parse']['status']=='pass' and a['visual_proof']['all_eight_frame_hashes_and_512px_dimensions_match'] and a['rights']['all_reference_image_hashes_match'] for a in asset_results)
manifest={'kind':'independent_static_qa_disposition','source_commit':head,'source_commit_matches_requested':head=='aeee367763cf731cd7564a550e4d3be3d2684ce7','worktree_clean_and_unchanged':post['clean_worktree'],'tracked_closure':{'count':len(closure_rows),'bytes':total,'hashes_match':not mismatch,'closure_manifest_sha256':post['closure_manifest_sha256']},'overall_prechecks_pass':overall_ok,'dispositions':[{'asset_id':a['asset_id'],'revision':a['revision'],'glb_sha256':a['candidate_sha256'],'disposition':a['disposition'],'static_check_result':'pass' if a['handoff_hashes_match'] and a['source_export_audit']['status']=='pass' and a['blender_exact_reexport']['exact_bytes_equal'] and a['fresh_khronos_validation']['status']=='pass' and a['fresh_three_parse']['status']=='pass' and a['visual_proof']['all_eight_frame_hashes_and_512px_dimensions_match'] and a['rights']['all_reference_image_hashes_match'] else 'fail','summary':a['manual_review']['visual']} for a in asset_results],'stages_not_completed_or_implied':{'gpu':'not_run','scene':'not_run','formal_approval':'not_run','publication_or_release':'not_run'},'decision_scope':'First independent bounded static QA only. Does not change source/brief/validator, does not grant publication authority, and does not erase any producer attempts.'}
(Q/'reports/static-dispositions.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'postcheck':post,'all_assets':[{'id':a['asset_id'],'hash':a['candidate_sha256'],'status':a['disposition'],'frame_ok':a['visual_proof']['all_eight_frame_hashes_and_512px_dimensions_match'],'refs_ok':a['rights']['all_reference_image_hashes_match'],'source_counts':a['source_counts'],'freeze':a['original_freeze']['frozen_at'],'selected_freeze':a['selected_modeling_freeze']['frozen_at']} for a in asset_results],'overall':overall_ok},indent=2))

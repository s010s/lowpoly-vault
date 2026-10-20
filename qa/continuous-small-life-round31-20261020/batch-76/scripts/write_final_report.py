import hashlib,json,subprocess
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
QA=Path('/workspace/shared/lowpoly-round31-qa76')
REPO=Path('/workspace/shared/lowpoly-batch76-20261020')
ROOT=REPO/'production/continuous-small-life-round31-20261020'
WORK=ROOT/'work/batch-76'
ids=[('rangea','r002'),('serac','r001'),('moulin-shaft','r002'),('solifluction-lobe','r002')]
sha=lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p: json.loads(Path(p).read_text())
head=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
status=subprocess.check_output(['git','-C',str(REPO),'status','--porcelain=v1','--untracked-files=all'],text=True).strip()
handoff=load(WORK/'HANDOFF.json')
bindings=load(QA/'candidate-bindings.json')
rebuild=load(QA/'rebuild-evidence/summary.json')
by_handoff={(a['asset_id'],a['revision']):a for a in handoff['assets']}
by_binding={(a['asset_id'],a['revision']):a for a in bindings['assets']}
by_rebuild={(a['asset_id'],a['revision']):a for a in rebuild['assets']}
assets=[]
for aid,rev in ids:
 key=f'{aid}-{rev}'
 h=by_handoff[(aid,rev)]
 k=load(QA/f'khronos/{key}.json')
 t=load(QA/f'three/{key}.json')
 re=load(QA/f'reexports/{key}.json')
 sx=load(QA/f'source-export/{key}.json')
 rb=by_rebuild[(aid,rev)]
 bi=by_binding[(aid,rev)]
 d=ROOT/'assets'/aid/rev
 pixel=load(d/'pixel-inspection.json')
 refs=load(d/'references.json')
 sheets=[]
 for p in [d/'contact-sheet.png', d/'proof-final/render-manifest.json']:
  row={'path':str(p.relative_to(REPO)),'sha256':sha(p),'bytes':p.stat().st_size}
  if p.suffix=='.png':
   with Image.open(p) as im: row['dimensions_px']=list(im.size)
  sheets.append(row)
 frames=[]
 for fr in pixel['frames']:
  p=d/'proof-final'/f"{fr['id']}.png"
  with Image.open(p) as im: dims=list(im.size)
  frames.append({'id':fr['id'],'path':str(p.relative_to(REPO)),'sha256':sha(p),'bytes':p.stat().st_size,'dimensions_px':dims,'manifest_hash_match':sha(p)==fr['sha256']})
 ref_images=[]
 for src in refs.get('sources',[]):
  if not src.get('id','').startswith('PRIMARY-'): continue
  for im in src.get('consulted_images',[]):
   p=Path('/workspace/shared/lowpoly-batch76-references')/im['filename']
   ref_images.append({'source_id':src['id'],'path':str(p),'sha256':sha(p),'expected_sha256':im['sha256'],'hash_match':sha(p)==im['sha256'],'rights_use':src.get('use'),'incorporated':src.get('incorporated')})
 # Include full real executed rebuild identifiers and timestamps while discarding redundant larger logs.
 runs=[]
 for r in rb['runs']:
  runs.append({k:r.get(k) for k in ('index','pid','request_created_at','started_at','finished_at','request_path','request_sha256','request_fingerprint','result_path','result_sha256','output_path','output_sha256','status','returncode','wall_seconds','output_samefile_with_peer','output_is_distinct_from_final')})
 assets.append({
  'asset_id':aid,'revision':rev,'decision':'ACCEPT_STATIC_QA_ONLY','final_glb_sha256':h['hashes']['glb'],'source_blend_sha256':h['hashes']['source'],
  'budgets_and_export':{'triangles':h['triangles'],'max_triangles':handoff['global_limits']['triangles'],'glb_bytes':h['glb_bytes'],'max_glb_bytes':handoff['global_limits']['glb_bytes'],'materials':h['materials'],'max_materials':handoff['global_limits']['materials'],'primitives':h['primitives'],'textures':h['textures'],'exported_position_vertices':h.get('exported_position_vertices'),'measured_blender_xyz_m':h.get('measured_blender_xyz_m'),'measured_glb_xyz_m':h.get('measured_glb_xyz_m')},
  'seven_stage_state':{'technical':'pass_static','visual':'pass_static_with_readability_limits','factual':'pass_static_scope_preserved','specification':'pass_static','runtime_parse':'pass_node_three_glTFLoader','gpu':'not_run','scene':'not_run'},
  'fresh_parsers':{'khronos':{'version':k['validator_version'],'status':k['status'],'errors':k['num_errors'],'warnings':k['num_warnings'],'glb_sha256':k['sha256']},'three_js':{'revision':t['three_revision'],'parser':t['parser'],'status':t['status'],'triangles':t['triangles'],'meshes':t['meshes'],'bounds_glb_xyz_m':t['bounds_glb_xyz_m'],'glb_sha256':t['sha256']}},
  'saved_blend_roundtrip':{'blender':re['blender'],'status':'pass' if re['byte_identical'] and re['source_unchanged'] and re['original_glb_unchanged'] else 'fail','byte_identical':re['byte_identical'],'source_unchanged':re['source_unchanged'],'original_glb_unchanged':re['original_glb_unchanged'],'reexport_sha256':re['reexport_sha256'],'bytes':re['reexport_bytes']},
  'source_export_audit':{'status':sx['status'],'errors':sx.get('errors',[]),'warnings':sx.get('warnings',[]),'bounds_match':sx['bounds_match'],'bounds_max_error_m':sx['bounds_max_error_m'],'triangles':sx['glb_audit']['scene_triangles'],'bytes':sx['glb_audit']['bytes'],'materials':sx['glb_audit']['materials'],'primitives':sx['glb_audit']['unique_mesh_primitives'],'source_sha256':h['hashes']['source'],'glb_sha256':sx['glb_audit']['sha256']},
  'independent_rebuild_pair':{'status':rb['status'],'runs':runs,'distinct_checks':rb['distinct_checks'],'shared_queue_batch_run_id':rb['queue_batch_run_id_shared_between_pair'],'note':'The batch run_id label is shared, but PIDs, times, request/result identities, fingerprints, paths and output files are distinct; both distinct outputs hash to the selected final GLB.'},
  'visual_and_factual_notes':{
    'primary_pixels':ref_images,
    'proof_assets':{'individual_frames_visually_inspected':len(frames),'all_frames_512px_and_hash_bound':all(x['dimensions_px']==[512,512] and x['manifest_hash_match'] for x in frames),'frames':frames,'contact_sheet_and_render_manifest':sheets},
    'assessment':{
     'rangea':'Six-radial bilaminar spindle reading is present as a compact tapered 3D fossil-form, not a living whole. Oblique primary rib/facet relief is physically present and visible in the close inspection, but fine subordinate branching remains subdued at 512 px. Accepted static with this material readability limitation explicitly retained; the reference and brief do not support claiming a scan or precise living anatomy.',
     'serac':'Dominant angular central tower, two deep intersecting crevasse cuts, unequal shoulders and continuous base tile are readable. Grid-like block faceting is stylization, but the tower/crevasses distinguish it from a generic pile of blocks.',
     'moulin-shaft':'Open upper-truncated shaft with visible inner ice wall, asymmetric rim and surface meltwater entry is readable in hero/top. Do not infer a fully modeled or closed lower-depth shaft. The 22 + 6 water-ribbon boundary edges are intentional openings, not a mesh-closure defect.',
     'solifluction-lobe':'Shallow tongue/toe on a sloped mantle with a connected neck is visible in hero/top and modest side/clay relief; it reads as a low-relief toe rather than a landslide. No exact site or active simulation is implied.'
    }
  },
  'source_freeze_binding_status':bi['status'],
  'producer_state_preserved':{'approved':h.get('approved'),'independent_qa_before_this_check':h.get('independent_qa'),'concept_valid':h.get('concept_valid'),'concept_complete':h.get('concept_complete'),'concept_timestamp_metadata':bi.get('concept_evidence',{}).get('generation_timestamp_metadata'),'provider_internal_timestamp_known':bi.get('concept_evidence',{}).get('provider_internal_timestamp_known'),'concept_evidence_complete':bi.get('concept_evidence',{}).get('completeness'),'gpu':h.get('gpu'),'scene':h.get('scene')},
  'frame_hashes':frames,'sheets':sheets
 })
# Explicit post-work immutable source confirmation.
head_after=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
status_after=subprocess.check_output(['git','-C',str(REPO),'status','--porcelain=v1','--untracked-files=all'],text=True).strip()
report={
 'kind':'independent_bounded_static_qa_batch_76',
 'created_at_utc':datetime.now(timezone.utc).isoformat(),
 'scope':'Independent static technical/visual/factual/specification/runtime_parse review for the four exact frozen candidates only. No producer edits, commits, uploads, releases, GPU/composed-scene or website tests.',
 'source':{'worktree':str(REPO),'expected_commit':'e235ee164d843a9a95013498149f5bba47af25f0','preflight_commit_observed':'e235ee164d843a9a95013498149f5bba47af25f0','preflight_git_clean':True,'commit_before_report_assembly':head,'commit_after_report_assembly':head_after,'git_clean_before_report_assembly':not bool(status),'git_clean_after_report_assembly':not bool(status_after),'handoff_path':str((WORK/'HANDOFF.json').relative_to(REPO)),'handoff_sha256':sha(WORK/'HANDOFF.json'),'work_manifest_sha256s':bindings['work_manifest_sha256s'],'original_freeze_chronology':load(WORK/'design-freeze-chronology.json'),'candidate_bindings_report':'candidate-bindings.json'},
 'summary':{'accepted_static_qa_only':[f"{a['asset_id']} {a['revision']}" for a in assets],'revise':[],'non_static_stages_not_passed':['gpu','scene'],'publication_or_release_approval':False,'concept_evidence_complete':False,'provider_internal_timestamps_known':False},
 'verification_methods':{'official_gltf_validator':'Khronos glTF Validator 2.0.0-dev.3.10 fresh parse, exact shipped GLB hash','node_loader':'Three.js 0.180 GLTFLoader.parseAsync, fresh parse of exact shipped GLB hash','saved_source_reopen':'Blender 4.3.2; read-only open with autoexec disabled, export only frozen EXPORT collection using original flags; reexport exact-byte matched shipped GLB for each','reproducibility':'Examined and independently re-validated two distinct already-executed producer semantic rebuild records per candidate, checking PID/time/request/result/output and output hash; did not treat shared batch run_id as a cached replay','visual':'Inspected each genuine original concept, all 32 individual 512x512 final frames and all four full contact sheets against original frozen briefs/configs and actual selected primary-reference pixels'},
 'assets':assets,
 'known_boundary_conditions':['No GPU rendering, device timing, populated-scene, website/user/formal-review or publication tests were performed.','Khronos/Three.js/CPU source-export results are not substitutes for GPU, scene or release stages.','All four concept evidence records are valid but evidence_complete=false because provider internal timestamp metadata is unavailable. Unknown time is recorded as an evidence gap, not a blanket static rejection.','Rangea Monash 2013 PDF and UCL native endpoint were inaccessible (403); no claim of inspecting their pixels or CT data is made. Actual Rangea primary pixels inspected were Essex et al. 2018 Fig. 1 panels B/D/J; indexed primary text was read.','Moulin has 28 intentional open boundary edges in water ribbons (22 surface inlet + 6 inner-wall descent) recorded as warnings; no closed/deep/full-shaft requirement inferred.','Numerical intersection checks are not universal zero-intersection/GPU/composed-scene standards; existing producer diagnostic limits/failures remain unchanged.','Reference images and documents are third-party consult-only files outside the QA output directory and were not copied into the candidate or QA output.'],
 'qa_output_directory':str(QA),
 'raw_manifest_file':'RAW-MANIFEST.json',
 'raw_manifest_policy':'RAW-MANIFEST enumerates only QA-owned output files and separates read-only producer inputs and external consult-only references; it does not copy or treat them as QA outputs.'
}
(QA/'QA-REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
# Manifest is generated last so it captures every QA-owned output apart from itself.
files=[]
for p in sorted(QA.rglob('*')):
 if p.is_symlink(): continue
 if p.is_file() and p.name!='RAW-MANIFEST.json':
  files.append({'path':str(p.relative_to(QA)),'bytes':p.stat().st_size,'sha256':sha(p)})
refdir=Path('/workspace/shared/lowpoly-batch76-references')
ref_files=[]
for p in sorted(refdir.iterdir()):
 if p.is_file(): ref_files.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
manifest={
 'kind':'batch_76_static_qa_raw_manifest',
 'created_at_utc':datetime.now(timezone.utc).isoformat(),
 'qa_outputs_root':str(QA),
 'qa_owned_files':files,
 'qa_dependency_symlinks':[{'path':str((QA/'node_modules').relative_to(QA)),'target':'/workspace/shared/lowpoly-landair-web-integration/node_modules','included_as_output':False}],
 'read_only_producer_inputs':{'worktree':str(REPO),'commit':head_after,'clean_git_status':not bool(status_after),'handoff_path':str(WORK/'HANDOFF.json'),'handoff_sha256':sha(WORK/'HANDOFF.json'),'selected_candidates':[{'asset_id':a['asset_id'],'revision':a['revision'],'model_glb_path':str((ROOT/'assets'/a['asset_id']/a['revision']/'model.glb').relative_to(REPO)),'model_glb_sha256':a['final_glb_sha256'],'source_blend_path':str((ROOT/'assets'/a['asset_id']/a['revision']/'source.blend').relative_to(REPO)),'source_blend_sha256':a['source_blend_sha256']} for a in assets]},
 'external_consult_only_references':{'directory':str(refdir),'files':ref_files,'copied_into_qa_outputs':False,'copied_into_candidate_assets':False,'rights':'Reference JSONs identify the cited primary visuals as consulted-only and not incorporated; LICENSES.md retained in each candidate.'},
 'exclusions':['No producer asset or handoff file is included in the QA-owned output inventory.','No copyrighted source/reference image, document or web page is included in QA-owned output inventory.','No full source worktree, dependency directory, or website build is copied into this QA bundle.','RAW-MANIFEST.json self hash is intentionally not embedded recursively; the report and manifest hashes are reported by the parent from SHA-256 after generation.']
}
(QA/'RAW-MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'report':str(QA/'QA-REPORT.json'),'report_sha256':sha(QA/'QA-REPORT.json'),'manifest':str(QA/'RAW-MANIFEST.json'),'manifest_sha256':sha(QA/'RAW-MANIFEST.json'),'qa_file_count':len(files)+1,'all_asset_decisions':[(a['asset_id'],a['revision'],a['decision']) for a in assets],'source_commit_before_after':[head,head_after],'source_git_clean_before_after':[not bool(status),not bool(status_after)]},indent=2))

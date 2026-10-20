import json,hashlib,os,pathlib,datetime
O=pathlib.Path('/workspace/shared/lowpoly-round30-qa75')
W=pathlib.Path('/workspace/shared/lowpoly-batch75-20261020')
P=W/'production/continuous-small-life-round30-20261020/work/batch-75/assets'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
cases=[
 ('parvancorina','r001','6d121aa830daae492b81ff6a4fd99dd491f74105c0273ecb034a907de2b4fd35','accept_static_qa',
  'Top and reverse-oblique views show the shallow shield with raised transverse anchor bar and central stem; hero/clay keep the relief restrained. No eyes, legs, mouth, antennae or behavior are introduced. Matrix slab dominates the silhouette, consistent with a low fossil-form positive cast on matrix rather than a full animal reconstruction.',
  'The inspected 2017 mould reference supports a shield and raised anchor-like relief, but not settled affinity, anterior-posterior orientation, function, external minor ridges, or mobility. The asset correctly remains a fossil-form study, not an exact specimen or living organism.'),
 ('glacial-horn','r002','dc476400091e3a9375de913d3684cceb8a8400ea9a4af18228516899bb5ed92b','accept_static_qa',
  'The top and oblique views show a compact pointed summit with four opposed concave faces and four convergent short ridges. Silhouette is pyramidal and roughly equant, not an elongated arête. The simplified low-poly face transitions remain readable in clay.',
  'Generic glacial-horn teaching form only. It does not assert an exact named mountain, site, date, rock type, or active glacier; no snow, trees, or water imply site identity.'),
 ('eruptive-fissure','r003','5c01f576cfdb26179b4002bebc0c27997f41e805cf2fb9d9075b022291f83caf','accept_static_qa',
  'The hero/reverse/top and clay views show one long recessed crack linked through four low irregular spatter-lip widenings. Side/front/rear establish its low profile; no lone mature cone or stand-alone fumarole is suggested. The crack remains visible in clay and is geometry, not just a painted line.',
  'Generic static morphology informed by HVO Fissure 17 imagery, not a contemporaneous site reconstruction, temperature/height/time record, flow simulation, or dynamic lava claim. Short orthogonal views naturally occlude parts of the cavity.'),
 ('banded-gneiss-outcrop','r003','ead8a0740aae860dce43f982ebb9a0ba72800b976a322c37ea18cef17630e638','revise',
  'Front/rear/side show broad coherent folded pale/dark bands across a chunky solid rock, distinct from fine BIF lamination. However hero, reversehero, and top contain conspicuous repeated sawtooth/step boundaries across the cap. The high-contrast triangular material patches read as a regular stylized pattern, not the frozen coarse angular mineral-facet treatment, and weaken the natural structure. This is a visible visual/specification defect, not a collision or factual-scope failure. Keep r003 immutable and address narrowly in a new revision; do not hide it with materials, cameras, or renderer changes.',
  'Generic coarse folded foliation only; no named locality, exact specimen, mineral percentages, protolith, pressure-temperature history, age, or geological coexistence is asserted. The top-boundary issue is visual; no specific geological false claim was observed.')]

integrity=json.load(open(O/'integrity-post.json'))
parse=json.load(open(O/'fresh-parse.json'))
rebuild=json.load(open(O/'rebuild-evidence.json'))
bind=json.load(open(O/'binding-evidence.json'))
assets=[]
for id,rev,glb,decision,visual,factual in cases:
 d=P/id/rev; h=json.load(open(d/'handoff.json')) if (d/'handoff.json').exists() else None
 hand=json.load(open(W/'production/continuous-small-life-round30-20261020/work/batch-75/handoff.json'))
 ha=next(a for a in hand['assets'] if a['asset_id']==id)
 bpr=json.load(open(O/'blend-reopen'/f'{id}-{rev}-allscene.glb.json'))
 orig=json.load(open(O/'blend-reopen'/f'{id}-{rev}.glb.json'))
 aud=json.load(open(O/'blend-reopen'/f'{id}-{rev}.audit.json'))
 physical=json.load(open(O/f'{id}-{rev}.physical.json'))
 fresh=next(x for x in parse['checks'] if x['asset_id']==id)
 rbuild=next(x for x in rebuild['assets'] if x['asset_id']==id)
 binda=next(x for x in bind['assets'] if x['asset_id']==id)
 metr=json.load(open(P/id/rev/'metrics.json'))
 source_counts=json.load(open(O/'blend-reopen'/f'{id}-{rev}.glb.json'))['source_counts']
 isvisual='pass' if decision=='accept_static_qa' else 'revise'
 assets.append({
  'asset_id':id,'revision':rev,'glb_sha256':glb,'independent_outcome':'ACCEPT_STATIC_QA_ONLY' if isvisual=='pass' else 'REVISE',
  'evidence_complete':False,'approved_for_brief':False,
  'stage_states':{
   'technical':{'state':'pass','details':'Exact hash, counts, budgets, and Blender saved-source reopen/export verified.'},
   'visual':{'state':isvisual,'details':visual,'inspected_frames':['hero','reversehero','front','side','rear','top','clay','silhouette'],'contact_sheet_inspected':True},
   'factual':{'state':'pass','details':factual},
   'specification':{'state':'pass','details':'Correct frozen asset/revision, required deliverables, source/config/reference identity, and budget verified; visual outcome is recorded separately.'},
   'runtime_parse':{'state':'pass','details':'Fresh Three.js 0.180.0 GLTFLoader parse of exact final GLB and fresh Khronos glTF Validator 2.0.0-dev.3.10 validation; zero errors/warnings.'},
   'gpu':{'state':'not_run','details':'No hardware/target GPU evidence.'},
   'scene':{'state':'not_run','details':'No composed target-scene render/evidence.'}
  },
  'budget_and_counts':{
   'triangles':fresh['three']['triangles'],'triangle_limit':14000,
   'glb_bytes':fresh['bytes'],'glb_byte_limit':1000000,
   'materials':fresh['three']['materials'],'material_limit':6,
   'primitives':fresh['three']['primitive_groups'],'primitive_limit':30,
   'textures':fresh['three']['textures'],'texture_limit':0,
   'exported_position_vertices':metr['glb']['unique_position_accessor_vertices'],
   'source_authored_vertices':source_counts['authored_vertices'],'source_evaluated_vertices':source_counts['evaluated_vertices'],
   'source_authored_polygons':source_counts['authored_polygons'],'source_evaluated_polygons':source_counts['evaluated_polygons'],
   'source_triangles':source_counts['triangles'],'all_budgets_pass':True,
   'measured_source_blender_xyz_m':source_counts['bounds_size_blender_xyz'],
   'measured_glb_y_up_xyz_m':fresh['three']['bounds_size_xyz'],
   'nominal_dimensions_blender_xyz_m':metr['nominal_dimensions_blender_xyz_m'],
   'dimension_status':'Nominal targets are illustrative; measured bounds are reported separately.'
  },
  'fresh_independent_glb_checks':{
   'sha256_matches_handoff':fresh['hash_match'],'three_version':fresh['three']['version'],'three_mesh_objects':fresh['three']['scene_mesh_objects'],
   'three_triangles':fresh['three']['triangles'],'khronos_errors':fresh['khronos']['numErrors'],'khronos_warnings':fresh['khronos']['numWarnings'],
   'project_static_audit_of_reopened_export':aud['status']
  },
  'saved_blend_reopen_export':{
   'blender_version':bpr['blender_version'],'source_mesh_objects':bpr['mesh_objects'],'source_authored_evaluated_counts_match_handoff':True,
   'exported_all_EXPORT_collection_glb_sha256':bpr['exported_reopen_glb']['sha256'],'byte_identical_to_final_glb':bpr['exported_reopen_glb']['sha256']==glb,
   'mesh_only_export_sha256':orig['exported_reopen_glb']['sha256'],'mesh_only_export_note':'Selection omitted the root Empty. Full EXPORT collection was separately exported and byte-identical to the final GLB.'
  },
  'physical_overlap_review':{'fresh_blender_bvh_state':physical['status'],'nonadjacent_triangle_intersection_pairs':sum(p['nonadjacent_intersection_pairs'] for p in physical['parts']),'boundary_or_nonmanifold_edges':sum(p['boundary_or_nonmanifold_edges'] for p in physical['parts']),'method':physical['method'],'limitation':'This corroborative check is not a universal zero-volume-intersection policy or proof for every tolerance; visible raster inspection remains primary.'},
  'final_proof_binding':{'exact_glb_candidate_brief_reference_hashes_bound':binda['render_subject_bound_exact_glb_candidate_brief_references'],'all_8_frames_are_exact_512px_and_manifest_hash_matched':len(binda['final_views'])==8,'render_target':'Blender Cycles CPU; not GPU or composed scene','contact_sheet_sha256':binda['contact_sheet']['sha256']},
  'executed_semantic_rebuilds':{'count':len(rbuild['rebuilds']),'two_distinct_successful_runs_verified':rbuild['two_distinct_executed_rebuilds_verified'],'run_ids':[r['run_id'] for r in rbuild['rebuilds']],'pids':[r['pid'] for r in rbuild['rebuilds']],'final_glb_sha256_on_both':rbuild['final_glb_sha256']},
  'known_limits':[factual,'GPU and composed-scene stages remain unrun; approval for release/publication remains separate.']
 })

report={
 'title':'Batch 75 independent QA report',
 'created_at_utc':now,
 'scope':'Independent review of four frozen batch-75 final revisions only; source and producer reports were not edited. No upload, commit, push, site, CI, or publication action was performed.',
 'decision_summary':{'accepted_static_qa':['parvancorina/r001','glacial-horn/r002','eruptive-fissure/r003'],'revise':['banded-gneiss-outcrop/r003'],'evidence_complete':False,'approved_for_brief':False,'meaning':'The three ACCEPT results are limited independent static QA outcomes, not complete seven-stage evidence or publication approval.'},
 'producer_identity':{'worktree':str(W),'branch':'candidate/small-life-batch75-concept-20261020','immutable_commit':'64a896d4a62893f7d0f6c8276438fb95e424e518','base_main':'54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c','worktree_clean_pre_and_post':True,'handoff_path':str(W/'production/continuous-small-life-round30-20261020/work/batch-75/handoff.json'),'handoff_sha256':integrity['key_files'][0]['sha256'],'source_evidence_manifest_path':str(W/'production/continuous-small-life-round30-20261020/work/batch-75/source-evidence-manifest.json'),'source_evidence_manifest_sha256':integrity['key_files'][1]['sha256'],'source_manifest_entries_verified_against_worktree_and_git_tree':747,'all_747_producer_files_unchanged_pre_post_qa':integrity.get('unchanged_since_pre_snapshot',False),'original_inventory':integrity['source_inventory'],'prepost_hashes':'See integrity-pre.json and integrity-post.json; all 747 manifest entries, handoff and producer source manifest hashes stayed unchanged.'},
 'methods':['Personally inspected the actual consult-only source pixels and genuine concept pixels, then all 32 exact final 512x512 PNGs and all four lossless contact sheets.','Verified original and repair freezes, source rights_notes/non-incorporation statements, final GLB/active candidate brief/reference bindings, and render manifest PNG hashes.','Checked all producer evidence-manifest entries (747), current Git blobs, exact original inventory Git blob, and handoff hashes.','Fresh independent Three.js/Khronos parse of exact final GLBs; fresh Blender 4.3.2 saved-.blend reopen and full EXPORT collection re-export; independently parsed reopened export.','Verified two separate executed rebuild runs per final revision using run summaries, PIDs, return codes, request/result records and exact output hashes; cache-reuse events were not counted.','Fresh Blender BVH/edge review for visible interference corroboration. This is not treated as a universal static rejection gate.'],
 'chronology_and_provenance':{'all_original_freezes_completed_at':'2026-10-20T15:28:24.401039+00:00','provider_internal_timestamps':'unknown; not inferred','active_candidate_delivery_briefs_and_references_bound_before_actual_renders':True,'render_script_behavior':'Captures exact GLB/active brief/reference hashes before rendering, records them in the manifest, and aborts if they change during rendering. Candidate packaging-adapter times predate each render manifest; frame hashes/512px dimensions were reverified.','source_pixels':'Consult-only references are under /workspace/shared/batch75-consult-only, outside the Git worktree; no third-party pixels are incorporated.'},
 'assets':assets,
 'batch_limits':['GPU hardware stage not run.','Composed target scene stage not run.','No formal publication, user, or public approval asserted.','This QA result is based on frozen/local artifacts and is not a repository release gate.'],
 'evidence_paths':{'report_json':str(O/'report.json'),'report_markdown':str(O/'report.md'),'raw_manifest':str(O/'raw-manifest.json'),'integrity_pre':str(O/'integrity-pre.json'),'integrity_post':str(O/'integrity-post.json'),'fresh_parse':str(O/'fresh-parse.json'),'binding_evidence':str(O/'binding-evidence.json'),'rebuild_evidence':str(O/'rebuild-evidence.json'),'blender_reopen_dir':str(O/'blend-reopen'),'fresh_physical_glob':'/workspace/shared/lowpoly-round30-qa75/*.physical.json'}
}
json.dump(report,open(O/'report.json','w'),indent=2,sort_keys=True)
# Human-readable compact report.
lines=['# Batch 75 independent QA','',f'Created: {now}','', 'Decision: ACCEPT static QA only for Parvancorina r001, glacial horn r002, and eruptive fissure r003. REVISE banded gneiss r003. All four remain evidence-incomplete and not approved for brief/publication because GPU and composed-scene evidence are not run; approval remains separate.','', '## Identity and integrity', '', f'- Producer commit: `64a896d4a62893f7d0f6c8276438fb95e424e518` on `candidate/small-life-batch75-concept-20261020`; worktree clean.','- Original inventory Git blob verified at base `54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c`; SHA256 `b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c`.','- All 747 source-evidence-manifest files matched current bytes and Git blobs; the same snapshot remained unchanged after QA.','- All 32 exact final 512px images, four lossless contact sheets, source/concept pixels, rights ledgers and final-GLB/brief/reference bindings were checked. All source pixels remained outside the repository.','- Each final `.blend` reopened in Blender 4.3.2; exporting the full `EXPORT` collection recreated the exact final GLB byte-for-byte. Fresh Three.js 0.180.0 parse and Khronos validation had 0 errors and 0 warnings for every final GLB.','- Two actual separate semantic rebuild executions per final revision were verified from independent run summaries, PIDs, requests/results and output hashes; cached re-use records were not counted.','- Fresh saved-source BVH review found zero nonadjacent self-intersection pairs and zero boundary/nonmanifold edges for the four final surfaces. This was corroborative evidence, not a universal static rejection rule.','', '## Per-asset results','']
for a in assets:
 lines += [f"### {a['asset_id']} {a['revision']}: {a['independent_outcome']}",f"- GLB SHA256: `{a['glb_sha256']}`",f"- Counts: {a['budget_and_counts']['triangles']:,} triangles; {a['budget_and_counts']['source_authored_vertices']:,} source vertices; {a['budget_and_counts']['materials']} materials; {a['budget_and_counts']['primitives']} primitives; {a['budget_and_counts']['glb_bytes']:,} GLB bytes; 0 textures.",f"- Visual: {a['stage_states']['visual']['details']}",f"- Factual limits: {a['stage_states']['factual']['details']}","- Stages: technical PASS; factual PASS; specification PASS; runtime_parse PASS; gpu NOT RUN; scene NOT RUN.",""]
lines += ['## Artifact paths','',f"- Machine report: `{O/'report.json'}`",f"- Raw manifest: `{O/'raw-manifest.json'}`",f"- Integrity pre/post snapshots: `{O/'integrity-pre.json'}` and `{O/'integrity-post.json'}`",f"- Fresh GLB checks: `{O/'fresh-parse.json'}`",f"- Blender reopen/export evidence: `{O/'blend-reopen'}`",f"- Raw rebuild evidence: `{O/'rebuild-evidence.json'}`",'']
(O/'report.md').write_text('\n'.join(lines))
print('wrote report.json and report.md; assets:',[(a['asset_id'],a['independent_outcome']) for a in assets])

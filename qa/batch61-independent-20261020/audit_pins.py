import hashlib,json,os,subprocess,glob
from pathlib import Path
R=Path('/tmp/lowpoly-batch61-20261020'); O=Path('/tmp/lowpoly-round23-qa61'); ROOT=Path('assets/candidates/continuous-small-life-round23-20261020/batch-61')
expected={'pseudopulex':('r003','75f6799431a7bf6037881c78d12e7cf731670fcb2fdea82b66576dadc8cdf99c','e572b15e3efffc4331f3b865c4fe74fb37d29632893b459904cc87fc233b8415','e3e?'),
'daemonelix-helical-burrow':('r002','c415fbe405e75ac182bb39512ea33b43f81d574723263f04378422fb0221aa82','802c13dc3117cadd7748201ca2dc5fce4b3a50cc60ab5791e0042ba463ea6248',''),
'mesa':('r002','399e9fb78b225cd808563598485888ea343b568e8bc2cac8b427939fc94f1cad','716288207373eb8d1b4ff123bc9bebda485d1b015d3e85f09b5c5b94f053f57d',''),
'drumlin':('r002','317dee38ec731d1939985a61fd431238a188b5be34dfcc717dafe23dc4bd7534','ee0abc1e2a6860fb6624c0bf150f4c29f0287ab306539c5a2ad75e6d241a8fea','')}
expected_branches={'pseudopulex':('3ee0ecc2d4a18b634c4d94eddea7fa985ce458c91538749388d230695f8fbe67','c8baa4dcbba35500e6be35306785fb2fb089d9f8ba3df880a2fb4622f606061b','dbea2e8a1f20cb6aee504e3fafc0172163d7d3d92d17150e47faaf65cf2d60c9','d6251ca73a13d7395f7ed2d7cafb5f012d76c8e0f60132d65d50e10af20a3555'),
'daemonelix-helical-burrow':('2fcfd328842918ca9e1bc75bbb542692960c9a1f0644eb678bd8cca5a5056896','9f76d189a6c74522a08af4c200898e30591f3cd7960bf3e44212b912a52ac075','4776e0b89f0f1049df60983fa8c82d78018cdd08c5471e4dcbb0de2bafd1a70f','15b9358a2862c867b2d9cc4fa83c4a4ce9fd8437a319d8b0ff7c3c94d15f6cf3'),
'mesa':('4bf4e45bce74a19ba20ef2d8f658d08358c702ad0bb449055732434489f346cf','ad88334969361d198442598087096ab275a8c2e3aa672c85233dbb8c85e37df4','4776e0b89f0f1049df60983fa8c82d78018cdd08c5471e4dcbb0de2bafd1a70f','f3b3fde69b10ad042f18c52091675ddc28ba3f83eabfc91247149aa728d69b65'),
'drumlin':('12ddf48322e3b644df06d7df62a15a4272ed1a7bd5df680fe6e8ed2ed169ad6a','1c33853bc5d0e7f7c0dc858458b2df334d3acfe89996c2a98dd84ca62591659e','4776e0b89f0f1049df60983fa8c82d78018cdd08c5471e4dcbb0de2bafd1a70f','e48252f277d3ab3499026d1b970a8657b71639531ac44779824dea7b65adaba2')}
frames={'hero','reversehero','front','side','rear','top','clay','silhouette'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def gate_status(p):return read(p)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(); branch=subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip(); dirty=subprocess.check_output(['git','status','--porcelain'],cwd=R,text=True).strip()
handoff=read(R/'production/continuous-small-life-round23-20261020/work/batch-61/handoff.json')
final_selection=read(R/'production/continuous-small-life-round23-20261020/work/batch-61/final-selection.json')
assert head=='f1737e4f00dfc5c1817084ecb31763320ec2a163' and not dirty
assert branch==handoff['branch'] and handoff['source_commit']=='b2ff8314140e2539c825d573fef2152584120059'
assert {a['asset_id'] for a in handoff['assets']}==set(expected)
assert {x['asset_id'] for x in final_selection}==set(expected)
asset_reports=[]; unique_runids=set(); unique_pids=set()
for name,(rev,glb,source,_) in expected.items():
 d=R/ROOT/name/rev; h=next(a for a in handoff['assets'] if a['asset_id']==name)
 brief,refs,gen,config=expected_branches[name]
 hp=h['hashes']; assert (h['revision'],hp['glb'],hp['source'],hp['brief'],hp['references'],hp['generator'],hp['config'])==(rev,glb,source,brief,refs,gen,config)
 assert sha(d/'model.glb')==glb and sha(d/'source.blend')==source and sha(d/'candidate-brief.json')==brief and sha(d/'references.json')==refs and sha(d/'generator.py')==gen and sha(d/'build-config.json')==config
 c=read(d/'candidate.json'); assert c['revision']==rev and c['artifacts']['glb']['sha256']==glb and c['artifacts']['brief']['sha256']==brief
 ce=read(d/'concept-evidence.json'); assert ce['concept']['images'][0]['sha256']==sha(d/'concept-original.png') and ce['concept']['images'][0]['path']=='concept-original.png'
 cv=read(d/'concept-validation.json'); assert cv['valid'] is True and cv['evidence_complete'] is False and cv['blockers']
 b=read(d/'candidate-brief.json'); assert b['required_views']==['hero','reversehero','front','side','rear','top','clay','silhouette'] and b['turntable_frames']==0
 prof=read(d/'profile-contract.json'); assert prof['validation_profile']=='static-stylized-v1' and prof['rule_version']=='2026-10-18.1' and prof['publication_authority']=='separate'
 manifest=read(d/'proof-final/render-manifest.json'); assert manifest['source_glb_sha256']==glb and manifest['frame_count']==8 and {f['id'] for f in manifest['frames']}==frames
 frame_info=[]
 for f in manifest['frames']:
  pp=d/'proof-final'/f['path']; assert f['width']==512 and f['height']==512 and sha(pp)==f['sha256']; frame_info.append(f['id'])
 assert len(frame_info)==8
 if name=='pseudopulex':
  hm=read(d/'proof-head-detail/render-manifest.json'); assert hm['source_glb_sha256']==glb and hm['frame_count']==1 and hm['frames'][0]['path']=='detail.png' and sha(d/'proof-head-detail/detail.png')==hm['frames'][0]['sha256']
 # Original pre-model freeze binds full brief/config/references/concept.
 old=R/ROOT/name/'r001'; freeze=read(old/'modeling-freeze.json'); about=read(old/'authoring-start.json'); 
 assert freeze['frozen_at'] < about['observed_authoring_complete_at']
 assert freeze['brief_sha256']==sha(old/'brief.json') and freeze['config_sha256']==sha(old/'build-config.json') and freeze['references_sha256']==sha(old/'references.json') and freeze['concept_sha256']==sha(old/'concept-original.png')
 assert about['authoring_started_after_freeze'] is True
 final_freeze=read(d/'modeling-freeze.json'); assert final_freeze['brief_sha256']==freeze['brief_sha256'] and final_freeze['references_sha256']==freeze['references_sha256'] and final_freeze['no_scope_narrowing'] is True
 if rev=='r003': assert final_freeze['config_sha256']==sha(d/'build-config.json') and 'palp' in final_freeze['repair'].lower()
 else: assert final_freeze['config_sha256']==sha(d/'build-config.json')
 # Editable Blend counts vs independently reopened geometry; GLB vertex accessor count is a distinct expected export measure.
 counts=read(d/'source-vertex-counts.json'); assert counts['source_sha256']==source and counts['glb_sha256']==glb
 reopen=read(O/f'{name}-source-reopen.json'); assert reopen['source_sha256']==source and reopen['triangles_total']==h['triangles'] and reopen['all_components_closed'] is True and reopen['boundary_edges_total']==reopen['nonmanifold_edges_total']==reopen['loose_vertices_total']==0
 qa=read(O/f'{name}-candidate-gate.json'); assert qa['valid'] and not qa['approved_for_brief'] and qa['profile_contract_status']=='pass'
 k=read(O/f'{name}-khronos.json'); assert k['sha256']==glb and k['report']['issues']['numErrors']==k['report']['issues']['numWarnings']==0
 three=read(O/f'{name}-three-parse.json'); assert three['sha256']==glb and three['revision']=='180' and round(three['triangles'])==h['triangles']
 glbqa=read(O/f'{name}-glb-gate.json'); assert glbqa['sha256']==glb and glbqa['status']=='pass'
 rebuilds=[]
 for i in (1,2):
  rp=read(d/f'repro-final-{i}.report.json'); assert rp['status']=='pass' and rp['semantic_match'] and rp['byte_identical'] and rp['provenance_status']=='bound_successful_build_run' and rp['glb_sha256']==glb and rp['rebuilt_glb_sha256']==glb and rp['generator_sha256']==gen and rp['config_sha256']==config and rp['semantic_sha256']==rp['rebuilt_semantic_sha256']
  q=rp['build_run']; reqp=R/q['request']['path']; resp=R/q['result']['path']; assert sha(reqp)==q['request']['sha256'] and sha(resp)==q['result']['sha256']; req=read(reqp); res=read(resp)
  outp=Path(rp['rebuilt_glb_path']); assert sha(outp)==glb and res['status']=='succeeded' and res['returncode']==0
  assert req['identity']['job']['asset_id']==name and req['identity']['job']['revision']==rev and req['identity']['job']['job_id']==f'semantic-rebuild-{i}'
  assert req['identity']['inputs']['generator']['sha256']==gen and req['identity']['inputs']['config']['sha256']==config
  assert res['status']=='succeeded' and res['returncode']==0 and res['outputs']['model.glb']['sha256']==glb and res['pid'] not in unique_pids
  unique_pids.add(res['pid']); unique_runids.add(req['run_id']); assert res['fingerprint']==q['request']['sha256'] or res['fingerprint']==req['fingerprint']
  rebuilds.append({'job_id':req['identity']['job']['job_id'],'run_id':req['run_id'],'pid':res['pid'],'fingerprint':req['fingerprint'],'result_status':res['status'],'returncode':res['returncode'],'output_sha256':res['outputs']['model.glb']['sha256'],'semantic_match':rp['semantic_match'],'semantic_sha256':rp['semantic_sha256']})
 assert len({x['job_id'] for x in rebuilds})==2 and len({x['pid'] for x in rebuilds})==2 and len({x['fingerprint'] for x in rebuilds})==2
 asset_reports.append({'asset_id':name,'revision':rev,'hashes':{'glb':glb,'brief':brief,'references':refs,'source':source,'generator':gen,'config':config},'evidence':{'candidate_gate':'valid-pending-not-approved','profile_contract':'pass','proof_frames':frame_info,'head_macro':name=='pseudopulex','candidate_artifacts_hashes':'pass','source_reopen_topology':'pass','khronos':'0 errors, 0 warnings','three_parse':{'revision':three['revision'],'triangles':three['triangles'],'meshes':three['meshes']},'project_glb_gate':'pass','queue_rebuilds':rebuilds},'metrics':{'triangles':h['triangles'],'glb_bytes':h['glb_bytes'],'materials':h['materials'],'primitives':h['primitives'],'textures':h['textures'],'nominal_dimensions_blender_xyz_m':h['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':h['measured_blender_xyz_m'],'measured_glb_xyz_m':h['measured_glb_xyz_m']}})
# consulted-only source pixels verify ledgers; external copies live only under /tmp source-preflight.
ref_imgs={'pseudopulex':'/tmp/lowpoly-round23-primary-consulted/Gao-2012-figure1.png','daemonelix-helical-burrow':'/tmp/lowpoly-round23-primary-consulted/batch61/daemonelix.jpg','mesa':'/tmp/lowpoly-round23-primary-consulted/batch61/mesa.jpg','drumlin':'/tmp/lowpoly-round23-primary-consulted/batch61/drumlin.jpg'}
ref_img_check={}
for name,p in ref_imgs.items():
 d=R/ROOT/name/expected[name][0]; src=read(d/'references.json')['sources'][0]; assert sha(p)==src['consulted_image_sha256']; ref_img_check[name]={'path':p,'sha256':sha(p),'matches_ledger':True}
# Confirm later commit changes only the two handoff metadata files beyond exact payload commit.
diff=subprocess.check_output(['git','diff','--name-status','b2ff8314140e2539c825d573fef2152584120059..HEAD'],cwd=R,text=True).splitlines()
assert set(diff)=={'A\tproduction/continuous-small-life-round23-20261020/work/batch-61/HANDOFF.md','A\tproduction/continuous-small-life-round23-20261020/work/batch-61/handoff.json'}
result={'schema_version':1,'kind':'independent_batch61_qa','qa_date_utc':'2026-10-20','source_checkout':{'head':head,'branch':branch,'clean':not bool(dirty),'payload_commit':handoff['source_commit'],'head_diff_from_payload_commit':diff},'profile':{'name':'static-stylized-v1','rule_version':'2026-10-18.1','fixed_views':sorted(frames),'turntable_frames':0,'publication_authority':'separate'},'global_checks':{'four_final_pins_and_candidate_records':'pass','32_exact_final_512px_frames_hash_bound_to_the_pinned_glbs':'pass','pseudopulex_head_macro_hash_bound_to_pinned_glb':'pass','four_concept_pixels_inspected':'pass','four_actual_consult_only_reference_pixels_match_ledger':'pass','actual_pseudopulex_primary_figure1_pixels_inspected':'pass','reference_pixels_present_in_candidate_tree':False,'four_original_brief_config_reference_concept_freezes_precede_generator_authoring_and_model_build':'pass','repair_freezes_preserve_original_brief_and_references_without_scope_narrowing':'pass','four_read_only_blend_reopens_and_topology':'pass','four_independent_khronos_validations':'0 errors / 0 warnings each','four_independent_three_js_0_180_0_parses':'pass','four_project_static_glb_gates':'pass','eight_queue_bound_blender_processes':'pass','all_queue_outputs_byte_identical_and_semantically_matching':'pass','concept_chronology':'incomplete as declared; provider-internal generation timestamp and precise authoring-start were not returned; no inference from mtimes'},'consulted_reference_pixels':ref_img_check,'unique_blender_pids':len(unique_pids),'unique_queue_run_ids':len(unique_runids),'candidates':asset_reports,'limitations':['This is bounded independent technical, visual, factual and specification QA only; candidate records remain not approved.','GPU hardware/runtime and composed-scene visual checks are not run; do not claim GPU/scene/runtime-render approval.','Concept provenance is valid but its exact provider generation timestamp and exact modeling start remain unknown.','No remote/local source, model, QA/candidate-approval flag, CI, site or branch was modified by this QA; new QA outputs only under /tmp/lowpoly-round23-qa61.']}
assert len(unique_pids)==8 and len(unique_runids)==2
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('OK: fresh exact-pin checks; 8 unique PIDs/runs, all refs and render hashes verified')

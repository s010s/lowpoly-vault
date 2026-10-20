import hashlib,json,pathlib,subprocess,sys,datetime
from PIL import Image
R=pathlib.Path('/tmp/lowpoly-batch61-20261020'); O=pathlib.Path('/tmp/lowpoly-round23-qa61-proof-v003')
BASE='896563bfcbc70f160edf29b84dacfc824536be6a'; HEAD='e2ed7b0b13a850f2663a6701fa28edc6ffef6951'; PAYLOAD='439ef387e3acd4e2413bcd2a9f001feed6165d1c'; INITIAL='013e48e352a2eb4b34c5770862eec5bbbf7bea9a'
PROD='production/continuous-small-life-round23-20261020/work/batch-61/render-proof-v003'
AR='assets/candidates/continuous-small-life-round23-20261020/batch-61'
ASSETS={
'daemonelix-helical-burrow':{'brief':'721ad77bfd1600cadda06b178a571f439c957c00f19ba1263d307f9e40449ac4','oldbrief':'2fcfd328842918ca9e1bc75bbb542692960c9a1f0644eb678bd8cca5a5056896','glb':'c415fbe405e75ac182bb39512ea33b43f81d574723263f04378422fb0221aa82','source':'802c13dc3117cadd7748201ca2dc5fce4b3a50cc60ab5791e0042ba463ea6248','refs':'9f76d189a6c74522a08af4c200898e30591f3cd7960bf3e44212b912a52ac075','run_pid':33},
'mesa':{'brief':'63de5d1f262ba10b471dba0587139685a141ca2105c5efdf77c8eee5a69798cd','oldbrief':'4bf4e45bce74a19ba20ef2d8f658d08358c702ad0bb449055732434489f346cf','glb':'399e9fb78b225cd808563598485888ea343b568e8bc2cac8b427939fc94f1cad','source':'716288207373eb8d1b4ff123bc9bebda485d1b015d3e85f09b5c5b94f053f57d','refs':'ad88334969361d198442598087096ab275a8c2e3aa672c85233dbb8c85e37df4','run_pid':63},
'drumlin':{'brief':'106e2bbd77cd9e7c69be89311af1aebb4dad808b1e25a40da0a98e3fded3da43','oldbrief':'12ddf48322e3b644df06d7df62a15a4272ed1a7bd5df680fe6e8ed2ed169ad6a','glb':'317dee38ec731d1939985a61fd431238a188b5be34dfcc717dafe23dc4bd7534','source':'ee0abc1e2a6860fb6624c0bf150f4c29f0287ab306539c5a2ad75e6d241a8fea','refs':'1c33853bc5d0e7f7c0dc858458b2df334d3acfe89996c2a98dd84ca62591659e','run_pid':93}}
def sha(b):return hashlib.sha256(b).hexdigest()
def hfile(p):return sha(p.read_bytes())
def git(*args):return subprocess.check_output(['git','-C',str(R),*args],stderr=subprocess.STDOUT).decode().strip()
def blob(rev,path):return subprocess.check_output(['git','-C',str(R),'show',f'{rev}:{path}'])
def jpath(path):return json.loads((R/path).read_text())
def jblob(rev,path):return json.loads(blob(rev,path))
def parse_time(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
assert git('rev-parse','HEAD')==HEAD
assert git('rev-parse','HEAD^')==PAYLOAD
assert not git('status','--porcelain')
changes=git('diff','--name-status',f'{BASE}..{HEAD}').splitlines()
assert len(changes)==65 and all(x.startswith('A\t') for x in changes), (len(changes),changes[:5])
handoff_path=f'{PROD}/handoff-proof-v003.json'; hbytes=blob(HEAD,handoff_path); handoff=json.loads(hbytes)
assert handoff['baseline_immutable_commit']==BASE and handoff['source_payload_commit']==PAYLOAD and handoff['render_payload_commit']==INITIAL
assert handoff['approval']=='Independent differential acceptance still pending; no maker approval or GPU/scene/hardware assertion'
# all 488 preserved prior-file hashes match both immutable baseline and new commit
pres_path=f'{PROD}/original-byte-preservation-v003.json'; pres=json.loads(blob(HEAD,pres_path)); prior=pres['files']; assert pres['baseline_commit']==BASE and pres['all_original_bytes_match_commit'] is True
pres_fail=[]
for p,expected in prior.items():
 if sha(blob(BASE,p))!=expected or sha(blob(HEAD,p))!=expected:pres_fail.append(p)
assert len(prior)==488 and not pres_fail,(len(prior),pres_fail[:10])
assert pres['pseudopulex_unchanged'] is True and pres['old_v001_v002_proofs_and_all_archived_qa_unchanged'] is True
run_pids=[]; run_results=[]; frame_results=[]; all_pixel_equal=True
expected_views=['hero','reversehero','front','side','rear','top','clay','silhouette']
for name,x in ASSETS.items():
 p=f'{AR}/{name}/r002'; pp=R/p
 assert sha(blob(BASE,f'{p}/model.glb'))==x['glb']==sha(blob(HEAD,f'{p}/model.glb'))
 assert sha(blob(BASE,f'{p}/source.blend'))==x['source']==sha(blob(HEAD,f'{p}/source.blend'))
 runpath=f'{PROD}/{name}-actual-run.json'; run=json.loads(blob(HEAD,runpath))
 manifestpath=f'{p}/proof-scale-v003/render-manifest.json'; mp=pp/'proof-scale-v003/render-manifest.json'; manifest=json.loads(blob(HEAD,manifestpath))
 # Inputs and commands independently pin exact corrected brief / GLB / reference closure.
 assert run['kind']=='actual-fresh-glb-render-run' and run['asset_id']==name and run['geometry_revision']=='r002' and run['metadata_proof_revision']=='v003'
 assert run['returncode']==0 and run['approval']=='not granted'
 assert run['blender_process_pid']==x['run_pid']; run_pids.append(run['blender_process_pid'])
 assert run['binary']['path']=='/usr/bin/blender' and hfile(pathlib.Path('/usr/bin/blender'))==run['binary']['sha256']
 cmd=run['command']; assert cmd[0]=='/usr/bin/blender' and '-b' in cmd and '--factory-startup' in cmd and '--disable-autoexec' in cmd
 for key,expected in [('glb',x['glb']),('corrected_brief',x['brief']),('references',x['refs'])]:
  inp=run['inputs'][key]; assert inp['sha256']==expected and sha(blob(HEAD,inp['path']))==expected and sha(blob(BASE,inp['path']))==expected
 # Ensure actual argv selected corrected brief and correct GLB, references, output, 8 fixed views at 512px.
 cmdstr=' '.join(cmd)
 assert f'{pp}/model.glb' in cmdstr and f'{pp}/candidate-brief-scale-v002.json' in cmdstr and f'{pp}/references.json' in cmdstr
 assert f'{pp}/proof-scale-v003' in cmdstr and '--resolution 512' in cmdstr and '--turntable-frames 0' in cmdstr
 assert ','.join(expected_views) in cmdstr
 for k in ['renderer_script','helper','audit_helper']:
  inp=run['inputs'][k]; assert sha(blob(HEAD,inp['path']))==inp['sha256']
 started=parse_time(run['started_at']); ended=parse_time(run['ended_at']); assert ended>started and 0<run['wall_seconds']<60
 logp=run['stdout']['path']; log_bytes=blob(HEAD,logp); assert sha(log_bytes)==run['stdout']['sha256']
 log=log_bytes.decode(errors='replace')
 assert 'Blender 4.3.2' in log and 'glTF import finished' in log and 'Blender quit' in log
 for v in expected_views: assert f'/proof-scale-v003/{v}.png' in log, (name,v)
 # fresh render records and subject/timing
 assert sha(blob(HEAD,manifestpath))==run['new_manifest']['sha256']
 assert manifest['stage']=='visual' and manifest['kind']=='render_manifest' and manifest['target_renderer']=='blender-cycles-cpu'
 assert manifest['subject']=={'revision':'r002','glb_sha256':x['glb'],'brief_sha256':x['brief'],'references_sha256':x['refs']}
 assert manifest['source_glb_sha256']==x['glb'] and manifest['source_unchanged'] is True
 assert parse_time(run['started_at']) <= parse_time(manifest['created_at']) <= parse_time(run['ended_at'])
 assert manifest['created_at']!=json.loads(blob(BASE,f'{p}/proof-final/render-manifest.json'))['created_at']
 assert manifest['frame_count']==8 and (manifest['width'],manifest['height'])==(512,512)
 assert manifest['visual_review']=='pending' and manifest['runtime_qa']=='not_run'
 config_rel=f'{p}/proof-scale-v003/{manifest["render_config"]["path"]}'
 assert hfile(R/config_rel)==manifest['config_sha256']==manifest['render_config']['sha256']
 config=json.loads((R/config_rel).read_text())
 assert config['source_glb_sha256']==x['glb'] if 'source_glb_sha256' in config else True
 frame_ids=[f['id'] for f in manifest['frames']]; assert frame_ids==expected_views
 # check exact PNG file hash/size and independently decode/compare to original v001 output (no byte-copy claim)
 comp_path=f'{p}/proof-scale-v003/decoded-pixel-comparison-v003.json'; comp=json.loads(blob(HEAD,comp_path))
 assert comp['all_eight_decoded_rgba_identical'] is True
 assert comp['actual_runner']['sha256']==sha(blob(HEAD,runpath))
 assert comp['new_manifest']['sha256']==sha(blob(HEAD,manifestpath))
 byname={f['frame']:f for f in comp['frames']}
 assert set(byname)==set(expected_views)
 for frame in manifest['frames']:
  v=frame['id']; new_rel=f'{p}/proof-scale-v003/{frame["path"]}'; old_rel=f'{p}/proof-final/{frame["path"]}'
  nb=blob(HEAD,new_rel); ob=blob(BASE,old_rel)
  assert sha(nb)==frame['sha256'] and len(nb)==frame['byte_length']
  oldm=jblob(BASE,f'{p}/proof-final/render-manifest.json')
  old_frame=next(z for z in oldm['frames'] if z['id']==v)
  assert sha(ob)==old_frame['sha256']
  new_im=Image.open(__import__('io').BytesIO(nb)).convert('RGBA')
  old_im=Image.open(__import__('io').BytesIO(ob)).convert('RGBA')
  assert new_im.size==old_im.size==(512,512)
  pixel_equal=new_im.tobytes()==old_im.tobytes()
  all_pixel_equal &= pixel_equal
  assert pixel_equal and byname[v]['decoded_rgba_identical'] is True
  assert byname[v]['old_png']['sha256']==sha(ob) and byname[v]['new_png']['sha256']==sha(nb)
  assert byname[v]['png_bytes_identical']==(sha(ob)==sha(nb))
  frame_results.append({'asset_id':name,'frame':v,'old_png_sha256':sha(ob),'new_png_sha256':sha(nb),'decoded_rgba_identical':pixel_equal,'new_png_bytes':len(nb),'render_wall_seconds':frame['wall_seconds']})
 # Candidate record and profile/hash bindings, status retained.
 canpath=f'{p}/candidate-proof-v003.json'; cp=blob(HEAD,canpath); cand=json.loads(cp)
 validationpath=f'{p}/candidate-validation-proof-v003.json'; validation=json.loads(blob(HEAD,validationpath))
 profilepath=f'{p}/profile-contract-proof-v003.json'; profile=json.loads(blob(HEAD,profilepath))
 oldcand=json.loads(blob(BASE,f'{p}/candidate-scale-v002.json'))
 assert cand['asset_id']==name and cand['revision']=='r002' and cand['render_proof_revision']=='fresh-fixed8-v003'
 assert cand['artifacts']['brief']['sha256']==x['brief'] and cand['artifacts']['brief']['path'].endswith('candidate-brief-scale-v002.json')
 assert cand['artifacts']['glb']['sha256']==x['glb'] and cand['artifacts']['source']['sha256']==x['source'] and cand['artifacts']['references']['sha256']==x['refs']
 assert cand['artifacts']['generator']['sha256']==oldcand['artifacts']['generator']['sha256']
 assert cand['artifacts']['config']['sha256']==oldcand['artifacts']['config']['sha256']
 assert [z['status'] for z in cand['stages'].values()]==[z['status'] for z in oldcand['stages'].values()]
 assert cand['approval']==oldcand['approval'] and cand['approval']=={'status':'pending'}
 assert cand['metadata_predecessor']['path']==f'{p}/candidate-scale-v002.json' and cand['metadata_predecessor']['sha256']==sha(blob(BASE,f'{p}/candidate-scale-v002.json'))
 assert cand['metadata_correction']['sha256']==oldcand['metadata_correction']['sha256'] and cand['metadata_correction']['path']==oldcand['metadata_correction']['path']
 assert cand['evidence'][0]['kind']=='render_manifest' and cand['evidence'][0]['path']==manifestpath and cand['evidence'][0]['sha256']==sha(blob(HEAD,manifestpath))
 expectedsub={'revision':'r002','glb_sha256':x['glb'],'brief_sha256':x['brief'],'references_sha256':x['refs']}
 assert cand['evidence'][0]['subject']==expectedsub
 assert validation['valid'] is True and validation['approved_for_brief'] is False and validation['approval_status']=='pending'
 assert validation['profile_contract_status']=='pass' and validation['subject']==expectedsub
 assert validation['profile_contract']['path']==profilepath and validation['profile_contract']['sha256']==sha(blob(HEAD,profilepath))
 assert profile['validation_profile']=='static-stylized-v1' and profile['rule_version']=='2026-10-18.1'
 assert profile['candidate']['path']==canpath and profile['candidate']['sha256']==sha(cp) and profile['publication_authority']=='separate'
 run_results.append({'asset_id':name,'independent_outcome':'ACCEPT_BOUNDED','render_pid':run['blender_process_pid'],'runner_pid':run['runner_pid'],'started_at':run['started_at'],'ended_at':run['ended_at'],'seconds':run['wall_seconds'],'brief_sha256':x['brief'],'glb_sha256':x['glb'],'manifest_sha256':sha(blob(HEAD,manifestpath)),'candidate_sha256':sha(cp),'candidate_valid':validation['valid'],'approved_for_brief':validation['approved_for_brief'],'stage_statuses':{k:v['status'] for k,v in cand['stages'].items()},'log_sha256':run['stdout']['sha256']})
assert len(set(run_pids))==3 and all_pixel_equal and len(frame_results)==24
# all fresh render started/ended intervals are sequential/non-overlapping
ints=sorted((parse_time(x['started_at']),parse_time(x['ended_at'])) for x in run_results)
assert all(ints[i][1] <= ints[i+1][0] for i in range(len(ints)-1))
# runner summary claims against our checks
verification=json.loads(blob(HEAD,f'{PROD}/verification-v003.json'))
assert verification['baseline_commit']==BASE and verification['fresh_render_inputs_and_subjects_verified'] is True
assert verification['all24_decoded_rgba_identical_to_previous_comparable_pixels'] is True
assert verification['all_render_process_pids']==[33,63,93]
assert verification['all_approval_and_stage_flags_unchanged'] is True and verification['geometry_rebuilds']==0 and verification['pseudopulex_renders']==0 and verification['new_imagegen_calls']==0 and verification['pushes']==0
# final selection: Pseudopulex unchanged, three corrected records point to v003 renders.
selection=json.loads(blob(HEAD,f'{PROD}/final-selection-proof-v003.json'))
assert len(selection)==3 and {s['asset_id'] for s in selection}==set(ASSETS)
for n in ASSETS:
 s=next(s for s in selection if s['asset_id']==n)
 assert s['candidate_record'].endswith('/candidate-proof-v003.json') and s['manifest']['path'].endswith('/proof-scale-v003/render-manifest.json')
# output budget: compare maker-recorded totals to exact new binaries (not including manifests/logs outside asset output dirs)
new_png_bytes=sum(x['new_png_bytes'] for x in frame_results)
new_contact_bytes=sum((R/f'{AR}/{n}/r002/proof-scale-v003/contact-sheet-v003.png').stat().st_size for n in ASSETS)
output_budget=json.loads(blob(HEAD,f'{PROD}/output-budget-v003.json'))
# serialize verified result
result={'schema_version':1,'kind':'focused_batch61_render_proof_differential','date_utc':'2026-10-20','outcome':'ACCEPT_BOUNDED for corrected Daemonelix/mesa/drumlin v003 delivery records only; original geometry, factual, visual and technical findings carry forward because exact GLB/Blend bytes match. This is not formal approval.','pins':{'baseline_commit':BASE,'initial_render_commit':INITIAL,'render_payload_commit':PAYLOAD,'final_head':HEAD,'branch':git('branch','--show-current'),'clean_worktree':True,'additions':len(changes),'modified_originals':0,'deleted_originals':0},'preservation':{'inventory_files':len(prior),'all_hashes_match_baseline_and_head':True,'pseudopulex_exact_pins_unchanged':pres['pseudopulex_unchanged'],'old_v001_v002_and_archived_qa_unchanged':pres['old_v001_v002_proofs_and_all_archived_qa_unchanged']},'runner_evidence':{'unique_blender_pids':run_pids,'runner_parent_pids':sorted(set(x['runner_pid'] for x in run_results)),'all_returncodes_zero':True,'actual_input_binding_verified':True,'logs_match_record_hashes':True,'blender_binary_hash_verified':True,'three_sequential_nonoverlapping_real_runs':True,'fixed8_512px_per_asset':True,'fresh_subject_matches_corrected_brief_glb_refs':True,'timing':run_results},'pixel_evidence':{'new_frames':len(frame_results),'all_24_decoded_rgba_identical_to_old_reviewed_pixels':all_pixel_equal,'new_png_bytes_identical_to_old':False,'new_png_total_bytes':new_png_bytes,'contact_sheet_total_bytes':new_contact_bytes,'fresh_output_budget_record':output_budget,'per_frame':frame_results},'candidate_bindings':{'candidate_profile_and_validation_hash_bindings_pass':True,'candidate_integrity_gate_valid':True,'approved_for_brief':False,'stage_statuses':'all unknown as before','publication_authority':'separate','records':run_results},'limitations':['No full four-model QA repeated; earlier geometry/factual/visual/technical findings retained only because exact GLB/Blend pins match prior independent review.','Fresh rendering was Blender Cycles CPU only; no GPU/hardware or composed-scene check is claimed.','No new geometry/source rebuild, ImageGen, Pseudopulex render, validator/CI/site change, approval, push or publication.'],'handoff_sha256':sha(hbytes),'verification_sha256':sha(blob(HEAD,f'{PROD}/verification-v003.json')),'original_byte_preservation_manifest_sha256':sha(blob(HEAD,pres_path)),'reports':{'markdown':str(O/'independent-differential-qa.md'),'checks_log':str(O/'checks.log')}}
(O/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
lines=[f'HEAD={HEAD}',f'PARENT_RENDER_PAYLOAD={PAYLOAD}',f'BASELINE={BASE}',f'GIT_STATUS=clean',f'DIFF_ADDITIONS={len(changes)} MODIFIED=0 DELETED=0',f'PRESERVED_BASELINE_FILE_HASHES={len(prior)} checked, zero mismatch',f'RUN_PIDS={run_pids}',f'RENDER_COUNT={len(run_results)}',f'PNG_FRAME_COUNT={len(frame_results)}',f'RGBA_EQUAL_FRAMES={sum(1 for f in frame_results if f["decoded_rgba_identical"])}',f'FRESH_INPUT_SUBJECT_BINDINGS=pass',f'NEW_CANDIDATE_PROFILE_VALIDATION_BINDINGS=pass',f'APPROVAL_STAGES_REMAIN_UNCHANGED=pass',f'NEW_PNG_BYTES={new_png_bytes}',f'CONTACT_SHEET_BYTES={new_contact_bytes}',f'OUTPUT_BUDGET_RECORD={json.dumps(output_budget,sort_keys=True)}']
(O/'checks.log').write_text('\n'.join(lines)+'\n')
print(json.dumps({'outcome':result['outcome'],'pids':run_pids,'preserved_files':len(prior),'new_frames':len(frame_results),'rgba_identical':all_pixel_equal,'bytes_new_pngs':new_png_bytes,'contact_sheets':new_contact_bytes},indent=2))

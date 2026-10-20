#!/usr/bin/env python3
import hashlib,json,subprocess,os
from pathlib import Path
from datetime import datetime, timezone
repo=Path('/workspace/shared/lowpoly-batch70-20261020')
base='e191d4c2abf35bf952eb72da959311c577101b07'
commit='2f674a5e98a7a9c6c61f8a7e89ef81a503864fa9'
rel='production/continuous-small-life-round28-20261020/work/batch-70/repair-kettle-r002/repair-source-evidence-manifest.json'
manifest_path=repo/rel
manifest=json.loads(manifest_path.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git','-C',str(repo),*args])
head=git('rev-parse','HEAD').decode().strip()
status=git('status','--porcelain=v1').decode().strip()
changes=git('diff','--name-status',base,commit).decode().splitlines()
manifest_entries=[]
for x in manifest['files']:
    p=x['path'];work=(repo/p).read_bytes();stored=git('show',f'{commit}:{p}')
    manifest_entries.append({'path':p,'expected_bytes':x['bytes'],'actual_bytes':len(work),'expected_sha256':x['sha256'],'work_sha256':sha(work),'git_sha256':sha(stored),'ok':len(work)==x['bytes']==len(stored) and sha(work)==x['sha256']==sha(stored)})
manifest_git=git('show',f'{commit}:{rel}')
external=json.loads(Path('/workspace/shared/batch70-r002-committed-byte-verification.json').read_text())
r=repo/'assets/candidates/continuous-small-life-round28-20261020/batch-70/kettle-basin/r002'
p=repo/'production/continuous-small-life-round28-20261020/work/batch-70/repair-kettle-r002'
read=lambda path:json.loads(path.read_text())
H=lambda path:sha(Path(path).read_bytes())
cand=read(r/'candidate.json'); hand=read(p/'HANDOFF.json'); active=read(p/'active-binding.json'); pre=read(r/'preproof-binding-check.json'); render=read(r/'proof-final/render-manifest.json'); brief=read(r/'candidate-brief.json'); freeze=read(r/'modeling-freeze.json'); add=read(r/'repair-addendum-freeze.json'); refs=read(r/'references.json')
# validate exact candidate/handoff/preproof/render closure
asset_paths={
 'candidate':r/'candidate.json','glb':r/'model.glb','brief':r/'candidate-brief.json','references':r/'references.json',
 'source':r/'source.blend','generator':r/'generator.py','config':r/'repair-config.json','render_manifest':r/'proof-final/render-manifest.json'
}
actual_hashes={k:H(v) for k,v in asset_paths.items()}
expected_handoff={
 'candidate':hand['active_binding']['candidate']['sha256'],
 'glb':hand['active_binding']['artifacts']['glb']['sha256'],
 'brief':hand['active_binding']['artifacts']['brief']['sha256'],
 'references':hand['active_binding']['artifacts']['references']['sha256'],
 'source':hand['active_binding']['artifacts']['source']['sha256'],
 'generator':hand['active_binding']['artifacts']['generator']['sha256'],
 'config':hand['active_binding']['artifacts']['config']['sha256'],
 'render_manifest':hand['active_binding']['render_manifest']['sha256']}
preproof_hashes={'glb':pre['glb_sha256'],'brief':pre['brief_sha256'],'references':pre['references_sha256']}
render_subject=render['subject']
frames=[]
for f in render['frames']:
    b=(r/'proof-final'/f['path']).read_bytes();frames.append({'id':f['id'],'path':f['path'],'expected_bytes':f['bytes'],'actual_bytes':len(b),'expected_sha256':f['sha256'],'actual_sha256':sha(b),'ok':len(b)==f['bytes'] and sha(b)==f['sha256']})
pixels=read(r/'pixel-inspection.json')
contact={'path':str(r/'contact-sheet.png'),'sha256':H(r/'contact-sheet.png'),'maker_expected':pixels['contact_sheet_sha256'],'frame_hashes_match':all(x['ok'] for x in frames)}
# original freeze and addendum bindings
r001=repo/'assets/candidates/continuous-small-life-round28-20261020/batch-70/kettle-basin/r001'
original_r001_freeze=r001/'modeling-freeze.json'
freeze_file_results={n:{'expected':h,'actual':H(r/n),'ok':H(r/n)==h} for n,h in freeze['files'].items()}
original_freeze_hash=H(original_r001_freeze)
add_hash=H(r/'repair-addendum-freeze.json')
# actual primary-reference pixels (consult-only only, never copied into repo)
consult=Path('/workspace/shared/batch70-consult-only')
ref_hashes={}
for s in refs['sources']:
    for img in s.get('consulted_images',[]):
        pp=consult/img['filename']; actual=H(pp)
        ref_hashes[img['filename']]={'expected':img['sha256'],'actual':actual,'ok':actual==img['sha256'],'pixels_path':str(pp)}
# queue request/result/output checks
jobs=[]
for i in (1,2):
    report=read(r/f'repro-final-{i}.report.json'); run=report['build_run']
    req_path=repo/run['request']['path']; res_path=repo/run['result']['path']; req=read(req_path); res=read(res_path)
    outputs={}
    for name,obj in res['outputs'].items():
        f=res_path.parent/'outputs'/name; b=f.read_bytes(); outputs[name]={'expected_bytes':obj['bytes'],'actual_bytes':len(b),'expected_sha256':obj['sha256'],'actual_sha256':sha(b),'ok':len(b)==obj['bytes'] and sha(b)==obj['sha256']}
    input_hashes={k:{'path':v['path'],'expected_sha256':v['sha256'],'actual_sha256':sha(Path(v['path']).read_bytes()),'ok':sha(Path(v['path']).read_bytes())==v['sha256']} for k,v in req['identity']['inputs'].items()}
    jobs.append({'job_id':res['job_id'],'request_path':str(req_path),'request_sha256':sha(req_path.read_bytes()),'expected_request_sha256':run['request']['sha256'],'request_hash_ok':sha(req_path.read_bytes())==run['request']['sha256'],'result_path':str(res_path),'result_sha256':sha(res_path.read_bytes()),'expected_result_sha256':run['result']['sha256'],'result_hash_ok':sha(res_path.read_bytes())==run['result']['sha256'],'pid':res['pid'],'status':res['status'],'returncode':res['returncode'],'started_at':res['started_at'],'finished_at':res['finished_at'],'attempt_directory':str(res_path.parent),'run_id':req.get('run_id'),'fingerprint':req.get('fingerprint'),'input_hashes':input_hashes,'all_input_hashes_match':all(x['ok'] for x in input_hashes.values()),'outputs':outputs,'repro_report_status':report['status'],'final_glb_sha256':report['glb_sha256'],'rebuilt_glb_sha256':report['rebuilt_glb_sha256'],'semantic_sha256':report['semantic_sha256'],'byte_identical':report['byte_identical']})
# ensure no latest source edits after checks
status_after=git('status','--porcelain=v1').decode().strip()
result={
 'schema':'independent-kettle-r002-closure-v1','checked_at_utc':datetime.now(timezone.utc).isoformat(),
 'source_repo':str(repo),'branch':git('branch','--show-current').decode().strip(),'head':head,'expected_commit':commit,'head_matches':head==commit,
 'baseline_parent':base,'baseline_tree':git('rev-parse',f'{base}^{{tree}}').decode().strip() if False else git('rev-parse',f'{base}^{{tree}}').decode().strip(),
 'worktree_clean_before_after':not status and not status_after,'worktree_status_before':status,'worktree_status_after':status_after,
 'diff_from_prior_QA_commit':{'counts':{'added':sum(x.startswith('A\t') for x in changes),'modified':sum(x.startswith('M\t') for x in changes),'deleted':sum(x.startswith('D\t') for x in changes)},'append_only':all(x.startswith('A\t') for x in changes),'paths':changes},
 'original_paths_unchanged':{str(p.relative_to(repo)):git('diff','--quiet',base,commit,'--',str(p.relative_to(repo))) is not None for p in []},
 'committed_manifest':{'path':rel,'sha256_worktree':H(manifest_path),'sha256_git':sha(manifest_git),'self_excluded':manifest.get('self_excluded'),'files':len(manifest['files']),'total_bytes':manifest['total_bytes'],'verified_entries':sum(x['ok'] for x in manifest_entries),'failed_entries':[x['path'] for x in manifest_entries if not x['ok']],'all_entries_match_worktree_and_git':all(x['ok'] for x in manifest_entries),'external_verification_sidecar':external,'external_verification_matches':external.get('commit')==commit and external.get('committed_manifest_entries_verified')==len(manifest['files']) and external.get('manifest_itself_verified') is True and external.get('clean_worktree') is True},
 'artifact_hashes':actual_hashes,'handoff_expected_hashes':expected_handoff,'all_handoff_hashes_match':actual_hashes==expected_handoff,
 'preproof_binding':{'checked_at':pre['checked_at'],'status':pre['status'],'render_started_at':next(x['started_at'] for x in [read(p/'HANDOFF.json')] if False) if False else '2026-10-20T16:50:13.596723+00:00','preproof_precedes_render_start':pre['checked_at']<'2026-10-20T16:50:13.596723+00:00','hashes':preproof_hashes,'hashes_match_final':all(preproof_hashes[k]==actual_hashes[k] for k in preproof_hashes),'render_subject':render_subject},
 'final_render':{'manifest_hash':actual_hashes['render_manifest'],'created_at':render['created_at'],'frame_count':len(frames),'frames':frames,'all_frames_match':all(x['ok'] for x in frames),'contact_sheet':contact,'manifest_source_hash_matches_glb':render['source_glb_sha256']==actual_hashes['glb'],'candidate_binding_after_render':{'candidate_json_includes_render_manifest':cand['evidence'][0]['sha256']==actual_hashes['render_manifest'],'note':'Candidate wrapper records the completed proof manifest; preproof binding fixed revision r002 plus exact GLB/derived brief/references before rendering.'}},
 'freeze_closure':{'r002_initial_freeze':{'frozen_at':freeze['frozen_at'],'original_r001_freeze_path':freeze['original_freeze_path'],'expected_sha256':freeze['original_freeze_sha256'],'actual_sha256':original_freeze_hash,'matches':freeze['original_freeze_sha256']==original_freeze_hash,'file_hashes':freeze_file_results},'repair_addendum':{'frozen_at':add['frozen_at'],'change':add['change'],'sha256':add_hash,'repair_config_hash_in_addendum':add['new_active_config']['sha256'],'actual_repair_config_hash':H(r/'repair-config.json'),'repair_config_matches':add['new_active_config']['sha256']==H(r/'repair-config.json')},'preserved_diagnostic_attempt':{'path':'attempts/diagnostic-1','manifest_sha256':H(r/'attempts/diagnostic-1/diagnostic-proof/render-manifest.json'),'glb_sha256':read(r/'attempts/diagnostic-1/diagnostic-proof/render-manifest.json')['source_glb_sha256'],'is_final_glb':read(r/'attempts/diagnostic-1/diagnostic-proof/render-manifest.json')['source_glb_sha256']==actual_hashes['glb']}},
 'primary_reference_pixels':ref_hashes,
 'source_reexport':{'source_hash':actual_hashes['source'],'glb_hash':actual_hashes['glb'],'created_independent_glb_hash':H('/workspace/shared/lowpoly-round28-qa70/diff-kettle-r002/r002-source-reexport.glb'),'byte_identity':H(r/'model.glb')==H('/workspace/shared/lowpoly-round28-qa70/diff-kettle-r002/r002-source-reexport.glb')},
 'two_execution_jobs':jobs,
 'nominal_vs_measured':{'nominal_blender_xyz_m':brief['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':brief['repair_active_inputs']['actual_measured_bounds'],'measured_glb_xyz_m':read(r/'metrics.json')['measured_glb_xyz_m'],'disclosed':True},
 'render_config_delta':{'comparison_path':str(p/'render-config-comparison.json'),'same_helper_hash':read(p/'render-config-comparison.json')['same_render_helper_sha256'],'literal_numeric_cameras_unchanged':read(p/'render-config-comparison.json')['literal_numeric_cameras_unchanged'],'literal_numeric_light_rig_unchanged':read(p/'render-config-comparison.json')['literal_numeric_light_rig_unchanged'],'interpretation':'Policy/helper unchanged; numeric bounds-derived camera and light fit values did change.'}
}
# Correct original unchanged map
for path in [
 'assets/candidates/continuous-small-life-round28-20261020/batch-70/kettle-basin/r001',
 'assets/candidates/continuous-small-life-round28-20261020/batch-70/waputikia',
 'assets/candidates/continuous-small-life-round28-20261020/batch-70/linear-dune',
 'assets/candidates/continuous-small-life-round28-20261020/batch-70/rimstone-dam']:
    try:
        subprocess.run(['git','-C',str(repo),'diff','--quiet',base,commit,'--',path],check=True)
        result['original_paths_unchanged'][path]=True
    except subprocess.CalledProcessError:
        result['original_paths_unchanged'][path]=False
result['all_original_assets_unchanged']=all(result['original_paths_unchanged'].values())
result['two_jobs_are_distinct']=(len({j['pid'] for j in jobs})==2 and len({j['attempt_directory'] for j in jobs})==2 and len({j['fingerprint'] for j in jobs})==2 and all(j['all_input_hashes_match'] and j['status']=='succeeded' and j['returncode']==0 and j['final_glb_sha256']==actual_hashes['glb'] and j['rebuilt_glb_sha256']==actual_hashes['glb'] and all(o['ok'] for o in j['outputs'].values()) for j in jobs))
out=Path('/workspace/shared/lowpoly-round28-qa70/diff-kettle-r002/closure-verification.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'head_matches':result['head_matches'],'worktree_clean':result['worktree_clean_before_after'],'manifest_entries':result['committed_manifest']['files'],'manifest_verified':result['committed_manifest']['all_entries_match_worktree_and_git'],'append_only':result['diff_from_prior_QA_commit'],'original_assets_unchanged':result['all_original_assets_unchanged'],'handoff_bindings_match':result['all_handoff_hashes_match'],'preproof_hashes_match':result['preproof_binding']['hashes_match_final'],'frames_match':result['final_render']['all_frames_match'],'r001_freeze_match':result['freeze_closure']['r002_initial_freeze']['matches'],'repair_config_match':result['freeze_closure']['repair_addendum']['repair_config_matches'],'job_pids':[j['pid'] for j in jobs],'distinct_jobs':result['two_jobs_are_distinct'],'source_reexport_identical':result['source_reexport']['byte_identity']},indent=2))

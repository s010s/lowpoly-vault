#!/usr/bin/env python3
"""Independent read-only batch77 integrity, candidate, render, and rebuild audit."""
from pathlib import Path
import subprocess,hashlib,json,sys,struct
repo=Path('/workspace/shared/lowpoly-batch77-20261020').resolve(); qadir=Path('/workspace/shared/lowpoly-round31-qa77/batch77-20261020').resolve(); coord=Path('/workspace/shared/lowpoly-round31-coordination')
commit='72a9aed63791e4aca88b837ed701dabd8872b3fd'; ids=[('ernietta','r004'),('loess-bluff','r005'),('rock-glacier','r002'),('slump-folded-bed','r003')]
def H(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def J(p): return json.loads(Path(p).read_text())
def git(*a): return subprocess.check_output(['git','-C',str(repo),*a],text=True).strip()
assert git('rev-parse','HEAD')==commit
status=git('status','--porcelain=v1'); assert not status,status
# Single read of the pinned Git tree verifies all 1,023 claimed source evidence blobs against both commit and worktree.
tree=subprocess.check_output(['git','-C',str(repo),'ls-tree','-r','-z','--full-tree',commit])
blob_by_path={}
for rec in tree.split(b'\0'):
 if not rec: continue
 meta,path=rec.split(b'\t',1); mode,kind,blob=meta.decode().split(' ')
 blob_by_path[path.decode()]=blob
manifest_path=repo/'production/small-life-batch77/source-evidence-manifest.json'; manifest=J(manifest_path); manifest_sha=H(manifest_path); entries=manifest['files']; assert len(entries)==1023
manifest_report=J(coord/'batch77-committed-blob-verification.json'); assert manifest_report['commit']==commit and manifest_report['manifest_sha256']==manifest_sha and manifest_report['files_checked']==1023
verification_by_path={e['path']:e for e in manifest_report['files']}
mismatch=[]; total=0
for e in entries:
 p=repo/e['path']; data=p.read_bytes(); total+=len(data); vr=verification_by_path.get(e['path'],{})
 if hashlib.sha256(data).hexdigest()!=e['sha256'] or len(data)!=e['bytes'] or blob_by_path.get(e['path'])!=vr.get('git_blob') or vr.get('sha256')!=e['sha256']:
  mismatch.append(e['path'])
assert total==107_123_938,total
assert not mismatch,mismatch[:5]
# Handoff supplied SHA is computed over bytes; Git blob ID is separately checked.
handoff='production/small-life-batch77/handoff.json'; handoff_sha=H(repo/handoff); handoff_blob=blob_by_path[handoff]
assert handoff_sha=='ce9f9c7001ba7575608cae2b9592f6ca5b699f9f80418a3dd46788d32a8ded45'
# Check target input integrity before and after independent work.
before={line.split()[1]:line.split()[0] for line in (qadir/'input-sha256-before.txt').read_text().splitlines()}
after={line.split()[1]:line.split()[0] for line in (qadir/'input-sha256-after.txt').read_text().splitlines()}; assert before==after
assert len(before)==29, len(before)
assets=[]; total_frames=0; all_run_pids=[]; all_run_paths=[]
for aid,rev in ids:
 d=repo/'production/small-life-batch77/assets'/aid/rev
 cand=J(d/'candidate.json'); brief=J(d/'brief.json'); cbrief=J(d/'candidate-brief.json'); freeze=J(d/'modeling-freeze.json'); refs=J(d/'references.json'); meta=J(d/'metadata.json'); mani=J(d/'proof-final/render-manifest.json'); pixels=J(d/'pixel-inspection.json'); binding=J(d/'final-rebuild-binding.json'); metrics=J(d/'metrics.json'); source_export=J(qadir/aid/'source-export.report.json'); reexport=J(qadir/aid/'reexport.report.json')
 assert cand['asset_id']==aid and cand['revision']==rev
 # Candidate closure: exact artifacts and manifest/brief/reference subject binding.
 def candidate_hash(key):
  a=cand['artifacts'][key]; p=repo/a['path']; assert H(p)==a['sha256']; assert blob_by_path[a['path']]==git('rev-parse',f'{commit}:{a["path"]}'); return a['sha256']
 glb_sha=candidate_hash('glb'); brief_sha=candidate_hash('brief'); refs_sha=candidate_hash('references'); source_sha=candidate_hash('source'); generator_sha=candidate_hash('generator'); config_sha=candidate_hash('config')
 assert mani['source_glb_sha256']==glb_sha and mani['subject']=={'revision':rev,'glb_sha256':glb_sha,'brief_sha256':brief_sha,'references_sha256':refs_sha}
 assert H(d/'proof-final/render-manifest.json')==cand['evidence'][0]['sha256']
 # Frozen premodel inputs and the original freeze time are checked independently, without treating derived candidate brief as original brief.
 for fname,want in freeze['files'].items(): assert H(d/fname)==want,(aid,fname)
 assert freeze['frozen_at'].startswith('2026-10-20T15:55:52.')
 assert brief['created_at'].startswith('2026-10-20T15:55:52.') and cbrief['brief_version']==brief['brief_version']
 assert brief['criteria']==cbrief['criteria'] and brief['claim_scope']==cbrief['claim_scope']
 # Eight exact 512x512 files and the matching independent contact sheet.
 assert mani['frame_count']==8 and len(mani['frames'])==8 and mani['width']==mani['height']==512
 frames=[]
 for fr in mani['frames']:
  fp=d/'proof-final'/fr['path']; assert H(fp)==fr['sha256']; data=fp.read_bytes(); assert data.startswith(b'\x89PNG') and struct.unpack('>II',data[16:24])==(512,512)
  frames.append({'id':fr['id'],'sha256':fr['sha256'],'width':512,'height':512})
 assert [x['id'] for x in frames]==brief['required_views']
 contact_sha=H(d/'contact-sheet.png'); assert pixels['contact_sheet_sha256']==contact_sha
 assert len(pixels['frames'])==8 and all(p['sha256']==frames[i]['sha256'] and p['dimensions']==[512,512] for i,p in enumerate(pixels['frames']))
 total_frames+=8
 # Rights and actual source-time data are carried through from references; no consulted source image is incorporated.
 source_refs=[]
 for s in refs['sources']:
  source_refs.append({'id':s['id'],'title':s['title'],'url':s['url'],'rights':s['license'],'use':s['use'],'incorporated':s['incorporated'],'consulted_at':s.get('consulted_at')})
  if s['id']!='CONCEPT': assert s['use']=='consulted-only; no source media, mesh or texture incorporated' and s['incorporated'] is False
 # Two real build queue records are checked against separate request/result/stdout/output files, PIDs, times, fingerprints, inputs and hashes.
 runs=[]; records=binding['distinct_real_queue_runs']; assert len(records)==2
 for run in records:
  run_dir=repo/run['path']; req_path=run_dir/'request.json'; res_path=run_dir/'result.json'; req=J(req_path); res=J(res_path)
  assert H(req_path)==run['request_sha256'] and H(res_path)==run['result_sha256']
  identity=req['identity']; fingerprint=hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
  assert req['fingerprint']==fingerprint==res['fingerprint']
  assert identity['job']['asset_id']==aid and identity['job']['revision']==rev and identity['job']['job_id']==run['job_id']
  assert res['status']=='succeeded' and res['returncode']==0 and res['error'] is None
  assert res['pid']==run['pid'] and res['started_at']==run['started_at'] and res['finished_at']==run['finished_at']
  assert res['started_at']<res['finished_at']
  for nm,expect in [('generator',generator_sha),('config',config_sha)]: assert identity['inputs'][nm]['sha256']==expect
  for nm in ('generator','config'): assert any(x==identity['inputs'][nm]['path'] or x.endswith('='+identity['inputs'][nm]['path']) for x in req['argv'])
  out=run_dir/'outputs/model.glb'; source_out=run_dir/'outputs/source.blend'; metrics_out=run_dir/'outputs/metrics.json'
  assert H(out)==run['output_glb_sha256']==glb_sha==res['outputs']['model.glb']['sha256']
  assert H(source_out)==res['outputs']['source.blend']['sha256'] and source_out.stat().st_size==res['outputs']['source.blend']['bytes']
  assert H(metrics_out)==res['outputs']['metrics.json']['sha256']
  stdout=(run_dir/'stdout.log').read_text(); assert f'BUILT {aid} {glb_sha} ' in stdout
  assert (run_dir/'stderr.log').stat().st_size==0
  runs.append({'pid':run['pid'],'job_id':run['job_id'],'started_at':run['started_at'],'finished_at':run['finished_at'],'request_sha256':run['request_sha256'],'result_sha256':run['result_sha256'],'output_glb_sha256':run['output_glb_sha256'],'output_source_blend_sha256':res['outputs']['source.blend']['sha256'],'fingerprint':fingerprint,'stdout_contains_built_record':True})
 assert len({r['pid'] for r in runs})==2 and len({r['job_id'] for r in runs})==2 and len({r['request_sha256'] for r in runs})==2 and len({r['result_sha256'] for r in runs})==2 and len({r['fingerprint'] for r in runs})==2 and len({r['started_at'] for r in runs})==2
 all_run_pids += [r['pid'] for r in runs];all_run_paths += [r['request_sha256'] for r in runs]
 # Fresh own source/export and exact byte re-export checks are bound to the final candidate.
 assert source_export['status']=='pass' and source_export['source_sha256']==source_sha and source_export['glb_sha256']==glb_sha
 assert source_export['source_triangles']==source_export['glb_triangles'] and source_export['bounds_max_error_m']<=1e-4
 assert reexport['status']=='pass' and reexport['byte_identical'] and reexport['reexport_sha256']==glb_sha and reexport['source_sha256_before']==reexport['source_sha256_after']==source_sha
 # Stages remain separate and no release/formal acceptance is implied.
 assert all(v['status']=='unknown' for v in cand['stages'].values()) and cand['approval']['status']=='pending'
 assets.append({'id':aid,'revision':rev,'sha256':glb_sha,'glb_bytes':(d/'model.glb').stat().st_size,'triangles':metrics['glb']['unique_mesh_triangles'],'materials':metrics['glb']['materials'],'primitives':metrics['glb']['unique_mesh_primitives'],'source_sha256':source_sha,'source_brief_sha256':H(d/'brief.json'),'candidate_brief_sha256':brief_sha,'references_sha256':refs_sha,'config_sha256':config_sha,'generator_sha256':generator_sha,'freeze_time':freeze['frozen_at'],'repair_freeze_time':J(d/'repair-freeze.json').get('frozen_at') if (d/'repair-freeze.json').exists() else None,'render_manifest_sha256':H(d/'proof-final/render-manifest.json'),'contact_sheet_sha256':contact_sha,'frames':frames,'references':source_refs,'semantic_rebuilds':runs,'technical_static':{'source_triangles':source_export['source_triangles'],'glb_triangles':source_export['glb_triangles'],'bounds_max_error_m':source_export['bounds_max_error_m'],'exact_byte_reexport':reexport['byte_identical']}})
assert total_frames==32 and len(set(all_run_pids))==8
# The official Khronos/Three fresh reports were generated by the independent read-only validators in this QA tree.
k_reports=[json.loads(x) for x in (qadir/'khronos-fresh.jsonl').read_text().splitlines()]; t_reports=[json.loads(x) for x in (qadir/'three-fresh.jsonl').read_text().splitlines()]
assert len(k_reports)==len(t_reports)==4
for a,k,t in zip(assets,k_reports,t_reports):
 assert k['sha256']==a['sha256'] and k['errors']==0 and k['warnings']==0
 assert t['glb_sha256']==a['sha256'] and t['triangles']==a['triangles'] and not t['errors']
# Candidate repair histories remain committed and unmodified by this review; no source artifact or brief was edited.
report={'kind':'independent_batch77_static_qa_integrity','status':'pass_integrity_and_static_technical; ernietta_scope_revise; other_three_accept_static_qa_only','pinned_commit':commit,'worktree_status':'clean','handoff_sha256':handoff_sha,'handoff_git_blob':handoff_blob,'source_manifest_path':'production/small-life-batch77/source-evidence-manifest.json','source_manifest_sha256':manifest_sha,'manifest_file_count':len(entries),'manifest_total_file_bytes':total,'manifest_files_matching_worktree_and_committed_git_blob':len(entries),'committed_manifest_producer_record_independently_reverified':True,'pinned_target_inputs_pre_post_unchanged':True,'frames_individually_viewed':total_frames,'contact_sheets_individually_viewed':4,'original_reference_pixels_viewed':4,'original_concept_pixels_viewed':4,'semantic_queue_runs_independently_reverified':len(all_run_pids),'semantic_queue_distinct_pids':len(set(all_run_pids)),'fresh_khronos':{'validator_version':k_reports[0]['validator_version'],'assets':4,'errors':0,'warnings':0},'fresh_three_node':{'version':'0.180.0','assets':4,'errors':0},'stages':{'technical':'fresh checks pass for all four','visual':'inspection pass except Ernietta basal zigzag seam is not visible in any fixed view; revise required','factual':'scope/feature/source review pass except visual evidence of Ernietta required seam is insufficient; do not misstate complete organism','specification':'candidate bundles/brief bindings pass; GPU/scene are separate not run','runtime_parse':'fresh Three.js Node parse pass; browser/hardware not run','gpu':'not run','scene':'not run'},'publication_or_formal_approval':'not asserted','own_qa_artifacts_only':True,'assets':assets}
out=qadir/'integrity-check.json';out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:report[k] for k in ['status','pinned_commit','handoff_sha256','source_manifest_sha256','manifest_file_count','manifest_total_file_bytes','frames_individually_viewed','contact_sheets_individually_viewed','semantic_queue_runs_independently_reverified','semantic_queue_distinct_pids','fresh_khronos','fresh_three_node']},indent=2))

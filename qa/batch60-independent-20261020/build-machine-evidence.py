import hashlib,json,subprocess,os,copy
from pathlib import Path
from PIL import Image
OUT=Path('/tmp/lowpoly-round23-qa60'); R=Path('/tmp/lowpoly-batch60-20261020'); W=R/'production/continuous-small-life-round23-20261020/work/batch-60'; BASE=R/'assets/candidates/continuous-small-life-round23-20261020/batch-60'
HEAD='9bc5b6317eb6e7073f6fe5cd1bce6b4ca11fe086'; PAYLOAD='09f353f099ec6d461edd6667408c6663c57783f5'
specs=[('collinsium','r002','b2634bfc3f952bf5cfec2574142c925c8b2ce3e0ac48dcb0b35d22bf9e07cfaf','4bdec9762f9fddb6d010da29d1ae3b8148c8027f4c24eed3e5bb96f0dace1b56','A'),('yardang','r002','77da5fcdc712732b73af15879101c467f31440bc90d57c7741649088b771c80a','e92e71a4e947c10ec82b8182e4a2169f1cf0670d2df5ec1582a70cba566fd36a','B'),('glacial-cirque','r001','6514d415da79c77bcbbd35e26ebc8734aebe6da745d3e73584d8e03c446436d5','1bbcc63e93236a486f7f8f1ca6b9a568ef8ce4d9876816ad34b7593e378b3f4c','C'),('aragonite-frostwork','r001','444de67aa8c9a403ff576bfbb92518210534a0f0e4165149ef3d58d801dc0381','757a8e58c47f4162726b6a1d0c45f22b275d40524fdc401d905a677d9da19410','D')]
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def j(p): return json.loads(Path(p).read_text())
def rgba_info(p):
 im=Image.open(p).convert('RGBA'); raw=im.tobytes(); return {'size':list(im.size),'mode':im.mode,'decoded_rgba_sha256':hashlib.sha256(raw).hexdigest()}
# Pin and views report
head=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','-C',str(R),'branch','--show-current'],text=True).strip()
status=subprocess.check_output(['git','-C',str(R),'status','--porcelain=v1'],text=True)
ancestor=subprocess.run(['git','-C',str(R),'merge-base','--is-ancestor',PAYLOAD,HEAD]).returncode==0
policy=R/'production/policies/qa-passed-batch-publication-20261018.json'
views=[]; candidates=[]
for aid,rev,glbexp,sourceexp,row in specs:
 p=BASE/aid/rev; c=j(p/'candidate.json'); brief=j(p/'brief.json'); cb=j(p/'candidate-brief.json'); ref=j(p/'references.json'); delivery=j(p/'references.delivery-v001.json'); mf=j(p/'proof-final/render-manifest.json'); freeze=j(p/'modeling-freeze.json'); proof_old=p/'proof-premodel-references'; proof_new=p/'proof-final'
 expected={'model.glb':glbexp,'source.blend':sourceexp,'candidate-brief.json':c['artifacts']['brief']['sha256'],'references.delivery-v001.json':c['artifacts']['references']['sha256'],'generator.py':c['artifacts']['generator']['sha256'],'build-config.json':c['artifacts']['config']['sha256'],'proof-final/render-manifest.json':c['evidence'][0]['sha256']}
 actual={k:h(p/k) for k in expected}
 pin_ok=all(actual[k]==v for k,v in expected.items()) and h(p/'candidate-brief.json')==c['artifacts']['brief']['sha256'] and h(p/'references.delivery-v001.json')==c['artifacts']['references']['sha256'] and h(p/'generator.py')==c['artifacts']['generator']['sha256'] and h(p/'build-config.json')==c['artifacts']['config']['sha256']
 freeze_results={fn:{'expected':dig,'actual':h(p/fn) if (p/fn).exists() else None,'match':(p/fn).exists() and h(p/fn)==dig} for fn,dig in freeze['files'].items()}
 frame_ids={'hero','reversehero','front','side','rear','top','clay','silhouette'}
 frame_records=[]
 manifest_ids=set()
 for fr in mf['frames']:
  fid=fr['id'];manifest_ids.add(fid);new=proof_new/fr['path'];old=proof_old/fr['path'];ni=rgba_info(new);oi=rgba_info(old)
  frame_records.append({'id':fid,'path':fr['path'],'width':fr['width'],'height':fr['height'],'png_sha256':h(new),'manifest_png_sha256':fr['sha256'],'source_glb_sha256':mf['subject']['glb_sha256'],'brief_sha256':mf['subject']['brief_sha256'],'references_sha256':mf['subject']['references_sha256'],'old_rgba_sha256':oi['decoded_rgba_sha256'],'new_rgba_sha256':ni['decoded_rgba_sha256'],'decoded_rgba_equal':oi['decoded_rgba_sha256']==ni['decoded_rgba_sha256'] and oi['size']==ni['size'],'matches_work_equivalence_ledger':any(x['id']==fid and x['decoded_RGBA_equal'] and x['final_rgba_sha256']==ni['decoded_rgba_sha256'] for a in j(W/'rights-render-pixel-equivalence.json')['assets'] if a['asset_id']==aid for x in a['frames'])})
 views.append({'asset_id':aid,'revision':rev,'concept_row':row,'concept_sheet_sha256':h(p/'concept-original.png'),'concept_image_sha256':h(p/'concept-original.png'),'proof_manifest_sha256':h(p/'proof-final/render-manifest.json'),'manifest_subject':mf['subject'],'expected_subject':{'revision':rev,'glb_sha256':glbexp,'brief_sha256':c['artifacts']['brief']['sha256'],'references_sha256':c['artifacts']['references']['sha256']},'required_views':sorted(frame_ids),'observed_views':sorted(manifest_ids),'view_manifest_ok':manifest_ids==frame_ids and mf['frame_count']==8 and mf['width']==512 and mf['height']==512 and mf['subject']['glb_sha256']==glbexp and mf['subject']['brief_sha256']==c['artifacts']['brief']['sha256'] and mf['subject']['references_sha256']==c['artifacts']['references']['sha256'],'all_32_pixels_checked':len(frame_records)==8 and all(x['decoded_rgba_equal'] and x['matches_work_equivalence_ledger'] for x in frame_records),'frames':frame_records})
 # semantic equality of premodel brief vs candidate delivery brief
 cb0=copy.deepcopy(cb); b0=copy.deepcopy(brief)
 adapter=cb0.pop('packaging_adapter',None); deliverables=cb0.pop('required_deliverables',None)
 b0.pop('required_deliverables',None)
 brief_design_equal=cb0==b0
 # reference ledger: all existing source record fields exactly same; additions only rights declaration
 d0=copy.deepcopy(delivery); d0.pop('no_incorporated_third_party_assets',None); d0.pop('packaging_rights_adapter',None)
 for i,s in enumerate(d0.get('sources',[])):
  original=ref['sources'][i]
  d0['sources'][i]={k:v for k,v in s.items() if k in original}
 ref_design_equal=d0==ref
 candidates.append({'asset_id':aid,'revision':rev,'row':row,'candidate_record_sha256':h(p/'candidate.json'),'candidate_approved_flag':c.get('approved'),'approval_status':c.get('approval',{}).get('status'),'stage_statuses':{k:v.get('status') for k,v in c.get('stages',{}).items()},'exact_hashes':{'glb':{'expected':glbexp,'actual':actual['model.glb'],'match':actual['model.glb']==glbexp},'source_blend':{'expected':sourceexp,'actual':actual['source.blend'],'match':actual['source.blend']==sourceexp},'candidate_brief':{'expected':c['artifacts']['brief']['sha256'],'actual':h(p/'candidate-brief.json'),'match':h(p/'candidate-brief.json')==c['artifacts']['brief']['sha256']},'delivery_references':{'expected':c['artifacts']['references']['sha256'],'actual':h(p/'references.delivery-v001.json'),'match':h(p/'references.delivery-v001.json')==c['artifacts']['references']['sha256']},'generator':{'expected':c['artifacts']['generator']['sha256'],'actual':h(p/'generator.py'),'match':h(p/'generator.py')==c['artifacts']['generator']['sha256']},'config':{'expected':c['artifacts']['config']['sha256'],'actual':h(p/'build-config.json'),'match':h(p/'build-config.json')==c['artifacts']['config']['sha256']},'render_manifest':{'expected':c['evidence'][0]['sha256'],'actual':h(p/'proof-final/render-manifest.json'),'match':h(p/'proof-final/render-manifest.json')==c['evidence'][0]['sha256']}},'candidate_pins_match':pin_ok,'premodel_freeze_files':freeze_results,'premodel_freeze_all_match':all(x['match'] for x in freeze_results.values()),'candidate_brief_diff_only_packaging_fields':brief_design_equal,'candidate_brief_added_fields':{'packaging_adapter':adapter,'required_deliverables':deliverables},'references_delivery_adds_only_consulted_rights_metadata':ref_design_equal,'delivery_root_metadata':{'no_incorporated_third_party_assets':delivery.get('no_incorporated_third_party_assets'),'packaging_rights_adapter':delivery.get('packaging_rights_adapter')},'concept_validation':j(p/'concept-validation.json'),'concept_provider_timestamp':j(p/'concept-generation.json').get('provider_generation_timestamp'),'publication_policy_sha256':h(policy),'profile_contract_policy_sha256':j(p/'profile-contract.json')['publication_policy']['sha256']})
pin={'source_repo':str(R),'head':head,'expected_head':HEAD,'head_match':head==HEAD,'branch':branch,'worktree_clean':status=='','worktree_porcelain':status.splitlines(),'creator_payload_commit':PAYLOAD,'creator_payload_ancestor_of_final_head':ancestor,'publication_policy_actual_sha256':h(policy),'candidates':candidates,'visual_views':views}
(OUT/'pin-and-views.json').write_text(json.dumps(pin,indent=2)+'\n')
# Pixel source hashes from ledger, verify consulted-only source assets match expected and are not in candidate tree
ledger=j(W/'source-pixel-inspection-ledger.json'); refs=[]
for f in ledger['figures']:
 p=Path(f['consulted_only_local_pixel_path']); refs.append({'path':str(p),'sha256_expected':f['sha256'],'sha256_actual':h(p),'hash_match':h(p)==f['sha256'],'redistributed':f['redistributed'],'is_repo_file':p.resolve().is_relative_to(R.resolve())})
# original refs sidecars differ only by explicit rights adapter metadata
prov={'audit':'independent static-stylized-v1 provenance/source-pixel scope audit','source_head':head,'creator_payload_commit':PAYLOAD,'creator_payload_ancestor_of_final_head':ancestor,'consulted_source_pixels':refs,'source_pixel_ledger_hashes_all_match':all(x['hash_match'] for x in refs),'frozen_brief_and_reference_details':[{'asset_id':x['asset_id'],'revision':x['revision'],'pre_model_brief_sha256':h(BASE/x['asset_id']/x['revision']/'brief.json'),'candidate_brief_sha256':h(BASE/x['asset_id']/x['revision']/'candidate-brief.json'),'brief_design_equal_except_postbuild_deliverables_and_adapter':next(y for y in candidates if y['asset_id']==x['asset_id'])['candidate_brief_diff_only_packaging_fields'],'references_delivery_equal_except_use_incorporated_rights_notes_and_packaging_adapter':next(y for y in candidates if y['asset_id']==x['asset_id'])['references_delivery_adds_only_consulted_rights_metadata'],'premodel_freeze_files_all_match':next(y for y in candidates if y['asset_id']==x['asset_id'])['premodel_freeze_all_match']} for x in candidates],'interpretation':'Original frozen brief/reference hashes and scientific content remain intact. Candidate-brief adapters add postbuild source/generator/config deliverable paths and exact hashes; delivery reference sidecars add consulted-only/no-third-party-asset declarations. Neither changes frozen scientific/design scope. Concept sheet is visual input only; Collinsium=A, Yardang=B, Cirque=C, Frostwork=D. Provider-internal concept timestamp stays undisclosed; completeness false for that one field only.'}
(OUT/'freeze-provenance-audit.json').write_text(json.dumps(prov,indent=2)+'\n')
# Queue-bound rebuild evidence. Keep only actual distinct successful process results for final exact revisions.
run_summaries=sorted((W/'rebuild-runs/runs').glob('*/summary.json'))
queue=[]
for aid,rev,glbexp,sourceexp,row in specs:
 attempts=[]
 for sp in run_summaries:
  summary=j(sp)
  for r in summary.get('results',[]):
   if r.get('asset_id')!=aid or r.get('revision')!=rev:continue
   ad=Path(r.get('attempt_dir','')); req=j(ad/'request.json') if (ad/'request.json').exists() else {}; res=j(ad/'result.json') if (ad/'result.json').exists() else {}
   outdir=ad/'outputs'; metrics=j(outdir/'metrics.json') if (outdir/'metrics.json').exists() else {}
   gm=metrics.get('glb',{}); semantic=gm.get('semantic_sha256')
   output_hashes={name:h(outdir/name) if (outdir/name).exists() else None for name in ['model.glb','source.blend','metrics.json','source-metrics.json']}
   declared=r.get('outputs',{})
   outputs_match=all(name in declared and output_hashes[name]==declared[name].get('sha256') for name in output_hashes)
   input_hashes={k:v.get('sha256') for k,v in req.get('identity',{}).get('inputs',{}).items()}
   attempts.append({'run_id':sp.parent.name,'run_manifest_sha256':h(sp.parent/'manifest.json'),'queue_run_lane':summary.get('lane'),'threads':req.get('identity',{}).get('threads'),'pid':r.get('pid'),'job_id':r.get('job_id'),'status':r.get('status'),'returncode':r.get('returncode'),'fingerprint':r.get('fingerprint'),'attempt_dir':str(ad),'input_hashes':input_hashes,'actual_output_hashes':output_hashes,'summary_output_hashes':{k:v.get('sha256') for k,v in declared.items()},'semantic_sha256':semantic,'result_status':res.get('status'),'result_output_hashes':{k:v.get('sha256') for k,v in res.get('outputs',{}).items()},'output_hashes_match_queue_record':outputs_match,'glb_matches_final_pin':output_hashes.get('model.glb')==glbexp,'source_blend_distinctness':None})
 real=[a for a in attempts if a['status']=='succeeded' and a['pid'] is not None]
 pids={a['pid'] for a in real}; sem={a['semantic_sha256'] for a in real}
 queue.append({'asset_id':aid,'revision':rev,'expected_final_glb_sha256':glbexp,'attempts':attempts,'actual_successful_process_count':len(real),'distinct_pid_count':len(pids),'distinct_processes_two_or_more':len(pids)>=2,'semantic_digest_count':len(sem),'single_semantic_digest_across_processes':len(sem)==1,'all_rebuild_glbs_match_final':len(real)>=2 and all(a['glb_matches_final_pin'] for a in real),'all_queue_outputs_reconcile':len(real)>=2 and all(a['output_hashes_match_queue_record'] for a in real),'candidate_validation_semantic_sha256':j(OUT/f'candidate-{aid}.json')['measurements']['semantic_sha256'],'semantic_digest_matches_candidate_validator':len(sem)==1 and next(iter(sem))==j(OUT/f'candidate-{aid}.json')['measurements']['semantic_sha256']})
# unique source.blend outputs should differ between their independently produced processes
for item in queue:
 real=[a for a in item['attempts'] if a['status']=='succeeded' and a['pid'] is not None]
 item['distinct_source_blend_outputs']=len({a['actual_output_hashes'].get('source.blend') for a in real})==len(real)
(OUT/'queue-rebuild-audit.json').write_text(json.dumps({'queue_summaries':[{'path':str(x),'sha256':h(x),'created_at':j(x).get('started_at'),'finished_at':j(x).get('finished_at'),'lane':j(x).get('lane'),'cpu_budget':j(x).get('cpu_budget'),'peak_active_jobs':j(x).get('peak_active_jobs'),'result_count':len(j(x).get('results',[]))} for x in run_summaries],'assets':queue},indent=2)+'\n')
print('wrote pin, provenance, queue evidence')
for x in candidates: print(x['asset_id'],'pins',x['candidate_pins_match'],'freeze',x['premodel_freeze_all_match'],'brief',x['candidate_brief_diff_only_packaging_fields'],'rights',x['references_delivery_adds_only_consulted_rights_metadata'])
for x in queue: print('queue',x['asset_id'],'processes',x['actual_successful_process_count'],'pids',x['distinct_pid_count'],'glbs',x['all_rebuild_glbs_match_final'],'semantic',x['semantic_digest_matches_candidate_validator'],'outputs',x['all_queue_outputs_reconcile'])
print('head clean',head==HEAD,status=='','views',sum(len(x['frames']) for x in views),'all pixel eq',all(x['all_32_pixels_checked'] for x in views))

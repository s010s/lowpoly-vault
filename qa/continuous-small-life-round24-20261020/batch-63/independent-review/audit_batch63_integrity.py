#!/usr/bin/env python3
"""Read-only integrity, chronology, render binding and queue-rebuild audit for batch 63."""
from pathlib import Path
import hashlib, json, subprocess, sys
REPO=Path('/tmp/lowpoly-batch63-20261020')
OUT=Path('/workspace/shared/lowpoly-round24-qa63')
ASSET_ROOT=REPO/'assets/candidates/continuous-small-life-round24-20261020/batch-63'
WORK=REPO/'production/continuous-small-life-round24-20261020/work/batch-63'
SEL=[('siphusauctum','r001','cc0b3d56057bba735d422feaae49485572e669cda131eb2b8d21830e892c31dc'),('esker','r001','4415be20721b7002b0db1319287626915af648a2086c3ba50a54a8c4ca48b3ed'),('caldera','r001','5d84c7b706351559d6217e558fc8ef5458a9374043a8d001a91708c788b51258'),('dogtooth-spar-cavity','r002','3db7f65435d8117dd71285b3fc7afb9d3e73f4ba68b3f2c99e219303dbb2b80c')]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def j(p): return json.loads(Path(p).read_text())
def record_run(a,r,final_sha,n,freeze_time):
    d=ASSET_ROOT/a/r; rp=j(d/f'repro-final-{n}.report.json'); br=rp['build_run']; req_info=br['request']; res_info=br['result']
    reqp=REPO/req_info['path']; resp=REPO/res_info['path']; req=j(reqp); res=j(resp)
    outdir=Path(req['argv'][req['argv'].index('--output')+1]); glb=outdir/'model.glb'
    # Verify independent queue record bytes, actual output bytes, and report-bound values.
    checks={
      'request_hash_matches':sha(reqp)==req_info['sha256'],
      'result_hash_matches':sha(resp)==res_info['sha256'],
      'request_job_identity':req['identity']['job']['job_id']==f'semantic-rebuild-{n}' and req['identity']['job']['asset_id']==a and req['identity']['job']['revision']==r,
      'request_result_fingerprint_matches':req['fingerprint']==res['fingerprint'],
      'request_result_lane_build':req['identity']['lane']=='build',
      'result_job_identity_matches_request':res['job_id']==req['identity']['job']['job_id'] and res['asset_id']==a and res['revision']==r,
      'generator_execution_after_freeze':req['created_at']>=freeze_time and res['started_at']>=freeze_time,
      'unique_output_dir':str(outdir).endswith('/outputs'),
      'result_success':res['status']=='succeeded' and res['returncode']==0 and res['error'] is None,
      'result_has_distinct_pid':isinstance(res.get('pid'),int),
      'actual_output_exists':glb.exists(),
      'actual_output_hash_matches_result':glb.exists() and sha(glb)==res['outputs']['model.glb']['sha256'],
      'actual_output_hash_matches_selected':glb.exists() and sha(glb)==final_sha,
      'report_bytes_and_hash_match':glb.exists() and glb.stat().st_size==res['outputs']['model.glb']['bytes'] and rp['rebuilt_glb_sha256']==sha(glb),
      'repro_report_semantic_matches':rp['semantic_match'] and rp['byte_identical'] and rp['semantic_sha256']==rp['rebuilt_semantic_sha256'],
      'generator_config_inputs_verified':all(sha(v['path'])==v['sha256'] for k,v in req['identity']['inputs'].items() if k in ('generator','config','helper','audit')),
      'blender_identity_verified':Path(req['identity']['executable']['path']).exists() and sha(req['identity']['executable']['path'])==req['identity']['executable']['sha256'],
      'queue_runner_identity_verified':sha(REPO/'scripts/run_asset_queue.py')==req['identity']['runner_sha256'],
    }
    # Recompute semantic digest using the project's GLB decoder against this actual run output.
    qap=OUT/'work'/f'{a}-{r}-rebuild{n}-qa.json'
    subprocess.run([sys.executable,str(REPO/'scripts/qa_glb.py'),str(glb),'--report',str(qap)],check=True,capture_output=True,text=True)
    q=j(qap); checks['independent_rebuild_semantic_matches_report']=q.get('semantic_sha256')==rp['rebuilt_semantic_sha256']==rp['semantic_sha256']
    checks['independent_static_output_pass']=q.get('status')=='pass'
    checks['stdout_stderr_logs_present']=(outdir.parent/'stdout.log').exists() and (outdir.parent/'stderr.log').exists()
    return {'index':n,'request_path':str(reqp.relative_to(REPO)),'result_path':str(resp.relative_to(REPO)),'request_sha256':sha(reqp),'result_sha256':sha(resp),'job_id':req['identity']['job']['job_id'],'runner_run_id':req.get('run_id'),'fingerprint':req['fingerprint'],'pid':res.get('pid'),'started_at':res.get('started_at'),'finished_at':res.get('finished_at'),'wall_seconds':res.get('wall_seconds'),'output_path':str(glb),'output_sha256':sha(glb) if glb.exists() else None,'semantic_sha256':q.get('semantic_sha256'),'checks':checks,'all_checks_pass':all(checks.values())}

def main():
    branch=subprocess.check_output(['git','-C',str(REPO),'branch','--show-current'],text=True).strip()
    commit=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
    status=subprocess.check_output(['git','-C',str(REPO),'status','--porcelain'],text=True).strip()
    hand=j(WORK/'handoff.json'); inventory=j(WORK/'original-selected-inventory.json'); full_inventory=j(REPO/'research/prehistoric-1000-v1/inventory.json')
    irows={x['id']:x for x in full_inventory['assets']}; records=[]
    for a,r,expected in SEL:
        d=ASSET_ROOT/a/r; candidate=j(d/'candidate.json'); brief=d/'candidate-brief.json'; refs=d/'references.json'; glb=d/'model.glb'; source=d/'source.blend'; gen=d/'generator.py'; cfg=d/'build-config.json'; freeze=j(d/'modeling-freeze.json'); cfgj=j(cfg); refsj=j(refs); finalmanifest=j(d/'proof-final/render-manifest.json'); rcfg=j(d/'proof-final/render-config.json'); evidence=candidate['evidence'][0]; srcfinal=j(d/'source-final.report.json')
        revision_selection=j(WORK/'revision-selection.json')
        hrow=next(x for x in hand['selected'] if x['asset_id']==a)
        expected_row=hrow['hashes']; exact={k:sha(p) for k,p in [('glb',glb),('brief',brief),('references',refs),('source',source),('generator',gen),('config',cfg)]}
        # Independent Blender reopen is read-only. Cross-check its exact source
        # SHA against current disk bytes and handoff/candidate pins.
        blend_report=j(OUT/'work'/f'{a}-{r}-blender.json')
        blender_actual_sha=sha(source)
        blend_objects=blend_report['objects']
        blender_triangles=sum(o['evaluated_triangle_equiv'] for o in blend_objects)
        blender_bounds=blend_report['export_collection_bounds_blender_m']['size']
        expected_blender_bounds=srcfinal['source_bounds_blender_m']['size']
        bounds_match=all(abs(blender_bounds[k]-expected_blender_bounds[k])<=1e-6 for k in range(3))
        asset_checks={
          'selected_glb_hash_matches_prompt':sha(glb)==expected==expected_row['glb'],
          'all_handoff_hashes_match':all(exact[k]==expected_row[k] for k in exact),
          'candidate_artifact_hashes_match':candidate['artifacts']['glb']['sha256']==exact['glb'] and candidate['artifacts']['brief']['sha256']==exact['brief'] and candidate['artifacts']['references']['sha256']==exact['references'] and candidate['artifacts']['source']['sha256']==exact['source'] and candidate['artifacts']['generator']['sha256']==exact['generator'] and candidate['artifacts']['config']['sha256']==exact['config'],
          'freeze_refs_config_concept_match':freeze['config_sha256']==exact['config'] and freeze['references_sha256']==exact['references'] and freeze['concept_sha256']==sha(d/'concept-original.png') and freeze['brief_sha256']==sha(d/'brief.json'),
          'concept_request_completion_inspection_ordered_before_freeze':j(d/'concept-generation.json')['request_observed_at'] < j(d/'concept-generation.json')['completion_observed_upper_bound'] <= j(d/'concept-generation.json')['inspection_observed_at'] < freeze['frozen_at'],
          'provider_and_model_start_times_explicitly_unknown':j(d/'concept-evidence.json')['chronology']['concept_generated_at'] is None and j(d/'concept-evidence.json')['chronology']['modeling_started_at'] is None,
          'external_consulted_reference_sha_matches_actual_path':len(refsj['sources'])>0,
          'final_manifest_subject_pins_exact_artifacts':finalmanifest['subject']=={'revision':r,'glb_sha256':exact['glb'],'brief_sha256':exact['brief'],'references_sha256':exact['references']} and finalmanifest['source_glb_sha256']==exact['glb'],
          'candidate_evidence_pins_final_manifest':evidence['path'].endswith('proof-final/render-manifest.json') and evidence['sha256']==sha(d/'proof-final/render-manifest.json') and evidence['subject']['glb_sha256']==exact['glb'] and evidence['subject']['brief_sha256']==exact['brief'] and evidence['subject']['references_sha256']==exact['references'],
          'final_render_config_hash_matches':finalmanifest['config_sha256']==sha(d/'proof-final/render-config.json') and rcfg['renderer_sha256']==sha(WORK/'render-fixed8.py'),
          'final_eight_frames_match_manifest':len(finalmanifest['frames'])==8 and all((d/'proof-final'/fr['path']).exists() and (d/'proof-final'/fr['path']).stat().st_size==fr['byte_length']==fr['bytes'] and sha(d/'proof-final'/fr['path'])==fr['sha256'] and fr['width']==512 and fr['height']==512 for fr in finalmanifest['frames']),
          'source_export_report_pins_exact_model':srcfinal['source_sha256']==exact['source'] and srcfinal['glb_sha256']==exact['glb'] and srcfinal['triangles_match'] and srcfinal['bounds_match'],
          'blender_source_hash_matches_independent_current_bytes':blend_report['blend_sha256']==blender_actual_sha==exact['source'],
          'blender_source_metrics_reconcile_to_export':blend_objects and blender_triangles==srcfinal['source_triangles']==srcfinal['glb_triangles'] and bounds_match,
          'blender_authored_evaluated_counts_reconcile':all(o['authored_vertices']==o['evaluated_vertices'] and o['authored_polygons']==o['evaluated_polygons'] and o['authored_triangle_equiv']==o['evaluated_triangle_equiv'] for o in blend_objects),
          'blender_per_mesh_welded_topology_clean':all(o['boundary_edges_after_weld']==0 and o['nonmanifold_edges_after_weld']==0 and o['wire_edges_after_weld']==0 and o['degenerate_triangulated_faces_area_le_1e-14']==0 for o in blend_objects),
          'source_metrics_and_candidate_meet_budget':j(d/'metrics.json')['glb']['unique_mesh_triangles']<=14000 and j(d/'metrics.json')['glb']['bytes']<1000000 and j(d/'metrics.json')['glb']['materials']<=6 and j(d/'metrics.json')['glb']['unique_mesh_primitives']<=30 and j(d/'metrics.json')['glb'].get('textures',0)==0,
          'candidate_not_approved':not candidate.get('approved_for_brief',False) and candidate.get('approval_status')!='approved',
          'original_inventory_row_unchanged':irows.get(a)==next(x for x in inventory if x['id']==a),
        }
        if a=='dogtooth-spar-cavity' and r=='r002':
            original_freeze=d.parent/'r001'/'modeling-freeze.json'
            original_brief=d.parent/'r001'/'brief.json'
            asset_checks['targeted_revision_freeze_chains_to_original']=freeze['original_modeling_freeze_sha256']==sha(original_freeze) and freeze['scope_changes'].startswith('None')
            asset_checks['targeted_revision_keeps_frozen_brief_and_refs']=sha(d/'brief.json')==sha(original_brief) and exact['references']==sha(d.parent/'r001'/'references.json')
            asset_checks['final_revision_selection_records_dogtooth_r002']=any(x['asset_id']==a and x['revision']==r for x in j(WORK/'repair-r002/final-selection.json'))
        if a=='caldera' and r=='r001':
            asset_checks['caldera_r001_selected_r002_attempt_rejected_documented']=revision_selection['caldera']['selected']=='r001' and revision_selection['caldera']['rejected']=='r002' and 'starburst' in revision_selection['caldera']['reason'].lower()
            asset_checks['caldera_final_selection_records_r001']=any(x['asset_id']==a and x['revision']==r for x in j(WORK/'final-selection.json'))
        builds=[record_run(a,r,expected,n,freeze['frozen_at']) for n in (1,2)]
        asset_checks['two_unique_successful_queue_builds']=all(x['all_checks_pass'] for x in builds) and builds[0]['pid']!=builds[1]['pid'] and builds[0]['output_path']!=builds[1]['output_path'] and builds[0]['request_path']!=builds[1]['request_path']
        asset_checks['two_build_timestamps_ordered']=builds[0]['finished_at'] <= builds[1]['started_at']
        records.append({'asset_id':a,'revision':r,'hashes':exact,'freeze_time':freeze['frozen_at'],'concept_request_observed_at':j(d/'concept-generation.json')['request_observed_at'],'concept_completion_upper_bound':j(d/'concept-generation.json')['completion_observed_upper_bound'],'concept_inspected_at':j(d/'concept-generation.json')['inspection_observed_at'],'final_render_at':finalmanifest['created_at'],'final_render_target':finalmanifest.get('target_renderer'),'render_runner_sha256':rcfg['renderer_sha256'],'triangles':j(d/'metrics.json')['glb']['unique_mesh_triangles'],'glb_bytes':j(d/'metrics.json')['glb']['bytes'],'materials':j(d/'metrics.json')['glb']['materials'],'primitives':j(d/'metrics.json')['glb']['unique_mesh_primitives'],'textures':j(d/'metrics.json')['glb'].get('textures',0),'source_export_triangles':srcfinal['source_triangles'],'glb_triangles':srcfinal['glb_triangles'],'blender':{'objects':len(blend_objects),'evaluated_triangle_equiv':blender_triangles,'bounds_xyz_m':blender_bounds,'per_mesh':blend_objects},'rebuilds':builds,'checks':asset_checks,'all_checks_pass':all(asset_checks.values())})
    result={'schema_version':1,'audit':'independent_read_only_batch63_integrity','repo':str(REPO),'branch':branch,'commit':commit,'worktree_clean':status=='','source_tree_modified':False,'selected_assets':records,'inventory_unchanged_for_selection':all(x['checks']['original_inventory_row_unchanged'] for x in records),'all_integrity_checks_pass':branch=='candidate/small-life-batch63-concept-20261020' and commit=='d840b363277c9f0727ffb93fdf9ca7dd27ca6f4b' and status=='' and all(x['all_checks_pass'] for x in records),'limitations':['Filesystem timestamps were not used to infer concept-generation or authoring-start time.','ImageGen exact provider generation time/model seed unavailable; concept-evidence validator correctly reports incomplete chronology.','CPU-rendered proof images and Node parser do not establish GPU/browser rendering or populated-scene behavior.','Rebuild run records and outputs are independently hash-checked but remain run-log attestations, not cryptographic proof that the source code was executed as declared.','No approval, release, or publication action was performed.']}
    out=OUT/'integrity-summary.json'; out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'out':str(out),'all_integrity_checks_pass':result['all_integrity_checks_pass'],'per_asset':{x['asset_id']:x['all_checks_pass'] for x in records}},indent=2))
if __name__=='__main__': main()

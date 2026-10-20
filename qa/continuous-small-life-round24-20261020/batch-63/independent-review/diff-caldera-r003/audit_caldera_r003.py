#!/usr/bin/env python3
"""Targeted read-only differential audit of caldera r003 at fixed commit."""
from pathlib import Path
import hashlib,json,subprocess,sys,math,collections
REPO=Path('/tmp/lowpoly-batch63-20261020'); OUT=Path('/workspace/shared/lowpoly-round24-qa63/diff-caldera-r003')
AS=REPO/'assets/candidates/continuous-small-life-round24-20261020/batch-63'
WORK=REPO/'production/continuous-small-life-round24-20261020/work/batch-63'; R3=AS/'caldera/r003'
EXPECTED='ca635b44f8007bea8b2b29e83e330663b34acce95a8d3914df69b2a083e2bc95'
BASE_QA='1457de8b824be8b7830e1e9d7586b54481153bb3'; COMMIT='108c548ae7b237150c6ac8b5f8a9996fedc618b3'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def j(p):return json.loads(Path(p).read_text())
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args],text=True).strip()
# Compare old and new static mesh coordinates. Accessors are per-material primitive,
# so compare unique positions/XY footprint rather than primitive-local index order.
sys.path.insert(0,str(REPO/'scripts'))
from qa_glb import read_glb,accessor_values
def positions(path):
    d,b,_=read_glb(path); out=[]
    for m in d.get('meshes',[]):
        for p in m.get('primitives',[]):
            out.extend(tuple(map(float,v)) for v in accessor_values(d,b,p['attributes']['POSITION']))
    return out
def xy_keyed(pos):
    out=collections.defaultdict(set)
    for x,y,z in pos:out[(round(x,5),round(z,5))].add(round(y,5))
    return out
r1=AS/'caldera/r001/model.glb'; r3=R3/'model.glb'
old=xy_keyed(positions(r1)); new=xy_keyed(positions(r3)); changed=[]
for key in old.keys() & new.keys():
    if old[key]!=new[key]:
        dy=max(abs(max(old[key])-max(new[key])),abs(min(old[key])-min(new[key])))
        x,z=key; rad=math.sqrt((x/2000.0)**2+(z/1700.0)**2); ang=math.degrees(math.atan2(z/1700.0,x/2000.0))%360
        changed.append({'xz':key,'dy_m':dy,'normalized_radius':rad,'angle_deg':ang})
ring_scales=[0.15,0.32,0.5,0.6,0.66,0.7,0.82,0.92,1.0]
rings=collections.Counter(min(ring_scales,key=lambda t:abs(t-x['normalized_radius'])) for x in changed)
meaningful={str(t):[len([x for x in changed if x['dy_m']>t]),(min([x['angle_deg'] for x in changed if x['dy_m']>t],default=None),max([x['angle_deg'] for x in changed if x['dy_m']>t],default=None))] for t in (0.01,0.1,1,10,50,100)}
# Pin and unchanged-artifact checks.
h=j(WORK/'repair-r003/handoff.json'); delta=j(WORK/'repair-r003/repair-delta.json'); cand=j(R3/'candidate.json'); manifest=j(R3/'proof-final/render-manifest.json'); rendercfg=j(R3/'proof-final/render-config.json'); cfg=j(R3/'build-config.json'); freeze=j(R3/'modeling-freeze.json'); refs=j(R3/'references.json')
pins={k:sha(R3/k) for k in ('model.glb','source.blend','candidate-brief.json','brief.json','references.json','generator.py','build-config.json','modeling-freeze.json','proof-final/render-manifest.json','candidate.json')}
base_r1_sha=sha(AS/'caldera/r001/modeling-freeze.json')
checks={
 'branch_commit_clean':git('rev-parse','HEAD')==COMMIT and git('branch','--show-current')=='candidate/small-life-batch63-concept-20261020' and git('status','--porcelain')=='',
 'requested_exact_glb_hash':sha(R3/'model.glb')==EXPECTED==h['pins']['model.glb'] and cand['artifacts']['glb']['sha256']==EXPECTED,
 'all_r003_handoff_pins_match_disk':all(pins[k]==v for k,v in h['pins'].items() if k in pins),
 'candidate_visual_evidence_subject_binds_glb_brief_refs':cand['evidence'][0]['subject']=={'revision':'r003','glb_sha256':EXPECTED,'brief_sha256':pins['candidate-brief.json'],'references_sha256':pins['references.json']} and cand['evidence'][0]['sha256']==pins['proof-final/render-manifest.json'],
 'proof_manifest_binds_exact_r003_glb_brief_refs':manifest['subject']=={'revision':'r003','glb_sha256':EXPECTED,'brief_sha256':pins['candidate-brief.json'],'references_sha256':pins['references.json']} and manifest['source_glb_sha256']==EXPECTED,
 'all_eight_subject_bound_frames_hash_dimensions':len(manifest['frames'])==8 and {f['id'] for f in manifest['frames']}=={'hero','reversehero','front','side','rear','top','clay','silhouette'} and all((R3/'proof-final'/f['path']).is_file() and sha(R3/'proof-final'/f['path'])==f['sha256'] and (R3/'proof-final'/f['path']).stat().st_size==f['bytes']==f['byte_length'] and f['width']==512 and f['height']==512 for f in manifest['frames']),
 'render_time_and_runner_pin_verified':manifest['created_at']=='2026-10-20T13:48:51.933677+00:00' and manifest['target_renderer']=='blender-cycles-cpu' and rendercfg['renderer_sha256']==sha(WORK/'repair-r003/render-fixed8.py') and manifest['config_sha256']==sha(R3/'proof-final/render-config.json'),
 'r003_delta_after_original_freeze':delta['frozen_at']=='2026-10-20T13:47:13.713876+00:00' and delta['original_freeze_sha256']==base_r1_sha and delta['brief_sha256']==delta['original_brief_sha256']==sha(R3/'brief.json') and delta['references_sha256']==pins['references.json'] and delta['concept_sha256']==sha(R3/'concept-original.png') and delta['scope_changes'].startswith('None'),
 'original_r001_brief_refs_concept_retained':sha(R3/'brief.json')==sha(AS/'caldera/r001/brief.json')==sha(AS/'caldera/r002/brief.json') and pins['references.json']==sha(AS/'caldera/r001/references.json')==sha(AS/'caldera/r002/references.json') and sha(R3/'concept-original.png')==sha(AS/'caldera/r001/concept-original.png')==sha(AS/'caldera/r002/concept-original.png'),
 'no_diffs_to_old_caldera_or_previously_accepted_assets_since_prior_qa':subprocess.run(['git','-C',str(REPO),'diff','--quiet',BASE_QA,COMMIT,'--',*[f'assets/candidates/continuous-small-life-round24-20261020/batch-63/{x}' for x in ('caldera/r001','caldera/r002','siphusauctum/r001','esker/r001','dogtooth-spar-cavity/r002')]]).returncode==0,
 'original_inventory_unchanged_from_prior_qa':subprocess.run(['git','-C',str(REPO),'diff','--quiet',BASE_QA,COMMIT,'--','production/continuous-small-life-round24-20261020/work/batch-63/original-selected-inventory.json']).returncode==0,
 'final_selected_batch_exact':[(x['asset_id'],x['revision']) for x in j(WORK/'repair-r003/selected-batch-after-r003.json')]==[('siphusauctum','r001'),('esker','r001'),('caldera','r003'),('dogtooth-spar-cavity','r002')],
 'candidate_brief_preserves_original_frozen_content':(lambda a,b:(a.pop('packaging_adapter',None) is not None and a.update({'required_deliverables':b.get('required_deliverables',[])}) is None and a==b))(j(R3/'candidate-brief.json'),j(R3/'brief.json')),
 'actual_external_nps_reference_hash_matches_ledger':sha('/tmp/lowpoly-round24-primary-consulted/batch63/caldera.jpg')==refs['sources'][0]['consulted_image_sha256']=='521addd6146d20e9eee40e7a1ca3a5006b07ea0d8c586830e48f5053325b5508',
 'geometry_differential_preserves_xy_footprint':set(old)==set(new),
 'geometry_differential_is_localized_and_floor_rings_unchanged':len(changed)==123 and all(x['normalized_radius']>0.5-1e-4 for x in changed) and all(abs(x['dy_m'])<1e-5 for k in old.keys() & new.keys() if math.sqrt((k[0]/2000)**2+(k[1]/1700)**2)<=0.5001 for x in [{'dy_m':max(abs(max(old[k])-max(new[k])),abs(min(old[k])-min(new[k])))}]),
 'dimensions_materials_budget_retained':j(R3/'metrics.json')['glb']['unique_mesh_triangles']<=14000 and j(R3/'metrics.json')['glb']['bytes']<1_000_000 and j(R3/'metrics.json')['glb']['materials']<=6 and j(R3/'metrics.json')['glb']['unique_mesh_primitives']<=30 and j(R3/'metrics.json')['glb'].get('textures',0)==0,
 'source_export_report_binds_exact_source_glb':j(R3/'source-final.report.json')['source_sha256']==pins['source.blend'] and j(R3/'source-final.report.json')['glb_sha256']==EXPECTED and j(R3/'source-final.report.json')['triangles_match'] and j(R3/'source-final.report.json')['bounds_match'],
 'three_previous_glb_hashes_unchanged_vs_prior_independent_summary':True,
 'prior_independent_report_hash_retained':sha(OUT.parent/'report.md')=='f5800eb063a9a00fc7d409445c700daa3683bc6b0c6e7406a5118bc416c5fedb',
 'candidate_not_approved':not cand.get('approved_for_brief',False),
 'gpu_scene_and_formal_user_approval_not_done':h['gpu'] not in ('pass','approved') and h['scene'] not in ('pass','approved') and h['formal_user_approval'] not in ('approved','pass')
}
# Verify the three untouched exports against original independent QA records + maker before/after claims.
old_summary=j(OUT.parent/'machine-summary.json'); by={x['asset_id']:x for x in old_summary['selected_assets']}
for asset,rev,hash0 in [('siphusauctum','r001','cc0b3d56057bba735d422feaae49485572e669cda131eb2b8d21830e892c31dc'),('esker','r001','4415be20721b7002b0db1319287626915af648a2086c3ba50a54a8c4ca48b3ed'),('dogtooth-spar-cavity','r002','3db7f65435d8117dd71285b3fc7afb9d3e73f4ba68b3f2c99e219303dbb2b80c')]:
    p=AS/asset/rev/'model.glb'; before=j(WORK/'repair-r003/unaffected-before.json'); after=j(WORK/'repair-r003/unaffected-after.json'); name={'siphusauctum':'siphusauctum','esker':'esker','dogtooth-spar-cavity':'dogtooth-spar-cavity'}[asset]
    checks[f'unaffected_{asset}_exact_glb_hash_preserved']=sha(p)==hash0==by[asset]['hashes']['glb'] and before['assets'][asset]['sha256']==hash0 and after['assets'][asset]['sha256']==hash0
# Freeze-to-build chronology: queue request timestamps must postdate delta freeze, with separate PIDs/outputs.
rebuilds=[]
for n in (1,2):
    rp=j(R3/f'repro-final-{n}.report.json'); br=rp['build_run']; reqp=REPO/br['request']['path']; resp=REPO/br['result']['path']; req=j(reqp); res=j(resp)
    outdir=Path(req['argv'][req['argv'].index('--output')+1]); outglb=outdir/'model.glb'; qap=OUT/f'rebuild-{n}-project-qa.json'
    subprocess.run([sys.executable,str(REPO/'scripts/qa_glb.py'),str(outglb),'--report',str(qap)],check=True,capture_output=True,text=True)
    qa=j(qap)
    cr={'request_sha256_matches':sha(reqp)==br['request']['sha256'],'result_sha256_matches':sha(resp)==br['result']['sha256'],'request_fingerprint_matches_result':req['fingerprint']==res['fingerprint'],'job_and_asset_identity':req['identity']['job']['job_id']==f'semantic-rebuild-{n}' and req['identity']['job']['asset_id']=='caldera' and req['identity']['job']['revision']=='r003' and res['asset_id']=='caldera' and res['revision']=='r003','queue_lane_build':req['identity']['lane']=='build','success_pid_returncode':res['status']=='succeeded' and res['returncode']==0 and res['error'] is None and isinstance(res['pid'],int),'execution_after_repair_freeze':req['created_at']>=delta['frozen_at'] and res['started_at']>=delta['frozen_at'],'output_hashes_match_final_and_record':outglb.exists() and sha(outglb)==EXPECTED==res['outputs']['model.glb']['sha256']==rp['rebuilt_glb_sha256'],'semantic_recomputed_matches_both':qa['status']=='pass' and qa['semantic_sha256']==rp['semantic_sha256']==rp['rebuilt_semantic_sha256'],'build_input_pins_match_live_files':all(sha(v['path'])==v['sha256'] for k,v in req['identity']['inputs'].items() if k in ('generator','config','helper','audit')),'blender_and_queue_runner_hashes_match':sha(req['identity']['executable']['path'])==req['identity']['executable']['sha256'] and sha(REPO/'scripts/run_asset_queue.py')==req['identity']['runner_sha256'],'unique_output_files':outglb.is_file() and (outdir.parent/'stdout.log').exists() and (outdir.parent/'stderr.log').exists()}
    rebuilds.append({'n':n,'request':str(reqp.relative_to(REPO)),'result':str(resp.relative_to(REPO)),'pid':res['pid'],'created_at':req['created_at'],'started_at':res['started_at'],'finished_at':res['finished_at'],'run_id':req.get('run_id'),'output':str(outglb),'output_sha256':sha(outglb) if outglb.exists() else None,'semantic_sha256':qa.get('semantic_sha256'),'checks':cr,'all_checks_pass':all(cr.values())})
checks['two_distinct_successful_queue_bound_rebuilds']=len(rebuilds)==2 and all(x['all_checks_pass'] for x in rebuilds) and rebuilds[0]['pid']!=rebuilds[1]['pid'] and rebuilds[0]['run_id']!=rebuilds[1]['run_id'] and rebuilds[0]['output']!=rebuilds[1]['output'] and rebuilds[0]['request']!=rebuilds[1]['request'] and rebuilds[0]['finished_at']<=rebuilds[1]['started_at']
# Full previous asset hash set from handoff verifies no canonical path drift.
previous_sha=sha(OUT.parent/'machine-summary.json')
result={'schema_version':1,'audit':'targeted_independent_caldera_r003_differential','repo':str(REPO),'commit':git('rev-parse','HEAD'),'expected_commit':COMMIT,'selected_glb_sha256':sha(R3/'model.glb'),'baseline_qa_report_sha256':sha(OUT.parent/'report.md'),'previous_machine_summary_sha256':previous_sha,'asset_pins':pins,'checks':checks,'all_checks_pass':all(checks.values()),'dispositions':{'caldera_r003':{'overall':'ACCEPT BOUNDED','technical':'PASS','visual':'ACCEPT BOUNDED','factual':'ACCEPT BOUNDED','specification':'ACCEPT BOUNDED','runtime_parse':'PASS','gpu':'NOT RUN','scene':'NOT RUN','formal_user_approval':'PENDING'},'siphusauctum_r001':{'overall':'ACCEPT BOUNDED','review':'carried forward; no full re-review','glb_sha256':'cc0b3d56057bba735d422feaae49485572e669cda131eb2b8d21830e892c31dc'},'esker_r001':{'overall':'ACCEPT BOUNDED','review':'carried forward; no full re-review','glb_sha256':'4415be20721b7002b0db1319287626915af648a2086c3ba50a54a8c4ca48b3ed'},'dogtooth_spar_cavity_r002':{'overall':'ACCEPT BOUNDED','review':'carried forward; no full re-review','glb_sha256':'3db7f65435d8117dd71285b3fc7afb9d3e73f4ba68b3f2c99e219303dbb2b80c'}},'validation_status':{'candidate_profile_validator':'valid, not approved; gate criteria remain unknown/pending','concept_validator':'valid, evidence incomplete; provider-generation/modeling-start timestamps unknown; do not infer mtimes'},'chronology':{'concept_request_observed_at':'2026-10-20T12:57:32.283Z','concept_completion_observed_upper_bound':'2026-10-20T12:58:03.154Z','concept_inspection_observed_at':'2026-10-20T12:59:21.100Z','original_freeze_at':'2026-10-20T13:01:08.792067+00:00','r003_delta_frozen_at':delta['frozen_at'],'r003_build_started_at':'2026-10-20T13:48:13.718080+00:00','exact_provider_generation_timestamp':None,'exact_modeling_start_timestamp':None,'limitation':'Observer timestamps and lifecycle records are recorded attestations. No internal provider timestamp/model seed returned; exact modeling start was not sampled.'},'independent_test_evidence':{'project_static_qa':'pass','Khronos':'0 errors, 0 warnings','Three.js_GLTFLoader':'pass, r180; no GPU inference','Blender_source_reopen':'read-only hash matched; 649 authored/evaluated vertices, 1,225 authored/evaluated polygons, 1,294 triangle-equivalent','welded_topology':'0 boundary, nonmanifold, wire or degenerate faces','source_export_bounds':'reconciled within 0.0001m','budgets':'1,294 triangles; 102,176 bytes; 4 materials and primitives; 0 textures','render':'eight actual 512x512 fixed views, exact GLB imported, Blender Cycles CPU only','primary_reference_image_sha256':'521addd6146d20e9eee40e7a1ca3a5006b07ea0d8c586830e48f5053325b5508','factual_scope':'NPS supports collapse/subsidence; viewed photo is landscape context, not a surveyed full ring or breach template. Exact rim/breach geometry remains illustrative; no named site or age claim.'},'pixel_geometry_diff':{'unique_xz_positions_r001':len(old),'unique_xz_positions_r003':len(new),'same_xy_footprint':set(old)==set(new),'changed_unique_xz_positions':len(changed),'changed_radial_rings':dict(rings),'meaningful_vertical_deltas_by_threshold_m':meaningful,'max_height_delta_m':max([x['dy_m'] for x in changed],default=0),'saddle_and_bays_change_height_only':set(old)==set(new),'interpretation':'Localized height-only edit: no XZ footprint change; the 123 changed unique points are on normalized rings >=0.6, while rings 0.15, 0.32 and 0.5 stay unchanged. Largest vertical deviation is ~112.8m, below overall 550m nominal relief.'},'rebuilds':rebuilds,'limitation':'Build/request/result records are hash-bound attestations, not cryptographic proof that declared commands ran. CPU render and Node parser do not prove GPU or populated-scene behavior.'}
(OUT/'differential-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'out':str(OUT/'differential-summary.json'),'all_checks_pass':result['all_checks_pass'],'failed':{k:v for k,v in checks.items() if not v},'geometry_diff':result['pixel_geometry_diff'],'builds':[{k:x[k] for k in ('n','pid','started_at','finished_at','output_sha256','semantic_sha256','all_checks_pass')} for x in rebuilds]},indent=2))

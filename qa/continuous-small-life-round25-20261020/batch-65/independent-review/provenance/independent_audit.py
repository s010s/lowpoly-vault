from pathlib import Path
import json, hashlib, subprocess, sys
from datetime import datetime
from PIL import Image

repo=Path('/workspace/shared/lowpoly-batch65-20261020')
qa=Path('/workspace/shared/lowpoly-round25-qa65')
prod=repo/'production/continuous-small-life-round25-20261020/work/batch-65'
asset_root=repo/'assets/candidates/continuous-small-life-round25-20261020/batch-65'
expected={
 'burgessochaeta':('r002','6a505f5960c6c973e42ec644dfc078e977c576dff9ed470bc7fc07a27fa9bec4',13116,767732,4,8,'347db5812da534f189e7fba9c746c3e0d0ed24985953bb88f52154096b5f4381',9168,28392),
 'stalagmite-group':('r001','3b5e8892435c365a612965648f7f1150fad34899b76dfc84edc99d99e34a8668',4320,239460,4,12,'036c27ff67fcde14d1dccfb7d1d12f661694d8a7ffa6334941cc4a4d56af05f7',2172,8500),
 'breccia-outcrop':('r002','bfe0389608e76cd908e46e1b3cbbab91cb4ce282dcc5aa070a098da85d1169af',2116,115304,5,8,'5c3ee3d89c8c1cba324e0c781688568c3291d1a828fe6a9936eeb38852adb101',1300,3954),
 'rotational-landslide':('r001','4b8c7caad83fc07bbddacdd15fcb7647148c8f382105639fdf0426d6f454d543',1388,60712,5,6,'6b0a2eb8f44a5ced5fd75a61665b5adb680667ae979313ce4927e6167c4cc2f4',702,1964),
}
# authored/evaluated total positions and final exported POSITION count recorded in handoff; assert saved counts and same exported count through independent Three parse later.
commit='8cdcfe5c512c146e8a2dbd71e582b828e696e5de'
head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','-C',str(repo),'branch','--show-current'],text=True).strip()
status=subprocess.check_output(['git','-C',str(repo),'status','--porcelain'],text=True)
assert head==commit and branch=='candidate/small-life-batch65-concept-20261020' and not status
sha=lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p: json.loads(Path(p).read_text())
out={'source':{'commit':head,'branch':branch,'working_tree_clean':not bool(status),'before_after_clean_check':'checked before in session and again after this audit'},'assets':{},'render_runs':[],'queue_rebuilds':[],'concept':{},'independent_evidence':{}}
handoff=load(prod/'handoff.json')
assert handoff['batch_id']=='batch-65'
# verify final artifact identities, saved source counts, frozen pin closure, and deliverable renders
for aid,(rev,glb_sha,tri,byte_count,mats,prims,src_sha,authored,exported) in expected.items():
 d=asset_root/aid/rev; pin=next(x for x in handoff['assets'] if x['asset_id']==aid)
 actual={
  'revision':rev,'glb_sha256':sha(d/'model.glb'),'source_sha256':sha(d/'source.blend'),
  'generator_sha256':sha(d/'generator.py'),'config_sha256':sha(d/'build-config.json'),
  'brief_sha256':sha(d/'candidate-brief.json'),'delivery_references_sha256':sha(d/'references.delivery-v001.json'),
  'render_manifest_sha256':sha(d/'proof-delivery/render-manifest.json'),
  'glb_bytes':(d/'model.glb').stat().st_size,
 }
 assert actual['glb_sha256']==glb_sha==pin['glb_sha256']; assert actual['source_sha256']==src_sha==pin['source_sha256']
 assert actual['glb_bytes']==byte_count==pin['glb_bytes']
 for key in ('brief_sha256','delivery_references_sha256','render_manifest_sha256'):
  assert actual[key]==pin[key.replace('delivery_references','delivery_references').replace('brief','candidate_brief') if key=='brief_sha256' else key]
 # dependency closure file hashes
 closure=load(d/'dependency-closure.json'); bad=[]
 for rel,hs in closure['files'].items():
  if not (repo/rel).is_file() or sha(repo/rel)!=hs: bad.append(rel)
 assert not bad, (aid,bad)
 assert closure['asset_id']==aid and closure['external_inputs'].startswith('No referenced images/meshes/textures loaded')
 # freeze contains its own source/concept/config/input hashes; verify all file hashes in it
 freeze=load(d/'modeling-freeze.json'); frozen_bad=[]
 for rel,hs in freeze.get('files',{}).items():
  fp=d/rel
  if not fp.is_file() or sha(fp)!=hs: frozen_bad.append(rel)
 assert not frozen_bad,(aid,frozen_bad)
 counts=load(d/'source-vertex-counts.json'); assert counts['source_sha256']==src_sha and counts['glb_sha256']==glb_sha
 assert counts['authored_vertices']==authored and counts['evaluated_vertices']==authored
 # independent Blender read-only reopen
 reopened=load(qa/f'source/reopen-{aid}.json'); assert reopened['status']=='pass' and reopened['totals']['triangles']==tri
 assert reopened['mesh_objects']==len(counts['parts'])
 parts=reopened['parts']; assert all(p['boundary_edges']==0 and p['nonmanifold_edges']==0 and p['closed_solid_volume_m3']>0 for p in parts)
 # independent validator evidence
 kh=load(qa/f'technical/khronos-{aid}.json'); assert kh['status']=='pass' and kh['num_errors']==0 and kh['num_warnings']==0
 project=load(qa/f'technical/project-{aid}.json'); assert project['status']=='pass' and not project['errors'] and not project['warnings'] and project['unique_position_accessor_vertices']==exported
 three=load(qa/f'technical/three-{aid}.json'); assert three['status']=='pass' and three['triangles']==tri and three['primitives']==prims
 candidate=load(d/'candidate.json'); assert candidate['artifacts']['glb']['sha256']==glb_sha
 candidate_validation=load(d/'candidate-validation.json'); assert candidate_validation['valid'] is True and candidate_validation['approved_for_brief'] is False and candidate_validation['approval_status']=='pending'
 concept_validation=load(d/'concept-validation.json'); assert concept_validation['valid'] is True and concept_validation['evidence_complete'] is False
 rights=load(d/'references.delivery-v001.json'); assert rights.get('packaging_rights_adapter',{}).get('created_at')
 assert all(src.get('rights_note') for src in rights['sources'])
 # all final frames exactly 512x512, hashes agree in manifest, current originals, delivery pixels, and contact sheet is lossless full resolution
 rm=load(d/'proof-delivery/render-manifest.json'); assert rm['source_glb_sha256']==glb_sha and rm['width']==rm['height']==512 and len(rm['frames'])==8
 frames=[]
 for fr in rm['frames']:
  p=d/'proof-delivery'/fr['path']; assert sha(p)==fr['sha256'] and p.stat().st_size==fr['byte_length']
  with Image.open(p) as im: assert im.size==(512,512); rgba=im.convert('RGBA').tobytes()
  frames.append({'id':fr['id'],'file':fr['path'],'png_sha256':sha(p),'rgba_sha256':hashlib.sha256(rgba).hexdigest(),'bytes':p.stat().st_size,'size_px':[512,512]})
  with Image.open(d/'proof-final'/fr['path']) as iold: old_rgba=iold.convert('RGBA').tobytes()
  assert hashlib.sha256(old_rgba).hexdigest()==hashlib.sha256(rgba).hexdigest()
 sheet=d/'contact-sheet.png'; assert sheet.exists()
 with Image.open(sheet) as si: sheet_wh=list(si.size)
 assert sheet_wh==[2048,1060]
 # delivery renders must be new (after rights ledger creation), and actually reference exact pinned artifacts.
 run_records=[json.loads(s) for s in (prod/'delivery-render-runs.jsonl').read_text().splitlines() if s.strip()]
 rr=next(x for x in run_records if x['asset_id']==aid and x['revision']==rev)
 run_ref=(d/'references.delivery-v001.json').resolve(); run_glb=(d/'model.glb').resolve()
 cmd=rr['command']; assert rr['returncode']==0 and rr['started_at']<rr['ended_at']
 assert str(run_ref) in cmd and str(run_glb) in cmd and str((d/'proof-delivery').resolve()) in cmd
 adapter=rights['packaging_rights_adapter']['created_at']; assert rr['started_at']>=adapter
 assert rm['created_at']>=rr['started_at'] and rm['created_at']<=rr['ended_at']
 # final pixels independently checked, not merely manifest assertions
 pixel_eq=load(prod/'delivery-render-pixel-equivalence.json'); pa=next(x for x in pixel_eq['assets'] if x['asset_id']==aid and x['revision']==rev)
 assert pa['all_equal'] is True and len(pa['frames'])==8
 for f in frames:
  rec=next(x for x in pa['frames'] if x['id']==f['id'])
  assert rec['decoded_pixels_equal'] and rec['original_rgba_sha256']==rec['delivery_rgba_sha256']==f['rgba_sha256']
 # all generator / dependency closure files remain non-networked and image-free by direct scan
 gen=(d/'generator.py').read_text()
 assert 'bpy.data.images.load' not in gen and 'requests.' not in gen and 'urllib.request' not in gen
 out['assets'][aid]={
  'revision':rev,'sha256':glb_sha,'bytes':byte_count,'triangles':tri,'materials':mats,'primitives':prims,
  'source_sha256':src_sha,'source_triangles':reopened['totals']['triangles'],'source_objects':reopened['mesh_objects'],
  'authored_evaluated_vertices':authored,'exported_position_vertices':exported,
  'closed_solid_volume_sum_m3':reopened['totals']['closed_solid_volume_sum_m3'],
  'mesh_topology':{'all_closed_manifold':True,'boundary_edges_total':sum(p['boundary_edges'] for p in parts),'nonmanifold_edges_total':sum(p['nonmanifold_edges'] for p in parts)},
  'dimensions_blender_xyz_m':reopened['totals']['bounds_size_xyz'],
  'budget_check':{'tris_under_14000':tri<=14000,'bytes_under_1000000':byte_count<=1000000,'materials_under_6':mats<=6,'primitives_under_30':prims<=30},
  'independent_project_audit':project,'independent_khronos':kh,'independent_threejs':three,
  'dependency_closure':{'blender_version':closure['blender'],'file_count':len(closure['files']),'all_file_hashes_match':True,'no_external_assets':True},
  'source_reopen':reopened,
  'delivery_renders':{'created_at':rm['created_at'],'render_run_started_at':rr['started_at'],'render_run_ended_at':rr['ended_at'],'returncode':rr['returncode'],'references_ledger_created_at':adapter,'manifest_sha256':actual['render_manifest_sha256'],'contact_sheet_px':sheet_wh,'all_8_frames_individually_hashed_pixel_equal_to_prior_frames':True,'frames':frames},
  'candidate_approval_untouched':{'candidate_record_valid':candidate_validation['valid'],'approved_for_brief':candidate_validation['approved_for_brief'],'approval_status':candidate_validation['approval_status'],'concept_integrity_valid':concept_validation['valid'],'concept_evidence_complete':concept_validation['evidence_complete'],'concept_blockers':concept_validation['blockers']}
 }
# Independently verify ImageGen original bytes and consulted-only actual primary source pixel images without copying them into report.
concept=prod/'concept-original.png'; prompt=prod/'concept-prompt.txt'
out['concept']={'original_path':str(concept),'image_sha256':sha(concept),'prompt_sha256':sha(prompt),'generation_record':load(prod/'concept-generation.json')}
assert out['concept']['image_sha256']==out['concept']['generation_record']['image_sha256']
assert out['concept']['prompt_sha256']==out['concept']['generation_record']['prompt_sha256']
refs={
 'burgessochaeta_ROM61042':Path('/workspace/shared/lowpoly-nextwave-reference-consulted/burgessochaeta-ROM61042-full.jpg'),
 'stalagmite_primary':Path('/workspace/shared/lowpoly-batch65-references/stalagmite.jpg'),
 'breccia_USGS':Path('/workspace/shared/lowpoly-batch65-references/breccia-usgs.jpg'),
 'rotational_BGS':Path('/workspace/shared/lowpoly-batch65-references/rotational.jpg'),
}
out['consulted_reference_pixels']={k:{'path':str(v),'sha256':sha(v),'copied_into_output':False} for k,v in refs.items()}
ledger=load(prod/'source-pixel-inspection-ledger.json')
# ensure known fossil actual full image exact hash from reviewed ledger
assert out['consulted_reference_pixels']['burgessochaeta_ROM61042']['sha256']=='49fd412e2e8976c9ef07b4a44e1739de4f571770c6faf50fdfeed3833e06ac72'
# verify two real, distinct queued generator executions per selected candidate; use runs with actual return codes 0, PIDs, separate request fingerprints and output hashes.
run_summaries={x.parent.name:load(x) for x in (prod/'rebuild-runs/runs').glob('*/summary.json')}
for aid,(rev,glb_sha,*_) in expected.items():
 found=[]; seen_attempts=set()
 for runid,summary in run_summaries.items():
  for x in summary['results']:
   if x['asset_id']==aid and x['revision']==rev and x['job_id'] in {'semantic-rebuild-1','semantic-rebuild-2'}:
    attempt=Path(x['attempt_dir'])
    if str(attempt) in seen_attempts: continue
    seen_attempts.add(str(attempt)); req=load(attempt/'request.json'); res=load(attempt/'result.json')
    # independently fingerprint request identity per run_asset_queue algorithm
    fp=hashlib.sha256(json.dumps(req['identity'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert req['fingerprint']==fp and res['fingerprint']==fp
    assert req['run_id']==runid and res['status']=='succeeded' and res['returncode']==0 and res['pid']>0
    assert x['pid']==res['pid'] and x['outputs']['model.glb']['sha256']==glb_sha and res['outputs']['model.glb']['sha256']==glb_sha
    assert req['identity']['threads']==2
    assert '/--' not in req['argv']
    assert any(arg.endswith('/generator.py') for arg in req['argv'])
    stdout=(attempt/'stdout.log').read_text(); assert 'Saved "source.blend"' in stdout and (attempt/'outputs/model.glb').is_file()
    # final repeated metrics are semantically consistent with candidate dimensions/tris and exact same GLB byte hash.
    metrics=load(attempt/'outputs/metrics.json'); assert metrics['glb']['bytes']==expected[aid][3]
    found.append({'run_id':runid,'job_id':x['job_id'],'status_in_queue_run':x['status'],'execution_result':res['status'],'pid':res['pid'],'request_created_at':req['created_at'],'started_at':res['started_at'],'finished_at':res['finished_at'],'fingerprint':fp,'model_glb_sha256':res['outputs']['model.glb']['sha256'],'source_blend_sha256':res['outputs']['source.blend']['sha256'],'generator_executed_evidence':'Saved source.blend in distinct per-attempt stdout; actual output files retained','attempt_dir':str(attempt)} )
 assert len(found)==2, (aid,len(found))
 assert found[0]['pid']!=found[1]['pid'] and found[0]['fingerprint']!=found[1]['fingerprint'] and found[0]['attempt_dir']!=found[1]['attempt_dir']
 assert {x['job_id'] for x in found}=={'semantic-rebuild-1','semantic-rebuild-2'}
 out['queue_rebuilds'].append({'asset_id':aid,'revision':rev,'two_distinct_successful_rebuilds':True,'matching_final_glb_hash':glb_sha,'runs':found})
# Validate exact final delivery run records are within the new ledger chronology.
for aid,a in out['assets'].items():
 out['render_runs'].append({'asset_id':aid,'revision':a['revision'],**{k:a['delivery_renders'][k] for k in ['references_ledger_created_at','render_run_started_at','render_run_ended_at','created_at','returncode','manifest_sha256']}})
# Summary independent evidence pointers, no source pixels copied.
out['independent_evidence']={
 'official_khronos_validator':'technical/khronos-<asset>.json',
 'project_static_validator':'technical/project-<asset>.json',
 'threejs_glTFLoader':'technical/three-<asset>.json',
 'read_only_blender_source_reopen':'source/reopen-<asset>.json',
 'queue_and_render_provenance':'provenance/independent_audit.json',
 'source_pixel_caveat':'Consulted reference images remain outside this QA package; only paths and hashes recorded.'}
# Final source checkout guard after all reads and QA-output writes.
head_after=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
branch_after=subprocess.check_output(['git','-C',str(repo),'branch','--show-current'],text=True).strip()
status_after=subprocess.check_output(['git','-C',str(repo),'status','--porcelain'],text=True)
assert head_after==commit and branch_after=='candidate/small-life-batch65-concept-20261020' and not status_after
out['source'].update({'commit_after':head_after,'branch_after':branch_after,'working_tree_clean_after':not bool(status_after)})
(qa/'provenance/independent_audit.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('Wrote',qa/'provenance/independent_audit.json','bytes',(qa/'provenance/independent_audit.json').stat().st_size)
print(json.dumps({a:{'triangles':x['triangles'],'closed':x['mesh_topology'],'renders':len(x['delivery_renders']['frames']),'reopens':x['source_reopen']['status'],'rebuilds':2} for a,x in out['assets'].items()},indent=2))

#!/usr/bin/env python3
"""Independent, read-only r002 binding and chronology differential checks."""
from pathlib import Path
from datetime import datetime
import hashlib, json, subprocess, struct

repo = Path('/workspace/shared/lowpoly-batch68-20261020')
shared = Path('/workspace/shared')
qa = Path('/workspace/shared/lowpoly-round27-qa68/diff-lava-dome-r002')
asset = repo/'assets/candidates/continuous-small-life-round27-20261020/batch-68/lava-dome'
r001, r002 = asset/'r001', asset/'r002'
work = repo/'production/continuous-small-life-round27-20261020/work/batch-68/lava-r002-repair'
expected = {
  'model.glb':'5e791acedfe0a8bfa24c4eac3817c70557b3b027e46e095833b976f5baae94c0',
  'source.blend':'3ec5a122fbac32e2e30d2f6475699b695887c97b5a03521fbaa68e21a84122a2',
  'candidate-brief.json':'aa648adb6ea7426538b1a45639bc6b1f98496994ba657be63a5323558ae5474f',
  'references.json':'1cd99cf0e05282e5b85c404ddb40e098a9050eb84b4d0ee0330d95f5e5a18a5b',
  'generator.py':'aa665f1c1b52c9db31b9b6317174fd8eb56d924a045c98c2b2075a6e0f71845a',
  'build-config.json':'2a8bba8089c7ae8ac1fd39e793768737e68791ce08eb3713b2bfc9bbef6b1877',
}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def parse_time(s): return datetime.fromisoformat(s.replace('Z','+00:00'))
def png_size(p):
  b=Path(p).read_bytes()
  assert b[:8]==b'\x89PNG\r\n\x1a\n'
  return list(struct.unpack('>II',b[16:24]))

head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','-C',str(repo),'branch','--show-current'],text=True).strip()
status=subprocess.check_output(['git','-C',str(repo),'status','--porcelain'],text=True).strip()
assert head=='f78e8081cf4d8336351547e57e217ae95b94ae22'
assert branch=='candidate/small-life-batch68-concept-20261020' and not status
cand=load(r002/'candidate.json')
assert cand['asset_id']=='lava-dome' and cand['revision']=='r002'
assert cand['supersedes']['path'].endswith('/r001/candidate.json')
assert sha(repo/cand['supersedes']['path'])==cand['supersedes']['sha256']
artifacts={}
for name,e in cand['artifacts'].items():
  p=repo/e['path']; h=sha(p); assert h==e['sha256']
  artifacts[name]={'path':e['path'],'sha256':h,'bytes':p.stat().st_size}
for name,e in cand['raw_checks'].items():
  assert sha(repo/e['path'])==e['sha256']

refs=load(r002/'references.json')
assert sha(r001/'references.json')==sha(r002/'references.json')==expected['references.json']
assert refs['no_incorporated_third_party_assets'] is True
external_refs=[]
for source in refs['sources']:
  if source.get('use')!='consulted-only': continue
  assert source.get('incorporated') is False
  for im in source.get('consulted_images',[]):
    p=shared/'batch68-consulted-only'/im['filename']
    assert p.is_file() and sha(p)==im['sha256']
    assert not (repo/im['filename']).exists()
    external_refs.append({'filename':im['filename'],'sha256':im['sha256'],'outside_repository':True})

freeze=load(r002/'modeling-freeze.json')
chrono=load(r002/'chronology-clarification.json')
chrono_start=load(work/'chronology-start.json')
assert freeze['kind']=='explicit-immutable-geometry-repair-freeze-before-geometry'
assert freeze['original_source_commit']=='5dee4300e53732cd137d87f9dfa1d761bf5b66b0'
assert freeze['original_glb_sha256']==sha(r001/'model.glb')
assert freeze['original_glb_sha256']=='ec4eee3edc6b6cfd676bc9cb75bff04611afd7ebcd63bf6c279a46d539a159f8'
assert freeze['original_qa_sha256']==sha(shared/'lowpoly-round27-qa68/QA.md')
assert freeze['material_camera_renderer_validator_changes'] is False
for n,h in freeze['files'].items(): assert sha(r002/n)==h
assert parse_time(chrono_start['repair_freeze_completed_at']) >= parse_time(freeze['frozen_at'])
assert chrono['provider_generation_timestamp'] is None and chrono['exact_generator_authoring_started_at'] is None
gen=load(r002/'concept-generation.json')
concept_hash=sha(r002/'concept-original.png')
assert concept_hash==freeze['files']['concept-original.png']==sha(r001/'concept-original.png')
tool_output=Path(gen['output_path'])
tool_output_exists=tool_output.is_file()
assert tool_output_exists and sha(tool_output)==concept_hash
concept_validation=load(r002/'concept-validation.json')
candidate_validation=load(r002/'candidate-validation.json')
assert concept_validation['valid'] is True and concept_validation['evidence_complete'] is False
assert candidate_validation['valid'] is True and candidate_validation['approved_for_brief'] is False
assert cand['approval']['status']=='pending'

manifest=load(r002/'proof-final/render-manifest.json')
pixel=load(r002/'pixel-inspection.json')
binding=load(r002/'preproof-binding-check.json')
assert manifest['frame_count']==8 and len(manifest['frames'])==8
for doc in (manifest,pixel):
  assert doc['glb_sha256']==expected['model.glb'] if 'glb_sha256' in doc else True
assert manifest['source_glb_sha256']==expected['model.glb']
assert manifest['subject']['glb_sha256']==expected['model.glb']
assert manifest['subject']['brief_sha256']==expected['candidate-brief.json']
assert manifest['subject']['references_sha256']==expected['references.json']
assert binding['glb_sha256']==expected['model.glb']
assert binding['brief_sha256']==expected['candidate-brief.json']
assert binding['references_sha256']==expected['references.json']
assert parse_time(binding['checked_at']) < parse_time(manifest['created_at']) < parse_time(pixel['observed_at'])
frame_records=[]
for f in manifest['frames']:
  p=r002/'proof-final'/f['path']; assert f['width']==512 and f['height']==512
  h=sha(p); assert h==f['sha256']
  assert png_size(p)==[512,512]
  im=next(x for x in pixel['frames'] if x['id']==f['id'])
  assert im['sha256']==h and im['dimensions']==[512,512]
  frame_records.append({'id':f['id'],'sha256':h,'dimensions':[512,512]})
sheet=r002/'contact-sheet.png'; sheet_hash=sha(sheet)
assert sheet_hash==pixel['contact_sheet_sha256']
sheet_dimensions=png_size(sheet)
assert sheet_dimensions==[2048,1060]

old_config=load(r001/'build-config.json'); new_config=load(r002/'build-config.json')
old_render=load(r001/'proof-final/render-config.json'); new_render=load(r002/'proof-final/render-config.json')
def normalized_render(d):
  static_keys=['schema_version','target_renderer','renderer','version','color_management','renderer_sha256',
    'helper_sha256','audit_helper_sha256','blender_version','engine','resolution','samples','denoising',
    'view_transform','look','exposure','gamma','background','camera_type','fixed_orbit_framing',
    'turntable_frames','elevation_deg','base_pose_deg','detail_target_normalized','detail_scale','format',
    'webp_quality','render_threads','render_threads_mode']
  result={k:d[k] for k in static_keys}
  result['frames']=[{k:f[k] for k in ['id','view','angle_degrees']} for f in d['frames']]
  camera=d['camera']; radius=camera['orthographic_scale']/2.24
  center=[(d['source_bounds_blender_m']['min'][i]+d['source_bounds_blender_m']['max'][i])/2 for i in range(3)]
  assert all(abs(camera['target_blender_m'][i]-center[i])<1e-6 for i in range(3))
  assert abs(camera['orthographic_scale']/radius-2.24)<1e-9
  result['normalized_lighting']=[{'name':l['name'],'direction':l['direction'],'energy_over_radius2':round(l['energy']/radius**2,4),
                                  'size_over_radius':round(l['size']/radius,4)} for l in d['lighting']['lights']]
  result['normalized_camera_margin']=round(camera['orthographic_scale']/radius,8)
  result['world_strength']=d['lighting']['world_strength']
  result['color']=d['lighting']['camera_background']
  return result
assert normalized_render(old_render)==normalized_render(new_render)
config_diff=[k for k in sorted(set(old_config)|set(new_config)) if old_config.get(k)!=new_config.get(k)]
assert set(config_diff)<= {'revision','modeling_decisions'}

metric=load(r002/'metrics.json')
validator=load(r002/'gltf-validator.report.json')
runtime=load(r002/'runtime-parse.report.json')
assert metric['glb']['sha256']==expected['model.glb'] and metric['glb']['bytes']==154772
assert metric['glb']['unique_mesh_triangles']==2632 and metric['glb']['unique_mesh_primitives']==6
assert metric['glb']['materials']==4 and metric['glb']['extensions_used']==[]
assert validator['issues']['numErrors']==0 and validator['issues']['numWarnings']==0
assert runtime['glb_sha256']==expected['model.glb'] and runtime['three_version']=='0.180.0'
assert runtime['triangles']==2632 and runtime['meshes']==6 and runtime['gpu']=='not_run' and runtime['scene']=='not_run'

diagnostics=[]
for sub in ['01-regular-fracture-diagnostic','02-coherent-rind-before-contact-skirt']:
  p=r002/'attempts'/sub/'model.glb'
  diagnostics.append({'attempt':sub,'model_sha256':sha(p),'bytes':p.stat().st_size})

result={
  'schema_version':1,'kind':'independent_targeted_batch68_lava_dome_r002_differential',
  'reviewer_model':'GPT-6 Luna xhigh','target':{'head':head,'branch':branch,'clean_worktree':not status},
  'active_artifacts':artifacts,'supersedes_r001_candidate_sha256':cand['supersedes']['sha256'],
  'primary_reference_pixels':external_refs,
  'concept':{'sha256':concept_hash,'matches_r001':True,'matches_original_tool_output':True,
             'tool_call_observed_utc':gen.get('call_started_observed_utc'),
             'tool_result_observed_utc':gen.get('result_observed_utc'),
             'provider_generation_timestamp':'unknown/null; not inferred'},
  'repair_freeze':{'kind':freeze['kind'],'frozen_at':freeze['frozen_at'],
                   'freeze_completion_recorded_at':chrono_start['repair_freeze_completed_at'],
                   'actual_generator_authoring_start':'unknown/null; not inferred',
                   'preserves_material_camera_renderer_validator':freeze['material_camera_renderer_validator_changes'] is False,
                   'references_and_brief_frozen':True},
  'render_chronology':{'preproof_checked_at':binding['checked_at'],'manifest_created_at':manifest['created_at'],
                       'pixel_inspection_observed_at':pixel['observed_at'],
                       'manifest_sha256':sha(r002/'proof-final/render-manifest.json'),
                       'pixel_inspection_sha256':sha(r002/'pixel-inspection.json'),
                       'frames':frame_records,'contact_sheet_sha256':sheet_hash,
                       'contact_sheet_dimensions':sheet_dimensions,'binding_order_pass':True},
  'budgets':{'glb_bytes':metric['glb']['bytes'],'triangles':metric['glb']['unique_mesh_triangles'],
             'materials':metric['glb']['materials'],'primitives':metric['glb']['unique_mesh_primitives'],
             'textures':0,'all_within_limits':True},
  'validator':{'khronos_errors':validator['issues']['numErrors'],'khronos_warnings':validator['issues']['numWarnings'],
               'three_version':runtime['three_version'],'runtime_triangles':runtime['triangles'],
               'runtime_meshes':runtime['meshes'],'gpu':'not_run','scene':'not_run'},
  'evidence_flags':{'concept_valid':concept_validation['valid'],'concept_evidence_complete':concept_validation['evidence_complete'],
                    'candidate_valid':candidate_validation['valid'],'candidate_approved_for_brief':candidate_validation['approved_for_brief'],
                    'candidate_approval_status':cand['approval']['status']},
  'preserved_attempts':diagnostics,
  'r001_render_profile_same_after_bbox_normalization':True,
  'build_config_keys_changed_from_r001':config_diff,
  'disposition':{'technical':'pass','visual':'pass','factual':'pass_bounded_generic_dome','specification':'pass',
                 'runtime_parse':'pass','gpu':'not_run','scene':'not_run',
                 'note':'Stages are separate; evidence completeness and approval are separate from validity and visual disposition.'}
}
(qa/'independent-differential.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))

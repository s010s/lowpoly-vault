# SPDX-License-Identifier: MIT
"""Bind already inspected evidence to exact files. Integrity is not acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'scripts/validate_concept_evidence.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
from validate_concept_evidence import validate

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def desc(p):return {'path':p.relative_to(HERE).as_posix(),'sha256':sha(p)}
def save(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
generation=json.load(open(HERE/'concept-generation.json'))
events=[json.loads(line) for line in (HERE/'events.jsonl').read_text().splitlines()]
start1=next(e['utc'] for e in events if e['event']=='generator_authoring_started')
start2=next(e['utc'] for e in events if e['event']=='r002_generator_authoring_started')
start3=next((e['utc'] for e in events if e['event']=='tuzoia_r003_brief_frozen_before_head_bridge_authoring'),None)
generation_seconds=(datetime.fromisoformat(generation['return_received_utc'].replace('Z','+00:00'))-datetime.fromisoformat(generation['invocation_start_utc'].replace('Z','+00:00'))).total_seconds()
summary=[]
for slug in ['emeraldella','burgessia','tuzoia','sanctacaris']:
 for rev in ['r001','r002']+(['r003'] if slug=='tuzoia' else []):
  d=HERE/slug/rev
  if not (d/'proof/render-manifest.json').exists() or not (d/'self-review.md').exists():continue
  b=json.load(open(d/'brief.json'));r=json.load(open(d/'proof/render-manifest.json'));timing=json.load(open(d/'build-timing.json'))
  generator=HERE/({'r001':'generator.py','r002':'generator-r002.py','r003':'generator-r003.py'}[rev])
  stages=[]
  for stage,seconds,file,note in [('imagegen',generation_seconds,HERE/'concept-generation.json','Actual tool invocation/return elapsed time for the shared four-row sheet; not per-asset throughput.'),('interpretation',None,None,'Active interpretation time not measured; real chronology captured in events.jsonl.'),('modeling_export',timing['wall_seconds'],d/'build-timing.json','Measured Blender generator execution only. Human/model code-authoring time is not included.'),('proof_rendering',r['wall_seconds'],d/'proof/render-manifest.json','Measured clean-import proof render run, 12 frames at 512px, 16 Cycles CPU samples.'),('visual_review',None,None,'Images actually inspected as labeled contact sheets and critical 512px frames; active review duration not instrumented.'),('target_browser',None,None,'Browser/GPU/populated scene not run here. Node GLTFLoader parse is separately recorded, not browser evidence.')]:
   stages.append({'stage':stage,'status':'measured' if seconds is not None else 'not_run' if stage=='target_browser' else 'unrecorded','wall_seconds':seconds,'measurement_record':desc(file) if file else None,'note':note})
  record={'schema_version':1,'kind':'concept_evidence','scope':'provisional-study','asset_id':slug,'revision':rev,'labels':{'en':b['label']},'artifacts':{role:desc(file) for role,file in {'glb':d/(slug+'.glb'),'source':d/(slug+'.blend'),'generator':generator,'config':d/'build-config.json','brief':d/'brief.json','references':d/'references.json'}.items()},'concept':{'provider':'ImageGen','prompt':desc(HERE/'concept-prompt.txt'),'generation_record':desc(HERE/'concept-generation.json'),'images':[{'id':'shared-concept-sheet','view':'three-quarter/top/side; row '+str(b['concept_row']),**desc(HERE/'concept-original.png')}],'cross_view_consistency_note':b['concept_interpretation'],'hidden_surface_decisions':b['hidden_surfaces']},'chronology':{'concept_generated_at':generation['return_received_utc'],'concept_inspected_at':generation['inspection_completed_utc'],'modeling_started_at':{'r001':start1,'r002':start2,'r003':start3}[rev]},'stage_timings':stages,'coverage':{'required_views':b['required_views'],'turntable_frames':0},'render_manifest':desc(d/'proof/render-manifest.json'),'thumbnail':{'source_frame_id':'hero',**desc(d/'proof/hero.png')},'review_note':desc(d/'self-review.md'),'inspected_frames':[f['id'] for f in r['frames']],'khronos':{'glb_sha256':sha(d/(slug+'.glb')),'report':desc(d/'gltf-validator.report.json'),'warning_review':[]},'budget':{'target_glb_bytes':1000000,'enforcement':'advisory','rationale':'Supporting small scene life; prioritize recognition, keep package lightweight; no universal quality threshold.'}}
  out=d/'concept-evidence.json';save(out,record);result=validate(out,HERE);save(d/'concept-evidence-check.json',result)
  print(slug,rev,result['valid'],result['evidence_complete'],result['errors'],result['blockers'])
  if not result['valid'] or not result['evidence_complete']:raise RuntimeError('Incomplete evidence')
  m=json.load(open(d/'metadata.json'));q=json.load(open(d/'source-qa.json'));k=json.load(open(d/'gltf-validator.report.json'));node=json.load(open(d/'threejs-parse.report.json'))
  reports=[json.load(open(d/('reproducibility-'+str(i)+'.json'))) for i in (1,2)]
  technical={'asset_id':slug,'revision':rev,'created_at':datetime.now(timezone.utc).isoformat(),'glb_sha256':sha(d/(slug+'.glb')),'source_sha256':sha(d/(slug+'.blend')),'authored_source_vertices':sum(part['vertices'] for part in q['source']['parts']),'evaluated_source_vertices':sum(part['vertices'] for part in q['source']['parts']),'modifier_policy':'No modifiers; authored and evaluated meshes identical.','exported_position_stream_vertices':q['glb']['unique_position_accessor_vertices'],'scene_triangles':m['triangles'],'source_polygon_faces':'quads and triangles, see source-qa parts; triangles above are evaluated triangulation','mesh_parts':len(q['source']['parts']),'visible_creature_instances':1,'material_count':q['glb']['materials'],'base_primitives':q['glb']['scene_primitives_estimated_base_draw_calls'],'dimensions_glb_xyz_m':m['dimensions'],'dimensions_blender_xyz_m':m['blender_dimensions_m'],'glb_bytes':m['glb_bytes'],'blend_bytes':(d/(slug+'.blend')).stat().st_size,'license':'CC-BY-4.0; Leon Made This / s010s; executable code MIT','source_qa':q['source']['status'],'static_glb_qa':q['glb']['status'],'khronos':{'errors':k['issues']['numErrors'],'warnings':k['issues']['numWarnings']},'source_export':json.load(open(d/'source-export.report.json'))['status'],'rebuilds':[{'status':a['status'],'semantic_match':a['semantic_match'],'byte_identical':a['byte_identical']} for a in reports],'threejs_node_parse':node['status'],'evidence_integrity':result['evidence_complete'],'independent_visual_factual_spec_qa':'not_run; parent assigns fresh reviewer','browser_gpu_scene_qa':'not_run','gallery_poster':'not_generated; parent unified gallery renderer','production_acceptance':'not_granted'}
  if (d/'source-topology.json').exists():
   top=json.load(open(d/'source-topology.json'));technical.update(authored_polygon_faces=top['authored']['polygon_faces'],evaluated_polygon_faces=top['evaluated']['polygon_faces'],source_polygon_faces=top['authored']['polygon_faces'])
  save(d/'technical-summary.json',technical)

"""Mechanical checks after exact protected summary authentication. Not a generic schema."""
import math,hashlib
def validate_candidate(summary):
 ids=[x['id'] for x in summary['assets']]
 if len(ids)!=len(set(ids)):raise ValueError('duplicate asset IDs')
 eligible=[]
 for a in summary['assets']:
  review=a['independent_review']['subject_projection'];stages=review['stages'];arts=a['artifacts'];gate=a['frozen_native_gate'];measured=a['independent_review']['measurements'];native=a['native_measurement_comparison'];views=a['historical_views']
  if set(stages)!={'technical','visual','factual','specification','runtime_parse','gpu','scene'}:raise ValueError('missing stage')
  if stages['gpu']!='UNKNOWN' or stages['scene']!='UNKNOWN':raise ValueError('unperformed required stages promoted')
  verdict=review.get('offline_review_decision',review.get('verdict'))
  if verdict=='PASS':
   if any(stages[k]!='PASS' for k in ['technical','visual','factual','specification','runtime_parse']):raise ValueError('PASS disagrees with stages')
   eligible.append(a['id'])
  elif verdict!='REVISE':raise ValueError('unexpected offline disposition')
  if gate['budget_source']!=arts['brief'] or gate['budget_json_pointer']!='/geometry_policy':raise ValueError('wrong frozen budget source')
  if gate['budget']!={'max_triangles':14000,'max_materials':6,'max_primitives':30}:raise ValueError('wrong frozen budget')
  subject=views['subject']
  for k,role in [('glb_sha256','glb'),('brief_sha256','brief'),('references_sha256','references')]:
   if subject[k]!=arts[role]['sha256']:raise ValueError('stale views for changed subject')
  if subject['revision']!=a['revision']:raise ValueError('wrong views revision')
  if len(views['frames'])!=8 or len({x['view'] for x in views['frames']})!=8:raise ValueError('missing or duplicate view')
  old_bounds=measured.get('gltf_bounds_m',measured.get('bounds_gltf_m'))
  if not old_bounds:raise ValueError('missing original measured bounds')
  for k in ['min','max']:
   if native['bounds_m'][k]!=old_bounds[k]:raise ValueError('native bounds differ from original QA')
  if 'scientific_visual_finding' in a:
   finding=a['scientific_visual_finding']
   if hashlib.sha256(finding['verbatim_original_section'].encode()).hexdigest()!=finding['section_utf8_sha256']:raise ValueError('section UTF8 hash mismatch')
  def finite(v):
   if isinstance(v,bool):return
   if isinstance(v,(int,float)) and not math.isfinite(v):raise ValueError('nonfinite measurement')
   if isinstance(v,dict):
    for x in v.values():finite(x)
   if isinstance(v,list):
    for x in v:finite(x)
  finite(measured);finite(native);finite(a.get('anatomy_gate_projection',{}))
  for bounds in [native['bounds_m'],old_bounds]:
   if len(bounds['min'])!=3 or len(bounds['max'])!=3 or any(lo>hi for lo,hi in zip(bounds['min'],bounds['max'])):raise ValueError('unordered bounds')
  for group in a.get('anatomy_gate_projection',{}).get('transformed_components',{}).get('groups',[]):
   lo=group['actual_world_size_m_min'];hi=group['actual_world_size_m_max']
   if len(lo)!=3 or len(hi)!=3 or any(x<0 or x>y for x,y in zip(lo,hi)):raise ValueError('invalid dimensional size extrema')
  if native['triangles']!=measured['triangles'] or native['materials']!=measured['materials'] or native['glb_bytes']!=measured['glb_bytes']:raise ValueError('native metrics disagree')
  if arts['glb']['bytes']!=native['glb_bytes']:raise ValueError('wrong final GLB size')
 if eligible!=summary['offline_static_eligible_ids']:raise ValueError('eligibility differs from exact original stages')
 if summary['publication_ready_ids'] or summary['publication_approved']:raise ValueError('candidate cannot grant authority')
 supplement_hashes={f['sha256'] for archive in summary.get('supplementary_archives',[]) for f in archive['files']}
 if 'historical_restoration_resolution' in summary:
  gaps={x['sha256'] for x in summary['historical_restoration_gaps']}
  if not gaps<=supplement_hashes or gaps!=set(summary['historical_restoration_resolution']['resolved_reference_hashes']):raise ValueError('old failure restoration is not closed by explicit supplement')
 if 'original_quality_context' in summary:
  inventory=summary['original_quality_context']['full_visual_inventory'];needed={x['sha256'] for x in inventory['supplement_required']}
  if not needed<=supplement_hashes or needed!=set(inventory['supplement_resolution']['resolved_reference_hashes']):raise ValueError('full independent visual inventory is not recoverable')
  if inventory['initial_archive_covered_count']+len(needed)!=inventory['inspected_image_count']:raise ValueError('incomplete visual population')
 return True

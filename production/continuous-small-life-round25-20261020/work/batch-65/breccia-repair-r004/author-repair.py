from pathlib import Path
import json,hashlib,datetime
R=Path.cwd();P=R/'production/continuous-small-life-round25-20261020/work/batch-65';W=P/'breccia-repair-r004';B=R/'assets/candidates/continuous-small-life-round25-20261020/batch-65';a=B/'breccia-outcrop/r003';b=B/'breccia-outcrop/r004';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
(b/'authoring-start.json').write_text(json.dumps({'observed_at':now(),'note':'Before r004 revised generator authorship, after truthful freeze'})+'\n')
s=(a/'generator.py').read_text();old="""   separation=abs((B['center']-A['center']).dot(A['normal']))
   if separation>1e-5:continue
   overlap=polygon_overlap(A,B)"""
new="""   signed_center_separation=(B['center']-A['center']).dot(A['normal']);separation=abs(signed_center_separation)
   # Physical depth intervals, not a distance fudge: each solid prism has its actual .65inside/.35outside extent.
   an=A['normal'];bn=B['normal'];cosine=an.dot(bn)
   Ainterval=[min((p-A['center']).dot(an) for p in A['shape'])-A['depth']*.65,max((p-A['center']).dot(an) for p in A['shape'])+A['depth']*.35]
   Boffsets=[(p-A['center']).dot(an)+d*cosine for p in B['shape'] for d in [-B['depth']*.65,B['depth']*.35]]
   Binterval=[min(Boffsets),max(Boffsets)];depth_overlap=min(Ainterval[1],Binterval[1])-max(Ainterval[0],Binterval[0])
   if depth_overlap<=1e-8:continue
   overlap=polygon_overlap(A,B)"""
assert old in s;s=s.replace(old,new)
s=s.replace("'plane_separation_m':separation,'original_positive_overlap_area_m2':overlap", "'plane_separation_m':separation,'signed_center_plane_separation_m':signed_center_separation,'a_actual_depth_m':A['depth'],'b_actual_depth_m':B['depth'],'a_depth_interval_on_a_normal_m':Ainterval,'b_depth_interval_on_a_normal_m':Binterval,'positive_depth_overlap_m':depth_overlap,'original_positive_overlap_area_m2':overlap")
s=s.replace("'method':'two-sided in-plane centroid-bisector clipping;0.1mm margin each side'","'method':'actual parallel-prism depth interval + footprint conflict, then two-sided bisector clipping;1mm matrix gap each side'")
old=""" (out/'geometry-repair-report.json').write_text(json.dumps({'asset_id':slug,'revision':cfg['revision'],'original_components':len(records),'corrected_actual_pairs':corrections,'unchanged_component_ids':[r['id'] for r in records if len(r['shape'])==len(r['original_shape']) and all((a-b).length<1e-9 for a,b in zip(r['shape'],r['original_shape']))],'limits':'Only actual coplanar overlapping footprint pairs clipped; no global offsets/material/render changes.'},indent=2)+'\\n')"""
new=""" component_metrics=[]
 for r in records:
  def footprint_area(poly):return abs(signed_area([((p-r['center']).dot(r['u']),(p-r['center']).dot(r['v'])) for p in poly]))
  before=footprint_area(r['original_shape']);after=footprint_area(r['shape']);component_metrics.append({'id':r['id'],'material':r['material'],'center':list(r['center']),'normal':list(r['normal']),'depth_m':r['depth'],'original_footprint_area_m2':before,'corrected_footprint_area_m2':after,'original_prism_volume_m3':before*r['depth'],'corrected_prism_volume_m3':after*r['depth'],'retained_volume_fraction':after/before if before else None,'emitted':len(r['shape'])>=3})
 (out/'geometry-repair-report.json').write_text(json.dumps({'asset_id':slug,'revision':cfg['revision'],'original_components':len(records),'corrected_actual_pairs':corrections,'component_metrics':component_metrics,'unchanged_component_ids':[r['id'] for r in records if len(r['shape'])==len(r['original_shape']) and all((a-b).length<1e-9 for a,b in zip(r['shape'],r['original_shape']))],'limits':'Actual parallel-prism volume conflicts only;1mm boundary gap is not an arbitrary plane offset. No global offsets/material/render changes. Website remains HOLD pending independent differential and fresh actual capture.'},indent=2)+'\\n')"""
assert old in s;s=s.replace(old,new);(b/'generator.py').write_text(s)
refs=json.load(open(a/'references.delivery-v001.json'));refs['packaging_rights_adapter']={'created_at':now(),'original_references_sha256':hashlib.sha256((b/'references.json').read_bytes()).hexdigest(),'scope':'r004 geometry-only repair delivery rights metadata; original source/design unchanged; exact new proof subject uses this ledger.'};(b/'references.delivery-v001.json').write_text(json.dumps(refs,indent=2)+'\n')
for name in ['run-lifecycle.py','compose-sheets.py','package-candidates.py']:
 t=(P/'breccia-repair-r003'/name).read_text().replace('breccia-repair-r003','breccia-repair-r004')
 if name=='package-candidates.py':
  start=t.index('notes={');end=t.index('summary=[]',start);t=t[:start]+"notes={'breccia-outcrop':'R004 targeted parallel-prism volume-conflict geometry repair under unchanged original target. Corrected actual depth-interval and projected-footprint conflicts, not arbitrary cap-distance offsets; exact component IDs, actual thickness, overlap intervals, area and retained-volume metrics supplied. Original host/materials/placements retained, angular closed fragments remain embedded. All eight exact final512px proof images personally inspected incl clay. R003 narrow static pass and later actual website failure preserved; no cache excuse or website clearance claim. Website HOLD until independent differential and fresh actual recapture.'}\n"+t[end:]
  t=t.replace("'base_main':'b15cdab97b07f86dbc71e56fce9a44861631a20b'","'base_main':'e1d536f5658dbd3ba6b4d3cfc9315b652045f565'")
 (W/name).write_text(t)

import bpy,json,pathlib,sys,datetime,hashlib,os
from mathutils import Vector
R=pathlib.Path('/workspace/shared/lowpoly-batch96-20261020');B=R/'production/batch96/assets/cordaites/r003';Q=pathlib.Path('/workspace/shared/lowpoly-batch96-independent-qa-20261021');bpy.ops.wm.open_mainfile(filepath=str(B/'source.blend'),load_ui=False,use_scripts=False)
rows=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 for g in o.vertex_groups:
  if not g.name.startswith('leaf-'):continue
  v=[o.matrix_world@x.co for x in o.data.vertices if any(k.group==g.index for k in x.groups)];assert len(v)==48
  widths=[(v[i*6+5]-v[i*6]).length for i in range(4)];centers=[sum(v[i*6:i*6+6],Vector())/6 for i in range(4)];ratios=[w/max(widths)for w in widths]
  rows.append({'leaf':g.name,'actual_world_station_widths_m':widths,'normalized_width_ratios':ratios,'station_centers_m':[list(c)for c in centers],'last_span_m':(centers[-1]-centers[-2]).length})
d={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'source_sha256':hashlib.sha256((B/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((B/'model.glb').read_bytes()).hexdigest(),'count':len(rows),'all_105_have_tip_width_5_percent_of_body':all(abs(x['normalized_width_ratios'][-1]-.05)<.00001 for x in rows),'measurement':'Actual source world vertices, each of four stations six equal-band vertices. No changed transforms or normalization. Final straight-sided terminal span runs from full width to 5% width; generator parameter station is t=.70 to1.00.','leaves':rows}
(Q/'cordaites-tip-measurements.json').write_text(json.dumps(d,indent=2)+'\n');print('105 leaf tips',d['all_105_have_tip_width_5_percent_of_body'])

import bpy,sys,json,math,os,datetime,pathlib
from mathutils import Vector
O=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-independent-qa-20261021');A=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-20261020/production/batch91-archaeopteris-repair/archaeopteris/r002');p=json.load(open(A/'config.json'))['parameters'];source=json.load(open(O/'source-geometry.json'));vertices=source['new']['parts'][0]['vertices'];geo=json.load(open(O/'geometry.report.json'));rows=[]
# Independently isolate the leaf construction arithmetic. No generator import, scene build, source save or model export.
for i in range(12):
 a=i*2.399963+.13*math.sin(i*2.3);z=1.4+i*.133;start=Vector((.055*math.sin(z/3.25*2),.028*math.sin(z/3.25*4),z));d=Vector((math.cos(a),math.sin(a),0));side=Vector((-math.sin(a),math.cos(a),0));end=start+d*(1.05-.024*i)+Vector((0,0,.51+.018*i))
 for k in range(4):
  q=start.lerp(end,.42+.17*k);sg=-1 if k%2 else 1;sd=(d*.62+side*sg*.70+Vector((0,0,.20))).normalized();tip=q+sd*(.53-.025*k);normal=sd.cross(side).normalized()
  if normal.z<0:normal=-normal
  spread=normal.cross(sd).normalized()
  for j in range(6):
   base=q.lerp(tip,.16+j*.135);nom=p['leaf_length_range_m'][1]-(p['leaf_length_range_m'][1]-p['leaf_length_range_m'][0])*(j/5)
   for sign in [-1,1]:
    direction=(sd*.36+spread*sign*.91+normal*.10).normalized();scaled=direction*nom;ep=base+scaled
    delta=[float(ep[c])-float(base[c]) for c in range(3)];row=geo['leaves'][len(rows)];first=row['source_first_vertex'];fv=vertices[first];ft=vertices[first+3]
    rows.append({'source_first_vertex':first,'nominal_m':nom,'direction_norm_double':math.sqrt(sum(float(x)**2 for x in direction)),'scaled_vector_norm_double':math.sqrt(sum(float(x)**2 for x in scaled)),'pre_normalization_base_tip_double':math.sqrt(sum(x*x for x in delta)),'pre_normalization_delta':delta,'final_glb_delta':[ft[c]-fv[c] for c in range(3)],'final_base':fv,'final_tip':ft,'single_storage_interval_m':row['single_float32_storage_length_interval_m'],'pre_normalization_length_within_final_interval':row['single_float32_storage_length_interval_m'][0]<=math.sqrt(sum(x*x for x in delta))<=row['single_float32_storage_length_interval_m'][1]})
r={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'blender':bpy.app.version_string,'argv':sys.argv,'method':'Independent isolated float32 mathutils leaf arithmetic, directly reconstructed from frozen parameters and audited construction expression. No maker generator import or execution. Delta before normalization compared to final GLB coordinate rounding-cell intervals. The mathematical direction is unit length; actual float32 normalized direction, scalar product and translated endpoints each round.','rows':rows}
(O/'precision-trace.json').write_text(json.dumps(r,indent=2)+'\n');print('rows',len(rows),'local-length-outside-final-rounding-interval',sum(not x['pre_normalization_length_within_final_interval'] for x in rows));print(json.dumps(rows[433],indent=2))

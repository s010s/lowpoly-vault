# SPDX-License-Identifier: MIT
"""Small read-only geometric checks against frozen dimensions, not config self-attestation."""
import bpy,sys,pathlib,json,hashlib,datetime,math,numpy as np
from mathutils import Vector
b=pathlib.Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str(b/'source.blend'));aid=b.parent.name;cfg=json.loads((b/'build-config.json').read_text());p=cfg['parameters'];objs=[o for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH'];deps=bpy.context.evaluated_depsgraph_get();parts=[]
for o in objs:
 o.data.calc_loop_triangles();e=o.evaluated_get(deps);m=e.to_mesh();m.calc_loop_triangles();parts.append(dict(name=o.name,authored_vertices=len(o.data.vertices),evaluated_vertices=len(m.vertices),authored_polygons=len(o.data.polygons),evaluated_polygons=len(m.polygons),authored_triangles=len(o.data.loop_triangles),evaluated_triangles=len(m.loop_triangles)));e.to_mesh_clear()
checks={};allv=np.array([tuple(o.matrix_world@v.co) for o in objs for v in o.data.vertices]);bounds=(allv.max(0)-allv.min(0)).tolist()
def check(n,v,lo,hi):checks[n]={'measured':v,'allowed':[lo,hi],'pass':lo-1e-7<=v<=hi+1e-7}
def rayz(obj,x,y):
 hit,pos,n,idx=obj.ray_cast(Vector((x,y,2)),Vector((0,0,-1)));return float(pos.z) if hit else None
if aid=='pertica':
 o=next(o for o in objs if o.name=='sixteen-four-rank-lateral-systems');check('whole_height_including_caps_m',bounds[2],.999999,1.000001);check('lateral_vertex_groups_with_actual_vertices',sum(any(any(g.group==vg.index for g in v.groups) for v in o.data.vertices) for vg in o.vertex_groups),16,16)
 faces=[f for f in o.data.polygons if o.data.materials[f.material_index].name.startswith('sporangia')];adj={}
 for f in faces:
  for i in f.vertices:adj.setdefault(i,set()).update(f.vertices)
 seen=set();components=[]
 for i in adj:
  if i in seen:continue
  todo=[i];ids=[]
  while todo:
   k=todo.pop()
   if k in seen:continue
   seen.add(k);ids.append(k);todo.extend(adj[k]-seen)
  components.append(ids)
 lengths=[];radii=[]
 for ids in components:
  vv=np.array([tuple(o.matrix_world@o.data.vertices[i].co) for i in ids]);center=vv.mean(0);a=vv-center;vals,vec=np.linalg.eigh(a.T@a);axis=vec[:,-1];proj=a@axis;lengths.append(float(proj.max()-proj.min()));rad=a-np.outer(proj,axis);radii.append(float(np.linalg.norm(rad,axis=1).max()))
 check('actual_closed_sporangia_components',len(components),160,160);check('sporangia_min_axial_length_including_caps_m',min(lengths),.015999,.016001);check('sporangia_max_axial_length_including_caps_m',max(lengths),.015999,.016001);check('sporangia_max_radius_m',max(radii),.002799,.002801)
 checks['four_rank_laterals']={'actual_group_count':len(o.vertex_groups),'groups':[vg.name for vg in o.vertex_groups],'method':'Counts real source vertex group membership, no config count substitution.'}
elif aid=='zoophycos-spiral-spreite':
 o=next(o for o in objs if o.name.startswith('broad-spiral'));vv=np.array([tuple(o.matrix_world@v.co) for v in o.data.vertices]);rr=np.linalg.norm(vv[:,:2],axis=1);check('actual_sheet_outer_envelope_radius_m',float(rr.max()),.0599,.060001)
 half=len(vv)//2;row=13;N=half//row-1;edge=vv[np.arange(row-1,half,row)];angles=np.unwrap(np.arctan2(edge[:,1],edge[:,0]));check('actual_coiling_turns',float(abs(angles[-1]-angles[0])/(2*math.pi)),1.249999,1.250001);check('actual_base_sheet_rise_m',float(edge[-1,2]-edge[0,2]),.019999,.020001)
 top=vv[half:];base=vv[:half];delta=top[:,2]-base[:,2];check('actual_min_full_sheet_thickness_m',float(delta.min()),.002999,.003001)
 signal=(top[np.arange(row-1,half,row),2]-edge[:,2]);maxima=[i for i in range(1,len(signal)-1) if signal[i]>signal[i-1]+1e-8 and signal[i]>signal[i+1]+1e-8];boundary_peaks=int(signal[0]>signal[1])+int(signal[-1]>signal[-2]);check('interior_complete_primary_lamellae',len(maxima),40,40);checks['boundary_half_ridges']={'count':boundary_peaks,'values':signal.tolist()}
 shaft=next(o for o in objs if o.name=='narrow-cylindrical-central-shaft');s=np.array([tuple(shaft.matrix_world@v.co) for v in shaft.data.vertices]);check('shaft_outer_radius_m',float(np.linalg.norm(s[:,:2],axis=1).max()),.003999,.004001);check('shaft_top_height_m',float(s[:,2].max()),.048999,.049001)
else:
 o=objs[0];T=p['slab_dimensions_m'][2];check('actual_slab_width_m',bounds[0],p['slab_dimensions_m'][0]-1e-6,p['slab_dimensions_m'][0]+1e-6);check('actual_slab_depth_m',bounds[1],p['slab_dimensions_m'][1]-1e-6,p['slab_dimensions_m'][1]+1e-6)
 if aid.startswith('rosary'):
  sample=[]
  for j in range(1201):
   t=j/1200;x=-.04+.08*t;y=.009*math.sin(math.tau*t-.4);sample.append(rayz(o,x,y)-T)
  peaks=[i for i in range(1,len(sample)-1) if sample[i]>sample[i-1]+1e-8 and sample[i]>sample[i+1]+1e-8 and sample[i]>.002]
  # Ends intentionally carry rounded chambers; count them if actual elevated raycast values agree.
  count=len(peaks)+int(sample[0]>.002)+int(sample[-1]>.002);check('actual_chamber_relief_peaks',count,13,13);check('max_chamber_relief_m',max(sample),.003299,.003301);check('minimum_continuous_connector_relief_m',min(sample),.0007,.00131)
  # Measure geometric cross-widths at a central chamber and an inter-chamber neck.
  widths=[]
  for t in [6/12,5.5/12]:
   x=-.04+.08*t;y=.009*math.sin(math.tau*t-.4);dx=.08;dy=.009*math.tau*math.cos(math.tau*t-.4);mag=math.hypot(dx,dy);nx=-dy/mag;ny=dx/mag
   vals=[(d/100000,rayz(o,x+nx*d/100000,y+ny*d/100000)-T) for d in range(-500,501)]
   positive=[d for d,z in vals if z>.00008];widths.append(max(positive)-min(positive))
  check('chamber_to_neck_measured_breadth_ratio',widths[0]/widths[1],2.4,4.5);checks['cross_widths_m']=widths
 else:
  check('actual_max_cord_relief_m',float(allv[:,2].max()-T),.001799,.001801)
  traced=allv[allv[:,2]>T+.0004];checks['actual_relief_footprint_m']=(traced.max(0)-traced.min(0)).tolist();checks['loop_and_crossing_readability']={'status':'requires_actual_pixel_inspection','note':'Compressed union uses one continuous surface; no claim of separated over-under original cords.'}
report={'kind':'actual-source-geometric-freeze-diagnostics','source_sha256':hashlib.sha256((b/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((b/'model.glb').read_bytes()).hexdigest(),'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':__import__('os').getpid(),'parts':parts,'bounds_blender_xyz_m':bounds,'checks':checks,'all_numeric_checks_pass':all(x.get('pass',True) for x in checks.values() if isinstance(x,dict)),'limitations':'Read-only actual source geometry measurement, not independent acceptance; numeric targets checked from real vertices/ray hits incl caps/perturbations, not echoed from config.'}
for k in ['authored_vertices','evaluated_vertices','authored_polygons','evaluated_polygons','authored_triangles','evaluated_triangles']:report[k]=sum(v[k] for v in parts)
(b/'source-vertex-counts.json').write_text(json.dumps(report,indent=2)+'\n');print(aid,report['all_numeric_checks_pass'],json.dumps({n:v for n,v in checks.items() if isinstance(v,dict) and v.get('pass') is False}))

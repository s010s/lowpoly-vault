#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reopen editable source and directly decode shipped GLB, measure actual local geometry."""
import sys,json,struct,hashlib,datetime,os,math
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from check_source_export import main
main()
a=sys.argv[sys.argv.index('--')+1:];src=Path(a[a.index('--source')+1]);glb=Path(a[a.index('--glb')+1]);out=Path(a[a.index('--output')+1]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=glb.read_bytes();jl,jt=struct.unpack_from('<II',raw,12);doc=json.loads(raw[20:20+jl]);bl,bt=struct.unpack_from('<II',raw,20+jl);blob=raw[28+jl:28+jl+bl]
for node in doc.get('nodes',[]):
 assert node.get('translation',[0,0,0])==[0,0,0] and node.get('rotation',[0,0,0,1])==[0,0,0,1] and node.get('scale',[1,1,1])==[1,1,1] and 'matrix' not in node,'Nonidentity node requires explicit transform decoding.'
positions=[]
for mesh in doc['meshes']:
 for prim in mesh['primitives']:
  ac=doc['accessors'][prim['attributes']['POSITION']];bv=doc['bufferViews'][ac['bufferView']];assert ac['componentType']==5126 and ac['type']=='VEC3';off=bv.get('byteOffset',0)+ac.get('byteOffset',0);step=bv.get('byteStride',12)
  for i in range(ac['count']):
   x,y,z=struct.unpack_from('<fff',blob,off+i*step);positions.append((x,-z,y))
positions=list(set(positions));objs=[o for o in bpy.data.objects if o.type=='MESH'];assert len(objs)==1;o=objs[0];source=[tuple(o.matrix_world@v.co) for v in o.data.vertices];eps=2e-6
lookup={tuple(round(c,6) for c in p):p for p in positions}
def nearest(p):
 key=tuple(round(c,6) for c in p)
 if key in lookup:return lookup[key]
 q=min(positions,key=lambda q:sum((x-y)**2 for x,y in zip(p,q)));assert math.dist(p,q)<=eps;return q
matched=[nearest(p) for p in source];maxerr=max(math.dist(p,q) for p,q in zip(source,matched));assert maxerr<=eps
bounds=lambda ps:{'min':[min(p[k] for p in ps) for k in range(3)],'max':[max(p[k] for p in ps) for k in range(3)],'size':[max(p[k] for p in ps)-min(p[k] for p in ps) for k in range(3)]}
def stats(a):return {'min':min(a),'max':max(a),'mean':sum(a)/len(a),'count':len(a)}
aid=glb.stem;measure={}
for label,ps in [('source',source),('exported_glb',matched)]:
 if aid=='spatter-cone':
  N=int(o['construction_angular_rays']);crest=ps[6*N:7*N];floor=ps[:2*N];nr=(len(ps)-N)//N
  actual={'crest_height_m':stats([p[2] for p in crest]),'crest_horizontal_radius_m':stats([math.hypot(p[0],p[1]) for p in crest]),'central_floor_z_m':stats([p[2] for p in floor]),'angular_rays':N,'construction_radial_intervals':int(o['construction_radial_intervals']),'construction_profile_stations':int(o['construction_profile_stations']),'actual_surface_rings':nr,'actual_lobe_group_count_attribute':int(o['construction_welded_lobe_groups']),'crest_is_unique_radial_height_maximum':all(crest[j][2]>max(ps[k*N+j][2] for k in range(nr) if k!=6) for j in range(N)),'min_crest_clearance_above_other_same_index_ray_m':min(crest[j][2]-max(ps[k*N+j][2] for k in range(nr) if k!=6) for j in range(N))}
  assert abs(actual['crest_height_m']['mean']-2.5)<=eps and abs(actual['crest_height_m']['max']-2.8)<=eps and abs(actual['crest_horizontal_radius_m']['mean']-.65)<=eps
  assert all(abs(p[2]-.18)<=eps for p in floor) and actual['crest_is_unique_radial_height_maximum']
 else:
  N=int(o['construction_cross_intervals']);levels=int(o['construction_levels']);K=N+1;regions=[(level,k) for level in range(levels) for k in range(6) if level==0 or k!=0];floor_ids=[(i*K+N//2,level) for i,(level,k) in enumerate(regions) if k==1];floors=[ps[i][2] for i,l in floor_ids];rises=[floors[i]-floors[i+1] for i in range(levels-1)];lip_records=[]
  for ri,(level,k) in enumerate(regions):
   if k not in (3,4):continue
   for j in range(K):
    t=-1+2*j/N;edge=.20*max(0,(abs(t)-.78)/.22);rough=.035*math.sin(j*1.3+level*2+k*.9) if abs(t)>.83 else 0;saddle=.15*math.exp(-((t-(.27 if level%2 else -.22))/.13)**2);observed=ps[ri*K+j][2]-floors[level];nominal=observed-edge-rough+saddle;lip_records.append({'vertex':ri*K+j,'floor_level':level,'measured_relief_m':observed,'side_edge_contribution_m':edge,'side_irregularity_m':rough,'overflow_subtraction_m':saddle,'recovered_nominal_primary_lip_m':nominal})
  actual={'main_floor_heights_m':floors,'consecutive_floor_rises_m':rises,'levels':levels,'cross_intervals':N,'vertices_per_row':K,'actual_top_rows':len(regions),'lip_measured_relief_range_m':stats([x['measured_relief_m'] for x in lip_records]),'lip_recovered_nominal_m':stats([x['recovered_nominal_primary_lip_m'] for x in lip_records]),'lip_samples':lip_records,'bottom_contact_z_m':min(p[2] for p in ps),'actual_sidewall_bottom_vertices':sum(abs(p[2])<=eps for p in ps),'no_z_scaling_check':'Four actual source/export floor differences remain 0.7 m; original nominal lip recovered from actual geometry after known saddle/side contribution removal.'}
  assert all(abs(x-.7)<=eps for x in rises) and all(abs(x['recovered_nominal_primary_lip_m']-.18)<=eps for x in lip_records)
 measure[label]={'bounds_blender_xyz_m':bounds(ps),'local':actual}
target=[7.8,7.4,2.8] if aid=='spatter-cone' else [10,18,4.7]
for label in measure:
 b=measure[label]['bounds_blender_xyz_m'];assert all(abs(v-t)<=eps for v,t in zip(b['size'],target));assert abs(b['min'][2])<=eps;assert all(abs(b['min'][k]+b['max'][k])<=eps for k in [0,1])
parts=[];dg=bpy.context.evaluated_depsgraph_get()
for ob in objs:
 ob.data.calc_loop_triangles();ev=ob.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();parts.append({'name':ob.name,'authored_vertices':len(ob.data.vertices),'authored_polygons':len(ob.data.polygons),'authored_triangles':len(ob.data.loop_triangles),'evaluated_vertices':len(me.vertices),'evaluated_polygons':len(me.polygons),'evaluated_triangles':len(me.loop_triangles),'modifier_count':len(ob.modifiers)});ev.to_mesh_clear()
record={'schema_version':1,'status':'pass','asset_id':aid,'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'blender':bpy.app.version_string,'source_sha256':sha(src),'glb_sha256':sha(glb),'source_saved':False,'measurement_epsilon_m':eps,'epsilon_scope':'Float32 serialization only, not art tolerance','method':'Actual reopened source mesh world vertices; GLB POSITION binary decode with checked identity node transforms, axis conversion and nearest-point correspondence. Semantic indices locate crest/floor/rows; numerical values come from final geometry, not constructor return values.','matched_source_vertices':len(source),'unique_exported_positions':len(positions),'max_source_export_point_error_m':maxerr,'measurements':measure,'parts':parts,'limitations':['Maker checks not independent acceptance.','outer_radius=3.7 is nominal input construction radius, not measurable final max; 9 group structure corroborated by generator/config and visual check, not invented final connected-component count.']}
with (out.parent/'actual-local-measurements.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
counts={'schema_version':1,'source_sha256':sha(src),'measured_at':record['measured_at'],'pid':os.getpid(),'blender':bpy.app.version_string,'parts':parts,'totals':{k:sum(x[k] for x in parts) for k in ['authored_vertices','authored_polygons','authored_triangles','evaluated_vertices','evaluated_polygons','evaluated_triangles']},'source_saved':False}
with (out.parent/'authored-evaluated-counts.json').open('x') as f:json.dump(counts,f,indent=2);f.write('\n')
print('Actual final source/GLB local measurements passed:',aid)

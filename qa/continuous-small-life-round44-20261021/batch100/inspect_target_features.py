import sys;sys.dont_write_bytecode=True
import bpy,json,pathlib,math,hashlib,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=pathlib.Path('/workspace/shared/lowpoly-batch100-20261021/production/small-life-batch100');Q=pathlib.Path(__file__).parent
for a,r in [('lygodium','r003'),('flabellophyton','r001'),('protosalvinia','r003')]:
 p=B/a/r/'artifacts'/f'{a}.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);bpy.context.view_layer.update();o=next(o for o in bpy.data.objects if o.type=='MESH');vv=[o.matrix_world@v.co for v in o.data.vertices];o.data.calc_loop_triangles();tt=[tuple(t.vertices)for t in o.data.loop_triangles];tree=BVHTree.FromPolygons(vv,tt,all_triangles=True);g={vg.name:[]for vg in o.vertex_groups}
 for v in o.data.vertices:
  for q in v.groups:g[o.vertex_groups[q.group].name].append(v.index)
 result={'asset_id':a,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pid':os.getpid()}
 if a=='lygodium':
  tips=[]
  for sign in [-1,1]:
   ids=[i for i in g['bifid_lamina']if vv[i].x*sign>0];maxz=max(vv[i].z for i in ids);near=[i for i in ids if abs(vv[i].z-maxz)<1e-9];i=min(near,key=lambda i:vv[i].y);pt=vv[i];d=Vector((0,-1,0));hit,_,_,_=tree.ray_cast(pt+d*1e-8,d,1);tips.append({'half':sign,'actual_vertex':i,'point':list(pt),'front_unoccluded':hit is None})
  result['actual_lamina_apices']=tips;result['blade_bbox_organ_only']={side:[fun(vv[i][k]for i in g['bifid_lamina'])for k in range(3)]for side,fun in [('min',min),('max',max)]}
 elif a=='flabellophyton':
  row=sorted([v for v in vv if abs(v.z-.036)<1e-8 and v.y<0],key=lambda v:v.x);minima=[i for i in range(1,len(row)-1)if row[i].y<row[i-1].y and row[i].y<row[i+1].y];result['actual_row_z_m']=.036;result['actual_row_vertices']=len(row);result['surface_ridge_apices']=len(minima);result['front_row_y_m']=[v.y for v in row];result['max_minus_min_y_m']=max(v.y for v in row)-min(v.y for v in row)
 else:
  half=len(vv)//2;cross=[e for e in o.data.edges if min(e.vertices)<half and max(e.vertices)>=half];border=sorted(set(i for e in cross for i in e.vertices if i<half));left=max((vv[i]for i in border if vv[i].x<0),key=lambda v:v.z);right=max((vv[i]for i in border if vv[i].x>0),key=lambda v:v.z);central=max((vv[i]for i in border if abs(vv[i].x)<1e-9),key=lambda v:v.z);result.update(front_boundary_vertices=len(border),left_apex=list(left),right_apex=list(right),central_notch=list(central),notch_depths_m=[left.z-central.z,right.z-central.z],actual_thickness_m=max(v.y for v in vv)-min(v.y for v in vv))
 (Q/a/'target-feature-measurements.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

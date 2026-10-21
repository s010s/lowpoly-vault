import bpy,sys,json,pathlib,math,hashlib,collections
from mathutils import Vector
from mathutils.bvhtree import BVHTree
W=pathlib.Path('/workspace/shared/lowpoly-batch99-20261021/production/small-life-batch99');Q=pathlib.Path('/workspace/shared/lowpoly-batch99-independent-qa-20261021');a=sys.argv[sys.argv.index('--')+1];r='r002' if a=='proterocladus' else 'r001';src=W/a/r/'artifacts'/(a+'.blend');bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);co=json.loads(bpy.data.texts['BATCH99_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[co['object_name']];v=[o.matrix_world@x.co for x in o.data.vertices];o.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in o.data.loop_triangles];cs={c['tag']:c for c in co['components']};out=[]
if a=='proterocladus':
 def rings(c,n):return [sum((v[i] for i in c['vertices'][s:s+n]),Vector())/n for s in range(0,len(c['vertices'])-2,n)]
 for c in cs.values():
  if c['kind'] not in ['primary_lateral','secondary_lateral']:continue
  p=cs[c['parent']];pr=rings(p,7);b=v[c['base_vertices'][0]];nextr=pr[-1] if p['kind']=='main_cell' else pr[6];axis=(pr[-1]-pr[0]).normalized();gap=(nextr-b).dot(axis);out.append({'tag':c['tag'],'parent':c['parent'],'actual_base_center_m':list(b),'actual_next_constriction_center_m':list(nextr),'axial_gap_below_constriction_m':gap,'below':gap>0})
 for tag in ['lateral_2','lateral_0']:
  c=cs[tag];rs=rings(c,7);rr=[max((v[i]-center).length for i in c['vertices'][j*7:j*7+7]) for j,center in enumerate(rs)];out.append({'tag':tag,'actual_ring_centers_m':[list(x) for x in rs],'actual_ring_max_radii_m':rr})
else:
 for c in cs.values():
  if c['kind']!='nutlet_ridge':continue
  ids=set(c['vertices']);par=cs[c['parent']];pids=set(par['vertices']);tree=BVHTree.FromPolygons(v,[t for t in tris if all(i in pids for i in t)],all_triangles=True);axis=(v[par['vertices'][-1]]-v[par['vertices'][0]]).normalized();samples=[]
  for t in tris:
   if not all(i in ids for i in t):continue
   for i in range(13):
    for j in range(13-i):samples.append(v[t[0]]*(i/12)+v[t[1]]*(j/12)+v[t[2]]*(1-(i+j)/12))
  exposed=[]
  for x in samples:
   q,n,f,d=tree.find_nearest(x)
   if (x-q).dot(n)>1e-9:exposed.append(x.dot(axis))
  full=[v[i].dot(axis) for i in ids];out.append({'tag':c['tag'],'surface_samples':len(samples),'outside_own_nut_surface_samples':len(exposed),'full_axial_span_m':max(full)-min(full),'exposed_axial_span_m':max(exposed)-min(exposed) if exposed else 0,'exposed_axial_fraction':(max(exposed)-min(exposed))/(max(full)-min(full)) if exposed else 0})
r={'asset_id':a,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_mutated':False,'purpose':'Actual original geometry diagnostics for required filament junctions or exposed longitudinal nut ridges, not config-only and not an arbitrary acceptance percent.','records':out};(Q/(a+'-targeted-diagnostics.json')).write_text(json.dumps(r,indent=2)+'\n');print(a, 'records',len(out));print(json.dumps(out[:3]))

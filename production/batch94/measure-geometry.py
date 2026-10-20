# SPDX-License-Identifier: MIT
"""Measured source world-space groups, actual base contacts, counts and topology."""
import bpy,bmesh,json,sys,pathlib,datetime,hashlib,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=pathlib.Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str(B/'source.blend'));sem=json.load(open(B/'geometry-semantics.json'));brief=json.load(open(B/'brief.json'));groups={};gfaces={};objects=[]
def bounds(points):
 a=[min(v[i]for v in points)for i in range(3)];b=[max(v[i]for v in points)for i in range(3)];return {'min':a,'max':b,'size':[b[i]-a[i]for i in range(3)]}
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 o.data.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(o.data);bm.normal_update();objects.append({'name':o.name,'authored_vertices':len(o.data.vertices),'authored_polygons':len(o.data.polygons),'evaluated_vertices':len(o.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.vertices),'triangles':len(o.data.loop_triangles),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<=1e-16 for f in bm.faces),'bounds_world_m':bounds([o.matrix_world@v.co for v in o.data.vertices])});bm.free()
 for g in o.vertex_groups:
  ix=[v.index for v in o.data.vertices if any(k.group==g.index for k in v.groups)];lookup={n:i for i,n in enumerate(ix)};points=[o.matrix_world@o.data.vertices[i].co for i in ix];groups[g.name]=points;gfaces[g.name]=[tuple(lookup[i]for i in t.vertices)for t in o.data.loop_triangles if all(i in lookup for i in t.vertices)]
trees={g:BVHTree.FromPolygons(v,gfaces[g],all_triangles=True)for g,v in groups.items()};directions=[Vector((1,.173,.291)).normalized(),Vector((.231,1,.379)).normalized(),Vector((.257,.319,1)).normalized()]
def contain(g,p):
 tree=trees[g];near=tree.find_nearest(p);dist=near[3]
 if dist is not None and dist<1e-7:return True,dist,'surface-contact'
 votes=[]
 for d in directions:
  origin=p.copy();n=0
  for j in range(100):
   hit,normal,idx,ds=tree.ray_cast(origin,d)
   if hit is None:break
   n+=1;origin=hit+d*1e-7
  votes.append(n%2==1)
 signed=(p-near[0]).dot(near[1]); inside=signed<0;return inside,dist,'oriented-nearest-surface-negative' if inside else 'outside'
contacts=[];errors=[];frames={x['group']:x for x in sem['leaf_frames']};tubes={}
for t in sem['tubes']:tubes.setdefault(t['group'],t)
for a in sem['attachments']:
 g=a['child'];v=groups[g]
 if g in frames:
  n=frames[g]['outline_vertices'];ids=[0,n]if n==4 else[0,n-1,n,2*n-1]
 elif g in tubes:ids=list(range(tubes[g]['sides']))
 elif a['kind']=='shallow-scar-inset':ids=list(range(len(v)//2))
 else:raise AssertionError(g)
 point=sum((v[i]for i in ids),Vector())/len(ids);inside,dist,mode=contain(a['parent'],point);base_tests=[contain(a['parent'],v[i]) for i in ids];connected=inside or any(t[0] for t in base_tests);rec={'child':g,'parent':a['parent'],'kind':a['kind'],'actual_child_base_center_world_m':list(point),'base_indices_in_group':ids,'nearest_parent_surface_m':dist,'parent_contact':connected,'base_center_inside':inside,'base_vertices_inside':sum(t[0]for t in base_tests),'method':mode};contacts.append(rec)
 if not connected:errors.append('Disconnected base '+g)
counts={prefix:sum(g==prefix if not prefix.endswith('-')else g.startswith(prefix)for g in groups)for prefix in brief['hard_component_counts']}
for key,expected in brief['hard_component_counts'].items():
 if counts[key]!=expected:errors.append('Count '+key)
leaves=[]
for g,frame in frames.items():
 pts=groups[g];u=Vector(frame['transverse']);v=Vector(frame['longitudinal']);n=u.cross(v).normalized();leaves.append({'group':g,'length_m':max(x.dot(v)for x in pts)-min(x.dot(v)for x in pts),'width_m':max(x.dot(u)for x in pts)-min(x.dot(u)for x in pts),'thickness_and_curvature_m':max(x.dot(n)for x in pts)-min(x.dot(n)for x in pts)})
for o in objects:
 if o['nonmanifold_edges']or o['zero_area_faces']:errors.append('Topology '+o['name'])
d={'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'source_blend_sha256':hashlib.sha256((B/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((B/'model.glb').read_bytes()).hexdigest(),'objects':objects,'world_component_counts':counts,'world_component_bounds':{g:bounds(v)for g,v in groups.items()},'base_contacts':contacts,'leaf_dimensions':leaves,'normalization_applied':sem['normalization_applied'],'measurement_scope':'Actual mesh world vertices after grounding, no scale normalization. All dimensional targets nominal; semantic counts and technical budgets are hard. Actual base center or actual ring vertex interior establishes plant joint connection; oriented nearest surface sign avoids ray duplicate intersections, not zero intentional volume overlap.','errors':errors,'pass':not errors}
(B/'source-vertex-counts-v002.json').write_text(json.dumps(d,indent=2)+'\n');print('MEASURE',B.parent.name,'groups',len(groups),'contacts',len(contacts),'errors',errors);assert not errors,errors

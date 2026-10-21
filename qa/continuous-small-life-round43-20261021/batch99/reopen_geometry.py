import bpy,bmesh,sys,json,pathlib,hashlib,collections,math,os,datetime
from mathutils import Vector
from mathutils.bvhtree import BVHTree
W=pathlib.Path('/workspace/shared/lowpoly-batch99-20261021');Q=pathlib.Path('/workspace/shared/lowpoly-batch99-independent-qa-20261021');a=sys.argv[sys.argv.index('--')+1];r='r002' if a=='proterocladus' else 'r001';p=W/'production/small-life-batch99'/a/r;src=p/'artifacts'/(a+'.blend');gh=p/'artifacts'/(a+'.glb')
sys.path.insert(0,str(W/'scripts'));from asset_common import audit_source;from qa_glb import audit_glb;from check_source_export import compare_source_audit
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();contract=json.loads(bpy.data.texts['BATCH99_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[contract['object_name']];verts=[o.matrix_world@v.co for v in o.data.vertices];o.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in o.data.loop_triangles];extent=max(max(v[k] for v in verts)-min(v[k] for v in verts) for k in range(3));eps=extent*1e-7;allids=[];comps={};trees={};out=[];contacts=[];dirs={k:Vector(v).normalized() for k,v in {'front':(0,-1,0),'rear':(0,1,0),'left':(-1,0,0),'right':(1,0,0),'top':(0,0,1),'bottom':(0,0,-1),'hero':(.47,-.67,.57),'reversehero':(-.47,.67,.57)}.items()}
for c in contract['components']:
 ids=set(c['vertices']);allids+=list(ids);ts=[t for t in tris if all(i in ids for i in t)];comps[c['tag']]=(c,ids,ts);trees[c['tag']]=BVHTree.FromPolygons(verts,ts,all_triangles=True)
def inside(tree,point):
 votes=[]
 for d in [Vector((1,.371,.129)).normalized(),Vector((.233,1,.487)).normalized(),Vector((.311,.199,1)).normalized()]:
  origin=point+d*eps;hits=0
  for _ in range(100):
   q,n,i,dist=tree.ray_cast(origin,d,extent*4)
   if q is None:break
   hits+=1;origin=q+d*eps
  votes.append(bool(hits%2))
 return sum(votes)>=2
for tag,(c,ids,ts) in comps.items():
 points=[verts[i] for i in sorted(ids)];axes=[]
 for ax in c['axes']:
  d=(o.matrix_world.to_3x3()@Vector(ax)).normalized();xs=[v.dot(d) for v in points];axes.append(max(xs)-min(xs))
 edge=collections.Counter();signed=0
 for t in ts:
  for x,y in zip(t,t[1:]+t[:1]):edge[tuple(sorted((x,y)))]+=1
  signed+=verts[t[0]].dot(verts[t[1]].cross(verts[t[2]]))/6
 boundary=[list(e) for e,n in edge.items() if n==1];nonman=[list(e) for e,n in edge.items() if n>2]
 rest=BVHTree.FromPolygons(verts,[t for t in tris if not all(i in ids for i in t)],all_triangles=True)
 samples=points+[(verts[t[0]]+verts[t[1]]+verts[t[2]])/3 for t in ts];visibility={d:0 for d in dirs};seen=set()
 for ix,x in enumerate(samples):
  for key,d in dirs.items():
   if rest.ray_cast(x+d*eps,d,extent*4)[0] is None:visibility[key]+=1;seen.add(ix)
 rec={'tag':tag,'kind':c['kind'],'vertices':len(ids),'triangles':len(ts),'bounds_world_m':{'min':[min(v[k] for v in points) for k in range(3)],'max':[max(v[k] for v in points) for k in range(3)]},'oriented_lengths_m':axes,'raw_boundary_edges':len(boundary),'raw_nonmanifold_edges':len(nonman),'signed_triangle_integral_m3':signed,'vertex_group_matches':o.vertex_groups.get(tag) is not None and {v.index for v in o.data.vertices if any(g.group==o.vertex_groups[tag].index for g in v.groups)}==ids,'all_scene_surface_samples':len(samples),'exposed_samples_any_direction':len(seen),'exposed_samples_by_direction':visibility}
 if boundary:rec['raw_boundary_index_pairs']=boundary
 if c['parent']:
  tree=trees[c['parent']];base=[{'index':i,'inside_parent_3ray_majority':inside(tree,verts[i]),'nearest_distance_m':tree.find_nearest(verts[i])[3]} for i in c['base_vertices']];contact={'child':tag,'parent':c['parent'],'base_vertices':base,'actual_base_contact':any(x['inside_parent_3ray_majority'] or x['nearest_distance_m']<=eps for x in base)};contacts.append(contact)
 out.append(rec)
col=next(c for c in bpy.data.collections if c.get('asset_root'));sa=audit_source(col,max_triangles=14000);ga=audit_glb(gh,max_triangles=14000,max_materials=6,max_primitives=30);compare=compare_source_audit(sa,ga,hashlib.sha256(src.read_bytes()).hexdigest(),hashlib.sha256(gh.read_bytes()).hexdigest());compare.update(source_audit=sa,glb_audit=ga)
(Q/(a+'-source-export.json')).write_text(json.dumps(compare,indent=2)+'\n')
report={'asset_id':a,'revision':r,'pid':os.getpid(),'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(gh.read_bytes()).hexdigest(),'source_saved':False,'source_mutated':False,'world_matrix':[list(row) for row in o.matrix_world],'declared_vertices':len(allids),'unique_declared_vertices':len(set(allids)),'actual_vertices':len(verts),'unassigned_vertices':sorted(set(range(len(verts)))-set(allids)),'components':out,'contacts':contacts,'contract':contract,'hard_organ_ranges':json.loads((p/'original-brief.json').read_text())['hard_organ_ranges'],'methods':{'contacts':'Every actual base vertex ray parity inside assigned closed parent using three oblique rays, majority vote; exact near-surface epsilon allowed. No fitted/config points.','exposure':'Every actual component vertex plus every triangle centroid raycast in eight directions against all OTHER component triangles. Not a screen-space pass gate; pixel inspection separate.','epsilon_m':eps,'topology':'Raw unchanged source triangle index edge use. Signed triangle integral is not called physical volume for open surfaces.'}}
(Q/(a+'-geometry.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'asset_id':a,'source_export':compare['status'],'components':len(out),'boundary_edges':sum(x['raw_boundary_edges'] for x in out),'detached':[x['child'] for x in contacts if not x['actual_base_contact']],'unexposed':[x['tag'] for x in out if not x['exposed_samples_any_direction']],'group_mismatch':[x['tag'] for x in out if not x['vertex_group_matches']]}))

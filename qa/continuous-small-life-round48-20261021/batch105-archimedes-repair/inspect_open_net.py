import bpy,json,pathlib,hashlib,sys,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
Q=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-independent-qa-20261021');D=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-repair-20261021/production/small-life-batch105-archimedes-repair/r002');p=D/'artifacts/archimedes.blend';sha=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False,load_ui=False);ct=json.loads(bpy.data.texts['BATCH105_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];vs=[o.matrix_world@v.co for v in o.data.vertices];o.data.calc_loop_triangles();ts=[tuple(t.vertices) for t in o.data.loop_triangles];tree=BVHTree.FromPolygons(vs,ts,all_triangles=True);frond=next(c for c in ct['components'] if c['kind']=='perforated_frond');ids=set(frond['vertices']);ft=[t for t in ts if set(t)<=ids];fTree=BVHTree.FromPolygons(vs,ft,all_triangles=True);z=Vector((0,0,1));holes=[]
for f in ct['integrated_features']:
 center=sum((vs[i] for i in f['vertices']),Vector())/len(f['vertices']);hit=fTree.ray_cast(center-z*.0003,z,.0006);assert hit[0] is None,f['tag'];holes.append({'tag':f['tag'],'local_vertical_throat_unobstructed':True})
dirs=[Vector(x).normalized() for x in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(.47,-.67,.57),(-.47,.67,.57)]];expo=[]
for c in ct['components']:
 ids=set(c['vertices']);own=[t for t in ts if set(t)<=ids];seen=0;per=[0]*len(dirs)
 for t in own:
  center=sum((vs[i] for i in t),Vector())/3;visible=False
  for j,di in enumerate(dirs):
   if tree.ray_cast(center+di*4.1e-10,di,.13)[0] is None:per[j]+=1;visible=True
  seen+=visible
 assert seen>0;expo.append({'tag':c['tag'],'all_scene_visible_triangle_centroids':seen,'triangles_sampled':len(own),'visible_by_direction':per})
assert len(holes)==300 and hashlib.sha256(p.read_bytes()).hexdigest()==sha
r={'status':'pass','source_sha256':sha,'pid':os.getpid(),'holes':holes,'actual_frond_open_throats':len(holes),'open_throat_method':'A0.6mm local vertical segment through each actual feature-center passes through the original frond without triangle intersection. This tests real thickness openings, not painted masks. Global exposure separately includes every model triangle.','all_scene_exposure':expo,'exposure_method':'Each actual triangle centroid traced in8 directions against all original triangles, including its own component, with numerical ray-origin epsilon4.1e-10m. No exposure-percentage gate imposed. Exact512 and detail pixels personally inspected separately.','source_modified':False};(Q/'open-net-independent.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'pass','real_open_throats':len(holes),'exposure':expo}))

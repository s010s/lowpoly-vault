import bpy,sys,json,hashlib,datetime,math,os
from pathlib import Path
from mathutils.bvhtree import BVHTree
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
o={args[i].lstrip('-'):args[i+1] for i in range(0,len(args),2)}
meshes=[x for x in bpy.context.scene.objects if x.type=='MESH']; parts=[]
for obj in meshes:
 me=obj.data; me.calc_loop_triangles(); vs=[obj.matrix_world@v.co for v in me.vertices]; tris=[tuple(t.vertices) for t in me.loop_triangles]
 tree=BVHTree.FromPolygons(vs,tris,all_triangles=True,epsilon=0.0); pairs=[]
 for a,b in tree.overlap(tree):
  if a>=b or (set(tris[a])&set(tris[b])): continue
  pairs.append((a,b))
 edges={}
 for tri in tris:
  for i in range(3):
   edge=tuple(sorted((tri[i],tri[(i+1)%3])));edges[edge]=edges.get(edge,0)+1
 bad_edges=sum(n!=2 for n in edges.values())
 parts.append({'object':obj.name,'vertices':len(vs),'triangles':len(tris),'boundary_or_nonmanifold_edges':bad_edges,'nonadjacent_intersection_pairs':len(pairs),'examples':[list(x) for x in pairs[:30]]})
r={'asset_id':o['asset'],'revision':o['revision'],'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Fresh Blender 4.3.2 reopen; zero-epsilon BVHTree self-overlap of transformed source triangles, excluding triangle pairs sharing vertex indices; edge-incidence check. This is not a universal zero-volume-intersection policy and is not proof for every possible tolerance.','source_blend':bpy.data.filepath,'source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'final_glb_sha256':hashlib.sha256(Path(o['glb']).read_bytes()).hexdigest(),'parts':parts,'status':'pass' if all(not x['boundary_or_nonmanifold_edges'] and not x['nonadjacent_intersection_pairs'] for x in parts) else 'review'}
Path(o['out']).write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r))

# SPDX-License-Identifier: MIT
"""Read-only saved Blender source inspection, with connected-shell orientation."""
import bpy,bmesh,sys,json,hashlib
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]; source=Path(args[0]).resolve(); output=Path(args[1]).resolve()
bpy.ops.wm.open_mainfile(filepath=str(source))
components=[]; objects=[]; errors=[]
for ob in bpy.context.scene.objects:
 if ob.type!='MESH':continue
 me=ob.data;me.calc_loop_triangles(); adj={i:set() for i in range(len(me.vertices))}
 for edge in me.edges:
  a,b=edge.vertices;adj[a].add(b);adj[b].add(a)
 ids={};n=0
 for v in adj:
  if v in ids:continue
  stack=[v];ids[v]=n
  while stack:
   a=stack.pop()
   for b in adj[a]:
    if b not in ids:ids[b]=n;stack.append(b)
  n+=1
 volumes=[0.0]*n
 for tri in me.loop_triangles:
  a,b,c=[me.vertices[i].co for i in tri.vertices];volumes[ids[tri.vertices[0]]]+=a.dot(b.cross(c))/6
 bad=[{'component':i,'signed_volume_m3':x} for i,x in enumerate(volumes) if x<=0]
 if bad:errors.append({'object':ob.name,'nonpositive_shells':bad})
 bm=bmesh.new();bm.from_mesh(me);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold and not e.is_boundary for e in bm.edges);bm.free()
 if boundary or nonmanifold:errors.append({'object':ob.name,'boundary':boundary,'nonmanifold':nonmanifold})
 objects.append({'name':ob.name,'connected_closed_shells':n,'all_shell_signed_volumes_positive':not bad,'minimum_shell_volume_m3':min(volumes),'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'vertex_groups':[g.name for g in ob.vertex_groups],'transform_identity':all(abs(ob.matrix_world[i][j]-(1 if i==j else 0))<1e-6 for i in range(4) for j in range(4))})
nonasset=[o.name for o in bpy.context.scene.objects if o.type not in {'MESH','EMPTY'}]
if nonasset:errors.append({'non_asset_objects':nonasset})
images=[im.name for im in bpy.data.images if im.type!='RENDER_RESULT']
if images:errors.append({'unexpected_images':images})
r={'status':'PASS' if not errors else 'FAIL','blend_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'python_version':sys.version,'objects':objects,'errors':errors,'external_images':images,'non_asset_objects':nonasset,'inspection_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Saved source reopened. Closed shells and signed-volume orientation checked, not a proof of no self intersections or boolean union. Anatomical shell overlap is intentional.'}
output.parent.mkdir(exist_ok=True,parents=True);output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if errors:raise RuntimeError('Source inspection failed')
